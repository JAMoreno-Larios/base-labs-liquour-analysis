"""
report_claude.py

Similar to report.py in the sense we generate a report for Annie
using the data we analyzed with analysis.py, but this time, we
generate the top three actionable suggestions using a LLM,
in this case, a Claude model.

For this implementation, we will be using Langchain as our framework

J. A. Moreno
"""

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from mdutils.mdutils import MdUtils
from dotenv import load_dotenv
from pydantic import BaseModel, Field

if __package__:
    from .config import Config
    from . import analysis
else:
    from config import Config
    import analysis

# Load environmental variables
load_dotenv()


# Define structured output for LLM
class ActionableInsights(BaseModel):
    """Actionable insights for our analysis"""
    actionables: str = Field(description="The markdown-formatted actionable insights derived from the input data")


def set_up_llm():
    # Initialize base model
    llm = ChatAnthropic(
        model="claude-haiku-4-5-20251001",  # Budget choice for this task
        temperature=0.0,  # We want answers to be more deterministic
    )
    # Add structured output
    llm_with_structure = llm.with_structured_output(ActionableInsights,
                                                    strict=True,
                                                    method="json_schema"
                                                    )
    return llm_with_structure
    

# Auxiliary functions to generate pandas views from SQL queries
def generate_brand_tables():
    """Generate brand-based tables"""
    cogs_brand = analysis.calculate_cogs_per_brand()
    summary_brand = analysis.calculate_brand_profits_margins(cogs_brand)
    top_profit = summary_brand[
        ["Brand", "Description", "total_revenue", "cogs", "profit", "margin"]
    ].nlargest(10, "profit")
    top_margin_naive = summary_brand[
        ["Brand", "Description", "total_revenue", "cogs", "profit", "margin"]
    ].nlargest(10, "margin")
    top_margin_filtered = summary_brand[summary_brand["cogs"] > 0]
    top_margin_filtered = top_margin_filtered[
        ["Brand", "Description", "total_revenue", "cogs", "profit", "margin"]
    ].nlargest(10, "margin")
    losing_brands = summary_brand[summary_brand["profit"] < 0].sort_values("profit")
    losing_brands = losing_brands[
            ["Brand", "Description", "total_revenue", "cogs", "profit", "margin"]
        ]
    return (top_profit, top_margin_naive, top_margin_filtered, losing_brands)

def generate_vendor_tables():
    """Generate vendor-based tables"""
    cogs_vendor = analysis.calculate_cogs_per_vendor()
    summary_vendor = analysis.calculate_vendor_profits_margins(cogs_vendor)

    top_profit_vendor = summary_vendor[
        ["VendorNumber", "VendorName", "total_revenue", "cogs", "profit", "margin"]
    ].nlargest(10, "profit")
    top_margin_vendor_naive = summary_vendor[
        ["VendorNumber", "VendorName", "total_revenue", "cogs", "profit", "margin"]
    ].nlargest(10, "margin")
    top_margin_vendor_filtered = summary_vendor[summary_vendor["cogs"] > 0]
    top_margin_vendor_filtered = top_margin_vendor_filtered[
        ["VendorNumber", "VendorName", "total_revenue", "cogs", "profit", "margin"]
    ].nlargest(10, "margin")
    losing_vendors = summary_vendor[summary_vendor["profit"] < 0].sort_values("profit")
    losing_vendors = losing_vendors[
        ["VendorNumber", "VendorName", "total_revenue", "cogs", "profit", "margin"]
    ]
    return (top_profit_vendor, top_margin_vendor_naive,
            top_margin_vendor_filtered, losing_vendors)


def generate_template() -> ChatPromptTemplate:
    """Forms the chat template that will be passed to the LLM"""

    # Define system prompt
    system_prompt = """
# Role
You are an expert business analyst working in the liquour and spirits market.
You will receive tabular data and will provide a paragraph with actionable
insights for Annie, the owner of a wholesale liquor business,
in a professional and consice manner.
Your output must be markdown, using H2 headers or smaller.
The answers must be grounded in the provided data.
"""

    # Define user prompt
    user_prompt = """
    # Data
    ## Brand-based data
    ### Top 10 profit
    {brand_profit}
    ### Top 10 margin
    {brand_margin_naive}
    ### Top 10 margin, filtered
    {brand_margin_filtered}
    ### Losing brands
    {brand_loses}
    ## Vendor-based data
    ### Top 10 profit
    {vendor_profit}
    ### Top 10 margin
    {vendor_margin_naive}
    ### Top 10 margin, filtered
    {vendor_margin_filtered}
    ### Losing vendors
    {vendor_loses}
    # To do
    Generate the top three actionable insights to improve business
    efficiency and increase profits (i. e. dropping losing brands/vendors,
    negotiating new prices) based on the brand and vendor
    data provided above.
    """

    # Generate chat prompt
    template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", user_prompt)
    ])

    # Return template
    return template


def generate_report():

    # Generate data
    brand_data = generate_brand_tables()
    vendor_data = generate_vendor_tables()

    # Instantiate the LLM
    llm = set_up_llm()

    # Instantiate the template
    template = generate_template()

    # Prepare chat template keyword arguments to fill the variables
    llm_variables = {
        "brand_profit": brand_data[0],
        "brand_margin_naive": brand_data[1],
        "brand_margin_filtered": brand_data[2],
        "brand_loses": brand_data[3],
        "vendor_profit": vendor_data[0],
        "vendor_margin_naive": vendor_data[1],
        "vendor_margin_filtered": vendor_data[2],
        "vendor_loses": vendor_data[3]
    }

    # Add data to template
    template.format_messages(**llm_variables)

    # Print to console
    print(template.pretty_print())

    # Run the LLM
    response = llm.invoke(template)

    # Start building the document

    mdFile = MdUtils(
        file_name=str(Config.REPORT_PATH / "report_llm.md"),
        title="Annie's Magic Numbers Code Challenge - LLM insights",
    )
    mdFile.author = "José Agustín Moreno"

    mdFile.new_header(level=1, title="Introduction")
    mdFile.new_paragraph(
        """
    The requirements for this report are to find out the following:
        """
    )
    mdFile.new_list(
        items=[
            "Top 10 brands based on profits and margins",
            "Top 10 vendors based on profits and margins",
            "Which brands and vendors to drop due loses.",
        ]
    )
    mdFile.new_paragraph("""
    For this analysis, we will calculate the profits using the Cost Of Goods Sold (COGS) metric. In this way we can determine our best-selling brands and vendors.
    
    From our SQL database exploration (refer to `notebooks/sql_columns_exploration.ipynb`), we do need to calculate two different COGS metrics: the full equation for the per-brand metrics, and a purchases-only COGS for the per-vendor one since the inventory tables do not contain vendor-specific information.
    
    The full accounting COGS formula is:
    $$COGS = Initial Inventory Value + Purchases + Freight Costs - Final Inventory Value$$
    
    Then, the profit is:
    $$Profit = Revenue - COGS$$
    
    Thus, the margins are:
    $$Margins = (Revenue - COGS) / Revenue * 100 [%]$$
    
    We'll explain a bit more in the following sections.
        """)

    ### BRANDS
    mdFile.new_header(level=1, title="Top 10 brands")

    mdFile.new_paragraph(
        """
    Freight costs are considered as a per-invoice basis, the data on the sales and purchases tables are shown as per-store.
    We will aggregate this information into a per-brand basis so we can account for a proportional freight allocation for
    the COGS calculation.
    
    From exploring the SQL tables, we identified that the brand refers to a single product type.
    """
    )
    # Calculate
    cogs_brand = analysis.calculate_cogs_per_brand()
    summary_brand = analysis.calculate_brand_profits_margins(cogs_brand)

    mdFile.new_header(level=2, title="Per profits")
    top_profit = summary_brand[
        ["Brand", "Description", "total_revenue", "cogs", "profit", "margin"]
    ].nlargest(10, "profit")
    mdFile.new_paragraph(top_profit.to_markdown(index=False, **Config.TABULATE_BRAND_KWARGS))
    mdFile.new_line("\n")

    mdFile.new_header(level=2, title="Per margins")
    mdFile.new_header(level=3, title="Naive run - no purchases done in the period")
    top_margin_naive = summary_brand[
        ["Brand", "Description", "total_revenue", "cogs", "profit", "margin"]
    ].nlargest(10, "margin")
    mdFile.new_paragraph(top_margin_naive.to_markdown(index=False, **Config.TABULATE_BRAND_KWARGS))
    mdFile.new_line("\n")

    mdFile.new_header(level=3, title="Considering if brand was ordered in the period")
    top_margin_filtered = summary_brand[summary_brand["cogs"] > 0]
    top_margin_filtered = top_margin_filtered[
        ["Brand", "Description", "total_revenue", "cogs", "profit", "margin"]
    ].nlargest(10, "margin")
    mdFile.new_paragraph(top_margin_filtered.to_markdown(index=False, **Config.TABULATE_BRAND_KWARGS))
    mdFile.new_line("\n")

    mdFile.new_header(level=2, title="Losing brands")

    losing_brands = summary_brand[summary_brand["profit"] < 0].sort_values("profit")
    mdFile.new_paragraph(
        losing_brands[
            ["Brand", "Description", "total_revenue", "cogs", "profit", "margin"]
        ]
        .head(20)
        .to_markdown(index=False, **Config.TABULATE_BRAND_KWARGS)
    )
    mdFile.new_line("\n")

    # Brand results
    mdFile.new_header(level=2, title="Brand Analysis - Key Results")

    mdFile.new_header(
        level=3, title="High Vodka and Whiskey sales drive most of the profit"
    )

    mdFile.new_paragraph(
        """
    Most of the profits are driven by high-volume sales, which are reflected on the first table.
    From it, we can see that four Vodka brands and three Whiskey bands dominate the leaderboard.
        """
    )

    mdFile.new_header(level=3, title="'100%' margins are inventory runoff")

    mdFile.new_paragraph(
        """
    Brands that have 100% margin over this period are because no purchases were made.
    Sales were made from existing stock, which means that these margins are an data artifact.
        """
    )

    mdFile.new_header(level=3, title="High margins correspond to low-volume items")

    mdFile.new_paragraph(
        """
    Brands with 90%+ margins correspond to tiny revenue scales. This is caused by existing inventory with minimal restocking.
    These products are not scalable profit drivers.
        """
    )

    mdFile.new_header(level=3, title="Losing brands reflect a change in consumer taste")

    mdFile.new_paragraph(
        """
    Most of the losing brands in the period are wines with high COGS, suggesting that Annie's may have
    overprovisioned the stock for the season.
    We'd recommend to not order new stock on the losing brands until their COGS value gets lower in future months.
        """
    )

    ### Vendor-based

    mdFile.new_header(level=1, title="Top 10 brands")

    mdFile.new_paragraph(
        """
    Since both beggining and end inventory tables do not have information regarding the vendor, we cannot use the
    full accounting formula.
    Instead we use the purchase-based COGS:
        COGS_vendor = Purchases_vendor + Freight_vendor
    """
    )
    # Calculate

    cogs_vendor = analysis.calculate_cogs_per_vendor()
    summary_vendor = analysis.calculate_vendor_profits_margins(cogs_vendor)

    mdFile.new_header(level=2, title="Per profits")
    top_profit_vendor = summary_vendor[
        ["VendorNumber", "VendorName", "total_revenue", "cogs", "profit", "margin"]
    ].nlargest(10, "profit")

    mdFile.new_paragraph(top_profit_vendor.to_markdown(index=False, **Config.TABULATE_VENDOR_KWARGS))
    mdFile.new_line("\n")

    mdFile.new_header(level=2, title="Per margins")
    mdFile.new_header(level=3, title="Naive run - no purchases done in the period")

    top_margin_vendor_naive = summary_vendor[
        ["VendorNumber", "VendorName", "total_revenue", "cogs", "profit", "margin"]
    ].nlargest(10, "margin")
    mdFile.new_paragraph(top_margin_vendor_naive.to_markdown(index=False, **Config.TABULATE_VENDOR_KWARGS))
    mdFile.new_line("\n")

    mdFile.new_header(
        level=3, title="Considering if we ordered from a given vendor during the period"
    )

    top_margin_vendor_filtered = summary_vendor[summary_vendor["cogs"] > 0]
    top_margin_vendor_filtered = top_margin_vendor_filtered[
        ["VendorNumber", "VendorName", "total_revenue", "cogs", "profit", "margin"]
    ].nlargest(10, "margin")

    mdFile.new_paragraph(top_margin_vendor_filtered.to_markdown(index=False, **Config.TABULATE_VENDOR_KWARGS))
    mdFile.new_line("\n")

    mdFile.new_header(level=2, title="Losing Vendors")

    losing_vendors = summary_vendor[summary_vendor["profit"] < 0].sort_values("profit")
    mdFile.new_paragraph(
        losing_vendors[
            ["VendorNumber", "VendorName", "total_revenue", "cogs", "profit", "margin"]
        ]
        .head(20)
        .to_markdown(index=False, **Config.TABULATE_VENDOR_KWARGS)
    )
    mdFile.new_line("\n")

    # Vendor results
    mdFile.new_header(level=2, title="Vendor Analysis - Key Results")

    mdFile.new_header(level=3, title="Diageo and Martignetti dominate profits")

    profit_share = (
        (top_profit_vendor["profit"].iloc[0] + top_profit_vendor["profit"].iloc[1])
        / top_profit_vendor["profit"].sum()
        * 100
    )
    mdFile.new_paragraph(f"""
    Diageo North America generates 17.5 million in profit; Martignetti Companies, 13.1 million.
    These two companies represent the {profit_share}% of the top 10 earners.
    """)

    mdFile.new_header(level=3, title="Losing vendors are small contributors")

    mdFile.new_paragraph(f"""
    All losing vendors are small producers with revenue under 70k. The only company worth reviewing are
    Adamba Imports (67.6k revenue, -9.6k loss).
    """)

    mdFile.new_header(level=3, title="No major vendor relationships need termination")

    mdFile.new_paragraph(f"""
    All 10 profit-driving vendors are healthy. Losing vendor losses can be either ignored or fixed through pricing.
    """)

    # Generate the file
    mdFile.create_md_file()


if __name__ == "__main__":
    generate_report()

"""
report.py

Here we will write the requested report for Annie.

J. A. Moreno
"""

from mdutils.mdutils import MdUtils
import analysis
from config import Config

mdFile = MdUtils(file_name=str(Config.REPORT_PATH/'report.md'),
                 title="Annie's Magic Numbers Code Challenge")
mdFile.author = "José Agustín Moreno"

mdFile.new_header(level=1, title="Annie's Magic Numbers")
mdFile.new_paragraph(
    """
The requirements for this report are to find out the following:
    """
)
mdFile.new_list(items=["Top 10 brands based on profits and margins",
                       "Top 10 vendors based on profits and margins",
                       "Which brands and vendors to drop due loses."])
mdFile.new_paragraph("""
For this analysis, we will calculate the profits using the Cost Of Goods Sold (COGS) metric. In this way we can determine our best-selling brands and vendors.

From our SQL database exploration (refer to `notebooks/sql_columns_exploration.ipynb`), we do need to calculate two different COGS metrics: the full equation for the per-brand metrics, and a purchases-only COGS for the per-vendor one since the inventory tables do not contain vendor-specific information.

The full accounting COGS formula is:
$COGS = Initial Inventory Value + Purchases + Freight Costs - Final Inventory Value$

Then, the profit is:
$Profit = Revenue - COGS$

Thus, the margins are:
$Margins = (Revenue - COGS) / Revenue * 100 [%]$

We'll explain a bit more in the following sections.
    """)

mdFile.new_header(level=2, title="Top 10 brands")

mdFile.new_paragraph(
"""
Freight costs are considered as a per-invoice basis, the data on the sales and purchases tables are shown as per-store.
We will aggregate this information into a per-brand basis so we can account for a proportional freight allocation for the COGS calculation

From exploring the SQL tables, we identified that the brand refers to a single product type.
""")
# Calculate
cogs_brand = analysis.calculate_cogs_per_brand()
summary_cogs = analysis.calculate_brand_profits_margins(cogs_brand)

mdFile.new_header(level=3, title="Per profits")
mdFile.new_paragraph(
    summary_cogs[["Brand", "Description", "profit"]]
    .nlargest(10, "profit")
    .to_markdown(index=False))

mdFile.new_header(level=3, title="Per margins")
mdFile.new_paragraph(
    summary_cogs[["Brand", "Description", "margin"]]
    .nlargest(10, "margin")
    .to_markdown(index=False))

# Generate the file
mdFile.create_md_file()

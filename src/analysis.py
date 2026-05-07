"""
analysis.py

From the SQL database we will:
    - Figure out the profits, margins per item and per brand
    - Provide insights on best and worst products

J. A. Moreno
"""

import sqlalchemy as sa
from config import Config
import pandas as pd
import numpy as np

# Create engine
engine = sa.create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False)

def calculate_cogs_per_brand() -> pd.DataFrame:
    """
    Calculate the Cost Of Sold Goods based on inventory and purchases.

    Freight costs are considered as a per-invoice basis, the data on the
    sales and purchases tables are shown as per-store.
    We will aggregate this information into a per-brand basis so we can
    account for a proportional freight allocation for the COGS calculation

    From exploring the SQL tables, we can assume that the
    brand refers to a single product type.
    """
    
    # Get initial inventory value per brand
    initial_inventory = pd.read_sql("""
        SELECT Brand,
        Description,
        SUM(onHand * Price) as beg_inv_value
        FROM BegInvDec
        GROUP BY Brand, Description
    """, engine)
    
    # Calculate the ending inventory value per brand
    ending_inventory = pd.read_sql("""
        SELECT Brand,
        Description,
        SUM(onHand * Price) as end_inv_value
        FROM EndInvDec
        GROUP BY Brand, Description
    """, engine)

    # Calculate the purchases done per brand
    purchases = pd.read_sql("""
        SELECT Brand,
        Description,
        SUM(Dollars) as total_purchases
        FROM PurchasesDec
        GROUP BY Brand, Description
    """, engine)

    # Calculate the freight cost per brand
    # Total freight cost across all invoices
    total_freight = pd.read_sql(
        "SELECT SUM(Freight) AS total_freight FROM VendorInvoicesDec",
        engine).iloc[0]["total_freight"]
    # We will take the brand's proportional freight share from the total
    # freight costs
    freight_allocation = purchases.copy()
    total_purchases = freight_allocation["total_purchases"].sum()
    # Figure out if we did purchase items for a given brand, if so,
    # calculate the brand's proportional freight cost.
    freight_allocation["freight_allocation"] = np.where(
        total_purchases > 0,
        (freight_allocation["total_purchases"] / total_purchases) * total_freight,
        0.0
    )

    # Merge dataframes, use union of keys for each pair of frames
    # Merge initial with ending
    cogs = initial_inventory.merge(ending_inventory, how="outer", on=["Brand", "Description"])
    # Merge with purchases
    cogs = cogs.merge(purchases, how="outer", on=["Brand", "Description"])
    # Merge with freight allocation
    cogs = cogs.merge(
        freight_allocation[["Brand", "Description", "freight_allocation"]],
        how="outer",
        on=["Brand", "Description"]
    )

    # If there are NaNs, fill with zeros
    cogs = cogs.fillna(0)

    # Calculate the Cost of Goods Sold
    cogs["cogs"] = (
        cogs["beg_inv_value"]
        + cogs["total_purchases"]
        + cogs["freight_allocation"]
        - cogs["end_inv_value"]
    )

    # Return completed dataframe
    return cogs[["Brand", "Description", "beg_inv_value", "total_purchases",
                 "freight_allocation", "end_inv_value",
                 "cogs"]]


def calculate_cogs_per_vendor() -> pd.DataFrame:
    """
    Calculate the Cost Of Sold Goods based on inventory and purchases
    in a per-vendor basis.
    Since both beggining and end inventory tables do not have
    information regarding the vendor, we cannot use the full
    accounting formula. Instead we use the purchase-based COGS:
    COGS_vendor = Purchases_vendor + Freight_vendor
    """
    

    # Calculate the purchases done per brand
    purchases = pd.read_sql("""
        SELECT VendorNumber,
        SUM(Dollars) as total_purchases
        FROM PurchasesDec
        GROUP BY VendorNumber
    """, engine)

    # Calculate the freight cost per vendor
    freight = pd.read_sql("""
        SELECT
            VendorNumber,
            SUM(Freight) as total_freight
        FROM VendorInvoicesDec
        GROUP BY VendorNumber
    """, engine)

    # Merge dataframes, use union of keys for each pair of frames
    cogs = purchases.merge(freight, how="outer", on="VendorNumber")

    # If there are NaNs, fill with zeros
    cogs = cogs.fillna(0)

    # Calculate the Cost of Goods Sold
    cogs["cogs"] = cogs["total_purchases"] + cogs["total_freight"]

    # Return completed dataframe
    return cogs[["VendorNumber", "total_purchases",
                 "total_freight", "cogs"]]


def calculate_brand_profits_margins(cogs_brand: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the profits and margins in a per-brand basis using
    a previously calculated COGS.
    The Profit is calculated as Revenue - COGS,
    the margins as (Revenue - COGS) / Revenue
    """

    # Aggregate revenue by brand
    revenue = pd.read_sql("""
        SELECT
            Brand,
            Description,
            SUM(SalesDollars) AS total_revenue,
            SUM(SalesQuantity) AS total_units
            FROM SalesDec
            GROUP BY Brand, Description
    """, engine)

    # Merge revenue and COGS into a new data frame, do calculations
    summary = revenue.merge(cogs_brand, how="left", on=["Brand", "Description"])
    summary["cogs"] = summary["cogs"].fillna(0)  # Replace NaNs with zero

    # Calculate profit and margin
    summary["profit"] = summary["total_revenue"] - summary["cogs"]
    summary["margin"] = np.where(
        summary["total_revenue"] > 0,
        summary["profit"] / summary["total_revenue"] * 100,
        np.nan
    )
    # Return final results
    return summary


def calculate_vendor_profits_margins(cogs_vendor: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the profits and margins in a per-vendor basis using
    a previously calculated COGS.
    The Profit is calculated as Revenue - COGS,
    the margins as (Revenue - COGS) / Revenue
    """

    # Aggregate revenue by brand
    revenue = pd.read_sql("""
        SELECT
            VendorNo as VendorNumber,
            SUM(SalesDollars) AS total_revenue,
            SUM(SalesQuantity) AS total_units
            FROM SalesDec
            GROUP BY VendorNumber
    """, engine)

    # Merge revenue and COGS into a new data frame, do calculations
    summary = revenue.merge(cogs_vendor, how="left", on="VendorNumber")
    summary["cogs"] = summary["cogs"].fillna(0)  # Replace NaNs with zero

    # Calculate profit and margin
    summary["profit"] = summary["total_revenue"] - summary["cogs"]
    summary["margin"] = np.where(
        summary["total_revenue"] > 0,
        summary["profit"] / summary["total_revenue"] * 100,
        np.nan
    )
    # Return final results
    return summary


if __name__ == "__main__":
    # Run
    cogs_brand = calculate_cogs_per_brand()
    print("===COGS===")
    print(cogs_brand.sort_values("cogs", ascending=False).head(5).to_string(index=False))
    print("===PROFITS===")
    summary = calculate_brand_profits_margins(cogs_brand)
    print(summary.nlargest(10, "profit").to_string(index=False))
    print("===MARGINS===")
    print(summary.nlargest(10, "margin").to_string(index=False))
    print("===LOSING BRANDS===")
    losing_brands = summary[summary["profit"] < 0].sort_values("profit")
    print(losing_brands[["Brand", "Description", "total_revenue",
                        "cogs", "profit", "margin"]].head(10)
          .to_string(index=False))

    # Per vendor
#     cogs_vendor = calculate_cogs_per_vendor()
#     print("===COGS PER VENDOR===")
#     print(cogs_vendor.sort_values("cogs", ascending=False).head(5).to_string(index=False))
#     print("===PROFITS===")
#     summary = calculate_vendor_profits_margins(cogs_vendor)
#     print(summary.nlargest(10, "profit").to_string(index=False))
#     print("===MARGINS===")
#     print(summary.nlargest(10, "margin").to_string(index=False))
#     print("===LOSING VENDORS===")
#     losing_vendors = summary[summary["profit"] < 0].sort_values("profit")
#     print(losing_vendors[["VendorNumber", "total_revenue",
#                         "cogs", "profit", "margin"]]
#           .to_string(index=False))

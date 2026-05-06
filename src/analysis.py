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
        SELECT Brand, SUM(onHand * Price) as beg_inv_value
        FROM BegInvDec
        GROUP BY Brand
    """, engine)
    
    # Calculate the ending inventory value per brand
    ending_inventory = pd.read_sql("""
        SELECT Brand, SUM(onHand * Price) as end_inv_value
        FROM EndInvDec
        GROUP BY Brand
    """, engine)

    # Calculate the purchases done per brand
    purchases = pd.read_sql("""
        SELECT Brand,
        SUM(Dollars) as total_purchases
        FROM PurchasesDec
        GROUP BY Brand
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
    cogs = initial_inventory.merge(ending_inventory, how="outer", on="Brand")
    # Merge with purchases
    cogs = cogs.merge(purchases, how="outer", on="Brand")
    # Merge with freight allocation
    cogs = cogs.merge(
        freight_allocation[["Brand", "freight_allocation"]],
        how="outer",
        on="Brand"
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
    return cogs[["Brand", "beg_inv_value", "total_purchases",
                 "freight_allocation", "end_inv_value",
                 "cogs"]]

if __name__ == "__main__":
    # Run
    cogs = calculate_cogs_per_brand()
    print(cogs.sort_values("cogs", ascending=False).head(5).to_string(index=False))

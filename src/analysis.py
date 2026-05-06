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

# Create engine
engine = sa.create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)

def calculate_cogs_per_brand():
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
    initial_inv = pd.read_sql("""
        SELECT Brand, SUM(onHand * Price) as beg_inv_value
        FROM BegInvDec
        GROUP BY Brand
    """, engine)

    # Calculate the purchases done per brand
    purchases = pd.read_sql("""
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

    # Calculate the freight cost per brand
    # We will take the brand's proportional freight share from the total
    # freight costs

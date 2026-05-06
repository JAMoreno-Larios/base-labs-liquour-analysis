"""
ingest.py

Here we will ingeest all raw .CSV files found in data/raw into a
SQLite database using SQLAlchemy as ORM

J. A. Moreno
"""

from pathlib import Path
import pandas as pd
import sqlalchemy as sa
from config import Config

# Create engine
engine = sa.create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)

def ingest_csv(input_path: Path, table_name: str):

    # Read csv into a pandas dataframe
    df = pd.read_csv(input_path)
    df.to_sql(table_name, engine, if_exists='replace', index=False)


if __name__ == "__main__":
    print("Initializing ingestion")
    ingest_csv(Config.RAW_DATA_PATH / 'SalesFINAL12312016.csv',
               'SalesDec')
    ingest_csv(Config.RAW_DATA_PATH / 'PurchasesFINAL12312016.csv',
               'PurchasesDec')
    ingest_csv(Config.RAW_DATA_PATH / 'InvoicePurchases12312016.csv',
               'VendorInvoicesDec')
    ingest_csv(Config.RAW_DATA_PATH / 'EndInvFINAL12312016.csv',
               'EndInvDec')
    ingest_csv(Config.RAW_DATA_PATH / 'BegInvFINAL12312016.csv',
               'BegInvDec')
    ingest_csv(Config.RAW_DATA_PATH / '2017PurchasePricesDec.csv',
               'PricingPurchasesDec')
    print("Ingestion finalized")

"""
gather_data.py

Downloads and extracts the PwC Inventory Analysis Case Study CSV files
from https://www.pwc.com/us/en/careers/university-relations/data-and-analytics-case-studies-files.html

J. A. Moreno
"""

import sys
import urllib.request
import zipfile
from pathlib import Path

from config import Config

# Define the website URL
BASE_URL = (
    "https://www.pwc.com/us/en/careers/"
    "university_relations/data_analytics_cases_studies"
)

# Create a dictionary with ZIP and CSV filename relations
FILES = {
    "PurchasesFINAL12312016csv.zip": "PurchasesFINAL12312016.csv",
    "BegInvFINAL12312016csv.zip": "BegInvFINAL12312016.csv",
    "2017PurchasePricesDeccsv.zip": "2017PurchasePricesDec.csv",
    "VendorInvoices12312016csv.zip": "InvoicePurchases12312016.csv",
    "EndInvFINAL12312016csv.zip": "EndInvFINAL12312016.csv",
    "SalesFINAL12312016csv.zip": "SalesFINAL12312016.csv",
}

def download_extract(zip_name: str,
                     csv_name: str,
                     target_dir: Path) -> None:

    # Download the zip file
    url = f"{BASE_URL}/{zip_name}"
    zip_path = target_dir / zip_name
    print(f"Downloading {zip_name}...")
    try:
        urllib.request.urlretrieve(url, zip_path)
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        sys.exit(1)  # Exit on error

    print(f"Extracting {csv_name}...")
    with zipfile.ZipFile(zip_path) as zf:
        zf.extract(csv_name, target_dir)
    zip_path.unlink()  # Remove the zip file from disk
    print(f"Done: {csv_name}")


if __name__ == "__main__":
    target = Config.RAW_DATA_PATH
    target.mkdir(parents=True, exist_ok=True) # Attempt to create directory if missing

    # Download, unzip, extract, and clean
    for zip_name, csv_name in FILES.items():
        download_extract(zip_name, csv_name, target)

    print("All files were downloaded and extracted successfully.")


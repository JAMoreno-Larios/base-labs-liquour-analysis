"""
run_pipeline.py

This is the entry point for our analysis.
We perform data gathering, ingestion, analysis and reporting.
The user should not need to do anything extra.

J. A. Moreno
"""

import argparse
from src import gather_data, ingest, report, report_claude
from src.config import Config

def gather():
    print("Gathering data")
    target = Config.RAW_DATA_PATH
    target.mkdir(parents=True, exist_ok=True) # Attempt to create directory if missing

    # Download, unzip, extract, and clean
    for zip_name, csv_name in gather_data.FILES.items():
        gather_data.download_extract(zip_name, csv_name, target)

    print("All files were downloaded and extracted successfully.")

def ingestion():
    print("Ingesting data into SQLite")
    ingest.ingest_csv(Config.RAW_DATA_PATH / 'SalesFINAL12312016.csv',
                      'SalesDec')
    ingest.ingest_csv(Config.RAW_DATA_PATH / 'PurchasesFINAL12312016.csv',
                      'PurchasesDec')
    ingest.ingest_csv(Config.RAW_DATA_PATH / 'InvoicePurchases12312016.csv',
                      'VendorInvoicesDec')
    ingest.ingest_csv(Config.RAW_DATA_PATH / 'EndInvFINAL12312016.csv',
                      'EndInvDec')
    ingest.ingest_csv(Config.RAW_DATA_PATH / 'BegInvFINAL12312016.csv',
                      'BegInvDec')
    ingest.ingest_csv(Config.RAW_DATA_PATH / '2017PurchasePricesDec.csv',
                      'PricingPurchasesDec')
    print("Ingestion complete")


def analyze_and_report():
    print("Running analysis + reporting")
    report.generate_report()
    print("Report generated in ./reports/report.md")

def analyze_and_report_llm():
    print("Running analysis + reporting with LLM support")
    report_claude.generate_report()
    print("Report generated in ./reports/report_llm.md")


def main():
    parser = argparse.ArgumentParser(description="Run the full Annie's analysis pipeline")
    parser.add_argument("--skip-gathering", action="store_true", help="Skip data download")
    parser.add_argument("--skip-ingest", action="store_true", help="Skip CSV ingestion")
    parser.add_argument("--skip-analysis", action="store_true", help="Skip analysis and reporting")
    parser.add_argument("--no-llm-analysis", action="store_true", help="Do not use the LLM-based analysis and reporting")
    args = parser.parse_args()

    if not args.skip_gathering:
        gather()
    if not args.skip_ingest:
        ingestion()
    if not args.skip_analysis:
        if args.no_llm_analysis:
            analyze_and_report()
        else:
            analyze_and_report_llm()

    print("Pipeline finished successfully")

if __name__ == "__main__":
    main()

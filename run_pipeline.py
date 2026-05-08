"""
run_pipeline.py

This is the entry point for our analysis.
We perform data gathering, ingestion, analysis and reporting.
The user should not need to do anything extra.

J. A. Moreno
"""

import argparse
import sys
from pathlib import Path
from src import gather_data, ingest, analysis, report
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

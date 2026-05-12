"""
config.py

Configuration file for our project
J. A. Moreno
"""

from pathlib import Path
from dataclasses import dataclass


basedir = Path(__file__).absolute().parents[1]  # Easier if we know where we are

@dataclass
class Config:
    """
    Data class that hold constants for our project
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(basedir) + '/data/store.db'
    RAW_DATA_PATH = basedir / 'data/raw'
    REPORT_PATH = basedir / 'reports'

    TABULATE_BRAND_KWARGS = {
                       "tablefmt": "github",
                        "headers": ["Brand", "Description", "Total Revenue [USD]", 
                                  "COGS [USD]", "Profit [USD]", "Margin [%]"],
        "floatfmt": ("10,.2f", "10,.2f", "10,.2f",
                                   "10,.2f", "10,.2f", "10,.2f"),
                       }
    TABULATE_VENDOR_KWARGS = {
                       "tablefmt": "github",
                        "headers": ["Vendor ID", "Vendor Name", "Total Revenue [USD]", 
                                               "Purchase COGS [USD]", "Profit [USD]", "Margin [%]"],
                        "floatfmt": ("10,.2f", "10,.2f", "10,.2f",
                                     "10,.2f", "10,.2f", "10,.2f"),
                       }

    def __class_getitem__(cls, item):
        # Makes our class subscriptable
        return getattr(cls, item)

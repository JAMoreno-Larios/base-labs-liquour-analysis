"""
config.py

Configuration file for our project
J. A. Moreno
"""

from pathlib import Path
from dataclasses import dataclass


basedir = Path(__file__).absolute()  # Easier if we know where we are

@dataclass
class Config:
    """
    Data class that hold constants for our project
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(basedir) + '/data/store.db'

    def __class_getitem__(cls, item):
        # Makes our class subscriptable
        return getattr(cls, item)

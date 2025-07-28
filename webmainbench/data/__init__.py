"""
Data module for WebMainBench.

This module handles loading, saving and managing benchmark datasets.
"""

from .dataset import BenchmarkDataset, DataSample
from .loader import DataLoader
from .saver import DataSaver

__all__ = [
    "BenchmarkDataset",
    "DataSample", 
    "DataLoader",
    "DataSaver",
] 
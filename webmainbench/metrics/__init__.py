"""
Metrics module for WebMainBench.

This module provides various evaluation metrics for web content extraction.
"""

from .base import BaseMetric, MetricResult
from .text_metrics import EditDistanceMetric, BLEUMetric, ROUGEMetric
from .table_metrics import TableExtractionMetric
from .formula_metrics import FormulaExtractionMetric
from .structure_metrics import StructureMetric
from .teds_metrics import TEDSMetric, StructureTEDSMetric
from .calculator import MetricCalculator

__all__ = [
    "BaseMetric",
    "MetricResult",
    "EditDistanceMetric",
    "BLEUMetric", 
    "ROUGEMetric",
    "TableExtractionMetric",
    "FormulaExtractionMetric",
    "StructureMetric",
    "TEDSMetric",
    "StructureTEDSMetric",
    "MetricCalculator",
] 
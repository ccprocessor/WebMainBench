"""
WebMainBench: A comprehensive benchmark for web main content extraction.

This package provides a standardized evaluation framework for comparing
different web content extraction tools and methods.
"""

__version__ = "0.1.0"
__author__ = "WebMainBench Team"

from .data import DataLoader, DataSaver, BenchmarkDataset, DataSample
from .extractors import BaseExtractor, ExtractorFactory, ExtractionResult
from .metrics import BaseMetric, MetricCalculator, MetricResult
from .evaluator import Evaluator, EvaluationResult
from .utils import setup_logging, format_results

__all__ = [
    "DataLoader",
    "DataSaver", 
    "BenchmarkDataset",
    "DataSample",
    "BaseExtractor",
    "ExtractorFactory",
    "ExtractionResult",
    "BaseMetric",
    "MetricCalculator",
    "MetricResult",
    "Evaluator",
    "EvaluationResult",
    "setup_logging",
    "format_results",
] 
"""
Extractors module for WebMainBench.

This module provides interfaces and implementations for various web content extractors.
"""

from .base import BaseExtractor, ExtractionResult
from .factory import ExtractorFactory
from .llm_webkit_extractor import LlmWebkitExtractor
from .jina_extractor import JinaExtractor

__all__ = [
    "BaseExtractor",
    "ExtractionResult",
    "ExtractorFactory",
    "LlmWebkitExtractor",
    "JinaExtractor",
] 
"""
Extractors module for WebMainBench.

This module provides interfaces and implementations for various web content extractors.
"""

from .base import BaseExtractor, ExtractionResult
from .factory import ExtractorFactory
from .llm_webkit_extractor import LlmWebkitExtractor
from .jina_extractor import JinaExtractor
from .test_model_extractor import TestModelExtractor
from .trafilatura_extractor import TrafilaturaExtractor
from .resiliparse_extractor import ResiliparseExtractor
from .magic_html_extractor import MagicHtmlExtractor



__all__ = [
    "BaseExtractor",
    "ExtractionResult",
    "ExtractorFactory",
    "LlmWebkitExtractor",
    "JinaExtractor",
    "TestModelExtractor",
    "TrafilaturaExtractor",
    "ResiliparseExtractor",
    "MagicHtmlExtractor",
] 
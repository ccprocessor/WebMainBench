"""
Base extractor interface for WebMainBench.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Union
import time
import traceback


@dataclass
class ExtractionResult:
    """Result of content extraction."""
    
    # Core extraction results
    content: str = ""  # Extracted markdown content
    content_list: Optional[List[Dict[str, Any]]] = None  # Structured content list
    version: str = None  # Version of the extractor
    
    # Metadata
    success: bool = True
    extraction_time: float = 0.0  # Time taken in seconds
    error_message: Optional[str] = None
    error_traceback: Optional[str] = None
    
    # Additional extracted information
    title: Optional[str] = None
    author: Optional[str] = None
    publish_date: Optional[str] = None
    language: Optional[str] = None
    
    # Quality indicators
    confidence_score: Optional[float] = None  # 0.0 to 1.0
    
    def __post_init__(self):
        if self.content_list is None:
            self.content_list = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "content": self.content,
            "content_list": self.content_list,
            "success": self.success,
            "extraction_time": self.extraction_time,
            "error_message": self.error_message,
            "error_traceback": self.error_traceback,
            "title": self.title,
            "author": self.author,
            "publish_date": self.publish_date,
            "language": self.language,
            "confidence_score": self.confidence_score,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExtractionResult":
        """Create from dictionary."""
        return cls(**data)
    
    @classmethod
    def create_error_result(cls, error_message: str, 
                          error_traceback: str = None,
                          extraction_time: float = 0.0) -> "ExtractionResult":
        """Create an error result."""
        return cls(
            success=False,
            error_message=error_message,
            error_traceback=error_traceback,
            extraction_time=extraction_time
        )


class BaseExtractor(ABC):
    """Base class for all content extractors."""
    
    def __init__(self, name: str, config: Dict[str, Any] = None):
        """
        Initialize the extractor.
        
        Args:
            name: Name of the extractor
            config: Configuration dictionary
        """
        self.name = name
        self.config = config or {}
        self._setup()
    
    @abstractmethod
    def _setup(self) -> None:
        """Setup the extractor (load models, initialize clients, etc.)."""
        pass
    
    @abstractmethod
    def _extract_content(self, html: str, url: str = None) -> ExtractionResult:
        """
        Extract content from HTML.
        
        Args:
            html: HTML content to extract from
            url: Optional URL of the page
            
        Returns:
            ExtractionResult instance
        """
        
    def extract_from_sample(self, sample: Dict[str, Any]) -> ExtractionResult:
        """
        直接从数据样本（如评测数据集的dict）中读取groundtruth内容，返回ExtractionResult。
        适用于评测流程的基线测试或简单抽取器。

        参数:
            sample: 包含groundtruth内容的数据样本dict

        返回:
            ExtractionResult实例，内容直接取自sample
        """
        # 兼容常见字段
        # 这里直接从sample中获取'llm-webkit_md'字段内容，注意字段名有'-'，不能用点操作符，需要用[]方式
        content = sample.llm_webkit_md
        content_list = sample.content_list
        language = sample.language
        # 置信度直接设为1.0，表示“完美抽取”
        confidence_score = 1.0

        return ExtractionResult(
            content=content,
            content_list=content_list,
            language=language,
            confidence_score=confidence_score,
            success=True
        )
    
    def extract(self, html: str, url: str = None) -> ExtractionResult:
        """
        Extract content with error handling and timing.
        
        Args:
            html: HTML content to extract from
            url: Optional URL of the page
            
        Returns:
            ExtractionResult instance
        """
        start_time = time.time()
        
        try:
            # Validate input
            if not html or not html.strip():
                return ExtractionResult.create_error_result(
                    "Empty HTML input",
                    extraction_time=time.time() - start_time
                )
            
            # Perform extraction
            result = self._extract_content(html, url)
            result.extraction_time = time.time() - start_time
            
            return result
            
        except Exception as e:
            error_message = f"Extraction failed: {str(e)}"
            error_traceback = traceback.format_exc()
            
            return ExtractionResult.create_error_result(
                error_message,
                error_traceback,
                time.time() - start_time
            )
    
    def batch_extract(self, html_list: List[str], 
                     url_list: List[str] = None) -> List[ExtractionResult]:
        """
        Extract content from multiple HTML documents.
        
        Args:
            html_list: List of HTML content
            url_list: Optional list of URLs
            
        Returns:
            List of ExtractionResult instances
        """
        if url_list is None:
            url_list = [None] * len(html_list)
        
        results = []
        for html, url in zip(html_list, url_list):
            result = self.extract(html, url)
            results.append(result)
        
        return results
    
    def get_config(self) -> Dict[str, Any]:
        """Get extractor configuration."""
        return self.config.copy()
    
    def set_config(self, config: Dict[str, Any]) -> None:
        """Update extractor configuration."""
        self.config.update(config)
    
    def get_info(self) -> Dict[str, Any]:
        """Get extractor information."""
        return {
            "name": self.name,
            "config": self.get_config(),
            "version": getattr(self, 'version', 'unknown'),
            "description": getattr(self, 'description', ''),
        }
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
    
    def __repr__(self) -> str:
        return self.__str__() 
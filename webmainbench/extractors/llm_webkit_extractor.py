"""
LLM-WebKit extractor implementation.
"""

from typing import Dict, Any, Optional
from .base import BaseExtractor, ExtractionResult
from .factory import extractor


@extractor("llm-webkit")
class LlmWebkitExtractor(BaseExtractor):
    """Extractor using LLM-WebKit."""
    
    version = "1.0.0"
    description = "LLM-WebKit based content extractor"
    
    def _setup(self) -> None:
        """Setup the LLM-WebKit extractor."""
        try:
            # Import llm_web_kit modules
            from llm_web_kit.simple import extract_html
            from llm_web_kit.libs.html_utils import get_cc_select_html
            from lxml.html import fromstring
            
            self._extract_html = extract_html
            self._get_cc_select_html = get_cc_select_html
            self._fromstring = fromstring
            
        except ImportError as e:
            raise RuntimeError(f"Failed to import llm_web_kit: {e}")
    
    def _extract_content(self, html: str, url: str = None) -> ExtractionResult:
        """
        Extract content using LLM-WebKit.
        
        Args:
            html: HTML content to extract from
            url: Optional URL of the page
            
        Returns:
            ExtractionResult instance
        """
        try:
            # Use llm_web_kit for extraction
            result = self._extract_html(html, url=url)
            
            # Extract additional groundtruth if HTML has cc-select annotations
            groundtruth_content = ""
            if "cc-select" in html:
                try:
                    element = self._fromstring(html)
                    cc_selected = self._get_cc_select_html(element)
                    # Convert selected elements to markdown
                    # This would need implementation based on your needs
                    groundtruth_content = self._element_to_markdown(cc_selected)
                except Exception as e:
                    print(f"Warning: Failed to extract cc-select content: {e}")
            
            return ExtractionResult(
                content=result.get('content', ''),
                content_list=result.get('content_list', []),
                title=result.get('title'),
                language=result.get('language'),
                # confidence_score=self._calculate_confidence(result),
                success=True
            )
            
        except Exception as e:
            return ExtractionResult.create_error_result(
                f"LLM-WebKit extraction failed: {str(e)}"
            )
    
    def _element_to_markdown(self, element) -> str:
        """Convert HTML element to markdown (placeholder implementation)."""
        # This is a placeholder - you would implement actual HTML to markdown conversion
        try:
            from llm_web_kit.libs.html_utils import element_to_html
            html_str = element_to_html(element)
            # Here you would convert HTML to markdown
            # For now, just return the HTML
            return html_str
        except:
            return ""
    
    def _calculate_confidence(self, result: Dict[str, Any]) -> float:
        """Calculate extraction confidence score."""
        # Simple confidence calculation based on content length and structure
        content = result.get('content', '')
        content_list = result.get('content_list', [])
        
        if not content:
            return 0.0
        
        # Factor in content length
        length_score = min(len(content) / 1000, 1.0)  # Normalize to 1000 chars
        
        # Factor in structure (content_list)
        structure_score = min(len(content_list) / 10, 1.0)  # Normalize to 10 blocks
        
        # Combine scores
        confidence = (length_score * 0.7 + structure_score * 0.3)
        return min(confidence, 1.0) 
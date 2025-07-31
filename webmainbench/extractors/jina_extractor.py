"""
Jina AI extractor implementation.
"""

from typing import Dict, Any, Optional
import requests
from .base import BaseExtractor, ExtractionResult
from .factory import extractor


@extractor("jina-ai")
class JinaExtractor(BaseExtractor):
    """Extractor using Jina AI Reader API."""
    
    version = "1.0.0"
    description = "Jina AI Reader API based content extractor"
    
    def _setup(self) -> None:
        """Setup the Jina AI extractor."""
        self.api_url = self.config.get('api_url', 'https://r.jina.ai/')
        self.api_key = self.config.get('api_key')
        self.timeout = self.config.get('timeout', 30)
        
        # Setup headers
        self.headers = {'Accept': 'application/json'}
        if self.api_key:
            self.headers['Authorization'] = f'Bearer {self.api_key}'
    
    def _extract_content(self, html: str, url: str = None) -> ExtractionResult:
        """
        Extract content using Jina AI Reader.
        
        Args:
            html: HTML content to extract from
            url: Optional URL of the page
            
        Returns:
            ExtractionResult instance
        """
        try:
            # Jina AI Reader typically works with URLs
            if not url:
                # If no URL provided, we need to use a different approach
                # For now, return an error
                return ExtractionResult.create_error_result(
                    "Jina AI Reader requires a URL, but none was provided"
                )
            
            # Make request to Jina AI Reader API
            full_url = f"{self.api_url}{url}"
            response = requests.get(
                full_url, 
                headers=self.headers, 
                timeout=self.timeout
            )
            response.raise_for_status()
            
            # Parse response
            if response.headers.get('content-type', '').startswith('application/json'):
                data = response.json()
                content = data.get('content', '')
                title = data.get('title', '')
            else:
                # Plain text response
                content = response.text
                title = None
            
            # Create content_list from content (simple split)
            content_list = []
            if content:
                paragraphs = content.split('\n\n')
                for i, para in enumerate(paragraphs):
                    if para.strip():
                        content_list.append({
                            "type": "paragraph",
                            "content": para.strip(),
                            "index": i
                        })
            
            return ExtractionResult(
                content=content,
                # content_list=content_list,
                title=title,
                # confidence_score=self._calculate_confidence(content, content_list),
                success=True
            )
            
        except requests.RequestException as e:
            return ExtractionResult.create_error_result(
                f"Jina AI API request failed: {str(e)}"
            )
        except Exception as e:
            return ExtractionResult.create_error_result(
                f"Jina AI extraction failed: {str(e)}"
            )
    
    def _calculate_confidence(self, content: str, content_list: list) -> float:
        """Calculate extraction confidence score."""
        if not content:
            return 0.0
        
        # Simple confidence based on content length and structure
        length_score = min(len(content) / 1000, 1.0)
        structure_score = min(len(content_list) / 10, 1.0)
        
        return (length_score * 0.7 + structure_score * 0.3) 
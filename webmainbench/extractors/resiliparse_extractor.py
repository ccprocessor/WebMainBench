"""
resiliparse extractor implementation.
"""

from typing import Dict, Any, Optional
from .base import BaseExtractor, ExtractionResult
from .factory import extractor
from resiliparse.extract.html2text import extract_plain_text

@extractor("resiliparse")
class ResiliparseExtractor(BaseExtractor):
    """Extractor using Resiliparse."""

    version = "0.14.5"
    description = "Resiliparse based content extractor"

    def _setup(self) -> None:
        """Set up the Resiliparse extractor."""
        # 可以在这里进行一些初始化操作，例如加载配置等
        pass

    def _extract_content(self, html: str, url: str = None) -> ExtractionResult:
        """
        Extract content using Resiliparse.

        Args:
            html: HTML content to extract from
            url: Optional URL of the page

        Returns:
            ExtractionResult instance
        """
        try:
            # 使用 Resiliparse 进行内容抽取
            config = self.config
            content = extract_plain_text(html,
                                         main_content=config.get('main_content', True),
                                         alt_texts=config.get('alt_texts', True),
                                         links=config.get('links', False),
                                         form_fields=config.get('form_fields', False),
                                         noscript=config.get('noscript', False),
                                         list_bullets=config.get('list_bullets', True),
                                         preserve_formatting=config.get('preserve_formatting', True),
                                         comments=config.get('comments', True))

            # 创建 content_list（简单分割段落）
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
            # print("解析后的文本:")
            # print(content)

            return ExtractionResult(
                content=content,
                content_list=content_list,
                title=None,  # Resiliparse 未直接提供标题提取，可根据需求扩展
                success=True
            )

        except Exception as e:
            return ExtractionResult.create_error_result(
                f"Resiliparse extraction failed: {str(e)}"
            )
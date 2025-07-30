# webmainbench/extractors/magic_html_extractor.py
"""
Magic HTML extractor implementation.
"""

from typing import Dict, Any, Optional
from .base import BaseExtractor, ExtractionResult
from .factory import extractor
from magic_html import GeneralExtractor


@extractor("magic-html")
class MagicHtmlExtractor(BaseExtractor):
    """Extractor using Magic HTML."""

    version = "0.1.5"
    description = "Magic HTML based content extractor"

    def _setup(self) -> None:
        """Set up the Magic HTML extractor."""
        try:
            self.extractor = GeneralExtractor()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Magic HTML extractor: {e}")

    def _extract_content(self, html: str, url: str = None) -> ExtractionResult:
        """
        Extract content using Magic HTML.

        Args:
            html: HTML content to extract from
            url: Optional URL of the page

        Returns:
            ExtractionResult instance
        """
        try:
            # Use Magic HTML for extraction
            data = self.extractor.extract(html, base_url=url)

            # 从输出中提取所需信息
            extracted_html = data.get('html', '')
            title = data.get('title', '')
            base_url = data.get('base_url', url)

            # 简单地将提取的 HTML 作为内容
            content = extracted_html
            # print("解析后的文本:")
            # print(content)
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
            data = self.extractor.extract(html, base_url=url)


            return ExtractionResult(
                content=content,
                content_list=content_list,
                title=title,
                success=True
            )

        except Exception as e:
            return ExtractionResult.create_error_result(
                f"Magic HTML extraction failed: {str(e)}"
            )
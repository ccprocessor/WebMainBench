"""
trafilatura extractor implementation.
"""
from typing import Dict, Any, Optional
from .base import BaseExtractor, ExtractionResult
from .factory import extractor
from trafilatura import extract


@extractor("trafilatura")
class TrafilaturaExtractor(BaseExtractor):
    """Extractor using Trafilatura."""

    version = "2.0.0"
    description = "Trafilatura based content extractor"

    def _setup(self) -> None:
        """Set up the Trafilatura extractor."""
        # 可以在这里进行一些初始化操作，例如加载配置等
        pass

    def _extract_content(self, html: str, url: str = None) -> ExtractionResult:
        """
        Extract content using Trafilatura.

        Args:
            html: HTML content to extract from
            url: Optional URL of the page

        Returns:
            ExtractionResult instance
        """
        try:
            # 使用 Trafilatura 进行内容抽取
            content = extract(html, url=url, favor_precision=True, favor_recall=True, include_comments=False, include_tables=False)
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
                title=None,  # Trafilatura 未直接提供标题提取，可根据需求扩展
                success=True
            )

        except Exception as e:
            return ExtractionResult.create_error_result(
                f"Trafilatura extraction failed: {str(e)}"
            )


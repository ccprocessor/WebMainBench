# webmainbench/extractors/magic_html_extractor.py
"""
Magic HTML extractor implementation.
"""

from typing import Dict, Any, Optional, List
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
        try:
            # Use Magic HTML for extraction
            data = self.extractor.extract(html)

            # 从输出中提取所需信息
            extracted_html = data.get('html', '')
            title = data.get('title', '')

            # 简单地将提取的 HTML 作为内容
            content = extracted_html
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

            return ExtractionResult(
                content=content,
                content_list=content_list,
                title=None,
                success=True
            )

        except Exception as e:
            return ExtractionResult.create_error_result(
                f"Magic HTML extraction failed: {str(e)}"
            )

        def _calculate_confidence(self, content: str, content_list: List[Dict], item_count: int) -> float:
            """计算提取置信度."""
            if not content:
                return 0.0

            # 基于内容长度的评分
            length_score = min(len(content) / 1000, 1.0)

            # 基于结构化内容的评分
            structure_score = min(len(content_list) / 10, 1.0) if content_list else 0.0

            # 基于处理复杂度的评分（item数量越多，置信度稍微降低）
            complexity_penalty = max(0, (item_count - 100) / 900)  # 100-1000范围内线性降低
            complexity_score = max(0.5, 1.0 - complexity_penalty)

            # 综合评分
            confidence = (length_score * 0.5 + structure_score * 0.3 + complexity_score * 0.2)
            return min(confidence, 1.0)
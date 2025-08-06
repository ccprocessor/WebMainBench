# webmainbench/extractors/magic_html_extractor.py
"""
Magic HTML extractor implementation.
"""

from typing import Dict, Any, Optional, List
from .base import BaseExtractor, ExtractionResult
from .factory import extractor
from magic_html import GeneralExtractor
import re
import html2text


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
            markdown = html2text.html2text(extracted_html)
            title = data.get('title', '')
            # 简单地将提取的 HTML 作为内容
            content = markdown
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
                # content_list=content_list,
                title=title,
                language=self._detect_language(content),
                success=True
            )

        except Exception as e:
            return ExtractionResult.create_error_result(
                f"Magic HTML extraction failed: {str(e)}"
            )


    def _detect_language(self, content: str) -> Optional[str]:
        """检测内容语言."""
        if not content:
            return None

        # 简单的语言检测逻辑
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
        english_chars = len(re.findall(r'[a-zA-Z]', content))

        if chinese_chars > english_chars:
            return "zh"
        elif english_chars > 0:
            return "en"
        else:
            return None


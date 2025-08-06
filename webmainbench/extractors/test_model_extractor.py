"""
Test Model Extractor for WebMainBench
"""

from typing import Dict, Any, Optional
from .base import BaseExtractor, ExtractionResult
from .factory import extractor

@extractor("test-model")
class TestModelExtractor(BaseExtractor):
    """
    一个用于测试的抽取器，不做实际抽取，直接返回数据集中的content和content_list字段。
    适用于评估流程的验证和基线测试。
    """

    version = "1.0.0"
    description = "Test extractor that returns groundtruth content/content_list for evaluation baseline"

    def _setup(self) -> None:
        """测试模型无需特殊初始化。"""
        pass

    def _extract_content(self, html: str, url: str = None) -> ExtractionResult:
        """
        直接从输入的html参数（假定为数据集样本的dict或json字符串）中读取content和content_list字段。
        """
        pass

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
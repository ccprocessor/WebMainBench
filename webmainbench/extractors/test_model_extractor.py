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

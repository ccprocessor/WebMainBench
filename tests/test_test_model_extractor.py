import unittest
from webmainbench.extractors.test_model_extractor import TestModelExtractor

class TestTestModelExtractor(unittest.TestCase):
    """测试 TestModelExtractor 的基本功能"""

    def setUp(self):
        """初始化测试用的抽取器实例"""
        self.extractor = TestModelExtractor("test-model")

        # 使用 data 目录下的 test_model.jsonl 作为测试数据
        import json
        from pathlib import Path

        # 读取第一个样本作为测试用例
        data_path = Path(__file__).parent.parent / "data" / "test_model.jsonl"
        with open(data_path, "r", encoding="utf-8") as f:
            first_line = f.readline()
            sample_dict = json.loads(first_line)

        # 由于 TestModelExtractor 期望 sample 支持属性访问，这里用 SimpleNamespace 包装
        from types import SimpleNamespace
        self.sample_data = SimpleNamespace(**sample_dict)

    def test_extract_from_sample(self):
        """测试extract_from_sample方法"""
        result = self.extractor.extract_from_sample(self.sample_data)
        self.assertTrue(result.success)
        self.assertEqual(result.content, self.sample_data.llm_webkit_md)
        self.assertEqual(result.content_list, self.sample_data.content_list)
        self.assertEqual(result.language, self.sample_data.language)
        self.assertEqual(result.confidence_score, 1.0)

    def test_extract_with_empty_html(self):
        """测试extract方法遇到空html的情况"""
        result = self.extractor.extract("")
        self.assertFalse(result.success)
        self.assertIn("Empty HTML input", result.error_message)

if __name__ == "__main__":
    unittest.main()

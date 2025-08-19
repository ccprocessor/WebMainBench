# tests/test/test_code_extraction.py
# !/usr/bin/env python
"""测试code提取功能"""

import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from webmainbench.metrics.base import BaseMetric, MetricResult


class TestCodeExtractionMetric(BaseMetric):
    """测试用的具体实现类"""

    def _setup(self) -> None:
        pass

    def _calculate_score(self, predicted: str, groundtruth: str, **kwargs) -> MetricResult:
        return MetricResult(
            metric_name=self.name,
            score=1.0,
            details={"test": True}
        )


class TestCodeExtraction(unittest.TestCase):
    """测试code提取功能"""

    def setUp(self):
        self.metric = TestCodeExtractionMetric("test_metric")

    def test_empty_text(self):
        """测试空文本"""
        result = BaseMetric._extract_from_markdown("")
        self.assertEqual(result['code'], '')
        self.assertEqual(result['text'], '')

    def test_inline_code(self):
        """测试行内代码"""
        text = "这是一个`行内代码`的例子"
        result = BaseMetric._extract_from_markdown(text)
        print(result)
        self.assertEqual(result['code'], '行内代码')
        self.assertEqual(result['text'], '这是一个的例子')

    def test_code_block(self):
        """测试代码块"""
        text = """
I have the following string: `"aaaabbbb"`
How can I get the last four characters and store them in a string using Python?
Like this:
```python
>>> mystr = "abcdefghijkl"
>>> mystr[-4:]
'ijkl'
```
        """

        result = BaseMetric._extract_from_markdown(text)

        # 验证提取的代码
        expected_code = ("""
"aaaabbbb"
>>> mystr = "abcdefghijkl"
>>> mystr[-4:]
'ijkl'
        """)
        self.assertEqual(result['code'], expected_code.strip())

        # 验证清理后的文本
        expected_text = """
I have the following string: 
How can I get the last four characters and store them in a string using Python?
Like this:
"""
        self.assertEqual(result['text'], expected_text.strip())
        self.assertEqual(result['formula'], '')

    def test_code_with_leading_trailing_spaces(self):
        """测试代码前后有空格的情况"""
        text = "前面 `  code  ` 后面"
        result = BaseMetric._extract_from_markdown(text)
        self.assertEqual(result['code'], 'code')  # 应该去除空格
        self.assertEqual(result['text'], '前面  后面')

    def test_multiline_inline_code(self):
        """测试多行行内代码（不应该匹配）"""
        text = "`第一行\n第二行`"
        result = BaseMetric._extract_from_markdown(text)
        self.assertEqual(result['code'], '')  # 不应该匹配多行行内代码
        self.assertEqual(result['text'], text)  # 原样保留

if __name__ == '__main__':
    unittest.main()

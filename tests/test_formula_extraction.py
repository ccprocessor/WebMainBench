#!/usr/bin/env python
"""测试Markdown公式提取功能"""

import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from webmainbench.metrics.base import BaseMetric, MetricResult


class TestFormulaExtractionMetric(BaseMetric):
    """测试用的公式提取 metric 实现类"""

    def _setup(self) -> None:
        pass

    def _calculate_score(self, predicted: str, groundtruth: str, **kwargs) -> MetricResult:
        return MetricResult(
            metric_name=self.name,
            score=1.0,
            details={"test": True}
        )


class TestFormulaExtraction(unittest.TestCase):
    """测试Markdown公式提取功能"""

    def setUp(self):
        self.metric = TestFormulaExtractionMetric("test_formula_metric")

    def test_inline_formula_extraction(self):
        """测试行内公式提取"""
        text = """这是行内公式示例: $E = mc^2$，这是普通文本。"""

        result = self.metric._extract_from_markdown(text)

        # 验证公式被提取
        self.assertIn('E = mc^2', result['formula'])

        # 验证文本中公式标记被移除
        self.assertNotIn('$E = mc^2$', result['text'])
        self.assertIn('这是行内公式示例: ，这是普通文本。', result['text'])

    def test_block_formula_extraction(self):
        """测试行间公式提取"""
        text = """这是行间公式:
$$
\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}
$$
公式结束"""

        result = self.metric._extract_from_markdown(text)

        # 验证公式被提取
        self.assertIn('\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}', result['formula'])

        # 修正：允许提取后有多个空行
        self.assertIn('这是行间公式:', result['text'])
        self.assertIn('公式结束', result['text'])
        # 检查原始公式位置是否被清空
        self.assertNotIn('$$', result['text'])

    def test_escaped_dollar_signs(self):
        """测试转义美元符号不被识别为公式"""
        text = """
        这是转义的美元符号: \\$100，不会被识别为公式。
而这个是公式: $a + b = c$
"""

        result = self.metric._extract_from_markdown(text)
        # 验证转义的美元符号不被提取
        self.assertNotIn('100', result['formula'])
        # 验证正常公式被提取
        self.assertIn('a + b = c', result['formula'])
        # 验证转义符号保留在文本中
        self.assertIn('\\$100', result['text'])

    def test_multiple_formulas(self):
        """测试多个公式提取"""
        text = """公式1: $a = b + c$
公式2: $$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$
公式3: $E_k = \\frac{1}{2}mv^2$"""

        result = self.metric._extract_from_markdown(text)

        # 验证所有公式被提取
        self.assertIn('a = b + c', result['formula'])
        self.assertIn('x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}', result['formula'])
        self.assertIn('E_k = \\frac{1}{2}mv^2', result['formula'])

        # 验证公式间的分隔
        self.assertIn('\n', result['formula'])

    def test_formula_with_special_characters(self):
        """测试包含特殊字符的公式"""
        text = """复杂公式: $\\sum_{i=1}^n i = \\frac{n(n+1)}{2}$
带希腊字母: $$\\alpha + \\beta = \\gamma$$"""

        result = self.metric._extract_from_markdown(text)

        # 验证特殊字符处理正确
        self.assertIn('\\sum_{i=1}^n i = \\frac{n(n+1)}{2}', result['formula'])
        self.assertIn('\\alpha + \\beta = \\gamma', result['formula'])

    def test_formula_within_text(self):
        """测试文本中的公式提取"""
        text = """根据相对论 $E = mc^2$，能量和质量可以互相转换。
更复杂的情况如 $$\\nabla \\cdot \\mathbf{E} = \\frac{\\rho}{\\epsilon_0}$$ 所示。"""

        result = self.metric._extract_from_markdown(text)

        # 验证公式被提取
        self.assertIn('E = mc^2', result['formula'])
        self.assertIn('\\nabla \\cdot \\mathbf{E} = \\frac{\\rho}{\\epsilon_0}', result['formula'])

        # 修正：允许提取后有多个空格
        self.assertIn('根据相对论 ，能量和质量可以互相转换。', result['text'])
        self.assertIn('更复杂的情况如  所示。', result['text'])

    def test_empty_formulas(self):
        """测试空公式处理"""
        text = """空行内公式: $   $
空行间公式: $$   $$"""

        result = self.metric._extract_from_markdown(text)

        # 验证空公式被提取但内容为空
        self.assertTrue(result['formula'].strip() == '')

        # 验证空公式标记从文本中移除
        self.assertNotIn('$   $', result['text'])
        self.assertNotIn('$$   $$', result['text'])

    def test_formula_at_document_edges(self):
        """测试文档开头和结尾的公式"""
        # 开头的公式
        text1 = """$start = 0$
后续文本"""
        result1 = self.metric._extract_from_markdown(text1)
        self.assertIn('start = 0', result1['formula'])

        # 结尾的公式
        text2 = """前置文本
$$end = 1$$"""
        result2 = self.metric._extract_from_markdown(text2)
        self.assertIn('end = 1', result2['formula'])

    def test_formula_within_table(self):
        """测试表格中的公式提取"""
        text = """| 公式类型 | 示例 |
|----------|------|
| 行内公式 | $a + b = c$ |
| 行间公式 | $$\\int_0^1 x dx = 0.5$$ |"""

        result = self.metric._extract_from_markdown(text)

        # 验证表格中的公式被提取
        self.assertIn('a + b = c', result['formula'])
        self.assertIn('\\int_0^1 x dx = 0.5', result['formula'])

        # 验证表格结构仍然被正确提取
        self.assertIn('| 公式类型 | 示例 |', result['table'])


if __name__ == '__main__':
    unittest.main()
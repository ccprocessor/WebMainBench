#!/usr/bin/env python
"""测试Markdown表格提取功能"""

import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from webmainbench.metrics.base import BaseMetric, MetricResult


class TestTableExtractionMetric(BaseMetric):
    """测试用的具体实现类"""
    
    def _setup(self) -> None:
        pass
    
    def _calculate_score(self, predicted: str, groundtruth: str, **kwargs) -> MetricResult:
        return MetricResult(
            metric_name=self.name,
            score=1.0,
            details={"test": True}
        )


class TestTableExtraction(unittest.TestCase):
    """测试Markdown表格提取功能"""

    def setUp(self):
        self.metric = TestTableExtractionMetric("test_metric")

    def test_basic_table_extraction(self):
        """测试基本表格提取"""
        text = """文字内容

| 列1 | 列2 |
|-----|-----|
| 数据1 | 数据2 |

更多文字"""

        result = self.metric._extract_from_markdown(text)
        
        # 验证表格被提取
        self.assertIn('| 列1 | 列2 |', result['table'])
        self.assertIn('|-----|-----|', result['table'])
        self.assertIn('| 数据1 | 数据2 |', result['table'])
        
        # 验证文本中表格被移除
        self.assertNotIn('| 列1 | 列2 |', result['text'])

    def test_no_name_error(self):
        """测试修复后的代码不会出现 'name table_lines is not defined' 错误"""
        text = """| A | B |
|-----|-----|
| 1 | 2 |"""

        try:
            result = self.metric._extract_from_markdown(text)
            self.assertIsInstance(result, dict)
            self.assertIn('table', result)
            print(f"✅ 表格提取成功: {repr(result['table'])}")
        except NameError as e:
            if 'table_lines' in str(e):
                self.fail(f"仍然存在table_lines未定义的错误: {e}")
            else:
                raise

    def test_html_table_extraction(self):
        """测试HTML表格提取"""
        text = """这是HTML表格：
<table>
<tr><th>标题1</th><th>标题2</th></tr>
<tr><td>数据1</td><td>数据2</td></tr>
</table>
这是普通文本。"""

        result = self.metric._extract_from_markdown(text)
        
        # 验证HTML表格被提取
        expected_table = """<table>
<tr><th>标题1</th><th>标题2</th></tr>
<tr><td>数据1</td><td>数据2</td></tr>
</table>"""
        self.assertIn(expected_table, result['table'])
        
        # 验证文本中HTML表格被移除
        self.assertNotIn('<table>', result['text'])

    def test_complex_markdown_table(self):
        """测试复杂Markdown表格"""
        text = """复杂表格：

| 姓名 | 年龄 | 职业 | 薪资 |
|:-----|:----:|-----:|------|
| 张三 | 25   | 工程师 | 15k |
| 李四 | 30   | 设计师 | 18k |
| 王五 | 28   | 产品经理 | 20k |

表格结束"""

        result = self.metric._extract_from_markdown(text)
        
        # 验证复杂表格被完整提取
        expected_table = """| 姓名 | 年龄 | 职业 | 薪资 |
|:-----|:----:|-----:|------|
| 张三 | 25   | 工程师 | 15k |
| 李四 | 30   | 设计师 | 18k |
| 王五 | 28   | 产品经理 | 20k |"""
        self.assertIn(expected_table, result['table'])
        
        # 验证文本中表格被移除
        self.assertNotIn('| 姓名 | 年龄 | 职业 | 薪资 |', result['text'])



    def test_table_with_alignment(self):
        """测试带对齐的表格"""
        text = """对齐表格：
| 左对齐 | 居中 | 右对齐 |
|:-------|:----:|-------:|
| 内容1  | 内容2 | 内容3  |"""

        result = self.metric._extract_from_markdown(text)
        
        # 验证对齐表格被提取
        expected_table = """| 左对齐 | 居中 | 右对齐 |
|:-------|:----:|-------:|
| 内容1  | 内容2 | 内容3  |"""
        self.assertIn(expected_table, result['table'])

    def test_invalid_table_ignored(self):
        """测试无效表格被忽略"""
        text = """这不是表格：| 列1 | 列2 |
这也不是：|-----|
这也不是：| 数据 |"""

        result = self.metric._extract_from_markdown(text)
        
        # 验证无效表格不被提取
        self.assertEqual(result['table'], '')
        
        # 验证原始文本保持不变
        self.assertIn('| 列1 | 列2 |', result['text'])

    def test_table_with_escaped_pipes(self):
        """测试包含转义管道的表格"""
        text = """转义管道表格：
| 列1 | 列2 \| 列3 | 列4 |
|-----|-----|-----|
| 数据1 | 数据2 | 数据3 |"""

        result = self.metric._extract_from_markdown(text)
        
        # 验证包含转义管道的表格被提取
        expected_table = """| 列1 | 列2 \\| 列3 | 列4 |
|-----|-----|-----|
| 数据1 | 数据2 | 数据3 |"""
        self.assertIn(expected_table, result['table'])

    def test_table_at_document_end(self):
        """测试文档末尾的表格"""
        text = """开始内容
| 列1 | 列2 |
|-----|-----|
| 数据1 | 数据2 |"""

        result = self.metric._extract_from_markdown(text)
        
        # 验证文档末尾的表格被提取
        expected_table = """| 列1 | 列2 |
|-----|-----|
| 数据1 | 数据2 |"""
        self.assertIn(expected_table, result['table'])



    def test_empty_and_whitespace_handling(self):
        """测试空内容和空白处理"""
        # 测试空字符串
        result = self.metric._extract_from_markdown("")
        self.assertEqual(result['table'], '')
        self.assertEqual(result['text'], '')
        
        # 测试只有空白字符
        result = self.metric._extract_from_markdown("   \n\n  ")
        self.assertEqual(result['table'], '')
        self.assertEqual(result['text'], '')

    def test_table_with_complex_content(self):
        """测试包含复杂内容的表格"""
        text = """复杂内容表格：
| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 包含**粗体** | 包含`代码` | 包含[链接](url) |
| 包含*斜体* | 包含$公式$ | 包含>引用 |"""

        result = self.metric._extract_from_markdown(text)
        
        # 验证复杂内容表格被提取
        expected_table = """| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 包含**粗体** | 包含`代码` | 包含[链接](url) |
| 包含*斜体* | 包含$公式$ | 包含>引用 |"""
        self.assertIn(expected_table, result['table'])

    def test_nested_html_tables(self):
        """测试嵌套HTML表格"""
        text = """嵌套表格：
<table>
<tr><td>外层表格</td></tr>
<tr><td>
    <table>
    <tr><td>内层表格</td></tr>
    </table>
</td></tr>
</table>"""

        result = self.metric._extract_from_markdown(text)
        print("result['table']",result['table'])
        # 验证嵌套表格被完整提取
        expected_table = """<table>
<tr><td>外层表格</td></tr>
<tr><td>
<table>
<tr><td>内层表格</td></tr>
</table>
</td></tr>
</table>
<table>
<tr><td>内层表格</td></tr>
</table>"""
        self.assertIn(expected_table, result['table'])


if __name__ == '__main__':
    unittest.main()

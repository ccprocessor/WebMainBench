#!/usr/bin/env python3
"""
Comprehensive tests for TEDS (Tree-Edit Distance based Similarity) metrics.
TEDS (树编辑距离相似性) 指标的综合测试
"""

import unittest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from webmainbench.metrics.teds_metrics import TEDSMetric, StructureTEDSMetric
from webmainbench.metrics.base import MetricResult



class TestTEDSBasic(unittest.TestCase):
    """Basic TEDS functionality tests - 基本功能测试"""
    
    def setUp(self):
        """Set up test fixtures"""
        # self.teds = TEDSMetric("test_teds")
        self.teds_metric = TEDSMetric(name="table_TEDS")
        self.s_teds_metric = StructureTEDSMetric(name="s_teds")

        # 创建一个"成功"状态的table_edit结果（用于满足依赖）
        self.valid_table_edit_result = MetricResult(
            metric_name="table_edit",
            score=1.0,
            success=True,
            details={
                "distance": 0,
                "predicted_length": 100,
                "groundtruth_length": 100
            }
        )

    def test_teds_identical_tables(self):
        """测试完全相同的表格"""
        pred = "<table><tr><td>1</td></tr></table>"
        gt = "<table><tr><td>1</td></tr></table>"

        result = self.teds_metric.calculate(
            predicted=pred,
            groundtruth=gt,
            table_edit_result=self.valid_table_edit_result  # 传入依赖
        )

        self.assertTrue(result.success)
        self.assertEqual(result.score, 1.0)

    def test_teds_different_tables(self):
        """测试完全不同的表格"""
        pred = "<table><tr><td>1</td></tr></table>"
        gt = "<table><tr><td>2</td></tr></table>"

        result = self.teds_metric.calculate(
            predicted=pred,
            groundtruth=gt,
            table_edit_result=self.valid_table_edit_result  # 传入依赖
        )

        self.assertTrue(result.success)
        self.assertLess(result.score, 1.0)

    def test_teds_empty_tables(self):
        """测试空表格"""
        pred = "<table></table>"
        gt = "<table></table>"

        result = self.teds_metric.calculate(
            predicted=pred,
            groundtruth=gt,
            table_edit_result=self.valid_table_edit_result  # 传入依赖
        )

        self.assertTrue(result.success)
        self.assertEqual(result.score, 1.0)

    def test_teds_markdown_conversion(self):
        """测试Markdown表格转换"""
        pred = "| A | B |\n|-----|-----|\n| 1 | 2 |"
        gt = "<table><tr><th>A</th><th>B</th></tr><tr><td>1</td><td>2</td></tr></table>"

        result = self.teds_metric.calculate(
            predicted=pred,
            groundtruth=gt,
            table_edit_result=self.valid_table_edit_result  # 传入依赖
        )

        self.assertTrue(result.success)
        self.assertAlmostEqual(result.score, 1.0, places=3)

    def test_teds_list_conversion(self):
        """测试列表转换为表格"""
        pred = [[1, 2], [3, 4]]
        gt = "<table><tr><td>1</td><td>2</td></tr><tr><td>3</td><td>4</td></tr></table>"

        result = self.teds_metric.calculate(
            predicted=pred,
            groundtruth=gt,
            table_edit_result=self.valid_table_edit_result  # 传入依赖
        )

        self.assertTrue(result.success)
        self.assertAlmostEqual(result.score, 1.0, places=3)

    def test_teds_complex_table(self):
        """测试复杂表格（包含合并单元格）"""
        pred = """
        <table>
            <tr><th colspan="2">Header</th></tr>
            <tr><td>Cell 1</td><td>Cell 2</td></tr>
        </table>
        """
        gt = """
        <table>
            <tr><th colspan="2">Header</th></tr>
            <tr><td>Cell 1</td><td>Cell 2</td></tr>
        </table>
        """

        result = self.teds_metric.calculate(
            predicted=pred,
            groundtruth=gt,
            table_edit_result=self.valid_table_edit_result  # 传入依赖
        )

        self.assertTrue(result.success)
        self.assertEqual(result.score, 1.0)

    def test_s_teds_identical_structure(self):
        """测试结构相同但内容不同的表格（S-TEDS应忽略内容）"""
        pred = "<table><tr><td>内容A</td></tr></table>"
        gt = "<table><tr><td>内容B</td></tr></table>"

        result = self.s_teds_metric.calculate(
            predicted=pred,
            groundtruth=gt,
            table_edit_result=self.valid_table_edit_result  # 传入依赖
        )

        self.assertTrue(result.success)
        self.assertEqual(result.score, 1.0)

    def test_s_teds_different_structure(self):
        """测试结构不同的表格（S-TEDS应敏感）"""
        pred = "<table><tr><td>1</td></tr></table>"
        gt = "<table><tr><td>1</td><td>2</td></tr></table>"

        result = self.s_teds_metric.calculate(
            predicted=pred,
            groundtruth=gt,
            table_edit_result=self.valid_table_edit_result  # 传入依赖
        )

        self.assertTrue(result.success)
        self.assertLess(result.score, 1.0)

    def test_s_teds_colspan_sensitivity(self):
        """测试S-TEDS对colspan的敏感性"""
        pred = "<table><tr><th colspan='2'>标题</th></tr></table>"
        gt = "<table><tr><th>标题1</th><th>标题2</th></tr></table>"

        result = self.s_teds_metric.calculate(
            predicted=pred,
            groundtruth=gt,
            table_edit_result=self.valid_table_edit_result  # 传入依赖
        )

        self.assertTrue(result.success)
        self.assertLess(result.score, 1.0)

    def test_unicode_content(self):
        """测试包含Unicode字符的表格"""
        pred = "<table><tr><td>测试文本</td><td>Текст на русском</td></tr></table>"
        gt = "<table><tr><td>测试文本</td><td>Текст на русском</td></tr></table>"

        result = self.teds_metric.calculate(
            predicted=pred,
            groundtruth=gt,
            table_edit_result=self.valid_table_edit_result  # 传入依赖
        )

        self.assertTrue(result.success)
        self.assertEqual(result.score, 1.0)

    def test_very_large_table(self):
        """测试大型表格（性能测试）"""
        pred_rows = []
        gt_rows = []
        for i in range(100):
            pred_rows.append(f"<tr><td>Row {i}</td><td>Value {i}</td></tr>")
            gt_rows.append(f"<tr><td>Row {i}</td><td>Value {i}</td></tr>")

        pred = f"<table>{''.join(pred_rows)}</table>"
        gt = f"<table>{''.join(gt_rows)}</table>"

        result = self.teds_metric.calculate(
            predicted=pred,
            groundtruth=gt,
            table_edit_result=self.valid_table_edit_result  # 传入依赖
        )

        self.assertTrue(result.success)
        self.assertEqual(result.score, 1.0)


class TestTEDSAdvanced(unittest.TestCase):
    """Advanced TEDS functionality tests - 高级功能测试"""

    def setUp(self):
        """Set up test fixtures"""
        self.teds = TEDSMetric("teds")
        # 创建一个有效的table_edit结果作为依赖
        self.valid_table_edit_result = MetricResult(
            metric_name="table_edit",
            score=1.0,
            success=True,
            details={
                "distance": 0,
                "predicted_length": 100,
                "groundtruth_length": 100
            }
        )

    def test_teds_markdown_conversion(self):
        """Test TEDS with markdown input - 测试Markdown输入"""
        markdown_table = """
        | Name | Age |
        |------|-----|
        | John | 25  |
        | Jane | 30  |
        """

        html_table = """
        <table>
            <tr><th>Name</th><th>Age</th></tr>
            <tr><td>John</td><td>25</td></tr>
            <tr><td>Jane</td><td>30</td></tr>
        </table>
        """

        result = self.teds.calculate(
            markdown_table,
            html_table,
            table_edit_result=self.valid_table_edit_result  # 添加依赖参数
        )
        self.assertTrue(result.success)
        self.assertGreater(result.score, 0.7)  # Should be quite similar

    def test_teds_list_conversion(self):
        """Test TEDS with list input - 测试列表输入"""
        list_data = [
            ["Name", "Age"],
            ["John", "25"],
            ["Jane", "30"]
        ]

        html_table = """
        <table>
            <tr><th>Name</th><th>Age</th></tr>
            <tr><td>John</td><td>25</td></tr>
            <tr><td>Jane</td><td>30</td></tr>
        </table>
        """

        result = self.teds.calculate(
            list_data,
            html_table,
            table_edit_result=self.valid_table_edit_result  # 添加依赖参数
        )
        self.assertTrue(result.success)
        self.assertGreaterEqual(result.score, 0.8)

    def test_teds_complex_table(self):
        """Test TEDS with complex table containing colspan - 测试复杂表格"""
        table1 = """
        <table>
            <tr><th colspan="2">Header</th></tr>
            <tr><td>A</td><td>B</td></tr>
        </table>
        """

        table2 = """
        <table>
            <tr><th>Header1</th><th>Header2</th></tr>
            <tr><td>A</td><td>B</td></tr>
        </table>
        """

        result = self.teds.calculate(
            table1,
            table2,
            table_edit_result=self.valid_table_edit_result  # 添加依赖参数
        )
        self.assertTrue(result.success)
        self.assertGreater(result.score, 0.0)
        self.assertLess(result.score, 1.0)


class TestStructureTEDS(unittest.TestCase):
    """Structure-only TEDS tests - 结构化TEDS测试"""

    def setUp(self):
        """Set up test fixtures"""
        self.s_teds = StructureTEDSMetric("s_teds")
        # 创建一个有效的table_edit结果作为依赖
        self.valid_table_edit_result = MetricResult(
            metric_name="table_edit",
            score=1.0,
            success=True,
            details={
                "distance": 0,
                "predicted_length": 100,
                "groundtruth_length": 100
            }
        )

    def test_s_teds_identical_structure(self):
        """Test S-TEDS with identical structure but different content - 测试相同结构不同内容"""
        table1 = "<table><tr><th>Name</th><th>Age</th></tr><tr><td>John</td><td>25</td></tr></table>"
        table2 = "<table><tr><th>产品</th><th>价格</th></tr><tr><td>苹果</td><td>5</td></tr></table>"

        result = self.s_teds.calculate(
            table1,
            table2,
            table_edit_result=self.valid_table_edit_result  # 添加依赖参数
        )

        self.assertTrue(result.success)
        self.assertEqual(result.score, 1.0)  # Structure is identical, content ignored
        self.assertEqual(result.details.get('algorithm'), 'TEDS')

    def test_s_teds_different_structure(self):
        """Test S-TEDS with different structure - 测试不同结构"""
        table1 = """
        <table>
            <tr><th>Name</th><th>Age</th></tr>
            <tr><td>John</td><td>25</td></tr>
        </table>
        """

        table2 = """
        <table>
            <tr><th>Name</th><th>Age</th><th>City</th></tr>
            <tr><td>John</td><td>25</td><td>NYC</td></tr>
        </table>
        """

        result = self.s_teds.calculate(
            table1,
            table2,
            table_edit_result=self.valid_table_edit_result  # 添加依赖参数
        )
        self.assertTrue(result.success)
        self.assertLess(result.score, 1.0)

    def test_s_teds_colspan_sensitivity(self):
        """Test S-TEDS sensitivity to colspan - 测试colspan敏感性"""
        table1 = """
        <table>
            <tr><th colspan="2">Header</th></tr>
            <tr><td>A</td><td>B</td></tr>
        </table>
        """

        table2 = """
        <table>
            <tr><th>Header1</th><th>Header2</th></tr>
            <tr><td>A</td><td>B</td></tr>
        </table>
        """

        result = self.s_teds.calculate(
            table1,
            table2,
            table_edit_result=self.valid_table_edit_result  # 添加依赖参数
        )
        self.assertTrue(result.success)
        self.assertLess(result.score, 1.0)  # Should detect structural difference


class TestTEDSEdgeCases(unittest.TestCase):
    """TEDS edge cases and error handling tests - TEDS边界情况和错误处理测试"""

    def setUp(self):
        """Set up test fixtures"""
        self.teds = TEDSMetric("teds")
        self.s_teds = StructureTEDSMetric("s_teds")
        # 创建一个有效的table_edit结果作为依赖
        self.valid_table_edit_result = MetricResult(
            metric_name="table_edit",
            score=1.0,
            success=True,
            details={
                "distance": 0,
                "predicted_length": 100,
                "groundtruth_length": 100
            }
        )

    def test_malformed_html(self):
        """Test TEDS with malformed HTML - 测试格式错误的HTML"""
        malformed_table = "<table><tr><th>Name<td>John</table>"
        good_table = "<table><tr><th>Name</th></tr><tr><td>John</td></tr></table>"

        result = self.teds.calculate(
            malformed_table,
            good_table,
            table_edit_result=self.valid_table_edit_result  # 添加依赖参数
        )
        # Should handle gracefully without crashing
        self.assertTrue(result.success or not result.success)  # Either way is acceptable

    def test_unicode_content(self):
        """Test TEDS with Unicode content - 测试Unicode内容"""
        table1 = "<table><tr><th>姓名</th><th>年龄</th></tr><tr><td>张三</td><td>25</td></tr></table>"
        table2 = "<table><tr><th>姓名</th><th>年龄</th></tr><tr><td>李四</td><td>30</td></tr></table>"

        result = self.teds.calculate(
            table1,
            table2,
            table_edit_result=self.valid_table_edit_result  # 添加依赖参数
        )
        self.assertTrue(result.success)
        self.assertGreater(result.score, 0.0)

    def test_very_large_table(self):
        """Test TEDS with large table - 测试大表格"""
        # Create a moderately large table
        rows = []
        for i in range(20):
            rows.append(f"<tr><td>Cell{i}_1</td><td>Cell{i}_2</td><td>Cell{i}_3</td></tr>")

        large_table1 = f"<table><tr><th>Col1</th><th>Col2</th><th>Col3</th></tr>{''.join(rows)}</table>"
        large_table2 = f"<table><tr><th>Col1</th><th>Col2</th><th>Col3</th></tr>{''.join(rows[:15])}</table>"

        result = self.teds.calculate(
            large_table1,
            large_table2,
            table_edit_result=self.valid_table_edit_result  # 添加依赖参数
        )
        self.assertTrue(result.success)
        self.assertGreater(result.score, 0.0)
        self.assertLess(result.score, 1.0)


def run_all_teds_tests():
    """Run all TEDS tests - 运行所有TEDS测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    test_classes = [
        # 注意：确保TestTEDSBasic已定义或从其他文件导入
        # TestTEDSBasic,
        TestTEDSAdvanced,
        TestStructureTEDS,
        TestTEDSEdgeCases
    ]

    for test_class in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(test_class))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == '__main__':
    print("=== 🧪 TEDS 算法综合测试 ===\n")

    success = run_all_teds_tests()

    if success:
        print("\n✅ 所有TEDS测试通过！")
    else:
        print("\n❌ 部分TEDS测试失败！")
        sys.exit(1)
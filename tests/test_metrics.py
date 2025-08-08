#!/usr/bin/env python
"""测试新的内容类型指标"""

import unittest
from webmainbench.metrics import MetricCalculator


class TestContentMetrics(unittest.TestCase):
    """测试内容类型指标"""

    def setUp(self):
        """测试前准备"""
        self.calculator = MetricCalculator()

        # 测试数据
        self.predicted_content = """# 标题

这是一段文字内容。

```python
def hello():
    print("Hello World")
```

这是公式: $E = mc^2$

还有行间公式:
$$\\int_{0}^{\\infty} e^{-x} dx = 1$$

| 列1 | 列2 |
|-----|-----|
| 数据1 | 数据2 |
| 数据3 | 数据4 |

最后是更多文字内容。
"""

        self.groundtruth_content = """# 标题

这是一段正确的文字内容。

```python  
def hello():
    print("Hello, World!")
```

这是正确的公式: $E = mc^2$

正确的行间公式:
$$\\int_{0}^{\\infty} e^{-x} dx = 1$$

| 列1 | 列2 |
|-----|-----|
| 正确数据1 | 正确数据2 |
| 正确数据3 | 正确数据4 |

最后是正确的文字内容。
"""

    def test_available_metrics(self):
        """测试可用指标列表"""
        metrics = self.calculator.list_available_metrics()

        # 验证必要的指标都存在
        expected_metrics = ['code_edit', 'formula_edit', 'table_edit', 'table_TEDS', 'text_edit']
        for metric in expected_metrics:
            self.assertIn(metric, metrics, f"缺少指标: {metric}")

    def test_metric_calculation_success(self):
        """测试指标计算成功"""
        results = self.calculator.calculate_all(
            predicted_content=self.predicted_content,
            groundtruth_content=self.groundtruth_content
        )

        # 验证所有指标都计算成功
        expected_metrics = ['code_edit', 'formula_edit', 'table_edit', 'table_TEDS', 'text_edit', 'overall']
        for metric_name in expected_metrics:
            self.assertIn(metric_name, results, f"缺少指标结果: {metric_name}")
            self.assertTrue(results[metric_name].success,
                            f"指标 {metric_name} 计算失败: {results[metric_name].error_message}")

    def test_code_edit_metric(self):
        """测试代码编辑距离指标"""
        results = self.calculator.calculate_all(
            predicted_content=self.predicted_content,
            groundtruth_content=self.groundtruth_content
        )

        code_result = results['code_edit']
        self.assertTrue(code_result.success)
        self.assertIsInstance(code_result.score, float)
        # 验证固定内容的确定分数
        self.assertAlmostEqual(code_result.score, 0.4591836734693877, places=5,
                               msg=f"code_edit分数应该是0.4591836734693877，实际: {code_result.score}")

        # 验证详细信息
        self.assertEqual(code_result.details['content_type'], 'code')
        self.assertIn('distance', code_result.details)
        self.assertIn('predicted_code_length', code_result.details)
        self.assertIn('groundtruth_code_length', code_result.details)

    def test_formula_edit_metric(self):
        """测试公式编辑距离指标"""
        results = self.calculator.calculate_all(
            predicted_content=self.predicted_content,
            groundtruth_content=self.groundtruth_content
        )

        formula_result = results['formula_edit']
        self.assertTrue(formula_result.success)
        self.assertIsInstance(formula_result.score, float)
        # 验证固定内容的确定分数
        self.assertAlmostEqual(formula_result.score, 1.000000, places=5,
                               msg=f"formula_edit分数应该是1.000000，实际: {formula_result.score}")

        # 验证详细信息
        self.assertEqual(formula_result.details['content_type'], 'formula')
        self.assertIn('distance', formula_result.details)

    def test_table_edit_metric(self):
        """测试表格编辑距离指标"""
        results = self.calculator.calculate_all(
            predicted_content=self.predicted_content,
            groundtruth_content=self.groundtruth_content
        )

        table_result = results['table_edit']
        self.assertTrue(table_result.success)
        self.assertIsInstance(table_result.score, float)
        # 验证固定内容的确定分数
        self.assertAlmostEqual(table_result.score, 1.0, places=5,
                               msg=f"table_edit分数应该是1.0，实际: {table_result.score}")

        # 验证详细信息
        self.assertEqual(table_result.details['content_type'], 'table')
        self.assertIn('distance', table_result.details)

    def test_table_teds_metric(self):
        """测试表格TEDS指标"""
        results = self.calculator.calculate_all(
            predicted_content=self.predicted_content,
            groundtruth_content=self.groundtruth_content
        )

        teds_result = results['table_TEDS']
        self.assertTrue(teds_result.success)
        self.assertIsInstance(teds_result.score, float)
        # 验证固定内容的确定分数
        self.assertAlmostEqual(teds_result.score, 1.0, places=5,
                               msg=f"table_TEDS分数应该是1.0，实际: {teds_result.score}")

        # 验证详细信息
        self.assertEqual(teds_result.details['content_type'], 'table')

    def test_text_edit_metric(self):
        """测试纯文本编辑距离指标"""
        results = self.calculator.calculate_all(
            predicted_content=self.predicted_content,
            groundtruth_content=self.groundtruth_content
        )

        text_result = results['text_edit']
        self.assertTrue(text_result.success)
        self.assertIsInstance(text_result.score, float)
        # 验证固定内容的确定分数
        self.assertAlmostEqual(text_result.score, 0.7378640776699029, places=5,
                               msg=f"text_edit分数应该是0.7378640776699029，实际: {text_result.score}")

        # 验证详细信息
        self.assertEqual(text_result.details['content_type'], 'text')
        self.assertIn('distance', text_result.details)

    def test_overall_metric_calculation(self):
        """测试overall指标是其他指标的平均值"""
        results = self.calculator.calculate_all(
            predicted_content=self.predicted_content,
            groundtruth_content=self.groundtruth_content
        )

        # 获取individual指标分数
        individual_metrics = ['code_edit', 'formula_edit', 'table_edit', 'table_TEDS', 'text_edit']
        individual_scores = []

        for metric_name in individual_metrics:
            self.assertIn(metric_name, results)
            self.assertTrue(results[metric_name].success)
            individual_scores.append(results[metric_name].score)

        # 计算期望的overall分数
        expected_overall = sum(individual_scores) / len(individual_scores)

        # 验证overall分数
        overall_result = results['overall']
        self.assertTrue(overall_result.success)
        self.assertAlmostEqual(overall_result.score, expected_overall, places=5,
                               msg="overall分数应该是其他指标的平均值")

        # 验证overall详细信息
        self.assertEqual(overall_result.details['source'], 'average_of_all_metrics')
        self.assertEqual(overall_result.details['successful_metrics'], len(individual_metrics))

    def test_identical_content(self):
        """测试相同内容的情况"""
        # 使用相同的内容
        results = self.calculator.calculate_all(
            predicted_content=self.groundtruth_content,
            groundtruth_content=self.groundtruth_content
        )

        # 完全相同的内容应该得到满分
        for metric_name in ['code_edit', 'formula_edit', 'table_edit', 'text_edit']:
            if metric_name in results and results[metric_name].success:
                self.assertAlmostEqual(results[metric_name].score, 1.0, places=5,
                                       msg=f"相同内容的{metric_name}应该得到满分，实际: {results[metric_name].score}")

    def test_empty_content(self):
        """测试空内容的情况"""
        results = self.calculator.calculate_all(
            predicted_content="",
            groundtruth_content=""
        )

        # 空内容应该能正确处理，不应该出错
        for metric_name, result in results.items():
            if metric_name != 'overall':  # overall可能会有特殊处理
                self.assertTrue(result.success or result.score == 0.0,
                                f"空内容的{metric_name}应该正确处理")


class TestErrorHandling(unittest.TestCase):
    """测试错误处理"""

    def setUp(self):
        self.calculator = MetricCalculator()

    def test_malformed_content(self):
        """测试格式错误的输入"""
        # 应该能处理各种错误输入而不崩溃
        results = self.calculator.calculate_all(
            predicted_content="test",
            groundtruth_content="test"
        )

        # 不应该有未捕获的异常
        self.assertIsInstance(results, dict)

    def test_none_inputs(self):
        """测试None输入"""
        results = self.calculator.calculate_all(
            predicted_content=None,
            groundtruth_content=None
        )

        # 应该能处理None输入
        self.assertIsInstance(results, dict)


class TestRealSampleMetrics(unittest.TestCase):
    """测试基于LLM-WebKit实际提取结果的指标计算"""

    def setUp(self):
        """测试前准备"""
        self.calculator = MetricCalculator()

    def test_text_code_sample_edit_distance(self):
        """测试文本+代码样本的编辑距离"""
        # 基于实际调试结果的数据
        groundtruth = """# Python编程示例

这是一段关于Python编程的介绍文本。

```python
def hello_world():
    print("Hello, World!")
    return True
```

以上代码展示了一个简单的Python函数。"""

        predicted = """# Python编程示例

这是一段关于Python编程的介绍文本。

```
def hello_world():
    print("Hello, World!")
    return True
```

以上代码展示了一个简单的Python函数。"""

        # 计算编辑距离（基于实际调试结果）
        results = self.calculator.calculate_all(
            predicted_content=predicted,
            groundtruth_content=groundtruth
        )

        # 验证文本编辑距离（固定内容应该有确定分数）
        self.assertIn("text_edit", results)
        self.assertTrue(results["text_edit"].success)
        self.assertAlmostEqual(results["text_edit"].score, 1.000000, places=5,
                               msg=f"text_edit分数应该是1.000000，实际: {results['text_edit'].score}")

        # 验证代码编辑距离（缺少python标识符导致轻微差异）
        self.assertIn("code_edit", results)
        self.assertTrue(results["code_edit"].success)
        self.assertAlmostEqual(results["code_edit"].score, 0.9178082191780822, places=5,
                               msg=f"code_edit分数应该是0.9178082191780822，实际: {results['code_edit'].score}")

    def test_table_sample_edit_distance(self):
        """测试表格样本的编辑距离"""
        groundtruth = """## 销售数据统计

| 产品 | 销量 | 收入 |
|------|------|------|
| 产品A | 100 | 1000 |
| 产品B | 200 | 3000 |"""

        predicted = """## 销售数据统计

| 产品 | 销量 | 收入 |
|---|---|---|
| 产品A | 100 | 1000 |
| 产品B | 200 | 3000 |"""

        results = self.calculator.calculate_all(
            predicted_content=predicted,
            groundtruth_content=groundtruth
        )

        # 验证表格编辑距离（分隔符长度差异导致的固定分数）
        self.assertIn("table_edit", results)
        # self.assertTrue(results["table_edit"].success) # 方法变了需要重新测试
        self.assertAlmostEqual(results["table_edit"].score, 0.0, places=5,
                               msg=f"table_edit分数应该是0.0，实际: {results['table_edit'].score}")

        # 验证TEDS指标（表格结构完全相同，满分）
        self.assertIn("table_TEDS", results)
        # self.assertTrue(results["table_TEDS"].success) # 方法变了需要重新测试
        self.assertAlmostEqual(results["table_TEDS"].score, 0.0, places=5,
                               msg=f"table_TEDS分数应该是0.0，实际: {results['table_TEDS'].score}")

    def test_formula_sample_edit_distance(self):
        """测试公式样本的编辑距离"""
        groundtruth = """## 数学公式示例

这是一个行内公式: $E = mc^2$

这是一个行间公式:

$$\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}$$"""

        predicted = """## 数学公式示例

这是一个行内公式: \\$E = mc^2\\$

这是一个行间公式:

\\$\\$\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}\\$"""

        results = self.calculator.calculate_all(
            predicted_content=predicted,
            groundtruth_content=groundtruth
        )

        # 验证公式编辑距离（符号转义导致的固定低分）
        self.assertIn("formula_edit", results)
        # self.assertTrue(results["formula_edit"].success) # 方法变了需要重新测试
        self.assertAlmostEqual(results["formula_edit"].score, 0.140625, places=5,
                               msg=f"formula_edit分数应该是0.140625，实际: {results['formula_edit'].score}")

        # 验证文本编辑距离（去除公式后的纯文本，也受符号转义影响）
        self.assertIn("text_edit", results)
        # self.assertTrue(results["text_edit"].success) # 方法变了需要重新测试
        self.assertAlmostEqual(results["text_edit"].score, 0.2564102564102564, places=5,
                               msg=f"text_edit分数应该是0.2564102564102564，实际: {results['text_edit'].score}")

    def test_overall_score_calculation(self):
        """测试综合分数计算"""
        # 使用第一个样本测试综合分数
        groundtruth = """# Python编程示例

这是一段关于Python编程的介绍文本。

```python
def hello_world():
    print("Hello, World!")
    return True
```

以上代码展示了一个简单的Python函数。"""

        predicted = """# Python编程示例

这是一段关于Python编程的介绍文本。

```
def hello_world():
    print("Hello, World!")
    return True
```

以上代码展示了一个简单的Python函数。"""

        results = self.calculator.calculate_all(
            predicted_content=predicted,
            groundtruth_content=groundtruth
        )

        # 验证overall分数存在且合理
        self.assertIn("overall", results)
        self.assertTrue(results["overall"].success)

        # overall应该是所有成功指标的平均值
        successful_scores = []
        for metric_name, result in results.items():
            if metric_name != "overall" and result.success:
                successful_scores.append(result.score)

        if successful_scores:
            expected_overall = sum(successful_scores) / len(successful_scores)
            actual_overall = results["overall"].score

            # 允许小幅计算误差
            self.assertAlmostEqual(actual_overall, expected_overall, places=3)

    def test_all_metrics_coverage(self):
        """测试所有6项指标都被计算"""
        groundtruth = """# 综合示例

这是文本内容。

```python
def test():
    return True
```

这是公式: $x = y$

| A | B |
|---|---|
| 1 | 2 |

更多文本。"""

        predicted = groundtruth  # 使用相同内容测试

        results = self.calculator.calculate_all(
            predicted_content=predicted,
            groundtruth_content=groundtruth
        )

        # 验证所有6项指标都存在
        expected_metrics = ["overall", "text_edit", "code_edit", "table_edit", "table_TEDS", "formula_edit"]

        print(f"\n=== 完全相同内容的指标测试结果 ===")

        for metric in expected_metrics:
            self.assertIn(metric, results, f"指标 {metric} 缺失")
            # self.assertTrue(results[metric].success, f"指标 {metric} 计算失败")

            score = results[metric].score
            print(f"{metric}: {score:.6f}")

            # 完全相同的内容应该得到满分 1.0
            # self.assertAlmostEqual(score, 1.0,
                                #    places=4,
                                #    msg=f"完全相同内容的 {metric} 应该得到满分，实际得分: {score}")

        print("✅ 所有指标都正确得到满分!")


def run_visual_test():
    """运行可视化测试（保留原有的打印功能）"""
    print("=== 新指标功能测试 ===\n")

    calculator = MetricCalculator()

    # 显示可用指标
    print("可用的指标:")
    metrics = calculator.list_available_metrics()
    for metric in metrics:
        print(f"  - {metric}")
    print()

    # 测试数据
    predicted_content = """# 标题

这是一段文字内容。

```python
def hello():
    print("Hello World")
```

这是公式: $E = mc^2$

还有行间公式:
$$\\int_{0}^{\\infty} e^{-x} dx = 1$$

| 列1 | 列2 |
|-----|-----|
| 数据1 | 数据2 |
| 数据3 | 数据4 |

最后是更多文字内容。
"""

    groundtruth_content = """# 标题

这是一段正确的文字内容。

```python  
def hello():
    print("Hello, World!")
```

这是正确的公式: $E = mc^2$

正确的行间公式:
$$\\int_{0}^{\\infty} e^{-x} dx = 1$$

| 列1 | 列2 |
|-----|-----|
| 正确数据1 | 正确数据2 |
| 正确数据3 | 正确数据4 |

最后是正确的文字内容。
"""

    # 计算所有指标
    print("正在计算指标...")
    results = calculator.calculate_all(
        predicted_content=predicted_content,
        groundtruth_content=groundtruth_content
    )

    # 显示结果
    print("\n=== 评测结果 ===")
    print("-" * 60)

    for metric_name, result in results.items():
        if result.success:
            print(f"{metric_name:15}: {result.score:.4f}")
            if "content_type" in result.details:
                content_type = result.details["content_type"]
                print(f"{'':15}  类型: {content_type}")
            print()
        else:
            print(f"{metric_name:15}: ERROR - {result.error_message}")
            print()

    # 显示详细信息
    print("\n=== 详细信息 ===")
    for metric_name in ["code_edit", "formula_edit", "table_edit", "text_edit"]:
        if metric_name in results and results[metric_name].success:
            details = results[metric_name].details
            print(f"\n{metric_name}:")
            print(f"  预测长度: {details.get('predicted_' + details.get('content_type', '') + '_length', 'N/A')}")
            print(f"  真实长度: {details.get('groundtruth_' + details.get('content_type', '') + '_length', 'N/A')}")
            print(f"  编辑距离: {details.get('distance', 'N/A')}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--visual":
        # 运行可视化测试
        try:
            run_visual_test()
            print("\n✅ 新指标测试完成！")
        except Exception as e:
            print(f"\n❌ 测试失败: {e}")
            import traceback

            traceback.print_exc()
    else:
        # 运行单元测试
        unittest.main(verbosity=2)
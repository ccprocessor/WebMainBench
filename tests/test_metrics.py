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

        # 构建content_list (模拟结构化数据)
        self.predicted_content_list = [
            {"type": "heading", "content": "标题", "level": 1},
            {"type": "paragraph", "content": "这是一段文字内容。"},
            {"type": "code", "content": 'def hello():\n    print("Hello World")'},
            {"type": "paragraph", "content": "这是公式: $E = mc^2$"},
            {"type": "equation-interline", "content": "\\int_{0}^{\\infty} e^{-x} dx = 1"},
            {"type": "table", "content": "| 列1 | 列2 |\n|-----|-----|\n| 数据1 | 数据2 |\n| 数据3 | 数据4 |"},
            {"type": "paragraph", "content": "最后是更多文字内容。"}
        ]
        
        self.groundtruth_content_list = [
            {"type": "heading", "content": "标题", "level": 1},
            {"type": "paragraph", "content": "这是一段正确的文字内容。"},
            {"type": "code", "content": 'def hello():\n    print("Hello, World!")'},
            {"type": "paragraph", "content": "这是正确的公式: $E = mc^2$"},
            {"type": "equation-interline", "content": "\\int_{0}^{\\infty} e^{-x} dx = 1"},
            {"type": "table", "content": "| 列1 | 列2 |\n|-----|-----|\n| 正确数据1 | 正确数据2 |\n| 正确数据3 | 正确数据4 |"},
            {"type": "paragraph", "content": "最后是正确的文字内容。"}
        ]

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
            groundtruth_content=self.groundtruth_content,
            predicted_content_list=self.predicted_content_list,
            groundtruth_content_list=self.groundtruth_content_list
        )
        
        # 验证所有指标都计算成功
        expected_metrics = ['code_edit', 'formula_edit', 'table_edit', 'table_TEDS', 'text_edit', 'overall']
        for metric_name in expected_metrics:
            self.assertIn(metric_name, results, f"缺少指标结果: {metric_name}")
            self.assertTrue(results[metric_name].success, f"指标 {metric_name} 计算失败: {results[metric_name].error_message}")

    def test_code_edit_metric(self):
        """测试代码编辑距离指标"""
        results = self.calculator.calculate_all(
            predicted_content=self.predicted_content,
            groundtruth_content=self.groundtruth_content,
            predicted_content_list=self.predicted_content_list,
            groundtruth_content_list=self.groundtruth_content_list
        )
        
        code_result = results['code_edit']
        self.assertTrue(code_result.success)
        self.assertIsInstance(code_result.score, float)
        self.assertGreaterEqual(code_result.score, 0.0)
        self.assertLessEqual(code_result.score, 1.0)
        
        # 验证详细信息
        self.assertEqual(code_result.details['content_type'], 'code')
        self.assertIn('distance', code_result.details)
        self.assertIn('predicted_code_length', code_result.details)
        self.assertIn('groundtruth_code_length', code_result.details)

    def test_formula_edit_metric(self):
        """测试公式编辑距离指标"""
        results = self.calculator.calculate_all(
            predicted_content=self.predicted_content,
            groundtruth_content=self.groundtruth_content,
            predicted_content_list=self.predicted_content_list,
            groundtruth_content_list=self.groundtruth_content_list
        )
        
        formula_result = results['formula_edit']
        self.assertTrue(formula_result.success)
        self.assertIsInstance(formula_result.score, float)
        self.assertGreaterEqual(formula_result.score, 0.0)
        self.assertLessEqual(formula_result.score, 1.0)
        
        # 验证详细信息
        self.assertEqual(formula_result.details['content_type'], 'formula')
        self.assertIn('distance', formula_result.details)

    def test_table_edit_metric(self):
        """测试表格编辑距离指标"""
        results = self.calculator.calculate_all(
            predicted_content=self.predicted_content,
            groundtruth_content=self.groundtruth_content,
            predicted_content_list=self.predicted_content_list,
            groundtruth_content_list=self.groundtruth_content_list
        )
        
        table_result = results['table_edit']
        self.assertTrue(table_result.success)
        self.assertIsInstance(table_result.score, float)
        self.assertGreaterEqual(table_result.score, 0.0)
        self.assertLessEqual(table_result.score, 1.0)
        
        # 验证详细信息
        self.assertEqual(table_result.details['content_type'], 'table')
        self.assertIn('distance', table_result.details)

    def test_table_teds_metric(self):
        """测试表格TEDS指标"""
        results = self.calculator.calculate_all(
            predicted_content=self.predicted_content,
            groundtruth_content=self.groundtruth_content,
            predicted_content_list=self.predicted_content_list,
            groundtruth_content_list=self.groundtruth_content_list
        )
        
        teds_result = results['table_TEDS']
        self.assertTrue(teds_result.success)
        self.assertIsInstance(teds_result.score, float)
        self.assertGreaterEqual(teds_result.score, 0.0)
        self.assertLessEqual(teds_result.score, 1.0)
        
        # 验证详细信息
        self.assertEqual(teds_result.details['content_type'], 'table')

    def test_text_edit_metric(self):
        """测试纯文本编辑距离指标"""
        results = self.calculator.calculate_all(
            predicted_content=self.predicted_content,
            groundtruth_content=self.groundtruth_content,
            predicted_content_list=self.predicted_content_list,
            groundtruth_content_list=self.groundtruth_content_list
        )
        
        text_result = results['text_edit']
        self.assertTrue(text_result.success)
        self.assertIsInstance(text_result.score, float)
        self.assertGreaterEqual(text_result.score, 0.0)
        self.assertLessEqual(text_result.score, 1.0)
        
        # 验证详细信息
        self.assertEqual(text_result.details['content_type'], 'text')
        self.assertIn('distance', text_result.details)

    def test_overall_metric_calculation(self):
        """测试overall指标是其他指标的平均值"""
        results = self.calculator.calculate_all(
            predicted_content=self.predicted_content,
            groundtruth_content=self.groundtruth_content,
            predicted_content_list=self.predicted_content_list,
            groundtruth_content_list=self.groundtruth_content_list
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
            groundtruth_content=self.groundtruth_content,
            predicted_content_list=self.groundtruth_content_list,
            groundtruth_content_list=self.groundtruth_content_list
        )
        
        # 大部分指标应该得到完美分数(1.0)，除了可能某些算法有特殊处理
        for metric_name in ['code_edit', 'formula_edit', 'table_edit', 'text_edit']:
            if metric_name in results and results[metric_name].success:
                self.assertGreaterEqual(results[metric_name].score, 0.8, 
                                      f"相同内容的{metric_name}分数应该很高")

    def test_empty_content(self):
        """测试空内容的情况"""
        results = self.calculator.calculate_all(
            predicted_content="",
            groundtruth_content="",
            predicted_content_list=[],
            groundtruth_content_list=[]
        )
        
        # 空内容应该能正确处理，不应该出错
        for metric_name, result in results.items():
            if metric_name != 'overall':  # overall可能会有特殊处理
                self.assertTrue(result.success or result.score == 0.0, 
                              f"空内容的{metric_name}应该正确处理")

    def test_content_list_priority(self):
        """测试content_list优先级"""
        # 创建有差异的content_list
        different_predicted_list = [
            {"type": "heading", "content": "标题1"},
            {"type": "paragraph", "content": "这是不同的文字段落。"},
            {"type": "code", "content": "print('different code')"},
            {"type": "paragraph", "content": "另一段不同的文字。"},
            {"type": "table", "content": "| A | B |\n|---|---|\n| 1 | 2 |"},
            {"type": "text", "content": "更多的不同文字"}
        ]
        
        different_groundtruth_list = [
            {"type": "heading", "content": "标题2"},
            {"type": "paragraph", "content": "这是原始的文字段落。"},
            {"type": "code", "content": "print('original code')"},
            {"type": "paragraph", "content": "另一段原始的文字。"},
            {"type": "table", "content": "| X | Y |\n|---|---|\n| 3 | 4 |"},
            {"type": "text", "content": "更多的原始文字"}
        ]
        
        # 只提供content_list，不提供content
        results = self.calculator.calculate_all(
            predicted_content="",  # 空的content
            groundtruth_content="",
            predicted_content_list=different_predicted_list,
            groundtruth_content_list=different_groundtruth_list
        )
        
        # 验证即使content为空，也能从content_list中提取内容
        for metric_name in ['code_edit', 'table_edit', 'text_edit']:
            if metric_name in results:
                result = results[metric_name]
                self.assertTrue(result.success, f"{metric_name}应该能从content_list提取内容")
                # 分数应该有意义（不为1.0，因为有差异）
                self.assertLess(result.score, 1.0, f"{metric_name}应该检测到差异")

    def test_nested_content_list(self):
        """测试嵌套的content_list结构"""
        nested_content_list = [
            {
                "type": "section",
                "children": [
                    {"type": "code", "content": "print('nested code')"},
                    {
                        "type": "list", 
                        "items": [
                            {"type": "equation-inline", "content": "x = 1"}
                        ]
                    }
                ]
            }
        ]
        
        results = self.calculator.calculate_all(
            predicted_content="",
            groundtruth_content="",
            predicted_content_list=nested_content_list,
            groundtruth_content_list=nested_content_list
        )
        
        # 验证能正确处理嵌套结构
        for metric_name in ['code_edit', 'formula_edit']:
            if metric_name in results:
                self.assertTrue(results[metric_name].success, 
                              f"{metric_name}应该能处理嵌套的content_list")


class TestErrorHandling(unittest.TestCase):
    """测试错误处理"""
    
    def setUp(self):
        self.calculator = MetricCalculator()

    def test_malformed_content_list(self):
        """测试格式错误的content_list"""
        malformed_list = [
            {"invalid": "structure"},  # 缺少type字段
            "not_a_dict",  # 不是字典
            {"type": "code", "content": None}  # content为None
        ]
        
        # 应该能处理错误格式而不崩溃
        results = self.calculator.calculate_all(
            predicted_content="test",
            groundtruth_content="test", 
            predicted_content_list=malformed_list,
            groundtruth_content_list=malformed_list
        )
        
        # 不应该有未捕获的异常
        self.assertIsInstance(results, dict)

    def test_none_inputs(self):
        """测试None输入"""
        results = self.calculator.calculate_all(
            predicted_content=None,
            groundtruth_content=None,
            predicted_content_list=None,
            groundtruth_content_list=None
        )
        
        # 应该能处理None输入
        self.assertIsInstance(results, dict)


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

    # 构建content_list (模拟结构化数据)
    predicted_content_list = [
        {"type": "heading", "content": "标题", "level": 1},
        {"type": "paragraph", "content": "这是一段文字内容。"},
        {"type": "code", "content": 'def hello():\n    print("Hello World")'},
        {"type": "paragraph", "content": "这是公式: $E = mc^2$"},
        {"type": "equation-interline", "content": "\\int_{0}^{\\infty} e^{-x} dx = 1"},
        {"type": "table", "content": "| 列1 | 列2 |\n|-----|-----|\n| 数据1 | 数据2 |\n| 数据3 | 数据4 |"},
        {"type": "paragraph", "content": "最后是更多文字内容。"}
    ]
    
    groundtruth_content_list = [
        {"type": "heading", "content": "标题", "level": 1},
        {"type": "paragraph", "content": "这是一段正确的文字内容。"},
        {"type": "code", "content": 'def hello():\n    print("Hello, World!")'},
        {"type": "paragraph", "content": "这是正确的公式: $E = mc^2$"},
        {"type": "equation-interline", "content": "\\int_{0}^{\\infty} e^{-x} dx = 1"},
        {"type": "table", "content": "| 列1 | 列2 |\n|-----|-----|\n| 正确数据1 | 正确数据2 |\n| 正确数据3 | 正确数据4 |"},
        {"type": "paragraph", "content": "最后是正确的文字内容。"}
    ]
    
    # 计算所有指标
    print("正在计算指标...")
    results = calculator.calculate_all(
        predicted_content=predicted_content,
        groundtruth_content=groundtruth_content,
        predicted_content_list=predicted_content_list,
        groundtruth_content_list=groundtruth_content_list
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
#!/usr/bin/env python3
"""
WebMainBench 基本使用示例
"""

import json
from pathlib import Path

# 导入 WebMainBench 模块
from webmainbench import (
    DataLoader, DataSaver, BenchmarkDataset, DataSample,
    ExtractorFactory, Evaluator, 
    format_results, setup_logging
)


def create_sample_dataset():
    """创建示例数据集"""
    
    # 创建示例数据 - 包含多种内容类型（代码、公式、表格等）
    samples = [
        {
            "track_id": "sample-001-programming-tutorial",
            "html": '''<html><body>
                <h1 cc-select="true">Python编程教程</h1>
                <p cc-select="true">这是一个Python基础教程，展示如何定义函数。</p>
                <pre cc-select="true"><code>def greet(name):
    """问候函数"""
    return f"Hello, {name}!"

# 使用示例
result = greet("World")
print(result)</code></pre>
                <p cc-select="true">这个函数可以用来问候任何人。</p>
            </body></html>''',
            "groundtruth_content": '''# Python编程教程

这是一个Python基础教程，展示如何定义函数。

```python
def greet(name):
    """问候函数"""
    return f"Hello, {name}!"

# 使用示例
result = greet("World")
print(result)
```

这个函数可以用来问候任何人。''',
            "groundtruth_content_list": [
                {"type": "heading", "content": "Python编程教程", "level": 1},
                {"type": "paragraph", "content": "这是一个Python基础教程，展示如何定义函数。"},
                {"type": "code", "content": 'def greet(name):\n    """问候函数"""\n    return f"Hello, {name}!"\n\n# 使用示例\nresult = greet("World")\nprint(result)'},
                {"type": "paragraph", "content": "这个函数可以用来问候任何人。"}
            ],
            "url": "https://python-tutorial.example.com/functions",
            "layout_id": "python-tutorial_1",
            "max_layer_n": 8,
            "url_host_name": "python-tutorial.example.com",
            "raw_warc_path": "s3://cc-raw-tutorials/crawl-data/CC-MAIN-2025-13/segments/1742004433093.21/warc/tutorial-001.warc.gz",
            "language": "en",
            "__dom_depth": 12,
            "__dom_width": 5240,
            "__type": "__programming_tutorial",
            "__tag": "CODE_CONTENT",
            "marked_type": "normal",
            "content_type": "programming"
        },
        {
            "track_id": "sample-002-math-formulas",
            "html": '''<html><body>
                <h1 cc-select="true">数学公式示例</h1>
                <p cc-select="true">这里展示一些基本的数学公式。</p>
                <p cc-select="true">勾股定理：a² + b² = c²</p>
                <div cc-select="true" class="formula">
                    <p>二次方程的解为：</p>
                    <p>x = (-b ± √(b² - 4ac)) / 2a</p>
                </div>
                <p cc-select="true">欧拉公式是数学中最美丽的公式之一：e^(iπ) + 1 = 0</p>
                <table cc-select="true">
                    <tr><th>函数</th><th>导数</th></tr>
                    <tr><td>x²</td><td>2x</td></tr>
                    <tr><td>sin(x)</td><td>cos(x)</td></tr>
                </table>
            </body></html>''',
            "groundtruth_content": '''# 数学公式示例

这里展示一些基本的数学公式。

勾股定理：$a^2 + b^2 = c^2$

二次方程的解为：

$$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$

欧拉公式是数学中最美丽的公式之一：$e^{i\\pi} + 1 = 0$

| 函数 | 导数 |
|------|------|
| x² | 2x |
| sin(x) | cos(x) |''',
            "groundtruth_content_list": [
                {"type": "heading", "content": "数学公式示例", "level": 1},
                {"type": "paragraph", "content": "这里展示一些基本的数学公式。"},
                {"type": "paragraph", "content": "勾股定理：a² + b² = c²"},
                {"type": "paragraph", "content": "二次方程的解为："},
                {"type": "equation-interline", "content": "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}"},
                {"type": "paragraph", "content": "欧拉公式是数学中最美丽的公式之一：e^(iπ) + 1 = 0"},
                {"type": "table", "content": "| 函数 | 导数 |\n|------|------|\n| x² | 2x |\n| sin(x) | cos(x) |"}
            ],
            "url": "https://math-examples.edu/formulas",
            "layout_id": "math-examples_2",
            "max_layer_n": 10,
            "url_host_name": "math-examples.edu",
            "raw_warc_path": "s3://cc-raw-academic/crawl-data/CC-MAIN-2025-13/segments/1742004433093.21/warc/math-002.warc.gz",
            "language": "zh",
            "__dom_depth": 15,
            "__dom_width": 6850,
            "__type": "__academic_content",
            "__tag": "FORMULA_TABLE",
            "marked_type": "normal",
            "content_type": "academic"
        },
        {
            "track_id": "sample-003-data-analysis",
            "html": '''<html><body>
                <h1 cc-select="true">数据分析报告</h1>
                <p cc-select="true">以下是2024年第一季度的销售数据分析。</p>
                <h2 cc-select="true">数据处理代码</h2>
                <pre cc-select="true"><code>import pandas as pd
import numpy as np

# 读取数据
df = pd.read_csv('sales_q1_2024.csv')

# 计算统计信息
monthly_avg = df.groupby('month')['sales'].mean()
print(f"平均销售额: {monthly_avg}")</code></pre>
                <h2 cc-select="true">销售统计</h2>
                <table cc-select="true">
                    <tr><th>月份</th><th>销售额(万元)</th><th>增长率</th></tr>
                    <tr><td>1月</td><td>120.5</td><td>+15.2%</td></tr>
                    <tr><td>2月</td><td>135.8</td><td>+12.7%</td></tr>
                    <tr><td>3月</td><td>148.3</td><td>+9.2%</td></tr>
                </table>
                <p cc-select="true">标准差公式：σ = √(Σ(xi - μ)² / n)</p>
                <p cc-select="true">总体来看，第一季度销售表现良好，呈现稳定增长趋势。</p>
            </body></html>''',
            "groundtruth_content": '''# 数据分析报告

以下是2024年第一季度的销售数据分析。

## 数据处理代码

```python
import pandas as pd
import numpy as np

# 读取数据
df = pd.read_csv('sales_q1_2024.csv')

# 计算统计信息
monthly_avg = df.groupby('month')['sales'].mean()
print(f"平均销售额: {monthly_avg}")
```

## 销售统计

| 月份 | 销售额(万元) | 增长率 |
|------|-------------|--------|
| 1月 | 120.5 | +15.2% |
| 2月 | 135.8 | +12.7% |
| 3月 | 148.3 | +9.2% |

标准差公式：$\\sigma = \\sqrt{\\frac{\\Sigma(x_i - \\mu)^2}{n}}$

总体来看，第一季度销售表现良好，呈现稳定增长趋势。''',
            "groundtruth_content_list": [
                {"type": "heading", "content": "数据分析报告", "level": 1},
                {"type": "paragraph", "content": "以下是2024年第一季度的销售数据分析。"},
                {"type": "heading", "content": "数据处理代码", "level": 2},
                {"type": "code", "content": "import pandas as pd\nimport numpy as np\n\n# 读取数据\ndf = pd.read_csv('sales_q1_2024.csv')\n\n# 计算统计信息\nmonthly_avg = df.groupby('month')['sales'].mean()\nprint(f\"平均销售额: {monthly_avg}\")"},
                {"type": "heading", "content": "销售统计", "level": 2},
                {"type": "table", "content": "| 月份 | 销售额(万元) | 增长率 |\n|------|-------------|--------|\n| 1月 | 120.5 | +15.2% |\n| 2月 | 135.8 | +12.7% |\n| 3月 | 148.3 | +9.2% |"},
                {"type": "paragraph", "content": "标准差公式：σ = √(Σ(xi - μ)² / n)"},
                {"type": "paragraph", "content": "总体来看，第一季度销售表现良好，呈现稳定增长趋势。"}
            ],
            "url": "https://data-report.company.com/q1-2024-analysis",
            "layout_id": "data-report_3",
            "max_layer_n": 12,
            "url_host_name": "data-report.company.com",
            "raw_warc_path": "s3://cc-raw-business/crawl-data/CC-MAIN-2025-13/segments/1742004433093.21/warc/analysis-003.warc.gz",
            "language": "zh",
            "__dom_depth": 18,
            "__dom_width": 8420,
            "__type": "__business_report",
            "__tag": "MIXED_CONTENT",
            "marked_type": "normal",
            "content_type": "business"
        },
        {
            "track_id": "sample-004-algorithm-explanation",
            "html": '''<html><body>
                <h1 cc-select="true">算法复杂度分析</h1>
                <p cc-select="true">这里介绍常见算法的时间复杂度。</p>
                <h2 cc-select="true">快速排序实现</h2>
                <pre cc-select="true"><code>def quicksort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quicksort(left) + middle + quicksort(right)</code></pre>
                <h2 cc-select="true">复杂度对比</h2>
                <table cc-select="true">
                    <tr><th>算法</th><th>最好情况</th><th>平均情况</th><th>最坏情况</th></tr>
                    <tr><td>快速排序</td><td>O(n log n)</td><td>O(n log n)</td><td>O(n²)</td></tr>
                    <tr><td>归并排序</td><td>O(n log n)</td><td>O(n log n)</td><td>O(n log n)</td></tr>
                    <tr><td>冒泡排序</td><td>O(n)</td><td>O(n²)</td><td>O(n²)</td></tr>
                </table>
                <p cc-select="true">Master定理：T(n) = aT(n/b) + f(n)</p>
                <p cc-select="true">其中 a ≥ 1, b > 1 是常数，f(n) 是正函数。</p>
            </body></html>''',
            "groundtruth_content": '''# 算法复杂度分析

这里介绍常见算法的时间复杂度。

## 快速排序实现

```python
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quicksort(left) + middle + quicksort(right)
```

## 复杂度对比

| 算法 | 最好情况 | 平均情况 | 最坏情况 |
|------|----------|----------|----------|
| 快速排序 | O(n log n) | O(n log n) | O(n²) |
| 归并排序 | O(n log n) | O(n log n) | O(n log n) |
| 冒泡排序 | O(n) | O(n²) | O(n²) |

Master定理：$T(n) = aT(n/b) + f(n)$

其中 $a \\geq 1, b > 1$ 是常数，$f(n)$ 是正函数。''',
            "groundtruth_content_list": [
                {"type": "heading", "content": "算法复杂度分析", "level": 1},
                {"type": "paragraph", "content": "这里介绍常见算法的时间复杂度。"},
                {"type": "heading", "content": "快速排序实现", "level": 2},
                {"type": "code", "content": "def quicksort(arr):\n    if len(arr) <= 1:\n        return arr\n    \n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    \n    return quicksort(left) + middle + quicksort(right)"},
                {"type": "heading", "content": "复杂度对比", "level": 2},
                {"type": "table", "content": "| 算法 | 最好情况 | 平均情况 | 最坏情况 |\n|------|----------|----------|----------|\n| 快速排序 | O(n log n) | O(n log n) | O(n²) |\n| 归并排序 | O(n log n) | O(n log n) | O(n log n) |\n| 冒泡排序 | O(n) | O(n²) | O(n²) |"},
                {"type": "equation-inline", "content": "T(n) = aT(n/b) + f(n)"},
                {"type": "paragraph", "content": "其中 a ≥ 1, b > 1 是常数，f(n) 是正函数。"}
            ],
            "url": "https://algorithm-guide.cs.edu/complexity-analysis",
            "layout_id": "algorithm-guide_4",
            "max_layer_n": 14,
            "url_host_name": "algorithm-guide.cs.edu",
            "raw_warc_path": "s3://cc-raw-computer-science/crawl-data/CC-MAIN-2025-13/segments/1742004433093.21/warc/algo-004.warc.gz",
            "language": "zh",
            "__dom_depth": 16,
            "__dom_width": 7320,
            "__type": "__computer_science",
            "__tag": "ALGORITHM_CONTENT",
            "marked_type": "normal",
            "content_type": "computer_science"
        }
    ]
    
    # 创建数据集
    dataset = BenchmarkDataset(name="sample_dataset", description="示例评测数据集")
    
    for sample_data in samples:
        sample = DataSample.from_dict(sample_data)
        dataset.add_sample(sample)
    
    return dataset


def demo_basic_evaluation():
    """演示基本评测流程"""
    
    print("=== WebMainBench 基本使用示例 ===\n")
    
    # 设置日志
    setup_logging(level="INFO")
    
    # 1. 创建或加载数据集
    print("1. 创建示例数据集...")
    dataset = create_sample_dataset()
    print(f"数据集包含 {len(dataset)} 个样本")
    print(f"数据集统计: {dataset.get_statistics()}\n")
    
    # 2. 保存数据集到文件
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    dataset_path = data_dir / "sample_dataset.jsonl"
    DataSaver.save_jsonl(dataset, dataset_path, include_results=False)
    print(f"数据集已保存到: {dataset_path}\n")
    
    # 3. 重新加载数据集
    print("2. 重新加载数据集...")
    loaded_dataset = DataLoader.load_jsonl(dataset_path)
    print(f"加载的数据集包含 {len(loaded_dataset)} 个样本\n")
    
    # 4. 列出可用的抽取器
    print("3. 可用的抽取器:")
    available_extractors = ExtractorFactory.list_available()
    for extractor_name in available_extractors:
        print(f"  - {extractor_name}")
    print()
    
    # 5. 创建评测器
    print("4. 创建评测器...")
    evaluator = Evaluator()
    print(f"可用的评测指标: {evaluator.metric_calculator.list_available_metrics()}\n")
    
    # 6. 创建一个模拟抽取器进行演示
    print("5. 创建模拟抽取器...")
    
    from webmainbench.extractors import BaseExtractor, ExtractionResult
    
    class MockExtractor(BaseExtractor):
        """模拟抽取器，用于演示"""
        
        def _setup(self):
            pass
        
        def _extract_content(self, html, url=None):
            # 简单的模拟抽取逻辑
            if "标题" in html:
                content = "# 提取的标题\n\n提取的正文内容。"
                content_list = [
                    {"type": "heading", "content": "提取的标题", "level": 1},
                    {"type": "paragraph", "content": "提取的正文内容。"}
                ]
            else:
                content = "提取的内容"
                content_list = [{"type": "paragraph", "content": "提取的内容"}]
            
            return ExtractionResult(
                content=content,
                content_list=content_list,
                success=True,
                confidence_score=0.85
            )
    
    # 注册模拟抽取器
    ExtractorFactory.register("mock", MockExtractor)
    mock_extractor = ExtractorFactory.create("mock")
    print("模拟抽取器已创建\n")
    
    # 7. 运行评测
    print("6. 运行评测...")
    result = evaluator.evaluate(
        dataset=loaded_dataset,
        extractor=mock_extractor,
        max_samples=2  # 限制样本数量用于演示
    )
    
    # 8. 显示结果
    print("\n7. 评测结果:")
    print("=" * 50)
    formatted_results = format_results(result.to_dict())
    print(formatted_results)
    
    # 9. 保存结果
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    results_path = results_dir / "evaluation_results.json"
    DataSaver.save_evaluation_results(result.to_dict(), results_path)
    print(f"\n结果已保存到: {results_path}")
    
    # 10. 生成报告
    report_path = results_dir / "evaluation_report.csv"
    DataSaver.save_summary_report(result.to_dict(), report_path)
    print(f"报告已保存到: {report_path}")


def demo_extractor_comparison():
    """演示多抽取器对比"""
    
    print("\n=== 多抽取器对比演示 ===\n")
    
    # 创建数据集
    dataset = create_sample_dataset()
    
    # 创建多个模拟抽取器
    from webmainbench.extractors import BaseExtractor, ExtractionResult
    
    class ExtractorA(BaseExtractor):
        def _setup(self):
            pass
        def _extract_content(self, html, url=None):
            return ExtractionResult(
                content="抽取器A的结果",
                content_list=[{"type": "paragraph", "content": "抽取器A的结果"}],
                success=True,
                confidence_score=0.9
            )
    
    class ExtractorB(BaseExtractor):
        def _setup(self):
            pass
        def _extract_content(self, html, url=None):
            return ExtractionResult(
                content="抽取器B的结果",
                content_list=[{"type": "paragraph", "content": "抽取器B的结果"}],
                success=True,
                confidence_score=0.8
            )
    
    # 注册抽取器
    ExtractorFactory.register("extractor_a", ExtractorA)
    ExtractorFactory.register("extractor_b", ExtractorB)
    
    # 运行对比
    evaluator = Evaluator()
    extractors = ["extractor_a", "extractor_b"]
    
    results = evaluator.compare_extractors(
        dataset=dataset,
        extractors=extractors,
        max_samples=2
    )
    
    # 显示对比结果
    print("对比结果:")
    print("-" * 40)
    for extractor_name, result in results.items():
        overall_score = result.overall_metrics.get('overall', 0)
        print(f"{extractor_name}: {overall_score:.4f}")
    
    # 保存多抽取器对比榜单
    all_results = []
    for extractor_name, result in results.items():
        all_results.append(result.to_dict())
    
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    leaderboard_path = results_dir / "leaderboard.csv"
    DataSaver.save_summary_report(all_results, leaderboard_path)
    print(f"\n📊 榜单已保存到: {leaderboard_path}")


if __name__ == "__main__":
    try:
        demo_basic_evaluation()
        # demo_extractor_comparison()
        print("\n✅ 示例运行完成！")
        
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        import traceback
        traceback.print_exc() 
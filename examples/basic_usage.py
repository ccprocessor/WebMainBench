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


def demo_basic_mock_evaluation():
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
    
    results_path = results_dir / "mock_evaluation_results.json"
    DataSaver.save_evaluation_results(result, results_path)
    print(f"\n结果已保存到: {results_path}")
    
    # 10. 生成报告
    report_path = results_dir / "mock_evaluation_report.csv"
    DataSaver.save_summary_report(result, report_path)
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
                # content_list=[{"type": "paragraph", "content": "抽取器A的结果"}],
                success=True,
                confidence_score=0.9
            )
    
    class ExtractorB(BaseExtractor):
        def _setup(self):
            pass
        def _extract_content(self, html, url=None):
            return ExtractionResult(
                content="抽取器B的结果",
                # content_list=[{"type": "paragraph", "content": "抽取器B的结果"}],
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


def demo_llm_webkit_evaluation():
    """演示LLM-WebKit抽取器的6项指标评测"""
    
    print("=== LLM-WebKit Extractor 6项指标评测示例 ===\n")
    
    # 设置日志
    setup_logging(level="INFO")
    
    # 1. 创建包含各种内容类型的测试数据集
    print("1. 创建包含多种内容类型的测试数据集...")
    
    samples = []
    
    # 样本1: 包含文本和代码
    samples.append(DataSample(
        id="text_code_sample",
        html="""
        <html>
        <body>
            <h1>Python编程示例</h1>
            <p>这是一段关于Python编程的介绍文本。</p>
            <pre><code>
def hello_world():
    print("Hello, World!")
    return True
            </code></pre>
            <p>以上代码展示了一个简单的Python函数。</p>
        </body>
        </html>
        """,
        groundtruth_content="""# Python编程示例

这是一段关于Python编程的介绍文本。

```python
def hello_world():
    print("Hello, World!")
    return True
```

以上代码展示了一个简单的Python函数。""",
        groundtruth_content_list=[
            {"type": "heading", "content": "Python编程示例", "level": 1},
            {"type": "text", "content": "这是一段关于Python编程的介绍文本。"},
            {"type": "code", "content": "def hello_world():\n    print(\"Hello, World!\")\n    return True", "language": "python"},
            {"type": "text", "content": "以上代码展示了一个简单的Python函数。"}
        ]
    ))
    
    # 样本2: 包含表格
    samples.append(DataSample(
        id="table_sample",
        html="""
        <html>
        <body>
            <h2>销售数据统计</h2>
            <table>
                <thead>
                    <tr>
                        <th>产品</th>
                        <th>销量</th>
                        <th>收入</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>产品A</td>
                        <td>100</td>
                        <td>1000</td>
                    </tr>
                    <tr>
                        <td>产品B</td>
                        <td>200</td>
                        <td>3000</td>
                    </tr>
                </tbody>
            </table>
        </body>
        </html>
        """,
        groundtruth_content="""## 销售数据统计

| 产品 | 销量 | 收入 |
|------|------|------|
| 产品A | 100 | 1000 |
| 产品B | 200 | 3000 |""",
        groundtruth_content_list=[
            {"type": "heading", "content": "销售数据统计", "level": 2},
            {"type": "table", "content": "| 产品 | 销量 | 收入 |\n|------|------|------|\n| 产品A | 100 | 1000 |\n| 产品B | 200 | 3000 |"}
        ]
    ))
    
    # 样本3: 包含公式
    samples.append(DataSample(
        id="formula_sample",
        html="""
        <html>
        <body>
            <h2>数学公式示例</h2>
            <p>这是一个行内公式: $E = mc^2$</p>
            <p>这是一个行间公式:</p>
            <div>$$\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}$$</div>
        </body>
        </html>
        """,
        groundtruth_content="""## 数学公式示例

这是一个行内公式: $E = mc^2$

这是一个行间公式:

$$\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}$$""",
        groundtruth_content_list=[
            {"type": "heading", "content": "数学公式示例", "level": 2},
            {"type": "text", "content": "这是一个行内公式: $E = mc^2$"},
            {"type": "text", "content": "这是一个行间公式:"},
            {"type": "formula", "content": "\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}"}
        ]
    ))
    
    # 创建数据集并添加样本
    dataset = BenchmarkDataset(name="llm_webkit_test", description="LLM-WebKit 6项指标测试数据集")
    for sample in samples:
        dataset.add_sample(sample)
    
    print(f"测试数据集包含 {len(dataset)} 个样本")
    print(f"样本类型: 文本+代码, 表格, 公式\n")
    
    # 2. 创建LLM-WebKit抽取器
    print("2. 创建LLM-WebKit抽取器...")
    
    # 显示所有可用的抽取器
    available_extractors = ExtractorFactory.list_available()
    print(f"可用的抽取器: {available_extractors}")
    
    # 直接创建LLM-WebKit抽取器，设置模型路径
    config = {
        "model_path": "/Users/chupei/model/checkpoint-3296"
    }
    extractor = ExtractorFactory.create("llm-webkit", config=config)
    print(f"✅ LLM-WebKit抽取器创建成功，模型路径: {config['model_path']}")
    
    print()
    
    # 3. 创建评测器并显示所有可用指标
    print("3. 创建评测器...")
    evaluator = Evaluator()
    available_metrics = evaluator.metric_calculator.list_available_metrics()
    print(f"✅ 可用的评测指标 ({len(available_metrics)}项):")
    
    # 按照6项指标分类显示
    target_metrics = ["overall", "text_edit", "code_edit", "table_edit", "table_TEDS", "formula_edit"]
    
    for metric in target_metrics:
        if metric in available_metrics:
            print(f"  ✅ {metric}")
        else:
            print(f"  ❌ {metric} (未注册)")
    
    print()
    
    # 4. 运行评测
    print("4. 开始评测...")
    print("=" * 60)
    
    result = evaluator.evaluate(
        dataset=dataset,
        extractor=extractor,
        max_samples=None  # 评测所有样本
    )
    
    # 5. 显示详细的6项指标结果
    print("\n5. 📊 6项指标详细评测结果:")
    print("=" * 60)
    
    results_dict = result.to_dict()
    
    # 从overall_metrics中提取指标结果
    metrics = results_dict.get('overall_metrics', {})
    
    # 按照指标分类显示
    print(f"\n🏆 综合指标:")
    if 'overall' in metrics:
        print(f"  overall (综合得分): {metrics['overall']:.4f}")
    else:
        print("  overall: 未计算")
    
    print(f"\n📝 文本相关指标:")
    if 'text_edit' in metrics:
        print(f"  text_edit (文本编辑距离): {metrics['text_edit']:.4f}")
    else:
        print("  text_edit: 未计算")
    if 'code_edit' in metrics:
        print(f"  code_edit (代码编辑距离): {metrics['code_edit']:.4f}")
    else:
        print("  code_edit: 未计算")
    
    print(f"\n📊 表格相关指标:")
    if 'table_edit' in metrics:
        print(f"  table_edit (表格编辑距离): {metrics['table_edit']:.4f}")
    else:
        print("  table_edit: 未计算")
    if 'table_TEDS' in metrics:
        print(f"  table_TEDS (表格结构相似度): {metrics['table_TEDS']:.4f}")
    else:
        print("  table_TEDS: 未计算")
    
    print(f"\n🧮 公式相关指标:")
    if 'formula_edit' in metrics:
        print(f"  formula_edit (公式编辑距离): {metrics['formula_edit']:.4f}")
    else:
        print("  formula_edit: 未计算")
    
    print(f"\n📈 详细统计:")
    print(f"  总样本数: {len(dataset)}")
    success_count = len([s for s in results_dict.get('sample_results', []) if s.get('extraction_success', False)])
    failure_count = len(dataset) - success_count
    print(f"  成功样本数: {success_count}")
    print(f"  失败样本数: {failure_count}")
    
    # 6. 保存结果到文件
    print("\n" + "=" * 60)
    print("6. 保存评测结果...")
    
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    # 保存详细结果
    results_path = results_dir / "llm_webkit_evaluation_results.json"
    DataSaver.save_evaluation_results(result, results_path)  # 直接传递result对象
    print(f"✅ 详细结果已保存到: {results_path}")
    
    # 生成CSV报告
    report_path = results_dir / "llm_webkit_evaluation_report.csv"
    DataSaver.save_summary_report(result, report_path)  # 直接传递result对象
    print(f"✅ CSV报告已保存到: {report_path}")
    
    print("\n" + "=" * 60)
    print("✅ LLM-WebKit 6项指标评测完成！")


def demo_dataset_with_extraction():
    """演示保存带有抽取内容的数据集"""
    print("=== 演示：保存带有抽取内容的数据集 ===")
    
    from webmainbench import DataLoader, DataSaver, Evaluator, ExtractorFactory
    from pathlib import Path
    
    # 配置文件路径
    data_dir = Path("data")
    dataset_path = data_dir / "sample_dataset.jsonl"
    # dataset_path = "/Users/chupei/Downloads/WebMainBench_dataset_merge_2549.jsonl"
    
    print(f"📂 数据集文件: {dataset_path}")
    
    # 🔧 创建llm-webkit抽取器（统一使用）
    extractor_config = {"model_path": "/Users/chupei/model/checkpoint-3296"}
    extractor = ExtractorFactory.create("llm-webkit", config=extractor_config)
    print(f"🤖 使用抽取器: {extractor.name}")
    
    # 创建评测器
    evaluator = Evaluator()
    
    # 🔧 选择评测模式：内存模式 vs 批处理模式
    USE_BATCHED_MODE = True  # 设置为True使用批处理模式（适用于大数据集）
    
    if USE_BATCHED_MODE:
        print("🔄 使用批处理模式（内存优化）")
        
        # 🚀 批处理评测（适用于大数据集）
        result = evaluator.evaluate_batched(
            jsonl_file_path=dataset_path,
            extractor=extractor,  # 直接传递extractor对象
            batch_size=10,        # 小批次
            max_samples=20        # 演示用
        )
        print(f"✅ 批处理评测完成，总体得分: {result.overall_metrics.get('overall', 0):.4f}")
        
        # 为了保存带有抽取内容的数据集，需要重新加载原始数据集
        # 注：这里只是短暂加载用于保存，不影响前面的内存优化评测
        dataset = DataLoader.load_jsonl(dataset_path, include_results=False)
        dataset.name = result.dataset_name
            
    else:
        print("🔄 使用传统内存模式")
        
        # 从文件加载数据集
        print(f"📂 从文件加载数据集: {dataset_path}")
        dataset = DataLoader.load_jsonl(dataset_path, include_results=False)
        dataset.name = "WebMainBench_with_extraction"
        dataset.description = "演示抽取内容保存的测试数据集"
        
        print(f"📊 加载数据集完成，包含 {len(dataset.samples)} 个样本")
        
        # 运行评测
        result = evaluator.evaluate(dataset, extractor)
    
    print(f"✅ 评测完成，总体得分: {result.overall_metrics.get('overall', 0):.4f}")
    
    # 保存带有抽取内容的数据集
    results_dir = Path("results")
    enriched_dataset_path = results_dir / f"{dataset.name}_with_{extractor.name}_extraction.jsonl"
    
    DataSaver.save_dataset_with_extraction(
        results=result,
        dataset=dataset, 
        file_path=enriched_dataset_path,
        extractor_name=extractor.name
    )
    
    print(f"💾 已保存带有抽取内容的数据集到: {enriched_dataset_path}")
    
    # 保存评测结果和摘要报告
    evaluation_results_path = results_dir / f"{dataset.name}_{extractor.name}_evaluation_results.json"
    summary_report_path = results_dir / f"{dataset.name}_{extractor.name}_evaluation_report.csv"
    
    DataSaver.save_evaluation_results(result, evaluation_results_path)
    DataSaver.save_summary_report(result, summary_report_path)
    
    print(f"📊 已保存评测结果到: {evaluation_results_path}")
    print(f"📈 已保存摘要报告到: {summary_report_path}")
    
    # 显示保存的字段信息
    print("\n📋 保存的新字段包括:")
    print(f"  - {extractor.name}_content: 抽取的内容")
    print(f"  - {extractor.name}_content_list: 抽取的结构化内容列表")
    print(f"  - {extractor.name}_success: 抽取是否成功")
    print(f"  - {extractor.name}_time: 抽取耗时")
    print(f"  - {extractor.name}_*_score: 各项指标分数")


def demo_multi_extraction():
    """演示保存带有多个抽取器抽取内容的数据集（支持批处理模式）"""
    print("=== 演示：保存带有多个抽取器抽取内容的数据集 ===")

    from webmainbench import DataLoader, DataSaver, Evaluator, ExtractorFactory
    from pathlib import Path
    import time


    # 设置日志
    setup_logging(level="INFO")

    # 配置文件路径
    data_dir = Path("../data")
    # dataset_path = data_dir / "sample_dataset.jsonl"
    dataset_path = "/home/lulindong/Pycharm_projects/cc/WebMainBench_llm-webkit_v1_WebMainBench_dataset_merge_with_llm_webkit.jsonl"

    print(f"📂 数据集文件: {dataset_path}")

    # 🔧 定义要使用的抽取器列表及配置
    extractors_info = [
        {"name": "resiliparse", "config": {
            "main_content": True,
            "alt_texts": True,
            "links": False,
            "list_bullets": True,
            "preserve_formatting": True
        }},
        {"name": "trafilatura", "config": {}},
        {"name": "magic-html", "config": {}},
    ]

    # 🔧 选择评测模式：内存模式 vs 批处理模式
    USE_BATCHED_MODE = True  # 大数据集建议设为True
    BATCH_SIZE = 10  # 批处理大小
    MAX_SAMPLES = None  # 演示用（全量评测可设为None）

    # 创建结果目录
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    # 存储所有抽取器的评测结果和性能数据
    all_results = []
    extractor_performance = []

    # 为每个抽取器运行评测
    for info in extractors_info:
        extractor_name = info["name"]
        config = info["config"]

        try:
            # 创建抽取器实例
            extractor = ExtractorFactory.create(extractor_name, config=config)
            print(f"\n🤖 使用抽取器: {extractor.name}")
        except Exception as e:
            print(f"⚠️ {extractor_name} 抽取器创建失败: {e}")
            continue

        # 记录总耗时
        start_time = time.time()

        # 初始化评测器
        evaluator = Evaluator()

        # 选择批处理模式或传统模式
        if USE_BATCHED_MODE:
            print(f"🔄 使用批处理模式（批大小: {BATCH_SIZE}，最大样本: {MAX_SAMPLES or '全部'}）")
            # 批处理评测（内存优化）
            result = evaluator.evaluate_batched(
                jsonl_file_path=dataset_path,
                extractor=extractor,
                batch_size=BATCH_SIZE,
                max_samples=MAX_SAMPLES
            )
            # 为保存数据集，临时加载原始数据（不影响内存优化）
            dataset = DataLoader.load_jsonl(dataset_path, include_results=False, max_samples=MAX_SAMPLES)
            dataset.name = result.dataset_name
        else:
            print("🔄 使用传统内存模式")
            # 加载完整数据集到内存
            dataset = DataLoader.load_jsonl(dataset_path, include_results=False, max_samples=MAX_SAMPLES)
            dataset.name = "WebMainBench_with_multi_extraction"
            dataset.description = "多抽取器内容保存演示数据集"
            print(f"📊 加载数据集完成，包含 {len(dataset.samples)} 个样本")

            # 传统模式评测
            result = evaluator.evaluate(dataset, extractor)

        # 计算耗时指标
        total_time = time.time() - start_time
        total_samples = len(dataset.samples)
        avg_time_per_sample = total_time / total_samples if total_samples else 0

        # 保存性能数据
        extractor_performance.append({
            "name": extractor_name,
            "total_samples": total_samples,
            "total_time": total_time,
            "avg_time_per_sample": avg_time_per_sample
        })

        # 输出评测结果
        print(f"⏱️ 总耗时: {total_time:.4f}秒（单样本平均: {avg_time_per_sample:.4f}秒）")
        print(f"📊 核心指标:")
        print(f"   code_edit: {result.overall_metrics.get('code_edit', 0):.4f}")
        print(f"   formula_edit: {result.overall_metrics.get('formula_edit', 0):.4f}")
        print(f"   table_TEDS: {result.overall_metrics.get('table_TEDS', 0):.4f}")
        print(f"   table_edit: {result.overall_metrics.get('table_edit', 0):.4f}")
        print(f"   text_edit: {result.overall_metrics.get('text_edit', 0):.4f}")
        print(f"✅ 总体得分: {result.overall_metrics.get('overall', 0):.4f}")

        all_results.append(result)

        # 保存带有当前抽取器内容的数据集
        enriched_dataset_path = results_dir / f"{dataset.name}_{extractor.name}_extraction_infer.jsonl"
        DataSaver.save_dataset_with_extraction(
            results=result,
            dataset=dataset,
            file_path=enriched_dataset_path,
            extractor_name=extractor.name
        )
        print(f"💾 已保存抽取内容到: {enriched_dataset_path}")

        # 保存单个抽取器的评测结果
        eval_results_path = results_dir / f"{dataset.name}_{extractor.name}_evaluation_results.json"
        DataSaver.save_evaluation_results(result, eval_results_path)
        print(f"📋 已保存评测结果到: {eval_results_path}")

    # 保存所有抽取器的汇总报告
    if all_results:
        summary_path = results_dir / f"{dataset.name}_multi_extractors_summary_report.csv"
        DataSaver.save_summary_report(all_results, summary_path)
        print(f"\n📈 已保存汇总报告到: {summary_path}")

    # 展示性能对比
    if extractor_performance:
        print("\n⚡ 抽取器性能对比:")
        for perf in extractor_performance:
            print(f"  {perf['name']}:")
            print(f"    样本数: {perf['total_samples']}")
            print(f"    总耗时: {perf['total_time']:.4f}秒")
            print(f"    单样本耗时: {perf['avg_time_per_sample']:.4f}秒")
            print(f"    效率: {1 / perf['avg_time_per_sample']:.2f}样本/秒")

    # 展示保存的字段信息
    print("\n📋 保存的新字段说明:")
    for info in extractors_info:
        name = info["name"]
        print(f"  {name}相关字段:")
        print(f"    - {name}_content: 抽取的原始内容")
        print(f"    - {name}_content_list: 结构化内容列表（含type字段）")
        print(f"    - {name}_success: 抽取是否成功（布尔值）")
        print(f"    - {name}_time: 单样本抽取耗时（秒）")
        print(f"    - {name}_*_score: 各指标得分（如{name}_text_edit）")


def demo_llm_webkit_with_preprocessed_html_evaluation():
    """演示LLM-WebKit预处理HTML功能的评测"""
    
    print("\n=== LLM-WebKit 预处理HTML功能演示 ===\n")
    
    # 设置日志
    setup_logging(level="INFO")
    
    # 1. 创建包含预处理HTML的测试数据集
    print("1. 创建包含预处理HTML的测试数据集...")
    
    samples = []
    
    # 样本1: 包含预处理的HTML（模拟第一阶段LLM简化后的结果）
    sample_1_data = {
        "id": "preprocessed_sample_1",
        "html": """<html><body><h1>原始复杂HTML</h1><p>这里是原始的复杂HTML内容...</p></body></html>""",
        # 这是关键：包含llm_webkit_html字段（预处理后的简化HTML）
        "llm_webkit_html": """
        <div _item_id="1">
            <h1>深度学习基础教程</h1>
            <p>深度学习是机器学习的一个重要分支，通过多层神经网络来学习数据的表征。</p>
        </div>
        <div _item_id="2">
            <h2>核心概念</h2>
            <p>神经网络由多个层组成，每层包含多个神经元。</p>
        </div>
        <div _item_id="3">
            <pre><code class="language-python">
import torch
import torch.nn as nn

class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(784, 10)
    
    def forward(self, x):
        return self.fc(x)
            </code></pre>
        </div>
        """,
        "groundtruth_content": """# 深度学习基础教程

深度学习是机器学习的一个重要分支，通过多层神经网络来学习数据的表征。

## 核心概念

神经网络由多个层组成，每层包含多个神经元。

```python
import torch
import torch.nn as nn

class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(784, 10)
    
    def forward(self, x):
        return self.fc(x)
```""",
        "groundtruth_content_list": [
            {"type": "heading", "content": "深度学习基础教程", "level": 1},
            {"type": "paragraph", "content": "深度学习是机器学习的一个重要分支，通过多层神经网络来学习数据的表征。"},
            {"type": "heading", "content": "核心概念", "level": 2},
            {"type": "paragraph", "content": "神经网络由多个层组成，每层包含多个神经元。"},
            {"type": "code", "content": "import torch\nimport torch.nn as nn\n\nclass SimpleNet(nn.Module):\n    def __init__(self):\n        super().__init__()\n        self.fc = nn.Linear(784, 10)\n    \n    def forward(self, x):\n        return self.fc(x)", "language": "python"}
        ]
    }
    # samples.append(DataSample.from_dict(sample_1_data))
    
    # 样本2: 包含表格的预处理HTML
    sample_2_data = {
        "id": "preprocessed_sample_2", 
        "html": """<html><body><h1>原始表格页面</h1><table>...</table></body></html>""",
        "llm_webkit_html": """
        <div _item_id="1">
            <h1>模型性能对比</h1>
            <p>以下是不同深度学习模型在CIFAR-10数据集上的表现：</p>
        </div>
        <div _item_id="2">
            <table>
                <thead>
                    <tr>
                        <th>模型</th>
                        <th>准确率</th>
                        <th>参数量</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>ResNet-18</td>
                        <td>95.3%</td>
                        <td>11.7M</td>
                    </tr>
                    <tr>
                        <td>VGG-16</td>
                        <td>92.7%</td>
                        <td>138M</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """,
        "groundtruth_content": """# 模型性能对比

以下是不同深度学习模型在CIFAR-10数据集上的表现：

| 模型 | 准确率 | 参数量 |
|------|--------|--------|
| ResNet-18 | 95.3% | 11.7M |
| VGG-16 | 92.7% | 138M |""",
        "groundtruth_content_list": [
            {"type": "heading", "content": "模型性能对比", "level": 1},
            {"type": "paragraph", "content": "以下是不同深度学习模型在CIFAR-10数据集上的表现："},
            {"type": "table", "content": "| 模型 | 准确率 | 参数量 |\n|------|--------|---------|\n| ResNet-18 | 95.3% | 11.7M |\n| VGG-16 | 92.7% | 138M |"}
        ]
    }
    # samples.append(DataSample.from_dict(sample_2_data))
    #
    # # 创建数据集并添加样本
    # dataset = BenchmarkDataset(name="preprocessed_html_test", description="预处理HTML功能测试数据集")



    # 本地加载数据集
    jsonl_file_path = "/home/lulindong/Pycharm_projects/cc/WebMainBench_llm-webkit_v1_WebMainBench_dataset_merge_with_llm_webkit.jsonl"

    # 使用DataLoader加载本地JSONL数据
    dataset = DataLoader.load_jsonl(jsonl_file_path)
    for sample in samples:
        dataset.add_sample(sample)
    
    print(f"✅ 测试数据集包含 {len(dataset)} 个样本")
    print("📋 每个样本都包含:")
    print("  - html: 原始复杂HTML")
    print("  - llm_webkit_html: 预处理后的简化HTML（包含_item_id标记）")
    print("  - groundtruth_content: 标准答案")
    print()
    
    # 2. 创建预处理HTML模式的LLM-WebKit抽取器
    print("2. 创建预处理HTML模式的LLM-WebKit抽取器...")
    
    config = {
        "use_preprocessed_html": True,          # 🔑 关键配置：启用预处理HTML模式
        "preprocessed_html_field": "llm_webkit_html"  # 指定预处理HTML字段名
    }
    
    extractor = ExtractorFactory.create("llm-webkit", config=config)
    print(f"✅ 抽取器创建成功")
    print(f"📋 配置信息:")
    print(f"  - use_preprocessed_html: {extractor.inference_config.use_preprocessed_html}")
    print(f"  - preprocessed_html_field: {extractor.inference_config.preprocessed_html_field}")
    print(f"  - 跳过LLM推理: 是（直接处理预处理HTML）")
    print()
    
    # 3. 性能对比：展示预处理HTML模式的优势
    print("3. 性能优势演示...")
    print("🚀 预处理HTML模式的优势:")
    print("  ✅ 无需加载大型LLM模型（节省内存）")
    print("  ✅ 跳过HTML简化推理步骤（节省时间）")
    print("  ✅ 只需要基础的llm_web_kit依赖")
    print("  ✅ 适合批量处理已预处理的数据")
    print()
    
    # 4. 运行评测
    print("4. 开始评测...")
    print("=" * 50)
    
    evaluator = Evaluator()
    result = evaluator.evaluate(
        dataset=dataset,
        extractor=extractor,
        max_samples=None
    )
    
    # 5. 显示评测结果
    print("\n5. 📊 预处理HTML模式评测结果:")
    print("=" * 50)
    
    results_dict = result.to_dict()
    metrics = results_dict.get('overall_metrics', {})
    
    # 显示关键指标
    print(f"\n🏆 综合指标:")
    print(f"  overall: {metrics.get('overall', 0):.4f}")
    
    print(f"\n📝 内容提取质量:")
    print(f"  text_edit: {metrics.get('text_edit', 0):.4f}")
    print(f"  code_edit: {metrics.get('code_edit', 0):.4f}")
    print(f"  table_edit: {metrics.get('table_edit', 0):.4f}")
    print(f"  table_TEDS: {metrics.get('table_TEDS', 0):.4f}")
    
    print(f"\n⚡ 性能统计:")
    sample_results = results_dict.get('sample_results', [])
    if sample_results:
        extraction_times = [s.get('extraction_time', 0) for s in sample_results if s.get('extraction_success')]
        if extraction_times:
            avg_time = sum(extraction_times) / len(extraction_times)
            print(f"  平均提取时间: {avg_time:.3f}秒")
            print(f"  处理速度: {1/avg_time:.1f}样本/秒")
    
    success_count = len([s for s in sample_results if s.get('extraction_success', False)])
    print(f"  成功样本数: {success_count}/{len(dataset)}")
    
    # 6. 展示样本提取结果
    print(f"\n6. 📄 样本提取结果预览:")
    print("-" * 50)
    
    for i, sample_result in enumerate(sample_results[:2]):  # 只显示前2个样本
        print(f"\n样本 {i+1}: {sample_result.get('sample_id', 'Unknown')}")
        if sample_result.get('extraction_success'):
            content = sample_result.get('extracted_content', '')
            preview = content[:100].replace('\n', ' ') if content else '无内容'
            print(f"  ✅ 提取成功")
            print(f"  📝 内容预览: {preview}...")
            print(f"  ⏱️  提取时间: {sample_result.get('extraction_time', 0):.3f}秒")
        else:
            print(f"  ❌ 提取失败")
    
    # 7. 保存结果
    print(f"\n7. 💾 保存评测结果...")
    
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    results_path = results_dir / "preprocessed_html_evaluation_results.json"
    report_path = results_dir / "preprocessed_html_evaluation_report.csv"
    
    DataSaver.save_evaluation_results(result, results_path)
    DataSaver.save_summary_report(result, report_path)
    
    print(f"✅ 详细结果已保存到: {results_path}")
    print(f"✅ CSV报告已保存到: {report_path}")
    
    # 8. 使用建议
    print(f"\n8. 💡 实际使用建议:")
    print("=" * 50)
    print("🔧 何时使用预处理HTML模式:")
    print("  1. 已有LLM简化后的HTML数据")
    print("  2. 需要批量处理大量数据")
    print("  3. 部署环境内存有限")
    print("  4. 对提取速度有较高要求")
    print()
    print("📝 数据准备要求:")
    print("  1. 确保预处理HTML包含_item_id属性")
    print("  2. 保持原始HTML作为备用")
    print("  3. 验证预处理质量")
    print()
    print("⚙️  配置参数说明:")
    print("  - use_preprocessed_html: True/False")
    print("  - preprocessed_html_field: 字段名（默认'llm_webkit_html'）")
    
    print("\n✅ 预处理HTML功能演示完成！")


if __name__ == "__main__":
    try:
        # demo_basic_mock_evaluation()
        # demo_llm_webkit_evaluation()  # 使用LLM-WebKit评测示例
        demo_llm_webkit_with_preprocessed_html_evaluation()
        # demo_extractor_comparison()
        # demo_dataset_with_extraction()  # 演示保存带有抽取内容的数据集
        # demo_multi_extraction() # 演示多个抽取器同时评测
        # demo_lld_workers_extraction()
        print("\n✅ 示例运行完成！")
        
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        import traceback
        traceback.print_exc() 
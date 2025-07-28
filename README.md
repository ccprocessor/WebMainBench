# WebMainBench

WebMainBench 是一个专门用于评测网页正文抽取质量的综合性基准测试工具。

## 功能特点

### 🎯 **核心功能**
- **多抽取器支持**: 支持 LLM-WebKit、Unstructured、Jina AI 等多种抽取工具
- **全面的评测指标**: 包含文本相似度、表格抽取、公式识别、结构保持等多维度指标
- **灵活的数据格式**: 支持 JSONL、JSON 等多种数据格式
- **人工标注支持**: 支持 `cc-select="true"` 标注的 groundtruth 数据

### 📊 **评测指标**
- **文本指标**: 编辑距离、BLEU、ROUGE 等
- **表格指标**: 表格结构识别准确率
- **公式指标**: 数学公式抽取质量
- **结构指标**: 内容层次结构保持度

#### 指标详细说明

| 指标名称 | 中文名称 | 取值范围 | 说明 |
|---------|----------|----------|------|
| `overall` | 综合得分 | 0.0-1.0 | 基于编辑距离的整体抽取质量，1.0表示完全匹配 |
| `table_extraction` | 表格抽取质量 | 0.0-1.0 | 表格结构和内容抽取准确性 |
| `formula_extraction` | 公式抽取质量 | 0.0-1.0 | 数学公式识别和抽取准确性 |

#### CSV榜单字段说明

评测完成后会生成CSV格式的榜单文件，包含以下字段：

| CSV列名 | 中文名称 | 说明 |
|---------|----------|------|
| `extractor` | 抽取器名称 | 被评测的抽取器标识 |
| `total_samples` | 总样本数 | 评测的样本总数 |
| `success_rate` | 成功率 | 成功处理的样本比例 (0.0-1.0) |
| `overall` | 综合得分 | 基于编辑距离的整体抽取质量 (越高越好) |
| `table_extraction` | 表格抽取得分 | 表格处理能力 (越高越好) |
| `formula_extraction` | 公式抽取得分 | 数学公式处理能力 (越高越好) |

**排序规则**: 榜单按 `overall` 综合得分降序排列，得分越高排名越靠前。

### 🔧 **核心模块**
1. **data 模块**: 评测集文件和结果的读写管理
2. **extractors 模块**: 各种抽取工具的统一接口
3. **metrics 模块**: 评测指标的计算实现
4. **evaluator 模块**: 评测任务的执行和结果输出

## 快速开始

### 安装

```bash
# 基础安装
pip install webmainbench

# 安装所有可选依赖
pip install webmainbench[all]

# 开发环境安装
pip install webmainbench[dev]
```

### 基本使用

```python
from webmainbench import DataLoader, Evaluator, ExtractorFactory

# 1. 加载评测数据集
dataset = DataLoader.load_jsonl("your_dataset.jsonl")

# 2. 创建抽取器
extractor = ExtractorFactory.create("llm-webkit")

# 3. 运行评测
evaluator = Evaluator()
result = evaluator.evaluate(dataset, extractor)

# 4. 查看结果
print(f"Overall Score: {result.overall_metrics['overall']:.4f}")
```

### 数据格式

评测数据集应包含以下字段：

```jsonl
{
  "track_id": "0b7f2636-d35f-40bf-9b7f-94be4bcbb396",
  "html": "<html><body><h1 cc-select="true">这是标题</h1></body></html>",   # 人工标注带cc-select="true" 属性
  "groundtruth_content": "# 标题\n\n正文内容",
  "groundtruth_content_list": [
      {"type": "heading", "content": "标题", "level": 1},
      {"type": "paragraph", "content": "正文内容"}
   ],
  "url": "https://orderyourbooks.com/product-category/college-books-p-u/?products-per-page=all",
  "layout_id": "orderyourbooks.com_4",
  "max_layer_n": 10,
  "url_host_name": "orderyourbooks.com",
  "raw_warc_path": "s3://cc-raw-huawei/crawl-data/CC-MAIN-2025-13/segments/1742004433093.21/warc/CC-MAIN-20250319080618-20250319110618-00909.warc.gz?bytes=461610805,172252",
  "language": "en",
  "__dom_depth": 19,
  "__dom_width": 10231,
  "__type": "__max_depth",
  "__tag": "DOM_WIDTH",
  "marked_type": "unwanted",  # normal：正常标注的网页；unable：正文内容无法抉择；unwanted：无需标注的网页；
  "unwanted_reason": "list"
}
```

## 支持的抽取器

- **LLM-WebKit**: 基于大语言模型的智能抽取
- **Jina AI**: Reader API 服务
- **自定义抽取器**: 通过继承 `BaseExtractor` 实现


## 高级功能

### 多抽取器对比

```python
# 对比多个抽取器
extractors = ["llm-webkit", "unstructured", "jina"]
results = evaluator.compare_extractors(dataset, extractors)

for name, result in results.items():
    print(f"{name}: {result.overall_metrics['overall']:.4f}")
```

### 自定义指标

```python
from webmainbench.metrics import BaseMetric, MetricResult

class CustomMetric(BaseMetric):
    def _setup(self):
        pass
    
    def _calculate_score(self, predicted, groundtruth, **kwargs):
        # 实现自定义评测逻辑
        score = your_calculation(predicted, groundtruth)
        return MetricResult(
            metric_name=self.name,
            score=score,
            details={"custom_info": "value"}
        )

# 添加到评测器
evaluator.metric_calculator.add_metric("custom", CustomMetric("custom"))
```

### 自定义抽取器

```python
from webmainbench.extractors import BaseExtractor, ExtractionResult

class MyExtractor(BaseExtractor):
    def _setup(self):
        # 初始化抽取器
        pass
    
    def _extract_content(self, html, url=None):
        # 实现抽取逻辑
        content = your_extraction_logic(html)
        
        return ExtractionResult(
            content=content,
            content_list=[...],
            success=True
        )

# 注册自定义抽取器
ExtractorFactory.register("my-extractor", MyExtractor)
```

## 项目架构

```
webmainbench/
├── data/           # 数据处理模块
│   ├── dataset.py  # 数据集类
│   ├── loader.py   # 数据加载器
│   └── saver.py    # 数据保存器
├── extractors/     # 抽取器模块
│   ├── base.py     # 基础接口
│   ├── factory.py  # 工厂模式
│   └── ...         # 具体实现
├── metrics/        # 指标模块
│   ├── base.py     # 基础接口
│   ├── text_metrics.py    # 文本指标
│   ├── table_metrics.py   # 表格指标
│   └── calculator.py      # 指标计算器
├── evaluator/      # 评估器模块
│   └── evaluator.py       # 主评估器
└── utils/          # 工具模块
    └── helpers.py          # 辅助函数
```


## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

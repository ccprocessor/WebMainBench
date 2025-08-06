# 2025-08-06 代码更新说明

## 1. 支持 `md` 字段的内容提取与对比（详细说明）

- 在 `BaseMetric._extract_from_content_list` 和 `BaseMetric._extract_from_markdown` 这两个核心内容提取方法的输出结果中，新增了 `md` 字段。该字段用于存放原始的 markdown 文本内容，便于后续直接对比结构化提取与原文内容的一致性。  
  - 对于 `content_list`，`md` 字段会将结构化内容还原为 markdown 格式，尽可能保留原有的排版和语义信息。
  - 对于 `markdown`，`md` 字段则直接返回原始的 markdown 文本。

- 在 `examples/test_content_list.py` 脚本中，针对同一份数据，分别用 `content_list` 和 `markdown` 两种方式提取内容，并对比以下五个字段的内容相似度：`code`（代码）、`formula`（公式）、`table`（表格）、`text`（纯文本）、`md`（markdown 原文）。  
  - 脚本会遍历数据集中的每个样本，分别提取上述字段，并计算两种方式下每个字段的相似度（如字符级、token级等）。
  - 对于相似度低于设定阈值（如 0.8）的样本，会详细输出这些样本的 id 及对应字段的内容差异，方便开发者定位和排查问题。
  - 除了输出差异较大的样本外，还会统计每个字段的整体相似度分布（如均值、最小值、最大值、标准差等），帮助评估整体一致性。

- 针对每个字段，脚本还会统计以下情况：
  - 字段内容为空的样本数量（分别统计 content_list 和 markdown 两种方式下的空值情况）。
  - 两种方式都存在该字段内容时的相似度分布，便于分析结构化提取和原文内容在不同类型字段上的表现差异。

- 通过上述详细的对比和统计，开发者可以更直观地了解 `content_list` 与 `markdown` 两种结构化方式在各类内容上的一致性、差异点及潜在问题，为后续算法优化和数据清洗提供数据支持。

## 2. 其他相关脚本说明

- `examples/test_id_data.py`  
  支持通过指定样本 id 检查单个样本的 `content_list` 结构分布，并可用于调试内容提取效果。脚本会输出该样本的 `content_list` 类型分布统计，便于分析结构化内容的组成情况。可辅助定位某些特殊样本的结构异常或内容缺失问题。

- `examples/table_test.py`  
  用于在数据集中查找包含特定 `__tag`（如 `TABLE_TEXT_RATIO`、`TABLE_HTML_SOURCE_RATIO`、`TABLE_AT_DOM_DEPTH` 等）的样本。脚本会遍历所有样本，筛选出含有目标 `__tag` 的样本 id，并输出相关信息，便于分析表格相关内容的分布和特征，辅助后续表格提取与评测。

- `examples/test_dataset.py`  
  用于批量统计数据集中各字段（如 `code`、`formula`、`table`、`text`）的提取一致性。脚本会对比 `content_list` 和 `markdown` 两种提取方式下各字段的内容相似度，统计相似度低于阈值的样本数量，并输出部分差异较大的样本，便于整体质量评估和问题定位。

- `examples/test_direct_extraction.py`  
  提供一个简单的用例，直接用模拟的 `content_list` 数据结构测试内容提取方法。可用于验证 `BaseMetric._extract_from_content_list` 的基本功能和输出格式，适合开发调试和单元测试。

- `examples/statics.py`  
  提供 `Statics` 类，用于统计 `content_list` 中各类型元素的分布情况。可作为分析数据结构、辅助数据清洗和特征工程的工具脚本。

- `examples/test_content_list.py`  
  用于批量对比 `content_list` 与 `markdown` 两种提取方式下的 `code`、`formula`、`table`、`text`、`md` 五个字段的内容相似度。脚本会输出每个字段的相似度分布、为空的情况，以及差异较大的样本，便于深入分析两种结构化方式的优缺点和一致性问题。

## 3. 主要用途

- 方便开发者对比 `content_list` 与 `markdown` 两种结构化提取方式的差异，定位不一致或异常样本。
- 为后续优化内容提取算法、提升数据一致性提供数据支持。

## 4. 注意事项

- 新增的 `md` 字段仅在新版提取方法中支持，老数据或老方法不一定包含。
- 统计脚本默认数据路径为 `WebMainBench/data/WebMainBench_llm-webkit_v1_WebMainBench_dataset_merge_with_llm_webkit.jsonl`，如有变动请自行调整。

如有问题请联系开发者。

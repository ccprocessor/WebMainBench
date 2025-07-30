# LLM-WebKit Extractor 使用指南

## 概述

LLM-WebKit Extractor集成了大语言模型（LLM）推理能力，能够智能地理解HTML结构并准确提取主要内容。

## 安装依赖

```bash
# 基础依赖
pip install torch transformers

# VLLM推理引擎
pip install vllm

# LLM-WebKit HTML处理
pip install llm_web_kit

# 可选：加速库
pip install flash-attn  # GPU加速
```

## 基本使用

### 1. 创建Extractor

```python
from webmainbench.extractors import ExtractorFactory

# 使用默认配置
extractor = ExtractorFactory.create("llm-webkit")

# 使用自定义配置
config = {
    "model_path": "/Users/chupei/model/checkpoint-3296",
    "use_logits_processor": True,
    "temperature": 0.0,
    "max_item_count": 500
}
extractor = ExtractorFactory.create("llm-webkit", config=config)
```

### 2. 提取内容

```python
html_content = """
<html>
<body>
    <nav _item_id="1">导航菜单</nav>
    <main _item_id="2">主要文章内容</main>
    <aside _item_id="3">侧边栏广告</aside>
</body>
</html>
"""

result = extractor.extract(html_content)

if result.success:
    print(f"提取的内容: {result.content}")
    print(f"置信度: {result.confidence_score}")
    print(f"分类结果: {result.metadata['classification_result']}")
else:
    print(f"提取失败: {result.error_message}")
```

## 配置选项

### LLMInferenceConfig 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `model_path` | str | `"/share/liukaiwen/models/qwen3-0.6b/checkpoint-3296"` | LLM模型路径 |
| `use_logits_processor` | bool | `True` | 是否启用JSON格式约束 |
| `max_tokens` | int | `32768` | 最大输入token数 |
| `temperature` | float | `0.0` | 采样温度（0=确定性输出） |
| `top_p` | float | `0.95` | 核采样参数 |
| `max_output_tokens` | int | `8192` | 最大输出token数 |
| `tensor_parallel_size` | int | `1` | 张量并行大小 |
| `dtype` | str | `"bfloat16"` | 模型精度 |
| `max_item_count` | int | `1000` | 处理的最大item数量 |

### 模式配置示例

#### 快速模式（适合批量处理）
```python
fast_config = {
    "use_logits_processor": False,  # 禁用格式约束提高速度
    "temperature": 0.0,
    "max_item_count": 200,
    "max_output_tokens": 2048,
    "dtype": "float16"  # 更快的精度
}
```

#### 精确模式（适合高质量提取）
```python
precise_config = {
    "use_logits_processor": True,  # 启用格式约束
    "temperature": 0.0,
    "max_item_count": 1000,
    "max_output_tokens": 8192,
    "dtype": "bfloat16"  # 更好的精度
}
```

#### 分布式模式（多GPU）
```python
distributed_config = {
    "tensor_parallel_size": 4,  # 使用4个GPU
    "dtype": "bfloat16",
    "max_item_count": 2000,  # 可以处理更复杂的HTML
}
```

## 工作流程详解

### 1. HTML预处理
```python
# 使用llm_web_kit简化HTML结构
simplified_html, raw_tag_html, _ = simplify_html(original_html)
```

### 2. 复杂度检查
```python
item_count = simplified_html.count('_item_id')
if item_count > max_item_count:
    # 跳过过于复杂的HTML
    return error_result
```

### 3. LLM推理
```python
# 创建分类提示
prompt = create_classification_prompt(simplified_html)

# 使用VLLM生成分类结果
output = model.generate(prompt, sampling_params)
classification = parse_json_output(output)
```

### 4. 内容重建
```python
# 根据分类结果重建主要内容
main_content, content_list = reconstruct_content(
    original_html, classification
)
```

## 提示工程

### 分类标准

**主要内容 ("main")**:
- 文章正文、博客内容
- 问答的问题和答案
- 论坛的主要讨论内容
- 嵌入的相关图片和媒体

**辅助内容 ("other")**:
- 导航菜单、侧边栏、页脚
- 元数据（作者、时间、浏览量等）
- 广告和推广内容
- 相关推荐和建议内容

### 自定义提示模板

如果需要修改分类逻辑，可以继承类并重写提示模板：

```python
class CustomLlmWebkitExtractor(LlmWebkitExtractor):
    CLASSIFICATION_PROMPT = """
    您的自定义分类提示...
    输入HTML: {alg_html}
    """
```

## 性能优化建议

### 1. 模型选择
- **小模型** (0.5B-1B): 适合快速批处理，准确率略低
- **中等模型** (3B-7B): 平衡性能和准确率
- **大模型** (13B+): 最高准确率，适合高质量需求

### 2. 硬件配置
```python
# 单GPU配置
config = {
    "tensor_parallel_size": 1,
    "dtype": "bfloat16",  # A100/H100推荐
    # "dtype": "float16",   # V100/RTX推荐
}

# 多GPU配置  
config = {
    "tensor_parallel_size": 4,  # 4个GPU
    "dtype": "bfloat16",
}
```

### 3. 批处理优化
```python
# 预加载模型避免重复初始化
extractor = ExtractorFactory.create("llm-webkit", config)

# 批量处理
for html in html_list:
    result = extractor.extract(html)
    process_result(result)
```

## 故障排除

### 常见问题

1. **模型加载失败**
   ```
   RuntimeError: Failed to load LLM model
   ```
   - 检查模型路径是否正确
   - 确保有足够的GPU内存
   - 验证模型格式兼容性

2. **JSON解析错误**
   ```
   Warning: LLM output is not valid JSON
   ```
   - 启用 `use_logits_processor=True`
   - 检查提示模板格式
   - 降低temperature增加确定性

3. **内存不足**
   ```
   CUDA out of memory
   ```
   - 减少 `max_item_count`
   - 降低 `max_output_tokens`
   - 使用 `dtype="float16"`
   - 增加 `tensor_parallel_size`

4. **处理速度慢**
   - 禁用 `use_logits_processor`
   - 减少 `max_output_tokens`
   - 使用更小的模型
   - 增加GPU并行度

### 调试技巧

```python
# 启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 检查分类结果
result = extractor.extract(html)
if result.success:
    print("分类详情:", result.metadata['classification_result'])
    print("LLM原始输出:", result.metadata['llm_output'])
```

## 集成示例

### 与WebMainBench评测框架集成

```python
from webmainbench.evaluator import Evaluator
from webmainbench.data import BenchmarkDataset

# 创建数据集
dataset = BenchmarkDataset.from_file("test_data.jsonl")

# 配置LLM-WebKit extractor
config = {
    "model_path": "/path/to/model",
    "use_logits_processor": True,
    "max_item_count": 500
}

# 运行评测
evaluator = Evaluator(extractor_name="llm-webkit", extractor_config=config)
results = evaluator.evaluate(dataset)

print(f"平均得分: {results['overall_score']}")
print(f"处理速度: {results['processing_speed']} samples/s")
```

# 🏆 TEDS 算法实现总结

## 📋 **实现概述**

成功为 WebMainBench 实现了 **TEDS (Tree-Edit Distance based Similarity)** 算法，这是来自 IBM 研究论文 "Image-based table recognition: data, model, and evaluation" 的学术级表格评估方法。

## 🎯 **核心特性**

### ✅ **已实现功能**

1. **完整的 TEDS 算法**
   - 基于树编辑距离的表格相似度计算
   - 动态规划优化的编辑距离算法
   - 支持复杂表格结构 (colspan, rowspan)

2. **多格式支持**
   - HTML 表格解析
   - Markdown 表格转换
   - 结构化数据 (list, dict) 处理

3. **灵活配置**
   - 结构化评估 (S-TEDS): 只关注表格结构
   - 内容敏感评估: 同时考虑结构和内容
   - 可忽略特定节点 (tbody, thead, tfoot)

4. **无缝集成**
   - 与现有 `TableExtractionMetric` 完全兼容
   - 通过配置 `use_teds: true` 即可启用
   - 保持向后兼容性

## 🧪 **测试结果**

### **基础功能测试**
| 测试场景 | TEDS 得分 | 说明 |
|---------|----------|------|
| 完全相同表格 | 1.0000 | ✅ 完美识别 |
| 缺少一行表格 | 0.6000 | ✅ 准确计算差异 |
| Markdown vs HTML | 1.0000 | ✅ 格式转换正确 |
| 复杂表格结构 | 0.4286 | ✅ 识别结构差异 |

### **算法对比分析**
| 测试用例 | 简单算法 | TEDS算法 | 差异 | 优势 |
|---------|---------|---------|------|------|
| 完全匹配 | 1.0000 | 1.0000 | 0.0000 | 结果一致 |
| 缺少一行 | 0.8640 | 0.6000 | 0.2640 | TEDS 更严格 |
| 内容不同 | 0.9655 | 0.4286 | 0.5369 | TEDS 更敏感 |
| 结构不同 | 0.8518 | 0.4444 | 0.4073 | TEDS 更准确 |

## 🚀 **使用方法**

### **方法 1: 在现有表格指标中启用**
```python
from webmainbench.metrics import TableExtractionMetric

# 启用 TEDS 算法
metric = TableExtractionMetric("table_teds", {
    'use_teds': True,
    'structure_only': False  # 同时考虑结构和内容
})

result = metric.calculate(predicted_table, ground_truth_table)
print(f"TEDS 得分: {result.score:.4f}")
```

### **方法 2: 直接使用 TEDS 指标**
```python
from webmainbench.metrics import TEDSMetric, StructureTEDSMetric

# 内容敏感的 TEDS
teds = TEDSMetric("teds")
result = teds.calculate(predicted_table, ground_truth_table)

# 仅结构的 S-TEDS
s_teds = StructureTEDSMetric("s_teds")
result = s_teds.calculate(predicted_table, ground_truth_table)
```

### **方法 3: 在评估器中配置**
```python
from webmainbench import Evaluator

evaluator = Evaluator(task_config={
    "metrics": {
        "table_extraction": {
            "use_teds": True,
            "structure_only": False
        }
    }
})
```

## 🔬 **算法原理**

### **TEDS 公式**
```
TEDS(Ta, Tb) = 1 - EditDist(Ta, Tb) / max(|Ta|, |Tb|)
```

其中：
- `Ta`, `Tb`: 两个表格的树结构表示
- `EditDist`: 树编辑距离
- `|T|`: 树中节点的数量

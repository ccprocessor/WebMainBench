#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json
sys.path.append(os.path.join(os.path.dirname(__file__), 'WebMainBench'))

from webmainbench.data.loader import DataLoader
from webmainbench.metrics.base import BaseMetric

# 测试id为这个的数据
test_id = "6500a9d5-f579-421d-8fee-dda5a48f7cd0"
data_file = "WebMainBench/data/WebMainBench_llm-webkit_v1_WebMainBench_dataset_merge_2549_llm_webkit.jsonl"

dataset = DataLoader.load_jsonl(data_file)
samples = dataset.samples

sample = None
for s in samples:
    if getattr(s, "id", None) == test_id:
        sample = s
        break

if not sample:
    print(f"未找到id为{test_id}的样本")
    sys.exit(1)

content_list = getattr(sample, "groundtruth_content_list", None)
from examples.statics import Statics

# 调用Statics统计content_list的类型分布
statics = Statics()
statics_result = statics.get_statics(content_list)
print("content_list statics:")
print(json.dumps(statics_result, ensure_ascii=False, indent=2))





# markdown_content = getattr(sample, "groundtruth_content", None)
# if not content_list:
#     print(f"样本{test_id}没有groundtruth_content_list")
#     sys.exit(1)
# if not markdown_content:
#     print(f"样本{test_id}没有groundtruth_content")
#     sys.exit(1)

# print("=== 测试综合提取 ===")
# result_content_list = BaseMetric._extract_from_content_list(content_list)
# result_markdown = BaseMetric._extract_from_markdown(markdown_content)

# # print("【content_list方法提取结果】")
# # print(json.dumps(result_content_list, ensure_ascii=False, indent=2))
# # print("【markdown方法提取结果】")
# # print(json.dumps(result_markdown, ensure_ascii=False, indent=2))

# import difflib

# def calc_similarity(a, b):
#     """计算两个字符串的相似度（简单用difflib.SequenceMatcher）"""
#     if not a and not b:
#         return 1.0
#     return difflib.SequenceMatcher(None, a, b).ratio()

# fields = ['code', 'formula', 'table']
# for field in fields:
#     cl_val = result_content_list.get(field, "")
#     md_val = result_markdown.get(field, "")
#     sim = calc_similarity(cl_val, md_val)
#     print(f"\n==== 字段: {field} ====")
#     print(f"content_list方法: {repr(cl_val)}")
#     print(f"markdown方法   : {repr(md_val)}")
#     print(f"相似度: {sim:.4f}")
#     if sim == 1.0:
#         print("✅ 完全一致")
#     elif sim >= 0.7:
#         print("🟡 相似度较高")
#     else:
#         print("❌ 相似度较低")
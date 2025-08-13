#!/usr/bin/env python3
"""
脚本：仅提取 WebMainBench 数据集中的表格内容到 table.md
"""

import json
import sys
import os
from pathlib import Path

# 添加父目录到 sys.path 以便导入 webmainbench
sys.path.append(str(Path(__file__).parent.parent))

from webmainbench.metrics.base import BaseMetric

def extract_only_tables_from_dataset():
    """只提取 WebMainBench 数据集中的表格内容并输出到 table.md（table为空的不记录）"""

    # 路径配置
    dataset_path = "/home/zhangshuo/Desktop/vscodeworkspace/WebMainBench/data/WebMainBench_llm-webkit_v1_WebMainBench_dataset_merge_with_llm_webkit.jsonl"
    output_path = "table.md"

    # 检查数据集文件是否存在
    if not os.path.exists(dataset_path):
        print(f"错误：未找到数据集文件 {dataset_path}")
        return

    extracted_tables = []
    line_ids = []

    # 按行读取 JSONL 文件
    with open(dataset_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                data = json.loads(line.strip())

                # 提取ID和内容
                item_id = data.get('track_id', f'line_{line_num}')
                content = data.get('llm_webkit_md', '')

                # 使用 _extract_from_markdown 提取
                if content:
                    extracted = BaseMetric._extract_from_markdown(content)
                    table_content = extracted.get("table", "")
                    # 只记录table不为空的项
                    if table_content and table_content.strip():
                        extracted_tables.append(table_content)
                        line_ids.append((item_id, line_num))
            except json.JSONDecodeError as e:
                print(f"解析JSON出错，行{line_num}: {e}")
                continue
            except Exception as e:
                print(f"处理第{line_num}行时出错: {e}")
                continue

    # 写入 table.md 文件，只输出 table 字段
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Extracted Table Content from WebMainBench Dataset\n\n")
        f.write(f"Total items processed: {len(extracted_tables)}\n\n")

        for idx, (table_content, (item_id, line_num)) in enumerate(zip(extracted_tables, line_ids), 1):
            f.write(f"## Item {idx}\n")
            f.write(f"- **ID**: {item_id}\n")
            f.write(f"- **Line Number**: {line_num}\n")
            f.write(f"- **Extracted Table**:\n\n")
            f.write("```\n")
            f.write(table_content)
            f.write("\n```\n\n")
            f.write("---\n\n")

    print(f"表格提取完成！共处理 {len(extracted_tables)} 条数据。")
    print(f"表格内容已保存到: {output_path}")

if __name__ == "__main__":
    extract_only_tables_from_dataset()

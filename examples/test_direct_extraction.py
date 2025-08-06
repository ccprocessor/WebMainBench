#!/usr/bin/env python3
"""
测试直接提取content_list的方法
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'WebMainBench'))

from webmainbench.metrics.base import BaseMetric

def test_direct_extraction():
    """测试直接提取方法"""
    
    # 模拟content_list数据结构
    content_list = [
        [
            {
                "type": "code",
                "bbox": [0, 0, 50, 50],
                "raw_content": "<code>def add(a, b):\n    return a + b</code>",
                "content": {
                    "code_content": "def add(a, b):\n    return a + b",
                    "language": "python"
                }
            },
            {
                "type": "equation-interline",
                "bbox": [0, 0, 50, 50],
                "raw_content": "a^2 + b^2 = c^2",
                "content": {
                    "math_content": "a^2 + b^2 = c^2",
                    "math_type": "latex"
                }
            },
            {
                "type": "simple_table",
                "bbox": [0, 0, 50, 50],
                "raw_content": None,
                "content": {
                    "html": "<table><tr><td>1</td><td>2</td></tr><tr><td>3</td><td>4</td></tr></table>",
                    "title": "example table"
                }
            },
            {
                "type": "paragraph",
                "bbox": [0, 0, 50, 50],
                "raw_content": None,
                "content": [
                    {"c": "这是一个段落，包含", "t": "text", "bbox": [0, 0, 10, 10]},
                    {"c": "行内公式", "t": "equation-inline", "bbox": [10, 0, 10, 10]},
                    {"c": "和", "t": "text", "bbox": [20, 0, 10, 10]},
                    {"c": "行内代码", "t": "code-inline", "bbox": [30, 0, 10, 10]},
                    {"c": "。", "t": "text", "bbox": [40, 0, 10, 10]}
                ]
            },
            {
                "type": "title",
                "bbox": [0, 0, 50, 50],
                "raw_content": None,
                "content": {
                    "title_content": "测试标题",
                    "level": 1
                }
            }
        ]
    ]
    
    print("测试直接提取方法...")

    
    result_original = BaseMetric._extract_from_content_list(
        content_list
    )
    
    print("原有方法结果:")
    print(f"代码: {result_original['code']}")
    print(f"公式: {result_original['formula']}")
    print(f"表格: {result_original['table']}")
    print(f"文本: {result_original['text']}")
    print(f"Markdown: {result_original['md'][:100]}...")
    
    print("\n" + "="*50 + "\n")
    
if __name__ == "__main__":
    test_direct_extraction() 
import unittest
import json
from pathlib import Path
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from webmainbench.data.loader import DataLoader
from webmainbench.metrics.base import BaseMetric

class TestDatasetConsistency(unittest.TestCase):
    """测试数据集一致性的测试用例，统计各字段对不上的数量（相似度不高即视为对不上）"""

    def setUp(self):
        """设置测试环境"""
        self.data_file = "WebMainBench/data/WebMainBench_llm-webkit_v1_WebMainBench_dataset_merge_2549_llm_webkit.jsonl"
        self.extract_from_markdown = BaseMetric._extract_from_markdown
        self.extract_from_content_list = BaseMetric._extract_from_content_list

    @staticmethod
    def _calculate_similarity(str1, str2):
        """
        计算两个字符串的简单字符级相似度，返回0~1
        """
        if not str1 and not str2:
            return 1.0
        if not str1 or not str2:
            return 0.0
        set1 = set(str1.lower())
        set2 = set(str2.lower())
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union > 0 else 0.0

    def test_field_mismatch_statistics(self):
        """
        统计各字段（code, formula, table, text）两种提取方法相似度低于阈值的样本数，并统计总体对不上的样本数
        并打印部分总体对不上的具体例子，便于排查
        """
        dataset = DataLoader.load_jsonl(self.data_file)
        samples = dataset.samples

        # 相似度阈值，低于此值视为对不上
        threshold = 0.8

        # 初始化每个字段的对不上计数
        mismatch_counts = {
            'code': 0,
            'formula': 0,
            'table': 0,
            'text': 0
        }
        # 记录每个字段对不上的样本id
        mismatch_ids = {
            'code': [],
            'formula': [],
            'table': [],
            'text': []
        }
        # 总体对不上的样本数
        total_mismatch = 0
        total_mismatch_ids = []
        # 记录总体对不上的样本的详细信息
        total_mismatch_examples = []

        for i, sample in enumerate(samples):
            # 只统计有groundtruth_content和groundtruth_content_list的样本
            if not sample.groundtruth_content or not sample.groundtruth_content_list:
                continue

            md_result = self.extract_from_markdown(sample.groundtruth_content)
            cl_result = self.extract_from_content_list(sample.groundtruth_content_list)

            # 记录本样本是否有任一字段对不上
            sample_mismatch = False
            mismatch_fields = []

            for key in ['code', 'formula', 'table', 'text']:
                sim = self._calculate_similarity(md_result[key], cl_result[key])
                if sim < threshold:
                    mismatch_counts[key] += 1
                    mismatch_ids[key].append(sample.id)
                    sample_mismatch = True
                    mismatch_fields.append(key)

            if sample_mismatch:
                total_mismatch += 1
                total_mismatch_ids.append(sample.id)
                # 只保存前5个例子，避免输出过多
                if len(total_mismatch_examples) < 5:
                    # 保存详细内容，便于排查
                    example = {
                        "id": sample.id,
                        "mismatch_fields": mismatch_fields,
                        "groundtruth_content": sample.groundtruth_content,
                        "groundtruth_content_list": sample.groundtruth_content_list if sample.groundtruth_content_list else [[]],
                        "md_result": {k: md_result[k] for k in mismatch_fields},
                        "cl_result": {k: cl_result[k] for k in mismatch_fields}
                    }
                    total_mismatch_examples.append(example)

        # 输出统计结果
        print("\n字段对不上（相似度低于{:.2f}）统计结果：".format(threshold))
        for key in ['code', 'formula', 'table', 'text']:
            print(f"{key} 字段对不上的样本数: {mismatch_counts[key]}")
        print(f"\n总体有任一字段对不上的样本数: {total_mismatch}")

        # 也可以输出部分样本id，方便排查
        print("\n各字段对不上的样本ID（前10个）：")
        for key in ['code', 'formula', 'table', 'text']:
            print(f"{key}: {mismatch_ids[key][:10]}")
        print("\n总体对不上的样本ID（前10个）:")
        print(total_mismatch_ids[:10])

        # 新增：打印部分总体对不上的具体例子
        print("\n总体对不上的样本详细例子（最多5个）：")
        for idx, example in enumerate(total_mismatch_examples):
            print(f"\n例子{idx+1}:")
            print(f"样本ID: {example['id']}")
            print(f"对不上的字段: {example['mismatch_fields']}")
            print("groundtruth_content（截断前200字）:")
            print(example['groundtruth_content'][:200].replace('\n', '\\n'))
            print("groundtruth_content_list（截断前200字）:")
            print(str(example['groundtruth_content_list'])[:200].replace('\n', '\\n'))
            print("Markdown提取结果（对不上的字段）:")
            for k in example['mismatch_fields']:
                print(f"  {k}: {example['md_result'][k]}")
            print("ContentList提取结果（对不上的字段）:")
            for k in example['mismatch_fields']:
                print(f"  {k}: {example['cl_result'][k]}")

    def test_data_loading(self):
        """测试数据加载是否正常"""
        try:
            dataset = DataLoader.load_jsonl(self.data_file)
            self.assertIsNotNone(dataset)
            self.assertGreater(len(dataset.samples), 0)
            print(f"成功加载 {len(dataset.samples)} 个样本")
        except Exception as e:
            self.fail(f"数据加载失败: {e}")

if __name__ == '__main__':
    unittest.main(verbosity=2)

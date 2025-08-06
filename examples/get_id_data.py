import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from webmainbench.data.loader import DataLoader

def get_sample_by_id(data_file, sample_id):
    dataset = DataLoader.load_jsonl(data_file)
    for sample in dataset.samples:
        if getattr(sample, "id", None) == sample_id:
            return sample
    return None

def main():
    import argparse
    parser = argparse.ArgumentParser(description="根据id获取groundtruth_content_list和groundtruth_content")
    parser.add_argument("--id", type=str, default="6500a9d5-f579-421d-8fee-dda5a48f7cd0", help="要查找的样本id")
    parser.add_argument("--data_file", type=str, default="WebMainBench/data/WebMainBench_llm-webkit_v1_WebMainBench_dataset_merge_2549_llm_webkit.jsonl", help="数据文件路径")
    args = parser.parse_args()

    sample = get_sample_by_id(args.data_file, args.id)
    if sample is None:
        print(f"未找到id为 {args.id} 的样本")
        return

    gt_content_list = getattr(sample, "groundtruth_content_list", None)
    gt_content = getattr(sample, "groundtruth_content", None)

    print(f"id: {args.id}")
    print("groundtruth_content_list:")
    print(gt_content_list)
    print("\ngroundtruth_content:")
    print(gt_content)

if __name__ == "__main__":
    main()

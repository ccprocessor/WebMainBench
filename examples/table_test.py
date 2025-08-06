
data_file = "WebMainBench/data/WebMainBench_llm-webkit_v1_WebMainBench_dataset_merge_with_llm_webkit.jsonl"

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from webmainbench.data.loader import DataLoader

TARGET_TAGS = {"TABLE_TEXT_RATIO", "TABLE_HTML_SOURCE_RATIO", "TABLE_AT_DOM_DEPTH"}

def main():
    dataset = DataLoader.load_jsonl(data_file)
    samples = dataset.samples
    found_ids = []
    for sample in samples:
        # 检查每个样本的所有字段，查找__tag属性
        # 假设参数都在groundtruth_content_list字段里
        cl = getattr(sample, "groundtruth_content_list", None)
        if not cl:
            continue
        # cl 可能是 List[Dict] 或 List[List[Dict]]
        if isinstance(cl, list) and cl and not isinstance(cl[0], list):
            cl = [cl]
        for page in cl:
            for elem in page:
                # 检查每个元素的__tag属性
                tag = elem.get("__tag")
                if tag in TARGET_TAGS:
                    found_ids.append(getattr(sample, "id", None))
                    print(f"Found sample id: {getattr(sample, 'id', None)} with __tag: {tag}")
                    break  # 一个样本只打印一次
            else:
                continue
            break

    print(f"Total samples with __tag in {TARGET_TAGS}: {len(found_ids)}")
    if found_ids:
        print("Sample ids:", found_ids)

if __name__ == "__main__":
    main()
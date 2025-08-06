import sys
import os
import json
from pathlib import Path
import difflib

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from webmainbench.data.loader import DataLoader
from webmainbench.metrics.base import BaseMetric

def calc_similarity(a, b):
    """计算两个字符串的相似度（简单用difflib.SequenceMatcher）"""
    if not a and not b:
        return 1.0
    return difflib.SequenceMatcher(None, a, b).ratio()

def main():
    data_file = "WebMainBench/data/WebMainBench_llm-webkit_v1_WebMainBench_dataset_merge_with_llm_webkit.jsonl"
    dataset = DataLoader.load_jsonl(data_file)
    samples = dataset.samples
    if not samples:
        print("数据集为空")
        return

    # 新增md字段
    fields = ['code', 'formula', 'table', 'text', 'md']
    sim_sums = {f: 0.0 for f in fields}
    sim_counts = {f: 0 for f in fields}
    sim_min = {f: 1.0 for f in fields}
    sim_max = {f: 0.0 for f in fields}
    sim_list = {f: [] for f in fields}
    diff_samples = {f: [] for f in fields}
    empty_cl = {f: 0 for f in fields}
    empty_md = {f: 0 for f in fields}
    total_with_content_list = 0
    total_with_markdown = 0

    for idx, sample in enumerate(samples):
        # 兼容groundtruth_content_list为None或空的情况
        cl = getattr(sample, "groundtruth_content_list", None)
        gt_content = getattr(sample, "groundtruth_content", None)
        if not cl:
            continue

        result_cl = BaseMetric._extract_from_content_list(cl)
        total_with_content_list += 1

        if gt_content is not None:
            try:
                result_md = BaseMetric._extract_from_markdown(gt_content)
            except Exception as e:
                print(f"样本{getattr(sample, 'id', idx)} markdown提取异常: {e}")
                continue
            total_with_markdown += 1
        else:
            result_md = None

        for field in fields:
            val_cl = result_cl.get(field, '')
            if result_md is not None:
                val_md = result_md.get(field, '')
            else:
                val_md = ''
            # 统计空字符串
            if not val_cl:
                empty_cl[field] += 1
            if not val_md:
                empty_md[field] += 1
            # 只在两者都存在时统计相似度
            if result_md is not None:
                sim = calc_similarity(val_cl, val_md)
                sim_sums[field] += sim
                sim_counts[field] += 1
                sim_min[field] = min(sim_min[field], sim)
                sim_max[field] = max(sim_max[field], sim)
                sim_list[field].append(sim)
                # 差异较大（相似度低于0.7）或完全不等，打印出来
                if sim < 0.7 or val_cl != val_md:
                    diff_samples[field].append({
                        "idx": idx,
                        "id": getattr(sample, "id", idx),
                        "similarity": sim,
                        "content_list": val_cl,
                        "markdown": val_md
                    })

    print("="*60)
    print(f"总样本数: {len(samples)}")
    print(f"有groundtruth_content_list的样本: {total_with_content_list}")
    print(f"有groundtruth_content的样本: {total_with_markdown}")
    print("="*60)
    print("空字符串占比统计:")
    for field in fields:
        cl_rate = empty_cl[field] / total_with_content_list * 100 if total_with_content_list else 0
        md_rate = empty_md[field] / total_with_markdown * 100 if total_with_markdown else 0
        print(f"{field:>8} | content_list空: {empty_cl[field]:>4} ({cl_rate:5.1f}%) | markdown空: {empty_md[field]:>4} ({md_rate:5.1f}%)")
    print("="*60)
    print("五种字段的相似度统计:")
    for field in fields:
        count = sim_counts[field]
        avg = sim_sums[field] / count if count else 0
        minv = sim_min[field] if count else 0
        maxv = sim_max[field] if count else 0
        print(f"{field:>8} | 样本数: {count:>5} | 平均相似度: {avg:.4f} | 最小: {minv:.4f} | 最大: {maxv:.4f}")
    # print("="*60)
    # print("差异较大（相似度<0.7或内容不一致）的样本（每字段最多展示5个）:")
    # for field in fields:
    #     print(f"\n字段 [{field}] 差异样本（共{len(diff_samples[field])}个，最多展示5个）:")
    #     for i, diff in enumerate(diff_samples[field][:5]):
    #         print(f"  样本idx: {diff['idx']}, id: {diff['id']}, 相似度: {diff['similarity']:.4f}")
    #         print(f"    content_list提取: {diff['content_list'][:300]}")
    #         print(f"    markdown提取   : {diff['markdown'][:300]}")
    #         print("    ---")
    # print("="*60)
    # 如果需要全部差异样本可保存到文件
    # with open("diff_samples.json", "w", encoding="utf-8") as f:
    #     json.dump(diff_samples, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()

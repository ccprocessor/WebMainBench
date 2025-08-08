#!/usr/bin/env python3
"""
统计测试脚本：分析_extract_from_markdown方法的结果统计（统计整个数据集）
并统计所有content_list的statics分布
"""

import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from webmainbench.data.loader import DataLoader
from webmainbench.metrics.base import BaseMetric

# 直接import merge_statics
from examples.statics import Statics

def analyze_sample(sample, sample_index):
    """分析单个样本的结果"""
    result = {
        'id': sample.id,
        'index': sample_index,
        'has_groundtruth_content': bool(sample.groundtruth_content),
        'markdown_result': None,
        'markdown_zero_chars': {'code': 0, 'formula': 0, 'table': 0, 'text': 0}
    }

    # 使用_extract_from_markdown
    if sample.groundtruth_content:
        try:
            markdown_result = BaseMetric._extract_from_markdown(sample.groundtruth_content)
            result['markdown_result'] = markdown_result

            # 统计0字符的情况
            for key in ['code', 'formula', 'table', 'text']:
                if len(markdown_result[key]) == 0:
                    result['markdown_zero_chars'][key] = 1
        except Exception as e:
            print(f"Markdown方法处理样本 {sample.id} 时出错: {e}")

    return result

def generate_summary_report(analysis_results, statics_total):
    """生成汇总报告"""
    total_samples = len(analysis_results)

    # 统计基本信息
    has_groundtruth_content = sum(1 for r in analysis_results if r['has_groundtruth_content'])

    # 统计0字符情况
    markdown_zero_stats = {'code': 0, 'formula': 0, 'table': 0, 'text': 0}

    for result in analysis_results:
        for key in ['code', 'formula', 'table', 'text']:
            markdown_zero_stats[key] += result['markdown_zero_chars'][key]

    # 生成报告
    print("=" * 60)
    print("数据集分析汇总报告")
    print("=" * 60)
    print(f"总样本数: {total_samples}")
    print(f"有groundtruth_content的样本: {has_groundtruth_content} ({has_groundtruth_content/total_samples*100:.1f}%)")

    print("\n" + "=" * 60)
    print("0字符统计 (Markdown方法)")
    print("=" * 60)
    for key in ['code', 'formula', 'table', 'text']:
        count = markdown_zero_stats[key]
        percentage = count / has_groundtruth_content * 100 if has_groundtruth_content > 0 else 0
        print(f"{key:>10}: {count:>3} 个样本 ({percentage:>5.1f}%)")

    # 找出所有0字符的样本
    print("\n" + "=" * 60)
    print("所有字段都为0的样本")
    print("=" * 60)

    markdown_all_zero = []

    for result in analysis_results:
        if result['markdown_result']:
            if all(result['markdown_zero_chars'].values()):
                markdown_all_zero.append(result['id'])

    print(f"Markdown方法全为0的样本: {len(markdown_all_zero)}")
    if markdown_all_zero:
        print("样本ID:", markdown_all_zero[:10])  # 只显示前10个

    # 新增：输出所有content_list statics统计
    print("\n" + "=" * 60)
    print("所有content_list statics统计（类型分布总和）")
    print("=" * 60)
    import json
    # 使用__getall__()方法获取字典数据而不是直接序列化Statics对象
    statics_dict = statics_total.__getall__()
    print(json.dumps(statics_dict, ensure_ascii=False, indent=2))

def main():
    """主函数"""
    print("开始数据集统计分析...")

    try:
        # 加载数据集
        data_file = "WebMainBench/data/WebMainBench_llm-webkit_v1_WebMainBench_dataset_merge_with_llm_webkit.jsonl"
        dataset = DataLoader.load_jsonl(data_file)

        print(f"成功加载 {len(dataset.samples)} 个样本")

        # 统计整个数据集（不再只取前100个样本）
        test_samples = dataset.samples
        print(f"分析全部 {len(test_samples)} 个样本...")

        # 分析每个样本
        analysis_results = []
        statics = Statics()
        for i, sample in enumerate(test_samples):
            if i % 100 == 0:  # 每100个样本显示进度
                print(f"处理进度: {i}/{len(test_samples)}")

            result = analyze_sample(sample, i)
            analysis_results.append(result)

            # 统计content_list statics
            if getattr(sample, "groundtruth_content_list", None):
                cl = sample.groundtruth_content_list
                # 兼容格式
                if cl and isinstance(cl, list) and (len(cl) == 0 or not isinstance(cl[0], list)):
                    cl_input = [cl]
                else:
                    cl_input = cl
                # 使用add_statics进行累计统计
                statics_result = statics.add_statics(cl_input)
                if i < 5:  # 只打印前5个样本的统计结果作为示例
                    print(f"样本 {i} 统计结果:")
                    print(json.dumps(statics_result, ensure_ascii=False, indent=2))
        # 生成汇总报告

        generate_summary_report(analysis_results, statics)

        print("\n" + "=" * 60)
        print("分析完成！")
        print("=" * 60)

    except Exception as e:
        print(f"分析失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
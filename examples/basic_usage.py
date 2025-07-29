#!/usr/bin/env python3
"""
WebMainBench 基本使用示例
"""

import json
from pathlib import Path

# 导入 WebMainBench 模块
from webmainbench import (
    DataLoader, DataSaver, BenchmarkDataset, DataSample,
    ExtractorFactory, Evaluator, 
    format_results, setup_logging
)


def create_sample_dataset():
    """创建示例数据集"""
    
    # 创建示例数据
    samples = [
        {
            "track_id": "0b7f2636-d35f-40bf-9b7f-94be4bcbb396",
            "html": "<html><body><h1 cc-select=\"true\">这是标题</h1></body></html>",   # 人工标注带cc-select="true" 属性
            "groundtruth_content": "# 标题\n\n正文内容",
            "groundtruth_content_list": [
                {"type": "heading", "content": "标题", "level": 1},
                {"type": "paragraph", "content": "正文内容"}
            ],
            "url": "https://orderyourbooks.com/product-category/college-books-p-u/?products-per-page=all",
            "layout_id": "orderyourbooks.com_4",
            "max_layer_n": 10,
            "url_host_name": "orderyourbooks.com",
            "raw_warc_path": "s3://cc-raw-huawei/crawl-data/CC-MAIN-2025-13/segments/1742004433093.21/warc/CC-MAIN-20250319080618-20250319110618-00909.warc.gz?bytes=461610805,172252",
            "language": "en",
            "__dom_depth": 19,
            "__dom_width": 10231,
            "__type": "__max_depth",
            "__tag": "DOM_WIDTH",
            "marked_type": "unwanted",  # normal：正常标注的网页；unable：正文内容无法抉择；unwanted：无需标注的网页；
            "unwanted_reason": "list"
        },
        {
            "track_id": "0b7f2636-d35f-40bf-9b7f-94be4bcbb396",
            "html": "<html><body><h1 cc-select=\"true\">这是标题</h1></body></html>",   # 人工标注带cc-select="true" 属性
            "groundtruth_content": "# 标题\n\n正文内容",
            "groundtruth_content_list": [
                {"type": "heading", "content": "标题", "level": 1},
                {"type": "paragraph", "content": "正文内容"}
            ],
            "url": "https://orderyourbooks.com/product-category/college-books-p-u/?products-per-page=all",
            "layout_id": "orderyourbooks.com_4",
            "max_layer_n": 10,
            "url_host_name": "orderyourbooks.com",
            "raw_warc_path": "s3://cc-raw-huawei/crawl-data/CC-MAIN-2025-13/segments/1742004433093.21/warc/CC-MAIN-20250319080618-20250319110618-00909.warc.gz?bytes=461610805,172252",
            "language": "en",
            "__dom_depth": 19,
            "__dom_width": 10231,
            "__type": "__max_depth",
            "__tag": "DOM_WIDTH",
            "marked_type": "unwanted",  # normal：正常标注的网页；unable：正文内容无法抉择；unwanted：无需标注的网页；
            "unwanted_reason": "list"
        },
    ]
    
    # 创建数据集
    dataset = BenchmarkDataset(name="sample_dataset", description="示例评测数据集")
    
    for sample_data in samples:
        sample = DataSample.from_dict(sample_data)
        dataset.add_sample(sample)
    
    return dataset


def demo_basic_evaluation():
    """演示基本评测流程"""
    
    print("=== WebMainBench 基本使用示例 ===\n")
    
    # 设置日志
    setup_logging(level="INFO")
    
    # 1. 创建或加载数据集
    print("1. 创建示例数据集...")
    dataset = create_sample_dataset()
    print(f"数据集包含 {len(dataset)} 个样本")
    print(f"数据集统计: {dataset.get_statistics()}\n")
    
    # 2. 保存数据集到文件
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    dataset_path = data_dir / "sample_dataset.jsonl"
    DataSaver.save_jsonl(dataset, dataset_path, include_results=False)
    print(f"数据集已保存到: {dataset_path}\n")
    
    # 3. 重新加载数据集
    print("2. 重新加载数据集...")
    loaded_dataset = DataLoader.load_jsonl(dataset_path)
    print(f"加载的数据集包含 {len(loaded_dataset)} 个样本\n")
    
    # 4. 列出可用的抽取器
    print("3. 可用的抽取器:")
    available_extractors = ExtractorFactory.list_available()
    for extractor_name in available_extractors:
        print(f"  - {extractor_name}")
    print()
    
    # 5. 创建评测器
    print("4. 创建评测器...")
    evaluator = Evaluator()
    print(f"可用的评测指标: {evaluator.metric_calculator.list_available_metrics()}\n")
    
    # 6. 创建一个模拟抽取器进行演示
    print("5. 创建模拟抽取器...")
    
    from webmainbench.extractors import BaseExtractor, ExtractionResult
    
    class MockExtractor(BaseExtractor):
        """模拟抽取器，用于演示"""
        
        def _setup(self):
            pass
        
        def _extract_content(self, html, url=None):
            # 简单的模拟抽取逻辑
            if "标题" in html:
                content = "# 提取的标题\n\n提取的正文内容。"
                content_list = [
                    {"type": "heading", "content": "提取的标题", "level": 1},
                    {"type": "paragraph", "content": "提取的正文内容。"}
                ]
            else:
                content = "提取的内容"
                content_list = [{"type": "paragraph", "content": "提取的内容"}]
            
            return ExtractionResult(
                content=content,
                content_list=content_list,
                success=True,
                confidence_score=0.85
            )
    
    # 注册模拟抽取器
    ExtractorFactory.register("mock", MockExtractor)
    mock_extractor = ExtractorFactory.create("mock")
    print("模拟抽取器已创建\n")
    
    # 7. 运行评测
    print("6. 运行评测...")
    result = evaluator.evaluate(
        dataset=loaded_dataset,
        extractor=mock_extractor,
        max_samples=2  # 限制样本数量用于演示
    )
    
    # 8. 显示结果
    print("\n7. 评测结果:")
    print("=" * 50)
    formatted_results = format_results(result.to_dict())
    print(formatted_results)
    
    # 9. 保存结果
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    results_path = results_dir / "evaluation_results.json"
    DataSaver.save_evaluation_results(result.to_dict(), results_path)
    print(f"\n结果已保存到: {results_path}")
    
    # 10. 生成报告
    report_path = results_dir / "evaluation_report.csv"
    DataSaver.save_summary_report(result.to_dict(), report_path)
    print(f"报告已保存到: {report_path}")


def demo_extractor_comparison():
    """演示多抽取器对比"""
    
    print("\n=== 多抽取器对比演示 ===\n")
    
    # 创建数据集
    dataset = create_sample_dataset()
    
    # 创建多个模拟抽取器
    from webmainbench.extractors import BaseExtractor, ExtractionResult
    
    class ExtractorA(BaseExtractor):
        def _setup(self):
            pass
        def _extract_content(self, html, url=None):
            return ExtractionResult(
                content="抽取器A的结果",
                content_list=[{"type": "paragraph", "content": "抽取器A的结果"}],
                success=True,
                confidence_score=0.9
            )
    
    class ExtractorB(BaseExtractor):
        def _setup(self):
            pass
        def _extract_content(self, html, url=None):
            return ExtractionResult(
                content="抽取器B的结果",
                content_list=[{"type": "paragraph", "content": "抽取器B的结果"}],
                success=True,
                confidence_score=0.8
            )
    
    # 注册抽取器
    ExtractorFactory.register("extractor_a", ExtractorA)
    ExtractorFactory.register("extractor_b", ExtractorB)
    
    # 运行对比
    evaluator = Evaluator()
    extractors = ["extractor_a", "extractor_b"]
    
    results = evaluator.compare_extractors(
        dataset=dataset,
        extractors=extractors,
        max_samples=2
    )
    
    # 显示对比结果
    print("对比结果:")
    print("-" * 40)
    for extractor_name, result in results.items():
        overall_score = result.overall_metrics.get('overall', 0)
        print(f"{extractor_name}: {overall_score:.4f}")
    
    # 保存多抽取器对比榜单
    all_results = []
    for extractor_name, result in results.items():
        all_results.append(result.to_dict())
    
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    leaderboard_path = results_dir / "leaderboard.csv"
    DataSaver.save_summary_report(all_results, leaderboard_path)
    print(f"\n📊 榜单已保存到: {leaderboard_path}")


if __name__ == "__main__":
    try:
        demo_basic_evaluation()
        # demo_extractor_comparison()
        print("\n✅ 示例运行完成！")
        
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        import traceback
        traceback.print_exc() 
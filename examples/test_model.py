from webmainbench import DataLoader, Evaluator, ExtractorFactory

# 1. 加载评测数据集
dataset = DataLoader.load_jsonl("WebMainBench/data/WebMainBench_llm-webkit_v1_WebMainBench_dataset_merge_2549_llm_webkit.jsonl")

# 2. 创建抽取器
extractor = ExtractorFactory.create("test-model")

# 3. 运行评测
evaluator = Evaluator()
result = evaluator.evaluate(dataset, extractor)

# 4. 查看结果
print(f"Overall Score: {result.overall_metrics}")
print(f"Category Metrics: {result.category_metrics}")
print(f"Error Analysis: {result.error_analysis}")

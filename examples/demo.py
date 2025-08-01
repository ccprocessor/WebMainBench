from webmainbench import DataLoader, Evaluator, ExtractorFactory

# 1. 加载评测数据集
dataset = DataLoader.load_jsonl("../../WebMainBench_v1_WebMainBench_dataset_0603.jsonl")

# 2. 创建抽取器
extractor = ExtractorFactory.create("resiliparse")

# 3. 运行评测
evaluator = Evaluator()
result = evaluator.evaluate(dataset, extractor)

# 4. 查看结果
print(f"Overall Score: {result}")

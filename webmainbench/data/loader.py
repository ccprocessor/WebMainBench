"""
Data loader for WebMainBench.
"""

import json
import jsonlines
from pathlib import Path
from typing import List, Dict, Any, Optional, Union, Iterator
from .dataset import BenchmarkDataset, DataSample


class DataLoader:
    """Data loader for various input formats."""
    
    @staticmethod
    def load_jsonl(file_path: Union[str, Path], **kwargs) -> BenchmarkDataset:
        """
        Load dataset from JSONL file.
        
        Args:
            file_path: Path to the JSONL file
            **kwargs: Additional parameters for dataset creation
        
        Returns:
            BenchmarkDataset instance
        """
        file_path = Path(file_path)
        dataset_name = kwargs.get('name', file_path.stem)
        dataset = BenchmarkDataset(name=dataset_name)
        
        with jsonlines.open(file_path, 'r') as reader:
            for idx, line in enumerate(reader):
                try:
                    # 使用DataSample.from_dict()来正确处理字段映射和过滤
                    sample = DataSample.from_dict(line)
                    dataset.add_sample(sample)
                    
                except Exception as e:
                    print(f"Warning: Failed to load sample at line {idx}: {e}")
                    continue
        
        return dataset
    
    @staticmethod
    def load_json(file_path: Union[str, Path], **kwargs) -> BenchmarkDataset:
        """
        Load dataset from JSON file.
        
        Args:
            file_path: Path to the JSON file
            **kwargs: Additional parameters for dataset creation
        
        Returns:
            BenchmarkDataset instance
        """
        file_path = Path(file_path)
        dataset_name = kwargs.get('name', file_path.stem)
        dataset = BenchmarkDataset(name=dataset_name)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle different JSON structures
        if isinstance(data, list):
            # Array of samples
            samples_data = data
        elif isinstance(data, dict):
            if 'samples' in data:
                # Structured format with metadata
                samples_data = data['samples']
                # Load metadata if available
                if 'metadata' in data:
                    for key, value in data['metadata'].items():
                        dataset.set_metadata(key, value)
            else:
                # Single sample in dict format
                samples_data = [data]
        else:
            raise ValueError(f"Unsupported JSON structure in {file_path}")
        
        for idx, sample_data in enumerate(samples_data):
            try:
                sample = DataSample.from_dict(sample_data)
                if not sample.id:
                    sample.id = f"sample_{idx}"
                dataset.add_sample(sample)
            except Exception as e:
                print(f"Warning: Failed to load sample {idx}: {e}")
                continue
        
        return dataset
    
    @staticmethod
    def load_from_directory(dir_path: Union[str, Path], 
                          pattern: str = "*.jsonl", 
                          **kwargs) -> Dict[str, BenchmarkDataset]:
        """
        Load multiple datasets from a directory.
        
        Args:
            dir_path: Directory containing dataset files
            pattern: File pattern to match (default: "*.jsonl")
            **kwargs: Additional parameters for dataset creation
        
        Returns:
            Dictionary mapping filenames to BenchmarkDataset instances
        """
        dir_path = Path(dir_path)
        datasets = {}
        
        for file_path in dir_path.glob(pattern):
            try:
                if file_path.suffix == '.jsonl':
                    dataset = DataLoader.load_jsonl(file_path, **kwargs)
                elif file_path.suffix == '.json':
                    dataset = DataLoader.load_json(file_path, **kwargs)
                else:
                    print(f"Warning: Unsupported file format: {file_path}")
                    continue
                
                datasets[file_path.stem] = dataset
                
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
                continue
        
        return datasets
    
    @staticmethod
    def merge_datasets(datasets: List[BenchmarkDataset], 
                      name: str = "merged_dataset") -> BenchmarkDataset:
        """
        Merge multiple datasets into one.
        
        Args:
            datasets: List of BenchmarkDataset instances to merge
            name: Name for the merged dataset
        
        Returns:
            Merged BenchmarkDataset instance
        """
        merged = BenchmarkDataset(name=name)
        
        for dataset in datasets:
            for sample in dataset.samples:
                # Ensure unique IDs
                original_id = sample.id
                counter = 1
                while merged.get_sample(sample.id) is not None:
                    sample.id = f"{original_id}_{counter}"
                    counter += 1
                
                merged.add_sample(sample)
        
        return merged
    
    @staticmethod
    def stream_jsonl(file_path: Union[str, Path],
                    categories: Optional[List[str]] = None,
                    max_samples: Optional[int] = None) -> Iterator[DataSample]:
        """
        流式读取JSONL文件，逐个返回DataSample，减少内存使用。
        
        Args:
            file_path: JSONL文件路径
            categories: 类别过滤列表
            max_samples: 最大样本数限制
            
        Yields:
            DataSample: 逐个生成的数据样本
        """
        file_path = Path(file_path)
        
        sample_count = 0
        with jsonlines.open(file_path, 'r') as reader:
            for line_idx, line in enumerate(reader):
                try:
                    # 创建样本
                    sample = DataSample.from_dict(line)
                    
                    # 类别过滤
                    if categories and sample.content_type not in categories:
                        continue
                    
                    # 返回样本
                    yield sample
                    sample_count += 1
                    
                    # 检查样本数限制
                    if max_samples and sample_count >= max_samples:
                        break
                        
                except Exception as e:
                    print(f"Warning: Failed to load sample at line {line_idx}: {e}")
                    continue
    
    @staticmethod
    def stream_jsonl_batched(file_path: Union[str, Path],
                           batch_size: int = 50,
                           categories: Optional[List[str]] = None,
                           max_samples: Optional[int] = None) -> Iterator[List[DataSample]]:
        """
        流式读取JSONL文件，按批次返回DataSample列表。
        
        Args:
            file_path: JSONL文件路径
            batch_size: 批次大小
            categories: 类别过滤列表
            max_samples: 最大样本数限制
            
        Yields:
            List[DataSample]: 批次数据样本列表
        """
        batch = []
        sample_count = 0
        
        for sample in DataLoader.stream_jsonl(file_path, categories, max_samples):
            batch.append(sample)
            sample_count += 1
            
            # 达到批次大小或样本数限制时返回批次
            if len(batch) >= batch_size or (max_samples and sample_count >= max_samples):
                yield batch
                batch = []
                
                if max_samples and sample_count >= max_samples:
                    break
        
        # 返回最后一批（如果有）
        if batch:
            yield batch 
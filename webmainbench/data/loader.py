"""
Data loader for WebMainBench.
"""

import json
import jsonlines
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
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
                    # Ensure required fields exist
                    sample_id = line.get('id', f"sample_{idx}")
                    html = line.get('html', '')
                    content = line.get('content', '')
                    content_list = line.get('content_list', [])
                    
                    # Create data sample
                    sample = DataSample(
                        id=sample_id,
                        html=html,
                        groundtruth_content=content,
                        groundtruth_content_list=content_list,
                        url=line.get('url'),
                        domain=line.get('domain'),
                        language=line.get('language'),
                        content_type=line.get('content_type'),
                        difficulty=line.get('difficulty'),
                        tags=line.get('tags'),
                    )
                    
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
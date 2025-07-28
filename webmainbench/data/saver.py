"""
Data saver for WebMainBench.
"""

import json
import jsonlines
from pathlib import Path
from typing import Union, List, Dict, Any
from .dataset import BenchmarkDataset, DataSample


class DataSaver:
    """Data saver for various output formats."""
    
    @staticmethod
    def save_jsonl(dataset: BenchmarkDataset, 
                   file_path: Union[str, Path],
                   include_results: bool = True) -> None:
        """
        Save dataset to JSONL file.
        
        Args:
            dataset: BenchmarkDataset to save
            file_path: Output file path
            include_results: Whether to include extraction results
        """
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with jsonlines.open(file_path, 'w') as writer:
            for sample in dataset.samples:
                sample_dict = sample.to_dict()
                if not include_results:
                    sample_dict.pop('extracted_results', None)
                writer.write(sample_dict)
    
    @staticmethod
    def save_json(dataset: BenchmarkDataset, 
                  file_path: Union[str, Path],
                  include_metadata: bool = True,
                  include_results: bool = True,
                  indent: int = 2) -> None:
        """
        Save dataset to JSON file.
        
        Args:
            dataset: BenchmarkDataset to save
            file_path: Output file path
            include_metadata: Whether to include dataset metadata
            include_results: Whether to include extraction results
            indent: JSON indentation level
        """
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "name": dataset.name,
            "description": dataset.description,
            "samples": []
        }
        
        if include_metadata:
            data["metadata"] = dataset.get_metadata()
            data["statistics"] = dataset.get_statistics()
        
        for sample in dataset.samples:
            sample_dict = sample.to_dict()
            if not include_results:
                sample_dict.pop('extracted_results', None)
            data["samples"].append(sample_dict)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
    
    @staticmethod
    def save_evaluation_results(results: Dict[str, Any], 
                              file_path: Union[str, Path],
                              format: str = "json") -> None:
        """
        Save evaluation results.
        
        Args:
            results: Evaluation results dictionary
            file_path: Output file path
            format: Output format ("json" or "jsonl")
        """
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        if format.lower() == "json":
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
        elif format.lower() == "jsonl":
            with jsonlines.open(file_path, 'w') as writer:
                if isinstance(results, dict) and 'samples' in results:
                    for sample_result in results['samples']:
                        writer.write(sample_result)
                else:
                    writer.write(results)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    @staticmethod
    def save_summary_report(results: Union[Dict[str, Any], List[Dict[str, Any]]], 
                          file_path: Union[str, Path]) -> None:
        """
        Save evaluation results as a CSV leaderboard.
        
        Args:
            results: Single evaluation results dictionary or list of results for multiple extractors
            file_path: Output CSV file path
        """
        import csv
        
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Ensure we have a list of results
        if isinstance(results, dict):
            results_list = [results]
        else:
            results_list = results
        
        # Prepare CSV data
        csv_data = []
        
        for result in results_list:
            # Extract basic info
            metadata = result.get('metadata', {})
            error_analysis = result.get('error_analysis', {})
            
            row = {
                'extractor': metadata.get('extractor_name', 'unknown'),
                'total_samples': metadata.get('total_samples', 0),
                'success_rate': error_analysis.get('success_rate', 0.0)
            }
            
            # Add only specified metrics
            if 'overall_metrics' in result:
                metrics_to_include = ['overall', 'table_extraction', 'formula_extraction']
                for metric_name in metrics_to_include:
                    if metric_name in result['overall_metrics']:
                        value = result['overall_metrics'][metric_name]
                        row[metric_name] = round(value, 4) if isinstance(value, (int, float)) else value
            
            csv_data.append(row)
        
        # Sort by overall score (descending)
        def get_sort_key(row):
            return row.get('overall', 0)
        
        csv_data.sort(key=get_sort_key, reverse=True)
        
        # Write CSV file
        if csv_data:
            # Define specific field order
            fieldnames = ['extractor', 'total_samples', 'success_rate', 'overall', 'table_extraction', 'formula_extraction']
            # Only include fields that exist in the data
            fieldnames = [f for f in fieldnames if f in csv_data[0]]
            
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(csv_data)
    
    @staticmethod
    def export_for_analysis(dataset: BenchmarkDataset,
                           file_path: Union[str, Path],
                           extractor_name: str = None) -> None:
        """
        Export dataset in a format suitable for analysis tools.
        
        Args:
            dataset: BenchmarkDataset to export
            file_path: Output file path
            extractor_name: Name of the extractor (for filtering results)
        """
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        analysis_data = []
        
        for sample in dataset.samples:
            row = {
                'sample_id': sample.id,
                'url': sample.url,
                'domain': sample.domain,
                'language': sample.language,
                'content_type': sample.content_type,
                'difficulty': sample.difficulty,
                'groundtruth_length': len(sample.groundtruth_content) if sample.groundtruth_content else 0,
                'groundtruth_blocks': len(sample.groundtruth_content_list),
            }
            
            # Add extraction results if available
            if sample.extracted_results and extractor_name:
                if extractor_name in sample.extracted_results:
                    result = sample.extracted_results[extractor_name]
                    row.update({
                        'extracted_length': len(result.get('content', '')),
                        'extracted_blocks': len(result.get('content_list', [])),
                        'extraction_time': result.get('extraction_time'),
                        'extraction_success': result.get('success', False),
                    })
            
            analysis_data.append(row)
        
        # Save as JSON for easy loading into analysis tools
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, indent=2, ensure_ascii=False) 
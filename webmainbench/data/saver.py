"""
Data saver for WebMainBench.
"""

import json
import jsonlines
from pathlib import Path
from typing import Union, List, Dict, Any, TYPE_CHECKING

from .dataset import BenchmarkDataset, DataSample

if TYPE_CHECKING:
    from ..evaluator import EvaluationResult
    from ..metrics import MetricResult


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
    def save_evaluation_results(results: Union["EvaluationResult", Dict[str, Any]], 
                              file_path: Union[str, Path],
                              format: str = "json") -> None:
        """
        Save evaluation results.
        
        Args:
            results: EvaluationResult instance or evaluation results dictionary
            file_path: Output file path
            format: Output format ("json" or "jsonl")
        """
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert EvaluationResult to dict if needed
        if hasattr(results, 'to_dict'):
            results_dict = results.to_dict()
        else:
            results_dict = results
        
        if format.lower() == "json":
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(results_dict, f, indent=2, ensure_ascii=False)
        elif format.lower() == "jsonl":
            with jsonlines.open(file_path, 'w') as writer:
                if isinstance(results_dict, dict) and 'samples' in results_dict:
                    for sample_result in results_dict['samples']:
                        writer.write(sample_result)
                else:
                    writer.write(results_dict)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    @staticmethod
    def save_summary_report(results: Union["EvaluationResult", List["EvaluationResult"], Dict[str, Any], List[Dict[str, Any]]], 
                          file_path: Union[str, Path]) -> None:
        """
        Save evaluation results as a CSV leaderboard.
        
        Args:
            results: Single EvaluationResult instance, list of EvaluationResult instances, 
                    or their dictionary representations
            file_path: Output CSV file path
        """
        import csv
        
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert EvaluationResult objects to dicts and ensure we have a list
        def to_dict_if_needed(item):
            return item.to_dict() if hasattr(item, 'to_dict') else item
        
        if isinstance(results, list):
            results_list = [to_dict_if_needed(item) for item in results]
        else:
            results_list = [to_dict_if_needed(results)]
        
        # Prepare CSV data
        csv_data = []
        
        for result in results_list:
            # Extract basic info
            metadata = result.get('metadata', {})
            error_analysis = result.get('error_analysis', {})
            
            row = {
                'extractor': metadata.get('extractor_name', 'unknown'),
                'dataset': metadata.get('dataset_name', 'unknown'),
                'total_samples': metadata.get('total_samples', 0),
                'success_rate': error_analysis.get('success_rate', 0.0)
            }
            
            # Add all available metrics from overall_metrics
            if 'overall_metrics' in result:
                for metric_name, value in result['overall_metrics'].items():
                    row[metric_name] = round(value, 4) if isinstance(value, (int, float)) else value
            
            csv_data.append(row)
        
        # Sort by overall score (descending)
        def get_sort_key(row):
            return row.get('overall', 0)
        
        csv_data.sort(key=get_sort_key, reverse=True)
        
        # Write CSV file
        if csv_data:
            # Define field order: basic info first, then overall, then other metrics alphabetically
            basic_fields = ['extractor', 'dataset', 'total_samples', 'success_rate']
            
            # Get all metric fields from the data
            all_fields = set()
            for row in csv_data:
                all_fields.update(row.keys())
            
            # Remove basic fields from metrics
            metric_fields = all_fields - set(basic_fields)
            
            # Sort metrics: overall first, then alphabetically
            sorted_metrics = []
            if 'overall' in metric_fields:
                sorted_metrics.append('overall')
                metric_fields.remove('overall')
            sorted_metrics.extend(sorted(metric_fields))
            
            # Final field order
            fieldnames = basic_fields + sorted_metrics
            
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(csv_data)
    

    @staticmethod
    def save_dataset_with_extraction(results: Union["EvaluationResult", Dict[str, Any]], 
                                   dataset: "BenchmarkDataset",
                                   file_path: Union[str, Path],
                                   extractor_name: str = None) -> None:
        """
        Save original dataset with extracted content added for manual review.
        
        Args:
            results: EvaluationResult instance or its dictionary representation
            dataset: Original dataset
            file_path: Output JSONL file path
            extractor_name: Name of the extractor (used for field naming)
        """
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert EvaluationResult to dict if needed
        if hasattr(results, 'to_dict'):
            results_dict = results.to_dict()
        else:
            results_dict = results
        
        # Get extractor name
        if not extractor_name:
            extractor_name = results_dict.get('metadata', {}).get('extractor_name', 'extracted')
        
        # Create mapping from sample_id to extraction result
        sample_results = results_dict.get('sample_results', [])
        extraction_map = {}
        for sample_result in sample_results:
            sample_id = sample_result.get('sample_id')
            if sample_id:
                extraction_map[sample_id] = sample_result
        
        # Process each sample and add extracted content
        enriched_samples = []
        for sample in dataset.samples:
            # Convert sample to dict
            sample_dict = sample.to_dict()
            
            # Add extraction results if available
            extraction_result = extraction_map.get(sample.id)
            if extraction_result:
                # Add extracted content with extractor name prefix
                sample_dict[f'{extractor_name}_content'] = extraction_result.get('extracted_content', '')
                sample_dict[f'{extractor_name}_content_list'] = extraction_result.get('extracted_content_list', [])
                sample_dict[f'{extractor_name}_success'] = extraction_result.get('extraction_success', False)
                sample_dict[f'{extractor_name}_time'] = extraction_result.get('extraction_time', 0)
                
                # Add metric scores for quick review
                metrics = extraction_result.get('metrics', {})
                for metric_name, metric_data in metrics.items():
                    if isinstance(metric_data, dict) and metric_data.get('success', False):
                        sample_dict[f'{extractor_name}_{metric_name}_score'] = metric_data.get('score', 0)
            
            enriched_samples.append(sample_dict)
        
        # Save as JSONL
        DataSaver._save_jsonl_list(enriched_samples, file_path)
    
    @staticmethod
    def _save_jsonl_list(data_list: List[Dict[str, Any]], file_path: Union[str, Path]) -> None:
        """Save list of dictionaries as JSONL file."""
        import json
        
        file_path = Path(file_path)
        with open(file_path, 'w', encoding='utf-8') as f:
            for item in data_list:
                json.dump(item, f, ensure_ascii=False)
                f.write('\n')

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
"""
Main evaluator for WebMainBench.
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Union
import time
from datetime import datetime

from ..data import BenchmarkDataset, DataSample
from ..extractors import BaseExtractor, ExtractorFactory
from ..metrics import MetricCalculator, MetricResult


@dataclass
class EvaluationResult:
    """Result of benchmark evaluation."""
    
    # Metadata
    dataset_name: str
    extractor_name: str
    timestamp: str
    total_samples: int
    
    # Overall metrics
    overall_metrics: Dict[str, float]
    
    # Sample-level results
    sample_results: List[Dict[str, Any]]
    
    # Category-wise metrics (if applicable)
    category_metrics: Optional[Dict[str, Dict[str, float]]] = None
    
    # Error analysis
    error_analysis: Optional[Dict[str, Any]] = None
    
    # Configuration
    extractor_config: Optional[Dict[str, Any]] = None
    metric_config: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "metadata": {
                "dataset_name": self.dataset_name,
                "extractor_name": self.extractor_name,
                "timestamp": self.timestamp,
                "total_samples": self.total_samples,
            },
            "overall_metrics": self.overall_metrics,
            "sample_results": self.sample_results,
            "category_metrics": self.category_metrics,
            "error_analysis": self.error_analysis,
            "extractor_config": self.extractor_config,
            "metric_config": self.metric_config,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EvaluationResult":
        """Create from dictionary."""
        metadata = data.get("metadata", {})
        return cls(
            dataset_name=metadata.get("dataset_name", ""),
            extractor_name=metadata.get("extractor_name", ""),
            timestamp=metadata.get("timestamp", ""),
            total_samples=metadata.get("total_samples", 0),
            overall_metrics=data.get("overall_metrics", {}),
            sample_results=data.get("sample_results", []),
            category_metrics=data.get("category_metrics"),
            error_analysis=data.get("error_analysis"),
            extractor_config=data.get("extractor_config"),
            metric_config=data.get("metric_config"),
        )


class Evaluator:
    """Main evaluator for web content extraction benchmarks."""
    
    def __init__(self, metric_config: Dict[str, Any] = None):
        """
        Initialize the evaluator.
        
        Args:
            metric_config: Configuration for metrics
        """
        self.metric_calculator = MetricCalculator(metric_config)
        self.metric_config = metric_config or {}
    
    def evaluate(self, 
                dataset: BenchmarkDataset,
                extractor: Union[BaseExtractor, str],
                extractor_config: Dict[str, Any] = None,
                max_samples: Optional[int] = None,
                categories: Optional[List[str]] = None) -> EvaluationResult:
        """
        Evaluate an extractor on a dataset.
        
        Args:
            dataset: BenchmarkDataset to evaluate on
            extractor: BaseExtractor instance or name
            extractor_config: Configuration for the extractor
            max_samples: Maximum number of samples to evaluate (for testing)
            categories: Specific categories to evaluate
            
        Returns:
            EvaluationResult instance
        """
        # Create extractor if string name provided
        if isinstance(extractor, str):
            extractor = ExtractorFactory.create(extractor, extractor_config)
        
        # Filter samples if needed
        samples_to_evaluate = list(dataset.samples)
        if categories:
            samples_to_evaluate = [
                s for s in samples_to_evaluate 
                if s.content_type in categories
            ]
        
        if max_samples:
            samples_to_evaluate = samples_to_evaluate[:max_samples]
        
        # Run evaluation
        sample_results = []
        extraction_errors = []
        
        print(f"Evaluating {len(samples_to_evaluate)} samples...")
        
        for i, sample in enumerate(samples_to_evaluate):
            if i % 10 == 0:
                print(f"Progress: {i}/{len(samples_to_evaluate)}")
            
            try:
                sample_result = self._evaluate_sample(sample, extractor)
                sample_results.append(sample_result)
                
                # Track extraction errors
                if not sample_result.get('extraction_success', True):
                    extraction_errors.append({
                        'sample_id': sample.id,
                        'error': sample_result.get('extraction_error', 'Unknown error')
                    })
                    
            except Exception as e:
                print(f"Error evaluating sample {sample.id}: {e}")
                # Create error result
                error_result = {
                    'sample_id': sample.id,
                    'extraction_success': False,
                    'extraction_error': str(e),
                    'metrics': {},
                }
                sample_results.append(error_result)
                extraction_errors.append({
                    'sample_id': sample.id,
                    'error': str(e)
                })
        
        # Aggregate results
        overall_metrics = self._aggregate_metrics(sample_results)
        category_metrics = self._calculate_category_metrics(sample_results, samples_to_evaluate)
        error_analysis = self._analyze_errors(extraction_errors, sample_results)
        
        # Create evaluation result
        evaluation_result = EvaluationResult(
            dataset_name=dataset.name,
            extractor_name=extractor.name,
            timestamp=datetime.now().isoformat(),
            total_samples=len(samples_to_evaluate),
            overall_metrics=overall_metrics,
            sample_results=sample_results,
            category_metrics=category_metrics,
            error_analysis=error_analysis,
            extractor_config=extractor.get_config(),
            metric_config=self.metric_config,
        )
        
        return evaluation_result
    
    def _evaluate_sample(self, sample: DataSample, extractor: BaseExtractor) -> Dict[str, Any]:
        """Evaluate a single sample."""
        # Extract content
        extraction_result = extractor.extract(sample.html, sample.url)
        
        # Prepare result
        sample_result = {
            'sample_id': sample.id,
            'extraction_success': extraction_result.success,
            'extraction_time': extraction_result.extraction_time,
        }
        
        if not extraction_result.success:
            sample_result['extraction_error'] = extraction_result.error_message
            sample_result['metrics'] = {}
            return sample_result
        
        # Calculate metrics
        metrics = self.metric_calculator.calculate_all(
            predicted_content=extraction_result.content,
            groundtruth_content=sample.groundtruth_content,
            predicted_content_list=extraction_result.content_list,
            groundtruth_content_list=sample.groundtruth_content_list,
        )
        
        # Convert metrics to dict
        metrics_dict = {}
        for metric_name, metric_result in metrics.items():
            metrics_dict[metric_name] = {
                'score': metric_result.score,
                'success': metric_result.success,
                'details': metric_result.details,
            }
            if not metric_result.success:
                metrics_dict[metric_name]['error'] = metric_result.error_message
        
        sample_result['metrics'] = metrics_dict
        
        # Add sample metadata
        sample_result['sample_metadata'] = {
            'url': sample.url,
            'domain': sample.domain,
            'language': sample.language,
            'content_type': sample.content_type,
            'difficulty': sample.difficulty,
        }
        
        return sample_result
    
    def _aggregate_metrics(self, sample_results: List[Dict[str, Any]]) -> Dict[str, float]:
        """Aggregate metrics across all samples."""
        # Collect metric results by metric name
        metric_groups = {}
        
        for sample_result in sample_results:
            if not sample_result.get('extraction_success', True):
                continue
                
            metrics = sample_result.get('metrics', {})
            for metric_name, metric_data in metrics.items():
                if metric_data.get('success', False):
                    if metric_name not in metric_groups:
                        metric_groups[metric_name] = []
                    metric_groups[metric_name].append(metric_data['score'])
        
        # Calculate aggregated scores
        aggregated_metrics = {}
        for metric_name, scores in metric_groups.items():
            if scores:
                aggregated_metrics[metric_name] = sum(scores) / len(scores)
            else:
                aggregated_metrics[metric_name] = 0.0
        
        # overall score is already calculated by MetricCalculator
        # No need to override it here
        
        return aggregated_metrics
    
    def _calculate_category_metrics(self, sample_results: List[Dict[str, Any]], 
                                  samples: List[DataSample]) -> Optional[Dict[str, Dict[str, float]]]:
        """Calculate metrics by category."""
        # Group samples by content type
        category_samples = {}
        for i, sample in enumerate(samples):
            if i >= len(sample_results):
                break
                
            content_type = sample.content_type or 'unknown'
            if content_type not in category_samples:
                category_samples[content_type] = []
            category_samples[content_type].append(sample_results[i])
        
        # Calculate metrics for each category
        category_metrics = {}
        for category, category_sample_results in category_samples.items():
            if len(category_sample_results) >= 3:  # Only calculate if enough samples
                category_metrics[category] = self._aggregate_metrics(category_sample_results)
        
        return category_metrics if category_metrics else None
    
    def _analyze_errors(self, extraction_errors: List[Dict[str, str]], 
                       sample_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze extraction errors."""
        total_samples = len(sample_results)
        failed_samples = len(extraction_errors)
        success_rate = (total_samples - failed_samples) / total_samples if total_samples > 0 else 0.0
        
        # Count error types
        error_types = {}
        for error in extraction_errors:
            error_msg = error['error']
            # Simple error categorization
            if 'timeout' in error_msg.lower():
                error_type = 'timeout'
            elif 'network' in error_msg.lower() or 'connection' in error_msg.lower():
                error_type = 'network'
            elif 'parse' in error_msg.lower() or 'parsing' in error_msg.lower():
                error_type = 'parsing'
            elif 'empty' in error_msg.lower():
                error_type = 'empty_input'
            else:
                error_type = 'other'
            
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        return {
            'total_samples': total_samples,
            'failed_count': failed_samples,
            'success_rate': success_rate,
            'common_errors': error_types,
            'sample_errors': extraction_errors[:10]  # Keep first 10 for debugging
        }
    
    def compare_extractors(self, 
                          dataset: BenchmarkDataset,
                          extractors: List[Union[BaseExtractor, str]],
                          extractor_configs: Optional[List[Dict[str, Any]]] = None,
                          **kwargs) -> Dict[str, EvaluationResult]:
        """
        Compare multiple extractors on the same dataset.
        
        Args:
            dataset: BenchmarkDataset to evaluate on
            extractors: List of extractors to compare
            extractor_configs: List of configs for each extractor
            **kwargs: Additional arguments for evaluate()
            
        Returns:
            Dictionary mapping extractor names to EvaluationResult
        """
        if extractor_configs is None:
            extractor_configs = [None] * len(extractors)
        
        results = {}
        
        for extractor, config in zip(extractors, extractor_configs):
            print(f"\nEvaluating extractor: {extractor if isinstance(extractor, str) else extractor.name}")
            
            try:
                result = self.evaluate(
                    dataset=dataset,
                    extractor=extractor,
                    extractor_config=config,
                    **kwargs
                )
                
                extractor_name = result.extractor_name
                results[extractor_name] = result
                
            except Exception as e:
                extractor_name = extractor if isinstance(extractor, str) else extractor.name
                print(f"Error evaluating {extractor_name}: {e}")
                continue
        
        return results 
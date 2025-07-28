"""
Metric calculator for WebMainBench.
"""

from typing import Dict, Any, List, Optional, Union
from .base import BaseMetric, MetricResult
from .text_metrics import EditDistanceMetric, BLEUMetric, ROUGEMetric
from .table_metrics import TableExtractionMetric
from .formula_metrics import FormulaExtractionMetric
from .structure_metrics import StructureMetric


class MetricCalculator:
    """Calculator for multiple evaluation metrics."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the metric calculator.
        
        Args:
            config: Configuration for metrics
        """
        self.config = config or {}
        self.metrics: Dict[str, BaseMetric] = {}
        self._setup_default_metrics()
    
    def _setup_default_metrics(self) -> None:
        """Setup default metrics."""
        # Core metrics only
        self.add_metric("edit_distance", EditDistanceMetric("edit_distance"))
        self.add_metric("table_extraction", TableExtractionMetric("table_extraction"))
        self.add_metric("formula_extraction", FormulaExtractionMetric("formula_extraction"))
        
        # Keep BLEU implementation but don't add to default metrics
        # try:
        #     self.add_metric("bleu", BLEUMetric("bleu"))
        # except RuntimeError:
        #     pass
    
    def add_metric(self, name: str, metric: BaseMetric) -> None:
        """
        Add a metric to the calculator.
        
        Args:
            name: Name of the metric
            metric: BaseMetric instance
        """
        self.metrics[name] = metric
    
    def remove_metric(self, name: str) -> None:
        """
        Remove a metric from the calculator.
        
        Args:
            name: Name of the metric to remove
        """
        if name in self.metrics:
            del self.metrics[name]
    
    def calculate_all(self, predicted_content: str, 
                     groundtruth_content: str,
                     predicted_content_list: List[Dict[str, Any]] = None,
                     groundtruth_content_list: List[Dict[str, Any]] = None,
                     **kwargs) -> Dict[str, MetricResult]:
        """
        Calculate all available metrics.
        
        Args:
            predicted_content: Predicted markdown content
            groundtruth_content: Ground truth markdown content
            predicted_content_list: Predicted content list
            groundtruth_content_list: Ground truth content list
            **kwargs: Additional arguments for specific metrics
            
        Returns:
            Dictionary mapping metric names to MetricResult instances
        """
        results = {}
        
        for metric_name, metric in self.metrics.items():
            try:
                if metric_name in ["edit_distance", "bleu", "rouge"]:
                    # Text-based metrics
                    result = metric.calculate(predicted_content, groundtruth_content, **kwargs)
                
                elif metric_name == "structure":
                    # Structure metric uses content_list
                    pred_list = predicted_content_list or []
                    gt_list = groundtruth_content_list or []
                    result = metric.calculate(pred_list, gt_list, **kwargs)
                
                elif metric_name in ["table_extraction", "formula_extraction"]:
                    # Content-specific metrics
                    result = metric.calculate(predicted_content, groundtruth_content, **kwargs)
                
                else:
                    # Generic calculation
                    result = metric.calculate(predicted_content, groundtruth_content, **kwargs)
                
                results[metric_name] = result
                
            except Exception as e:
                # Create error result for failed metrics
                results[metric_name] = MetricResult.create_error_result(
                    metric_name, f"Metric calculation failed: {str(e)}"
                )
        
        # Add overall score as edit_distance
        if "edit_distance" in results and results["edit_distance"].success:
            overall_result = MetricResult(
                metric_name="overall",
                score=results["edit_distance"].score,
                details={"source": "edit_distance", "description": "Overall score based on edit distance"}
            )
            results["overall"] = overall_result
        
        return results
    
    def calculate_batch(self, samples: List[Dict[str, Any]]) -> List[Dict[str, MetricResult]]:
        """
        Calculate metrics for multiple samples.
        
        Args:
            samples: List of sample dictionaries containing:
                - predicted_content: str
                - groundtruth_content: str
                - predicted_content_list: List[Dict] (optional)
                - groundtruth_content_list: List[Dict] (optional)
                
        Returns:
            List of metric results for each sample
        """
        batch_results = []
        
        for sample in samples:
            sample_results = self.calculate_all(
                predicted_content=sample.get('predicted_content', ''),
                groundtruth_content=sample.get('groundtruth_content', ''),
                predicted_content_list=sample.get('predicted_content_list'),
                groundtruth_content_list=sample.get('groundtruth_content_list'),
            )
            batch_results.append(sample_results)
        
        return batch_results
    
    def aggregate_results(self, batch_results: List[Dict[str, MetricResult]]) -> Dict[str, MetricResult]:
        """
        Aggregate results across multiple samples.
        
        Args:
            batch_results: List of metric result dictionaries
            
        Returns:
            Aggregated metric results
        """
        if not batch_results:
            return {}
        
        # Group results by metric name
        metric_groups = {}
        for sample_results in batch_results:
            for metric_name, result in sample_results.items():
                if metric_name not in metric_groups:
                    metric_groups[metric_name] = []
                metric_groups[metric_name].append(result)
        
        # Aggregate each metric
        aggregated_results = {}
        for metric_name, results in metric_groups.items():
            if metric_name in self.metrics:
                metric = self.metrics[metric_name]
                aggregated_results[metric_name] = metric.aggregate_results(results)
            else:
                # Fallback aggregation for unknown metrics
                aggregated_results[metric_name] = self._simple_aggregate(metric_name, results)
        
        return aggregated_results
    
    def _simple_aggregate(self, metric_name: str, results: List[MetricResult]) -> MetricResult:
        """Simple aggregation for unknown metrics."""
        successful_results = [r for r in results if r.success]
        
        if not successful_results:
            return MetricResult.create_error_result(metric_name, "All calculations failed")
        
        scores = [r.score for r in successful_results]
        avg_score = sum(scores) / len(scores)
        
        return MetricResult(
            metric_name=f"{metric_name}_aggregate",
            score=avg_score,
            details={
                "num_samples": len(results),
                "num_successful": len(successful_results),
                "scores": scores,
            }
        )
    
    def get_summary(self, aggregated_results: Dict[str, MetricResult]) -> Dict[str, Any]:
        """
        Get a summary of aggregated results.
        
        Args:
            aggregated_results: Aggregated metric results
            
        Returns:
            Summary dictionary
        """
        summary = {
            "overall_score": 0.0,
            "metric_scores": {},
            "successful_metrics": 0,
            "failed_metrics": 0,
        }
        
        successful_scores = []
        
        for metric_name, result in aggregated_results.items():
            summary["metric_scores"][metric_name] = result.score
            
            if result.success:
                summary["successful_metrics"] += 1
                successful_scores.append(result.score)
            else:
                summary["failed_metrics"] += 1
        
        # Calculate overall score as mean of successful metrics
        if successful_scores:
            summary["overall_score"] = sum(successful_scores) / len(successful_scores)
        
        return summary
    
    def list_available_metrics(self) -> List[str]:
        """List all available metrics."""
        return list(self.metrics.keys())
    
    def get_metric_info(self, metric_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific metric."""
        if metric_name in self.metrics:
            return self.metrics[metric_name].get_info()
        return None 
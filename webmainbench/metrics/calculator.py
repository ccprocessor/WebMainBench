"""
Metric calculator for WebMainBench.
"""

from typing import Dict, Any, List, Optional, Union
from .base import BaseMetric, MetricResult
from .text_metrics import EditDistanceMetric, BLEUMetric, ROUGEMetric, CodeEditMetric, TextEditMetric
from .table_metrics import TableEditMetric, TableTEDSMetric
from .formula_metrics import FormulaEditMetric


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
        # 注册新的内容类型指标
        self.add_metric("code_edit", CodeEditMetric("code_edit"))
        self.add_metric("formula_edit", FormulaEditMetric("formula_edit"))
        self.add_metric("table_edit", TableEditMetric("table_edit"))
        self.add_metric("table_TEDS", TableTEDSMetric("table_TEDS"))
        self.add_metric("text_edit", TextEditMetric("text_edit"))
    
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
        # results = {}
        #
        # for metric_name, metric in self.metrics.items():
        #     try:
        #         if metric_name in ["edit_distance", "bleu", "rouge"]:
        #             # Text-based metrics
        #             result = metric.calculate(predicted_content, groundtruth_content, **kwargs)
        #         elif metric_name in ["code_edit", "formula_edit",
        #                            "table_edit", "table_TEDS", "text_edit"]:
        #             # 新的内容类型指标，需要传递 content_list
        #             result = metric.calculate(
        #                 predicted_content,
        #                 groundtruth_content,
        #                 predicted_content_list=predicted_content_list,
        #                 groundtruth_content_list=groundtruth_content_list,
        #                 **kwargs
        #             )
        #         else:
        #             # Generic calculation
        #             result = metric.calculate(predicted_content, groundtruth_content, **kwargs)
        #
        #         results[metric_name] = result
        #
        #     except Exception as e:
        #         # Create error result for failed metrics
        #         results[metric_name] = MetricResult.create_error_result(
        #             metric_name, f"Metric calculation failed: {str(e)}"
        #         )

        results: Dict[str, MetricResult] = {}

        # 1. 先计算非表格指标（无依赖关系）
        for metric_name in list(self.metrics.keys()):
            if metric_name in ["table_edit", "table_TEDS"]:
                continue  # 表格相关指标单独处理

            metric = self.metrics[metric_name]
            result = metric.calculate(
                predicted=predicted_content,
                groundtruth=groundtruth_content,
                predicted_content_list=predicted_content_list,
                groundtruth_content_list=groundtruth_content_list, **kwargs
            )
            results[metric_name] = result

        # 2. 处理表格相关指标（有依赖关系）
        # 2.1 计算 table_edit
        if "table_edit" in self.metrics:
            table_edit_result = self.metrics["table_edit"].calculate(
                predicted=predicted_content,
                groundtruth=groundtruth_content,
                predicted_content_list=predicted_content_list,
                groundtruth_content_list=groundtruth_content_list,
                **kwargs
            )
            results["table_edit"] = table_edit_result

            # 2.2 计算 table_TEDS（依赖 table_edit 的结果）
            if "table_TEDS" in self.metrics:
                teds_result = self.metrics["table_TEDS"].calculate(
                    predicted=predicted_content,
                    groundtruth=groundtruth_content,
                    predicted_content_list=predicted_content_list,
                    groundtruth_content_list=groundtruth_content_list,
                    table_edit_result=table_edit_result,  # 传递依赖结果
                    **kwargs
                )
                results["table_TEDS"] = teds_result
        
        # 3. 计算综合得分（所有成功指标的平均值）
        successful_scores = []
        failed_metrics = []
        
        for metric_name, result in results.items():
            if result.success:
                successful_scores.append(result.score)
            else:
                failed_metrics.append(metric_name)
        
        if successful_scores:
            overall_score = sum(successful_scores) / len(successful_scores)
            overall_result = MetricResult(
                metric_name="overall",
                score=overall_score,
                details={
                    "source": "average_of_all_metrics", 
                    "description": "Overall score as average of all successful metrics",
                    "successful_metrics": len(successful_scores),
                    "failed_metrics": len(failed_metrics),
                    "individual_scores": {name: result.score for name, result in results.items() if result.success}
                }
            )
            results["overall"] = overall_result
        else:
            # 如果所有指标都失败了，overall分数为0
            overall_result = MetricResult.create_error_result(
                "overall", "All individual metrics failed"
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
        metrics = list(self.metrics.keys())
        # Add overall metric which is calculated dynamically
        if "overall" not in metrics:
            metrics.insert(0, "overall")  # Put overall first
        return metrics
    
    def get_metric_info(self, metric_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific metric."""
        if metric_name in self.metrics:
            return self.metrics[metric_name].get_info()
        return None 
"""
Main evaluator for WebMainBench.
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Union, Iterator
import time
import itertools
from datetime import datetime
from pathlib import Path

from ..data import BenchmarkDataset, DataSample, DataLoader, DataSaver
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
        
        # Filter samples if needed (避免不必要的副本)
        samples_iter = dataset.samples
        
        # 只有在需要过滤时才创建副本
        if categories:
            samples_iter = [
                s for s in samples_iter 
                if s.content_type in categories
            ]
        
        # 如果有max_samples限制，使用itertools.islice避免完整列表
        if max_samples:
            import itertools
            samples_to_evaluate = list(itertools.islice(samples_iter, max_samples))
        else:
            # 如果没有任何过滤，直接使用原始列表避免副本
            samples_to_evaluate = samples_iter if not categories else samples_iter
        
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
    
    def evaluate_batched(self,
                        jsonl_file_path: Union[str, Path],
                        extractor: Union[BaseExtractor, str],
                        batch_size: int = 50,
                        extractor_config: Dict[str, Any] = None,
                        max_samples: Optional[int] = None,
                        categories: Optional[List[str]] = None,
                        output_file: Optional[Union[str, Path]] = None) -> EvaluationResult:
        """
        分批处理评测，减少内存使用。
        
        Args:
            jsonl_file_path: JSONL数据集文件路径
            extractor: BaseExtractor实例或名称
            batch_size: 批处理大小（默认50）
            extractor_config: 抽取器配置
            max_samples: 最大样本数限制
            categories: 特定类别过滤
            output_file: 可选的结果输出文件（用于大数据集）
            
        Returns:
            EvaluationResult实例
        """
        # Create extractor if string name provided
        if isinstance(extractor, str):
            extractor = ExtractorFactory.create(extractor, extractor_config)
        
        jsonl_file_path = Path(jsonl_file_path)
        
        # 统计信息
        total_samples = 0
        processed_samples = 0
        all_sample_results = []
        all_extraction_errors = []
        
        print(f"🔄 开始批处理评测")
        print(f"   数据集: {jsonl_file_path}")
        print(f"   批大小: {batch_size}")
        print(f"   最大样本数: {max_samples or '无限制'}")
        
        start_time = time.time()
        
        # 使用DataLoader的流式批处理方法
        for batch_samples in DataLoader.stream_jsonl_batched(
            file_path=jsonl_file_path,
            batch_size=batch_size,
            categories=categories,
            max_samples=max_samples
        ):
            # 处理当前批次
            batch_results, batch_errors = self._process_batch(batch_samples, extractor)
            all_sample_results.extend(batch_results)
            all_extraction_errors.extend(batch_errors)
            
            processed_samples += len(batch_samples)
            total_samples += len(batch_samples)
            
            print(f"   已处理: {processed_samples} 样本")
            
            # 如果有输出文件，可以立即写入避免内存累积
            if output_file and len(all_sample_results) > 1000:
                DataSaver.append_intermediate_results(all_sample_results, output_file)
                all_sample_results = []  # 清空已保存的结果
        
        end_time = time.time()
        print(f"✅ 批处理评测完成")
        print(f"   总耗时: {end_time - start_time:.2f}秒")
        print(f"   处理样本: {processed_samples}")
        
        # 聚合结果
        overall_metrics = self._aggregate_metrics(all_sample_results)
        # 批处理模式下跳过分类指标（为了节约内存，不保存样本列表）
        category_metrics = None
        error_analysis = self._analyze_errors(all_extraction_errors, all_sample_results)
        
        evaluation_result = EvaluationResult(
            dataset_name=jsonl_file_path.stem,
            extractor_name=extractor.name,
            timestamp=datetime.now().isoformat(),
            total_samples=processed_samples,
            overall_metrics=overall_metrics,
            sample_results=all_sample_results,
            category_metrics=category_metrics,
            error_analysis=error_analysis,
            extractor_config=extractor.get_config(),
            metric_config=self.metric_config,
        )
        
        return evaluation_result
    
    def _process_batch(self, batch_samples: List[DataSample], extractor: BaseExtractor) -> tuple[List[Dict[str, Any]], List[Dict[str, str]]]:
        """处理一批样本"""
        batch_results = []
        batch_errors = []
        
        for sample in batch_samples:
            try:
                sample_result = self._evaluate_sample(sample, extractor)
                batch_results.append(sample_result)
                
                # 收集错误信息
                if not sample_result.get('extraction_success', False):
                    batch_errors.append({
                        'sample_id': sample.id,
                        'error': sample_result.get('extraction_error', 'Unknown error'),
                        'url': sample.url,
                    })
                    
            except Exception as e:
                print(f"⚠️  样本 {sample.id} 评测失败: {e}")
                batch_errors.append({
                    'sample_id': sample.id,
                    'error': str(e),
                    'url': sample.url,
                })
        
        return batch_results, batch_errors
    

    def _evaluate_sample(self, sample: DataSample, extractor: BaseExtractor) -> Dict[str, Any]:
        """Evaluate a single sample."""
        if extractor.__class__.__name__ == 'TestModelExtractor':
            extraction_result = extractor.extract_from_sample(sample)
        else:
            # Extract content
            extraction_result = extractor.extract(sample.html, sample.url)
        
        # Prepare result
        sample_result = {
            'sample_id': sample.id,
            'extraction_success': extraction_result.success,
            'extraction_time': extraction_result.extraction_time,
            'extracted_content': extraction_result.content if extraction_result.success else None,
            'extracted_content_list': extraction_result.content_list if extraction_result.success else None,
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
        # # Collect metric results by metric name
        # metric_groups = {}
        #
        # for sample_result in sample_results:
        #     if not sample_result.get('extraction_success', True):
        #         continue
        #
        #     metrics = sample_result.get('metrics', {})
        #     for metric_name, metric_data in metrics.items():
        #         if metric_data.get('success', False):
        #             if metric_name not in metric_groups:
        #                 metric_groups[metric_name] = []
        #             metric_groups[metric_name].append(metric_data['score'])
        #
        # # Calculate aggregated scores
        # aggregated_metrics = {}
        # for metric_name, scores in metric_groups.items():
        #     if scores:
        #         aggregated_metrics[metric_name] = sum(scores) / len(scores)
        #     else:
        #         aggregated_metrics[metric_name] = 0.0
        #
        # # overall score is already calculated by MetricCalculator
        # # No need to override it here
        #
        # return aggregated_metrics
        """
            聚合所有样本的指标，计算全局平均值（每个指标单独聚合）
            """
        if not sample_results:
            return {}

        # 初始化每个指标的总分和样本数
        metric_totals = {
            "text_edit": 0.0,
            "code_edit": 0.0,
            "table_edit": 0.0,
            "table_TEDS": 0.0,
            "formula_edit": 0.0,
            "overall": 0.0  # 全局overall单独计算
        }
        metric_counts = {k: 0 for k in metric_totals.keys()}  # 记录每个指标有效样本数

        # 累加所有样本的指标分数
        for sample in sample_results:
            metrics = sample.get("metrics", {})
            for metric_name in metric_totals.keys():
                if metric_name in metrics and metrics[metric_name].get("success", False):
                    metric_totals[metric_name] += metrics[metric_name]["score"]
                    metric_counts[metric_name] += 1

        # 计算每个指标的平均值（全局overall为5个单项指标的平均值）
        overall_metrics = {}
        for metric_name in metric_totals.keys():
            if metric_counts[metric_name] > 0:
                overall_metrics[metric_name] = metric_totals[metric_name] / metric_counts[metric_name]
            else:
                overall_metrics[metric_name] = 0.0  # 无有效样本时默认为0

        # 特别处理全局overall：固定为5个单项指标的平均值（无论单项是否有有效样本）
        # 排除样本级overall，仅用5个核心指标计算全局overall
        core_metrics = ["text_edit", "code_edit", "table_edit", "table_TEDS", "formula_edit"]
        core_scores = [overall_metrics[metric] for metric in core_metrics]
        overall_metrics["overall"] = sum(core_scores) / len(core_metrics)

        return overall_metrics
    
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
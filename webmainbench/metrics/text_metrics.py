"""
Text-based metrics for WebMainBench.
"""

from typing import Dict, Any, List
import difflib
import re
from .base import BaseMetric, MetricResult
from rapidfuzz.distance import Levenshtein

class EditDistanceMetric(BaseMetric):
    """Edit distance (Levenshtein distance) metric."""
    
    version = "1.0.0"
    description = "Character-level edit distance metric"
    
    def _setup(self) -> None:
        """Setup the edit distance metric."""
        self.normalize = self.config.get('normalize', True)
    
    def _calculate_score(self, predicted: str, groundtruth: str, **kwargs) -> MetricResult:
        """
        Calculate edit distance between predicted and ground truth text.
        
        Args:
            predicted: Predicted text
            groundtruth: Ground truth text
            
        Returns:
            MetricResult with edit distance score
        """
        if not isinstance(predicted, str) or not isinstance(groundtruth, str):
            return MetricResult.create_error_result(
                self.name, "Both inputs must be strings"
            )
        
        # Calculate edit distance using difflib
        distance = self._levenshtein_distance(predicted, groundtruth)
        
        # Normalize by the length of the longer string
        if self.normalize:
            max_len = max(len(predicted), len(groundtruth))
            if max_len == 0:
                score = 1.0  # Both strings are empty
            else:
                score = 1.0 - (distance / max_len)
        else:
            score = distance
        
        details = {
            "distance": distance,
            "predicted_length": len(predicted),
            "groundtruth_length": len(groundtruth),
            "normalized": self.normalize,
        }
        
        return MetricResult(
            metric_name=self.name,
            score=score,
            details=details
        )
    
    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """Calculate Levenshtein distance between two strings."""

        return Levenshtein.distance(s1, s2)



class BLEUMetric(BaseMetric):
    """BLEU score metric for text similarity."""
    
    version = "1.0.0"
    description = "BLEU score for text similarity evaluation"
    
    def _setup(self) -> None:
        """Setup the BLEU metric."""
        try:
            from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
            self._sentence_bleu = sentence_bleu
            self._smoothing = SmoothingFunction()
        except ImportError:
            raise RuntimeError("NLTK is required for BLEU metric")
        
        self.max_n = self.config.get('max_n', 4)
        self.smoothing_method = self.config.get('smoothing_method', 'method1')
    
    def _calculate_score(self, predicted: str, groundtruth: str, **kwargs) -> MetricResult:
        """
        Calculate BLEU score between predicted and ground truth text.
        
        Args:
            predicted: Predicted text
            groundtruth: Ground truth text
            
        Returns:
            MetricResult with BLEU score
        """
        if not isinstance(predicted, str) or not isinstance(groundtruth, str):
            return MetricResult.create_error_result(
                self.name, "Both inputs must be strings"
            )
        
        # Tokenize texts (simple whitespace tokenization)
        predicted_tokens = predicted.split()
        groundtruth_tokens = groundtruth.split()
        
        if not predicted_tokens and not groundtruth_tokens:
            score = 1.0  # Both are empty
        elif not predicted_tokens or not groundtruth_tokens:
            score = 0.0  # One is empty
        else:
            # Calculate BLEU score
            smoothing_func = getattr(self._smoothing, self.smoothing_method)
            score = self._sentence_bleu(
                [groundtruth_tokens], 
                predicted_tokens,
                smoothing_function=smoothing_func
            )
        
        details = {
            "predicted_tokens": len(predicted_tokens),
            "groundtruth_tokens": len(groundtruth_tokens),
            "max_n": self.max_n,
            "smoothing_method": self.smoothing_method,
        }
        
        return MetricResult(
            metric_name=self.name,
            score=score,
            details=details
        )


class ROUGEMetric(BaseMetric):
    """ROUGE score metric for text similarity."""
    
    version = "1.0.0"
    description = "ROUGE score for text similarity evaluation"
    
    def _setup(self) -> None:
        """Setup the ROUGE metric."""
        try:
            import rouge
            self._rouge = rouge.Rouge()
        except ImportError:
            raise RuntimeError("rouge-score package is required for ROUGE metric")
        
        self.rouge_types = self.config.get('rouge_types', ['rouge-1', 'rouge-2', 'rouge-l'])
        self.use_stemmer = self.config.get('use_stemmer', True)
    
    def _calculate_score(self, predicted: str, groundtruth: str, **kwargs) -> MetricResult:
        """
        Calculate ROUGE score between predicted and ground truth text.
        
        Args:
            predicted: Predicted text
            groundtruth: Ground truth text
            
        Returns:
            MetricResult with ROUGE scores
        """
        if not isinstance(predicted, str) or not isinstance(groundtruth, str):
            return MetricResult.create_error_result(
                self.name, "Both inputs must be strings"
            )
        
        if not predicted.strip() and not groundtruth.strip():
            # Both are empty
            score = 1.0
            details = {"rouge-1": {"f": 1.0}, "rouge-2": {"f": 1.0}, "rouge-l": {"f": 1.0}}
        elif not predicted.strip() or not groundtruth.strip():
            # One is empty
            score = 0.0
            details = {"rouge-1": {"f": 0.0}, "rouge-2": {"f": 0.0}, "rouge-l": {"f": 0.0}}
        else:
            # Calculate ROUGE scores
            try:
                scores = self._rouge.get_scores(predicted, groundtruth)[0]
                # Use ROUGE-L F1 as the main score
                score = scores['rouge-l']['f']
                details = scores
            except Exception as e:
                return MetricResult.create_error_result(
                    self.name, f"ROUGE calculation failed: {str(e)}"
                )
        
        return MetricResult(
            metric_name=self.name,
            score=score,
            details=details
        ) 


class CodeEditMetric(EditDistanceMetric):
    """代码编辑距离指标"""
    
    version = "1.0.0"
    description = "Code block edit distance metric"
    
    def _calculate_score(self, predicted: str, groundtruth: str, 
                        predicted_content_list: List[Dict[str, Any]] = None,
                        groundtruth_content_list: List[Dict[str, Any]] = None,
                        **kwargs) -> MetricResult:
        """计算代码块的编辑距离"""
        
        # 从content_list中提取代码内容
        pred_code = self._extract_code_content(predicted, predicted_content_list)
        gt_code = self._extract_code_content(groundtruth, groundtruth_content_list)
        
        # 计算编辑距离
        result = super()._calculate_score(pred_code, gt_code, **kwargs)
        result.metric_name = self.name
        result.details.update({
            "predicted_code_length": len(pred_code),
            "groundtruth_code_length": len(gt_code),
            "content_type": "code"
        })
        
        return result
    
    def _extract_code_content(self, text: str, content_list: List[Dict[str, Any]] = None) -> str:
        """从文本和content_list中提取代码内容"""
        # 使用统一的内容分割方法
        content_parts = self.split_content(text, content_list)
        return content_parts.get('code', '')
    
    def _extract_codes_from_content_list(self, content_list: List[Dict[str, Any]]) -> List[str]:
        """递归从content_list中提取代码内容"""
        codes = []
        
        def _recursive_extract(items):
            if not isinstance(items, list):
                return
            
            for item in items:
                if not isinstance(item, dict):
                    continue
                
                # 检查当前项是否为代码
                item_type = item.get('type', '')
                if item_type in ['code']:
                    content = item.get('content', '')
                    if content:
                        codes.append(content)
                
                # 递归检查children字段
                children = item.get('children')
                if children:
                    _recursive_extract(children)
                
                # 递归检查items字段
                items_field = item.get('items')
                if items_field:
                    _recursive_extract(items_field)
        
        _recursive_extract(content_list)
        return codes


class TextEditMetric(EditDistanceMetric):
    """纯文本编辑距离指标（除代码、表格、公式外的文本）"""
    
    version = "1.0.0"
    description = "Pure text edit distance metric (excluding code, tables, formulas)"
    
    def _calculate_score(self, predicted: str, groundtruth: str,
                        predicted_content_list: List[Dict[str, Any]] = None,
                        groundtruth_content_list: List[Dict[str, Any]] = None,
                        **kwargs) -> MetricResult:
        """计算纯文本的编辑距离"""
        
        # 从文本中移除代码、表格、公式
        pred_text = self._extract_pure_text(predicted, predicted_content_list)
        gt_text = self._extract_pure_text(groundtruth, groundtruth_content_list)
        
        # 计算编辑距离
        result = super()._calculate_score(pred_text, gt_text, **kwargs)
        result.metric_name = self.name
        result.details.update({
            "predicted_text_length": len(pred_text),
            "groundtruth_text_length": len(gt_text),
            "content_type": "text"
        })
        
        return result
    
    def _extract_pure_text(self, text: str, content_list: List[Dict[str, Any]] = None) -> str:
        """提取纯文本内容（排除代码、表格、公式）"""
        # 使用统一的内容分割方法
        content_parts = self.split_content(text, content_list)
        return content_parts.get('text', '')
    
    def _extract_text_from_content_list(self, content_list: List[Dict[str, Any]]) -> List[str]:
        """递归从content_list中提取纯文本内容（排除代码、表格、公式）"""
        texts = []
        
        def _recursive_extract(items):
            if not isinstance(items, list):
                return
            
            for item in items:
                if not isinstance(item, dict):
                    continue
                
                # 检查当前项是否为纯文本内容
                item_type = item.get('type', '')
                # 排除代码、表格、公式等特殊内容类型
                if item_type in ['paragraph', 'heading', 'text', 'list_item', 'list-item']:
                    content = item.get('content', '')
                    if content:
                        texts.append(content)
                
                # 递归检查children字段
                children = item.get('children')
                if children:
                    _recursive_extract(children)
                
                # 递归检查items字段
                items_field = item.get('items')
                if items_field:
                    _recursive_extract(items_field)
        
        _recursive_extract(content_list)
        return texts

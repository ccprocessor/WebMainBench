"""
Formula extraction metrics for WebMainBench.
"""

from typing import Dict, Any, List
import re
from .base import BaseMetric, MetricResult
from .text_metrics import EditDistanceMetric


class FormulaEditMetric(EditDistanceMetric):
    """公式编辑距离指标（包括行内和行间公式）"""
    
    version = "1.0.0"
    description = "Formula (inline and block) edit distance metric"
    
    def _calculate_score(self, predicted: str, groundtruth: str,
                        predicted_content_list: List[Dict[str, Any]] = None,
                        groundtruth_content_list: List[Dict[str, Any]] = None,
                        **kwargs) -> MetricResult:
        """计算公式的编辑距离"""
        
        # 从content_list中提取公式内容
        pred_formula = self._extract_formula_content(predicted, predicted_content_list)
        gt_formula = self._extract_formula_content(groundtruth, groundtruth_content_list)
        
        # 计算编辑距离
        result = super()._calculate_score(pred_formula, gt_formula, **kwargs)
        result.metric_name = self.name
        result.details.update({
            "predicted_formula_length": len(pred_formula),
            "groundtruth_formula_length": len(gt_formula),
            "content_type": "formula"
        })
        
        return result
    
    def _extract_formula_content(self, text: str, content_list: List[Dict[str, Any]] = None) -> str:
        """从文本和content_list中提取公式内容"""
        # 使用统一的内容分割方法
        content_parts = self.split_content(text, content_list)
        return content_parts.get('formula', '')
    
    def _extract_formulas_from_content_list(self, content_list: List[Dict[str, Any]]) -> List[str]:
        """递归从content_list中提取公式内容"""
        formulas = []
        
        def _recursive_extract(items):
            if not isinstance(items, list):
                return
            
            for item in items:
                if not isinstance(item, dict):
                    continue
                
                # 检查当前项是否为公式
                item_type = item.get('type', '')
                if item_type in ['equation-interline', 'equation-inline']:
                    content = item.get('content', '')
                    if content:
                        formulas.append(content)
                
                # 递归检查children字段
                children = item.get('children')
                if children:
                    _recursive_extract(children)
                
                # 递归检查items字段（有些实现可能使用items）
                items_field = item.get('items')
                if items_field:
                    _recursive_extract(items_field)
        
        _recursive_extract(content_list)
        return formulas 
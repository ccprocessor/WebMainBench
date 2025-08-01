"""
Table extraction metrics for WebMainBench.
"""

from typing import Dict, Any, List
import re
from .base import BaseMetric, MetricResult
from .teds_metrics import TEDSMetric, StructureTEDSMetric
from .text_metrics import EditDistanceMetric


class TableEditMetric(EditDistanceMetric):
    """表格编辑距离指标"""
    
    version = "1.0.0"
    description = "Table content edit distance metric"
    
    def _calculate_score(self, predicted: str, groundtruth: str,
                        predicted_content_list: List[Dict[str, Any]] = None,
                        groundtruth_content_list: List[Dict[str, Any]] = None,
                        **kwargs) -> MetricResult:
        """计算表格内容的编辑距离"""
        
        # 从content_list中提取表格内容
        pred_table = self._extract_table_content(predicted, predicted_content_list)
        gt_table = self._extract_table_content(groundtruth, groundtruth_content_list)
        
        # 计算编辑距离
        result = super()._calculate_score(pred_table, gt_table, **kwargs)
        result.metric_name = self.name
        result.details.update({
            "predicted_table_length": len(pred_table),
            "groundtruth_table_length": len(gt_table),
            "content_type": "table"
        })
        
        return result
    
    def _extract_table_content(self, text: str, content_list: List[Dict[str, Any]] = None) -> str:
        """从文本和content_list中提取表格内容"""
        # 使用统一的内容分割方法
        content_parts = self.split_content(text, content_list)
        return content_parts.get('table', '')
    
    def _extract_tables_from_content_list(self, content_list: List[Dict[str, Any]]) -> List[str]:
        """递归从content_list中提取表格内容"""
        tables = []
        
        def _recursive_extract(items):
            if not isinstance(items, list):
                return
            
            for item in items:
                if not isinstance(item, dict):
                    continue
                
                # 检查当前项是否为表格
                item_type = item.get('type', '')
                if item_type in ['table']:
                    content = item.get('content', '')
                    if content:
                        tables.append(content)
                
                # 递归检查children字段
                children = item.get('children')
                if children:
                    _recursive_extract(children)
                
                # 递归检查items字段
                items_field = item.get('items')
                if items_field:
                    _recursive_extract(items_field)
        
        _recursive_extract(content_list)
        return tables


class TableTEDSMetric(TEDSMetric):
    """表格TEDS指标"""
    
    version = "1.0.0"
    description = "Table TEDS (Tree-Edit Distance based Similarity) metric"
    
    def _calculate_score(self, predicted: str, groundtruth: str,
                        predicted_content_list: List[Dict[str, Any]] = None,
                        groundtruth_content_list: List[Dict[str, Any]] = None,
                        **kwargs) -> MetricResult:
        """计算表格的TEDS分数"""
        
        # 从content_list中提取表格内容
        pred_table = self._extract_table_content(predicted, predicted_content_list)
        gt_table = self._extract_table_content(groundtruth, groundtruth_content_list)
        
        # 使用父类的TEDS计算
        result = super()._calculate_score(pred_table, gt_table, **kwargs)
        result.metric_name = self.name
        result.details.update({
            "content_type": "table",
            "algorithm": "TEDS"
        })
        
        return result
    
    def _extract_table_content(self, text: str, content_list: List[Dict[str, Any]] = None) -> str:
        """从文本和content_list中提取表格内容"""
        # 使用统一的内容分割方法
        content_parts = self.split_content(text, content_list)
        return content_parts.get('table', '') 
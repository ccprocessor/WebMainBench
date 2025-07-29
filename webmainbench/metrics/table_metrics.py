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
        table_parts = []
        
        # 优先从content_list中递归提取
        if content_list:
            table_parts = self._extract_tables_from_content_list(content_list)
            
            # 如果content_list中有表格，直接返回
            if table_parts:
                return '\n'.join(table_parts)
        
        # 只有当content_list中没有表格时，才从markdown文本中提取
        if text:
            lines = text.split('\n')
            table_lines = []
            in_table = False
            
            for line in lines:
                if '|' in line:
                    table_lines.append(line)
                    in_table = True
                elif in_table and line.strip() == '':
                    # 表格结束
                    if table_lines:
                        table_parts.append('\n'.join(table_lines))
                        table_lines = []
                    in_table = False
                elif in_table:
                    # 表格内的非表格行，表格结束
                    if table_lines:
                        table_parts.append('\n'.join(table_lines))
                        table_lines = []
                    in_table = False
            
            # 处理文档末尾的表格
            if table_lines:
                table_parts.append('\n'.join(table_lines))
        
        return '\n'.join(table_parts)
    
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
        # 复用TableEditMetric的表格提取逻辑
        table_edit_metric = TableEditMetric("temp")
        return table_edit_metric._extract_table_content(text, content_list) 
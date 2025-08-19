"""
Base metric interface for WebMainBench.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Union
import traceback
import re
from bs4 import BeautifulSoup

@dataclass
class MetricResult:
    """Result of metric calculation."""
    
    metric_name: str
    score: float
    details: Dict[str, Any] = None
    success: bool = True
    error_message: Optional[str] = None
    
    def __post_init__(self):
        if self.details is None:
            self.details = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "metric_name": self.metric_name,
            "score": self.score,
            "details": self.details,
            "success": self.success,
            "error_message": self.error_message,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MetricResult":
        """Create from dictionary."""
        return cls(**data)
    
    @classmethod
    def create_error_result(cls, metric_name: str, error_message: str) -> "MetricResult":
        """Create an error result."""
        return cls(
            metric_name=metric_name,
            score=0.0,
            success=False,
            error_message=error_message
        )


class BaseMetric(ABC):
    """Base class for all evaluation metrics."""
    
    def __init__(self, name: str, config: Dict[str, Any] = None):
        """
        Initialize the metric.
        
        Args:
            name: Name of the metric
            config: Configuration dictionary
        """
        self.name = name
        self.config = config or {}
        self._setup()
    
    @abstractmethod
    def _setup(self) -> None:
        """Setup the metric (load models, initialize components, etc.)."""
        pass
    
    @abstractmethod
    def _calculate_score(self, predicted: Any, groundtruth: Any, **kwargs) -> MetricResult:
        """
        Calculate the metric score.
        
        Args:
            predicted: Predicted/extracted content
            groundtruth: Ground truth content
            **kwargs: Additional arguments
            
        Returns:
            MetricResult instance
        """
        pass
    
    def calculate(self, predicted: Any, groundtruth: Any, **kwargs) -> MetricResult:
        """
        Calculate metric with error handling.
        
        Args:
            predicted: Predicted/extracted content
            groundtruth: Ground truth content
            **kwargs: Additional arguments
            
        Returns:
            MetricResult instance
        """
        try:
            return self._calculate_score(predicted, groundtruth, **kwargs)
        except Exception as e:
            error_message = f"Metric calculation failed: {str(e)}"
            return MetricResult.create_error_result(self.name, error_message)
    
    def batch_calculate(self, predicted_list: List[Any], 
                       groundtruth_list: List[Any],
                       **kwargs) -> List[MetricResult]:
        """
        Calculate metrics for multiple samples.
        
        Args:
            predicted_list: List of predicted/extracted content
            groundtruth_list: List of ground truth content
            **kwargs: Additional arguments
            
        Returns:
            List of MetricResult instances
        """
        results = []
        for pred, gt in zip(predicted_list, groundtruth_list):
            result = self.calculate(pred, gt, **kwargs)
            results.append(result)
        return results
    
    @staticmethod
    def split_content(text: str, content_list: List[Dict[str, Any]] = None) -> Dict[str, str]:
        """
        统一的内容分割方法，将文本分为代码、公式、表格和剩余文本4个部分。
        
        Args:
            text: 原始markdown文本
            content_list: 结构化内容列表（来自llm-webkit等）
            
        Returns:
            Dict with keys: 'code', 'formula', 'table', 'text'
        """
        # 优先从content_list中提取
        if content_list:
            extracted_content = BaseMetric._extract_from_content_list(content_list)
            if any(extracted_content.values()):
                return extracted_content
        
        # 从markdown文本中提取
        return BaseMetric._extract_from_markdown(text or "")
    
    @staticmethod
    def _extract_from_content_list(content_list: List[Dict[str, Any]]) -> Dict[str, str]:
        """从content_list中递归提取各种类型的内容"""
        extracted = {
            'code': [],
            'formula': [],  
            'table': [],
            'text': []
        }
        
        def _recursive_extract(items):
            if not isinstance(items, list):
                return
            
            for item in items:
                if not isinstance(item, dict):
                    continue
                
                item_type = item.get('type', '').lower()
                content = item.get('content', '').strip()
                
                # 根据类型分类内容
                if item_type in ['code', 'code_block', 'inline_code']:
                    if content:
                        extracted['code'].append(content)
                elif item_type in ['formula', 'math', 'equation', 'latex']:
                    if content:
                        extracted['formula'].append(content)
                elif item_type in ['table', 'table_content', 'html_table', 'table_row', 'table_cell']:
                    if content:
                        extracted['table'].append(content)
                elif item_type in ['text', 'paragraph', 'heading']:
                    if content:
                        extracted['text'].append(content)
                
                # 递归处理子元素
                for child_key in ['children', 'items', 'content_list']:
                    if child_key in item and isinstance(item[child_key], list):
                        _recursive_extract(item[child_key])
        
        _recursive_extract(content_list)
        
        # 将列表转换为字符串
        return {
            'code': '\n'.join(extracted['code']),
            'formula': '\n'.join(extracted['formula']),
            'table': '\n'.join(extracted['table']),
            'text': '\n'.join(extracted['text'])
        }
    
    @staticmethod 
    def _extract_from_markdown(text: str) -> Dict[str, str]:
        """从markdown文本中提取各种类型的内容"""
        if not text:
            return {'code': '', 'formula': '', 'table': '', 'text': ''}
        
        # 收集所有需要移除的内容片段
        extracted_segments = []
        code_parts = []
        # 同时匹配行内代码 `...` 和代码块 ```...```
        pattern = r'(```[\s\S]*?```|`[^`\n]+`)'
        for match in re.finditer(pattern, text):
            code_segment = match.group(0)
            extracted_segments.append(code_segment)

            if code_segment.startswith('```'):
                # 处理代码块（保留内部缩进）
                lines = code_segment.split('\n')
                # 移除首尾的```标记
                content_lines = lines[1:-1]
                # 保留原始缩进，只拼接内容
                code_content = '\n'.join(content_lines)
            else:
                # 处理行内代码（只去除外层`和前后空格）
                code_content = code_segment[1:-1].strip()

            if code_content:  # 只添加非空内容
                code_parts.append(code_content)
        
        # # 提取代码
        # code_parts = []
        # # 代码块 ```code```
        # for match in re.finditer(r'```[\s\S]*?```', text):
        #     code_block = match.group(0)
        #     extracted_segments.append(code_block)
        #     code_parts.append(code_block.strip('`').strip())
        #
        # # 行内代码 `code`
        # for match in re.finditer(r'`([^`]+)`', text):
        #     inline_code_full = match.group(0)  # 包含反引号的完整匹配
        #     inline_code_content = match.group(1)  # 只是内容
        #     extracted_segments.append(inline_code_full)
        #     code_parts.append(inline_code_content)
        
        # 提取公式
        formula_parts = []
        # 统一的公式提取模式
        latex_patterns = [
            # r'(?<!\\)\$\$([^$]+)\$\$(?!\\)',  # Display math (not escaped)
            # r'(?<!\\)\$([^$\n]+)\$(?![\\\$])',  # Inline math (not escaped)
            # r'\\begin\{equation\*?\}(.*?)\\end\{equation\*?\}',  # Equation environment
            # r'\\begin\{align\*?\}(.*?)\\end\{align\*?\}',        # Align environment
            # r'\\begin\{gather\*?\}(.*?)\\end\{gather\*?\}',      # Gather environment
            # r'\\begin\{eqnarray\*?\}(.*?)\\end\{eqnarray\*?\}',  # Eqnarray environment
            # r'\\begin\{multline\*?\}(.*?)\\end\{multline\*?\}',  # Multline environment
            # r'\\begin\{split\}(.*?)\\end\{split\}',              # Split environment
            # r'(?<!\\)\$\$([^$]+)\$\$(?!\\)',
            # r'(?<!\\)\$([^$\n\w][^$\n]*[^$\n\w])\$(?![\\\$])',
            r'(?<!\\)\$\$(.*?)(?<!\\)\$\$',  # 行间 $$...$$，确保 $ 没有被转义
            r'(?<!\\)\\\[(.*?)(?<!\\)\\\]',  # 行间 \[...\]，确保 \ 没有被转义
            r'(?<!\\)\$(.*?)(?<!\\)\$',  # 行内 $...$，确保 $ 没有被转义
            r'(?<!\\)\\\((.*?)(?<!\\)\\\)',  # 行内 \(...\)，确保 \ 没有被转义
        ]
        
        for pattern in latex_patterns:
            for match in re.finditer(pattern, text, re.DOTALL):
                formula_full = match.group(0)  # 完整匹配（包含$符号）
                formula_content = match.group(1)  # 只是公式内容
                extracted_segments.append(formula_full)
                if formula_content.strip():
                    formula_parts.append(formula_content.strip())

        # 提取表格
        table_parts = []

        # ===== 1. 提取 HTML 表格 =====
        # 用 BeautifulSoup 替代正则，防止嵌套或匹配不全
        soup = BeautifulSoup(text, "html.parser")
        for table in soup.find_all("table"):
            html_table = str(table)
            extracted_segments.append(html_table)
            table_parts.append(html_table)

        # ===== 2. 提取 Markdown 表格 =====
        lines = text.split('\n')
        table_lines = []
        in_markdown_table = False
        found_separator = False  # 是否已找到分隔行

        def is_md_table_line(line):
            """判断是否可能是 Markdown 表格行"""
            if line.count("|") < 3:  # 至少三个竖线
                return False
            return True

        def is_md_separator_line(line):
            """判断是否为 Markdown 分隔行"""
            parts = [p.strip() for p in line.split("|")]
            # 检查是否所有部分都是分隔符格式
            for p in parts:
                if p and not re.match(r"^:?\-{3,}:?$", p):
                    return False
            return True

        def save_table():
            """保存当前表格并清空缓存"""
            nonlocal table_lines
            # 只有当表格行数大于等于2，且第二行是分隔行时才保存
            if len(table_lines) >= 2 and is_md_separator_line(table_lines[1]):
                md_table = '\n'.join(table_lines)
                extracted_segments.append(md_table)
                table_parts.append(md_table)

        for line in lines:
            if is_md_table_line(line):
                table_lines.append(line)
                in_markdown_table = True
                if is_md_separator_line(line):
                    found_separator = True
            else:
                if in_markdown_table:
                    save_table()
                    table_lines = []
                    in_markdown_table = False
                    found_separator = False

        # 处理文档末尾的 Markdown 表格
        if in_markdown_table:
            save_table()

        # 提取剩余文本（移除所有已提取的内容片段）
        clean_text = text
        for segment in extracted_segments:
            clean_text = clean_text.replace(segment, '', 1)
        
        # 清理多余的空行
        clean_text = re.sub(r'\n\s*\n', '\n\n', clean_text)
        clean_text = clean_text.strip()
        
        return {
            'code': '\n'.join(code_parts),
            'formula': '\n'.join(formula_parts),
            'table': '\n'.join(table_parts),
            'text': clean_text
        }
    
    def aggregate_results(self, results: List[MetricResult]) -> MetricResult:
        """
        Aggregate multiple metric results.
        
        Args:
            results: List of MetricResult instances
            
        Returns:
            Aggregated MetricResult
        """
        if not results:
            return MetricResult.create_error_result(self.name, "No results to aggregate")
        
        # Filter successful results
        successful_results = [r for r in results if r.success]
        
        if not successful_results:
            return MetricResult.create_error_result(self.name, "All calculations failed")
        
        # Calculate aggregate score (mean by default)
        scores = [r.score for r in successful_results]
        avg_score = sum(scores) / len(scores)
        
        # Aggregate details
        aggregate_details = {
            "num_samples": len(results),
            "num_successful": len(successful_results),
            "num_failed": len(results) - len(successful_results),
            "scores": scores,
            "min_score": min(scores),
            "max_score": max(scores),
            "std_score": self._calculate_std(scores),
        }
        
        return MetricResult(
            metric_name=f"{self.name}_aggregate",
            score=avg_score,
            details=aggregate_details,
            success=True
        )
    
    def _calculate_std(self, scores: List[float]) -> float:
        """Calculate standard deviation."""
        if len(scores) <= 1:
            return 0.0
        
        mean = sum(scores) / len(scores)
        variance = sum((x - mean) ** 2 for x in scores) / (len(scores) - 1)
        return variance ** 0.5
    
    def get_config(self) -> Dict[str, Any]:
        """Get metric configuration."""
        return self.config.copy()
    
    def set_config(self, config: Dict[str, Any]) -> None:
        """Update metric configuration."""
        self.config.update(config)
    
    def get_info(self) -> Dict[str, Any]:
        """Get metric information."""
        return {
            "name": self.name,
            "config": self.get_config(),
            "version": getattr(self, 'version', 'unknown'),
            "description": getattr(self, 'description', ''),
        }
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
    
    def __repr__(self) -> str:
        return self.__str__() 
"""
Base metric interface for WebMainBench.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Union
import traceback
import re

class ParagraphTextType(object):
    TEXT = 'text'
    MARKDOWN = 'md'
    EQUATION_INLINE = 'equation-inline'
    CODE_INLINE = 'code-inline'

class DocElementType(object):
    PARAGRAPH = 'paragraph'
    LIST = 'list'
    SIMPLE_TABLE = 'simple_table'
    COMPLEX_TABLE = 'complex_table'
    EQUATION_INTERLINE = 'equation-interline'
    CODE = 'code'
    TITLE = 'title'

    EQUATION_INLINE = ParagraphTextType.EQUATION_INLINE

    IMAGE = 'image'
    AUDIO = 'audio'
    VIDEO = 'video'

    MM_NODE_LIST = [IMAGE, AUDIO, VIDEO]

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
        """从markdown文本中提取各种类型的内容，采用extract.py的改进思路"""
        if not text:
            return {'code': '', 'formula': '', 'table': '', 'text': '', 'md': ''}
        
        # 预处理：移除图片
        img_pattern = r'!\[.*?\]\(.*?\)'
        text = re.sub(img_pattern, '', text)
        
        # 收集所有提取的内容片段
        extracted_segments = []
        
        # 1. 提取代码块 - 使用更精确的匹配
        code_parts = []
        code_block_pattern = r'```(\w+)?\n(.*?)```'
        for match in re.finditer(code_block_pattern, text, re.DOTALL):
            language = match.group(1) or ''
            code_content = match.group(2).strip()
            code_block = match.group(0)
            extracted_segments.append((match.start(), match.end(), code_block))
            code_parts.append(f"```{language}\n{code_content}\n```")
        
        # 行内代码
        inline_code_pattern = r'`([^`]+)`'
        for match in re.finditer(inline_code_pattern, text):
            inline_code = match.group(0)
            code_content = match.group(1)
            extracted_segments.append((match.start(), match.end(), inline_code))
            code_parts.append(code_content)
        
        # 2. 提取数学公式 - 使用更全面的模式
        formula_parts = []
        # 块级公式
        display_patterns = [
            r'\$\$(.*?)\$\$',           # $$...$$
            r'\\\[(.*?)\\\]',           # \[...\]
            r'\\begin\{equation\*?\}(.*?)\\end\{equation\*?\}',  # equation环境
            r'\\begin\{align\*?\}(.*?)\\end\{align\*?\}',        # align环境
            r'\\begin\{gather\*?\}(.*?)\\end\{gather\*?\}',      # gather环境
            r'\\begin\{eqnarray\*?\}(.*?)\\end\{eqnarray\*?\}',  # eqnarray环境
            r'\\begin\{multline\*?\}(.*?)\\end\{multline\*?\}',  # multline环境
            r'\\begin\{split\}(.*?)\\end\{split\}'               # split环境
        ]
        
        for pattern in display_patterns:
            for match in re.finditer(pattern, text, re.DOTALL):
                formula_full = match.group(0)
                formula_content = match.group(1)
                extracted_segments.append((match.start(), match.end(), formula_full))
                if formula_content.strip():
                    # 统一格式为$$...$$
                    clean_content = formula_content.strip()
                    formula_parts.append(f"$${clean_content}$$")
        
        # 行内公式
        inline_patterns = [
            # 更精确的行内公式匹配，避免误识别价格
            r'(?<!\$)\$(?!\$)([^$\n]+?)(?<!\$)\$(?!\$)',  # $...$ (避免$$)
            r'\\\((.*?)\\\)'                               # \(...\)
        ]
        
        for pattern in inline_patterns:
            for match in re.finditer(pattern, text):
                formula_full = match.group(0)
                formula_content = match.group(1)
                
                # 添加验证：检查内容是否真的像数学公式
                if BaseMetric._is_valid_math_formula(formula_content):
                    extracted_segments.append((match.start(), match.end(), formula_full))
                    if formula_content.strip():
                        formula_parts.append(f"${formula_content.strip()}$")
        
        # 3. 提取表格 - 使用栈结构处理嵌套
        table_parts = []
        
        # 提取HTML表格
        def extract_html_tables(content):
            """使用栈结构提取嵌套的HTML表格"""
            begin_pattern = r'<table(?:[^>]*)>'
            end_pattern = r'</table>'
            
            tables = []
            positions = []
            current_pos = 0
            stack = []
            
            while current_pos < len(content):
                begin_match = re.search(begin_pattern, content[current_pos:])
                end_match = re.search(end_pattern, content[current_pos:])
                
                if not begin_match and not end_match:
                    break
                    
                if begin_match and (not end_match or begin_match.start() < end_match.start()):
                    stack.append(current_pos + begin_match.start())
                    current_pos += begin_match.start() + len(begin_match.group())
                elif end_match:
                    if stack:
                        start_pos = stack.pop()
                        if not stack:  # 栈为空表示找到完整表格
                            end_pos = current_pos + end_match.start() + len(end_match.group())
                            table_code = content[start_pos:end_pos]
                            tables.append(table_code)
                            positions.append((start_pos, end_pos))
                    current_pos += end_match.start() + len(end_match.group())
                else:
                    current_pos += 1
            
            return tables, positions
        
        html_tables, html_positions = extract_html_tables(text)
        for table, (start, end) in zip(html_tables, html_positions):
            extracted_segments.append((start, end, table))
            table_parts.append(table)
        
        # 提取Markdown表格
        def extract_markdown_tables(content):
            """提取Markdown表格"""
            lines = content.split('\n')
            tables = []
            positions = []
            table_lines = []
            in_table = False
            table_start = 0
            
            for i, line in enumerate(lines):
                if '|' in line and line.strip():
                    # 检查是否真的是表格行
                    if BaseMetric._is_valid_table_row(line):
                        if not in_table:
                            in_table = True
                            table_start = sum(len(l) + 1 for l in lines[:i])  # +1 for newline
                        table_lines.append(line)
                    elif in_table:
                        # 如果当前行不是表格行，但之前有表格行，则结束表格
                        if table_lines:
                            table_content = '\n'.join(table_lines)
                            table_end = table_start + len(table_content)
                            tables.append(table_content)
                            positions.append((table_start, table_end))
                            table_lines = []
                        in_table = False
                elif in_table:
                    # 空行或非表格行，结束表格
                    if table_lines:
                        table_content = '\n'.join(table_lines)
                        table_end = table_start + len(table_content)
                        tables.append(table_content)
                        positions.append((table_start, table_end))
                        table_lines = []
                    in_table = False
            
            # 处理文档末尾的表格
            if table_lines:
                table_content = '\n'.join(table_lines)
                table_end = table_start + len(table_content)
                tables.append(table_content)
                positions.append((table_start, table_end))
            
            return tables, positions
        
        md_tables, md_positions = extract_markdown_tables(text)
        for table, (start, end) in zip(md_tables, md_positions):
            extracted_segments.append((start, end, table))
            table_parts.append(table)
        
        # 4. 提取标题
        title_parts = []
        title_pattern = r'^\s*(#{1,6})\s+(.+)$'
        for match in re.finditer(title_pattern, text, re.MULTILINE):
            level = len(match.group(1))
            title_content = match.group(2).strip()
            title_full = match.group(0)
            extracted_segments.append((match.start(), match.end(), title_full))
            title_parts.append(f"{'#' * level} {title_content}")
        
        # 5. 清理和替换已提取的内容
        # 按位置排序，从后往前替换，避免位置偏移
        extracted_segments.sort(key=lambda x: x[0], reverse=True)
        
        clean_text = text
        for start, end, segment in extracted_segments:
            clean_text = clean_text[:start] + ' ' * (end - start) + clean_text[end:]
        
        # 6. 清理LaTeX样式
        clean_text = re.sub(r'\\title\{(.*?)\}', r'\1', clean_text)
        clean_text = re.sub(r'\\section\*?\{(.*?)\}', r'\1', clean_text)
        clean_text = re.sub(r'\\text\s*\{\s*(.*?)\s*\}', r'\1', clean_text, flags=re.DOTALL)
        
        # 7. 提取剩余文本块
        text_parts = []
        # 按段落分割
        paragraphs = clean_text.split('\n\n')
        if len(paragraphs) == 1:
            paragraphs = clean_text.split('\n')  # 如果没有双换行，按单换行分割
        
        for para in paragraphs:
            para = para.strip()
            if para:
                # 清理多余空格和换行
                para = re.sub(r'\s+', ' ', para)
                para = para.strip()
                if para:
                    text_parts.append(para)
        
        # 8. 处理特殊格式的数学公式
        # 处理[tex][/tex]和[itex][/itex]格式
        text_parts_processed = []
        for para in text_parts:
            # 处理[tex]...[/tex]格式
            para = re.sub(r'\[tex\](.*?)\[/tex\]', r'$$\1$$', para, flags=re.DOTALL)
            # 处理[itex]...[/itex]格式
            para = re.sub(r'\[itex\](.*?)\[/itex\]', r'$\1$', para, flags=re.DOTALL)
            text_parts_processed.append(para)
        
        return {
            'code': '\n\n'.join(code_parts),
            'formula': '\n\n'.join(formula_parts),
            'table': '\n\n'.join(table_parts),
            'text': '\n\n'.join(text_parts_processed),
            'md': text
        }
    
    @staticmethod
    def _is_valid_math_formula(content: str) -> bool:
        """
        验证内容是否为有效的数学公式
        Args:
            content: 被$包围的内容
        Returns:
            bool: 是否为有效的数学公式
        """
        content = content.strip()
        
        # 如果内容太短，可能是价格
        if len(content) < 3:
            return False
        
        # 检查是否是不完整的公式（以-结尾）
        if content.endswith('-'):
            return False
        
        # 检查文字密度 - 数学公式不应该包含太多完整单词
        words = content.split()
        long_words = [word for word in words if len(word) > 6]  # 超过6个字符的单词
        word_density = len(long_words) / len(words) if words else 0
        
        # 如果包含太多长单词，可能是价格或普通文本
        if word_density > 0.3:  # 超过30%是长单词
            return False
        
        # 检查是否包含常见的价格相关词汇
        price_words = [
            'billion', 'million', 'thousand', 'hundred', 'dollars', 'dollar',
            'cents', 'cent', 'pounds', 'pound', 'euros', 'euro', 'yuan',
            'won', 'yen', 'rupees', 'rupee', 'francs', 'franc', 'marks',
            'mark', 'pesos', 'peso', 'liras', 'lira', 'kroner', 'krona',
            'kronor', 'krona', 'zloty', 'forint', 'koruna', 'leu', 'lei',
            'lev', 'leva', 'taka', 'ringgit', 'baht', 'dong', 'rupiah',
            'tugrik', 'kyat', 'kip', 'riel', 'kina', 'vatu', 'tala',
            'paanga', 'tolar', 'tolarjev', 'tolarja', 'tolarjev', 'tolarja',
            'credits', 'range', 'per', 'day', 'video', 'set', 'photos', 'costs',
            'total', 'month', 'year', 'week', 'hour', 'minute', 'second'
        ]
        
        content_lower = content.lower()
        has_price_words = any(word in content_lower for word in price_words)
        
        # 如果包含价格词汇，很可能不是公式
        if has_price_words:
            return False
        
        # 检查是否包含常见的数学符号
        math_symbols = [
            r'[+\-*/=<>≤≥≠≈]',  # 数学运算符
            r'[αβγδεθλμπσφω]',  # 希腊字母
            r'[∫∑∏√∞∂∇]',      # 数学符号
            r'[()\[\]{}]',      # 括号
            r'[a-zA-Z]',        # 字母
            r'[0-9]',           # 数字
            r'[^a-zA-Z0-9\s]'   # 特殊字符
        ]
        
        # 检查是否包含数学符号
        has_math_symbols = any(re.search(pattern, content) for pattern in math_symbols)
        
        # 检查是否看起来像价格（只包含数字、逗号、点和美元符号）
        price_pattern = r'^[\d,\.\s]+$'
        looks_like_price = bool(re.match(price_pattern, content))
        
        # 检查是否包含货币单位
        currency_patterns = [
            r'\$[\d,\.]+',  # $29.8 billion
            r'[\d,\.]+\s*billion',  # 29.8 billion
            r'[\d,\.]+\s*million',  # 815 million
            r'[\d,\.]+\s*thousand',  # 500 thousand
            r'[\d,\.]+\s*k',  # 50k
            r'[\d,\.]+\s*K',  # 50K
            r'[\d,\.]+\s*\$',  # 29.8 $
            r'\$[\d,\.]+\s*[a-zA-Z]+',  # $29.8 billion
        ]
        has_currency_units = any(re.search(pattern, content, re.IGNORECASE) for pattern in currency_patterns)
        
        # 检查是否包含常见的数学关键词
        math_keywords = [
            'sin', 'cos', 'tan', 'log', 'ln', 'exp', 'sqrt', 'frac',
            'sum', 'prod', 'int', 'lim', 'inf', 'infty', 'alpha', 'beta',
            'gamma', 'delta', 'theta', 'lambda', 'mu', 'pi', 'sigma', 'phi', 'omega'
        ]
        has_math_keywords = any(keyword in content.lower() for keyword in math_keywords)
        
        # 检查是否包含LaTeX命令
        latex_pattern = r'\\[a-zA-Z]+'
        has_latex_commands = bool(re.search(latex_pattern, content))
        
        # 检查是否包含数学运算符（更严格的检查）
        math_operators = [
            r'[+\-*/=<>≤≥≠≈]',  # 基本运算符
            r'[∫∑∏√∞∂∇]',      # 高级数学符号
            r'[αβγδεθλμπσφω]',  # 希腊字母
            r'[()\[\]{}]',      # 括号
        ]
        has_math_operators = any(re.search(pattern, content) for pattern in math_operators)
        
        # 检查是否包含字母和数字的组合（可能是变量）
        has_variable_pattern = re.search(r'[a-zA-Z].*[0-9]|[0-9].*[a-zA-Z]', content)
        
        # 检查是否包含常见的数学函数和符号
        math_functions = [
            r'\\[a-zA-Z]+',  # LaTeX命令
            r'[a-zA-Z]+\s*\(',  # 函数调用
            r'[a-zA-Z]+\s*[+\-*/=]',  # 变量运算
            r'[+\-*/=]\s*[a-zA-Z]+',  # 运算变量
        ]
        has_math_functions = any(re.search(pattern, content) for pattern in math_functions)
        
        # 如果是价格格式且没有数学符号，则不是公式
        if (looks_like_price or has_currency_units) and not has_math_operators and not has_math_keywords and not has_latex_commands:
            return False
        
        # 如果包含数学符号、关键词或LaTeX命令，则可能是公式
        if has_math_operators or has_math_keywords or has_latex_commands or has_math_functions:
            return True
        
        # 如果内容包含字母和数字的组合，可能是公式
        if has_variable_pattern:
            return True
        
        # 如果内容包含特殊字符且长度适中，可能是公式
        if len(content) > 5 and re.search(r'[^a-zA-Z0-9\s]', content):
            return True
        
        # 默认情况下，不是公式
        return False
    
    @staticmethod
    def _is_valid_table_row(line: str) -> bool:
        """
        验证是否为有效的表格行
        Args:
            line: 包含竖线的行
        Returns:
            bool: 是否为有效的表格行
        """
        line = line.strip()
        
        # 如果行太短，可能不是表格
        if len(line) < 5:
            return False
        
        # 检查是否包含数学公式中的绝对值符号
        # 数学公式中的绝对值通常有这种模式：|变量名| 或 |表达式|
        if re.search(r'\|[A-Za-zαβγδεθλμπσφω]+\|', line):
            return False
        
        # 检查是否包含数学公式中的绝对值（更复杂的模式）
        if re.search(r'\|[^|]+\|', line) and re.search(r'[+\-*/=<>≤≥≠≈∫∑∏√∞∂∇]', line):
            return False
        
        # 检查是否包含LaTeX数学环境
        if re.search(r'\\begin\{.*\}', line) or re.search(r'\\end\{.*\}', line):
            return False
        
        # 检查是否包含LaTeX命令
        if re.search(r'\\[a-zA-Z]+', line):
            return False
        
        # 计算竖线数量
        pipe_count = line.count('|')
        
        # 如果竖线太少，可能不是表格
        if pipe_count < 2:
            return False
        
        # 检查是否包含分隔符行（只包含 | - : 和空格）
        if re.match(r'^[\s|\-:]+$', line):
            return True
        
        # 检查是否包含表格单元格内容
        # 表格行应该包含非空内容
        cells = line.split('|')
        non_empty_cells = [cell.strip() for cell in cells if cell.strip()]
        
        # 如果非空单元格太少，可能不是表格
        if len(non_empty_cells) < 2:
            return False
        
        # 检查是否包含数学公式中的双竖线（范数符号）
        if re.search(r'\|\|[^|]*\|\|', line):
            return False
        
        # 检查是否包含代码中的逻辑运算符
        if re.search(r'\|\|', line) and not re.search(r'\$.*\|\|.*\$', line):
            return False
        
        # 检查是否包含常见的非表格分隔符模式
        non_table_patterns = [
            r'[A-Z]{2}\|[A-Z]{2}',  # 如 BL|NM|PT|SA
            r'\d+\s*\|\s*\d+',      # 如 8GB | 32GB
            r'[A-Za-z]+\s*\|\s*[A-Za-z]+',  # 如 Drama| Biography
            r'[A-Za-z]+\s*Abstract\s*\|\s*[A-Za-z]+',  # 如 PubMed Abstract| Publisher
            r'\d+\s*×\s*\d+\s*pixels\s*\|',  # 如 98 × 240 pixels|
            r'\\[a-zA-Z]+\{[^}]*\|\s*[^}]*\}',  # LaTeX命令中的分隔符
            r'[a-zA-Z_]+\.found\([^)]*\)\s*\|\|\s*[a-zA-Z_]+\.empty\(\)',  # 代码逻辑运算符
        ]
        
        for pattern in non_table_patterns:
            if re.search(pattern, line):
                return False
        
        # 检查是否包含数学公式 - 如果包含数学公式，通常不是表格
        if re.search(r'\$.*\$', line):
            # 检查是否包含复杂的数学内容
            math_indicators = [
                r'\\[a-zA-Z]+\{',  # LaTeX命令
                r'\\[a-zA-Z]+',    # LaTeX命令
                r'[αβγδεθλμπσφω]',  # 希腊字母
                r'[∫∑∏√∞∂∇]',      # 数学符号
                r'\\[a-zA-Z]+\s*\{[^}]*\}',  # LaTeX命令带参数
                r'\\newcommand',   # LaTeX命令定义
                r'\\renewcommand', # LaTeX命令重定义
                r'\\begin\{',      # LaTeX环境开始
                r'\\end\{',        # LaTeX环境结束
            ]
            
            has_math_indicators = any(re.search(pattern, line) for pattern in math_indicators)
            if has_math_indicators:
                return False  # 包含数学公式的行不是表格
        
        # 检查单元格内容是否合理
        for cell in non_empty_cells:
            # 如果单元格内容太长，可能不是表格
            if len(cell) > 100:
                return False
            
            # 如果单元格包含太多特殊字符，可能不是表格
            special_char_ratio = len(re.findall(r'[^a-zA-Z0-9\s]', cell)) / len(cell)
            if special_char_ratio > 0.5:
                return False
            
            # 检查是否包含代码特征
            if re.search(r'[a-zA-Z_]+\([^)]*\)', cell):  # 函数调用
                return False
            
            if re.search(r'[a-zA-Z_]+\.', cell):  # 对象方法调用
                return False
        
        # 检查是否看起来像图片分辨率信息
        if re.search(r'\d+\s*×\s*\d+\s*pixels', line):
            return False
        
        # 检查是否包含文件大小信息
        if re.search(r'\d+\s*[KMGT]?B', line):
            return False
        
        # 检查是否包含URL或路径
        if re.search(r'https?://', line) or re.search(r'[a-zA-Z]:\\', line):
            return False
        
        # 检查是否包含时间格式
        if re.search(r'\d{1,2}:\d{2}(:\d{2})?', line):
            return False
        
        # 检查是否包含日期格式
        if re.search(r'\d{1,2}/\d{1,2}/\d{2,4}', line):
            return False
        
        # 检查是否包含版本号
        if re.search(r'v?\d+\.\d+(\.\d+)?', line):
            return False
        
        # 检查是否包含邮箱地址
        if re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', line):
            return False
        
        # 检查是否包含IP地址
        if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line):
            return False
        
        # 检查是否包含数学表达式（简单的）
        if re.search(r'[+\-*/=<>]', line):
            # 如果包含数学运算符，检查是否真的是表格
            # 表格中的数学运算符通常比较简单
            complex_math_patterns = [
                r'\\[a-zA-Z]+',  # LaTeX命令
                r'[αβγδεθλμπσφω]',  # 希腊字母
                r'[∫∑∏√∞∂∇]',      # 数学符号
                r'\\[a-zA-Z]+\s*\{[^}]*\}',  # LaTeX命令带参数
            ]
            
            has_complex_math = any(re.search(pattern, line) for pattern in complex_math_patterns)
            if has_complex_math:
                return False
        
        # 如果通过了所有检查，可能是表格
        return True
    
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
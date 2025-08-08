"""
Base metric interface for WebMainBench.
update_extract_from_content_list: 2025-08-08
"""

from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Union
import traceback
import re
import hashlib
from lxml import html as lxmlhtml
from lxml.html import HtmlElement, HTMLParser, fromstring, tostring

def normalize_math_delimiters(text: str) -> str:
    """将[tex][/tex]和[itex][/itex]格式的数学公式转换为$$..$$和$..$ 格式.

    这是兜底处理，针对公式被br标签分割后没有识别为公式的情况.
    处理两种情况:
    1. 行间公式: [tex]...[/tex] -> $$...$$
    2. 行内公式: [itex]...[/itex] -> $...$
    该方法保留公式内容的原始格式，包括换行符和空格。
    Args:
        text (str): 包含数学公式的文本
    Returns:
        str: 替换数学公式标记后的文本
    """
    import re

    # 替换行间公式 [tex]...[/tex] -> $$...$$
    # 使用非贪婪匹配和DOTALL标志以匹配跨行公式
    display_pattern = re.compile(r'\[tex\](.*?)\[/tex\]', re.DOTALL)
    text = display_pattern.sub(lambda m: f'$${m.group(1).strip()}$$', text)

    # 替换行内公式 [itex]...[/itex] -> $...$
    inline_pattern = re.compile(r'\[itex\](.*?)\[/itex\]', re.DOTALL)
    text = inline_pattern.sub(lambda m: f'${m.group(1).strip()}$', text)

    return text

def _escape_table_cell(text: str) -> str:
    """转义表格单元格中的特殊字符.

    比如 |、内容中的\n等
    """
    # 首先处理换行符，将其替换为空格
    text = re.sub(r'[\r\n]+', ' ', text)
    # 转义竖线和点号，避免与markdown表格语法冲突
    escaped = text.replace('|', '\\|')
    return escaped

def sha256_hash(data: str) -> str:
    """计算字符串的 SHA-256 哈希值."""
    # 创建 SHA-256 对象
    sha256 = hashlib.sha256()
    # 更新数据（需编码为字节）
    sha256.update(data.encode('utf-8'))
    # 返回十六进制哈希值
    return sha256.hexdigest()

def html_to_markdown_table(table_html_source: str) -> str:
    """把html代码片段转换成markdown表格.

    Args:
        table_html_source: 被<table>标签包裹的html代码片段(含<table>标签)

    Returns: 如果这个表格内没有任何文字性内容，则返回空字符串
    """
    # 解析HTML
    table_el = html_to_element(table_html_source)
    rows = table_el.xpath('.//tr')
    if not rows:
        return ''

    # 确定最大列数
    max_cols = 0
    for row in rows:
        cols = row.xpath('.//th | .//td')
        max_cols = max(max_cols, len(cols))

    if max_cols == 0:
        return ''
    markdown_table = []
    first_row = rows[0]
    # 检查第一行是否是表头并获取表头内容
    first_row_tags = first_row.xpath('.//th | .//td')
    if not first_row_tags:
        # 如果第一行没有td/th，则取整行内容作为表头
        headers = [_escape_table_cell(first_row.text_content().strip())]
    else:
        headers = [_escape_table_cell(tag.text_content().strip()) for tag in first_row_tags]
    # 如果表头存在，添加表头和分隔符，并保证表头与最大列数对齐
    if headers:
        while len(headers) < max_cols:
            headers.append('')  # 补充空白表头
        markdown_table.append('| ' + ' | '.join(headers) + ' |')
        markdown_table.append('|---' * max_cols + '|')
    else:
        # 如果没有明确的表头，创建默认表头
        default_headers = [''] * max_cols
        markdown_table.append('| ' + ' | '.join(default_headers) + ' |')
        markdown_table.append('|---' * max_cols + '|')

    # 添加表格内容，跳过已被用作表头的第一行（如果有的话）
    for row in rows[1:]:
        cells = row.xpath('.//td | .//th')
        if not cells:  # 无td/th时取整行内容，放到第一个单元格
            columns = [_escape_table_cell(row.text_content().strip())]
        else:
            columns = [_escape_table_cell(cell.text_content().strip()) for cell in cells]
        while len(columns) < max_cols:
            columns.append('')
        markdown_table.append('| ' + ' | '.join(columns) + ' |')

    md_str = '\n'.join(markdown_table)
    return md_str.strip()

def html_to_element(html:str) -> HtmlElement:
    """构建html树.

    Args:
        html: str: 完整的html源码

    Returns:
        element: lxml.html.HtmlElement: element
    """
    parser = HTMLParser(collect_ids=False, encoding='utf-8', remove_comments=True, remove_pis=True)
    # 将 HTML 字符串编码为字节类型, 兼容html中有 XML 声明（如 <?xml version="1.0" encoding="utf-8"?>）
    html_bytes = html.encode('utf-8')
    root = fromstring(html_bytes, parser=parser)
    standalone = deepcopy(root)  # 通过拷贝才能去掉自动加入的<html><body>等标签， 非常奇怪的表现。
    return standalone

def get_element_text(element: HtmlElement) -> str:
    """
    获取这个节点下，包括子节点的所有文本.
    Args:
        element:

    Returns:

    """
    text = ''.join(element.itertext())
    return text

def table_cells_count(table_html_source: str) -> int:
    """获取表格的单元格数量. 当只有1个单元格时，这个table就要被当做普通的一个段落处理。 只计算有实际内容的单元格数量。

    Args:
        table_html_source: str: 被<table>标签包裹的html代码片段(含<table>标签)

    Returns:
        int: 有内容的单元格数量
    """
    table_el = html_to_element(table_html_source)
    cell_count = 0

    # 获取所有行
    rows = table_el.xpath('.//tr')
    for row in rows:
        # 先检查是否有 td 或 th
        cells = row.xpath('.//td | .//th')
        if cells:
            # 如果有 td 或 th，计算有内容的单元格
            cell_count += sum(1 for cell in cells if cell.text_content().strip())
        else:
            # 如果没有 td 或 th，检查 tr 是否直接包含内容
            row_content = row.text_content().strip()
            if row_content:
                cell_count += 1

    return cell_count

class ListAttribute():
    """列表属性."""
    UNORDERED = 'unordered'
    ORDERED = 'ordered'
    DEFINITION = 'definition'


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
    
    @staticmethod
    def _content_lst_node_2_md(content_lst_node: dict, exclude_inline_types: list = [], use_raw_image_url=False) -> str:
        """把content_list里定义的每种元素块转化为markdown格式.

        Args:
            content_lst_node (dict): content_list里定义的每种元素块
        Returns:
            str: markdown格式
        """
        node_type = content_lst_node['type']
        if node_type == DocElementType.CODE:
            code = content_lst_node['content']['code_content']  # 这里禁止有None的content, 如果有应该消灭在模块内部。模块应该处理更精细，防止因为拼装导致掩盖了错误。
            # 代码不可以 strip，因为首行可能有缩进，只能 rstrip
            code = code.rstrip()
            if not code:
                return ''
            language = content_lst_node['content'].get('language', '')
            if content_lst_node.get('inline', False):
                code = f'`{code}`'
            else:
                code = f'```{language}\n{code}\n```'
            return code
        elif node_type == DocElementType.EQUATION_INTERLINE:
            math_content = content_lst_node['content']['math_content']
            math_content = math_content.strip()
            math_content = f'$$\n{math_content}\n$$'
            return math_content
        elif node_type == DocElementType.IMAGE:
            image_path = content_lst_node['content'].get('path', '')
            image_data = content_lst_node['content'].get('data', '')
            image_alt = content_lst_node['content'].get('alt', '')
            image_title = content_lst_node['content'].get('title', '')
            image_caption = content_lst_node['content'].get('caption', '')
            image_url = content_lst_node['content'].get('url', '')

            if not image_path and not image_data:
                image_path = sha256_hash(image_url)

            if use_raw_image_url:
                image_path = image_url

            if image_alt:
                image_alt = image_alt.strip()
            else:
                image_alt = ''

            if image_title:
                image_title = image_title.strip()
            else:
                image_title = ''

            if image_caption:
                image_caption = image_caption.strip()
            else:
                image_caption = ''

            image_des = image_title if image_title else image_caption if image_caption else ''
            # 优先使用data, 其次path.其中data是base64编码的图片，path是图片的url
            if image_data:
                if image_des:
                    image = f'![{image_alt}]({image_data} "{image_des}")'
                else:
                    image = f'![{image_alt}]({image_data})'
            else:
                if image_des:
                    image = f'![{image_alt}]({image_path} "{image_des}")'
                else:
                    image = f'![{image_alt}]({image_path})'
            return image
        elif node_type == DocElementType.AUDIO:
            return ''  # TODO: 音频格式
        elif node_type == DocElementType.VIDEO:
            return ''  # TODO: 视频格式
        elif node_type == DocElementType.TITLE:
            title_content = content_lst_node['content']['title_content'].strip()
            if not title_content:
                return ''
            level = content_lst_node['content']['level']
            # 确保level是整数
            try:
                level = int(level)
            except (ValueError, TypeError):
                level = 1
            md_title_level = '#' * level
            md_title = f'{md_title_level} {title_content}'
            return md_title
        elif node_type == DocElementType.PARAGRAPH:
            paragraph_el_lst = content_lst_node['content']
            one_para = BaseMetric._join_one_para(paragraph_el_lst, exclude_inline_types)
            return one_para
        elif node_type == DocElementType.LIST:
            list_content = content_lst_node['content']
            list_attribute = list_content.get('list_attribute', ListAttribute.UNORDERED)
            items = list_content.get('items', [])
            result = BaseMetric._process_nested_list(items, list_attribute, 0, exclude_inline_types)
            return '\n'.join(result)
        elif node_type == DocElementType.SIMPLE_TABLE:
            # 对文本格式来说，普通表格直接转为md表格，复杂表格返还原始html
            html_table = content_lst_node['content']['html']
            if html_table is not None:
                html_table = html_table.strip()
                cells_count = table_cells_count(html_table)
                if cells_count <= 1:  # 单个单元格的表格，直接返回文本
                    text = get_element_text(html_to_element(html_table)).strip()
                    return text
                md_table = html_to_markdown_table(html_table)
                return md_table
            else:
                return ''
        elif node_type == DocElementType.COMPLEX_TABLE:
            html_table = content_lst_node['content']['html']
            if html_table is not None:
                html_table = html_table.strip()
                return html_table
            else:
                return ''
        else:
            raise ValueError(f'content_lst_node contains invalid element type: {node_type}')  # TODO: 自定义异常

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

    @staticmethod
    def _extract_from_content_list(
        content_lst: List[List[Dict[str, Any]]],
        exclude_nodes=[],
        exclude_inline_types=[],
        use_raw_image_url=False
    ) -> Dict[str, str]:
        """
        直接从content_list数据结构中提取代码、公式、表格和文本部分。

        Args:
            content_lst (List[List[Dict[str, Any]]]): 结构化内容列表
            exclude_nodes (list): 需要排除的节点类型
            exclude_inline_types (list): 需要排除的行内类型
            use_raw_image_url (bool): 是否使用原始图片URL

        Returns:
            Dict[str, str]: 包含'code', 'formula', 'table', 'text', 'md'的字典
        """
        code_parts = []
        formula_parts = []
        table_parts = []
        text_parts = []
        md_blocks = []

        for page in content_lst:
            for content_lst_node in page:
                if content_lst_node['type'] in exclude_nodes:
                    continue
                
                node_type = content_lst_node['type']
                content = content_lst_node.get('content', {})
                

                # 处理代码块
                if node_type in ['code', 'code-block', 'codeblock', 'code_block']:
                    # 兼容所有可能的字段名
                    code_content = content.get('code_content', '') or content.get('content', '') or content.get('code', '')
                    language = content.get('language', '') or content.get('lang', '')
                    inline = content_lst_node.get('inline', False)
                    if code_content:
                        if inline:
                            # 行内代码
                            md_code_block = f"`{code_content}`"
                        else:
                            # 代码块
                            md_code_block = f"```{language}\n{code_content}\n```"
                        code_parts.append(code_content)
                        md_blocks.append(md_code_block)

                # 处理公式
                elif node_type in [
                    'equation-interline', 'equation', 'math', 'formula',
                    'equation_block', 'equation-block', 'equation_inline', 'equation-inline',
                    'math_block', 'math-block', 'math_inline', 'math-inline'
                ]:
                    # 兼容所有可能的字段名
                    math_content = (
                        content.get('math_content', '') or
                        content.get('content', '') or
                        content.get('formula', '') or
                        content.get('math', '')
                    )
                    if math_content:
                        # 构建markdown公式
                        md_formula = f"$${math_content}$$"
                        formula_parts.append(math_content)
                        md_blocks.append(md_formula)

                # 处理表格
                elif node_type in [
                    'simple_table', 'complex_table', 'table', 'html_table', 'table-block', 'table_block'
                ]:
                    # 兼容所有可能的字段名
                    html_content = (
                        content.get('html', '') or
                        content.get('content', '') or
                        content.get('table', '') or
                        content.get('table_content', '')
                    )
                    if html_content:
                        table_parts.append(html_content)
                        md_blocks.append(html_content)

                # 处理段落
                elif node_type in ['paragraph', 'para', 'textblock', 'text_block']:
                    paragraph_text = BaseMetric._extract_paragraph_content(
                        content, exclude_inline_types
                    )
                    if paragraph_text:
                        text_parts.append(paragraph_text)
                        md_blocks.append(paragraph_text)

                    # 从段落中提取代码内容、公式内容、表格内容
                    if isinstance(content, list):
                        for item in content:
                            t = item.get('t')
                            # 代码行内
                            if t in ['code-inline', 'code_inline', 'codeinline']:
                                code_content = item.get('c', '')
                                if code_content:
                                    code_parts.append(code_content)
                            # 公式行内
                            elif t in ['equation-inline', 'equation_inline', 'equation', 'math-inline', 'math_inline', 'math']:
                                formula_content = item.get('c', '')
                                if formula_content:
                                    formula_parts.append(formula_content)
                            # 表格行内
                            elif t in ['table-inline', 'table_inline', 'table']:
                                table_content = item.get('c', '')
                                if table_content:
                                    table_parts.append(table_content)
                
                # 处理标题
                elif node_type == 'title':
                    title_content = content.get('title_content', '')
                    level = content.get('level', 1)
                    # 确保level是整数
                    try:
                        level = int(level)
                    except (ValueError, TypeError):
                        level = 1
                    if title_content:
                        md_title = f"{'#' * level} {title_content}"
                        text_parts.append(md_title)  # 添加带#的标题到文本部分
                        md_blocks.append(md_title)
                
                # 处理列表
                elif node_type == 'list':
                    list_text = BaseMetric._extract_list_content(
                        content, exclude_inline_types
                    )
                    if list_text:
                        text_parts.append(list_text)
                        md_blocks.append(list_text)
                
                # 处理图片
                elif node_type == 'image':
                    # 图片信息不添加到文本部分，只添加到markdown中用于完整性
                    if not use_raw_image_url:
                        image_text = BaseMetric._extract_image_content(content)
                        if image_text:
                            md_blocks.append(image_text)
                
                # 处理其他多媒体内容
                elif node_type in ['audio', 'video']:
                    # 多媒体信息不添加到文本部分，只添加到markdown中用于完整性
                    media_text = BaseMetric._extract_media_content(content)
                    if media_text:
                        md_blocks.append(media_text)

        # 拼接markdown文本
        md = '\n\n'.join(md_blocks)
        md = normalize_math_delimiters(md)
        md = md.strip() + '\n'


        result = {
            'code': '\n'.join(code_parts).strip(),
            'formula': '\n'.join(formula_parts).strip(),
            'table': '\n\n'.join(table_parts).strip(),
            'text': '\n\n'.join([t for t in text_parts if t]).strip(),
            'md': md.strip()
        }
        
        return result

    @staticmethod
    def _extract_paragraph_content(content: List[Dict[str, Any]], exclude_inline_types: List[str]) -> str:
        """从段落内容中提取文本和行内元素"""
        if not isinstance(content, list):
            return ""
        
        text_parts = []
        for item in content:
            item_type = item.get('t', '')
            item_content = item.get('c', '')
            
            if item_type in exclude_inline_types:
                continue
            
            if item_type == 'text':
                text_parts.append(item_content)
            elif item_type == 'equation-inline':
                text_parts.append(f"${item_content}$")
            elif item_type == 'code-inline':
                text_parts.append(f"`{item_content}`")
            elif item_type == 'md':
                text_parts.append(item_content)
        
        return ''.join(text_parts)

    @staticmethod
    def _extract_list_content(content: Dict[str, Any], exclude_inline_types: List[str]) -> str:
        """从列表内容中提取文本"""
        items = content.get('items', [])
        ordered = content.get('ordered', False)
        
        list_texts = []
        for i, item in enumerate(items):
            if not isinstance(item, list):
                continue
            
            item_texts = []
            for paragraph in item:
                if isinstance(paragraph, list):
                    paragraph_text = BaseMetric._extract_paragraph_content(paragraph, exclude_inline_types)
                    if paragraph_text:
                        item_texts.append(paragraph_text)
            
            if item_texts:
                prefix = f"{i+1}. " if ordered else "- "
                list_texts.append(prefix + ' '.join(item_texts))
        
        return '\n'.join(list_texts)

    @staticmethod
    def _extract_image_content(content: Dict[str, Any]) -> str:
        """从图片内容中提取文本描述"""
        alt = content.get('alt', '')
        title = content.get('title', '')
        caption = content.get('caption', '')
        
        text_parts = []
        if alt:
            text_parts.append(f"图片: {alt}")
        if title and title != alt:
            text_parts.append(f"标题: {title}")
        if caption:
            text_parts.append(f"说明: {caption}")
        
        return ' '.join(text_parts) if text_parts else ""

    @staticmethod
    def _extract_media_content(content: Dict[str, Any]) -> str:
        """从音频/视频内容中提取文本描述"""
        title = content.get('title', '')
        caption = content.get('caption', '')
        
        text_parts = []
        if title:
            text_parts.append(f"媒体: {title}")
        if caption:
            text_parts.append(f"说明: {caption}")
        
        return ' '.join(text_parts) if text_parts else ""

    @staticmethod
    def _join_one_para(para: list, exclude_inline_types: list = []) -> str:
        """将段落元素列表连接成一个字符串"""
        if not isinstance(para, list):
            return ""
        
        text_parts = []
        for item in para:
            item_type = item.get('t', '')
            item_content = item.get('c', '')
            
            if item_type in exclude_inline_types:
                continue
            
            if item_type == 'text':
                text_parts.append(item_content)
            elif item_type == 'equation-inline':
                text_parts.append(f"${item_content}$")
            elif item_type == 'code-inline':
                text_parts.append(f"`{item_content}`")
            elif item_type == 'md':
                text_parts.append(item_content)
        
        return ''.join(text_parts)

    @staticmethod
    def _process_nested_list(items, list_attribute, indent_level=0, exclude_inline_types=[]):
        """处理嵌套列表"""
        result = []
        for i, item in enumerate(items):
            if not isinstance(item, list):
                continue
            
            item_texts = []
            for paragraph in item:
                if isinstance(paragraph, list):
                    paragraph_text = BaseMetric._join_one_para(paragraph, exclude_inline_types)
                    if paragraph_text:
                        item_texts.append(paragraph_text)
            
            if item_texts:
                if list_attribute == ListAttribute.ORDERED:
                    prefix = f"{i+1}. "
                else:
                    prefix = "- "
                
                indent = "  " * indent_level
                result.append(f"{indent}{prefix}{' '.join(item_texts)}")
        
        return result 
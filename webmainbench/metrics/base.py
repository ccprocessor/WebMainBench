"""
Base metric interface for WebMainBench.
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
        """从markdown文本中提取各种类型的内容"""
        if not text:
            return {'code': '', 'formula': '', 'table': '', 'text': ''}
        
        # 收集所有需要移除的内容片段
        extracted_segments = []
        
        # 提取代码
        code_parts = []
        # 代码块 ```code```
        for match in re.finditer(r'```[\s\S]*?```', text):
            code_block = match.group(0)
            extracted_segments.append(code_block)
            code_parts.append(code_block.strip('`').strip())
        
        # 行内代码 `code`
        for match in re.finditer(r'`([^`]+)`', text):
            inline_code_full = match.group(0)  # 包含反引号的完整匹配
            inline_code_content = match.group(1)  # 只是内容
            extracted_segments.append(inline_code_full)
            code_parts.append(inline_code_content)
        
        # 提取公式
        formula_parts = []
        # 统一的公式提取模式
        latex_patterns = [
            r'(?<!\\)\$\$([^$]+)\$\$(?!\\)',  # Display math (not escaped)
            r'(?<!\\)\$([^$\n]+)\$(?![\\\$])',  # Inline math (not escaped)
            # r'\\begin\{equation\*?\}(.*?)\\end\{equation\*?\}',  # Equation environment
            # r'\\begin\{align\*?\}(.*?)\\end\{align\*?\}',        # Align environment
            # r'\\begin\{gather\*?\}(.*?)\\end\{gather\*?\}',      # Gather environment
            # r'\\begin\{eqnarray\*?\}(.*?)\\end\{eqnarray\*?\}',  # Eqnarray environment
            # r'\\begin\{multline\*?\}(.*?)\\end\{multline\*?\}',  # Multline environment
            # r'\\begin\{split\}(.*?)\\end\{split\}',              # Split environment
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
        
        # 1. 提取HTML表格
        html_table_pattern = r'<table[^>]*>.*?</table>'
        for match in re.finditer(html_table_pattern, text, re.DOTALL | re.IGNORECASE):
            html_table = match.group(0)
            extracted_segments.append(html_table)
            table_parts.append(html_table)
        
        # 2. 提取Markdown表格
        lines = text.split('\n')
        table_lines = []
        in_markdown_table = False
        
        for line in lines:
            if '|' in line and line.strip():
                table_lines.append(line)
                in_markdown_table = True
            elif in_markdown_table and line.strip() == '':
                # Markdown表格结束（空行）
                if table_lines:
                    md_table = '\n'.join(table_lines)
                    extracted_segments.append(md_table)
                    table_parts.append(md_table)
                    table_lines = []
                in_markdown_table = False
            elif in_markdown_table:
                # 表格内的非表格行，Markdown表格结束
                if table_lines:
                    md_table = '\n'.join(table_lines)
                    extracted_segments.append(md_table)
                    table_parts.append(md_table)
                    table_lines = []
                in_markdown_table = False
        
        # 处理文档末尾的Markdown表格
        if table_lines:
            md_table = '\n'.join(table_lines)
            extracted_segments.append(md_table)
            table_parts.append(md_table)
        
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
            'text': clean_text,
            'md': text
        }
    
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
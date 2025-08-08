from abc import ABCMeta
import json
from typing import Dict, Any, List, Optional, Union, override

from webmainbench.metrics.base import DocElementType, ParagraphTextType

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

class ABC(metaclass=ABCMeta):
    """Helper class that provides a standard way to create an ABC using
    inheritance.
    """
    __slots__ = ()

class StructureMapper(ABC):
    """作用是把contentList结构组合转化为另外一个结构 例如，从contentList转化为html, txt, md等等.

    Args:
        object (_type_): _description_
    """
    def __init__(self):
        self.__txt_para_splitter = '\n'
        self.__md_para_splitter = '\n\n'
        self.__text_end = '\n'
        self.__list_item_start = '-'  # md里的列表项前缀
        self.__list_para_prefix = '  '  # 两个空格，md里的列表项非第一个段落的前缀：如果多个段落的情况，第二个以及之后的段落前缀
        self.__md_special_chars = ['#', '`', '$']  # TODO 拼装table的时候还应该转义掉|符号
        self.__nodes_document_type = [DocElementType.MM_NODE_LIST, DocElementType.PARAGRAPH, DocElementType.LIST, DocElementType.SIMPLE_TABLE, DocElementType.COMPLEX_TABLE, DocElementType.TITLE, DocElementType.IMAGE, DocElementType.AUDIO, DocElementType.VIDEO, DocElementType.CODE, DocElementType.EQUATION_INTERLINE]
        self.__inline_types_document_type = [ParagraphTextType.EQUATION_INLINE, ParagraphTextType.CODE_INLINE]

    def to_html(self):
        raise NotImplementedError('This method must be implemented by the subclass.')

    def to_txt(self, exclude_nodes=DocElementType.MM_NODE_LIST, exclude_inline_types=[]):
        """把content_list转化为txt格式.

        Args:
            exclude_nodes (list): 需要排除的节点类型
        Returns:
            str: txt格式的文本内容
        """
        text_blocks: list[str] = []  # 每个是个DocElementType规定的元素块之一转换成的文本
        content_lst = self._get_data()
        for page in content_lst:
            for content_lst_node in page:
                if content_lst_node['type'] not in exclude_nodes:
                    txt_content = self.__content_lst_node_2_txt(content_lst_node, exclude_inline_types)
                    if txt_content and len(txt_content) > 0:
                        text_blocks.append(txt_content)

        txt = self.__txt_para_splitter.join(text_blocks)
        txt = normalize_math_delimiters(txt)
        txt = txt.strip() + self.__text_end  # 加上结尾换行符
        return txt

class ContentList(StructureMapper):
    """content_list格式的工具链实现."""

    def __init__(self, json_data_lst: list):
        super().__init__()
        if json_data_lst is None:
            json_data_lst = []
        self.__content_list = json_data_lst

    def length(self) -> int:
        return len(self.__content_list)

    def append(self, content: dict):
        self.__content_list.append(content)

    def __getitem__(self, key):
        return self.__content_list[key]  # 提供读取功能

    def __setitem__(self, key, value):
        self.__content_list[key] = value  # 提供设置功能

    def __delitem__(self, key):
        del self.__content_list[key]

    @override
    def _get_data(self) -> List[Dict]:
        return self.__content_list

class Statics:
    """统计content_list中每个元素的type的数量."""
    def __init__(self, statics: dict = None):
        self.statics = statics if statics else {}
        self._validate(self.statics)

    def _validate(self, statics: dict):
        """校验statics的格式.需要是字典且只有一个为"statics"的key.示例:
            {
                "list": 1,
                "list.text": 2,
                "list.equation-inline": 1,
                "paragraph": 2,
                "paragraph.text": 2,
                "equation-interline": 2
            }
        """
        if not isinstance(statics, dict):
            raise ValueError('statics must be a dict')

    def __additem__(self, key, value):
        self.statics[key] = value

    def __getitem__(self, key):
        return self.statics[key]

    def __getall__(self):
        return self.statics

    def __clear__(self):
        self.statics = {}

    def print(self):
        print(json.dumps(self.statics, indent=4))

    def merge_statics(self, statics: dict) -> dict:
        """合并多个contentlist的统计结果.

        Args:
            statics: 每个contentlist的统计结果
        Returns:
            dict: 合并后的统计结果
        """
        for key, value in statics.items():
            if isinstance(value, (int, float)):
                self.statics[key] = self.statics.get(key, 0) + value

        return self.statics

    def get_statics(self, contentlist) -> dict:
        """
        统计contentlist中每个元素的type的数量（会清空之前的数据）
        Args:
            contentlist: 可以是ContentList对象或直接的列表数据
        Returns:
            dict: 每个元素的类型的数量
        """
        self.__clear__()
        return self._calculate_statics(contentlist)

    def add_statics(self, contentlist) -> dict:
        """
        统计contentlist中每个元素的type的数量（累计到现有数据）
        Args:
            contentlist: 可以是ContentList对象或直接的列表数据
        Returns:
            dict: 累计后的统计结果
        """
        return self._calculate_statics(contentlist)

    def _calculate_statics(self, contentlist) -> dict:
        """
        内部方法：计算contentlist的统计结果
        Args:
            contentlist: 可以是ContentList对象或直接的列表数据
        Returns:
            dict: 统计结果
        """
        def process_list_items(items, parent_type):
            """递归处理列表项
            Args:
                items: 列表项
                parent_type: 父元素类型（用于构建统计key）
            """
            if isinstance(items, list):
                for item in items:
                    process_list_items(item, parent_type)
            elif isinstance(items, dict) and 't' in items:
                # 到达最终的文本/公式元素
                item_type = f"{parent_type}.{items['t']}"
                current_count = self.statics.get(item_type, 0)
                self.statics[item_type] = current_count + 1

        # 处理不同类型的输入
        if hasattr(contentlist, '_get_data'):
            # 如果是ContentList对象
            data = contentlist._get_data()
        else:
            # 如果是直接的列表数据
            data = contentlist

        for page in data:  # page是每一页的内容列表
            for element in page:  # element是每个具体元素
                # 1. 统计基础元素
                element_type = element['type']
                current_count = self.statics.get(element_type, 0)
                self.statics[element_type] = current_count + 1

                # 2. 统计复合元素内部结构
                if element_type == DocElementType.PARAGRAPH:
                    # 段落内部文本类型统计
                    for item in element['content']:
                        item_type = f"{DocElementType.PARAGRAPH}.{item['t']}"
                        current_count = self.statics.get(item_type, 0)
                        self.statics[item_type] = current_count + 1

                elif element_type == DocElementType.LIST:
                    # 使用递归函数处理列表项
                    process_list_items(element['content']['items'], DocElementType.LIST)
                elif element_type == DocElementType.COMPLEX_TABLE:
                    # 统计复杂表格数量
                    if element.get('content', {}).get('is_complex', False):
                        item_type = f'{DocElementType.COMPLEX_TABLE}.complex'
                        current_count = self.statics.get(item_type, 0)
                        self.statics[item_type] = current_count + 1

        return self.statics


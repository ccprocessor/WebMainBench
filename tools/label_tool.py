'''
本脚本用于从jsonl文件读取表格数据，并在streamlit应用中展示和编辑。
命令行输入示例：
streamlit run /home/zhangshuo/Desktop/vscodeworkspace/WebMainBench/tools/label_tool.py -- WebMainBench/data/WebMainBench_test_0814_llm-webkit_filtered_table_results.jsonl
注意：-- 后面有个空格，否则会报错，然后再接数据文件路径

'''

import json
import os
import streamlit as st
import markdown

import sys

# 支持通过命令行参数传入数据文件路径
if len(sys.argv) > 1:
    DATA_FILE = sys.argv[1]
else:
    st.error("请通过命令行参数传入数据文件路径，例如：python read_table.py /path/to/data.jsonl")
    st.stop()

# 读取所有数据
@st.cache_data(show_spinner=False)
def load_data():
    data = []
    if not os.path.exists(DATA_FILE):
        return data
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data

# 只更新单条数据，避免全文件重写
def update_single_item(index, new_item):
    lines = []
    if not os.path.exists(DATA_FILE):
        return
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    if 0 <= index < len(lines):
        # 保证只替换对应行
        lines[index] = json.dumps(new_item, ensure_ascii=False) + "\n"
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            f.writelines(lines)

# Streamlit页面布局
st.set_page_config(layout="wide")
st.title("WebMainBench Table Editor")

data = load_data()
if not data:
    st.warning("未找到数据文件或文件为空。")
    st.stop()

# 选择要编辑的条目
index = st.sidebar.number_input("选择条目索引", min_value=0, max_value=len(data)-1, value=0, step=1)
item = data[index]

# 三列布局
col1, col2, col3 = st.columns([1.5, 1.5, 2])

with col1:
    st.subheader("HTML 渲染")
    # 尝试用st.components.v1.html增强HTML+CSS渲染能力
    try:
        st.components.v1.html(
            f'<div style="border:1px solid #ddd;padding:8px;overflow:auto;max-height:600px">{item.get("html","")}</div>',
            height=620,
            scrolling=True,
        )
    except Exception as e:
        st.markdown(
            f'<div style="border:1px solid #ddd;padding:8px;overflow:auto;max-height:600px">{item.get("html","")}</div>',
            unsafe_allow_html=True
        )
        st.info("st.components.v1.html不可用，已回退为st.markdown。")

with col2:
    st.subheader("Markdown 渲染")
    # 实时渲染 Markdown，优先显示编辑区内容
    # 使用 session_state 保持编辑内容
    if f"markdown_edit_{index}" not in st.session_state:
        st.session_state[f"markdown_edit_{index}"] = item.get("groundtruth_content", "")
    current_markdown = st.session_state[f"markdown_edit_{index}"]
    st.markdown(
        current_markdown,
        unsafe_allow_html=True
    )

with col3:
    st.subheader("Markdown 源代码（可编辑）")
    # 实时更新 session_state
    new_markdown = st.text_area(
        "编辑 Markdown",
        value=st.session_state.get(f"markdown_edit_{index}", item.get("groundtruth_content", "")),
        height=600,
        key=f"markdown_edit_{index}"
    )
    # 提交按钮只用于保存到文件
    if st.button("提交更改", key=f"submit_{index}"):
        if new_markdown != item.get("groundtruth_content", ""):
            # 只更新当前条目，避免全文件重写和数据覆盖
            data[index]["groundtruth_content"] = new_markdown
            update_single_item(index, data[index])
            load_data.clear()  # 清理缓存，确保下次读取到最新数据
            st.success("更改已保存！")
        else:
            st.info("内容未更改，无需保存。")

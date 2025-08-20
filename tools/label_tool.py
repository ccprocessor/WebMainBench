'''
This script is used to read the table data from the jsonl file and display it in a streamlit app.

命令行输入：
streamlit run WebMainBench/webmainbench/utils/Data_Modification_Tools.py -- WebMainBench/data/WebMainBench_test_0814_llm-webkit_filtered_table_results.jsonl
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

# 保存所有数据
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        for item in data:
            print(item)
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

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
    st.markdown(
        f'<div style="border:1px solid #ddd;padding:8px;overflow:auto;max-height:600px">{item.get("html","")}</div>',
        unsafe_allow_html=True
    )

with col2:
    st.subheader("Markdown 渲染")
    st.markdown(
        item.get("groundtruth_content", ""),
        unsafe_allow_html=True
    )

with col3:
    st.subheader("Markdown 源代码（可编辑）")
    new_markdown = st.text_area(
        "编辑 Markdown",
        value=item.get("groundtruth_content", ""),
        height=600,
        key=f"markdown_edit_{index}"
    )
    if st.button("提交更改", key=f"submit_{index}"):
        if new_markdown != item.get("groundtruth_content", ""):
            data[index]["groundtruth_content"] = new_markdown
            save_data(data)
            st.success("更改已保存！")
        else:
            st.info("内容未更改，无需保存。")

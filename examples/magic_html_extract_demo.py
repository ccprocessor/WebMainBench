from magic_html import GeneralExtractor

# 初始化提取器
extractor = GeneralExtractor()

url = "http://example.com/"
html_content = """

<html>
    <body>
        <h1 cc-select="true">Python编程教程</h1>
        <p cc-select="true">这是一个Python基础教程，展示如何定义函数。</p>
        <pre cc-select="true"><code>def greet(name):
    ""问候函数""
    return f"Hello, {name}!"

# 使用示例
result = greet("World")
print(result)</code></pre>
        <p cc-select="true">这个函数可以用来问候任何人。</p>
    </body>
</html>
"""

data = extractor.extract(html_content, base_url=url)
# 从输出中提取所需信息
extracted_html = data.get('html', '')
title = data.get('title', '')
base_url = data.get('base_url', url)

# 将提取的 HTML 作为内容
content = extracted_html
print(content)
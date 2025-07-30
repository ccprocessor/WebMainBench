from resiliparse.extract.html2text import extract_plain_text

html_content ="""

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

print(extract_plain_text(html_content))

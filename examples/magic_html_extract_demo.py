import time
from webmainbench.extractors import ExtractorFactory

# 配置 MagicHTML 抽取器（这里可根据需要添加更多配置）
config = {}
try:
    # 创建 MagicHTML 抽取器实例
    extractor = ExtractorFactory.create("magic-html", config=config)
    print(f"✅ Extractor创建成功: {extractor.description}")
    print(f"📋 版本: {extractor.version}")
    print(f"⚙️ 配置: {extractor.get_config()}\n")
except Exception as e:
    print(f"❌ Extractor创建失败: {e}")

# 测试 HTML
test_html = """
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

print("🔍 开始内容提取...")
start_time = time.time()

try:
    result = extractor.extract(test_html)
    end_time = time.time()

    print(f"⏱️ 提取耗时: {end_time - start_time:.2f}秒\n")

    # 显示提取结果
    if result.success:
        print("✅ 内容提取成功！\n")

        print("📄 提取的主要内容:")
        print("=" * 50)
        print(result.content[:500] + "..." if len(result.content) > 500 else result.content)
        print("=" * 50)

        print(f"\n📊 提取统计:")
        print(f"  • 内容长度: {len(result.content)} 字符")
        print(f"  • 标题: {result.title}")
        print(f"  • 语言: {result.language}")
        print(f"  • 提取时间: {result.extraction_time:.3f}秒")

        if result.content_list:
            print(f"  • 结构化内容块: {len(result.content_list)}个")
            for i, item in enumerate(result.content_list[:3]):  # 显示前3个
                print(f"    [{i + 1}] {item.get('type', 'unknown')}: {item.get('content', '')[:50]}...")
    else:
        print("❌ 内容提取失败")
        print(f"错误信息: {result.error_message}")
        if result.error_traceback:
            print(f"错误详情:\n{result.error_traceback}")

except Exception as e:
    print(f"❌ 提取过程中发生异常: {e}")
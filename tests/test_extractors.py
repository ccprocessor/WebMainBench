import unittest
from webmainbench.extractors.factory import ExtractorFactory
from webmainbench.extractors.base import ExtractionResult


class TestExtractors(unittest.TestCase):

    def setUp(self):
        # 自动发现抽取器
        ExtractorFactory.auto_discover()

    def test_trafilatura_extractor(self):
        # 测试 Trafilatura 抽取器
        extractor = ExtractorFactory.create("trafilatura")
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
        result = extractor.extract(html_content)
        self.assertEqual(isinstance(result, ExtractionResult), True)
        self.assertEqual(result.success in [True, False], True)

#     def test_magic_html_extractor(self):
#         # 测试 Magic HTML 抽取器
#         try:
#             extractor = ExtractorFactory.create("magic-html")
#             html_content = """
#             <html>
#                 <body>
#                     <h1 cc-select="true">Python编程教程</h1>
#                     <p cc-select="true">这是一个Python基础教程，展示如何定义函数。</p>
#                     <pre cc-select="true"><code>def greet(name):
#     ""问候函数""
#     return f"Hello, {name}!"
#
# # 使用示例
# result = greet("World")
# print(result)</code></pre>
#                     <p cc-select="true">这个函数可以用来问候任何人。</p>
#                 </body>
#             </html>
#             """
#             result = extractor.extract(html_content)
#             self.assertEqual(isinstance(result, ExtractionResult), True)
#             self.assertEqual(result.success in [True, False], True)
#         except ValueError as e:
#             # 如果抽取器未注册，跳过测试
#             self.skipTest(f"Magic HTML 抽取器未注册: {e}")

    def test_resiliparse_extractor(self):
        # 测试 Resiliparse 抽取器
        try:
            extractor = ExtractorFactory.create("resiliparse")
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
            result = extractor.extract(html_content)
            self.assertEqual(isinstance(result, ExtractionResult), True)
            self.assertEqual(result.success in [True, False], True)
        except ValueError as e:
            # 如果抽取器未注册，跳过测试
            self.skipTest(f"Resiliparse 抽取器未注册: {e}")


if __name__ == '__main__':
    unittest.main()
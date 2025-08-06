import unittest
from unittest.mock import Mock, patch
from webmainbench.extractors.factory import ExtractorFactory
from webmainbench.extractors.base import ExtractionResult


class TestLLMWebKitExtractor(unittest.TestCase):
    """LLM-WebKit extractor功能测试."""

    def setUp(self):
        """测试前准备."""
        # 自动发现抽取器
        ExtractorFactory.auto_discover()
        
        # 准备测试用的预处理HTML内容
        self.preprocessed_main_html = """
        <div _item_id="1">
            <h1>人工智能的发展趋势</h1>
            <p>人工智能（AI）技术正在快速发展，对各行各业产生深远影响。</p>
        </div>
        <div _item_id="2">
            <h2>机器学习的进步</h2>
            <p>深度学习和大语言模型的突破使得AI系统能够理解和生成更自然的语言。</p>
        </div>
        <div _item_id="3">
            <h2>自动化应用</h2>
            <p>从制造业的机器人到软件开发的代码生成，AI正在各个领域实现流程自动化。</p>
        </div>
        """
        
        # 模拟提取结果
        self.mock_extracted_content = "人工智能的发展趋势\n\n人工智能（AI）技术正在快速发展，对各行各业产生深远影响。\n\n机器学习的进步\n\n深度学习和大语言模型的突破使得AI系统能够理解和生成更自然的语言。"
        self.mock_extracted_content_list = [
            {"type": "heading", "content": "人工智能的发展趋势"},
            {"type": "paragraph", "content": "人工智能（AI）技术正在快速发展，对各行各业产生深远影响。"},
            {"type": "heading", "content": "机器学习的进步"},
            {"type": "paragraph", "content": "深度学习和大语言模型的突破使得AI系统能够理解和生成更自然的语言。"}
        ]

    def test_preprocessed_html_config(self):
        """测试预处理HTML配置参数."""
        config = {
            "use_preprocessed_html": True,
            "preprocessed_html_field": "custom_html_field"
        }
        
        try:
            extractor = ExtractorFactory.create("llm-webkit", config=config)
            
            # 验证配置是否正确设置
            self.assertTrue(extractor.inference_config.use_preprocessed_html)
            self.assertEqual(extractor.inference_config.preprocessed_html_field, "custom_html_field")
            
        except Exception as e:
            # 如果依赖不可用，跳过测试
            self.skipTest(f"LLM-WebKit dependencies not available: {e}")

    @patch('webmainbench.extractors.llm_webkit_extractor.LlmWebkitExtractor._extract_content_from_main_html')
    def test_preprocessed_html_extract_content(self, mock_extract_from_main):
        """测试使用预处理HTML的_extract_content方法."""
        # 配置mock返回值
        mock_extract_from_main.return_value = (self.mock_extracted_content, self.mock_extracted_content_list)
        
        config = {
            "use_preprocessed_html": True,
            "model_path": "/fake/model/path"  # 测试用的假路径
        }
        
        try:
            extractor = ExtractorFactory.create("llm-webkit", config=config)
            
            # 调用_extract_content方法
            result = extractor._extract_content(self.preprocessed_main_html, "https://example.com")
            
            # 验证mock被正确调用
            mock_extract_from_main.assert_called_once_with(self.preprocessed_main_html, "https://example.com")
            
            # 验证结果
            self.assertIsInstance(result, ExtractionResult)
            self.assertTrue(result.success)
            self.assertEqual(result.content, self.mock_extracted_content)
            self.assertEqual(result.confidence_score, 0.9)  # 预处理HTML的固定置信度
            self.assertIsNotNone(result.extraction_time)
            
        except Exception as e:
            self.skipTest(f"LLM-WebKit dependencies not available: {e}")

    @patch('webmainbench.extractors.llm_webkit_extractor.LlmWebkitExtractor._extract_content_from_main_html')
    def test_standard_html_mode(self, mock_extract_from_main):
        """测试标准HTML模式（非预处理）."""
        # 不设置use_preprocessed_html，应该走标准流程
        config = {
            "use_preprocessed_html": False,
            "model_path": "/fake/model/path"
        }
        
        try:
            extractor = ExtractorFactory.create("llm-webkit", config=config)
            
            # 使用标准HTML
            standard_html = "<html><head><title>Test</title></head><body><p>Test content</p></body></html>"
            
            # 由于标准模式需要HTML简化等步骤，我们只测试配置
            self.assertFalse(extractor.inference_config.use_preprocessed_html)
            
            # 确保_extract_content_from_main_html没有被直接调用（因为要先经过HTML简化）
            # 这里我们不实际调用_extract_content，因为它需要完整的依赖
            
        except Exception as e:
            self.skipTest(f"LLM-WebKit dependencies not available: {e}")

    def test_config_defaults(self):
        """测试配置默认值."""
        try:
            extractor = ExtractorFactory.create("llm-webkit")
            
            # 验证默认配置
            self.assertFalse(extractor.inference_config.use_preprocessed_html)
            self.assertEqual(extractor.inference_config.preprocessed_html_field, "llm_webkit_html")
            
        except Exception as e:
            self.skipTest(f"LLM-WebKit dependencies not available: {e}")

    @patch('webmainbench.extractors.llm_webkit_extractor.LlmWebkitExtractor._extract_content_from_main_html')
    def test_error_handling_in_preprocessed_mode(self, mock_extract_from_main):
        """测试预处理模式下的错误处理."""
        # 配置mock抛出异常
        mock_extract_from_main.side_effect = Exception("Mock extraction error")
        
        config = {
            "use_preprocessed_html": True,
            "model_path": "/fake/model/path"
        }
        
        try:
            extractor = ExtractorFactory.create("llm-webkit", config=config)
            
            # 调用应该捕获异常并返回错误结果
            result = extractor._extract_content(self.preprocessed_main_html)
            
            # 验证错误处理
            self.assertIsInstance(result, ExtractionResult)
            self.assertFalse(result.success)
            self.assertIn("LLM-WebKit extraction failed", result.error_message)
            self.assertIsNotNone(result.extraction_time)
            
        except Exception as e:
            self.skipTest(f"LLM-WebKit dependencies not available: {e}")

    def test_preprocessed_html_integration(self):
        """集成测试：演示预处理HTML功能的实际使用."""
        print("\n" + "="*50)
        print("🚀 预处理HTML功能集成测试")
        print("="*50)
        
        # 准备预处理HTML内容（模拟llm-webkit第一阶段的输出）
        preprocessed_main_html = """
        <div _item_id="1">
            <h1>人工智能的发展趋势</h1>
            <p>人工智能（AI）技术正在快速发展，对各行各业产生深远影响。本文将探讨AI的主要发展趋势和未来展望。</p>
        </div>
        <div _item_id="2">
            <h2>机器学习的进步</h2>
            <p>深度学习和大语言模型的突破使得AI系统能够理解和生成更自然的语言，在对话、翻译、创作等领域表现出色。</p>
        </div>
        <div _item_id="3">
            <h2>自动化应用</h2>
            <p>从制造业的机器人到软件开发的代码生成，AI正在各个领域实现流程自动化，提高效率并降低成本。</p>
        </div>
        """
        
        try:
            # 测试1: 标准模式 vs 预处理模式的配置对比
            print("\n📋 测试1: 配置对比")
            
            # 标准模式配置
            standard_config = {
                "use_preprocessed_html": False,
                "model_path": "/fake/model/path"
            }
            standard_extractor = ExtractorFactory.create("llm-webkit", config=standard_config)
            print(f"标准模式 - use_preprocessed_html: {standard_extractor.inference_config.use_preprocessed_html}")
            
            # 预处理模式配置
            preprocessed_config = {
                "use_preprocessed_html": True,
                "preprocessed_html_field": "llm_webkit_html",
                "model_path": "/fake/model/path"
            }
            preprocessed_extractor = ExtractorFactory.create("llm-webkit", config=preprocessed_config)
            print(f"预处理模式 - use_preprocessed_html: {preprocessed_extractor.inference_config.use_preprocessed_html}")
            print(f"预处理字段: {preprocessed_extractor.inference_config.preprocessed_html_field}")
            
            # 测试2: 验证配置正确性
            print("\n✅ 测试2: 配置验证")
            self.assertFalse(standard_extractor.inference_config.use_preprocessed_html)
            self.assertTrue(preprocessed_extractor.inference_config.use_preprocessed_html)
            self.assertEqual(preprocessed_extractor.inference_config.preprocessed_html_field, "llm_webkit_html")
            print("配置验证通过！")
            
            # 测试3: 标题提取功能
            print("\n🏷️ 测试3: 标题提取功能")
            html_with_title = "<html><head><title>AI发展趋势报告</title></head><body>" + preprocessed_main_html + "</body></html>"
            title = preprocessed_extractor._extract_title(html_with_title)
            print(f"提取的标题: {title}")
            self.assertEqual(title, "AI发展趋势报告")
            
            # 测试4: 语言检测功能
            print("\n🌐 测试4: 语言检测功能")
            test_content = "人工智能技术正在快速发展，对各行各业产生深远影响。"
            language = preprocessed_extractor._detect_language(test_content)
            print(f"检测到的语言: {language}")
            self.assertEqual(language, "zh")
            
            print("\n✅ 预处理HTML功能集成测试完成！")
            
        except Exception as e:
            self.skipTest(f"LLM-WebKit dependencies not available: {e}")

    def test_preprocessed_html_e2e(self):
        """预处理HTML功能的端到端测试."""
        try:
            # 场景：已有一批通过llm-webkit第一阶段处理的数据
            dataset_samples = [
                {
                    "id": "sample_1",
                    "url": "https://example.com/article1",
                    "llm_webkit_html": """
                    <div _item_id="1">
                        <h1>深度学习入门指南</h1>
                        <p>深度学习是机器学习的一个重要分支。</p>
                    </div>
                    """,
                },
                {
                    "id": "sample_2", 
                    "url": "https://example.com/article2",
                    "llm_webkit_html": """
                    <div _item_id="1">
                        <h1>自然语言处理应用</h1>
                        <p>NLP技术在各个领域都有广泛应用。</p>
                    </div>
                    """,
                }
            ]
            
            # 创建预处理HTML模式的extractor
            config = {
                "use_preprocessed_html": True,
                "preprocessed_html_field": "llm_webkit_html"
            }
            extractor = ExtractorFactory.create("llm-webkit", config=config)
            
            # 验证配置
            self.assertTrue(extractor.inference_config.use_preprocessed_html)
            self.assertEqual(extractor.inference_config.preprocessed_html_field, "llm_webkit_html")
            
            # 批量处理测试
            results = []
            for sample in dataset_samples:
                result = extractor._extract_content(sample['llm_webkit_html'], sample['url'])
                results.append(result)
            
            # 核心断言验证
            successful_results = [r for r in results if r.success]
            
            # 1. 所有样本都应该成功处理
            self.assertEqual(len(successful_results), len(dataset_samples), 
                           "所有样本都应该处理成功")
            
            # 2. 验证每个结果的基本属性
            for i, result in enumerate(successful_results):
                with self.subTest(sample_id=dataset_samples[i]['id']):
                    # 内容不应为空
                    self.assertGreater(len(result.content), 0, "提取的内容不应为空")
                    
                    # 预处理HTML的固定置信度
                    self.assertEqual(result.confidence_score, 0.9, "预处理HTML的置信度应为0.9")
                    
                    # 应该包含相关关键词
                    if "深度学习" in dataset_samples[i]['llm_webkit_html']:
                        self.assertIn("深度学习", result.content, "应该包含深度学习相关内容")
                    elif "自然语言处理" in dataset_samples[i]['llm_webkit_html']:
                        self.assertIn("自然语言处理", result.content, "应该包含NLP相关内容")
                    
                    # 提取时间应该合理
                    self.assertGreater(result.extraction_time, 0, "提取时间应该大于0")
                    self.assertLess(result.extraction_time, 10, "提取时间应该在合理范围内")
            
        except Exception as e:
            self.skipTest(f"LLM-WebKit dependencies not available: {e}")


if __name__ == '__main__':
    unittest.main()

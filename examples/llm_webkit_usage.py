#!/usr/bin/env python3
"""
LLM-WebKit Extractor使用示例

本示例展示如何使用集成了VLLM推理能力的LLM-WebKit extractor。
"""

import time
from webmainbench.extractors import ExtractorFactory


def main():
    print("🚀 LLM-WebKit Extractor 使用示例\n")
    
    # 1. 创建带有自定义配置的extractor
    config = {
        "model_path": "/Users/chupei/model/checkpoint-3296",  # 替换为您的模型路径
        "use_logits_processor": True,  # 启用JSON格式约束
        "temperature": 0.0,  # 确定性输出
        "max_item_count": 500,  # 处理的最大item数量
        "max_output_tokens": 4096,  # 最大输出token数
        "dtype": "bfloat16",  # 模型精度
        "tensor_parallel_size": 1  # 张量并行大小
    }
    
    try:
        extractor = ExtractorFactory.create("llm-webkit", config=config)
        print(f"✅ Extractor创建成功: {extractor.description}")
        print(f"📋 版本: {extractor.version}")
        print(f"⚙️ 配置: {extractor.inference_config.__dict__}\n")
        
    except Exception as e:
        print(f"❌ Extractor创建失败: {e}")
        print("💡 请确保已安装所需依赖：")
        print("   pip install vllm transformers torch llm_web_kit")
        return
    
    # 2. 准备测试HTML（包含_item_id属性的结构化HTML）
    test_html = """
    <html>
    <head>
        <title>测试文章 - 人工智能的发展趋势</title>
    </head>
    <body>
        <nav _item_id="1">
            <ul>
                <li><a href="/">首页</a></li>
                <li><a href="/news">新闻</a></li>
                <li><a href="/tech">科技</a></li>
            </ul>
        </nav>
        
        <header _item_id="2">
            <h1>人工智能的发展趋势</h1>
            <p class="meta">作者：张三 | 发布时间：2024-01-15 | 阅读量：1,234</p>
        </header>
        
        <main _item_id="3">
            <article>
                <p>人工智能（AI）技术正在快速发展，对各行各业产生深远影响。本文将探讨AI的主要发展趋势和未来展望。</p>
                
                <h2>1. 机器学习的进步</h2>
                <p>深度学习和大语言模型的突破使得AI系统能够理解和生成更自然的语言，在对话、翻译、创作等领域表现出色。</p>
                
                <h2>2. 自动化应用</h2>
                <p>从制造业的机器人到软件开发的代码生成，AI正在各个领域实现流程自动化，提高效率并降低成本。</p>
                
                <h2>3. 个性化服务</h2>
                <p>基于用户数据的个性化推荐和服务正变得越来越精准，为用户提供更好的体验。</p>
            </article>
        </main>
        
        <aside _item_id="4">
            <h3>相关文章</h3>
            <ul>
                <li><a href="/article1">机器学习基础入门</a></li>
                <li><a href="/article2">深度学习应用案例</a></li>
                <li><a href="/article3">AI伦理与安全</a></li>
            </ul>
        </aside>
        
        <footer _item_id="5">
            <p>&copy; 2024 科技资讯网. 保留所有权利.</p>
            <div class="social-links">
                <a href="#">微博</a> | <a href="#">微信</a> | <a href="#">知乎</a>
            </div>
        </footer>
    </body>
    </html>
    """
    
    # 3. 执行内容提取
    print("🔍 开始内容提取...")
    start_time = time.time()
    
    try:
        result = extractor.extract(test_html)
        end_time = time.time()
        
        print(f"⏱️ 提取耗时: {end_time - start_time:.2f}秒\n")
        
        # 4. 显示提取结果
        if result.success:
            print("✅ 内容提取成功！\n")
            
            print("📄 提取的主要内容:")
            print("=" * 50)
            print(result.content[:500] + "..." if len(result.content) > 500 else result.content)
            print("=" * 50)
            
            print(f"\n📊 提取统计:")
            print(f"  • 内容长度: {len(result.content)} 字符")
            print(f"  • 置信度: {result.confidence_score:.3f}")
            print(f"  • 标题: {result.title}")
            print(f"  • 语言: {result.language}")
            print(f"  • 提取时间: {result.extraction_time:.3f}秒")
            
            if result.content_list:
                print(f"  • 结构化内容块: {len(result.content_list)}个")
                for i, item in enumerate(result.content_list[:3]):  # 显示前3个
                    print(f"    [{i+1}] {item.get('type', 'unknown')}: {item.get('content', '')[:50]}...")
        
        else:
            print("❌ 内容提取失败")
            print(f"错误信息: {result.error_message}")
            if result.error_traceback:
                print(f"错误详情:\n{result.error_traceback}")
    
    except Exception as e:
        print(f"❌ 提取过程中发生异常: {e}")
    
    print("\n🎯 高级功能说明:")
    print("• 智能分类: 使用LLM理解HTML元素语义，准确区分主要内容和辅助内容")
    print("• 格式约束: 通过logits processor确保LLM输出有效的JSON格式")
    print("• 性能优化: 自动跳过过于复杂的HTML，支持延迟加载模型")
    print("• 详细反馈: 提供分类结果、置信度和性能指标")


if __name__ == "__main__":
    main()
    
    print("\n💡 使用提示:")
    print("1. 确保已安装所需依赖: vllm, transformers, torch, llm_web_kit")
    print("2. 设置正确的模型路径")
    print("3. 根据硬件资源调整tensor_parallel_size和dtype")
    print("4. 对于大规模HTML，适当调整max_item_count限制")
    print("5. 使用use_logits_processor=True确保输出格式可靠性") 
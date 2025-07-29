#!/usr/bin/env python3
"""
WebMainBench TEDS 算法使用示例

展示如何在评估中使用 TEDS (Tree-Edit Distance based Similarity) 算法进行表格评估
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from webmainbench import (
    DataLoader, Evaluator, EvaluationResult,
    TEDSMetric, StructureTEDSMetric
)
from webmainbench.extractors import LLMWebkitExtractor
from webmainbench.data import DataSample, ExtractionResult


def demo_teds_configuration():
    """演示如何配置 TEDS 算法"""
    print("=== 🔧 TEDS 配置示例 ===\n")
    
    # 方法1: 使用 TableTEDSMetric 指标
    print("**方法1: 使用专用的 TableTEDSMetric 指标**")
    evaluation_config = {
        "metrics": {
            "table_extraction": {
                "use_teds": True,  # 启用 TEDS 算法
                "structure_only": False  # 同时考虑结构和内容
            }
        }
    }
    print("配置:", evaluation_config)
    print()
    
    # 方法2: 直接使用 TEDS 指标
    print("**方法2: 直接使用独立的 TEDS 指标**")
    teds_config = {
        "metrics": {
            "teds": {
                "structure_only": False,
                "ignore_nodes": ["tbody", "thead", "tfoot"]
            },
            "s_teds": {  # 结构化 TEDS
                "structure_only": True
            }
        }
    }
    print("配置:", teds_config)
    print()


def demo_teds_comparison():
    """演示 TEDS 与简单算法的对比"""
    print("=== ⚖️ TEDS vs 简单算法对比 ===\n")
    
    # 准备测试数据
    test_cases = [
        {
            "name": "完全匹配的表格",
            "extracted": """
            <table>
                <tr><th>产品</th><th>价格</th></tr>
                <tr><td>苹果</td><td>5元</td></tr>
                <tr><td>橙子</td><td>3元</td></tr>
            </table>
            """,
            "groundtruth": """
            <table>
                <tr><th>产品</th><th>价格</th></tr>
                <tr><td>苹果</td><td>5元</td></tr>
                <tr><td>橙子</td><td>3元</td></tr>
            </table>
            """
        },
        {
            "name": "缺少行的表格",
            "extracted": """
            <table>
                <tr><th>产品</th><th>价格</th></tr>
                <tr><td>苹果</td><td>5元</td></tr>
            </table>
            """,
            "groundtruth": """
            <table>
                <tr><th>产品</th><th>价格</th></tr>
                <tr><td>苹果</td><td>5元</td></tr>
                <tr><td>橙子</td><td>3元</td></tr>
                <tr><td>香蕉</td><td>4元</td></tr>
            </table>
            """
        },
        {
            "name": "结构不同的表格",
            "extracted": """
            <table>
                <tr><th>产品</th><th>价格</th></tr>
                <tr><td>苹果</td><td>5元</td></tr>
            </table>
            """,
            "groundtruth": """
            <table>
                <tr><th>产品</th><th>价格</th><th>库存</th></tr>
                <tr><td>苹果</td><td>5元</td><td>100</td></tr>
            </table>
            """
        }
    ]
    
    print("| 测试用例 | 简单算法 | TEDS算法 | S-TEDS | 差异 |")
    print("|---------|---------|---------|--------|------|")
    
    for case in test_cases:
        # 简单算法评估
        simple_evaluator = Evaluator(task_config={
            "metrics": {
                "table_extraction": {"use_teds": False}
            }
        })
        
        # TEDS 算法评估
        teds_evaluator = Evaluator(task_config={
            "metrics": {
                "table_extraction": {"use_teds": True}
            }
        })
        
        # 创建模拟数据
        sample = DataSample(
            id=f"test_{case['name']}",
            html="<div>测试HTML</div>",
            content="测试内容",
            content_list=[{"table": case["groundtruth"]}]
        )
        
        extraction_result = ExtractionResult(
            extractor_name="test",
            extracted_content="测试内容",
            extracted_content_list=[{"table": case["extracted"]}]
        )
        
        # 计算得分
        try:
            simple_result = simple_evaluator.evaluate_single(sample, extraction_result)
            teds_result = teds_evaluator.evaluate_single(sample, extraction_result)
            
            simple_score = simple_result.overall_metrics.get("table_extraction", 0.0)
            teds_score = teds_result.overall_metrics.get("table_extraction", 0.0)
            
            # S-TEDS (结构化) 评估
            s_teds = StructureTEDSMetric("s_teds")
            s_teds_result = s_teds.calculate(case["extracted"], case["groundtruth"])
            s_teds_score = s_teds_result.score
            
            diff = abs(simple_score - teds_score)
            
            print(f"| {case['name'][:10]}... | {simple_score:.4f} | {teds_score:.4f} | {s_teds_score:.4f} | {diff:.4f} |")
            
        except Exception as e:
            print(f"| {case['name'][:10]}... | 错误 | 错误 | 错误 | - |")
            print(f"  错误信息: {e}")
    
    print()


def demo_advanced_teds_features():
    """演示 TEDS 的高级功能"""
    print("=== 🚀 TEDS 高级功能演示 ===\n")
    
    # 1. 处理 Markdown 表格
    print("**1. Markdown 表格支持**")
    teds = TEDSMetric("teds")
    
    markdown_table = """
    | 姓名 | 年龄 | 职业 |
    |------|------|------|
    | 张三 | 25   | 工程师 |
    | 李四 | 30   | 设计师 |
    """
    
    html_table = """
    <table>
        <tr><th>姓名</th><th>年龄</th><th>职业</th></tr>
        <tr><td>张三</td><td>25</td><td>工程师</td></tr>
        <tr><td>李四</td><td>30</td><td>设计师</td></tr>
    </table>
    """
    
    result = teds.calculate(markdown_table, html_table)
    print(f"Markdown vs HTML 表格 TEDS 得分: {result.score:.4f}")
    print(f"详细信息: {result.details}")
    print()
    
    # 2. 复杂表格结构
    print("**2. 复杂表格结构支持 (colspan, rowspan)**")
    complex_table1 = """
    <table>
        <tr><th colspan="2">学生信息</th></tr>
        <tr><th>姓名</th><th>成绩</th></tr>
        <tr><td>张三</td><td>95</td></tr>
        <tr><td>李四</td><td>87</td></tr>
    </table>
    """
    
    complex_table2 = """
    <table>
        <tr><th>类别</th><th>详情</th></tr>
        <tr><th>姓名</th><th>成绩</th></tr>
        <tr><td>张三</td><td>95</td></tr>
        <tr><td>李四</td><td>87</td></tr>
    </table>
    """
    
    result = teds.calculate(complex_table1, complex_table2)
    print(f"复杂表格结构 TEDS 得分: {result.score:.4f}")
    print(f"编辑距离: {result.details.get('edit_distance')}")
    print(f"节点数量: 预测={result.details.get('predicted_nodes')}, 真实={result.details.get('groundtruth_nodes')}")
    print()
    
    # 3. 结构化 vs 内容敏感评估
    print("**3. 结构化 vs 内容敏感评估对比**")
    content_teds = TEDSMetric("content_teds", {"structure_only": False})
    structure_teds = StructureTEDSMetric("structure_teds")
    
    table_diff_content = """
    <table>
        <tr><th>A</th><th>B</th></tr>
        <tr><td>数据1</td><td>数据2</td></tr>
    </table>
    """
    
    table_same_structure = """
    <table>
        <tr><th>X</th><th>Y</th></tr>
        <tr><td>值1</td><td>值2</td></tr>
    </table>
    """
    
    content_result = content_teds.calculate(table_diff_content, table_same_structure)
    structure_result = structure_teds.calculate(table_diff_content, table_same_structure)
    
    print(f"内容敏感 TEDS 得分: {content_result.score:.4f}")
    print(f"仅结构 S-TEDS 得分: {structure_result.score:.4f}")
    print(f"说明: S-TEDS 忽略文本内容差异，只关注表格结构")
    print()


def demo_evaluation_workflow():
    """演示完整的评估工作流程"""
    print("=== 📋 完整评估工作流程 ===\n")
    
    print("**步骤 1: 准备数据**")
    # 模拟评估数据
    sample_data = DataSample(
        id="sample_001",
        html="""
        <div>
            <h1>产品价格表</h1>
            <table>
                <tr><th>产品</th><th>价格</th><th>库存</th></tr>
                <tr><td>iPhone</td><td>5999元</td><td>50</td></tr>
                <tr><td>iPad</td><td>3999元</td><td>30</td></tr>
                <tr><td>MacBook</td><td>12999元</td><td>10</td></tr>
            </table>
        </div>
        """,
        content="产品价格表\n\n| 产品 | 价格 | 库存 |\n|------|------|------|\n| iPhone | 5999元 | 50 |\n| iPad | 3999元 | 30 |\n| MacBook | 12999元 | 10 |",
        content_list=[
            {
                "type": "title",
                "content": "产品价格表"
            },
            {
                "type": "table",
                "content": "| 产品 | 价格 | 库存 |\n|------|------|------|\n| iPhone | 5999元 | 50 |\n| iPad | 3999元 | 30 |\n| MacBook | 12999元 | 10 |"
            }
        ]
    )
    print("✅ 数据准备完成")
    
    print("\n**步骤 2: 配置 TEDS 评估器**")
    evaluation_config = {
        "metrics": {
            "overall": "edit_distance",
            "table_extraction": {
                "use_teds": True,
                "structure_only": False
            }
        }
    }
    
    evaluator = Evaluator(task_config=evaluation_config)
    print("✅ 评估器配置完成")
    
    print("\n**步骤 3: 模拟抽取结果**")
    # 模拟一个有轻微错误的抽取结果
    extraction_result = ExtractionResult(
        extractor_name="TestExtractor",
        extracted_content="产品价格表\n\n| 产品 | 价格 |\n|------|------|\n| iPhone | 5999元 |\n| iPad | 3999元 |",  # 缺少库存列和MacBook行
        extracted_content_list=[
            {
                "type": "title", 
                "content": "产品价格表"
            },
            {
                "type": "table",
                "content": "| 产品 | 价格 |\n|------|------|\n| iPhone | 5999元 |\n| iPad | 3999元 |"
            }
        ]
    )
    print("✅ 模拟抽取结果生成")
    
    print("\n**步骤 4: 执行评估**")
    evaluation_result = evaluator.evaluate_single(sample_data, extraction_result)
    
    print(f"📊 评估结果:")
    print(f"  - 整体得分: {evaluation_result.overall_metrics.get('overall', 'N/A'):.4f}")
    print(f"  - 表格抽取 (TEDS): {evaluation_result.overall_metrics.get('table_extraction', 'N/A'):.4f}")
    print(f"  - 成功率: {evaluation_result.metadata.get('success_rate', 'N/A'):.2%}")
    
    # 显示详细的 TEDS 信息
    if evaluation_result.detailed_metrics:
        for metric_name, metric_result in evaluation_result.detailed_metrics.items():
            if 'teds' in metric_name.lower():
                print(f"\n🔍 {metric_name} 详细信息:")
                details = metric_result.details
                print(f"  - 算法: {details.get('algorithm', 'N/A')}")
                print(f"  - 编辑距离: {details.get('edit_distance', 'N/A')}")
                print(f"  - 节点数量 (预测/真实): {details.get('predicted_nodes', 'N/A')}/{details.get('groundtruth_nodes', 'N/A')}")
    
    print("\n✅ 评估完成")


if __name__ == "__main__":
    print("🚀 WebMainBench TEDS 算法使用示例\n")
    print("=" * 60)
    
    try:
        demo_teds_configuration()
        print("=" * 60)
        
        demo_teds_comparison()
        print("=" * 60)
        
        demo_advanced_teds_features()
        print("=" * 60)
        
        demo_evaluation_workflow()
        
        print("\n🎉 所有演示完成！")
        print("\n💡 要点总结:")
        print("  1. TEDS 算法提供更学术严谨的表格评估")
        print("  2. 支持 HTML、Markdown 等多种表格格式")
        print("  3. 可配置结构化评估 (S-TEDS) 或内容敏感评估")
        print("  4. 能够准确识别表格结构差异和内容差异")
        print("  5. 与现有评估流程完全兼容")
        
    except Exception as e:
        print(f"\n❌ 演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc() 
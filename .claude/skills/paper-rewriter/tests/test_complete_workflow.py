#!/usr/bin/env python3
"""
完整工作流测试
测试从文档解析到改写到反馈的完整流程
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from rewrite_with_feedback import RewriteWithFeedback
from document_parser import parse_document, get_text_for_rewrite


def main():
    """主测试函数"""
    print("=" * 60)
    print("完整工作流测试")
    print("=" * 60)

    system = RewriteWithFeedback()

    # 测试1: 解析文档
    print("\n--- 测试1: 解析文档 ---")
    paper_path = r"E:\Desktop\Manuscript星儿修订版(1) - 副本.docx"
    result = parse_document(paper_path)

    if "error" in result:
        print(f"错误: {result['error']}")
        return

    print(f"文件: {result['file']}")
    print(f"段落数: {result['paragraph_count']}")
    for name, content in result["sections"].items():
        if content:
            if isinstance(content, list):
                print(f"  {name}: {len(content)} 段落")
            else:
                print(f"  {name}: {content[:50]}...")

    # 测试2: 获取摘要
    print("\n--- 测试2: 获取摘要 ---")
    abstract = get_text_for_rewrite(result, "abstract")
    print(f"摘要长度: {len(abstract)} 字符")

    # 测试3: 模拟改写并分析
    print("\n--- 测试3: 模拟改写并分析 ---")
    abstract_rewritten = """Rapid urbanization and intensive resource extraction have progressively deteriorated global ecosystems, especially within arid and semi-arid regions. While ecological security pattern (ESP) construction has emerged as a widely accepted strategy for maintaining ecosystem equilibrium, current methodologies predominantly address surface-level conditions and systematically neglect subsurface systems—specifically groundwater—which represents a critical constraining factor in dryland environments."""

    analysis = system.analyze_rewrite(
        abstract[:500],
        abstract_rewritten,
        domain="生态安全格局",
        intensity="heavy",
        section_type="abstract"
    )

    print(f"会话ID: {analysis['session_id']}")
    print(f"综合评分: {analysis['composite_score']}/100")
    sim = analysis["similarity"]
    print(f"  LCS 比率: {sim['lcs_ratio']:.1%}")
    print(f"  三元组精度: {sim['trigram_precision']:.1%}")
    print(f"  最长连续匹配: {sim['max_consecutive']} 词")

    # 测试4: 提交反馈
    print("\n--- 测试4: 提交反馈 ---")
    feedback = system.submit_feedback(
        session_id=analysis["session_id"],
        vocabulary_score=5,
        structure_score=4,
        terminology_score=5,
        overall_score=4,
        liked="专业术语保留得很好",
        improved="部分句子改写后不够自然",
        missing_terms=["生态安全格局", "地下水脆弱性"],
        suggestions="希望提供更多改写选项"
    )
    print(f"平均分: {sum(feedback['scores'].values()) / len(feedback['scores']):.1f}/5")

    # 测试5: 获取改写建议
    print("\n--- 测试5: 获取改写建议 ---")
    suggestions = system.get_suggestions("生态安全格局", "heavy")
    print(f"推荐技术: {[t['technique'] for t in suggestions['effective_techniques']]}")
    print(f"新术语: {suggestions['new_terms_to_preserve'][:5]}")

    # 测试6: 查看学习报告
    print("\n--- 测试6: 学习报告 ---")
    report = system.get_strategy_report()
    print(report[:500] + "..." if len(report) > 500 else report)

    print("\n" + "=" * 60)
    print("✅ 所有测试通过")
    print("=" * 60)


if __name__ == "__main__":
    main()

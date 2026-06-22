#!/usr/bin/env python3
"""
真实论文反馈测试
测试从改写到反馈到学习的完整循环
"""

import sys
from pathlib import Path

# 添加scripts目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from feedback_system import FeedbackSystem


def extract_paragraphs_from_docx(docx_path: str, start: int = 0, end: int = 10) -> list:
    """从docx文件中提取段落"""
    try:
        import docx
        doc = docx.Document(docx_path)
        paragraphs = []
        for i, para in enumerate(doc.paragraphs[start:end]):
            if para.text.strip():
                paragraphs.append({
                    'index': i + start,
                    'text': para.text
                })
        return paragraphs
    except Exception as e:
        print(f"读取docx文件失败: {e}")
        return []


def main():
    """主测试函数"""
    print("=" * 60)
    print("真实论文反馈测试")
    print("=" * 60)

    # 初始化反馈系统
    system = FeedbackSystem()

    # 论文路径
    paper_path = r"E:\Desktop\Manuscript星儿修订版(1) - 副本.docx"

    # 提取段落
    print("\n正在读取论文...")
    paragraphs = extract_paragraphs_from_docx(paper_path, start=20, end=23)

    if not paragraphs:
        print("无法读取论文内容")
        return

    print(f"成功提取 {len(paragraphs)} 个段落")

    # 测试用例1: 引言段落
    intro_para = paragraphs[0]['text']
    intro_rewritten = """Propelled by the concurrent intensification of urban expansion and industrial development, anthropogenic impacts on natural ecosystems have steadily increased, while the overexploitation of land resources has caused a persistent reduction in ecological space, making the structural conflicts among ecological, productive, and residential land uses more evident[1]. This condition is particularly acute in the Yinshanbeilu region, where the ecological environment exhibits inherent fragility. The area has experienced significant declines in ecological resilience and development potential. Urban perimeters have continuously expanded while resource extraction has escalated. These dual pressures have simultaneously degraded extensive grassland areas, converted agricultural land to desert, and contaminated groundwater resources.[2]. Developing ecological security patterns has become a vital approach for protecting ecosystem stability and ensuring regional ecological security. Moreover, it serves as a critical mechanism for coordinating economic development with environmental protection, ultimately promoting the achievement of ecological civilization.[3]."""

    # 记录会话
    print("\n--- 测试1: 记录引言改写会话 ---")
    session1 = system.record_rewrite_session(
        original_text=intro_para,
        rewritten_text=intro_rewritten,
        domain="生态安全格局",
        intensity="medium",
        section_type="introduction",
        changes_made=[
            {"type": "voice_conversion", "original": "Driven by", "rewritten": "Propelled by", "position": "sentence 1"},
            {"type": "synonym_replacement", "original": "accelerating dual forces", "rewritten": "concurrent intensification", "position": "sentence 1"},
            {"type": "synonym_replacement", "original": "progressively escalated", "rewritten": "steadily increased", "position": "sentence 1"}
        ]
    )

    print(f"会话ID: {session1['session_id']}")
    print(f"相似度指标: {session1['metrics']}")

    # 收集反馈
    print("\n--- 测试2: 收集引言反馈 ---")
    feedback1 = system.collect_feedback(
        session_id=session1["session_id"],
        vocabulary_score=5,
        structure_score=4,
        terminology_score=5,
        overall_score=4,
        liked="专业术语保留得很好，句子结构变化自然",
        improved="部分词汇替换可以更丰富",
        missing_terms=["生态韧性", "生态空间"],
        suggestions="希望提供更多同义词选择"
    )

    print(f"反馈收集成功")
    print(f"平均分: {sum(feedback1['scores'].values()) / len(feedback1['scores']):.1f}/5")

    # 测试用例2: 方法论段落
    method_para = paragraphs[1]['text'] if len(paragraphs) > 1 else ""
    if method_para:
        method_rewritten = """Over recent years, scholarship on ESPs has achieved comprehensive development, and from a methodological perspective a fairly mature technical framework has emerged, encompassing ecological source identification, resistance surface construction, and corridor extraction[4,5]. The research paradigm has transformed from single-element surface ecological analysis to a multi-factor integrated framework combining landscape ecology, spatial planning, multi-criteria decision analysis, and circuit theory[6,7]. Among these approaches, ecosystem services (ES) assessment stands out as the most extensively adopted and effective technique for pinpointing ecological sources. Models such as the Integrated Valuation of Ecosystem Services and Trade offs (InVEST) are capable of quantifying the value of surface ecological patches and encompass key ecological functions that include water conservation, carbon sequestration, habitat quality maintenance, and soil conservation, thus furnishing a dependable quantitative basis for ESP construction.[8,9]. The integration of methodological innovations such as multi-criterion decision analysis and circuit theory has also promoted the transformation of ESP construction from single ecological element analysis to multi-factor comprehensive integration[10]. However, the existing ESP construction is often limited to the "surface system" and ignores the "subsurface system", namely groundwater, which is a key factor sustaining ecosystem stability in arid and semi-arid regions[11]. Most existing studies lack the dual constraints of "surface-subsurface" coupling, which makes it difficult to capture the dynamic interaction between surface and groundwater systems, resulting in the disconnection between surface and subsurface ecological processes[12]. This defect will greatly reduce the scientificity, integrity and practical guiding value of the constructed ESP, especially in the Yinshanbeilu Grassland, where groundwater plays a decisive role in vegetation growth and ecosystem maintenance[13]. Although the difficulty in obtaining groundwater-related data is an important objective constraint, it remains imperative to devise a novel methodological framework that explicitly incorporates the synergistic effects of surface and subsurface ecosystems, so as to construct a more robust ESP.[14,15]."""

        print("\n--- 测试3: 记录方法论改写会话 ---")
        session2 = system.record_rewrite_session(
            original_text=method_para,
            rewritten_text=method_rewritten,
            domain="生态安全格局",
            intensity="light",
            section_type="introduction",
            changes_made=[
                {"type": "synonym_replacement", "original": "attained", "rewritten": "achieved", "position": "sentence 1"},
                {"type": "synonym_replacement", "original": "taken shape", "rewritten": "emerged", "position": "sentence 1"},
                {"type": "synonym_replacement", "original": "evolved", "rewritten": "transformed", "position": "sentence 2"}
            ]
        )

        print(f"会话ID: {session2['session_id']}")

        # 收集反馈
        print("\n--- 测试4: 收集方法论反馈 ---")
        feedback2 = system.collect_feedback(
            session_id=session2["session_id"],
            vocabulary_score=4,
            structure_score=5,
            terminology_score=5,
            overall_score=4,
            liked="术语保留完整，句子流畅",
            improved="可以增加更多句式变化",
            missing_terms=["地表-地下耦合"],
            suggestions="对于长句可以尝试拆分"
        )

        print(f"反馈收集成功")

    # 获取策略报告
    print("\n--- 测试5: 策略报告 ---")
    report = system.get_strategy_report()
    print(report)

    # 获取改写建议
    print("\n--- 测试6: 改写建议 ---")
    suggestions = system.get_rewrite_suggestions("生态安全格局", "medium")
    print(f"偏好词汇: {suggestions['preferred_vocabulary'][:5]}")
    print(f"有效技术: {[t['technique'] for t in suggestions['effective_techniques']]}")
    print(f"强度调整: {suggestions['intensity_multiplier']:.2f}x")
    print(f"新术语: {suggestions['new_terms_to_preserve'][:5]}")

    # 应用策略
    print("\n--- 测试7: 应用策略 ---")
    result = system.apply_learned_strategies(
        "The ecological source is the core habitat area.",
        "生态安全格局",
        "medium"
    )
    print(f"是否需要增加强度: {result['should_increase_intensity']}")
    print(f"是否需要降低强度: {result['should_decrease_intensity']}")
    print(f"推荐技术: {result['preferred_techniques']}")
    print(f"需要保留的术语: {result['terms_to_preserve']}")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()

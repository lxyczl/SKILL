#!/usr/bin/env python3
"""
反馈系统测试脚本
测试完整的反馈学习循环
"""

import sys
from pathlib import Path

# 添加scripts目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from feedback_system import FeedbackSystem


def test_feedback_system():
    """测试反馈系统"""
    print("=" * 60)
    print("反馈系统测试")
    print("=" * 60)

    # 初始化系统
    system = FeedbackSystem()
    print(f"✅ 系统初始化成功")
    print(f"   反馈目录: {system.feedback_dir}")

    # 测试1: 记录改写会话
    print("\n--- 测试1: 记录改写会话 ---")
    original = "The ecological source is the core habitat area. The ecological corridor connects fragmented patches."
    rewritten = "The ecological source constitutes the fundamental habitat area. The ecological corridor facilitates connectivity between fragmented patches."

    session = system.record_rewrite_session(
        original_text=original,
        rewritten_text=rewritten,
        domain="生态安全格局",
        intensity="medium",
        section_type="introduction",
        changes_made=[
            {"type": "synonym_replacement", "original": "is", "rewritten": "constitutes", "position": "sentence 1"},
            {"type": "synonym_replacement", "original": "connects", "rewritten": "facilitates connectivity between", "position": "sentence 2"}
        ]
    )

    print(f"✅ 会话记录成功: {session['session_id']}")
    print(f"   指标: {session['metrics']}")

    # 测试2: 收集反馈
    print("\n--- 测试2: 收集反馈 ---")
    updated_session = system.collect_feedback(
        session_id=session["session_id"],
        vocabulary_score=5,
        structure_score=4,
        terminology_score=5,
        overall_score=4,
        liked="专业术语保留得很好",
        improved="部分句子改写后不够自然",
        missing_terms=["生态节点", "生态阻力面"],
        suggestions="希望提供更多改写选项"
    )

    print(f"✅ 反馈收集成功")
    print(f"   评分: {updated_session['scores']}")

    # 测试3: 记录多个会话以测试学习
    print("\n--- 测试3: 记录多个会话 ---")
    test_sessions = [
        {
            "original": "The model was used to calculate the water yield.",
            "rewritten": "The model was employed to compute the water yield.",
            "domain": "生态水文",
            "intensity": "light",
            "scores": {"vocabulary_score": 4, "structure_score": 3, "terminology_score": 5, "overall_score": 4}
        },
        {
            "original": "The results show that the method is effective.",
            "rewritten": "The findings demonstrate that the approach is effective.",
            "domain": "生态水文",
            "intensity": "medium",
            "scores": {"vocabulary_score": 5, "structure_score": 5, "terminology_score": 5, "overall_score": 5}
        },
        {
            "original": "The study area is located in the north of China.",
            "rewritten": "The research region is situated in northern China.",
            "domain": "生态安全格局",
            "intensity": "heavy",
            "scores": {"vocabulary_score": 3, "structure_score": 2, "terminology_score": 4, "overall_score": 3}
        }
    ]

    for i, test in enumerate(test_sessions, 1):
        session = system.record_rewrite_session(
            test["original"],
            test["rewritten"],
            test["domain"],
            test["intensity"]
        )
        system.collect_feedback(
            session["session_id"],
            **test["scores"]
        )
        print(f"   会话 {i}: {session['session_id']}")

    print(f"✅ 成功记录 {len(test_sessions)} 个会话")

    # 测试4: 获取策略报告
    print("\n--- 测试4: 策略报告 ---")
    report = system.get_strategy_report()
    print(report)

    # 测试5: 获取改写建议
    print("\n--- 测试5: 改写建议 ---")
    suggestions = system.get_rewrite_suggestions("生态水文", "medium")
    print(f"偏好词汇: {suggestions['preferred_vocabulary'][:5]}")
    print(f"有效技术: {[t['technique'] for t in suggestions['effective_techniques']]}")
    print(f"强度调整: {suggestions['intensity_multiplier']:.2f}x")
    print(f"新术语: {suggestions['new_terms_to_preserve'][:5]}")

    # 测试6: 应用策略
    print("\n--- 测试6: 应用策略 ---")
    result = system.apply_learned_strategies(
        "The model was used to calculate the water yield.",
        "生态水文",
        "medium"
    )
    print(f"是否需要增加强度: {result['should_increase_intensity']}")
    print(f"是否需要降低强度: {result['should_decrease_intensity']}")
    print(f"推荐技术: {result['preferred_techniques']}")
    print(f"需要保留的术语: {result['terms_to_preserve']}")

    print("\n" + "=" * 60)
    print("✅ 所有测试通过")
    print("=" * 60)


if __name__ == "__main__":
    test_feedback_system()

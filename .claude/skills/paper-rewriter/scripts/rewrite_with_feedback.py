"""
改写分析 + 反馈集成
SKILL.md 调用此脚本完成：相似度分析 → 会话记录 → 获取学习建议
"""
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from feedback_system import FeedbackSystem
from similarity_calculator import calculate_similarity, format_report


class RewriteWithFeedback:
    """改写分析 + 反馈系统"""

    def __init__(self, skill_dir: Path = None):
        if skill_dir is None:
            skill_dir = Path(__file__).parent.parent
        self.skill_dir = skill_dir
        self.feedback_system = FeedbackSystem(skill_dir)

    def analyze_rewrite(
        self,
        original: str,
        rewritten: str,
        domain: str = "general",
        intensity: str = "medium",
        section_type: str = "unknown"
    ) -> dict:
        """
        分析改写结果并记录会话。

        返回:
            session_id, similarity (完整指标), suggestions, composite_score, report
        """
        similarity = calculate_similarity(original, rewritten)

        session = self.feedback_system.record_rewrite_session(
            original_text=original,
            rewritten_text=rewritten,
            domain=domain,
            intensity=intensity,
            section_type=section_type
        )

        suggestions = self.feedback_system.get_rewrite_suggestions(domain, intensity)

        return {
            "session_id": session["session_id"],
            "similarity": similarity,
            "suggestions": suggestions,
            "composite_score": similarity["composite_score"],
            "report": format_report(original, rewritten),
        }

    def submit_feedback(self, session_id: str, **kwargs) -> dict:
        """提交用户反馈"""
        return self.feedback_system.collect_feedback(session_id=session_id, **kwargs)

    def get_suggestions(self, domain: str = "general", intensity: str = "medium") -> dict:
        """获取基于历史反馈的改写建议"""
        return self.feedback_system.get_rewrite_suggestions(domain, intensity)

    def get_strategy_report(self) -> str:
        """获取反馈学习策略报告"""
        return self.feedback_system.get_strategy_report()



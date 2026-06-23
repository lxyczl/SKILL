"""
反馈系统测试
"""
import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from feedback_system import FeedbackSystem


class TestFeedbackSystemUnit:
    """反馈系统单元测试"""

    def test_record_session(self, tmp_path):
        system = FeedbackSystem(tmp_path)
        session = system.record_rewrite_session(
            original_text="The results show that the method is effective",
            rewritten_text="The findings demonstrate that the approach is efficacious",
            domain="general",
            intensity="medium",
            section_type="abstract"
        )
        assert "session_id" in session
        assert session["domain"] == "general"
        assert "metrics" in session
        assert session["metrics"]["lcs_ratio"] > 0

    def test_collect_feedback(self, tmp_path):
        system = FeedbackSystem(tmp_path)
        session = system.record_rewrite_session(
            original_text="Test original",
            rewritten_text="Test rewritten",
            domain="test",
            intensity="medium"
        )
        result = system.collect_feedback(
            session_id=session["session_id"],
            vocabulary_score=4,
            structure_score=5,
            terminology_score=4,
            overall_score=4
        )
        assert result["scores"]["vocabulary"] == 4
        assert result["scores"]["overall_satisfaction"] == 4

    def test_get_suggestions(self, tmp_path):
        system = FeedbackSystem(tmp_path)
        suggestions = system.get_rewrite_suggestions("general", "medium")
        assert "effective_techniques" in suggestions
        assert "intensity_multiplier" in suggestions
        assert "new_terms_to_preserve" in suggestions

    def test_learning_from_feedback(self, tmp_path):
        system = FeedbackSystem(tmp_path)
        session = system.record_rewrite_session(
            original_text="Test",
            rewritten_text="Test rewritten",
            domain="test",
            intensity="medium"
        )
        system.collect_feedback(
            session_id=session["session_id"],
            vocabulary_score=5,
            structure_score=5,
            terminology_score=5,
            overall_score=5,
            missing_terms=["new_term_1", "new_term_2"]
        )
        suggestions = system.get_rewrite_suggestions("test", "medium")
        assert "new_term_1" in suggestions["new_terms_to_preserve"]

    def test_strategy_report(self, tmp_path):
        system = FeedbackSystem(tmp_path)
        report = system.get_strategy_report()
        assert "反馈学习策略报告" in report

    def test_multiple_sessions_learning(self, tmp_path):
        """测试多次会话后学习效果"""
        system = FeedbackSystem(tmp_path)
        sessions_data = [
            ("water flow", "hydrological flux", "生态水文", "light", 4),
            ("method is effective", "approach demonstrates efficacy", "生态水文", "medium", 5),
            ("study area", "research region", "生态安全格局", "heavy", 3),
        ]
        for orig, rew, domain, intensity, score in sessions_data:
            session = system.record_rewrite_session(orig, rew, domain, intensity)
            system.collect_feedback(session["session_id"], overall_score=score)

        suggestions = system.get_rewrite_suggestions("生态水文", "medium")
        assert "intensity_multiplier" in suggestions

    def test_missing_session_raises(self, tmp_path):
        """测试提交不存在的会话 ID 报错"""
        system = FeedbackSystem(tmp_path)
        with pytest.raises(ValueError, match="找不到会话"):
            system.collect_feedback(session_id="nonexistent-id", overall_score=3)

    def test_apply_learned_strategies(self, tmp_path):
        """测试策略应用"""
        system = FeedbackSystem(tmp_path)
        session = system.record_rewrite_session(
            "The model was used to calculate the water yield.",
            "The model was employed to compute the water yield.",
            "生态水文", "medium"
        )
        system.collect_feedback(session["session_id"], overall_score=5)

        result = system.apply_learned_strategies(
            "The model was used to calculate the water yield.",
            "生态水文", "medium"
        )
        assert "should_increase_intensity" in result
        assert "preferred_techniques" in result
        assert "terms_to_preserve" in result


class TestAutoEvaluate:
    """测试自动评估"""

    def test_auto_evaluate_excellent(self):
        from feedback_system import auto_evaluate
        metrics = {"max_consecutive": 2, "trigram_precision": 0.05}
        result = auto_evaluate(metrics)
        assert result["verdict"] == "excellent"
        assert result["is_success"] is True

    def test_auto_evaluate_fail(self):
        from feedback_system import auto_evaluate
        metrics = {"max_consecutive": 10, "trigram_precision": 0.1}
        result = auto_evaluate(metrics)
        assert result["verdict"] == "fail"
        assert result["is_success"] is False

    def test_auto_evaluate_warning_mc(self):
        from feedback_system import auto_evaluate
        metrics = {"max_consecutive": 6, "trigram_precision": 0.1}
        result = auto_evaluate(metrics)
        assert result["verdict"] == "warning"

    def test_auto_evaluate_warning_tri(self):
        from feedback_system import auto_evaluate
        metrics = {"max_consecutive": 3, "trigram_precision": 0.35}
        result = auto_evaluate(metrics)
        assert result["verdict"] == "warning"

    def test_auto_evaluate_success(self):
        from feedback_system import auto_evaluate
        metrics = {"max_consecutive": 4, "trigram_precision": 0.20}
        result = auto_evaluate(metrics)
        assert result["verdict"] == "success"
        assert result["is_success"] is True


class TestClassifyFailure:
    """测试失败分类"""

    def test_classify_failure_consecutive(self):
        from feedback_system import classify_failure
        assert classify_failure({"max_consecutive": 10}, "fail") == "consecutive_too_long"

    def test_classify_failure_structure(self):
        from feedback_system import classify_failure
        assert classify_failure({"max_consecutive": 6, "trigram_precision": 0.28}, "warning") == "structure_too_similar"

    def test_classify_failure_consecutive_risk(self):
        from feedback_system import classify_failure
        assert classify_failure({"max_consecutive": 6, "trigram_precision": 0.1}, "warning") == "consecutive_risk"

    def test_classify_failure_trigram_risk(self):
        from feedback_system import classify_failure
        assert classify_failure({"max_consecutive": 3, "trigram_precision": 0.25}, "warning") == "trigram_risk"

    def test_classify_failure_none(self):
        from feedback_system import classify_failure
        assert classify_failure({}, "excellent") == "none"
        assert classify_failure({}, "success") == "none"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

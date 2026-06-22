"""
基础测试套件
测试核心功能
"""
import pytest
from pathlib import Path
import sys

# 添加 scripts 目录到路径
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))


class TestSimilarityCalculator:
    """测试相似度计算器"""

    def test_tokenize(self):
        from similarity_calculator import tokenize
        result = tokenize("The results show that the method is effective")
        assert len(result) > 0
        assert "the" in result
        assert "results" in result

    def test_tokenize_ignores_punctuation(self):
        from similarity_calculator import tokenize
        result = tokenize("Hello, world! This is a test.")
        assert result == ["hello", "world", "this", "is", "a", "test"]

    def test_ngrams(self):
        from similarity_calculator import ngrams
        tokens = ["the", "results", "show", "that"]
        result = ngrams(tokens, 2)
        assert len(result) == 3
        assert ("the", "results") in result
        assert ("show", "that") in result

    def test_lcs_identical(self):
        from similarity_calculator import lcs_ratio
        a = ["the", "method", "is", "effective"]
        assert lcs_ratio(a, a) == 1.0

    def test_lcs_completely_different(self):
        from similarity_calculator import lcs_ratio
        a = ["a", "b", "c"]
        b = ["x", "y", "z"]
        assert lcs_ratio(a, b) == 0.0

    def test_lcs_partial(self):
        from similarity_calculator import lcs_ratio
        a = ["the", "method", "is", "effective"]
        b = ["the", "approach", "is", "effective"]
        # LCS = ["the", "is", "effective"] = 3, min(len) = 4
        ratio = lcs_ratio(a, b)
        assert 0.5 < ratio < 1.0

    def test_lcs_empty(self):
        from similarity_calculator import lcs_ratio
        assert lcs_ratio([], ["a"]) == 0.0
        assert lcs_ratio(["a"], []) == 0.0

    def test_ngram_precision(self):
        from similarity_calculator import ngram_precision, tokenize
        orig = tokenize("the method is effective and reliable")
        rew = tokenize("the method is effective and reliable")
        assert ngram_precision(orig, rew, 2) == 1.0

    def test_ngram_precision_low(self):
        from similarity_calculator import ngram_precision, tokenize
        orig = tokenize("the method is effective")
        rew = tokenize("an approach works well")
        assert ngram_precision(orig, rew, 2) < 0.3

    def test_ngram_recall(self):
        from similarity_calculator import ngram_recall, tokenize
        orig = tokenize("the method is effective")
        rew = tokenize("the method is effective and reliable")
        # orig bigrams are all in rew
        assert ngram_recall(orig, rew, 2) == 1.0

    def test_vocabulary_overlap_identical(self):
        from similarity_calculator import vocabulary_overlap, tokenize
        tokens = tokenize("the method is effective")
        assert vocabulary_overlap(tokens, tokens) == 1.0

    def test_vocabulary_overlap_different(self):
        from similarity_calculator import vocabulary_overlap, tokenize
        a = tokenize("the method is effective")
        b = tokenize("an approach works well")
        assert vocabulary_overlap(a, b) < 0.3

    def test_find_consecutive_matches(self):
        from similarity_calculator import find_consecutive_matches, tokenize
        orig = tokenize("the quick brown fox jumps over the lazy dog")
        rew = tokenize("the quick brown fox leaps over the lazy dog")
        matches = find_consecutive_matches(orig, rew, min_length=4)
        # "the quick brown fox" = 4 consecutive, "over the lazy dog" = 4 consecutive
        assert len(matches) >= 2
        assert any(m["length"] >= 4 for m in matches)

    def test_find_consecutive_no_match(self):
        from similarity_calculator import find_consecutive_matches, tokenize
        orig = tokenize("the method is effective")
        rew = tokenize("an approach works well")
        matches = find_consecutive_matches(orig, rew, min_length=4)
        assert len(matches) == 0

    def test_calculate_similarity(self):
        from similarity_calculator import calculate_similarity
        original = "The results show that the method is effective"
        rewritten = "The findings demonstrate that the approach is efficacious"
        result = calculate_similarity(original, rewritten)
        assert "composite_score" in result
        assert "lcs_ratio" in result
        assert "bigram_precision" in result
        assert "trigram_precision" in result
        assert "max_consecutive" in result
        assert "consecutive_matches" in result
        assert 0 <= result["composite_score"] <= 100

    def test_calculate_similarity_identical(self):
        from similarity_calculator import calculate_similarity
        text = "The results show that the method is effective"
        result = calculate_similarity(text, text)
        assert result["composite_score"] >= 80  # identical = very high similarity

    def test_calculate_similarity_different(self):
        from similarity_calculator import calculate_similarity
        original = "The results show that the method is effective"
        rewritten = "An entirely different approach was utilized for this investigation"
        result = calculate_similarity(original, rewritten)
        assert result["composite_score"] < 40  # very different = low similarity

    def test_format_report(self):
        from similarity_calculator import format_report
        original = "The results show that the method is effective"
        rewritten = "The findings demonstrate that the approach is efficacious"
        result = format_report(original, rewritten)
        assert "相似度分析报告" in result
        assert "综合评分" in result
        assert "LCS" in result


class TestTurnitinParser:
    """测试 Turnitin 解析器"""

    def test_detect_color(self):
        from turnitin_parser import detect_color
        assert detect_color("[RED] This is red text") == "red"
        assert detect_color("[ORANGE] This is orange text") == "orange"
        assert detect_color("[YELLOW] This is yellow text") == "yellow"
        assert detect_color("[GREEN] This is green text") == "green"
        assert detect_color("[BLUE] This is blue text") == "blue"

    def test_detect_color_none(self):
        from turnitin_parser import detect_color
        assert detect_color("This is normal text") is None

    def test_parse_turnitin_report(self):
        from turnitin_parser import parse_turnitin_report
        report = """
[RED] This is high similarity text.
[ORANGE] This is medium similarity text.
[YELLOW] This is low similarity text.
[GREEN] This is citation text.
[BLUE] This is no similarity text.
"""
        result = parse_turnitin_report(report)
        assert "summary" in result
        assert "paragraphs" in result
        assert "priority_report" in result
        assert result["summary"]["red_count"] == 1

    def test_format_turnitin_report(self):
        from turnitin_parser import format_turnitin_report
        result = {
            "summary": {
                "total_paragraphs": 5,
                "red_count": 1,
                "orange_count": 1,
                "yellow_count": 1,
                "green_count": 1,
                "blue_count": 1
            },
            "paragraphs": {
                "red": [{"index": 1, "text": "Red text", "color": "red", "priority": "HIGH"}],
                "orange": [{"index": 2, "text": "Orange text", "color": "orange", "priority": "MEDIUM"}],
                "yellow": [{"index": 3, "text": "Yellow text", "color": "yellow", "priority": "LOW"}],
                "green": [{"index": 4, "text": "Green text", "color": "green", "priority": "CITATION"}],
                "blue": [{"index": 5, "text": "Blue text", "color": "blue", "priority": "NONE"}]
            },
            "priority_report": []
        }
        report = format_turnitin_report(result)
        assert "Turnitin 报告分析" in report

    def test_get_intensity_for_color(self):
        from turnitin_parser import get_intensity_for_color
        assert get_intensity_for_color("red") == "heavy"
        assert get_intensity_for_color("orange") == "medium"
        assert get_intensity_for_color("yellow") == "light"
        assert get_intensity_for_color("blue") == "none"


class TestFeedbackSystem:
    """测试反馈系统"""

    def test_record_session(self, tmp_path):
        from feedback_system import FeedbackSystem
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

    def test_collect_feedback(self, tmp_path):
        from feedback_system import FeedbackSystem
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
        from feedback_system import FeedbackSystem
        system = FeedbackSystem(tmp_path)
        suggestions = system.get_rewrite_suggestions("general", "medium")
        assert "effective_techniques" in suggestions
        assert "intensity_multiplier" in suggestions
        assert "new_terms_to_preserve" in suggestions

    def test_learning_from_feedback(self, tmp_path):
        from feedback_system import FeedbackSystem
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
        from feedback_system import FeedbackSystem
        system = FeedbackSystem(tmp_path)
        report = system.get_strategy_report()
        assert "反馈学习策略报告" in report


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

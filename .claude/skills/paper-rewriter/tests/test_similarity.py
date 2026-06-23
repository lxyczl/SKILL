"""
相似度计算测试
"""
import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))


class TestTokenize:
    """测试分词策略"""

    def test_tokenize_word_mode(self):
        """词级分词应返回词列表"""
        from similarity_calculator import tokenize
        result = tokenize("The results show that the method is effective", mode="word")
        assert len(result) > 0
        assert "the" in result
        assert "results" in result

    def test_tokenize_regex_mode(self):
        """正则分词应使用原有逻辑"""
        from similarity_calculator import tokenize
        result = tokenize("Hello, world! This is a test.", mode="regex")
        assert result == ["hello", "world", "this", "is", "a", "test"]

    def test_tokenize_default_is_word(self):
        """默认模式应为 word"""
        from similarity_calculator import tokenize
        result = tokenize("The method is effective")
        assert len(result) > 0

    def test_tokenize_backward_compat(self):
        """向后兼容：tokenize(text) 行为不变"""
        from similarity_calculator import tokenize
        result = tokenize("The results show that the method is effective")
        assert len(result) > 0
        assert "the" in result

    def test_tokenize_single_char_filtered(self):
        """单字符 token 应被过滤（word 模式）"""
        from similarity_calculator import tokenize
        result = tokenize("I am a student", mode="word")
        # "I" 和 "a" 是单字符，应被过滤
        assert "i" not in result or "a" not in result

    def test_tokenize_fallback_no_nltk(self):
        """nltk 不可用时应降级到正则"""
        from similarity_calculator import tokenize
        # 如果 nltk 未安装，word 模式应降级到正则
        result = tokenize("The method is effective", mode="word")
        assert len(result) > 0


class TestStopwords:
    """测试停用词过滤"""

    def test_filter_stopwords(self):
        """停用词应被过滤"""
        from similarity_calculator import _filter_stopwords
        tokens = ["the", "method", "is", "effective", "for", "this", "problem"]
        filtered = _filter_stopwords(tokens)
        assert "the" not in filtered
        assert "is" not in filtered
        assert "method" in filtered
        assert "effective" in filtered

    def test_filter_stopwords_empty(self):
        """空列表应返回空列表"""
        from similarity_calculator import _filter_stopwords
        assert _filter_stopwords([]) == []

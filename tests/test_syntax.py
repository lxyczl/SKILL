import pytest
from analyzer.syntax import analyze_syntax

def test_uniform_sentences():
    text = "这是第一个测试句子。这是第二个测试句子。这是第三个测试句子。"
    result = analyze_syntax(text)
    assert result["score"] > 0
    assert any(i["type"] == "uniform_sentence_length" for i in result["issues"])

def test_varied_sentences():
    text = "短句。这是一个明显更长的句子，包含更多的内容和细节描述。中等长度的句子。"
    result = analyze_syntax(text)
    assert result["score"] < 0.3

def test_short_text():
    result = analyze_syntax("一句话。")
    assert result["score"] == 0.0

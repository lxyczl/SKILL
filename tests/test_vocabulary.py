import pytest
from analyzer.vocabulary import analyze_vocabulary

def test_cliche_detection():
    text = "综上所述，本文提出了一种方法。值得注意的是，该方法取得了较好的效果。"
    result = analyze_vocabulary(text, [])
    assert result["score"] > 0
    assert any(i["type"] == "cliche_detected" for i in result["issues"])

def test_clean_text():
    text = "这个方案的思路来自对问题的拆解。我们先处理核心矛盾，再扩展到边界情况。"
    result = analyze_vocabulary(text, [])
    assert result["score"] < 0.3

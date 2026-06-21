import pytest
from analyzer.structure import analyze_structure

def test_uniform_paragraphs():
    paras = [
        {"index": 0, "text": "A" * 100, "char_count": 100, "section_type": "body"},
        {"index": 1, "text": "B" * 100, "char_count": 100, "section_type": "body"},
        {"index": 2, "text": "C" * 100, "char_count": 100, "section_type": "body"},
    ]
    result = analyze_structure(paras)
    assert result["score"] > 0

def test_varied_paragraphs():
    paras = [
        {"index": 0, "text": "短段", "char_count": 10, "section_type": "body"},
        {"index": 1, "text": "B" * 200, "char_count": 200, "section_type": "body"},
        {"index": 2, "text": "C" * 50, "char_count": 50, "section_type": "body"},
    ]
    result = analyze_structure(paras)
    assert result["score"] < 0.3

import pytest
from analyzer.ai_traces import analyze_ai_traces

def test_too_fluent():
    text = "这是一个非常标准的学术论文段落。它包含了完整的句子结构。每个句子都很规范。没有口语化的表达。行文非常工整。"
    result = analyze_ai_traces(text)
    assert result["score"] > 0

def test_natural_text():
    text = "笔者在实验中发现——意外地——结果和预期不同。可能是参数设置的问题，也可能是数据本身的噪声。不确定。"
    result = analyze_ai_traces(text)
    assert result["score"] < 0.3

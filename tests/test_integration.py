"""端到端集成测试。"""

import json
import pytest
from pathlib import Path
from analyzer.paragraphs import split_paragraphs
from analyzer.scorer import score_paragraphs, compute_overall_risk
from analyzer.patterns import PatternLibrary
from rewriter.context import build_context
from rewriter.verify import verify_accuracy
from rewriter.diff import generate_diff_report


@pytest.fixture
def builtin_patterns():
    return PatternLibrary.load(Path(".claude/skills/rewrite/patterns"))


def test_full_pipeline(builtin_patterns):
    """测试完整分析流程。"""
    text = """综上所述，本文提出了一种基于深度学习的方法。该方法具有重要意义，引起了广泛关注。实验结果表明，该方法取得了较好的效果。该方法具有重要意义。该方法取得了较好的效果。该领域的研究日益增多。该方法具有重要意义。该方法取得了较好的效果。该领域的研究日益增多。

近年来，该领域的研究日益增多。该方法具有重要意义。该方法取得了较好的效果。该领域的研究日益增多。该方法具有重要意义。该方法取得了较好的效果。该领域的研究日益增多。该方法具有重要意义。该方法取得了较好的效果。该领域的研究日益增多。"""

    paragraphs = split_paragraphs(text, is_markdown=False)
    assert len(paragraphs) == 2

    scored = score_paragraphs(paragraphs, builtin_patterns.get_patterns())
    assert len(scored) == 2

    overall = compute_overall_risk(scored)
    assert overall > 0.3  # 这段文本 AI 特征明显


def test_low_risk_text(builtin_patterns):
    """低风险文本不应被过度标记。"""
    text = """笔者在搭建实验环境时遇到了一个问题——服务器的 GPU 内存不够。

最后换了 batch size 才解决，虽然浪费了不少时间。

这个经历让笔者意识到，实验前的资源评估同样重要。"""

    paragraphs = split_paragraphs(text, is_markdown=False)
    scored = score_paragraphs(paragraphs, builtin_patterns.get_patterns())
    overall = compute_overall_risk(scored)
    assert overall < 0.4


def test_context_window(builtin_patterns):
    """测试上下文窗口构建。"""
    text = "段落一。\n\n段落二。\n\n段落三。\n\n段落四。\n\n段落五。"
    paragraphs = split_paragraphs(text, is_markdown=False)
    ctx = build_context(paragraphs, 2)
    assert len(ctx["before"]) == 2
    assert len(ctx["after"]) == 2
    assert ctx["target"] == "段落三。"


def test_accuracy_verification():
    """测试准确性验证。"""
    original = "围护结构的热工性能直接影响建筑能耗模拟的结果。"
    rewritten_good = "围护结构的热工特性对建筑能耗模拟的输出有直接影响。"
    rewritten_bad = "外围结构的热工特性对建筑能耗模拟的输出有直接影响。"

    result_good = verify_accuracy(original, rewritten_good, {"围护结构", "建筑能耗模拟"})
    assert result_good["is_safe"]

    result_bad = verify_accuracy(original, rewritten_bad, {"围护结构", "建筑能耗模拟"})
    assert not result_bad["is_safe"]


def test_diff_report():
    """测试 diff 报告生成。"""
    results = [
        {
            "index": 0,
            "section_type": "body",
            "original_risk": 0.8,
            "rewritten_risk": 0.2,
            "original_text": "综上所述，本文提出了一种方法。",
            "rewritten_text": "回到前文的问题，本文的方案如下。",
            "suspects": [],
        }
    ]
    report = generate_diff_report(results)
    assert "| 0 |" in report
    assert "0.80" in report
    assert "0.20" in report


def test_markdown_sections():
    """测试 Markdown 文件的章节识别。"""
    text = """# 论文标题

## 摘要

本文研究了建筑能耗模拟方法。

## 引言

近年来，建筑能耗问题日益突出。

## 方法

实验采用了 EnergyPlus 软件。

## 结论

综上所述，该方法有效。"""

    paragraphs = split_paragraphs(text, is_markdown=True)
    sections = [p["section_type"] for p in paragraphs]
    assert "abstract" in sections
    assert "introduction" in sections
    assert "method" in sections
    assert "conclusion" in sections

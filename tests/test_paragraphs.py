"""段落切分与章节识别测试。"""

import pytest
from analyzer.paragraphs import split_paragraphs, detect_section


class TestDetectSection:
    def test_chinese_abstract(self):
        assert detect_section("摘要") == "abstract"
        assert detect_section("## 摘要") == "abstract"

    def test_chinese_introduction(self):
        assert detect_section("1 引言") == "introduction"

    def test_chinese_method(self):
        assert detect_section("3 实验方法") == "method"

    def test_chinese_results(self):
        assert detect_section("4 实验结果") == "results"

    def test_chinese_discussion(self):
        assert detect_section("5 讨论") == "discussion"

    def test_chinese_conclusion(self):
        assert detect_section("6 结论") == "conclusion"

    def test_english_abstract(self):
        assert detect_section("Abstract") == "abstract"

    def test_english_method(self):
        assert detect_section("## Methodology") == "method"

    def test_unmatched(self):
        assert detect_section("任意标题") == "body"


class TestSplitParagraphs:
    def test_plain_text(self):
        text = "第一段内容。\n\n第二段内容。\n\n第三段内容。"
        paras = split_paragraphs(text, is_markdown=False)
        assert len(paras) == 3
        assert paras[0]["text"] == "第一段内容。"
        assert paras[1]["text"] == "第二段内容。"
        assert paras[2]["index"] == 2

    def test_markdown_with_headings(self):
        text = "# 标题\n\n## 摘要\n\n这是摘要内容。\n\n## 引言\n\n这是引言内容。"
        paras = split_paragraphs(text, is_markdown=True)
        # 标题行不作为独立段落，而是标记后续段落的章节类型
        assert paras[0]["section_type"] == "abstract"
        assert paras[1]["section_type"] == "introduction"

    def test_empty_text(self):
        paras = split_paragraphs("", is_markdown=False)
        assert paras == []

    def test_whitespace_only(self):
        paras = split_paragraphs("   \n\n   ", is_markdown=False)
        assert paras == []

    def test_long_paragraph_split(self):
        """单段 > 2000 字应拆分。"""
        text = "这是一个测试。" * 500  # 约 3000 字
        paras = split_paragraphs(text, is_markdown=False)
        assert len(paras) > 1

    def test_char_count(self):
        text = "测试段落。"
        paras = split_paragraphs(text, is_markdown=False)
        assert paras[0]["char_count"] == 5

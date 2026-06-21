"""模式库加载器测试。"""

import json
import pytest
from pathlib import Path
from analyzer.patterns import PatternLibrary


@pytest.fixture
def tmp_patterns(tmp_path):
    """创建临时模式库目录。"""
    builtin = {
        "patterns": [
            {"id": "test_001", "type": "cliche", "match": "测试词", "replacements": ["替换词"], "platform_weight": {"cnki": 0.8}}
        ],
        "protected_terms": ["测试术语"]
    }
    user = {"patterns": [], "protected_terms": ["用户术语"]}
    learned = {"patterns": [], "protected_terms": []}

    (tmp_path / "builtin.json").write_text(json.dumps(builtin, ensure_ascii=False), encoding="utf-8")
    (tmp_path / "user.json").write_text(json.dumps(user, ensure_ascii=False), encoding="utf-8")
    (tmp_path / "learned.json").write_text(json.dumps(learned, ensure_ascii=False), encoding="utf-8")
    return tmp_path


def test_load_patterns(tmp_patterns):
    lib = PatternLibrary.load(tmp_patterns)
    assert len(lib.get_patterns()) == 1
    assert lib.get_patterns()[0]["id"] == "test_001"


def test_protected_terms_merge(tmp_patterns):
    lib = PatternLibrary.load(tmp_patterns)
    terms = lib.get_protected_terms()
    assert "测试术语" in terms
    assert "用户术语" in terms


def test_add_learned_pattern(tmp_patterns):
    lib = PatternLibrary.load(tmp_patterns)
    lib.add_learned_pattern({"id": "learned_001", "type": "cliche", "match": "新词", "replacements": ["新替换"], "platform_weight": {"cnki": 0.5}})
    lib.save_learned()

    lib2 = PatternLibrary.load(tmp_patterns)
    assert any(p["id"] == "learned_001" for p in lib2.get_patterns())


def test_load_missing_file(tmp_path):
    """缺少某个文件时不应崩溃。"""
    (tmp_path / "builtin.json").write_text('{"patterns": [], "protected_terms": []}', encoding="utf-8")
    lib = PatternLibrary.load(tmp_path)
    assert len(lib.get_patterns()) == 0


def test_load_corrupted_file(tmp_path):
    """损坏的文件应被跳过。"""
    (tmp_path / "builtin.json").write_text("not json", encoding="utf-8")
    (tmp_path / "user.json").write_text('{"patterns": [], "protected_terms": []}', encoding="utf-8")
    lib = PatternLibrary.load(tmp_path)
    assert len(lib.get_patterns()) == 0

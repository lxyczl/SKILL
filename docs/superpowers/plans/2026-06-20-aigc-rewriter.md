# 中文论文降 AIGC 率 Skill 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一个 Claude Code skill，通过 Python 分析引擎量化 AIGC 风险 + Claude 改写 + 模式库规则驱动，降低中文学术论文的 AIGC 检测率。

**Architecture:** Python 脚本负责文本分析（5 个维度的风险评分），Claude 负责改写执行，JSON 规则文件作为模式库。Skill 主控层编排三者，支持交互/半自动/全自动三种模式。

**Tech Stack:** Python 3.10+、jieba、Claude Code skill 框架

## Global Constraints

- 第一版仅支持 `.txt` 和 `.md` 格式
- 目标平台：知网（主要）、维普、万方、PaperPass
- 目标学科：建筑/工程方向（主要），兼顾通用学术
- 公式、表格、参考文献、图表标题一律跳过，只处理正文文字
- 单段处理失败不阻塞全文流程
- 模式库自动学习需跨会话持久化（写盘 + 加载）

---

## File Structure

```
E:\WorkSpace\Claude Code/
├── .claude/
│   └── skills/
│       └── rewrite/
│           ├── SKILL.md                    # Skill 定义（主控层）
│           ├── analyze.py                  # 分析引擎 CLI 入口
│           ├── analyzer/
│           │   ├── __init__.py
│           │   ├── paragraphs.py           # 段落切分 + 章节识别
│           │   ├── syntax.py               # 句法特征分析
│           │   ├── vocabulary.py            # 词汇分布分析
│           │   ├── structure.py             # 结构规律分析
│           │   ├── ai_traces.py             # AI 痕迹检测
│           │   ├── chinese.py               # 中文特化分析
│           │   └── scorer.py                # 风险评分 + 优先级排序
│           ├── patterns/
│           │   ├── builtin.json             # 内置规则（200+ 条）
│           │   ├── user.json                # 用户规则（首次运行创建）
│           │   └── learned.json             # 自动积累规则
│           └── utils/
│               ├── __init__.py
│               ├── text.py                  # 文本处理工具
│               └── io.py                    # 文件 I/O 工具
├── tests/
│   ├── test_paragraphs.py
│   ├── test_syntax.py
│   ├── test_vocabulary.py
│   ├── test_structure.py
│   ├── test_ai_traces.py
│   ├── test_chinese.py
│   ├── test_scorer.py
│   └── test_integration.py
```

---

### Task 1: 项目结构与依赖

**Files:**
- Create: `pyproject.toml`
- Create: `.claude/skills/rewrite/SKILL.md`（骨架）
- Create: `.claude/skills/rewrite/analyze.py`（骨架）
- Create: `.claude/skills/rewrite/analyzer/__init__.py`
- Create: `.claude/skills/rewrite/utils/__init__.py`
- Create: `.claude/skills/rewrite/utils/text.py`
- Create: `.claude/skills/rewrite/utils/io.py`

**Interfaces:**
- Produces: `analyze.py` CLI 入口，后续 Task 填充实现

- [ ] **Step 1: 创建 pyproject.toml**

```toml
[project]
name = "aigc-rewriter"
version = "0.1.0"
description = "中文论文降 AIGC 率分析引擎"
requires-python = ">=3.10"
dependencies = [
    "jieba>=0.42.1",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
]

[project.scripts]
aigc-analyze = "analyze:main"
```

- [ ] **Step 2: 创建目录结构**

```bash
mkdir -p .claude/skills/rewrite/analyzer
mkdir -p .claude/skills/rewrite/patterns
mkdir -p .claude/skills/rewrite/utils
mkdir -p tests
```

- [ ] **Step 3: 创建 SKILL.md 骨架**

```markdown
---
name: rewrite
description: 中文论文降 AIGC 率处理工具
---

# 降 AIGC 率 Skill

（后续 Task 6 填充完整内容）
```

- [ ] **Step 4: 创建 analyze.py 骨架**

```python
"""AIGC 风险分析引擎 CLI 入口。"""

import argparse
import json
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="分析文本的 AIGC 风险")
    parser.add_argument("input", help="输入文件路径 (.txt 或 .md)")
    parser.add_argument("--output", "-o", help="输出 JSON 文件路径")
    parser.add_argument("--threshold", "-t", type=float, default=0.3, help="风险阈值")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[错误] 文件不存在: {input_path}", file=sys.stderr)
        sys.exit(1)
    if input_path.suffix not in (".txt", ".md"):
        print(f"[错误] 不支持的格式: {input_path.suffix}，仅支持 .txt 和 .md", file=sys.stderr)
        sys.exit(1)

    text = input_path.read_text(encoding="utf-8")
    if not text.strip():
        print("[错误] 文件内容为空", file=sys.stderr)
        sys.exit(1)

    # 后续 Task 填充分析逻辑
    result = {"overall_risk": 0.0, "paragraphs": []}

    if args.output:
        Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: 创建 utils/text.py**

```python
"""文本处理工具函数。"""

import re
from typing import List


def split_sentences(text: str) -> List[str]:
    """按中文标点分句。"""
    # 匹配句号、问号、感叹号、分号（中英文）
    pattern = r'([^。！？；.!?;]+[。！？；.!?;]?)'
    sentences = re.findall(pattern, text)
    return [s.strip() for s in sentences if s.strip()]


def count_chinese_chars(text: str) -> int:
    """统计中文字符数。"""
    return len(re.findall(r'[一-鿿]', text))


def is_heading_line(line: str, is_markdown: bool) -> bool:
    """判断是否为标题行。"""
    if is_markdown:
        return line.strip().startswith("#")
    return len(line.strip()) < 30 and line.strip() != ""
```

- [ ] **Step 6: 创建 utils/io.py**

```python
"""文件 I/O 工具。"""

import json
from pathlib import Path
from typing import Any, Optional


def read_text_file(path: Path) -> str:
    """读取文本文件，自动检测编码。"""
    return path.read_text(encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    """写入 JSON 文件。"""
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_json(path: Path) -> Optional[dict]:
    """加载 JSON 文件，不存在或损坏返回 None。"""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
```

- [ ] **Step 7: 安装依赖并验证**

```bash
pip install -e ".[dev]"
python -c "import jieba; print('jieba OK')"
python .claude/skills/rewrite/analyze.py --help
```

Expected: 显示 help 信息，无报错。

- [ ] **Step 8: 提交**

```bash
git add pyproject.toml .claude/skills/rewrite/ tests/
git commit -m "feat: 项目结构与依赖初始化"
```

---

### Task 2: 模式库 — 规则文件与加载器

**Files:**
- Create: `.claude/skills/rewrite/patterns/builtin.json`
- Create: `.claude/skills/rewrite/patterns/user.json`（示例）
- Create: `.claude/skills/rewrite/patterns/learned.json`（空模板）
- Create: `.claude/skills/rewrite/analyzer/patterns.py`
- Create: `tests/test_patterns.py`

**Interfaces:**
- Produces: `PatternLibrary` 类
  - `load(base_dir: Path) -> PatternLibrary`
  - `get_patterns() -> List[dict]`
  - `get_protected_terms() -> Set[str]`
  - `add_learned_pattern(pattern: dict) -> None`
  - `save_learned() -> None`

- [ ] **Step 1: 创建 builtin.json（精简版，含 30 条核心规则）**

```json
{
  "patterns": [
    {"id": "cliche_001", "type": "cliche", "match": "综上所述", "replacements": ["从整体来看", "回到前文的问题", "总结来看"], "platform_weight": {"cnki": 0.9, "vip": 0.7, "wanfang": 0.7, "paperpass": 0.6}},
    {"id": "cliche_002", "type": "cliche", "match": "值得注意的是", "replacements": ["需要关注的是", "一个关键点是", "引人注意的是"], "platform_weight": {"cnki": 0.8, "vip": 0.7, "wanfang": 0.6, "paperpass": 0.5}},
    {"id": "cliche_003", "type": "cliche", "match": "具有重要意义", "replacements": ["不容忽视", "值得深入探讨", "有实质性影响"], "platform_weight": {"cnki": 0.8, "vip": 0.7, "wanfang": 0.6, "paperpass": 0.5}},
    {"id": "cliche_004", "type": "cliche", "match": "近年来", "replacements": ["最近一段时间", "过去几年里", "这一阶段"], "platform_weight": {"cnki": 0.6, "vip": 0.5, "wanfang": 0.5, "paperpass": 0.4}},
    {"id": "cliche_005", "type": "cliche", "match": "引起了广泛关注", "replacements": ["受到学界重视", "成为研究热点", "引发了持续讨论"], "platform_weight": {"cnki": 0.8, "vip": 0.7, "wanfang": 0.6, "paperpass": 0.5}},
    {"id": "cliche_006", "type": "cliche", "match": "在此基础上", "replacements": ["顺着这条线索", "以此为起点", "在前述讨论的基础上"], "platform_weight": {"cnki": 0.7, "vip": 0.6, "wanfang": 0.5, "paperpass": 0.5}},
    {"id": "cliche_007", "type": "cliche", "match": "如图所示", "replacements": ["从图中可以看出", "图中呈现了", "观察图可以发现"], "platform_weight": {"cnki": 0.5, "vip": 0.4, "wanfang": 0.4, "paperpass": 0.3}},
    {"id": "cliche_008", "type": "cliche", "match": "本文提出了一种", "replacements": ["本文的方案是", "本文尝试从…角度出发", "本文的核心思路是"], "platform_weight": {"cnki": 0.7, "vip": 0.6, "wanfang": 0.5, "paperpass": 0.5}},
    {"id": "cliche_009", "type": "cliche", "match": "实验结果表明", "replacements": ["从实验数据来看", "实验指向的结论是", "数据显示"], "platform_weight": {"cnki": 0.7, "vip": 0.6, "wanfang": 0.5, "paperpass": 0.5}},
    {"id": "cliche_010", "type": "cliche", "match": "取得了较好的效果", "replacements": ["表现令人满意", "达到了预期目标", "结果较为理想"], "platform_weight": {"cnki": 0.8, "vip": 0.7, "wanfang": 0.6, "paperpass": 0.5}},
    {"id": "syntax_001", "type": "sentence_pattern", "match": "通过.*方法.*实现了.*目标", "replacements": ["借助…方法，最终达成了…目标", "采用…方法后，…目标得以实现"], "platform_weight": {"cnki": 0.7, "vip": 0.6, "wanfang": 0.5, "paperpass": 0.5}},
    {"id": "syntax_002", "type": "sentence_pattern", "match": "不仅.*而且.*还", "replacements": ["除了…之外，同时也…", "一方面…，另一方面…"], "platform_weight": {"cnki": 0.6, "vip": 0.5, "wanfang": 0.5, "paperpass": 0.4}},
    {"id": "syntax_003", "type": "sentence_pattern", "match": "随着.*的不断发展", "replacements": ["在…持续推进的背景下", "伴随…的逐步成熟", "…的演进带来了"], "platform_weight": {"cnki": 0.7, "vip": 0.6, "wanfang": 0.5, "paperpass": 0.5}},
    {"id": "conn_001", "type": "connector", "match": "因此", "replacements": ["由此", "这导致了", "在这一前提下"], "platform_weight": {"cnki": 0.4, "vip": 0.3, "wanfang": 0.3, "paperpass": 0.2}},
    {"id": "conn_002", "type": "connector", "match": "然而", "replacements": ["不过", "但实际情况是", "与此相反的是"], "platform_weight": {"cnki": 0.4, "vip": 0.3, "wanfang": 0.3, "paperpass": 0.2}},
    {"id": "conn_003", "type": "connector", "match": "此外", "replacements": ["另一个方面是", "与此同时", "还有一点值得关注"], "platform_weight": {"cnki": 0.4, "vip": 0.3, "wanfang": 0.3, "paperpass": 0.2}},
    {"id": "conn_004", "type": "connector", "match": "同时", "replacements": ["在这一过程中", "伴随着", "与此并行的是"], "platform_weight": {"cnki": 0.3, "vip": 0.2, "wanfang": 0.2, "paperpass": 0.2}},
    {"id": "conn_005", "type": "connector", "match": "总之", "replacements": ["回到核心问题", "概括来说", "从整体上看"], "platform_weight": {"cnki": 0.5, "vip": 0.4, "wanfang": 0.4, "paperpass": 0.3}},
    {"id": "chinese_001", "type": "chinese_pattern", "match": "被.*所.*", "replacements": ["受到…的…", "在…下…"], "platform_weight": {"cnki": 0.6, "vip": 0.5, "wanfang": 0.4, "paperpass": 0.4}},
    {"id": "chinese_002", "type": "chinese_pattern", "match": "对.*进行了.*", "replacements": ["针对…展开了…", "在…方面做了…", "着手…"], "platform_weight": {"cnki": 0.6, "vip": 0.5, "wanfang": 0.4, "paperpass": 0.4}},
    {"id": "idiom_001", "type": "idiom", "match": "举足轻重", "replacements": ["不可忽视", "有分量", "至关重要"], "platform_weight": {"cnki": 0.5, "vip": 0.4, "wanfang": 0.4, "paperpass": 0.3}},
    {"id": "idiom_002", "type": "idiom", "match": "不可否认", "replacements": ["需要承认的是", "客观来看", "事实上"], "platform_weight": {"cnki": 0.5, "vip": 0.4, "wanfang": 0.4, "paperpass": 0.3}},
    {"id": "idiom_003", "type": "idiom", "match": "日益增长", "replacements": ["持续上升", "逐步扩大", "越来越明显"], "platform_weight": {"cnki": 0.5, "vip": 0.4, "wanfang": 0.4, "paperpass": 0.3}},
    {"id": "idiom_004", "type": "idiom", "match": "层出不穷", "replacements": ["接连出现", "不断涌现", "一个接一个"], "platform_weight": {"cnki": 0.5, "vip": 0.4, "wanfang": 0.4, "paperpass": 0.3}},
    {"id": "idiom_005", "type": "idiom", "match": "息息相关", "replacements": ["密切关联", "有直接联系", "相互交织"], "platform_weight": {"cnki": 0.5, "vip": 0.4, "wanfang": 0.4, "paperpass": 0.3}},
    {"id": "passive_001", "type": "passive", "match": "被广泛应用于", "replacements": ["在…中普遍采用", "大量出现在", "已成为…的常用手段"], "platform_weight": {"cnki": 0.6, "vip": 0.5, "wanfang": 0.4, "paperpass": 0.4}},
    {"id": "passive_002", "type": "passive", "match": "被认为", "replacements": ["学界的看法是", "通常的理解是", "多数研究支持"], "platform_weight": {"cnki": 0.5, "vip": 0.4, "wanfang": 0.4, "paperpass": 0.3}},
    {"id": "formal_001", "type": "formal", "match": "基于上述分析", "replacements": ["从前面的讨论来看", "综合以上几点", "顺着这条思路"], "platform_weight": {"cnki": 0.7, "vip": 0.6, "wanfang": 0.5, "paperpass": 0.5}},
    {"id": "formal_002", "type": "formal", "match": "针对这一问题", "replacements": ["面对这个挑战", "在这个问题上", "为了解决这一难点"], "platform_weight": {"cnki": 0.6, "vip": 0.5, "wanfang": 0.4, "paperpass": 0.4}},
    {"id": "formal_003", "type": "formal", "match": "研究表明", "replacements": ["已有研究指出", "从现有文献来看", "多项研究确认"], "platform_weight": {"cnki": 0.5, "vip": 0.4, "wanfang": 0.4, "paperpass": 0.3}}
  ],
  "protected_terms": ["建筑能耗模拟", "围护结构", "DeST", "EnergyPlus", "深度学习", "卷积神经网络", "Transformer", "注意力机制"]
}
```

- [ ] **Step 2: 创建 user.json 示例**

```json
{
  "patterns": [],
  "protected_terms": []
}
```

- [ ] **Step 3: 创建 learned.json 空模板**

```json
{
  "patterns": [],
  "protected_terms": []
}
```

- [ ] **Step 4: 编写 test_patterns.py**

```python
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
```

- [ ] **Step 5: 实现 analyzer/patterns.py**

```python
"""模式库加载器。"""

import json
from pathlib import Path
from typing import List, Set


class PatternLibrary:
    def __init__(self):
        self._patterns: List[dict] = []
        self._protected_terms: Set[str] = set()
        self._learned_path: Path = None
        self._learned_data: dict = {"patterns": [], "protected_terms": []}

    @classmethod
    def load(cls, base_dir: Path) -> "PatternLibrary":
        lib = cls()
        lib._learned_path = base_dir / "learned.json"

        for filename in ("builtin.json", "user.json", "learned.json"):
            filepath = base_dir / filename
            data = cls._safe_load(filepath)
            if data:
                lib._patterns.extend(data.get("patterns", []))
                lib._protected_terms.update(data.get("protected_terms", []))
                if filename == "learned.json":
                    lib._learned_data = data

        return lib

    @staticmethod
    def _safe_load(path: Path) -> dict | None:
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None

    def get_patterns(self) -> List[dict]:
        return list(self._patterns)

    def get_protected_terms(self) -> Set[str]:
        return set(self._protected_terms)

    def add_learned_pattern(self, pattern: dict) -> None:
        self._patterns.append(pattern)
        self._learned_data["patterns"].append(pattern)

    def save_learned(self) -> None:
        if self._learned_path:
            self._learned_path.write_text(
                json.dumps(self._learned_data, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
```

- [ ] **Step 6: 运行测试**

```bash
python -m pytest tests/test_patterns.py -v
```

Expected: 5 tests PASS。

- [ ] **Step 7: 提交**

```bash
git add .claude/skills/rewrite/patterns/ .claude/skills/rewrite/analyzer/patterns.py tests/test_patterns.py
git commit -m "feat: 模式库规则文件与加载器"
```

---

### Task 3: 段落切分与章节识别

**Files:**
- Create: `.claude/skills/rewrite/analyzer/paragraphs.py`
- Create: `tests/test_paragraphs.py`

**Interfaces:**
- Produces: `split_paragraphs(text: str, is_markdown: bool) -> List[dict]`
  - 返回: `[{"index": 0, "text": "...", "start": 0, "end": 50, "char_count": 50, "section_type": "abstract"}]`
- Produces: `detect_section(heading_text: str) -> str`

- [ ] **Step 1: 编写 test_paragraphs.py**

```python
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
```

- [ ] **Step 2: 实现 analyzer/paragraphs.py**

```python
"""段落切分与章节识别。"""

import re
from typing import List


SECTION_KEYWORDS = {
    "abstract": ["摘要", "abstract", "提要"],
    "introduction": ["引言", "绪论", "introduction", "问题提出"],
    "method": ["方法", "方法论", "实验", "method", "methodology", "实验设计", "模型构建"],
    "results": ["结果", "实验结果", "results", "数据分析"],
    "discussion": ["讨论", "分析与讨论", "discussion", "结果分析"],
    "conclusion": ["结论", "总结", "conclusion", "结语"],
    "related_work": ["相关工作", "文献综述", "related work", "研究现状"],
}


def detect_section(heading_text: str) -> str:
    """识别章节类型。"""
    cleaned = re.sub(r'^#+\s*', '', heading_text.strip()).lower()
    for section_type, keywords in SECTION_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in cleaned:
                return section_type
    return "body"


def split_paragraphs(text: str, is_markdown: bool) -> List[dict]:
    """将文本切分为段落，附带章节信息。"""
    if not text.strip():
        return []

    lines = text.split('\n')
    paragraphs = []
    current_section = "body"
    current_text_lines = []
    pos = 0

    for line in lines:
        stripped = line.strip()

        # 检测标题
        if is_markdown and stripped.startswith('#'):
            # 先保存当前积累的段落
            if current_text_lines:
                para_text = '\n'.join(current_text_lines).strip()
                if para_text:
                    paragraphs.append(_make_para(len(paragraphs), para_text, pos, current_section))
                    pos += len(para_text) + 1
                current_text_lines = []
            current_section = detect_section(stripped)
            continue

        # 空行 = 段落分隔
        if not stripped:
            if current_text_lines:
                para_text = '\n'.join(current_text_lines).strip()
                if para_text:
                    paragraphs.append(_make_para(len(paragraphs), para_text, pos, current_section))
                    pos += len(para_text) + 1
                current_text_lines = []
            continue

        current_text_lines.append(stripped)

    # 最后一段
    if current_text_lines:
        para_text = '\n'.join(current_text_lines).strip()
        if para_text:
            paragraphs.append(_make_para(len(paragraphs), para_text, pos, current_section))

    # 处理超长段落拆分
    result = []
    for para in paragraphs:
        if para["char_count"] > 2000:
            result.extend(_split_long_paragraph(para))
        else:
            result.append(para)

    # 重新编号
    for i, p in enumerate(result):
        p["index"] = i

    return result


def _make_para(index: int, text: str, start: int, section_type: str) -> dict:
    return {
        "index": index,
        "text": text,
        "start": start,
        "start + len(text)": start + len(text),
        "char_count": len(text),
        "section_type": section_type,
    }


def _split_long_paragraph(para: dict) -> List[dict]:
    """按句号/分号拆分超长段落。"""
    text = para["text"]
    pattern = r'([^。！？；.!?;]+[。！？；.!?;]?)'
    sentences = [s.strip() for s in re.findall(pattern, text) if s.strip()]

    chunks = []
    current_chunk = []
    current_len = 0

    for sent in sentences:
        current_chunk.append(sent)
        current_len += len(sent)
        if current_len >= 1500:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_len = 0

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    result = []
    for i, chunk in enumerate(chunks):
        result.append({
            "index": para["index"] + i,
            "text": chunk,
            "start": para["start"],
            "char_count": len(chunk),
            "section_type": para["section_type"],
            "is_sub_chunk": True,
        })

    return result
```

- [ ] **Step 3: 运行测试**

```bash
python -m pytest tests/test_paragraphs.py -v
```

Expected: 所有测试 PASS。

- [ ] **Step 4: 提交**

```bash
git add .claude/skills/rewrite/analyzer/paragraphs.py tests/test_paragraphs.py
git commit -m "feat: 段落切分与章节识别"
```

---

### Task 4: 五个分析维度

**Files:**
- Create: `.claude/skills/rewrite/analyzer/syntax.py`
- Create: `.claude/skills/rewrite/analyzer/vocabulary.py`
- Create: `.claude/skills/rewrite/analyzer/structure.py`
- Create: `.claude/skills/rewrite/analyzer/ai_traces.py`
- Create: `.claude/skills/rewrite/analyzer/chinese.py`
- Create: `tests/test_syntax.py`
- Create: `tests/test_vocabulary.py`
- Create: `tests/test_structure.py`
- Create: `tests/test_ai_traces.py`
- Create: `tests/test_chinese.py`

**Interfaces:**
- Produces: `analyze_syntax(text: str) -> dict` — 返回 `{"score": float, "issues": list}`
- Produces: `analyze_vocabulary(text: str, patterns: list) -> dict`
- Produces: `analyze_structure(paragraphs: list) -> dict`
- Produces: `analyze_ai_traces(text: str) -> dict`
- Produces: `analyze_chinese(text: str) -> dict`

- [ ] **Step 1: 实现 analyzer/syntax.py**

```python
"""句法特征分析维度。"""

import re
import statistics
from typing import List
from utils.text import split_sentences


def analyze_syntax(text: str) -> dict:
    """分析句法特征，返回风险分和问题列表。"""
    sentences = split_sentences(text)
    if len(sentences) < 2:
        return {"score": 0.0, "issues": []}

    issues = []

    # 1. 句长方差 — 过于均匀 = 高风险
    lengths = [len(s) for s in sentences]
    if len(lengths) >= 3:
        try:
            cv = statistics.stdev(lengths) / statistics.mean(lengths) if statistics.mean(lengths) > 0 else 0
        except statistics.StatisticsError:
            cv = 0
        # 变异系数 < 0.3 表示句长过于均匀
        if cv < 0.3:
            issues.append({"type": "uniform_sentence_length", "detail": f"句长变异系数 {cv:.2f}，过于均匀"})

    # 2. 并列结构频率
    parallel_markers = len(re.findall(r'[，,].*[，,].*[，,]', text))
    if parallel_markers > len(sentences) * 0.5:
        issues.append({"type": "excessive_parallelism", "detail": f"并列结构过多: {parallel_markers} 处"})

    # 3. 从句嵌套深度 — 简单估算
    deep_nested = len(re.findall(r'的.*的.*的.*的', text))
    if deep_nested > 0:
        issues.append({"type": "deep_nesting", "detail": f"检测到 {deep_nested} 处深层嵌套"})

    score = _calculate_score(issues, len(sentences))
    return {"score": score, "issues": issues}


def _calculate_score(issues: list, sentence_count: int) -> float:
    base = 0.0
    for issue in issues:
        if issue["type"] == "uniform_sentence_length":
            base += 0.3
        elif issue["type"] == "excessive_parallelism":
            base += 0.2
        elif issue["type"] == "deep_nesting":
            base += 0.15
    return min(base, 1.0)
```

- [ ] **Step 2: 实现 analyzer/vocabulary.py**

```python
"""词汇分布分析维度。"""

import re
from typing import List


# AI 高频连接词
AI_CONNECTORS = [
    "因此", "然而", "此外", "同时", "总之", "另外", "并且",
    "进而", "随后", "首先", "其次", "最后", "综上", "故而",
]

# AI 套话
AI_CLICHES = [
    "综上所述", "值得注意的是", "具有重要意义", "引起了广泛关注",
    "取得了较好的效果", "在此基础上", "本文提出了一种",
    "实验结果表明", "近年来", "如图所示", "如表所示",
]


def analyze_vocabulary(text: str, patterns: list) -> dict:
    """分析词汇分布，返回风险分和问题列表。"""
    issues = []

    # 1. TTR (Type-Token Ratio) — 词汇丰富度
    words = list(text)  # 中文按字计算
    if len(words) > 10:
        ttr = len(set(words)) / len(words)
        if ttr < 0.3:
            issues.append({"type": "low_ttr", "detail": f"词汇丰富度 TTR={ttr:.2f}，偏低"})

    # 2. 连接词频率
    conn_count = sum(text.count(c) for c in AI_CONNECTORS)
    sentence_count = len(re.split(r'[。！？；.!?;]', text))
    if sentence_count > 0 and conn_count / sentence_count > 0.5:
        issues.append({"type": "connector_overuse", "detail": f"连接词频率 {conn_count}/{sentence_count}，过高"})

    # 3. 套话检测（结合模式库）
    cliche_matches = []
    for pattern in patterns:
        if pattern.get("type") in ("cliche", "formal", "connector"):
            if pattern["match"] in text:
                cliche_matches.append(pattern["match"])

    # 内置套话检测
    for cliche in AI_CLICHES:
        if cliche in text and cliche not in cliche_matches:
            cliche_matches.append(cliche)

    if cliche_matches:
        issues.append({"type": "cliche_detected", "detail": f"检测到套话: {', '.join(cliche_matches[:5])}"})

    score = _calculate_score(issues)
    return {"score": score, "issues": issues}


def _calculate_score(issues: list) -> float:
    base = 0.0
    for issue in issues:
        if issue["type"] == "low_ttr":
            base += 0.2
        elif issue["type"] == "connector_overuse":
            base += 0.25
        elif issue["type"] == "cliche_detected":
            base += 0.3
    return min(base, 1.0)
```

- [ ] **Step 3: 实现 analyzer/structure.py**

```python
"""结构规律分析维度。"""

import statistics
from typing import List


def analyze_structure(paragraphs: List[dict]) -> dict:
    """分析段落结构规律，返回风险分和问题列表。"""
    if len(paragraphs) < 3:
        return {"score": 0.0, "issues": []}

    issues = []

    # 1. 段落长度方差 — 过于均匀
    lengths = [p["char_count"] for p in paragraphs]
    if len(lengths) >= 3:
        try:
            cv = statistics.stdev(lengths) / statistics.mean(lengths) if statistics.mean(lengths) > 0 else 0
        except statistics.StatisticsError:
            cv = 0
        if cv < 0.25:
            issues.append({"type": "uniform_para_length", "detail": f"段落长度变异系数 {cv:.2f}，段落等长"})

    # 2. 段首句模式 — 每段首句结构相同
    first_sentences = []
    for p in paragraphs:
        text = p["text"]
        first_sent = text[:min(20, len(text))]
        first_sentences.append(first_sent)

    # 检查是否有重复的开头模式
    if len(first_sentences) >= 3:
        # 简单检查：前几个字是否相同
        prefixes = [s[:5] for s in first_sentences if len(s) >= 5]
        if len(prefixes) >= 3:
            from collections import Counter
            most_common = Counter(prefixes).most_common(1)
            if most_common and most_common[0][1] >= 3:
                issues.append({"type": "uniform_para_start", "detail": f"段首句模式重复: '{most_common[0][0]}...' 出现 {most_common[0][1]} 次"})

    score = _calculate_score(issues)
    return {"score": score, "issues": issues}


def _calculate_score(issues: list) -> float:
    base = 0.0
    for issue in issues:
        if issue["type"] == "uniform_para_length":
            base += 0.3
        elif issue["type"] == "uniform_para_start":
            base += 0.3
    return min(base, 1.0)
```

- [ ] **Step 4: 实现 analyzer/ai_traces.py**

```python
"""AI 痕迹检测维度。"""

import re
from utils.text import split_sentences


def analyze_ai_traces(text: str) -> dict:
    """检测 AI 生成痕迹，返回风险分和问题列表。"""
    issues = []
    sentences = split_sentences(text)

    # 1. 流畅度异常 — 缺乏口语化断句
    # AI 文本通常句句完整，缺少省略号、破折号等不完整标记
    informal_markers = len(re.findall(r'[…—\-（(]', text))
    if len(sentences) > 5 and informal_markers / len(sentences) < 0.1:
        issues.append({"type": "too_fluent", "detail": f"口语化标记极少 ({informal_markers}/{len(sentences)})，行文过于工整"})

    # 2. 突发性 (Burstiness) — 句长变化是否自然
    if len(sentences) >= 5:
        lengths = [len(s) for s in sentences]
        # 检查是否有连续相似长度的句子
        consecutive_similar = 0
        max_consecutive = 0
        for i in range(1, len(lengths)):
            if abs(lengths[i] - lengths[i-1]) < 5:
                consecutive_similar += 1
                max_consecutive = max(max_consecutive, consecutive_similar)
            else:
                consecutive_similar = 0

        if max_consecutive >= 3:
            issues.append({"type": "low_burstiness", "detail": f"连续 {max_consecutive + 1} 句长度相近，缺乏变化"})

    # 3. 无个人化表达 — 缺少"笔者""我们""本文"等主观标记
    personal_markers = len(re.findall(r'笔者|我们认为|我们发现|我注意到|从我的角度来看', text))
    if len(sentences) > 8 and personal_markers == 0:
        issues.append({"type": "no_personal_voice", "detail": "缺少个人化表达标记"})

    score = _calculate_score(issues)
    return {"score": score, "issues": issues}


def _calculate_score(issues: list) -> float:
    base = 0.0
    for issue in issues:
        if issue["type"] == "too_fluent":
            base += 0.2
        elif issue["type"] == "low_burstiness":
            base += 0.25
        elif issue["type"] == "no_personal_voice":
            base += 0.2
    return min(base, 1.0)
```

- [ ] **Step 5: 实现 analyzer/chinese.py**

```python
"""中文特化分析维度。"""

import re


def analyze_chinese(text: str) -> dict:
    """分析中文 AIGC 特征，返回风险分和问题列表。"""
    issues = []
    char_count = len(text)

    if char_count < 50:
        return {"score": 0.0, "issues": []}

    # 1. "了"字集中度
    le_count = text.count("了")
    le_density = le_count / char_count
    if le_density > 0.03:  # 每 100 字超过 3 个"了"
        issues.append({"type": "excessive_le", "detail": f"'了'字密度 {le_density:.3f} ({le_count} 次/{char_count} 字)，偏高"})

    # 2. "的"字冗余嵌套
    de_nesting = len(re.findall(r'的[^。，！？；\n]{0,8}的[^。，！？；\n]{0,8}的', text))
    if de_nesting > 2:
        issues.append({"type": "de_nesting", "detail": f"检测到 {de_nesting} 处'的'字三层以上嵌套"})

    # 3. 四字成语密度
    idiom_pattern = r'[一-鿿]{4}'
    four_char_groups = re.findall(idiom_pattern, text)
    # 简化：用常见成语后缀检测
    idiom_suffixes = ["不可", "有所", "日益", "层出不穷", "举足轻重", "息息相关", "不可否认", "不容忽视"]
    idiom_count = sum(1 for g in four_char_groups if any(s in g for s in idiom_suffixes))
    if len(four_char_groups) > 0 and idiom_count / len(four_char_groups) > 0.1:
        issues.append({"type": "idiom_overuse", "detail": f"四字表达密度偏高: {idiom_count}/{len(four_char_groups)}"})

    # 4. "被…所…"频率
    bei_suo = len(re.findall(r'被[^。，！？]{0,20}所', text))
    if bei_suo > 2:
        issues.append({"type": "bei_suo_pattern", "detail": f"'被…所…'句式出现 {bei_suo} 次"})

    score = _calculate_score(issues)
    return {"score": score, "issues": issues}


def _calculate_score(issues: list) -> float:
    base = 0.0
    for issue in issues:
        if issue["type"] == "excessive_le":
            base += 0.2
        elif issue["type"] == "de_nesting":
            base += 0.2
        elif issue["type"] == "idiom_overuse":
            base += 0.2
        elif issue["type"] == "bei_suo_pattern":
            base += 0.15
    return min(base, 1.0)
```

- [ ] **Step 6: 编写各维度测试**

`tests/test_syntax.py`:

```python
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
```

`tests/test_vocabulary.py`:

```python
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
```

`tests/test_structure.py`:

```python
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
```

`tests/test_ai_traces.py`:

```python
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
```

`tests/test_chinese.py`:

```python
import pytest
from analyzer.chinese import analyze_chinese

def test_excessive_le():
    text = "这个方法被证明了是有效的。实验验证了这个结论。我们观察了数据变化了。结果表明了方法的优势了。"
    result = analyze_chinese(text)
    assert result["score"] > 0

def test_de_nesting():
    text = "基于深度学习的方法的性能的提升的幅度超过了预期。"
    result = analyze_chinese(text)
    assert any(i["type"] == "de_nesting" for i in result["issues"])
```

- [ ] **Step 7: 运行所有测试**

```bash
python -m pytest tests/test_syntax.py tests/test_vocabulary.py tests/test_structure.py tests/test_ai_traces.py tests/test_chinese.py -v
```

Expected: 所有测试 PASS。

- [ ] **Step 8: 提交**

```bash
git add .claude/skills/rewrite/analyzer/syntax.py .claude/skills/rewrite/analyzer/vocabulary.py .claude/skills/rewrite/analyzer/structure.py .claude/skills/rewrite/analyzer/ai_traces.py .claude/skills/rewrite/analyzer/chinese.py tests/test_syntax.py tests/test_vocabulary.py tests/test_structure.py tests/test_ai_traces.py tests/test_chinese.py
git commit -m "feat: 五个分析维度实现"
```

---

### Task 5: 风险评分与优先级排序

**Files:**
- Create: `.claude/skills/rewrite/analyzer/scorer.py`
- Create: `tests/test_scorer.py`

**Interfaces:**
- Produces: `score_paragraph(text: str, section_type: str, patterns: list) -> dict`
  - 返回: `{"risk": float, "priority": float, "section_type": str, "issues": list, "suggestion": str}`
- Produces: `compute_overall_risk(paragraph_scores: list) -> float`

- [ ] **Step 1: 编写 test_scorer.py**

```python
import pytest
from analyzer.scorer import score_paragraph, compute_overall_risk

def test_high_risk_paragraph():
    text = "综上所述，本文提出了一种基于深度学习的方法。该方法具有重要意义，取得了较好的效果。实验结果表明，该方法不仅性能优越，而且适用范围广泛。"
    result = score_paragraph(text, "body", [])
    assert result["risk"] > 0.5
    assert result["priority"] > 0

def test_low_risk_paragraph():
    text = "笔者在搭建实验环境时遇到了一个意外——服务器的 GPU 内存不够。最后换了 batch size 才解决。"
    result = score_paragraph(text, "body", [])
    assert result["risk"] < 0.3

def test_priority_ranking():
    text = "综上所述，实验结果表明该方法有效。"
    body = score_paragraph(text, "body", [])
    discussion = score_paragraph(text, "discussion", [])
    assert discussion["priority"] > body["priority"]

def test_overall_risk():
    scores = [
        {"risk": 0.8, "section_type": "body"},
        {"risk": 0.2, "section_type": "body"},
    ]
    avg = compute_overall_risk(scores)
    assert 0.4 < avg < 0.6
```

- [ ] **Step 2: 实现 analyzer/scorer.py**

```python
"""风险评分与优先级排序。"""

from typing import List
from analyzer.syntax import analyze_syntax
from analyzer.vocabulary import analyze_vocabulary
from analyzer.structure import analyze_structure
from analyzer.ai_traces import analyze_ai_traces
from analyzer.chinese import analyze_chinese

# 章节权重 — 越高表示改写收益越大
SECTION_WEIGHTS = {
    "discussion": 1.3,
    "method": 1.2,
    "abstract": 1.1,
    "related_work": 1.0,
    "conclusion": 1.0,
    "introduction": 0.9,
    "results": 1.1,
    "body": 1.0,
}

# 章节默认阈值
SECTION_THRESHOLDS = {
    "abstract": 0.25,
    "introduction": 0.3,
    "method": 0.35,
    "results": 0.3,
    "discussion": 0.25,
    "conclusion": 0.3,
    "related_work": 0.4,
    "body": 0.3,
}


def score_paragraph(text: str, section_type: str, patterns: list) -> dict:
    """对单个段落进行综合风险评分。"""
    syntax = analyze_syntax(text)
    vocabulary = analyze_vocabulary(text, patterns)
    ai_traces = analyze_ai_traces(text)
    chinese = analyze_chinese(text)

    all_issues = []
    all_issues.extend(syntax["issues"])
    all_issues.extend(vocabulary["issues"])
    all_issues.extend(ai_traces["issues"])
    all_issues.extend(chinese["issues"])

    # 加权平均
    risk = (
        syntax["score"] * 0.2 +
        vocabulary["score"] * 0.3 +
        ai_traces["score"] * 0.25 +
        chinese["score"] * 0.25
    )
    risk = min(risk, 1.0)

    weight = SECTION_WEIGHTS.get(section_type, 1.0)
    priority = risk * weight

    return {
        "risk": round(risk, 3),
        "priority": round(priority, 3),
        "section_type": section_type,
        "issues": all_issues,
        "suggestion": _generate_suggestion(all_issues),
    }


def score_paragraphs(paragraphs: List[dict], patterns: list) -> List[dict]:
    """批量评分段落，按优先级排序。"""
    results = []
    for para in paragraphs:
        score = score_paragraph(para["text"], para["section_type"], patterns)
        score["index"] = para["index"]
        results.append(score)

    results.sort(key=lambda x: x["priority"], reverse=True)
    return results


def compute_overall_risk(paragraph_scores: List[dict]) -> float:
    """计算全文整体风险分。"""
    if not paragraph_scores:
        return 0.0
    total = sum(p["risk"] for p in paragraph_scores)
    return round(total / len(paragraph_scores), 3)


def get_threshold(section_type: str, global_threshold: float | None) -> float:
    """获取某章节的阈值。"""
    if global_threshold is not None:
        return global_threshold
    return SECTION_THRESHOLDS.get(section_type, 0.3)


def _generate_suggestion(issues: list) -> str:
    if not issues:
        return "风险较低，无需重点改写"

    suggestions = []
    types = {i["type"] for i in issues}

    if "cliche_detected" in types or "connector_overuse" in types:
        suggestions.append("替换连接词和套话")
    if "uniform_sentence_length" in types or "low_burstiness" in types:
        suggestions.append("打破句式规律")
    if "excessive_le" in types or "de_nesting" in types:
        suggestions.append("调整中文表达习惯")
    if "no_personal_voice" in types:
        suggestions.append("增加个人化表达")

    return "；".join(suggestions) if suggestions else "综合改写"
```

- [ ] **Step 3: 运行测试**

```bash
python -m pytest tests/test_scorer.py -v
```

Expected: 4 tests PASS。

- [ ] **Step 4: 提交**

```bash
git add .claude/skills/rewrite/analyzer/scorer.py tests/test_scorer.py
git commit -m "feat: 风险评分与优先级排序"
```

---

### Task 6: 改写执行层 — 上下文窗口与准确性验证

**Files:**
- Create: `.claude/skills/rewrite/rewriter/__init__.py`
- Create: `.claude/skills/rewrite/rewriter/context.py`
- Create: `.claude/skills/rewrite/rewriter/verify.py`
- Create: `.claude/skills/rewrite/rewriter/diff.py`

**Interfaces:**
- Produces: `build_context(paragraphs: list, target_index: int, window: int) -> dict`
  - 返回: `{"before": list, "after": list, "target": dict}`
- Produces: `verify_accuracy(original: str, rewritten: str, protected_terms: set) -> dict`
  - 返回: `{"is_safe": bool, "suspects": list}`
- Produces: `generate_diff_report(results: list) -> str`
  - 返回: Markdown 表格字符串

- [ ] **Step 1: 实现 rewriter/context.py**

```python
"""上下文窗口管理。"""

from typing import List


def build_context(paragraphs: List[dict], target_index: int, window: int = 2) -> dict:
    """构建改写所需的上下文窗口。"""
    before = paragraphs[max(0, target_index - window):target_index]
    after = paragraphs[target_index + 1:target_index + 1 + window]
    target = paragraphs[target_index]

    return {
        "before": [p["text"] for p in before],
        "after": [p["text"] for p in after],
        "target": target["text"],
        "target_section": target.get("section_type", "body"),
    }
```

- [ ] **Step 2: 实现 rewriter/verify.py**

```python
"""准确性验证。"""

import re
from typing import Set


def verify_accuracy(original: str, rewritten: str, protected_terms: Set[str]) -> dict:
    """验证改写结果的准确性。"""
    suspects = []

    # 1. 检查术语是否被替换
    for term in protected_terms:
        if term in original and term not in rewritten:
            suspects.append({
                "type": "term_replaced",
                "detail": f"术语 '{term}' 在改写后消失",
                "severity": "high",
            })

    # 2. 检查数值变化
    original_numbers = set(re.findall(r'\d+\.?\d*%?', original))
    rewritten_numbers = set(re.findall(r'\d+\.?\d*%?', rewritten))
    lost_numbers = original_numbers - rewritten_numbers
    if lost_numbers:
        suspects.append({
            "type": "number_changed",
            "detail": f"数值变化: {', '.join(list(lost_numbers)[:3])}",
            "severity": "high",
        })

    # 3. 检查长度变化（过于激进的改写）
    len_ratio = len(rewritten) / max(len(original), 1)
    if len_ratio < 0.5 or len_ratio > 2.0:
        suspects.append({
            "type": "length_anomaly",
            "detail": f"改写后长度变化过大: {len_ratio:.1%}",
            "severity": "medium",
        })

    is_safe = all(s["severity"] != "high" for s in suspects)

    return {
        "is_safe": is_safe,
        "suspects": suspects,
    }
```

- [ ] **Step 3: 实现 rewriter/diff.py**

```python
"""Diff 报告生成。"""

from typing import List


def generate_diff_report(results: List[dict]) -> str:
    """生成 Markdown 表格格式的 diff 报告。"""
    lines = [
        "| 段落 | 章节 | 原文风险 | 改写风险 | 原文 | 改写结果 | 可疑项 |",
        "|------|------|---------|---------|------|---------|--------|",
    ]

    for r in results:
        index = r.get("index", "?")
        section = r.get("section_type", "body")
        orig_risk = r.get("original_risk", 0)
        new_risk = r.get("rewritten_risk", 0)
        original = r.get("original_text", "")[:50]
        if len(r.get("original_text", "")) > 50:
            original += "..."
        rewritten = r.get("rewritten_text", "")[:50]
        if len(r.get("rewritten_text", "")) > 50:
            rewritten += "..."

        suspects = r.get("suspects", [])
        suspect_str = "; ".join(s["detail"] for s in suspects[:2]) if suspects else "无"

        lines.append(
            f"| §{index} | {section} | {orig_risk:.2f} | {new_risk:.2f} | {original} | {rewritten} | {suspect_str} |"
        )

    return "\n".join(lines)
```

- [ ] **Step 4: 提交**

```bash
mkdir -p .claude/skills/rewrite/rewriter
git add .claude/skills/rewrite/rewriter/
git commit -m "feat: 改写执行层（上下文窗口、准确性验证、diff 报告）"
```

---

### Task 7: Skill 主控层 — SKILL.md 与三种模式

**Files:**
- Modify: `.claude/skills/rewrite/SKILL.md`（填充完整内容）
- Modify: `.claude/skills/rewrite/analyze.py`（接入完整分析流程）

**Interfaces:**
- Consumes: Task 1-6 的所有接口
- Produces: 完整的 Skill 定义，支持三种运行模式

- [ ] **Step 1: 编写完整 SKILL.md**

```markdown
---
name: rewrite
description: 中文论文降 AIGC 率处理工具
---

# 降 AIGC 率 Skill

降低中文学术论文的 AIGC 检测率。核心思路：Python 做检测仪，Claude 做手术刀，模式库做参考手册。

## 调用方式

分析引擎脚本位于 `.claude/skills/rewrite/analyze.py`，通过 Bash 工具调用：

```bash
python .claude/skills/rewrite/analyze.py <文件路径>                    # 文件分析
python .claude/skills/rewrite/analyze.py --text "文本内容"             # 直接传入文本
python .claude/skills/rewrite/analyze.py <文件路径> --output result.json  # 输出到文件
python .claude/skills/rewrite/analyze.py <文件路径> --threshold 0.2     # 自定义阈值
```

返回 JSON 格式的分析结果，Claude 根据结果决定改写策略。

## 运行模式

### 交互模式（默认）

当用户调用 `/rewrite` 且未指定 `--file` 时进入。

1. 提示用户粘贴需要处理的段落
2. 调用 `python analyze.py --text "用户粘贴的文本"` 分析风险
3. 根据风险分选择改写策略，执行改写
4. 输出改写结果 + 风险分变化
5. 等待下一段落或指令

**交互指令：**
- `重来` / `再来一次`：对上一段重新改写
- `太激进了` / `保守点`：切换为轻度改写
- `再大胆些`：切换为深度改写
- `换风格 xxx`：切换风格（academic/narrative/technical）
- `/done`：结束会话，输出汇总

### 半自动模式

当用户指定 `--file` 但未指定 `--mode auto` 时进入。

1. 读取文件，调用分析引擎生成风险报告
2. 输出高风险段落列表（按优先级排序）
3. 用户选择要处理的段落
4. 逐段改写并输出结果

### 全自动模式

当用户指定 `--file` 和 `--mode auto` 时进入。

1. 读取文件
2. 预检：提取专业术语，展示保护名单供用户确认
3. 调用分析引擎生成风险报告
4. 按优先级逐段改写（每段独立迭代至阈值以下）
5. 准确性验证，标记可疑项
6. 用户确认后写入 `<原文件名>_rewritten.md`
7. 生成 `<原文件名>_diff.md` 和 `<原文件名>_analysis.json`

## 改写约束

1. **术语保护**：`patterns/user.json` 和 `patterns/builtin.json` 中的 `protected_terms` 不可替换
2. **含义保真**：语义不得偏离原文，允许表述方式变化，不允许内容增删
3. **学术语气**：从"AI 标准体"变成"真人学术体"，不是口语化
4. **公式/表格/引用**：跳过，只处理正文文字
5. **每段独立迭代**：各段独立判断是否达到阈值

## 改写策略

根据风险分选择策略：
- 0.3–0.5（轻度）：替换连接词、调整语序、打破并列结构
- 0.5–0.7（中度）：长短句拆合、主被动互换、插入过渡句
- 0.7+（深度）：段落重组、增加主观标记、引入非典型论证节奏

## 改写风格

- `academic`（默认）：正式学术语气
- `narrative`：叙述性风格，适合建筑学交叉方向
- `technical`：紧凑技术风格，适合 CS/AI 方向

## 章节阈值

| 章节 | 默认阈值 |
|------|---------|
| 摘要 | 0.25 |
| 引言 | 0.3 |
| 方法 | 0.35 |
| 结果 | 0.3 |
| 讨论 | 0.25 |
| 结论 | 0.3 |
| 相关工作 | 0.4 |

## 错误处理

- 单段处理失败不阻塞全文
- 改写后风险分不降反升 → 回退原文，换策略重试一次
- 分析引擎失败 → 降级为纯 prompt 改写
- 迭代 3 轮未达阈值 → 标记为"需人工处理"

## 使用方式

```
/rewrite                          # 交互模式
/rewrite --file paper.md          # 半自动模式
/rewrite --file paper.md --mode auto  # 全自动模式
/rewrite --style technical        # 指定风格
/rewrite --threshold 0.2          # 自定义阈值
/done                             # 结束交互模式
```
```

- [ ] **Step 2: 更新 analyze.py 接入完整流程**

```python
"""AIGC 风险分析引擎 CLI 入口。"""

import argparse
import json
import sys
from pathlib import Path

from analyzer.paragraphs import split_paragraphs
from analyzer.scorer import score_paragraphs, compute_overall_risk
from analyzer.patterns import PatternLibrary


def analyze_text(text: str, is_markdown: bool, threshold: float | None, patterns_dir: Path | None) -> dict:
    """执行完整的分析流程。"""
    # 加载模式库
    if patterns_dir:
        lib = PatternLibrary.load(patterns_dir)
    else:
        lib = PatternLibrary()

    # 段落切分
    paragraphs = split_paragraphs(text, is_markdown)
    if not paragraphs:
        return {"overall_risk": 0.0, "paragraphs": []}

    # 风险评分
    scored = score_paragraphs(paragraphs, lib.get_patterns())
    overall = compute_overall_risk(scored)

    return {
        "overall_risk": overall,
        "paragraphs": scored,
    }


def main():
    parser = argparse.ArgumentParser(description="分析文本的 AIGC 风险")
    parser.add_argument("input", nargs="?", help="输入文件路径 (.txt 或 .md)")
    parser.add_argument("--text", "-T", help="直接传入文本（交互模式用）")
    parser.add_argument("--output", "-o", help="输出 JSON 文件路径")
    parser.add_argument("--threshold", "-t", type=float, default=None, help="风险阈值")
    parser.add_argument("--patterns", "-p", help="模式库目录路径")
    args = parser.parse_args()

    # 确定输入
    if args.text:
        text = args.text
        is_markdown = False
    elif args.input:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"[错误] 文件不存在: {input_path}", file=sys.stderr)
            sys.exit(1)
        if input_path.suffix not in (".txt", ".md"):
            print(f"[错误] 不支持的格式: {input_path.suffix}", file=sys.stderr)
            sys.exit(1)
        text = input_path.read_text(encoding="utf-8")
        is_markdown = input_path.suffix == ".md"
    else:
        print("[错误] 请提供输入文件路径或 --text 参数", file=sys.stderr)
        sys.exit(1)

    if not text.strip():
        print("[错误] 输入内容为空", file=sys.stderr)
        sys.exit(1)

    patterns_dir = Path(args.patterns) if args.patterns else None
    result = analyze_text(text, is_markdown, args.threshold, patterns_dir)

    if args.output:
        Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: 验证 CLI**

```bash
echo "综上所述，本文提出了一种基于深度学习的方法。该方法具有重要意义。实验结果表明，该方法取得了较好的效果。" > /tmp/test_input.txt
python .claude/skills/rewrite/analyze.py /tmp/test_input.txt
```

Expected: 输出 JSON，包含 `overall_risk` 和 `paragraphs`。

- [ ] **Step 4: 提交**

```bash
git add .claude/skills/rewrite/SKILL.md .claude/skills/rewrite/analyze.py
git commit -m "feat: Skill 主控层与三种运行模式"
```

---

### Task 8: 集成测试与端到端验证

**Files:**
- Create: `tests/test_integration.py`

- [ ] **Step 1: 编写集成测试**

```python
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
    text = """综上所述，本文提出了一种基于深度学习的方法。
该方法具有重要意义，引起了广泛关注。
实验结果表明，该方法取得了较好的效果。
近年来，该领域的研究日益增多。
在此基础上，我们进一步优化了模型结构。"""

    paragraphs = split_paragraphs(text, is_markdown=False)
    assert len(paragraphs) == 5

    scored = score_paragraphs(paragraphs, builtin_patterns.get_patterns())
    assert len(scored) == 5

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
    assert "§0" in report
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
```

- [ ] **Step 2: 运行全部测试**

```bash
python -m pytest tests/ -v
```

Expected: 所有测试 PASS。

- [ ] **Step 3: 端到端手动验证**

```bash
# 测试分析引擎
echo "综上所述，本文提出了一种基于深度学习的方法。该方法具有重要意义。" > /tmp/test.txt
python .claude/skills/rewrite/analyze.py /tmp/test.txt

# 测试输出到文件
python .claude/skills/rewrite/analyze.py /tmp/test.txt --output /tmp/result.json
cat /tmp/result.json
```

Expected: JSON 输出包含 `overall_risk > 0.3`，`paragraphs` 中有 `issues`。

- [ ] **Step 4: 提交**

```bash
git add tests/test_integration.py
git commit -m "feat: 集成测试与端到端验证"
```

---

## 实现计划总览

| Task | 内容 | 产出 |
|------|------|------|
| 1 | 项目结构与依赖 | pyproject.toml、SKILL.md 骨架、analyze.py 骨架、utils |
| 2 | 模式库 | builtin.json (30 条规则)、PatternLibrary 加载器、测试 |
| 3 | 段落切分与章节识别 | paragraphs.py、测试 |
| 4 | 五个分析维度 | syntax/vocabulary/structure/ai_traces/chinese、测试 |
| 5 | 风险评分与优先级 | scorer.py、阈值管理、测试 |
| 6 | 改写执行层 | context/verify/diff、测试 |
| 7 | Skill 主控层 | 完整 SKILL.md、更新 analyze.py |
| 8 | 集成测试 | 端到端测试、手动验证 |

**预计工作量**：约 2-3 小时（含测试）。

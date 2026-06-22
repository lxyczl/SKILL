# Advanced Features Reference

This document describes the advanced features of the Paper Rewriter skill.

## Table of Contents

1. [Turnitin Report Parsing](#turnitin-report-parsing)
2. [Multiple Rewrite Options](#multiple-rewrite-options)
3. [Interactive Approval Mode](#interactive-approval-mode)
4. [Export Functionality](#export-functionality)
5. [Style Consistency Checking](#style-consistency-checking)
6. [Grammar Checking](#grammar-checking)
7. [Progress Tracking](#progress-tracking)
8. [Feedback Collection and Learning](#feedback-collection-and-learning)
9. [Batch Processing](#batch-processing)

---

## Turnitin Report Parsing

Parse Turnitin reports to identify high-priority sections. The skill automatically parses Turnitin reports when provided.

### Color Codes

| Color | Similarity | Priority | Action |
|-------|------------|----------|--------|
| 🔴 Red | 25-49% | HIGH | Must rewrite thoroughly |
| 🟠 Orange | 50-74% | MEDIUM | Rewrite as needed |
| 🟡 Yellow | 1-24% | LOW | Minor adjustments |
| 🟢 Green | Citation | CITATION | Keep as-is |
| 🔵 Blue | 0% | NONE | No changes needed |

### Processing Order

1. Process red sections first (highest priority)
2. Process orange sections next
3. Process yellow sections if time permits
4. Skip green and blue sections

### Intensity Mapping

- Red sections → Heavy intensity
- Orange sections → Medium intensity
- Yellow sections → Light intensity

---

## Multiple Rewrite Options

Provide multiple rewrite options for each sentence.

### Usage

When interactive mode is enabled, the skill provides 2-3 options:

```
## Sentence: "The results show that the method is effective."

### Option A (Light - 轻度改写)
"The findings demonstrate that the approach is efficacious."

**改动说明**:
- 词汇替换: results→findings, show→demonstrate, method→approach, effective→efficacious
- 句子结构: 保持不变
- 改写程度: 30%

### Option B (Medium - 中度改写)
"The obtained results indicate that the methodology exhibits effectiveness."

**改动说明**:
- 词汇替换: results→obtained results, show→indicate, method→methodology, is effective→exhibits effectiveness
- 句子结构: 添加 "obtained"，使用 "exhibits" 替代 "is"
- 改写程度: 60%

### Option C (Heavy - 重度改写)
"Effectiveness of the methodology is evidenced by the obtained results."

**改动说明**:
- 词汇替换: 完全重组
- 句子结构: 主被动转换，将 "effective" 提前作为主语
- 改写程度: 90%

## 推荐选择

- **如果相似度较低 (<25%)**: 选择 Option A
- **如果相似度中等 (25-50%)**: 选择 Option B
- **如果相似度较高 (>50%)**: 选择 Option C

请根据你的需求选择最合适的选项，或提供你自己的版本。
```

---

## Interactive Approval Mode

Process changes one by one with user approval.

### Usage

When interactive mode is enabled:

```
## Change 1 of 10

**Original**: "The study shows that social media has a big impact on young people."

**Proposed**: "The investigation demonstrates that social media exerts a substantial influence on adolescents."

**Reason**: Replaced "shows" with "demonstrates", "big impact" with "substantial influence", "young people" with "adolescents"

**Options**:
1. Accept this change
2. Reject this change
3. Modify this change
4. Skip to next change
```

### User Decisions

- **Accept**: Apply the change and move to next
- **Reject**: Keep original and move to next
- **Modify**: Let user edit the proposed change
- **Skip**: Move to next change without deciding

### Final Output

After all changes are processed, generate the final rewritten text with:
- Accepted changes applied
- Rejected changes kept as original
- Modified changes updated per user's edits

---

## Export Functionality

Export rewritten text to multiple formats.

### Supported Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| Text | .txt | Plain text output (default) |
| Word | .docx | Microsoft Word document |
| LaTeX | .tex | LaTeX source file |
| PDF | .pdf | PDF document |

### Usage

Export functionality is not currently available as a standalone script. For exporting, consider:
- Copy the rewritten text directly into your document editor
- Use Claude Code to help format the output in your preferred format

---

## Style Consistency Checking

Check for terminology consistency across the document. This is handled manually by reviewing:
- Same concept using different terms
- Different capitalization styles
- Inconsistent abbreviation usage
- Formal vs. informal language
- Active vs. passive voice
- Sentence length variation

---

## Grammar Checking

Grammar checking is performed manually or using external tools. Key areas to check:
- Subject-verb agreement
- Tense consistency within paragraphs
- Article usage ("a" vs "an")
- Proper use of academic language

### 错误详情

1. **subject_verb_agreement** (句子 5)
   - 错误: 主谓不一致: 'the results shows'
   - 建议: 建议改为: 'show'

2. **article_usage** (句子 12)
   - 错误: 冠词使用错误: 'a unique'
   - 建议: 元音前应使用 'an'，建议改为 'an unique'

### 整体评估
⚠️ 良好：存在少量语法问题，建议修正
```

---

## Progress Tracking

Track progress when rewriting long documents.

### Usage

When rewriting multiple paragraphs, the skill displays progress:

```
## Progress: 45% complete

### Completed:
- Paragraph 1: ✅ Rewritten (Heavy intensity)
- Paragraph 2: ✅ Rewritten (Medium intensity)
- Paragraph 3: ✅ Rewritten (Light intensity)

### In Progress:
- Paragraph 4: 🔄 Rewriting...

### Remaining:
- Paragraph 5: ⏳ Pending
- Paragraph 6: ⏳ Pending
- Paragraph 7: ⏳ Pending

### Statistics:
- Total paragraphs: 7
- Completed: 3
- In progress: 1
- Remaining: 3
- Estimated time remaining: 2 minutes
```

---

## Feedback Collection and Learning

Collect user feedback to improve the skill over time.

### Feedback Collection

After each rewriting session, the skill asks:

```
## 改写完成！请提供反馈

### 改写质量评分 (1-5分)
- 词汇替换质量: ___/5
- 句子结构调整: ___/5
- 专业术语保留: ___/5
- 整体满意度: ___/5

### 具体反馈
1. 哪些改写你最满意？
2. 哪些改写需要改进？
3. 有没有遗漏的专业术语？
4. 其他建议：

### 是否保存此反馈？
- 是，保存到学习库
- 否，不保存
```

### Feedback Storage

Feedback is saved to:
```
E:\WorkSpace\Claude Code\.claude\skills\paper-rewriter\feedback\
├── sessions/
│   ├── 2026-06-20-001.json
│   ├── 2026-06-20-002.json
│   └── ...
├── summaries/
│   ├── 2026-06-summary.json
│   └── ...
└── learning/
    ├── vocabulary_updates.json
    ├── technique_updates.json
    └── ...
```

### Learning Analysis

The skill automatically loads learned strategies when rewriting. Feedback data is stored in `feedback/learning/strategies.json`.

### Output

```
## 反馈分析报告

### 摘要
- 总会话数: 150
- 平均满意度: 4.2/5
- 最佳领域: 生态安全格局 (4.5/5)
- 最需改进领域: SHAP分析 (3.8/5)

### 常见问题
1. 25% 用户反馈"部分句子改写后不够自然"
2. 15% 用户反馈"希望提供更多改写选项"
3. 10% 用户反馈"某些专业术语未被识别"

### 改进建议
1. 优化句子结构调整算法，提高自然度
2. 为每个句子提供 3-5 个改写选项
3. 扩充专业术语库，添加更多领域词汇
```

---

## Batch Processing

Process multiple paragraphs or complete sections.

### Usage

When rewriting multiple paragraphs:

1. **Analyze the Complete Text**
   - Identify all paragraphs that need rewriting
   - Note which paragraphs have high similarity
   - Plan the rewriting strategy

2. **Process Paragraphs Sequentially**
   - Rewrite each paragraph using the core process
   - Maintain consistency across paragraphs
   - Keep track of terminology used

3. **Verify Cross-Paragraph Consistency**
   - Check that the same concept uses the same term throughout
   - Verify transitions are smooth
   - Ensure logical flow is maintained

4. **Generate Summary Report**
   - List all changes made
   - Note which paragraphs were heavily/lightly modified
   - Highlight any areas that need manual review

### Example

```
## Batch Processing Report

### Summary
- Total paragraphs: 10
- Rewritten: 8
- Skipped: 2 (citations only)

### Paragraph Details

1. ✅ Paragraph 1 (Heavy intensity)
   - Similarity: 45% → 12%
   - Changes: Complete restructuring

2. ✅ Paragraph 2 (Medium intensity)
   - Similarity: 35% → 8%
   - Changes: Vocabulary + structure

3. ⏭️ Paragraph 3 (Skipped)
   - Reason: Citation only, no changes needed

...

### Overall Results
- Average similarity reduction: 28%
- Total words changed: 150
- Estimated time: 5 minutes
```

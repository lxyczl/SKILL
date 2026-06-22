# Best Practices Guide

## Getting the Best Results

### 1. Choose the Right Intensity

| Similarity Score | Recommended Intensity | When to Use |
|------------------|----------------------|-------------|
| <25% (Yellow) | Light | Low similarity, just need minor adjustments |
| 25-50% (Red) | Medium | Moderate similarity, need sentence restructuring |
| >50% (Orange) | Heavy | High similarity, need complete rewrite |

**Tips:**
- Start with Medium intensity for most cases
- Use Heavy only for high-similarity sections
- Light intensity is best for fine-tuning

---

### 2. Specify Your Domain

Always mention your academic domain when requesting a rewrite.

**Why:**
- Preserves professional terminology
- Uses domain-specific vocabulary
- Ensures accuracy

**Example:**
```
改写这段话，学科：生态水文
```

**Supported Domains:**
- 生态水文 (Ecohydrology)
- 土木水利 (Civil and Hydraulic Engineering)
- 绿色建筑 (Green Building)
- 建筑节能 (Building Energy Efficiency)
- And 16 more...

See `references/domains.md` for the complete list.

---

### 3. Mention the Section Type

Different sections require different writing styles.

| Section | Style | Tense | Voice |
|---------|-------|-------|-------|
| Abstract | Concise | Present/Past | Active |
| Introduction | Background | Present/Past | Mixed |
| Methods | Precise | Past | Passive |
| Results | Data-driven | Past | Active |
| Discussion | Explanatory | Present | Active |
| Conclusion | Summary | Present | Active |

**Example:**
```
改写这段Methods部分
```

---

### 4. Use Turnitin Reports

If you have a Turnitin report, use it to prioritize your rewriting.

**Steps:**
1. Provide the Turnitin report to the skill
2. Focus on red sections first (25-49% similarity)
3. Then orange sections (50-74% similarity)
4. Skip green sections (citations)
5. Skip blue sections (0% similarity)

**Example:**
```
我有一个Turnitin报告，红色部分是这段：...
```

---

### 5. Use Multiple Options

Enable interactive mode to get multiple rewrite options.

**Benefits:**
- Choose the best version for your needs
- Compare different rewriting approaches
- Maintain control over the output

**Example:**
```
为这句话提供3个改写选项
```

---

### 6. Preserve Special Elements

Make sure to preserve:
- Citations: [1], [2,3], (Author, Year)
- Formulas: $E = mc^2$, $$\int_0^1 f(x) dx$$
- Code: `variable_name`, ```python ... ```
- Special characters: α, β, γ, Δ, Σ

**Example:**
```
改写这段话，保留引用和公式
```

---

### 7. Check the Output

After rewriting, verify:
1. ✅ Professional terminology is preserved
2. ✅ Citations and formulas are intact
3. ✅ The meaning is unchanged
4. ✅ The text sounds natural
5. ✅ No more than 5 consecutive words match the original

**Tools:**
- The skill automatically runs similarity checks after rewriting
- Provide Turnitin reports for priority-based rewriting

---

### 8. Use Batch Processing

For long papers with multiple paragraphs:
1. Process all paragraphs together
2. Maintain consistency across paragraphs
3. Verify cross-paragraph references
4. Generate a summary report

**Example:**
```
改写这3段话，保持上下文一致性
```

---

### 9. Collect Feedback

After each rewriting session:
1. Provide feedback on quality
2. Report missing terminology
3. Suggest improvements
4. Help improve the skill

**Why:**
- Improves the skill over time
- Adds missing domain vocabulary
- Fixes issues and bugs

---

### 10. Quality Control

After rewriting, verify:
- Similarity score is acceptable
- Professional terminology is preserved
- Citations and formulas are intact
- The meaning is unchanged

The skill automatically runs similarity checks and collects feedback.

---

## Common Mistakes to Avoid

### ❌ Don't: Skip Domain Specification
**Wrong:** "改写这段话"
**Right:** "改写这段话，学科：生态水文"

### ❌ Don't: Use Wrong Intensity
**Wrong:** Using Heavy intensity for low-similarity text
**Right:** Using Light intensity for low-similarity text

### ❌ Don't: Ignore Citations
**Wrong:** Not mentioning citations need to be preserved
**Right:** "改写这段话，保留引用"

### ❌ Don't: Skip Verification
**Wrong:** Using the output without checking
**Right:** Running quality checks before using the output

### ❌ Don't: Use Single Option
**Wrong:** Accepting the first rewrite without alternatives
**Right:** Requesting multiple options to choose from

---

## Workflow Recommendations

### For Individual Paragraphs
1. Copy the paragraph
2. Specify domain and intensity
3. Get rewritten text
4. Verify terminology and citations
5. Use the output

### For Entire Sections
1. Copy all paragraphs
2. Specify section type and domain
3. Use batch processing
4. Verify consistency across paragraphs
5. Run quality checks
6. Export to desired format

### For High-Similarity Text
1. Parse Turnitin report
2. Identify red/orange sections
3. Use Heavy intensity for red sections
4. Use Medium intensity for orange sections
5. Verify all changes
6. Run similarity check

---

## Quality Checklist

Before finalizing your rewritten text, check:

- [ ] Professional terminology preserved
- [ ] Citations intact ([1], [2,3], (Author, Year))
- [ ] Formulas preserved ($...$, $$...$$)
- [ ] Code snippets preserved (`...`)
- [ ] Special characters preserved (α, β, γ)
- [ ] Meaning unchanged
- [ ] Natural sounding text
- [ ] No more than 5 consecutive words matching original
- [ ] Consistent style across paragraphs
- [ ] Grammar correct
- [ ] Appropriate academic tone

---

## Getting Help

- **Quick Start:** See `QUICKSTART.md`
- **Troubleshooting:** See `TROUBLESHOOTING.md`
- **Domain Vocabulary:** See `references/domains.md`
- **Examples:** See `references/examples.md`
- **Advanced Features:** See `references/advanced.md`

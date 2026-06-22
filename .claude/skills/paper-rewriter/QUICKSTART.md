# Quick Start Guide

## 3-Step Quick Start

### Step 1: Prepare Your Text

Copy the paragraph(s) you want to rewrite from your paper.

**Example:**
```
The results show that the method is effective. The accuracy is high. The performance is good.
```

### Step 2: Choose Options

**Intensity** (改写强度):
- 🟢 **Light** (轻度): Just replace words, keep structure
- 🟡 **Medium** (中度): Replace words + adjust structure (default)
- 🔴 **Heavy** (重度): Complete rewrite

**Domain** (学科领域):
- Choose your field (e.g., 生态水文, 建筑节能, 土木工程)
- See `references/domains.md` for full list

**Section** (论文章节):
- Abstract (摘要), Introduction (引言), Methods (方法), Results (结果), Discussion (讨论), Conclusion (结论)

### Step 3: Get Rewritten Text

The skill will provide:

1. **Rewritten text** with changes highlighted
2. **Multiple options** (if interactive mode enabled)
3. **Change summary** showing what was modified

## Common Use Cases

### Use Case 1: Simple Rewrite

**Input:**
```
The study shows that social media has a big impact on young people.
```

**Output:**
```
The investigation demonstrates that social media exerts a substantial influence on adolescents.
```

### Use Case 2: Domain-Specific Rewrite

**Input (建筑节能):**
```
The building uses a lot of energy for heating in winter.
```

**Output:**
```
During winter months, the building consumes substantial amounts of energy for space heating purposes.
```

### Use Case 3: With Citations

**Input:**
```
The water flow rate Q was calculated using Equation (1) [1]. The results show good agreement with [2,3].
```

**Output:**
```
The volumetric flow rate Q was determined through application of Equation (1) [1]. The obtained findings demonstrate favorable concordance with the results reported in [2,3].
```

**Preserved:** Equation (1), [1], [2,3]

## Tips for Best Results

1. **Choose the right intensity**
   - Low similarity (<25%): Use Light
   - Medium similarity (25-50%): Use Medium
   - High similarity (>50%): Use Heavy

2. **Specify your domain**
   - This ensures professional terminology is preserved
   - Uses domain-specific vocabulary enhancements

3. **Provide context**
   - Mention the section type (Methods, Results, etc.)
   - This helps apply the right writing style

4. **Check the output**
   - Verify professional terminology is preserved
   - Ensure citations and formulas are intact
   - Confirm the meaning is unchanged

## Troubleshooting

### Problem: Professional terminology was modified

**Solution:** Make sure to specify your domain when requesting a rewrite.

### Problem: Citations were changed

**Solution:** Citations should be preserved. If they were changed, please report this issue.

### Problem: The rewrite doesn't sound natural

**Solution:** Try a different intensity level. Heavy intensity may produce less natural text.

### Problem: The similarity is still too high

**Solution:** Use Heavy intensity and consider rewriting multiple times.

## Need Help?

- See `references/domains.md` for domain-specific vocabulary
- See `references/examples.md` for all examples
- See `references/advanced.md` for advanced features

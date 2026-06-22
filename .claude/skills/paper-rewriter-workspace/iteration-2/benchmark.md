# Paper Rewriter Skill - Benchmark Results

## Iteration 2 (Updated with Terminology Preservation)

### Summary

| Configuration | Pass Rate | Std Dev |
|--------------|-----------|---------|
| **with_skill** | 100% | 0% |
| **without_skill** | 36.7% | 25% |

**Improvement: +173%**

### Per-Eval Breakdown

| Eval | with_skill | without_skill |
|------|------------|---------------|
| vocabulary-enhancement | 100% (4/4) | 50% (2/4) |
| sentence-structure-variation | 100% (4/4) | 25% (1/4) |
| passive-voice-and-insertions | 100% (4/4) | 25% (1/4) |
| high-priority-rewrite | 100% (4/4) | 25% (1/4) |
| preserve-terminology | 100% (6/6) | 83.3% (5/6) |

### Key Findings

1. **With-skill version achieves 100% pass rate** across all 5 test cases
2. **Without-skill version improved on terminology test** (83.3%) but still fails consecutive word matching
3. **New terminology preservation test validates** the skill correctly preserves technical terms
4. **Skill demonstrates consistent performance** across different rewriting scenarios
5. **The terminology preservation rule is working as intended**

### Terminology Preservation Test Results

**Preserved Terms (with_skill):**
- ✅ ResNet-50
- ✅ ImageNet
- ✅ CNN
- ✅ Adam optimizer
- ✅ LSTM

**Key Insight**: The skill correctly identifies and preserves all professional terminology while still restructuring sentences and replacing common words.

### Assertion Analysis

**Most Discriminating Assertions:**
- "No more than 5 consecutive words match the original" - Failed in 4/5 without-skill cases
- "Uses varied sentence structures" - Failed in all without-skill cases
- "Includes parenthetical insertions" - Failed in all without-skill cases

**Non-Discriminating Assertions:**
- "Preserves technical terms" - Passed in all cases (both with and without skill)
- "Maintains academic tone" - Passed in all cases

### Recommendations

1. The skill is performing well with the new terminology preservation rule
2. Consider adding more edge cases with mixed terminology and common words
3. Test with longer paragraphs containing multiple technical terms

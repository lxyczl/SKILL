# Troubleshooting Guide

## Common Issues and Solutions

### 1. Professional Terminology Was Modified

**Problem:** Domain-specific terms were changed during rewriting.

**Example:**
- Original: "The evapotranspiration rate is high"
- Wrong: "The evaporation rate is high"
- Correct: "The evapotranspiration rate demonstrates elevated levels"

**Solution:**
1. Make sure to specify your domain when requesting a rewrite
2. Check that the term is in the domain vocabulary list (`references/domains.md`)
3. If the term is missing, please report it so we can add it

**Prevention:**
- Always mention your domain (e.g., "学科：生态水文")
- Review the output to ensure terms are preserved

---

### 2. Citations Were Changed

**Problem:** Citations like [1] or (Smith, 2020) were modified.

**Example:**
- Original: "The results show [1]"
- Wrong: "The results indicate [2]"
- Correct: "The findings demonstrate [1]"

**Solution:**
1. Citations should always be preserved exactly
2. If citations were changed, this is a bug - please report it
3. Check that citations are in standard formats: [1], [2,3], (Author, Year)

**Prevention:**
- Ensure citations are in standard formats
- Review the output to verify citations are intact

---

### 3. Formulas Were Modified

**Problem:** Mathematical formulas were changed during rewriting.

**Example:**
- Original: "Q = A × v"
- Wrong: "Q = A * v"
- Correct: "Q = A × v" (preserved exactly)

**Solution:**
1. Formulas should always be preserved exactly
2. If formulas were changed, this is a bug - please report it
3. Use standard notation: $...$ for inline, $$...$$ for display

**Prevention:**
- Use standard formula notation
- Review the output to verify formulas are intact

---

### 4. The Rewrite Doesn't Sound Natural

**Problem:** The rewritten text sounds awkward or unnatural.

**Example:**
- Original: "The method is effective"
- Awkward: "The methodology exhibits effectiveness"
- Natural: "The approach demonstrates effectiveness"

**Solution:**
1. Try a different intensity level:
   - Heavy intensity may produce less natural text
   - Medium intensity usually provides the best balance
2. Use the multiple options feature to choose the best version
3. Manually adjust the output if needed

**Prevention:**
- Use Medium intensity for most cases
- Specify the section type for appropriate style
- Review and adjust the output as needed

---

### 5. The Similarity Is Still Too High

**Problem:** After rewriting, the similarity score is still high.

**Solution:**
1. Use Heavy intensity for high-similarity sections
2. Rewrite multiple times with different wording
3. Consider restructuring the entire paragraph
4. Use the Turnitin parser to identify high-priority sections

**Prevention:**
- Start with high-similarity sections
- Use Heavy intensity for red-marked sections
- Review the Turnitin report before rewriting

---

### 6. Missing Domain Vocabulary

**Problem:** Your domain is not supported or missing terms.

**Solution:**
1. Check `references/domains.md` for the full list of supported domains
2. If your domain is missing, please report it
3. If terms are missing, provide them in your feedback

**Prevention:**
- Check the domain list before requesting a rewrite
- Provide domain-specific terms in your request

---

### 7. Export Failed

**Problem:** Unable to export to Word/LaTeX/PDF format.

**Solution:**
1. **Word export failed:**
   - Install python-docx: `pip install python-docx`
   - Check file permissions

2. **LaTeX export failed:**
   - Check LaTeX syntax in the output
   - Ensure special characters are properly escaped

3. **PDF export failed:**
   - Install pdflatex (TeX Live or MiKTeX)
   - Check LaTeX compilation errors

**Prevention:**
- Install required dependencies
- Check file permissions
- Review error messages

---

### 8. Grammar Errors in Output

**Problem:** The rewritten text contains grammar errors.

**Solution:**
1. Review and fix errors manually
2. Report the issue so we can improve the skill

**Prevention:**
- Review the output carefully
- Report any grammar errors you find

---

### 9. Style Inconsistency

**Problem:** Different paragraphs use different terminology.

**Example:**
- Paragraph 1: "water resources"
- Paragraph 2: "water resource"

**Solution:**
1. Standardize terminology across the document
2. Maintain a list of preferred terms

**Prevention:**
- Maintain consistent terminology throughout
- Review the entire document for consistency

---

### 10. Interactive Mode Not Working

**Problem:** The interactive approval feature is not working.

**Solution:**
1. Make sure to specify "interactive mode: Yes" in your request
2. Check that the skill is properly configured
3. Try restarting the skill

**Prevention:**
- Explicitly request interactive mode
- Follow the interactive mode instructions

---

## Reporting Issues

If you encounter any issues not covered here, please report them:

1. **Describe the issue clearly**
   - What happened?
   - What did you expect?
   - What was the input?

2. **Provide examples**
   - Original text
   - Rewritten text
   - Expected result

3. **Include context**
   - Domain
   - Intensity level
   - Section type

4. **Save feedback**
   - Use the feedback collection feature
   - Include all relevant information

---

## Getting Help

- **Quick Start:** See `QUICKSTART.md`
- **Domain Vocabulary:** See `references/domains.md`
- **Examples:** See `references/examples.md`
- **Advanced Features:** See `references/advanced.md`

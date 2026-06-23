---
name: paper-rewriter
description: |
  Rewrite English academic papers to reduce similarity scores. Use this skill when the user wants to:
  - Rewrite/paraphrase English academic text
  - Reduce plagiarism/similarity detection scores
  - "降重", "改写", "rewrite", "paraphrase", "reduce similarity"
---

# 英文学术论文改写降重

## 核心流程

### 场景1：用户发文本
1. **分析风险**：运行 `$PY analyze.py --text "<原文>"` 获取风险评分和问题列表
   - 关注 `overall_risk`（0-1）和各段落的 `issues`（具体问题）
   - `suggestion` 字段给出改写建议
2. **获取历史建议**：运行 `$PY scripts/rewrite_with_feedback.py suggest <domain> <intensity>` 获取反馈学习建议
3. 扫描学科关键词 → 读取 `references/domains.md` 对应词汇
4. **针对性改写**：
   - 优先解决分析引擎指出的高风险问题（`priority` 最高的段落）
   - 应用反馈建议：优先使用 `effective_techniques`，保护 `new_terms_to_preserve`
   - 针对具体 issue 类型改写（见下方"风险类型与改写策略"）
5. **记录改动**：改写完成后，将每处改动记录为 `changes_made`（格式：`{"type": "技巧类型", "original": "原文片段", "rewritten": "改写片段"}`）
6. **分析结果**：运行以下 CLI 命令分析并记录会话：
   ```bash
   $PY scripts/rewrite_with_feedback.py analyze <原文文件> <改写文件> <学科> <强度>
   ```
   输出 JSON 包含：session_id, composite_score, auto_evaluation, hot_sentences, needs_iteration, report
7. **迭代验证**（自动）：
   - 如果 `needs_iteration` 为 true：
     a. 查看 `hot_sentences`，定位需要重点改写的句子
     b. 使用 `suggested_techniques` 针对性改写这些句子
     c. 再次运行 analyze 验证（最多 3 轮）
     d. 如果 3 轮后仍有 fail/warning：返回当前最佳结果，附带 warning 提示"以下句子仍需手动调整"并列出未解决的热点句子
8. 改写后主动询问满意度，收集反馈

### 场景2：用户给文件
1. 运行 `$PY scripts/document_parser.py <file> [section]` 提取文本
2. **分析风险**（同场景1步骤1）
3. **获取历史建议**（同场景1步骤2）
4. **针对性改写**（同场景1步骤4）— 每段 ≤500 词
5. **记录改动**（同场景1步骤5）
6. **分析每段结果**（同场景1步骤6）
7. **迭代验证**：对 `needs_iteration` 的段落自动迭代改写（最多 3 轮）
8. 合并结果 + 报告，返回最终结果
9. 改写后主动询问满意度，收集反馈

### 场景3：用户反馈
1. 改写后询问满意度（词汇1-5、结构1-5、术语保留1-5、总体1-5）
2. 运行 `$PY scripts/rewrite_with_feedback.py feedback <session_id> <v> <s> <t> <o>` 记录反馈
3. 如有缺失术语或建议，一并记录
4. 系统自动学习，下次改写时应用

### 反馈闭环（关键）
每次改写必须遵循：**获取建议 → 应用建议 → 记录改动 → 分析结果 → 收集反馈**

建议的使用方式：
- `effective_techniques`：成功率 ≥70% 的技巧优先使用
- `new_terms_to_preserve`：这些词必须原样保留，不改写
- `intensity_multiplier`：>1.1 时加强改写，<0.9 时减弱改写
- `preferred_vocabulary`：历史高分替换对，优先采用
- `domain_issues`：该学科常见问题，避免重复犯错

反馈数据存储在 `feedback/sessions/`，学习结果在 `feedback/learning/strategies.json`

### 风险类型与改写策略

分析引擎会输出具体的风险类型，针对每种类型有对应的改写策略：

| 风险类型 | 含义 | 改写策略 |
|----------|------|----------|
| `uniform_sentence_length` | 句长过于均匀 | 制造长短交错：拆长句、合短句 |
| `excessive_passive` | 被动语态过多 | 主被动交替，关键结果用主动 |
| `excessive_parallelism` | 并列结构过多 | 拆分并列，用从句/分词替代 |
| `deep_nesting` | 从句嵌套太深 | 拆分为独立句子 |
| `low_ttr` | 词汇重复率高 | 同义词替换，丰富用词 |
| `connector_overuse` | 连接词过多 | 删减多余连接词，用逻辑隐连 |
| `cliche_detected` | 套话/模板化表达 | 替换为具体/个性化表达 |
| `too_fluent` | 过于流畅工整 | 加入破折号、括号补充等非正式标记 |
| `low_burstiness` | 句长变化缺乏突发性 | 制造长短句交替的节奏感 |
| `no_personal_voice` | 缺少个人表达 | 加入 "we"、"our"、"the authors" |
| `monotonous_openings` | 句首模式单调 | 变换句首：从句开头、分词开头、there be |
| `excessive_the` | 冠词 "the" 过度 | 用具体名词替代，减少不必要的 the |
| `excessive_hedging` | 模糊限定词过多 | 减少 may/might/could，更直接表达 |
| `excessive_nominalization` | 名词化过度 | 把名词还原为动词（implementation→implement） |
| `verbose_phrases` | 冗长短语 | 简化（in order to→to, due to the fact that→because） |
| `uniform_para_length` | 段落长度过于均匀 | 合并短段、拆分长段 |
| `uniform_para_start` | 段首句模式重复 | 变换段首句开头方式 |

---

## 必须保留（不能改）

专业术语、引用 [1] (Author, Year)、公式 $...$、数字、单位、地名、模型名、人名、缩写

## 关键规则

1. **不能连续5个词和原文相同**
2. **每句话至少用2种技巧**
3. **保持学术正式语体**
4. **不改变原意**

---

### 章节差异化阈值

不同章节的 composite_score 阈值不同：

| 章节 | 阈值 | 理由 |
|------|------|------|
| Abstract | 50 | 摘要是查重重灾区 |
| Introduction | 60 | 引言容易与文献综述重复 |
| Methods | 70 | 方法描述常用固定表达 |
| Results | 60 | 结果描述相对客观 |
| Discussion | 50 | 讨论容易与已有研究重复 |
| Conclusion | 60 | 结论常用套话 |

超过阈值时应继续迭代改写。

---

## 改写技巧（按效果排序）

### 第一梯队：优先使用

| 技巧 | 示例 |
|------|------|
| 名词化+被动 | "We analyzed..." → "A comprehensive analysis was performed..." |
| 分词结构 | "Because the study focused on..." → "Focusing on..." |
| 从句插入 | "The model achieved accuracy" → "The model, trained on large datasets, achieved accuracy" |
| 引用移动 | "X is important [1]" → "According to [1], X is important" |
| 转述动词 | "The study found" → "The study revealed/demonstrated/highlighted" |

### 第二梯队：常用技巧

| 技巧 | 示例 |
|------|------|
| 语态转换 | "Researchers conducted..." → "The experiment was conducted..." |
| 同义词替换 | 见下方词汇表 |
| 词序调整 | 把状语提前，调整从句位置 |
| 介词重组 | "In the study, we found" → "Through our investigation, we identified" |
| 让步从句 | "X is true, but Y" → "Although X is true, Y" |

### 第三梯队：辅助技巧

| 技巧 | 示例 |
|------|------|
| 句子合并 | "A is good. It reduces cost." → "A is good, reducing cost." |
| 否定反转 | "This is not uncommon" → "This is rather common" |
| 假设语气 | "X causes Y" → "X is likely to contribute to Y" |
| 存在句 | "Many factors affect..." → "There are numerous factors affecting..." |
| 抽象名词化 | "The temperature increased" → "An increase in temperature was observed" |

---

## 同义词表

**必须掌握**：show→demonstrate/indicate, use→utilize/employ, find→identify/detect, result→outcome/finding, important→crucial/vital, increase→enhance/augment, decrease→reduce/diminish, many→numerous/various, have→possess/exhibit, provide→offer/furnish

**常用**：so→therefore, because→since/due to, but→however/whereas, also→additionally/moreover, about→approximately, enough→sufficient, get→obtain, make→generate, help→facilitate, problem→issue/challenge, think→consider, study→investigation, method→approach, data→evidence, model→framework, area→region

---

## 复杂句处理

**长句拆分**：超过30词，考虑拆成2句

**嵌套从句重组**：多层嵌套简化为分词结构

**并列结构变换**：重复主语合并为并列结构

---

## 句型模板

| 场景 | 改写模式 |
|------|---------|
| 被用于 | Y was accomplished through X |
| 结果显示 | From the results, it can be observed that... |
| 因果 | Given X, Y / X; consequently, Y |
| 越来越多 | An increasing number of investigations... |
| 重要意义 | X plays a crucial role in Y |
| 研究表明 | Previous investigations have demonstrated that... |
| 导致 | X gives rise to Y / X contributes to Y |

---

## 强度选择

| 用户说 | 做法 |
|--------|------|
| 轻度/light | 主要同义词替换，不改结构 |
| 中度/medium | 同义词+结构调整（默认） |
| 重度/heavy | 完全重组，使用所有技巧 |

---

## 章节风格

| 章节 | 时态 | 语态 |
|------|------|------|
| Abstract | 现在/过去 | 主动 |
| Introduction | 现在/过去 | 混合 |
| Methods | 过去 | 被动 |
| Results | 过去 | 主动 |
| Discussion | 现在 | 主动 |
| Conclusion | 现在 | 主动 |

---

## 反面教材

- ❌ 只换词不改结构（相似度还是高）
- ❌ 改变原意（加了"somehow"等限定词）
- ❌ 破坏专业术语（把 InVEST 改成 InVEST framework）
- ❌ 破坏引用格式（[1] 变成 [ 1 ]）
- ❌ 过度拆分（句子太碎不流畅）

---

## 检查清单

返回前必须检查：
- [ ] 连续词：有没有连续8个词和原文相同？（Turnitin 阈值）
- [ ] 术语：专业术语是否保留？
- [ ] 引用：引用格式是否完整？
- [ ] 公式：公式是否原样保留？
- [ ] 原意：是否改变了原意？
- [ ] 语法：语法是否正确？
- [ ] 流畅：读起来是否通顺？
- [ ] 学术：是否保持学术正式语体？
- [ ] 迭代：needs_iteration 是否已处理？

---

## 输出格式

直接返回改写后的文本，不需要额外解释。

如果用户要求看改动说明，再附上用了哪些技巧和主要替换了哪些词。

---

## 示例

**示例1**：名词化+被动+引用移动
> 原文：We analyzed the data and found that the temperature increased significantly [1].
> 改写：A comprehensive analysis of the data was performed, revealing a significant increase in temperature [1].

**示例2**：分词+让步+目的从句
> 原文：The method has limitations, but it is widely used. We applied this approach to assess the vulnerability.
> 改写：Although the method exhibits certain limitations, it remains widely adopted. This approach was applied with the aim of assessing vulnerability.

**示例3**：转述动词+介词重组+存在句
> 原文：The study found that many factors affect groundwater quality.
> 改写：The investigation revealed that numerous factors influence groundwater quality.

---

## 学科自动识别

当用户提到以下关键词时，自动识别学科并读取对应词汇：

### 关键词 → 学科映射

| 关键词 | 学科 | 自动读取 |
|--------|------|---------|
| 生态水文、水量平衡、蒸散发、产水服务、水源涵养、水循环 | 生态水文 | `references/domains.md` |
| 生态安全格局、生态源地、生态廊道、生态阻力面、生态节点、生态网络 | 生态安全格局 | `references/domains.md` |
| 地下水脆弱性、DRASTIC、地下水埋深、含水层、包气带、水文地质 | 地下水脆弱性 | `references/domains.md` |
| InVEST、habitat quality、carbon storage、water yield、生态系统服务 | InVEST模型 | `references/domains.md` |
| OWA、有序加权平均、风险因子、权重系数、多准则决策 | OWA算法 | `references/domains.md` |
| 土木水利、水利工程、大坝、水库、水工结构 | 土木水利 | `references/domains.md` |
| 绿色建筑、建筑节能、BIPV、光伏、太阳能 | 绿色建筑/光伏 | `references/domains.md` |
| SHAP、SHAP分析、可解释性、特征重要性 | SHAP分析 | `references/domains.md` |
| 半干旱区、地表-地下耦合、生态耦合 | 半干旱区耦合 | `references/domains.md` |
| 电路理论、电路模型、电流、电阻 | 电路理论 | `references/domains.md` |

### 识别流程

1. 用户发文本或说学科 → 自动扫描关键词
2. 识别到学科 → 自动读取 `references/domains.md` 对应章节
3. 使用该学科的专业术语（不改）和替换词

### 识别示例

```
用户：帮我改写这段生态水文的论文摘要
→ 识别到"生态水文" → 自动读取生态水文词汇 → 使用专业术语

用户：The InVEST model was used to calculate ecosystem services
→ 识别到"InVEST"、"ecosystem services" → 自动读取InVEST模型词汇 → 使用专业术语

用户：We applied the OWA algorithm to balance trade-offs
→ 识别到"OWA"、"trade-offs" → 自动读取OWA算法词汇 → 使用专业术语
```

### 未识别到学科

如果用户没有说学科，也从文本中识别不到关键词：
- 使用通用学术词汇
- 不使用特定学科的专业术语
- 告知用户："未识别到特定学科，使用通用学术词汇。如需更精准的改写，请告知学科。"

完整学科列表见 `references/domains.md`（20个学科）

---

## 边界情况

| 情况 | 处理方式 |
|------|---------|
| 短文本（<20词） | 告知用户太短，建议提供更长段落 |
| 非学术文本 | 告知技能不适用，如用户坚持仍尝试 |
| 已低相似度 | 先计算，如果已经很低则告知不需要改写 |
| 混合语言 | 只改英文，保留中文 |
| 大量公式/引用 | 标记不改，只改其他部分 |
| 超长文本（>500词） | 建议分段，每段不超过300词 |
| 列表/枚举 | 保留结构，只改内容 |
| 直接引语 | 引号内不改，只改转述部分 |
| 术语密集 | 标记术语不改，只改连接词和动词 |

---

## 参考资料（需要时自动读取）

当遇到以下情况时，自动读取对应的参考文件：

| 情况 | 读取文件 |
|------|---------|
| 需要更多改写技巧示例 | `references/techniques.md` |
| 需要更多同义词 | `references/synonyms.md` |
| 识别到学科关键词 | `references/domains.md` |
| 遇到边界情况（短文本、非学术等） | `references/edge_cases.md` |
| 需要更多改写示例 | `references/examples.md` |

**读取方式**：使用 Read 工具读取对应文件，获取详细信息。

**自动识别学科**：扫描用户文本中的关键词，自动匹配学科，读取对应词汇。

---

**记住：用户发文本（或给文件），你自动改写、自动验证、自动收集反馈。遇到边界情况，主动告知用户。**

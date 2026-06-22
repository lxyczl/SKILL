# English Academic Paper Rewriter

一个用于英文学术论文改写降重的 Claude Code 技能。

## 功能特点

- **6种改写技巧**: 语态转换、从句插入、句子合并/拆分、同义词替换、词序调整、高级词汇替换
- **3种强度级别**: 轻度 (Light)、中度 (Medium)、重度 (Heavy)
- **20个学科领域**: 生态水文、土木水利、绿色建筑、建筑节能等
- **专业术语保护**: 自动识别并保留专业术语、引用、公式
- **相似度检测**: LCS + N-gram precision/recall + 连续匹配检测的复合评分
- **反馈学习系统**: 自动记录改写结果，收集用户满意度，学习并优化改写策略
- **文档解析**: 自动从 docx/pdf 文件中提取文本和章节

## 快速开始

### 1. 使用技能

**方式一：直接告诉 Claude**

```
帮我改写这段英文论文：
[paste your text here]
```

**方式二：提供文件**

```
帮我改写这个论文的摘要：
E:\Desktop\paper.docx
```

**方式三：指定选项**

```
请用中等强度改写这段生态水文领域的论文摘要：
[paste your text here]
```

## 文件结构

```
paper-rewriter/
├── SKILL.md                    # 核心技能文件
├── README.md                   # 本文件
├── references/
│   ├── domains.md              # 20个学科的专业词汇表
│   ├── examples.md             # 26个改写示例
│   ├── techniques.md           # 改写技巧详解
│   ├── synonyms.md             # 同义词替换表
│   └── edge_cases.md           # 边界情况处理
├── scripts/
│   ├── document_parser.py      # 文档解析
│   ├── similarity_calculator.py # 相似度计算（LCS + N-gram）
│   ├── rewrite_with_feedback.py # 分析 + 反馈入口
│   ├── feedback_system.py      # 反馈记录 & 学习
│   └── turnitin_parser.py      # Turnitin 报告解析
├── feedback/
│   ├── sessions/               # 改写会话记录
│   └── learning/               # 学习到的策略
└── tests/
    ├── test_basic.py           # 基础单元测试
    ├── test_real_paper.py      # 真实论文测试
    ├── test_feedback_system.py # 反馈系统测试
    ├── test_real_feedback.py   # 真实论文反馈测试
    └── test_complete_workflow.py # 完整工作流测试
```

## 使用方法

直接在 Claude Code 中使用：

```
帮我改写这段英文论文：
[paste your text here]
```

或提供文件：

```
帮我改写这个论文的摘要：
E:\Desktop\paper.docx
```

脚本由 SKILL.md 自动调用，无需手动执行。

## 改写技巧

| 技巧 | 示例 |
|------|------|
| 语态转换 | "Researchers conducted..." → "The experiment was conducted..." |
| 从句插入 | "The model achieved high accuracy" → "The model, trained on large datasets, achieved high accuracy" |
| 句子合并 | "The algorithm is efficient. It reduces time." → "The algorithm is efficient, reducing computation time." |
| 同义词替换 | "use" → "utilize", "show" → "demonstrate" |
| 词序调整 | 移动状语短语，重新排列从句顺序 |

## 强度级别

| 级别 | 描述 | 适用场景 |
|------|------|---------|
| 🟢 轻度 (Light) | 仅替换词汇 | 低相似度 (1-24%) |
| 🟡 中度 (Medium) | 词汇+结构调整 | 中等相似度 (25-49%) |
| 🔴 重度 (Heavy) | 完全重组 | 高相似度 (50%+) |

## 学科领域

支持以下学科的专业词汇：

- 生态水文 | 土木水利 | 绿色建筑 | 建筑节能
- 水利工程 | 土木工程 | BIPV | 光伏
- 生态安全格局 | SHAP分析 | 地下水脆弱性 | 生态系统服务
- 半干旱区地表-地下生态耦合 | InVEST模型 | 改进DRASTIC模型
- 电路理论 | OWA有序加权平均算法 | 生态源地 | 生态廊道 | 生态阻力面

## 反馈学习系统

技能包含一个反馈学习系统，可以：

1. **记录改写会话**: 每次改写自动记录原文、改写后文本、相似度指标
2. **收集用户反馈**: 用户可以对词汇、句子结构、术语保留、总体满意度评分
3. **学习改写策略**: 系统分析反馈，学习哪些技术最有效
4. **优化未来改写**: 基于学习结果，自动调整改写策略

### 学习内容

- **词汇偏好**: 哪些词汇替换获得高评分
- **技术有效性**: 哪些改写技术最有效
- **领域模式**: 各学科领域的常见问题
- **强度调整**: 是否需要增加或减少改写强度
- **新术语**: 用户希望保留的新术语

## 使用建议

1. **选择合适的强度**: 根据相似度报告选择改写强度
2. **指定学科领域**: 提供学科信息以获得更准确的专业词汇替换
3. **保留专业术语**: 技能会自动保留专业术语，无需手动标注
4. **检查改写结果**: 使用相似度计算器验证改写效果
5. **提供反馈**: 使用反馈系统帮助技能学习和改进

## 注意事项

- 改写不会改变原文的核心含义和事实内容
- 专业术语、引用、公式会被自动保留
- 改写后的文本保持学术正式语体
- 不适用于非学术写作、翻译或生成全新内容

## 许可证

MIT License

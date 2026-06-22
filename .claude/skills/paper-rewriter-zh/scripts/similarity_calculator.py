"""
中文相似度计算脚本
用于评估改写前后文本的相似度
"""
from pathlib import Path
import re
from collections import Counter


def tokenize(text: str) -> list[str]:
    """将文本分词为汉字列表（按字分割）"""
    # 提取汉字和数字
    return re.findall(r'[一-鿿]|[0-9]+', text)


def ngrams(tokens: list[str], n: int) -> list[tuple]:
    """生成 n-gram"""
    return [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]


def calculate_similarity(original: str, rewritten: str) -> dict:
    """
    计算两段文本的相似度

    返回:
        - unigram_overlap: 字级别的重叠率
        - bigram_overlap: 二元组重叠率
        - trigram_overlap: 三元组重叠率
        - max_consecutive: 最长连续匹配字数
        - vocabulary_diversity: 词汇多样性分数
    """
    orig_tokens = tokenize(original)
    rewrite_tokens = tokenize(rewritten)

    # 字级别重叠
    orig_set = set(orig_tokens)
    rewrite_set = set(rewrite_tokens)
    unigram_overlap = len(orig_set & rewrite_set) / len(orig_set) if orig_set else 0

    # 二元组重叠
    orig_bigrams = set(ngrams(orig_tokens, 2))
    rewrite_bigrams = set(ngrams(rewrite_tokens, 2))
    bigram_overlap = len(orig_bigrams & rewrite_bigrams) / len(orig_bigrams) if orig_bigrams else 0

    # 三元组重叠
    orig_trigrams = set(ngrams(orig_tokens, 3))
    rewrite_trigrams = set(ngrams(rewrite_tokens, 3))
    trigram_overlap = len(orig_trigrams & rewrite_trigrams) / len(orig_trigrams) if orig_trigrams else 0

    # 最长连续匹配（知网查重规则：连续13字相同）
    max_consecutive = 0
    current_consecutive = 0
    for i in range(min(len(orig_tokens), len(rewrite_tokens))):
        if orig_tokens[i] == rewrite_tokens[i]:
            current_consecutive += 1
            max_consecutive = max(max_consecutive, current_consecutive)
        else:
            current_consecutive = 0

    # 词汇多样性（独特字/总字数）
    vocabulary_diversity = len(rewrite_set) / len(rewrite_tokens) if rewrite_tokens else 0

    return {
        "unigram_overlap": round(unigram_overlap, 3),
        "bigram_overlap": round(bigram_overlap, 3),
        "trigram_overlap": round(trigram_overlap, 3),
        "max_consecutive": max_consecutive,
        "vocabulary_diversity": round(vocabulary_diversity, 3),
        "original_char_count": len(orig_tokens),
        "rewritten_char_count": len(rewrite_tokens)
    }


def format_report(original: str, rewritten: str) -> str:
    """生成格式化的相似度报告"""
    metrics = calculate_similarity(original, rewritten)

    report = """
## 相似度分析报告

### 基本信息
- 原文字数: {original_char_count}
- 改写字数: {rewritten_char_count}

### 相似度指标
| 指标 | 值 | 说明 |
|------|-----|------|
| 字重叠率 | {unigram_overlap:.1%} | 字级别的相似度 |
| 二元组重叠率 | {bigram_overlap:.1%} | 连续两个字的相似度 |
| 三元组重叠率 | {trigram_overlap:.1%} | 连续三个字的相似度 |
| 最长连续匹配 | {max_consecutive} 字 | 改写后最多连续几个字与原文相同 |
| 词汇多样性 | {vocabulary_diversity:.1%} | 独特字占比 |

### 评估结果
{assessment}
"""

    # 评估结果（知网查重规则：连续13字相同算抄袭）
    if metrics["max_consecutive"] >= 13:
        assessment = "⚠️ **警告**: 存在超过13个连续字匹配，需要进一步改写"
    elif metrics["max_consecutive"] >= 10:
        assessment = "⚠️ **注意**: 存在超过10个连续字匹配，建议调整"
    elif metrics["trigram_overlap"] > 0.3:
        assessment = "⚠️ **注意**: 三元组重叠率较高，建议调整句子结构"
    elif metrics["unigram_overlap"] > 0.7:
        assessment = "⚠️ **注意**: 字重叠率较高，建议增加同义词替换"
    else:
        assessment = "✅ **通过**: 相似度在可接受范围内"

    return report.format(**metrics, assessment=assessment)


def find_consecutive_matches(original: str, rewritten: str, min_length: int = 13) -> list[dict]:
    """找出所有超过指定长度的连续匹配"""
    orig_tokens = tokenize(original)
    rewrite_tokens = tokenize(rewritten)

    matches = []
    i = 0
    while i < len(orig_tokens):
        j = 0
        while j < len(rewrite_tokens):
            # 找到匹配起点
            if orig_tokens[i] == rewrite_tokens[j]:
                length = 0
                while (i + length < len(orig_tokens) and
                       j + length < len(rewrite_tokens) and
                       orig_tokens[i + length] == rewrite_tokens[j + length]):
                    length += 1

                if length >= min_length:
                    matches.append({
                        "start_orig": i,
                        "start_rewrite": j,
                        "length": length,
                        "text": "".join(orig_tokens[i:i+length])
                    })
                j += length
            else:
                j += 1
        i += 1

    return matches


def main():
    """主函数 - 命令行接口"""
    import sys

    if len(sys.argv) < 3:
        print("用法: python similarity_calculator.py <原文文件> <改写文件>")
        print("示例: python similarity_calculator.py original.txt rewritten.txt")
        sys.exit(1)

    original_file = Path(sys.argv[1])
    rewritten_file = Path(sys.argv[2])

    if not original_file.exists():
        print(f"错误: 找不到文件 {original_file}")
        sys.exit(1)

    if not rewritten_file.exists():
        print(f"错误: 找不到文件 {rewritten_file}")
        sys.exit(1)

    original = original_file.read_text(encoding='utf-8')
    rewritten = rewritten_file.read_text(encoding='utf-8')

    print(format_report(original, rewritten))

    # 显示超过13个字的连续匹配
    matches = find_consecutive_matches(original, rewritten, min_length=13)
    if matches:
        print("\n### 超过13个字的连续匹配")
        for i, match in enumerate(matches, 1):
            print(f"{i}. 位置 {match['start_orig']}: \"{match['text']}\" ({match['length']} 字)")


if __name__ == "__main__":
    main()

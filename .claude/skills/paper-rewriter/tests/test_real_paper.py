#!/usr/bin/env python3
"""
真实论文测试脚本
测试论文改写技能在实际学术论文上的效果
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from similarity_calculator import calculate_similarity


def extract_paragraphs_from_docx(docx_path: str, start: int = 0, end: int = 10) -> list:
    """从docx文件中提取段落"""
    try:
        import docx
        doc = docx.Document(docx_path)
        paragraphs = []
        for i, para in enumerate(doc.paragraphs[start:end]):
            if para.text.strip():
                paragraphs.append({
                    'index': i + start,
                    'text': para.text
                })
        return paragraphs
    except Exception as e:
        print(f"读取docx文件失败: {e}")
        return []


def test_similarity(original: str, rewritten: str, label: str = "") -> dict:
    """测试两个文本的相似度"""
    print(f"\n{'='*60}")
    if label:
        print(f"测试: {label}")
    print(f"{'='*60}")

    print(f"\n原文 (前200字):")
    print(original[:200] + "..." if len(original) > 200 else original)

    print(f"\n改写后 (前200字):")
    print(rewritten[:200] + "..." if len(rewritten) > 200 else rewritten)

    result = calculate_similarity(original, rewritten)

    print(f"\n相似度分析:")
    print(f"  综合评分: {result['composite_score']}/100")
    print(f"  LCS 比率: {result['lcs_ratio']:.1%}")
    print(f"  三元组精度: {result['trigram_precision']:.1%}")
    print(f"  三元组召回: {result['trigram_recall']:.1%}")
    print(f"  词汇重叠: {result['vocabulary_overlap']:.1%}")
    print(f"  最长连续匹配: {result['max_consecutive']} 词")

    # 评估
    if result["max_consecutive"] >= 8:
        assessment = "[WARNING] 存在 ≥8 词连续匹配"
    elif result["max_consecutive"] >= 5:
        assessment = "[WARNING] 存在 ≥5 词连续匹配"
    elif result["trigram_precision"] > 0.3:
        assessment = "[WARNING] 三元组精度偏高"
    elif result["composite_score"] > 60:
        assessment = "[WARNING] 综合相似度偏高"
    else:
        assessment = "[PASS] 相似度在可接受范围内"

    print(f"  评估: {assessment}")
    result['assessment'] = assessment
    return result


def main():
    """主测试函数"""
    print("=" * 60)
    print("真实论文测试 - 英文学术论文改写技能")
    print("=" * 60)

    paper_path = r"E:\Desktop\Manuscript星儿修订版(1) - 副本.docx"

    print("\n正在读取论文...")
    paragraphs = extract_paragraphs_from_docx(paper_path, start=17, end=25)

    if not paragraphs:
        print("无法读取论文内容")
        return

    print(f"成功提取 {len(paragraphs)} 个段落")

    # 测试用例1: 摘要
    abstract = paragraphs[0]['text']
    abstract_rewritten = """Rapid urbanization and intensive resource extraction have progressively deteriorated global ecosystems, especially within arid and semi-arid regions. While ecological security pattern (ESP) construction has emerged as a widely accepted strategy for maintaining ecosystem equilibrium, current methodologies predominantly address surface-level conditions and systematically neglect subsurface systems—specifically groundwater—which represents a critical constraining factor in dryland environments."""

    result1 = test_similarity(abstract, abstract_rewritten, "摘要改写 (高强度)")

    # 测试用例2: 引言
    intro_para = paragraphs[3]['text']
    intro_rewritten = """Propelled by the concurrent intensification of urban expansion and industrial development, anthropogenic impacts on natural ecosystems have steadily increased, while the overexploitation of land resources has caused a persistent reduction in ecological space, making the structural conflicts among ecological, productive, and residential land uses more evident[1]."""

    result2 = test_similarity(intro_para, intro_rewritten, "引言第一段改写 (中等强度)")

    # 测试用例3: 方法论
    method_para = paragraphs[7]['text'] if len(paragraphs) > 7 else ""
    result3 = None
    if method_para:
        method_rewritten = """Groundwater vulnerability describes the capacity of aquifer systems to resist pollutant infiltration and migration under natural conditions. Based on the fundamental principles of the DRASTIC model and the ecological environment characteristics of Yinshanbeilu Grassland, this study selected six factors: groundwater table depth, KNDVI, soil medium, land cover type, topographic slope, and hydraulic conductivity to construct a modified DRASTIC model for groundwater vulnerability assessment."""
        result3 = test_similarity(method_para, method_rewritten, "方法论改写 (轻度)")

    # 汇总
    print("\n" + "=" * 60)
    print("测试汇总")
    print("=" * 60)

    results = [result1, result2]
    if result3:
        results.append(result3)

    for i, r in enumerate(results, 1):
        print(f"\n测试 {i}:")
        print(f"  综合评分: {r['composite_score']}/100")
        print(f"  LCS 比率: {r['lcs_ratio']:.1%}")
        print(f"  最长连续匹配: {r['max_consecutive']} 词")
        print(f"  评估: {r['assessment']}")

    avg_composite = sum(r['composite_score'] for r in results) / len(results)
    avg_consecutive = sum(r['max_consecutive'] for r in results) / len(results)

    print(f"\n平均值:")
    print(f"  平均综合评分: {avg_composite:.1f}/100")
    print(f"  平均最长连续匹配: {avg_consecutive:.1f} 词")

    if avg_consecutive <= 5 and avg_composite < 60:
        print("\n[PASS] 测试通过: 改写效果良好")
    else:
        print("\n[WARNING] 测试警告: 相似度偏高，需要进一步优化")


if __name__ == "__main__":
    main()

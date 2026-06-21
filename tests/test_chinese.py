import pytest
from analyzer.chinese import analyze_chinese

def test_excessive_le():
    text = "这个方法被证明了是有效的。实验验证了这个结论。我们观察了数据变化了。结果表明了方法的优势了。该方案提高了性能，增强了稳定性。"
    result = analyze_chinese(text)
    assert result["score"] > 0

def test_de_nesting():
    text = "基于深度学习的方法的性能的提升的幅度超过了预期。传统的图像处理的方法的精度的不足的缺陷日益明显。最新的算法的效果的好转的迹象已经出现。"
    result = analyze_chinese(text)
    assert any(i["type"] == "de_nesting" for i in result["issues"])

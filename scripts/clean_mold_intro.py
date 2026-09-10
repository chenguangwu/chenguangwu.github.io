# -*- coding: utf-8 -*-
"""清理 mold 分类 analysis-simulator / analysis-35 的 tool-intro-body intro-scenes 通用默认占位
（'日常办公与学习'等 4 条，_build.py 不重建该区块），替换为真实模具工程场景。
detector-mold 的 intro-scenes 已是真实内容，不处理。
"""
import re

# 通用默认占位 4 条（顺序固定）
OLD = """      <li>日常办公与学习</li>
      <li>开发调试与数据处理</li>
      <li>快速计算与格式转换</li>
      <li>信息查询与参考</li>"""

REPL = {
    "tools/mold/analysis-simulator.html": """      <li>模流填充平衡评估</li>
      <li>冷却均匀性分析</li>
      <li>工艺窗口对比</li>
      <li>试模数据复盘</li>""",
    "tools/mold/analysis-35.html": """      <li>试模缺陷量化</li>
      <li>修模前后对比</li>
      <li>多轮试模稳定性</li>
      <li>供应商试模验收</li>""",
}

for path, new in REPL.items():
    with open(path, encoding="utf-8") as f:
        s = f.read()
    if OLD not in s:
        print("SKIP (no placeholder found):", path)
        continue
    s = s.replace(OLD, new, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(s)
    print("CLEANED:", path)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 uiux 分类 2 个工具页 tool-intro-body 的 intro-scenes 通用默认占位
（日常办公与学习/开发调试与数据处理/快速计算与格式转换/信息查询与参考），
替换为各自真实的 UI/UX 工程使用场景。_build.py 不重建该区块，需手动清理。
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = """      <li>日常办公与学习</li>
      <li>开发调试与数据处理</li>
      <li>快速计算与格式转换</li>
      <li>信息查询与参考</li>"""

REPL = {
    "tools/uiux/generator-38.html": """      <li>UI 文案与提示词批量生成</li>
      <li>配色与图标风格探索</li>
      <li>竞品界面与用户流程梳理</li>
      <li>可用性测试脚本起草</li>""",
    "tools/uiux/analysis-64.html": """      <li>竞品功能清单量化对比</li>
      <li>性能与体验指标横向评测</li>
      <li>多版本差异与差距定位</li>
      <li>评分标准一致性校验</li>""",
}

def main():
    for rel, new in REPL.items():
        p = os.path.join(ROOT, rel)
        with open(p, "r", encoding="utf-8") as f:
            s = f.read()
        if OLD not in s:
            print("SKIP (无占位):", rel); continue
        s = s.replace(OLD, new, 1)
        with open(p, "w", encoding="utf-8") as f:
            f.write(s)
        print("OK 已清理:", rel)

if __name__ == "__main__":
    main()

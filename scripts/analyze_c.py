# -*- coding: utf-8 -*-
"""分析指定行业里【无 formula-box】的工具页特征，辅助 P3b 决策。

输出：slug | h2 | has_calc | has_intro | n_inputs
- has_calc：是否含 function calc() 计算逻辑（= 真计算器）
- has_intro：是否有标准 intro <p>（可注入公式面板的前提）
- n_inputs：输入框数量（>0 说明交互式）

用法：python3 scripts/analyze_c.py surveying energy meteorology
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools")
INTRO_RE = re.compile(r'<p style="font-size:13px;color:var\(--text-muted\);margin-bottom:\d+px;">.*?</p>', re.S)


def analyze(industry):
    d = os.path.join(TOOLS_DIR, industry)
    if not os.path.isdir(d):
        print("!! 行业目录不存在: %s" % industry)
        return
    print("\n===== %s =====" % industry)
    files = sorted(f for f in os.listdir(d) if f.endswith(".html") and f != "index.html")
    for fn in files:
        slug = fn[:-5]
        c = open(os.path.join(d, fn), encoding="utf-8").read()
        if "formula-box" in c:
            continue  # 已升 A，跳过
        if "TOOLBOX-REDIRECT" in c:
            continue  # 已删除的桩，跳过
        h2 = re.search(r"<h2>([^<]*)</h2>", c)
        h2 = h2.group(1) if h2 else ""
        has_calc = "function calc" in c
        has_intro = bool(INTRO_RE.search(c))
        n_in = len(re.findall(r'<input', c))
        if has_calc or has_intro or n_in:
            flag = "C" if not has_intro else "C?"
            print("%s | %s | calc=%s intro=%s in=%d" % (slug, h2, has_calc, has_intro, n_in))
        else:
            # 既无计算也无公式面板，可能是纯展示/知识/记录类
            print("%s | %s | [纯展示/知识类] calc=%s intro=%s in=%d" % (slug, h2, has_calc, has_intro, n_in))


if __name__ == "__main__":
    for ind in sys.argv[1:]:
        analyze(ind)

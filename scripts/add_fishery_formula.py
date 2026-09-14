#!/usr/bin/env python3
"""fishery 分类公式框补充（收口批次 C）：为缺框的计算类工具注入真实公式框。
用法：python3 scripts/add_fishery_formula.py [--apply]
与 scripts/add_optical_formula.py 同构：在首个锚点（tip-box/tabs/scale-row/set-row/tool-result/input-row/subject-row）前插入 formula-box。
"""
import argparse
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools", "fishery")

ANCHORS = [
    "tip-box", "tabs", "scale-row", "set-row", "tool-result", "input-row", "subject-row",
]

FORMULAS = {
    "water-oxygen": (
        "饱和溶氧 DO_sat = 二维线性插值(温度 t, 盐度 s)；饱和度 = 实测溶氧 / DO_sat × 100%",
        "先按水温定位温度区间、按盐度定位盐度区间，做双线性插值得到该条件下的理论饱和溶氧；"
        "饱和度 = 实测 ÷ 饱和 × 100%。分级：<2 危险(浮头)，<4 偏低(开增氧机)，≤8 正常，>8 过饱和(防气泡病)。",
    ),
}


def build_box(eq, desc):
    return (
        '<div class="card formula-box">\n'
        '  <h3>📐 计算公式</h3>\n'
        '  <div class="formula-eq">%s</div>\n'
        '  <p class="formula-desc">%s</p>\n'
        '</div>\n'
    ) % (eq, desc)


def find_anchor(s):
    for a in ANCHORS:
        m = re.search(
            r'<(?:\w+)\b[^>]*\bclass="[^"]*\b%s\b[^"]*"[^>]*>' % re.escape(a), s)
        if m:
            return m.start()
    return -1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    total = len(FORMULAS)
    done = skipped = 0
    for slug, (eq, desc) in FORMULAS.items():
        fp = os.path.join(TOOLS_DIR, slug + ".html")
        if not os.path.isfile(fp):
            print("  缺失: %s" % slug)
            continue
        s = open(fp, encoding="utf-8").read()
        if 'class="formula-box"' in s:
            skipped += 1
            continue
        pos = find_anchor(s)
        if pos < 0:
            print("  无锚点(跳过): %s" % slug)
            continue
        box = build_box(eq, desc)
        s2 = s[:pos] + box + s[pos:]
        if a.apply:
            open(fp, "w", encoding="utf-8").write(s2)
        done += 1
        print("  补框: %s" % slug)
    print("公式框：已补 %d / 缺框 0 / 跳过(已有) %d（共 %d）" % (done, skipped, total))


if __name__ == "__main__":
    main()

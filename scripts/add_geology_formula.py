#!/usr/bin/env python3
"""geology 分类公式框补充（收口批次 C）：为缺框的计算类工具注入真实公式框。
用法：python3 scripts/add_geology_formula.py [--apply]
与 scripts/add_aerospace_formula.py 同构：在首个锚点（tip-box/tabs/scale-row/set-row/tool-result/input-row/subject-row）前插入 formula-box。
"""
import argparse
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools", "geology")

ANCHORS = [
    "tip-box", "tabs", "scale-row", "set-row", "tool-result", "input-row", "subject-row",
]

FORMULAS = {
    "calc-1": (
        "RQD = Σ(长度 ≥ 阈值 的完整岩芯段) / 钻孔总长度 × 100%",
        "岩芯段在裂隙、破碎带处断开；仅计入长度不小于阈值（默认 100 mm）的完整段，本工具按 Deere 标准分级评价岩体质量。",
    ),
    "calc-25": (
        "震中距 D = Δt × Vp × Vs / (Vp − Vs)；角距 = D / 111.32；P 波传播距离 = Δt × Vp",
        "Δt 为 S 波与 P 波到时差，Vp、Vs 为纵波与横波速度；D / 111.32 将千米换算为球面度（1° ≈ 111.32 km）。",
    ),
    "calc-87": (
        "衬度系数 Ac = 异常值 / 背景值；异常下限 T = 背景值 + 2 × 标准差；异常强度 = 异常值 / T",
        "Ac > 1 判为正异常、< 1 为负异常；强度 ≥ 2 为强异常，≥ 1.5 中异常，≥ 1 弱异常，否则落于背景范围。",
    ),
    "weight-sample": (
        "σ² = C · d³ · (1/w − 1) / m；富集因子 (1/w − 1) = (1 − w) / w；σ_rel = √σ²；m_min = C · d³ · (1/w − 1) / (tol_rel)²",
        "按 Gy 采样理论，相对采样方差与颗粒尺寸 d 的三次方成正比、与样品质量 m 成反比（d 单位 cm、m 单位 g、w 为目标品位小数、C 为采样常数）；当相对误差 σ_rel 超过允许值 tol 时，按 m_min 反算最小样重。",
    ),
    "wutanyichangjieyi": (
        "推测埋深 ≈ 异常半宽 W / 1.31（Peters 半宽法）",
        "磁异常幅值 > 500 nT 为高幅值、> 100 nT 中幅值；重力异常 > 5 mGal 为高、> 1 mGal 为中；结合半宽（> 200 m 大范围）与梯度分级判读地质体类型与埋深。",
    ),
    "dizhiyijipinggu": (
        "综合评分 = 类型评分 × 0.3 + 规模评分 × 0.2 + 完整度评分 × 0.2 + 科学价值评分 × 0.3",
        "规模评分按面积分级（> 10 km² 记 5 分、> 1 km² 记 4 分、> 0.1 km² 记 3 分，否则 2 分），完整度评分 = 完整度 / 20，科学价值评分取 0–5；总分 ≥ 4.2 为一级（国家级保护），依次递减至五级。",
    ),
    "dizhiwurandiaochapinggu": (
        "单因子污染指数 Pi = Cn / Sn；超标倍数 = (Cn − Sn) / Sn；地累积指数 Igeo = log₂( Cn / (1.5 × Bn) )",
        "Cn 为实测浓度、Bn 为背景值、Sn 为评价标准值；Igeo < 0 无污染，0–1 无至中度，1–2 中度，2–3 中至强，≥ 3 强污染（Müller 地累积指数分级）。",
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

#!/usr/bin/env python3
"""aerospace 分类公式框补充（收口批次 C）：为缺框的计算类工具注入真实公式框。
用法：python3 scripts/add_aerospace_formula.py [--apply]
与 scripts/add_securities_formula.py 同构：在首个锚点（tip-box/tabs/scale-row/set-row/tool-result/input-row/subject-row）前插入 formula-box。
"""
import argparse
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools", "aerospace")

ANCHORS = [
    "tip-box", "tabs", "scale-row", "set-row", "tool-result", "input-row", "subject-row",
]

FORMULAS = {
    "flight-time": (
        "实际飞行时长 = (到达当地时刻 − 出发当地时刻) + (到达时区 − 出发时区)",
        "先按各自时区换算为同一基准（UTC）再相减，避免跨日与时差误差；结果为空中实际飞行时间，不含地面停场。",
    ),
    "fuel-consumption": (
        "飞行时间 t = 距离 / 巡航速度；航段油 = 耗油率 × t × 航段系数；备份油 = 耗油率 × 备份分钟 / 60；"
        "总油量 = 滑行油 + 航段油 + 备份油；体积 = 总油量 / 0.8（kg/L）",
        "按巡航耗油率与飞行时间估航段油，另加滑行油与备份油得轮挡总油量；航煤密度约 0.8 kg/L，用于换算体积。",
    ),
    "lift-coefficient": (
        "线性段 CL = CLα · (α − α0)，并封顶 CLmax；α > α_stall 后按失速下降修正",
        "升力系数随迎角线性增长，斜率即升力线斜率 CLα；达到最大升力系数 CLmax 后进入失速，本工具对失速后做平滑下降处理。",
    ),
    "runway-length": (
        "ISA 温度 = 15 − 0.0065 × 海拔(m)；修正长 = 基准长 × 重量系数 × (1 + 海拔/300 × 0.07) × (1 + max(0, ΔT) × 0.01) × (1 + 坡度 × 0.10) × (1 − 顶风/5 × 0.07)；建议长 = 修正长 × 1.15",
        "海拔每高 300m 需加长 7%、高于 ISA 每 1℃ 加长 1%、上坡每 1% 加长 10%、顶风每 5m/s 缩短 7%（最多 30%）；再叠加 15% 安全余量。",
    ),
    "weight-balance": (
        "CG = Σ(Wi × Armi) / ΣWi；校核 cgFwd ≤ CG ≤ cgAft",
        "总力矩为各装载项重量乘以其力臂之和，除以总重得重心位置；重心须落在前限 cgFwd 与后限 cgAft 之间，否则配载不可放行。",
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

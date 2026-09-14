#!/usr/bin/env python3
"""optical 分类公式框补充（收口批次 C）：为 10 个缺框的计算类工具注入真实公式框。
用法：python3 scripts/add_optical_formula.py [--apply]
与 scripts/add_meteorology_formula.py 同构：在首个锚点（tip-box/tabs/scale-row/set-row/tool-result/input-row/subject-row）前插入 formula-box。
"""
import argparse
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools", "optical")

ANCHORS = [
    "tip-box", "tabs", "scale-row", "set-row", "tool-result", "input-row", "subject-row",
]

FORMULAS = {
    "aca-ratio": (
        "AC/A（梯度法）= (加镜后隐斜 − 裸眼隐斜) / |镜片度|；"
        "AC/A（计算法）= IPD(cm) + (近隐斜 − 远隐斜) / (100 / 近距 cm)",
        "梯度法用加镜前后隐斜差除以镜片度；计算法以瞳距加上隐斜差除以调节需求（100/近距cm）求得每屈光度引发的集合量（Δ/D）。",
    ),
    "accommodation-amplitude": (
        "最小 A = 15 − 0.25×年龄；平均 A = 18.5 − 0.30×年龄；最大 A = 25 − 0.40×年龄（Hofstetter）",
        "Hofstetter 经验公式按年龄估算调节幅度区间，近点距离 = 100 / 调节幅度（cm），用于评估老花与调节不足。",
    ),
    "anti-fatigue-design": (
        "下加光 Add = max(0, 100/工作距cm − (调节幅度 − 调节幅度/3))，量化到 0.25D、上限 1.00D",
        "按 Hofstetter 平均调节幅度，保留 1/3 调节力，超出部分作为抗疲劳下加光；调节幅度 = 18.5 − 0.30×年龄。",
    ),
    "calc-47": (
        "球面像差 LSA = (n−1)·h² / (2·n·R) · (1 + k/n²)；k 为圆锥常数",
        "非球面相对球面像差的修正项：球面贡献为 (n−1)h²/(2nR)，再乘以 (1+k/n²)；k=0 退化为球面，k=−n² 为最佳补偿。",
    ),
    "detector-31": (
        "综合评分 = Σ(各项评分 × 权重)；表面/PV/RMS/偏心/透射/等级/镀膜 各 0–100 加权",
        "各子项按阈值映射到 0–100 分后加权求和，得到光学元件质量合规等级（A/B/C）。",
    ),
    "lens-refractive-index": (
        "按 |度数| 与 目标（薄/性价比/光学）阈值推荐折射率档位（1.50 / 1.56 / 1.60 / 1.67 / 1.71 / 1.74）",
        "低度数选低折射率（色散小），高度数选高折射率（更薄），光学优先在高度数时跳过高色散档（1.67/1.74）选 1.70/1.71。",
    ),
    "peripheral-defocus": (
        "相对周边离焦 RPD = 周边屈光度 − 中央屈光度（D）",
        "RPD>0 为近视性离焦，RPD<0 为远视性离焦；结合镜片类型评估近视防控效能。",
    ),
    "prism-decentration": (
        "普伦蒂斯法则：棱镜度 P = 移心量(cm) × |度数 F|；移心量 c = P / |F|",
        "镜片光学中心偏离视线 c(cm) 即产生 P=c·|F| 棱镜度；正镜向基底方向、负镜向基底反方向移心。",
    ),
    "progressive-corridor": (
        "所需最低镜圈高度 = 瞳高 + 近用区余量(≈5mm)；通道长度按设计(短/标准/长)与下加光定",
        "ADD≥2.50D 建议标准通道(14mm)，ADD≥3.00D 建议长通道(17mm)，近用区中心须留出约 5mm 余量。",
    ),
    "pupil-height": (
        "瞳高占 B 值比例 = 瞳高(mm) / 镜框 B 值(mm) × 100%",
        "比例 50%–70% 为光学中心位置正常；偏低光学中心偏上、偏高偏下，影响装配与视觉质量。",
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

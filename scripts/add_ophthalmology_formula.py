#!/usr/bin/env python3
"""ophthalmology 分类公式框补充（收口批次 C）：为缺框的 4 个计算类工具注入真实公式框。
用法：python3 scripts/add_ophthalmology_formula.py [--apply]
锚点优先 'input-row'（位于静态表单 markup，不会落在 <script> 内），回退 'card'。
注入前剔除 <script>/<style> 区域，确保 formula-box 不落入脚本。
"""
import argparse
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools", "ophthalmology")

ANCHORS = ["input-row", "card"]


def strip_script_style(s):
    return re.sub(r"<script[\s\S]*?</script>", "", re.sub(r"<style[\s\S]*?</style>", "", s))


FORMULAS = {
    "iol-power": (
        "SRK II：P = A′ − 0.9K − 2.5L（A′ 随眼轴分段校正）；SRK/T：P = 1336/(AL − ELP) − 1336/(1336/K − ELP)，"
        "ELP = pACD + H，pACD = 0.62467A − 68.747，R = 337.5/K，H = R − √(R² − (Cw/2)²)",
        "SRK II 为线性回归式；SRK/T 用 vergence 公式并以 ELP（有效晶状体位置）修正。"
        "目标屈光预留由 vergence 反算：P = 1336/(AL − ELP) − 1336/(1336/K − ELP) − 目标屈光。"
        "眼轴每误差 1 mm 约影响 2.5 D。",
    ),
    "calc-length-1": (
        "K̄ = (K1 + K2)/2；SRK II：P = A′ − 2.5·AL − 0.9·K̄；SRK/T：P = A − 2.5·AL − 0.9·K̄（按眼轴分段修正）；"
        "Hoffer Q 近似：P = 5.45 − 0.87·AL − 0.22·K̄ + 0.5·ACD",
        "三种公式均以眼轴 AL(mm) 与平均角膜曲率 K̄(D) 为核心，A 常数随眼轴分段校正；"
        "结果为正视化（目标屈光度 0 D）的人工晶状体度数估算。",
    ),
    "corneal-endothelium": (
        "细胞密度 CD = 细胞数 / 框面积（cells/mm²）；变异系数 CV = SD / 平均细胞面积；"
        "六角形比例 6A = 六角形细胞数 / 总细胞数 × 100%",
        "CD ≥ 2500 正常、1500–2500 临界、< 1500 低密度；CV < 0.30 正常、0.30–0.40 临界、> 0.40 异常；"
        "六角形比例 ≥ 55% 正常、50%–55% 临界。",
    ),
    "refraction-error": (
        "等效球镜 SE = S + C/2；功率向量 M = S + C/2，J0 = −(C/2)·cos2α，J45 = −(C/2)·sin2α；"
        "柱镜转置：S′ = S + C，C′ = −C，α′ = α + 90°",
        "等效球镜与功率向量把处方分解为球性(M)与两个散光分量(J0/J45)，用于正负柱镜互换、"
        "两片柱镜叠加（过矫）与轴位归一化计算。",
    ),
}


def build_box(eq, desc):
    return (
        '<div class="card formula-box">\n'
        '  <h3>\U0001f4d0 计算公式</h3>\n'
        '  <div class="formula-eq">%s</div>\n'
        '  <p class="formula-desc">%s</p>\n'
        '</div>\n'
    ) % (eq, desc)


def find_anchor(s):
    clean = strip_script_style(s)
    for a in ANCHORS:
        m = re.search(
            r'<(?:\w+)\b[^>]*\bclass="[^"]*\b%s\b[^"]*"[^>]*>' % re.escape(a), clean)
        if m:
            orig = re.search(
                r'<(?:\w+)\b[^>]*\bclass="[^"]*\b%s\b[^"]*"[^>]*>' % re.escape(a), s)
            return orig.start() if orig else m.start()
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
        if 'formula-box' in s:
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

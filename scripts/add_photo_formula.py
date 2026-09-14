#!/usr/bin/env python3
"""photo 分类公式框补充（收口批次 C）：为缺框的 2 个计算类工具注入真实公式框。
用法：python3 scripts/add_photo_formula.py [--apply]
锚点优先 'input-row'（位于静态表单 markup，不会落在 <script> 内），回退 'card'。
注入前剔除 <script>/<style> 区域，确保 formula-box 不落入脚本。
"""
import argparse
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools", "photo")

ANCHORS = ["input-row", "card"]


def strip_script_style(s):
    return re.sub(r"<script[\s\S]*?</script>", "", re.sub(r"<style[\s\S]*?</style>", "", s))


FORMULAS = {
    "calc-exposure-aperture": (
        "EV\u2081\u2080\u2080 = log\u2082(N\u00b2/t) \u2212 log\u2082(S/100)\uff1b"
        "绝对曝光值 EV = log\u2082(N\u00b2/t)\uff1b等效快门 t = 100\u00b7N\u00b2/(S\u00b72^EV\u2081\u2080\u2080)",
        "N 为光圈 f 值，t 为快门时间(s)，S 为 ISO。EV\u2081\u2080\u2080 归一到 ISO 100 便于跨感光度比较；"
        "每差 1 EV 相当于光线亮度差一倍。场景亮度按 EV\u2081\u2080\u2080 分级（雪地正午 \u226516、阳光 16 法则 \u224814、阴天 \u224812、夜景 \u22642）。",
    ),
    "print-size": (
        "打印尺寸 = 像素数 / DPI \u00d7 单位换算（in=1\u3001cm=2.54\u3001mm=25.4）；"
        "百万像素 MP = W\u00d7H/10\u2076；宽高比 = W/H；300DPI 所需像素 = 打印尺寸(in)\u00d7300",
        "W\u00d7H 为像素数，DPI 为打印分辨率。同一张图 DPI 越高，可打印的物理尺寸越小；"
        "300 DPI 为高质量印刷基准，150 DPI 适合大幅海报。宽高比决定照片比例（3:2、4:3、1:1 等）。",
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
    print("公式框：已补 %d / 跳过(已有) %d（共 %d）" % (done, skipped, total))


if __name__ == "__main__":
    main()

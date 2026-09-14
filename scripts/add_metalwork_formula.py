#!/usr/bin/env python3
"""metalwork 分类公式框补充（收口批次 C）：为缺框的 5 个计算类工具注入真实公式框。
用法：python3 scripts/add_metalwork_formula.py [--apply]
锚点优先 'input-row'（位于静态表单 markup，不会落在 <script> 内），回退 'card'。
注入前剔除 <script>/<style> 区域，确保 formula-box 不落入脚本。
"""
import argparse
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools", "metalwork")

ANCHORS = ["input-row", "card"]


def strip_script_style(s):
    return re.sub(r"<script[\s\S]*?</script>", "", re.sub(r"<style[\s\S]*?</style>", "", s))


FORMULAS = {
    "assessor-34": (
        "Rp\u2080 按腐蚀面积分级（GB/T 6461）：0%\u2192Rp10，\u22640.1%\u2192Rp8，\u22641%\u2192Rp5，"
        "\u22648%\u2192Rp3，>25%\u2192Rp0；最终 Rp = max(Rp\u2080 \u2212 0.5\u00b7生锈数 \u2212 0.3\u00b7起泡数 "
        "\u2212 0.5\u00b7开裂数 \u2212 红锈扣分2, 0)",
        "试验时长 \u2265 标准时长、无红锈、且最终评级 \u2265 要求等级时判定合格。Rp 越高耐蚀性越好："
        "\u22659 极优、\u22658 优秀、\u22657 良好；Rp 与起泡/开裂/生锈等级共同决定最终结论。",
    ),
    "cable-tray-sizing": (
        "单根截面积 A\u2081 = \u03c0\u00b7D\u00b2/4；电缆总截面积 A = A\u2081\u00b7N；所需桥架面积 "
        "A_need = A / 填充率；推荐规格取满足「宽\u00d7高 \u2265 A_need」的最小规格；"
        "实际填充率 = A /(宽\u00d7高)\u00d7100%",
        "D 为单根电缆外径(mm)，N 为电缆根数；填充率按用途取 40%（动力）、50%（控制）等。"
        "按面积法选型可保证散热余量与施工空间。",
    ),
    "detector-hardness": (
        "划格法结合力得分：0级\u2192100、1级\u219285、2级\u219265、3级\u219240、4级\u219220、5级\u21920；"
        "拉开法：\u226515 MPa\u2192100、10~15\u219285、5~10\u219265、3~5\u219240；"
        "厚度偏差 = (实测厚度 \u2212 标准厚度)/标准厚度 \u00d7100%",
        "结合力得分 \u2265 要求等级对应分值时结合力判合格；涂层硬度按铅笔硬度或维氏/纳米压痕测定；"
        "厚度偏差应落在允许公差内。三项共同评价涂层质量。",
    ),
    "recorder-9": (
        "保温时间 t = k\u00b7\u03b4 + 20（分钟）；\u03b4 为工件有效厚度(mm)，k 为工艺系数；"
        "参考温度取材料\u00b7工艺区间的中值 T = (T_min + T_max)/2",
        "\u6e17\u78b3工艺按渗层深度估算（约 0.12~0.15 mm/h），保温时间随渗层深度确定；"
        "k 由钢种与工艺决定，用于保证心部到温与组织均匀。目标温度可一键取参考区间中值。",
    ),
    "tester-19": (
        "绝缘电阻温度修正：R\u2082\u2080 = R_t \u00d7 0.5^((t\u221220)/10)；判定 R\u2082\u2080 \u2265 限值"
        "（PVC/XLPE/控制 0.5、10kV XLPE 1.0 M\u03a9\u00b7km）；直流耐压试验电压 U：额定 \u22641kV\u21923.5kV，"
        "\u22648.7kV\u21922.5\u00b7U_N+2000V，>8.7kV\u21922.0\u00b7U_N；试验时间 5 min",
        "绝缘电阻随温度升高而下降，故统一修正到 20\u2103 比较；导体电阻以标准截面值 \u00d71.1 为上限。"
        "绝缘电阻、导体电阻、耐压三项均合格才判定安装检测合格。",
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

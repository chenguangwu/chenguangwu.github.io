#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""eco 分类公式框补充（收口批次 C）：为 4 个缺框的计算类工具注入真实公式框。

缺框页：carbon-offset / solid-waste / waste-calculator / wastewater-calc
（convert-air-aqi 与 recycling-guide 已自带 formula-box，不在本批。）

用法：python3 scripts/add_eco_formula.py [--apply]
与 scripts/add_fitness_formula.py 同构：在首个 markup 锚点前插入 formula-box。
锚点搜索严格排除 <script>/<style> 区间（防把框插进 JS 模板串）。
所有公式逐条对照页面 calc() 实现撰写，不写套话。
"""
import argparse
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools", "eco")

ANCHORS = [
    "tip-box", "tabs", "scale-row", "set-row", "tool-result", "input-row", "subject-row",
]

FORMULAS = {
    "carbon-offset": (
        "月排放 = 交通 + 能源 + 饮食 + 外卖 + 购物 + 衣物；年排放 = 月排放 × 12",
        "交通 = 私家车×0.192 + 公交×0.089 + 短途航班×0.255 + 长途航班×0.195（kg/km，按公里数）；"
        "能源 = 用电×0.583（kg/kWh） + 天然气×2.04（kg/m³）；"
        "饮食按年值（素食 100 / 基本素食 150 / 少量肉 250 / 平均 330 / 高肉 500 kg）除以 12 转月度；"
        "外卖 1.5 kg/次、购物 5 kg/单、新衣 25 kg/件（年值除以 12）。"
        "判定：<2000 kg 低碳、<5000 kg 符合全球平均、<8000 kg 略高、否则偏高；"
        "抵消估算：植树 = ⌈年排放/21⌉ 棵（每树年吸收约 21 kg），光伏 = ⌈年排放/1300⌉ kW（每 kW 年减约 1300 kg）。",
    ),
    "solid-waste": (
        "固废产生量 = 产品产量 × 产污系数；回收量 = 总量 × 回收比例；"
        "处置量 = 总量 × 处置比例；贮存量 = 总量 − 回收量 − 处置量（负值归零）",
        "产污系数取行业典型值（kg/单位）：煤炭采选 300、金属矿采选 1000、钢铁冶炼 400、火力发电 250、"
        "化工 150、建筑材料 50、造纸 200、纺织 60、食品加工 100，可切「自定义」手工填写。"
        "总量以 kg 计，≥1000 kg 时换算显示为吨；回收与处置按百分比拆分流向，剩余部分为贮存/排放，"
        "用于工业企业固废台账与合规核算参考。",
    ),
    "waste-calculator": (
        "月垃圾量 = 基础量 + 食品残渣 + 包装 + 一次性用品 + 衣物；"
        "人均每日 = (月量 × 12 / 人数) / 365",
        "基础量 = 人数 × 1.2 kg/人/天 × (1 + 地区修正)（城区 0、郊区 −0.1、农村 −0.2）；"
        "食品残渣 = 人数 × (烹饪系数 + 剩菜系数) × 30（烹饪：餐餐做 2.5 / 经常 1.5 / 偶尔 0.8 / 几乎不做 0.3；"
        "剩菜：无 0 / 偶尔 0.3 / 较多 0.7，单位 kg/人/天）；"
        "包装 = 外卖次数×4×0.4 + 快递件数×4×0.15 kg；一次性 = 人数 × 系数 × 30（低 0.5 / 中 1.0 / 高 2.0）；"
        "衣物 = 无 0 / 少量 5 / 较多 15 kg。判定以人均每日计：<0.5 极低、<1.0 较低、<1.5 接近平均、否则偏高。",
    ),
    "wastewater-calc": (
        "日排放量 = 流量(m³/h) × 运行小时数；年排放量 = 日排放量 × 年运行天数；"
        "污染物排放量(kg) = 浓度(mg/L) × 体积(m³) / 1000",
        "单位换算：1 m³ = 1000 L，浓度 mg/L × 1000 L = 1000 mg = 1 g，故 kg = mg/L × m³ / 1000。"
        "COD、BOD₅、氨氮、总磷、悬浮物、总氮六项分别按上式换算为日排放量与年排放总量，"
        "用于企业环保合规、排污许可与总量核算参考，结果不作为监测报告依据。",
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


def script_or_style_spans(s):
    """<script>/<style> 区间：锚点搜索必须排除，否则会命中 JS 模板串里的 input-row/tip-box。"""
    spans = []
    for pat in (r'<script\b[\s\S]*?</script>', r'<style\b[\s\S]*?</style>'):
        spans += [(m.start(), m.end()) for m in re.finditer(pat, s, re.I)]
    return spans


def has_formula_box(s):
    """按 class 属性匹配（兼容 card formula-box 等复合类名），避免重复注入。"""
    return bool(re.search(r'class="[^"]*\bformula-box\b[^"]*"', s))


def find_anchor(s):
    spans = script_or_style_spans(s)
    for a in ANCHORS:
        for m in re.finditer(
            r'<(?:\w+)\b[^>]*\bclass="[^"]*\b%s\b[^"]*"[^>]*>' % re.escape(a), s):
            if any(x <= m.start() < y for x, y in spans):
                continue
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
        if has_formula_box(s):
            skipped += 1
            continue
        pos = find_anchor(s)
        if pos < 0:
            print("  无锚点(跳过): %s" % slug)
            continue
        box = build_box(eq, desc)
        s2 = s[:pos] + box + s[pos:]
        # 自检：插入后公式框不得落在 script/style 内
        spans2 = script_or_style_spans(s2)
        i2 = s2.find('class="card formula-box"')
        assert i2 > 0 and not any(x <= i2 < y for x, y in spans2), "%s 插入位置异常" % slug
        if a.apply:
            open(fp, "w", encoding="utf-8").write(s2)
        done += 1
        print("  补框: %s" % slug)
    print("公式框：已补 %d / 缺框 0 / 跳过(已有) %d（共 %d）" % (done, skipped, total))


if __name__ == "__main__":
    main()

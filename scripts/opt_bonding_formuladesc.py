#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bonding 全量：清除 5 个工具页的 formula-desc 占位套话。

对齐 agriculture 范本格式：依据标准/原理 + 真实用途 + 数据不出浏览器，去除
「本计算依据通用财务与货币规则...」/「本校验工具依据对应数据格式与语法规范...」通用免责套话，
保留并提炼真实工具信息。幂等：仅当命中套话前缀才替换；已替换过的文件再次运行不变。
"""
import re
import sys

BASE = "tools/bonding"

REPLACE = {
    "analysis-cost-4.html": (
        "依据成本/效率/替代方案对比逻辑，输入各项粘接方案的材料、工时与设备费用，"
        "输出单位成本与替代经济性排序，辅助选材决策；纯前端计算，数据不出浏览器。"
    ),
    "analysis-resolution.html": (
        "依据粘接故障的常见成因与排查路径，输入工况与失效现象，"
        "输出可能原因与处置建议清单，辅助定位与复盘；纯前端计算，数据不出浏览器。"
    ),
    "assessor-cycle-lifespan.html": (
        "依据疲劳寿命的应力—循环关系（S-N 曲线与 Miner 线性累积损伤准则），"
        "输入载荷谱与材料参数，估算可达循环次数与安全寿命，辅助耐久性判定；"
        "纯前端计算，数据不出浏览器。"
    ),
    "detector-26.html": (
        "依据胶层厚度、均匀度与缺陷的判定阈值，输入实测厚度与公差带，"
        "给出合格/偏薄/偏厚与缺陷风险提示，辅助在线质检；纯前端计算，数据不出浏览器。"
    ),
    "detector-27.html": (
        "依据超声波无损检测的声程与缺陷回波判定规则，输入声速、探头角度与回波位置，"
        "估算缺陷深度与类型，辅助粘接质量评估；纯前端计算，数据不出浏览器。"
    ),
}

PAT = re.compile(r'<p class="formula-desc">.*?</p>', re.S)


def main():
    dry = "--dry" in sys.argv
    for fn, new_desc in REPLACE.items():
        p = f"{BASE}/{fn}"
        html = open(p, encoding="utf-8").read()
        m = PAT.search(html)
        if not m:
            print(f"[SKIP] {fn}: 未找到 formula-desc 块")
            continue
        old = m.group(0)
        if not any(k in old for k in (
            "本计算依据通用财务", "本校验工具依据对应数据格式",
            "本工程计算基于标准物理", "本速查内容依据权威标准",
        )):
            print(f"[SKIP] {fn}: 已是真实说明，无需替换")
            continue
        new = f'<p class="formula-desc">{new_desc}</p>'
        if dry:
            print(f"[DRY] {fn}:\n  - {old[:60]}...\n  + {new[:60]}...")
            continue
        html2 = PAT.sub(new, html, count=1)
        open(p, "w", encoding="utf-8").write(html2)
        print(f"[DONE] {fn}: formula-desc 已替换为真实说明")


if __name__ == "__main__":
    main()

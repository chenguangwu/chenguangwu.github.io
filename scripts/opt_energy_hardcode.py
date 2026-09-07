#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""energy 分类硬编码套话清理 + cat 错标修正。
1) B类套话「工作与生活中的相关计算与查询。」在 6 个文件（opt-guide 适用场景 + FAQ JSON-LD + opt-faq）替换为真实能源场景。
2) tool-intro 领域错标（"科学研究领域"等 19 文件）批量替换为能源电力真实表述。
3) cat 错标修正 2 文件（air-purifier-area finance→energy、calculator-calc-power-usage finance→calculator）。
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDIR = os.path.join(ROOT, "tools/energy")

OLD = "工作与生活中的相关计算与查询。"

REAL_B = {
 "lcoe.html": "家庭光伏与风电项目初投、运维与年发电量核算，对比不同容量机组的度电成本与回收期。",
 "electrical-power.html": "家庭与车间配电回路功率核算、空开与线缆容量选型、设备同时率与负载评估。",
 "air-purifier-area.html": "卧室与客厅按 CADR 与层高选净化器，规划多房间布置数量与运行档位。",
 "energy-efficiency.html": "电器与电机能效对比、变频与围护改造节能收益测算、定位高耗能用电项。",
 "joule-heating.html": "电热器具发热功率核算、导线载流量与发热安全校核、线路损耗 I²R 评估。",
 "fridge-power-estimator.html": "选购冰箱按能效标识估年电费、新旧冰箱耗电对比、优化使用习惯降耗。",
}

TOOLBOX_FIX = [
 ("科学研究领域的在线工具", "能源电力领域的在线工具"),
 ("科学研究工具，采用标准科学公式，计算精准。", "基于标准物理与工程公式，计算精准、结果可信。"),
 ("采用标准科学计算公式", "基于标准物理与工程公式"),
 ("科学实验数据分析", "用电与能耗数据分析"),
 ("物理化学计算", "电功率与能量换算"),
 ("学术研究辅助", "能源方案评估辅助"),
 ("学习科学知识", "学习能源电学知识"),
]

CAT_FIX = {
 "air-purifier-area.html": ("cat=finance,", "cat=energy,"),
 "calculator-calc-power-usage.html": ("cat=finance,", "cat=calculator,"),
}

def main():
    files = [f for f in os.listdir(EDIR) if f.endswith(".html")]
    total_b = 0
    total_fix = 0
    total_cat = 0
    for f in files:
        p = os.path.join(EDIR, f)
        s = open(p, encoding="utf-8").read()
        orig = s
        # 1) B类套话
        if f in REAL_B:
            real = REAL_B[f]
            n = s.count(OLD)
            s = s.replace(OLD, real)
            total_b += n
            if n:
                print(f"[B类] {f}: 替换 {n} 处 -> {real[:24]}...")
        # 2) tool-intro 领域错标
        for a, b in TOOLBOX_FIX:
            c = s.count(a)
            if c:
                s = s.replace(a, b)
                total_fix += c
        # 3) cat 错标
        if f in CAT_FIX:
            old, new = CAT_FIX[f]
            if old in s:
                s = s.replace(old, new, 1)
                total_cat += 1
                print(f"[cat] {f}: {old} -> {new}")
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
    print(f"done. B类替换={total_b}, 领域错标替换={total_fix}, cat修正={total_cat}")

if __name__ == "__main__":
    main()

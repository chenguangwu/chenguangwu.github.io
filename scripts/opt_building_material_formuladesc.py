#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""building-material：清 2 工具页 formula-desc 占位，替换为对齐 agriculture 范本的真实说明。

占位文本（标准两类）：
- analysis-cost-profit-2：本计算依据通用财务与货币规则…工具名称：财务（成本/利润/现金流）分析。
- detector-35：本校验工具依据对应数据格式与语法规范…工具名称：质量（检测/标准/追溯）体系 - 建材质量检测追溯工具…

替换为：依据标准 + 原理 + 用途 + 数据不出浏览器。幂等：仅当命中占位子串才替换（s!=s2 不写）。
支持 --dry 预览。
"""
import re, os, sys

CAT = "building-material"
dry = "--dry" in sys.argv

# 占位子串 → 真实说明（整行替换 <p class="formula-desc">…</p>）
REPL = {
    "本计算依据通用财务与货币规则": (
        '<p class="formula-desc">本工具基于描述统计方法，对输入的建材成本、价格或工程量等数值序列计算总和、'
        '平均值、中位数、极差、方差与标准差，用于材料比价、报价离散度分析与预算执行波动评估。'
        '所有计算在浏览器本地完成，数据不上传服务器。</p>'
    ),
    "本校验工具依据对应数据格式与语法规范": (
        '<p class="formula-desc">本工具依据 GB/T 175（通用水泥）、GB/T 50081（混凝土）、GB/T 5101（烧结砖）、'
        'GB/T 11968（砌块）等标准，对输入的抗压强度、抗折强度等指标自动判定质量等级'
        '（优等品/一等品/合格品/不合格品），并生成含批次编号的可追溯检测报告。'
        '判定与计算均在浏览器本地完成，数据不上传服务器。</p>'
    ),
}

# 精确匹配整行 formula-desc（含占位子串）
PAT = re.compile(r'<p class="formula-desc">.*?</p>', re.S)

changed = 0
skipped = 0
for base, marker in [("analysis-cost-profit-2", "本计算依据通用财务与货币规则"),
                     ("detector-35", "本校验工具依据对应数据格式与语法规范")]:
    f = "tools/%s/%s.html" % (CAT, base)
    if not os.path.exists(f):
        print("NOFILE", base)
        skipped += 1
        continue
    s = open(f, encoding="utf-8").read()
    if marker not in s:
        skipped += 1
        print("NO-PLACEHOLDER", base)
        continue
    new_desc = REPL[marker]
    s2 = PAT.sub(lambda m: new_desc if marker in m.group(0) else m.group(0), s, count=1)
    if s2 != s:
        changed += 1
        if not dry:
            open(f, "w", encoding="utf-8").write(s2)
        print(("DRY " if dry else "OK ") + base)
    else:
        skipped += 1
        print("UNMATCH", base)
print("changed=%d skipped=%d" % (changed, skipped))

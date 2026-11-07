#!/usr/bin/env python3
"""第 49 批补丁 B：calc 入口清明细表（仅 4 页）。

背景：全站 823 页的 `__tbInputGuard` 已被补丁 A 加上「guard 触发即清空明细表」，
但下面 4 页的 guard 不在计算路径上（注到了 copyResult 之类），或页面自带前置校验
先 `return`，导致 calc 早退时 `#<pre>Table` 明细表保留上一组参数的行 ⇒
「导出明细 CSV」把旧数据当成本次结果带走。

做法：在页面 `function calc(...)` 函数体开头插入一行清表。成功路径末尾的
`__<pre>Render()` 会用 `TBKit.matrix.table`（首行 `box.innerHTML=''`）重写容器，
因此对正常结果无影响；只有早退路径会留下空表。
幂等：已插过标记的不重复插。

审计/复验：scripts/_audit_guard_stale_table.mjs（全量）、
scripts/_verify_guard_clear_table.mjs（门禁 #232 的 12 页固定样本）。
"""
import re, pathlib

MARK = '__tbClearDetailStart'
FILES = [
    'tools/cardiology/ckd-epi.html',
    'tools/nephrology/shenxiaoqiulvguolv-24h-jiganqingchu-ccr.html',
    'tools/marketing/marketing-ltv-cac-ratio.html',
    'tools/ophthalmology/iol-power.html',
]

changed = 0
for f in FILES:
    p = pathlib.Path(f)
    s = p.read_text(encoding='utf-8')
    m = re.search(r"matrix\.table\('#([A-Za-z0-9_]+Table)'", s)
    if not m:
        print('SKIP no-table', f); continue
    tbl = m.group(1)
    if MARK in s:
        print('SKIP done', f); continue
    fm = re.search(r'\nfunction (calc|calcTool|calculate)\s*\(([^)]*)\)\s*\{\n', s)
    if not fm:
        print('SKIP no-calc', f); continue
    ins = f"var __tbT=document.getElementById('{tbl}');if(__tbT)__tbT.innerHTML='';/*{MARK}*/\n"
    p.write_text(s[:fm.end()] + ins + s[fm.end():], encoding='utf-8')
    changed += 1
    print('PATCH', f, '->', fm.group(1), 'tbl', tbl)
print('changed', changed)

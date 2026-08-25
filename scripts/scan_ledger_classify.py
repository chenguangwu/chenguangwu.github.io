#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# B-OPT22 精细分类：48 候选中，哪些是"纯本地记录本"(该删)，哪些有真实效用(保留)。
import os, re, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")

KW = re.compile(r'记录|台账|记账|账本|日志|清单|备忘|笔记|收支|明细|追踪|打卡|习惯|待办|todo|tracker|record|ledger|note|history|历史')
CALC = re.compile(r'function\s+calc\s*\(|calc\s*=\s*function|calc\s*=\s*function')
LS = re.compile(r'localStorage\.(setItem|getItem)')
ADDDEL = re.compile(r'addItem|removeItem|deleteItem|push\(|splice\(|appendChild|条目|记录项|新增|删除')
TIMER = re.compile(r'setInterval|setTimeout|requestAnimationFrame|Date\.now|new Date\(|countdown|倒计时|提醒|remind')
GEN = re.compile(r'模板|template|生成|generator|innerHTML\s*=\s*`|document\.write')
VIZ = re.compile(r'<canvas|getContext|Chart|Plotly|echarts|createElementNS|Highcharts|\.svg')
SCORE = re.compile(r'progress|score|评分|进度|percent|%|完成度')
REF = re.compile(r'参考|手册|百科|知识|词条|cheat|速查|介绍|说明')

def classify(h):
    reasons = []
    if CALC.search(h): reasons.append("有function calc真计算")
    if TIMER.search(h): reasons.append("有定时/倒计时/提醒")
    if GEN.search(h): reasons.append("有模板/文档生成")
    if VIZ.search(h): reasons.append("有可视化")
    if SCORE.search(h): reasons.append("有进度/评分")
    if REF.search(h): reasons.append("有参考资料属性")
    return reasons

delete, keep = [], []
for hp in glob.glob(os.path.join(TOOLS, "*", "*.html")):
    try: h = open(hp, encoding="utf-8").read()
    except: continue
    if not LS.search(h) or CALC.search(h): continue
    name = re.search(r'<title>(.*?)</title>', h); name = name.group(1) if name else ""
    desc = re.search(r'<meta name="description" content="(.*?)"', h); desc = desc.group(1) if desc else ""
    if not KW.search(name+" "+desc): continue
    if not ADDDEL.search(h): continue
    rel = os.path.relpath(hp, ROOT)
    r = classify(h)
    if r:
        keep.append((rel, r))
    else:
        delete.append(rel)

print(f"【该删·纯本地记录本】{len(delete)} 个:")
for d in delete: print("   ", d)
print(f"\n【保留·有真实效用】{len(keep)} 个:")
for rel, r in keep:
    print(f"   {rel}  ->  {'; '.join(r)}")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# B-OPT22 候选识别：纯前端"记录/台账"型工具
# 保守标准：① 含 localStorage.setItem(本地持久化) ② 无 function calc/calc=function(无真计算)
#          ③ 名称或描述含记录类关键词 ④ 存在"增删条目"的列表式 UI 痕迹
import os, re, glob, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")

KW = re.compile(r'记录|台账|记账|账本|日志|清单|备忘|笔记|收支|明细|追踪|打卡|习惯|待办|todo|tracker|record|ledger|note|history|历史')
CALC = re.compile(r'function\s+calc\s*\(|calc\s*=\s*function|calc\s*=\s*function')
LS = re.compile(r'localStorage\.(setItem|getItem)')
ADDDEL = re.compile(r'addItem|removeItem|deleteItem|push\(|splice\(|appendChild|条目|记录项|新增|删除')

cands = []
for hp in glob.glob(os.path.join(TOOLS, "*", "*.html")):
    try:
        h = open(hp, encoding="utf-8").read()
    except Exception:
        continue
    if not LS.search(h):
        continue
    if CALC.search(h):
        continue  # 有真计算，跳过高估风险
    name = re.search(r'<title>(.*?)</title>', h)
    name = name.group(1) if name else ""
    desc = re.search(r'<meta name="description" content="(.*?)"', h)
    desc = desc.group(1) if desc else ""
    text = name + " " + desc
    if not KW.search(text):
        continue
    if not ADDDEL.search(h):
        continue
    rel = os.path.relpath(hp, ROOT)
    cands.append(rel)

print(f"候选纯前端记录/台账型工具: {len(cands)}\n")
for c in cands:
    print(" ", c)

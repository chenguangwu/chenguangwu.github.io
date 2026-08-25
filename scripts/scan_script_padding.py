#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# B-OPT20 前哨：对 1106 个"脚本>=6000字符"撑 A 的工具，计算代码密度，
# 标记"被注水"脚本（注释+空白占比过高 / 重复行多 / 无实际计算），交人工复核。
import os, re, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = json.load(open(os.path.join(ROOT, "tools.json"), encoding="utf-8"))

def inline_scripts(h):
    return re.findall(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', h, re.S)

def strip_js_comments(s):
    # 去 /* */ 与 // 行注释（粗略）
    s = re.sub(r'/\*.*?\*/', ' ', s, flags=re.S)
    s = re.sub(r'//[^\n]*', ' ', s)
    return s

def metrics(h):
    scripts = inline_scripts(h)
    total = sum(len(s) for s in scripts)
    if total == 0:
        return None
    # 合并去注释
    merged = strip_js_comments("\n".join(scripts))
    lines = merged.split("\n")
    code_chars = sum(len(l.strip()) for l in lines)
    ws = sum(len(l) - len(l.strip()) for l in lines) + merged.count(" ") + merged.count("\t") + merged.count("\n")
    comment_chars = total - len(merged)  # 注释被替换成空格，粗略
    # 重复行检测（去空去缩进后完全相同的行）
    norm = [l.strip() for l in lines if l.strip()]
    from collections import Counter
    cnt = Counter(norm)
    dup_lines = sum(v - 1 for v in cnt.values() if v > 1)
    density = code_chars / total if total else 0
    has_calc = ("function calc(" in h) or ("calc=function" in h) or ("calc = function" in h)
    has_math = bool(re.search(r'Math\.|[\+\-\*/]=|\breturn\b', merged))
    return dict(total=total, code=code_chars, density=round(density, 3),
                dup_lines=dup_lines, has_calc=has_calc, has_math=has_math,
                nlines=len(norm))

rows = []
for d in data:
    if d.get("quality") != "A":
        continue
    p = os.path.join(ROOT, "tools", d.get("path", ""))
    if not os.path.exists(p):
        continue
    h = open(p, encoding="utf-8").read()
    if "formula-box" in h:
        continue
    scripts = inline_scripts(h)
    total = sum(len(s) for s in scripts)
    if total < 6000:
        continue
    m = metrics(h)
    # 注水信号：代码密度低(<0.45) 或 重复行多(>40) 或 无计算无math
    padded = (m["density"] < 0.45) or (m["dup_lines"] > 40) or (not m["has_calc"] and not m["has_math"])
    rows.append((d.get("path"), m["total"], m["density"], m["dup_lines"],
                 m["has_calc"], m["has_math"], padded))

padded_rows = [r for r in rows if r[6]]
print(f"脚本>=6000 撑A 工具总数: {len(rows)}")
print(f"疑似注水/堆砌(低代码密度/多重复行/无计算): {len(padded_rows)}\n")
print(f"{'path':<42}{'chars':>7}{'dens':>6}{'dup':>5}  calc math")
for r in sorted(padded_rows, key=lambda x: x[2]):
    print(f"{r[0]:<42}{r[1]:>7}{r[2]:>6}{r[3]:>5}  {int(r[4])}    {int(r[5])}")

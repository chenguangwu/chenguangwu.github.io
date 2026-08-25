#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 枚举全站 formula-box 工具，按行业统计分布，输出抽样候选。
import os, re, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")

FB = re.compile(r'<div class="formula-box".*?</div>\s*</div>', re.S)
EQ = re.compile(r'<div class="formula-eq">(.*?)</div>', re.S)
IND = re.compile(r'/tools/([^/]+)/')

def strip(s):
    return re.sub(r'\s+', ' ', s or '').strip()

by_ind = {}
total = 0
for hp in glob.glob(os.path.join(TOOLS, "*", "*.html")):
    try:
        h = open(hp, encoding="utf-8").read()
    except Exception:
        continue
    if "formula-box" not in h:
        continue
    m = IND.search(hp)
    ind = m.group(1) if m else "?"
    eqs = EQ.findall(h)
    eq = strip(eqs[0]) if eqs else ""
    by_ind.setdefault(ind, []).append((os.path.relpath(hp, ROOT), eq))
    total += 1

# 行业分布
dist = {k: len(v) for k, v in by_ind.items()}
dist_sorted = sorted(dist.items(), key=lambda x: -x[1])
print(f"总 formula-box 工具: {total}")
print(f"涉及行业数: {len(dist_sorted)}\n")
print(f"{'行业':<24}{'数量':>6}")
for ind, n in dist_sorted:
    print(f"{ind:<24}{n:>6}")

# 写出 JSON 供抽样
with open(os.path.join(ROOT, "scripts", "_fb_index.json"), "w", encoding="utf-8") as f:
    json.dump(by_ind, f, ensure_ascii=False, indent=1)
print("\n已写出 scripts/_fb_index.json")

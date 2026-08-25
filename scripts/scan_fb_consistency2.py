#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 改进版：栈式抽取 formula-eq（支持嵌套 div），去标签后判数学信号。
# 高置信可疑两类：
#  A) desc_no_math : formula-eq 去标签后非空但无数学符号 → 描述型假公式(高价值)
#  B) empty_eq     : formula-eq 抽取为空(可能嵌套<code>未吃到) → 需人工看
import os, re, glob, json, html as htmlmod

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")
IND = re.compile(r'/tools/([^/]+)/')

MATHSIG = re.compile(
    r'[+\-*/^=×÷·]|'
    r'\d|'
    r'(?:Math\.)?(?:sin|cos|tan|asin|acos|atan|log|ln|exp|sqrt|pow|abs|floor|ceil|round)|'
    r'[α-ωΑ-Ω]|'
    r'[A-Za-z][²³ⁿ]|'
    r'[A-Za-z]+\(|'
    r'\^|√|％|%'
)

def extract_block(h, cls):
    # 找到 <div class="cls" ...> 起点，用栈配对到对应 </div>
    pat = re.compile(r'<div class="%s"[^>]*>' % re.escape(cls))
    m = pat.search(h)
    if not m:
        return None
    i = m.end()
    depth = 1
    j = i
    while j < len(h):
        if h.startswith("<div", j):
            depth += 1; j = h.find(">", j) + 1
        elif h.startswith("</div>", j):
            depth -= 1; j += 6
            if depth == 0:
                return h[m.end():j-6]
        else:
            j += 1
    return None

def strip_tags(s):
    s = re.sub(r'<[^>]+>', ' ', s or '')
    return htmlmod.unescape(re.sub(r'\s+', ' ', s)).strip()

rows = []
for hp in glob.glob(os.path.join(TOOLS, "*", "*.html")):
    try:
        h = open(hp, encoding="utf-8").read()
    except Exception:
        continue
    if "formula-box" not in h:
        continue
    blk = extract_block(h, "formula-eq")
    eq = strip_tags(blk) if blk is not None else ""
    m = IND.search(hp)
    ind = m.group(1) if m else "?"
    rel = os.path.relpath(hp, ROOT)

    if eq == "":
        rows.append({"file": rel, "ind": ind, "eq": "", "flag": "empty_eq"})
    elif not MATHSIG.search(eq):
        rows.append({"file": rel, "ind": ind, "eq": eq[:160], "flag": "desc_no_math"})

print(f"命中可疑工具: {len(rows)}\n")
# 先统计 flag 分布
from collections import Counter
c = Counter(r["flag"] for r in rows)
print("分布:", dict(c), "\n")
for r in rows:
    print(f"[{r['flag']}] {r['file']}")
    if r["eq"]:
        print(f"    eq: {r['eq']}")

with open(os.path.join(ROOT, "scripts", "_fb_suspect2.json"), "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=1)
print(f"\n已写出 scripts/_fb_suspect2.json ({len(rows)} 条)")

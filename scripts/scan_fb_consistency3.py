#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 鲁棒抽取 formula-box 内的"等式文本"：
#  1) 栈式抽取 <div class="formula-box" ...> 整块
#  2) 去掉 formula-title / formula-desc 子块
#  3) 优先取 .formula-eq 或 .formula 子块；否则取剩余文本（如凯撒密码直接写在框内）
#  4) 去标签 + unescape → 等式文本
# 判定：空 → empty_eq(需人工)；含文本但无数学符号 → desc_no_math(高价值)
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
    r'\^|√|％|%|mod|MOD'
)

def find_block(h, cls):
    pat = re.compile(r'<div class="%s"[^>]*>' % re.escape(cls))
    m = pat.search(h)
    if not m:
        return None
    i = m.end(); depth = 1; j = i
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

def get_eq(h):
    fb = find_block(h, "formula-box")
    if fb is None:
        return None
    # 去掉 title / desc
    tmp = fb
    for cls in ("formula-title", "formula-desc"):
        b = find_block(tmp, cls)
        if b is not None:
            tmp = tmp.replace(f'<div class="{cls}"', f'\x00<div class="{cls}"', 1)
    # 用占位去掉
    # 更简单：直接移除 title/desc 块文本
    cleaned = fb
    for cls in ("formula-title", "formula-desc"):
        cb = find_block(cleaned, cls)
        if cb is not None:
            full = cleaned[cleaned.find(f'<div class="{cls}"'):]
            end = full.find("</div>") + 6
            # 找到对应闭合（粗略：取从 <div class=cls 到第一个 </div> 后 匹配深度）——用 find_block 已得 cb
            start_idx = cleaned.find(f'<div class="{cls}"')
            # 计算 cb 在 cleaned 中的结束位置
            seg = find_block(cleaned, cls)
            seg_full = cleaned[cleaned.find(f'<div class="{cls}"'):]
            seg_full = seg_full[:seg_full.find("</div>")+6]
            cleaned = cleaned.replace(seg_full, "", 1)
    # 取 .formula-eq 或 .formula 子块
    for cls in ("formula-eq", "formula"):
        sub = find_block(cleaned, cls)
        if sub is not None:
            return strip_tags(sub)
    # 否则取剩余文本
    return strip_tags(cleaned)

rows = []
for hp in glob.glob(os.path.join(TOOLS, "*", "*.html")):
    try:
        h = open(hp, encoding="utf-8").read()
    except Exception:
        continue
    if "formula-box" not in h:
        continue
    eq = get_eq(h)
    if eq is None:
        continue
    m = IND.search(hp)
    ind = m.group(1) if m else "?"
    rel = os.path.relpath(hp, ROOT)
    if eq == "":
        rows.append({"file": rel, "ind": ind, "eq": "", "flag": "empty_eq"})
    elif not MATHSIG.search(eq):
        rows.append({"file": rel, "ind": ind, "eq": eq[:160], "flag": "desc_no_math"})

from collections import Counter
c = Counter(r["flag"] for r in rows)
print(f"命中可疑工具: {len(rows)}  分布: {dict(c)}\n")
for r in rows:
    print(f"[{r['flag']}] {r['file']}")
    if r["eq"]:
        print(f"    eq: {r['eq']}")
with open(os.path.join(ROOT, "scripts", "_fb_suspect3.json"), "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=1)
print(f"\n已写出 scripts/_fb_suspect3.json ({len(rows)} 条)")

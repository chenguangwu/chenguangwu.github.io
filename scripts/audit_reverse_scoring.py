#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""反向计分扫描（只报不改）。

判据：
  1) 页面文字声明「反向计分 / 反向条目 / 反向题」；
  2) 页面 JS 是否真的做了分值翻转（`max+1-v`、`(总分+最小分)-原始分`、`reverseScore()`、
     `REV`/`revItems` 数组、`Math.abs` 之外的减法）；
  3) 声明有、代码全是正向累加 ⇒ 缺陷候选（总分被系统性抬高）。

输出 /tmp/reverse_scan.json，控制台按影响排序打印 Top 20。
用法：python3 scripts/audit_reverse_scoring.py [--all]
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")

DECL_RE = re.compile(r"反向(?:计分|评分|条目|题|赋分|编码)")
REV_NAME_RE = re.compile(r"\b\w*_?REV[A-Z_]*\s*=\s*\[|\b\w*_?REV\[|FWD\s*=\s*\{|FWD\[|reverseScore|revScore|reverseItem", re.I)
# 分值翻转的常见写法（只收「量表分值翻转」特有的形态，避免普通算术误命中）
FLIP_PATTERNS = [
    (r"(?:max|MAX|最大值|\bhi\b)[^\n]{0,20}\+\s*1\s*-", "max+1-v"),
    (r"\(\s*\d+\s*\+\s*1\s*\)\s*-", "(N+1)-v"),
    (r"(?<![.\w])(?:4|5|6|7|8|10)\s*[-−]\s*(?:v|raw|val|t)\b", "N - 原始分"),
    (r"\(\s*\d+\s*[-−]\s*[A-Za-z_$][\w$]*\s*\[", "(N - 数组项)"),
]
ITEM_IDS_RE = re.compile(r"第\s*([\d、,，和及\s]{2,20})\s*(?:题|项|条目)[^\n]{0,10}反向")


def read(p):
    with io.open(p, encoding="utf-8", errors="ignore") as f:
        return f.read()


def with_external_scripts(html, page_path):
    """把页面引用的本地外置脚本内容拼进来（反向逻辑常写在 js/tools/*.js）。"""
    extra = []
    for src in re.findall(r'<script[^>]*src="([^"]+)"', html):
        s = src.split("?")[0]
        if s.startswith("http"):
            continue
        cand = os.path.normpath(os.path.join(os.path.dirname(page_path), s))
        if not os.path.exists(cand):
            cand = os.path.normpath(os.path.join(ROOT, s.lstrip("./")))
        if os.path.exists(cand) and cand.endswith(".js") and (
                "/js/tools/" in s.replace("\\", "/") or os.path.basename(cand) == os.path.basename(page_path).replace(".html", ".js")):
            extra.append(read(cand))
    return html + "\n" + "\n".join(extra)


def reverse_decl_count(html):
    n = 0
    items = []
    for m in ITEM_IDS_RE.finditer(html):
        ids = re.findall(r"\d+", m.group(1))
        if ids:
            n += len(ids)
            items.extend(ids)
    if not n and DECL_RE.search(html):
        n = 1
    return n, items


def has_flip(html):
    hits = []
    for pat, label in FLIP_PATTERNS:
        if re.search(pat, html):
            hits.append(label)
    if REV_NAME_RE.search(html):
        hits.append("reverse/REV 命名")
    return hits


def scan():
    rows = []
    for ind in sorted(os.listdir(TOOLS)):
        d = os.path.join(TOOLS, ind)
        if not os.path.isdir(d) or ind.startswith("_"):
            continue
        for name in sorted(os.listdir(d)):
            if not name.endswith(".html") or name == "index.html":
                continue
            p = os.path.join(d, name)
            raw = read(p)
            if "反向" not in raw:
                continue
            html = with_external_scripts(raw, p)
            n_items, ids = reverse_decl_count(raw)
            flips = has_flip(html)
            # 影响：声明反向条目却无翻转实现
            handled = ("max+1-v" in flips or "(N+1)-v" in flips
                       or "(N - 数组项)" in flips or "N - 原始分" in flips
                       or "reverse/REV 命名" in flips)
            defect = bool(n_items) and not handled
            rows.append({
                "page": f"{ind}/{name}",
                "reverse_items": n_items,
                "ids": ids,
                "flip": flips,
                "defect": defect,
                "decl": bool(DECL_RE.search(html)),
            })
    rows.sort(key=lambda r: (not r["defect"], -r["reverse_items"], r["page"]))
    with io.open("/tmp/reverse_scan.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)
    defects = [r for r in rows if r["defect"]]
    print(f"含「反向」字样页 {len(rows)} 个；缺陷候选（声明反向但代码无翻转）{len(defects)} 个")
    for r in defects[:20]:
        print(f"· {r['page']:52s} 反向条目≈{r['reverse_items']:<3} ids={r['ids'][:8]} 翻转={r['flip'] or '无'}")


if __name__ == "__main__":
    scan()

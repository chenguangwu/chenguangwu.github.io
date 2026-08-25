#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B-OPT15 · 清理"通用算术壳"垃圾工具。
签名特征：calc 内 const r=p0*p1;const s2=p0+p1;const d=p0-p1;const m=p1?p0/p1:0
——对任意两个输入只做 ×/+/−/÷ 并硬套标题关键词显示，无任何真实计算逻辑，标题纯属误导。
与 P4 清理的 score=(a+b)/2 壳同类，转重定向桩（保留旧 URL，零死链）。
"""
import os, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")
SIG = re.compile(r'p0\*p1;const s2=p0\+p1;const d=p0-p1;const m=p1\?p0/p1:0')
REDIRECT = re.compile(r'TOOLBOX-REDIRECT')

def get_title(h):
    m = re.search(r'<title>([^<]*)</title>', h)
    return m.group(1).replace(' - ToolBox', '').strip() if m else '工具'

def main():
    targets = []
    for dp, _, fns in os.walk(TOOLS):
        for fn in fns:
            if not fn.endswith('.html'):
                continue
            p = os.path.join(dp, fn)
            try:
                h = open(p, encoding='utf-8', errors='ignore').read()
            except Exception:
                continue
            if REDIRECT.search(h):
                continue
            if SIG.search(h):
                industry = os.path.basename(dp)
                title = get_title(h)
                targets.append((p, industry, title))
    print(f"待清理通用算术壳: {len(targets)}")
    done = 0
    for p, industry, title in targets:
        stub = f"""<!DOCTYPE html>
<!-- TOOLBOX-REDIRECT -->
<html lang="zh-CN"><head><meta charset="UTF-8">
<meta http-equiv="refresh" content="0;url=/tools/{industry}/index.html">
<link rel="canonical" href="/tools/{industry}/index.html"><title>{title} - ToolBox</title></head>
<body><p>该工具已整合至 <a href="/tools/{industry}/index.html">对应分类页</a>。</p>
<script>window.location.href='/tools/{industry}/index.html';</script></body></html>
"""
        open(p, 'w', encoding='utf-8').write(stub)
        done += 1
    print(f"已转重定向桩: {done}")

if __name__ == '__main__':
    main()

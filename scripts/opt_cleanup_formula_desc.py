#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""站点级清除工具页 <x class="formula-desc"> 内的「工具名称：」SEO 模板尾巴。

背景：每个工具页 tool-intro-body 内有一段 <p class="formula-desc">，绝大多数内容为
模板生成的低质 SEO 描述：「本工具基于标准…结果仅供参考。 工具名称：X - XX在线工具。」
（或「工具名称：X - 工具，按…计算…」）。这类段与页面标题冗余、无实质信息，属介绍级
套话，home 批（2026-09-09）发现并留待专项清理。

分界标志：段内含「工具名称：」即判为 SEO 套话段；不含「工具名称：」的 formula-desc
（如 assessor-1 的「依据 GB/T 8097…损失率=…」）是真实公式说明，必须保留。

做法：匹配单个 formula-desc 叶子段（p/div/span），段内含「工具名称：」则整段删除
（含前后空白），否则原样保留。幂等：s2==s 不写。支持 --cat <category> 限定、--dry 预览。

注意：_build.py 不生成 formula-desc（它只注入 TOOLBOX-DEEP-DIVE 块），故删源 html 后
build 不会重建该段，安全。删除不影响页面布局（formula-desc 为独立叶子段落）。
"""
import re, glob, sys, os

CATS = None
if "--cat" in sys.argv:
    CATS = [sys.argv[sys.argv.index("--cat") + 1]]
dry = "--dry" in sys.argv

# formula-desc 叶子段（p/div/span，容错其它属性），非贪婪到同标签闭合
PAT = re.compile(
    r'<(?P<t>p|div|span)[^>]*class="formula-desc"[^>]*>(?P<inner>.*?)</(?P=t)>',
    re.S,
)

roots = ["tools/*/*.html"] if CATS is None else ["tools/%s/*.html" % c for c in CATS]

files_changed = 0
segs_removed = 0
kept_real = 0  # 保留的真实 formula-desc 段（不含工具名称）
unmatched = 0


def repl(m):
    global segs_removed, kept_real
    inner = m.group("inner")
    if "工具名称：" in inner:
        segs_removed += 1
        return ""  # 删除整段（含前后空白由外层 strip 处理）
    kept_real += 1
    return m.group(0)


for rg in roots:
    for f in sorted(glob.glob(rg)):
        if f.endswith("index.html"):
            continue
        s = open(f, encoding="utf-8").read()
        if 'class="formula-desc"' not in s:
            continue
        s2 = PAT.sub(repl, s)
        if s2 != s:
            # 顺手收掉删除后产生的多余空行（>2 连续换行压成 2）
            s2 = re.sub(r"\n{3,}", "\n\n", s2)
            files_changed += 1
            if not dry:
                open(f, "w", encoding="utf-8").write(s2)
            if 'class="formula-desc"' in s2 and '工具名称：' in s2:
                unmatched += 1
                print("RESIDUAL %s" % f)
            else:
                print(("DRY " if dry else "OK ") + f)

print("files_changed=%d segs_removed=%d kept_real_formula_desc=%d unmatched=%d"
      % (files_changed, segs_removed, kept_real, unmatched))

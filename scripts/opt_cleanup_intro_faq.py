#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""站点级清除硬编码 intro-faq-item 套话（"这个工具是免费的吗？""计算结果准确吗？"等）。

该块位于每个工具页 <div class="tool-intro-body"> 内的 <h4>常见问题</h4> + N 个
<div class="intro-faq-item">（含嵌套 intro-faq-q / intro-faq-a）。它不属于 _build.py
生成内容（_build.py 仅在分类首页生成 tool-intro，且不含 intro-faq），是此前所有批次
都漏清的源 html 硬编码套话，线上 3137 个文件带此块。

做法：匹配 常见问题 h4 + 其后全部 intro-faq-item（精确处理嵌套 div），整段删除。
幂等：s2==s 不写。支持 --cat <category> 限定范围、--dry 预览。

注意：凡引 common.js 的工具页均含此块；删除后工具页仅保留 opt-faq（真实 FAQPage
已注入），不再有重复/套话的常见问题区。
"""
import re, glob, os, sys

CATS = None
if "--cat" in sys.argv:
    CATS = [sys.argv[sys.argv.index("--cat") + 1]]
dry = "--dry" in sys.argv

# 常见问题 h4（限定在单个 h4 内，避免跨 h4 误吞） + 其后全部 intro-faq-item
PAT = re.compile(
    r'<h4>(?:(?!</h4>).)*?常见问题(?:(?!</h4>).)*?</h4>'
    r'\s*(?:<div class="intro-faq-item">\s*<div class="intro-faq-q">.*?</div>'
    r'\s*<div class="intro-faq-a">.*?</div>\s*</div>\s*)+',
    re.S,
)

roots = ["tools/*/*.html"] if CATS is None else ["tools/%s/*.html" % c for c in CATS]

files_changed = 0
items_removed = 0
unmatched = 0
for rg in roots:
    for f in sorted(glob.glob(rg)):
        if f.endswith("index.html"):
            continue
        s = open(f, encoding="utf-8").read()
        if 'class="intro-faq-item"' not in s:
            continue
        s2 = PAT.sub("", s, count=0)
        if s2 != s:
            n = s.count('class="intro-faq-item"')
            files_changed += 1
            items_removed += n
            if not dry:
                open(f, "w", encoding="utf-8").write(s2)
            # 若删除后仍有残留（结构异常），报警
            if 'class="intro-faq-item"' in s2:
                unmatched += 1
                print("UNMATCHED-RESIDUAL %s" % f)
            else:
                print(("DRY " if dry else "OK ") + f)
        else:
            # 有 intro-faq-item 但正则未匹配（h4 文案异常），报警待查
            unmatched += 1
            print("UNMATCHED-NOMATCH %s" % f)

print("files_changed=%d items_removed=%d unmatched=%d"
      % (files_changed, items_removed, unmatched))

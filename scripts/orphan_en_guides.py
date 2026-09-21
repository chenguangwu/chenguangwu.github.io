#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""孤儿化 guides/*.en.html 英文副本（2026-09-21 老板指令）。

策略：文件保留一个月，但切断所有引用，让搜索引擎自然脱落、权重由 ?lang=en-US 承接。
本脚本只改「简体指南页」对 .en.html 的引用，不删 .en.html 文件本身：
  1) <head> 的 <link rel="alternate" hreflang="en-US" href="...en.html"> 整行移除
     —— 不能改成 ?lang=en-US：zh-tw 副本里会变成 /zh-tw/...?lang=en-US 死链。
     英文态仍由页面通用 ?lang=en-US 运行时切换提供，不显式声明（与站内其余指南页一致）。
  2) <body> 的 <a ... data-en-guide-link>🌐 English</a> 整段移除（同上，避免死链）。

（sitemap 排除在 _build.py 的 generate_sitemap/generate_core_sitemap 中处理）

幂等：已无 .en.html 引用及 en-US alternate 的页面不会重复改动。
"""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDES = os.path.join(ROOT, 'guides')

# 1) 删除 head 里 en-US 的 alternate link（兼容已改成 ?lang=en-US 的绝对链接与原始 .en.html 链接）
pat_head_del = re.compile(r'\s*<link[^>]*hreflang="en-US"[^>]*>\s*')
# 2) 删除 body 里 data-en-guide-link 英文入口
pat_body_del = re.compile(r'<a[^>]*data-en-guide-link[^>]*>.*?</a>', re.S)

total = changed = 0
for f in sorted(glob.glob(os.path.join(GUIDES, '*-guide.html'))):
    bn = os.path.basename(f)
    if bn.endswith('.en.html') or bn == 'index.html':
        continue
    s = open(f, encoding='utf-8').read()
    orig = s
    s2 = pat_head_del.sub('', s)
    s2 = pat_body_del.sub('', s2)
    if s2 != orig:
        open(f, 'w', encoding='utf-8').write(s2)
        changed += 1
        n_head = len(pat_head_del.findall(orig))
        n_body = 1 if 'data-en-guide-link' in orig else 0
        print('  %s (head_enUS_removed=%d body_removed=%d)' % (bn, n_head, n_body))
    total += 1

print('扫描简体指南页: %d  已改: %d' % (total, changed))

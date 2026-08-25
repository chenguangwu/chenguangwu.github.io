#!/usr/bin/env python3
"""一次性修补：统一工具页使用指南链接文案为 `📖 查看「{title}」`（title 兜底带"使用指南"）。

背景：Q6 第一次生成的 117 个工具页含「...使用指南」使用指南」重复文案
（_build.py 模板 `📖 查看「%s」使用指南` 与 gen_*_guides.py title 字段 `{name} 使用指南` 叠加）。
本次同时改 _build.py 模板（`📖 「%s」`）+ GUIDE_MAP 加载时 title 兜底补"使用指南"，
本脚本负责把历史 137 个文件统一刷成最终形态（按 json/guides.json 真实 title）。

幂等：以最终态为基准，已是 `查看「<title>」</a>` 的文件跳过。
"""
import os
import re
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools')
GUIDES_JSON = os.path.join(ROOT, 'json', 'guides.json')

# 加载映射（与 _build.py 一致：title 兜底补"使用指南"）
guide_map = {}  # basename -> (url, title)
if os.path.isfile(GUIDES_JSON):
    for g in json.load(open(GUIDES_JSON, encoding='utf-8')):
        t = g.get('tool')
        if not t:
            continue
        title = g.get('title', '') or ''
        if title and '使用指南' not in title:
            title = title + '使用指南'
        guide_map[t] = (g.get('guide', ''), title)

# 匹配三种旧形态（inner 可能以" 使用指南"或"使用指南"结尾；尾巴可能无/有"使用指南"）：
#   A: 查看「<X使用指南」使用指南</a>      inner 含"使用指南"，尾巴再叠
#   B: 查看「<X」使用指南</a>                inner 不含"使用指南"，尾巴补
#   C: 查看「<X 使用指南」</a>              inner 已含"使用指南"但中间多空格
# 最终态：查看「<correct>」</a>（correct = json title 兜底 + "使用指南"）
LINK_PATTERNS = [
    re.compile(r'(<a href="[^"]*?/guides/[^"]*?">)📖 查看「([^」]*?使用指南)」(?:使用指南)?\s*</a>'),
    re.compile(r'(<a href="[^"]*?/guides/[^"]*?">)📖 查看「([^」]+)」(?:使用指南)?\s*</a>'),
]

fixed = 0
total = 0
for ind in sorted(os.listdir(TOOLS)):
    d = os.path.join(TOOLS, ind)
    if not os.path.isdir(d):
        continue
    for fn in os.listdir(d):
        if not fn.endswith('.html'):
            continue
        p = os.path.join(d, fn)
        with open(p, encoding='utf-8') as f:
            h = f.read()
        if 'data-guide-link' not in h:
            continue
        total += 1
        base = fn  # basenname 就是工具页文件名

        def _repl(m):
            global fixed
            prefix = m.group(1)
            old_inner = m.group(2)
            entry = guide_map.get(base)
            correct = entry[1] if entry and entry[1] else old_inner
            if old_inner == correct:
                return m.group(0)
            fixed += 1
            return f'{prefix}📖 查看「{correct}」</a>'

        new_h = h
        for pat in LINK_PATTERNS:
            new_h = pat.sub(_repl, new_h)
        if new_h != h:
            with open(p, 'w', encoding='utf-8') as f:
                f.write(new_h)

print(f"扫描含 data-guide-link 的页面 {total} 个；统一文案 {fixed} 处")

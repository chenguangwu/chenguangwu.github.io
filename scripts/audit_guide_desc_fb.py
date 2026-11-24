#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""指南页 description 一致性审计。

`data-i18n-head-fb` 是英文/繁体字典缺键时的回退文本。`_build.py`
`normalize_guide_descriptions()` 会改写 description / og / twitter 的
content，若不同步同一 meta 的回退属性，英文态会显示旧描述，形成
“中文 content 新、英文回退旧”的分叉。本审计断言三处 description
的 content 与同标签回退值逐字一致。

同时拦截两类全站通用尾句（2026-11-24 新增）：它们曾在数百页 description
重复出现，属于站内大规模重复描述；一旦再次写入构建或页面即失败。
"""
import glob
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
META_RE = re.compile(
    r'<meta (?:(?:name="description")|(?:property="og:description")|(?:name="twitter:description"))'
    r'[^>]*?data-i18n-head-fb="([^"]*)"[^>]*?\scontent="([^"]*)"'
)
DESC_RE = re.compile(r'<meta name="description"[^>]*\scontent="([^"]*)"')
BOILER = (
    '本指南整理核心功能、适用场景、使用步骤与常见问题，纯前端免费在线使用，数据不上传。',
    '页面提供详细操作步骤、参数说明与常见问题解答，可直接对照使用。',
)

def main():
    bad = []
    boiler = []
    checked = 0
    for p in sorted(glob.glob(os.path.join(ROOT, 'guides', '*.html'))):
        s = open(p, encoding='utf-8').read()
        if 'TOOLBOX-REDIRECT' in s or 'name="robots" content="noindex' in s:
            continue
        for m in META_RE.finditer(s):
            checked += 1
            fb = html.unescape(m.group(1)).strip()
            c = html.unescape(m.group(2)).strip()
            if fb != c:
                bad.append((os.path.relpath(p, ROOT), fb[:70], c[:70]))
        dm = DESC_RE.search(s)
        if dm:
            desc = html.unescape(dm.group(1)).strip()
            if any(t in desc for t in BOILER):
                boiler.append(os.path.relpath(p, ROOT))
    print('guide desc fallback: %d checked, %d mismatched; boilerplate: %d pages'
          % (checked, len(bad), len(boiler)))
    for p, fb, c in bad[:20]:
        print('  %s\n    fb: %s\n    c : %s' % (p, fb[:70], c[:70]))
    for p in boiler[:20]:
        print('  boilerplate: %s' % p)
    return 1 if (bad or boiler) else 0

if __name__ == '__main__':
    sys.exit(main())

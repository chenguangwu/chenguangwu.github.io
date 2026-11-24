#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""指南页 description 与 i18n 回退值一致性审计。

`data-i18n-head-fb` 是英文/繁体字典缺键时的回退文本。`_build.py`
`normalize_guide_descriptions()` 会改写 description / og / twitter 的
content，若不同步同一 meta 的回退属性，英文态会显示旧描述，形成
“中文 content 新、英文回退旧”的分叉。本审计断言三处 description
的 content 与同标签回退值逐字一致。
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

def main():
    bad = []
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
    print('guide desc fallback: %d checked, %d mismatched' % (checked, len(bad)))
    for p, fb, c in bad[:20]:
        print('  %s\n    fb: %s\n    c : %s' % (p, fb, c))
    return 1 if bad else 0

if __name__ == '__main__':
    sys.exit(main())

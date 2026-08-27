#!/usr/bin/env python3
"""Clarity Reference Gate
========================
Build-time check to ensure public HTML pages include the shared Clarity loader.

Run: python3 scripts/check_clarity_refs.py
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLARITY_SNIPPET = '/js/analytics.js'
EXEMPT_PATTERNS = [
    # Google site ownership verification files intentionally keep minimal markup.
    re.compile(r'^google[0-9a-f]+\.html$')
]


def _is_exempt(rel_path):
    file_name = os.path.basename(rel_path)
    return any(p.match(file_name) for p in EXEMPT_PATTERNS)


def collect_html_files():
    html_files = []
    for current, dirs, files in os.walk(ROOT):
        # 跳过不需要扫描的目录（提高稳定性，避免误扫编辑/临时产物）
        dirs[:] = [d for d in dirs if d not in {'.git', '.github', 'node_modules', '.idea'}]
        for fn in files:
            if fn.endswith('.html'):
                rel = os.path.join(current, fn)
                rel = os.path.relpath(rel, ROOT)
                # 门禁聚焦工具页：工具页和工具行业落地页统一要求含 Clarity，其他站点页面不做强制
                if rel.startswith('tools' + os.sep) or rel.startswith('tools' + '/'):
                    html_files.append(os.path.join(current, fn))
    return html_files


def main():
    files = collect_html_files()
    missing = []

    for path in files:
        rel = os.path.relpath(path, ROOT)
        if _is_exempt(rel):
            continue
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception:
            continue
        if CLARITY_SNIPPET not in content:
            missing.append(rel)

    if not missing:
        print(f'Clarity check pass: {len(files)} html files scanned, all required pages reference {CLARITY_SNIPPET}')
        return 0

    print(f'Clarity check failed: {len(missing)} html files missing {CLARITY_SNIPPET} reference')
    for p in missing[:200]:
        print('  - ' + p)
    if len(missing) > 200:
        print('  ... truncated, total: ' + str(len(missing)))
    return 1


if __name__ == '__main__':
    sys.exit(main())

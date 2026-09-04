#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
optimize_common_js_defer.py — 把工具页/静态页 head 中「同步」加载的 common.js 改为 defer，
并在其之前注入一个极小的内联 API 兼容桩（队列回放），保证页面内联脚本的顶层调用不报错。

背景
----
国内访问 github.io 较慢，common.js（约 170KB / gzip 42KB）在 <head> 同步加载会阻塞
HTML 解析，弱网下表现为长时间白屏。改为 defer 后 HTML/CSS 可立即渲染，
脚本在 DOM 解析完成后、DOMContentLoaded 之前执行。

风险与对策
----------
改 defer 会改变执行时序：body 中的内联脚本会「先于」common.js 执行，
若其顶层直接调用 ToolBox.xxx（实测 221 处 ToolBox.initToolTheme() 与
1 处 ToolBox.addToolStyles()）会抛 TypeError。
对策：注入内联桩脚本（约 400B，无额外请求）先把这些调用收进 window.__tbq 队列，
common.js 加载完成后回放队列，行为与原来一致。

幂等性
------
注入内容带 `<!-- TOOLBOX-API-STUB -->` 标记；已含该标记或 common.js 已是 defer 的文件直接跳过。
可安全重复运行。

用法
----
    python3 scripts/optimize_common_js_defer.py            # 实际执行
    python3 scripts/optimize_common_js_defer.py --dry-run  # 只看会改多少，不落盘
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STUB = (
    '<script>window.__tbq=window.__tbq||[];window.ToolBox=window.ToolBox||{};'
    "['initToolTheme','addToolStyles','showToast','toast','copyText','copyToClipboard',"
    "'copyFromElement','downloadText','injectPrivacyBadge','toggleFavTool','addToRecentTool',"
    "'toggleToolTheme','applyTheme'].forEach(function(k){if(typeof window.ToolBox[k]!=='function')"
    'window.ToolBox[k]=function(){window.__tbq.push([k,[].slice.call(arguments)]);};});</script>'
    '<!-- TOOLBOX-API-STUB -->\n'
)

MARKER = '<!-- TOOLBOX-API-STUB -->'

# 匹配 <script src="...common.js" ...></script>（标签内不含 defer）
TAG_RE = re.compile(r'<script\s+src="([^"]*js/common\.js)"([^>]*)>\s*</script>')


def iter_html_files():
    """遍历需要处理的所有 HTML 页面"""
    for base in ('tools', 'guides'):
        d = os.path.join(ROOT, base)
        if not os.path.isdir(d):
            continue
        for dirpath, _dirnames, filenames in os.walk(d):
            for fn in filenames:
                if fn.endswith('.html'):
                    yield os.path.join(dirpath, fn)
    # 根目录静态页（排除构建产物与 Google 验证文件）
    skip_prefix = ('_', '.')
    for fn in sorted(os.listdir(ROOT)):
        if not fn.endswith('.html'):
            continue
        if fn.startswith(skip_prefix) or fn.startswith('google'):
            continue
        p = os.path.join(ROOT, fn)
        if os.path.isfile(p):
            yield p


def process(path, dry_run=False):
    """处理单个文件，返回状态：'skipped' | 'changed'"""
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            src = f.read()
    except Exception:
        return 'skipped'

    if MARKER in src:
        return 'skipped'

    m = TAG_RE.search(src)
    if not m:
        return 'skipped'
    if 'defer' in m.group(2):
        return 'skipped'

    new_tag = '<script src="%s"%s defer></script>' % (m.group(1), m.group(2))
    new_src = src[:m.start()] + STUB + new_tag + src[m.end():]

    if not dry_run:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_src)
    return 'changed'


def main():
    dry_run = '--dry-run' in sys.argv
    changed = skipped = 0
    for p in iter_html_files():
        st = process(p, dry_run=dry_run)
        if st == 'changed':
            changed += 1
        else:
            skipped += 1
    mode = '预检(dry-run)' if dry_run else '已执行'
    print('%s: 改造 %d 个文件，跳过 %d 个文件' % (mode, changed, skipped))


if __name__ == '__main__':
    main()

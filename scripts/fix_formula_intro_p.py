#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为「formula-box 紧随 h2、页面无独立 intro <p>」的工具页补 intro 段落（配合 fix_prerender_reset.py）。

坑（§6「build 预渲染陷阱」的变体）：`_prerender_tool_body` 用 count=1 命中文档**首个 `<p>`**。
公式型工具页的 formula-box 插在 h2 之后，其 formula-desc 成为首个 `<p>`，被注入 intro 英文（套话）。
仅把 formula-desc 改 `<div>` 还不够——首个 `<p>` 会落到 **`<script>` 内的 JS 模板字符串**
（如 ``let html = `<p><strong>输入：</strong>${raw}</p>` ``），build 会把英文 intro 注入 JS 源码，破坏页面。

做法（逐页）：
  1) 把 `<p class="formula-desc" …>英文</p>` 改为 `<div class="formula-desc">中文</div>`（中文取 data-zh）
  2) 在 formula-box 闭合 `</div>` 之后插入一个中文 intro `<p>`，供 build 预渲染注入英文 intro
     （中文取自 `i18n/tools/<ind>.json` 的 `zh-CN.intro`，缺失时退回工具标题）

用法：
  python3 scripts/fix_formula_intro_p.py --industry finance --dry-run
  python3 scripts/fix_formula_intro_p.py --industry finance --apply
"""
import argparse
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INTRO_STYLE = 'font-size:13px;color:var(--text-muted);margin-bottom:16px;'


def formula_box_end(html):
    """返回 `<div class="formula-box">` 配对闭合 `</div>` 的结束下标；未找到返回 -1。"""
    i = html.find('<div class="formula-box">')
    if i < 0:
        return -1
    depth = 0
    for m in re.finditer(r'<div\b[^>]*>|</div>', html[i:]):
        if m.group(0).startswith('</'):
            depth -= 1
            if depth == 0:
                return i + m.end()
        else:
            depth += 1
    return -1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--industry', required=True)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--apply', action='store_true')
    a = ap.parse_args()
    if not (a.dry_run or a.apply):
        print('请指定 --dry-run 或 --apply')
        return 2

    ind = a.industry
    gdir = os.path.join(ROOT, 'tools', ind)
    gis_path = os.path.join(ROOT, 'i18n', 'tools', '%s.json' % ind)
    gis = json.load(open(gis_path, encoding='utf-8')) if os.path.isfile(gis_path) else {}

    files = [f for f in sorted(glob.glob(os.path.join(gdir, '*.html'))) if os.path.basename(f) != 'index.html']
    n_div = n_ins = changed = 0
    preview = []
    for f in files:
        slug = os.path.basename(f)[:-5]
        html = open(f, encoding='utf-8').read()
        if not re.search(r'<p class="formula-desc"', html):
            continue
        # 仅处理「首个 <p> 即 formula-desc」的页面（其余已有独立 intro <p>，无需插入）
        first_p = re.search(r'<p\b', html)
        fd_pos = html.find('<p class="formula-desc"')
        if first_p is None or first_p.start() != fd_pos:
            continue

        zh_intro = ((gis.get(slug, {}) or {}).get('zh-CN', {}) or {}).get('intro', '') or ''
        if not zh_intro:
            zh_intro = ((gis.get(slug, {}) or {}).get('zh-CN', {}) or {}).get('title', '') or slug

        # 1) formula-desc 的 <p> → <div>（中文取 data-zh）
        def _fd(m):
            nonlocal n_div
            attrs, inner = m.group(1), m.group(2)
            zh = re.search(r'data-zh="([^"]*)"', attrs)
            text = zh.group(1) if zh else inner.strip()
            n_div += 1
            return '<div class="formula-desc">%s</div>' % text

        new = re.sub(r'<p class="formula-desc"([^>]*)>([\s\S]*?)</p>', _fd, html, count=1)

        # 2) formula-box 后插入中文 intro <p>
        end = formula_box_end(new)
        if end < 0:
            preview.append((slug, 'formula-box 未闭合，跳过插入'))
            continue
        ins = '\n    <p style="%s">%s</p>' % (INTRO_STYLE, zh_intro)
        new = new[:end] + ins + new[end:]
        n_ins += 1
        if new != html:
            changed += 1
            if len(preview) < 3:
                preview.append((slug, zh_intro[:50]))
            if a.apply:
                open(f, 'w', encoding='utf-8').write(new)

    print('[%s] formula-desc 改 div %d 处；插入 intro <p> %d 处；有改动文件 %d' % (ind, n_div, n_ins, changed))
    for pv in preview:
        print('  预览 %s: %s' % pv)
    if a.dry_run:
        return 0
    print('已写入')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

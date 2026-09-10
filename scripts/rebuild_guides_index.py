#!/usr/bin/env python3
"""重建 guides/index.html 的「全部指南」列表（幂等，可重跑）。

背景（2026-09-10）：
- guides/index.html 历史上由多个 gen_*_guides.py 批次纯追加，早期批次留下的条目
  标题为通用「使用指南」、描述为空（当时页面还是旧格式，或追加时未传 desc）；
- guide 页面后来统一改造成 i18n 双语头（<title data-i18n-head-fb="中文标题">英文</title>），
  旧脚本用 <title> 纯文本提取中文标题/描述会失败；
- 且 index 只列了 145/614 篇，大量指南未收录。

本脚本直接扫描 guides/*-guide.html 真实页面：
- 标题：优先 title 标签的 data-i18n-head-fb（中文 fallback），去掉「 - ToolBox」后缀；
  否则退回 <title> 文本同样去后缀。
- 描述：优先 meta description 的 data-i18n-head-fb，否则其 content 属性。
按 slug 排序后整体替换 index.html 中「全部指南」标题后的 <ul>...</ul>。
不修改 index.html 其它部分；_build.py 不重写该文件，故重建结果稳定。
"""
import os
import re
import html
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDES_DIR = os.path.join(ROOT, 'guides')

FB_TITLE_RE = re.compile(
    r'<title[^>]*data-i18n-head-fb="([^"]*)"[^>]*>.*?</title>', re.S)
TITLE_RE = re.compile(r'<title[^>]*>(.*?)</title>', re.S)
FB_DESC_RE = re.compile(
    r'<meta\s+name="description"[^>]*data-i18n-head-fb="([^"]*)"', re.S)
DESC_CONTENT_RE = re.compile(
    r'<meta\s+name="description"[^>]*content="([^"]*)"', re.S)


def strip_suffix(t):
    t = t.strip()
    t = re.sub(r'\s*-\s*ToolBox\s*$', '', t)
    return t.strip()


def extract(page):
    m = FB_TITLE_RE.search(page)
    title = strip_suffix(html.unescape(m.group(1))) if m and m.group(1).strip() else ''
    if not title:
        m = TITLE_RE.search(page)
        title = strip_suffix(html.unescape(m.group(1))) if m else ''
    m = FB_DESC_RE.search(page)
    desc = html.unescape(m.group(1)).strip() if m and m.group(1).strip() else ''
    if not desc:
        m = DESC_CONTENT_RE.search(page)
        desc = html.unescape(m.group(1)).strip() if m else ''
    return title, desc


def main():
    entries = []
    empty_pages = []
    for fn in sorted(os.listdir(GUIDES_DIR)):
        if not fn.endswith('-guide.html'):
            continue
        slug = fn[:-len('-guide.html')]
        path = os.path.join(GUIDES_DIR, fn)
        with open(path, encoding='utf-8') as f:
            page = f.read()
        title, desc = extract(page)
        if not title or not desc:
            empty_pages.append(fn)
        entries.append((slug, title, desc))

    if empty_pages:
        print('警告：%d 篇页面缺中文标题或描述（仍会列出）:' % len(empty_pages))
        for fn in empty_pages[:20]:
            print('  ', fn)
        if len(empty_pages) > 20:
            print('   ... 共 %d' % len(empty_pages))

    lis = ''.join(
        '<li><a href="https://chenguangwu.github.io/guides/%s-guide.html">%s</a>'
        '<span style="color:var(--muted);font-size:13px;"> — %s</span></li>'
        % (slug, html.escape(title), html.escape(desc[:120]))
        for slug, title, desc in entries)

    ip = os.path.join(GUIDES_DIR, 'index.html')
    with open(ip, encoding='utf-8') as f:
        s = f.read()

    anchor = s.find('全部指南')
    if anchor == -1:
        print('错误：index.html 中找不到「全部指南」锚点', file=sys.stderr)
        return 1
    ul_start = s.find('<ul>', anchor)
    ul_end = s.find('</ul>', ul_start)
    if ul_start == -1 or ul_end == -1:
        print('错误：index.html 中找不到列表 <ul>...', file=sys.stderr)
        return 1

    new_s = s[:ul_start] + '<ul>' + lis + '</ul>' + s[ul_end + len('</ul>'):]
    with open(ip, 'w', encoding='utf-8') as f:
        f.write(new_s)
    print('重建完成：%d 条（替换原列表），缺标题/描述 %d 篇' % (len(entries), len(empty_pages)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

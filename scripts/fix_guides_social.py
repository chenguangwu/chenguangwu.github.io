#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为 guides/*.html 补齐缺失的社交卡片标签（og:description / og:image / twitter:*），幂等。

背景：
- 指南页由 scripts/gen_*_guides.py 生成，但 _build.py 重建只将其纳入 sitemap，不重写 HTML 内容，
  因此直接修补静态页即可立即生效。
- 仅补充社交分享卡片标签，不影响搜索 CTR；规范与工具页 _build.py fix A 一致。
- 取值来源：description 复用 <meta name="description">；og:title 复用 <meta property="og:title">；
  社交图统一用 https://chenguangwu.github.io/og-image.png（与全站一致）。

用法：
    python3 scripts/fix_guides_social.py
"""
import os
import re
import html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = os.path.join(ROOT, 'guides')
IMG = 'https://chenguangwu.github.io/og-image.png'
IMG_ALT = 'ToolBox - 免费在线工具与使用指南'


def get_prop(h, prop):
    m = re.search(r'<meta[^>]*property="%s"[^>]*content="([^"]*)"' % re.escape(prop), h)
    return m.group(1) if m else None


def get_name(h, name):
    m = re.search(r'<meta[^>]*name="%s"[^>]*content="([^"]*)"' % re.escape(name), h)
    return m.group(1) if m else None


def e(v):
    return html.escape(v or '', quote=True)


def main():
    if not os.path.isdir(G):
        print('guides/ 不存在，跳过')
        return
    fixed = 0
    for fn in sorted(os.listdir(G)):
        if not fn.endswith('.html'):
            continue
        p = os.path.join(G, fn)
        h = open(p, encoding='utf-8').read()
        desc = get_name(h, 'description')
        og_title = get_prop(h, 'og:title')
        ins = []
        if 'og:description' not in h:
            ins.append('<meta property="og:description" content="%s">' % e(desc or og_title))
        if 'og:image' not in h:
            ins.append('<meta property="og:image" content="%s">' % IMG)
            ins.append('<meta property="og:image:width" content="1200">')
            ins.append('<meta property="og:image:height" content="630">')
            ins.append('<meta property="og:image:alt" content="%s">' % e(IMG_ALT))
        if 'twitter:card' not in h:
            ins.append('<meta name="twitter:card" content="summary_large_image">')
        if 'twitter:title' not in h:
            ins.append('<meta name="twitter:title" content="%s">' % e(og_title))
        if 'twitter:description' not in h:
            ins.append('<meta name="twitter:description" content="%s">' % e(desc or og_title))
        if 'twitter:image' not in h:
            ins.append('<meta name="twitter:image" content="%s">' % IMG)
            ins.append('<meta name="twitter:image:alt" content="%s">' % e(IMG_ALT))
        if not ins:
            continue
        block = '\n' + '\n'.join(ins)
        if '<meta property="og:url"' in h:
            h = re.sub(r'(<meta property="og:url"[^>]*>)', r'\1' + block, h, count=1)
        else:
            h = h.replace('</head>', block + '\n</head>', 1)
        open(p, 'w', encoding='utf-8').write(h)
        fixed += 1
        print('OK: %s (+%d tags)' % (fn, len(ins)))
    print('总修补: %d 页' % fixed)


if __name__ == '__main__':
    main()

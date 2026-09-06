#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为 automotive 分类缺 hreflang 的源码工具页补注入多语言 SEO 区块。

根因：automotive 46 个源码 html 创建于 hreflang 注入机制加入构建流程之前，
从未整页 regenerate，因此缺 <!-- TOOLBOX-HREFLANG --> 区块；_build.py 的 deep-dive
重建路径不调用 inject_hreflang，故本次内容优化未触发补齐。zh-tw 由源码转换生成，
源码缺则 zh-tw 也缺，导致 gen_opencc_locales.mjs --check 失败。

本脚本逐字复用 _build.py 的 build_hreflang_block / inject_hreflang 逻辑，仅对
I18N_HREFLANG_MARKER 缺失的 automotive 源码页进行幂等注入，绝不触碰其他文件、
不触发全站 regenerate，保证与既有 4941 个工具页的输出字节一致。
"""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

I18N_LOCALES = ['zh-CN', 'zh-TW', 'en-US']
I18N_STATIC_DIRS = {'zh-TW': 'zh-tw'}
I18N_XDEFAULT = 'zh-CN'
I18N_HREFLANG_MARKER = '<!-- TOOLBOX-HREFLANG -->'
I18N_HREFLANG_BLOCK_RE = re.compile(
    r'<!-- TOOLBOX-HREFLANG -->\s*'
    r'(?:<link rel="alternate" hreflang="[^"]+" href="[^"]*">\s*)+'
    r'(?:<meta property="og:locale(?::alternate)?" content="[^"]+">\s*)+',
    re.I,
)


def _loc_under(locale):
    return locale.replace('-', '_')


def localized_i18n_url(abs_url, locale):
    if locale == 'zh-CN':
        return abs_url
    if locale == 'en-US':
        return abs_url + ('&' if '?' in abs_url else '?') + 'lang=en-US'
    prefix = I18N_STATIC_DIRS[locale]
    base = 'https://chenguangwu.github.io'
    suffix = abs_url[len(base):] if abs_url.startswith(base) else abs_url
    if suffix in ('', '/'):
        return base + '/' + prefix + '/'
    return base + '/' + prefix + suffix


def build_hreflang_block(abs_url, default_locale='zh-CN'):
    lines = [I18N_HREFLANG_MARKER]
    for loc in I18N_LOCALES:
        lines.append('<link rel="alternate" hreflang="%s" href="%s">'
                     % (loc, localized_i18n_url(abs_url, loc)))
    lines.append('<link rel="alternate" hreflang="x-default" href="%s">'
                 % localized_i18n_url(abs_url, I18N_XDEFAULT))
    lines.append('<meta property="og:locale" content="%s">'
                 % _loc_under(default_locale))
    for loc in I18N_LOCALES:
        if loc != default_locale:
            lines.append('<meta property="og:locale:alternate" content="%s">'
                         % _loc_under(loc))
    return '\n'.join(lines) + '\n'


def inject_hreflang(content, abs_url, default_locale='zh-CN'):
    block = build_hreflang_block(abs_url, default_locale)
    if I18N_HREFLANG_MARKER in content:
        updated, count = I18N_HREFLANG_BLOCK_RE.subn(block, content, count=1)
        if count:
            return updated
        marker_pos = content.find(I18N_HREFLANG_MARKER)
        end_pos = content.find('</head>', marker_pos)
        if end_pos != -1:
            return content[:marker_pos] + block + content[end_pos:]
    if '</head>' in content:
        content = content.replace('</head>', block + '</head>', 1)
    return content


def main():
    cat = 'automotive'
    files = sorted(glob.glob(os.path.join(ROOT, 'tools', cat, '*.html')))
    changed = 0
    skipped = 0
    added_head = 0
    for f in files:
        if f.endswith('index.html'):
            continue
        base = os.path.basename(f)[:-5]
        s = open(f, encoding='utf-8').read()
        if I18N_HREFLANG_MARKER in s:
            skipped += 1
            continue
        # 46 个 stale 文件：单引号属性、<head> 未闭合、且无 <body> 开标签
        # （只有 </body> 闭标签，靠浏览器隐式 body）。浏览器隐式在 <body> 前闭合 head，
        # 故在 </body> 前显式补 </head> 锚点，使 inject_hreflang 与 gen_opencc 的
        # localeHead 注入能定位。
        if '</head>' not in s:
            if '</body>' in s:
                s = s.replace('</body>', '</head>\n</body>', 1)
                added_head += 1
            else:
                print('SKIP no </head> and no </body>:', base)
                continue
        abs_url = 'https://chenguangwu.github.io/tools/%s/%s.html' % (cat, base)
        s2 = inject_hreflang(s, abs_url)
        if s2 != s:
            open(f, 'w', encoding='utf-8').write(s2)
            changed += 1
        else:
            print('UNCHANGED:', base)
    print('automotive hreflang injected: %d, added </head>: %d, skipped(had marker): %d'
          % (changed, added_head, skipped))


if __name__ == '__main__':
    main()

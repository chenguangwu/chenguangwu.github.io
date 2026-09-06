#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""banking 单文件补 hreflang（复刻 _build.py inject_hreflang，仅处理缺失者）。

背景：fisher-real-rate.html 是 hreflang 机制加入前提交的旧模板页，
_build.py 的 deep-dive 重建路径不会整页 regenerate，故缺 TOOLBOX-HREFLANG
区块，导致 gen_opencc_locales.mjs --check 繁体校验失败。
其余 26 个 banking 页结构正常已含 hreflang，自动跳过。
"""
import os
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

I18N_LOCALES = ['zh-CN', 'zh-TW', 'en-US']
I18N_XDEFAULT = 'zh-CN'
I18N_HREFLANG_MARKER = '<!-- TOOLBOX-HREFLANG -->'
I18N_STATIC_DIRS = {'zh-TW': 'zh-tw'}


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
        return content
    if '</head>' in content:
        content = content.replace('</head>', block + '</head>', 1)
    return content


def main():
    cat = 'banking'
    files = sorted(glob.glob(os.path.join(ROOT, 'tools', cat, '*.html')))
    changed = 0
    skipped = 0
    for f in files:
        if f.endswith('index.html'):
            continue
        base = os.path.basename(f)[:-5]
        s = open(f, encoding='utf-8').read()
        if I18N_HREFLANG_MARKER in s:
            skipped += 1
            continue
        abs_url = 'https://chenguangwu.github.io/tools/%s/%s.html' % (cat, base)
        s2 = inject_hreflang(s, abs_url)
        if s2 != s:
            open(f, 'w', encoding='utf-8').write(s2)
            changed += 1
            print('INJECTED:', base)
        else:
            print('UNCHANGED (no </head>?):', base)
    print('banking hreflang injected: %d, skipped(had marker): %d' % (changed, skipped))


if __name__ == '__main__':
    main()

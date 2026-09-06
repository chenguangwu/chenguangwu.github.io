#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""beauty 3 个旧模板页补 hreflang（复刻 _build.py inject_hreflang，仅处理缺失者）。
全站扫描确认：修完这 3 页后，全站 4987 个工具页不再有缺 TOOLBOX-HREFLANG 者（autombile 46 + banking 1 已在前序批次修复）。"""
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
    cat = 'beauty'
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
    print('beauty hreflang injected: %d, skipped(had marker): %d' % (changed, skipped))


if __name__ == '__main__':
    main()

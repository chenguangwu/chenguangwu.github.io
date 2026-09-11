#!/usr/bin/env python3
"""幂等补注：让所有引用 /js/common.js 的公开 HTML 页面同时引用 /js/i18n.js。

背景：
- 项目约定「凡引 common.js 须引 i18n.js」（AGENTS.md）。common.js 的 i18nText()
  依赖 window.I18n，若页面未加载 i18n.js，则 ?lang=en-US 下所有 data-i18n 元素
  都会回退 data-i18n-fb 的中文，英文态整页失效。
- 实测缺陷：444 个页面（guides/*.html 441 个 + 404.html + embed.html + sitemap.html）
  只引 common.js 未引 i18n.js，英文态下导航/页脚/Tab 栏全部显示中文。
- _build.py 已统一处理工具页/首页（模板自带 i18n.js）；本脚本补注它不处理的静态页。
- 注入位置：i18n.js 必须在 common.js **之前**（common.js 的 i18nText 依赖 I18n）。
- google 验证文件（google*.html）不动；已含 i18n.js 的页面跳过，保证幂等。

运行：python3 scripts/inject_i18n_js.py
"""
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 匹配完整的 common.js script 标签（含 </script>），捕获前缀（/ 或 ../）与其余属性（如 defer）
PAT = re.compile(r'<script\s+src="([^"]*?)js/common\.js"([^>]*)></script>')


def repl(m):
    prefix, attrs = m.group(1), m.group(2)
    return ('<script src="%sjs/i18n.js"%s></script>\n'
            '<script src="%sjs/common.js"%s></script>' % (prefix, attrs, prefix, attrs))


def main():
    out = subprocess.check_output(['git', 'ls-files', '*.html'], cwd=ROOT, text=True)
    files = [f for f in out.splitlines() if f]

    injected = 0
    skipped_covered = 0
    skipped_no_common = 0
    skipped_google = 0
    touched = []

    for rel in files:
        base = os.path.basename(rel)
        if base.startswith('google') and base.endswith('.html'):
            skipped_google += 1
            continue
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p):
            continue
        with open(p, encoding='utf-8') as f:
            src = f.read()
        if 'js/i18n.js' in src:
            skipped_covered += 1
            continue
        if not PAT.search(src):
            skipped_no_common += 1
            continue
        new, n = PAT.subn(repl, src, count=1)
        if n:
            with open(p, 'w', encoding='utf-8') as f:
                f.write(new)
            injected += 1
            touched.append(rel)

    print('补注 i18n.js：%d 个页面' % injected)
    print('  已含 i18n.js 跳过 : %d' % skipped_covered)
    print('  无 common.js 跳过 : %d' % skipped_no_common)
    print('  google 验证文件跳过: %d' % skipped_google)
    if touched:
        print('  本次改动示例（前 10）：')
        for f in touched[:10]:
            print('     ' + f)


if __name__ == '__main__':
    main()

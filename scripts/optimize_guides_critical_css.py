#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""guides 页 critical CSS 内联 + 本地 CSS 非阻塞加载（幂等批量改造）。

注意：工具页/落地页由 _build.py 统一注入（fix_tool_pages_seo / generate_category_indexes），
guides 页不在 _build.py 扫描范围，故单独处理。逻辑与工具页完全一致，保证全站首屏一致。
- 内联首屏外壳样式（scripts/critical_tool_css.txt），弱网首访立即可见、防 FOUC；
- ../css/common.css（guides 相对路径）由阻塞 <link rel=stylesheet> 改为
  <link rel=preload as=style onload=...> + <noscript> 兜底，不再阻塞首屏。

幂等：已含 id="critical-css" 的页跳过；已非阻塞的 link 不重复替换。
"""
import os
import re
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRIT_PATH = os.path.join(ROOT, "scripts", "critical_tool_css.txt")

with open(CRIT_PATH, encoding="utf-8") as f:
    CRIT = f.read().strip()

# 仅处理站点本地 common.css / nav-menu.css
LOCAL_CSS_RE = re.compile(
    r'<link rel="stylesheet" href="([^"]*(?:common\.css|nav-menu\.css))">'
)


def transform(html):
    if 'id="critical-css"' in html:
        return None  # 已处理，幂等跳过
    first = LOCAL_CSS_RE.search(html)
    if not first:
        return None  # 无本地 css link，跳过
    # 在第一个本地 css link 之前插入内联 critical（基于原始文档定位，避免命中 noscript 内 link）
    ins = '<style id="critical-css">\n%s\n</style>\n' % CRIT
    html2 = html[: first.start()] + ins + html[first.start():]
    # 本地 css link 改为非阻塞 preload + noscript 兜底
    def repl(m):
        href = m.group(1)
        return (
            '<link rel="preload" as="style" href="' + href + '" '
            'onload="this.onload=null;this.rel=\'stylesheet\'">\n'
            '<noscript><link rel="stylesheet" href="' + href + '"></noscript>'
        )

    return LOCAL_CSS_RE.sub(repl, html2)


def main():
    d = os.path.join(ROOT, "guides")
    targets = glob.glob(os.path.join(d, "**", "*.html"), recursive=True) if os.path.isdir(d) else []
    changed = skipped = errors = 0
    for p in targets:
        try:
            with open(p, encoding="utf-8") as f:
                html = f.read()
            res = transform(html)
            if res is None:
                skipped += 1
                continue
            with open(p, "w", encoding="utf-8") as f:
                f.write(res)
            changed += 1
        except Exception as e:  # noqa
            errors += 1
            print("ERR", p, e)
    print("DONE changed=%d skipped=%d errors=%d" % (changed, skipped, errors))


if __name__ == "__main__":
    main()

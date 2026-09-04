#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""工具页 / guides 页 critical CSS 内联 + 全量本地 CSS 非阻塞加载（幂等批量改造）。

与首页 critical CSS 思路一致：
- 内联首屏外壳样式（scripts/critical_tool_css.txt），保证弱网首访立即可见、避免 FOUC；
- common.css / nav-menu.css 由普通阻塞 <link rel=stylesheet> 改为
  <link rel=preload as=style onload=...> + <noscript> 兜底，不再阻塞首屏渲染。

幂等：已含 id="critical-css" 的页直接跳过；无本地 css link 的页跳过。
"""
import os
import re
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRIT_PATH = os.path.join(ROOT, "scripts", "critical_tool_css.txt")

with open(CRIT_PATH, encoding="utf-8") as f:
    CRIT = f.read().strip()

# 仅处理站点本地 common.css / nav-menu.css（不动外部 CDN css，如 highlight.js）
LOCAL_CSS_RE = re.compile(
    r'<link rel="stylesheet" href="([^"]*(?:common\.css|nav-menu\.css))">'
)


def transform(html):
    if 'id="critical-css"' in html:
        return None  # 已处理，幂等跳过
    first = LOCAL_CSS_RE.search(html)
    if not first:
        return None  # 无本地 css link，跳过
    # 1) 在第一个本地 css link 之前插入内联 critical（基于原始文档定位，避免命中 noscript 内 link）
    ins = '<style id="critical-css">\n%s\n</style>\n' % CRIT
    html2 = html[: first.start()] + ins + html[first.start():]
    # 2) 本地 css link 改为非阻塞 preload + noscript 兜底
    def repl(m):
        href = m.group(1)
        return (
            '<link rel="preload" as="style" href="' + href + '" '
            'onload="this.onload=null;this.rel=\'stylesheet\'">\n'
            '<noscript><link rel="stylesheet" href="' + href + '"></noscript>'
        )

    return LOCAL_CSS_RE.sub(repl, html2)


def main():
    targets = []
    for base in ("tools", "guides"):
        d = os.path.join(ROOT, base)
        if os.path.isdir(d):
            targets += glob.glob(os.path.join(d, "**", "*.html"), recursive=True)
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

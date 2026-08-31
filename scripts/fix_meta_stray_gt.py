#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 <meta> 标签结尾多余的 '>'。

背景
----
部分工具页写成：
    <meta name="description" content="...">>
末尾多出的 '>' 会在 <head> 内产生裸文本节点，浏览器据此**提前关闭 <head>**，
导致其后所有 <title> / canonical / og:* / JSON-LD 被挪进 <body> 而失效。
2026-08-31 全站排查命中 273 个工具页。

修法：把 '">' 之后再跟一个 '>' 的情况收敛为单个 '>'。
只匹配紧跟换行、且标签内不含裸 '>' 的 meta 行，避免误伤属性值里合法的 &gt;。

用法
----
    python3 scripts/fix_meta_stray_gt.py          # 应用修复
    python3 scripts/fix_meta_stray_gt.py --dry    # 只报告不落盘
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 形如 <meta ..."> 后紧跟一个多余的 >，且该行到此结束
PAT = re.compile(r'(<meta\s[^>]*?)>[ \t]*>(?=[ \t]*\n)')


def main():
    dry = '--dry' in sys.argv
    files = sorted(glob.glob(os.path.join(ROOT, 'tools', '**', '*.html'), recursive=True))
    changed_files = 0
    changed_tags = 0

    for fp in files:
        with open(fp, encoding='utf-8', errors='ignore') as f:
            src = f.read()
        new, n = PAT.subn(r'\1>', src)
        if not n:
            continue
        changed_files += 1
        changed_tags += n
        if dry:
            print('  [dry] %s  (%d 处)' % (os.path.relpath(fp, ROOT), n))
            continue
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(new)

    print('\n修复文件 %d 个，meta 标签 %d 处%s'
          % (changed_files, changed_tags, '（dry-run 未落盘）' if dry else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main())

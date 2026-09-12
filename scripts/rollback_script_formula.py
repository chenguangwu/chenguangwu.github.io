#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""回滚 fix_formula.py 误插入到 <script> 内的 formula-box。

背景：部分页面的「输入区」由 JS 模板字符串动态生成（`let html = '<div class="input-row">…'`），
通用脚本的 insert_anchor 会命中 script 内的 input-row，把公式框插进 JS 源码（破坏模板）。

本脚本按 MAP 精确移除「位于 <script> 块内、且内容与 MAP 一致」的 formula-box（幂等）。
用法：python3 scripts/rollback_script_formula.py --industry science --map fix_science_formula_map:MAP [--apply]
"""
import argparse
import importlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BOX = re.compile(r'<div\b[^>]*\bclass="formula-box"[^>]*>')


def script_spans(s):
    return [(m.start(), m.end()) for m in re.finditer(r'<script\b[\s\S]*?</script>', s, re.I)]


def in_script(pos, spans):
    return any(a <= pos < b for a, b in spans)


def box_span(s, i):
    """从 <div ...formula-box...> 起点做 div 配平，返回 (start, end)。"""
    depth = 0
    for m in re.finditer(r'<div\b[^>]*>|</div>', s[i:]):
        if m.group(0).startswith('</'):
            depth -= 1
            if depth == 0:
                return (i, i + m.end())
        else:
            depth += 1
    return (-1, -1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--industry', required=True)
    ap.add_argument('--map', required=True)
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    if not (a.dry_run or a.apply):
        ap.error('需指定 --dry-run 或 --apply')

    mod, _, var = a.map.partition(':')
    MAP = getattr(importlib.import_module(mod), var or 'MAP')
    tools_dir = os.path.join(ROOT, 'tools', a.industry)

    rolled = []
    for slug in MAP:
        path = os.path.join(tools_dir, slug + '.html')
        if not os.path.exists(path):
            continue
        s = open(path, encoding='utf-8').read()
        spans = script_spans(s)
        # 找出所有落在 script 内、且 desc 与 MAP 一致的 formula-box，逐个移除
        removed = 0
        while True:
            target = None
            for m in BOX.finditer(s):
                if not in_script(m.start(), spans):
                    continue
                st, en = box_span(s, m.start())
                if st < 0:
                    continue
                seg = s[st:en]
                if MAP[slug]['desc'].strip() in seg:
                    # 连同紧邻的前导空白一起删（JS 模板串内只删框体本身）
                    target = (st, en)
                    break
            if not target:
                break
            s = s[:target[0]] + s[target[1]:]
            removed += 1
            spans = script_spans(s)
        if removed:
            rolled.append((slug, removed))
            if a.apply:
                open(path, 'w', encoding='utf-8').write(s)

    print('模式: %s | industry=%s | 回滚页面 %d' % ('apply' if a.apply else 'dry-run', a.industry, len(rolled)))
    for slug, n in rolled:
        print('  [ROLLBACK×%d] %s' % (n, slug))
    return 0


if __name__ == '__main__':
    sys.exit(main())

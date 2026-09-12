#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""通用「📐 计算公式 / 原理」块补齐与修正（§4.1.2 真实内容）。

从 fix_finance_formula.py 抽取的通用逻辑，按 `--industry` + `--map` 复用，
避免每个分类复制一份插入/更新实现。数据（MAP）留在各自的 *_formula_map.py。

三类处理（按 MAP 逐 slug 判定，幂等）：
  A) 页面无 formula-box            → 在锚点插入完整框（formula-title + 可选 formula-eq + formula-desc）
  B) 有框但无 formula-desc         → 在框内补 formula-desc（并在缺 eq 时补 formula-eq）
  C) 有 formula-desc 但为套话/占位 → 替换为真实依据说明

锚点优先级：`<div class="input-row">` → `<div class="input-row2">` → h2 后首个 intro `<p>` 之后 → h2 之后。
formula-desc 一律用 `<div>`：`_prerender_tool_body` 的 count=1 只匹配 `<p>`，用 div 可避免被注入 intro（见 §6）。

用法：
  python3 scripts/fix_formula.py --industry design --map fix_design_formula_map:MAP --dry-run
  python3 scripts/fix_formula.py --industry design --map fix_design_formula_map:MAP --apply
"""
import argparse
import importlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

TITLE = '📐 计算公式 / 原理'

BOX_RE = re.compile(r'<div\b[^>]*\bclass="formula-box"[^>]*>')


def build_box(entry, title=TITLE):
    lines = ['    <div class="formula-box">', '      <div class="formula-title">%s</div>' % title]
    eq = (entry.get('eq') or '').strip()
    if eq:
        lines.append('      <div class="formula-eq">%s</div>' % eq)
    lines.append('      <div class="formula-desc">%s</div>' % entry['desc'].strip())
    lines.append('    </div>')
    return '\n'.join(lines)


def find_box_span(s):
    """返回 (start, end) 覆盖整个 formula-box；未找到返回 (-1, -1)。"""
    m0 = BOX_RE.search(s)
    if not m0:
        return (-1, -1)
    i = m0.start()
    depth = 0
    for m in re.finditer(r'<div\b[^>]*>|</div>', s[i:]):
        if m.group(0).startswith('</'):
            depth -= 1
            if depth == 0:
                return (i, i + m.end())
        else:
            depth += 1
    return (-1, -1)


def insert_anchor(s):
    """返回插入公式框的位置下标（插在该位置之前）。"""
    for a in ('<div class="input-row">', '<div class="input-row2">'):
        i = s.find(a)
        if i > 0:
            return i
    m = re.search(r'</h2>', s)
    if m:
        p = re.search(r'<p\b[^>]*>[\s\S]*?</p>', s[m.end():])
        if p:
            return m.end() + p.end()
        return m.end() + 1
    i = s.find('<div class="container">')
    return i if i > 0 else len(s)


def process_html(s, entry, title=TITLE):
    """对单个页面 HTML 应用 MAP 条目，返回 (new_html, action)。"""
    start, end = find_box_span(s)
    if start < 0:
        box = build_box(entry, title)
        pos = insert_anchor(s)
        return (s[:pos] + box + '\n' + s[pos:], 'INSERT')
    box = s[start:end]
    eq = (entry.get('eq') or '').strip()
    desc = entry['desc'].strip()
    has_eq = 'formula-eq' in box
    has_desc = 'formula-desc' in box
    nb = box
    if has_desc:
        nb = re.sub(r'(<(?:div|p) class="formula-desc"[^>]*>)[\s\S]*?(</(?:div|p)>)',
                    lambda m: m.group(1) + desc + m.group(2), nb, count=1)

    def _meta_end(text):
        ms = list(re.finditer(r'<div class="formula-(?:title|eq)">[\s\S]*?</div>', text))
        if ms:
            return ms[-1].end()
        m0 = BOX_RE.search(text)
        return m0.end() if m0 else 0

    if eq and not has_eq:
        at = _meta_end(nb)
        nb = nb[:at] + '\n      <div class="formula-eq">%s</div>' % eq + nb[at:]
    if not has_desc:
        at = _meta_end(nb)
        nb = nb[:at] + '\n      <div class="formula-desc">%s</div>' % desc + nb[at:]
    if nb != box:
        return (s[:start] + nb + s[end:], 'UPDATE')
    return (s, 'NOCHANGE')


def load_map(spec):
    """spec = 'module:VAR' 或 'module'（默认 MAP）。"""
    mod, _, var = spec.partition(':')
    m = importlib.import_module(mod)
    return getattr(m, var or 'MAP')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--industry', required=True)
    ap.add_argument('--map', required=True, help='模块:变量名，如 fix_design_formula_map:MAP')
    ap.add_argument('--title', default=TITLE)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--apply', action='store_true')
    a = ap.parse_args()
    if not (a.dry_run or a.apply):
        ap.error('需指定 --dry-run 或 --apply')

    MAP = load_map(a.map)
    tools_dir = os.path.join(ROOT, 'tools', a.industry)
    stat = {}
    for slug in MAP:
        path = os.path.join(tools_dir, slug + '.html')
        if not os.path.exists(path):
            stat['MISSING'] = stat.get('MISSING', 0) + 1
            print('  [MISSING] %s' % slug)
            continue
        s = open(path, encoding='utf-8').read()
        new, action = process_html(s, MAP[slug], a.title)
        stat[action] = stat.get(action, 0) + 1
        if action in ('INSERT', 'UPDATE') and not a.apply:
            print('  [%s] %s' % (action, slug))
        if action != 'NOCHANGE' and a.apply:
            open(path, 'w', encoding='utf-8').write(new)
    print('\n模式: %s | industry=%s | MAP 条目 %d | %s'
          % ('apply' if a.apply else 'dry-run', a.industry, len(MAP), stat))
    return 0


if __name__ == '__main__':
    sys.exit(main())

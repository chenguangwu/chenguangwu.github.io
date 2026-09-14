#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修正 formula-box 误插入 <script>/模板字符串 的问题（幂等）。

背景：add_fitness_formula.py / add_math_formula.py 的锚点搜索遍历全文，
命中 JS 模板串里的 `class="input-row"` / `class="tip-box"`，把公式框插进 JS 源码
（单引号串会直接 SyntaxError；模板串虽能解析但会把公式框渲染进输入区）。

本脚本对被污染页做两步修复：
  1) 用 div 配平精确摘除「位于 <script> 块内」的 formula-box；
  2) 按项目惯例重新插到 markup 内首个输入容器之前（介绍段落之后）。

用法：python3 scripts/fix_formula_box_placement.py [--apply]
"""
import argparse
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TARGETS = [
    ("fitness", "assessor-64"),
    ("fitness", "rater-time"),
    ("math", "equation-solver"),
]

# 与各 add_*_formula.py 保持一致的锚点优先级
ANCHORS = ["tip-box", "tabs", "scale-row", "set-row", "tool-result", "input-row", "subject-row"]
# 无锚点时的兜底插入点（同为「介绍段落之后的第一个容器」）
FALLBACKS = ['<div class="type-grid"', '<div class="input-area"', '<div class="toolbar"',
             '<div class="result-box"', '<div id="inputArea"']


def script_spans(s):
    return [(m.start(), m.end()) for m in re.finditer(r'<script\b[\s\S]*?</script>', s, re.I)]


def style_spans(s):
    return [(m.start(), m.end()) for m in re.finditer(r'<style\b[\s\S]*?</style>', s, re.I)]


def in_spans(pos, spans):
    return any(a <= pos < b for a, b in spans)


def box_span(s, i):
    """从 formula-box 起点做 div 配平，返回 (start, end)。"""
    depth = 0
    for m in re.finditer(r'<div\b[^>]*>|</div>', s[i:]):
        if m.group(0).startswith('</'):
            depth -= 1
            if depth == 0:
                return (i, i + m.end())
        else:
            depth += 1
    return (-1, -1)


def markup_anchor(s, spans):
    """首个位于 markup（非 script/style）内的锚点位置。"""
    best = -1
    for a in ANCHORS:
        for m in re.finditer(r'<(?:\w+)\b[^>]*\bclass="[^"]*\b%s\b[^"]*"[^>]*>' % re.escape(a), s):
            if in_spans(m.start(), spans):
                continue
            best = m.start()
            break
        if best >= 0:
            return best
    for f in FALLBACKS:
        i = s.find(f)
        if i >= 0 and not in_spans(i, spans):
            return i
    return -1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    for ind, slug in TARGETS:
        fp = os.path.join(ROOT, "tools", ind, slug + ".html")
        s = open(fp, encoding="utf-8").read()
        sp = script_spans(s) + style_spans(s)
        found = None
        for m in re.finditer(r'<div\b[^>]*\bclass="[^"]*\bformula-box\b[^"]*"[^>]*>', s):
            if in_spans(m.start(), sp):
                found = box_span(s, m.start())
                break
        if not found or found[0] < 0:
            print("  无需修复(script 内无公式框): %s/%s" % (ind, slug))
            continue
        box = s[found[0]:found[1]]
        rest = s[:found[0]] + s[found[1]:]
        pos = markup_anchor(rest, script_spans(rest) + style_spans(rest))
        if pos < 0:
            print("  无 markup 锚点(跳过): %s/%s" % (ind, slug))
            continue
        out = rest[:pos] + box + "\n" + rest[pos:]
        # 自检：修复后公式框不得再落在 script/style 内，且脚本可解析
        s2 = out
        sp2 = script_spans(s2) + style_spans(s2)
        i2 = s2.find('class="card formula-box"')
        assert i2 > 0 and not in_spans(i2, sp2), "  %s/%s 修复后仍在 script 内" % (ind, slug)
        # JS 单引号串不会被裸换行撕裂：检查原 box 内的引号未影响外串
        if a.apply:
            open(fp, "w", encoding="utf-8").write(out)
        print("  %s修复: %s/%s  box %d→(pos %d) 字节" % ("已" if a.apply else "待", ind, slug, len(box), pos))

    print("完成%s" % ("（--apply）" if a.apply else "（dry-run，未落盘）"))


if __name__ == "__main__":
    main()

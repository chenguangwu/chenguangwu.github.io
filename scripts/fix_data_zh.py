#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复工具页「中文原文」容器属性 data-zh 的两类损坏（可重复执行）。

背景（2026-09-16 全站扫描确认，无头 Chrome 取证）：
  运行时 js/tool-i18n.js 取 data-zh 写回 node.textContent 作为中文态文案
  （`h2.textContent = h2.getAttribute('data-zh')`、`introP.textContent = ...`），
  所以 data-zh 里任何多余/被转义的字符，中文用户都会原样看到。

损坏一（189 条）：intro <p> 的 data-zh 开头多余一个 '>'
    tools/design/checker.html
      <p ... data-zh="&gt;输入前景色和背景色，计算 WCAG 2.1 对比度比率…">
  无头 Chrome 实测用户所见为「>输入前景色和背景色…」，而正常页（edu/exam-timer）
  为「倒计时、正计时、休息提醒一体化」——对照组无前导符号。
  根因：早期批量脚本按 markdown 引用行 '> 描述' 生成 intro，保留了引导符 '>'。

损坏二（4 条）：<h2> 的 data-zh 被整段 HTML 转义后塞入
    tools/it/jwt-parser.html
      <h2 data-zh="🔑 &lt;span data-i18n=&quot;it.jwt.title&quot; …&gt;JWT Parser&lt;/span&gt;">
           🔑 &lt;JWT Parser</h2>
  data-zh 应仅为「图标 + 中文名」，此处塞了一整个 <span> 的转义文本；
  英文正文还多出一个 '&lt;'，渲染成「🔑 <JWT Parser」。

修法（幂等，按"能不改就不改"原则）：
  1. data-zh 的前导 '&gt;' 一律剥离（仅剥离开头那一个，其余位置保留——
     正文中间的 '>'（如 'TDS&gt;5.45'）是合法内容，不动）。
  2. 4 个白名单 h2 按「页面 <title> 或 i18n zh-CN.title」权威源重写 data-zh，
     并去掉英文正文多余的 '&lt;'。英文文案取 i18n/tools/*-body.json 的 title。
  3. 含真实 HTML 标签 / JS 模板（<strong>…${raw}）的 data-zh 属动态文案模板，
     运行时由页面脚本自己填值，**不在本脚本处理范围**（36 条，另列待办）。

用法：
    python3 scripts/fix_data_zh.py --dry-run
    python3 scripts/fix_data_zh.py --apply
"""
import argparse
import glob
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 损坏二白名单：<相对路径> -> (中文标题, 英文标题)
# 中文取页面 <title>（构建期 i18n zh-CN.title 权威源与此一致），
# 英文取 i18n/tools/*-body.json 的 title。
H2_FIX = {
    'tools/it/base64-converter.html': ('Base64 编解码工具', 'Base64 Encoder / Decoder'),
    'tools/it/jwt-parser.html': ('JWT 解析', 'JWT Parser'),
    'tools/hvac/dehumidifier.html': ('除湿量计算器 Dehumidifier Sizing', 'Dehumidifier Sizing'),
    'tools/finance/stock-profit-calculator.html': ('股票盈亏计算器 卖出模式', 'Stock Profit Calculator'),
}

# 标签图标取自各页 <meta name="toolbox"> 的 icon（已是权威源），脚本运行时从页面读取
H2_LINE = re.compile(r'<h2([^>]*\bdata-zh="[^"]*"[^>]*)>(.*?)</h2>', re.S)
DZ = re.compile(r'data-zh="([^"]*)"')


def strip_leading_gt(val):
    """剥离 data-zh 开头的多余 '>'（含实体写法 &gt;），仅剥离一个。"""
    if val.startswith('&gt;'):
        return val[4:], True
    if val.startswith('>'):
        return val[1:], True
    return val, False


def process_file(rel, apply=False):
    """返回 (改动数, 说明列表)"""
    path = os.path.join(ROOT, rel)
    src = open(path, encoding='utf-8').read()
    orig = src
    notes = []

    # ---- 损坏一：所有 data-zh 的前导 &gt; ----
    # 注意：re.subn 的计数 =「匹配次数」，而非「实际修改次数」
    # （未改动的分支 return 原串也计入），故此处自行统计真实改动数。
    fix1 = [0]

    def _fix_dz(m):
        val = m.group(1)
        new, changed = strip_leading_gt(val)
        if changed:
            fix1[0] += 1
            return 'data-zh="%s"' % new
        return m.group(0)

    src = re.sub(DZ, _fix_dz, src)
    n1 = fix1[0]
    if n1:
        notes.append('剥离 data-zh 前导 &gt; ×%d' % n1)

    # ---- 损坏二：白名单 h2 整段重写 ----
    if rel in H2_FIX:
        zh_title, en_title = H2_FIX[rel]

        def _fix_h2(m):
            attrs, inner = m.group(1), m.group(2)
            # 图标沿用页面原有（原 data-zh 首位 emoji），不取 meta icon：
            # meta icon 只是占位（构建期由 _build.py TOOL_ICON_RULES 重分配），
            # 与 h2 里实际渲染的图标未必一致，照抄会改变页面现有视觉。
            old = DZ.search(attrs)
            icon = ''
            if old:
                head = old.group(1)[:1]
                if head and not head.isascii() and '&' not in head:
                    icon = head
            new_zh = ('%s %s' % (icon, zh_title)).strip()
            new_inner = ('%s %s' % (icon, en_title)).strip()
            attrs_new = DZ.sub(lambda mm: 'data-zh="%s"' % new_zh, attrs)
            return '<h2%s>%s</h2>' % (attrs_new, new_inner)

        before = src
        src = H2_LINE.sub(_fix_h2, src, count=1)
        if src != before:
            zm = DZ.search(H2_LINE.search(src).group(1))
            notes.append('重写 h2 → data-zh=%r / 英文=%r'
                         % (zm.group(1), H2_LINE.search(src).group(2)))

    if src == orig:
        return 0, notes
    if apply:
        open(path, 'w', encoding='utf-8').write(src)
    return 1, notes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true', help='落盘（默认 dry-run）')
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(ROOT, 'tools', '**', '*.html'), recursive=True))
    changed = 0
    total_dz = 0
    for p in files:
        rel = os.path.relpath(p, ROOT)
        n, notes = process_file(rel, apply=args.apply)
        if n:
            changed += 1
            total_dz += 1
            print('%-52s %s' % (rel, '; '.join(notes)))
    print()
    print('待改动文件数: %d（%s）' % (changed, '已落盘' if args.apply else 'dry-run，未写入'))
    return 0


if __name__ == '__main__':
    sys.exit(main())

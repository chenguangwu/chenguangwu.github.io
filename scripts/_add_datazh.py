#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给无 data-zh 的硬编码英文 td/th 补 data-zh 中文锚点（只加属性，不改英文文本）。

用法:
  python3 scripts/_add_datazh.py <industry|all> [--apply]
  默认 dry-run 只统计；--apply 才写盘。

高置信词典见 _zh_datazh_dict.py。标准名/文献/专名不在词典，自动跳过。
"""
import os, re, sys, collections
from _zh_datazh_dict import TERMS, KEEP_PATTERNS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools')
# 反转为 lower -> 中文
DICT = {k.lower(): v for k, v in TERMS.items()}
KEEP_RE = [re.compile(p) for p in KEEP_PATTERNS]

# <td/th 属性 >文本</td/th>，文本为纯英文单词串（可含 / - . 空格 括号 数字 符号）
CELL_RE = re.compile(r'<(td|th)\b([^>]*)>([^<]{1,80})</\1>', re.I)


def esc_attr(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')


def add_to_content(content):
    """返回 (新内容, 本次新增数, 新增明细列表)。

    ⚠ 只在真实 HTML 上改：先把 <script>/<style> 块换成等长占位符，避免把
    data-zh 加进 JS 字符串里的 innerHTML 模板 —— 那会在双引号 JS 字符串内
    引入未转义双引号，导致 "Unexpected identifier" 语法错误（2026-11-12 实测踩坑）。
    """
    protected = []

    def _hide(m):
        protected.append(m.group(0))
        return '__DZPROT%d__' % (len(protected) - 1)

    masked = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', _hide, content, flags=re.S | re.I)

    added = [0]
    details = []

    def repl(m):
        tag, attrs, txt = m.group(1), m.group(2), m.group(3)
        raw = txt.strip()
        if not raw:
            return m.group(0)
        if 'data-zh' in attrs:
            return m.group(0)
        # 纯英文判定：不含中文/日文/韩文，且至少 2 个字母
        if re.search(r'[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]', raw):
            return m.group(0)
        if not re.search(r'[A-Za-z]{2}', raw):
            return m.group(0)
        # 单位/符号跳过
        if any(p.match(raw) for p in KEEP_RE):
            return m.group(0)
        key = raw.lower()
        if key not in DICT:
            return m.group(0)
        zh = DICT[key]
        # 在起始标签末尾（> 前）插入 data-zh
        new_attrs = attrs.rstrip()
        if new_attrs.endswith('/'):
            new_attrs = new_attrs[:-1].rstrip()
        new_tag = '<%s%s data-zh="%s">%s</%s>' % (tag, new_attrs, esc_attr(zh), txt, tag)
        added[0] += 1
        details.append((raw, zh))
        return new_tag

    out = CELL_RE.sub(repl, masked)
    # 还原被保护的 script/style 块
    for i, block in enumerate(protected):
        out = out.replace('__DZPROT%d__' % i, block)
    return out, added[0], details


def main():
    args = sys.argv[1:]
    apply = '--apply' in args
    args = [a for a in args if a != '--apply']
    target = args[0] if args else 'all'
    if target == 'all':
        files = [os.path.join(r, f) for r, ds, fs in os.walk(TOOLS) for f in fs if f.endswith('.html')]
    else:
        d = os.path.join(TOOLS, target)
        if not os.path.isdir(d):
            print('NO DIR', d); return 1
        files = [os.path.join(d, f) for f in os.listdir(d) if f.endswith('.html')]
    total_added = 0
    total_files = 0
    all_details = collections.Counter()
    for p in sorted(files):
        s = open(p, encoding='utf-8').read()
        out, n, details = add_to_content(s)
        if n:
            total_files += 1
            total_added += n
            for en, zh in details:
                all_details[en] += 1
            if apply:
                open(p, 'w', encoding='utf-8').write(out)
    print('%s target=%s: 修改 %d 页 / 新增 %d 个 data-zh' % ('APPLY' if apply else 'DRY', target, total_files, total_added))
    for en, c in all_details.most_common(30):
        print('  %3dx %-30s -> %s' % (c, en, DICT[en.lower()]))
    return 0


if __name__ == '__main__':
    sys.exit(main())

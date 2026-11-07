#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 47 批 · 旧模板变体（Raw/Restore 逐字段）复选框历史缺陷修复。

旧模板三处改动：
  1) Raw: 未勾选返回 '0'（原返回 '' ⇒ 稀疏 ⇒ 全不勾状态永不入库）
  2) record: 追加全部静态复选框/单选的勾选态（原 record 只列了文本字段，勾选态根本没存）
  3) Restore: 先把记录里没有的勾选项清空（否则恢复后残留当前多勾状态）
"""
import re
import sys


def find_balanced(s, start):
    """从 s[start]=='{' 起找配对 '}'，返回闭合下标。"""
    depth = 0
    for i in range(start, len(s)):
        c = s[i]
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return i
    return -1


def patch(path):
    with open(path, encoding='utf-8') as f:
        src = f.read()
    orig = src
    notes = []

    # ---- 1) Raw 全量 ----
    old_raw = "return e.checked?(e.value||'1'):'';"
    if old_raw in src:
        src = src.replace(old_raw, "return e.checked?'1':'0';")
        notes.append('raw')

    # ---- 3) Restore 前清理 ----
    if '__cbClear' not in src:
        m = re.search(r"function (__[A-Za-z0-9_]+Restore)\(rec\)\{", src)
        if not m:
            return None, 'no-restore'
        ins = m.end()
        blk = ("var __cbs=document.querySelectorAll('input[type=checkbox],input[type=radio]');"
               "for(var __ci=0;__ci<__cbs.length;__ci++){if(!Object.prototype.hasOwnProperty.call(rec,__cbs[__ci].id))__cbs[__ci].checked=false;}")
        src = src[:ins] + blk + src[ins:]
        notes.append('restore')

    # ---- 2) record 追加勾选态 ----
    if '__rec[' not in src:
        m = re.search(r"TBKit\.history\.record\(\{", src)
        if not m:
            return None, 'no-record'
        ob = m.start() + len('TBKit.history.record(')
        cb = find_balanced(src, ob)
        if cb < 0:
            return None, 'unbalanced'
        obj = src[ob:cb + 1]
        line_start = src.rfind('\n', 0, m.start()) + 1
        indent = re.match(r'[ \t]*', src[line_start:m.start()]).group(0)
        new = (f"var __rec={obj};\n"
               f"{indent}var __cbs=document.querySelectorAll('input[type=checkbox],input[type=radio]');\n"
               f"{indent}for(var __ci=0;__ci<__cbs.length;__ci++){{if(__cbs[__ci].id)__rec[__cbs[__ci].id]=__cbs[__ci].checked?'1':'0';}}\n"
               f"{indent}TBKit.history.record(__rec);")
        src = src[:m.start()] + new + src[cb + 3:]  # +3 越过 '});'
        notes.append('record')

    if src == orig:
        return None, 'nochange'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(src)
    return notes, 'ok'


if __name__ == '__main__':
    for p in sys.argv[1:]:
        notes, st = patch(p)
        print(('✓ ' + p + '  [' + '/'.join(notes) + ']') if st == 'ok' else ('↷ ' + p + '  (' + st + ')'))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补齐复选框历史状态缺陷（第 47 批缺口 50 页）。

两处同构改动（与已修 302 页完全一致）：
  1) 快照把未勾选记为 '0' 而非空串（原写法稀疏，全不勾时快照为空 ⇒ 该状态永不入库）
  2) 恢复前清空记录里没有的勾选项（旧记录稀疏，不清理会残留当前多勾状态）
"""
import re
import sys

OLD_SNAP = "var v=(t==='checkbox'||t==='radio')?(e.checked?(e.value||'1'):''):e.value;"
NEW_SNAP = "var v=(t==='checkbox'||t==='radio')?(e.checked?'1':'0'):e.value;"

BLOCK_BODY = [
    "// 恢复前先清空未记录的勾选：旧记录是稀疏的（只存勾选中的项），",
    "// 不清理会把当前多勾的权限带过来（600→777→恢复 600 仍显示 777）。",
    "var __cbs=document.querySelectorAll('input[type=checkbox],input[type=radio]');",
    "for(var __ci=0;__ci<__cbs.length;__ci++){",
    "    if(!Object.prototype.hasOwnProperty.call(rec,__cbs[__ci].id)) __cbs[__ci].checked=false;",
    "}",
]
MARK = "__cbs[__ci].checked=false"


def patch(path):
    with open(path, encoding='utf-8') as f:
        src = f.read()
    orig = src
    notes = []

    # ---- 改动 1：快照全量 ----
    if OLD_SNAP in src:
        src = src.replace(OLD_SNAP, NEW_SNAP)
        notes.append('snap')
    elif NEW_SNAP not in src:
        return None, 'no-snap-pattern'

    # ---- 改动 2：恢复前清理 ----
    if MARK not in src:
        m = re.search(r"TBKit\.history\.mount\(", src)
        if not m:
            return None, 'no-history-mount'
        ti = src.find('try{', m.end())
        if ti < 0 or ti - m.end() > 400:
            return None, 'no-try'
        ins = src.find('\n', ti) + 1
        # 取下一行的缩进作为插入块缩进
        line = src[ins:src.find('\n', ins)]
        indent = line[:len(line) - len(line.lstrip())] or '                '
        block = ''.join(indent + ln + '\n' for ln in BLOCK_BODY)
        src = src[:ins] + block + src[ins:]
        notes.append('clear')

    if src == orig:
        return None, 'nochange'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(src)
    return notes, 'ok'


if __name__ == '__main__':
    lst = sys.argv[1]
    ok = skip = bad = 0
    for p in open(lst, encoding='utf-8').read().split():
        notes, st = patch(p)
        if st == 'ok':
            ok += 1
            print(f"✓ {p}  [{'/'.join(notes)}]")
        else:
            skip += 1
            print(f"↷ {p}  ({st})")
    print(f"--- 改动 {ok} / 跳过 {skip} ---")

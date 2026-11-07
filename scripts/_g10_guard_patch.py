#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G10：给 __tbInputGuard 页加「护栏触发即清空明细表」包装。

背景：页面主结果在护栏失败时会写「请填写「X」后再计算」，但明细表（matrix.table 渲染的
#<pre>Table）保留上一组参数的行 ⇒ 「导出明细 CSV」把旧参数的结果当成本次结果带走。

做法（幂等）：把原函数改名为 __tbInputGuardCore，外面套一层同名包装：
    返回非空消息 ⇒ 先把 #<pre>Table 清空，再返回消息。
"""
import re
import sys

HDR = 'function __tbInputGuard(_ids,_labels){'


def patch(path):
    with open(path, encoding='utf-8') as f:
        s = f.read()
    if '__tbInputGuardCore' in s:
        return 'skip-already'
    cnt = s.count(HDR)
    if cnt == 0:
        return 'skip-nohdr'
    m = re.search(r"matrix\.table\('#([A-Za-z0-9_]+Table)'", s)
    if not m:
        return 'skip-notable'
    tbl = m.group(1)

    wrapper = (
        'function __tbInputGuard(_ids,_labels){\n'
        '  var __r=__tbInputGuardCore(_ids,_labels);\n'
        f'  if(__r){{var __t=document.getElementById(\'{tbl}\');if(__t)__t.innerHTML=\'\';}}\n'
        '  return __r;\n'
        '}\n'
        f'function __tbInputGuardCore(_ids,_labels){{'
    )
    # 有些页存在两份同名定义（早期批次插入 + 原文），后一份才生效 ⇒ 只改最后一份。
    i = s.rfind(HDR)
    s = s[:i] + wrapper + s[i + len(HDR):]

    # 终态断言：必须恰好一个包装 + 一个 core
    assert s.count('__tbInputGuardCore') == 2, path
    assert s.count(f"getElementById('{tbl}')") >= 1, path
    with open(path, 'w', encoding='utf-8') as f:
        f.write(s)
    return 'ok'


if __name__ == '__main__':
    lst = sys.argv[1]
    stat = {}
    for p in open(lst, encoding='utf-8').read().split():
        r = patch(p)
        stat[r] = stat.get(r, 0) + 1
        if r != 'ok':
            print(f'↷ {p}  ({r})')
    print('---', stat)

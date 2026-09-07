#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 electromagnetism 分类下硬编码 B 类 opt 套话。

仅 2 页含「工作与生活中的相关计算与查询」：
  - energy-inductor.html
  - magnetic-flux.html
每页 3 处：JSON-LD FAQ / 适用场景段 / opt-faq dd。
"""
import sys
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools', 'electromagnetism')

B_OPT = '工作与生活中的相关计算与查询'

# 工具名 → 真实场景描述
REPLACEMENTS = {
    'energy-inductor': '电感储能用于开关电源纹波抑制、感性负载去磁续流、磁悬浮超导线圈储能、电磁发射装置等场景。',
    'magnetic-flux': '磁通用于电机/发电机定子磁路设计、变压器铁芯截面积选取、霍尔传感器磁场测量、磁屏蔽设计与磁路仿真等场景。',
}


def fix_page(path: str) -> bool:
    fn = os.path.basename(path).replace('.html', '')
    if fn not in REPLACEMENTS:
        return False
    text = open(path, encoding='utf-8').read()
    new = text.replace(B_OPT, REPLACEMENTS[fn])
    if new != text:
        open(path, 'w', encoding='utf-8').write(new)
        return True
    return False


def main():
    if '--dry' in sys.argv:
        dry = True
    else:
        dry = False

    pages = ['energy-inductor.html', 'magnetic-flux.html']
    total = 0
    for fn in pages:
        path = os.path.join(TOOLS, fn)
        if not os.path.exists(path):
            print(f'  ⚠️  missing: {fn}')
            continue
        text = open(path, encoding='utf-8').read()
        before = text.count(B_OPT)
        if not dry:
            changed = fix_page(path)
            after_text = open(path, encoding='utf-8').read()
            after = after_text.count(B_OPT)
            print(f'  {fn}: before={before} -> after={after}  {"✅" if after==0 else "❌残留"}')
            if changed:
                total += 1
        else:
            print(f'  [DRY] {fn}: 残留 {before} 处')

    print(f'\n{"dry 仅检查" if dry else f"已修改 {total} 个文件"}')


if __name__ == '__main__':
    main()
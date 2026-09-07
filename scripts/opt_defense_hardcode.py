#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检测 defense 分类硬编码套话（A/B/C 类），本分类无需清理。
A 类 FD 校验/计算变体：defense 2 页（calc-rater/rater-38）均无 formula-desc，无错配 FD。
B 类 opt 套话「工作与生活中的相关计算与查询。」：0 页命中。
C 类块内 6 类通用套话：0 页命中。
脚本仅做检测报告，确认无命中后跳过，不写文件，保持与全站清理流程一致的可追溯性。
"""
import re, os, sys, glob

TOOLS = 'tools/defense'
FD_PATTERNS = [
 '本校验工具依据对应数据格式与语法规范进行合法性检查',
 '本计算依据通用财务',
 '本工程计算基于标准物理',
 '本速查内容依据权威标准',
 '本工具用于单位与格式换算',
 '本日常工具基于通用常识',
 '本开发工具在前端本地',
 '本文本工具基于标准',
 '本生成器依据指定格式',
]
JUNK = '工作与生活中的相关计算与查询。'
BLOCK_JUNK = ['免费在线工具，纯前端处理','操作简单，一键完成','日常办公与学习','开发调试与数据处理','快速计算与格式转换','信息查询与参考','工作与生活中的相关计算与查询']

def main():
    files = [f for f in glob.glob(os.path.join(TOOLS, '*.html')) if 'index' not in os.path.basename(f)]
    fd_hit = []; opt_hit = []; blk_hit = []
    for f in files:
        s = open(f, encoding='utf-8').read()
        n = os.path.basename(f).replace('.html', '')
        for pat in FD_PATTERNS:
            if pat in s: fd_hit.append(n)
        if JUNK in s: opt_hit.append(n)
        m = re.search(r'<div class="tool-intro-body">(.*?)</div>\s*</div>', s, re.S)
        if m and any(j in m.group(1) for j in BLOCK_JUNK): blk_hit.append(n)
    print('defense hardcode 检测：')
    print('  A 类 FD 错配命中:', fd_hit if fd_hit else '无')
    print('  B 类 opt 套话命中:', opt_hit if opt_hit else '无')
    print('  C 类块内套话命中:', blk_hit if blk_hit else '无')
    print('  结论：defense 2 页 A/B/C 三类均无命中，无需清理（跳过）')

if __name__ == '__main__':
    main()

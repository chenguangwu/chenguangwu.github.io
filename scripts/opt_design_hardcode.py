#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""design 分类硬码清理检测（A/B/C 三类）。

之前的探查结论：
- A 类 FD：物理/速查/SI/生成器/设计工具五类全部语义相符（快门速度=BPM=物理、
  音阶=速查、色温=SI、各生成器/设计工具=对应变体），无错配，无需清理。
- B 类 opt 套话「工作与生活中的相关计算与查询」：0 页。
- C 类块内 6 类通用套话：0 页。
本脚本对所有 design 页做全量检测，输出命中数（预期全 0），不做任何写入，
以保持可追溯、可复现。
"""
import glob, os, re, json

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OPT = '工作与生活中的相关计算与查询'
BLOCK_JUNK = ['免费在线工具，纯前端处理', '操作简单，一键完成', '日常办公与学习',
              '开发调试与数据处理', '快速计算与格式转换', '信息查询与参考', OPT]
FD_MIS = ['本校验工具依据对应数据格式与语法规范进行合法性检查']

def main():
    files = [f for f in glob.glob(os.path.join(D, 'tools/design/*.html')) if 'index' not in os.path.basename(f)]
    opt_hits = []
    blk_hits = []
    fd_hits = []
    for f in files:
        s = open(f, encoding='utf-8').read()
        n = os.path.basename(f).replace('.html', '')
        if OPT in s:
            opt_hits.append(n)
        m = re.search(r'<div class="tool-intro-body">(.*?)</div>\s*</div>', s, re.S)
        if m and any(j in m.group(1) for j in BLOCK_JUNK):
            blk_hits.append(n)
        for pat in FD_MIS:
            if pat in s:
                fd_hits.append((n, pat))
    print('=== design 硬码清理检测 ===')
    print('扫描页数:', len(files))
    print('A 类 FD 错配命中:', fd_hits if fd_hits else '无（全部语义相符，跳过）')
    print('B 类 opt 套话命中:', opt_hits if opt_hits else '无（跳过）')
    print('C 类块内套话命中:', blk_hits if blk_hits else '无（跳过）')
    if not (fd_hits or opt_hits or blk_hits):
        print('结论：design 三类套话均 0 命中，无需清理，直接跳过（可追溯）。')
    # JSON-LD 合法性抽检（全页）
    bad = []
    for f in files:
        s = open(f, encoding='utf-8').read()
        j = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
        if j:
            try:
                json.loads(j.group(1))
            except Exception:
                bad.append(os.path.basename(f).replace('.html', ''))
    print('JSON-LD 非法页:', bad if bad else '无')

if __name__ == '__main__':
    main()

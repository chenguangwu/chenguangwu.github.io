# -*- coding: utf-8 -*-
"""清理 dynamics B 类硬编码套话。
仅 banked-curve 含「工作与生活中的相关计算与查询」占位（JSON-LD FAQ + 旧 deep-dive dd，
构建后仅 JSON-LD 残留）→ 真实场景。其余页 A 类 formula-desc 为真实/语义相符描述，无需处理；
C 类 0 命中。
"""
import sys, os

DRY = '--dry' in sys.argv
B_OLD = '工作与生活中的相关计算与查询'
B_NEW = '用于公路与赛道弯道的倾角设计、无摩擦设计车速估算与限速参考，帮助理解向心力来源与行车安全。'

def main():
    p = 'tools/dynamics/banked-curve.html'
    s = open(p, encoding='utf-8').read()
    cnt = s.count(B_OLD)
    new = s.replace(B_OLD + '。', B_NEW + '。').replace(B_OLD, B_NEW)
    print('(B)[banked-curve] 替换前出现 %d 次, 替换后残留: %s' % (cnt, B_OLD in new))
    if DRY:
        print('DRY 完成'); return
    open(p, 'w', encoding='utf-8').write(new)
    print('写入完成')

if __name__ == '__main__':
    main()

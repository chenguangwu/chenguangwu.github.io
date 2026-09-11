#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修正 automotive/loan-calculator deep-dive 示例中的算术错误。

原文：月供≈3137 元，总利息≈3137×36−105000≈12832 元
实际：3137×36 − 105000 = 7932，与 12832 矛盾；按精确月供 3137.5 元累计，
      总利息 = 3137.5×36 − 105000 ≈ 7951 元（页面 calc 即此口径）。
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, 'i18n/tools/content_deepdive.json')

OLD = '月利率 r=0.048/12=0.004，月供=105000×0.004×(1.004)^36/((1.004)^36−1)≈3137 元，总利息≈3137×36−105000≈12832 元。'
NEW = '月利率 r=0.048/12=0.004，月供=105000×0.004×(1.004)^36/((1.004)^36−1)≈3137.5 元（约 3138 元），总利息 = 3137.5×36−105000 ≈ 7951 元。'

d = json.load(open(P, encoding='utf-8'))
n = len(d)
hits = 0
for e in d['automotive/loan-calculator'].get('examples', []):
    if OLD in e.get('body', ''):
        e['body'] = e['body'].replace(OLD, NEW)
        hits += 1
assert len(d) == n, '键数变化: %d -> %d' % (n, len(d))
with open(P, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=1, separators=(",", ": "))
print('替换命中: %d | 键数: %d（守恒）' % (hits, n))
print('新示例:', d['automotive/loan-calculator']['examples'][0]['body'][-60:])

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修正 automotive/calc-5 与 calc-72 deep-dive 示例中的算术微偏差。

calc-5 ：c运行 v=27.8m/s、s=40m 时 a = 27.8² ÷ 80 = 9.6605 → 9.66 m/s²（原文写 9.67），
         等效 g = 9.6605 ÷ 9.81 = 0.9847 → 0.98g（原文写 0.99g）。
calc-72：单缸排量 π/4 × 86² × 86 = 499556 mm³（原文写 499900），
         故压缩比 = (56000 + 499556) ÷ 56000 = 9.9206 → 9.92（原文写 9.93）。
以上均按 node 实跑取值。
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, 'i18n/tools/content_deepdive.json')

SUBS = {
    'automotive/calc-5': [
        ('≈9.67m/s²', '≈9.66m/s²'),
        ('≈0.99g', '≈0.98g'),
    ],
    'automotive/calc-72': [
        ('499900mm³', '499556mm³'),
        ('499900)/56000≈9.93', '499556)/56000≈9.92'),
    ],
}

d = json.load(open(P, encoding='utf-8'))
n = len(d)
for key, pairs in SUBS.items():
    for e in d[key].get('examples', []):
        body = e.get('body', '')
        for old, new in pairs:
            if old in body:
                body = body.replace(old, new)
        e['body'] = body
    print('[%s] %s' % (key, d[key]['examples'][0]['body']))
assert len(d) == n, '键数变化'
with open(P, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=1, separators=(",", ": "))
print('键数守恒:', n)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""event 批：用确定性字符串替换修正 assessor-65.html 中构建不重写的两处字段。

- toolbox meta 的 cat=validator -> calculator（错标修正：本工具是四维度加权计分器）
- h2 可见英文（en-US 模式展示）：机翻坏名 -> Event Effectiveness Assessment
deep-dive 区块由 _build.py 据 content_deepdive.json 重建，此处不动。
"""
P = 'tools/event/assessor-65.html'
s = open(P, encoding='utf-8').read()

repl = [
    ('cat=validator,industry=event', 'cat=calculator,industry=event'),
    ('🔧 Evaluate ( Effect / Report / Improvement ) System', '🔧 Event Effectiveness Assessment'),
]
for a, b in repl:
    n = s.count(a)
    s = s.replace(a, b)
    print('replaced %r x%d' % (a, n))

open(P, 'w', encoding='utf-8').write(s)

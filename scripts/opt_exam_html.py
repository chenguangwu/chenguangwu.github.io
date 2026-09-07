#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""exam 批工具页 HTML 定点修正（构建不重写的部分）：
- exam-timer: cat=convert -> cat=calculator（计时器非转换）
- gpa-calculator: 可见 h2 英文名 GPA Calculate -> GPA Calculator
- study-planner: 可见 h2 英文名 Learning Plan -> Study Plan
- 4 工具 <p> 英文 fallback 套话/泛化文案 -> 真实描述

title-en / desc-en 由 _build.py 依据 _en_override.json 重写，无需在此改。
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools', 'exam')


def edit(fn, repls):
    p = os.path.join(TOOLS, fn)
    with open(p, encoding='utf-8') as f:
        s = f.read()
    for old, new in repls:
        if old not in s:
            raise SystemExit('NOT FOUND in %s: %r' % (fn, old[:60]))
        s = s.replace(old, new, 1)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(s)
    print('edited', fn, '(%d 处)' % len(repls))


edit('exam-timer.html', [
    ('cat=convert,industry=exam', 'cat=calculator,industry=exam'),
    ('Exam Timer is available directly in your browser, with no data uploaded.',
     'Countdown and count-up exam timer with progress bar and auto beep; log practice sessions locally. Browser-only, no data uploaded.'),
])

edit('gpa-calculator.html', [
    ('🎓 GPA Calculate', '🎓 GPA Calculator'),
    ('GPA Calculate - calculate online, free and accurate.',
     'Weighted GPA across 5 grading scales: standard 4.0, improved 4.0, 5.0, percentage and China 4.0. Browser-only, no data uploaded.'),
])

edit('study-planner.html', [
    ('📝 Learning Plan', '📝 Study Plan'),
    ('Learning Plan is available directly in your browser, with no data uploaded.',
     'Plan study tasks by subject and priority, track focus with a Pomodoro timer and review completion stats. Browser-only, no data uploaded.'),
])

edit('certificate-check.html', [
    ('Certificate Query is available directly in your browser, with no data uploaded.',
     'Search 30+ certificates across language, IT, finance and professional fields — exam requirements, difficulty, fees and career value at a glance. Browser-only, no data uploaded.'),
])

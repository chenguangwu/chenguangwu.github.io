#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""exam 批英文 i18n 清理：_en_override.json / slug-en.json / exam.json 套话清零 + gpa/study-planner 英文名修正。

_en_override.json 与 slug-en.json 中 4 工具条目均已存在，仅更新 en/ed（保留 ind 等其它字段）。
exam.json 的 en-US.title/intro 同步去套话、改正确英文名。
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OV = os.path.join(ROOT, 'i18n', 'tools', '_en_override.json')
SL = os.path.join(ROOT, 'i18n', 'tools', 'slug-en.json')
EX = os.path.join(ROOT, 'i18n', 'tools', 'exam.json')

ED = {
    "exam/certificate-check": (
        "Search 30+ common certificates across language, IT, finance and professional fields — "
        "exam requirements, difficulty, fees and career value at a glance. Browser-only, no data uploaded."
    ),
    "exam/exam-timer": (
        "Countdown and count-up exam timer with progress bar and auto beep; log practice sessions "
        "locally. Browser-only, no data uploaded."
    ),
    "exam/gpa-calculator": (
        "Weighted GPA across 5 grading scales: standard 4.0, improved 4.0, 5.0, percentage and "
        "China 4.0. Browser-only, no data uploaded."
    ),
    "exam/study-planner": (
        "Plan study tasks by subject and priority, track focus with a Pomodoro timer and review "
        "completion stats. Browser-only, no data uploaded."
    ),
}

EN = {
    "exam/certificate-check": "Certificate Query",
    "exam/exam-timer": "Exam Timer",
    "exam/gpa-calculator": "GPA Calculator",
    "exam/study-planner": "Study Plan",
}

INTRO = {
    "exam/certificate-check": (
        "Search 30+ certificates across language, IT, finance and professional fields — exam "
        "requirements, difficulty, fees and career value at a glance. Browser-only, no data uploaded."
    ),
    "exam/exam-timer": (
        "Countdown and count-up exam timer with progress bar and auto beep; log practice sessions "
        "locally. Browser-only, no data uploaded."
    ),
    "exam/gpa-calculator": (
        "Weighted GPA across 5 grading scales: standard 4.0, improved 4.0, 5.0, percentage and "
        "China 4.0. Browser-only, no data uploaded."
    ),
    "exam/study-planner": (
        "Plan study tasks by subject and priority, track focus with a Pomodoro timer and review "
        "completion stats. Browser-only, no data uploaded."
    ),
}


def load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def save(p, d):
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write('\n')


# 1) _en_override.json
ov = load(OV)
for k in EN:
    if k not in ov:
        raise SystemExit('missing _en_override key: ' + k)
    ov[k]['en'] = EN[k]
    ov[k]['ed'] = ED[k]
save(OV, ov)
print('_en_override.json 更新:', list(EN.keys()))

# 2) slug-en.json
sl = load(SL)
for k in EN:
    if k not in sl:
        raise SystemExit('missing slug-en key: ' + k)
    sl[k]['en'] = EN[k]
    sl[k]['ed'] = ED[k]
save(SL, sl)
print('slug-en.json 更新:', list(EN.keys()))

# 3) exam.json —— 注意：exam.json 用裸 slug（certificate-check），而 _en_override/slug-en 用全 slug（exam/...）
ex = load(EX)
for full, en in EN.items():
    slug = full.split('/')[-1]
    if slug not in ex:
        raise SystemExit('missing exam.json key: ' + slug)
    ex[slug]['en-US']['title'] = en
    ex[slug]['en-US']['h1'] = en
    ex[slug]['en-US']['intro'] = INTRO[full]
save(EX, ex)
print('exam.json 更新:', [k.split('/')[-1] for k in EN.keys()])

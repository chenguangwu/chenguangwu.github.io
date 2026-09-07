#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""event 批：清理 event/assessor-65 的英文 i18n 套话并改真实名。

- i18n/tools/slug-en.json       : en / ed
- i18n/tools/_en_override.json  : en / ed / ind（构建据其重写 title-en / desc-en）
- i18n/tools/event.json         : zh-CN.title/h1/desc + en-US.title/h1/intro（行业 i18n 权威源）

去掉机翻坏名 "Evaluate ( Effect / Report / Improvement ) System" 与 "free online tool" 套话。
幂等可重跑。
"""
import json

EN_TITLE = "Event Effectiveness Assessment"
EN_DESC = ("Event Effectiveness Assessment scores events across attendance, budget execution, "
           "satisfaction, and goal achievement, then grades results and suggests improvements "
           "— 100% client-side, no data uploaded.")
EN_DESC_SHORT = ("Event Effectiveness Assessment scores events across attendance, budget execution, "
                 "satisfaction, and goal achievement — 100% client-side, no data uploaded.")

# 1) slug-en.json
sp = 'i18n/tools/slug-en.json'
se = json.load(open(sp, encoding='utf-8'))
se['event/assessor-65'] = {"en": EN_TITLE, "ed": EN_DESC_SHORT}
json.dump(se, open(sp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# 2) _en_override.json
op = 'i18n/tools/_en_override.json'
eo = json.load(open(op, encoding='utf-8'))
eo['event/assessor-65'] = {"en": EN_TITLE, "ed": EN_DESC, "ind": "event"}
json.dump(eo, open(op, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# 3) event.json（行业 i18n 权威源）
ep = 'i18n/tools/event.json'
ev = json.load(open(ep, encoding='utf-8'))
ev['assessor-65']['zh-CN']['title'] = "活动效果评估"
ev['assessor-65']['zh-CN']['h1'] = "活动效果评估"
ev['assessor-65']['zh-CN']['desc'] = "活动效果评估"
ev['assessor-65']['en-US'] = {"title": EN_TITLE, "h1": EN_TITLE, "intro": EN_DESC}
json.dump(ev, open(ep, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

print("UPDATED i18n: slug-en / _en_override / event.json for event/assessor-65")

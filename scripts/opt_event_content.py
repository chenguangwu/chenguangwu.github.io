#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""event 批：把 event/assessor-65 的 content_deepdive 占位壳替换为真实活动效果评估内容。

数据源 i18n/tools/content_deepdive.json：_build.py 据此重建工具页 deep-dive 区块，
直接改 HTML 会被覆盖。本脚本只更新 event/assessor-65 一个键，幂等可重跑。
"""
import json

P = 'i18n/tools/content_deepdive.json'
d = json.load(open(P, encoding='utf-8'))
k = 'event/assessor-65'

entry = {
    "title": "活动效果评估",
    "summary": "活动效果评估工具：输入到场率、预算执行、满意度、目标达成率等关键指标，按四维度加权模型计算综合得分（0–100）并划分等级，自动给出改进建议，用于营销与运营活动复盘。",
    "scenarios": [
        "会议、展览、庆典、培训等活动结束后，快速量化整体成效，向管理层输出可复核的复盘报告。",
        "对比多场同类活动（如不同城市路演）的得分与等级，沉淀可复用的效果基线。",
        "活动策划阶段用目标值做预评估，反向校准邀请规模、预算与满意度目标设定。"
    ],
    "examples": [
        {
            "title": "一场 500 人会议的效果评估",
            "body": "目标参与 500、实际到场 450（到场率 90%），预算 50 万、实际支出 45 万（执行率 90%），满意度 8.5/10，目标达成率 85%。综合得分 = 90×0.25 + (100−|90−100|)×0.2 + 8.5×10×0.3 + 85×0.25 = 22.5+18+25.5+21.25 = 87.25 → 等级「卓越」，无需改进。"
        }
    ],
    "faqs": [
        {
            "q": "四个维度的权重为什么这样设定？",
            "a": "到场率与预算执行衡量投入产出基本盘（合计 45%），满意度反映体验质量（30%），目标达成率衡量业务结果（25%）；可在此基础上按活动类型微调，但建议保持总和 100%。"
        },
        {
            "q": "预算执行率偏离 100% 越多为什么得分越低？",
            "a": "模型用 100−|执行率−100| 衡量贴合度：执行率恰好 100% 得满分，超支或严重节余都说明预算管控偏差，贴合度下降、得分降低，引导精细化成本控制。"
        }
    ]
}

old = d.get(k)
d[k] = entry
json.dump(d, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print("UPDATED content_deepdive[%s]" % k)
print("old had summary:", bool(old and old.get('summary')))

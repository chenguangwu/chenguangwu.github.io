#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""真实化 brand/assessor-51 的 deep-dive 内容（替换另一种占位模板）。

占位模板特征：scenarios 形如「在brand场景中先确认 Assessor 51 口径与边界…」，
examples/faqs 为通用模板。本脚本用真实 Interbrand 品牌评估场景覆盖。
indent=1 写入，避免全文件重排。
"""
import json

PATH = "i18n/tools/content_deepdive.json"
KEY = "brand/assessor-51"

d = json.load(open(PATH, encoding="utf-8"))

real = {
    "title": "品牌（资产/评估/审计）体系",
    "scenarios": [
        "并购与投融资尽职调查：买方用本工具快速估算标的公司品牌资产价值，作为收购溢价与对赌条款谈判的量化依据；输入标的近三年平均净利润、行业品牌贡献率与品牌强度系数即可得出区间。",
        "年度品牌审计：市场部按 Interbrand 七维度（领导力、稳定力、市场力、国际化、趋势力、支持力、保护力）自评品牌强度，逐年更新品牌资产估值，跟踪品牌健康度与同业位次变化。",
        "品牌战略规划：对比不同投入方案（提升品牌强度系数 vs 延长收益预测年限）对品牌资产现值的影响，辅助市场预算在品牌建设、渠道扩张与研发之间的分配决策。",
    ],
    "examples": [
        {
            "title": "演练示例（默认参数）",
            "body": "输入品牌年净利润 5000 万元、贡献率 65%、强度系数 0.75、折现率 12%、预测年限 10 年、市占率 15%：品牌净利润=3250 万元，品牌强度评分=75（强势品牌），调整后折现率约 12.5%，10 年品牌净利润现值约 1.8 亿元，品牌等级「强势品牌」。把强度系数调到 0.9 可对比现值提升幅度。",
        }
    ],
    "faqs": [
        {
            "q": "本工具与 Interbrand 官方模型有何差异？",
            "a": "Interbrand 官方用「品牌净利润 × 品牌强度倍数（由 S 曲线将 0–100 分映射为 0–20 倍）」一次性估算；本工具改用折现现金流近似（品牌净利润按调整后折现率分年折现），更直观体现年限与折现率影响，适合快速估算与管理参考。",
        },
        {
            "q": "品牌贡献率如何确定？",
            "a": "通过消费者调研或联合分析分离「品牌」对购买决策的影响占比；无调研数据时可对标同行业上市公司披露的品牌贡献率区间（通常 30%–70%），并在报告中注明假设来源。",
        },
        {
            "q": "品牌强度七维度具体指什么？",
            "a": "领导力、稳定力、市场力、国际化、趋势力、支持力、保护力。各维度加权得 0–100 分，分数越高代表品牌抗风险与溢价能力越强，直接决定资产倍数或折现结果。",
        },
        {
            "q": "结果能直接写进财报吗？",
            "a": "按 IAS 38，企业内部自创商誉与品牌一般不确认为无形资产；本工具结果建议作为管理参考与投融资沟通素材，正式财务披露须经审计并符合会计准则。",
        },
    ],
}

d[KEY] = real
json.dump(d, open(PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print("updated:", KEY)
# 校验无旧占位残留（两种模板都查）
left1 = [k for k, v in d.items() if k.startswith("brand/") and "先做单位与边界核对" in v.get("scenarios", [""])[0]]
left2 = [k for k, v in d.items() if k.startswith("brand/") and "在brand场景中先确认" in v.get("scenarios", [""])[0]]
print("brand placeholder(先做单位):", len(left1), " brand placeholder(在brand场景):", len(left2))

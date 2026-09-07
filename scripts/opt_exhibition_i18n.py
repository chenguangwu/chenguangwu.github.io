# -*- coding: utf-8 -*-
"""exhibition 批：清理英文 i18n 套话（free online tool），同步真实英文名/描述。

- _en_override.json  : 全 slug，更新 en / ed（保留 ind）
- slug-en.json       : 全 slug，更新 en / ed
- exhibition.json     : 裸 slug，更新 en-US.title / h1 / intro
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EN_OVERRIDE = os.path.join(ROOT, 'i18n', 'tools', '_en_override.json')
SLUG_EN = os.path.join(ROOT, 'i18n', 'tools', 'slug-en.json')
EXHIBITION = os.path.join(ROOT, 'i18n', 'tools', 'exhibition.json')

# 短英文名（h2 / title-en / en-US）
EN_NAME = {
    "analysis-61": "Exhibition Cost Statistics",
    "analysis-pnl": "Exhibition P&L Statistics",
    "assessor-60": "Post-show Evaluation Report",
    "assessor-61": "Exhibition Scorecard",
    "assessor-evacuation": "Venue Safety Assessment",
    "stats-12": "Audience Statistics",
}

# _en_override.ed：真实英文描述（不含 free online tool 套话）
ED_OVERRIDE = {
    "analysis-61": "Descriptive statistics for exhibition cost and budget line items: count, sum, mean, median, range, variance and standard deviation. Browser-only, no data uploaded.",
    "analysis-pnl": "Descriptive statistics for exhibition revenue, expense and profit-loss figures: count, sum, mean, median, range, variance, standard deviation. Browser-only, no data uploaded.",
    "assessor-60": "Evaluate exhibition ROI, lead conversion and cost-per-lead from booth, travel and revenue inputs, then generate a post-show assessment with follow-up actions. Browser-only, no data uploaded.",
    "assessor-61": "Score an exhibition across 6 dimensions on a 1–5 scale — scale, audience quality, branding, lead efficiency, organization, ROI — for a composite score and improvement pointers. Browser-only, no data uploaded.",
    "assessor-evacuation": "Assess exhibition venue safety — evacuation width, egress distance, floor load and fire systems — against standard thresholds, output risks and remediation. Browser-only, no data uploaded.",
    "stats-12": "Descriptive statistics for audience traffic, dwell time and survey feedback: count, sum, mean, median, range, variance, standard deviation. Browser-only, no data uploaded.",
}

# 运行时英文 intro（slug-en.ed / exhibition.json en-US.intro）
EN_INTRO = {
    "analysis-61": "Compute descriptive statistics — count, sum, mean, median, range, variance, standard deviation — for exhibition cost and budget items. Runs entirely in your browser.",
    "analysis-pnl": "Summarize exhibition revenue, expense and profit-loss figures with descriptive statistics — count, sum, mean, median, range, variance, standard deviation. Runs entirely in your browser.",
    "assessor-60": "Enter booth, travel and revenue figures to evaluate exhibition ROI, lead conversion and cost-per-lead, then get a post-show assessment with follow-up actions. Runs entirely in your browser.",
    "assessor-61": "Rate an exhibition across 6 dimensions (scale, audience quality, branding, lead efficiency, organization, ROI) on a 1–5 scale to get a composite score and improvement pointers. Runs entirely in your browser.",
    "assessor-evacuation": "Check exhibition venue safety: evacuation width, egress distance, floor load and fire systems against common thresholds, then list risks and remediation. Runs entirely in your browser.",
    "stats-12": "Summarize audience traffic, dwell time and survey feedback with descriptive statistics — count, sum, mean, median, range, variance, standard deviation. Runs entirely in your browser.",
}


def load(p):
    with open(p, 'r', encoding='utf-8') as f:
        return json.load(f)


def dump(p, obj):
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def main():
    en = load(EN_OVERRIDE)
    sl = load(SLUG_EN)
    ex = load(EXHIBITION)

    for slug, name in EN_NAME.items():
        full = "exhibition/" + slug
        # _en_override
        if full not in en:
            raise SystemExit("缺少 _en_override 键: " + full)
        en[full]["en"] = name
        en[full]["ed"] = ED_OVERRIDE[slug]
        # slug-en
        if full not in sl:
            raise SystemExit("缺少 slug-en 键: " + full)
        sl[full]["en"] = name
        sl[full]["ed"] = EN_INTRO[slug]
        # exhibition.json（裸 slug）
        if slug not in ex:
            raise SystemExit("缺少 exhibition.json 键: " + slug)
        ex[slug]["en-US"]["title"] = name
        ex[slug]["en-US"]["h1"] = name
        ex[slug]["en-US"]["intro"] = EN_INTRO[slug]

    dump(EN_OVERRIDE, en)
    dump(SLUG_EN, sl)
    dump(EXHIBITION, ex)
    print("英文 i18n 已清理并同步 %d 个 exhibition 工具" % len(EN_NAME))


if __name__ == '__main__':
    main()

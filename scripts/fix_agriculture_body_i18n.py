#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""agriculture (62) 分类英文态数据源根治：同步三端 + 补中文态缺口。

三处数据源（与 science/sports/fun/ai/biz/life 同坑，§6「英文态数据源三处」）：
  ① i18n/tools/agriculture-body.json   -> build `_prerender_tool_body` 预渲染 h1 + 首个 <p>
  ② i18n/tools/agriculture.json en-US  -> industry JSON 的 ed 最高优先级源
  ③ i18n/tools/_en_override.json       -> 运行时 en（h2/h1）与 ed

本轮缺口：
  - 62 页 en-US / body / ov 三端英文全为占位或代号（如 "Convert Content 1" / "X is a free online tool."）
  - 3 页（cycle-honey / detector-13 / detector-nutrition）在三端**全缺**，由 ZH_TITLE / ZH_INTRO 补中文名与简介
  - agriculture-body.json 4 个孤儿键（calc-11 / simulator-area / countdown-6 / stats-recorder）全站无页面，删除

用法：
  python3 scripts/fix_agriculture_body_i18n.py --dry-run
  python3 scripts/fix_agriculture_body_i18n.py --apply
"""
import argparse
import glob
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools', 'agriculture')
OV = os.path.join(ROOT, 'i18n', 'tools', '_en_override.json')
BODY = os.path.join(ROOT, 'i18n', 'tools', 'agriculture-body.json')
GIS = os.path.join(ROOT, 'i18n', 'tools', 'agriculture.json')

# 3 个三端全缺的工具：补中文名与简介（依据页面 <h1> 与实际功能）
ZH_TITLE = {
    'cycle-honey': '采蜜期（摇蜜周期）安排',
    'detector-13': '蜂螨（寄生率）检测',
    'detector-nutrition': '花粉（发酵）全营养检测',
}

ZH_INTRO = {
    'cycle-honey': '按蜂箱的流蜜周期与开始日期排定摇蜜（取蜜）计划，生成摇蜜日历与提醒，辅助蜂场作业组织与蜜源调度。',
    'detector-13': '输入样本工蜂数与检出蜂螨数，计算蜂螨寄生率并评估蜂群受害程度，辅助确定治螨时机与用药方案。',
    'detector-nutrition': '按蛋白质、脂肪、还原糖、水分、灰分与乳酸含量评估（发酵）蜂花粉的营养品质与发酵程度，辅助原料品质判定与定价。',
}

# NAME = 英文名（h1 / 导航 / 英文态标题），INTRO = 真实英文描述（intro / ed）。
NAME = {
    'agri-calculator': 'Agriculture Calculator',
    'assessor-1': 'Harvest Loss Rate (Machine/Manual) Assessor',
    'calc-12': 'Irrigation Water Requirement Estimator',
    'calc-13': 'Farm Machinery Fuel Consumption Estimator',
    'calc-15': 'Sowing Date Calculator',
    'calc-2': 'Planting Density Calculator (Spacing × Row)',
    'calc-36': 'Crop Water Requirement (ET) Calculator',
    'calc-37': 'Daily Light Integral (DLI) Calculator',
    'calc-38': "Irrigation Uniformity (Christiansen's Coefficient)",
    'calc-6': 'Livestock Stocking Capacity Estimator',
    'calc-7': 'Fertigation (Drip) Ratio Adjuster',
    'calc-8': 'Soil pH Adjustment Calculator',
    'calc-ventilation-2': 'Greenhouse Ventilation Volume (Air Changes) Calculator',
    'calculator-calc-1': 'Sowing Date Calculator (Frost-Free Period)',
    'calculator-calc-concentration': 'Pesticide Dilution Concentration Calculator',
    'calculator-calc-density': 'Planting Density Calculator (By Spacing)',
    'calculator-calc-ratio': 'N-P-K Fertilizer Ratio Calculator',
    'calculator-calc-ratio-1': 'Feed Mix Ratio Calculator (by Nutrient Content)',
    'calculator-calc-soil': 'Soil pH Adjustment Calculator (Sulfur or Lime)',
    'canopy-coverage': 'Canopy Coverage Estimator',
    'continuous-cropping-index': 'Continuous Cropping Obstacle Index Calculator',
    'convert-content-1': 'Agricultural Dry Matter & Moisture Conversion',
    'countdown-4': 'Egg Incubation Countdown (21 Days)',
    'countdown-cycle': 'Harvest Countdown (by Crop Growth Cycle)',
    'crop-rotation': 'Crop Rotation Planner',
    'crop-water-requirement': 'Crop Water Requirement Calculator',
    'crop-yield': 'Crop Yield Estimator',
    'cycle-honey': 'Honey Harvest Cycle Planner',
    'detector-13': 'Varroa Mite Infestation Detector',
    'detector-nutrition': 'Bee Pollen (Fermented) Nutrient Analysis',
    'dli-calculator': 'DLI Calculator',
    'dry-matter-conversion': 'Dry Matter Conversion Calculator',
    'estimate-3': 'Irrigation Water Requirement Estimator (ET-based)',
    'estimate-analysis': 'Canopy Coverage Estimator (Photo Analysis)',
    'estimate-area-density': 'Livestock Stocking Capacity Estimator (Area × Density)',
    'estimate-area-yield': 'Forage Yield Estimator (Yield × Area)',
    'estimate-content-soil': 'Soil Organic Matter Estimator (Loss-on-Ignition)',
    'estimate-fuel-engine-oil': 'Farm Machinery Fuel Consumption Estimator (per Unit Area)',
    'estimate-soil': 'Continuous Cropping Obstacle Index Estimator (Pathogen Build-up)',
    'estimate-yield-rate': 'Fertilizer Use Efficiency Estimator (N-P-K Uptake)',
    'fertigation-ratio': 'Fertigation Ratio Calculator',
    'fertilizer-calculator': 'Fertilizer Ratio Calculator',
    'fertilizer-efficiency': 'Fertilizer Efficiency Estimator',
    'gdd-calculator': 'GDD Calculator',
    'greenhouse-rolling-time': 'Greenhouse Film-Rolling Time Advisor',
    'greenhouse-ventilation': 'Greenhouse Ventilation Calculator',
    'harvest-date-predictor': 'Harvest Date Predictor',
    'harvest-loss-rate': 'Harvest Loss Rate Calculator',
    'harvest-planner': 'Harvest Planner',
    'irrigation-calculator': 'Irrigation Water Calculator',
    'irrigation-uniformity': 'Irrigation Uniformity Calculator',
    'machinery-efficiency': 'Machinery Efficiency Comparison',
    'mulch-coverage': 'Mulch Coverage Calculator',
    'nongjijuzuoyexiaolv-mu-xiaoshi-duibi': 'Farm Machinery Efficiency (Mu/Hour) Comparison',
    'pesticide-dose': 'Pesticide Dilution Calculator',
    'pesticide-interval': 'Pesticide Pre-Harvest Interval Countdown',
    'ratio-10': 'Fertigation Drip Ratio (EC/pH) Adjuster',
    'seed-germination-rate': 'Seed Germination Rate & Vigour Index Calculator',
    'soil-organic-matter': 'Soil Organic Matter Estimator',
    'storage-pest-alert': 'Stored-Grain Pest Temperature Alert',
    'straw-return': 'Straw Return Rate Optimizer',
    'temp-2': 'Stored-Grain Pest Outbreak Temperature Alert',
    'temp-time-2': 'Greenhouse Film-Rolling Time Advisor (Temp/Wind)',
}

INTRO = {
    'agri-calculator': 'A multi-purpose agriculture calculator covering fertilizer ratio, planting density, pesticide dilution, irrigation water, incubation countdown and machinery fuel use.',
    'assessor-1': 'Evaluate harvest loss for machine or manual harvesting from before-and-after crop weights, and check it against loss-rate standards to support harvester scheduling and loss reduction.',
    'calc-12': 'Estimate gross irrigation water use from irrigated area, planned irrigation depth and the irrigation efficiency coefficient, for drip, sprinkler and flood systems.',
    'calc-13': 'Estimate hourly and total diesel use from engine power, load factor and specific fuel consumption, with optional fuel price, for farm machinery cost accounting.',
    'calc-15': 'Work back from a target harvest date and crop growth period to the recommended sowing date, helping growers hit the best sowing window.',
    'calc-2': 'Given plant spacing, row spacing and area, calculate theoretical planting density and total plant count to plan sowing rates and rational close planting.',
    'calc-36': 'Compute crop water requirement from reference evapotranspiration ET₀, crop coefficient and growth stage to guide irrigation quotas and water-saving design.',
    'calc-37': 'Integrate light intensity and duration into daily light integral (DLI) to assess whether greenhouse crops receive enough light, for supplementary lighting and photoperiod control.',
    'calc-38': "From catch-can water depths at each measuring point, compute Christiansen's uniformity coefficient to assess sprinkler and drip system evenness for acceptance testing.",
    'calc-6': 'From house area, stocking density and rearing cycle, estimate carrying capacity and annual batches to support capacity planning, feed purchasing and manure handling.',
    'calc-7': 'Calculate the stock-solution ratio and injection volume for fertigation drip systems from growth stage, target nutrient concentration and fertiliser content.',
    'calc-8': 'From current and target soil pH, compute the lime or sulfur needed to amend acidic or alkaline soil and improve planting suitability.',
    'calc-ventilation-2': 'From greenhouse dimensions and target air changes per hour, estimate the required ventilation rate and fan configuration to keep temperature and humidity in range.',
    'calculator-calc-1': 'Work back from the local frost-free period and crop growth period to safe sowing and harvest dates, reducing frost risk.',
    'calculator-calc-concentration': 'From active-ingredient concentration and target dilution ratio, calculate the pesticide and water mix for precise spraying and safe intervals.',
    'calculator-calc-density': 'Enter plant and row spacing (or band width) to get theoretical planting density and total plants per unit area for close-planting schemes and yield potential.',
    'calculator-calc-ratio': 'Enter target N-P-K nutrient requirements and application area, choose common straight fertilisers, and get each fertiliser amount plus a cost estimate.',
    'calculator-calc-ratio-1': 'Blend two feed ingredients to a target nutrient level using the cross (Pearson square) method, supporting livestock ration design.',
    'calculator-calc-soil': 'Enter current and target soil pH, soil texture and area to estimate the lime (to raise pH) or sulfur (to lower pH) needed.',
    'canopy-coverage': 'Estimate canopy coverage from row spacing, plant spacing, canopy diameter and overlap, or by grid-counting green pixels in a photo, and read intercepted light to judge canopy closure.',
    'continuous-cropping-index': 'Score the risk of continuous-cropping obstacles from cropping years, crop sensitivity, soil pathogen load, organic matter and pH, and get a graded risk level to guide rotation and soil improvement.',
    'convert-content-1': 'Convert between moisture content and dry-matter content, or derive dry-matter weight from initial weight and moisture, for grain storage, purchase pricing and raw-material accounting.',
    'countdown-4': 'Set the incubation date to follow the 21-day chick embryo development day by day, with current stage, temperature and humidity and candling reminders.',
    'countdown-cycle': 'Choose a crop and planting date to predict the harvest date and show the current growth stage, with support for multiple batches.',
    'crop-rotation': 'Based on the legume → cereal → leafy → root rotation principle, pick area and starting season to generate a four-year rotation plan with the crop and reason for each season.',
    'crop-water-requirement': 'Enter crop coefficient Kc and reference evapotranspiration ET₀ to compute crop evapotranspiration ETc = Kc × ET₀ and convert it into daily irrigation water use by area.',
    'crop-yield': 'Estimate yield from ears per unit area, grains per ear and thousand-grain weight, with multiple crops and historical yield references.',
    'cycle-honey': 'Plan the honey-extraction cycle for each hive from its flow period and start date, and generate a harvest schedule to keep apiary work organised.',
    'detector-13': 'Detect varroa mite infestation rate from the sample worker-bee count and mites found, and assess the colony parasite load for treatment decisions.',
    'detector-nutrition': 'Assess the nutritional quality and fermentation degree of (fermented) bee pollen from protein, fat, reducing sugar, moisture, ash and lactic acid content.',
    'dli-calculator': 'Enter PPFD and daily lighting hours to compute daily light integral (DLI, mol/m²/d) and compare it with crop requirements to decide supplementary lighting strategy.',
    'dry-matter-conversion': 'Convert between fresh weight, dry weight and moisture content, with standard-moisture normalisation for grain purchase and forage measurement.',
    'estimate-3': 'Estimate crop water requirement and irrigation amount over a period from crop coefficient (Kc) and reference evapotranspiration (ET₀).',
    'estimate-analysis': 'Estimate canopy coverage from the green-pixel share of a canopy photo to assess crop vigour and canopy closure, for population monitoring and remote-sensing validation.',
    'estimate-area-density': 'Enter stocking area, density and average body weight to quickly estimate total stock, total biomass and yield per unit area.',
    'estimate-area-yield': 'Enter fresh forage yield per unit area, area and dry-matter rate to estimate total fresh and dry forage and the number of hay bales.',
    'estimate-content-soil': 'Enter crucible empty weight and pre- and post-ignition dry soil weight to estimate soil organic matter and organic carbon by loss-on-ignition, for rapid lab fertility assessment.',
    'estimate-fuel-engine-oil': 'Enter operation area and total fuel use to compute fuel consumption per unit area and fuel cost, with optional hours and fuel price.',
    'estimate-soil': 'From continuous-cropping years and the annual pathogen growth rate, estimate soil pathogen accumulation and the continuous-cropping obstacle risk level.',    'estimate-yield-rate': 'From fertiliser applied and nutrients removed by the harvest, compute apparent N, P and K use efficiency by the difference method to quantify uptake efficiency and losses.',
    'fertigation-ratio': 'From a target EC value, calculate the fertiliser stock-solution ratio, injection rate and nutrient concentration for precise drip fertigation control.',
    'fertilizer-calculator': 'Support N-P-K compound blending, soil-test-based recommendations and base/top-dressing schemes for scientific and reduced fertiliser use.',
    'fertilizer-efficiency': 'Estimate current-season N, P and K use efficiency by the difference method to assess fertiliser plans and guide reduction for higher efficiency.',
    'gdd-calculator': 'Accumulate growing degree days (GDD) to predict crop development stages and phenology, supporting field-timing management and maturity-group selection.',
    'greenhouse-rolling-time': 'Recommend when to roll or unroll greenhouse film based on temperature, wind speed and humidity, supporting greenhouse climate control and crop protection.',
    'greenhouse-ventilation': 'Calculate the required ventilation rate, air changes per hour and vent area to keep crop conditions suitable and support ventilation system sizing.',
    'harvest-date-predictor': 'Predict the best harvest window from grain moisture and maturity to cut shattering and mould losses.',
    'harvest-loss-rate': 'Assess harvest loss rate for machine or manual harvesting, break down loss sources and give optimisation advice to improve grain recovery.',
    'harvest-planner': 'Plan harvest windows, labour needs, machine efficiency and progress for large-scale harvesting with people-and-machine scheduling.',
    'irrigation-calculator': 'Support different irrigation methods, crop water coefficients and soil types, and estimate water charges to help with water-saving irrigation plans.',
    'irrigation-uniformity': "From flow or water-depth readings at each point, compute Christiansen's uniformity coefficient (CU) and distribution uniformity (DU) to spot clogging or pressure imbalance.",
    'machinery-efficiency': 'Calculate and compare area-per-hour efficiency, fuel use and economics across several machines to support machinery selection and job scheduling.',
    'mulch-coverage': 'Work out plastic-film quantity, covered area and coverage rate to plan purchase and laying and reduce waste.',
    'nongjijuzuoyexiaolv-mu-xiaoshi-duibi': 'Enter working width, speed, hours and actual area to compare theoretical and actual machinery efficiency and assess machine utilisation.',
    'pesticide-dose': 'Professional pesticide dilution and ratio calculation with spraying methods, a common-pesticide reference table and pre-harvest-interval lookup.',
    'pesticide-interval': 'Choose a pesticide and enter the application date to count down to the safe harvest date (PHI values for reference only).',
    'ratio-10': 'From target EC, source-water EC and stock-solution EC, calculate the dilution ratio and injection-pump ratio for a drip fertigation system.',
    'seed-germination-rate': 'Enter the number of seeds tested and daily germination counts to compute germination percentage, germination energy, germination index (GI) and vigour index (VI).',
    'soil-organic-matter': 'Estimate organic matter and organic carbon by the loss-on-ignition method to support soil-fertility assessment and fertilisation decisions.',
    'storage-pest-alert': 'Predict pest outbreak risk from bin temperature, humidity and grain type and give control advice to protect stored grain.',
    'straw-return': 'Optimise the amount of straw returned to the field and the supplementary nitrogen needed, based on carbon-to-nitrogen balance, to avoid nitrogen deficiency after return.',
    'temp-2': 'Enter grain temperature, bin humidity and grain type to judge the risk level of a stored-grain pest outbreak and give handling advice.',
    'temp-time-2': 'Enter inside and outside temperatures, wind speed and film ventilation area to estimate natural-ventilation cooling capacity and advise on vent opening height and timing.',
}

DEFAULT_NOTE = [
    '本工具纯前端运行，数据不会上传到服务器',
    '建议在主流浏览器（Chrome/Safari/Firefox/Edge）中使用',
    '计算结果仅供参考，请以实际应用场景为准',
]


def load(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


_CANDIDATES = (
    dict(indent=0, separators=(',', ':')),
    dict(indent=1, separators=(',', ':')),
    dict(indent=1),
    dict(indent=2, separators=(',', ':')),
    dict(indent=2),
    dict(indent=None, separators=(',', ':')),
    dict(indent=None),
)


def dump_like(path, data, orig_raw):
    """按文件原有 JSON 格式回写：逐一尝试候选格式，取能无损还原原串的那个。"""
    body_raw = orig_raw.rstrip('\n')
    trailing = '\n' if orig_raw.endswith('\n') else ''
    try:
        orig = json.loads(orig_raw)
    except Exception:
        orig = None
    if orig is not None:
        for c in _CANDIDATES:
            try:
                if json.dumps(orig, ensure_ascii=False, **c) == body_raw:
                    return json.dumps(data, ensure_ascii=False, **c) + trailing
            except Exception:
                continue
    return json.dumps(data, ensure_ascii=False, indent=2) + trailing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--apply', action='store_true')
    a = ap.parse_args()
    if not a.dry_run and not a.apply:
        ap.error('需指定 --dry-run 或 --apply')

    slugs = sorted(
        os.path.basename(f)[:-5]
        for f in glob.glob(os.path.join(TOOLS, '*.html'))
        if os.path.basename(f) != 'index.html'
    )
    missing_name = [s for s in slugs if s not in NAME]
    missing_intro = [s for s in slugs if s not in INTRO]
    if missing_name or missing_intro:
        print('!! NAME/INTRO 缺条目:', missing_name, missing_intro)
        return 1

    ov_raw = open(OV, encoding='utf-8').read()
    body_raw = open(BODY, encoding='utf-8').read()
    gis_raw = open(GIS, encoding='utf-8').read()
    ov = json.loads(ov_raw)
    body = json.loads(body_raw)
    gis = json.loads(gis_raw)

    chg_en = chg_ed = chg_body = added_body = added_gis = chg_zh = 0

    for slug in slugs:
        name = NAME[slug]
        intro = INTRO[slug]
        k = 'agriculture/' + slug

        e = ov.get(k)
        if not isinstance(e, dict):
            e = {'ind': 'agriculture'}
        if e.get('en') != name:
            chg_en += 1
        if e.get('ed') != intro:
            chg_ed += 1
        e['en'] = name
        e['ed'] = intro
        e.setdefault('ind', 'agriculture')
        ov[k] = e

        b = body.get(slug)
        if not isinstance(b, dict):
            b = {}
            added_body += 1
            print('  + agriculture-body.json 新增条目:', slug)
        if b.get('title') != name or b.get('h1') != name or b.get('intro') != intro:
            chg_body += 1
        b['title'] = name
        b['h1'] = name
        b['intro'] = intro
        en = b.get('en')
        if not isinstance(en, dict):
            en = {}
        en['title'] = name
        en['h1'] = name
        en['intro'] = intro
        b['en'] = en
        body[slug] = b

        g = gis.get(slug)
        if not isinstance(g, dict):
            g = {}
            added_gis += 1
            print('  + agriculture.json 新增条目:', slug)
        z = g.get('zh-CN')
        if not isinstance(z, dict):
            z = {}
        if not (z.get('title') or '').strip():
            zt = ZH_TITLE.get(slug)
            if zt:
                z['title'] = zt
                z['h1'] = zt
                chg_zh += 1
        if not (z.get('intro') or '').strip():
            zi = ZH_INTRO.get(slug)
            if zi:
                z['intro'] = zi
                chg_zh += 1
        g['zh-CN'] = z
        eu = g.get('en-US')
        if not isinstance(eu, dict):
            eu = {}
        eu['title'] = name
        eu['h1'] = name
        eu['intro'] = intro
        g['en-US'] = eu
        if 'note' not in g:
            g['note'] = list(DEFAULT_NOTE)
        gis[slug] = g

    # 孤儿/跨行业残留键清理：本行业数据源中不属于 agriculture 工具页的键一律删除。
    agri_slugs = set(slugs)
    orph_body = [k for k in list(body.keys()) if k not in agri_slugs]
    for k in orph_body:
        del body[k]
    orph_ov = [k for k in list(ov.keys())
               if k.startswith('agriculture/') and k.split('/', 1)[1] not in agri_slugs]
    for k in orph_ov:
        del ov[k]
    orph_gis = [k for k in list(gis.keys()) if k not in agri_slugs]
    for k in orph_gis:
        del gis[k]

    print('\n--- 汇总 ---')
    print('agriculture 工具页:', len(slugs))
    print('_en_override  en 更新:', chg_en, ' ed 更新:', chg_ed)
    print('agriculture-body 更新:', chg_body, ' 新增:', added_body)
    print('agriculture.json 更新 en-US:', len(slugs), ' 新增条目:', added_gis, ' 中文 title/intro 补齐:', chg_zh)
    print('孤儿键删除  body:', len(orph_body), ' _en_override:', len(orph_ov), ' agriculture.json:', len(orph_gis))
    if orph_body:
        print('   body:', orph_body)
    if orph_ov:
        print('   ov  :', orph_ov)
    if orph_gis:
        print('   gis :', orph_gis)

    if a.dry_run:
        print('\n[dry-run] 未写盘')
        return 0

    open(OV, 'w', encoding='utf-8').write(dump_like(OV, ov, ov_raw))
    open(BODY, 'w', encoding='utf-8').write(dump_like(BODY, body, body_raw))
    open(GIS, 'w', encoding='utf-8').write(dump_like(GIS, gis, gis_raw))
    print('\n已写盘:', OV, BODY, GIS)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

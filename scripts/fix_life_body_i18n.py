#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""life (72) 分类英文态数据源根治：同步三端 + 补中文态缺口。

三处数据源（与 science/sports/fun/ai/biz 同坑，§6「英文态数据源三处」）：
  ① i18n/tools/life-body.json   -> build `_prerender_tool_body` 预渲染 h1 + 首个 <p>
  ② i18n/tools/life.json en-US  -> industry JSON 的 ed 最高优先级源
  ③ i18n/tools/_en_override.json -> 运行时 en（h2/h1）与 ed

本轮缺口：16 个工具（analysis-23 / analysis-74 / analysis-80 / analysis-cost-9 /
analysis-cost-10 / assessor-target / cycle-4 / cycle-pruning-lawn / daily-calorie-needs /
drinking-water-plan / generator-price / parking-fee / recommender-8 / reminder-cycle /
report-profit / stats-13）在 life.json / life-body.json / _en_override 三端**全缺**，
导致中文名、简介、英文态全部缺失，由 ZH_TITLE / ZH_INTRO 一并补齐。

用法：
  python3 scripts/fix_life_body_i18n.py --dry-run
  python3 scripts/fix_life_body_i18n.py --apply
"""
import argparse
import glob
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools', 'life')
OV = os.path.join(ROOT, 'i18n', 'tools', '_en_override.json')
BODY = os.path.join(ROOT, 'i18n', 'tools', 'life-body.json')
GIS = os.path.join(ROOT, 'i18n', 'tools', 'life.json')

# 16 个三端全缺的工具：补中文名与简介（依据页面 <h1> 与实际功能）
ZH_TITLE = {
    'analysis-23': '景观（视线/朝向）分析',
    'analysis-74': '竞争（分析/应对/差异化）',
    'analysis-80': '损耗（控制/分析/改善）体系',
    'analysis-cost-9': '成本（控制/优化/分析）体系',
    'analysis-cost-10': '成本（控制/分析/优化）体系',
    'assessor-target': '选址（评估/竞争/目标）模型',
    'cycle-4': '清洁用品消耗量与补货周期',
    'cycle-pruning-lawn': '草坪（修剪/养护）周期',
    'daily-calorie-needs': '卡路里计算器',
    'drinking-water-plan': '喝水提醒计划计算器',
    'generator-price': '合同（服务/价格/条款）生成',
    'parking-fee': '停车费计算器',
    'recommender-8': '保险（责任/意外/雇主）推荐',
    'reminder-cycle': '家电深度清洁周期提醒',
    'report-profit': '财务（利润/现金流/报表）核算',
    'stats-13': '预售（发布/接龙/统计）工具',
}

ZH_INTRO = {
    'analysis-23': '输入视线、朝向、间距等景观相关数据（逗号或换行分隔），输出均值、极差与对比结果，辅助住宅与项目的景观视线评估。',
    'analysis-74': '输入竞品价格、份额、增速等数据（逗号或换行分隔），统计均值与差距，辅助竞争分析与差异化策略制定。',
    'analysis-80': '输入损耗数量与基准数据（逗号或换行分隔），统计损耗率、均值与波动，辅助损耗控制与改善分析。',
    'analysis-cost-9': '输入成本明细（逗号或换行分隔），输出合计、均值与极差，辅助识别可优化的成本项。',
    'analysis-cost-10': '输入各项成本数据（逗号或换行分隔），统计占比、均值与离散度，辅助成本控制与结构优化。',
    'assessor-target': '按日均人流量、竞争店数、常住人口、租金、面积与可见性评分综合测算，输出加权得分与选址建议，辅助开店选址与商圈评估。',
    'cycle-4': '登记清洁用品的单位、库存、消耗速率与补货阈值，自动推算补货周期与建议下单量，辅助家庭或办公室耗材管理。',
    'cycle-pruning-lawn': '按草坪类型与起始日期排定修剪、施肥、浇水等养护周期，生成养护日历，辅助庭院草坪的季节性维护。',
    'daily-calorie-needs': '输入性别、年龄、身高、体重与活动水平，按基础代谢与活动系数估算每日所需热量，辅助控重与饮食规划。',
    'drinking-water-plan': '输入体重、运动强度与当日气温，结合特殊情况估算每日建议饮水量并生成喝水时间表，辅助日常补水管理。',
    'generator-price': '按设定数量生成合同服务条款与报价文本样例，辅助合同初稿撰写与条款模板整理，纯前端运行不上传数据。',
    'parking-fee': '输入停放时长、每小时费率、免费时长与每日封顶，自动计算应收停车费，辅助停车场收费核对与预估。',
    'recommender-8': '按责任、意外、雇主等保险类别生成投保建议文本样例，辅助保险方案梳理与销售沟通，内容仅供参考。',
    'reminder-cycle': '按家电类型与上次清洁日期排定深度清洁提醒周期，生成待办清单，辅助家庭清洁计划管理。',
    'report-profit': '输入利润与现金流数据（逗号或换行分隔），汇总合计、均值与波动并输出报表要点，辅助经营复盘与财务分析。',
    'stats-13': '汇总预售、接龙或报名数据，统计人数、占比与分档结果，辅助活动预售与团购统计。',
}

# NAME = 英文名（h1 / 导航 / 英文态标题），INTRO = 真实英文描述（intro / ed）。
NAME = {
    'age-calculator': 'Age Calculator',
    'age-in-days': 'Age in Days Calculator',
    'analysis-23': 'Landscape & Sightline Analysis',
    'analysis-74': 'Competitive Analysis & Differentiation',
    'analysis-80': 'Loss Control & Analysis System',
    'analysis-cost-9': 'Cost Optimization & Analysis',
    'analysis-cost-10': 'Cost Control & Optimization Analysis',
    'angle-converter': 'Angle Converter',
    'area-converter': 'Area Converter',
    'assessor-target': 'Site Selection & Target Model',
    'base-convert': 'Base / Radix Converter',
    'bill-splitter': 'Bill Splitter',
    'birthday-paradox': 'Birthday Paradox Calculator',
    'bra-size-converter': 'Bra Size Converter',
    'chinese-number': 'Chinese Numeral Converter',
    'clothing-size-converter': 'Clothing Size Converter',
    'color-name-finder': 'Color Name Finder',
    'concentration-converter': 'Concentration Converter',
    'countdown': 'Countdown Timer',
    'countdown-1': 'Count-Up & Count-Down Timer',
    'countdown-2': 'Anniversary Countdown (Multiple)',
    'countdown-timer': 'Multi-Function Countdown Timer',
    'csv-json': 'CSV / JSON Converter',
    'csv-to-markdown': 'CSV to Markdown Table',
    'cycle-4': 'Consumable Usage & Reorder Cycle',
    'cycle-pruning-lawn': 'Lawn Care Cycle Planner',
    'daily-calorie-needs': 'Daily Calorie Needs Calculator',
    'data-rate-converter': 'Data Rate Converter',
    'data-unit-converter': 'Data Storage Unit Converter',
    'date-add-subtract': 'Date Add & Subtract',
    'date-diff': 'Date Difference Calculator',
    'date-difference-calculator': 'Date Difference Calculator (Y/M/W/D)',
    'density-converter': 'Density Converter',
    'detector-checker-strength': 'Password Strength Checker',
    'drinking-water-plan': 'Daily Water Intake Planner',
    'energy-converter': 'Energy Converter',
    'event-countdown': 'Holiday & Event Countdown',
    'flow-rate-converter': 'Flow Rate Converter',
    'frequency-converter': 'Frequency Converter',
    'fuel-converter': 'Fuel Consumption Converter',
    'generator-price': 'Service Contract & Pricing Generator',
    'generator-random-1': 'Random Number Generator',
    'generator-strength': 'Password Generator with Strength Meter',
    'holiday-calendar': 'Holiday Calendar',
    'leap-year-checker': 'Leap Year Checker',
    'length-converter': 'Length Converter',
    'magnet-converter': 'Magnetic Field Strength Converter',
    'music-practice-timer': 'Music Practice Timer',
    'number-to-chinese': 'Number to Chinese Converter',
    'parking-fee': 'Parking Fee Calculator',
    'percentage-calculator': 'Percentage Calculator',
    'power-converter': 'Power Converter',
    'pressure-converter': 'Pressure Converter',
    'radiation-converter': 'Radiation Dose Converter',
    'recommender-8': 'Insurance Recommendation Generator',
    'reminder-cycle': 'Appliance Deep-Clean Reminder',
    'report-profit': 'Profit & Cash-Flow Report Tool',
    'ring-size-converter': 'Ring Size Converter',
    'roman-numeral': 'Roman Numeral Converter',
    'shoe-size-converter': 'Shoe Size Converter',
    'speed-converter': 'Speed Converter',
    'stats-13': 'Pre-Sale Statistics Tool',
    'temperature-converter': 'Temperature Converter',
    'time-converter': 'Time Unit Converter',
    'timestamp': 'Timestamp Converter',
    'unit-converter': 'Unit Converter',
    'volume-converter': 'Volume Converter',
    'weight-converter': 'Weight Converter',
    'workday-calculator': 'Workday Calculator',
    'world-clock': 'World Clock',
    'yaml-json': 'YAML / JSON Converter',
    'zodiac-calculator': 'Zodiac & Chinese Zodiac Calculator',
}

INTRO = {
    'age-calculator': 'Enter a birth date and exact time to calculate your current age down to years, months, days, hours, minutes and seconds, plus zodiac signs and total days lived.',
    'age-in-days': 'Convert a birth date into the total number of days lived and the days remaining to the next birthday or a target date.',
    'analysis-23': 'Paste sightline, orientation or spacing figures (comma or newline separated) to get mean, extremes and comparison values for residential and project landscape assessments.',
    'analysis-74': 'Paste competitor price, share or growth figures to summarise averages and gaps, supporting competitive analysis and differentiation planning.',
    'analysis-80': 'Enter loss quantities and baseline figures to compute loss rate, mean and fluctuation for loss-control and improvement analysis.',
    'analysis-cost-9': 'Paste a cost breakdown to output the total, mean and range and identify the items with the most optimisation potential.',
    'analysis-cost-10': 'Paste cost items to analyse share, mean and dispersion, supporting cost control and structure optimisation.',
    'assessor-target': 'Score a candidate location by foot traffic, nearby competitors, resident population, rent, area and visibility to produce a weighted site score and selection advice.',
    'angle-converter': 'Convert angles between degrees, radians, gradians and turns instantly and accurately.',
    'area-converter': 'Convert area units such as m², km², hectare, ft², acre and more with one input.',
    'base-convert': 'Convert numbers between binary, octal, decimal, hexadecimal and any custom base, with text and ASCII support.',
    'bill-splitter': 'Split a bill among any number of people with tip or service fee, and handle uneven shares and per-person amounts.',
    'birthday-paradox': 'Calculate the probability that at least two people share a birthday in a group of N, with a day-count parameter.',
    'bra-size-converter': 'Convert bra size across US, UK, EU, JP and CN systems using under-bust and bust measurements.',
    'chinese-number': 'Convert between Arabic digits and Chinese numerals, with lowercase, uppercase and traditional uppercase amount styles.',
    'clothing-size-converter': 'Convert clothing sizes across US, UK, EU, CN and JP systems for men, women and children.',
    'color-name-finder': 'Enter a hex or RGB colour value to find the nearest named colour and its closest matches.',
    'concentration-converter': 'Convert concentration units such as mol/L, g/L, ppm, ppb and percent between each other.',
    'countdown': 'Set a target date, time and event name to count down to it in days, hours, minutes and seconds.',
    'countdown-1': 'Run a simple count-up stopwatch or count-down timer by minutes and seconds, with start, pause and reset.',
    'countdown-2': 'Track several anniversaries or birthdays at once with yearly-repeat countdowns and custom icons.',
    'countdown-timer': 'Set an hours, minutes and seconds countdown for workouts, cooking, focus sessions and meetings.',
    'csv-json': 'Convert between CSV and JSON in both directions with options for delimiter, quote character, headers and number parsing.',
    'csv-to-markdown': 'Turn CSV content into a Markdown table with alignment, header and whitespace-trimming options, plus a rendered preview.',
    'cycle-4': 'Register each consumable with unit, stock, consumption rate and reorder threshold to work out the replenishment cycle and suggested order quantity.',
    'cycle-pruning-lawn': 'Plan mowing, fertilising and watering cycles by lawn type and start date, and generate a seasonal care calendar.',
    'daily-calorie-needs': 'Enter sex, age, height, weight and activity level to estimate daily calorie needs from basal metabolism and activity factors.',
    'data-rate-converter': 'Convert data transfer rates such as bps, kbps, Mbps and Gbps between each other.',
    'data-unit-converter': 'Convert data storage units from bit to TB with both binary (1024) and decimal (1000) bases.',
    'date-add-subtract': 'Add or subtract years, months, days, hours, minutes and seconds from a base date and time to get the resulting moment.',
    'date-diff': 'Calculate the gap between two dates in total days or weekdays, with options to exclude weekends and the start or end day.',
    'date-difference-calculator': 'Compute the difference between two dates in years, months, weeks and days, with inclusive-start and weekend options.',
    'density-converter': 'Convert density units such as kg/m³, g/cm³, lb/ft³ and g/L between each other.',
    'detector-checker-strength': 'Check a password against length, character variety, common patterns and repetition to estimate its strength and fix weak points.',
    'drinking-water-plan': 'Estimate your daily recommended water intake from weight, exercise intensity and temperature, and generate a drinking schedule.',
    'energy-converter': 'Convert energy units such as joule, calorie, kilowatt-hour, BTU and electronvolt between each other.',
    'event-countdown': 'Count down to holidays and special events in days, hours and minutes with a clear display.',
    'flow-rate-converter': 'Convert volumetric and mass flow rates such as L/s, m³/h, gal/min and kg/s between each other.',
    'frequency-converter': 'Convert frequency between hertz, kilohertz, megahertz, gigahertz and revolutions per minute.',
    'fuel-converter': 'Convert fuel economy between L/100km, mpg (US), mpg (UK) and km/L.',
    'generator-price': 'Generate sample contract clauses and pricing text in batches by quantity, supporting first-draft contracts and clause-template tidying.',
    'generator-random-1': 'Generate random integers within any minimum and maximum range and quantity you set, entirely in the browser.',
    'generator-strength': 'Generate strong passwords with configurable length, character sets and ambiguity filters, and check the resulting strength.',
    'holiday-calendar': 'View public holidays and observances for a selected region and year in a convenient calendar layout.',
    'leap-year-checker': 'Check whether a given year is a leap year and list all leap years within a queried range.',
    'length-converter': 'Convert length and distance units from nanometre to mile, including metric and imperial systems.',
    'magnet-converter': 'Convert magnetic field strength units such as tesla, gauss, ampere per metre and oersted.',
    'music-practice-timer': 'Time music practice sessions and segments, helping you keep to a practice schedule and log the minutes.',
    'number-to-chinese': 'Convert numbers into Chinese lowercase numerals, uppercase amount form or traditional uppercase, up to long integers.',
    'parking-fee': 'Enter parking duration, hourly rate, free period and daily cap to calculate the parking fee payable.',
    'percentage-calculator': 'Compute the percentage of a value, percentage increase or decrease, and the value from a percentage in one page.',
    'power-converter': 'Convert power units such as watt, kilowatt, horsepower and BTU per hour between each other.',
    'pressure-converter': 'Convert pressure units such as pascal, bar, psi, atmosphere and millimetre of mercury.',
    'radiation-converter': 'Convert radiation dose units such as sievert, rem, gray and rad between each other.',
    'recommender-8': 'Generate sample insurance recommendation text across liability, accident and employer lines to assist plan review and communication; for reference only.',
    'reminder-cycle': 'Set deep-cleaning reminder cycles for household appliances by type and last clean date, and generate a to-do list.',
    'report-profit': 'Paste profit and cash-flow figures to summarise the total, mean and fluctuation and produce report highlights for business review.',
    'ring-size-converter': 'Convert ring sizes across US, UK, EU, JP and CN systems from a diameter or circumference measurement.',
    'roman-numeral': 'Convert between Arabic numbers (1–3999) and Roman numerals in both directions.',
    'shoe-size-converter': 'Convert shoe sizes across US, UK, EU, CN and JP systems for men, women and children.',
    'speed-converter': 'Convert speed units such as metre per second, kilometre per hour, mile per hour and knot.',
    'stats-13': 'Aggregate pre-sale, group-buy or sign-up data into counts, shares and banded results for campaign statistics.',
    'temperature-converter': 'Convert temperature between Celsius, Fahrenheit and Kelvin with a clear interactive control.',
    'time-converter': 'Convert time units such as second, minute, hour, day and week between each other.',
    'timestamp': 'Convert between Unix timestamps and human-readable dates and times, with timezone-aware parsing and formatting.',
    'unit-converter': 'Convert between any two units across length, mass, volume, area, temperature and more in a single page.',
    'volume-converter': 'Convert volume units such as litre, millilitre, cubic metre, gallon and cubic foot.',
    'weight-converter': 'Convert mass and weight units such as kilogram, gram, pound, ounce and tonne.',
    'workday-calculator': 'Count the working days between two dates, excluding weekends and any custom holidays you specify.',
    'world-clock': 'Compare the current time across multiple cities and time zones side by side.',
    'yaml-json': 'Convert between YAML and JSON in both directions with syntax validation and error hints.',
    'zodiac-calculator': 'Enter a birth date to get the Western zodiac sign and the Chinese zodiac animal with related notes.',
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
        k = 'life/' + slug

        e = ov.get(k)
        if not isinstance(e, dict):
            e = {'ind': 'life'}
        if e.get('en') != name:
            chg_en += 1
        if e.get('ed') != intro:
            chg_ed += 1
        e['en'] = name
        e['ed'] = intro
        e.setdefault('ind', 'life')
        ov[k] = e

        b = body.get(slug)
        if not isinstance(b, dict):
            b = {}
            added_body += 1
            print('  + life-body.json 新增条目:', slug)
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
            print('  + life.json 新增条目:', slug)
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

    # 孤儿/跨行业残留键清理：本行业数据源中不属于 life 工具页的键一律删除。
    life_slugs = set(slugs)
    orph_body = [k for k in list(body.keys()) if k not in life_slugs]
    for k in orph_body:
        del body[k]
    orph_ov = [k for k in list(ov.keys())
               if k.startswith('life/') and k.split('/', 1)[1] not in life_slugs]
    for k in orph_ov:
        del ov[k]
    orph_gis = [k for k in list(gis.keys()) if k not in life_slugs]
    for k in orph_gis:
        del gis[k]

    print('\n--- 汇总 ---')
    print('life 工具页:', len(slugs))
    print('_en_override  en 更新:', chg_en, ' ed 更新:', chg_ed)
    print('life-body 更新:', chg_body, ' 新增:', added_body)
    print('life.json 更新 en-US:', len(slugs), ' 新增条目:', added_gis, ' 中文 title/intro 补齐:', chg_zh)
    print('孤儿键删除  body:', len(orph_body), ' _en_override:', len(orph_ov), ' life.json:', len(orph_gis))
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

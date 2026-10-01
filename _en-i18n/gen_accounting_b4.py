#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""accounting 第4批：analysis-46 / asset-turnover / calc-1 / cash-conversion-cycle"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'accounting')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'accounting')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        for i, it in enumerate(items):
            print('   ', i, repr((it.get('zh') or '')[:50]))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    return mp


def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'accounting', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))


# ---------------- analysis-46 (20) ----------------
write('analysis-46', build('analysis-46', [
    "🔮 Financial Analysis, Decision and Forecasting Model",
    "Model financial analysis, decision-making and forecasting: enter historical financial data to obtain trend readouts and scenario estimates.",
    '📖 View the "Financial Analysis, Decision and Forecasting Model Guide"',
    "Fit a linear trend y = a + b·x by least squares (x is the period index); the slope b gives the average change per period.",
    "Next-period forecast = a + b·(n+1); the closer the goodness-of-fit R² is to 1, the clearer the linear trend.",
    "CAGR = (ending value ÷ beginning value)^(1/(n−1)) − 1, used alongside the moving average for cross-checking the trend.",
    'Historical financial data (one value per line, or "period,value", in chronological order)',
    "Trend Forecast",
    "📚 In-Depth Analysis: Financial Trend Fitting and Next-Period Forecasting",
    "Corporate budgeting",
    "Business review and trend assessment",
    "Investment and financing scenario analysis",
    "Least squares: b = (n·Σxy − Σx·Σy) ÷ (n·Σx² − (Σx)²), a = (Σy − b·Σx) ÷ n; next-period forecast = a + b·(n+1); R² = 1 − SSres ÷ SStot.",
    "100, 118, 132, 151, 170 → slope 17.30, intercept 82.30, next-period forecast 186.10; R² 0.9974, last 3-period moving average 151.00, CAGR 14.19%.",
    "What does a low R² mean?",
    "It means the data is volatile or has seasonal or non-linear factors, so linear extrapolation is unreliable; switch to seasonal adjustment or scenario-based estimates.",
    "Can the forecast be used directly?",
    "For reference only. Extrapolation assumes the existing trend continues; real decisions must also weigh budget plans, market conditions and possible policy and seasonal effects.",
    'About "Financial Analysis, Decision and Forecasting Model"',
    "Financial Analysis, Decision and Forecasting Model. A free online tool that runs entirely in the front end, uploads no data and keeps your privacy safe.",
]))

# ---------------- asset-turnover (19) ----------------
write('asset-turnover', build('asset-turnover', [
    "Asset Turnover Ratio Calculator",
    "Compute total asset turnover from revenue and average total assets to gauge how efficiently assets generate sales.",
    "Asset Turnover = Revenue / Total Assets",
    "/ Asset Turnover Calculator",
    "Asset Turnover Calculator",
    '📖 View the "Asset Turnover Ratio Calculator Guide"',
    "Asset Turnover = Revenue / Total Assets",
    "Total assets (10k CNY)",
    "Measures how efficiently assets generate revenue.",
    "📚 In-Depth Analysis: Asset Turnover Ratio Calculator",
    "Measures how efficiently management uses all assets to generate revenue, allowing a horizontal comparison of asset operation against peers.",
    "Assesses whether asset-heavy expansion brings proportional revenue growth, avoiding blind capacity expansion.",
    "Works with the DuPont ROE decomposition to pinpoint whether the efficiency bottleneck comes from profitability or asset turnover.",
    "Computing Annual Total Asset Turnover",
    "A company has annual revenue of 5000 (10k CNY), beginning total assets of 2000 (10k CNY) and ending total assets of 3000 (10k CNY), so average total assets = (2000+3000)/2 = 2500 (10k CNY) and asset turnover = 5000/2500 = 2.0 times per year, meaning every 1 yuan of assets generates 2 yuan of revenue a year.",
    "Should asset turnover use ending or average total assets?",
    "It usually uses average total assets = (beginning + ending) / 2 to smooth seasonal swings; the formula is revenue ÷ average total assets, and the higher the ratio, the better the asset utilisation efficiency.",
    "Is a low turnover ratio always bad?",
    "Not necessarily. Retail has a high turnover, while asset-heavy industries such as utilities and real estate are naturally lower; judge it against industry characteristics and the historical trend.",
]))

# ---------------- calc-1 (20) ----------------
write('calc-1', build('calc-1', [
    "🧾 VAT Calculator",
    "Convert between tax-inclusive and tax-exclusive amounts and compute the VAT payable from the applicable rate.",
    '📖 View the "VAT Calculator Guide"',
    "VAT payable = Output VAT − Input VAT",
    "Tax-exclusive price given",
    "Tax-inclusive price given",
    "Tax-exclusive amount (CNY)",
    "Ex-tax price → tax = ex-tax price × rate; tax-inclusive price = ex-tax price × (1 + rate)",
    "Tax-inclusive price → ex-tax price = tax-inclusive price / (1 + rate); tax = tax-inclusive price − ex-tax price",
    "Common rates: goods sales 13%, transport/construction 9%, modern services 6%, simplified levy 3%",
    "📚 In-Depth Analysis: VAT Calculator",
    "General taxpayers compute VAT payable monthly as current output VAT − current input VAT.",
    "Small-scale taxpayers use simplified taxation of sales × levy rate and do not deduct input VAT.",
    "Tax computation for imports or cases deemed as sales.",
    "Monthly VAT Payable for a General Taxpayer",
    "A trading company has output VAT of 13 (10k CNY), input VAT of 8 (10k CNY) and a prior-period credit carryforward of 1 (10k CNY), so VAT payable = 13−8−1 = 4 (10k CNY); if input exceeds output the difference is a credit carryforward to offset in later periods.",
    "Why can input VAT be deducted?",
    "VAT taxes the value added, so input VAT already paid upstream can be deducted from output VAT on sale, avoiding double taxation of the same value-added stage; input VAT used for tax-exempt or non-taxable items is not deductible.",
    "How does taxation differ between general and small-scale taxpayers?",
    "General taxpayers use the deduction method (output − input) with rates mostly 13%/9%/6%; small-scale taxpayers use simplified taxation of sales × 3% (currently reduced to 1%), cannot deduct input VAT but face simpler administration.",
]))

# ---------------- cash-conversion-cycle (20) ----------------
write('cash-conversion-cycle', build('cash-conversion-cycle', [
    "Cash Conversion Cycle Calculator",
    "Compute the cash conversion cycle as DSO + DIO minus DPO from receivable, inventory and payable days.",
    "Cash Conversion Cycle Calculator",
    "/ Cash Conversion Cycle Calculator",
    '📖 View the "Cash Conversion Cycle Calculator Guide"',
    "Receivable days DSO (days)",
    "Inventory days DIO (days)",
    "Payable days DPO (days)",
    "The shorter the CCC, the higher the capital efficiency.",
    "36.5+91.25−48.67 → 79.08 days.",
    "📚 In-Depth Analysis: Cash Conversion Cycle Calculator",
    "Measures the days from paying cash for purchases to collecting cash from sales; the shorter the cycle, the less working capital is tied up.",
    "Compares supplier terms (DPO) with customer terms (DSO) to optimise credit policy along the supply chain.",
    "Estimate the cash cycle before seasonal stockpiling to time short-term financing.",
    "Computing a Company's Cash Cycle",
    "A company has DSO = 45 days, inventory turnover days DIH = 30 days and DPO = 40 days, so the cash conversion cycle CCC = 45+30−40 = 35 days, meaning cash is tied up in operations for 35 days before returning.",
    "What is the cash cycle formula?",
    "CCC = days sales outstanding (DSO) + days inventory held (DIH) − days payable outstanding (DPO); a larger DPO shortens the cycle, but supplier terms cannot be stretched indefinitely.",
    "What does a negative cash cycle mean?",
    "When DPO exceeds DSO + DIH the cycle turns negative, meaning the company can use supplier funds free of charge to cover operating needs - a sign of strong supply-chain power (as with some retail giants).",
]))

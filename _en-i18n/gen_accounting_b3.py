#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""accounting 第3批：roe-dupont / break-even-units / working-capital / ebit"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'accounting')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'accounting')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EXTRA = {
    'roe-dupont': {'净利率': 'net profit margin'},
    'ebit': {'绩效考核': 'performance appraisal'},
}


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


# ---------------- roe-dupont (23) ----------------
write('roe-dupont', build('roe-dupont', [
    "DuPont ROE Analysis Calculator",
    "Decompose ROE into net profit margin, asset turnover and equity multiplier to identify the drivers of shareholder return.",
    "ROE = Net Profit Margin × Asset Turnover × Equity Multiplier",
    "/ DuPont ROE Analysis Calculator",
    "DuPont ROE Analysis Calculator",
    '📖 View the "DuPont ROE Analysis Guide"',
    "Net profit margin (%)",
    "Asset turnover",
    "Equity multiplier",
    "DuPont decomposition reveals what drives ROE.",
    "📚 In-Depth Analysis: DuPont ROE Analysis",
    "Use DuPont analysis to break ROE into the ",
    ", asset turnover and the equity multiplier to pinpoint the driving factor.",
    "When ROE falls, work out whether profitability, efficiency or leverage is at fault.",
    "Management benchmarks against leading peers and targets improvement at the weakest factor.",
    "Decomposing ROE into Three DuPont Factors",
    "A company has a 15% net profit margin, asset turnover of 1.2 times and an equity multiplier of 2.0, so ROE = 15%×1.2×2.0 = 36%, showing the high return comes from profitability, efficiency and leverage combined.",
    "What does each of the three DuPont factors reflect?",
    "Net profit margin reflects profitability, asset turnover reflects operating efficiency and the equity multiplier reflects financial leverage; ROE is their product, which makes layered attribution easy.",
    "How is the equity multiplier calculated?",
    "Equity multiplier = total assets ÷ net assets = 1 ÷ (1 − ",
    "debt-to-asset ratio",
    "); the higher the leverage, the larger the multiplier, amplifying ROE more - and risk along with it.",
]))

# ---------------- break-even-units (22) ----------------
write('break-even-units', build('break-even-units', [
    "Compute the break-even sales volume from fixed cost, unit price and unit variable cost using fixed cost / (price - variable cost).",
    "Break-Even Point",
    "/ Break-Even Volume",
    "Break-Even Volume",
    '📖 View the "Break-Even Volume Guide"',
    "Break-even volume = FC/(P−VC)",
    "Fixed cost (CNY)",
    "Profit begins once sales pass this point.",
    "Contribution margin = price − unit variable cost.",
    "📚 In-Depth Analysis: Break-Even Point",
    "Before launching a new product, work out how many units must sell to avoid a loss, supporting pricing and capacity decisions.",
    "In price negotiations or promotion appraisals, model how a lower unit price shifts the break-even volume.",
    "When fixed costs rise (a rent increase, say), recompute the break-even point to reset operating targets.",
    "Computing the Break-Even Volume",
    "A product sells for 100 CNY with a unit variable cost of 60 CNY and monthly fixed costs of 40,000 CNY, giving a unit ",
    "contribution margin",
    " of 100−60 = 40 CNY and a break-even volume of 40000/40 = 1000 units; profit only begins above 1000 units a month.",
    "break-even",
    " point calculated?",
    "Break-even volume = fixed cost ÷ (unit price − unit variable cost), where the denominator is the unit contribution margin; break-even sales value = fixed cost ÷ contribution margin ratio.",
    "What is the contribution margin ratio?",
    "The contribution margin ratio = unit contribution margin ÷ unit price, showing the share of each yuan of sales available to cover fixed costs and generate profit.",
]))

# ---------------- working-capital (21) ----------------
write('working-capital', build('working-capital', [
    "Working Capital Calculator",
    "Compute net working capital from current assets and current liabilities for cash flow planning and liquidity management.",
    "WC = Current Assets − Current Liabilities",
    "/ Working Capital Calculator",
    "Working Capital Calculator",
    '📖 View the "Working Capital Calculator Guide"',
    "Working capital = current assets − current liabilities",
    "Current assets (10k CNY)",
    "Current liabilities (10k CNY)",
    "WC>0 usually means sound short-term solvency.",
    "500−300 → 2,000,000 CNY.",
    "📚 In-Depth Analysis: Working Capital Calculator",
    "Assess a company's short-term liquidity buffer and whether it covers day-to-day operations.",
    "Before expanding or taking a large order, check whether working capital is sufficient to avoid a cash squeeze.",
    "Track how working capital swings with seasons and payment terms so short-term financing can be arranged.",
    "Computing Working Capital",
    "A company has current assets of 800 (10k CNY) and current liabilities of 400 (10k CNY), so working capital = 800−400 = 400 (10k CNY) - the net funds freely available for day-to-day operations in the short term.",
    "Is positive working capital always safe?",
    "Positive working capital means current assets cover current liabilities, but if much of it is slow-moving inventory or hard-to-collect receivables, liquidity can still be tight, so look at quick assets as well.",
    "What if working capital is negative?",
    "A negative figure means current liabilities exceed current assets and operations rely on continued financing or faster collection; cash-rich industries such as retail can run negative for a while, but most companies need to improve their payment-term structure.",
]))

# ---------------- ebit (21) ----------------
write('ebit', build('ebit', [
    "EBIT Calculator",
    "Compute earnings before interest and taxes from revenue, operating cost and operating expenses.",
    "EBIT = Revenue − Operating Cost − Operating Expenses",
    "/ EBIT Calculator",
    "EBIT Calculator",
    '📖 View the "EBIT Calculator Guide"',
    "EBIT = revenue − operating cost − expenses",
    "Operating expenses (10k CNY)",
    "Operating profit with interest and tax removed.",
    "1000−600−200 → 2,000,000 CNY.",
    "📚 In-Depth Analysis: EBIT Calculator",
    "When comparing operating profitability across companies, it removes differences in capital structure and tax burden and shows only the earning power of the core business.",
    "For valuation, the EV/EBIT multiple avoids comparability being distorted by differing leverage and tax rates.",
    "For management ",
    ", EBIT is free from financing decisions and tax policy.",
    "Computing EBIT",
    "A company has revenue of 1,000 (10k CNY), operating cost of 600 (10k CNY) and operating expenses of 200 (10k CNY), so EBIT = 1000−600−200 = 200 (10k CNY) - operating profit before interest and tax.",
    "How does EBIT relate to net profit?",
    "EBIT = net profit + interest expense + income tax; it removes the effect of financing choices (interest) and tax arrangements, focusing on operating profitability.",
    "Is EBIT the same as operating profit?",
    "The definitions are close but not identical: operating profit has usually already deducted fair-value changes, asset impairments and the like, whereas EBIT focuses on operating cash-based income and expenses; the statement presentation governs.",
]))

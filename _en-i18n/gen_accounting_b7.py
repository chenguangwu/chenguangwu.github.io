#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""accounting 第7批：ebitda / free-cash-flow / gross-margin / gross-profit"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'accounting')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'accounting')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EXTRA = {
    'gross-margin': {'净利率': 'net profit margin'},
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


# ---------------- ebitda (20) ----------------
write('ebitda', build('ebitda', [
    "EBITDA Calculator",
    "Compute EBITDA by adding depreciation and amortization back to EBIT to assess operating cash generation.",
    "EBITDA = EBIT + Depreciation and Amortisation",
    "/ EBITDA Calculator",
    "EBITDA Calculator",
    '📖 View the "EBITDA Calculator Guide"',
    "EBITDA = EBIT + Depreciation + Amortisation",
    "EBIT (10k CNY)",
    "EBITDA approximates operating cash flow.",
    "200+50 → 2,500,000 CNY.",
    "📚 In-Depth Analysis: EBITDA Calculator",
    "For comparing companies with different capital structures and depreciation policies, EBITDA removes those differences.",
    "In leveraged buyouts (LBO) and valuation, EV/EBITDA measures the purchase price relative to earnings.",
    "Assesses cash generation before interest, tax, depreciation and amortisation.",
    "Computing EBITDA",
    "A company has EBIT of 200 (10k CNY), depreciation of 50 (10k CNY) and amortisation of 30 (10k CNY), so EBITDA = 200+50+30 = 280 (10k CNY), reflecting operating earnings before non-cash costs.",
    "Can EBITDA replace cash flow?",
    "No. It does not deduct capital expenditure, changes in working capital or taxes, so it overstates true free cash; read it together with free cash flow.",
    "Why is the EBITDA multiple so common in capital markets?",
    "It strips out differences in depreciation policy, capital structure and tax rates, making cross-company comparison easier; but asset-heavy industries have large depreciation, so it can be abused to hide true earnings quality.",
]))

# ---------------- free-cash-flow (19) ----------------
write('free-cash-flow', build('free-cash-flow', [
    "Free Cash Flow Calculator",
    "Compute free cash flow as operating cash flow minus capital expenditure for valuation and dividend capacity analysis.",
    "FCF = OCF − Capital Expenditure",
    "/ Free Cash Flow Calculator",
    "Free Cash Flow Calculator",
    '📖 View the "Free Cash Flow Calculator Guide"',
    "Capital expenditure (10k CNY)",
    "FCF can be allocated to debt repayment and dividends.",
    "150−80 → 700,000 CNY.",
    "📚 In-Depth Analysis: Free Cash Flow Calculator",
    "Measures the cash available to distribute to creditors and shareholders after maintaining the asset base.",
    "A core input to DCF valuation: forecast future FCF and discount it to get enterprise value.",
    "Monitor whether the core business truly generates free cash rather than just book profit.",
    "Computing Free Cash Flow",
    "A company has operating cash flow of 500 (10k CNY) and capital expenditure of 200 (10k CNY), so free cash flow = 500−200 = 300 (10k CNY) - the cash freely available after maintaining operations and growth.",
    "Why is FCF more truthful than net profit?",
    "Net profit includes accruals and non-cash depreciation, so a company may be profitable yet short of cash; FCF deducts the capital expenditure needed to maintain assets and reflects the cash truly available for dividends or debt repayment.",
    "What does capital expenditure include?",
    "It is the cash outflow for building fixed assets, intangible assets and other long-term assets - a necessary investment to maintain and expand capacity; capitalised R&D may also be included.",
]))

# ---------------- gross-margin (19) ----------------
write('gross-margin', build('gross-margin', [
    "Gross Margin Calculator",
    "Compute the gross margin from revenue and cost of goods sold to support pricing strategy and profit structure analysis.",
    "/ Gross Margin",
    '📖 View the "Gross Margin Calculator Guide"',
    "Gross Margin = (Revenue − Cost) / Revenue × 100%",
    "Cost of sales (CNY)",
    "Gross margin reflects product profitability.",
    "It varies widely across industries.",
    "📚 In-Depth Analysis: Gross Margin Calculator",
    "Measures direct product profitability and compares gross margin across product lines or channels.",
    "When setting pricing strategy, ensure the gross margin still leaves a net profit after operating costs and taxes.",
    "Monitor the gross margin trend to warn of margin erosion from rising raw-material prices or price wars.",
    "Computing the Gross Margin",
    "A company has revenue of 1000 (10k CNY) and cost of sales of 700 (10k CNY), so gross profit = 1000−700 = 300 (10k CNY) and gross margin = 300/1000 = 30% - for every 1 yuan of revenue, 0.3 yuan remains to cover expenses and form profit.",
    "Gross margin and ",
    " — what is the difference?",
    "Gross margin deducts only direct cost of sales and reflects the product's own profitability; net profit margin further deducts expenses, interest and tax to reach final profit, so it is more comprehensive.",
    "Is a falling gross margin always bad?",
    "Not necessarily. Cutting prices to win market share lowers the gross margin, but if it brings higher volume and economies of scale, long-term net profit may actually improve, so judge it together with the volume-price strategy.",
]))

# ---------------- gross-profit (19) ----------------
write('gross-profit', build('gross-profit', [
    "Gross Profit Calculator",
    "Compute gross profit and gross margin from revenue and cost of goods sold.",
    "Gross Profit = Revenue − Cost of Sales",
    "/ Gross Profit Calculator",
    "Gross Profit Calculator",
    '📖 View the "Gross Profit Calculator Guide"',
    "Gross Profit = Revenue − Cost of Sales",
    "Gross profit is revenue minus direct cost.",
    "1000−600 → 4,000,000 CNY.",
    "📚 In-Depth Analysis: Gross Profit Calculator",
    "Computes the absolute amount of single-period product profit as the base before deducting expenses and taxes.",
    "Compare the gross profit contribution of different business segments to optimise product and resource allocation.",
    "Set a target gross profit and work back to the maximum acceptable purchase/production cost.",
    "Computing Gross Profit",
    "A company has revenue of 1000 (10k CNY) and cost of sales of 700 (10k CNY), so gross profit = 1000−700 = 300 (10k CNY) - the preliminary profit after deducting direct cost.",
    "What is the difference between gross profit and operating profit?",
    "Gross profit = revenue − cost of sales; operating profit additionally deducts taxes and surcharges, selling/administrative/R&D expenses and asset impairments, so it is closer to the final profit from day-to-day operations.",
    "How can gross profit be increased?",
    "Either raise the selling price (branding/differentiation) or reduce cost of sales (supply-chain optimisation, bulk purchasing, process improvement), while guarding against margin erosion from trading price for volume.",
]))

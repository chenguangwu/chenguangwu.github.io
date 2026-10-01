#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""accounting 第2批：debt-service-coverage / calc-2 / split-bill / amortization-intangible"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'accounting')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'accounting')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EXTRA = {
    'amortization-intangible': {'现金流预测': 'cash flow forecast'},
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


# ---------------- debt-service-coverage (26) ----------------
write('debt-service-coverage', build('debt-service-coverage', [
    "Debt Service Coverage Ratio Calculator",
    "Compute DSCR from operating cash flow and annual debt service to assess loan repayment capacity.",
    "DSCR = Operating Cash Flow / Debt Service",
    "/ Debt Service Coverage Ratio Calculator",
    "Debt Service Coverage Ratio Calculator",
    '📖 View the "Debt Service Coverage Ratio Calculator Guide"',
    "DSCR = OCF / debt service",
    "Debt service (10k CNY)",
    "Only DSCR>1 is enough to cover debt.",
    "📚 In-Depth Analysis: Debt Service Coverage Ratio Calculator",
    "A core metric in bank loan approval - DSCR≥1.2~1.5 makes credit easier to obtain.",
    "In project finance or bond issuance, it demonstrates repayment capacity to investors.",
    "For self-monitoring, so a falling DSCR prompts refinancing or spending cuts early.",
    "Computing the Debt Service Coverage Ratio",
    "A company has annual operating cash flow of 6,000,000 CNY and principal plus interest of 4,000,000 CNY for the year, so DSCR = 600/400 = 1.5: operating cash flow is 1.5 times debt service, a reasonable safety margin.",
    "What does a DSCR below 1 mean?",
    "A DSCR<1 means operating cash flow cannot cover current principal and interest, so cash reserves or refinancing are needed; if this persists, default risk follows.",
    "Why use operating cash flow rather than net profit in the numerator?",
    "Operating cash flow is the cash genuinely available to service debt, whereas net profit includes non-cash items such as depreciation and can be manipulated through accruals; cash flow is the more conservative choice.",
    "How to Use the Debt Service Coverage Ratio Calculator",
    "What the Metric Means",
    "Debt service coverage ratio DSCR = net operating cash flow ÷ (interest + principal repayments).",
    "cash flow covers the debt;",
    "a shortfall needs external financing; the common safety line is ≥1.2.",
    "For bank credit and debt-servicing risk assessment; the higher the multiple, the stronger the repayment capacity.",
    "The cash flow basis (pre-tax or EBITDA) affects the result; judge together with the industry and the maturity structure.",
]))

# ---------------- calc-2 (26) ----------------
write('calc-2', build('calc-2', [
    "🧾 Corporate Income Tax Prepayment Calculator",
    "Estimate the quarterly corporate income tax prepayment from taxable profit and the applicable tax rate.",
    '📖 View the "Corporate Income Tax Prepayment Guide"',
    "Prepaid income tax = profit × tax rate",
    "Quarterly operating revenue (CNY)",
    "Quarterly costs and expenses (CNY)",
    "Deductible losses from prior years (CNY)",
    "Corporate income tax rate (%)",
    "25% (general enterprises)",
    "20% (non-residents and others)",
    "15% (high-tech enterprises)",
    "5% (effective rate for small businesses)",
    "Quarterly taxable income = quarterly operating revenue - quarterly costs and expenses - deductible losses (no more than current profit)",
    "Prepaid tax for the quarter = taxable income × applicable tax rate",
    "An effective 5% rate for small businesses is a common current relief; the latest tax law and the tax authority's determination govern.",
    "This tool is a simplified estimate and ignores tax adjustments, reliefs, assessed collection and other complex situations.",
    "📚 In-Depth Analysis: Corporate Income Tax Prepayment",
    "Enterprises prepay income tax quarterly, based on cumulative profit for the year × the applicable rate − amounts already prepaid.",
    "Prepayment is monthly or quarterly, with a final settlement at year end that refunds or collects the difference.",
    "Where reliefs such as the extra deduction for R&D costs apply, taxable income can already be reduced at the prepayment stage.",
    "Quarterly Income Tax Prepayment",
    "A company's cumulative total profit over the first three quarters is 3,000,000 CNY at an applicable rate of 25% with 500,000 CNY already prepaid; by this quarter cumulative profit reaches 4,000,000 CNY, so tax payable = 4,000,000×25%−500,000 = 500,000 CNY, i.e. 500,000 CNY to prepay this quarter.",
    "What is the difference between prepayment and the annual settlement?",
    "Prepayment is estimated from book profit and paid quarterly; the annual settlement adjusts for permanent and temporary differences under the tax rules to determine the year's tax, and the difference against amounts prepaid is refunded or collected.",
    "What reliefs are there for small and micro-profit enterprises?",
    "Qualifying small and micro-profit enterprises may enjoy a much lower effective rate (for example tiered 5%/10% rates, subject to the latest policy), available already at the prepayment stage without waiting for the settlement.",
]))

# ---------------- split-bill (24) ----------------
write('split-bill', build('split-bill', [
    "🧮 Split Bill Calculator",
    "Splitting a bill after a group meal, shared flat or group buy usually means dividing the cost and adding a tip. Enter the total, the number of people and the tip percentage to get each person's share and the total tip, avoiding mistakes from working it out in your head.",
    "/ Split Bill Calculator",
    '📖 View the "Split Bill Calculator Guide"',
    "Per-person share = total ÷ number of people; with a service charge, total = spend × (1 + service rate); for proportional splitting an individual's share = total × their spend ÷ total spend; adjustment = total − Σ amounts actually paid; after rounding to the cent, give the remainder to whoever has the largest decimal part, so that Σ shares equals the total exactly.",
    "Bill total",
    "Tip percentage (%)",
    "Tips are usually calculated on the pre-tax or post-tax bill; this tool multiplies the total (pre-tax basis) by the percentage, which matches most restaurants' practice; some overseas venues use the pre-tax bill, so adjust to local rules.",
    "The number of people must be a positive integer; a fractional count is meaningless, so the tool rounds it.",
    "To split by differing amounts (when some people order more), use item-by-item splitting; this tool only splits evenly.",
    "📋 Examples",
    "Total",
    "Tip",
    "Per person",
    "📚 In-Depth Analysis: Split Bill Calculator",
    "At meals out, on trips and in similar situations, share the total fairly per person or proportionally.",
    "When a tip, tax or service charge applies, spread the extra across everyone too.",
    "When someone gets a discount or eats free, adjust each person's share flexibly.",
    "Splitting a Meal Three Ways",
    "A meal costs 300 CNY with a 30 CNY tip and a 20 CNY discount, so 310 CNY split three ways is about 103.33 CNY each; if one person eats free, the remaining two pay 155 CNY each.",
    "How does proportional splitting differ from splitting per person?",
    "Per-person splitting divides equally and suits shared consumption; proportional splitting uses each person's order amount or an agreed weight, which is fairer but harder to reconcile.",
    "How are discounts and taxes handled?",
    "Work out the total payable first (including tax and taking discounts into account), then split by the chosen method; the tip is normally added proportionally to each share so nobody is overcharged.",
]))

# ---------------- amortization-intangible (24) ----------------
write('amortization-intangible', build('amortization-intangible', [
    "Intangible Asset Straight-Line Amortization Calculator",
    "Compute annual amortization of an intangible asset from cost, residual value and useful life using the straight-line method.",
    "Intangible Asset Amortization",
    "/ Intangible Asset Amortization",
    '📖 View the "Straight-Line Amortization Guide"',
    "Annual amortization = (original cost − residual value) / useful life",
    "Amortization life (years)",
    "Intangible assets with a finite useful life must be amortized.",
    "In essence it is the same as depreciation.",
    "📚 In-Depth Analysis: Straight-Line Amortization",
    "When you hold intangible assets such as patents, trademarks or software copyrights, the straight-line method spreads the carrying cost evenly over the expected useful life, making each period's profit easier to compute and aligning with tax depreciation.",
    "After an acquisition or investment brings in an identifiable intangible asset, the portion of the consideration allocated to it is amortized over time, avoiding a one-off expense that would distort the income statement.",
    "When preparing the annual budget and the ",
    ", show intangible amortization separately as a non-cash cost, distinguishing operating cash inflow from book expense.",
    "Amortizing a 5-Year Software Copyright",
    "A software copyright is carried at 120 (10k CNY) with an expected residual value of 0 and a 5-year life, so annual amortization = (120−0)/5 = 24 (10k CNY) and monthly amortization is 2 (10k CNY); after 2.5 years, accumulated amortization is 60 (10k CNY) and the net book value is 60 (10k CNY).",
    "How does this differ from accelerated amortization?",
    "The straight-line method charges an equal amount each period - simple to compute and smooth for profit; accelerated methods, such as ",
    "sum-of-the-years'-digits",
    ", charge more early and less later, better matching the declining utility of technology assets but depressing early profit.",
    "How is the amortization life determined?",
    "It is the shorter of the contractual right, the legal provision and the expected period of economic benefit; intangible assets with an indefinite useful life, and goodwill, are not amortized but tested for impairment.",
    "Is amortization tax-deductible?",
    "Amortization is deducted as an expense before tax, reducing taxable income; however, the tax authorities recognise only the life and method set by tax law, so a temporary difference against accounting amortization arises and a tax adjustment is needed.",
]))

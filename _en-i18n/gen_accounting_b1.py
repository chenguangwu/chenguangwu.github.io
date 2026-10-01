#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""accounting 第1批：assessor-risk-11 / analysis-cost-5 / report-2"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'accounting')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'accounting')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EXTRA = {
    'analysis-cost-5': {'毛利率': 'gross margin'},
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


# ---------------- assessor-risk-11 (35) ----------------
write('assessor-risk-11', build('assessor-risk-11', [
    "📋 Financial Risk Assessment and Early-Warning Model",
    "Enter corporate financial risk indicators to compute bankruptcy risk with the Z-Score model and generate response strategies.",
    '📖 View the "Financial Risk Assessment and Early-Warning Model Guide"',
    "X₁ = working capital / total assets, X₂ = retained earnings / total assets, X₃ = EBIT / total assets, X₄ = market value of equity / total liabilities, X₅ = sales / total assets. Z≥2.99 is the safe zone, 1.81–2.99 the grey zone, and <1.81 the distress zone.",
    "Current assets / total assets",
    "Retained earnings / total assets",
    "EBIT / total assets",
    "Market value of equity / total liabilities",
    "Sales / total assets",
    "📚 In-Depth Analysis: Financial Risk Assessment and Early-Warning Model",
    "Banks use it in credit review to flag bankruptcy risk, putting borrowers whose Z falls below the threshold on a high-risk list.",
    "Investors screen candidates with the model, filtering out companies with fragile financial structures.",
    "Companies run a self-check on internal control, track the Z trend and deleverage early.",
    "Computing the Altman Z-Score of a manufacturer",
    "A manufacturer has X₁ = working capital / total assets = 0.15, X₂ = retained earnings / total assets = 0.20, X₃ = EBIT / total assets = 0.12, X₄ = market value of equity / total liabilities = 1.0 and X₅ = sales / total assets = 1.2, so Z = 1.2×0.15+1.4×0.20+3.3×0.12+0.6×1.0+1.0×1.2 = 0.18+0.28+0.396+0.6+1.2 = 2.656, which falls in the 1.81–2.99 grey zone and warrants attention.",
    "How are the Z-Score thresholds interpreted?",
    "The classic thresholds for manufacturers: Z≥2.99 is the safe zone, 1.81–2.99 the grey zone and <1.81 the distress zone; non-manufacturers may refer to a revised model, and these thresholds are empirical rather than legal standards.",
    "What are the limitations of the Z-Score?",
    "It is based on historical financial statements, so its discriminating power drops for young, asset-light companies; X₄ (equity market value / liabilities) is unstable when markets swing sharply, so cash flow and the industry cycle should be considered together.",
    "The Z-Score model, proposed by Altman, weights five financial ratios to estimate bankruptcy probability.",
    "Z≥2.99 is the safe zone, 1.81-2.99 the grey zone, and Z<1.81 the distress zone.",
    "The model fits listed manufacturers; private companies need adjusted coefficients.",
    "Compute the Z-Score quarterly and build a risk early-warning trend chart.",
    "A steadily falling Z should trigger the risk early-warning mechanism and contingency plans.",
    'About "Financial Risk Assessment and Early-Warning Model"',
    "A corporate financial risk assessment tool that computes bankruptcy risk with the Altman Z-Score model and outputs a risk grade with response suggestions.",
    "Z-Score five-factor model",
    "Three-tier risk zone classification",
    "Targeted response strategies",
    "Financial early-warning trend monitoring",
    "Corporate financial risk early warning",
    "Investment risk assessment",
    "Credit risk analysis",
    "Corporate operating diagnosis",
    "How to Use the Financial Risk Assessment and Early-Warning Model",
]))

# ---------------- analysis-cost-5 (29) ----------------
write('analysis-cost-5', build('analysis-cost-5', [
    "💰 Cost Accounting and Analysis Method",
    "Classify and analyze product costs, separate fixed and variable costs, and produce descriptive cost statistics.",
    "Costing under the absorption method: direct materials, direct labor and variable manufacturing overhead move with output, while fixed manufacturing overhead is allocated over current output. The companion contribution-margin analysis reclassifies costs into variable and fixed parts: unit contribution margin equals unit price minus unit variable cost, and dividing total fixed cost by it gives the break-even volume. Both views are shown side by side so the book full cost can be compared with the decision-relevant cost. All calculations run locally in your browser.",
    '📖 View the "Cost Accounting and Analysis Method Guide"',
    "Unit full cost = unit variable cost + fixed manufacturing overhead ÷ output; break-even volume = total fixed cost ÷ unit contribution margin",
    "Current output (units)",
    "Direct materials per unit (CNY/unit)",
    "Direct labor per unit (CNY/unit)",
    "Variable manufacturing overhead per unit (CNY/unit)",
    "Total fixed manufacturing overhead (CNY)",
    "Variable selling expense per unit (CNY/unit)",
    "Total fixed selling and administrative expenses (CNY)",
    "Unit selling price (CNY/unit)",
    "Target gross margin (%)",
    "📚 In-Depth Analysis: Cost Accounting and Analysis Method",
    "Before pricing a product, work out the unit full cost (materials, labor and overhead allocation) to see whether costs are covered and to set a sensible margin.",
    "Use cost-volume-profit analysis to find the ",
    "break-even point",
    ", to assess how far sales can fall before turning to a loss.",
    "Use standard-cost variance analysis (price and usage variances) to pinpoint where costs overran.",
    "Working Out the Unit Full Cost",
    "A product has direct materials of 40 CNY per unit, direct labor of 20 CNY, variable manufacturing overhead of 10 CNY, and fixed manufacturing overhead of 15 CNY allocated over output, so the unit full cost = 40+20+10+15 = 85 CNY; if the target ",
    "is 30%, the price should be ≥85/(1−0.3)≈121 CNY.",
    "What are the common cost accounting methods?",
    "By production organization there are process costing, job-order costing and step costing; management accounting also uses variable costing and activity-based costing (ABC) to allocate overhead more precisely.",
    "How are fixed and variable costs distinguished?",
    "Costs that change in direct proportion to output are variable (materials, piece-rate wages); those whose total stays fixed in the short run are fixed (rent, management salaries).",
    'About "Cost Accounting and Analysis Method"',
    "Cost Accounting and Analysis Method. A free online tool that runs entirely in the front end, uploads no data and keeps your privacy safe.",
]))

# ---------------- report-2 (27) ----------------
write('report-2', build('report-2', [
    "🧾 Bookkeeping and Financial Statement Preparation",
    "Support voucher, ledger and financial statement preparation with account balance summaries and trial balance checks.",
    '📖 View the "Bookkeeping and Financial Statement Preparation Guide"',
    "Trial balance: Σ debit balances = Σ credit balances; the debit-credit difference = total debits − total credits, and only a zero difference permits closing.",
    "List each account by the direction of its balance: assets and cost or expense accounts normally carry debit balances, while liabilities, equity and revenue normally carry credit balances.",
    "The tool also shows each account's share of total debits and the largest debit and credit accounts, making the trial balance quick to check.",
    'Account balances (one line per account: "account,debit balance,credit balance", enter 0 on the unused side)',
    "Cash on hand,8000,0\nBank deposits,60000,0\nAccounts receivable,22000,0\nAccounts payable,0,30000\nShort-term borrowings,0,40000\nPaid-in capital,0,20000",
    "Trial Balance",
    "📚 In-Depth Analysis: Account Balance Summary and Trial Balance",
    "Period-end closing trial balance",
    "Reconciliation for agency bookkeeping",
    "Preparing the trial balance",
    "A trial balance requires Σ debit balances = Σ credit balances; the debit-credit difference = total debits − total credits, and only a zero difference allows closing.",
    "Cash on hand 5000, bank deposits 120000, accounts receivable 35000, accounts payable 48000, short-term borrowings 60000, paid-in capital 52000 → total debits 160000.00, total credits 160000.00, difference 0.00, balanced.",
    "What if the trial balance does not balance?",
    "First check for reversed directions, omitted accounts and keying errors in amounts, then verify that opening balances and current-period movements were carried forward completely.",
    "Why must debits and credits always be equal?",
    "Under double-entry bookkeeping every entry has equal debits and credits, so after summarising all accounts the totals must match; a mismatch means an error in the bookkeeping process.",
    'About "Bookkeeping and Financial Statement Preparation"',
    "Bookkeeping and Financial Statement Preparation. A free online tool that runs entirely in the front end, uploads no data and keeps your privacy safe.",
    "How to Use Bookkeeping and Financial Statement Preparation",
    "Small businesses and sole proprietors use the template to complete month-end closing, from accounting vouchers and ledger entries through to issuing statements.",
    "What is the logical relationship between vouchers, ledgers and statements?",
    "Source documents are reviewed first and accounting vouchers prepared; the vouchers then feed the journals and ledgers; after period-end adjustments and closing, financial statements are prepared from ledger balances and movements - each step builds on the last.",
    "Check first whether debits and credits are equal and whether accounts were mixed up, omitted or recorded twice; cross-check balance directions against movements to locate the error before correcting it.",
    "Cash on hand,5000,0",
]))

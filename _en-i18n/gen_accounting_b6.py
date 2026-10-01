#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""accounting 第6批：debt-to-asset / depreciation-declining / depreciation-straight / depreciation-syd"""
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


# ---------------- debt-to-asset (18) ----------------
write('debt-to-asset', build('debt-to-asset', [
    "Debt-to-Asset Ratio Calculator",
    "Compute the debt-to-asset ratio from total liabilities and total assets to gauge leverage and long-term solvency.",
    "Debt-to-Asset Ratio",
    "/ Debt-to-Asset Ratio",
    '📖 View the "Debt-to-Asset Ratio Calculator Guide"',
    "Debt-to-Asset Ratio = Total Liabilities / Total Assets",
    "The higher it is, the greater the financial risk.",
    "Capital structure varies widely across industries.",
    "📚 In-Depth Analysis: Debt-to-Asset Ratio Calculator",
    "Assesses a company's long-term solvency and capital structure risk.",
    "A core measure of financial leverage for creditors, rating agencies and investors.",
    "Monitor how the ratio changes with expansion or debt repayment to warn of over-leverage.",
    "Computing the Debt-to-Asset Ratio",
    "A company has total liabilities of 1500 (10k CNY) and total assets of 5000 (10k CNY), so the debt-to-asset ratio = 1500/5000 = 30%, meaning 30% of assets are funded by creditors - relatively low financial leverage.",
    "How high is a dangerous debt-to-asset ratio?",
    "There is no universal threshold; asset-heavy industries such as utilities can tolerate a higher ratio, while asset-light or cyclical industries should stay lower; a ratio above 70% generally means markedly reduced financial flexibility.",
    "How does the debt-to-asset ratio relate to the debt-to-equity ratio?",
    "Debt-to-equity = liabilities / owners' equity, while debt-to-asset = liabilities / (liabilities + equity); both measure leverage and can be converted into each other.",
]))

# ---------------- depreciation-declining (19) ----------------
write('depreciation-declining', build('depreciation-declining', [
    "Double Declining Balance Depreciation Calculator",
    "Compute accelerated depreciation with the double declining balance method from cost, salvage value and useful life.",
    "Double Declining Balance",
    "/ Double Declining Balance",
    '📖 View the "Double Declining Balance Depreciation Calculator Guide"',
    "Annual Depreciation = Net Book Value × 2 / Useful Life",
    "Annual Depreciation = Beginning Book Value × 2/n (adjusted to salvage value in the final year)",
    "More depreciation early, less later.",
    "The final two years usually switch to the straight-line method down to the salvage value.",
    "📚 In-Depth Analysis: Double Declining Balance Depreciation Calculator",
    "Equipment is more useful and productive early on, so accelerated depreciation better matches cost with revenue.",
    "Where tax law allows accelerated depreciation, use tax planning to defer tax.",
    "For fast-obsoleting assets, higher early depreciation lowers early book profit and the tax base.",
    "First Two Years of Double Declining Balance Depreciation",
    "An asset has a cost of 100 (10k CNY), salvage value of 10 (10k CNY) and useful life of 5 years, so the annual depreciation rate = 2/5 = 40%. Year 1 depreciation = 100×40% = 40 (10k CNY), net book value 60 (10k CNY); Year 2 depreciation = 60×40% = 24 (10k CNY), net book value 36 (10k CNY); the final two years switch to the straight-line method to spread the remaining book value less salvage value.",
    "How are the last two years handled under the double declining balance method?",
    "To stop depreciating at the salvage value, the remaining net book value less salvage value is usually amortised evenly over the last two years of the asset's life (i.e. switching to the straight-line method).",
    "Why is the salvage value not deducted in the early years?",
    "The double declining balance method multiplies a fixed rate by the net book value; deducting salvage value early would lower the depreciation base. The salvage value is naturally reflected through the straight-line method in the last two years, ensuring the ending net book value equals the salvage value.",
]))

# ---------------- depreciation-straight (18) ----------------
write('depreciation-straight', build('depreciation-straight', [
    "Straight-Line Depreciation Calculator",
    "Compute annual depreciation and the depreciation rate with the straight-line method from cost, salvage value and useful life.",
    "Straight-Line Depreciation",
    "/ Straight-Line Depreciation",
    '📖 View the "Straight-Line Depreciation Calculator Guide"',
    "Annual Depreciation = (Cost − Salvage Value) / Useful Life",
    "Straight-line depreciation is the same each year.",
    "No depreciation is charged on the salvage value.",
    "📚 In-Depth Analysis: Straight-Line Depreciation Calculator",
    "For assets such as buildings and furniture whose usefulness is even across periods, the straight-line method spreads the cost evenly.",
    "When a simple, predictable annual depreciation expense is needed to ease budgeting and quoting.",
    "When tax and accounting depreciation match, it reduces tax adjustment work.",
    "Computing Straight-Line Annual Depreciation",
    "An asset has a cost of 50 (10k CNY), expected salvage value of 5 (10k CNY) and useful life of 5 years, so annual depreciation = (50−5)/5 = 9 (10k CNY) and monthly depreciation = 0.75 (10k CNY); after five years the net book value equals the salvage value of 5 (10k CNY).",
    "Why is the straight-line method the most common?",
    "It is simple to compute, keeps expenses even across periods and smooths profit, suits assets with stable usefulness and slow technological change, and aligns easily with external reporting and tax.",
    "What if the expected net salvage value is zero or negative?",
    "Net salvage value is generally the expected disposal proceeds minus disposal costs, usually 0 or more; if expected disposal costs exceed proceeds, practice still treats it as 0 and it may not be set negative.",
]))

# ---------------- depreciation-syd (19) ----------------
write('depreciation-syd', build('depreciation-syd', [
    "Sum-of-Years-Digits Depreciation Calculator",
    "Compute accelerated depreciation with the sum-of-years-digits method using year = (n - k + 1) / SYD x (cost - salvage).",
    "Sum-of-Years-Digits Method",
    "/ Sum-of-Years-Digits Method",
    '📖 View the "Sum-of-Years-Digits Depreciation Calculator Guide"',
    "Annual Depreciation = (Cost − Salvage Value) × Remaining Years / Sum of Years",
    "The depreciation amount decreases year by year.",
    "First-year depreciation is the highest.",
    "📚 In-Depth Analysis: Sum-of-Years-Digits Depreciation Calculator",
    "When you want more depreciation early and less later, matching the asset's declining usefulness.",
    "double declining balance",
    " method is also accelerated depreciation, but with a gentler, more controllable decline.",
    "Where tax law allows, use it to defer tax and smooth the tax burden across periods.",
    "First-Year Depreciation under Sum-of-Years-Digits",
    "An asset has a cost of 100 (10k CNY), salvage value of 10 (10k CNY) and useful life of 5 years, so the sum of years = 5+4+3+2+1 = 15. Year 1 rate = 5/15, depreciation = (100−10)×5/15 = 30 (10k CNY); Year 2 = (100−10)×4/15 = 24 (10k CNY), decreasing each year.",
    "What is the difference between sum-of-years-digits and double declining balance?",
    "The former uses a rate of remaining years / sum of years with a fixed base of (cost − salvage value) and declines linearly; the latter multiplies a rate by the net book value, is faster early on, and does not deduct salvage value in the early years.",
    "Does the sum-of-years-digits base include the salvage value?",
    "Yes. Sum-of-years-digits uses (cost − expected net salvage value) as the depreciation base, spreads it with weights that fall each year, and the ending net book value equals exactly the salvage value.",
]))

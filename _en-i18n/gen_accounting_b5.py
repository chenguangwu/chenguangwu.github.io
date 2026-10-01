#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""accounting 第5批：contribution-margin / current-ratio / days-payable-outstanding / days-sales-outstanding"""
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


# ---------------- contribution-margin (19) ----------------
write('contribution-margin', build('contribution-margin', [
    "Contribution Margin Calculator",
    "Compute the unit contribution margin and contribution margin ratio from unit price and unit variable cost for cost-volume-profit analysis.",
    "Contribution Margin",
    "/ Contribution Margin",
    '📖 View the "Contribution Margin Calculator Guide"',
    "Unit Contribution Margin = Price − Unit Variable Cost",
    "Sales volume (units)",
    "Contribution margin first covers fixed costs.",
    "Anything left over becomes profit.",
    "📚 In-Depth Analysis: Contribution Margin Calculator",
    "Single-product profitability analysis to judge whether a product is worth continuing to produce or keep.",
    "When optimising a multi-product mix, schedule products with a high unit contribution margin first.",
    "Estimate the room for price cuts: within the range where contribution margin stays positive, short-term promotions can clear inventory.",
    "Computing the Unit Contribution Margin",
    "A product sells for 80 CNY with a unit variable cost of 50 CNY, so the unit contribution margin = 80−50 = 30 CNY; with monthly fixed costs of 30,000 CNY, 1000 units must sell before fixed costs are covered and profit begins.",
    "What is the difference between unit contribution margin and gross profit?",
    "Unit contribution margin = price − unit variable cost, used for cost-volume-profit and short-term decisions; gross profit = revenue − cost of sales and includes allocated fixed manufacturing overhead, so it is a broader measure.",
    "Why stop production when the contribution margin is negative?",
    "A negative contribution margin means each unit sold adds a loss equal to its variable cost, so stopping limits the damage; but if it still covers part of the fixed costs, continuing to produce in the short term loses less than stopping.",
]))

# ---------------- current-ratio (19) ----------------
write('current-ratio', build('current-ratio', [
    "Current Ratio Calculator",
    "Compute the current ratio from current assets and current liabilities to assess short-term solvency.",
    "/ Current Ratio",
    '📖 View the "Current Ratio Calculator Guide"',
    "Current Ratio = Current Assets / Current Liabilities",
    "Above 2 is relatively safe, but too high may mean idle assets.",
    "Judge it in the context of the industry.",
    "📚 In-Depth Analysis: Current Ratio Calculator",
    "For creditors assessing short-term solvency, the current ratio is the primary indicator.",
    "Companies monitor their own liquidity to avoid a short-term cash squeeze from expanding too fast.",
    "Compare with peers to judge whether asset allocation is conservative or aggressive.",
    "Computing the Current Ratio",
    "A company has current assets of 800 (10k CNY) and current liabilities of 400 (10k CNY), so the current ratio = 800/400 = 2.0, meaning every 1 yuan of short-term liabilities is covered by 2 yuan of current assets - a fairly strong short-term solvency position.",
    "Is a higher current ratio always better?",
    "Not necessarily. Too high may mean slow-moving inventory or idle cash and low returns on assets; a ratio of 2 or more is usually sound, but it must be read together with the",
    "quick ratio",
    "and industry characteristics.",
    "How does the current ratio differ from the quick ratio?",
    "The quick ratio excludes slow-moving inventory: (current assets − inventory) / current liabilities, which better reflects immediate solvency.",
]))

# ---------------- days-payable-outstanding (20) ----------------
write('days-payable-outstanding', build('days-payable-outstanding', [
    "Days Payable Outstanding Calculator",
    "Compute DPO from accounts payable and annual cost of goods sold to understand and plan the payment cycle.",
    "DPO = Accounts Payable / Cost of Goods Sold × 365",
    "/ Days Payable Outstanding Calculator",
    "Days Payable Outstanding Calculator",
    '📖 View the "Days Payable Outstanding Calculator Guide"',
    "DPO = Accounts Payable / Cost of Goods Sold × 365",
    "Accounts payable (10k CNY)",
    "The longer the DPO, the longer the company holds supplier funds.",
    "80/600×365 → 48.7 days.",
    "📚 In-Depth Analysis: Days Payable Outstanding Calculator",
    "Measures the average days a company holds supplier funds, reflecting its bargaining power and payment policy.",
    "Compare with DSO and DIH to assess whether supplier terms offset the overall cash cycle.",
    "Monitor for an abnormal lengthening of the payment cycle as an early warning of supply-chain or cash flow stress.",
    "Computing Days Payable Outstanding",
    "A company has ending accounts payable of 200 (10k CNY) and annual cost of goods sold of 2400 (10k CNY), so DPO = 200 ÷ (2400/365) = 200 ÷ 6.575 ≈ 30.4 days - on average it pays suppliers every 30 days.",
    "Is a longer DPO always better?",
    "Moderately long lets the company use interest-free funds and improves the cash cycle, but too long damages supplier relationships and may affect supply and discounts, so balance bargaining power against creditworthiness.",
    "How does DPO relate to the cash cycle?",
    "Cash cycle = DSO + DIH − DPO; DPO is the only subtraction, so extending payment days shortens the time the company's own cash is tied up.",
]))

# ---------------- days-sales-outstanding (20) ----------------
write('days-sales-outstanding', build('days-sales-outstanding', [
    "Days Sales Outstanding Calculator",
    "Compute DSO from accounts receivable and annual revenue to evaluate collection efficiency and cash tie-up.",
    "DSO = Accounts Receivable / Revenue × 365",
    "/ Days Sales Outstanding Calculator",
    "Days Sales Outstanding Calculator",
    '📖 View the "Days Sales Outstanding Calculator Guide"',
    "DSO = Accounts Receivable / Revenue × 365",
    "Accounts receivable (10k CNY)",
    "The shorter the DSO, the faster the collection.",
    "100/1000×365 → 36.5 days.",
    "📚 In-Depth Analysis: Days Sales Outstanding Calculator",
    "Assesses the speed of sales collection and monitors bad-debt and cash flow risk.",
    "Serves as a quantitative basis when setting customer credit policy (payment terms, credit limits).",
    "Compare with the industry average to judge your own collection efficiency or customer quality.",
    "Computing Days Sales Outstanding",
    "A company has ending accounts receivable of 500 (10k CNY) and annual revenue of 6000 (10k CNY), so DSO = 500 ÷ (6000/365) = 500 ÷ 16.44 ≈ 30.4 days - sales are collected in about 30 days on average.",
    "Is a lower DSO always better?",
    "Generally, the lower the DSO the faster the collection and the smaller the bad-debt risk, but overly strict credit policy can drive customers away; balance it against industry norms and sales growth targets.",
    "Why use revenue rather than credit sales?",
    "Public financial statements usually report only revenue, so it is used as an approximation; if credit sales are a small share, DSO is understated, and internal analysis should use net credit sales where possible.",
]))

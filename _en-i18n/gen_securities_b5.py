#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""securities 第5批：earnings-yield / fcf-yield / gordon-growth-price / holding-return-stock"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'securities')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'securities')

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
    out = {'slug': slug, 'industry': 'securities', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))


# ---------------- earnings-yield (21) ----------------
write('earnings-yield', build('earnings-yield', [
    "Compute earnings yield from EPS and share price",
    "Enter earnings per share (EPS) and share price (P) to compute the earnings yield.",
    "Earnings Yield = EPS / P",
    "/ Earnings Yield Calculator",
    "Earnings Yield Calculator",
    '📖 View the "Compute earnings yield from EPS and share price User Guide"',
    "Earnings yield = EPS/P × 100%",
    "The reciprocal of the P/E ratio.",
    "📚 Deep Dive: Earnings Yield",
    "E/P is the",
    "P/E ratio",
    "reciprocal, measuring earnings per unit of market price.",
    "Bond yield",
    "comparison (Fed-model equity-bond attractiveness).",
    "Value-stock screening (high E/P is relatively cheap).",
    "Earnings yield = 1/PE = 1/20 = 5%. That is, every 100 yuan of market cap corresponds to 5 yuan of annualized earnings.",
    "E/P = 1/15 ≈ 6.67%. More earnings-attractive than PE=20 (same price earns more).",
    "What do earnings yield and bond yield compare?",
    "Roughly compare a stock's E/P with risk-free/credit-bond yields to judge whether stocks or bonds are relatively cheap. But earnings are volatile and not fixed coupons, so it is only a reference.",
    "When a cyclical stock's PE is distorted, is its E/P also distorted?",
    "Yes. At a cyclical peak earnings are high, E/P is falsely high and PE falsely low; normalize earnings (cyclical average) to correct it.",
]))

# ---------------- fcf-yield (21) ----------------
write('fcf-yield', build('fcf-yield', [
    "Compute free-cash-flow yield from FCF per share and share price",
    "Enter free cash flow per share (FCF) and share price (P) to compute the FCF yield.",
    "FCF Yield = FCF / Share Price",
    "/ FCF Yield Calculator",
    "FCF Yield Calculator",
    '📖 View the "Compute free-cash-flow yield from FCF per share and share price User Guide"',
    "FCF yield = FCF/Share Price × 100%",
    "FCF per share (yuan)",
    "Harder to manipulate than earnings yield.",
    "📚 Deep Dive: Free-Cash-Flow Yield",
    "FCF/market cap, measuring the free-cash-flow return per yuan of market value.",
    "Harder to manipulate than earnings yield (cash-flow perspective).",
    "Value/dividend investment strategy screening.",
    "FCF = 800M, market cap = 10B",
    "FCF yield = 8/100 = 8%. That is, every 100 yuan of market cap corresponds to 8 yuan of free cash flow.",
    "Market cap rises",
    "FCF unchanged at 800M, market cap rises to 12B: FCF yield = 8/120 ≈ 6.67%, attractiveness declines.",
    "Which FCF measure should be used?",
    "Typically operating cash flow minus capital expenditure (FCFF or FCFE); it must match market cap (equity) or EV (whole firm), and the basis must be consistent to be comparable.",
    "Is FCF yield better than PE?",
    "Cash flow is harder to dress up than profit, but FCF is volatile (affected by capex cycles); judge using a multi-year average.",
]))

# ---------------- gordon-growth-price (18) ----------------
write('gordon-growth-price', build('gordon-growth-price', [
    "Compute stock price from expected dividend, required return and growth rate",
    "Enter expected dividend per share D1, required return r and dividend growth rate g to find the fair stock price.",
    "Gordon Growth Model Price Calculator",
    "/ Gordon Growth Model Price Calculator",
    '📖 View the "Compute stock price from expected dividend, required return and growth rate User Guide"',
    "Required return r",
    "4/(0.1-0.04) -> 66.67 yuan.",
    "📚 Deep Dive: Gordon Growth Model Valuation",
    "Intrinsic value estimate for stable-growth stocks (P = D1/(r-g)).",
    "Equivalent to DDM; commonly used in dividend-discount teaching and valuation.",
    "Sensitivity analysis: tiny changes in r and g have an enormous impact on price.",
    "P = 2.1/(0.10-0.05) = 42 yuan. If r rises to 11%: P = 2.1/(0.11-0.05) = 35 yuan; a one-notch spread widens price down 17%.",
    "Low growth",
    "D1=2.1, r=10%, g=3%: P=2.1/(0.07)=30 yuan. Lower growth means lower valuation.",
    "How is it different from DDM?",
    "The Gordon growth model is exactly the single-stage DDM; the formulas are identical, only the name differs.",
    "Can g exceed r?",
    "No; otherwise the denominator is negative/zero and valuation is unbounded. In reality g never exceeds the long-run nominal GDP growth rate.",
]))

# ---------------- holding-return-stock (20) ----------------
write('holding-return-stock', build('holding-return-stock', [
    "Compute holding-period return from buy/sell prices and dividends",
    "Enter the buy price, sell price and dividends received to compute the holding-period return.",
    "Stock Holding-Period Return Calculator",
    "/ Stock Holding-Period Return Calculator",
    '📖 View the "Compute holding-period return from buy/sell prices and dividends User Guide"',
    "Buy price P0 (yuan)",
    "Sell price P1 (yuan)",
    "Dividend D (yuan)",
    "Total return including dividends.",
    "📚 Deep Dive: Stock Holding-Period Return",
    "Computes total return from buy to sell (including capital gain and dividends).",
    "Combine multiple buys and sells into one holding-period return.",
    "Convert to annualized return (given holding days).",
    "Buy 50, sell 55, dividend 2",
    "Holding-period return = (Sell-Buy+Dividend)/Buy = (55-50+2)/50 = 7/50 = 14%.",
    "Buy 50, sell 45, dividend 1: return = (45-50+1)/50 = -4/50 = -8%.",
    "Does it include dividend reinvestment?",
    "This tool counts dividends as cash; if dividends are reinvested, use the adjusted (ex-rights) price to compute total return, which is usually slightly higher.",
    "How to annualize?",
    "Annualized = (1+period return)^(365/holding days) - 1. Holding half a year with 14% return -> annualized ≈ (1.14)^2 - 1 ≈ 29.96%.",
]))

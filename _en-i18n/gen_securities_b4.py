#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""securities 第4批：calc-30 / current-yield / ddm-price / dividend-payout"""
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


# ---------------- calc-30 (39) ----------------
write('calc-30', build('calc-30', [
    "🧮 Maximum Drawdown Calculator",
    "Enter a portfolio net-value series (one value per line) to compute the peak-to-trough maximum drawdown, the drawdown recovery period, the annualized return and the Calmar ratio, and to plot the drawdown curve.",
    '📖 View the "Maximum Drawdown Calculator User Guide"',
    "Portfolio net-value series (one value per line)",
    "Data frequency (annualization factor)",
    "Daily (252)",
    "Weekly (52)",
    "Monthly (12)",
    "Yearly (1)",
    "Risk-free rate (%, for the Calmar excess return)",
    "🎲 Sample data",
    "💡 Maximum drawdown = max(peak − trough) / peak; Calmar ratio = annualized excess return ÷ maximum drawdown, measuring the excess return per unit of risk.",
    "The net-value series needs at least 2 data points, entered line by line in chronological order",
    "The annualized return is computed as CAGR = (final value / initial value)^(annualization factor / number of periods) − 1",
    'For a drawdown that has not recovered to a new high, the recovery period is shown as "not recovered"',
    "A Calmar ratio > 1 is usually considered excellent, and < 0 means a negative excess return",
    "📚 Deep Dive: Compound Annual Return and Maximum Drawdown",
    "Given a multi-period net-value series, compute ",
    " (compound annual growth rate) and the maximum drawdown.",
    "Assess a strategy's long-term compounding ability and its worst loss.",
    "Use CAGR together with maximum drawdown (as in the Calmar ratio) to evaluate risk-adjusted return.",
    "Start 1.0, end 2.0, over 5 years",
    "CAGR = (2.0/1.0)^(1/5) − 1 = 2^0.2 − 1 ≈ 14.87%. The net value doubles over five years, about 14.9% a year.",
    "Maximum drawdown",
    "Net-value series 1.0 → 2.0 → 1.4 → 1.8: peak 2.0, trough 1.4, maximum drawdown = (1.4 − 2.0)/2.0 = −30%. That is, a loss of up to 30% from the peak.",
    "How does CAGR differ from the arithmetic average return?",
    "CAGR is a geometric mean (accounting for compounding) while the arithmetic mean ignores volatility. The greater the volatility, the more the arithmetic mean exceeds the CAGR.",
    "Can a drawdown recover?",
    "A drawdown is the fall from a historical peak to a trough; recovery requires a rise from the trough back to the peak (for example, after −30% a gain of +42.86% is needed to return to the original value).",
    'About "Maximum Drawdown Calculator"',
    "A portfolio maximum-drawdown analysis tool: enter a net-value series to compute the peak-to-trough maximum drawdown, the drawdown recovery period, the annualized return and the Calmar ratio, and plot the drawdown curve as SVG to support risk and drawdown assessment.",
    "Maximum drawdown (MDD) calculation",
    "Drawdown recovery period detection",
    "Calmar ratio risk-adjusted return",
    "Inline SVG drawdown curve",
    "Fund / portfolio risk assessment",
    "Strategy backtest analysis",
    "Risk-adjusted return comparison",
    "Investor education and drawdown demonstration",
]))

# ---------------- current-yield (22) ----------------
write('current-yield', build('current-yield', [
    "Annual Interest / Current Price",
    "Current yield = annual interest / bond price.",
    "Current Yield",
    "/ Bond Current Yield",
    "Bond Current Yield",
    '📖 View the "Annual Interest / Current Price User Guide"',
    "CY = annual interest / current price",
    "Bond price (CNY)",
    "Current yield ignores capital gains and maturity.",
    "Unlike YTM, it does not include the price converging to face value.",
    "📚 Deep Dive: Current Yield",
    "Annual bond interest divided by the current market price, for a quick look at the coupon return rate.",
    "Distinguish it from YTM: current yield ignores capital gains and the discount.",
    "Comparing coupon rates across money-market and bond funds.",
    "Annual interest 50, market price 1000",
    "Current yield = annual interest / market price = 50/1000 = 5%. If the market price falls to 950: 50/950 ≈ 5.26%.",
    "Discount bond",
    "Face value 1000, coupon 4% (annual interest 40), market price 960: current yield = 40/960 ≈ 4.17%, below the YTM of a par trade (which also includes accretion of the discount).",
    "How does current yield differ from YTM?",
    "Current yield looks only at coupon / price; YTM also includes the accretion or amortisation of the principal discount or premium held to maturity, so it is more complete.",
    "What is the current yield of a zero-coupon bond?",
    "A zero-coupon bond has no coupon, so its current yield is 0 and the entire return comes from the capital gain of the discount at maturity (reflected in the YTM).",
]))

# ---------------- ddm-price (23) ----------------
write('ddm-price', build('ddm-price', [
    "Gordon Growth Model Valuation",
    "P = D₁ / (r − g), for stocks with stable growth.",
    "Dividend Discount Model",
    "/ Dividend Discount Model (DDM)",
    "Dividend Discount Model (DDM)",
    '📖 View the "Gordon Growth Model Valuation User Guide"',
    "P = D₁ / (r − g). Only for stocks with stable growth and r > g.",
    "Required rate of return r",
    "Dividend growth rate g",
    "Gordon model P = D₁ / (r − g).",
    "Only for stocks with stable growth and r > g.",
    "📚 Deep Dive: Dividend Discount Model (DDM)",
    "Valuing companies with steadily growing dividends (the Gordon model).",
    "Cross-checking value-stock pricing with PEG and P/E.",
    "Dividend yield",
    " investment strategies' discounted cash-flow benchmark.",
    "D₁ = D₀ × (1+g) = 2.1; P = D₁/(r−g) = 2.1/(10%−5%) = 2.1/0.05 = 42 CNY.",
    "A higher growth rate",
    "If g = 6%: P = 2.12/(0.10−0.06) = 53 CNY. A small rise in growth pushes the valuation up sharply (the denominator is sensitive).",
    "What if r − g is negative or close to 0?",
    "The model requires r > g, otherwise the valuation diverges and is meaningless. When g approaches r for a high-growth stock the result is extremely unstable and this model should not be used.",
    "Two-stage or three-stage DDM?",
    "This tool is the single-stage Gordon model. High-growth companies should be discounted in stages (high growth first, then stable), otherwise they are undervalued.",
]))

# ---------------- dividend-payout (22) ----------------
write('dividend-payout', build('dividend-payout', [
    "Dividend per Share / Earnings per Share",
    "Payout ratio = DPS / EPS.",
    "Dividend Payout Ratio",
    "/ Dividend Payout Ratio",
    '📖 View the "Dividend per Share / Earnings per Share User Guide"',
    "A high payout ratio means generous dividends and low retention.",
    "Growth stocks usually have a lower payout ratio.",
    "📚 Deep Dive: Dividend Payout Ratio",
    "Compute the share of net profit distributed to shareholders.",
    "Retention ratio",
    " (1 − payout ratio), to judge reinvestment capacity.",
    "Dividend-strategy screening (high payout, but it must be sustainable).",
    "Dividends 100m, net profit 500m",
    "Payout ratio = dividends / net profit = 1/5 = 20%. The retention ratio is 80%, used for reinvestment and expansion.",
    "High payout",
    "Dividends 400m, net profit 500m: payout ratio = 80%. A high payout is good for cash returns, but insufficient retention may limit growth.",
    "How does the payout ratio differ from the ",
    "dividend yield",
    "?",
    "Payout ratio = dividends / net profit (the share of earnings distributed); dividend yield = annual dividends / share price (the holding return). The two have different denominators.",
    "Is a higher payout ratio always better?",
    "Not necessarily. A high payout is reasonable for mature, low-growth companies; for a growth company it may sacrifice expansion. Consider the industry and the stage of development.",
]))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""securities 第3批：book-value-per-share / calc-1 / calc-29 / capm-beta"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'securities')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'securities')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EXTRA = {
    'calc-1': {'印花税': 'stamp duty'},
    'calc-29': {'正态分布': 'normal distribution'},
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
    out = {'slug': slug, 'industry': 'securities', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))


# ---------------- book-value-per-share (24) ----------------
write('book-value-per-share', build('book-value-per-share', [
    "(Net Assets − Preferred Stock) / Shares Outstanding",
    "BVPS = shareholders' equity / shares outstanding.",
    "Book Value per Share (BVPS)",
    "/ Book Value per Share",
    "Book Value per Share",
    '📖 View the "(Net Assets − Preferred Stock) / Shares Outstanding User Guide"',
    "Book value per share BVPS = (total shareholders' equity − preferred stock equity) ÷ number of common shares outstanding; it reflects the net assets behind each share and is often used in value investing and in judging a break below book value; it is the counterpart of the price-to-book ratio PB = price ÷ BVPS.",
    "Shareholders' equity (CNY)",
    "Preferred stock equity (CNY)",
    "Shares outstanding (shares)",
    "BVPS reflects the book net-asset backing.",
    "Its ratio to the market price is the reciprocal of the price-to-book ratio.",
    "📚 Deep Dive: Book Value per Share (BVPS)",
    "Compute the book value of shareholders' equity per share.",
    "Compare it with the share price to get a P/B valuation.",
    "Recalculate whenever the share count changes after a dividend, a placement or a buyback.",
    "Net assets 1.0bn, total shares 200m",
    "BVPS = shareholders' equity / total shares = 1.0bn / 200m = 5.00 CNY per share. If the share price is 30 CNY, then P/B = 6.",
    "Share count falls after a buyback",
    "Net assets 1.0bn, share count 180m after a buyback and cancellation: BVPS = 10/1.8 ≈ 5.56 CNY per share, higher than before the buyback (the numerator is unchanged while the denominator shrinks).",
    "Does net assets include minority interests?",
    "Usually the net assets attributable to the parent's shareholders are used (excluding minority interests); the basis must match the denominator of P/B, otherwise it is distorted.",
    "Does a dividend reduce BVPS?",
    "Yes. A dividend reduces retained earnings (net assets) without reducing the share count, so BVPS falls; but the share price adjusts down on the ex-dividend date, so P/B is unchanged.",
]))

# ---------------- calc-1 (28) ----------------
write('calc-1', build('calc-1', [
    "📈 Stock Profit and Loss Calculator",
    "Enter the buy and sell prices and the number of shares to compute the true profit or loss after commissions and taxes",
    '📖 View the "Stock Profit and Loss Calculator User Guide"',
    "Net P&L = sell proceeds − buy cost − buy commission − sell commission − stamp duty − transfer fee; commission = max(turnover × commission rate, minimum commission); stamp duty = sell proceeds × rate (sell side only)",
    "Buy cost = buy price × shares and sell proceeds = sell price × shares; commission is charged as a proportion of turnover and is never below the minimum commission; stamp duty is levied on the sell side only, and the transfer fee is charged on both sides as a proportion of turnover.",
    "Buy price (CNY/share)",
    "Sell price (CNY/share)",
    "Number of shares",
    "Sell stamp duty (%)",
    "Transfer fee (%)",
    "Buy commission = max(buy amount × commission rate, minimum commission)",
    "Sell stamp duty = sell amount × stamp duty rate (charged on the sell side only for A-shares)",
    "Transfer fee = turnover × transfer fee rate (charged by the Shanghai exchange; waived by some brokers in Shenzhen; included here by default)",
    "Net P&L = net sell proceeds − total buy cost",
    "Results are for reference only; actual fees are subject to the broker's settlement statement",
    "📚 Deep Dive: Stock Break-Even Price",
    "Compute the minimum price the stock must reach when sold to cover all trading costs (commission, ",
    ", transfer fee).",
    "Assess the minimum gain threshold before a short-term trade.",
    "Compare the true break-even point under different brokers' commission rates.",
    "Buy at 10 CNY × 1000 shares",
    "Buy amount = 10,000 CNY. Commission rate 0.025% (minimum 5 CNY) → 5 CNY; stamp duty is charged only on the sell side at 0.05% → 5 CNY (estimated on a sale of 10,000); transfer fee 0.001% on both sides ≈ 0.2 CNY. Break-even price ≈ (10000+5+5+0.2)/1000 ≈ 10.02 CNY, i.e. a gain of about 0.2% to recover costs.",
    "The effect of a lower commission rate",
    "With a commission rate of 0.015% (still 5 CNY because of the minimum), the cost of a small order is driven mainly by the minimum commission; for a large order (say 100,000 CNY) the commission is 15 CNY and the effect on the break-even price is clearer.",
    "How is stamp duty charged now?",
    "For A-shares, 0.05% of turnover is charged on the sell side (after the 2023 halving) and nothing on the buy side; the transfer fee is about 0.001% on both sides in both Shanghai and Shenzhen.",
    "How is the 5 CNY minimum commission handled?",
    "If a single trade's commission is under 5 CNY it is charged at 5 CNY, so the effective rate on small trades is far above the nominal rate and the break-even point is raised mainly by the minimum commission.",
]))

# ---------------- calc-29 (22) ----------------
write('calc-29', build('calc-29', [
    "📈 Bollinger Bands (Upper / Lower / Std Dev) Calculator",
    "Compute the Bollinger Band middle line (SMA), upper band, lower band, %B and bandwidth",
    '📖 View the "Bollinger Bands (Upper / Lower / Std Dev) Calculator User Guide"',
    "Period N (default 20)",
    "Standard deviation multiple K (default 2)",
    "Price series (one value per line, at least N data points)",
    "Middle line = MA(N); upper/lower bands = middle ± K × σN; σN = √( Σ(price_i − MA)² / N )",
    "Bollinger Bands use an N-period moving average as the middle line and K standard deviations as the band width; a price touching the upper or lower band is seen as an overbought or oversold signal, and a narrowing band often means falling volatility.",
    "📖 Formula: middle SMA = average of the last N closing prices; upper band = SMA + K×σ; lower band = SMA − K×σ (σ is the N-day population standard deviation); %B = (price − lower band)/(upper band − lower band)×100; bandwidth = (upper band − lower band)/SMA×100.",
    "📚 Deep Dive: Bollinger Bands",
    "Use 20-day closing prices to compute the middle line (SMA) and the upper/lower bands (±2σ) and judge the price's relative position.",
    "Identify overbought (near the upper band) and oversold (near the lower band) conditions.",
    "Bandwidth measures volatility expansion or contraction.",
    "20-day average price 50, σ = 2",
    "Middle = 50; upper = 50 + 2 × 2 = 54; lower = 50 − 2 × 2 = 46. Bandwidth = (54 − 46)/50 = 16%; %B = (price − 46)/(54 − 46): at a price of 50 → %B = (50 − 46)/8 = 50% (at the middle line), at a price of 54 → %B = 100% (touching the upper band).",
    "A narrowing band",
    'If σ falls to 1: upper band 52, lower band 48, bandwidth = (52 − 48)/50 = 8%. A contracting band often signals an expansion in volatility (the "Bollinger squeeze").',
    "Why are the parameters 20 and 2?",
    "20 days is a common short-to-medium-term window, and 2σ covers about 95% of the ",
    " interval. They can be adjusted to suit the strategy (for example 10 and 1.5, or 50 and 2.5).",
    "What is %B?",
    "%B = (price − lower band)/(upper band − lower band): 0 at the lower band, 1 at the upper band and >1 when the price breaks above the upper band. It quantifies the overbought or oversold position.",
]))

# ---------------- capm-beta (21) ----------------
write('capm-beta', build('capm-beta', [
    "Covariance / Market Variance",
    "/ Beta Coefficient Calculation",
    "Beta Coefficient Calculation",
    '📖 View the "Covariance / Market Variance User Guide"',
    "β = covariance / market variance. The samples must be the same length.",
    "Stock returns (comma-separated)",
    "Market returns (comma-separated)",
    "β = covariance / market variance.",
    "The samples must be the same length.",
    "📚 Deep Dive: CAPM Beta Inputs",
    "Given the risk-free rate, expected market return and Beta, estimate the expected return of a stock or ",
    "portfolio",
    "A portfolio Beta is the weighted average of its holdings' Betas, then fed into CAPM.",
    "Compare the required rate of return at different Betas.",
    "Risk-free 3%, market 8%: E(R) = 3% + 1.2 × (8% − 3%) = 9%. With Beta = 0.8, E(R) = 3% + 0.8 × 5% = 7%.",
    "Portfolio Beta",
    "Holding A (Beta 1.5, weight 60%) + B (Beta 0.9, weight 40%): portfolio Beta = 1.5 × 0.6 + 0.9 × 0.4 = 1.26, and feeding it into CAPM gives E(R) = 3% + 1.26 × 5% = 9.3%.",
    "What are the limitations of CAPM?",
    "It relies on an unobservable market portfolio, Beta is unstable, and the single factor ignores size, value, momentum and so on. In practice it is a benchmark, not a precise forecast.",
    "Which market's Beta should be used?",
    "Typically a regression against the corresponding market index (the CSI 300 for A-shares, the S&P 500 for US stocks); Betas across markets are not directly comparable.",
]))

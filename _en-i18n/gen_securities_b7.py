#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""securities 第7批：market-risk-premium / max-drawdown / option-breakeven-call / option-breakeven-put"""
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


# ---------------- market-risk-premium (18) ----------------
write('market-risk-premium', build('market-risk-premium', [
    "Market Return - Risk-Free Rate",
    "/ Market Risk Premium",
    '📖 View the "Market Return - Risk-Free Rate User Guide"',
    "Expected market return",
    "Risk premium is a core CAPM input.",
    "Long-run history about 4%-6%.",
    "📚 Deep Dive: Market Risk Premium (MRP)",
    "Expected market return minus risk-free rate, the equity risk premium.",
    "Core input to CAPM and DCF discount rates.",
    "Premium estimates across markets/periods.",
    "Expected market 8%, risk-free 3%",
    "MRP = 8% - 3% = 5%. That is, the extra compensation required for bearing market systemic risk is about 5%.",
    "Risk-free declines",
    "Risk-free 2%, expected 8%: MRP = 6%. Low-rate environments expand the premium.",
    "How is MRP estimated?",
    "Commonly via the historical mean equity-index excess return, surveys (e.g. Ibbotson), or an implied reverse method; results vary widely.",
    "Can MRP be negative?",
    "Extremely rare (e.g. market underperforms the risk-free rate over the long run); theoretically invalid, usually due to a special estimation window.",
]))

# ---------------- max-drawdown (21) ----------------
write('max-drawdown', build('max-drawdown', [
    "Compute maximum drawdown from peak and trough prices",
    "Enter the peak and trough prices over a period to compute the maximum drawdown.",
    "MD = (Peak - Trough) / Peak",
    "/ Maximum Drawdown Calculator",
    "Maximum Drawdown Calculator",
    '📖 View the "Compute maximum drawdown from peak and trough prices User Guide"',
    "MDD = (Peak-Trough)/Peak × 100%",
    "The smaller the drawdown, the more comfortable the risk bearing.",
    "📚 Deep Dive: Maximum Drawdown",
    "The largest decline from a peak to a subsequent trough in a net-value series.",
    'Risk-management core metric (more intuitive than volatility at showing "the worst loss").',
    "Used with the Calmar ratio.",
    "Net value 100 -> 70",
    "Maximum Drawdown",
    "= (70-100)/100 = -30%. That is, the most you can lose from the highest point is 30%.",
    "Take the largest across multiple drawdowns",
    "Series 100->80->120->84: first -20% (100->80), second 120->84 is -30%; so the maximum drawdown = -30% (the largest in absolute value).",
    "What is the difference between drawdown and volatility?",
    'Volatility is a symmetric dispersion; drawdown only measures downside, the cumulative drop from peak to trough, and better fits "the worst loss actually experienced".',
    "Can maximum drawdown be negative?",
    'Drawdown itself is recorded as negative (-30%), indicating a loss; "maximum" means the largest in absolute value.',
]))

# ---------------- option-breakeven-call (23) ----------------
write('option-breakeven-call', build('option-breakeven-call', [
    "Strike Price + Premium",
    "Breakeven = strike price + premium.",
    "Call Option Breakeven",
    "/ Call Option Breakeven",
    '📖 View the "Call Option Breakeven User Guide"',
    "Call breakeven = K + premium",
    "Premium (yuan)",
    "Above this point the buyer profits.",
    "The seller's breakeven is the same but opposite in direction.",
    "📚 Deep Dive: Call Option Breakeven",
    "The underlying price at which a call buyer breaks even at expiry = strike price + premium.",
    "Options strategy",
    "breakeven",
    "estimation.",
    "Compare with the cost of buying the stock directly.",
    "Strike 100, premium 5",
    "Call breakeven = K + premium = 100 + 5 = 105. At expiry, underlying > 105 buyer profits, = 105 breakeven, < 105 loss (max loss = premium 5).",
    "Higher premium",
    "K=100, premium 8: breakeven = 108. The more expensive the premium, the more the price must rise to recoup.",
    "Why add the premium?",
    "The buyer has already paid the premium; the underlying must rise past the strike and then cover this cost to break even.",
    "What about the put option breakeven?",
    "K - premium (see option-breakeven-put), opposite direction.",
]))

# ---------------- option-breakeven-put (22) ----------------
write('option-breakeven-put', build('option-breakeven-put', [
    "Compute the put option breakeven price from strike price and premium",
    "Enter the strike price and premium to compute the put option breakeven price.",
    "BE = Strike Price - Premium",
    "/ Put Option Breakeven Price Calculator",
    "Put Option Breakeven Price Calculator",
    '📖 View the "Compute the put option breakeven price from strike price and premium User Guide"',
    "Put breakeven = K - P",
    "Premium P (yuan)",
    "The underlying falling below this price starts to profit.",
    "50-3 -> 47 yuan.",
    "📚 Deep Dive: Put Option Breakeven",
    "The underlying price at which a put buyer breaks even at expiry = strike price - premium.",
    "Cost estimation for protective-put insurance.",
    "Analysis with a short-underlying hedging portfolio.",
    "Strike 100, premium 5",
    "Put breakeven = K - premium = 100 - 5 = 95. At expiry, underlying < 95 buyer profits, = 95 breakeven, > 95 loss (max loss = premium 5).",
    "Premium 3",
    "K=100, premium 3: breakeven = 97. The cheaper the insurance, the higher the downside-protection threshold (profit triggered more easily).",
    "What is the maximum profit on a put option?",
    "Maximum profit occurs when the underlying falls to 0 = K - premium (theoretical), still bounded; maximum loss is the premium.",
    "How does it differ from a stop-loss order?",
    "A put option is paid insurance (locks in downside); a stop-loss order is free but has slippage and gap risk; their cost structures differ.",
]))

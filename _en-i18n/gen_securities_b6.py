#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""securities 第6批：enterprise-value / information-ratio / margin-requirement / market-cap"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'securities')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'securities')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EXTRA = {
    'market-cap': {'市值': 'Market Cap'},
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


# ---------------- enterprise-value (23) ----------------
write('enterprise-value', build('enterprise-value', [
    "Compute enterprise value from market cap, debt and cash",
    "Enter the stock market cap, total debt and cash & equivalents to compute enterprise value.",
    "EV = Market Cap + Debt - Cash",
    "/ Enterprise Value (EV) Calculator",
    "Enterprise Value (EV) Calculator",
    '📖 View the "Compute enterprise value from market cap, debt and cash User Guide"',
    "Stock market cap (10k yuan)",
    "Total debt (10k yuan)",
    "Cash & equivalents (10k yuan)",
    "EV reflects the total acquisition cost.",
    "1000+200-100 -> 1100 (10k).",
    "📚 Deep Dive: Enterprise Value (EV)",
    "EV = Market Cap + Total Debt - Cash; measures the total cost to acquire the whole firm.",
    "EV/EBITDA valuation (strips out capital-structure effects).",
    "Compare peer companies at different leverage levels.",
    "Market cap 5B, debt 1B, cash 0.5B",
    "EV = 50 + 10 - 5 = 55 (100M). If EBITDA = 800M, then EV/EBITDA = 55/8 ≈ 6.875x.",
    "High-cash company",
    "Market cap 5B, debt 0.5B, cash 2B: EV = 50 + 5 - 20 = 35 (100M). High cash markedly lowers EV.",
    "Why subtract cash?",
    "The acquirer also takes over the cash, which is like a reduced net payment, so it is deducted from market cap plus debt.",
    "What is the difference between EV and market cap?",
    "Market cap looks only at equity; EV includes debt and deducts cash, reflecting the cost to 'buy the whole business', and is better for cross-leverage comparison.",
]))

# ---------------- information-ratio (23) ----------------
write('information-ratio', build('information-ratio', [
    "Compute the information ratio from an active-return series",
    "Enter the series of excess returns over the benchmark (comma- or space-separated) to compute the information ratio.",
    "IR = Mean Active Return / Tracking Error",
    "/ Information Ratio Calculator",
    "Information Ratio Calculator",
    '📖 View the "Compute the information ratio from an active-return series User Guide"',
    "Information Ratio IR = mean active return / tracking error; active return = portfolio return - benchmark return; tracking error = std dev of the active-return series (annualized by multiplying sqrt of yearly periods); the higher the IR, the more stable the excess return per unit of active risk; generally IR > 0.5 is considered good and > 1.0 excellent.",
    "IR measures excess return per unit of active risk.",
    "Sample series -> about 0.408.",
    "📚 Deep Dive: Information Ratio (IR)",
    "The mean active return divided by",
    "tracking error",
    ", measuring the stability of excess returns.",
    "Risk-adjusted assessment of a fund/portfolio manager's stock-selection skill.",
    "Difference: IR looks at excess relative to the benchmark, Sharpe looks at absolute.",
    "Mean active return 1.5%, tracking error 2%",
    "IR = mean active return / tracking error = 1.5%/2% = 0.75. IR > 0.5 is generally considered to show some excess-return capability.",
    "Tracking error narrows",
    "Mean active return 1.5%, TE drops to 1%: IR = 1.5. The smaller the TE (closer to the benchmark yet still ahead), the higher the IR.",
    "What is the difference between IR and Sharpe?",
    "Sharpe uses the risk-free rate as the benchmark and looks at absolute risk-adjusted return; IR uses a market/performance benchmark and looks at the stability of relative excess.",
    "What IR counts as excellent?",
    "Empirically IR > 1 is excellent, 0.5-1 good, < 0.5 unstable excess. But a long enough sample is needed; short-term IR is noisy.",
]))

# ---------------- margin-requirement (24) ----------------
write('margin-requirement', build('margin-requirement', [
    "Compute the margin ratio from account equity and position market value",
    "Enter account equity and position market value to compute the margin ratio.",
    "Margin Ratio = Equity / Position Market Value",
    "/ Margin Requirement Calculator",
    "Margin Requirement Calculator",
    '📖 View the "Compute the margin ratio from account equity and position market value User Guide"',
    "Margin ratio = Equity / Position Market Value × 100%",
    "Account equity (yuan)",
    "Position market value (yuan)",
    "The lower the ratio, the higher the leverage and the greater the liquidation risk.",
    "📚 Deep Dive: Margin Requirement",
    "Margin buying (or",
    "futures margin",
    ") requires frozen funds = position market value × margin rate.",
    "Broker/exchange maintenance-margin and initial-margin estimation.",
    "Leverage multiple = 1 / margin-rate conversion.",
    "Position market value 100k, margin rate 50%",
    "Margin = 100k × 50% = 50k. Leverage = 1/50% = 2x. If the margin rate is 100% (no leverage), the full 100k is required.",
    "Maintenance margin warning",
    "Initial margin 50%, maintenance 30%: when the market value falls so that equity < 30% of position market value, a margin call is triggered and must be topped up.",
    "Initial margin and maintenance margin?",
    "Initial is the frozen ratio at open; maintenance is the minimum equity ratio, below which a margin call/forced liquidation occurs.",
    "Does a lower margin rate mean higher leverage?",
    "Yes. A 10% margin rate corresponds to 10x leverage; risk and reward are amplified together, and the liquidation line is closer.",
]))

# ---------------- market-cap (22) ----------------
write('market-cap', build('market-cap', [
    "Share Price × Total Shares",
    "Market cap = share price × total shares outstanding.",
    "Total Market Cap",
    "/ Total Market Cap Calculation",
    "Total Market Cap Calculation",
    '📖 View the "Share Price × Total Shares User Guide"',
    "Market cap = share price × total shares",
    "Total shares (shares)",
    "Market cap moves in real time with the share price.",
    "Float market cap counts only tradable shares.",
    "📚 Deep Dive: Total Market Cap",
    ", measuring company size.",
    "Large-cap/mid-cap/small-cap classification thresholds.",
    "Index weighting and liquidity tiering.",
    "Share price 50, shares 200M",
    "Market cap = 50 × 200M = 10B yuan. Mid-to-large cap.",
    "Share count change",
    "After issuance 220M shares, price 48: market cap = 48 × 220M = 10.56B. Share expansion dilutes price; total cap change depends on the product of the two.",
    "Total market cap vs float market cap?",
    "Total market cap uses total shares; float market cap counts only tradable shares. Index inclusion/exclusion is usually based on float market cap.",
    "Does market cap include debt?",
    "No. Market cap is equity value; enterprise value (EV) is what includes debt and deducts cash.",
]))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""securities 第1批：annualized-vol / annualized-volatility / beta-covariance / black-scholes-call / black-scholes-put"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'securities')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'securities')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EXTRA = {
    'annualized-vol': {'标准差': 'standard deviation', '夏普比率': 'Sharpe ratio'},
    'annualized-volatility': {'标准差': 'standard deviation'},
    'beta-covariance': {'百分比': 'percentage'},
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


# ---------------- annualized-vol (26) ----------------
write('annualized-vol', build('annualized-vol', [
    "Annualized Volatility from Daily Volatility",
    "Enter the daily volatility σ_d to obtain the annualized volatility.",
    "σ_year = σ_d × √252",
    "/ Annualized Volatility Calculator",
    "Annualized Volatility Calculator",
    '📖 View the "Annualized Volatility from Daily Volatility User Guide"',
    "Daily volatility σ_d",
    "252 is the number of annualized trading days.",
    "📚 Deep Dive: Annualized Volatility",
    "A stock's past-year daily-return ",
    " (daily volatility) has to be converted into a directly comparable ",
    "annualized volatility",
    "Fund / portfolio risk disclosure and ",
    "maximum drawdown",
    " and other metrics used together must share the same annualized basis.",
    "When option implied volatility is compared with historical volatility, both must be on the same annualized basis to be meaningful.",
    "Daily volatility 1.5% → annualized",
    "Formula σ_year = σ_day × √252. With σ_day = 1.5%: σ_year = 1.5% × √252 ≈ 1.5% × 15.875 ≈ 23.81%. That is, the stock's annualized volatility is about 23.8%.",
    "Daily volatility 0.8% → annualized",
    "σ_year = 0.8% × √252 ≈ 0.8% × 15.875 ≈ 12.70%. A low-volatility blue chip has annualized volatility of about 12.7%.",
    "Why multiply by √252 and not 365?",
    "252 is the number of annualized trading days for A-shares and US stocks (weekends and holidays excluded); volatility accumulates by the time",
    "square root",
    "rule, hence √252. Using calendar days would need √365, but that overstates real trading volatility.",
    "Can annualized volatility be taken directly as the annual gain or loss range?",
    'No. Volatility is a standard-deviation measure that only describes dispersion, not direction. An annualized volatility of 24% does not equal "a 24% gain in a year"; it is the extension of roughly a 67% probability that daily returns stay within ±1.5%.',
]))

# ---------------- annualized-volatility (21) ----------------
write('annualized-volatility', build('annualized-volatility', [
    "Daily Volatility × √252",
    "Annualized volatility = daily volatility × √number of trading days.",
    "Annualized Volatility",
    "/ Annualized Volatility",
    '📖 View the "Daily Volatility × √252 User Guide"',
    "Daily volatility",
    "Trading days per year (days)",
    "√252 is commonly used for annualization.",
    "Volatility aggregates over time.",
    "📚 Deep Dive: Annualized Volatility (Custom Periods)",
    "Given an asset's per-period volatility over a sample period (such as weekly or monthly volatility), it must be annualized by the actual number of periods.",
    "When comparing across markets, the number of trading days per year differs (about 242 for A-shares and 252 for US stocks), so the period count d must be specified explicitly.",
    "In backtesting, annualizing by 250 trading days or by 12 months must match the benchmark's basis.",
    "Daily volatility 2%, annualized over 250 trading days",
    "Formula σ_year = σ_period × √d. With σ_period = 2% and d = 250: σ_year = 2% × √250 ≈ 2% × 15.811 ≈ 31.62%.",
    "Monthly volatility 6%, annualized over 12 months",
    "σ_year = 6% × √12 ≈ 6% × 3.464 ≈ 20.78%. Note: confirm that the monthly volatility is the monthly-return ",
    "Should d be 250 or 252?",
    "The difference is tiny (√250 = 15.811, √252 = 15.875, a 0.4% gap). A-shares commonly use 242-250 and US stocks 252; what matters is matching the comparison benchmark, not absolute precision.",
    "Where does the per-period volatility come from?",
    "Take the standard deviation of the returns in each period of the sample: σ = √(Σ(rᵢ−r̄)²/N). This tool takes the per-period volatility as input and annualizes it directly by √d.",
]))

# ---------------- beta-covariance (21) ----------------
write('beta-covariance', build('beta-covariance', [
    "Compute β from the Covariance and Variance of Stock and Market Returns",
    "Enter the covariance of stock and market returns and the variance of market returns to obtain β.",
    "Beta Calculator (Covariance Method)",
    "/ Beta Calculator (Covariance Method)",
    '📖 View the "Compute β from the Covariance and Variance of Stock and Market Returns User Guide"',
    "Covariance Cov",
    "Market variance Var_m",
    "β measures a stock's systematic risk relative to the market.",
    "📚 Deep Dive: Beta Coefficient (Covariance Method)",
    "Given the covariance of stock and market returns and the market variance, obtain Beta directly.",
    "For cases where a spreadsheet has already produced the covariance matrix and only a quick Beta conversion is needed.",
    "To check whether a Beta from the regression method is consistent.",
    "Covariance 0.0018, market variance 0.0015",
    "Beta = cov / var(market) = 0.0018 / 0.0015 = 1.20. Consistent with the regression method.",
    "Covariance 0.0009, market variance 0.0020",
    "Beta = 0.0009 / 0.0020 = 0.45. Beta < 1 is defensive, with less volatility than the market.",
    "What units are used for cov and var?",
    "Both use the squared scale of return decimals or ",
    " — as long as the numerator and denominator match (both in % or both in decimals).",
    "What does a negative Beta mean?",
    "The stock and the market move in opposite directions (as with some safe-haven assets): the stock rises when the market falls. This is actually rare and mostly appears in specific hedge portfolios.",
]))

# ---------------- black-scholes-call (18) ----------------
write('black-scholes-call', build('black-scholes-call', [
    "European Call Option Pricing",
    "Black-Scholes Call",
    "/ Black-Scholes Call Option",
    "Black-Scholes Call Option",
    '📖 View the "European Call Option Pricing User Guide"',
    "European option, no-dividend assumption.",
    "N(x) is the standard normal distribution function.",
    "📚 Deep Dive: Black-Scholes Call Option Pricing",
    "Estimating the theoretical price of a European call option given the underlying price, strike, risk-free rate, volatility and time to expiry.",
    "Compare with the option market quote to spot over- or under-valuation.",
    "A pricing baseline before option Greeks and arbitrage strategies.",
    "d1 = (ln(100/100) + (0.05 + 0.2²/2) × 1) / (0.2 × √1) = 0.07 / 0.2 = 0.35; d2 = 0.35 − 0.2 = 0.15. N(0.35) ≈ 0.6368, N(0.15) ≈ 0.5596. Call = 100 × 0.6368 − 100 × e^(−0.05) × 0.5596 ≈ 63.68 − 53.24 = 10.44.",
    "Out-of-the-money option S = 95",
    "S = 95, K = 100, r = 5%, σ = 20%, T = 1: d1 = (ln0.95 + 0.07) / 0.2 ≈ 0.166, d2 ≈ −0.034. N(0.166) ≈ 0.566, N(−0.034) ≈ 0.486. Call ≈ 95 × 0.566 − 100 × 0.951 × 0.486 ≈ 53.77 − 46.22 = 7.55.",
    "What assumptions does the BS formula make?",
    "It assumes the underlying follows a geometric Brownian motion, no arbitrage, no dividends, a European option (not exercised before expiry) and constant volatility and interest rate. Real markets have dividends, gaps and volatility smiles, so it is a theoretical baseline.",
    "Why is the computed value below or above the market price?",
    "Implied volatility ≠ historical volatility. If the theoretical price is below the market price, the market's implied volatility is higher (more expectation of volatility); if above, it is lower.",
]))

# ---------------- black-scholes-put (18) ----------------
write('black-scholes-put', build('black-scholes-put', [
    "European Put Option Pricing",
    "Black-Scholes Put",
    "/ Black-Scholes Put Option",
    "Black-Scholes Put Option",
    '📖 View the "European Put Option Pricing User Guide"',
    "Satisfies put-call parity with the call.",
    "No-dividend assumption.",
    "📚 Deep Dive: Black-Scholes Put Option Pricing",
    "Estimating the theoretical price of a European put option.",
    "Checking the put-call parity relation (Put = Call − S + K·e^(−rT)).",
    "Cost estimation for a protective put insurance strategy.",
    "As above, d1 = 0.35, d2 = 0.15. Put = K·e^(−rT)·N(−d2) − S·N(−d1) = 100 × 0.9512 × 0.4404 − 100 × 0.3632 ≈ 41.88 − 36.32 = 5.56. Check by parity: Call − S + K·e^(−rT) = 10.44 − 100 + 95.12 = 5.56 ✓.",
    "Deep in-the-money put S = 80",
    "S = 80, K = 100, r = 5%, σ = 20%, T = 1: d1 = (ln0.8 + 0.07) / 0.2 ≈ −0.216, d2 ≈ −0.416. Put ≈ 100 × 0.951 × 0.661 − 80 × 0.586 ≈ 62.87 − 46.88 = 15.99.",
    "What is the price relationship between a put and a call?",
    "Put-call parity: P + S = C + K·e^(−rT). It holds whenever there are no dividends before expiry and is the core of arbitrage pricing.",
    "What does rising volatility do to a put option?",
    "Rising volatility increases the value of a put option (as with a call) - volatility favours the option buyer, since downside is limited and upside potential is large.",
]))

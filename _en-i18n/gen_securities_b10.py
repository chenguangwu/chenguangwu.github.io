#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""securities 第10批：index（分类索引页）"""
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


# ---------------- index (76) ----------------
write('index', build('index', [
    "📈 Securities Investment Tools",
    "Securities Investment",
    "Securities Investment Tools",
    "Bond Convexity Calculator",
    "First discount each period's coupon and principal repayment to get the bond price; Macaulay duration is the time-weighted average of cash flows (annualized per period); convexity captures the second-order rate sensitivity of duration, correcting the curvature of the price-yield curve.",
    "Enter win rate, risk-reward ratio or per-trade affordable loss to compute the optimal position fraction with the Kelly formula f* = W - (1-W)/R, or determine order lots by the fixed-risk method.",
    "Enter a closing-price series to compute moving average MA, MACD, RSI and KDJ, aiding trend and buy/sell signal judgment for technical analysis.",
    "Enter stock and market return series to compute the Beta coefficient, covariance and correlation, measuring a stock's systematic risk relative to the market, for CAPM pricing and portfolio risk assessment.",
    "Bond Duration Calculator",
    "Macaulay duration = sum of each cash flow's present value times its time t, divided by the bond price; modified duration = Macaulay / (1 + per-period yield), the percentage price change for a 1% yield change.",
    "Covariance-Method Beta Calculator",
    "Compute Beta from the covariance and variance of stock and market returns",
    "Gordon Growth Model Price Calculator",
    "Compute stock price from expected dividend, required return and growth rate",
    "Tracking Error Calculator",
    "Enter the excess-return series of portfolio and benchmark (comma- or space-separated) to compute tracking error TE = std(r_p - r_b), measuring the volatility risk of active management deviating from the benchmark.",
    "Stock Holding-Period Return Calculator",
    "Compute holding-period return from buy/sell prices and dividends",
    "Book-to-Market Ratio Calculator",
    "Compute book-to-market ratio from net assets per share and share price",
    "PEG Valuation Metric Calculator",
    "Compute PEG from the P/E ratio and earnings growth rate",
    "Enter a portfolio net-value series (one number per line) to compute the maximum drawdown from peak to trough, drawdown recovery period, annualized return and Calmar ratio, and plot the drawdown curve.",
    "Stock Profit and Loss Calculation",
    "Enter buy price, sell price, share count and commission/fees to compute the gross profit, net P/L and return of a stock trade, for reviewing trading costs and real profit estimates.",
    "Bollinger Bands Upper/Lower Bands (Std Dev) Calculation",
    "Compute Bollinger Bands middle (SMA), upper, lower, %B and bandwidth",
    "Black-Scholes Call",
    "Black-Scholes European call option pricing calculator; enter underlying price, strike, volatility, risk-free rate and term to output the theoretical option price and Greeks, aiding derivatives valuation; pure front-end.",
    "Black-Scholes Put",
    "Black-Scholes European put option pricing calculator; enter underlying price, strike, volatility, risk-free rate and term to output the theoretical option price and Greeks, aiding derivatives valuation; pure front-end.",
    "Market risk premium calculator; enter the equity market's expected return and the risk-free rate to obtain the equity risk premium (ERP), for CAPM and asset valuation, suited to investment-analysis teaching; pure front-end.",
    "Book Value per Share (BVPS)",
    "(Net assets - preferred stock) / tradable shares",
    "Margin Ratio = Equity / Position Market Value",
    "Enter account equity and position market value to compute the margin ratio = equity / position market value, for monitoring the margin usage and risk level of margin or futures accounts.",
    "Price-to-Book Ratio",
    "Price-to-Book (P/B) calculator: enter share price and book value per share BVPS to compute P/B = price / BVPS, for judging stock valuation levels.",
    "Call Option Breakeven",
    "Call option breakeven calculator: enter strike price and premium to compute breakeven = strike + premium, for options trade profit/loss analysis.",
    "BE = Strike Price - Premium",
    "Compute the put option breakeven price from strike price and premium",
    "FCF Yield = FCF / Share Price",
    "Enter FCF per share and share price to compute the FCF yield = FCF / share price, for assessing a firm's real cash return and valuation margin of safety.",
    "Beta Coefficient",
    "Beta coefficient online calculator; enter stock and market return series to compute the ratio of covariance to market variance for the systematic risk coefficient, for CAPM and portfolio analysis; pure front-end.",
    "Annualized Volatility",
    "Enter daily volatility (or daily-return std dev) and trading days per year to annualize volatility = daily volatility x sqrt(trading days), for risk assessment and option pricing.",
    "Earnings Yield = EPS / P",
    "Enter EPS and share price to compute earnings yield = EPS / P, the reciprocal of the P/E ratio, for cross-comparing stock earnings return with bond yield.",
    "EV = Market Cap + Debt - Cash",
    "Enter stock market cap, total debt and cash & equivalents to compute EV = market cap + debt - cash, for comparing acquisition valuations across capital structures.",
    "IR = Mean Active Return / Tracking Error",
    "Information ratio (IR) calculator: enter the mean of the active-return series and tracking error to compute IR = mean active return / tracking error, assessing a fund manager's excess-return stability.",
    "YTM Approximation",
    "Bond yield (YTM) approximation tool; enter face value, current price, coupon and years to maturity to quickly compute YTM with an approximate formula, aiding bond investment return assessment; pure front-end.",
    "Current Yield",
    "Enter annual bond interest and current market price to compute current yield = annual interest / bond price, for comparing fixed-income levels and pre-maturity coupon returns across bonds.",
    "Dividend Payout Ratio",
    "Dividend payout ratio calculator: enter EPS and DPS to compute payout ratio = DPS/EPS, measuring a company's dividend proportion and retention policy.",
    "Dividend Discount Model",
    "Enter next-year expected dividend, discount rate and perpetual growth rate to estimate the intrinsic value of a stable-growth stock with P = D1/(r-g) via the Gordon growth model, for dividend-discount valuation.",
    "MD = (Peak - Trough) / Peak",
    "Maximum drawdown calculator: enter the period's peak and trough prices to compute MD = (peak - trough) / peak, measuring investment risk and downside magnitude.",
    "σ_year = σ_day × √252",
    "Annualized volatility calculator: enter daily volatility σ_day and convert to annualized volatility by √252 trading days, for portfolio risk measurement and volatility assessment.",
    "Total Market Cap",
    "Total market cap calculator: enter share price and total shares to compute total market cap = share price × total shares, for listed-company size assessment and index-weight judgment.",
    'About "Securities Investment Tools"',
    "The Securities Investment Tools collection includes 35 free online tools, covering common calculation, conversion and lookup needs in securities investment scenarios. Whether you are a practitioner, student or ordinary user in the field, you can find ready-to-use utilities here. All tools run purely in the front end; data is not uploaded to servers, protecting privacy and security.",
    "The securities investment tools on this page include (some representative tools):",
    "These tools help you quickly complete common securities-investment tasks without memorizing complex formulas or manual conversions; just enter to get results.",
    "Do the securities investment tools need to be downloaded or registered?",
    "No. All securities investment tools on this page are pure front-end online tools; open the page to use them directly, no software installation, no account registration, and no data upload.",
    "Are the securities investment tools' results accurate? Is the data safe?",
    "The tools compute locally in your browser based on public math formulas and common industry standards, with results available instantly. All calculations complete on your device; data is never uploaded to servers, ensuring privacy and security.",
]))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""securities 第9批：position-sizing / technical-indicator"""
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


# ---------------- position-sizing (52) ----------------
write('position-sizing', build('position-sizing', [
    "🧮 Position Sizing Calculator",
    "Kelly formula for the optimal position, supporting both risk-ratio and fixed-risk-capital modes",
    "/ Position Sizing",
    '📖 View the "Position Sizing Calculator User Guide"',
    "🎲 Kelly Formula",
    "💵 Fixed Risk",
    "Win rate (%)",
    "Risk-reward ratio (win/loss)",
    "Total capital (yuan)",
    "Risk capital per trade (yuan)",
    "Buy price",
    "Stop-loss price",
    "Target price",
    "Fee rate (%)",
    "🔢 Kelly Formula",
    "W = win rate, R = risk-reward ratio (avg win / avg loss)",
    "Half-Kelly",
    "= f* / 2 (practically common, reduces volatility)",
    "Suggested position amount",
    "= total capital × Kelly fraction",
    "🔢 Fixed-Risk Capital Method",
    "Risk capital",
    "= total capital × risk ratio",
    "Risk per lot",
    "= |buy price - stop-loss price| × lots",
    "Suggested lots",
    "= risk capital / risk per lot",
    "Risk-reward ratio",
    "= (target price - buy price) / (buy price - stop-loss price)",
    "📊 Kelly Fraction Reference",
    "Not recommended to trade (negative expectation)",
    "Conservative, lighter per-trade position",
    "Moderate, half-Kelly commonly used",
    "Aggressive, high volatility risk",
    "Theoretically should go all-in + leverage (not advised in practice)",
    "Fixed risk: shares = capital × risk% / |entry price - stop price|; Kelly: f* = win rate - loss rate / risk-reward (half-Kelly = f* / 2)",
    "The fixed-fraction method first sets the affordable loss per trade (capital × risk%), then divides by per-share risk to get the position; the Kelly formula gives the optimal bet fraction by win rate and risk-reward, and half-Kelly is commonly used in practice to reduce drawdown.",
    "The Kelly formula assumes repeatable games; single trades need caution. In practice, half-Kelly or lower is used, with a per-trade risk cap (usually 1%-3%).",
    "📚 Deep Dive: Position Sizing and the Kelly Formula",
    "Compute the shares to buy from the affordable risk amount and per-share risk (fixed-risk method).",
    "The Kelly formula estimates the optimal bet fraction (f=(W-L)/W, W win rate, L odds-related).",
    "Half-Kelly (more robust) made operational.",
    "Account 100k, per-trade risk 2%, per-share risk 2 yuan",
    "Affordable loss = 100k × 2% = 2000 yuan; shares = 2000/2 = 1000 shares. That is, buy at most 1000 shares; a 2 yuan/share stop-loss loses 2000.",
    "Kelly",
    "Win rate 55%, odds 1 (risk-reward 1:1): f = (0.55×1-0.45)/1 = 0.10, full Kelly 10%, half-Kelly 5%. Half-Kelly is more robust, reducing ruin risk.",
    "Do fixed-risk and Kelly conflict?",
    'No conflict: Kelly sets the "account fraction", fixed-risk sets the "shares per share stop-loss". In practice, half-Kelly + fixed-risk dual constraints are often used.',
    "What are the assumptions of the Kelly formula?",
    "Assumes independent repeated gambling with known and stable probabilities and odds. Live probability estimates have errors, so half-Kelly or more conservative fractions are used.",
    'About "Position Sizing Calculator"',
    "Position Sizing Calculator - Kelly-formula position calculation, an online capital-management tool, free to use. A professional financial calculator using standard formulas, with data processed locally and not leaked.",
]))

# ---------------- technical-indicator (48) ----------------
write('technical-indicator', build('technical-indicator', [
    "📈 Technical Indicator Calculator",
    "Enter a closing-price series to compute MA, MACD, RSI and KDJ technical indicators",
    "/ Technical Indicator Calculation",
    '📖 View the "Technical Indicator Calculator User Guide"',
    "Closing-price series (comma- or newline-separated)",
    "MA period",
    "RSI period",
    "MACD fast line",
    "MACD slow line",
    "Signal line",
    "📋 Indicator Notes",
    "📊 MA Moving Average",
    "MA(n) = arithmetic mean of the most recent n days' closing prices. Reflects trend direction; golden cross (short above long) is bullish, death cross (short below long) is bearish.",
    "📊 MACD Moving Average Convergence Divergence",
    "= EMA(fast) - EMA(slow)",
    "= EMA(DIF, signal line)",
    "MACD histogram",
    "DIF crossing above DEA is a golden cross (bullish); crossing below is a death cross (bearish).",
    "📊 RSI Relative Strength Index",
    "RSI = 100 × average gain / (average gain + average loss)",
    "RSI > 70 overbought, RSI < 30 oversold.",
    "📊 KDJ Stochastic Oscillator",
    "= (today's close - N-day low) / (N-day high - N-day low) × 100",
    "= 2/3 × prev K + 1/3 × RSV",
    "= 2/3 × prev D + 1/3 × K",
    "= 3K - 2D (J>100 overbought, J<0 oversold)",
    "MA(N) = sum of the last N closes / N; MACD: DIF = EMA(fast) - EMA(slow), DEA = EMA(DIF, 9), histogram = (DIF - DEA) × 2; RSI = 100 - 100 / (1 + avg gain / avg loss); KDJ: RSV = (C - L9)/(H9 - L9)×100, K/D recursively smoothed, J = 3K - 2D",
    "MA is the N-day average close; MACD takes the difference of fast and slow EMAs (DIF) and its 9-day EMA (DEA), with the histogram twice their difference; RSI uses average gain/loss to gauge overbought/oversold; KDJ first computes RSV then smooths K/D, and the J line amplifies signals.",
    "This tool only computes indicator values and does not constitute investment advice. Real trading needs a combined judgment of volume, patterns and other factors.",
    "📚 Deep Dive: Technical Indicators (MA/RSI/MACD)",
    "Compute common indicators such as moving averages (MA), relative strength (RSI) and MACD.",
    "Judgment of trend (MA long/short alignment), overbought/oversold (RSI) and momentum (MACD golden/death cross).",
    "Preliminary verification of multi-indicator combined signals.",
    "Average close of the last 20 days, e.g. [48,49,50,51,52…] mean = 50 → MA20 = 50. Price crossing above MA20 is often seen as short-term strengthening.",
    "RSI = 100 - 100/(1+RS), RS = 14-day average gain / average loss. RSI > 70 overbought, < 30 oversold. E.g. if gains exceed losses over 14 days RS = 2 → RSI = 100 - 100/3 ≈ 66.7 (strong but not overbought).",
    "DIF = EMA12 - EMA26; DEA = EMA(DIF, 9); MACD histogram = DIF - DEA. DIF crossing above DEA is a golden cross (bullish).",
    "Can indicators decide alone?",
    "No. Technical indicators lag and give false signals easily; combine multiple indicators + volume/price + fundamentals, and use strict stop-losses.",
    "How to choose parameters?",
    "Common MA: 5/10/20/60/250; RSI 14; MACD(12,26,9). Adjust by instrument and cycle; there is no universal parameter.",
    'About "Technical Indicator Calculator"',
    "Technical Indicator Calculator - MA/MACD/RSI/KDJ computation, an online securities technical-analysis tool, free to use. A professional financial calculator using standard formulas, with data processed locally and not leaked.",
    "How to Use the Technical Indicator Calculator",
    "What does the Technical Indicator Calculator do?",
    "Enter a closing-price series to compute moving average MA, MACD, RSI and KDJ, aiding trend and buy/sell signal judgment for technical analysis.",
    "How to use the Technical Indicator Calculator?",
    "Which scenarios is the Technical Indicator Calculator suitable for?",
    "e.g. 100,102,101,103,105,104,106,108,107,109",
]))

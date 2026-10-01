#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""securities 第2批：beta-calc / bond-convexity / bond-duration / book-to-market"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'securities')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'securities')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EXTRA = {
    'bond-convexity': {'到期收益率 YTM（%）': 'Yield to Maturity YTM (%)'},
    'bond-duration': {'百分比': 'percentage', '到期收益率 YTM（%）': 'Yield to Maturity YTM (%)'},
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


# ---------------- beta-calc (47) ----------------
write('beta-calc', build('beta-calc', [
    "🧮 Beta Coefficient Calculator",
    "Compute the Beta coefficient and correlation from stock and market return series",
    "/ Beta Coefficient Calculation",
    '📖 View the "Beta Coefficient Calculator User Guide"',
    "Stock return series (%, comma- or newline-separated)",
    "Market return series (%, comma- or newline-separated)",
    "Expected market return (%)",
    "🔢 Beta Formula",
    "where Cov is covariance, Var is variance, R",
    " is the stock return, R",
    " is the market return",
    "Correlation coefficient",
    "📊 CAPM Model",
    "Expected return",
    " is the risk-free rate, E(R",
    ") is the expected market return",
    "📈 Interpreting Beta",
    "Beta range",
    "Risk characteristics",
    "In sync",
    "Moves in step with the market",
    "Aggressive",
    "More volatile than the market, with larger gains and losses",
    "Defensive",
    "Less volatile than the market, relatively steady",
    "Unrelated",
    "Unrelated to market movements",
    "Inverse",
    "Moves inversely to the market (rare)",
    "Take the covariance of the stock and market return series and divide it by the variance of market returns; equivalently β = ρ(s,m)·σs / σm, measuring a stock's systematic risk relative to the market.",
    "The two series must be the same length; at least 12 periods of data are recommended for statistical reliability. Beta reflects systematic risk, not total risk.",
    "📚 Deep Dive: Beta Coefficient (Regression Method)",
    "Given period-by-period return series for a stock and the market, compute the stock's systematic-risk Beta relative to the market.",
    "Use it with CAPM to estimate a stock's expected return, or to judge whether it is aggressive or defensive.",
    "Before a multi-factor model, use the single-factor Beta for an initial risk stratification.",
    "Computing Beta from sample data",
    "Stock returns [1.5,-0.8,2.1,0.5,3.0,-1.5,0.8,1.9,-0.3,2.5]%, market returns [1.2,-1.0,1.8,0.3,2.6,-1.2,0.6,1.6,-0.5,2.2]%. Beta = cov(stock, market) / var(market). cov ≈ 0.00216, var(market) ≈ 0.00180 → Beta ≈ 1.20.",
    "CAPM expected return",
    "Risk-free 3%, expected market 8%, Beta = 1.20: E(R) = 3% + 1.20 × (8% − 3%) = 3% + 6% = 9%. Beta > 1 is aggressive (higher risk, higher return).",
    "What does Beta = 1.2 mean?",
    "When the market rises 1%, the stock has historically risen 1.2% on average; when it falls 1%, the stock falls 1.2% on average. A higher Beta means greater systematic risk, but not stock-specific risk (unsystematic risk is removed by diversification).",
    "What happens if the two series differ in length?",
    "This tool requires the stock and market returns to correspond one-to-one and to be the same length, otherwise it reports an error. Align the dates before computing.",
    'About "Beta Coefficient Calculator"',
    "Beta Coefficient Calculator - stock Beta calculation and a CAPM risk-measurement tool, free to use. A professional financial calculator that uses standard financial formulas and processes data locally without leaking it.",
    "e.g. 2.5,-1.2,3.1,0.8,...",
    "e.g. 1.5,-0.8,2.1,0.5,3.0,-1.5,0.8,1.9,-0.3,2.5,0.6,-1.0,2.0,0.2,2.6",
]))

# ---------------- bond-convexity (22) ----------------
write('bond-convexity', build('bond-convexity', [
    "🧮 Bond Convexity Calculator",
    "Convexity complements duration: duration measures the first-order slope of the price-yield relationship, while convexity captures its curvature. Enter the coupon rate, face value, YTM and years remaining to obtain the convexity value and compare it with the duration approximation error.",
    "/ Bond Convexity Calculator",
    '📖 View the "bond-convexity User Guide"',
    "P = Σ CFt / (1+y/f)^t; Macaulay D = (Σ t·PVt / P) / f; modified duration D* = Macaulay / (1+y/f); convexity = Σ PVt·t(t+1) / (P·(1+y/f)²·f²)",
    "First discount each period's coupon and the principal at maturity to obtain the bond price; Macaulay duration is the cash-flow-time-weighted average (converted from periods to years); convexity describes the second-order sensitivity of duration to interest rates, correcting the curvature of the price-yield curve.",
    "📚 Deep Dive: Bond Duration and Convexity",
    "Assess the second-order sensitivity of a bond price to interest rates (duration is first order, convexity corrects the curvature).",
    "When interest rates move a lot, a duration-only linear approximation has a large error and a convexity correction is needed.",
    "In an immunisation strategy (duration matching), compare the convexity of two bonds.",
    "5-year, 5% coupon, 5% YTM, face value 1000",
    "Macaulay duration ≈ 4.55 years, modified duration ≈ 4.33. Convexity C = Σ[t(t+1)·cf_t/(1+y)^(t+2)]/P ≈ 22.5. Rates +1%: price change ≈ −modified duration × 1% + 0.5 × convexity × 1%² = −4.33% + 0.0011 ≈ −4.33%.",
    "Is higher convexity always better?",
    "For the holder, higher convexity means a bigger price gain when rates fall and a smaller loss when they rise (positive convexity), which is favourable. But high-convexity bonds usually have a lower YTM.",
    "What is the relationship between duration and convexity?",
    "Duration is the first-order approximation (the price-yield slope) and convexity is the second-order correction (the curvature of the curve). For small rate changes duration is enough; for large changes the convexity term must be added.",
    "What is negative convexity?",
    "Callable bonds, MBS and other bonds with embedded options can show negative convexity - when rates fall the issuer exercises the option and the price gain is capped.",
    "Convexity = Σ(PV(Ct)·t·(t+1)) / (P·(1+y)²), the second-order term of the price-yield relationship",
    "ΔP/P ≈ −modified duration·Δy + ½·convexity·Δy²; the convexity term corrects the linear-approximation error of duration",
    "When rates rise, a bond with positive convexity falls less than the duration linear estimate; when rates fall, it rises more than the estimate",
    "This tool is a simplified model; results are for reference only and do not constitute investment advice",
]))

# ---------------- bond-duration (22) ----------------
write('bond-duration', build('bond-duration', [
    "🏦 Bond Duration Calculator",
    "Duration is the core measure of a bond's price sensitivity to interest rates. Enter the coupon rate, face value, yield to maturity and years remaining to obtain the Macaulay and modified duration, and estimate the effect of a rate change on price.",
    "/ Bond Duration Calculator",
    '📖 View the "bond-duration User Guide"',
    "Macaulay D = Σ t·PVt / P (periods) → years = D / f; modified duration D* = Macaulay / (1+y/f)",
    "Macaulay duration = the sum of each period's cash-flow present value multiplied by its time t, divided by the bond price; modified duration = Macaulay divided by (1 + per-period yield), expressing the price change for a 1% change in yield.",
    "📚 Deep Dive: Bond Duration (Macaulay / Modified)",
    "Measures the average time to recover a bond's cash flows, used to estimate interest-rate risk.",
    "Portfolio duration management (matching asset and liability durations, interest-rate immunisation).",
    "Compare the interest-rate sensitivity of bonds with different maturities and coupons.",
    "5-year, 5% coupon, 5% YTM, face value 1000",
    "Weighting each period's cash-flow present value: Macaulay duration = Σ[t·PV(cf_t)] / ΣPV(cf_t) ≈ 4.55 years. Modified duration = 4.55/(1+5%) ≈ 4.33. For every 1% rise in rates, the price falls about 4.33%.",
    "10-year zero-coupon bond",
    "For a zero-coupon bond, Macaulay duration = maturity = 10 years and modified duration = 10/1.05 ≈ 9.52. Rates +1% → price falls about 9.52%, far more sensitive than a coupon bond.",
    "Does longer duration mean more risk?",
    "Yes. Duration approximates the elasticity of price to interest rates; the longer the duration, the bigger the price swing for a rate move in either direction.",
    "What is the difference between Macaulay and modified duration?",
    "Macaulay duration is in units of time (years); modified duration = Macaulay/(1+y), directly giving, for a 1% change in yield, the price change as a ",
    "Macaulay duration = Σ(PV(Ct)×t) / P, the cash-flow-weighted average recovery time",
    "Modified duration = Macaulay duration (years) / (1 + per-period yield)",
    "ΔP/P ≈ −modified duration × Δy: duration measures interest-rate sensitivity",
    "This tool is a simplified model and does not include convexity; results are for reference only and do not constitute investment advice",
]))

# ---------------- book-to-market (19) ----------------
write('book-to-market', build('book-to-market', [
    "Compute the Book-to-Market Ratio from Book Value per Share and Price",
    "Enter the book value per share (BVPS) and the price P to obtain the book-to-market ratio.",
    "Book-to-Market Calculator",
    "/ Book-to-Market Calculator",
    '📖 View the "Compute the Book-to-Market Ratio from Book Value per Share and Price User Guide"',
    "Book value per share BVPS (CNY)",
    "The reciprocal of the price-to-book ratio; often high for value stocks.",
    "📚 Deep Dive: Book-to-Market Ratio (B/M)",
    "Value-investing screens (a low P/B = a high B/M, usually a value stock).",
    "Construction of HML (the value factor) in the Fama-French three-factor model.",
    "A rough indicator of whether a company is undervalued or overvalued.",
    "Net assets 1.0bn, market cap 2.5bn",
    "B/M = book value / market value = 10/25 = 0.40. B/M < 1 means the market value exceeds book value, implying stronger growth expectations; value stocks usually have a B/M close to or above 1.",
    "Net assets 0.8bn, market cap 0.6bn",
    "B/M = 8/6 ≈ 1.33. B/M > 1 means the market value is below net assets, leaning deep value (watch out for asset-quality traps).",
    "How are B/M and P/B related?",
    "They are reciprocals: P/B = 1/(B/M). P/B < 1 ⇔ B/M > 1 (market value below book value).",
    "Does a high B/M always mean cheap?",
    'Not necessarily. Book value may include goodwill or inventory-impairment risk, or the industry may have declined. Judge it together with ROE and asset quality to avoid a "value trap".',
]))

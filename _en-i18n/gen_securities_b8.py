#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""securities 第8批：peg-ratio / price-to-book / tracking-error / ytm-approx"""
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


# ---------------- peg-ratio (20) ----------------
write('peg-ratio', build('peg-ratio', [
    "Compute PEG from the P/E ratio and earnings growth rate",
    "Enter the P/E ratio and earnings growth rate g (percent) to compute PEG.",
    "PEG Valuation Metric Calculator",
    "/ PEG Valuation Metric Calculator",
    '📖 View the "Compute PEG from the P/E ratio and earnings growth rate User Guide"',
    "P/E ratio PE",
    "Growth rate g (%)",
    "PEG < 1 is often considered undervalued.",
    "📚 Deep Dive: PEG Ratio",
    "P/E divided by earnings growth rate, correcting the high P/E of high-growth stocks.",
    "Cross-comparison of growth stocks vs value stocks.",
    'PEG < 1 is often seen as "growth not fully priced in".',
    "PE=20, growth rate 15%",
    "PEG = PE/growth = 20/15 ≈ 1.33. If PE=30, growth 30%: PEG=1.0 (same PEG but higher growth).",
    "PE=15, growth 20%: PEG=15/20=0.75. Relative to growth, valuation is low (verify growth sustainability).",
    "Which growth rate to use?",
    "Usually the next 3-5 years'",
    "expected compound growth rate, or historical growth, but it must be consistent. The denominator unit must match the P/E (both in % or both in decimals).",
    "Is a lower PEG always better?",
    "Not necessarily. A low PEG may reflect unsustainable growth or high risk (e.g. a cyclical peak). PEG is only a growth correction to P/E, not a panacea.",
]))

# ---------------- price-to-book (22) ----------------
write('price-to-book', build('price-to-book', [
    "Share Price / Book Value per Share",
    "P/B = share price / BVPS.",
    "Price-to-Book Ratio",
    "/ Price-to-Book Ratio (P/B)",
    "Price-to-Book Ratio (P/B)",
    '📖 View the "Share Price / Book Value per Share User Guide"',
    "P/B = share price / book value per share",
    "Book value per share (yuan)",
    "P/B < 1 may be undervalued (need to combine with asset quality).",
    "Commonly used in asset-heavy industries.",
    "📚 Deep Dive: Price-to-Book Ratio (P/B)",
    "Share price divided by net assets per share, measuring the premium of market value over book value.",
    "Commonly used in banks/asset-heavy industries (assets are measurable).",
    "Stock picking below book (P/B < 1) and value-trap identification.",
    "Share price 30, BVPS 5",
    "P/B = 30/5 = 6. That is, market value is 6x the net assets per share.",
    "Below book",
    "Share price 4, BVPS 5: P/B = 4/5 = 0.8 < 1, market value below book (below book), need to check whether asset quality hides landmines.",
    "Which industries is P/B suitable for?",
    "Asset-heavy, reliably measurable assets (banks, real estate, steel) fit; light-asset/tech stocks have many intangibles and P/B is distorted.",
    "Is P/B < 1 always cheap?",
    "Not necessarily. It may have high impairment risk and low ROE. Combine with ROE: low P/B but also low ROE is not necessarily undervalued.",
]))

# ---------------- tracking-error (20) ----------------
write('tracking-error', build('tracking-error', [
    "Compute tracking error from an active-return series",
    "Enter the series of excess returns over the benchmark (comma- or space-separated) to compute tracking error.",
    "Tracking Error Calculator",
    "/ Tracking Error Calculator",
    '📖 View the "Compute tracking error from an active-return series User Guide"',
    "The smaller the TE, the closer to the benchmark.",
    "Sample series -> about 0.589%.",
    "📚 Deep Dive: Tracking Error (TE)",
    "The portfolio's active return (relative to benchmark)",
    ", measuring the degree of deviation from the benchmark.",
    "Index funds/passive products require small TE (tight tracking).",
    "Large TE in active funds means more deviation (style aggressiveness).",
    "Active returns [1,2,-1,3,0]%",
    "Mean=1%; variance=((0)²+(1)²+(−2)²+(2)²+(−1)²)/5=(0+1+4+4+1)/5=2; TE=√2≈1.41%.",
    "Tracks the benchmark",
    "Active returns [0.1,−0.1,0.2,0,−0.2]%: mean ≈ 0, TE ≈ 0.16%, almost perfectly tracked.",
    "Is smaller TE always better?",
    'Passive products: smaller is better (tight tracking); active products with small TE are "pseudo-active" (charging active fees yet no deviation), so combine with IR to see if it is worth the money.',
    "What is the relationship between TE and IR?",
    "IR = mean active return / TE. With the same excess, smaller TE gives higher IR (more stable excess).",
]))

# ---------------- ytm-approx (21) ----------------
write('ytm-approx', build('ytm-approx', [
    "Bond Yield Estimation",
    "YTM Approximation",
    "/ Bond Yield to Maturity (Approx)",
    "Bond Yield to Maturity (Approx)",
    '📖 View the "Bond Yield Estimation User Guide"',
    "Current price P (yuan)",
    "Remaining years",
    "The approximation formula fits bonds near par.",
    "Precise YTM requires iterative solving.",
    "📚 Deep Dive: Yield to Maturity Approximation (YTM)",
    "Quickly estimate a bond's YTM with the approximation formula (coupon + amortized discount/premium, divided by average price).",
    "Cross-check against the precise YTM (trial-and-error / Newton's method).",
    "Quick price comparison when screening bonds.",
    "Coupon 5%, face 1000, price 950, 10 years left",
    "Annual coupon = 1000 × 5% = 50; YTM ≈ (50+(1000−950)/10)/((1000+950)/2) = (50+5)/975 = 55/975 ≈ 5.64%. The precise value is about 5.7%; the approximation error is tiny.",
    "Premium bond",
    "Price 1050: YTM ≈ (50+(1000−1050)/10)/1025 = (50−5)/1025 = 45/1025 ≈ 4.39% (below the coupon, due to premium purchase).",
    "The approximation formula and units?",
    "YTM ≈ (annual coupon + (face - price)/years left) / ((face + price)/2), annualized. Difference from precise YTM is usually < 0.1%.",
    "Zero-coupon bond YTM?",
    "A zero-coupon bond has no coupon; YTM ≈ ((face/price)^(1/years) - 1), using the compound formula; the above approximation cannot be used (no coupon in the numerator).",
]))

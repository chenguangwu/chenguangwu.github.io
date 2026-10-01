#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""insurance 第2批：claim-frequency / claim-reserve / combined-ratio / complete-life-expectancy / endowment-premium"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'insurance')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'insurance')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        for i, it in enumerate(items):
            print('   ', i, repr((it.get('zh') or it.get('zh_src', ''))[:50]))
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
    out = {'slug': slug, 'industry': 'insurance', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))


# ---------------- claim-frequency (20) ----------------
write('claim-frequency', build('claim-frequency', [
    "Claim count per unit of risk exposure",
    "Claim frequency = claim count ÷ exposure units.",
    "Claim Frequency",
    "/ Claim Frequency Calculator",
    "Claim Frequency Calculator",
    '\U0001F4D6 View the "Claim Count per Unit of Risk Exposure User Guide"',
    "Claim frequency = claims / exposure",
    "Claim count",
    "Exposure (car-years)",
    "Frequency = claim count / exposure units.",
    "Commonly used as a basis for auto-insurance pricing.",
    "\U0001F4DA Deep Dive: Claim Frequency (per Unit of Risk Exposure)",
    "Compute occurrence density and combine with severity for expected loss.",
    "Compare claim frequency across lines of business or years.",
    "120 claims among 1000 risks",
    "Claim frequency = 120/1000 = 0.12 claims/risk-year. That is, each risk incurs claims 0.12 times per year on average.",
    "How to define the exposure unit?",
    "It can be policy count, car-years, person-years, etc. The basis must be consistent to compare; different exposure definitions make frequencies incomparable.",
    "Can frequency and probability be interchanged?",
    "No. Frequency is the expected count per exposure period (can exceed 1); probability is the proportion of a single event (≤1). Auto uses per-car-year frequency; health uses per-person-year incidence.",
]))

# ---------------- claim-reserve (47) ----------------
write('claim-reserve', build('claim-reserve', [
    "\U0001F9EE Claims Reserve Calculator",
    "Estimate unpaid-claim reserves (RBNS + IBNR), with loss-ratio and chain-ladder methods compared.",
    "/ Claims Reserve",
    '\U0001F4D6 View the "Claims Reserve Calculator User Guide"',
    "Reserve = ultimate loss − paid loss",
    "Current earned premium (10k ¥)",
    "Expected ultimate loss ratio (%)",
    "Paid claims (10k ¥)",
    "Reported-but-not-settled RBNS (10k ¥)",
    "Settled-claim closure rate (%)",
    "Development period (years)",
    "1 year (fast development)",
    "2 years (typical)",
    "3 years (long-tail line)",
    "4 years (long-tail line)",
    "5 years and above",
    "\U0001F522 Loss-Ratio Method (IBNR Estimate)",
    "Expected ultimate loss",
    "= current earned premium × expected loss ratio",
    "= expected ultimate loss − paid claims − RBNS",
    "Unpaid-claim reserve",
    "\U0001F4E8 Chain-Ladder Method (Reference)",
    "Ultimate loss estimate",
    "= paid claims ÷ closure rate",
    "Unpaid reserve",
    "= ultimate loss estimate − paid claims",
    "The development factor here adjusts for long-tail-line uncertainty.",
    "\U0001F4DA Concept Notes",
    "(RBNS): claims that have occurred and been reported but are not yet settled",
    "(IBNR): claims that have occurred but not yet reported to the insurer",
    "Earned premium",
    ": premium income attributable to the elapsed part of the policy period",
    "Loss ratio",
    ": claims as a share of premium, reflecting business quality",
    "The two methods may differ; in practice they are considered together. This tool is a simplified model for learning reference only.",
    "\U0001F4DA Deep Dive: Claims Reserve Calculator",
    "For reported-unsettled claims, book a reserve as ultimate loss minus paid.",
    "Assess claims progress and see how much remains unpaid.",
    "Ultimate 10M, paid 3.5M",
    "Reserve = 10M − 3.5M = 6.5M. That is, this line still needs 6.5M of unpaid-claim reserve booked.",
    "How to estimate ultimate loss?",
    "Use the reported-development-factor or chain-ladder method to extrapolate. A low paid ratio means claims are early, so the reserve is volatile.",
    "How to split reported and unreported reserves?",
    "Reported-unsettled (case reserve) is assessed per case; unreported (IBNR) by runoff",
    "and development factors. The two together equal ultimate loss minus paid.",
    'About "Claims Reserve Calculator"',
    "Claims reserve calculator — unpaid-claim reserve estimation, an online actuarial tool, free to use. A professional financial tool using standard formulas; data is processed locally and not leaked.",
]))

# ---------------- combined-ratio (19) ----------------
write('combined-ratio', build('combined-ratio', [
    "Core metric for underwriting profit/loss",
    "Combined ratio = loss ratio + expense ratio.",
    "/ Combined Ratio Calculator",
    "Combined Ratio Calculator",
    '\U0001F4D6 View the "Core Metric for Underwriting Profit/Loss User Guide"',
    "Combined ratio = (claims + expenses) / premium × 100%",
    "Combined ratio < 100% means an underwriting profit.",
    "With investment income, the overall result can still be profitable.",
    "\U0001F4DA Deep Dive: Combined Ratio (Underwriting Core Metric)",
    "See if the underwriting side makes money: <100% underwriting profit, >100% underwriting loss covered by investment income.",
    "Compare combined ratios across lines of business or years.",
    "Claims 6.5M, expenses 2.5M, premium 10M",
    "Combined ratio = (650+250)/1000×100% = 90%. <100% underwriting profit,",
    "underwriting profit",
    "rate 10%.",
    "Does 90% guarantee profit?",
    "Only a 10% underwriting profit; you must also look at investment income. If investment income cannot cover the expense overrun, the overall result can still be a loss.",
    "Does a combined ratio below 100% mean real profit?",
    "It only means underwriting profit, excluding investment income. Insurance profit = underwriting profit + investment income; even at CR=98% in a low-rate environment, investment income can fill the gap or do better.",
]))

# ---------------- complete-life-expectancy (16) ----------------
write('complete-life-expectancy', build('complete-life-expectancy', [
    "Complete life expectancy from yearly survival-probability sequence",
    "Enter a yearly survival-probability sequence (comma or space separated) to find life expectancy.",
    "Complete Life Expectancy Calculator",
    "/ Complete Life Expectancy Calculator",
    '\U0001F4D6 View the "Complete Life Expectancy from Yearly Survival Sequence User Guide"',
    "Survival-probability sequence ₜpₓ",
    "Approximated by summing survival probabilities.",
    "\U0001F4DA Deep Dive: Complete Life Expectancy (Sum of Yearly Survival Probabilities)",
    "From a set of yearly survival probabilities ₜpₓ, compute the complete life expectancy eₓ.",
    "Validate mortality assumptions for population or pension actuarial work.",
    "Sequence 0.95,0.9,0.85,0.8,0.75",
    "eₓ = 1×0.95+2×0.9+3×0.85+4×0.8+5×0.75 = 0.95+1.8+2.55+3.2+3.75 = 12.25 years.",
    "Difference between complete and curtate expectancy?",
    "Complete eₓ weights and sums ₜpₓ directly; the common curtate expectancy eₓ° = Σₜ₌₁^ω ₜpₓ ≈ eₓ − 0.5.",
    "Why sum survival probabilities instead of looking up mean residual life directly?",
    "Complete life expectancy also counts the within-year survival segment (continuous), running about 0.5 year longer than the discrete curtate; actuarial reserves and annuity pricing must use the complete expectancy for precision.",
]))

# ---------------- endowment-premium (19) ----------------
write('endowment-premium', build('endowment-premium', [
    "Death-benefit and maturity-benefit combination",
    "Endowment insurance = term life + PV of maturity survival benefit.",
    "Endowment Premium",
    "/ Endowment Premium Calculator",
    "Endowment Premium Calculator",
    '\U0001F4D6 View the "Death-Benefit and Maturity-Benefit Combination User Guide"',
    "Endowment premium = death PV + maturity PV",
    "Policy years",
    "Endowment = PV of death benefit + PV of survival benefit.",
    "Then divide the level premium by the annuity PV factor.",
    "\U0001F4DA Deep Dive: Endowment Premium (Death + Maturity)",
    "Death protection + maturity return combined, each discounted then summed into the annual premium.",
    "Compare premium gaps between pure protection and endowment.",
    "Sum assured 1M, 3%, 20 years",
    "Death PV = 1M×A₁ₙ(3%,20) ≈ 1M×0.1488 = 148.8k; maturity PV = 1M×v²⁰ = 1M×0.5537 = 553.7k; endowment PV ≈ 702.5k, spread to about 47k/year.",
    "Why is endowment pricier than term?",
    "The certain maturity return (a guaranteed cash flow) raises the PV, and death protection adds a layer, so the premium exceeds pure-death term insurance.",
    "Is the endowment maturity return a free gain?",
    "No. The maturity sum is the policyholder's own savings returned; the survival-benefit portion accrues at the valuation rate — it is just term insurance bundled with a savings plan, and the total cost is not below the sum of the two.",
]))

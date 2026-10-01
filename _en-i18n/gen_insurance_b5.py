#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""insurance 第5批：mortality-table / net-single-premium / premium-calc / premium-elasticity / pure-premium-rate"""
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


# ---------------- mortality-table (41) ----------------
write('mortality-table', build('mortality-table', [
    "\U0001F4DA Life Table Lookup",
    "Look up mortality rate (qx), survivors (lx) and remaining life expectancy by age - a simplified actuarial life table",
    '\U0001F4D6 View the "Life Table Lookup User Guide"',
    "Deaths at age x = lx \u00d7 qx",
    "Query age",
    "\U0001F4CA Simplified Life Table (excerpt)",
    "Click a header to switch sex; below are actuarial reference values at 10-year intervals",
    "qx male",
    "qx female",
    "lx male",
    "lx female",
    "ex male",
    "ex female",
    "\U0001F4DA Field descriptions",
    "\U0001F522 Life-table symbols",
    ": age",
    ": probability of death at age x (death before age x+1 given survival to age x)",
    ": survival probability at age x = 1 - qx",
    ": number surviving to age x (out of a base of 100,000)",
    ": deaths at age x = lx \u00d7 qx",
    ": remaining life expectancy at age x (average years still to live)",
    "\U0001F4D6 Application scenarios",
    "Life insurance pricing",
    ": compute actuarial present value of death benefits",
    "Annuity pricing",
    ": estimate payment periods of survival annuities",
    "Reserve valuation",
    ": set aside life insurance reserves",
    "Demographics",
    ": analyze population structure and aging",
    "This is a simplified teaching life table with approximate reference values. Actual actuarial work should use the official life table published by the regulator (e.g. CL2003-2013).",
    "\U0001F4DA Deep Dive: Life Table Lookup (Deaths = lx\u00d7qx)",
    "Look up survivors lx and mortality qx at age x, then compute deaths at that age.",
    "Build survival / death distributions for pensions or life insurance.",
    "Deaths at age x = 97000\u00d70.0008 = 77.6 \u2248 78. That is, about 78 people in that cohort die that year.",
    "Where do lx and qx come from?",
    "From experience or industry tables (e.g. CL tables). Male/female tables differ; pick one matching the insured.",
    "How to choose between experience and select tables?",
    "Experience tables reflect actual mortality of the insured (usually below the national table); select tables additionally capture the healthier selection effect in early policy years. Pricing with select tables fits real risk better.",
    'About "Life Table Lookup"',
    "Life Table Lookup - a simplified life table to query mortality, survival and life expectancy by age, free to use. A professional financial calculator using standard formulas, with data processed locally and not leaked.",
]))

# ---------------- net-single-premium (18) ----------------
write('net-single-premium', build('net-single-premium', [
    "Pure premium paid in one lump sum",
    "Under given mortality and interest, the present value of death benefits is the net single premium.",
    "Net single premium (NSP)",
    "/ Net Single Premium Calculator",
    "Net Single Premium Calculator",
    '\U0001F4D6 View the "Pure Premium Paid in One Lump Sum User Guide"',
    "NSP = \u03a3 benefit_t/(1+i)^t",
    "NSP is the expected value of future death benefits discounted at the interest rate.",
    "A simplifying assumption is equal mortality each year.",
    "\U0001F4DA Deep Dive: Net Single Premium (Lump-Sum Pure Premium)",
    "Discount future yearly benefits at the assumed interest rate and sum them to get the net single premium.",
    "Compare net single premiums under different assumed interest rates.",
    "Annual benefit 1M, 3%, 10 years",
    "NSP = \u03a3 1M/(1.03)^t (t=1..10) = 1M\u00d7\u00e4\u2081\u2080@3% (\u22488.530) \u2248 8.53M. That is, the net single premium is about 8.53M.",
    "Does the net single premium include expenses?",
    "No. It is the pure risk present value; the gross premium also multiplies by (1+loading rate) and considers the payment mode.",
    "How much does the net single premium differ from the single premium?",
    "The net single premium equals the pure-risk present value; the single premium equals net single plus expense loading (one-time). Healthy-life single premium is usually 15-30% above the installment net-single present value; the gap is expense and profit margin.",
]))

# ---------------- premium-calc (52) ----------------
write('premium-calc', build('premium-calc', [
    "\U0001F6E1\uFE0F Premium Calculator",
    "A base premium rate model that estimates premium from sum assured, rate and risk coefficients",
    '\U0001F4D6 View the "Premium Calculator User Guide"',
    "Premium = sum assured \u00d7 rate",
    "Sum assured (\u00a5)",
    "Base rate (\u2030)",
    "Age 0-17",
    "Age 18-30",
    "Age 31-40",
    "Age 41-50",
    "Age 51-60",
    "Age 61-70",
    "Occupation class",
    "Class 1 (office work)",
    "Class 2 (light physical)",
    "Class 3 (field service)",
    "Class 4 (semi-physical)",
    "Class 5 (heavy physical)",
    "Class 6 (high risk)",
    "Payment term",
    "1 year (short term)",
    "Payment mode",
    "Annual",
    "Semi-annual",
    "Quarterly",
    "Monthly",
    "Single (lump sum)",
    "\U0001F522 Calculation formula",
    "Base premium",
    "= sum assured \u00d7 rate \u00f7 1000",
    "Actual premium",
    "= base premium \u00d7 age factor \u00d7 occupation factor \u00d7 term factor \u00d7 payment-mode factor",
    "\U0001F4CA Age-factor reference table",
    "Risk note",
    "Minor, lower risk",
    "Youth, base factor",
    "Prime age, risk slightly up",
    "Middle age, health risk rising",
    "Older middle age, higher risk",
    "Elderly, risk significantly up",
    "This tool is for premium estimation only; actual premium is subject to the insurer's underwriting. Rates and coefficients vary widely by product and company.",
    "\U0001F4DA Deep Dive: Premium Calculator (Sum Assured \u00d7 Rate)",
    "Given sum assured and rate, compute premium directly for a quick quote.",
    "Stack the extra coefficients to see the final premium.",
    "Sum assured 500k, base rate 2.5\u2030",
    "Premium = 500000\u00d70.0025 = 1250 \u00a5. After multiplying the extra coefficient (e.g. 1.3) the result is about 1625 \u00a5.",
    "What does a 2.5\u2030 rate mean?",
    "It charges 2.5 \u00a5 per 1000 \u00a5 of cover. 500k cover is 500 per-mille units \u00d72.5 = 1250 \u00a5.",
    "What adjusts the rate?",
    "The base rate is loaded/unloaded by age, sex, occupation, health disclosure, deductible and cover tier (underwriting coefficients); high-risk groups can pay several times the base, not a simple cover \u00d7 fixed rate.",
    'About "Premium Calculator"',
    "Premium Calculator - a base premium rate model, an online insurance premium estimator, free to use. A professional financial calculator using standard formulas, with data processed locally and not leaked.",
]))

# ---------------- premium-elasticity (19) ----------------
write('premium-elasticity', build('premium-elasticity', [
    "Elasticity from demand and premium change rates",
    "Enter the change rates of demand and premium to find demand elasticity.",
    "Elasticity = (%\u0394 demand) / (%\u0394 premium)",
    "/ Premium Demand Elasticity Calculator",
    "Premium Demand Elasticity Calculator",
    '\U0001F4D6 View the "Elasticity from Demand and Premium Change Rates User Guide"',
    "Elasticity = (\u0394 demand/demand) / (\u0394 premium/premium)",
    "Demand change rate",
    "Premium change rate",
    "Elasticity < 1 means inelastic (a necessity).",
    "\U0001F4DA Deep Dive: Premium Demand Elasticity",
    "See how much demand drops when premium rises 1%, to judge room for a price hike.",
    "Do sensitivity analysis for pricing strategy.",
    "Demand down 10%, premium up 20%",
    "Elasticity = (-10%)/(+20%) = -0.5. Absolute value < 1 means inelastic, so a price hike raises total premium.",
    "How to read the negative sign of elasticity?",
    "Demand and premium move opposite, so elasticity is negative; read the absolute value. |E|<1 allows a price hike to raise revenue; |E|>1 should cut price for volume.",
    "Is high elasticity good for insurers?",
    "Neutral but risky. High elasticity means price-sensitive, easily churned customers; a small hike loses volume, but a cut also gains volume fast. Pricing must find the profit-maximizing point between price and volume, not just hike.",
]))

# ---------------- pure-premium-rate (20) ----------------
write('pure-premium-rate', build('pure-premium-rate', [
    "Pure rate from expected loss and exposure units",
    "Enter expected loss and number of risk exposure units to find the pure rate.",
    "Pure rate = expected loss / risk exposure",
    "/ Pure Rate Calculator",
    "Pure Rate Calculator",
    '\U0001F4D6 View the "Pure Rate from Expected Loss and Exposure Units User Guide"',
    "Pure rate = expected loss / exposure unit",
    "Expected loss (\u00a5)",
    "Risk exposure (units)",
    "The pure rate is the basis of risk consideration.",
    "1000/100 \u2192 10 \u00a5/unit.",
    "\U0001F4DA Deep Dive: Pure Rate (Expected Loss / Exposure Unit)",
    "Divide expected loss by exposure units to get the per-unit pure rate.",
    "It is the bottom-layer basis for rate making.",
    "Expected loss 1000, exposure 100 units",
    "Pure rate = 1000/100 = 10/unit. That is, pure premium is 10 \u00a5 per exposure unit.",
    "Difference between pure and gross rate?",
    "Pure rate covers only expected loss; gross rate = pure rate \u00d7 (1+loading rate), plus expense, profit and safety margin.",
    "Can the pure rate be quoted externally?",
    "No. The pure rate is the per-unit risk cost; external quotes add a loading rate (expense + profit + tax) on top to get the gross rate; the pure rate is only the pricing starting point.",
]))

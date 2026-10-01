#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""insurance 第3批：expected-claim-loss / expense-ratio / force-of-mortality / gross-premium-loading / ibnr-estimate"""
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


# ---------------- expected-claim-loss (21) ----------------
write('expected-claim-loss', build('expected-claim-loss', [
    "Expected loss from claim frequency and average severity",
    "Enter the per-risk claim frequency and average severity to find the expected loss cost.",
    "ECL = claim frequency × average severity",
    "/ Expected Claim Loss Calculator",
    "Expected Claim Loss Calculator",
    '\U0001F4D6 View the "Expected Loss from Claim Frequency and Average Severity User Guide"',
    "Claim frequency",
    "Frequency × severity is the pure-premium basis.",
    "0.05×20000 → 1000 ¥.",
    "\U0001F4DA Deep Dive: Expected Loss (Frequency × Severity)",
    "Pure-premium basis for pricing: expected claim per risk = occurrence rate × average severity.",
    "For a line of business",
    "at break-even",
    "pure risk cost.",
    "Frequency 5%, average severity 20k",
    "Expected loss = 0.05×20000 = 1000 ¥/risk-year. That is, the pure risk cost is about 1000 ¥.",
    "Is this only the pure premium?",
    "It is the pure premium (risk cost), before expenses, profit and safety margin; the gross premium still multiplies by (1 + loading rate).",
    "Should expected loss include a safety margin?",
    "Pure premium equals expected loss, but actual pricing also adds a risk margin (for volatility) and expense loading. Pricing directly on expected loss will be underwater in bad years, so you need to add a",
    "multiple.",
]))

# ---------------- expense-ratio (22) ----------------
write('expense-ratio', build('expense-ratio', [
    "Ratio of operating expenses to premium",
    "Expense ratio = operating expenses ÷ premium income.",
    "Expense Ratio",
    "/ Expense Ratio Calculator",
    "Expense Ratio Calculator",
    '\U0001F4D6 View the "Ratio of Operating Expenses to Premium User Guide"',
    "Expense ratio = operating expenses / premium",
    "Expense ratio = expenses / premium.",
    "Added to the loss ratio it gives the combined ratio.",
    "\U0001F4DA Deep Dive: Expense Ratio (Operating Expenses / Premium)",
    "See how much of premium is consumed by expenses and assess efficiency.",
    "With the",
    "loss ratio, judge underwriting profit.",
    "Expenses 2.5M, premium 10M",
    "Expense ratio = 250/1000 = 25%. That is, 0.25 of every premium yuan goes to operating expenses.",
    "What expense ratio is healthy?",
    "It differs for life / non-life; generally",
    "underwriting profit",
    "requires expense ratio +",
    " < 100%. 25% is in the common range, but must be read with the loss ratio.",
    "What is the relation between expense ratio and combined ratio?",
    "The expense ratio is a component of the combined ratio (loss ratio + expense ratio = combined ratio). A persistently >20% expense ratio usually squeezes underwriting profit and needs scale or digitalization to cut cost.",
]))

# ---------------- force-of-mortality (15) ----------------
write('force-of-mortality', build('force-of-mortality', [
    "Force of mortality from one-year survival probability",
    "Enter the one-year survival probability p_x to find the force of mortality μ.",
    "Force of Mortality (Central Death Rate) Calculator",
    "/ Force of Mortality (Central Death Rate) Calculator",
    '\U0001F4D6 View the "Force of Mortality from One-Year Survival Probability User Guide"',
    "Survival probability p_x",
    "The force of mortality is the instantaneous death rate.",
    "\U0001F4DA Deep Dive: Force of Mortality (from One-Year Survival Probability)",
    "Convert the yearly survival probability pₓ to the continuous force of mortality μₓ for modeling.",
    "Smooth and compare mortality-rate curves.",
    "μₓ = −ln(0.99) ≈ 0.01005. That is, the continuous force of mortality at that age is about 1.0%.",
    "Relation between force of mortality and q?",
    "qₓ = 1−pₓ = 1−e^−μ ≈ μ (approximately equal when μ is small); exactly q = 1−e^−μ.",
    "Is a negative force of mortality meaningful?",
    "No. The force μ comes from the negative log of p; since p (yearly survival) is between 0 and 1, μ is never negative. A negative result means the input p exceeds 1 — check the data.",
]))

# ---------------- gross-premium-loading (20) ----------------
write('gross-premium-loading', build('gross-premium-loading', [
    "Gross premium from net premium and loading rate",
    "Enter the net premium and loading rate to find the gross premium.",
    "Gross premium = net premium × (1 + loading rate)",
    "/ Gross Premium Loading Calculator",
    "Gross Premium Loading Calculator",
    '\U0001F4D6 View the "Gross Premium from Net Premium and Loading Rate User Guide"',
    "Gross premium = net premium × (1 + loading rate)",
    "Net premium (¥)",
    "Loading rate",
    "Loading covers expenses and profit.",
    "10×1.4 → 14 ¥.",
    "\U0001F4DA Deep Dive: Gross Premium (Net Premium × Loading Rate)",
    "Net premium plus expenses, profit and safety margin gives the gross premium.",
    "Adjust the loading rate to see the premium increase.",
    "Net premium 10, loading 40%",
    "Gross premium = 10×(1+0.4) = 14. That is, the gross premium per risk unit is 14, of which 4 is loading for expenses and profit.",
    "What does the loading rate include?",
    "Expenses (acquisition + maintenance), expected profit, and risk safety margin. 40% is a common range but varies greatly by channel.",
    "Is a 40% loading rate high?",
    "On the high side. The loading includes commission (often 20%–40% first year), operations, tax, profit and safety margin; long-term protection products usually carry 15%–30%, while unit-linked or online sales can be lower.",
]))

# ---------------- ibnr-estimate (20) ----------------
write('ibnr-estimate', build('ibnr-estimate', [
    "IBNR estimate from ultimate loss and paid ratio",
    "Enter the ultimate loss and paid ratio to find the IBNR reserve.",
    "IBNR = ultimate loss × (1 − paid ratio)",
    "/ IBNR Reserve Estimator",
    "IBNR Reserve Estimator",
    '\U0001F4D6 View the "IBNR Estimate from Ultimate Loss and Paid Ratio User Guide"',
    "IBNR = ultimate loss × (1 − paid ratio)",
    "Ultimate loss (¥)",
    "Paid ratio",
    "IBNR is incurred-but-not-reported claims.",
    "100k×(1−0.7) → 30k ¥.",
    "\U0001F4DA Deep Dive: IBNR Estimation (Ultimate × Unpaid Ratio)",
    "Estimate the IBNR reserve as ultimate loss times the unpaid ratio.",
    "Quickly check reserve adequacy.",
    "Ultimate 100k, paid 70%",
    "IBNR = 100000×(1−0.7) = 30000. That is, about 30k remains to occur / unreported.",
    "What does a high paid ratio indicate?",
    "Paid 70% means claims are mature, with only 30% IBNR left; early-stage business with low paid has a large IBNR share and high uncertainty.",
    "Does estimating IBNR by paid ratio understate it?",
    "Yes. A high paid ratio only means money is paid fast; unreported claims (reporting lag) may still be substantial. A safer approach uses the reported ratio or chain-ladder to estimate both IBNR and reported-unpaid together.",
]))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""insurance 第4批：ibnr-reserve / level-premium-life / life-cover-need / loss-ratio / mortality-prob"""
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


# ---------------- ibnr-reserve (20) ----------------
write('ibnr-reserve', build('ibnr-reserve', [
    "Incurred but not reported claims (IBNR)",
    "IBNR is commonly estimated by multiplying reported claims by a development factor.",
    "IBNR Reserve",
    "/ IBNR Reserve Estimation",
    "IBNR Reserve Estimation",
    '\U0001F4D6 View the "Incurred but Not Reported Claims User Guide"',
    "IBNR = incurred losses - reported losses",
    "Reported claims (\u00a5)",
    "Development factor",
    "IBNR \u2248 reported \u00d7 (development factor - 1).",
    "The development factor is set from historical loss-development experience.",
    "\U0001F4DA Deep Dive: Incurred but Not Reported Claims (IBNR)",
    "Estimating IBNR as incurred minus reported is a major part of reserves.",
    "See how reporting lag drives the reserve.",
    "Incurred 4M, reported 3.2M",
    "IBNR = 400-320 = 0.8M. That is, incurred but not reported claims are about 0.8M.",
    "What is the difference between incurred and reported?",
    "Incurred = all claims on the books (including unreported); reported = those already filed. The gap is IBNR, reflecting reporting lag.",
    "Why is IBNR especially large for long-tail business?",
    "For liability and medical lines claims take long to develop; accidents occur but are reported years later (reporting lag), so IBNR can reach 30-60% of ultimate claims; under-estimating it badly understates liabilities.",
]))

# ---------------- level-premium-life (19) ----------------
write('level-premium-life', build('level-premium-life', [
    "Spread a single-premium into annual payments",
    "Level annual premium = net single premium \u00f7 annuity present-value factor.",
    "Level annual premium",
    "/ Level Annual Premium Calculator",
    "Level Annual Premium Calculator",
    '\U0001F4D6 View the "Spread Single Premium into Annual Payments User Guide"',
    "Annual premium = single premium /\u00e4\u2099",
    "Net single premium (\u00a5)",
    "Payment term (years)",
    "Annual premium falls as interest rate rises.",
    "\U0001F4DA Deep Dive: Level Annual Premium (Single-Premium Amortization)",
    "Amortize a one-time net single premium into equal annual payments.",
    "Compare annual payments under different payment terms.",
    "Single premium 85k, 3%, 20 years",
    "Annual premium = 85000/\u00e4\u2082\u2080@3% (\u224814.877) \u2248 5713 \u00a5/year. That is, about 5713 \u00a5 paid each year.",
    "Why divide by the annuity factor?",
    "Single premium is a present value, annual is an annuity stream; present value / annuity factor spreads it evenly per year, ensuring actuarial equivalence.",
    "Why does level premium lose money early?",
    "Level premium spreads the single-premium present value across years; early premiums exceed the year's risk cost, and the surplus builds reserves (front-loaded surplus) to cover later shortfalls - this is the essence of life-insurance cash-flow design.",
]))

# ---------------- life-cover-need (21) ----------------
write('life-cover-need', build('life-cover-need', [
    "Estimate required life cover by the income-replacement method",
    "Estimate a family's required life cover from income replacement and liabilities.",
    "Life cover need",
    "/ Life Cover Need Calculator",
    "Life Cover Need Calculator",
    '\U0001F4D6 View the "Estimate Life Cover by Income-Replacement Method User Guide"',
    "Life cover = annual income gap \u00d7 discount annuity factor",
    "Annual income (\u00a5)",
    "Existing liabilities (\u00a5)",
    "Usable assets (\u00a5)",
    "Cover = annual income \u00d7 coverage years + liabilities - assets.",
    "This is only a rough estimate; actual need should reflect the family structure.",
    "\U0001F4DA Deep Dive: Life Cover Need (Income-Replacement Method)",
    "Use the family's annual income gap \u00d7 discount annuity factor to estimate required cover.",
    "Diagnose cover adequacy for the family breadwinner.",
    "Annual income gap 300k, cover 10 years",
    "Required cover \u2248 300k\u00d7\u00e4\u2081\u2080@3% (\u22488.53) \u2248 2.56M. That is, about 2.56M life cover to cover 10 years of income gap.",
    "Should existing assets also be deducted?",
    "Deduct usable financial assets and existing policy cover. The income-replacement method gives an upper bound; calibrate by net assets for a safer figure.",
    "Does the income-replacement method overstate the need?",
    "Yes. Basing it only on an income multiple ignores savings, social security and spouse income, inflating cover. Properly, need = liabilities + expense gap - existing resources, then cross-check with an income multiple.",
]))

# ---------------- loss-ratio (19) ----------------
write('loss-ratio', build('loss-ratio', [
    "Ratio of paid claims to premium",
    "Loss ratio = claim payments \u00f7 premium income.",
    "/ Loss Ratio Calculator",
    "Loss Ratio Calculator",
    '\U0001F4D6 View the "Ratio of Paid Claims to Premium User Guide"',
    "Loss ratio = paid claims / premium",
    "The lower the loss ratio, the larger the profit margin.",
    "The combined ratio must also include the expense ratio.",
    "\U0001F4DA Deep Dive: Loss Ratio (Paid Claims / Premium)",
    "See how much of premium is paid out as claims - the core of underwriting quality.",
    "and",
    "expense ratio",
    "sum to",
    "Paid 6.5M, premium 10M",
    "Loss ratio = 650/1000 = 65%. That is, 0.65 of every premium yuan is paid out.",
    "Difference between paid and incurred loss ratios?",
    "Paid looks only at settled claims; incurred includes IBNR and is more complete. Early in development paid is low and rises as claims mature.",
    "Is a 70% loss ratio good or bad?",
    "A loss ratio alone is not enough. 70% loss ratio + 25% expense ratio = 95% combined ratio (thin underwriting profit); but with a high expense ratio, 70% can still break even negative. Always read the combined ratio with the expense ratio.",
]))

# ---------------- mortality-prob (19) ----------------
write('mortality-prob', build('mortality-prob', [
    "Derive mortality rate from survival rate",
    "Given annual survival p, mortality q = 1 - p.",
    "Mortality / survival conversion",
    "/ Mortality and Survival Conversion",
    "Mortality and Survival Conversion",
    '\U0001F4D6 View the "Derive Mortality from Survival Rate User Guide"',
    "Mortality q\u2093 = 1-p\u2093",
    "Annual survival p",
    "n-year survival probability = p^n.",
    "\U0001F4DA Deep Dive: Mortality (Derived from Survival Rate)",
    "Get mortality q\u2093 directly from annual survival p\u2093.",
    "build",
    "life table",
    "or price mortality assumptions.",
    "q\u2093 = 1-0.99 = 0.01. That is, the annual mortality at that age is 1%.",
    "Is q identical to 1-p?",
    "Yes. One-year q\u2093 = 1-p\u2093 holds exactly; multi-year needs survival probabilities multiplied.",
    "Can crude and actuarial mortality be mixed?",
    "No. Crude mortality comes from population statistics without age/sex split; actuarial mortality is stratified by age, sex, smoking, etc. (life table). Mixing them biases pricing by tens of basis points.",
]))

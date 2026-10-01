#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""insurance 第1批：annuity-certain-pv / annuity-nsp / annuity-present / average-severity / calc-1"""
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


# ---------------- annuity-certain-pv (19) ----------------
write('annuity-certain-pv', build('annuity-certain-pv', [
    "Insurance Annuity Pricing Basis",
    "Annuity-certain present value a_n| = (1 \u2212 v^n) / i.",
    "Annuity-Certain Present Value",
    "/ Annuity-Certain PV Calculator",
    "Annuity-Certain PV Calculator",
    '\U0001F4D6 View the "Insurance Annuity Pricing Basis User Guide"',
    "Annual amount (\u00a5)",
    "Number of years",
    "End-of-period a_n| = (1 \u2212 v^n) / i.",
    "Beginning-of-period = end-of-period × (1+i).",
    "\U0001F4DA Deep Dive: Annuity-Certain Present Value (Premium Pricing Basis)",
    "Compute the present value of an annuity paid a fixed amount each year for n years, for pricing or product comparison.",
    "Discount a series of future certain payments to today and check whether the internal return is reasonable.",
    "Annual 12k, 3%, 15 years",
    "PV = 12000×(1\u22121.03\u207b\u00b9\u2075)/0.03 = 12000×11.9379 ≈ 143254 ¥. That is, the PV of 12k/yr for 15 years at 3% is about 143k ¥.",
    "What interest rate i to use?",
    "Use the valuation rate or a market-comparable yield. Higher i \u2192 lower PV; 3% is a common illustration rate, but the contract's valuation rate governs in practice.",
    "Can pricing rate and illustration rate be mixed?",
    "No. The pricing rate is the conservative assumption for premium calculation (capped by regulation); the illustration rate may be higher for benefit display. Mixing them overstates client returns and understates company liabilities.",
]))

# ---------------- annuity-nsp (22) ----------------
write('annuity-nsp', build('annuity-nsp', [
    "Net single premium from annual benefit and annuity factor",
    "Enter the annual benefit and annuity-present-value factor a_x to find the net single premium.",
    "NSP = annual benefit × annuity PV factor a_x",
    "/ Annuity Net Single Premium Calculator",
    "Annuity Net Single Premium Calculator",
    '\U0001F4D6 View the "Net Single Premium from Annual Benefit and Annuity Factor User Guide"',
    "Net single premium = annual benefit × ä\u2099",
    "Annual benefit (\u00a5)",
    "Annuity factor a_x",
    "a_x is derived by discounting the life table.",
    "1000×15 → 15000 ¥.",
    "\U0001F4DA Deep Dive: Net Single Premium from Annual Benefit and Annuity Factor",
    "Given the annual annuity amount and payout period, back-calculate the one-time net premium (fees excluded).",
    "Compare net single premiums across different payout periods.",
    "Annual 1000, 15 years",
    "Net single premium = annual benefit × ä\u2099. ä\u2081\u2085@3% ≈ 11.94, so 1000×11.94 = 11940 ¥.",
    "What is the relation between ä\u2099 and the PV formula?",
    "ä\u2099 = (1\u2212v\u207f)/i, the beginning-of-period annuity factor; annual benefit × ä\u2099 = PV = PMT×ä\u2099, same as",
    "annuity-certain present value",
    ".",
    "Where does net single premium differ from gross premium?",
    "The net single premium only covers insurance benefits (pure risk cost); the gross premium adds loadings (commission, operations, profit and safety margin) on top, typically 15%\u201340% higher.",
]))

# ---------------- annuity-present (38) ----------------
write('annuity-present', build('annuity-present', [
    "\U0001F3E6 Annuity Present Value Calculator",
    "Annuity present and future value, supporting ordinary, due and perpetuity annuities.",
    "/ Annuity PV Calculation",
    '\U0001F4D6 View the "Annuity PV Calculator (Insurance) User Guide"',
    "Interest rate (%/period)",
    "Annuity type",
    "Ordinary annuity (end-of-period)",
    "Annuity due (beginning-of-period)",
    "Perpetuity",
    "\U0001F522 Ordinary Annuity (End-of-Period)",
    "Present value PV",
    "Future value FV",
    "\U0001F522 Annuity Due (Beginning-of-Period)",
    "= ordinary annuity PV × (1+i)",
    "= ordinary annuity FV × (1+i)",
    "\U0001F522 Perpetuity",
    "A perpetuity has no future value (infinite term).",
    "Pension planning",
    ": estimate the annuity value of annual retirement income",
    "Insurance pricing",
    ": actuarial pricing of annuity insurance products",
    "Installment payments",
    ": present-value of level loan or rent payments",
    "Investment evaluation",
    ": cash-flow discounting analysis",
    "The rate must match the period (annual rate with years, monthly rate with months). A perpetuity requires a rate greater than 0.",
    "\U0001F4DA Deep Dive: Annuity PV Calculator (Insurance)",
    "Switch between ordinary and due annuities to see the PV difference.",
    "Given per-period payment, rate and periods, compute the PV for planning.",
    "End-of-period 10k, 5%, 20 years",
    "PV = 10000×(1\u22121.05\u207b\u00b2\u2070)/0.05 = 10000×12.4622 ≈ 124622 ¥. Due (ordinary→due) ×1.05 ≈ 130853 ¥.",
    "How much do ordinary and due differ?",
    "Due multiplies by (1+i) more than ordinary. At 5%, 20 years the gap is ~5%, larger for longer terms.",
    "Annuity present value",
    "Can it be used directly as a premium?",
    "No. The annuity PV is the benefit's present value; you must still multiply by the sum assured or benefit and add expense loadings to get the actual premium. This result only handles the cash-flow discounting step.",
    'About "Annuity Present Value Calculator"',
    "Annuity present value calculator — annuity PV and FV, supporting ordinary, due and perpetuity annuities, free to use. A professional financial tool using standard formulas; data is processed locally and not leaked.",
]))

# ---------------- average-severity (21) ----------------
write('average-severity', build('average-severity', [
    "Average claim severity from total claims and claim count",
    "Enter total claims and claim count to find the average claim amount.",
    "Severity = total claims / claim count",
    "/ Average Claim Severity Calculator",
    "Average Claim Severity Calculator",
    '\U0001F4D6 View the "Average Claim Severity from Total Claims and Count User Guide"',
    "Average severity = total claims / claim count",
    "Total claims (\u00a5)",
    "Claim count",
    "Average severity measures how large claims are.",
    "500k / 25 → 20k ¥.",
    "\U0001F4DA Deep Dive: Average Claim Severity (Total Claims / Claim Count)",
    "See the average payout per claim for a line of business to judge if pricing covers it.",
    "Compare average severity trends across years or channels.",
    "Total claims 500k, 25 claims",
    "Average severity = 500000/25 = 20000 ¥/claim. That is, the average payout per claim for this line is 20k ¥.",
    "Why also look at frequency?",
    "Severity (per-claim) must combine with frequency (occurrence rate) to get expected loss = frequency × severity; alone it misses claim density.",
    "Can a single catastrophe distort the average?",
    "Yes. A single catastrophe payout far exceeds normal claims and inflates the mean. In practice we truncate / layer (e.g. quantile method) or switch to",
    "to avoid extreme-value-driven average severity pricing.",
]))

# ---------------- calc-1 (21) ----------------
write('calc-1', build('calc-1', [
    "\U0001F6E1 Premium Waiver Calculation",
    "Estimate the total waived future premium and net benefit once premium waiver is triggered.",
    '\U0001F4D6 View the "Premium Waiver Calculation User Guide"',
    "PV of waived premium = Σ unpaid premium_t/(1+i)^t",
    "Annual premium (\u00a5)",
    "Premium-paying term (years)",
    "Years already paid",
    "Waiver rider annual cost (\u00a5, optional)",
    "Total waived premium = annual premium × remaining paying years",
    "Net benefit = total waived premium − cumulative waiver-rider cost (if purchased)",
    "This tool uses static amounts and ignores the time value of premiums and investment returns.",
    "Whether waiver triggers is governed by the policy terms and the insurer's claims decision.",
    "\U0001F4DA Deep Dive: Premium Waiver Present Value",
    "After the insured's death/disability, remaining premiums are waived; compute the PV of waived premiums for the reserve.",
    "Compare waiver PVs across different remaining terms.",
    "Annual premium 10k, 15 years left, 3%",
    "Waiver PV = Σ 10000/(1.03)^t (t=1..15) = 10000×ä\u2081\u2085@3% ≈ 10000×11.94 = 119400 ¥.",
    "What does years already paid affect?",
    "Only future unpaid years are discounted. Paid portions generate no more cash flow; the shorter the remaining term, the smaller the waiver PV.",
    "Is waiver PV the same as cash value?",
    "No. Waiver PV is the present value of future waived premiums, a company liability; cash value is the policyholder's surrender benefit, in a different account — they are not additive.",
]))

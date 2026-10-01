#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""insurance 第6批：pure-premium / surrender-value / survival-prob-t / uw-margin / uw-profit"""
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


# ---------------- pure-premium (20) ----------------
write('pure-premium', build('pure-premium', [
    "Expected loss = frequency \u00d7 severity",
    "Pure premium = claim frequency \u00d7 average claim amount.",
    "Pure premium (risk premium)",
    "/ Pure Premium Calculator",
    "Pure Premium Calculator",
    '\U0001F4D6 View the "Expected Loss = Frequency \u00d7 Severity User Guide"',
    "Claim frequency (times/unit)",
    "Pure premium = frequency \u00d7 severity.",
    "Actual premium also needs expense and profit loadings.",
    "\U0001F4DA Deep Dive: Pure Premium (Expected Loss = Frequency \u00d7 Severity)",
    "Multiply claim frequency by average severity to get the pure premium.",
    "Compare pure risk costs across business lines.",
    "Frequency 12%, average severity 30k",
    "Pure premium = 0.12\u00d730000 = 3600 \u00a5/policy-year. That is, 3600 \u00a5 risk cost per policy.",
    "Is pure premium the premium that should be charged?",
    "It is only the risk cost. Actual premium must also add",
    "expense ratio",
    "and profit margin, or underwriting will surely lose.",
    "Why add expenses before selling if it is pure premium?",
    "Pure premium covers only expected claims, with no expense or profit. Selling at pure premium alone means certain loss. Actual premium equals pure premium \u00d7 (1+loading rate) plus a risk margin.",
]))

# ---------------- surrender-value (18) ----------------
write('surrender-value', build('surrender-value', [
    "Cash value from policy reserve and surrender ratio",
    "Enter the policy reserve and surrender ratio to find the surrender cash value.",
    "/ Surrender Cash Value Calculator",
    "Surrender Cash Value Calculator",
    '\U0001F4D6 View the "Cash Value from Policy Reserve and Surrender Ratio User Guide"',
    "Policy reserve (\u00a5)",
    "Surrender ratio",
    "Early surrender ratio is usually low.",
    "50k \u00d7 0.8 \u2192 40k.",
    "\U0001F4DA Deep Dive: Cash Value (Reserve \u00d7 Surrender Ratio)",
    "On surrender, cash value = reserve \u00d7 surrender ratio.",
    "See how much is recoverable on surrender in different years.",
    "Reserve 50k, surrender ratio 80%",
    "Cash value = 50000 \u00d7 0.8 = 40000 \u00a5. That is, 40k received on surrender.",
    "Difference from estimate-20?",
    "Same formula and basis; estimate-20 takes the customer view (surrender benefit) while this tool takes the actuarial view (reserve \u00d7 ratio), but the calculation is identical.",
    "Are surrender ratio and surrender rate the same?",
    "No. Surrender ratio is the share of reserve actually returned to the customer (bound by minimum-cash-value regulation), while surrender rate is a business metric of surrendered policies over in-force policies; their denominators differ.",
]))

# ---------------- survival-prob-t (16) ----------------
write('survival-prob-t', build('survival-prob-t', [
    "t-year survival probability from survivor counts",
    "Enter the survivor counts at age x+t and x to find the t-year survival probability.",
    "t-Year Survival Probability Calculator",
    "/ t-Year Survival Probability Calculator",
    '\U0001F4D6 View the "t-Year Survival Probability from Survivor Counts User Guide"',
    "l_{x+t} (persons)",
    "l_x (persons)",
    "Core columns of the life table.",
    "\U0001F4DA Deep Dive: t-Year Survival Probability (from Survivor Counts)",
    "From survivor counts l at age x and x+t, find the t-year survival probability \u209ctp\u2093.",
    "Make survival assumptions for pension benefits or coverage periods.",
    "\u209ctp\u2093 = 950/1000 = 0.95. That is, a person aged x has a 95% chance of surviving t years.",
    "Relation between \u209ctp\u2093 and yearly p?",
    "\u209ctp\u2093 = p\u2093\u00b7p\u2093\u208a\u2081\u00b7\u2026\u00b7p\u2093\u208a\u209c\u208b\u2081, the product of yearly survival probabilities; dividing directly from the l table is more robust.",
    "Can survival probability exceed 1?",
    "No. Survival probability is a cumulative probability between 0 and 1, from multiplying yearly survival probabilities; if it exceeds 1, some year's survivors exceed the start-of-year count, a data error to verify.",
]))

# ---------------- uw-margin (24) ----------------
write('uw-margin', build('uw-margin', [
    "Underwriting profit inferred from combined ratio",
    "Enter loss ratio and expense ratio to find the underwriting profit margin.",
    "Underwriting margin = 1 - (loss ratio + expense ratio)",
    "/ Underwriting Margin Calculator",
    "Underwriting Margin Calculator",
    '\U0001F4D6 View the "Underwriting Profit from Combined Ratio User Guide"',
    "Underwriting profit = premium \u00d7 (1 - combined ratio)",
    "Loss ratio LR (%)",
    "Expense ratio ER (%)",
    "Underwriting profits only when combined ratio < 100%.",
    "\U0001F4DA Deep Dive: Underwriting Profit (Inferred from Combined Ratio)",
    "given",
    "underwriting profit",
    "= premium \u00d7 (1 - CR).",
    "See the profit space contributed by the underwriting side.",
    "Premium 1M, CR 95%",
    "Underwriting profit = 1M \u00d7 (1 - 0.95) = 50k. That is, the underwriting side earns 50k,",
    "margin",
    "Is CR 95% with 5% underwriting profit correct?",
    "Yes. Combined ratio =",
    "expense ratio",
    ", and 1 - CR is the underwriting margin; investment income is separate.",
    "Are underwriting margin and combined ratio always complementary?",
    "Yes, underwriting margin equals 100% minus combined ratio (excluding investment). But total profit also includes investment income; a low CR is not necessarily good performance - if investment loses big, a thin underwriting profit cannot save it.",
]))

# ---------------- uw-profit (20) ----------------
write('uw-profit', build('uw-profit', [
    "Premium minus claims minus expenses",
    "Underwriting profit = premium - claims - expenses.",
    "Underwriting profit",
    "/ Underwriting Profit Calculator",
    "Underwriting Profit Calculator",
    '\U0001F4D6 View the "Premium Minus Claims Minus Expenses User Guide"',
    "Underwriting profit = premium - claims - expenses",
    "Cross-check with the combined ratio.",
    "\U0001F4DA Deep Dive: Underwriting Profit (Premium - Claims - Expenses)",
    "The direct three-difference method:",
    "yields the underwriting profit.",
    "and",
    "method cross-check.",
    "Premium 10M, claims 6.5M, expenses 2.5M",
    "Underwriting profit = 10M - 6.5M - 2.5M = 1M. That is, the underwriting-side profit is 1M,",
    "margin",
    "Does it match uw-margin?",
    "Yes: (10M - 6.5M - 2.5M) = 1M = 10M \u00d7 (1 - 0.9) = 1M; at CR = 90% the two methods are equivalent.",
    "Underwriting profit negative but company still profitable?",
    "Possible. Underwriting loss can be offset by investment income (interest spread), the core of the insurance business model. But if underwriting keeps losing heavily and investment cannot cover it, that is an operating warning sign.",
]))

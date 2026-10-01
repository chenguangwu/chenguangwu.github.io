#!/usr/bin/env python3
# gen_economics_b5.py — economics b5 (5 slugs): pv-annuity/real-gdp/rule-of-72/spending-multiplier/tax-multiplier
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'economics')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'economics')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EXTRA = {}

def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items)); sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en)); sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en)); sys.exit(1)
        mp[z] = en
    return mp

def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'economics', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))


B = {}

B['pv-annuity'] = [
 'The present value of an annuity with equal receipts PMT at the end of each period, N periods in total, at rate i per period.',
 'Annuity Present Value Calculator',
 '/ Annuity Present Value',
 'Annuity Present Value',
 '📖 Read the "Annuity Present Value Calculator (Economics) Usage Guide"',
 '1,000 per period at 1% for 12 periods gives a present value of about 11,255.08.',
 '📚 Deep Dive: Annuity Present Value Calculator',
 'Loan valuation: enter each repayment and the rate to get the present value of the loan (its principal).',
 'Pension estimation: work out what must be set aside today for regular withdrawals.',
 'Teaching demo: show that a longer term and a lower rate give a higher present value.',
 'Example: receiving 1,000 a month at a 0.5% monthly rate for 12 periods gives PV ≈ 1000 × (1 − 1.005^−12)/0.005 ≈ 11562 yuan.',
 'Beginning or end of period?',
 'An ordinary annuity pays at period end,',
 'the annuity-due present value',
 'is multiplied by an extra (1+i), so it is slightly higher. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'How does it relate to',
 'the monthly loan payment',
 'the present value of the monthly payment is the loan principal, and the rate and term determine the payment level. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Rate frequency?',
 'Use the per-period rate that matches the payment frequency; convert an annual rate to a monthly one and never mix them. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
]

B['real-gdp'] = [
 'Real GDP = nominal GDP / (1 + deflator %)',
 'Use the GDP deflator to strip out price changes and obtain real output.',
 'Real GDP Calculator',
 '/ Real GDP',
 '📖 Read the "Real GDP = Nominal GDP / (1 + Deflator %) Usage Guide"',
 'GDP = nominal GDP / (1 + deflator',
 'Nominal GDP',
 'GDP deflator (%)',
 'Real GDP strips out the effect of inflation.',
 'With a deflator of 10%, 1100 becomes 1000.',
 '📚 Deep Dive: Real GDP = Nominal GDP / (1 + Deflator %)',
 'Real output: enter nominal GDP and the deflator to get real GDP.',
 'Splitting volume and price: compare nominal and real growth to see the price contribution.',
 'Teaching demo: show that nominal output far exceeds real output when inflation is high.',
 'Example: nominal GDP of 110 with a deflator of 110 gives real = 110/(110/100) = 100, meaning zero real growth.',
 'What is the deflator?',
 'The GDP deflator = nominal/real × 100 and reflects the overall price level, unlike CPI. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'How does it relate to real growth?',
 'Real GDP is used to compute true growth, stripping the price effect out of the deflator. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'How does it relate to CPI deflation?',
 'CPI covers consumption items while the deflator covers all of GDP; the coverage differs, so do not mix them. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
]

B['rule-of-72'] = [
 'A rule of thumb for estimating the number of years needed to double an investment.',
 'Rule of 72 Calculator',
 '/ Rule of 72 (Doubling Time)',
 'Rule of 72 (Doubling Time)',
 '📖 Read the "Rule of 72 Calculator Usage Guide"',
 'Annual growth rate r (%)',
 'r = 6% doubles in about 12 years.',
 'The higher the rate, the larger the error; for the exact value use ln2/ln(1+r).',
 '📚 Deep Dive: Rule of 72 Calculator',
 'Doubling years: enter the annualized return to get the years needed to double.',
 'Return comparison: see how quickly different returns double.',
 'Teaching demo: show the inverse relationship between doubling time and the rate.',
 'Example: at 8% a year, doubling takes about 72/8 = 9 years; at 12%, about 6 years.',
 'Why 72?',
 '72 approximates ln2 × 100 and has many divisors, so it divides easily; it is a rule of thumb, not an exact value. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'How accurate is it?',
 'The rule is an approximation; the error grows when returns are not constant or fees apply, and for exact doubling use the logarithmic formula t = ln2/r. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Does it work for negative returns?',
 'Only for positive returns; for losses, use 72 divided by the loss rate to estimate the years to halve, in the opposite direction. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'How does it relate to',
 'CAGR? The rule rests on compound growth and shares its basis with CAGR, so it works as a quick mental estimate. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
]

B['spending-multiplier'] = [
 'The government purchases multiplier determined by the marginal propensity to consume MPC.',
 'Government Spending Multiplier Calculator',
 '/ Spending Multiplier',
 'Spending Multiplier',
 '📖 Read the "Government Spending Multiplier Calculator Usage Guide"',
 'MPC = 0.8 gives a multiplier of 5.',
 'The tax multiplier is −MPC/(1−MPC).',
 '📚 Deep Dive: Government Spending Multiplier Calculator',
 'Multiplier measurement: enter MPC to get the government spending multiplier.',
 'Policy evaluation: use the multiplier to estimate the output gain from fiscal stimulus.',
 'Teaching demo: show that a higher MPC means a larger multiplier.',
 'Example: with MPC = 0.8, k = 1/(1 − 0.8) = 5, so an extra 10 billion of government spending leverages 50 billion of output (simplified).',
 'How does it relate to',
 'the tax multiplier',
 'the tax multiplier is −MPC/(1−MPC), opposite in sign, because a tax cut first raises disposable income and only then consumption. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Is the real multiplier below the theory?',
 'Crowding out, import leakage and rising prices weaken the multiplier, so the theoretical value is an upper bound. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Where does MPC come from?',
 'Estimated from consumption data or taken from history; see',
 'the marginal propensity to consume',
 'tool. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
]

B['tax-multiplier'] = [
 'Finding the tax multiplier from the marginal propensity to consume',
 'Enter the marginal propensity to consume MPC to get the tax multiplier.',
 'Tax Multiplier Calculator',
 '/ Tax Multiplier Calculator',
 '📖 Read the "Finding the Tax Multiplier from the Marginal Propensity to Consume Usage Guide"',
 'k_t = −MPC/(1−MPC); the minus sign means it works in reverse.',
 '📚 Deep Dive: Finding the Tax Multiplier from the Marginal Propensity to Consume',
 'Tax cut effect: enter MPC to get the tax multiplier (a negative value).',
 'Policy comparison: compare it with',
 'the government spending multiplier',
 'to gauge the strength of each fiscal tool.',
 'Teaching demo: show that the tax multiplier is smaller in absolute value than the spending multiplier.',
 'Example: with MPC = 0.8, the tax multiplier = −0.8/0.2 = −4, so a 10 billion tax cut adds about 40 billion of output.',
 'Why is it negative?',
 'A tax cut first raises disposable income and then consumption through MPC, so the effect on output is positive while the sign in the formula reflects the reverse direction relative to the spending multiplier. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'How does it differ from the spending multiplier?',
 'The absolute values differ by a factor of MPC, and the spending multiplier is larger because part of a tax cut leaks into saving. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Weaker in reality?',
 'As with the spending multiplier, crowding out and leakage make the actual value smaller than the theoretical one. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
]

for s, lst in B.items():
    write(s, build(s, lst))

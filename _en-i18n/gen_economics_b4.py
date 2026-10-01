#!/usr/bin/env python3
# gen_economics_b4.py — economics b4 (5 slugs): marginal-propensity-consume/mpc-from-multiplier/nominal-to-real/okuns-law/present-value
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

B['marginal-propensity-consume'] = [
 'Finding the marginal propensity to consume from changes in consumption and income',
 'Enter the consumption change ΔC and the income change ΔY to get MPC.',
 'Marginal Propensity to Consume Calculator',
 '/ Marginal Propensity to Consume Calculator',
 '📖 Read the "Finding the Marginal Propensity to Consume from Changes in Consumption and Income Usage Guide"',
 'Consumption change ΔC',
 'Income change ΔY',
 '📚 Deep Dive: Finding the Marginal Propensity to Consume from Changes in Consumption and Income',
 'MPC measurement: enter two periods of consumption and income to compute the marginal propensity to consume.',
 'Multiplier inference: estimate the size of the expenditure multiplier from MPC.',
 'Teaching demo: show that a larger MPC means a larger multiplier.',
 'Example: income rises 1000 and consumption rises 800, so MPC = 0.8.',
 'What is the range of MPC?',
 '0 < MPC < 1 (the marginal propensity to consume is below 1), otherwise saving or borrowing behaviour is abnormal. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'How does it relate to the multiplier?',
 'The expenditure multiplier is k = 1/(1 − MPC), so MPC = 0.8 gives k = 5, meaning autonomous spending leverages five times the output. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'How does it relate to APC?',
 'APC is an average (level) measure and MPC a marginal (incremental) one, with MPC below APC in the short run. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
]

B['mpc-from-multiplier'] = [
 'Backing out the marginal propensity to consume from the expenditure multiplier',
 'Enter the expenditure multiplier k to get the marginal propensity to consume.',
 'MPC from Multiplier Calculator',
 '/ MPC from Multiplier Calculator',
 '📖 Read the "Backing Out the Marginal Propensity to Consume from the Expenditure Multiplier Usage Guide"',
 'Expenditure multiplier k',
 '📚 Deep Dive: Backing Out the Marginal Propensity to Consume from the Expenditure Multiplier',
 'Back out MPC: enter the expenditure multiplier k to compute MPC.',
 'Policy evaluation: use the estimated multiplier to gauge the consumption pass-through of fiscal stimulus.',
 'Teaching demo: show that a larger k means MPC closer to 1.',
 'Example: with an expenditure multiplier k = 5, MPC = 1 − 1/5 = 0.8.',
 'What is the formula?',
 'Rearranging k = 1/(1 − MPC) gives MPC = 1 − 1/k, which requires k > 1. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Can k be below 1?',
 'In theory k ≥ 1 (MPC ≥ 0); a computed value below 1 means the parameters or definitions are wrong. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Tax multiplier',
 'The tax multiplier is −MPC/(1 − MPC), which has the opposite sign and a slightly smaller magnitude than',
 'the government spending multiplier',
 '. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
]

B['nominal-to-real'] = [
 'Finding the real value from the nominal value and the inflation rate',
 'Enter the nominal value and the inflation rate π to get the real value.',
 'Nominal to Real Value Calculator',
 '/ Nominal to Real Value Calculator',
 '📖 Read the "Finding the Real Value from the Nominal Value and the Inflation Rate Usage Guide"',
 'Real = nominal/(1+π)',
 'Nominal value',
 'Inflation rate π',
 '📚 Deep Dive: Finding the Real Value from the Nominal Value and the Inflation Rate',
 'Making it real: enter the nominal value and the inflation rate to get the real value (purchasing power).',
 'Wage assessment: divide the nominal wage by inflation to see whether real wages rise or fall.',
 'Teaching demo: show that under high inflation the nominal value rises while the real one falls.',
 'Example: a nominal wage of 11,000 with 10% inflation gives a real wage of 11000/1.1 = 10000, so purchasing power is unchanged.',
 'Which deflator should be used?',
 'Use the GDP deflator for GDP and CPI for consumption, choosing the price index that matches the object. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'How does it relate to the real interest rate?',
 'Fisher equation',
 'the real rate ≈ nominal − inflation, the same idea as the deflation in this tool. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Deflation error?',
 'The single-period approximation is good enough; over many periods a chain index is more accurate, and watch the base period over long spans. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
]

B['okuns-law'] = [
 'Δu ≈ −½(actual growth − potential growth)',
 'The effect of the gap between actual and potential GDP growth on the change in the unemployment rate.',
 "Okun's Law Calculator",
 "/ Okun's Law",
 "Okun's Law",
 '📖 Read the "Okun\'s Law Calculator Usage Guide"',
 'The effect of the gap between actual GDP growth and potential growth on the change in the unemployment rate.',
 'Actual GDP growth rate (%)',
 'Potential growth rate (%)',
 'Actual 4% and potential 3% means the unemployment rate falls by about 0.5 points.',
 'The coefficient is −½ (a common approximation).',
 '📚 Deep Dive: Okun\'s Law Calculator',
 'Unemployment assessment: enter the actual and potential growth gap to estimate the change in',
 'the unemployment rate',
 '.',
 'Gap monitoring: read the direction of the output gap to judge whether the labour market is hot or cold.',
 'Teaching demo: show that the unemployment rate rises when growth is below potential.',
 'Example: actual growth 2% and potential 3% gives a gap of −1%, so with an Okun coefficient of 2 the unemployment rate rises by about 0.5 percentage points.',
 'Is the coefficient fixed?',
 'The classic value is about −2 (each 1% of output gap corresponds to −0.5% difference in unemployment), and estimates differ across countries. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'What is potential growth?',
 'It is estimated from labour and total factor productivity trends and updated periodically by statistical agencies; it is not directly observed. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Is it really a law?',
 'It is an empirical relationship rather than a strict law; it drifts when the structure changes, so treat it as an approximation. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
]

B['present-value'] = [
 'Present Value Calculator',
 'The value today of a future cash flow, discounted at a given rate.',
 '/ Present Value (Discounting)',
 'Present Value (Discounting)',
 '📖 Read the "Present Value Calculator Usage Guide"',
 'Present value: PV = FV ÷ (1 + r)^t; discount amount = FV − PV; discount factor = (1 + r)^t; implied annualized return = (FV ÷ PV)^(1/t) − 1, used to discount investments and notes and to back out returns.',
 'Future value FV',
 '20,000 yuan at 5% over 10 years gives a present value of about 12,278.27.',
 'The higher the discount rate, the lower the present value.',
 '📚 Deep Dive: Present Value Calculator',
 'Discounting decisions: enter the future amount and the discount rate, compute the present value and judge whether it is worth it.',
 'Bond valuation: discount several periods of coupons plus principal to get the present value.',
 'Teaching demo: show that a higher discount rate gives a lower present value.',
 'Example: 11,000 one year later at a 10% discount rate gives PV = 11000/1.1 = 10000.',
 'How is the discount rate set?',
 'Use the opportunity cost of funds or the required return; the higher it is, the lower the present value, and it is the core assumption. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'How does it relate to future value?',
 'Present value is the future value discounted back, and the two are inverse (PV × (1+r)^t = FV). Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Multiple periods of cash flow?',
 'Discount each period separately and add them up, which is',
 'the part of NPV before subtracting the initial investment. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
]

for s, lst in B.items():
    write(s, build(s, lst))

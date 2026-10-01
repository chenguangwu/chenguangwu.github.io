#!/usr/bin/env python3
# gen_economics_b2.py — economics b2 (5 slugs): elasticity-demand/fisher-equation/fv-annuity/gdp-expenditure/gdp-growth-rate
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

B['elasticity-demand'] = [
 'Compute the elasticity of demand with respect to price using the midpoint method, avoiding endpoint dependence.',
 'Demand Price Elasticity Calculator',
 '/ Demand Price Elasticity (Midpoint Method)',
 'Demand Price Elasticity (Midpoint Method)',
 '📖 Read the "Demand Price Elasticity Calculator Usage Guide"',
 'E_d ≈ −1.22 (elastic). An absolute value above 1 means elastic.',
 'Initial price P₁',
 'New price P₂',
 'Price 10→12 and quantity 100→80 give E_d ≈ −1.22 (elastic).',
 'An absolute value above 1 means elastic.',
 '📚 Deep Dive: Demand Price Elasticity Calculator',
 'Elasticity measurement: enter two quantity-price pairs and compute',
 'price elasticity',
 ', where an absolute value above 1 means elastic.',
 'Revenue judgement: when demand is elastic, cutting price raises revenue; when it is inelastic, raising price does.',
 'Teaching demo: show that the midpoint method gives consistent results for price increases and decreases.',
 'Example: price 10→12 and quantity 100→80 give a midpoint elasticity of (−20/90)/(2/11) ≈ −1.22, which is elastic.',
 'Why use the midpoint method?',
 'The ordinary endpoint method gives different results for rises and falls, while the midpoint method averages and is more symmetric and stable. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'What does the absolute value mean?',
 'Above 1 is elastic (quantity is sensitive to price), below 1 inelastic, and exactly 1 is unit elastic. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'How does it relate to total revenue?',
 'When demand is elastic, cutting price raises revenue, and when it is inelastic, raising price does; this is the core basis for pricing. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
]

B['fisher-equation'] = [
 'Finding the nominal interest rate from the real rate and inflation',
 'Enter the real interest rate r and the inflation rate π to get the nominal interest rate.',
 'Fisher Equation Calculator',
 '/ Fisher Equation Calculator',
 '📖 Read the "Finding the Nominal Rate from the Real Rate and Inflation Usage Guide"',
 'Real interest rate r (%)',
 'Inflation rate π (%)',
 'i ≈ r + π (approximate).',
 '📚 Deep Dive: Finding the Nominal Rate from the Real Rate and Inflation',
 'Nominal rate: enter the real rate and expected inflation to get the nominal rate.',
 'Real rate: subtract inflation from the nominal rate to get the real rate (approximately).',
 'Teaching demo: show that rising inflation expectations push the nominal rate up.',
 'Example: a real rate of 2% and inflation of 3% give a nominal rate of about 5%.',
 'Exact or approximate?',
 'The approximate form is i ≈ r + π; the exact one is (1+i) = (1+r)(1+π), and the difference is small at low inflation. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Expected or actual inflation?',
 'Fisher uses expected inflation; after the fact you can back out the realized real rate from actual inflation. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Negative real rates?',
 'When the nominal rate is below inflation the real rate is negative, which encourages borrowing and discourages saving. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
]

B['fv-annuity'] = [
 'The future value of an annuity with equal deposits PMT at the end of each period, N periods in total, at rate i per period.',
 'Annuity Future Value Calculator',
 '/ Annuity Future Value',
 'Annuity Future Value',
 '📖 Read the "Annuity Future Value Calculator Usage Guide"',
 '1,000 per period at 1% for 12 periods gives about 12,682.50.',
 '📚 Deep Dive: Annuity Future Value Calculator',
 'Savings goals: enter the periodic contribution and rate to get the accumulated amount at the end.',
 'Comparing contributions: try different PMT or period counts and compare the future values.',
 'Teaching demo: show ordinary versus annuity-due (the due version is multiplied by an extra 1+i).',
 'Example: depositing 1,000 per month at 6% a year (0.5% a month) for 12 periods gives FV ≈ 1000 × ((1.005^12 − 1)/0.005) ≈ 12340 yuan.',
 'Beginning or end of period?',
 'An ordinary annuity pays at period end; an annuity due has a future value multiplied by an extra (1+i), so it is slightly higher. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Should the rate be a per-period rate?',
 'It must be converted to the per-period rate matching the deposit frequency (for monthly deposits, the monthly rate), otherwise the result is wrong. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'How does it relate to',
 'compound amount',
 'the annuity future value is the sum of the compounded values of several equal cash flows, essentially sequential compounding. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
]

B['gdp-expenditure'] = [
 'Finding GDP from its expenditure components',
 'Enter consumption C, investment I, government spending G and net exports NX to get GDP.',
 'Expenditure-Approach GDP Calculator',
 '/ Expenditure-Approach GDP Calculator',
 '📖 Read the "Finding GDP from Its Expenditure Components Usage Guide"',
 'Consumption C (100 million yuan)',
 'Investment I (100 million yuan)',
 'Government spending G (100 million yuan)',
 'Net exports NX (100 million yuan)',
 '📚 Deep Dive: Finding GDP from Its Expenditure Components',
 'Aggregate accounting: enter the four components to compute total GDP.',
 'Structural analysis: look at each share to judge what drives demand.',
 'Teaching demo: show how negative net exports (a deficit) drag GDP down.',
 'Example: C = 60, I = 20, G = 18, NX = 2 (trillion) gives GDP = 100 trillion.',
 'What are the four components?',
 'C is consumption, I investment, G government purchases and NX net exports (exports − imports), the expenditure-approach definition. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Does it match the income approach?',
 'They are identical in theory; in practice statistical definitions and error terms cause small differences, so defer to official figures. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Do house prices count as investment?',
 'Newly built homes count as investment I,',
 'while resale prices do not (a pure asset transfer); rent counts as consumption C. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
]

B['gdp-growth-rate'] = [
 'Finding the growth rate from two periods of GDP',
 'Enter the current-period and base-period GDP to get the growth rate.',
 'GDP Growth Rate Calculator',
 '/ GDP Growth Rate Calculator',
 '📖 Read the "Finding the Growth Rate from Two Periods of GDP Usage Guide"',
 'Current-period GDP_t (100 million yuan)',
 'Base-period GDP (100 million yuan)',
 '📚 Deep Dive: Finding the Growth Rate from Two Periods of GDP',
 'Growth measurement: enter the current-period and base-period GDP to compute the growth rate.',
 'Real vs nominal: use',
 'to compute real growth, stripping out prices.',
 'Teaching demo: show that high nominal growth may be nothing but inflation.',
 'Example: a current period of 102 and a base period of 100 give a growth rate of 2%.',
 'Nominal or real?',
 'For real output use real GDP growth (inflation stripped out); nominal growth contains price effects. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Year on year or quarter on quarter?',
 'Annual figures usually use year-on-year growth, quarterly ones often annualized quarter-on-quarter; do not mix the two bases. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Negative growth?',
 'Two consecutive quarters of negative real GDP growth is often defined as a technical recession, subject to the official determination. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
]

for s, lst in B.items():
    write(s, build(s, lst))

#!/usr/bin/env python3
# gen_economics_b1.py — economics b1 (5 slugs): average-propensity-consume/balance-of-trade/cobb-douglas/compound-amount/cross-elasticity
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

B['average-propensity-consume'] = [
 'Finding the average propensity to consume from consumption and income',
 'Enter consumption C and income Y to get the average propensity to consume.',
 'Average Propensity to Consume Calculator',
 '/ Average Propensity to Consume Calculator',
 '📖 Read the "Finding the Average Propensity to Consume from Consumption and Income Usage Guide"',
 'Consumption C',
 'Income Y',
 '📚 Deep Dive: Finding the Average Propensity to Consume from Consumption and Income',
 'Macro view: enter total household consumption and disposable income to see the overall consumption rate.',
 'Cross-country comparison: enter APC for different economies to compare saving-rate gaps.',
 'Teaching demo: show the pattern that APC usually falls as income rises.',
 'Example: with consumption of 80 thousand and income of 100 thousand, APC = 0.8, meaning 80% of income goes to consumption and 20% to saving.',
 'What is the difference between APC and MPC?',
 'APC is total consumption / total income (a level measure), while MPC is the change in consumption / change in income (a marginal measure) and feeds the multiplier. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Can APC exceed 1?',
 'At low incomes, borrowing to consume can push APC above 1 (consumption exceeds income); normally it falls as income rises. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'How does it relate to the saving rate?',
 'APS = 1 − APC; the two are complementary, so a lower APC means a higher saving rate. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
]

B['balance-of-trade'] = [
 'Finding the balance of trade from exports and imports',
 'Enter exports X and imports M to get the trade balance.',
 'Balance of Trade Calculator',
 '/ Balance of Trade Calculator',
 '📖 Read the "Finding the Balance of Trade from Exports and Imports Usage Guide"',
 'Exports X (100 million yuan)',
 'Imports M (100 million yuan)',
 'BoT = X − M; positive means a surplus.',
 '200 − 180 gives a surplus of 2 billion yuan.',
 '📚 Deep Dive: Finding the Balance of Trade from Exports and Imports',
 'Surplus vs deficit: enter exports and imports and compute the difference; positive is a surplus, negative a deficit.',
 'Trend watching: enter several periods to see how the trade balance moves.',
 'Teaching demo: show that net exports NX is one component of the expenditure approach to GDP.',
 'Example: exports of 200 billion and imports of 180 billion give a trade balance of +20 billion (a surplus).',
 'Is a surplus always good?',
 'A surplus means net output sold abroad, but a persistently large one may come with excess saving or exchange-rate pressure, so read it against the structure. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'How does it relate to NX?',
 'The trade balance is net exports NX = X − M, a component of GDP = C + I + G + NX. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Does it include trade in services?',
 'The goods trade balance excludes services; for the full picture look at the current account, while this tool follows the export/import basis you enter. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
]

B['cobb-douglas'] = [
 'Finding output from capital, labor and technology',
 'Enter total factor productivity A, capital K, capital elasticity α and labor L to get output.',
 'Cobb-Douglas Production Function Calculator',
 '/ Cobb-Douglas Production Function Calculator',
 '📖 Read the "Finding Output from Capital, Labor and Technology Usage Guide"',
 'Y = A·K^α·L^(1−α) (constant returns to scale). With A=1, K=200, α=0.3, L=100 the result is about 123.3.',
 'Technology level A',
 'Capital K',
 'Capital elasticity α',
 'Labor L',
 'Y = A·K^α·L^(1−α) (constant returns to scale).',
 'With A=1, K=200, α=0.3, L=100 the result is about 123.3.',
 '📚 Deep Dive: Finding Output from Capital, Labor and Technology',
 'Output measurement: enter A, K, L and α to compute total output Y.',
 'Contribution breakdown: adjust α to see the capital versus labor contribution elasticity.',
 'Teaching demo: show that with constant returns to scale (α + 1 − α = 1), doubling inputs doubles output.',
 'Example: with A = 1, K = 100, L = 50 and α = 0.3, Y = 1 × 100^0.3 × 50^0.7 ≈ 100^0.3 × 50^0.7 ≈ 71.',
 'What is α?',
 'The output elasticity of capital, usually 0.2–0.4; 1 − α is the labor elasticity, and α + labor elasticity = 1 means constant returns to scale. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Where does A come from?',
 'Total factor productivity (TFP), reflecting technical efficiency; it is backed out from actual output or estimated as the Solow residual. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Returns to scale?',
 'If the exponents sum to 1, returns are constant; above 1 they are increasing. This tool defaults to constant, and you can adjust the elasticities to try increasing returns. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
]

B['compound-amount'] = [
 'The future value of a principal at annual rate r, compounded n times per year, after t years.',
 '/ Compound Amount',
 'Compound Amount',
 '📖 Read the "Compound Amount Calculator Usage Guide"',
 'n = 12 means monthly compounding.',
 '10,000 yuan at 5% for 10 years with annual compounding gives 16,288.95.',
 '📚 Deep Dive: Compound Amount Calculator',
 'Future value: enter principal, rate and years to get the value at maturity.',
 'Frequency comparison: compare annual, semi-annual, quarterly and monthly compounding to see the effect of frequency.',
 'Teaching demo: show how interest on interest makes the future value exceed simple interest.',
 'Example: principal 10,000, annual rate 5%, annual compounding, 10 years gives FV = 10000 × 1.05^10 ≈ 16289 yuan.',
 'Compound versus simple interest?',
 'Simple interest pays only on the principal, while compound interest pays interest on interest, so the gap widens over time. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Does a larger n give more?',
 'More frequent compounding gives a slightly higher future value, but it converges to the continuous-compounding limit e^(rt), so the difference is limited. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'What about inflation?',
 'The nominal future value is not adjusted for inflation; to compare real purchasing power, discount it by the real rate (Fisher). Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
]

B['cross-elasticity'] = [
 'Cross-Price Elasticity Calculator',
 'The effect of a price change in good y on the quantity demanded of good x. Positive means substitutes, negative means complements.',
 '/ Cross-Price Elasticity',
 'Cross-Price Elasticity',
 '📖 Read the "Cross-Price Elasticity Calculator Usage Guide"',
 'Good x initial quantity',
 'Good x new quantity',
 'Good y initial price',
 'Good y new price',
 'If y gets pricier and demand for x rises, they are substitutes (positive).',
 'Negative means complements.',
 '📚 Deep Dive: Cross-Price Elasticity Calculator',
 'Relationship test: enter the quantity and price changes of two goods and compute the cross elasticity; positive means substitutes, negative complements.',
 'Pricing reference: raise the price of a complement to see the effect on your own demand.',
 'Teaching demo: show that cross elasticity is positive for substitutes and negative for complements.',
 'Example: the price of B rises 10% and the quantity of A rises 5%, so cross elasticity = 0.5 > 0 and A and B are substitutes.',
 'What do the signs mean?',
 'Positive = substitutes (a price rise for one lifts demand for the other), negative = complements (a price rise for one cuts demand for the other), near 0 = unrelated. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Should the midpoint method be used?',
 'As with demand elasticity, the midpoint method avoids direction dependence and gives stabler results. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'How does it differ from own-price elasticity?',
 'Cross elasticity looks across goods,',
 'demand price elasticity',
 'looks at a good own price; the two are different dimensions. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
]

for s, lst in B.items():
    write(s, build(s, lst))

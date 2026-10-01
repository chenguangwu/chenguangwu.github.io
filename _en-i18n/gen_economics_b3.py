#!/usr/bin/env python3
# gen_economics_b3.py — economics b3 (5 slugs): income-elasticity/inflation-rate/labor-force-participation/labor-force/marginal-product-labor
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

B['income-elasticity'] = [
 'Income Elasticity Calculator',
 'The effect of a change in income on quantity demanded. Positive for normal goods, negative for inferior goods.',
 '/ Income Elasticity',
 'Income Elasticity',
 '📖 Read the "Income Elasticity Calculator Usage Guide"',
 'Income elasticity of demand E_i = rate of change in quantity demanded ÷ rate of change in income = (ΔQ ÷ Q) ÷ (ΔI ÷ I); the arc elasticity form (ΔQ ÷ average quantity) ÷ (ΔI ÷ average income) can also be used. E_i above 1 means a luxury, 0 to 1 a necessity, 0 a neutral good and below 0 an inferior good; an elasticity above 1 means demand grows faster than income, which helps forecast how income changes reshape consumption.',
 'Initial income I₁',
 'New income I₂',
 'Rising income with rising demand means a normal good (positive).',
 'A negative value means an inferior good.',
 '📚 Deep Dive: Income Elasticity Calculator',
 'Category test: enter the quantity and income changes and compute income elasticity; positive means a normal good.',
 'Consumption structure: compare the elasticity difference between necessities and luxuries.',
 'Teaching demo: show that luxuries have elasticity above 1, necessities 0–1 and inferior goods a negative value.',
 'Example: income rises 10% and demand rises 15%, so income elasticity = 1.5 > 1, a luxury (demand grows faster).',
 'What do the signs mean?',
 'Positive = normal good (demand rises with income); negative = inferior good (demand falls as income rises, such as cheap substitutes). Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Necessity or luxury?',
 'Among normal goods, elasticity above 1 means a luxury and 0–1 a necessity, reflecting how sensitive demand is to income. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Should the midpoint method be used?',
 'As before, the midpoint method averages and is more stable, avoiding endpoint direction bias. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
]

B['inflation-rate'] = [
 'The period inflation rate based on the consumer price index.',
 'Inflation Rate Calculator',
 '/ Inflation Rate (CPI)',
 'Inflation Rate (CPI)',
 '📖 Read the "Inflation Rate Calculator Usage Guide"',
 'Base-period CPI',
 'Reporting-period CPI',
 'CPI 100→105 corresponds to 5% inflation.',
 'The denominator is the base-period CPI.',
 '📚 Deep Dive: Inflation Rate Calculator',
 'Inflation measurement: enter two periods of CPI to compute the year-on-year inflation rate.',
 'Purchasing power: read the loss of money purchasing power from the inflation rate.',
 'Teaching demo: show that inflation makes the real rate = nominal − inflation.',
 'Example: base-period CPI 100 and reporting-period CPI 105 give inflation = (105 − 100)/100 = 5%.',
 'What is the difference between CPI and PPI?',
 'CPI measures a consumer basket of prices while PPI measures the producer side; the pass-through lags and the two have different coverage. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Core inflation?',
 'Inflation with food and energy volatility stripped out, which reflects the trend better and is what monetary policy usually watches. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Negative inflation?',
 'A falling CPI is deflation; persistent deflation comes with weak demand and needs a policy response. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'How to use the Inflation Rate Calculator',
 'Use the base-period and reporting-period CPI to measure inflation, assess changes in the price level and in the purchasing power of money, and support personal financial planning, pay-adjustment judgement and macroeconomic observation.',
 'What does the Inflation Rate Calculator do?',
 'Enter two periods of the consumer price index (CPI) and compute the period inflation rate for a quantitative assessment of price-level change and purchasing power.',
 'How do I use the Inflation Rate Calculator?',
 'What scenarios is the Inflation Rate Calculator suited to?',
 'Inflation rate = (current price level − base-period price level) / base period × 100%, measuring the overall rise in prices over a period.',
 'Definition',
 'Commonly CPI year on year (versus the same month last year) or month on month (versus last month). A positive result means inflation, a negative one deflation.',
 'Different baskets and base periods give different results; monthly swings reflect seasonality and temporary shocks, so judge against the trend.',
]

B['labor-force-participation'] = [
 'Finding the labor force participation rate from the labor force and total population',
 'Enter the labor force LF and the working-age population POP to get the participation rate.',
 'Labor Force Participation Rate Calculator',
 '/ Labor Force Participation Rate Calculator',
 '📖 Read the "Finding the Labor Force Participation Rate from the Labor Force and Total Population Usage Guide"',
 'Labor force LF (10 thousand people)',
 'Working-age population POP (10 thousand people)',
 '📚 Deep Dive: Finding the Labor Force Participation Rate from the Labor Force and Total Population',
 'Participation rate: enter the labor force and the working-age population to compute the rate.',
 'Trend watching: compare participation across groups or periods.',
 'Teaching demo: show that population ageing drags the overall participation rate down.',
 'Example: a labor force of 70 million and a working-age population of 100 million give a participation rate of 70%.',
 'Who is in the labor force?',
 'The employed plus the unemployed (actively seeking work); students, retirees and those not seeking work are excluded. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'How does it relate to',
 'the unemployment rate',
 'the participation rate looks at potential supply while the unemployment rate looks at the share of the labor force without a job; the two indicators complement each other. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Is a decline good or bad?',
 'It may reflect more retirements (structural) or weak confidence (cyclical), so read it together with the cause. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
]

B['labor-force'] = [
 'Finding the labor force from the numbers employed and unemployed',
 'Enter the number employed E and the number unemployed U to get the size of the labor force.',
 'Labor Force Size Calculator',
 '/ Labor Force Size Calculator',
 '📖 Read the "Finding the Labor Force from the Numbers Employed and Unemployed Usage Guide"',
 'Employed E (10 thousand people)',
 'Unemployed U (10 thousand people)',
 'LF = employed + unemployed.',
 '140 + 10 gives 1.5 million people.',
 '📚 Deep Dive: Finding the Labor Force from the Numbers Employed and Unemployed',
 'Labor force accounting: enter employment and unemployment to get the total labor force.',
 'Structural split: look at the employed / unemployed shares.',
 'Teaching demo: show that people outside the labor force are not counted in the denominator.',
 'Example: 66 million employed and 4 million unemployed give a labor force of 70 million.',
 'How is unemployment defined?',
 'People without a job who have actively searched recently and can start immediately; those who withdraw passively count neither as unemployed nor as part of the labor force. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'How does it relate to the total population?',
 'The labor force is no larger than the working-age population; the gap is the non-participation (students, retirees, caregivers and so on). Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Hidden unemployment?',
 'Informal or low-commitment work is hard to capture fully; official figures rely on the surveyed unemployed. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
]

B['marginal-product-labor'] = [
 'Finding the marginal product from output and the change in labor',
 'Enter the output change ΔQ and the labor change ΔL to get the marginal product of labor.',
 'Marginal Product of Labor Calculator',
 '/ Marginal Product of Labor Calculator',
 '📖 Read the "Finding the Marginal Product from Output and the Change in Labor Usage Guide"',
 'Output change ΔQ',
 'Labor change ΔL',
 '📚 Deep Dive: Finding the Marginal Product from Output and the Change in Labor',
 'Marginal output: enter two periods of output and labor to compute MPL.',
 'Hiring decisions: compare MPL × product price with the wage to judge whether to hire more.',
 'Teaching demo: show diminishing marginal returns (MPL falls as L rises).',
 'Example: labor 10→11 and output 100→108 give MPL = 8/1 = 8 units per worker.',
 'Diminishing marginal returns?',
 'With other inputs fixed, continuously adding labor eventually lowers MPL, which is the law of diminishing marginal returns. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'How does it relate to average product?',
 'When MPL > APL the average rises and when MPL < APL it falls; their intersection is the maximum of the average. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'How is it used for decisions?',
 'Hire up to the point where MPL × product price = wage for maximum profit (marginal revenue product = cost). Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
]

for s, lst in B.items():
    write(s, build(s, lst))

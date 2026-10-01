#!/usr/bin/env python3
# gen_economics_b6.py — economics b6 (2 slugs): unemployment-rate/velocity-of-money
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

B['unemployment-rate'] = [
 'u = unemployed / labor force × 100%',
 'The share of unemployed people within the labor force.',
 'Unemployment Rate Calculator',
 '/ Unemployment Rate',
 'Unemployment Rate',
 '📖 Read the "Unemployment Rate Calculator Usage Guide"',
 'u = unemployed / labor force',
 'Number unemployed',
 'Total labor force',
 '600/10000 gives a 6% unemployment rate.',
 'Labor force = employed + unemployed.',
 '📚 Deep Dive: Unemployment Rate Calculator',
 'Unemployment measurement: enter the unemployed and the labor force to get the unemployment rate.',
 'Trend watching: compare the unemployment rate across several periods.',
 'Teaching demo: show that the labor force does not include those who have dropped out.',
 'Example: 4 million unemployed and a labor force of 70 million give an unemployment rate of 400/7000 ≈ 5.71%.',
 'Who is in the denominator?',
 'The labor force (employed + unemployed), excluding people outside the labor force, so the participation rate affects the reading. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Natural rate of unemployment?',
 'The lowest sustainable unemployment rate excluding cyclical unemployment, about 4–5%; above it may signal weak demand. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'U3 and U6?',
 'The commonly used U3 is the narrow measure, while U6 includes marginally attached and underemployed workers, a broader definition. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
]

B['velocity-of-money'] = [
 'Finding the velocity of circulation from the price level, output and money supply',
 'Enter the price level P, real output Y and money supply M to get the velocity of money.',
 'Velocity of Money Calculator',
 '/ Velocity of Money Calculator',
 '📖 Read the "Finding the Velocity of Circulation from the Price Level, Output and Money Supply Usage Guide"',
 'MV = PY (the equation of exchange). With P=1, Y=2000, M=500 the result is 4.',
 'Price level P',
 'Real output Y (100 million yuan)',
 'Money supply M (100 million yuan)',
 'MV = PY (the equation of exchange).',
 '📚 Deep Dive: Finding the Velocity of Circulation from the Price Level, Output and Money Supply',
 'Velocity measurement: enter P, Y and M to compute the velocity of money.',
 'Money assessment: watch how V changes to judge how active money is.',
 'Teaching demo: show that a falling V usually comes with idle money balances (a liquidity trap).',
 'Example: with P = 1.05, Y = 100 and M = 50, V = 1.05 × 100/50 = 2.1 times a year.',
 'What is MV = PY?',
 'The quantity equation of money (Fisher): M is the money supply, V velocity, P the price level and Y real output. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'What does a falling V mean?',
 'Money circulates more slowly and trade is slack; in the extreme it is a liquidity trap where monetary policy loses traction. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
 'Is Y real?',
 'The equation uses real output Y, so PY is the nominal value of transactions; do not multiply nominal GDP by P again. Results are for economics teaching and quick estimation only; they are not investment advice or a policy basis, and for forecasts and empirical estimates defer to official statistics and textbooks.',
]

for s, lst in B.items():
    write(s, build(s, lst))

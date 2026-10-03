#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'restaurant')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'restaurant')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
DISCL = "Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected."
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
    out = {'slug': slug, 'industry': 'restaurant', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
# -*- coding: utf-8 -*-
def main():
    write('seasoning-scaler', build('seasoning-scaler', [
        '🖼️ Seasoning Ratio Scaler',
        'Scale seasoning quantities by servings while keeping the ratio unchanged',
        'Core formula (from input variables): String(Math.round(scaledAmt)); formatted.slice(0,-3); formatted.slice(0,-2)',
        '/ Seasoning Ratio Scaler',
        '📖 Read the "Seasoning Ratio Scaler User Guide"',
        '🖼️ Scale',
        '📊 Scaling result',
        '📚 Deep dive: proportional scaling of seasoning ratios',
        'Scale a home recipe from 2 servings up to a 8-serving dinner, converting each seasoning quantity proportionally.',
        'In restaurant batch prep, scale a trial formula up to actual output volume while keeping flavor consistent.',
        'Scale servings down for small test batches so you do not mix too much and waste it.',
        'Scaling 4 servings up to 10',
        'Scale factor = 10 ÷ 4 = 2.50. Salt 5 g → 12.5 g; light soy sauce 20 ml → 50 ml; sugar 8 g → 20 g; dried chili 8 g → 20 g. Note that pungent seasonings (chili, Sichuan pepper, pepper) are best scaled at 80% (i.e. 16 g), because the perceived heat accumulates faster than linearly; salt and sugar are also best added at 80% first, then tasted and topped up, to avoid over-salting or over-sweetening.',
        'Why scale every seasoning proportionally?',
        'Recipe flavor depends on the relative ratios among seasonings, so only proportional scaling keeps taste consistent. Scaling up the main ingredient alone while leaving seasonings unchanged makes the dish taste bland.',
        'What to watch for when scaling up a lot?',
        'Perception of heat, umami and spices is nonlinear, so when scaling by 3x or more add these seasonings at 70-80% first and adjust after tasting; larger liquid volume also means a longer reduction time, so extend the cooking time accordingly.',
        'About "Seasoning Ratio Scaler"',
    ]))

    write('table-turnover', build('table-turnover', [
        '🍽️ Table Turnover Optimizer',
        'Enter business hours, table count and average dining time to compute turnover rate and service capacity',
        'Core formula (from input variables): Math.floor(actualTurnover×tables); Math.floor(totalTables×perTable); min(actualTurnover÷5×100,100)',
        '/ Table Turnover Optimizer',
        '📖 Read the "Table Turnover Optimizer User Guide"',
        '🍽️ Compute turnover rate',
        '📊 Turnover analysis',
        '📚 Deep dive: turnover rate and service capacity estimation',
        'Compute the turnover rate from business hours, table count and average dining time to see whether seat turnover has hit its bottleneck.',
        'Estimate daily covers and revenue to verify whether the revenue target is reachable.',
        'Assess the payoff of time limits, added tables or table assignment changes: shorten average dining time by 5 minutes and watch the turnover rate respond.',
        'Daily capacity for a 20-table restaurant',
        '8 business hours (480 minutes), average dining 50 minutes → theoretical max turnover = 480 ÷ 50 = 9.6; seat occupancy 75% → actual turnover = 9.6 × 0.75 = 7.2 (graded "excellent"). 20 tables → 144 table turns a day; 3 guests per table → 432 covers; average ticket 80 CNY → daily revenue about 34,560 CNY. If average dining time is cut to 45 minutes, theoretical turnover rises to 10.67 and actual to 8.0, and daily revenue grows to about 38,400 CNY.',
        'What turnover rate counts as good?',
        'The tool grades the actual turnover rate: ≥4 excellent, ≥3 good, ≥2 average, <2 low. Reasonable ranges differ greatly between fast food and hot pot, so the more practical approach is to compare against your own store history and read the trend rather than an absolute number.',
        'How do I estimate seat occupancy?',
        'Seat occupancy is actual opened table turns divided by the theoretical maximum; it can be estimated from historical opened-table records for the same time slot. Without data, start with 60-70% and back-calibrate from actual revenue.',
        'About "Table Turnover Optimizer"',
        'How to use the Table Turnover Optimizer',
        'What does the Table Turnover Optimizer do?',
        'Enter business hours, table count and average dining time; the tool computes the turnover rate and receivable guest flow, and grades them, helping restaurants spot queue bottlenecks and boost seat turnover by adjusting table assignment or time limits.',
        'How do I use the Table Turnover Optimizer?',
        'What scenarios suit the Table Turnover Optimizer?',
    ]))

    write('taste-preference', build('taste-preference', [
        '📊 Taste Preference Statistics',
        'Record customer taste preferences locally and generate statistical charts (data stays in your browser)',
        '/ Taste Preference Statistics',
        '📖 Read the "Taste Preference Statistics User Guide"',
        'Preference distribution: vote share of each taste = votes for that taste ÷ total votes × 100%; average rating = Σrating ÷ number of raters; the modal taste is the one with the most votes; use the distribution to identify the salty / sweet / spicy preferences of your customer base and iterate the menu and new items. Data stays local and is never uploaded.',
        '📈 Statistical charts',
        '📚 Deep dive: local statistics of customer taste preferences',
        'Let customers tap a taste on the store tablet or POS terminal (salty / sweet / spicy / sour, etc.); each tap records one entry.',
        'After collecting for a while, look at the distribution ratio of each taste to judge the main customer preference and guide menu adjustments.',
        'Check the existing preference distribution before launching a new item so it does not clash with the main customer base.',
        'How to record and view',
        'Each customer tap writes one record (including',
        '), and the page aggregates in real time into a distribution chart with percentages. For example, of 120 records at a store "mild spicy" takes 42%, "not spicy" 33% and "hot" 25%, meaning the core customers accept spice but prefer mild levels, so new items should lead with mild spicy and offer hot as a minority option. A mis-tap can undo the last entry, or you can clear everything and start collecting again.',
        'Where is the data stored, and is it uploaded?',
        'Only in this browser localStorage. It is never uploaded to any server and does not sync across devices. Clearing browser data or switching devices loses the records, so export anything important and keep it yourself.',
        'Can I distinguish stores or time slots?',
        'No. The tool only counts entries per taste and does not separate store, time slot or dish. For multi-dimensional analysis, record each dimension separately or export and process it in a spreadsheet.',
        'About "Taste Preference Statistics"',
    ]))


if __name__ == '__main__':
    main()

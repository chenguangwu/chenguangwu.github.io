#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'hotel')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'hotel')
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
    out = {'slug': slug, 'industry': 'hotel', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
# -*- coding: utf-8 -*-
def main():
    write('itinerary-planner', build('itinerary-planner', [
        '📏 Itinerary Time Allocation',
        'Optimize travel time allocation by total days and attraction priority, balancing sightseeing and rest',
        'Core formula (from input variables): max(minHours, s.hours); totalHours × 0.15; avgHours × 0.5',
        '📖 Read the "Itinerary Time Allocation User Guide"',
        'Effective sightseeing hours per day',
        'Number of attractions',
        'Average time per attraction (hours)',
        'Attraction priority (1-5 stars)',
        'Allocated time',
        '📐 Allocation logic',
        'Total available hours',
        '= total days × effective sightseeing hours per day',
        'Weighted by priority',
        ': higher-priority attractions get more time',
        'Buffer time',
        ': 15% reserved for transport and rest',
        'Keep to 3 attractions per day or less to avoid an over-packed itinerary.',
        '📚 Deep dive: itinerary time allocation planning',
        'Before a free trip, allocate available hours by attraction priority (weights) based on total days and effective daily hours, and auto-reserve meal and rest buffers so the plan is neither too rushed to be a superficial tour nor too loose to waste time.',
        'When traveling with elderly people or children, lower daily net sightseeing hours (leaving more rest) and spread high-exertion attractions by weight to reduce fatigue.',
        'With multi-city transfers, subtract transport and check-in buffers first, then allocate the remaining days by city weight so no single city is rushed.',
        'Worked example (5-day city trip, 3 attractions)',
        'Total days 5, effective sightseeing 8 h/day, 3 h/day reserved for meals and rest → net 5 h/day, total net 25 h. Attraction weights 3:2:1 (total weight 6): A = 25×3/6 ≈ 12.5 h, B = 25×2/6 ≈ 8.3 h, C = 25×1/6 ≈ 4.2 h, i.e. A gets 2.5 days, B 1.7 days, C 0.8 days. If a day includes cross-city transport, subtract the transport time from that day net hours before allocating.',
        'Why is the buffer estimated at 3 h?',
        'An empirical value: three meals about 2 h + rest/queue/unexpected 1 h; with children or elderly you can raise it to 4-5 h. The buffer is the deduction in "daily net sightseeing = daily hours - buffer", so increasing it shortens every attraction proportionally.',
        'How do I set the weights?',
        'Give 3/2/1 for "must see / want to see / optional", or adjust by ticket cost or uniqueness. Weights only affect the proportion of allocated time, not the total available hours.',
        'About "Itinerary Time Allocation"',
        'The Itinerary Time Allocation tool optimizes travel time allocation by weighted priority based on total days, daily sightseeing hours and attraction priority, and reserves buffer time to balance sightseeing and rest.',
        'Weighted allocation by priority',
        'Automatic buffer reservation',
        'Visualized time proportions',
        'Itinerary density hints',
        'Travel itinerary planning',
        'Multi-attraction time allocation',
        'Free-trip pacing control',
        'Group travel arrangements',
    ]))

    write('occupancy-revpar', build('occupancy-revpar', [
        '🧮 Occupancy and RevPAR Calculator',
        'Compute core hotel metrics such as room occupancy, ADR (average daily rate) and RevPAR',
        'Occupancy and RevPAR Calculator',
        '/ Occupancy and RevPAR Calculator',
        '📖 Read the "Occupancy and RevPAR Calculator User Guide"',
        'Available room nights = total rooms × days; occupancy OCC = sold room nights ÷ available room nights × 100%; average daily rate ADR = total room revenue ÷ sold room nights; revenue per available room RevPAR = total room revenue ÷ available room nights = ADR × OCC. Together the three reflect hotel operating efficiency and pricing level.',
        'Total available rooms',
        'Rooms actually sold (room nights)',
        'Total room revenue (CNY)',
        'Days in the period',
        '📐 Metric formulas',
        'Occupancy (OCC)',
        '= rooms sold / rooms available × 100%',
        'ADR (average daily rate)',
        '= total room revenue / rooms sold',
        'RevPAR (revenue per available room)',
        '= total room revenue / rooms available = ADR × occupancy',
        'Reference: budget hotel RevPAR 100-200 CNY, mid-range 200-400 CNY, luxury 500-1000+ CNY.',
        '📚 Deep dive: occupancy and RevPAR calculation',
        'Daily hotel review: enter available rooms, sold rooms and room revenue to compute occupancy (OCC), ADR and RevPAR, then decide whether to push occupancy or raise rates.',
        'For revenue management decisions, compare the effect of "discount to drive volume" versus "hold price, cap volume" on RevPAR and choose the plan that grows revenue without harming the brand.',
        'When reporting to investors or owners, benchmark RevPAR against same-tier competitors to demonstrate operating efficiency.',
        'Worked example (120 rooms, 90 sold, revenue 45,000)',
        'OCC = sold/available = 90/120 = 75%; ADR = revenue/sold = 45000/90 = 500 CNY; RevPAR = revenue/available = 45000/120 = 375 CNY, and RevPAR = OCC×ADR = 75%×500 = 375 CNY (the two forms are equivalent and cross-check each other). To lift RevPAR to 400 you can raise ADR to ≈533 with occupancy unchanged, or push OCC to 80% with ADR unchanged, which requires selling 6 more rooms.',
        'What is the difference between RevPAR and ADR?',
        'ADR is the average price of sold rooms, looking only at rooms that sold; RevPAR is total revenue over all available rooms, spreading vacancies too, so it better reflects overall capacity utilization. Both should be high - with high ADR but low OCC, RevPAR can still be low.',
        'Does the available room count include owner-use rooms?',
        'No. Available rooms = physical rooms − maintenance/owner use − blocked rooms; the RevPAR denominator should use rooms that can really be sold, otherwise real performance is understated. In this tool the basis is the available room count you enter.',
        'About "Occupancy and RevPAR Calculator"',
        'The Occupancy and RevPAR Calculator quickly computes core hotel operating metrics such as occupancy (OCC), average daily rate (ADR) and revenue per available room (RevPAR).',
        'One-click computation of the three core metrics',
        'Supports multi-day periods',
        'Automatic occupancy grading',
        'Hotel operations data analysis',
        'Room revenue management',
        'Performance evaluation',
        'Industry metric benchmarking',
    ]))


if __name__ == '__main__':
    main()

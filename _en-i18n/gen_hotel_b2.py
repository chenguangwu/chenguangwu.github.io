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
    write('assessor-62', build('assessor-62', [
        '📋 Franchise (Standards / Support / Assessment) System',
        'Standards / Support / Assessment',
        '📖 Read the "Franchise (Standards / Support / Assessment) System User Guide"',
        'Hotel franchise system score = brand standards + head office support + loyalty program + supply chain + profitability (each scored 1 to 5), average = total ÷ 5; an average of 4.5 or above is an excellent franchise system, 3.5 to 4.4 is good, 2.5 to 3.4 is average, and below 2.5 is poor - in that case scrutinize head office support and the profit model.',
        'Hotel franchise system assessment (5 dimensions, 1-5 points each)',
        '1. Brand standards (VI / operations rules)',
        'Incomplete (2 points)',
        '2. Head office support (training / technology)',
        '3. Loyalty program (traffic / loyalty)',
        'Strong (5 points)',
        'Fairly strong (4 points)',
        'Weak (2 points)',
        'None (1 point)',
        '4. Supply chain (procurement / pricing)',
        'Clear advantage (5 points)',
        'Disadvantaged (2 points)',
        'No advantage (1 point)',
        '5. Profitability (return on investment)',
        'Generous return (5 points)',
        'Assess franchise system',
        '📚 Deep dive: hotel franchise system assessment',
        'Before preparing to join a hotel brand, score each of the five dimensions (brand standards / head office support / loyalty program / supply chain / profitability) to judge quickly whether the system is mature and which link is weakest.',
        'When comparing 2-3 candidate brands, score the same dimensions and values, then rank them side by side, preferring high totals with fixable shortfalls so a single highlight does not mislead you.',
        'Post-franchise annual review: re-score the same five dimensions to track whether the promised "support / supply chain" actually landed, as a basis for renewal or exit.',
        'Worked example (budget brand self-assessment)',
        'Choosing "fairly good (4 points)" for all five → total = 4×5 = 20, on a 100-point scale = 20/25×100 = 80 points. Dimension breakdown: brand standards 4, head office support 4, loyalty 4, supply chain 3 (no procurement price advantage), profitability 4. Conclusion: the system is fairly mature, the only shortfall is supply chain, so press procurement costs in negotiation; if supply chain rises to 4 points the total becomes 21 → 84 points.',
        'Are all dimensions weighted equally?',
        'This tool uses equal weights by default (each item 1-5 points, total 5-25, percentage = total/25×100). In real decisions brand standards and profitability matter more, and you can weight them subjectively in the notes, but equal weights already suffice for side-by-side comparison.',
        'Can a standalone hotel use it?',
        'Yes. The dimensions target a "franchise system", so a standalone self-run store with no head office support or loyalty program can enter "missing (1 point)" and ignore those items, using it purely as an internal standardization self-check.',
        'About "Franchise (Standards / Support / Assessment) System"',
        'Franchise (Standards / Support / Assessment) System. A free online tool processed entirely in the browser, no data uploaded, your privacy and security protected.',
    ]))

    write('checker-assessor', build('checker-assessor', [
        '⚖️ Service Quality (Inspection / Assessment / Improvement)',
        'Inspection / Assessment / Improvement',
        '📖 Read the "Service Quality (Inspection / Assessment / Improvement) User Guide"',
        'Hotel service quality score = front desk service + room cleanliness + facility condition + food and beverage service + safety management + customer satisfaction (each scored 1 to 5), average = total ÷ 6; an average of 4.5 or above is excellent, 3.5 to 4.4 is good, 2.5 to 3.4 is average and below 2.5 is poor - build the improvement plan around the lowest-scoring dimension.',
        'Hotel service quality inspection assessment (6 dimensions, 1-5 points each)',
        '1. Front desk service',
        'Poor (2 points)',
        '2. Room cleanliness',
        '3. Facility condition',
        'Intact (5 points)',
        'Damaged (2 points)',
        'Severely damaged (1 point)',
        '4. Food and beverage service',
        '6. Customer satisfaction',
        '📚 Deep dive: hotel service quality inspection assessment',
        'Monthly or quarterly store inspection: score the six dimensions (front desk / room cleanliness / facilities / F&B / safety / satisfaction) to output a total and the weakest item as an operations improvement list.',
        'During mystery guest or duty manager walkthroughs, score on site with the same 1-5 scale to reduce subjective inconsistency and enable cross-store ranking.',
        'Pre-opening benchmarking: compare a new store trial-run score with the target benchmark store and prioritize the dimensions that lag.',
        'Worked example (monthly inspection)',
        'Six dimension scores: front desk 5, room cleanliness 4, facilities 4, F&B 3 (slow serving), safety 5, customer satisfaction 4 → total = 25, percentage = 25/30×100 ≈ 83 points. The weakest item is F&B (3 points), so fix it first (streamline serving flow / add a breakfast counter); if F&B rises to 4 points the total becomes 26 → 87 points.',
        'Can the six dimensions be reweighted?',
        'Equal weights by default (total 6-30, percentage = total/30×100). F&B and safety strongly affect word of mouth and you may weight them subjectively, but keeping equal weights is recommended for cross-store inspection comparison.',
        'How often should scoring be done?',
        'Monthly routine plus immediate re-evaluation after a major complaint; two consecutive periods below 70 points (on the percentage scale) should trigger a dedicated rectification and a report to the regional manager.',
        'About "Service Quality (Inspection / Assessment / Improvement)"',
        'Service Quality (Inspection / Assessment / Improvement). A free online tool processed entirely in the browser, no data uploaded, your privacy and security protected.',
    ]))

    write('index', build('index', [
        '🏨 Hotel Management Tools',
        'Hotel Management',
        'Hotel Management Tools',
        'Enter the bill amount and tip percentage (or a service level preset) to compute the tip, the total including tip and the per-person cost after splitting, supporting different currencies and head counts - ideal for quickly estimating tips when dining abroad.',
        'Occupancy and RevPAR Calculator',
        'Occupancy and RevPAR computation',
        'Enter total travel days, effective sightseeing hours per day and attraction priority, then distribute sightseeing time by weight while automatically reserving rest and meal buffers, generating a schedule balancing check-in efficiency and fatigue level to help free travelers plan routes sensibly.',
        'Currency Exchange',
        'Manually enter the live rate from a bank or forex platform, convert amounts bidirectionally between any two currencies and generate a quick reference table - ideal for offline estimation while traveling abroad or shopping overseas; results follow the rate you enter.',
        'Hotel service quality (inspection / assessment / improvement) tool. Evaluates service inspection quality across 6 dimensions (each 1-5 points), outputs scores and improvement items, and supports hotel operations service quality improvement.',
        'Hotel franchise (standards / support / assessment) system tool. Quantitatively evaluates the standards, support and execution of a franchise system across 5 dimensions (each 1-5 points), aggregates the score and gives optimization suggestions for franchise decision reference.',
        'Recommends total carry-on and checked luggage weight ranges by trip length, travel type (business / leisure / outdoor), gender and transport mode, with a reference of common airline checked allowances, so you can judge before departure whether baggage may be overweight.',
        'About "Hotel Management Tools"',
        'This Hotel Management Tools collection gathers 7 free online tools covering the common calculation, conversion and lookup needs of hotel management. Whether you are a practitioner, a student or an ordinary user, you will find ready-to-use utilities here. Every tool runs purely in the browser; no data is uploaded to the server, so your privacy and security are protected.',
        'Hotel management tools included on this page (representative tools only):',
        'These tools help you finish common hotel management tasks fast, with no need to memorize complex formulas or convert by hand - input and you get the result.',
        'Do the Hotel Management Tools require downloads or registration?',
        'No. All Hotel Management Tools on this page are pure front-end online tools: open the page and use them right away, with no software to install, no account to register, and no data uploaded.',
        'Are the Hotel Management Tools results accurate, and is the data safe?',
        'The tools compute in your browser using public math formulas and common industry standards, so results are available instantly. All computation happens locally on your device; no data is uploaded to the server, so privacy and security are guaranteed.',
    ]))


if __name__ == '__main__':
    main()

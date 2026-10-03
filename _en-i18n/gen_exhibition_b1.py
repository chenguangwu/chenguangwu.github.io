#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'exhibition')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'exhibition')
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
    out = {'slug': slug, 'industry': 'exhibition', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # ===== analysis-61 (28) =====
    write('analysis-61', build('analysis-61', [
        '💰 Budget (cost / control / optimization) analysis',
        'Exhibition budget control and optimization',
        '📖 View "Budget (cost / control / optimization) analysis user guide"',
        'Enter one line per "cost item, budget, actual" and fill in the number of attendees. Budget execution rate = actual ÷ budget × 100%; variance = actual − budget; cost per attendee = total actual ÷ attendees, for horizontally comparing the input efficiency of different exhibitions.',
        'Attendees (persons)',
        'Cost data (each line "cost item, budget, actual")',
        'Booth fee,80000,80000\nBooth construction,50000,55000',
        'Budget analysis',
        '📚 In-depth: exhibition budget control and input efficiency',
        'Exhibitors prepare a budget before the show and check actual spending after, locating overspend items by execution rate and variance.',
        'The marketing department compares cost per attendee across multiple exhibitions to decide next year attendance portfolio and budget allocation.',
        'When a project lead optimizes costs, first see the largest overspend item and the overspend count, then compress item by item.',
        'Five-item cost trial',
        'Attendees 3000, input "Booth fee,120000,120000; Booth construction,80000,96000; Printed materials,25000,22000; Travel,40000,52000; Promotion,30000,28000", budget total 295000.00, actual total 318000.00, variance +23000.00, execution rate 107.80%, 2 overspend items, largest overspend is booth construction, cost per attendee 106.00.',
        'What is cost per attendee for?',
        'It spreads the total input across each attendee, convenient to compare exhibitions of different scale and cost structure; the lower the value the higher the customer-acquisition efficiency.',
        'At what execution rate should we alert?',
        'The tool uses two thresholds 100% and 110%: no more than 100% is budget-controllable, 100%~110% is slight overspend, over 110% is judged obvious overspend needing optimization.',
        'How to fill for a pure online exhibition with no onsite attendees?',
        'Replace attendees with online participants or leave blank; the cost-per-unit criterion changes with the denominator definition, as long as the same batch comparison stays consistent.',
        'About "budget (cost / control / optimization) analysis"',
        'Budget (cost / control / optimization) analysis. Free online tool, pure front-end processing, data not uploaded, privacy and security protected.',
        'How to use budget (cost / control / optimization) analysis',
        'What does budget (cost / control / optimization) analysis do?',
        'Exhibition budget (cost / control / optimization) analysis tool. Enter each exhibition expenditure and income, compute the cost structure by general financial rules and give control/optimization suggestions, for exhibition cost management and ROI evaluation.',
        'How to use budget (cost / control / optimization) analysis?',
        'Which scenarios is budget (cost / control / optimization) analysis suitable for?',
        'Booth fee,120000,120000',
    ]))

    # ===== analysis-pnl (42) =====
    write('analysis-pnl', build('analysis-pnl', [
        '📈 Budget (income / expense / profit-loss) analysis',
        'Income / expense / profit-loss',
        'The exhibition budget splits the account into two sides: fixed expenses are booth fee, construction, travel, materials, labor and others, spent once you exhibit; direct income includes sponsorship and ticketing, first used to offset fixed expenses. What remains must be recovered by onsite orders; the truly disposable amount per order is the net contribution after deducting product and delivery cost from the unit price. Divide the amount to be covered by the net contribution per order to get the minimum orders this show must close; divide again by expected leads and conversion rate to get the required conversion rate, reverse-checking whether the target is realistic. All calculations run locally in the browser, no data uploaded.',
        '📖 View "Budget (income / expense / profit-loss) analysis user guide"',
        'Per-order net contribution = unit price × (1 − variable cost rate); break-even orders = (fixed expense − sponsorship and ticketing income) ÷ per-order net contribution',
        'Expected valid leads (items)',
        'Order conversion rate (%)',
        'Average unit price (CNY/order)',
        'Per-order variable cost rate (%)',
        'Sponsorship income (CNY)',
        'Ticketing and other direct income (CNY)',
        'Booth fee (CNY)',
        'Construction and decoration fee (CNY)',
        'Travel and logistics (CNY)',
        'Materials and promotion (CNY)',
        'Personnel and other expense (CNY)',
        'Exhibition profit-loss analysis',
        '📚 In-depth: exhibition budget and break-even analysis',
        'At the project-initiation stage enter each expense and the expected leads,',
        'conversion rate',
        'to first see how many orders at minimum are needed to offset this show expenses.',
        'When comparing schemes replace the booth or construction budget, observe',
        'break-even',
        'order count and required conversion rate changes, judging whether the extra spend is worth it.',
        'At the review stage backfill with actual signed orders and unit price, compute the real',
        ', and compare against next show budget and conversion target.',
        'Minimum orders to close',
        'A show fixed expense 178000 CNY (booth 95000 + construction 42000 + travel 15000 + materials 8000 + personnel 18000), sponsorship and ticketing bring 57000 CNY direct income, so amount to cover = 121000 CNY. Unit price 9600 CNY, variable cost rate 58%, per-order net contribution 4032 CNY, break-even orders = 121000 ÷ 4032 ≈ 30.0 orders, converted to conversion rate about 5.77% (520 leads). Actual plan executes at 15% conversion, safety margin ample.',
        'Is upgrading the booth worth it',
        'Raising the booth fee from 80000 CNY to 130000 CNY, fixed expense rises to 213000 CNY, break-even orders rise to about 38.7, required conversion rate from 5.77% to 7.44%. If historical data shows a large booth can lift lead conversion by more than 3 percentage points, this upgrade pays off; otherwise better to put the budget into construction and samples.',
        'How to read ROI',
        'At 15% conversion, sales revenue 748800 CNY, minus variable cost 434304 CNY leaves contribution margin 314496 CNY, minus fixed expense 178000 CNY gives net profit-loss = 193496 CNY, ROI = 193496 ÷ 178000 ≈ 108.71%. Same criterion can compare across shows, but first unify "whether to include labor and travel".',
        'Here computed',
        'break-even point',
        'accurate?',
        'It is built on three estimates: conversion rate, unit price and variable cost rate; it is a planning-basis management accounting result, not equal to bookkeeping profit. To raise credibility, backfill these three with previous-show actual data rather than sales-side target values.',
        'What should the variable cost rate include?',
        'Any cost that rises with orders should be included: product cost, logistics and installation, after-sales and commission, generally also payment handling fees. Excludes sales rep fixed base salary and the show own fixed expense, which are already in fixed expense; double-counting would falsely raise the break-even point.',
        'Why have ticket and sponsorship direct income?',
        'These two incomes are unrelated to onsite orders, and can first offset fixed expense, directly affecting how many orders are needed to break even. Mixing them with order income hides the fact that "fixed sponsorship already offset most booth fee", causing distorted targets.',
        'About "budget (income / expense / profit-loss) analysis"',
        'Budget (income / expense / profit-loss) analysis. Free online tool, pure front-end processing, data not uploaded, privacy and security protected.',
    ]))

    # ===== assessor-60 (30) =====
    write('assessor-60', build('assessor-60', [
        '📋 Post-show (evaluation / report / follow-up) summary',
        'Evaluation / report / follow-up',
        '📖 View "Post-show (evaluation / report / follow-up) summary user guide"',
        'Total show investment = booth fee + construction fee + travel fee; single-lead cost = total investment ÷ valid leads; lead conversion rate = closed customers ÷ valid leads × 100%; input-output ratio ROI = (deal amount − total investment) ÷ total investment × 100%; average visitor dwell = total dwell time ÷ visitors; leads followed up by intention grade (A within 7 days, B within 2 weeks, C within 1 month).',
        'Post-show effect evaluation and follow-up summary (input-output analysis + customer follow-up)',
        'Booth fee (10,000 CNY)',
        'Construction fee (10,000 CNY)',
        'Personnel travel fee (10,000 CNY)',
        'Exhibition days',
        'Booth visitors',
        'Collected cards / leads',
        'Intentional customers',
        'Onsite signed orders',
        'Signed amount (10,000 CNY)',
        'Generate summary',
        '📚 In-depth: post-show (evaluation / report / follow-up) summary',
        'After the show, enter booth, construction and travel total cost and signed amount to immediately get',
        ', quickly judging whether this show input-output meets the target.',
        'Combine visitors, collected leads, intentional customers and onsite signed orders to measure lead',
        'conversion rate',
        'and single-lead cost, locating the acquisition-link short board.',
        'Auto-generate follow-up suggestions by ROI grade (excellent / good / average / poor), guiding the sales team to reach leads within 1 week and revisit intentional customers within 2 weeks.',
        'Post-show evaluation example',
        'Input booth fee 50000 CNY, construction 30000 CNY, travel 20000 CNY, visitors 500, leads 120, intentional 45, signed 8 orders, amount 250000 CNY, the tool outputs ROI≈1.67, total investment 100000 CNY, lead conversion rate 24%, single-lead cost about 833 CNY, and gives a "good effect" follow-up suggestion.',
        'How to compute ROI?',
        'ROI = signed amount ÷ (booth fee + construction fee + travel fee) total cost. The result is computed only from your input local data; if hidden costs are not included it is for reference only.',
        'What is single-lead cost for?',
        'Single-lead cost = total cost ÷ collected leads, for horizontally comparing the acquisition efficiency of different exhibitions, the lower the value the more economical the acquisition.',
        'About "post-show (evaluation / report / follow-up) summary"',
        'Post-show (evaluation / report / follow-up) summary. Free online tool, pure front-end processing, data not uploaded, privacy and security protected.',
    ]))

    print('body_exhibition_b1 done')

if __name__ == '__main__':
    main()

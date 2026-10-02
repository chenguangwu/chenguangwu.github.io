#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'property')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'property')
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
    out = {'slug': slug, 'industry': 'property', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('analysis-40', build('analysis-40', [
        "📖 Benchmarking (Compare / Learn / Surpass) Analysis",
        "Compare / learn / surpass",
        "📖 Read the \"Benchmarking (Compare / Learn / Surpass) Analysis\" guide",
        "Benchmarking analysis quantifies the gap between your own performance and industry or internal benchmarks to set improvement priorities:",
        "Relative gap rel = (benchmark value − own value) ÷ benchmark value; when the direction is low (lower is better, such as expense ratio or vacancy rate) the sign is inverted, so \"better than benchmark\" is negative and \"behind\" is positive.",
        "Composite gap score = mean of the |rel| values × 100%; sorting by |rel| descending takes the Top3 as priority improvement items.",
        "Benchmark comparison data (one line per row: metric, own value, benchmark value, direction; direction is high or low)",
        "Gross margin,20,28,high\nExpense ratio,15,10,low\nStaff productivity,60,80,high\nCustomer retention,70,75,high",
        "Start calculation",
        "📚 Deep dive: benchmarking (compare / learn / surpass) analysis",
        "Property companies compare key community metrics (repair response, greening compliance rate) against benchmark projects of the same tier",
        "Monthly management meetings use ticket volume and satisfaction data to find the gaps",
        "Set the benchmark value as next quarter's target to build a catch-up plan",
        "Repair response comparison",
        "The community averages 4.2 hours against a benchmark of 2.0 hours → a 2.2 hour gap, listed as the number one improvement item; the target of 3.0 hours for next quarter is set and tracked.",
        "Satisfaction benchmarking",
        "Community satisfaction is 86 points against a benchmark of 92 → a 6 point gap, located in the \"slow complaint closure\" dimension, so adopt the benchmark's 24-hour follow-up mechanism.",
        "How should benchmark projects be chosen?",
        "Pick projects in the same city and tier with similar scale and credible public data, avoiding cross-category comparisons that distort the conclusion.",
        "Is copying only the metrics enough after benchmarking?",
        "No. Analyse the processes behind the benchmark (rostering, training, follow-up) and localise the practice rather than chasing numbers alone.",
        "About \"Benchmarking (Compare / Learn / Surpass) Analysis\"",
        "Benchmarking (Compare / Learn / Surpass) Analysis. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
        "For example: Gross margin,20,28,high\nExpense ratio,15,10,low",
    ]))

    write('calc-shared-property-fee', build('calc-shared-property-fee', [
        "💰 Fee (Property Fee / Common Area) Calculator",
        "Enter floor area, gross-up coefficient, property fee unit price and payment period to compute in-unit area, common area, property fee and common area fee, plus the total payable.",
        "📖 Read the \"Fee (Property Fee / Common Area) Calculator\" guide",
        "Property fee = area × unit price",
        "Gross-up coefficient (%)",
        "Property fee unit price (CNY/㎡·month)",
        "Common area fee unit price (CNY/㎡·month)",
        "Payment period (months)",
        "1 month",
        "Custom period (months)",
        "💡 Common area = floor area × gross-up coefficient; in-unit area = floor area − common area; property fee = floor area × unit price × period; common area fee = common area × common area unit price × period.",
        "Gross-up coefficient = common area ÷ floor area, typically 15%-25% for residential and possibly higher for high-rise buildings",
        "The property fee unit price follows the property service contract and varies widely between communities",
        "The common area fee is usually calculated separately on common area, and some communities have already merged it into the property fee unit price",
        "Results are cost estimates; actual bills and the contract govern",
        "📚 Deep dive: fee (property fee / common area) calculation",
        "Homeowners self-check the monthly property fee and common energy fee payable",
        "Property service quotes quickly by area and rate",
        "Simulate the impact of a new rate on owners before a rate adjustment",
        "Residential calculation",
        "100 ㎡, property fee 2.8 CNY/㎡·month, gross-up coefficient 15%, common area fee 0.5 CNY/㎡·month → property fee 280 CNY + common area 75 CNY = 355 CNY/month.",
        "Rate change simulation",
        "Raising the rate from 2.8 to 3.2 → property fee 320 CNY, +40 CNY per month and +480 CNY per year, for public notice to owners.",
        "Does the property fee already include common area energy?",
        "Usually not, or only a basic portion; common area utilities are charged separately by coefficient or area and the contract must state this.",
        "Is area taken as floor area or in-unit area?",
        "Billing by the floor area on the title deed is the norm; a minority bill by in-unit area, so follow the contract.",
        "About \"Fee (Property Fee / Common Area) Calculator\"",
        "Online property fee and common area fee calculator that automatically computes in-unit area, common area, property fee, common area fee and total payable from floor area, gross-up coefficient, property fee unit price, common area unit price and payment period.",
        "Floor area, common area and in-unit area linked",
        "Itemised property fee and common area fee",
        "Supports multiple payment periods",
        "Itemised costs at a glance",
        "Annual property fee budget for homeowners",
        "Cost estimate before renting",
        "Property fee bill reconciliation",
        "Common area fee reasonableness assessment",
    ]))

    write('stats-manager', build('stats-manager', [
        "📊 Parking (Space Management / Fees) Statistics",
        "Space management / fees",
        "From the total number of spaces, monthly occupancy and transient parking data, compute the transient turnover rate, average daily vehicles on site, space occupancy rate and monthly revenue mix, for the property monthly report and income disclosure. Average vehicles on site is estimated from \"transient parking sessions × average parking duration ÷ 24\". Data is processed locally in the browser only and never uploaded.",
        "📖 Read the \"Parking (Space Management / Fees) Statistics\" guide",
        "Transient space turnover = transient sessions that day ÷ transient spaces",
        "Estimated monthly revenue = transient sessions × duration × unit price × 30 + monthly spaces × monthly rent",
        "From the total number of spaces, monthly occupancy and transient parking data, compute the transient turnover rate, average daily vehicles on site, space occupancy rate and monthly revenue mix, for the property monthly report and income disclosure. Average vehicles on site is estimated from \"transient parking sessions × average parking duration ÷ 24\". All data is processed locally in the browser and never uploaded.",
        "Total parking spaces (count)",
        "Monthly spaces (count)",
        "Transient sessions that day (count)",
        "Average parking duration (h)",
        "Transient unit price (CNY/h)",
        "Monthly unit price (CNY/month)",
        "📚 Deep dive: parking (space management / fees) statistics",
        "Property management reviews space utilisation, transient income and arrears monthly",
        "Reconcile the barrier system against the fee ledger to catch leakage",
        "Disclose parking income and expenses at the homeowners' meeting to justify a price rise or shared spaces",
        "Monthly report",
        "200 fixed spaces (180 rented, 20 vacant), transient monthly income 45000 CNY, arrears 8000 CNY → utilisation 90%, transient share 33%, arrears rate 1.5%.",
        "Anomaly check",
        "The barrier records 1500 transient sessions but the ledger shows 1380 → a gap of 120; check free releases and manual barrier lifts, and closing the gap could recover about 3600 CNY/month.",
        "How is space utilisation calculated?",
        "Rented fixed spaces divided by total fixed spaces, combined with transient turnover; long-vacant spaces should be repriced or converted to shared use.",
        "What to check first when fees and the system disagree?",
        "Start with free-release permissions, manual barrier lift records and monthly passes that expired without renewal, since these three leak fees most often.",
        "About \"Parking (Space Management / Fees) Statistics\"",
        "Parking (Space Management / Fees) Statistics. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
    ]))

    write('cycle-10', build('cycle-10', [
        "🔍 Inspection Routes and Cycle Planning",
        "Build inspection routes and checkpoints, schedule them automatically by cycle, record completion and compute the completion rate and issue count.",
        "Inspection (route / cycle) planning",
        "/ Inspection Route Plan",
        "📖 Read the \"Inspection Routes and Cycle Planning\" guide",
        "Route name",
        "Inspection frequency",
        "Last inspection date",
        "Add route",
        "Inspection routes",
        "Route details",
        "Delete route",
        "Checkpoint settings",
        "+ Add checkpoint",
        "Start this inspection",
        "Next inspection schedule",
        "Inspection history",
        "Inspection execution",
        "Complete inspection",
        "Next inspection day = last inspection day + cycle; anything not completed by the due date counts as a missed inspection",
        "During execution, mark each checkpoint as normal or abnormal with a note; abnormal items are counted automatically",
        "Completion rate = on-time completions ÷ required inspections; used for property service quality assessment",
        "📚 Deep dive: inspection routes and cycle planning",
        "Property engineering or security plans daily inspection points and frequencies by route",
        "The system computes the next due date and sends reminders to prevent missed inspections",
        "Increase inspection frequency in key areas (power distribution, fire protection) around holidays",
        "Cycle calculation",
        "A route with a 7-day frequency last inspected on 2026-03-10 → next due 2026-03-17; if today is 03-19 it is 2 days overdue, flagged in red for re-inspection.",
        "Route planning",
        "Route A covers the distribution room + pump room + fire hydrants (daily), route B covers corridors + car park (every 3 days) → resourcing: 1 person per day for A, rotating duty for B.",
        "How should the inspection cycle be set?",
        "Base it on risk: distribution and fire protection daily, general common areas weekly; follow the rules where regulations or the contract specify them.",
        "What if an inspection is missed?",
        "The system flags overdue items in red and the supervisor arranges a re-inspection and records the reason, preventing equipment hazards from escalating.",
        "About \"Inspection Route Plan\"",
        "An inspection scheduling tool for property and facility management that builds inspection routes and checkpoints, schedules them automatically by cycle, records completion, and computes the completion rate and issue count.",
        "Multi-route checkpoint management",
        "Automatic scheduling by cycle",
        "Inspection checklist execution",
        "Completion rate and missed-inspection reminders",
        "Daily property inspection",
        "Fire / power distribution facility inspection",
        "Inspection quality assessment",
        "Missed-inspection alerts",
        "e.g. basement fire inspection",
        "Add a checkpoint, e.g. distribution room, fire escape route...",
    ]))


if __name__ == '__main__':
    main()
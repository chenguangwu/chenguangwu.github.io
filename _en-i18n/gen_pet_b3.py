#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'pet')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'pet')
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
    out = {'slug': slug, 'industry': 'pet', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('analysis-cost-profit-1', build('analysis-cost-profit-1', [
        "💰 Cost (Control/Optimization/Profit) Analysis",
        "Control / optimization / profit",
        "A pet store or clinic's costs fall into two types: rent, basic staff wages and utility miscellaneous fees are fixed monthly expenses; grooming consumables, vaccine and drug purchases, and disposables vary with foot traffic and count as unit variable cost. Grooming margins, boarding and retail and other income can first offset fixed costs, and only the remainder must be earned back through foot traffic. Dividing the gap by the unit contribution margin gives the minimum monthly customers to break even; comparing with expected traffic shows the operating safety cushion. All calculations run locally in the browser with no data uploaded.",
        "📖 View the \"Cost (Control/Optimization/Profit) Analysis User Guide\"",
        "Unit contribution margin = average ticket − unit variable cost; break-even traffic = (monthly fixed cost − other income) ÷ unit contribution margin",
        "Expected monthly foot traffic (visits)",
        "Average ticket (CNY/visit)",
        "Unit variable cost (CNY/visit)",
        "Monthly rent (CNY)",
        "Monthly labor cost (CNY)",
        "Utilities and miscellaneous (CNY)",
        "Boarding, retail and other income (CNY)",
        "Operating profit/loss analysis",
        "📚 In-Depth Analysis: Pet Store Operating Cost and Break-Even Analysis",
        "Before opening or taking over a store, estimate rent, labor and utilities, and with expected ticket and traffic, back-calculate the minimum monthly customers to serve.",
        "Peak/off-season estimate: in peak season with high traffic value the safety margin; in off-season with low traffic compare",
        "break-even",
        "traffic, and arrange promotions or a booking system in advance to smooth fluctuations.",
        "For business-adjustment comparison, e.g. adding a grooming membership card or adjusting the ticket, first see the unit",
        "contribution margin",
        "and break-even-visits change before deciding.",
        "How many customers at minimum",
        "A store with monthly rent 14000 CNY, labor 26000 CNY, utilities 3500 CNY, plus boarding/retail income 9500 CNY; ticket 320 CNY, unit variable cost 130 CNY, so unit contribution margin 190 CNY, amount to cover = 43500 − 9500 = 34000 CNY, break-even traffic = 34000 ÷ 190 ≈ 178.9 visits. If expected monthly traffic is 380 visits, the safety margin is 201 visits, showing strong risk resistance.",
        "Can the ticket be lowered",
        "With the same data, if the grooming price drops from 320 to 280 CNY while variable cost stays 130 CNY, the unit contribution margin falls to 150 CNY and break-even traffic rises to about 226.7 visits, needing 48 more visits than before to maintain the same profit. A price cut presupposes a corresponding traffic increase; otherwise profit is directly compressed.",
        "Impact of holiday closure",
        "This store closed 5 days in February for lease maintenance; at 12.7 visits/day it served about 63 fewer visits, losing about 11970 CNY of contribution margin, yet rent and labor fixed costs are still paid, so that month likely fell below break-even. Stores with high fixed-cost share feel closures far more than small traffic swings.",
        "What exactly to enter for unit variable cost?",
        "Items that become actual consumption per customer: grooming consumables, drug and vaccine purchases, disposables, packaging, and energy consumption accrued by traffic. If pet-food retail is allocated by rented square meters it is more like a fixed cost; classify by your actual accounting basis, and the key is consistency across periods.",
        "Why list boarding and retail separately?",
        "Their cost structure and service differ and are relatively independent of traffic, so handling them first as 'other income' offsetting fixed costs is closer to reality. For precise accounting, set separate income and variable cost for boarding and fold it into the unit contribution margin.",
        "What if the calculated break-even traffic is close to expected traffic?",
        "It means almost no buffer. Consider three paths: raise the ticket or lower unit variable cost to lift the contribution margin, develop stable income not dependent on store visits (membership cards, boarding packages), or negotiate variable rent with the landlord to convert some fixed cost into variable cost.",
        "About Cost (Control/Optimization/Profit) Analysis",
        "Cost (control/optimization/profit) analysis. A pet-care tool that helps compute pet diet and health metrics.",
    ]))

    write('checker-16', build('checker-16', [
        "⚖️ Pet Business Compliance Check",
        "Check each compliance item, and the system automatically evaluates qualification completeness, regulatory compliance and inspection pass rate, giving a compliance grade and remediation advice.",
        "Compliance (qualification / regulation / inspection) assurance",
        "/ Compliance (qualification / regulation / inspection) assurance",
        "📖 View the \"Pet Business Compliance Check User Guide\"",
        "Weighted evaluation by three groups (qualification completeness, regulatory compliance, inspection pass rate): each group's score rate = sum of weights of its met items ÷ total group weight × 100%; composite score = sum of each group's score rate × its weight; a pass rate ≥90% is grade A, 75%–89% B, 60%–74% C, below 60% D (must remediate); unmet items are listed by remediation priority in descending weight.",
        "Business type",
        "Veterinary clinic",
        "Pet sales / breeding facility",
        "Pet grooming shop",
        "Pet boarding center",
        "I. Qualification certificates (required)",
        "Business license (scope covering pet-related)",
        "Animal diagnosis/treatment license (required for clinics)",
        "Animal epidemic-prevention certificate",
        "EIA approval / discharge permit",
        "Fire-safety inspection certificate",
        "Staff health certificate",
        "Licensed veterinarian certificate (clinics)",
        "II. Regulatory compliance (management norms)",
        "Complete animal in/out registration ledger",
        "Complete vaccination records (rabies, etc.)",
        "Husbandry environment meets animal-welfare standards",
        "Harmless waste-disposal agreement",
        "Clear pricing / standardized service contracts",
        "Customer privacy protection measures",
        "Food / feed source traceability records",
        "Regular regulatory training",
        "III. Daily inspection (operation norms)",
        "Regular premises disinfection records",
        "Daily animal-health patrol records",
        "Isolation-area setup and use norms",
        "Medical-waste sorted disposal",
        "Ventilation / temperature-humidity control up to standard",
        "Complaint-handling mechanism and records",
        "Emergency plan (epidemic / fire / escape)",
        "Qualification certificates are hard requirements; missing them directly affects the compliance judgement",
        "The animal diagnosis/treatment license is needed only for clinics; other types can skip it",
        "Each inspection item is scored by weight; total 100 points",
        "Compliance grade: ≥90 excellent, 75–89 good, 60–74 fair, <60 fail",
        "📚 In-Depth Analysis: Pet Business Compliance Check",
        "Before opening or for annual review of a pet shop / kennel / cattery, check each qualification, regulatory and daily-inspection item to quickly get the compliance total score and grade.",
        "For chain stores doing store self-checks, use unified weights (qualification 40% / regulation 35% / inspection 25%) to compare compliance across stores.",
        "Remediation tracking: first fill the missing qualification items (hard 85% threshold), then raise regulatory and daily-inspection pass rates, reaching standard step by step.",
        "Example: three-factor weighted scoring",
        "Qualifications complete (completeness 100% → 40 pts), regulation 80% (→28 pts), daily 70% (→17.5 pts): composite = 40+28+17.5 = 85.5 → 86 pts, judged 'compliant-good'. If qualification completeness is below 85%, regardless of total score it is directly judged 'fail (missing qualification)'.",
        "Why does incomplete qualification directly fail?",
        "Qualification certificates (business license, animal-epidemic-prevention certificate, etc.) are preconditions for operation. The tool sets qualification weight 40% with an 85% hard threshold; below it is judged fail, avoiding the 'high score but no license' compliance illusion.",
        "How is the composite score computed?",
        "Composite = qualification completeness × 40 + regulatory compliance × 35 + inspection pass rate × 25 (each rate 0–1), rounded to integer; grades are excellent (≥90) / good (≥75) / fair (≥60) / fail.",
        "About Pet Business Compliance Check",
        "A pet business compliance-check tool covering three dimensions (qualification, regulation, daily inspection) with 22 items, supporting four business types (clinic / sales-breeding / grooming / boarding), auto-computing the compliance score and giving remediation advice.",
        "Three-dimension weighted scoring (qualification 40% + regulation 35% + inspection 25%)",
        "Four business types with adaptive check items",
        "Hard qualification threshold with veto",
        "Item-by-item pass / missing status",
        "Auto compliance-grade judgement and remediation advice",
        "New pet-shop compliance self-check",
        "Veterinary clinic annual-review prep",
        "Pre-assessment before regulator inspection",
        "Unified compliance standard for pet chains",
    ]))


if __name__ == '__main__':
    main()

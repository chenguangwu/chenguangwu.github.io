#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'usedcar')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'usedcar')
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
    out = {'slug': slug, 'industry': 'usedcar', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('recorder-maintenance', build('recorder-maintenance', [
        "🚙 Maintenance Record (completeness) Bonus",
        "Enter maintenance records and auto-assess completeness and its effect on used-car residual value",
        "\"Enter maintenance records and auto-assess completeness and its effect on used-car residual value\" runs on the input parameters and outputs the result.",
        "📖 View the \"Maintenance Record (completeness) Bonus User Guide\"",
        "Vehicle valuation (CNY)",
        "➕ Add maintenance record",
        "Maintenance date",
        "Mileage (km)",
        "Spark plug",
        "Battery",
        "Cost (CNY)",
        "Repair shop type",
        "4S store",
        "Repair shop",
        "📋 Export maintenance report",
        "📖 Scoring notes",
        "Effect on residual value",
        "Value add about 10–15%",
        "Value add about 5–10%",
        "Value add about 0–5%",
        "Possible devaluation",
        "Scoring basis:",
        "Computed by the actual record coverage of the maintenance items that should be done by current mileage (engine oil, filter, spark plug, brake fluid, transmission oil, coolant, timing belt, etc.). 4S-store records weigh slightly higher than repair-shop records.",
        "💡 A complete maintenance record is an important value-add for used-car premium. A car with all-4S records + on-time maintenance usually retains 5–15% more than a no-record car.",
        "📚 In-Depth Analysis: Maintenance Record (completeness) Bonus",
        "Before selling, organise each maintenance detail (item, mileage, cost, 4S store or repair shop) and quantify maintenance completeness.",
        "Assess the value-add effect of complete maintenance records on",
        "used-car residual value",
        "as a basis for packaging selling points.",
        "Generate an exportable / printable maintenance assessment report to prove condition credibility to buyers.",
        "Example: current mileage 60k km, all expected maintenance items covered and all 4S-store records",
        "Completeness score is by expected-item coverage (4S-store weight 1.0, repair shop 0.85); full coverage and standard records give score>90, grade \"excellent\". Residual value-add ratio taken as +12.5%: if vehicle valuation is 100k CNY, the maintenance bonus ≈ +12.5k CNY, adjusted residual ≈ 112.5k. If only half the items are covered, score falls in 50~70, only +2.5% (+2.5k).",
        "How does the completeness score affect residual value?",
        "Score>90 → residual +12.5%, ≥70 → +7.5%, ≥50 → +2.5%, otherwise -5%. 4S-store records weigh higher than ordinary repair shops (1.0 vs 0.85); continuous, on-time records within the maintained mileage add more. This ratio is only empirical; actual premium also depends on brand and condition.",
        "What if records are incomplete?",
        "You can back-fill known maintenance (noting the source); missing items lower the coverage score; it is advised to complete 4S electronic records or invoices as much as possible. The tool supports entering multiple records and judging \"done or not\" by current mileage; items not yet due are not counted as missing.",
        "The residual estimate is for reference only; actual deal price is subject to condition and market",
        "About Maintenance Record (completeness) Bonus",
        "Maintenance-record completeness tool helps enter vehicle maintenance details (item, mileage, cost, 4S store / repair shop), computes a maintenance completeness score by current mileage, and estimates the value-add effect on used-car residual, supporting report export.",
        "Auto-account completeness by mileage",
        "4S store vs repair shop classified records",
        "Four-level rating (excellent / good / fair / poor)",
        "Residual value-add estimate",
        "Missing maintenance item hints",
        "One-click export maintenance report",
        "Organise maintenance records before selling",
        "Used-car valuation reference",
        "4S store vs repair shop record comparison",
        "Car-keeping cost statistics",
        "e.g. 2018 Corolla",
        "e.g. 40000",
        "e.g. 600",
    ]))

    write('tester-12', build('tester-12', [
        "📝 Electrical (function / fault) Test",
        "Used-car electrical-system test checklist covering 14 electrical functions such as lights, wipers, windows, AC, audio and charging, generating a fault-diagnosis report",
        "Core formula (by input variable): Math.round(totalScore÷totalWeight)",
        "📖 View the \"Electrical (function / fault) Test User Guide\"",
        "Electrical function test checklist",
        "Test each electrical function and select the result (normal / intermittent fault / complete fault); the system auto-assesses the electrical-system condition",
        "Battery voltage (V, off state)",
        "Battery voltage (V, running state)",
        "Generate test report",
        "📚 In-Depth Analysis: Electrical (function / fault) Test",
        "Before buying, test 14 electrical functions of the system: lights, wipers, windows, AC, audio, charging, etc.",
        "Combine battery and charging voltage to judge power-system health and locate occasional / constant faults.",
        "Output a fault-diagnosis report distinguishing \"confirmed fault\" from \"intermittent fault\" for easier bargaining.",
        "Example: battery 12.4V, charging 14.2V, AC not cooling, right-rear window occasional stutter",
        "Battery 12.4V and charging 14.2V are in the normal range, power system healthy; 14 functions ticked one by one, AC not cooling counted as \"confirmed fault\", right-rear window occasional stutter counted as \"intermittent fault\". The report summarises fault and intermittent items, giving the diagnosis: power OK, but AC needs repair and the right-rear window motor may be aging. Such clear fault points can be used directly to push price down or demand reconditioning.",
        "What battery and charging voltages are normal?",
        "Static off battery voltage about 12.2~12.8V is normal; below 12.0V may mean undercharge or aging; running charging voltage about 13.8~14.6V is normal alternator output. Abnormal values on either often point to battery or alternator failure. Specific thresholds follow the model manual.",
        "Why is intermittent fault listed separately?",
        "Intermittent (occasional) faults are hard to reproduce, costly to fix and easy to hide; the tool counts them separately from \"confirmed fault\" to remind buyers to reserve repair uncertainty; confirmed faults can be directly deducted from pricing.",
        "Electrical testing is advised with the engine running to ensure normal power supply",
        "Intermittent faults may be wire-harness contact issues or module problems and need further diagnosis",
        "Battery voltage reference: off ≥12.4V normal, running 13.8–14.4V means charging normal",
        "About Electrical (function / fault) Test",
        "Used-car electrical-system test tool covering 14 electrical functions such as lighting, comfort, instrument aids, combined with battery and charging-system voltage detection, generating a fault-diagnosis report and repair-cost estimate.",
        "14 electrical functions tested item by item",
        "Three-level judgement (normal / intermittent fault / complete fault)",
        "Battery / charging-system voltage analysis",
        "Fault repair-cost estimate and purchase advice",
        "Pre-purchase electrical inspection",
        "Pre-repair fault troubleshooting",
        "Electrical-system maintenance assessment",
    ]))

    write('usedcar-valuation', build('usedcar-valuation', [
        "🚙 Used Car Valuation",
        "Estimate a used-car reference price by new-car price, age and mileage.",
        "/ Used Car Valuation",
        "📖 View the \"usedcar-valuation User Guide\"",
        "Condition-rate valuation: age condition rate = 1 − age × 5%; mileage condition rate = 1 − mileage (10k km) × 3%; the composite condition rate takes the smaller of the two and is limited to 45% to 100%; valuation = new-car price × composite condition rate, then floats up/down by condition to form a residual range.",
        "New-car manufacturer guide price (CNY)",
        "Accumulated mileage (10k km)",
        "Estimated amount",
        "📚 In-Depth Analysis: Used Car Valuation",
        "Quickly estimate residual before buying/selling: enter new-car price, registration age and accumulated mileage to get the condition rate and valuation range.",
        "Compare valuations of different age / mileage combinations to judge whether the current car's quote is reasonable.",
        "Serve as a rough reference baseline for trade-in subsidy or insurance loss assessment.",
        "Example: new-car price 200k CNY, age 4 years, accumulated mileage 80k km",
        "Age depreciation rate = 1-4×0.05 = 0.80; mileage depreciation rate = 1-8×0.03 = 0.76; take the smaller and limit to 0.45~1 → condition rate 0.76 (76%); valuation = 200000×0.76 = 152k CNY. If age is only 3 years and mileage 50k km, condition rate 0.85, valuation about 127.5k+ (150k new corresponds to 127.5k).",
        "Why take the smaller of age and mileage condition rates?",
        "Vehicle residual is constrained by both \"age depreciation\" and \"mileage depreciation\"; whichever dimension worsens pulls value down, so the smaller one is taken (with a 0.45 floor to prevent zeroing) as the composite condition rate. Mileage unit is 10k km.",
        "Does the valuation differ a lot from the actual deal price?",
        "This tool is a linear simplified depreciation model that does not count brand retention, condition, regional market, configuration or accident history. The actual deal should follow the market same-model deal price and professional inspection; this valuation is only a quick baseline reference.",
    ]))

    write('wear', build('wear', [
        "📏 Mileage Wear Correction",
        "Compare actual mileage with the age-based reference mileage, compute the excess-mileage charge and value-adjustment ratio, and judge whether wear is in the normal range, for residual assessment and leasing-return settlement.",
        "Core formula (by input variable): -min(0.25,deviation×0.30); min(0.05,-deviation×0.05); max(0,expected-odo)",
        "📖 View the \"Mileage Wear Correction User Guide\"",
        "Odometer reading (km)",
        "Annual reference mileage (km/year)",
        "Excess-mileage unit price (CNY/km, leasing settlement)",
        "Vehicle valuation (CNY, for value adjustment)",
        "Normal wear tolerance band (±%, default ±20%)",
        "💡 Expected mileage = annual base × age; mileage deviation rate = (actual − expected) ÷ expected; excess mileage is charged by unit price and value is adjusted by the deviation ratio.",
        "Within the normal wear band usually no extra deduction (subject to contract)",
        "Excess-mileage charges are mostly used for finance leasing and long-rental return settlement",
        "Under-mileage vehicles may get a slight premium but have a usage floor",
        "Odometer-rolled cars are fraud; this tool assumes the odometer is genuine",
        "📚 In-Depth Analysis: Mileage Wear Correction",
        "Leasing-return settlement: compare actual mileage with age-based reference mileage, compute excess-mileage charge and value adjustment.",
        "When assessing residual, correct \"odometer-rolled / under-driven\" deviation: convert actual mileage into its effect ratio on valuation.",
        "Used-car acquisition judges whether wear is normal (whether deviation is within the tolerance band).",
        "Example: odometer 150k km, age 5 years, annual base 20k km, excess rate 1 CNY/km, original value 100k CNY, tolerance 30%",
        "Expected mileage = 2×5 = 100k km; actual 150k exceeds by 50k km; mileage deviation rate = (15-10)/10 = +50% (exceeds the 30% tolerance band, judged \"over mileage\"). Excess-mileage charge = 50k×1 = 50000 CNY; value adjustment ratio = -min(25%, 50%×0.30 = -15%) = -15%, i.e. original 100k minus 15k → adjusted valuation 85k. In leasing, an extra 50k excess charge is also due.",
        "What is the ceiling of value adjustment?",
        "On excess mileage, every 10% over deducts about 3% value (deviation rate × 0.30), capped at -25%; on under mileage, every 10% under adds about 0.5% value (absolute deviation rate × 0.05), capped at +5%. This both penalises severe excess mileage and rewards low-mileage sources.",
        "What is the tolerance band (tol) for?",
        "tol is the allowed normal deviation ratio (e.g. 30%); deviation within this band is judged \"normal wear\" and does not adjust value; only beyond it is charged or adjusted. Once the lease contract sets the tolerance, this parameter directly maps to the contract threshold.",
        "About Mileage Wear Correction",
        "Mileage wear correction tool compares actual mileage with age-based reference mileage, computes the excess-mileage charge and value-adjustment ratio, and judges normal / over-mileage / under-mileage wear states, for residual assessment and finance-lease return settlement.",
        "Expected mileage and deviation-rate calculation",
        "Excess-mileage charge billing",
        "Value adjusted by ratio",
        "Normal / abnormal wear judgement",
        "Finance-lease return settlement",
        "Used-car residual correction",
        "Condition assessment aid",
        "Long-rental contract mileage audit",
    ]))


if __name__ == '__main__':
    main()
#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'procurement')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'procurement')
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
    out = {'slug': slug, 'industry': 'procurement', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('stats-on-time-qualified', build('stats-on-time-qualified', [
        "📊 Arrival On-time Rate and Pass Rate Statistics",
        "Online tool for arrival on-time rate and pass rate statistics",
        "📖 View \"Arrival On-time and Pass Rate Statistics Guide\"",
        "📐 Calculation Principle",
        "Enter total purchase batches, on-time arrival batches, and quality-qualified batches to automatically compute on-time rate, pass rate, and on-time-and-pass rate (estimated under independence assumption), for supplier performance evaluation. Calculation is done locally in the browser.",
        "Total Batches",
        "On-time Arrival Batches",
        "Quality-qualified Batches",
        "📚 In-Depth Analysis: Descriptive Statistics",
        "Statistics on various quality values from arrival inspection (e.g. moisture content, strength) to see mean and dispersion, assessing incoming material consistency.",
        "Paste the raw sample counts or scores of multiple batches' pass rates into a number series, and use",
        "to judge whether quality is stable.",
        "In the supplier's monthly performance summary, perform on key quality indicators",
        "descriptive statistics",
        ", as input for grading and improvement.",
        "Example: \"8 batches of arrival quality scores\"",
        "Input 10,20,30,40,50,60,70,80 → sample size n=8, sum=360.00, mean=45.00,",
        "=45.00, range=70.00, variance=525.00, standard deviation=22.91. A large standard deviation indicates obvious quality fluctuation across batches; trace the source of differences (different origins/batches).",
        "What is the difference between this tool and the on-time rate statistics?",
        "Both share the same core; both are descriptive",
        ", differing only in application scenario: one leans toward delivery data, the other toward quality data. The real on-time/pass rates must first be computed by you into ratios or scores, then pasted in to statistically analyze distribution and fluctuation.",
        "Can the statistical results be used directly for appraisal?",
        "Descriptive statistics reflect the concentration and dispersion characteristics of the data itself and can serve as a quantitative basis for appraisal, but the appraisal caliber (weights, pass line) must be separately specified by the enterprise. The tool runs purely front-end, data does not leave local, suitable for quick internal estimation.",
        "About \"Arrival On-time and Pass Rate Statistics\"",
        "Arrival On-time and Pass Rate Statistics. Free online tool, pure front-end processing, no data uploaded, protecting privacy and security.",
    ]))
    write('supplier-score', build('supplier-score', [
        "📋 Supplier Composite Scoring",
        "Weighted scoring across four dimensions — quality, price, delivery, service — with automatic ranking to select the best supplier",
        "Supplier Scoring",
        "/ Supplier Scoring",
        "📖 View \"Supplier Composite Scoring Guide\"",
        "Composite score = quality × delivery × price × service",
        "Score Weight Settings (%)",
        "Quality Weight",
        "Price Weight",
        "Delivery Weight",
        "Service Weight",
        "Supplier Scores (each 0-100)",
        "➕ Add Supplier",
        "📊 Composite Score Ranking",
        "Supplier",
        "Price",
        "Delivery",
        "Composite Score",
        "📈 Dimension Comparison Chart",
        "📚 In-Depth Analysis: Supplier Composite Scoring",
        "Annual supplier performance ranking: enter four uniformly-calibrated scores (quality/price/delivery/service), set weights for automatic ranking and grading.",
        "Sourcing selection: score several newly introduced candidate suppliers and select the best by composite score as the basis for sourcing.",
        "KPI appraisal: substitute the quarterly four-dimension scores to track each supplier's ranking changes and weak dimensions.",
        "Example: \"suppliers A/B/C/D, weights quality 30/price 20/delivery 30/service 20\"",
        "Data: A(92,85,88,90), B(88,95,92,82), C(85,90,78,88), D(78,88,85,92), weights normalized to 0.3/0.2/0.3/0.2. Composite scores: A = 92×0.3 + 85×0.2 + 88×0.3 + 90×0.2 = 89.0; B = 88×0.3 + 95×0.2 + 92×0.3 + 82×0.2 = 89.4; C = 85×0.3 + 90×0.2 + 78×0.3 + 88×0.2 = 84.5; D = 78×0.3 + 88×0.2 + 85×0.3 + 92×0.2 = 84.9. Ranking: B (89.4) > A (89.0) > D (84.9) > C (84.5); B is the best overall (≥90 excellent, ≥80 good).",
        "What if the weights do not sum to 100%?",
        "The tool auto-normalizes: actual weight = your weight / sum of four, so you need not manually reach 100%. The page shows 'weight total' and hints whether it equals 100% for easy checking; even if not fully filled it scales proportionally (defaults to equal weight when all are 0).",
        "How do the four dimension scores come from?",
        "Quality/price/delivery/service are each normalized scores of 0-100, mappable from enterprise appraisal rules (e.g. pass rate → quality score, quote competitiveness → price score, on-time rate → delivery score, response and after-sales → service score). Always use scores of the same scale, so cross-dimension comparison is meaningful.",
        "About \"Supplier Scoring\"",
        "Supplier Scoring is an online tool in the business office domain. Business office tool, improves efficiency, data processed locally to protect privacy.",
    ]))
    write('wuliu-yunshufangshi-yunfei-bidui', build('wuliu-yunshufangshi-yunfei-bidui', [
        "🚚 Logistics (Transport Mode/Freight) Comparison",
        "Estimate freight by transport distance and cargo weight using road/rail reference unit prices and compare, assisting transport mode selection.",
        "📖 View \"Logistics (Transport Mode/Freight) Comparison Guide\"",
        "Freight ≈ distance × weight × unit price; road 0.5 CNY/(ton·km), rail 0.25 CNY/(ton·km)",
        "Freight grows linearly with distance and weight: estimated at reference unit prices (road 0.5, rail 0.25 CNY/ton·km, 1 ton = 1000 kg), road freight = distance × weight × 0.0005, rail × 0.00025. Compare unit costs of different modes and choose an economical scheme combined with timeliness.",
        "Transport Distance (km)",
        "Cargo Weight (kg)",
        "💡 Freight ≈ distance × weight × unit price; road 0.5, rail 0.25 CNY/(ton·km).",
        "📚 In-Depth Analysis: Logistics (Transport Mode/Freight) Comparison",
        "Express vs LTL price comparison: fill the express quote and LTL quote of the same shipment into A and B respectively, and see the difference and proportion to judge how much cost is conceded for timeliness.",
        "FTL vs LTL cost comparison: bulk goods via FTL vs shared LTL, compare unit freight to determine the break-even shipment volume.",
        "Domestic vs overseas warehouse fulfillment cost comparison: fill the per-unit fulfillment cost of both schemes to quantify the cost gap, assisting channel selection.",
        "Example: \"",
        "express freight",
        "120 CNY vs LTL freight 80 CNY\" example",
        "A=express 120, B=LTL 80: ratio (A/B)=120/80=1.5000, difference=40.00, A as % of B=150.00%, average=100.00, larger=express. Conclusion: choosing LTL saves 40 CNY (about 33%), at the cost of slower timeliness, suitable for non-urgent goods.",
        "Is comparing freight alone enough?",
        "Not enough. Freight is only part of total fulfillment cost; also consider timeliness (affecting inventory and sales), damage rate, MOQ/minimum charge, and whether pickup and insurance are included. This tool does 'same-caliber numerical comparison' to help you see the cost difference; decisions still need to integrate other dimensions.",
        "Should the comparison keep the same caliber?",
        "Yes. The A and B values should be costs under the same goods, same route, same billing unit (e.g. both 'per-piece door price' or both 'per cubic meter'); otherwise the ratio is meaningless. Labels can be manually changed to specific scheme names (e.g. express/LTL) for readability.",
        "About \"Logistics (Transport Mode/Freight) Comparison\"",
        "Logistics (Transport Mode/Freight) Comparison. Free online tool, pure front-end processing, no data uploaded, protecting privacy and security.",
        "Transport Mode",
        "Freight",
    ]))
if __name__ == '__main__':
    main()

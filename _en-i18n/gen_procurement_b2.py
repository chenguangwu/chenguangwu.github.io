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
    write('eoq', build('eoq', [
        "🛒 Economic Order Quantity (EOQ)",
        "Calculate the optimal order quantity that minimizes the sum of procurement cost and inventory holding cost",
        "Economic Order Quantity",
        "/ Economic Order Quantity",
        "📖 View \"Economic Order Quantity (EOQ) Guide\"",
        "Unit Annual Holding Cost H (CNY)",
        "EOQ Formula",
        "D: annual demand, S: cost per order, H: unit annual holding cost",
        "Optimal Order Frequency",
        "Optimal Order Cycle",
        "(days)",
        "Minimum Total Cost",
        "EOQ model assumptions: constant demand, zero lead time, no stockouts, no quantity discounts. In practice, adjust with safety stock and lead time.",
        "📚 In-Depth Analysis: Economic Order Quantity (EOQ)",
        "Buyers compute EOQ for common materials: fill annual demand D, cost per order S, unit annual holding cost H, to directly get EOQ and order cycle.",
        "When doing annual cost-reduction estimation, compare the total cost difference between 'replenish by EOQ' and 'current experience-based bulk purchasing'.",
        "Before seasonal demand fluctuation, use average annual demand to estimate a baseline EOQ, then fine-tune order frequency by off/peak season.",
        "Example: \"D=1200, S=50, H=2\"",
        "EOQ = √(2×1200×50/2) ≈ 244.95 units; annual order frequency = 1200/244.95 ≈ 4.90 orders; order cycle = 365/4.90 ≈ 74.5 days; annual ordering cost = 4.90×50 ≈ 244.95 CNY; annual holding cost = (244.95/2)×2 ≈ 244.95 CNY; annual total cost ≈ 489.90 CNY. At the EOQ point the tool makes ordering and holding costs equal, minimizing total cost.",
        "What are the three parameters D, S, H?",
        "D = total demand in the planning period (usually one year); S = fixed cost per order (order processing, transport, inspection, etc., independent of batch size); H = annual holding cost per unit (capital, storage, loss, etc.). All three must share the same time basis and be greater than 0.",
        "What if the calculated EOQ is not an integer?",
        "EOQ is a theoretical optimum; actual order quantity should be rounded based on packaging specs, MOQ, and whole-box counts; rounding slightly raises total cost but is usually negligible. Too large a batch ties up capital, too small means frequent orders; EOQ provides a balance reference.",
        "About \"Economic Order Quantity\"",
        "Economic Order Quantity (EOQ). Business office tool, improves efficiency, data processed locally to protect privacy.",
    ]))
    write('rater-price', build('rater-price', [
        "⚖️ Supplier Composite Score Comparison",
        "Enter quality/price/delivery data for multiple suppliers, customize weights, and the system automatically calculates composite scores and ranks them, assisting procurement decisions.",
        "Supplier Composite Score (Quality/Price/Delivery)",
        "/ Supplier Composite Score (Quality/Price/Delivery)",
        "📖 View \"Supplier Composite Score Comparison Guide\"",
        "Supplier score = composite weighting",
        "Score Weight Settings (total 100%)",
        "Quality Weight (%)",
        "Price Weight (%)",
        "Delivery Weight (%)",
        "Supplier Data (compare up to 4)",
        "+ Add Supplier",
        "Quality score: outgoing pass rate (0-100 points, 100% pass = 100 points)",
        "Price score: lowest quote scored 100, scaled proportionally",
        "Delivery score: on-time delivery rate (0-100 points, 100% on-time = 100 points)",
        "Weights are customizable; the three should sum to 100%",
        "📚 In-Depth Analysis: Supplier Composite Score Comparison",
        "Compare three suppliers: fill each one's pass rate, quote, on-time rate, set quality/price/delivery weights, and automatically weight-rank and recommend the top one.",
        "Bid award: substitute the quality, quote, and delivery scores from commercial evaluation into the set weights to get a composite score assisting award decision.",
        "Price-weight sensitivity analysis: raise the price weight to see if ranking reverses, verifying how dependent selection is on price.",
        "Example: \"suppliers A/B/C, weights quality 40/price 30/delivery 30\"",
        "Data: A(pass 98.5, quote 100, on-time 96), B(95, 92, 98), C(99, 110, 92). After weight normalization quality 0.4/price 0.3/delivery 0.3, lowest price = 92 as the price full-score baseline. Scores: A = 98.5×0.4 + min(92/100, 1)×100×0.3 + 96×0.3 = 39.4 + 27.6 + 28.8 = 95.8; B = 95×0.4 + 100×0.3 + 98×0.3 = 97.4; C = 99×0.4 + (92/110×100)×0.3 + 92×0.3 ≈ 92.3. Ranking: B (97.4) > A (95.8) > C (92.3); recommended supplier B.",
        "Why is 'lowest price = 100 points'?",
        "The price dimension uses relative lowest-price mapping: the lowest quote among evaluated suppliers is the full-score baseline, and the rest are scaled by lowest price/own quote × 100, avoiding the unreasonable steep drop of 'higher quote means lower price score', while keeping price advantage at full score. If a supplier's quote is higher than the lowest, its price score decreases proportionally.",
        "How should weights be set reasonably?",
        "Strategic materials and technically complex parts should weight quality and delivery more (e.g. quality 50/price 20/delivery 30); standardized, fully competitive products can weight price more. Weights auto-normalize; the three need not sum to 100, and the tool scales proportionally. It is recommended to set them based on corporate procurement strategy and category risk.",
        "About \"Supplier Composite Score Comparison\"",
        "The Supplier Composite Score Comparison tool supports comparing up to 4 suppliers simultaneously, weighted scoring across three dimensions — quality (pass rate), price (quote competitiveness), delivery (on-time rate) — with customizable weights, automatic ranking, and procurement suggestions.",
        "Compare multiple suppliers simultaneously (up to 4)",
        "Three-dimensional weighted scoring (quality/price/delivery)",
        "Custom weights, auto-normalization",
        "Price score based on lowest quote",
        "Automatic ranking and procurement suggestions",
        "Procurement sourcing price-comparison decisions",
        "Annual supplier performance ranking",
        "Bid evaluation assistance",
        "Supplier optimization and elimination decisions",
    ]))
    write('stats-on-time-1', build('stats-on-time-1', [
        "📊 Delivery On-time Rate and Quality Pass Rate Analysis",
        "Enter four types of batch counts to compute on-time rate, good-rate, and joint pass rate",
        "📖 View \"Delivery (On-time/Defect Rate) Statistics Guide\"",
        "Enter the month's total delivery batches, on-time batches, qualified batches, and 'on-time and qualified' batches (intersection), and automatically compute on-time rate, good-rate, joint pass rate, on-time-but-defective rate, and non-compliance rate, for supplier performance appraisal.",
        "Total Delivery Batches",
        "On-time Batches",
        "Qualified Batches",
        "On-time and Qualified Batches",
        "Start Analysis",
        "📚 In-Depth Analysis: Delivery On-time Rate and Quality Pass Rate Analysis",
        "Supplier monthly appraisal: split a supplier's monthly delivery batches into four count types — total, on-time, qualified, on-time-and-qualified — and compute on-time rate, good-rate, and joint pass rate in one click as the basis for performance scoring.",
        "Arrival quality review: when there are many on-time-but-defective or not-on-time-but-qualified batches, the joint pass rate will be significantly lower than individual indicators, suggesting separate talks with delivery and quality owners.",
        "Example: 300 delivery batches in a month",
        "On-time 255 batches, qualified 270 batches, on-time-and-qualified 240 batches. On-time rate = 255/300 = 85.00%, good-rate = 270/300 = 90.00%, joint pass rate = 240/300 = 80.00%, on-time-defective rate = (255−240)/300 = 5.00%, non-compliance rate = (300−240)/300 = 20.00%.",
        "Why does on-time and qualified matter?",
        "On-time rate and good-rate may both look high individually, but only batches that are 'both on-time and qualified' truly meet delivery requirements; joint pass rate = on-time-and-qualified ÷ total batches, the strictest measure of delivery quality.",
        "How to fill the four count types?",
        "Total batches is the denominator; on-time batches are those delivered by the agreed date; qualified batches are those with no defects on arrival inspection; on-time-and-qualified must satisfy both (intersection) and cannot be simply added.",
        "About \"Delivery (On-time/Defect Rate) Statistics\"",
        "Delivery (On-time/Defect Rate) Statistics. Free online tool, pure front-end processing, no data uploaded, protecting privacy and security.",
    ]))
if __name__ == '__main__':
    main()

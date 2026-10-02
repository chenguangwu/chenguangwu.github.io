#!/usr/bin/env python3
# gen_construction_head.py — shared head for construction batches b1..bN
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'construction')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'construction')
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
    out = {'slug': slug, 'industry': 'construction', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('calc-dosage', build('calc-dosage', [
        "Flooring Usage",
        "Computes required plank count, purchase boxes and skirting by room area and flooring spec.",
        "Core formula (by inputs): Math.ceil(net x (1+p.waste/100)); p.fLen x p.fWid/1000000; Math.ceil(total/p.perBox)",
        'View "Flooring Usage User Guide"',
        "Room shape",
        "Approx. square",
        "Elongated",
        "Irregular/polygonal",
        "Plank area = length x width / 1000000 (m2); count = area / plank area x (1 + waste), round up; skirting by room perimeter.",
        "Waste: solid wood 5%-8%, laminate 3%-5%.",
        "Leave 8-12mm expansion gap between floor and wall.",
        "Skirting estimated by perimeter + 5% waste; deduct door openings.",
        "In-Depth: Flooring Usage",
        "For laminate/engineered flooring, measured area + 5%-8% waste gives purchase; elongated rooms waste less than herringbone.",
        "Tally skirting length (perimeter minus doors) and underlay area to avoid missing accessories.",
        "Compare full-box vs per-m2 pricing and pick the cheaper with waste.",
        "Flooring plank count",
        "Room 18 m2, plank 1215x195mm~0.237 m2/pc, waste 5%\nPurchase area = 18 x 1.05 = 18.9 m2\nCount = 18.9 / 0.237 ~ 80 pcs",
        "Typical waste rate?",
        "Standard 5%, herringbone/fishbone 8%-12%, irregular or narrow rooms more; this tool uses your input waste.",
        "Count joists/furring?",
        "Solid wood often uses joists; joist quantity is separate (spacing x length). This tool counts only surface flooring and common accessories.",
        "Can leftover be returned?",
        "Unopened full boxes are usually returnable per shop rules; keep 1-2 spares for damage, handle the rest per return policy.",
        "About the Flooring Usage",
        "Combines flooring spec and waste to compute plank count and boxes, and estimates skirting by room shape, completing the purchase budget in one step.",
        "Auto plank/box conversion",
        "Room shape affects perimeter",
        "Skirting with waste estimate",
        "Home flooring purchase",
        "Wood-floor project budget",
        "Skirting accessory estimate",
        "One-click material list",
    ]))
    write('calc-power-voltage', build('calc-power-voltage', [
        "Circuit Load",
        "Computes working current from total power, voltage and power factor, and recommends breaker and wire size.",
        "Core formula (by inputs): BREAKERS[BREAKERS.length-1]; p.power x p.kd; current x 1.25",
        'View "Circuit Load User Guide"',
        "Total power (W)",
        "Voltage type",
        "Demand factor Kd",
        "Single-phase I = P / (U x cos phi); three-phase I = P / (sqrt3 x U x cos phi); breaker rating >= calc current x 1.25.",
        "Demand factor reflects simultaneous use; whole-house residential ~0.6-0.8, commercial 0.7-0.9.",
        "Inductive load (motor, AC) power factor ~0.7-0.85; resistive (lighting) ~0.9-1.0.",
        "Wire size is for exposed copper; conduit or long runs need one step up.",
        "In-Depth: Circuit Load",
        "A new circuit for AC + outlets: sum device power, compute current, pick breaker and size (e.g. 2.5 mm2 copper ~16A).",
        "For long-distance supply, check wire size vs length",
        "voltage drop",
        "to prevent end-device undervoltage from failing to start.",
        "For frequent trips, back-calc overload or undersized wire to locate the fix.",
        "Circuit current",
        "Total 3500W, 220V single-phase\nCurrent I = 3500 / 220 ~ 15.9A\nPick 2.5 mm2 copper (~16-20A) + 16A/20A breaker",
        "How do wire size and current map?",
        "Rule of thumb: 1.5 mm2 ~10-13A, 2.5 mm2 ~16-20A, 4 mm2 ~25-32A (exposed, ambient). Conduit, heat or long runs derate.",
        "What voltage drop is normal?",
        "End drop usually <=5% (~11V at 220V). Exceed it and thicken the wire or shorten distance.",
        "Can I rewire myself?",
        "Not advised. Strong current risks shock and fire; must be designed, installed and accepted by a licensed electrician per GB 50054/50096.",
        "About the Circuit Load",
        "From total power, voltage type and power factor with demand factor, computes working current and auto-matches breaker rating and copper wire size, aiding distribution design.",
        "Auto single/three-phase",
        "Breaker size rounded up",
        "Wire size recommended",
        "Residential panel config",
        "Commercial load estimate",
        "Breaker and cable selection",
        "Temporary power design",
    ]))
    write('calculator-calc-area', build('calculator-calc-area', [
        "House Area Calculator",
        "Enter each room length/width to auto-compute inner total, per-room area and share, convertible to floor area.",
        'The "House Area Calculator" performs a professional calculation from your inputs and outputs the result.',
        'View "House Area Calculator User Guide"',
        "+ Add room",
        "Shared ratio (%)",
        "Room area = length x width; inner area = sum of rooms; floor area = inner area / (1 - shared ratio).",
        "Shared ratio: residential 15%-30%, commercial 30%-50%, 0 means no shared area.",
        "For half-area balconies, halve length or width when entering.",
        "Spaces under 2.2m height usually do not count as floor area.",
        "In-Depth: House Area Calculator",
        "When the contractor quotes by usable area, measure each room yourself and sum to verify the base includes water or not.",
        "For storage/",
        "furniture layout",
        "first tally usable floor area to judge if large furniture fits.",
        "For area-priced rental, reconcile by net usable area, avoiding shared area in the rent base.",
        "Inner subtotal",
        "Bedroom 4x3=12, living 5x4=20, kitchen 2.5x2=5, bath 2x1.5=3\nUsable total = 12+20+5+3 = 40 m2",
        "Usable area and",
        "floor area difference?",
        "Usable area is the net floor you can step on; floor area is the enveloping area including walls and shared parts, usually 15%-25% larger.",
        "Who accounts for wall thickness?",
        "Inner usable area usually goes to the wall substrate (no plaster expansion); this tool uses your net input; clarify the basis.",
        "Do bay windows/equipment platforms count?",
        "Rules vary; some bay windows/platforms count not at all or half; follow local survey; this tool counts only entered walkable areas.",
        "About the House Area Calculator",
        "Enter each room length/width to auto-subtotal inner area and per-room share, with shared-ratio conversion to floor area, for viewing, inspection and measuring.",
        "Dynamic room add/remove",
        "Auto share stats",
        "Shared-ratio to floor area",
        "View/inspect area check",
        "Renovation measure summary",
        "Property area review",
        "Property quote estimate",
    ]))
    write('calculator-calc-ratio-2', build('calculator-calc-ratio-2', [
        "Concrete Mix",
        "Looks up per-m3 quantities by strength grade; with pour volume computes cement, sand, stone, water totals and material cost.",
        "Core formula (by inputs): tC/1000 x p.pC + tS/1000 x p.pS + tSt/1000 x p.pSt; m.sand/(m.sand+m.stone)x100",
        'View "Concrete Mix User Guide"',
        "Pour volume (m3)",
        "Cement price (yuan/t)",
        "Sand price (yuan/t)",
        "Stone price (yuan/t)",
        "Table per-m3 quantities are empirical mixes (slump 35-50mm); total = per-m3 x volume; water-cement ratio = water / cement.",
        "This is an empirical reference; actual work must use the lab mix design.",
        "Sand ratio and water-cement ratio vary with materials and slump.",
        "Admixtures, fly ash etc. are not included; estimate separately.",
        "In-Depth: Concrete Mix",
        "For self-mixed C20/C25 blinding or small works, estimate per-m3 materials by empirical mix and check sand ratio and water-cement ratio.",
        "Compare cement use across grades and pick the mark by cost (higher is not always cheaper).",
        "When adjusting slump on site, use this tool to see how water-cement ratio affects strength, avoiding random watering.",
        "C25 reference mix",
        "Per m3 about: cement 350kg, medium sand 680kg, stone 1180kg, water 180kg\nMass ratio ~ 1 : 1.94 : 3.37, water-cement 0.51",
        "Can the mix be used directly?",
        "No. Formal works need a lab mix report, adjusted live by aggregate moisture. This tool gives empirical magnitude.",
        "What if too much water is added?",
        "Higher water-cement ratio lowers strength and risks cracking/segregation; random watering on site is a common quality hazard; control water strictly.",
        "How much differ C20 and C30?",
        "Grade gap is 10MPa, with different cement use and ratio; at large volume each step up clearly raises material and cost.",
        "About the Concrete Mix",
        "Built-in C15-C40 empirical mixes; enter pour volume to compute cement/sand/stone/water totals and estimate material cost, aiding preparation and budget.",
        "Multiple grade mixes built-in",
        "Volume auto-scales quantity",
        "Water-cement & sand ratio shown",
        "On-site mixing prep",
        "Material purchase budget",
        "Mix design reference",
        "Quick quantity estimate",
    ]))
    write('cement-mortar-ratio', build('cement-mortar-ratio', [
        'The "Cement Mortar Ratio" tool performs a professional calculation from your inputs and outputs the result.',
        "/ Cement Mortar Ratio Calculator",
        'View "Cement Mortar Ratio Calculator User Guide"',
        "Cement Mortar Ratio Calculator",
        "Masonry/plaster cement mortar has fixed mix ratios. Pick grade and total volume to auto-convert cement, sand and water amounts (weight and bags) for easy purchase.",
        "Mortar grade",
        "M5 (cement:sand = 1:5.0)",
        "Mortar volume (m3)",
        "Cement bag (kg/bag)",
        "In-Depth: Cement Mortar Ratio Calculator",
        "For M5/M7.5/M10 masonry mortar, pick cement-sand ratio by strength (e.g. 1:3-1:5) to estimate per-m3 materials.",
        "Plaster at 1:2-1:3; check sand mud content and sieving to avoid hollowing.",
        "Floor leveling uses a stiffer mix; compute per-m2 by thickness then multiply by area for total.",
        "M7.5 masonry mortar",
        "Mass ratio cement:sand ~ 1:4.5\nPer m3 about: cement 280kg, sand 1500kg, water ~300kg (by sand moisture)",
        "How to pick mortar grade?",
        "Load-bearing masonry uses M5+, plaster/leveling lower; follow design; too high a grade cracks and is uneconomic.",
        "Must sand be treated?",
        "Use medium sand with compliant mud content and sieved; excess mud weakens bond and causes hollowing.",
        "Can glue or mortar additive be added?",
        "Admixtures must follow product and code; random use lowers strength; this tool excludes admixture ratios, check separately.",
        "Common mixes: M5 cement:sand=1:5.0, M7.5=1:4.8, M10=1:4.5, M15=1:4.0",
        "Cement amount is an estimate; actual mix follows the masonry mortar design code.",
        "Sand moisture strongly affects actual water addition.",
        "For reference only; actual quantities follow design drawings and test mixes.",
        "About the Cement Mortar Ratio",
        "Gives cement mortar mass ratio and per-m3 quantity by use, aiding masonry/plaster/leveling batching.",
        "Strength grade selection",
        "Per-m3 material estimate",
        "Sand ratio control",
        "Masonry mortar batching",
        "Wall plaster estimate",
        "Floor leveling quantity",
    ]))

if __name__ == "__main__":
    main()

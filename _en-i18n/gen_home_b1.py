#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'home')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'home')
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
    out = {'slug': slug, 'industry': 'home', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # ===== furniture-layout (19) =====
    en = [
        "🛋️ Furniture Layout Planner",
        "Drag and drop furniture to simulate room layout. All calculations run locally in the browser",
        "/ Furniture Layout",
        "📖 View the usage guide for Furniture Layout Planning",
        "Furniture layout is checked by area and passage: space utilization = sum of furniture projection areas ÷ room area × 100%, recommended 40% to 60% (too low looks empty, too high looks cramped); main passage width not less than 60 cm, bedside passage 60-75 cm, sofa-to-coffee-table gap 40-50 cm, dining table clearance 75-90 cm; circulation length = sum of passage lengths between functional zones, and door swing radius must be reserved to avoid interference with furniture.",
        "🔄 Rotate",
        "🗑 Delete",
        "📚 Deep Dive: Furniture Layout Planning",
        "Before renovation, pre-place the bed, sofa and dining table on the floor plan, confirm the main passage clear width ≥60 cm and bedside clearance ≥50 cm, to avoid buying furniture that does not fit or blocks the way.",
        "Small units use the 'against-wall + multi-function' principle: bed against the long wall, desk by the window, sofa doubling as guest bed; calculate occupied area before ordering to prevent the aisle from being eaten up.",
        "Circulation check: the path from the door to the balcony/bathroom is not cut by furniture, the bed head not directly facing the bathroom door, and reserve reachable distance to switches and sockets.",
        "Example (bedroom 3.6×3.0 m)",
        "Bedroom area 3.6×3.0=10.8 m², double bed 1.8×2.0 occupies 3.6 m² (about 33%); 0.5 m aisle on each side, 0.7 m at bed foot, leaving room for 2 bedside cabinets 0.5×0.4 and a 1.2 m wardrobe. Passage clear width 0.5 m meets the standard but is tight; it is suggested to change the bed to 1.5×2.0 to free 0.3 m. The tool uses furniture bounding boxes for collision detection and occupancy estimation, giving 'fits or not + occupancy ratio'.",
        "How wide should the passage be?",
        "Adult main passage ≥60 cm, bedside clearance ≥50 cm, wheelchair/moving ≥90 cm; below 50 cm will rub legs and make bed-making hard. This tool computes clear distance by bounding box and warns when below threshold.",
        "Does it compute area utilization or placeability?",
        "Both: occupied area ratio (furniture projection /",
        ") and collision detection result (overlap or not / blocks main passage or not). It does not replace professional circulation design, only helps you rehearse with real dimensions before ordering.",
        "About 'Furniture Layout'",
    ]
    mp = build('furniture-layout', en); write('furniture-layout', mp)

    # ===== lighting-calculator (15) =====
    en = [
        "🧮 Lighting Calculator",
        "Compute required luminous flux and fixture count by room type and area",
        "/ Lighting Calculator",
        "📖 View the usage guide for Lighting Calculator",
        "📚 Deep Dive: Lighting Calculator",
        "Estimate the main lamp total luminous flux for a living room by recommended illuminance, then derive how many 800 lm downlights or what luminous-flux ceiling light to choose.",
        "Study / kitchen need higher illuminance (500 / 750 lux); at ceiling height 2.8 m, CU=0.6, MF=0.8, recompute fixture count.",
        "Open-plan office workstations use 500 lux to verify even fixture layout and no dark zones on work surfaces.",
        "Example (living room 5×4 m, illuminance 300 lux)",
        "Area 5×4=20 m², total luminous flux = area × illuminance standard ÷ (CU × MF) = 20×300÷(0.6×0.8)=20×300÷0.48=12500 lm. If a single lamp is 800 lm, need 12500÷800≈15.6→round up 16; or choose 2 ceiling lights of 6000 lm each to cover.",
        "What are CU / MF and how to set them?",
        "Utilization factor CU is the ratio of light reaching the work plane (home 0.4-0.8, light-colored ceiling takes the high value); maintenance factor MF is dust attenuation (0.7-0.9). Multiply them as denominator; the smaller, the more lamps needed.",
        "How much illuminance in lux?",
        "Reference GB 50034: living/dining 100-300, kitchen/study 300-750, bathroom 100-200 lux. The finer the activity, the higher; this tool has built-in illuminance tables per room, or manual override.",
        "About 'Lighting Calculator'",
    ]
    mp = build('lighting-calculator', en); write('lighting-calculator', mp)

    # ===== paint-calculator (18) =====
    en = [
        "📐 Paint Usage Calculator",
        "Estimate paint usage and cost from wall/ceiling area, coats and paint coverage",
        "Core formula (by input variables): Math.ceil(totalPaint ÷ bucketSize)",
        "/ Paint Usage Calculator",
        "📖 View the usage guide for Paint Usage Calculator",
        "📚 Deep Dive: Paint Usage Calculator",
        "For renovation, compute latex paint liters for two walls + ceiling, deduct door/window area to avoid buying too much and causing waste and color difference.",
        "Estimate purchase buckets by coats (2 primer + 2 top) and coverage 10-12 m²/L, avoiding running short and a batch difference on refill.",
        "Enter different rooms by surface separately (living wall / bedroom wall), price separately, control overall painting budget.",
        "Example (living wall 30 + bedroom wall 22 + ceiling 20 m²)",
        "Total 72 m², coats 2, coverage 10 m²/L → usage = 72×2÷10 = 14.4 L; 5 L/bucket needs 14.4÷5=2.88→3 buckets, unit price 280 CNY/bucket ≈ 840 CNY. Door/window deductions not counted; actual can save 1-2 buckets (each door/window about 1.5-2 m²).",
        "How to set coverage?",
        "Latex paint theoretical 10-12 m²/L/coat; dark/porous wall takes the low value; actual loss add 10%~15%. Primer and topcoat differ in coverage, recommend entering separately.",
        "Should doors/windows be deducted?",
        "It is recommended to deduct door/window area, otherwise overestimate by 1-2 buckets. This tool supports entering by surface separately and summing, closer to real purchase after deduction.",
        "About 'Paint Usage Calculator'",
        "e.g.: living room wall",
        "Area m²",
    ]
    mp = build('paint-calculator', en); write('paint-calculator', mp)

if __name__ == '__main__':
    main()

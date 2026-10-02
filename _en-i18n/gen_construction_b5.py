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
    write('radiator-calculator', build('radiator-calculator', [
        "Radiator Count",
        "By room condition and radiator type, computes heat load and required sections",
        'The "Radiator Count" performs a professional calculation from your inputs and outputs the result.',
        'View "Radiator Count User Guide"',
        "Select radiator type",
        "Exterior walls (faces)",
        "0 (no exterior wall)",
        "1 face",
        "2 faces",
        "3 faces",
        "Triple glazing / thermal-break",
        "Region",
        "Severe cold (below -30C)",
        "Cold (-10 to -30C)",
        "Hot-summer cold-winter (0 to -10C)",
        "Mild (above 0C)",
        "Compute sections",
        "Radiator spec table",
        "Output per section",
        "Height per section",
        "In-Depth: Radiator Count",
        "For radiator fixing, by ",
        "x heat index gives total W, divided by selected model section W for count, rounded.",
        "For connected living/dining, use combined area to avoid per-room under-estimate causing weak heating.",
        "For old-home add-on, compare add sections vs replace larger by joints and looks.",
        "Living/dining",
        "Area 35 m2, index 85W/m2 -> 2975W\nPick 130W/section -> 2975/130~23 sections (2 groups)",
        "Difference from estimate-volume-load?",
        "Same topic, two names; this tool leans room-based selection; core is area x heat index / section output, same result.",
        "Does floor matter?",
        "Ground/top/end units lose more heat; add 10%-20%; middle units use base.",
        "Round sections up?",
        "Yes. Radiators assemble in whole sections; round up with margin; too many waste heat/space, too few no heat.",
        "About the Radiator Count",
        "Estimates radiator sections by area and heat index, aiding heating selection and budget.",
        "Area heat-load method",
        "Section output conversion",
        "End/top unit margin",
        "Radiator fixing",
        "Living/dining combined",
        "Old-home add-on compare",
    ]))
    write('renovation-labor-cost', build('renovation-labor-cost', [
        "/ Renovation Labor Estimator",
        'View "Renovation Labor Estimator User Guide"',
        "Renovation Labor Estimator",
        "Labor is a big share of renovation budget. Enter inner area and select trades to estimate total labor by common unit prices (yuan/m2), aiding planning and quote comparison.",
        "Inner area (m2)",
        "Work items (multi-select)",
        "Demolition 25 yuan/m2",
        "Water/electric 45 yuan/m2",
        "Masonry 55 yuan/m2",
        "Carpentry 35 yuan/m2",
        "Painting 30 yuan/m2",
        "Kitchen/bath waterproof 60 yuan/m2",
        "In-Depth: Renovation Labor Estimator",
        "Under half-package, list each trade quantity (e.g. tiling m2, paint m2), times day-rate or unit price for labor total.",
        "Compare day-rate vs lump-sum; day-rate is flexible but hard to cap; lump-sum is clear but risks cutting corners.",
        "Keep labor and material separate to avoid mixed labor in full-package quotes, hard to compare.",
        "Tiling labor",
        "Tiling 60 m2, 45 yuan/m2\nLabor = 60 x 45 = 2700 yuan\nWater/electric by meter, paint by m2 separate",
        "What basis is fairest for labor?",
        "By project: tiling/paint by m2, water/electric by m, demolition by item or day; fix the basis before comparing to avoid unit traps.",
        "Why big same-city spread?",
        "Craft, season and site distance all matter; low price may hide extras; check reputation and contract.",
        "How to prevent extras?",
        "Before signing, write quantities and unit prices clearly, cap extras; this tool lists the baseline; check item by item at handover.",
        "Trade unit prices are common market medians: demolition 25, water/electric 45, masonry 55, carpentry 35, painting 30 yuan/m2",
        "Kitchen/bath waterproof is estimated by inner area; actual billed by developed area",
        "Labor excludes main and auxiliary materials; half-package/clean-package differ much",
        "For reference only; follow local contractor quotes",
        "About the Renovation Labor Estimator",
        "Roughly computes total renovation labor by trade and billing, aiding half-package comparison and contract check.",
        "Item unit-price check",
        "Day-rate vs lump-sum",
        "Labor-material separation",
        "Half-package labor items",
        "Trade rate comparison",
        "Extra-prevention check",
    ]))
    write('soundproof-material', build('soundproof-material', [
        "Soundproof Material",
        "By wall area and material type, estimates quantity and cost",
        'View "Soundproof Material User Guide"',
        "Estimates use by net wall area and material width; actual soundproofing depends on system build and seam sealing, not a single material.",
        "Select material",
        "Pick material and enter area to compute",
        "Material spec table",
        "Sheet area",
        "Reference price",
        "Sound reduction",
        "In-Depth: Soundproof Material",
        "For a street-side bedroom, measure net wall area minus openings, by mat width (e.g. 1m x 10m) for rolls plus waste.",
        "For ceiling cavity, lay absorption wool by batten grid for volume and pieces, watch fire rating.",
        "Compare single mat vs wool + gypsum cavity for quantity and sound gain, pick by value.",
        "Mat rolls",
        "Wall 16 m2, mat 1.0m x 10m = 10 m2/roll\nNeed 16 x 1.05 = 16.8 m2 -> ~2 rolls",
        "Can material alone decide isolation?",
        "No. Isolation is a mass + damping + cavity + seal system; seam leakage weakens greatly; this tool only counts material.",
        "Absorption wool vs barrier mat?",
        "Wool leans absorption/less reverberation; mat leans mass to block transmission; often combined, pick by goal.",
        "Mind fire rating?",
        "Yes. Filled materials must meet the combustion grade (e.g. A non-combustible), especially public and high-rise.",
        "About the Soundproof Material",
        "By wall/ceiling area and material width, estimates barrier mat and absorption wool for cutting.",
        "Net area calc",
        "Width-to-roll conversion",
        "Waste reserve",
        "Street-side bedroom",
        "Ceiling wool laying",
        "Build value comparison",
    ]))
    write('timber-volume', build('timber-volume', [
        "Timber Volume",
        "Log and sawn volume, with quick common-spec selection",
        'The "Timber Volume" performs a professional calculation from your inputs and outputs the result.',
        'View "Sawn Timber Volume User Guide"',
        "Log calc",
        "Sawn calc",
        "Log formula: V = pi/4 x (D1^2 + D2^2)/2 x L, D1 butt diameter, D2 small-end diameter",
        "Butt diameter D1 (cm)",
        "Small-end diameter D2 (cm)",
        "Compute volume",
        "Sawn formula: V = length x width x thickness",
        "Quantity (pieces)",
        "Log",
        "Sawn",
        "In-Depth: Timber Volume",
        "For cutting, net volume by L x W x T, then divide by recovery for log need.",
        "For inventory of boards/blocks, batch-convert volume for ledger and cost.",
        "Compare dried vs wet weight (same volume, different moisture) by use.",
        "Block volume",
        "Board 2.0m x 0.12m x 0.04m\nVolume = 2.0 x 0.12 x 0.04 = 0.0096 m3\n10 pcs = 0.096 m3",
        "How to convert volume and weight?",
        "Air-dried ~500-800 kg/m3 (by species), wet heavier; this tool computes volume; weight = species x density.",
        "Big impact from sawn tolerance?",
        "Custom stock has +/- error, accumulating in bulk; settle by actual scale; this tool uses your net input.",
        "Same algorithm for log and board?",
        "Different. Log uses small-end diameter table (see calc-5); board directly L x W x T; this tool targets sawn.",
        "About the Timber Volume",
        "By board/block section and length computes volume, for cutting, trade and inventory.",
        "L x W x T volume",
        "Log scale reference",
        "Spec summary",
        "Carpenter cutting estimate",
        "Inventory volume check",
        "Species weight conversion",
    ]))
    write('window-shading', build('window-shading', [
        "Window Shading Coefficient",
        "By solar altitude and window orientation computes shading coefficient; simplified model for reference",
        'The "Window Shading Coefficient" performs a professional calculation from your inputs and outputs the result.',
        'View "Window Shading Coefficient User Guide"',
        "Jan",
        "Feb",
        "Apr",
        "May",
        "Jul",
        "Aug",
        "Oct",
        "Nov",
        "Time (hour)",
        "South",
        "North",
        "East",
        "West",
        "Window height H (m)",
        "Window width W (m)",
        "Overhang projection P (m)",
        "Compute SC",
        "Simplified model formula:",
        "where: P=overhang projection, H=window height, alpha=solar altitude, K=orientation factor",
        "Orientation factor:",
        "South K=1.0, North K=0.3, East/West K=0.7",
        "Solar altitude:",
        "alpha = 90 - |latitude - solar declination|",
        "This is a simplified model; use professional software for actual projects.",
        "In-Depth: Window Shading Coefficient",
        "For west-sun windows add adjustable blinds; estimate post-shade SC by blade angle and height to judge afternoon heat cut.",
        "Compare fixed overhang vs movable shade in summer/winter; prefer a south solution that keeps winter sun.",
        "Before energy review roughly check window SC x external ",
        "shading coefficient",
        " for compliance.",
        "External SC",
        "Window SC 0.8, with movable external shade external SC 0.4\nCombined SC = 0.8 x 0.4 = 0.32 (much better insulation)",
        "How to compute combined SC?",
        "Combined SC = window SC x external SC, multiplied; more effective external shade gives smaller product and better insulation.",
        "Movable better than fixed?",
        "Usually yes. Adjust by season/time: block in summer, admit in winter; fixed overhang is limited for east/west low-angle sun.",
        "Difference from calc-6?",
        "Same shading topic; this tool leans window SC selection and combined factor, calc-6 leans geometric modeling; core is consistent, cross-reference.",
        "About the Window Shading Coefficient",
        "Estimates combined window SC after external shade, aiding insulation selection and energy judgment.",
        "Geometric occlusion",
        "Combined SC multiply",
        "Movable vs fixed",
        "West-sun window shade",
        "South keeps winter sun",
        "Energy-review rough check",
    ]))

if __name__ == "__main__":
    main()

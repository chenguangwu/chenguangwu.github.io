#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'woodwork')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'woodwork')
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
    out = {'slug': slug, 'industry': 'woodwork', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # ===== angle-1 (13) =====
    write('angle-1', build('angle-1', [
        '📐 Curve-saw bevel angle calculator',
        'Enter the target bevel angle, material thickness and blade type to compute the chamfer width, blade travel and blade-drift compensation, plus a compound miter/bevel conversion table.',
        'Core formulas (by input variables): min(89.9,max(0,th)); th×π÷180',
        '📚 In-depth: curve-saw bevel angle calculation',
        'Furniture chamfer and beveled-edge joints: when chamfering a panel at 45° or joining a beveled edge, first compute the face chamfer width and blade travel to confirm the blade can cut through in one pass.',
        'Crown molding / cove corner cuts: where crown meets an inside/outside wall corner, use the compound miter (Miter+Bevel) formula to convert the corner angle into the saw-table angle.',
        'Curve-saw bevel setup: a curve-saw blade tends to drift when beveling; compensate the base-plate angle by blade type so the actual cut angle stays accurate.',
        'Bevel example (45° / 20mm stock / curve saw / standard tooth / 45° crown)',
        'Face chamfer width = 20 × tan45° = 20.0 mm; blade travel = 20 / cos45° = 28.28 mm; curve-saw drift = 0.04 × 1.0 × 28.28 × sin45° = 0.80 mm, suggest raising base-plate compensation angle atan(0.80/28.28) = 1.62°. Compound miter: for 90° corner and 45° crown, saw-table miter M = atan(sin45°/tan45°) = 35.26°, bevel B = asin(cos45°×sin45°) = 30.00°.',
        'Why does a curve saw drift when beveling?',
        'A curve-saw blade is narrow and flexible; when beveling, uneven tooth load and the lateral force shift the kerf. The model uses K=0.04 multiplied by the blade factor (heavy tooth 0.5 / standard 1.0 / thin tooth 1.8) then by blade travel and sinθ to estimate drift; circular and miter saws have rigid blades so it is negligible. Compensate by locking the orbital action off, feeding slowly against a guide rail, and raising the base-plate compensation angle.',
        'How do I use the crown-angle compound-miter formula?',
        'When fitting crown molding, given wall-corner angle C and the molding own crown angle S, saw-table miter M = atan(sinS / tan(C/2)) and bevel B = asin(cosS × sin(C/2)). Use C=90° for inside corners and C=270° (or the equivalent inside angle) for outside corners; set the computed M/B directly on the saw table to complete the corner joint.',
    ]))

    # ===== calculator-calc-15 (13) =====
    write('calculator-calc-15', build('calculator-calc-15', [
        '🪵 Tenon dimension calculator',
        'Enter the stock thickness, width, tenon-thickness ratio and tenon type to compute each dimension and the mortise depth by woodworking standard ratios (tenon ≈ 1/3 thickness, tenon length ≈ 1.5× thickness).',
        'Core formulas (by input variables): tenonCount×2×cheekPer; (W-2×edge-gap)÷2; (T-tt)÷2',
        '📚 In-depth: tenon dimension calculator',
        'Furniture frame tenon-joint design: for square-stock joints in table/cabinet frames, set the tenon thickness, length and mortise depth by stock thickness to ensure strength without splitting the mortise.',
        'Door/window frames and cabinet structure: compute each tenon width and shoulder before batch cutting to avoid mortises that are too deep and nearly through.',
        'Woodworking teaching and stock reference: turn the empirical ratios (tenon ≈ 1/3 thickness, length ≈ 1.5× thickness) into a recomputable checklist for training and material prep.',
        'Blind tenon example (stock 30mm / width 80mm / ratio 1:3 / mating piece 60mm / end shoulder 6mm)',
        'Tenon thickness tt = 0.333 × 30 = 9.99 mm (card shows 10.0); single-side shoulder in thickness = (30 − 9.99)/2 = 10.00 mm; tenon length tl = 1.5 × 30 = 45.00 mm (card 45.0); blind-mortise depth md = 45 + 2 = 47.00 mm, bottom thickness = 60 − 47 = 13.00 mm (≥6mm, no warning); tenon width tw = 80 − 2×6 = 68.00 mm; single-cheek glue area = 45×68 = 3060 mm² = 30.60 cm², both-cheek total glue area = 61.20 cm², strength adequate.',
        'Why set tenon thickness to 1/3 of stock thickness?',
        'Empirically tenon thickness is 1/3 (hardwood) to 3/8 (softwood) of stock thickness, giving enough glue area without weakening the stock; too thick splits the mortise, too thin lacks shear strength. The calculator outputs tenon thickness and single-side shoulder directly from the chosen ratio for easy checking.',
        'Why keep ≥6mm bottom thickness in the mortise?',
        'Blind-mortise depth = tenon length + 2mm assembly clearance; if the bottom thickness (mating-piece thickness − mortise depth) is under about 6mm, drilling or chiseling risks reaching through and the joint splits easily under load. The calculator warns when bottom thickness is insufficient, suggesting a shorter tenon or thicker mating piece.',
    ]))

    # ===== convert-30 (18) =====
    write('convert-30', build('convert-30', [
        '🪵 Wood moisture content and shrinkage conversion',
        'Wood moisture content and shrinkage conversion online tool',
        '📚 In-depth: wood moisture content and shrinkage conversion',
        'Unify moisture-content reading units: a single batch QC sheet may show moisture content in several units at once',
        ', millipercent and decimal; use this tool to convert readings of different magnitudes into one unit to avoid misjudging dryness.',
        'Shrinkage magnitude conversion: wood shrinkage is usually given as a percentage by tangential/radial direction, but process cards record it as a decimal; convert before applying the stock allowance.',
        'Batch moisture comparison: incoming logs are sampled by wet-basis moisture content, converted to the oven-dry basis for horizontal batch comparison to decide whether to extend the conditioning period.',
        'Magnitude-conversion example (milli',
        '→ wood moisture-content unit)',
        'Input value 2500, coefficient 1, from "milli wood moisture content" (factor 0.001) to "wood moisture content" (factor 1): result = 2500 × 1 × 0.001 / 1 = 2.500000. That is, 2500 milli-moisture units equal 2.5 moisture-content units. Reverse: 2.5 moisture-content units selected "to kilo-shrinkage conversion" (factor 1000), result = 2.5 × 1 × 1 / 1000 = 0.002500, convenient for cross-table checking.',
        'What is the relationship between moisture content and shrinkage?',
        'Wood moisture content is the percentage of water mass relative to oven-dry mass; once drying continues from the fiber saturation point (about 30%) toward oven-dry, the cell-cavity water is gone and the cell walls shrink, producing linear shrinkage (tangential about 6%–12%, radial about 3%–6%). This tool only does reading-magnitude conversion, not physical shrinkage calculation.',
        'Why unify the magnitude?',
        'QC, process cards and supplier reports often use different magnitudes (percent / decimal / millipercent); subtracting directly without unifying differs by 100–1000×. Convert to one unit first, then compare, to avoid using 2.5% as 0.025 for stocking.',
        'Incoming-log moisture sampling and conditioning-period judgment',
        'Kiln-out moisture content and stock allowance accounting',
        'Cross-batch moisture-content horizontal comparison',
        'Unify shrinkage readings to the process-card decimal basis',
    ]))

    print('body_woodwork_b1 done')

if __name__ == '__main__':
    main()

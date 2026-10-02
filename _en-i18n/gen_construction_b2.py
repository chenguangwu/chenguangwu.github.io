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
    write('calc-1', build('calc-1', [
        "Scaffold Bearing Capacity",
        "Computes upright stability capacity and construction-load check for coupler-type steel-tube scaffolds.",
        'The "Scaffold Bearing Capacity" tool performs a professional calculation from your inputs and outputs the result.',
        'View "Scaffold Bearing Capacity User Guide"',
        "Tube outer diameter D (mm)",
        "Wall thickness t (mm)",
        "Steel yield strength fy (N/mm2)",
        "Lift height h (m)",
        "Effective-length factor mu",
        "Upright extension a (m)",
        "Area per upright A (m2)",
        "Construction load q (kN/m2)",
        "Plank & self-weight g (kN/m2)",
        "Effective length l0 = k x h + 2a (simplified coupler-type formula)",
        "Slenderness lambda = l0 / i, i = radius of gyration",
        "Stability factor phi from class-a section table (linear interp)",
        "Upright capacity N <= phi x A x f, f = fy / resistance factor (1.1)",
        "In-Depth: Scaffold Bearing Capacity",
        "For exterior decoration scaffolding, first estimate single-upright load at 1.5m bay, 0.9m row and 1.8m lift to judge if the tube is adequate.",
        "Before a loading platform (e.g. materials), use this tool to check if construction load exceeds the single-upright allowance, preventing local buckling.",
        "Compare lift-height effects on stability; where work space allows, reduce lift to improve safety margin.",
        "Single-upright allowable load estimate",
        "Phi48x3.0 tube, lift 1.8m, bay 1.5m\nReference allowance ~20-30kN/post (by code & couplers)\nConstruction load 2kN/m2 x 1.5 x 0.9 ~ 2.7kN/post, ample margin",
        "Can I build directly from the result?",
        "No. Scaffolding is a high-risk sub-project; it must be designed and accepted by qualified personnel per JGJ130 etc. before use.",
        "Is wind load considered?",
        "This tool estimates vertical load only; wind load, wall ties and foundation settlement need formal calculation, especially for tall scaffolds.",
        "Same for coupler and ringlock?",
        "No. Node stiffness and capacity differ greatly; follow the rules for each system. This tool gives only a general magnitude.",
        "About the Scaffold Bearing Capacity",
        "Roughly estimates single-upright allowable load by spacing and lift for pre-check; the formal scheme must be designed by certified staff per code.",
        "Upright load estimate",
        "Lift-height impact",
        "Loading-platform check",
        "Exterior scaffold pre-check",
        "Material-platform check",
        "Stability-margin assessment",
    ]))
    write('calc-5', build('calc-5', [
        "Timber Volume (Log/Sawn)",
        "Pick timber type and enter dimensions to compute volume (m3) by national standard.",
        "Core formula (by inputs): 0.7854 x L x (D+0.45 x L+0.2)^2 / 10000",
        'View "Timber Volume (Log/Sawn) User Guide"',
        "Log (GB 4814)",
        "Sawn timber (length x width x thickness)",
        "Small-end diameter (cm)",
        "Pieces",
        "Log: V = 0.7854 x L x (D + 0.45L + 0.2)^2 / 10000 (GB 4814, D small-end cm, L length m). Sawn: V = length x width x thickness (m).",
        "The log formula is the GB 4814 scaled-volume simplification; for large diameters use the official scale table.",
        "Sawn width/thickness are in mm, length in m; the tool auto-converts.",
        "Actual recovery is affected by bow and defects; allow waste.",
        "In-Depth: Timber Volume (Log/Sawn)",
        "When buying logs, estimate volume by small-end diameter and length against GB/T 4814.",
        "Log volume",
        "Cross-check the table with hand calc to avoid metering error.",
        "For cutting, find net sawn volume (L x W x T), then divide by recovery to estimate log need.",
        "For inventory, batch-convert different sizes with this tool for ledger and cost.",
        "Small-end 200mm, length 4m\nBy log formula V~0.7854 x 0.2^2 x (4+0.5)~0.113 m3",
        "Why by small-end diameter?",
        "Log taper decreases from butt to tip; the national standard uses the scaled small-end diameter as the table base for stable comparison.",
        "Can sawn and log volume be compared directly?",
        "No. Logs include bark, heartwood and processing loss; sawn is finished net stock. Apply recovery (often 40%-60%) when cutting.",
        "Is scaled length the same as actual length?",
        "Not always. Scaled length rounds per grade rules (e.g. 0.2m steps) and may differ from measured length; use scaled length for the table.",
        "About the Timber Volume (Log/Sawn)",
        "Supports both log and sawn volume: log uses GB 4814 by small-end diameter and length; sawn uses L x W x T directly, serving timber purchase and project settlement.",
        "One-click log/sawn switch",
        "Auto national-standard conversion",
        "Batch count by pieces",
        "Timber purchase settlement",
        "Timber-structure quantity",
        "Furniture material estimate",
        "Forestry scaling reference",
    ]))
    write('calc-6', build('calc-6', [
        "Shading Coefficient",
        "Estimates external shading coefficient and blocking efficiency by window orientation, solar altitude and horizontal overhang size.",
        "Core formula (by inputs): p.oh x Math.tan(p.alt x pi/180); min(1, proj/p.wh)",
        'View "Shading Coefficient User Guide"',
        "Southeast / Southwest",
        "East / West",
        "Solar altitude (deg)",
        "Overhang projection (m)",
        "Window height (m)",
        "Projection = projection x tan(altitude); block ratio = projection / window height; shading eff = block ratio x orientation factor; combined SC = 1 - shading eff.",
        "This tool uses a horizontal overhang model; vertical louvers are not covered.",
        "The orientation factor reflects how well horizontal shading works for each orientation.",
        "Solar altitude can be derived from latitude and time; enter it directly here.",
        "In-Depth: Shading Coefficient",
        "For a large south window with a horizontal overhang, estimate SC by the geometry of board width and window height to judge summer heat gain reduction.",
        "Compare SC of no-shade, interior curtain and exterior blind schemes, combined with ",
        "AC load",
        "to trade off cost and benefit.",
        "Before energy review, roughly check the combined window SC (window SC x external shade) for compliance.",
        "Horizontal overhang shading",
        "Window 1.5m, overhang 0.6m, noon altitude ~82 deg at solstice\nBlock ratio 0.6/1.5=0.4 -> blocks low-angle, weak at noon\nCombined SC ~0.5-0.7 (by construction)",
        "What does SC=1 mean?",
        "SC=1 means full heat gain with no shade (or standard glass); smaller SC blocks better; 0.3 insulates far better than 0.8.",
        "Big difference between external and internal shade?",
        "Very big. External shade blocks heat before it enters; interior curtain reflects after entry, far weaker.",
        "Does it block winter sun?",
        "Yes. A south horizontal board blocks high summer sun but admits low winter sun if designed well; east/west low-angle sun needs angled or movable shade.",
        "About the Shading Coefficient",
        "Based on the horizontal-overhang geometry, combined with solar altitude and window orientation, estimates blocking ratio and combined SC to aid building energy design.",
        "Auto geometry projection",
        "Built-in orientation factor",
        "Instant blocking-efficiency feedback",
        "Building energy preliminary design",
        "Overhang size optimization",
        "Window-wall heat-gain estimate",
        "Green-building assessment",
    ]))
    write('calc-area-lux', build('calc-area-lux', [
        "Lighting Wattage",
        "Computes the number of fixtures and total power by room area and illuminance.",
        "Core formula (by inputs): Math.ceil(totalFlux/lampFlux)",
        'View "Lighting Wattage User Guide"',
        "Illuminance (lux)",
        "Bedroom 75 lux",
        "Living room 100 lux",
        "Kitchen 150 lux",
        "Study/Office 300 lux",
        "Bench 500 lux",
        "Corridor 50 lux",
        "LED lamp (90 lm/W, 18W each)",
        "CFL (60 lm/W, 24W each)",
        "Incandescent (13 lm/W, 60W each)",
        "High-eff LED (100 lm/W, 20W each)",
        "Utilization factor CU",
        "Total flux = illuminance x area / (CU x MF); fixture count = total flux / (lamp power x efficacy); total power = count x lamp power.",
        "CU depends on room shape, reflectance and luminaire distribution, typically 0.4-0.7.",
        "MF reflects lumen decay and dust; clean space 0.8, general 0.7.",
        "Power density should stay within national limits (office ~<=9 W/m2, residential <=7 W/m2).",
        "In-Depth: Lighting Wattage",
        "For a study at 300-500lux, area x illuminance gives total lumens, divided by per-lamp lumens gives count, avoiding too dim or harsh.",
        "For workshops/kitchens at 500-750lux, verify existing lamp power is enough to prevent low task illuminance.",
        "When switching to LED, back-calc new lamp power from total lumen need (LED ~100lm/W); more accurate than reading watts.",
        "Study lamp selection",
        "Area 12 m2, target 400lux\nTotal flux = 12 x 400 = 4800 lm\nLED~100lm/W -> ~48W, split 2-3 fixtures evenly",
        "Relation between lux and watts?",
        "Lux is illuminance (light on surface), watts is power; they link via lm/W efficacy. LED has high efficacy, far fewer watts than incandescent at same lumens.",
        "Why still dim after calculation?",
        "Utilization (absorption) and maintenance (dust decay) factors were not counted; add 1.2-1.5 margin; dark walls and high ceilings also absorb light.",
        "Suitable illuminance per room?",
        "Living 100-200, study 300-500, kitchen bench 500-750, corridor 50-100 (lux); follow GB 50034.",
        "About the Lighting Wattage",
        "Based on the lumen method (average illuminance), computes fixture count and total power, with built-in lamp efficacy and typical standards, aiding lighting design and energy check.",
        "Multiple lamp efficacy options",
        "Quick illuminance presets",
        "Power-density energy hint",
        "Residential lighting design",
        "Office lighting layout",
        "Energy-retrofit assessment",
        "Fixture purchase reference",
    ]))
    write('calc-dosage-1', build('calc-dosage-1', [
        "Tile Usage",
        "Computes required tile count by room area, tile size, joint width and waste rate.",
        "Core formula (by inputs): ((p.tLen+p.gap)x(p.tWid+p.gap))/1000000; Math.ceil(net x (1+p.waste/100)); Math.ceil(total/p.perBox)",
        'View "Tile Usage User Guide"',
        "Joint width (mm)",
        "Tile-with-joint area = (length+joint) x (width+joint) / 1000000 (m2); count = area / tile area x (1 + waste), rounded up.",
        "Joint width included in tile area, closer to real layout.",
        "For odd spaces, diagonal or pattern laying, raise waste to 8%-12%.",
        "Keep 1-2 extra boxes for later breakage and color match.",
        "In-Depth: Tile Usage",
        "For kitchen/bath walls and floors, net area + 5%-10% waste gives count; small tiles and diagonal laying waste more.",
        "Estimate grout: volume by seam length/width/depth, divided by product coverage.",
        "Compare 600x600 vs 800x800 for waste and labor, then choose by look.",
        "Floor tile count",
        "Floor 20 m2, tile 800x800=0.64 m2/pc, waste 6%\nPurchase area = 20 x 1.06 = 21.2 m2\nCount = 21.2 / 0.64 ~ 34 pcs",
        "Why is waste higher than flooring?",
        "Tiles cannot be joined after cutting, and corners/pipe holes waste more; diagonal/pattern waste can reach 10%-15%. This tool uses your input waste.",
        "How to estimate grout?",
        "Seam volume ~ seam length x width x depth; total / per-pack coverage = packs, usually +10% margin.",
        "Notes for tiling floor tiles on wall?",
        "Large tiles on wall need special adhesive and back-buttering; low-absorption tiles cannot use cement-sand; this tool counts only, follow code for workmanship.",
        "About the Tile Usage",
        "Combines tile size, joint and waste to compute exact tile count and boxes, avoiding shortage or waste.",
        "Joint width in layout",
        "Custom waste rate",
        "Auto box conversion",
        "Home floor/wall tile purchase",
        "Commercial tile budget",
        "Construction layout estimate",
        "Material bidding reference",
    ]))

if __name__ == "__main__":
    main()

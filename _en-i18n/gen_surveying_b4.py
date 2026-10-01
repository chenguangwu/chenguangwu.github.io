#!/usr/bin/env python3
# surveying batch4 (9 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'surveying')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'surveying')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'horizontal-distance': [
"Rangefinder Slant Distance → Horizontal Distance",
"D = L·cos(α), α is the vertical angle.",
"Slant to Horizontal Distance",
"/ Slant to Horizontal Distance",
"📖 View the \"Rangefinder Slant Distance → Horizontal Distance User Guide\"",
"Slant distance L (m)",
"Vertical angle α (°)",
"α is the inclination relative to the horizontal plane.",
"Height difference = L·sin(α).",
"📚 In-depth: Horizontal Distance",
"Compute horizontal distance from coordinate differences.",
"Same core as coordinate-distance-2d.",
"Staking-out boundary distance.",
"Basic",
"ΔN=60, ΔE=80 → horizontal distance = √(60²+80²) = 100 m.",
"Set boundary/edge stakes by horizontal distance; on slopes reduce slant distance to horizontal first.",
"Is horizontal distance the projected distance?",
"Yes, the plane distance ignoring elevation; this is the measured horizontal distance.",
"And slant distance?",
"Slant includes elevation; horizontal = slant × sin(zenith), larger slope means bigger difference.",
],
'horizontal-from-slope': [
"Horizontal Distance from Slant Distance and Vertical Angle",
"Enter slant distance S and vertical angle v (degrees) to obtain the horizontal distance.",
"Slant-to-Horizontal Distance Calculator",
"/ Slant-to-Horizontal Distance Calculator",
"📖 View the \"Horizontal Distance from Slant Distance and Vertical Angle User Guide\"",
"Horizontal = slant · cos(vertical angle)",
"Slant distance S (m)",
"Vertical angle v (degrees)",
"Larger vertical angle gives shorter horizontal distance.",
"100·cos10° → 98.48 meters.",
"📚 In-depth: Slant to Horizontal Distance",
"Compute horizontal distance from slant and inclination.",
"Total-station slant-distance reduction.",
"Slope-side length reduction.",
"Reduction",
"Slant 100.5 m, depression 5.71% (≈ zenith 84.29°) → horizontal = 100.5×sin(84.29°) = 100.0 m.",
"At 10% slope the slant is about 0.5% longer than horizontal; at large slopes (30%) the gap reaches 15%, so reduction is mandatory.",
"Formula?",
"Horizontal = slant × cos(depression) = slant × sin(zenith).",
"What if not reduced?",
"Areas / coordinates are all overstated; on slopes the difference is significant, so reduce before computing.",
],
'leveling-calc': [
"🧮 Leveling Calculation",
"Leveling-route height difference and elevation computation, with misclosure and allowable-misclosure checking",
"📖 View the \"Leveling Calculation User Guide\"",
"H_i = H_{i−1} + backsight − foresight",
"Start elevation H₀ (m)",
"Known end elevation Hn (m, for closed leveling)",
"Allowable misclosure coefficient (mm·√km⁻¹)",
"Setup",
"Backsight a (m)",
"Foresight b (m)",
"Section distance (km)",
"Height difference (m)",
"+ Add setup",
"Height diff h = a − b (backsight minus foresight); elevation accumulates station by station. Misclosure fh = measured end elevation − known elevation; allowable misclosure = ±coefficient×√(ΣL) mm. Ordinary leveling often uses coefficient ±40.",
"📚 In-depth: Leveling Check",
"Compute and check height difference and misclosure for open/closed leveling.",
"Judge acceptance by the per-km limit.",
"Distribute height differences for adjustment.",
"Misclosure",
"Closed leveling measured Σh = +0.012 m, theory should be 0 → f_h = +12 mm; limit = ±12√L (mm, L in km), at L = 1 km the tolerance is ±12 mm, just acceptable.",
"Adjustment",
"Distribute the misclosure by station count with reversed sign; each station gets a correction −12/n mm to obtain each point's elevation.",
"What is the misclosure limit?",
"Below-standard ±12√L mm, fourth-order ±20√L mm (L in km); higher order is stricter.",
"What if over the limit?",
"First check the instrument i-angle / readings; remeasure if over limit, never force a split to hide gross errors.",
"About \"Leveling Calculation\"",
"Leveling Calculation is an online tool in the scientific research domain. A scientific tool using standard scientific formulas for accurate computation.",
],
'middle-ordinate-curve': [
"Middle Ordinate from Radius and Deflection Angle",
"Enter circular-curve radius R and deflection angle Δ (degrees) to obtain the middle ordinate.",
"Circular Curve Middle-Ordinate Calculator",
"/ Circular Curve Middle-Ordinate Calculator",
"📖 View the \"Middle Ordinate from Radius and Deflection Angle User Guide\"",
"Used for curve deflection-angle staking.",
"100×(1−cos30°) → 13.40 meters.",
"📚 In-depth: Circular Curve Middle Ordinate",
"Compute middle ordinate M from radius and deflection angle.",
"Curve-midpoint positioning.",
"One of the curve elements.",
"Middle ordinate",
"R=200 m, Δ=60° → M = R(1−cos(Δ/2)) = 200×(1−cos30°) = 200×0.13397 ≈ 26.8 m, i.e. the perpendicular distance from intersection to curve midpoint.",
"Staking-out",
"From JD measure E along the bisector to the curve midpoint QZ, or measure M to verify, together with T/L.",
"Middle ordinate and radius?",
"M = R(1−cos(Δ/2)); larger Δ gives larger M, reflecting a sharper curve.",
"What is the difference between E and M?",
"E is the slant distance from JD to QZ (along the bisector), M is the perpendicular; E > M because it includes a tangential component.",
],
'prismoidal-volume': [
"Frustum Volume from End and Mid-Section Areas",
"Enter the two end areas A₁, A₂, mid section A_m and spacing L to obtain the volume.",
"Frustum Volume (Simpson) Calculator",
"/ Frustum Volume (Simpson) Calculator",
"📖 View the \"Frustum Volume from End and Mid-Section Areas User Guide\"",
"End area A₁ (m²)",
"Mid section A_m (m²)",
"End area A₂ (m²)",
"Simpson's rule, more accurate than average end-area.",
"50/6×(10+60+20) → 750 m³.",
"📚 In-depth: Prismoidal Volume",
"Compute volume from end and mid-section areas by the prismoidal formula.",
"More accurate than average end-area.",
"Precise earthwork computation.",
"Prismoidal",
"L=20 m, A₁=100, mid Am=80, A₂=60 → V = L/6(A₁+4Am+A₂) = 20/6×(100+320+60) = 20/6×480 = 1600 m³.",
"Equal to average end-area under linear change; for nonlinear (e.g. conical) the prismoidal is more accurate, avoiding average-method error.",
"What is the prismoidal formula?",
"V = L/6(A₁+4Am+A₂), Am is the section at the midpoint, a Simpson-integration approximation.",
"When is it mandatory?",
"When section change is nonlinear (steep slope breaks, heaps), the average method has systematic bias; use prismoidal.",
"How to use Frustum Volume from End and Mid-Section Areas",
"What does Frustum Volume from End and Mid-Section Areas do?",
"Enter end areas A₁, A₂, mid section A_m and spacing L, compute volume by the frustum formula, suited to earthwork quantification.",
"How do I use Frustum Volume from End and Mid-Section Areas?",
"What scenarios suit Frustum Volume from End and Mid-Section Areas?",
],
'reduced-level-bsfs': [
"Unknown Point Elevation from Cumulative Backsight/Foresight",
"Enter known elevation BM, cumulative backsight BS and cumulative foresight FS to obtain the elevation.",
"Level Height-Difference Method Elevation Calculator",
"/ Level Height-Difference Method Elevation Calculator",
"📖 View the \"Unknown Point Elevation from Cumulative Backsight/Foresight User Guide\"",
"Known elevation BM (m)",
"Cumulative backsight BS (m)",
"Cumulative foresight FS (m)",
"BS raises, FS lowers.",
"100+1.5−0.5 → 101.0 meters.",
"📚 In-depth: Level Elevation (Back/Foresight Method)",
"Compute each point's RL from known BM and back/foresight.",
"Pass elevation station by station.",
"Attach-and-check (bonding check).",
"Propagation",
"BM=100.000, Σbacksight=3.500, Σforesight=1.200 → end RL = 100+3.500−1.200 = 102.300 m.",
"Check",
"When bonding to another known point, the difference between computed and known is the misclosure; adjust within the limit.",
"Formula?",
"RL = BM + ΣBS − ΣFS (or this station RL = last station RL + backsight − foresight).",
"Back/foresight order?",
"At each station read backsight to set instrument height then foresight for the front point; wrong order corrupts the whole line.",
],
'scale-converter': [
"🔄 Scale Conversion",
"Mutual conversion between topographic-map scale and map/ground distances",
"📖 View the \"Scale Conversion User Guide\"",
"Map length = ground length / scale denominator",
"Map → ground",
"Ground → map",
"Map + ground → scale",
"Formula: ground distance = map distance × scale denominator N; map distance = ground distance / N. Common units: 1 km = 1000 m = 100000 cm.",
"📚 In-depth: Scale Conversion",
"Convert map distance ↔ ground distance by scale.",
"1:n scaling.",
"Drawing and ground staking.",
"Map-ground mutual conversion",
"1:1000 map 0.5 m → ground = 0.5×1000 = 500 m; ground 2 km on a 1:5000 map = 2000/5000 = 0.4 m.",
"Map distance = ground / denominator, ground = map × denominator; unify to m before computing.",
"What does scale mean?",
"1:n means 1 unit on map = n units on ground; larger n means a smaller, more general map.",
"How to convert area?",
"Area ratio = scale squared; on 1:1000, 1 cm² on map = 100 m² on ground.",
"About \"Scale Conversion\"",
"Scale Conversion is an online tool in the scientific research domain. A scientific tool using standard scientific formulas for accurate computation.",
],
'slope-percent': [
"Grade = Rise / Horizontal",
"Slope % = (h / d) × 100.",
"Slope Percentage",
"/ Slope Percentage",
"📖 View the \"Grade = Rise / Horizontal User Guide\"",
"= rise / horizontal",
"Rise h (m)",
"Horizontal distance d (m)",
"Slope % = rise/horizontal × 100.",
"Slope angle = arctan(h/d).",
"📚 In-depth: Slope Percentage",
"Compute slope % from rise and horizontal distance.",
"Road / pipeline grade.",
"Convert with angle.",
"Basic",
"Rise 10 m, horizontal 100 m → slope = 10/100×100% = 10% (about 5.71°).",
"Pipeline",
"Drain pipe slope 2%: drops 2 m per 100 m to ensure gravity flow; too small silts, too large erodes.",
"What is the slope % formula?",
"Slope % = (rise/horizontal) × 100, denominator is horizontal not slant.",
"And slope ratio?",
"A 10% slope = ratio 1:10; slope ratio = horizontal:rise, reciprocal relation.",
],
'stadia-distance': [
"Stadia Interval Method",
"Stadia Distance Measurement",
"/ Stadia Distance Measurement",
"📖 View the \"Stadia Interval Method User Guide\"",
"Stadia interval s (m)",
"Vertical angle θ (°)",
"Stadia constant k = 100.",
"Height difference = ½k·s·sin(2θ).",
"📚 In-depth: Stadia Surveying",
"Compute horizontal distance D = K·s + C from the stadia interval.",
"Quick distance by theodolite.",
"Used for detail surveying.",
"Stadia",
"Stadia constant K=100, interval s=1.5 m, add constant C≈0 → D = 100×1.5 = 150 m; with vertical-angle reduction gives horizontal distance and height difference.",
"Accuracy",
"Stadia error about 1/200–1/300, lower than steel tape / RTK, suited to sketch surveys and low-grade work.",
"What are K and C?",
"Internally focused K=100, C≈0; D = K·s + C, s is the difference between upper and lower stadia hair readings.",
"Is stadia accurate?",
"Affected by reading / atmosphere, large error at mid-long range; use EDM / RTK for official results.",
],
}

def build(slug, en_list):
    path = os.path.join(WORK, slug + '.json')
    wj = json.load(open(path, encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('!! %s length mismatch %d vs %d' % (slug, len(en_list), len(items)))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src'):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if not en or not isinstance(en, str):
            print('!! %s empty translation' % slug)
            sys.exit(1)
        if CJK.search(en) or CNP.search(en):
            print('!! %s CJK/CNP violation: %s' % (slug, en[:60]))
            sys.exit(1)
        mp[z] = en
    return mp

def write(slug, mp):
    os.makedirs(OUT, exist_ok=True)
    name = ''
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('name', slug)
    out = {'slug': slug, 'industry': 'surveying', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

if __name__ == '__main__':
    for slug, en_list in EN.items():
        mp = build(slug, en_list)
        write(slug, mp)
    print('gen_surveying_b4 done')

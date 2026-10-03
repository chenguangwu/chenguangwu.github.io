#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'mining')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'mining')
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
    out = {'slug': slug, 'industry': 'mining', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('ore-grade', build('ore-grade', [
        "🔄 Ore Grade Conversion",
        "Ore grade (g/t ↔ %) with metal content and ore value conversion, supporting precious and base metals",
        "Core formulas (by input variable): metalKg × 1000 × price; oreTon × grade ÷ 1000; oreTon × grade ÷ 100",
        "Metal type",
        "Gold Au (g/t)",
        "Silver Ag (g/t)",
        "Copper Cu (%)",
        "Iron Fe (%)",
        "Lead Pb (%)",
        "Zinc Zn (%)",
        "Grade (g/t)",
        "Ore amount (t)",
        "Metal unit price (CNY/g or CNY/t)",
        "📖 Grade Conversion Notes",
        "g/t (grams per tonne)",
        ": grams of metal contained in one tonne of ore, commonly used for precious metals (gold, silver, platinum)",
        "% (percentage)",
        ": percentage of metal by ore mass, commonly used for base metals (copper, iron, lead, zinc)",
        "Conversion relation",
        ": 1% = 10000 g/t (that is, a grade of 1% means 10 kg of metal per tonne)",
        "Metal content (kg) = ore amount (t) × grade (g/t) ÷ 1000",
        "Metal content (t) = ore amount (t) × grade (%) ÷ 100",
        "Ore value = metal content × metal unit price",
        "Reference grades",
        "Gold: cut-off grade 0.5-1.0 g/t, industrial grade 2-5 g/t",
        "Silver: cut-off grade 40-50 g/t, industrial grade 80-100 g/t",
        "Copper: cut-off grade 0.2-0.3%, industrial grade 0.5-1.0%",
        "Iron: cut-off grade 20-25%, industrial grade 30-45%",
        "📚 Deep Dive: Ore Grade Conversion",
        "Assay unit alignment: convert g/t to % and vice versa, and judge industrial/cut-off grades against the mineral type (gold, silver, copper, iron, etc.).",
        "Metal content estimation: given the ore amount, convert grade into metal content (kg/t) to support the resource tonnage ledger.",
        "Economic evaluation: combine the unit price to estimate the metal value per tonne of ore, supporting cut-off grade and mining decisions.",
        "Formula scope",
        "g/t mode: grade g/t, metal content kg = ore amount (t) × grade / 1000, tonne of metal = kg/1000, % = g/t ÷ 10000; % mode: %, metal content t = ore amount × % / 100. Value: g/t mode = metal kg × 1000 × unit price (CNY/g), % mode = metal t × unit price (CNY/t). Evaluation uses per-mineral thresholds (e.g. gold ≥5 rich ore, 2–5 industrial, 0.5–2 cut-off).",
        "Worked example (gold)",
        "Gold, grade 3.5 g/t, ore amount 100,000 t, unit price 500 CNY/g. Grade % = 0.00035%, metal content 350 kg (0.35 t), value per tonne of ore = 350×1000×500 = 1.75×10⁸ CNY; against the gold thresholds, 3.5 g/t falls under 'industrial grade' (2–5).",
        "Boundary: copper/iron use % mode",
        "Switch to copper, grade 0.8%, ore amount 100,000 t, unit price 65,000 CNY/t: metal content = 100000×0.8/100 = 800 t, value = 800×65000 = 5.2×10⁷ CNY; 0.8% falls under copper 'industrial grade' (0.5–1%). Gold/silver use g/t while copper/iron/lead/zinc use %; picking the wrong mode makes the unit differ by a factor of ten thousand.",
        "How do g/t and % convert?",
        "1% = 10000 g/t (1% = 1/100 = 10000/1000000, i.e. 10000 grams per tonne). g/t to % divides by 10000, % to g/t multiplies by 10000. Gold and silver have extremely low grades, so g/t is more intuitive for them, while copper, iron and the rest use %. The tool automatically switches the formula according to the unit of the selected mineral.",
        "Is a value of 175 million too high?",
        "This is the linear theoretical metal value from grade × unit price, without deducting beneficiation/smelting recovery and cost. Gold at 3.5 g/t in 100,000 t of ore contains 350 kg of gold, which at 500 CNY/g is indeed 175 million CNY of contained metal value; but going from run-of-mine ore to saleable gold requires beneficiation (recovery often 80–90%), smelting and sales, so the realisable value must be multiplied by the recovery and reduced by the full cost.",
        "About 'Ore Grade Conversion'",
        "Ore Grade Conversion is an online tool in the scientific research field. A scientific research tool that uses standard scientific formulas and computes precisely.",
    ]))

    write('estimate-reserve', build('estimate-reserve', [
        "🔮 Geological Block Method Reserve Estimate",
        "Enter the area, average thickness, ore density and grade of each block, compute ore amount and metal content by the block method, and automatically total all blocks.",
        "Core formula (by input variable): r.totalMetal÷r.totalOre×100",
        "Block",
        "Density (t/m³)",
        "Grade (%)",
        "Ore amount (t)",
        "Metal content (t)",
        "➕ Add block",
        "💡 Ore amount Q = area S × thickness M × density ρ (t); metal content = Q × grade (%). The total is the sum of all blocks.",
        "Area, thickness and density must be positive; enter grade as a percentage (e.g. 1.5 means 1.5%)",
        "The block method suits tabular or quasi-tabular ore bodies with little thickness variation",
        "The result is the in-situ geological reserve, without deducting mining losses or dilution",
        "📚 Deep Dive: Geological Block Method Reserve Estimate",
        "Enter the blocks delimited by exploration drilling (area, thickness, density, grade) row by row, and automatically total ore amount, metal content and average grade.",
        "Level/stope reserve balance: compare the ore share of each block to identify the main blocks and the small peripheral blocks.",
        "Resource upgrade: estimate by the block method on top of inferred/indicated resources, and combine with recovery to obtain mineable reserves.",
        "Formula scope",
        "Per block: ore amount = area × thickness × density (t); metal content = ore amount × grade / 100 (%). Sum all blocks for the total ore amount and total metal content; average grade = total metal / total ore × 100; block share = block ore amount / largest block ore amount × 100.",
        "Three blocks: A (area 20000 m², thickness 8 m, density 2.8, grade 3.5%), B (15000, 10, 2.7, 2.8%), C (30000, 6, 2.9, 4.2%). Ore amount A = 448000 t, B = 405000 t, C = 522000 t, total 1,375,000 t (1.375 million t); total metal content 48,944 t; average grade 3.560%.",
        "Boundary: block overlap",
        "Blocks must not overlap (otherwise they are double counted); area units must be consistent (all m² or all km²), and density is in tonnes per cubic metre (ore density). If a block has an abnormally high grade it will pull the average grade up markedly, so check whether it is an exceptionally high grade needing separate treatment or removal.",
        "What ore bodies does the block method suit?",
        "It suits ore bodies with fairly regular shape, stable occurrence and dense exploration drilling (e.g. tabular or quasi-tabular deposits). It cuts the ore body into blocks and estimates from the average thickness/grade within each block; the computation is simple but accuracy depends on how the blocks are divided and on the degree of drilling control; for complex shapes or sparse exploration, combine it with the cross-section method or Kriging.",
        "How does the 3.560% average grade relate to the individual block grades?",
        "The average grade is weighted by ore amount, not a simple average. Here block C has the largest ore amount and a relatively high grade of 4.2%, pulling the overall figure up to 3.560%, above the simple average of A and B (about 3.17%). Weighting reflects the dominance of the larger tonnage and is closer to the actual mill feed grade than the arithmetic mean.",
        "About 'Geological Block Method Reserve Estimate'",
        "Used for mineral resource reserve estimation. Enter the area, average thickness, ore density and grade of each block under the geological block method, compute the ore amount and metal content of each block and total them automatically; it suits reserve calculation for tabular and quasi-tabular ore bodies.",
        "Supports dynamic add/remove of multiple blocks",
        "Automatically totals ore amount and metal content",
        "Visualises the ore share of each block",
        "General exploration reserve estimation",
        "Deposit economic evaluation",
        "Mining design reserve verification",
        "Geological exploration data summary",
    ]))

    write('calc-1', build('calc-1', [
        "🧮 Blasting Charge Calculation",
        "Estimate per-hole charge, unit consumption and hole pattern parameters from the volume formula or the Langefors formula.",
        "'Estimate per-hole charge, unit consumption and hole pattern parameters from the volume formula or the Langefors formula.' Performs a professional calculation from the input parameters and outputs the result.",
        "Volume formula Q = q·a·b·H",
        "Langefors formula Q = k·W³",
        "Explosive unit consumption q (kg/m³)",
        "Langefors coefficient k (kg/m³)",
        "Hole spacing a (m)",
        "Row spacing b (m)",
        "Bench height H (m)",
        "Minimum burden W (m)",
        "Number of blast holes",
        "Stemming length Ls (m)",
        "Calculate charge",
        "The volume formula suits per-hole charge estimation for bench blasting",
        "The Langefors formula Q = k·W³ suits initial charge estimation for rock blasting",
        "Charge length = Q / (π·r²·ρ), where ρ is the charge density and r the cartridge radius (empirical value)",
        "Actual blasting must be adjusted for rock properties, explosive type and field trials",
        "📚 Deep Dive: Blasting Charge Calculation",
        "Volume method: given the hole pattern (hole spacing, row spacing, hole depth) and the unit explosive consumption q, estimate the per-hole charge, total charge and blasted volume.",
        "Langefors method: given the minimum burden W and the unit charge consumption k, estimate the per-hole charge by Q=k·W³ (suits small-burden smooth blasting / pre-splitting).",
        "Back-calculate the charge length and hole depth, and check whether the charge structure exceeds the safe stemming margin.",
        "Formula scope",
        "Volume method: volume V=a·b·H, per-hole charge Q=q·V, total charge=Q×number of holes; charge length=Q/(π·0.05²·1000) (linear density estimated on a 50 mm charge radius), hole depth≈H+0.3·W. Langefors method: Q=k·W³, volume≈W³/q.",
        "Worked example (volume method)",
        "q=0.45 kg/m³, a=3.0 m, b=2.5 m, H=10 m, 20 holes, W=2.5 m. Per-hole volume 75 m³, per-hole charge 33.75 kg, total charge 675 kg, charge length 4.30 m, hole depth 10.75 m.",
        "Boundary: Langefors method",
        "Switch to the Langefors method, k=0.4, W=2.5 m: per-hole charge = 0.4×2.5³ = 6.25 kg, corresponding volume ≈ 2.5³/0.45 ≈ 34.7 m³. This method suits concentrated charges at small burden (W generally <3 m); for large burden switch to the volume method or split the charge.",
        "How should q (unit explosive consumption) be chosen?",
        "q is determined by rock blastability, hole diameter, number of free faces and so on; consult a blasting handbook or use experience from comparable works (e.g. 0.4–0.5 kg/m³ for bench blasting in medium-hard rock). Here q is a user input and must be chosen for the actual conditions; a wrong value skews the total charge by multiples.",
        "How is the charge length of 4.30 m computed?",
        "The tool uses the linear density π·0.05²·1000≈7.854 kg/m of 50 mm (radius 0.05 m) charges to back-calculate: Q/7.854 = 33.75/7.854 ≈ 4.30 m. This is an approximation for a fixed 50 mm cartridge; with a different diameter or a decoupled charge, use the corresponding linear density.",
    ]))

    write('safety-check', build('safety-check', [
        "🔍 Mine Safety Risk Assessment",
        "Risk matrix (L×S) + checklist + hazard grade",
        "Mine Safety Inspection Assessment",
        "/ Safety Check",
        "Assessment mode",
        "🔍 Assess risk",
        "👆 Select an assessment mode",
        "📚 Deep Dive: Mine Safety Risk Assessment",
        "Risk matrix (L×S): in LSI mode enter likelihood L and severity S to get the risk value = L×S plus its graded handling.",
        "Checklist scoring: tick 10 basic/monitoring/emergency/management checkpoints and derive the safety grade from the score rate.",
        "High-risk closure: extreme risk (L×S≥17) triggers immediate shutdown for rectification; medium-high risk must be rectified within a deadline and tracked.",
        "Formula scope",
        "LSI mode: risk value = likelihood L × severity S. Grades: ≥17 extreme risk (immediate shutdown for rectification), ≥10 high risk (rectify within a deadline ≤7 days), ≥5 medium risk (set measures within ≤30 days), <5 low risk (routine management). Checklist mode: score = ticked items / total items × 100, graded by thresholds.",
        "Worked example (LSI)",
        "For a blasting job with likelihood L=4 and severity S=4, the risk value = 16, which is 'high risk (rectify within ≤7 days)'. If L=5 and S=5, the risk value = 25, which is 'extreme risk (immediate shutdown for rectification)'.",
        "Boundary: matrix mode computes nothing",
        "The default matrix view only shows the L×S formula and the grading notes; switch to the L×S assessment to enter L and S for actual numbers. The 10 checklist items (ventilation/support/electrical/gas/dust/access/fire protection/certification/training/PPE) all ticked gives 100 points; below 60 points is judged unqualified.",
        "How are L and S usually scored?",
        "Likelihood L is usually graded 1–5 (very low to very high), and severity S is also graded 1–5 (minor to catastrophic), giving risk values of 1–25. The exact grading thresholds differ by company",
        "policy, so this tool uses the three bands ≥17/≥10/≥5 as a common simplification; a formal assessment should combine a consequence matrix with the ALARP principle.",
        "Why do risk values of 16 and 17 lead to so different handling?",
        "17 is the extreme-risk threshold that requires immediate shutdown, while 16 is only high risk needing rectification by a deadline. Such hard thresholds make the handling on either side of the boundary differ drastically, so L and S should be scored from data rather than by guesswork — especially near the threshold it is better to round up one level and add control measures, avoiding the luck of landing just below the shutdown line.",
        "About 'Mine Safety Inspection Assessment'",
        "Mine Safety Inspection Assessment. A mining and metallurgy tool that helps compute mineral parameters and indicators.",
    ]))


if __name__ == '__main__':
    main()

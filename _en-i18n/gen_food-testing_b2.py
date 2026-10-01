#!/usr/bin/env python3
# gen_food-testing_b2.py — food-testing b2 (5 slugs): colony-count/convert-36/convert-37/detector-3/elisa-conversion
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'food-testing')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'food-testing')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

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
    out = {'slug': slug, 'industry': 'food-testing', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))


B = {}

B['colony-count'] = [
 '✨ Aerobic Plate Count Report Generator',
 'Per the GB 4789.2 plate count method, it computes the aerobic plate count (CFU) and generates a report.',
 '📖 Read the "Aerobic Plate Count Usage Guide"',
 'Per GB 4789.2 the sample is diluted, pour-plated and incubated (36 ± 1 °C, 48 ± 1 h); plates with a colony count in the',
 'range are counted and multiplied by the dilution factor to give the result.',
 'Aerobic plate count = mean colony count of the parallel plates at one dilution × dilution factor',
 ', reported in CFU/g (or CFU/mL).',
 'If every plate is below 30, estimate from the lowest dilution; if every plate is above 300, report from the highest dilution.',
 'Spreading colonies or confluent growth are converted or repeated according to the standard rules.',
 'The result is a hygiene indicator organism count, not a pathogen count; judge it against the limit in the product standard.',
 '⚠️ Professional tool disclaimer',
 'This tool only supports estimation, learning and record keeping for plate counts. It is not a test report issued by an accredited laboratory and must not be used directly for product release, compliance decisions, recalls, penalties or medical decisions. Actual results must be confirmed by a qualified laboratory following the current standard with defined sampling and culture conditions.',
 'Solid sample (result in CFU/g)',
 'Liquid sample (result in CFU/mL)',
 'First dilution',
 'First dilution, plate 1 (CFU)',
 'First dilution, plate 2 (CFU)',
 'Second dilution',
 'Second dilution, plate 1 (CFU)',
 'Second dilution, plate 2 (CFU)',
 'Inoculum (mL)',
 'Calculate and generate the report',
 '📋 Counting rules (GB 4789.2)',
 'Both dilutions fall in 30~300',
 ': N = ΣC / [(n₁ + 0.1 × n₂) × d] × (1 / inoculum)',
 'Only one dilution falls in 30~300',
 ': N = mean colony count × dilution factor / inoculum',
 'All plates at the lowest dilution below 30',
 ': count as-is and report an "estimated value"',
 'All plates at the highest dilution above 300',
 ': report "too numerous to count" and estimate from the highest dilution',
 '📚 Deep Dive: Aerobic Plate Count',
 'Microbiological hygiene evaluation of food',
 'Aerobic plate count for release testing and sampling',
 'Cold chain and shelf-life monitoring',
 'Per GB 4789.2, take plates with 30–300 colonies: CFU/g(mL) = mean of the two plates at the same dilution ÷ (dilution × inoculum); outside that range use the next dilution or the weighted formula.',
 'The two plates at the first dilution read 156 and 168 (both within 30–300), mean 162, dilution 10⁻¹, inoculum 1 mL: aerobic plate count = 162/(10⁻¹ × 1) ≈ 1.6×10³ CFU/g.',
 'Why is the count limited to 30–300?',
 'Counting error is smallest in this range; below 30 or above 300 the statistical bias is large, so recount at an adjacent dilution.',
 'Does the plate count indicate pathogenicity?',
 'Not directly: it is a hygiene indicator organism count, and a high value points to contamination risk in processing, storage or transport.',
 'About the Aerobic Plate Count Report Generator',
 'An aerobic plate count report generator. A cooking helper for keeping ingredient ratios and nutrition precise.',
]

B['convert-36'] = [
 '🧪 Acid Value / Peroxide Value (Fats and Oils) Titration Conversion',
 'Fats and oils',
 '📖 Read the "Acid Value / Peroxide Value Titration Conversion Usage Guide"',
 'Acid value',
 'Milli acid value',
 'Kilo acid value',
 'Peroxide value titration conversion',
 'Milli peroxide value titration conversion',
 'Kilo peroxide value titration conversion',
 '📚 Deep Dive: Acid Value / Peroxide Value Titration Conversion',
 'Titration results',
 'Converting between different factors',
 'Standardizing reported data',
 'Converted result = input value × conversion factor × (source unit factor ÷ target unit factor).',
 'A titration gives an acid value of 2.81 (as mg KOH/g); multiplying by the factor (0.1000/0.1000) × 1 = 1 gives 2.81. To convert under a factor expressed in mmol/g, apply the corresponding molecular factor, and the result changes linearly with the factor chosen.',
 'How is the factor chosen?',
 'It follows from the',
 'molar concentration',
 'of the titrant and the equivalent weight (KOH 56.1, Na₂S₂O₃ 126.9); the units must stay consistent.',
 'Does it conflict with the direct formula?',
 'No. This tool does a secondary unit conversion of the AV/POV result, and the underlying result still comes from the standard titration formula.',
 'About the Acid Value / Peroxide Value (Fats and Oils) Titration Conversion',
 'An acid value / peroxide value titration conversion for fats and oils. A free online tool that runs entirely in the browser: data is never uploaded, so your privacy stays safe.',
 'Converting and recording laboratory titration data for the acid value and peroxide value of fats and oils',
 'Quality monitoring and discard decisions for frying oil',
 'Nutrition and shelf-life assessment for food labels',
 'Teaching demos of the degree of oil oxidation',
]

B['convert-37'] = [
 '🥗 Protein (Kjeldahl) Factor Conversion',
 'Protein content = nitrogen content × 6.25 (the general Kjeldahl conversion factor)',
 '📖 Read the "Kjeldahl Protein Factor Conversion Usage Guide"',
 'Unit conversion runs by ratio: result = input value × source unit factor ÷ target unit factor. The same physical quantity scales proportionally across units, and the factor ratio is the unit conversion factor, which suits linear conversions such as mass and concentration.',
 'Nitrogen content (%)',
 'Protein (%)',
 '📚 Deep Dive: Kjeldahl Protein Factor Conversion',
 'Converting nitrogen content into protein',
 'Conversion factors for different foods',
 'Protein accounting for nutrition labels',
 'Protein (%) = nitrogen content (%) × conversion factor F (cereals 5.70, soy and soy products 6.25, milk 6.38, nuts 5.30 and so on).',
 'A measured nitrogen content of 2.40% with the general factor F = 6.25 gives protein = 2.40 × 6.25 = 15.0%; with the dairy factor 6.38 it is 15.3%.',
 'How is the factor chosen?',
 'Pick the factor specified in GB 5009.5 for the food category; for mixed foods use a weighted or prescribed factor to avoid overstating protein.',
 'What is the principle behind nitrogen-to-protein?',
 'Protein averages about 16% nitrogen, so 6.25 (1/0.16) is used to back it out; foods with a different measured nitrogen content get a different factor.',
 'About Protein (Kjeldahl) Factor Conversion',
 'A protein (Kjeldahl) factor conversion. A free online tool that runs entirely in the browser: data is never uploaded, so your privacy stays safe.',
 'Converting the protein content of foods using different factors',
 'Converting the nitrogen content of animal and plant foods into protein',
 'Protein claim accounting for formulations and nutrition labels',
 'Teaching demos of the Kjeldahl calculation',
]

B['detector-3'] = [
 '🔍 Pesticide Residue Rapid Test (Enzyme Inhibition Rate) Interpretation',
 'Rapid testing for organophosphorus and carbamate pesticide residues in vegetables and fruit based on the enzyme inhibition method (GB/T 5009.199). Enter the absorbance change of the control and the sample and it computes the inhibition rate and interprets the result.',
 '📖 Read the "Pesticide Residue Enzyme Inhibition Rapid Test Usage Guide"',
 'Enzyme inhibition rate = (control absorbance change ΔA₀ − sample change ΔA) ÷ ΔA₀ × 100%. ΔA₀ should fall between 0.3 and 0.8: too low means insufficient enzyme activity, too high means dilute and retest. An inhibition rate of at least 50% is positive, suggesting organophosphorus or carbamate residues above the limit, while below 50% is negative and passes.',
 'Control solution ΔA0 (absorbance change)',
 'Sample solution ΔAt (absorbance change)',
 'Note: ΔA is the absorbance change before and after the reaction, usually read automatically by a spectrophotometer or a pesticide residue analyser. If ΔA0 < 0.3, enzyme activity is insufficient and the reagent must be prepared again.',
 'Calculate inhibition rate',
 'The enzyme inhibition method follows GB/T 5009.199-2003 and suits rapid screening for organophosphorus and carbamate residues',
 'An inhibition rate of at least 50% is positive (fails) and needs chromatographic confirmation; 35%-50% is suspect and needs retesting; below 35% is negative (passes)',
 'The control ΔA0 should fall in the 0.3-0.8 range; otherwise enzyme activity is abnormal and the reagent must be prepared again',
 'This method is a rapid screen and cannot replace confirmatory analysis by gas or liquid chromatography',
 '📚 Deep Dive: Pesticide Residue Enzyme Inhibition Rapid Test',
 'Rapid organophosphorus testing of fruit and vegetables',
 'Residue screening and release decisions',
 'Sampling on market entry',
 'Inhibition rate (%) = (ΔA₀ − ΔA_t)/ΔA₀ × 100, where ΔA is the absorbance change; at least 50% is positive, 15–50% suspect and below 15% negative.',
 'Control ΔA₀ = 0.500 and sample ΔA_t = 0.300: inhibition rate = (0.500 − 0.300)/0.500 × 100 = 40%, which falls in the suspect range, so retest or send it for chromatographic confirmation.',
 'Does a positive result mean the limit is exceeded?',
 'No. The enzyme inhibition method is only a screen: a positive result suggests possible organophosphorus or carbamate residues that must be confirmed and quantified by GC/LC-MS.',
 'Why must the control be 0.3-0.8?',
 'A ΔA₀ that is too low means insufficient enzyme activity and one that is too high means an abnormal reagent; both undermine the reliability of the inhibition rate, so remake the enzyme solution.',
 'About the Pesticide Residue Rapid Test (Enzyme Inhibition Rate) Interpretation',
 'The enzyme inhibition method is a common rapid screen for organophosphorus and carbamate pesticide residues in vegetables and fruit (GB/T 5009.199-2003). Its principle is that pesticides inhibit cholinesterase activity, so measuring the absorbance change of the enzyme-catalysed reaction gives the inhibition rate, which indirectly reflects the residue level.',
 'Enter the control and sample absorbance changes and get the inhibition rate in one click',
 'Automatic three-level interpretation: pass, suspect or fail',
 'Control value range check (0.3-0.8) to prevent misjudgement',
 'Detailed interpretation of results and handling advice',
 'Rapid residue testing rooms in wet markets and supermarkets',
 'Self-inspection at agricultural production sites',
 'Ingredient acceptance by catering businesses',
 'On-site screening by food safety regulators',
]

B['elisa-conversion'] = [
 '🔄 Veterinary Drug Residue ELISA Absorbance Converter',
 'Enter standard concentrations with their OD values to fit a curve, then enter the sample OD to compute the concentration. It supports the zero-standard OD (B₀) and the percent binding calculation.',
 'Core formulas (by input variables): Math.round(r×r×10000)÷10000; (sampleOD÷b0od)×100; (d.od÷b0od)×100',
 '📖 Read the "ELISA Standard Curve Back-Calculation Usage Guide"',
 '1. Standard curve data',
 '+ Add standard point',
 '- Delete the last row',
 'Sample OD value',
 'Sample dilution factor',
 'Limit standard (μg/L)',
 'Percent binding B/B₀ (%)',
 '= (standard or sample OD / zero-standard OD) × 100%',
 'Concentration calculation',
 ': linear regression of log(concentration) against B/B₀%, y = a·x + b, back-calculating the sample concentration.',
 'Actual concentration',
 '= curve concentration × dilution factor',
 '📚 Deep Dive: ELISA Standard Curve Back-Calculation',
 'Converting kit OD readings into concentration',
 'Sample quantification and limit comparison',
 'Batch conversion of test data',
 'Percent binding B/B₀ = (OD_sample / OD₀) × 100; regress log₁₀(concentration) against B/B₀',
 'linear regression',
 'and back-calculate the sample concentration.',
 'Sample OD = 0.650 and zero-standard OD₀ = 1.000: B/B₀ = 65%; from the fitted curve log₁₀(c) = a·65 + b the corresponding concentration is about 0.85 mg/kg (the measured standard curve governs).',
 'Why use B/B₀?',
 'It removes plate-to-plate and substrate differences so OD values are comparable, and concentration is roughly linear after taking logs, which makes interpolation easy.',
 'How many curve points are needed?',
 'At least two non-zero standards are needed to fit; more points give a wider accurate range, and the zero standard B₀ must be included.',
 'About the Veterinary Drug Residue ELISA Absorbance Converter',
 'A veterinary drug residue ELISA absorbance converter. A cooking helper for keeping ingredient ratios and nutrition precise.',
]

for s, lst in B.items():
    write(s, build(s, lst))

#!/usr/bin/env python3
# gen_food-testing_b5.py — food-testing b5 (4 slugs): pesticide-residue-test/protein-kjeldahl/salmonella-serotype/salt-titration
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

B['pesticide-residue-test'] = [
 '🔍 Pesticide Residue Rapid Test Result Interpreter',
 'Based on the enzyme inhibition method (GB/T 5009.199): enter the absorbance change of the control and the sample and it computes the inhibition rate and interprets the result.',
 '📖 Read the "Pesticide Residue Enzyme Inhibition Screening Usage Guide"',
 'Enzyme inhibition rate = (ΔA₀ − ΔA) ÷ ΔA₀ × 100%. The control ΔA₀ must be above 0.3 and below 0.8 for the test to be valid. When the inhibition rate reaches the judgement threshold (50% by default) the result is positive, suggesting possible organophosphorus or carbamate residues that must be confirmed by gas or liquid chromatography.',
 'Control absorbance change ΔA₀',
 'Sample absorbance change ΔA',
 'Judgement threshold (%)',
 '50% (standard, organophosphorus and carbamates)',
 '15% (sensitive mode)',
 'Calculate and interpret',
 '📊 Interpretation criteria (GB/T 5009.199)',
 'Inhibition rate of at least 50%',
 ': the sample is positive and may contain organophosphorus or carbamate pesticide residues',
 '15% up to but below 50%',
 ': the result is suspect, so confirm it by chromatography',
 'Inhibition rate below 15%',
 ': the sample is negative and the residue risk is low',
 '⚠️ The rapid method is only a screen, and a positive result must be confirmed by gas or liquid chromatography. This tool only supports laboratory interpretation.',
 '📚 Deep Dive: Pesticide Residue Enzyme Inhibition Screening',
 'Rapid residue testing of fruit and vegetables',
 'Screening on market entry or dispatch',
 'Preparing positive samples for confirmation',
 'Inhibition rate (%) = (ΔA₀ − ΔA)/ΔA₀ × 100; at or above the threshold is positive, between 15 and the threshold is suspect, and below 15% is negative.',
 'Control ΔA₀ = 0.500 and sample ΔA = 0.450: inhibition rate = (0.500 − 0.450)/0.500 × 100 = 10%, which is negative and the residue risk is low; at 60% it is positive and must be confirmed.',
 'What threshold should be set?',
 '50% is the usual positive criterion, subject to the method standard; this tool controls it through the threshold parameter.',
 'Does a negative screen mean it is safe?',
 'It only means no inhibition of this type was detected, not zero residue; high-risk items still need chromatographic confirmation.',
 'About the Pesticide Residue Rapid Test Result Interpreter',
 'A pesticide residue rapid test result interpreter. A cooking helper for keeping ingredient ratios and nutrition precise.',
]

B['protein-kjeldahl'] = [
 '🥗 Protein Kjeldahl Factor Converter',
 'V is the titration volume (mL), c the acid concentration (mol/L) and m the sample mass (g); F is the nitrogen-to-protein conversion factor (wheat 5.70, corn 6.25 and so on).',
 '📖 Read the "Kjeldahl Protein Content Usage Guide"',
 'Nitrogen (%) = |V₁ − V₀| × c × 0.014 / m × 100; protein (%) = nitrogen content × F',
 'Per the GB 5009.5 Kjeldahl method, it computes the protein content of a food and supports several nitrogen conversion factors.',
 'Sample titration volume V₁ (mL)',
 'Blank titration volume V₀ (mL)',
 'Standard acid concentration c (mol/L)',
 'Food type / conversion factor F',
 'General foods (F = 6.25)',
 'Wheat/flour (F = 5.70)',
 'Milk and dairy products (F = 6.38)',
 'Soy and soy products (F = 5.71)',
 'Rice (F = 5.95)',
 'Peanut (F = 5.46)',
 'Sesame/nuts (F = 5.30)',
 'Meat and meat products (F = 6.25)',
 'Gelatin (F = 5.55)',
 'Eggs (F = 6.25)',
 'Corn/sorghum (F = 6.25)',
 'Beer/beverages (F = 6.25)',
 'Nitrogen conversion factor F',
 'Calculate protein content',
 'Protein content (g/100g)',
 '0.014 is the millimole mass of nitrogen (14 g/mol ÷ 1000)',
 'F converts nitrogen into protein and differs by food type.',
 '💡 The Kjeldahl method measures total nitrogen, so non-protein nitrogen is counted as well. Nitrogenous compounds such as melamine push the result higher.',
 '📚 Deep Dive: Kjeldahl Protein Content',
 'Determining protein in food',
 'Protein accounting for nutrition labels',
 'Nitrogen analysis of feed and grain',
 'Nitrogen (%) = |V₁ − V₀| × c × 0.014 / m × 100; protein (%) = nitrogen % × F, where F is the conversion factor.',
 'Titration V₁ = 10.50, blank V₀ = 0.20 mL, c = 0.0500 mol/L, sample 0.500 g, F = 6.25: nitrogen % = (10.30 × 0.0500 × 0.014)/0.500 × 100 ≈ 1.44%, protein = 1.44 × 6.25 ≈ 9.01%.',
 'Why subtract the blank?',
 'V₀ corrects for the nitrogen in the reagents and the environment, so the nitrogen comes only from the sample and the result is more accurate.',
 'What if the wrong F is used?',
 'A wrong factor scales the protein result directly, so take the value that GB 5009.5 specifies for the category.',
 'About the Protein Kjeldahl Factor Converter',
 'A protein Kjeldahl factor converter. A cooking helper for keeping ingredient ratios and nutrition precise.',
]

B['salmonella-serotype'] = [
 '📚 Salmonella Serotype Antigen Lookup',
 'Based on the Kaufmann-White antigenic scheme, enter the O and H antigens to look up the Salmonella serotype name.',
 '📖 Read the "Salmonella Serotype Lookup Usage Guide"',
 'Search by antigen combination',
 'Search by serotype name',
 'O antigen (somatic antigen)',
 'H antigen, phase 1 (flagellar antigen)',
 'H antigen, phase 2 (optional)',
 'Serotype name',
 '📋 Notes on the Kaufmann-White antigenic scheme',
 'O antigen',
 '(somatic antigen): written with Arabic numerals such as 4, 9, 1,3 and 6,7.',
 'H antigen',
 '(flagellar antigen): phase 1 uses lower-case letters or a letter plus a number (a-z, z6 and so on), phase 2 uses numbers (1,2; 1,5 and so on).',
 'Vi antigen',
 ': the capsular antigen, found in a few serotypes such as Salmonella Typhi.',
 '📚 Deep Dive: Salmonella Serotype Lookup',
 'Antigenic typing of isolates',
 'Tracing foodborne disease',
 'Classifying surveillance data',
 'Under the Kaufmann-White scheme, the O antigen (group) and the H antigens (phase 1 and 2) are looked up in the antigenic table to find the matching serotype name.',
 'O antigen 4 (group B), H phase 1 i and phase 2 1,2 give the serotype Salmonella 1,4,[5],12:i:1,2 (Typhimurium).',
 'Why type the serotype?',
 'Different serotypes differ in pathogenicity and in their outbreak associations, so typing supports tracing and control (Typhimurium, for example, is common in food).',
 'Can it be typed when antigens are incomplete?',
 'A complete O plus both H phases is needed; with autoagglutination or missing antigens, confirm with biochemical and molecular tests.',
 'About the Salmonella Serotype Antigen Lookup',
 'A Salmonella serotype antigen lookup. A cooking helper for keeping ingredient ratios and nutrition precise.',
 'For example 4, 9, 1,3',
 'For example i, g,m, b, d',
 'For example 1,2 or 1,5',
 'For example Typhimurium',
]

B['salt-titration'] = [
 '🧪 Salt Content Silver Nitrate Titration Calculator',
 'Per GB 5009.44 (the Mohr method), it computes the sodium chloride (salt) content of a food.',
 'Core formulas (by input variables): Math.round(naclMass×10000)÷10000; min(100,(naclContent÷limit)×100); Math.round(naclContent×10000)÷10000',
 '📖 Read the "Salt (Sodium Chloride) Content Titration Usage Guide"',
 'AgNO₃ volume consumed V (mL)',
 'AgNO₃ concentration c (mol/L)',
 'Aliquot volume for the test V₂ (mL)',
 'General foods',
 'Soy sauce (≤15%)',
 'Pickled products',
 'Bread and pastries',
 'Infant and young children food',
 'Limit standard (%)',
 'Calculate salt content',
 'Salt content (g/100g)',
 'V is the AgNO₃ volume consumed, c the AgNO₃ concentration and 58.5 the molar mass of NaCl',
 'V₁ is the volume the sample was made up to, V₂ the aliquot volume taken and m the sample mass',
 '📚 Deep Dive: Salt (Sodium Chloride) Content Titration',
 'Determining the salt content of food',
 'Accounting for low-sodium and reduced-salt formulations',
 'Converting the sodium figure for labels',
 'Per the GB 5009.44 Mohr method: NaCl(%) = V × c × 0.05844 / m × (total volume / test volume) × 100, where V is the AgNO₃ volume, c the concentration and m the sample.',
 'AgNO₃ 10.50 mL (0.1000 mol/L), sample 5.00 g, total volume 100 mL, 20 mL taken for the test: NaCl = (10.50 × 0.1000 × 0.05844)/5.00 × (100/20) × 100 ≈ 6.14%.',
 'What is 0.05844?',
 'The milli',
 'molar mass of NaCl in g/mmol, which converts the titration volume straight into a mass of salt.',
 'How is the sodium content calculated?',
 'NaCl × 0.3934 (Na/NaCl) gives the sodium content, used for the sodium NRV% on nutrition labels.',
 'About the Salt Content Silver Nitrate Titration Calculator',
 'A salt content silver nitrate titration calculator. A cooking helper for keeping ingredient ratios and nutrition precise.',
]

for s, lst in B.items():
    write(s, build(s, lst))

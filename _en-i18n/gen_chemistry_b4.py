#!/usr/bin/env python3
# gen_chemistry_b4.py — chemistry b4 (5 slugs): molarity/mole-fraction/nernst-equation/normality/partial-pressure
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'chemistry')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'chemistry')

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
    out = {'slug': slug, 'industry': 'chemistry', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

B = {}

B['molarity'] = [
 'Molarity (c = n / V)',
 'Compute molar concentration from the amount of substance and the solution volume.',
 'Molarity Calculator',
 '/ Molarity Calculation',
 'Molarity Calculation',
 '📖 Read the "Molarity (c = n / V) Usage Guide"',
 'c = n / V; V is the solution volume (L).',
 '2 mol dissolved in 1 L gives 2 mol/L.',
 '📚 Deep Dive: Molarity (c = n / V)',
 'Standard solution preparation: weigh the solid, dilute to volume V to obtain c, and use it as a titration standard.',
 'Titration calculations: use c and V to find the moles that react, then solve for the unknown concentration.',
 'Dilution check: after dilution c follows C1V1 = C2V2.',
 'Walkthrough: 0.5 mol of solute made up to 250 mL',
 'Enter n = 0.5 mol and V = 250 mL, the tool outputs c = 2.0 mol/L and reminds you to dilute to the mark rather than adding solvent up to the volume.',
 'Dilute to V, not add up to V?',
 'Yes, dilute to the mark: dissolve first, then add water up to the line, rather than adding solvent up to V.',
 'Does temperature matter?',
 'Volume changes with temperature, so c shifts slightly; precise work needs a constant temperature.',
 'How do I choose between molarity and molality?',
 'Use c when preparing titrations, and b for colligative properties.',
]

B['mole-fraction'] = [
 'Mole fraction from the amount of substance of each component',
 'Enter the amount of substance of two or more components and it is normalized into mole fractions automatically.',
 'Mole Fraction x',
 '/ Mole Fraction Calculator',
 'Mole Fraction Calculator',
 '📖 Read the "Finding Mole Fraction from the Amount of Substance Usage Guide"',
 'x_i = n_i / Σn_i, and all x_i sum to 1. Only positive entries are counted.',
 'Component 1 amount of substance (mol)',
 'Component 2 amount of substance (mol)',
 'Component 3 amount of substance (0 allowed) (mol)',
 'x_i = n_i / Σn_i, and all x_i sum to 1.',
 'Only positive entries are counted.',
 '📚 Deep Dive: Finding Mole Fraction from the Amount of Substance',
 'Binary solutions: get x_A and x_B from the moles of the two components (they sum to 1).',
 'Dalton partial pressure: multiply x_i by the total pressure to get the component partial pressure.',
 'Ideal solution activity approximation: in dilute solutions, use x to approximate activity.',
 'Walkthrough: A 2 mol, B 3 mol',
 'Enter A = 2 mol and B = 3 mol, the tool outputs x_A = 0.40 and x_B = 0.60 and notes that all components sum to 1.',
 'Do mole fractions sum to 1?',
 'All components sum to 1; if not, a component was missed or the arithmetic is wrong.',
 'Is it the same as volume fraction?',
 'Roughly equal for ideal gases, but not for liquids (molecular volumes differ).',
 'How do I handle more than two components?',
 'Compute n_i / Σn for each; it is the same binary idea generalized.',
]

B['nernst-equation'] = [
 'Electrode potential under non-standard conditions',
 'Enter the standard potential, electron count n, reaction quotient Q and temperature to get the actual electrode potential.',
 'Nernst Equation Calculator',
 '/ Nernst Equation Calculator',
 '📖 Read the "Electrode Potential Under Non-Standard Conditions Usage Guide"',
 'E = E° − (RT/nF)lnQ. At 25 °C, 2.303RT/F ≈ 0.0592 V. When Q = 1, E = E°.',
 'Standard electrode potential E° (V)',
 'Electron transfer number n',
 'Reaction quotient Q',
 'E = E° − (RT/nF)lnQ. At 25 °C, 2.303RT/F ≈ 0.0592 V.',
 'When Q = 1, E = E°.',
 '📚 Deep Dive: Electrode Potential Under Non-Standard Conditions',
 'Cell potential: derive the actual E from E°, n and Q to assess the output voltage.',
 'Concentration cells: compute the EMF from the concentration difference between the two sides.',
 'Equilibrium check: when Q = K, E = 0 and the reaction has reached equilibrium.',
 'Walkthrough: Zn²⁺/Zn concentration difference',
 'Enter E° = −0.76 V, n = 2, [Zn²⁺] = 0.01 M and T = 298 K, the tool outputs E ≈ −0.82 V and notes that half-reactions containing H⁺ vary with pH.',
 'What is n?',
 'The number of electrons transferred, obtained by balancing the half-reaction.',
 'Is temperature in K?',
 'Yes, 273 + °C; it affects the RT/nF term.',
 'Is it related to pH?',
 'For half-reactions containing H⁺/OH⁻, Q includes [H⁺], so E changes with pH.',
]

B['normality'] = [
 'Normality (N = n·z / V)',
 'Normality = amount of substance × equivalence factor / volume, commonly used in acid-base and redox titrations.',
 'Normality Calculator',
 '/ Normality Calculation',
 'Normality Calculation',
 '📖 Read the "Normality (N = n·z / V) Usage Guide"',
 'N = n·z / V; z is the number of equivalents per mole. 1 mol H₂SO₄ (z = 2) made up to 1 L gives 2 N.',
 'Equivalence factor z (eq/mol)',
 'N = n·z / V; z is the number of equivalents per mole.',
 '1 mol H₂SO₄ (z = 2) made up to 1 L gives 2 N.',
 '📚 Deep Dive: Normality (N = n·z / V)',
 'Acid-base titration: z = 1 for monoprotic acids and z = 2 for diprotic acids, so N = c·z.',
 'Redox: set z from the electron transfer number, then compute the normality.',
 'Equivalent conversion: N and c are bridged by z, unifying the measurement basis.',
 'Walkthrough: 0.1 mol/L H₂SO₄ (z = 2)',
 'Enter c = 0.1 mol/L and z = 2, the tool outputs N = 0.2 N and notes that z changes with the reaction type.',
 'How is z (the equivalence factor) determined?',
 'For acids and bases, count the exchangeable H⁺/OH⁻; for redox, use the electron transfer number.',
 'Is normality still commonly used?',
 'Still used in titrations, especially redox; modern practice often uses mol/L plus z directly.',
 'Can N and c be compared directly?',
 'N = z·c, so different z gives different numbers; always state the reaction type.',
]

B['partial-pressure'] = [
 'Dalton partial pressure (Pᵢ = xᵢ · P_total)',
 'In a gas mixture, the partial pressure of a component equals its mole fraction times the total pressure.',
 "Dalton's Law of Partial Pressure Calculator",
 '/ Dalton Partial Pressure',
 'Dalton Partial Pressure',
 '📖 Read the "Dalton Partial Pressure (Pᵢ = xᵢ · P_total) Usage Guide"',
 'Pᵢ = xᵢ · P_total',
 'Mole fraction',
 'Total pressure (kPa)',
 'Pᵢ = xᵢ · P_total; xᵢ is the mole fraction of the component.',
 'With a mole fraction of 0.2 and a total pressure of 100 kPa, the partial pressure is 20 kPa.',
 '📚 Deep Dive: Dalton Partial Pressure (Pᵢ = xᵢ · P_total)',
 'Mixture partial pressures: derive each gas partial pressure from composition and total pressure to assess operating conditions.',
 'Gas collection: when collecting over water, subtract the water vapor partial pressure to get the dry gas partial pressure.',
 'Breathing gas: the O₂ partial pressure in air is about 0.21 × the total pressure.',
 'Walkthrough: air with x_O2 = 0.21, P = 1 atm',
 'Enter x_O2 = 0.21 and P = 1 atm, the tool outputs P_O2 ≈ 0.21 atm and notes that the partial pressure ratio = mole ratio = volume ratio.',
 'How do partial pressure and volume fraction relate?',
 'For ideal gases, the partial pressure ratio = mole ratio = volume ratio.',
 'How is water vapor subtracted?',
 'Subtract the saturated vapor pressure at that temperature from the total pressure to get the dry gas partial pressure.',
 'How do partial pressures change when the total pressure changes?',
 'At fixed composition, each partial pressure scales in proportion to the total pressure.',
]

for s, lst in B.items():
    write(s, build(s, lst))

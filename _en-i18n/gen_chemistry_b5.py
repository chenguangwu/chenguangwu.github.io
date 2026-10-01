#!/usr/bin/env python3
# gen_chemistry_b5.py — chemistry b5 (5 slugs): ph-from-ka/ph-to-h/poh-to-ph/reaction-quotient/resistivity-from-r
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

B['ph-from-ka'] = [
 'Estimating pH from the acid dissociation constant and concentration',
 'Enter the weak acid concentration and Ka, then use the approximate formula to get the hydrogen ion concentration and pH.',
 'pH of a monoprotic weak acid ≈ ½(pKₐ − log C)',
 '/ Weak Acid pH Calculator',
 'Weak Acid pH Calculator',
 '📖 Read the "Estimating pH from the Acid Dissociation Constant and Concentration Usage Guide"',
 'Weak acid concentration (mol/L)',
 'Acid dissociation constant Ka',
 'Approximation [H⁺] = √(Ka·C), valid for C/Ka > 400.',
 '0.1 mol/L acetic acid (Ka = 1.8e-5) gives pH ≈ 2.87.',
 '📚 Deep Dive: Estimating pH from the Acid Dissociation Constant and Concentration',
 'Weak acid pH: 0.1 M acetic acid with Ka = 1.8e-5 gives pH ≈ 2.87.',
 'Effect of Ka: a larger Ka means a lower pH, which reflects acid strength.',
 'Validity of the approximation: it holds well at C/Ka > 100, otherwise solve the quadratic equation.',
 'Walkthrough: 0.10 M acetic acid with Ka = 1.8×10⁻⁵',
 'Enter C = 0.10 and Ka = 1.8e-5, the tool outputs [H⁺] ≈ 1.34×10⁻³ and pH ≈ 2.87, and notes that the approximation is reliable when C/Ka > 100.',
 'When should the approximate formula be used?',
 '√(Ka·C) is reliable when C/Ka ≥ 100 and the degree of dissociation is below 5%.',
 'Can it be used for strong acids?',
 'Strong acids ionize completely, so pH = −lgC directly and no Ka is needed.',
 'How much do the exact and approximate results differ?',
 'The difference is small for dilute weak acids; for concentrated solutions or large Ka, solve the quadratic equation.',
]

B['ph-to-h'] = [
 'pH and [H⁺] ([H⁺] = 10⁻ᴾᴴ)',
 'pH = -log₁₀[H⁺]; this tool converts pH into hydrogen ion concentration and vice versa.',
 'pH and Hydrogen Ion Concentration Converter',
 '/ pH and Hydrogen Ion Concentration',
 'pH and Hydrogen Ion Concentration',
 '📖 Read the "[H⁺] ([H⁺] = 10⁻ᴾᴴ) Usage Guide"',
 '[H⁺] = 10^(-pH); at pH = 7, [H⁺] = 1×10⁻⁷ mol/L.',
 'pH < 7 is acidic, > 7 is basic.',
 '📚 Deep Dive: [H⁺] ([H⁺] = 10⁻ᴾᴴ)',
 'pH→[H⁺]: pH = 3 gives [H⁺] = 1e-3 mol/L.',
 'Logarithmic intuition: every 1-unit drop in pH raises [H⁺] tenfold.',
 'Reporting: convert measured pH into concentration for inspection reports.',
 'Walkthrough: back-calculating from pH = 2.5',
 'Enter pH = 2.5, the tool outputs [H⁺] ≈ 3.16×10⁻³ mol/L and notes that pH + pOH = 14 (25 °C).',
 'What does a negative pH mean?',
 'When [H⁺] > 1 in concentrated strong acid, pH < 0 is mathematically possible, although tables usually run 0–14.',
 'What is the unit of [H⁺]?',
 'How does it relate to pOH?',
 'pH + pOH = 14 (25 °C), so the two can be converted into each other.',
]

B['poh-to-ph'] = [
 'Finding pOH and pH from [OH⁻]',
 'Enter the hydroxide concentration to get pOH and pH.',
 'pOH and pH Converter',
 '/ pOH and pH Converter',
 '📖 Read the "Finding pOH and pH from [OH⁻] Usage Guide"',
 'Hydroxide concentration [OH⁻] (mol/L)',
 '📚 Deep Dive: Finding pOH and pH from [OH⁻]',
 'Alkaline solution pH: 0.01 M NaOH gives pOH = 2 and pH = 12.',
 'Strong vs weak bases: strong bases are used directly, weak bases need Kb to get [OH⁻].',
 'Reporting: convert measured [OH⁻] into pH for reports.',
 'Walkthrough: [OH⁻] = 1.0×10⁻³',
 'Enter [OH⁻] = 1.0×10⁻³, the tool outputs pOH = 3.0 and pH = 11.0 and notes that pH + pOH ≠ 14 outside 25 °C.',
 'How do I handle weak bases?',
 'Use Kb to get [OH⁻] for weak bases; you cannot approximate straight from the concentration.',
 'Does pH + pOH = 14 hold outside 25 °C?',
 'Only at 25 °C where the ion product is 1e-14; Kw changes with temperature, so the sum is not 14.',
 'How does pH change when a strong base is diluted?',
 'Each 10-fold dilution lowers pH by 1 (slowing down as it approaches 7).',
 'How to use Finding pOH and pH from [OH⁻]',
 'Quick pH estimates for alkaline systems: checking the pH of NaOH/ammonia solutions prepared in the lab, assessing the alkalinity of wastewater and cleaning fluids, and predicting the pH change around an acid-base titration endpoint.',
 'What does Finding pOH and pH from [OH⁻] do?',
 'A pOH-to-pH calculator: enter the hydroxide concentration to get pOH, then pH via pH + pOH = 14, used for alkaline solution analysis.',
 'How do I use Finding pOH and pH from [OH⁻]?',
 'What scenarios is Finding pOH and pH from [OH⁻] suited to?',
 'pH describes the acidity or alkalinity of an aqueous solution: pH < 7 acidic, = 7 neutral, > 7 basic. Convert from pOH using pH = 14 − pOH (25 °C standard).',
 'Applicability limits',
 'pH + pOH = 14 holds only in dilute solutions at 25 °C; as temperature changes the neutral pH shifts away from 7 (about 7.47 at 0 °C and 6.14 at 100 °C). At high concentrations of strong acid or base, activity effects are significant and activity rather than concentration must be used.',
 'Results are for reference only; for accurate measurement rely on a pH meter or test paper, and handle corrosive liquids with care.',
]

B['reaction-quotient'] = [
 'Determining the direction a reaction proceeds',
 'Enter the reactant and product concentrations with their coefficients to get the reaction quotient Q and compare it with K.',
 'Q = Π(concentration^coefficient)',
 '/ Reaction Quotient Q Calculator',
 'Reaction Quotient Q Calculator',
 '📖 Read the "Determining the Direction a Reaction Proceeds Usage Guide"',
 'Q = [P]^ν_P / [R]^ν_R (partial pressures for gases). Q < K forward, Q > K reverse.',
 'Reactant concentration [R] (mol/L)',
 'Reactant coefficient ν_R',
 'Product concentration [P] (mol/L)',
 'Product coefficient ν_P',
 'Equilibrium constant K',
 'Q = [P]^ν_P / [R]^ν_R (partial pressures for gases).',
 'K reverse.',
 '📚 Deep Dive: Determining the Direction a Reaction Proceeds',
 'Direction: compute Q and compare it with K to see which way the reaction goes.',
 'Initial state: compute Q from the feed to predict the trend.',
 'Approaching equilibrium: as the reaction proceeds, Q moves toward K.',
 'Walkthrough: N₂+3H₂⇌2NH₃ direction',
 'Enter the concentrations to compute Q; the tool compares it with K and reports "Q < K, proceeds forward" or "Q > K, reverse", noting that Q = K means equilibrium.',
 'Do Q and K share the same units?',
 'Both use the same activity/concentration basis, and K is dimensionless (normalized to the standard state).',
 'What does Q = K mean?',
 'Equilibrium is reached and the net rate in both directions is zero.',
 'Does a pressure change affect Q?',
 'When gases are expressed as partial pressures, a change in total pressure changes each partial pressure, and Q changes with it.',
]

B['resistivity-from-r'] = [
 'Resistivity (ρ = R·A / L)',
 'Compute the resistivity of a material (the reciprocal of conductivity) from a measured resistance, cross-sectional area and length.',
 'Resistivity Calculator',
 '/ Resistivity Calculation',
 'Resistivity Calculation',
 '📖 Read the "Resistivity (ρ = R·A / L) Usage Guide"',
 'ρ = R·A / L; A is converted from mm² to m². Copper resistivity is about 1.7×10⁻⁸ Ω·m.',
 'ρ = R·A / L; A is converted from mm² to m².',
 'Copper resistivity is about 1.7×10⁻⁸ Ω·m.',
 '📚 Deep Dive: Resistivity (ρ = R·A / L)',
 'Material resistivity: measure R and the geometry to get ρ, then compare it with handbooks.',
 'Wire selection: determine the cross-sectional area from the target R and ρ.',
 'Temperature effect: the ρ of metals rises slightly with temperature, so state the temperature.',
 'Walkthrough: R = 2 Ω, A = 1 mm², L = 1 m',
 'Enter R = 2 Ω, A = 1e-6 m² and L = 1 m, the tool outputs ρ = 2×10⁻⁶ Ω·m (illustrative) and reminds you that units must be kept consistent in Ω·m.',
 'Do the units have to be consistent?',
 'Use Ω for R, m² for A and m for L, which gives ρ in Ω·m.',
 'How does it relate to conductivity?',
 'Conductivity σ = 1/ρ.',
 'Does temperature matter?',
 'The ρ of metals rises with temperature while semiconductors do the opposite; experiments must state the temperature.',
]

for s, lst in B.items():
    write(s, build(s, lst))

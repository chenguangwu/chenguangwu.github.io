#!/usr/bin/env python3
# gen_chemistry_b6.py — chemistry b6 (2 slugs): solubility-product/solution-dilution
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

B['solubility-product'] = [
 'Finding the solubility product from ion concentrations, or vice versa',
 'Enter the cation and anion concentrations with their stoichiometric exponents to get the solubility product Ksp.',
 'Solubility Product Ksp Calculator',
 '/ Solubility Product Ksp Calculator',
 '📖 Read the "Finding the Solubility Product from Ion Concentrations or Vice Versa Usage Guide"',
 'Cation concentration [A] (mol/L)',
 'Cation exponent m',
 'Anion concentration [B] (mol/L)',
 'Anion exponent n',
 '📚 Deep Dive: Finding the Solubility Product from Ion Concentrations or Vice Versa',
 'Saturation concentration: given Ksp, compute the saturation concentration of a single ion (such as AgCl).',
 'Ion product Qsp test: compute Qsp from the current concentrations; Qsp > Ksp indicates precipitation.',
 'Common-ion effect: a shared ion lowers the solubility.',
 'Walkthrough: AgCl with Ksp = 1.8×10⁻¹⁰',
 'Enter Ksp = 1.8e-10, the tool outputs a saturated [Ag⁺] ≈ 1.34×10⁻⁵ M and notes that adding Cl⁻ lowers the solubility through the common-ion effect.',
 'Does Qsp > Ksp always mean precipitation?',
 'Supersaturated solutions may stay clear for a while (metastable) and only settle out after a disturbance; thermodynamically Qsp > Ksp is the criterion.',
 'Common-ion effect?',
 'A shared ion lowers the solubility (Le Chatelier principle).',
 'Is it related to pH?',
 'Salts of weak-acid anions (such as CaF₂) are affected by [H⁺] (F⁻ protonation), so solubility changes as pH rises.',
]

B['solution-dilution'] = [
 'Solution dilution (C₁V₁ = C₂V₂)',
 'The amount of solute is conserved during dilution: C₁V₁ = C₂V₂, solve for the final volume V₂ required.',
 '/ Solution Dilution Calculation',
 'Solution Dilution Calculation',
 '📖 Read the "Solution Dilution (C₁V₁ = C₂V₂) Usage Guide"',
 'Dilution law: C₁V₁ = C₂V₂, the amount of solute is unchanged before and after dilution; the final volume V₂ = C₁V₁ ÷ C₂; the solvent to add = V₂ − V₁; the dilution factor = C₁ ÷ C₂, used for preparing lab solutions and diluting stock solutions.',
 'Initial concentration (mol/L)',
 'Initial volume (mL)',
 'Target concentration (mol/L)',
 'C₁V₁ = C₂V₂, the amount of solute is unchanged before and after dilution.',
 '10 mol/L, 100 mL diluted to 2 mol/L must be made up to 500 mL.',
 '📚 Deep Dive: Solution Dilution (C₁V₁ = C₂V₂)',
 'Dilution to volume: take 10 mL of 1 M and dilute to 100 mL to get 0.1 M.',
 'Water added: derive the amount of water from V1 and V2 (≈V2 − V1).',
 'Multi-step dilution: work out the final concentration step by step to avoid exceeding the range in a single step.',
 'Walkthrough: C1 = 1.0, V1 = 50 mL, C2 = 0.2',
 'Enter C1 = 1.0, V1 = 50 mL and C2 = 0.2, the tool outputs V2 = 250 mL (about 200 mL of water added) and notes that diluting to the final volume V2 is what counts.',
 'Is the water added = V2 − V1?',
 'It holds approximately for dilute solutions; for concentrated solutions volumes are not strictly additive, so dilute to the final volume V2.',
 'How does it differ from dilution-c1v1?',
 'This tool focuses on dilution scenarios (finding V2 or the water to add), while the other one solves for any fourth value.',
 'Any precautions when diluting concentrated acid?',
 'Add acid to water slowly with cooling to prevent splashing.',
]

for s, lst in B.items():
    write(s, build(s, lst))

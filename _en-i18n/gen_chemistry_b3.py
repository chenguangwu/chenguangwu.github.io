#!/usr/bin/env python3
# gen_chemistry_b3.py — chemistry b3 (5 slugs): limiting-reagent/mass-fraction/mass-percent/mass-to-moles/molality
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

LMR = [
 "Identify the limiting reagent and theoretical yield from the charge and stoichiometric ratio",
 "Enter the masses and molar masses of two reactants plus the reaction equation coefficients, and it decides which one is limiting.",
 "Limiting Reagent",
 "/ Limiting Reagent Calculator",
 "Limiting Reagent Calculator",
 "📖 View Guide: \"Identify the limiting reagent and theoretical yield from the charge and stoichiometric ratio\"",
 "ξ = n_i/ν_i, and the substance with the smaller value is the limiting reagent. Ex",
 "Reactant A mass (g)",
 "A molar mass (g/mol)",
 "A coefficient",
 "Reactant B mass (g)",
 "B molar mass (g/mol)",
 "B coefficient",
 "Product molar mass (g/mol)",
 "Product coefficient",
 "ξ = n_i/ν_i, and the substance with the smaller value is the limiting reagent.",
 "Example: HCl of molar mass 36.46 at 10 g against NaOH of molar mass 40 at 8 g leaves A limiting.",
 "📚 Deep Dive: Identifying the limiting reagent and theoretical yield from the charge and stoichiometric ratio",
 "Charge optimisation: compare the mole counts of the reactants and find the smallest ratio, which is the limiting one, to avoid wasting feedstock.",
 "Theoretical yield: compute the upper limit of product mass from the limiting reagent ratio.",
 "Excess accounting: work out how many times over a reactant is charged, showing where the charge can be cut to save cost.",
 "N₂ + 3H₂ → 2NH₃ limiting reagent example",
 "Enter 1 mol of N₂ and 2 mol of H₂ and the tool finds H₂ limiting, since 2/3 is below 1/1, gives a theoretical NH₃ of about 1.33 mol and notes that 0.33 mol of N₂ is left over.",
 "How is the limiting reagent found?",
 "Divide each reactant's moles by its own coefficient; the smallest result is the limiting one.",
 "Does the excess reagent count towards the yield?",
 "No, the yield is set by the limiting reagent and the excess simply remains.",
 "Must the coefficients be balanced integers?",
 "The simplest integer ratio is enough; what matters is the mole ratio.",
]

MFR = [
 "Mass fraction (w = m_solute / m_total x 100%)",
 "Compute the mass fraction of the solute in a solution.",
 "/ Mass Fraction Calculation",
 "Mass Fraction Calculation",
 "📖 View Guide: \"Mass fraction (w = m_solute / m_total x 100%)\"",
 "w = m_solute / m_total x 100%",
 "Total solution mass (g)",
 "w = m_solute / m_total x 100%.",
 "20 g of solute in 100 g of solution gives a mass fraction of 20%.",
 "📚 Deep Dive: Mass fraction (w = m_solute / m_total x 100%)",
 "Preparing a solution: dissolve 10 g of salt in 90 g of water to get w = 10%.",
 "Laboratory reports: compute the mass fraction of each component from weighing data to fill in the test report.",
 "Rechecking after dilution: the solute mass is conserved across a dilution, so back out the new w to verify the label.",
 "5 g of solute in 50 g of solution",
 "Enter 5 g of solute and 50 g of solution and the tool outputs the",
 "mass fraction w",
 "= 10.0%, noting how it differs from the molar concentration.",
 "Can a mass fraction exceed 100%?",
 "No, the solute mass is at most the total mass; anything above that means a weighing or definition error.",
 "How does it differ from molar concentration?",
 "The mass fraction is unaffected by volume changes with temperature, while mol/L depends on both.",
 "Does it work for solid mixtures?",
 "Yes, the mass fraction applies to any homogeneous mixture.",
]

MPE = [
 "Find the mass fraction, the percentage concentration, from the solute and solution masses",
 "Enter the solute mass and the total solution mass to get the mass fraction, the percentage concentration.",
 "Mass fraction w",
 "/ Mass Fraction Calculator",
 "📖 View Guide: \"Find the mass fraction from the solute and solution masses\"",
 "w = m_solute / m_solution. 9 g of NaCl in 100 g of solution gives 9%.",
 "Solution mass (g)",
 "w = m_solute / m_solution.",
 "9 g of NaCl in 100 g of solution gives 9%.",
 "📚 Deep Dive: Finding the mass fraction from the solute and solution masses",
 "Labelling a formulation: compute the mass percentage of the active substance from the raw material ratio to write the label.",
 "Quality checks: compare the measured content against the stated percentage to judge conformance.",
 "Blending: work out the overall",
 "mass fraction",
 "when two solutions are mixed.",
 "20 g of solute in 200 g of solution",
 "Enter 20 g of solute and 200 g of solution and the tool gives a mass percentage of 10.0%, noting that switching to a volume percentage needs the density as a bridge.",
 "Does it overlap with the mass-fraction tool?",
 "Both use the same formula; this one targets the direct solute plus solution input case with a simpler interface.",
 "Can mass and volume percentages be interchanged?",
 "Only through the density as a bridge, not directly; the error is largest for non-aqueous systems.",
 "Does water content count towards the mass fraction?",
 "Yes, water as the solvent is part of the total mass.",
]

MTM = [
 "Convert mass to amount of substance (n = m / M)",
 "Given the mass and molar mass of a substance, find the amount of substance in moles.",
 "Mass to Amount of Substance Calculator",
 "/ Mass to Amount of Substance",
 "Mass to Amount of Substance",
 "📖 View Guide: \"Convert mass to amount of substance (n = m / M)\"",
 "n = m / M, where m is the mass in g and M the molar mass in g/mol.",
 "18 g of water, H₂O with M = 18.015, is about 1 mol.",
 "📚 Deep Dive: Converting mass to amount of substance (n = m / M)",
 "Weighing out a solution: from the target moles and M, compute the mass to weigh and guide the balance work.",
 "Reaction stoichiometry: convert masses into mole ratios to check the charge.",
 "Yield checks: back out the moles from the product mass and combine it with the yield.",
 "5.0 g of NaOH with M = 40",
 "Enter a mass of 5.0 g and M = 40 g/mol and the tool gives n = 0.125 mol, noting that hydrates must include the water of crystallisation.",
 "Where does M come from?",
 "Sum the atomic weights from the chemical formula, and include the water of crystallisation for hydrates such as CuSO₄·5H₂O.",
 "Why convert between mass and moles?",
 "Reactions are counted in moles while the balance gives mass, so a conversion is needed to match the equation.",
 "Does it work for gases?",
 "Yes. Volume is more common for gases, but the mass route applies just as well.",
]

MLT = [
 "Molality (b = n / m_solvent)",
 "Molality is the amount of solute divided by the solvent mass in kg, independent of temperature.",
 "Molality Calculator",
 "/ Molality",
 "Molality",
 "📖 View Guide: \"Molality (b = n / m_solvent)\"",
 "b = n / m_solvent",
 "Solvent mass (kg)",
 "b = n_solute / m_solvent in kg.",
 "1 mol dissolved in 0.5 kg of solvent gives 2 mol/kg.",
 "📚 Deep Dive: Molality (b = n / m_solvent)",
 "Freezing point depression: from b and Kf compute ΔTf and estimate the freezing point.",
 "Preparation basis: weigh solute and solvent to get b, unaffected by volume changes with temperature.",
 "Osmotic pressure: compute the osmotic pressure as π = bRT from b.",
 "0.1 mol of solute in 0.5 kg of water",
 "Enter n = 0.1 mol and a solvent mass of 0.5 kg and the tool gives b = 0.20 mol/kg, noting that the solvent mass excludes the solute.",
 "How does it differ from",
 "molar concentration",
 "?",
 "Molality uses the solvent mass and is unaffected by volume changes with temperature, while molarity uses the solution volume.",
 "Why do colligative properties use b?",
 "Colligative properties depend only on the number of particles per solvent mass, so b is more stable.",
 "Does the solvent mass include the solute?",
 "No, it is the mass of the pure solvent; the solution mass is the solvent plus the solute.",
 "How to use molality (b = n / m_solvent)",
 "It suits colligative calculations: estimating freezing point depression and boiling point elevation from the molality, computing osmotic pressure for plant cell plasmolysis or reverse osmosis design, and preparing standard solutions unaffected by temperature and volume for physical chemistry experiments.",
 "What is molality, b = n / m_solvent, for?",
 "Enter the amount of solute and the solvent mass in kg and it computes the molality as b = n/m; this concentration is independent of temperature and is common in colligative and thermodynamic work.",
 "How do I use molality, b = n / m_solvent?",
 "Which scenarios suit molality, b = n / m_solvent?",
 "Molality b is the amount of solute in mol divided by the solvent mass in kg, in mol/kg, expressing the amount of solute per kilogram of solvent.",
 "Difference from molar concentration",
 "Molar concentration c is the solute in mol divided by the solution volume in L and varies with temperature through thermal expansion, while molality is based on mass and is unaffected by temperature, so it is preferred for colligative properties such as boiling point elevation and freezing point depression.",
]

write('limiting-reagent', build('limiting-reagent', LMR))
write('mass-fraction', build('mass-fraction', MFR))
write('mass-percent', build('mass-percent', MPE))
write('mass-to-moles', build('mass-to-moles', MTM))
write('molality', build('molality', MLT))

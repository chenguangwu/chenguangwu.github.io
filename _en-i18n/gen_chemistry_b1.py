#!/usr/bin/env python3
# gen_chemistry_b1.py — chemistry b1 (5 slugs): acid-base-titration/arrhenius/boiling-point-elevation/buffer-ph/dilution-c1v1
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

ABT = [
 "Acid-base neutralisation titration calculator",
 "Work out the volume of the other solution needed for neutralisation from the acid-base equivalence.",
 "/ Acid-Base Neutralisation Titration",
 "Acid-Base Neutralisation Titration",
 "📖 View Guide: \"Acid-Base Neutralisation Titration Calculator\"",
 "Volume of base needed for neutralisation, V_b = C_a·V_a·n_a / (C_b·n_b)",
 "Acid concentration (mol/L)",
 "Acid volume (mL)",
 "Acid proticity n_a",
 "Base concentration (mol/L)",
 "Base proticity n_b",
 "V_b = C_a·V_a·n_a / (C_b·n_b), where n is the number of ionisable H⁺ or OH⁻ groups.",
 "A monoprotic acid and a monobasic base of equal concentration neutralise at equal volumes.",
 "📚 Deep Dive: Acid-base neutralisation titration calculator",
 "Finding a concentration by strong acid-strong base titration: titrate unknown HCl with NaOH of known concentration and back out the HCl concentration from the volume used, to verify a laboratory result.",
 "Predicting the end point volume: given a target concentration and the standard solution concentration, budget the titrant volume needed to reach the equivalence point and pace the addition.",
 "Re-measuring a diluted sample: dilute an over-concentrated sample before titrating, then convert back to the original concentration using the dilution factor to widen the working range.",
 "0.1000 mol/L NaOH titrating unknown HCl",
 "Enter a standard solution of 0.1000 mol/L, 23.50 mL consumed and a 25.00 mL sample, and the tool back-calculates HCl at about 0.0940 mol/L, reminding you that the end point volume is the final reading minus the initial one to avoid cumulative error.",
 "How should the indicator be chosen?",
 "Phenolphthalein or methyl orange both work for strong acid against strong base; weak pairs must follow the pH jump range or the end point is misjudged. This tool only computes concentration, the indicator is an experimental choice.",
 "Is the concentration from the titrant volume reliable?",
 "It holds when the system is close to complete neutralisation with no significant side reactions; weak acids and bases need dissociation accounted for, so judge the end point together with the pH curve.",
 "Why read the consumed volume as a difference?",
 "The burette usually starts at a non-zero reading, so the end point volume is the final reading minus the initial one; reading it directly brings in cumulative error.",
]

ARR = [
 "How temperature affects the reaction rate constant",
 "Enter the pre-exponential factor A, the activation energy Ea and the temperature to get the rate constant k.",
 "Arrhenius Equation Calculator",
 "/ Arrhenius Equation Calculator",
 "📖 View Guide: \"How temperature affects the reaction rate constant\"",
 "Pre-exponential factor A (s⁻¹)",
 "Activation energy Ea (J/mol)",
 "📚 Deep Dive: How temperature affects the reaction rate constant",
 "Comparing rates as temperature rises: given Ea and T1/T2, compute k2/k1 to quantify how much a temperature rise speeds the reaction.",
 "Estimating activation energy: back out Ea from two temperature and rate constant pairs when analysing kinetic data.",
 "Judging storage stability: low temperature lowers k and lengthens",
 "shelf life, so the slowdown estimates how long a material can be kept.",
 "Ea = 50 kJ/mol with a 10 K rise",
 "Enter Ea = 50 kJ/mol with T1 = 300 K and T2 = 310 K and the tool gives k2/k1 ≈ 2.0, showing the rate roughly doubles, the empirical rule of doubling per 10 K.",
 "Why does the rate climb exponentially with temperature?",
 "The Arrhenius exponential contains -Ea/RT, so a higher temperature raises the rate constant almost exponentially rather than linearly.",
 "Should Ea be in kJ or J?",
 "The formula pairs J/mol with R = 8.314; using kJ requires multiplying by 1000, and mixing the units gives a 1000-fold error.",
 "Can you predict the reaction time directly?",
 "A larger k means a faster rate, but the reaction time also depends on the reaction order, so only similar reactions can be compared.",
]

BPE = [
 "Boiling Point Elevation Calculator",
 "The boiling point elevation of a dilute solution of a non-volatile nonelectrolyte is proportional to its molality.",
 "/ Boiling Point Elevation Calculation",
 "Boiling Point Elevation Calculation",
 "📖 View Guide: \"Boiling Point Elevation Calculator\"",
 "Boiling point elevation, ΔT_b = K_b · m · i",
 "Boiling point elevation constant (°C·kg/mol)",
 "Molality (mol/kg)",
 "Van 't Hoff factor",
 "ΔT_b = K_b·m·i, with K_b = 0.512 °C·kg/mol for water.",
 "A 1 mol/kg nonelectrolyte raises the boiling point of water by about 0.512 °C.",
 "📚 Deep Dive: Boiling Point Elevation Calculator",
 "Judging the boiling point of an aqueous solution: from the",
 "molality",
 "of a non-volatile solute such as sucrose, compute ΔTb and get the solution boiling point.",
 "Comparing solvent Kb: compare the Kb of water, benzene and ethanol to see how the solvent changes the boiling point elevation.",
 "Back-calculating",
 ": infer the molar mass of the solute from the measured elevation, the colligative property method.",
 "0.50 mol/kg sucrose solution in water",
 "Enter a",
 "molality",
 "of 0.50 mol/kg with Kb = 0.512 K·kg/mol for water and the tool gives ΔTb ≈ 0.256 °C, so the solution boils at about 100.256 °C.",
 "When does the formula apply?",
 "Only for dilute solutions of a non-volatile nonelectrolyte; electrolytes need the van 't Hoff factor i multiplied in.",
 "Why do electrolytes deviate so much?",
 "NaCl dissociates with i ≈ 2, so ΔTb nearly doubles; correct with i before calculating.",
 "Does altitude affect the boiling point?",
 "Lower outside pressure lowers the boiling point; this formula covers the solute induced rise at the same pressure, which is independent of the altitude effect.",
]

BPH = [
 "Enter pKa and the conjugate base to acid concentration ratio to get the pH of a buffer solution.",
 "Henderson-Hasselbalch Equation",
 "/ Buffer Solution pH Calculator",
 "Buffer Solution pH Calculator",
 "📖 View Guide: \"Henderson-Hasselbalch Equation\"",
 "pH = pKₐ + log([A⁻]/[HA]). For an acetate buffer with pKa = 4.76, equal concentrations give pH = 4.76.",
 "Conjugate base concentration [A⁻] (mol/L)",
 "Weak acid concentration [HA] (mol/L)",
 "For an acetate buffer with pKa = 4.76, equal concentrations give pH = 4.76.",
 "📚 Deep Dive: Henderson-Hasselbalch equation",
 "Preparing a buffer pH: given the acetic acid to sodium acetate ratio and pKa, budget the target pH and guide the dosing.",
 "Judging buffer capacity: the capacity peaks when [A⁻]/[HA] is near 1 and the further it strays, the easier it is for added acid or base to break through.",
 "pH shift after adding acid: estimate how the ratio change from added strong acid moves the pH, verifying the buffer capacity.",
 "Acetic acid and sodium acetate buffer pH",
 "Enter pKa = 4.76 with [A⁻]/[HA] = 1 and the tool gives pH ≈ 4.76; raising the ratio to 10 gives pH ≈ 5.76, showing the logarithmic effect of the ratio on pH.",
 "When is the formula inaccurate?",
 "The deviation grows when the acid or base concentration approaches the amount dissociated, or when the pH is more than 2 units from pKa.",
 "How is buffer capacity maximised?",
 "Capacity peaks at [A⁻] = [HA], i.e. pH = pKa; the further you move away, the easier it is for added acid or base to break through.",
 "How does this relate to biological buffers?",
 "Blood relies on the H₂CO₃/HCO₃⁻ buffer with pH ≈ 6.1 + lg([HCO₃⁻]/[H₂CO₃]), the same principle as this formula.",
 "How to use the Henderson-Hasselbalch equation",
 "It suits the pH estimation and preparation of buffer solutions such as acetic acid/sodium acetate or ammonia/ammonium salt: keeping enzymes at their optimum pH in biochemical work, designing titration systems in analytical chemistry, and demonstrating the logarithmic relation between buffer capacity, the conjugate ratio and pH in teaching.",
 "What is the Henderson-Hasselbalch equation for?",
 "It is a buffer solution pH calculator: enter pKa and the conjugate base to acid ratio to get the pH from the Henderson-Hasselbalch equation, used to design buffer systems.",
 "How do I use the Henderson-Hasselbalch equation?",
 "Which scenarios suit the Henderson-Hasselbalch equation?",
]

DCV = [
 "Find the fourth quantity from any three, concentration or volume",
 "Enter the initial concentration and volume plus the target concentration to get the volume needed, or solve for the target volume.",
 "Dilution formula C₁V₁ = C₂V₂",
 "/ Solution Dilution Calculator",
 "📖 View Guide: \"Find the fourth quantity from any three, concentration or volume\"",
 "(0 = solve for this) (mL)",
 "Initial concentration C₁ (mol/L)",
 "Initial volume V₁ (mL)",
 "Target concentration C₂ (mol/L)",
 "Target volume V₂ (0 = solve for this) (mL)",
 "C₁V₁ = C₂V₂ expresses conservation of solute before and after dilution.",
 "1 mol/L x 100 mL diluted to 0.1 mol/L needs 1000 mL.",
 "📚 Deep Dive: Find the fourth quantity from any three, concentration or volume",
 "Diluting to volume: given the stock C1 and V1 plus the target C2, compute the final volume V2 to make up to.",
 "Stock volume to take: given C1, C2 and V2, compute the stock volume V1 needed.",
 "Reverse checking: infer the other concentration from known V1/V2 and one concentration to audit the lab record.",
 "Taking 10 mL of a 1.0 mol/L stock solution",
 "Enter C1 = 1.0 mol/L, V1 = 10 mL and V2 = 100 mL and the tool gives C2 = 0.10 mol/L, reminding you to make up to the final volume.",
 "Can volumes simply be added?",
 "Dilution means making up to V2, not V1 plus the water added equalling V2, since concentrated solutions contract; use the final volume.",
 "Must the units of C and V agree?",
 "The concentrations need consistent units among themselves and so do the volumes, otherwise the result will be wrong.",
 "How does it differ from the",
 "solution dilution",
 "tool?",
 "This tool solves any fourth quantity and is more general, while the solution dilution tool always solves for the diluted concentration or the water to add.",
]

write('acid-base-titration', build('acid-base-titration', ABT))
write('arrhenius', build('arrhenius', ARR))
write('boiling-point-elevation', build('boiling-point-elevation', BPE))
write('buffer-ph', build('buffer-ph', BPH))
write('dilution-c1v1', build('dilution-c1v1', DCV))

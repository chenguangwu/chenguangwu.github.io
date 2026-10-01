#!/usr/bin/env python3
# gen_chemistry_b2.py — chemistry b2 (5 slugs): empirical-formula/gas-density/gibbs-free-energy/ideal-gas-volume/kp-kc
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

EMF = [
 "Convert element mass percentages into the simplest whole-number ratio of atoms",
 "Enter the mass percentages and atomic weights of up to three elements; it works out the atom ratio and reduces it.",
 "Empirical Formula from Mass Percentages",
 "/ Empirical Formula Calculator",
 "Empirical Formula Calculator",
 "📖 View Guide: \"Convert element mass percentages into the simplest whole-number ratio of atoms\"",
 "n_i = w_i% / A_i, then divide by the smallest value to get the integer ratio. Example: C 40%, H 6.7%, O 53.3% gives CH₂O.",
 "Element 1 mass % (%)",
 "Element 1 atomic weight (g/mol)",
 "Element 2 mass % (%)",
 "Element 2 atomic weight (g/mol)",
 "Element 3 mass % (%)",
 "Element 3 atomic weight (g/mol)",
 "n_i = w_i% / A_i, then divide by the smallest value to get the integer ratio.",
 "Example: C 40%, H 6.7%, O 53.3% gives CH₂O.",
 "📚 Deep Dive: Converting element mass percentages into the simplest whole-number ratio of atoms",
 "Turning elemental analysis into an empirical formula: from the C/H/O",
 "mass fractions",
 "compute the mole ratio and reduce it to the simplest integers.",
 "Verifying the molecular formula: from the empirical formula mass and the measured",
 "molecular weight",
 "infer the multiplier n of the molecular formula.",
 "Approximate judgement for mixtures: roughly infer the likely group composition from the ratios of the major elements.",
 "C 40% / H 6.7% / O 53.3% empirical formula example",
 "Enter the mass fractions and the tool gets a C:H:O mole ratio of about 1:2:1, outputs the empirical formula CH₂O and notes that the molecular weight is needed to confirm the molecular formula.",
 "What if the mass fractions do not add to 100%?",
 "There may be unmeasured elements such as nitrogen, ash or water of crystallisation, so check for missing items before converting.",
 "Is the empirical formula the same as the molecular formula?",
 "Not necessarily: the empirical formula is the smallest integer ratio, while the molecular formula is the empirical formula times n, which needs the molecular weight to confirm.",
 "How do you turn a decimal ratio into integers?",
 "After dividing by the smallest value, multiply by factors such as 2/3 to land near integers, as in 1:2.01:1 ≈ 1:2:1.",
 "How to use converting element mass percentages into the simplest whole-number ratio of atoms",
 "It suits compound composition analysis: turning element mass fractions from an elemental analyser into the simplest whole-number atom ratio, estimating the empirical formula and then deriving the molecular formula, plus composition exercises in organic and inorganic chemistry teaching.",
 "What is converting element mass percentages into the simplest whole-number ratio of atoms for?",
 "Enter the mass percentages and atomic weights of up to three elements and it automatically finds the atom ratio and reduces it to the simplest integers, giving the empirical formula of the compound.",
 "How do I use converting element mass percentages into the simplest whole-number ratio of atoms?",
 "Which scenarios suit converting element mass percentages into the simplest whole-number ratio of atoms?",
]

GSD = [
 "Ideal gas density (ρ = PM / RT)",
 "Estimate the ideal gas density from the pressure, molar mass and temperature.",
 "Gas Density Calculator",
 "/ Gas Density Calculation",
 "Gas Density Calculation",
 "📖 View Guide: \"Ideal gas density (ρ = PM / RT)\"",
 "ρ = PM / RT with R = 8.314, and the result is in g/L. Air at 28.97 gives about 1.29 g/L at STP.",
 "ρ = PM / RT with R = 8.314, and the result is in g/L.",
 "Air at 28.97 is about 1.29 g/L at STP.",
 "📚 Deep Dive: Ideal gas density (ρ = PM / RT)",
 "Working conditions",
 ": compute the actual working density from the standard density and P/T, to guide metering at working conditions.",
 "molar mass",
 "estimation: back out the value from the measured density and P/T.",
 "Judging whether a gas rises: compare the density with air to decide if the gas rises or sinks in a ventilation design.",
 "28 g/mol gas density at standard conditions",
 "Enter M = 28 g/mol, P = 1 atm and T = 273 K and the tool gives ρ ≈ 1.29 g/L, close to the density of air, so there is no marked rise or sink.",
 "When does the ideal gas assumption fail?",
 "Real gases deviate at high pressure and low temperature, so a compressibility factor Z is needed, giving ρ = PM/ZRT.",
 "How do you convert from the standard condition density?",
 "ρ/ρ₀ = (P/P₀)(T₀/T), and the temperature must use the absolute scale K.",
 "Must the units be consistent?",
 "Match P in Pa or atm with R; T must be in K, since using degrees Celsius gives a wrong answer.",
]

GFE = [
 "Judge whether a reaction is spontaneous",
 "Enter the enthalpy change, entropy change and temperature to get the Gibbs free energy change and the reaction direction.",
 "Gibbs Free Energy Calculator",
 "/ Gibbs Free Energy Calculator",
 "📖 View Guide: \"Judge whether a reaction is spontaneous\"",
 "Enthalpy change ΔH (kJ/mol)",
 "Entropy change ΔS (kJ/(mol·K))",
 "ΔG = ΔH - TΔS, with the units consistent in kJ.",
 "ΔH = -100, ΔS = 0.05, T = 298 gives ΔG ≈ -114.9, spontaneous.",
 "📚 Deep Dive: Judging reaction spontaneity",
 "Spontaneity check: compute ΔG from ΔH, ΔS and T, where ΔG < 0 means spontaneous.",
 "Transition temperature: solve ΔG = 0 for T = ΔH/ΔS to see whether the spontaneous range lies at high or low temperature.",
 "Identifying entropy driven reactions: with ΔH > 0 but ΔS > 0 the reaction becomes spontaneous at high temperature, as with ice melting.",
 "ΔH = -100 kJ/mol, ΔS = +50 J/mol·K example",
 "Enter T = 298 K and the tool gives ΔG ≈ -114.9 kJ/mol, judged spontaneous, and notes that T = 2000 K is the transition temperature where ΔG = 0.",
 "Does ΔG < 0 guarantee the reaction happens?",
 "It only means thermodynamically spontaneous; the rate is set by kinetics and may be extremely slow, as with diamond turning into graphite.",
 "Should entropy be in J or kJ?",
 "With ΔH in kJ and ΔS in J the TΔS term is off by a factor of 1000, so both must use the same energy unit.",
 "Do standard and actual conditions differ?",
 "Real concentrations or partial pressures need ΔG = ΔG° + RT ln Q, while this tool computes directly from the values given.",
]

IGV = [
 "Ideal gas volume (V = nRT / P)",
 "Use the ideal gas law PV = nRT to find the gas volume at a given pressure, temperature and amount of substance.",
 "Ideal Gas Law Calculator",
 "/ Ideal Gas Volume",
 "Ideal Gas Volume",
 "📖 View Guide: \"Ideal gas volume (V = nRT / P)\"",
 "At standard conditions of 0 °C and 101.325 kPa, one mole of ideal gas occupies about 22.4 L.",
 "📚 Deep Dive: Ideal gas volume (V = nRT / P)",
 "Verifying the standard volume: one mole at 0 °C and 1 atm is about 22.4 L, which checks the stoichiometric relation.",
 "Working condition",
 "volume conversion",
 ": compute the actual volume from n and P/T to guide vessel selection.",
 "Estimating gas output: from the moles reacted, compute the gas volume generated to size venting or collection.",
 "n = 2 mol, T = 298 K, P = 1 atm example",
 "Enter n = 2 mol, T = 298 K and P = 1 atm and the tool gives V ≈ 48.9 L, comparing it with 44.8 L at standard conditions to show the temperature effect.",
 "Why is the standard volume 22.4 L?",
 "One mole of ideal gas at 0 °C, or 273 K, and 1 atm follows directly from V = nRT/P.",
 "How does the volume change as pressure rises?",
 "At fixed n and T the volume is inversely proportional to pressure, so raising the pressure shrinks the volume.",
 "Does it work for real gases?",
 "The approximation is good at low pressure and high temperature, while high pressure needs the compressibility factor Z.",
]

KPK = [
 "Converting equilibrium constants for gas reactions",
 "Enter Kc, the temperature and the change in gas moles Δn to get Kp, with R = 8.314 and T in kelvin.",
 "Kp and Kc Converter",
 "/ Kp and Kc Converter",
 "📖 View Guide: \"Converting equilibrium constants for gas reactions\"",
 "R = 8.314. When Δn = 0, Kp = Kc.",
 "Concentration equilibrium constant Kc",
 "Change in gas moles Δn",
 "When Δn = 0, Kp = Kc.",
 "📚 Deep Dive: Converting equilibrium constants for gas reactions",
 "Converting Kp to Kc and back: given Kc, T and Δn, the gas stoichiometric difference, find Kp.",
 "Determining Δn: the sign of Δn follows the difference between the gas stoichiometric coefficients in the reaction equation and sets the direction of the conversion.",
 "Temperature effect: the RT term varies with T, which is why Kp and Kc generally differ.",
 "Kc = 0.5, T = 298 K, Δn = 1 example",
 "Enter Kc = 0.5, T = 298 K and Δn = 1 and the tool gives Kp ≈ 12.3 with RT ≈ 24.6 L·atm/mol, noting that Kp = Kc when Δn = 0.",
 "How is Δn computed?",
 "It is the sum of the gas stoichiometric coefficients of the products minus that of the reactants; with no gas or equal amounts Δn = 0 and Kp = Kc.",
 "Which value of R?",
 "Match it to the pressure unit: 0.0821 L·atm/(mol·K) when P is in atm, or 8.314 when it is in Pa.",
 "Do Kp and Kc have the same dimensions?",
 "The values and dimensions differ, since (RT)^Δn carries units, so they cannot be compared directly.",
]

write('empirical-formula', build('empirical-formula', EMF))
write('gas-density', build('gas-density', GSD))
write('gibbs-free-energy', build('gibbs-free-energy', GFE))
write('ideal-gas-volume', build('ideal-gas-volume', IGV))
write('kp-kc', build('kp-kc', KPK))

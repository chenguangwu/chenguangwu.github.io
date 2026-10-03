#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'misc')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'misc')
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
    out = {'slug': slug, 'industry': 'misc', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('physics-constants', build('physics-constants', [
        "📚 Physics Constants Quick Reference",
        "Built-in 30+ common physics constants, with values, units, symbols and descriptions, supporting search and category filtering. Data based on CODATA 2018 recommended values.",
        "Common physics constants (CODATA 2018 recommended values): speed of light in vacuum c = 299792458 m/s, Planck constant h = 6.62607015×10⁻³⁴ J·s, elementary charge e = 1.602176634×10⁻¹⁹ C, Avogadro constant N_A = 6.02214076×10²³ mol⁻¹, Boltzmann constant k = 1.380649×10⁻²³ J/K.",
        "No matching constant found",
        "📐 Mnemonics for Common Constants",
        "Speed of light c:",
        "About 3×10⁸ m/s, the upper limit of information transfer in vacuum.",
        "Planck constant h:",
        "About 6.626×10⁻³⁴ J·s, a core constant of quantum mechanics.",
        "Gravitational constant G:",
        "About 6.674×10⁻¹¹ N·m²/kg², Newton's gravitational constant.",
        "Avogadro number Nₐ:",
        "About 6.022×10²³ /mol, the number of particles in one mole.",
        "📚 In-Depth: Physics Constants Quick Reference",
        "When substituting into formulas, accurate constants such as c, h, e, G, N_A are needed to avoid magnitude errors from misremembering.",
        "In dimensional checks, use constants to align results across unit systems (SI, CGS).",
        "In teaching and popular-science writing, cite the latest CODATA / SI defined values to keep statements rigorous.",
        "Example: Speed of Light in Vacuum and Planck Constant",
        "c=299792458 m/s (defined value, exact); h=6.62607015×10⁻³⁴ J·s (defined value, exact). From E=hν we get",
        "photon energy",
        ", for example when ν=5×10¹⁴ Hz, E≈3.313×10⁻¹⁹ J.",
        "Example: Avogadro Constant and the Mole",
        "N_A = 6.02214076×10²³ mol⁻¹ (defined value). One mole of carbon-12 contains N_A atoms; from m = M/N_A one can convert",
        "M into a single particle's mass, e.g. for H₂O (M≈18 g/mol) a single molecule ≈ 2.99×10⁻²³ g.",
        "Which constants are 'exact values'?",
        "After the 2019 SI redefinition, c, h, e, k_B, N_A etc. were assigned exact values (infinite significant digits); the remaining constants (e.g. G, fine-structure constant) are still experimentally determined with uncertainties and are fine-tuned with CODATA updates.",
        "Why is G's precision far lower than other constants?",
        "universal gravitation",
        "The constant G is extremely weak; experiments are easily disturbed by the environment, and its measurement uncertainty remains at the 10⁻⁵ level, making it one of the fundamental constants with the largest relative error; whereas c, h etc. are locked by definition and no longer have experimental error.",
        "About 'Physics Constants Quick Reference'",
        "The physics constants quick reference is an online tool in the scientific research field. A scientific research tool that uses standard scientific formulas for accurate calculation.",
        "Search constant name / symbol (e.g. speed of light, Planck, G)",
    ]))
    write('scientific-notation', build('scientific-notation', [
        "🔄 Scientific Notation Converter",
        "Two-way conversion between standard decimals and scientific notation (a×10^n), supporting engineering notation and E notation.",
        "Performs professional calculation from the input parameters and outputs the result, based on 'two-way conversion between standard decimals and scientific notation (a×10^n), supporting engineering notation and E notation'.",
        "Enter a number (plain decimal or scientific notation both OK, e.g. 12345 or 1.23e4 or 6.022e23)",
        "Copy scientific notation",
        "Copy full decimal",
        "Reverse: scientific notation -> plain decimal",
        "Convert to plain decimal",
        "📐 About Scientific Notation",
        "Standard form:",
        "a × 10^n, where 1 ≤ |a| < 10, and n is an integer.",
        "The mantissa a satisfies 1 ≤ |a| < 1000, and the exponent n is a multiple of 3.",
        "E notation:",
        "The common form in computers, e.g. 6.022E23 means 6.022×10²³.",
        "Engineering notation",
        "📚 In-Depth: Scientific Notation Conversion",
        "When dealing with astronomical, microscopic or financial extremes (e.g. galaxy mass, atomic radius, national debt), scientific notation avoids writing long strings of zeros and reduces misreading.",
        "In engineering and programming, normalize float strings like 6.022e23 into the standard form m×10^n (1≤|m|<10) to ease magnitude comparison.",
        "significant digits",
        "In precision expression, scientific notation explicitly states retained digits, distinguishing 1.0×10³ from 1.00×10³.",
        "Example: Avogadro constant",
        "N_A = 602214076000000000000000 expressed as 6.02214076×10²³. Method: exponent e = ⌊log₁₀|N|⌋ = 23, mantissa m = N/10²³ = 6.02214076, satisfying 1≤m<10.",
        "Example: Representing Very Small Values",
        "Electron charge e = 0.0000000000000000001602176634 C expressed as 1.602176634×10⁻¹⁹ C. For very small values e = ⌊log₁₀|N|⌋ is negative, as in this example e = -19, m = 1.602176634.",
        "What is the difference between scientific and engineering notation?",
        "Scientific notation requires mantissa 1≤|m|<10 with any integer exponent; engineering notation requires the exponent to be a multiple of 3 (e.g. 10³, 10⁶, 10⁻⁹), with the mantissa accordingly between 1 and 1000, making it easy to map to SI prefixes like k, M, μ.",
        "How to decide how many significant digits to keep?",
        "It is determined by the precision of the measurement or data. For example 6.022×10²³ is 4 significant digits, 6.02214076×10²³ is 9; trailing zeros are meaningful (1.0×10³ ≠ 1×10³). Conversion should not invent significant digits that were not there.",
        "About 'Scientific Notation Converter'",
        "The scientific notation converter is an online tool in the scientific research field. A scientific research tool that uses standard scientific formulas for accurate calculation.",
        "Enter any number",
        "Mantissa a",
        "Exponent n",
    ]))

if __name__ == '__main__':
    main()

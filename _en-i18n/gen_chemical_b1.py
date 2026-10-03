#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'chemical')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'chemical')
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
    out = {'slug': slug, 'industry': 'chemical', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('detector-39', build('detector-39', [
        "🔍 Chemical Product Purity Calculation and Quality Verdict",
        "Supports acid-base titration and gravimetric methods to calculate chemical purity; enter the experimental data to compute the purity percentage automatically and check it against the standard threshold.",
        "'Supports acid-base titration and gravimetric methods to calculate chemical purity; enter the experimental data to compute the purity percentage automatically and check it against the standard threshold.' Performs a professional calculation from the input parameters and outputs the result.",
        "Quality (Purity/Standard/Testing) Assurance",
        "/ Quality (Purity/Standard/Testing) Assurance",
        "📖 View the usage guide for 'Chemical Product Purity Calculation and Quality Verdict'",
        "Acid-base titration method",
        "Gravimetric method",
        "Titrant concentration c (mol/L)",
        "Titrant consumption volume V (mL)",
        "Sample mass m (g)",
        "Molar mass M (g/mol)",
        "Reaction stoichiometric ratio n (mol analyte/mol titrant)",
        "Qualified purity threshold (%)",
        "Sample mass m₁ (g)",
        "Mass after drying/ignition m₂ (g)",
        "Conversion factor F (molar mass of target / molar mass of weighed form)",
        "Calculate purity",
        "Acid-base titration: purity(%) = (c × V × n × M / m) × 100, where c is the titrant concentration, V the consumption volume, n the stoichiometric ratio, M the molar mass and m the sample mass",
        "Gravimetric method: purity(%) = (m₂ × F / m₁) × 100, where m₁ is the sample mass, m₂ the mass after drying/ignition and F the conversion factor",
        "Blank test: in actual operation the blank consumption volume should be deducted; this tool can accept the net consumption volume after the blank has been deducted",
        "Parallel determinations should be no fewer than 3, take the mean value, and the relative deviation should be ≤0.2%",
        "📚 Deep Dive: Chemical Product Purity Calculation and Quality Verdict",
        "Titration purity calculation: compute the purity of the analyte from the standard",
        "solution concentration",
        ", the consumption volume and the stoichiometric ratio.",
        "Gravimetric purity accounting: convert the mass of the weighed form into the target component's",
        "mass fraction",
        "Release verdict: check the purity against the product standard threshold and give a qualified/unqualified conclusion with the deviation.",
        "Titration purity walkthrough",
        "Entering standard solution concentration 0.1mol/L, consumption 25.0mL, stoichiometric ratio 1:1 and sample 0.5000g, the tool outputs a purity of about 50.0% (by equivalent conversion) and checks it against the threshold.",
        "Which is more accurate, titration or gravimetry?",
        "Each has its own application: titration is fast and suits macro quantities; gravimetry is more accurate but time-consuming. Follow the method specified in the product standard, and use the arbitration method when in dispute.",
        "How do I investigate the cause when the purity falls short?",
        "Check the titration endpoint judgement, the reagent concentration standardisation, the sample weighing and any interfering ions; re-check item by item to avoid systematic bias.",
        "Where do the thresholds come from?",
        "They come from the enterprise product standard or the national/industry standard (such as the GB/T series); this tool is only for calculation cross-checking, and the qualified verdict is governed by the formal standard.",
        "About 'Chemical Product Purity Calculation and Quality Verdict'",
        "A chemical product purity calculation tool supporting the two common purity determination methods, acid-base titration and gravimetry. Enter the experimental data to compute the purity percentage automatically and judge whether the product quality is qualified against the standard threshold.",
        "Supports acid-base titration (concentration x volume x stoichiometric ratio)",
        "Supports the gravimetric method (weighed form conversion)",
        "Customisable qualified purity threshold",
        "Laboratory chemical product purity determination",
        "Raw material incoming inspection",
        "Finished product release quality verdict",
        "Chemical analysis laboratory teaching",
    ]))

    write('calc-pipeline-pressure-drop', build('calc-pipeline-pressure-drop', [
        "🎚️ Pipeline Pressure Drop (Darcy Formula) Calculation",
        "Enter two parameters to compute the common result automatically",
        "📖 View the usage guide for 'Pipeline Pressure Drop (Darcy Formula) Calculation'",
        "ΔP = f · (L/D) · (ρ·v²/2) (Darcy-Weisbach formula)",
        "Pipe diameter D (mm)",
        "Roughness ε (mm)",
        "💡 The friction pressure drop is proportional to the pipe length, inversely proportional to the diameter, and is affected by the square of the velocity and the friction factor; it is used for pump selection and network design.",
        "📚 Deep Dive: Pipeline Pressure Drop (Darcy Formula) Calculation",
        "Plant transfer pipeline friction accounting: given the diameter and flow rate, estimate the friction pressure drop and judge whether pressurisation or a larger diameter is needed.",
        "Pump selection head margin assessment: convert the friction and local pressure drops into a head requirement, add the elevation difference and safety margin, and select the pump.",
        "Network renovation pressure drop comparison: compare the pressure drop of the old pipe (high roughness from scaling) with that of the new pipe to quantify the energy-saving potential of the renovation.",
        "DN200 steel pipe water transport pressure drop walkthrough",
        "Entering diameter 200mm, length 100m, velocity 1.5m/s, steel pipe roughness 0.045mm and water viscosity 1.0e-3 Pa·s, the tool outputs a friction pressure drop of about 0.9m water column by the Darcy formula, and gives",
        "the flow regime.",
        "What is the difference between the Darcy formula and the Hazen-Williams formula?",
        "Darcy-Weisbach works through a general friction factor and suits clean water and most Newtonian fluids; Hazen-Williams is used more for empirical estimation in water supply pipes. The choice of formula depends on the fluid and engineering convention.",
        "What do I do if the computed pressure drop is too large?",
        "Check whether the velocity is too high (a larger diameter lowers it), whether the roughness value is too strict (take a large value only for scaled old pipes), and whether local losses have been omitted; re-check item by item.",
        "What is the Reynolds number used for?",
        "The Reynolds number determines laminar/turbulent flow: <2000 laminar, >4000 turbulent, and the friction factor is taken differently. The result varies with the flow regime, so it is a prerequisite judgement in the pressure drop accounting.",
        "About 'Pipeline Pressure Drop (Darcy Formula) Calculation'",
        "A pipeline friction pressure drop calculation tool: estimates friction resistance loss based on the Darcy-Weisbach formula, assisting pump selection and network design. Processed in the front end, with data computed locally to protect privacy.",
        "One-click specification/parameter conversion: results in real time by formula",
        "Local computation: data never leaves the browser, protecting business data",
        "Results can be copied and exported: convenient for records and re-checking",
        "Supports switching common units: reduces manual conversion errors",
        "Plant transfer pipeline friction accounting",
        "Pump selection head margin assessment",
        "Network renovation pressure drop comparison",
        "Reynolds number flow regime determination",
        "Pipe diameter D (mm)",
        "Pipe length L (m)",
        "Velocity v (m/s)",
        "Viscosity μ (Pa·s)",
        "Roughness ε (mm)",
    ]))

    write('molar-mass', build('molar-mass', [
        "⚖️ Molar Mass Calculation",
        "Compute the molar mass (g/mol) from the molecular formula",
        "/ Molar Mass",
        "📖 View the usage guide for 'Molar Mass Calculation'",
        "Based on IUPAC relative atomic masses, the molar mass (g/mol) is obtained by summing the atomic weights of the elements in the chemical formula, with support for parenthesised hydrates and common ions; atomic weights use standard values, and the result can serve as a reference for solution preparation and reaction stoichiometry. Computed locally in the front end, data never leaves the browser.",
        "Common substances",
        "Molecular formula (e.g. H2SO4)",
        "Substance mass (g)",
        "👆 Enter a molecular formula",
        "📚 Deep Dive: Molar Mass Calculation",
        "Chemical formula molar mass: parse formulas such as H₂SO₄ and Ca(OH)₂ and sum the IUPAC atomic weights to obtain g/mol.",
        "Solution preparation mole conversion: back-calculate the required solute moles and the volumetric flask volume from the mass and target concentration.",
        "Reaction stoichiometry accounting: convert the molar relationships of each substance from the coefficients of the balanced equation.",
        "H₂SO₄ molar mass walkthrough",
        "Entering H2SO4, the tool parses H×2, S×1, O×4 and outputs about 98.08 g/mol by atomic weight, giving a weighing reference of 98.08g per 1mol.",
        "Which standard is used for atomic weights?",
        "The relative atomic masses published by IUPAC are used (for interval values the common standard atomic weight is taken); for radioactive/unstable elements the most stable isotope governs.",
        "How are hydrates calculated?",
        "Include the water of crystallisation in the formula (e.g. CuSO₄·5H₂O), sum each part separately and then add them; watch the expansion of parentheses and coefficients.",
        "Are molar mass and",
        "molecular weight",
        "the same?",
        "For molecular substances they are approximately synonymous; for ionic compounds 'formula weight' is more accurate. This tool uniformly outputs molar mass in g/mol.",
        "About 'Molar Mass Calculation'",
        "A molar mass calculation tool: parses atomic weights by chemical formula and sums them to obtain the molar mass, supporting hydrates and common ions, assisting solution preparation and reaction stoichiometry. Processed in the front end, with data computed locally to protect privacy.",
        "One-click specification/parameter conversion: results in real time by formula",
        "Local computation: data never leaves the browser, protecting business data",
        "Results can be copied and exported: convenient for records and re-checking",
        "Supports switching common units: reduces manual conversion errors",
        "Chemical formula molar mass parsing",
        "Solution preparation mole conversion",
        "Reaction stoichiometry accounting",
        "Hydrate and parenthesis handling",
        "e.g. Ca(OH)2, Al2(SO4)3",
    ]))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'metallurgy')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'metallurgy')
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
    out = {'slug': slug, 'industry': 'metallurgy', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('steel-profile-weight', build('steel-profile-weight', [
        "\"Steel Profile Weight\" is computed from the input parameters with professional calculations and outputs a result.",
        "Steel Section Weight Calculator",
        "/ Steel Section Weight Calculator",
        "\u2696\ufe0f Steel Section Weight Calculator",
        "Steel purchasing and transport are charged by weight. Choose a section type, enter dimensions and length, and the theoretical weight formula (density 7.85 g/cm\u00b3) converts the weight automatically.",
        "Section Type",
        "Round bar / round tube",
        "Square bar",
        "Flat bar",
        "Equal angle",
        "Channel",
        "Main Dimension a (mm)",
        "Secondary Dimension b (mm, for flat bar / channel)",
        "Wall or Leg Thickness t (mm, for tube / angle)",
        "Length (m)",
        "\U0001F4DA In-Depth Analysis: Steel Profile Weight",
        "Purchasing and material preparation: estimate the weight of a single piece or a whole batch from the theoretical metre weight \u00d7 length, to check purchased tonnage and freight quickly and avoid blind quoting by piece count.",
        "Transport and lifting: theoretical weight is used for truck payload, lifting gear rating and yard bearing checks, especially when aggregating by weight with mixed sections.",
        "Cutting optimisation: once the weight per metre is known, a nesting plan can be converted into offcut weight to compare which layout saves material and yields less scrap.",
        "Default parameters for the five section types (a=20mm / b=10mm / t=3mm / L=6m)",
        "Empirical coefficients derived from the carbon steel density 7.85 g/cm\u00b3 (round bar 0.00617, square bar / flat bar / angle 0.00785): round bar a\u00b2\u00d70.00617 = 20\u00b2\u00d70.00617 = 2.468 kg/m, total 2.468\u00d76 \u2248 14.81 kg; square bar a\u00b2\u00d70.00785 = 3.14 kg/m, total 18.84 kg; flat bar a\u00d7b\u00d70.00785 = 20\u00d710\u00d70.00785 = 1.57 kg/m, total 9.42 kg; equal angle (2a\u2212t)\u00d7t\u00d70.00785 = (40\u22123)\u00d73\u00d70.00785 = 0.871 kg/m, total 5.23 kg; channel (a+b\u22122t)\u00d7t\u00d70.00785\u00d71.05 = (20+10\u22126)\u00d73\u00d70.00785\u00d71.05 = 0.593 kg/m, total 3.56 kg (the \u00d71.05 includes a correction for thicker leg ends).",
        "Where do the coefficients 0.00617 and 0.00785 come from?",
        "Derived from the density 7.85 g/cm\u00b3: converting dimensions from mm to cm and length from m to cm, the unit volume mass 7.85 g/cm\u00b3 becomes about 0.00785 in kg/m\u00b7mm\u00b2; for round bar, multiplying 0.00785 by the area ratio \u03c0/4 \u2248 0.785 between \u03c0(d/2)\u00b2 and (d/2)\u00b2 gives 0.00617. The coefficients are approximations including rolling fillets and negative tolerance; settlement follows the weighbridge.",
        "Is a large difference between theoretical and weighed weight normal?",
        "Yes. Theoretical weight uses nominal dimensions, actual tolerance is around \u00b15%, and surface rust, coating and negative tolerance make actual weight lower than theoretical. For bulk purchasing, use the weighbridge or the theoretical weight plus tolerance for settlement and capacity checks; this tool's results are estimates.",
        "Theoretical weight is calculated at a density of 7.85 g/cm\u00b3 and is an approximation",
        "Round bar 0.00617, square bar 0.00785 and flat bar 0.00785 are common empirical coefficients",
        "Actual section weight allows around \u00b15% tolerance",
        "Results are for reference only; settlement follows the weighed weight",
        "Price (Quote / Volatility / Hedging) Analysis",
    ]))
    write('analysis-heatmap', build('analysis-heatmap', [
        "\U0001F4CA Metallurgical (Thermodynamics / Equilibrium / Phase Diagram) Analysis",
        "Thermodynamics / Equilibrium / Phase Diagram",
        "When a binary alloy equilibrates in a two-phase region, use the lever rule for the mass fractions of the two phases: f\u03b1=(C\u03b2\u2212C0)/(C\u03b2\u2212C\u03b1), f\u03b2=(C0\u2212C\u03b1)/(C\u03b2\u2212C\u03b1), where C0 is the overall alloy composition and C\u03b1/C\u03b2 are the equilibrium compositions of the two phases (same units, such as wt% B). It must satisfy C\u03b1 \u2264 C0 \u2264 C\u03b2, otherwise it indicates the composition is outside the two-phase region.",
        "Enter Alloy Composition (one line: C0,C\u03b1,C\u03b2, unit wt% B)",
        "Phase Fraction Calculation",
        "\U0001F4DA In-Depth Analysis: Metallurgical (Thermodynamics / Equilibrium / Phase Diagram) Analysis",
        "Use the Gibbs free energy criterion to analyse phase transformations and reaction direction, and judge whether a reaction can proceed spontaneously at a given temperature.",
        "Judge the effect of temperature on reaction equilibrium from how the equilibrium constant varies with temperature.",
        "Use the lever rule in the two-phase region to find the",
        "mass fractions",
        "of the two phases, combined with heatmap statistics of the composition distribution.",
        "Thermodynamics and Phase Diagrams",
        "Gibbs free energy change \u0394G = \u0394H \u2212 T\u0394S; the spontaneous condition is \u0394G<0. Equilibrium constant ln K_eq = \u2212\u0394G/(R\u00b7T). Lever rule in the two-phase (\u03b1+\u03b2) region: mass fraction of \u03b1 = (C\u03b2 \u2212 C)/(C\u03b2 \u2212 C\u03b1), of \u03b2 = (C \u2212 C\u03b1)/(C\u03b2 \u2212 C\u03b1) (C is the average alloy composition).",
        "For a binary system in the two-phase region with C\u03b1=10%, C\u03b2=80% and average alloy C=38%: \u03b1 phase = (80\u221238)/(80\u221210)=42/70=60%, \u03b2 phase=40%. That is, at equilibrium this composition is 60% \u03b1 phase and 40% \u03b2 phase; changing temperature moves the equilibrium composition around the eutectic point.",
        "Where does the lever rule apply?",
        "Only to the two-phase region under equilibrium cooling, with the composition between the two phase compositions. Non-equilibrium conditions (such as rapid cooling) produce dendritic segregation and the actual proportions deviate from the lever rule.",
        "What is the relationship between \u0394G and temperature?",
        "\u0394G=\u0394H\u2212T\u0394S. For an endothermic reaction (\u0394S>0), raising temperature makes \u0394G more likely to be negative and the reaction more favourable; for an exothermic reaction, lower temperature is favourable. This is the basis for temperature-controlled phase equilibrium.",
        "About \"Metallurgical (Thermodynamics / Equilibrium / Phase Diagram) Analysis\"",
        "Metallurgical (Thermodynamics / Equilibrium / Phase Diagram) Analysis. A free online tool processed entirely in the browser with no data upload, protecting your privacy.",
    ]))
    write('calc-temp-1', build('calc-temp-1', [
        "\U0001F321\ufe0f Forging (Temperature / Deformation / Force) Calculation",
        "Compute the pressure per unit projected area from forging force and forging projected area, and convert it into the required press tonnage (including a safety factor).",
        "Unit pressure = forging force (kN) \u00f7 projected area (cm\u00b2) \u00d7 10 (MPa, 1 kN/cm\u00b2 = 10 MPa); equipment tonnage = forging force \u00f7 9.807 (t); including the 1.25 factor = tonnage \u00d7 1.25",
        "The unit projected area pressure is used to check die pressure: 1 kN/cm\u00b2 equals 10 MPa. Equipment tonnage converts at 1 t \u2248 9.807 kN, and the selection tonnage is given with a 1.25 times safety factor, avoiding overloading and stalling.",
        "Forging Force (kN)",
        "Forging Projected Area (cm\u00b2)",
        "\U0001F4A1 Unit pressure (MPa) = forging force (kN) \u00d7 1000 \u00f7 projected area (cm\u00b2); tonnage = forging force \u00f7 9.807 kN/t, and multiply the selection by 1.25.",
        "\U0001F4DA In-Depth Analysis: Forging (Temperature / Deformation / Force) Calculation",
        "Press selection: convert the forging force into unit projected area pressure and equipment tonnage from the forging projected area, then select the press model with a 1.25 times safety factor to avoid overload stalling.",
        "Die pressure check: convert the actual forging force into unit projected area pressure (MPa) and compare it with the allowable die pressure for the die material, to judge whether a larger bolster or stepped forming is needed.",
        "Process card drafting: write the forging force, projected area and tonnage requirement into the process card for cutting and equipment scheduling.",
        "Example: 3000 kN forging force, 250 cm\u00b2 projected area",
        "Unit projected area pressure = 3000 \u00f7 250 \u00d7 10 = 120.00 MPa (1 kN/cm\u00b2 = 10 MPa); equipment tonnage = 3000 \u00f7 9.807 = 305.90 t; selection tonnage with the 1.25 safety factor = 382.38 t; force per cm\u00b2 = 12.000 kN/cm\u00b2.",
        "Why must MPa be multiplied by 10?",
        "1 kN/cm\u00b2 = 1000 N \u00f7 0.0001 m\u00b2 = 10 MPa. Doing only the kN/cm\u00b2 division without multiplying by 10 gives a result ten times smaller than the true pressure, leading to far undersized selection.",
        "Why multiply equipment tonnage by 1.25?",
        "Actual forging involves friction, variation in deformation resistance and impact loads, so leaving 25% margin avoids stalling and die damage. For cold forging or high-strength materials a factor of 1.3 to 1.5 is advised.",
        "About \"Forging (Temperature / Deformation / Force) Calculation\"",
        "Forging (Temperature / Deformation / Force) Calculation. A free online tool processed entirely in the browser with no data upload, protecting your privacy.",
        "Deformation",
    ]))


if __name__ == '__main__':
    main()
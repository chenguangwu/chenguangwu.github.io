#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'rubber')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'rubber')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    return mp


def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'rubber', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

#!/usr/bin/env python3


def main():
    write('abrasion-test', build('abrasion-test', [
        '⚖️ Rubber Abrasion Test Standard Comparison',
        'Compare common abrasion test methods, test conditions and result conversion',
        'Abrasion Test Standard Comparison',
        '/ Abrasion Test',
        '📖 View the Rubber Abrasion Test Standard Comparison user guide',
        'Abrasion conversion reference: taking the Akron abrasion loss as the baseline, DIN abrasion ≈ Akron value × 130 and Grasselli ≈ Akron value × 1.2; the specimen shape and drum conditions differ between standards, so the conversion is only for qualitative comparison, and formal judgement must be based on actual testing to the relevant standard.',
        'Test standards',
        'Result conversion',
        'Akron abrasion (cm³/1.61km)',
        'DIN abrasion (mm³)',
        'Grasselli abrasion (cm³/h)',
        'Abrasion value',
        'Abrasion notes:',
        'A smaller abrasion value means better wear resistance. Values from different test methods cannot be compared directly; the test conditions must be understood. Akron abrasion is the standard commonly used in China.',
        'Common rubber abrasion performance reference',
        '📚 In-depth analysis: Rubber Abrasion Test Standard Comparison',
        'Interworking results across standards: the same compound often has to satisfy reports under different abrasion standards such as Akron (GB/T 1689), DIN 53516 (German standard) and Grasselli; the tool converts between them by coefficient, making comparison and export order handling easier.',
        'Compound ',
        'abrasion resistance assessment',
        ': grade by the Akron abrasion value, ≤0.1 excellent, ≤0.2 good, ≤0.4 fair, guiding tread and conveyor belt formulation adjustments.',
        'Third-party report review: when a DIN or Grasselli report arrives, back-calculate the Akron value to judge quickly whether internal control thresholds are met, avoiding misjudgement from confused units and standards.',
        'Worked example: Akron abrasion 0.15 cm³/1.61km',
        'Akron = 0.15 cm³/1.61km;\nDIN = 0.15 × 130 = 19.50 mm³;\nGrasselli = 0.15 × 1.2 = 0.1800 cm³/h;\nAkron 0.15 ≤ 0.2 → abrasion resistance is good.\nIf the original value is DIN 20 mm³: Akron = 20 ÷ 130 = 0.1538 cm³/1.61km, and DIN to Grasselli 20 ÷ 100 = 0.20 cm³/h.',
        'Why do the three abrasion standards differ so much in dimension?',
        'Akron measures volume loss per 1.61 km of travel (cm³/1.61km), DIN measures volume loss (mm³), and Grasselli measures volume loss per unit time (cm³/h); the three use different machines, abrasives and loads, so only approximate conversion factors are given, and precise comparison requires retesting to the same standard.',
        'Is a smaller abrasion value always more wear resistant?',
        'Yes. The abrasion value is the volume loss per unit distance or time, so a smaller value means a more wear-resistant compound; but too small a value may sacrifice grip, elasticity and other properties, so judge together with tensile, tear and hardness results.',
        'About Abrasion Test',
        'A rubber abrasion test standard comparison table: it compares the Akron, Grasselli and DIN abrasion test methods and converts results between them. A business and office tool that improves work efficiency; data is processed locally to protect privacy.',
    ]))

    write('cure-time', build('cure-time', [
        '🧮 Rubber Cure Time Calculation',
        'Calculate the equivalent cure time from a temperature change, converted with the Arrhenius equation',
        'Cure Time Calculation',
        '/ Cure Time',
        '📖 View the Rubber Cure Time Calculation user guide',
        'Reference temperature (°C)',
        'Reference cure time (min)',
        'Activation energy Ea (kJ/mol)',
        'Calculate cure time',
        'Calculation principle:',
        'Cure time roughly halves for every 10 °C rise in temperature, which is van’t Hoff’s rule. For an exact calculation the Arrhenius equation is used: t2 = t1 × exp[Ea/R × (1/T2 - 1/T1)].',
        'Equivalent cure time at different temperatures',
        '📚 In-depth analysis: Rubber Cure Time Calculation',
        'Cure temperature adjustment: when the on-site autoclave temperature differs from the laboratory standard temperature, for example 150 °C, use the Arrhenius equation to back-calculate the new cure time needed for the same degree of crosslinking, avoiding under-cure or over-cure.',
        'Energy and takt optimisation: raising the cure temperature shortens the time, and van’t Hoff’s 10 °C rule roughly halves the time for every 10 °C rise; the tool gives the rate multiplier to help weigh energy use against capacity.',
        'Process transfer verification: when equipment temperature fluctuates at a new plant, estimate the time window from the reference activation energy, commonly 80–110 kJ/mol for rubber, to keep physical properties consistent.',
        'Worked example: reference 150 °C / 10 min, activation energy 90 kJ/mol, target 160 °C',
        'T1 = 150 + 273.15 = 423.15 K, T2 = 160 + 273.15 = 433.15 K, Ea = 90000 J/mol, R = 8.314;\nArrhenius time = 10 × exp((90000/8.314) × (1/433.15 − 1/423.15)) ≈ 10 × 0.5509 = 5.5 min;\nvan’t Hoff approximation = 10 ÷ 2^(10/10) = 5.0 min;\ncure rate multiplier = 10 ÷ 5.5 ≈ 1.81×.\nIf the temperature drops to 140 °C: Arrhenius ≈ 18.6 min, rate 0.54×, markedly slower.',
        'Which is more accurate, Arrhenius or van’t Hoff?',
        'Arrhenius is based on activation energy and is more accurate for a chemical reaction such as curing, especially across a wide temperature span; van’t Hoff’s rule of halving the time per 10 °C is an empirical approximation valid only within a narrow temperature band, so a large gap between the two means the range has gone beyond the empirical limits.',
        'What value should I enter for the activation energy?',
        'It varies greatly with the compound and cure system: natural rubber and sulphur systems are mostly 80–110 kJ/mol, while peroxide curing is higher. With no measured value, use the value stated on the process card or calibrate with stepped laboratory trials; the tool result is only a process estimate.',
        'About Cure Time',
        'A rubber cure time calculator: it works out the equivalent cure time from the cure temperature and activation energy, converted with the Arrhenius equation. A business and office tool that improves work efficiency; data is processed locally to protect privacy.',
    ]))

    write('hardness-calc', build('hardness-calc', [
        '🔄 Rubber Shore Hardness Conversion',
        'Shore A/D and IRHD hardness comparison, plus elastic modulus estimation',
        '"Shore A/D and IRHD hardness comparison, plus elastic modulus estimation" — the tool runs a professional calculation from the input parameters and outputs the result.',
        'Rubber Hardness Conversion',
        '/ Hardness Calc',
        '📖 View the Rubber Shore Hardness Conversion user guide',
        'Hardness conversion',
        'Elastic modulus',
        'Hardness type',
        'Shore A',
        'Shore D',
        'Hardness value',
        'Shore A hardness',
        'Hardness notes:',
        'Shore A is used for soft rubber (0-100 HA) and Shore D for hard rubber and plastics. IRHD, the international rubber hardness, is approximately equal to Shore A in the middle hardness range.',
        'Rubber hardness grade reference',
        '📚 In-depth analysis: Rubber Shore Hardness Conversion',
        'Standard mutual recognition: when the customer drawing specifies Shore D and the in-house instrument measures Shore A, or when IRHD (international rubber hardness) is needed to match European standards, the tool converts between them with approximate formulas to ease acceptance discussions.',
        'Hardness-modulus link: estimate Young’s modulus from Shore A with the Gent empirical formula to judge quickly whether the compound stiffness meets a sealing or vibration-damping design, without waiting for dynamic mechanical testing.',
        'Soft and hard range judgement: Shore A ≤ 20 very soft (sponge, gaskets), 20–40 soft (O-rings), 40–70 medium hard (tyres, shoe soles), 70–90 hard (industrial rollers), above 90 very hard (hard rubber); the tool gives the grade and material selection hints by hardness.',
        'Worked example: Shore A 70',
        'Shore A = 70 → Shore D ≈ (70−50)×0.5 + (70−50)×0.01×(70−50) = 10+4 = 14 HD, where the conversion applies only at 50 or above and is not meaningful in the soft range;\nIRHD ≈ 70+1 = 71;\nGent Young’s modulus E = 0.0981 × (0.1375×70²/(100−70) + 2.963) = 0.0981 × (22.458+2.963) ≈ 2.494 MPa; ',
        'shear modulus',
        'G ≈ E/3 ≈ 0.831 MPa.\nFor Shore D 60 → Shore A ≈ 60×2+50 = 170, capped at 100 HA, IRHD 101.',
        'Can Shore A, Shore D and IRHD be converted precisely?',
        'No. The three differ in indenter shape, ',
        ' and measuring principle; this tool gives an engineering approximation, converting to Shore D only at Shore A of 50 or above since D is meaningless in the soft range, and taking IRHD ≈ Shore A + 1 in the middle band, so precise acceptance must use actual measurement on the corresponding standard instrument.',
        'What range does the Gent modulus formula cover?',
        'The Gent empirical formula E = 0.0981 × (0.1375·HA²/(100−HA) + 2.963) applies to rubber-like elastomers in the Shore A 20–90 range and is used for an initial stiffness estimate; the actual modulus is affected by filler and crosslink density, so important structural parts should be measured by DMA.',
        'About Hardness Calc',
        'A rubber Shore hardness conversion tool: it supports Shore A/D/IRHD hardness comparison and conversion between hardness and elastic modulus. A business and office tool that improves work efficiency; data is processed locally to protect privacy.',
    ]))

    write('mixing-ratio', build('mixing-ratio', [
        '🧮 Rubber Mixing Ratio Calculation',
        'Calculate the actual amount of each component from the total formulation weight and the component ratios',
        'Mixing Ratio Calculation',
        '/ Mixing Ratio',
        '📖 View the Rubber Mixing Ratio Calculation user guide',
        'Rubber formulations use',
        'phr (parts per hundred rubber)',
        'as the basis. The actual mass of a component = total mixing mass × (that component’s phr ÷ total phr). The raw rubber is fixed at 100 phr, and vulcanising agents, fillers and additives are summed in phr to give the total phr, from which the mass of each ingredient is back-calculated against the target total weight.',
        'Mass fraction (%) = component phr ÷ total phr × 100%.',
        'Where densities differ greatly, note that volume fraction and mass fraction are not the same; in practice materials are charged by mass.',
        'The results are a reference for weighing out; the actual values are determined by trial mixing and physical property testing.',
        'Total formulation weight (kg)',
        'Formulation components',
        'Ratio notes:',
        'Rubber formulations usually take the raw rubber as 100 parts (phr), with other compounding ingredients measured in relative parts. Total parts = the sum of the parts of all components. Actual amount = total weight × (that component’s parts / total parts).',
        'Typical rubber formulation reference',
        '📚 In-depth analysis: Rubber Mixing Ratio Calculation',
        'Charging by the phr formulation: rubber formulations are expressed in parts per hundred rubber, phr, with raw rubber as 100, and the tool back-calculates the actual weight to be weighed for each material from the total charge, avoiding manual ratio errors.',
        'Scaling up from laboratory to production: a 1 kg laboratory formulation scaled to 10 kg per batch has every component scaled proportionally in phr, and the tool gives every weight at once to keep batches consistent.',
        'Formulation fine-tuning accounting: after adjusting a component’s phr, for example reinforcing carbon black from 40 to 50, the tool recalculates the weight distribution of the whole formulation to confirm the change in total and cost.',
        'Worked example: 10 kg total, the default 8-component formulation (NR100 / ZnO5 / SA2 / S2.5 / DM1.2 / 4010NA1.5 / N33040 / oil 5)',
        'Total parts = 100+5+2+2.5+1.2+1.5+40+5 = 157.2 phr;\nweight per part = 10 ÷ 157.2 = 0.06361 kg/phr;\nNR = 10 × 100/157.2 = 6.361 kg, ZnO 0.318 kg, stearic acid 0.127 kg, sulphur 0.159 kg, accelerator DM 0.076 kg, antioxidant 0.095 kg, carbon black N330 2.545 kg, aromatic oil 0.318 kg, totalling 10.000 kg.',
        'What unit is phr, and why is raw rubber taken as 100?',
        'phr means parts per hundred rubber, the relative ratio convention of the rubber industry; it is independent of absolute weight, which makes scaling across batch sizes and sharing formulations easy. Raw rubber is normally taken as 100 parts as the baseline, and other additives are stacked proportionally.',
        'What happens if both the total and the total phr change?',
        'The tool divides the total by the total phr to get the weight per part, then multiplies by each component’s phr; changing only the total scales every weight proportionally, while changing a component’s phr changes the weight distribution, but the total still equals the set total provided the sum of phr is greater than 0.',
        'About Mixing Ratio',
        'A rubber mixing formulation ratio calculator: it works out the actual amount of each component from the total weight and the percentage of each component, and supports formulation adjustment. A business and office tool that improves work efficiency; data is processed locally to protect privacy.',
    ]))

    write('tensile-strength', build('tensile-strength', [
        '🧴 Rubber Tensile Strength Calculation',
        'Calculate rubber tensile strength, elongation at break and the stress-strain curve',
        '/ Tensile Strength',
        '📖 View the Rubber Tensile Strength Calculation user guide',
        'Tensile strength = maximum force / (width × thickness)',
        'Maximum tensile force (N)',
        'Specimen width (mm)',
        'Specimen thickness (mm)',
        'Elongation at break',
        'Original gauge length (mm)',
        'Gauge length at break (mm)',
        'Tensile strength = maximum force / (width × thickness); elongation at break = (gauge length at break - original gauge length) / original gauge length × 100%. Unit: MPa = N/mm².',
        'Common rubber tensile strength reference',
        '📚 In-depth analysis: Rubber Tensile Strength Calculation',
        'Physical property compliance judgement: measure the maximum force on a GB/T 528 dumbbell specimen; the tool uses width × thickness for the cross-sectional area and computes the tensile strength in MPa and the elongation at break as a percentage, for acceptance against the product standard.',
        'Formulation improvement verification: compare tensile strength and elongation before and after reinforcement to judge whether the carbon black or silica loading is reasonable, guiding formulation iteration.',
        'Grade assessment: tensile ≥ 20 MPa and elongation ≥ 300% is rated high strength and high elongation, suitable for dynamically loaded parts such as tyre treads and drive belts; lower values mean the cure or reinforcement needs adjusting.',
        'Worked example: maximum force 500 N, width 6 mm, thickness 2 mm, gauge length 25 mm, break at 125 mm',
        'Cross-sectional area = 6 × 2 = 12 mm²;\ntensile strength = 500 ÷ 12 = 41.67 MPa;\nelongation at break = (125 − 25) ÷ 25 × 100 = 400%;\nelongation ratio at break = 125/25 = 5.00;\ntensile ≥ 20 and elongation ≥ 300 → high strength and high elongation.',
        'Why use the cross-sectional area rather than the cross-section perimeter?',
        'Tensile strength is defined as the maximum tensile force divided by the minimum cross-sectional area of the specimen, width × thickness, in MPa (N/mm²); using the perimeter underestimates the true stress, and GB/T 528 explicitly specifies the product of width and thickness in the central parallel section of the dumbbell as the effective cross-sectional area.',
        'Is elongation affected by the gauge length?',
        'Elongation at break = (length at break − initial gauge length) / initial gauge length × 100%, so it depends on the gauge length used; standard specimens have a fixed gauge length, for example 25 mm for type I, and results from different gauge lengths cannot be compared directly, as they must be tested under the same standard.',
        'About Tensile Strength',
        'A rubber tensile strength calculator: it works out the tensile strength from the tensile force and cross-sectional area, and supports elongation at break. A business and office tool that improves work efficiency; data is processed locally to protect privacy.',
    ]))


if __name__ == '__main__':
    main()

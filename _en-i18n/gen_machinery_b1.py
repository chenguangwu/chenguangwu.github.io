#!/usr/bin/env python3
# machinery batch1 (5 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'machinery')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'machinery')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'analysis-casting': [
"⚖️ Casting Pouring Weight and Solidification Time Calculator",
"Casting Process Calculation",
"Casting Pouring Weight and Solidification Time",
"/ Casting Pouring Weight and Solidification Time",
'📖 View the "Casting Pouring Weight and Solidification Time Guide"',
"Weight G = V·ρ; casting modulus M = V / A; solidification time t = C·Mⁿ (commonly n=2, i.e. Chvorinov's rule t = C·M²).",
"The casting modulus M reflects the heat-dissipation conditions: the larger the modulus, the slower the heat dissipation and the longer the solidification time; thin walls and small features have a small modulus and are prone to misruns or cold shuts. Given the volume V, surface area A, metal density ρ and coefficient C, the poured-metal weight and solidification time can be estimated quickly, aiding gating-system design and process-window evaluation. Results are for reference only.",
"Casting volume V (cm³)",
"Casting surface area A (cm²)",
"Metal density ρ (g/cm³)",
"Chvorinov coefficient C (s/cm²)",
"📚 In-Depth Analysis: Casting Pouring Weight and Solidification Time",
"Process design: estimate the poured-metal weight from the casting volume, surface area and metal density, and check the ladle capacity and pouring system.",
"Solidification analysis: estimate with the casting modulus and Chvorinov's rule",
"solidification time",
", and judge the solidification sequence and shrinkage-porosity risk of thin-wall and thick sections.",
"Gating evaluation: compare the effect of different process schemes (such as changing the riser or chill to alter the modulus) on solidification time, and optimise the process window.",
"Example (V=1000 cm³, A=400 cm², ρ=7.2, C=2.0)",
"Weight G = 1000 × 7.2 = 7200.00 g; modulus M = 1000 / 400 = 2.500 cm; solidification time t = 2.0 × 2.500² = 12.5 s (0.21 min). The modulus is relatively large, so solidification is slow; thick sections need feeding attention.",
"Why is the modulus important in Chvorinov's rule?",
"The modulus M=V/A combines the volume and the heat-dissipating surface area and determines how fast the casting cools. The larger the modulus, the slower the solidification; it is a key parameter for judging shrinkage cavities and porosity and for sizing risers.",
"How is the coefficient C chosen?",
"C depends on the alloy, the mould material and the cooling conditions (for example about 1.0-2.0 s/cm² for cast iron in green sand). This tool computes with the C you enter; for actual values refer to process handbooks and comparable experience.",
'About "Casting Pouring Weight and Solidification Time"',
"A casting pouring weight and solidification time calculator. Free online tool, processed entirely on the client side; data is not uploaded, protecting your privacy.",
],
'analysis-lifespan': [
"📊 Reliability (Life / Failure / Repair) Analysis",
"Life / Failure / Repair",
"From the total operating time, number of failures and cumulative repair time, compute the mean time between failures (MTBF), mean time to repair (MTTR) and inherent availability, and give the reliability for a specified mission duration assuming an exponential distribution. Data is processed only locally in the browser and is not uploaded.",
'📖 View the "Reliability (Life / Failure / Repair) Analysis Guide"',
"MTBF = total operating time ÷ number of failures",
"Reliability R(t) = e^(−t ÷ MTBF)",
"From the total operating time, number of failures and cumulative repair time, compute MTBF, MTTR and inherent availability, and give the reliability for a specified mission duration assuming an exponential distribution. All data is processed only locally in the browser and is not uploaded.",
"Total operating time (h)",
"Number of failures",
"Cumulative repair time (h)",
"Mission duration t (h)",
"📚 In-Depth Analysis: Equipment Life Analysis",
"Estimate the achievable cycle life of critical components from the fatigue S-N curve.",
"Assess the rated life of rotating parts using the L10 approach.",
"Compare the life reduction under different loads.",
"Stress amplitude σa, fatigue strength coefficient σ', exponent b: N=(σa/σ')^(−1/b). If σa=200 MPa, σ'=600 MPa, b=0.1: N=(200/600)^(−10)=(1/3)^(−10)=3^10≈59049 cycles.",
"Load de-rating",
"Raise the load by 20% (stress amplitude 200→240): N∝σa^(−10); the de-rated life N=(200/240)^10·59049≈0.148×59049≈8743 cycles, i.e. the life drops to about 1/7.",
"How does L10 relate to fatigue life?",
"L10 is the rated life at 90% reliability (in millions of revolutions); together with S-N fatigue life it belongs to reliability life, the former being commonly used for bearings and the latter for structural fatigue.",
"Can analysis replace testing?",
"No. The calculation only gives an initial order of magnitude; critical parts still need bench/field life-test verification, especially when there is",
"stress concentration",
", corrosion or variable-amplitude loading.",
'About "Reliability (Life / Failure / Repair) Analysis"',
"A reliability (life / failure / repair) analysis calculator. Free online tool, processed entirely on the client side; data is not uploaded, protecting your privacy.",
],
'area-dosage-1': [
"📐 Coating Film Thickness, Area and Usage",
"Enter the coating area, dry film thickness, volume solids and transfer efficiency to compute the theoretical and actual paint usage",
'📖 View the "Coating Film Thickness, Area and Usage Guide"',
"Coating usage = area × film thickness × density",
"Coating area A (m²)",
"Volume solids VS (%)",
"Transfer efficiency TE (%)",
"💡 Formula: theoretical usage (L) = A×DFT÷(10×VS); actual usage (L) = theoretical usage÷(TE÷100); theoretical coverage (m²/L) = 10×VS÷DFT",
"Take the volume solids VS from the volume-solids fraction in the paint technical data sheet (TDS)",
"Transfer efficiency (application efficiency) depends on the application method: brush 85%-95%, roller 80%-90%, air spray 50%-70%, airless spray 60%-80%",
"Add a 5%-10% loss allowance in actual procurement",
"Dry film thickness is usually measured in μm, commonly 40-250 μm",
"📚 In-Depth Analysis: Surface-Treatment Area Dosage",
"Estimate the material usage of coating/plating/spraying by area × film thickness.",
"Compare the paint or coating weight under different film thicknesses.",
"Total surface area and dosage statistics for batches of parts.",
"Spray usage",
"Area A=1 m², film thickness h=50 μm, paint density ρ=1.2 g/cm³: usage m=A·h·ρ=1×0.005×1.2=0.006 kg=6 g (one side). Both sides with 10% loss → ≈13.2 g.",
"Electroplated zinc layer",
"Area 0.5 m², coating 10 μm, zinc density 7.14: m=0.5×0.001×7.14=0.00357 kg≈3.57 g.",
"Why is film thickness measured in microns?",
"Surface-treatment film thickness is usually a few to a few tens of microns (μm); converting to m gives a very small number, so μm is more intuitive and avoids decimal errors.",
"Why is the actual usage greater than the theoretical?",
"Spraying has overspray loss, and electroplating has current-efficiency loss and edge thickening; the actual usage is usually multiplied by a 1.1-1.3 loss factor.",
'About "Coating Film Thickness, Area and Usage"',
"A coating film thickness, area and usage calculator: based on the paint volume solids and application transfer efficiency, it quickly computes the theoretical and actual paint usage for a given area and dry film thickness, aiding coating-engineering material budgeting.",
"Computes both theoretical and actual usage",
"Supports custom volume solids and transfer efficiency",
"Outputs coverage, mass and gallon conversion",
"Coating engineering material budgeting",
"Anti-corrosion paint usage estimation",
"Spray-process parameter verification",
"Procurement planning",
"Coating area",
"Volume solids",
"Transfer efficiency",
],
'banjinzhewanzhankai': [
"⚙️ Sheet-Metal Bend Unfolding Calculator",
"Enter the sheet thickness, bend angle, inside bend radius and K-factor to compute the bend allowance, bend deduction and unfolded length",
"Sheet-Metal Bend Unfolding",
"/ Sheet-Metal Bend Unfolding",
'📖 View the "Sheet-Metal Bend Unfolding Calculator Guide"',
"Unfolded length = neutral axis + bend compensation",
"Bend angle θ (°)",
"Inside bend radius R (mm)",
"Material (K-factor preset)",
"Steel (K≈0.45)",
"Stainless steel (K≈0.42)",
"Hard aluminium (K≈0.38)",
"Soft aluminium (K≈0.35)",
"Copper (K≈0.33)",
"K-factor",
"Flange length A (mm)",
"Flange length B (mm)",
"💡 Formula: outside setback OSSB=(R+t)·tan(θ/2); bend allowance BA=(R+K·t)·π·θ/180; bend deduction BD=2·OSSB-BA; unfolded length L=A+B-BD",
"The K-factor is usually 0.3-0.5, depending on the material and the relative bend radius R/t",
"When R/t < 0.5, cracks may occur; the inside bend radius should be increased",
"The bend angle θ is the bend complementary angle (the actual bending angle of the material); 90° is the most common",
"Flange lengths A and B are the distances from the outer edge to the tangent point; leaving them 0 computes only the bend parameters",
"Actual unfolding should account for springback; the bend angle usually needs 1°-3° of overbending",
"📚 In-Depth Analysis: Sheet-Metal Bend Unfolded Length",
"Compute the total unfolded length of multi-bend parts from the neutral axis, for blanking.",
"The effect of different K-factors (material/process) on the bend deduction.",
"Verify whether the bend deduction BD equals 2·OSSB−BA.",
"Single 90° bend",
"Flanges a=50, b=50, inside radius R=2, sheet thickness t=2, K=0.33, θ=90°: OSSB=(R+t)·tan(θ/2)=(4)·tan45°=4; BA=(R+K·t)·(π·θ/180)=(2+0.66)·1.5708=4.178; BD=2×4−4.178=3.822; unfolded L=a+b−BD=100−3.822=96.178 mm.",
"K-factor effect",
"Same parameters with K=0.5: BA=(2+1.0)·1.5708=4.712, BD=8−4.712=3.288, L=100−3.288=96.712 mm. The larger the K, the further out the neutral axis and the longer the unfolded length.",
"What is the K-factor?",
"It is the neutral-axis position coefficient: K = distance from the neutral axis to the inner surface / sheet thickness. For mild steel it is about 0.33-0.5, depending on the material, thickness, tooling and radius.",
"Why use 2·OSSB−BA?",
"The bend deduction BD = outer-tension compensation − inner compression; the standard unfolded length L = sum of straight segments − ΣBD. OSSB is the outside setback, and geometrically BD=2·OSSB−BA.",
'About "Sheet-Metal Bend Unfolding"',
"A sheet-metal bend unfolding calculator: based on the sheet thickness, bend angle, inside bend radius and K-factor, it computes the bend allowance (BA), bend deduction (BD), outside setback (OSSB) and total unfolded length, and checks the relative bend radius, aiding sheet-metal blanking and process design.",
"Computes the three main bend parameters BA, BD and OSSB",
"Supports a custom K-factor or material presets",
"Checks the relative bend radius R/t and gives formability hints",
"Enter the flange dimensions to get the total unfolded length directly",
"Unfolded blank-size calculation for sheet-metal parts",
"Bend-process parameter determination and verification",
"K-factor and formability assessment",
"Bend-by-bend unfolding of multi-bend sheet-metal parts",
],
'calc-64': [
"🧮 Assembly Clearance / Interference Calculator",
"Enter the basic hole/shaft size and upper/lower deviations to automatically determine the fit type and compute the clearance/interference",
'📖 View the "Assembly Clearance / Interference Calculator Guide"',
"Assembly clearance / interference = tolerance fit",
"Hole (H)",
"Hole upper deviation ES (μm)",
"Hole lower deviation EI (μm)",
"Shaft (h)",
"Shaft upper deviation es (μm)",
"Shaft lower deviation ei (μm)",
"-- Common fit presets --",
"H7/h6 clearance (sliding fit)",
"H7/g6 clearance (precision sliding)",
"H7/js6 transition",
"H7/k6 transition",
"H7/p6 interference",
"H7/r6 interference (heavy press)",
"💡 Clearance = hole − shaft (positive = clearance, negative = interference). Maximum clearance = ES − ei; minimum clearance = EI − es.",
"Common fit type descriptions",
": the hole tolerance zone lies entirely above the shaft tolerance zone, giving clearance",
"Interference fit",
": the hole tolerance zone lies entirely below the shaft tolerance zone and needs press fitting",
"Transition fit",
": the hole and shaft tolerance zones overlap, so there may be clearance or interference",
"📚 In-Depth Analysis: Hole-Shaft Fit Clearance / Interference",
"Given the hole and shaft limit deviations, compute the maximum/minimum clearance (clearance fit) or interference (interference fit).",
"Fit tolerance",
"Is it within the design band?",
"Compare the assembly characteristics of H7/g6 and H7/k6.",
"Φ50 H7/g6 clearance fit",
"Hole H7: ES=+0.025, EI=0; shaft g6: es=−0.009, ei=−0.025 (in mm, deviation ×1). Xmax=(ES−ei)/1000=(0.025−(−0.025))/1000=0.050 mm; Xmin=(EI−es)/1000=(0−(−0.009))/1000=0.009 mm. Clearance 0.009-0.050 mm, sliding fit.",
"Maximum interference = (EI−es)/1000 (negative direction); assembly needs a press force or a shrink/expansion-fit process, and the greater the interference the larger the required press force.",
"Why divide the deviation by 1000?",
"ISO tolerance-table deviations are usually given in μm, and this tool converts them to mm internally (÷1000). Make sure ES/EI/es/ei are in the same unit before computing.",
"Can a clearance fit transmit torque?",
"A pure clearance fit cannot transmit torque by friction; it requires a key, pin or interference assist. The clearance only ensures relative motion and lubrication.",
"Hole upper deviation",
"Hole lower deviation",
"Shaft upper deviation",
"Shaft lower deviation",
"Common fit presets",
],
}

# term-link nodes missed by extract: zh -> en
EXTRA = {
'analysis-lifespan': {'疲劳寿命（Basquin）': 'Fatigue Life (Basquin)'},
}

def build(slug, en_list):
    path = os.path.join(WORK, slug + '.json')
    wj = json.load(open(path, encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('!! %s length mismatch %d vs %d' % (slug, len(en_list), len(items)))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if not en or not isinstance(en, str):
            print('!! %s empty translation' % slug)
            sys.exit(1)
        if CJK.search(en) or CNP.search(en):
            print('!! %s CJK/CNP violation: %s' % (slug, en[:60]))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('!! %s EXTRA CJK/CNP violation: %s' % (slug, en[:60]))
            sys.exit(1)
        mp[z] = en
    return mp

def write(slug, mp):
    os.makedirs(OUT, exist_ok=True)
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('name', slug)
    out = {'slug': slug, 'industry': 'machinery', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

for slug, en_list in EN.items():
    write(slug, build(slug, en_list))

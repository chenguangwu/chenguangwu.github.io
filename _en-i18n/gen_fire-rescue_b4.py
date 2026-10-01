#!/usr/bin/env python3
# fire-rescue batch4 (5 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'fire-rescue')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'fire-rescue')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'sprinkler-design': [
"📐 Sprinkler System Designer",
"Compute the sprinkler count, operating area, design flow and water-supply pressure of an automatic sprinkler system.",
"Sprinkler flow q = K·√P (K = flow coefficient, P = working pressure in MPa); open-head count N = operating area Aₒₚ ÷ head coverage area a; system design flow Q = N·q (L/min), then checked against the code-required spray density.",
"Ordinary hazard Class I",
"Ordinary hazard Class II",
"Extra hazard Class I",
"Extra hazard Class II",
"Storage hazard Class I",
"Total protected area (m²)",
"Coverage area per sprinkler (m²)",
"Sprinkler working pressure P (MPa)",
"Sprinkler flow coefficient K",
"System operating area (m², leave blank to use the standard value)",
"📖 Design Parameters",
"Sprinkler flow formula",
"Single-sprinkler flow q = K × √(10P), K is the flow coefficient, P is the working pressure (MPa), q in L/min",
"System design flow Qs = sum of the sprinkler flows within the operating area (considering simultaneous opening)",
"Standard parameters by hazard level (GB 50084)",
"Light hazard: operating area 160 m², spray density 4 L/(min·m²)",
"Ordinary hazard Class I: operating area 160 m², spray density 6 L/(min·m²)",
"Ordinary hazard Class II: operating area 160 m², spray density 8 L/(min·m²)",
"Extra hazard Class I: operating area 260 m², spray density 12 L/(min·m²)",
"Extra hazard Class II: operating area 260 m², spray density 16 L/(min·m²)",
"This tool provides estimates based on the Code for Design of Sprinkler Systems (GB 50084); the formal design must be determined together with hydraulic pipe calculations.",
"📚 In-Depth Analysis: Automatic Sprinkler System Design",
"In sprinkler system design, determine the operating area, spray density and sprinkler layout by hazard level.",
"Verify whether the flow within the most unfavorable operating area and the system flow meet the code minimum.",
"When renovating or expanding, back-calculate whether the fire water-storage volume meets 1-2 hours of firefighting water use.",
"Design for Ordinary hazard Class I, operating area 160 m²",
"With the default parameters (Ordinary hazard Class I, standard operating area 160 m², standard spray density 6 L/(min·m²)): about 13 sprinklers within the operating area (spacing about 3.6 m), single-sprinkler flow 80 L/min; system design flow = 1040 L/min = 17.3 L/s, actual spray density 6.5 L/(min·m²) ≥ standard 6, meeting the design requirement. Recommended fire water-storage volume 1040 L (1 hour) to 2080 L (2 hours).",
"Why is the spray density taken as 6 L/(min·m²)?",
"It comes from GB 50084's provisions by fire hazard class: Ordinary hazard Class I is 6, Class II is 8, and extra hazard is higher; the design spray density must not be below the lower limit of the corresponding class, otherwise the fire cannot be controlled effectively.",
"Why use 13×80 for the system flow instead of area × density?",
"The operating-area method controls the system flow by 'number of sprinklers simultaneously open within the most unfavorable operating area × single-sprinkler flow', which already implies the sprinkler spacing and pressure distribution and is closer to the actual spray distribution than simple area × density.",
'About "Sprinkler System Designer"',
"Based on the sprinkler system design code, compute the sprinkler count, system design flow and spray density, and verify compliance with the hazard-level requirements.",
"Parameters for multiple hazard levels",
"Sprinkler flow calculation",
"Spray-density verification",
"Water-storage volume estimation",
"Preliminary sprinkler system design",
"Fire-flow estimation",
"Water-tank capacity planning",
],
'hydrant-flow': [
"💧 Hydrant Flow Calculator",
"Compute hydrant discharge flow, pressure loss and fire-stream reach.",
"Nozzle flow q = 0.0348·dn²·√Pq (dn = nozzle diameter in mm, Pq = nozzle pressure in MPa, L/s); invert q = K√Pq to get Pq=(q/K)²; the fire-stream reach Sk follows nozzle pressure via the φ coefficient.",
"Hydrant outlet pressure P (MPa)",
"Hose diameter d (mm)",
"Nozzle diameter dn (mm)",
"Hose length L (m)",
"Hose resistance coefficient A (MPa/(m·(L/s)²))",
"Required fire-stream reach Sk (m)",
"Nozzle flow (orifice discharge)",
"q = (π/4)·dn²·μ·√(2g·H), with μ≈1.0 and H = 100·Pq (m)",
"Simplified: q = 0.0348 × dn² × √Pq (q: L/s, dn: mm, Pq: MPa)",
"Check: dn=19 mm, Pq=0.25 MPa → q≈6.3 L/s, consistent with the code design value 6.5 L/s",
"Hose friction loss (Hazen-Williams)",
"i = 10.67 × Q^1.852 / (C^1.852 × d^4.87), with C=140 for lined hose",
"This tool uses the equivalent form A×L×q² (A calibrated at q≈5 L/s), which can be compared directly with the code tables",
"Hose resistance coefficient A reference (per metre, MPa/(m·(L/s)²))",
"Switching the hose diameter automatically fills in the corresponding A value; using a new polyurethane lining (C=150) can reduce it by a further about 12%",
"Fire-stream reach (GB 50974)",
"Sk = Hq / (1 + φ·Hq), where Hq is the nozzle pressure head (m) and φ is taken by nozzle diameter",
"Check: 19 mm nozzle, Pq=0.235 MPa (Hq=23.5 m) → Sk≈19.1 m",
"Indoor hydrant fire-stream reach is generally ≥10 m, and ≥13 m for high-rise buildings and factories/warehouses",
"This tool is for fire water-supply engineering estimation; formal design should follow the Technical Code for Fire Protection Water Supply and Hydrant Systems (GB 50974).",
"📚 In-Depth Analysis: Hydrant Discharge Flow Calculation",
"In fire water supply, estimate the actual discharge flow and fire-stream reach from the hydrant outlet pressure, hose diameter/length and nozzle diameter.",
"In design review, verify whether an indoor hydrant reaches the single-hydrant flow benchmark of 5 L/s.",
"On the training ground, demonstrate how different hose diameters/lengths attenuate the discharge flow and throw.",
"Verification for a DN65/25 m hose, 16 mm nozzle and 250 kPa outlet pressure",
"With the default parameters (outlet pressure 250 kPa, DN65 lined hose, length 25 m, 16 mm nozzle): hose friction loss 7.1 kPa (0.71 m head), nozzle pressure head Hq = 24.3 m, nozzle coefficient φ = 0.0124; discharge flow q = 4.39 L/s (15.8 m³/h), fire-stream reach Sk = 18.7 m ≥ required 13.0 m, meeting the fire water-supply requirement. Note: the single-hydrant benchmark is 5 L/s; here 4.39 L/s is slightly below it, and a longer or larger-diameter hose would raise it further.",
"Is the fire-stream reach of 18.7 m enough or not?",
"The indoor hydrant fire-stream reach requirement is ≥13 m for high-rise buildings and factories/warehouses and ≥10 m for other buildings. 18.7 m already meets the high-rise requirement; but to reach the single-hydrant benchmark of 5 L/s, the outlet pressure must be increased or the hose length shortened.",
"Why is the flow lower with a longer hose?",
"Hose friction loss increases roughly linearly with length, consuming part of the outlet pressure so the nozzle pressure drops and the flow decreases; hence long-distance supply often needs parallel mains or relay pressurization.",
'About "Hydrant Flow Calculator"',
"Based on fire hydraulics formulas, compute the hydrant's discharge flow at a given outlet pressure, the nozzle pressure, the hose friction loss and the fire-stream reach.",
"Combined flow and pressure calculation",
"Hose friction-loss calculation",
"Fire-stream reach verification",
"Multiple diameter options",
"Fire water-supply design",
"Hydrant system verification",
"Fire pump selection",
],
'zuranyangzhishupanding': [
"📋 Limiting Oxygen Index (LOI) Grader",
"Select a material type or enter the limiting oxygen index (LOI) directly to grade the material's flame retardancy and burning-performance classification.",
"The limiting oxygen index LOI (%, the minimum oxygen concentration to sustain burning): LOI not below 27 is a flame-retardant material (self-extinguishing away from the flame), 22 to 26 is combustible and below 22 is flammable; air contains about 21% oxygen, so a material with LOI not below 21 does not easily sustain burning away from the flame; per GB 8624 the burning performance of building materials is graded into A non-combustible, B1 flame-retardant, B2 combustible and B3 flammable, with LOI often used as a supporting criterion.",
"Material type (reference)",
"Polyethylene PE (LOI≈17)",
"Polypropylene PP (LOI≈18)",
"Polystyrene PS (LOI≈18)",
"Polyvinyl chloride PVC (LOI≈45)",
"Polytetrafluoroethylene PTFE (LOI≈95)",
"Wood (LOI≈22)",
"Cotton (LOI≈18)",
"Wool (LOI≈25)",
"Polyurethane PU (LOI≈16)",
"Nylon (LOI≈24)",
"Custom material",
"Limiting oxygen index LOI (%)",
"💡 Limiting oxygen index LOI = the minimum oxygen concentration (%) to sustain candle-like burning; the higher the LOI the harder to burn, and air contains about 21% oxygen.",
"The oxygen index is measured per GB/T 2406; air contains about 21% oxygen, so a material with LOI≤21 easily sustains burning in air.",
"GB 8624 burning-performance grading: B1 (flame-retardant) corresponds to LOI≥32 and B2 (combustible) to LOI≥26, for reference only.",
"The same material can vary widely in LOI with formulation, thickness and additives; the measured value should prevail.",
"The oxygen index only reflects how easily a material ignites and is not directly equivalent to overall flame-retardant performance.",
"📚 In-Depth Analysis: Flame-Retardant LOI Grading",
"In flame-retardant material selection, judge from the limiting oxygen index (LOI) whether the material burns in air and its flame-retardant grade.",
"Compare the LOI of different materials to help select products that meet GB 8624 grading.",
"Teaching demonstrates the concept that 'hard to burn in air is not non-burning in vacuum/high oxygen'.",
"Flame-retardant grade for LOI=45%",
"With the default parameters (limiting oxygen index LOI 45%): air contains about 21% oxygen, so the material is hard to burn in air, rated 'extremely hard to burn', GB 8624 grade B1 (flame-retardant); assessed as 'almost non-combustible, requiring a high-oxygen environment to burn'. LOI>45 is usually classed as extremely hard to burn, LOI 21-27 as combustible and >27 as flame-retardant; the higher the value the better the flame retardancy.",
"Does a high oxygen index always mean safety?",
"LOI reflects the ignition lower limit of a material in a static oxygen-nitrogen mixture, and the higher the value the harder to ignite; but a real fire involves thermal radiation, convection and ignition-source intensity, so it must still be judged together with the total heat of combustion and actual conditions.",
"What level is B1 in GB 8624?",
"GB 8624 classifies the burning performance of building materials into A (non-combustible), B1 (flame-retardant), B2 (combustible) and B3 (flammable); the B1 flame-retardant level is the minimum compliance requirement for decoration and insulation materials in most public places.",
'About "Limiting Oxygen Index (LOI) Grader"',
"Determine a material's flame-retardant grade and burning-performance classification from its limiting oxygen index (LOI), with reference values for common materials, for a quick evaluation of flame-retardant performance.",
"Built-in reference LOI for 10 common materials",
"Six-level flame-retardant grading",
"Corresponding GB 8624 burning-performance grading",
"Determine combustibility in air",
"Flame-retardant performance evaluation of decoration materials",
"Flame-retardant material selection and procurement",
"Fire-material acceptance verification",
"Flame-retardant instruction and outreach",
"Oxygen index",
],
'time-41': [
"🚑 Breaching Time Estimator",
"Select a breaching tool and the material to be breached, enter the thickness, and estimate the working time required to complete the breach.",
"Breaching tool",
"Hydraulic cutter",
"Abrasive saw",
"Power chain saw",
"Hydraulic breaker",
"Oxy-fuel cutting equipment",
"Manual breaching",
"Material to be breached",
"Brick wall",
"Material thickness (mm)",
"💡 Estimate: t = thickness / cutting rate; the cutting rate uses tool-material empirical values, and thick workpieces are corrected by a difficulty factor.",
"The cutting rate is an empirical average; in practice it is strongly affected by tool power, material strength and operator skill.",
"When the thickness exceeds 50 mm the difficulty rises, and the time has been corrected by a difficulty factor.",
"When the tool and material do not match (e.g. a chain saw cutting steel) the tool prompts that it is unsuitable and a proper tool should be used.",
"The estimate is for reference in work planning and force allocation and does not represent the precise working time.",
"📚 In-Depth Analysis: Breaching Time Estimation",
"Before rescue, estimate the breaching time from material, thickness and tool type to plan the attack and rescue pace.",
"Compare the breaching speed under different difficulty factors to choose the best tool combination.",
"In drills, incorporate the breaching time into RSET to assess its impact on overall evacuation safety.",
"Breaching calculation with difficulty factor ×1.0",
"With the default parameters (difficulty factor 1.0, cutting rate 120 mm/min): breaching time about 0.08 min (about 5 s), efficiency rated 'fast, breachable'. The higher the difficulty factor (e.g. reinforced ",
", composite structures) significantly lengthen the breaching time, so heavy tools or a backup passage must be prepared in advance.",
"What factors affect the cutting rate?",
"It mainly depends on material strength, thickness, tool power and blade condition; metals, concrete and composites differ hugely, and drill data should prevail in practice.",
"What if breaching is too slow?",
"When breaching becomes the bottleneck for rescue, entry should be made via another route or breaching and shoring carried out in parallel, and the actual time fed back into ",
"evacuation time",
" for re-verification of safety in the assessment.",
'About "Breaching Time Estimator"',
"Based on the combination of breaching tool and material, estimate the working time required for breaching together with the thickness, to aid firefighting force allocation and work planning.",
"6 breaching tools × 6 materials",
"Automatic thickness-difficulty correction",
"Smart prompt for tool mismatch",
"Output in minutes/seconds with an efficiency rating",
"Firefighting and rescue breaching planning",
"Rescue force and equipment allocation",
"Estimate for forced-entry operations",
"Rescue-training timing assessment",
"Material thickness",
],
'smoke-management': [
"🔥 Smoke Control Designer",
"Compute the plume mass flow, mechanical exhaust volume and smoke-layer control height based on the axisymmetric plume model.",
"Smoke generation is converted using the ideal-gas equation of state: V = m × T ÷ (ρ₀ × T₀), where m is the smoke mass flow, T is the absolute smoke temperature (K), ρ₀ = 1.293 kg/m³ is the air density at standard conditions and T₀ = 273 K; volumetric exhaust = smoke generation × safety factor (usually 1.2 to 1.5); exhaust-opening area = exhaust volume ÷ allowable velocity (natural exhaust 1 to 2 m/s, mechanical exhaust 8 to 10 m/s); the smoke-layer interface must be kept above the minimum clear height.",
"Height from the fuel surface to the smoke-layer bottom z (m)",
"Flame-height limit zl (m)",
"Design clear height of the smoke layer Hc (m)",
"Number of exhaust openings N",
"Maximum flow per exhaust opening (m³/h)",
"📖 Design Method",
"Axisymmetric plume mass flow (NFPA 92)",
"When z > zl: m = 0.071 × Qc^(1/3) × z^(5/3) × [1 + 0.027 × Qc^(2/3)/z]",
"When z ≤ zl: m = 0.032 × Qc^(3/5) × z",
"where Qc = 0.7 × Q (convective heat release rate, kW)",
"Volume-flow conversion",
"Smoke volume flow V = m × T / (ρ0 × T0)",
"ρ0 = 1.2 kg/m³ (air density), T0 = 293 K, T = smoke temperature (K)",
"Smoke temperature estimate: Ts = T0 + Qc / (m × Cp), Cp = 1.0 kJ/(kg·K)",
"This calculation is based on the NFPA 92 axisymmetric plume model and is suitable for exhaust-design estimation in large spaces. Formal design must follow the relevant codes and account for building geometry.",
"📚 In-Depth Analysis: Smoke Management System Design",
"For large-space, underground and atrium projects, calculate the exhaust volume and exhaust-opening layout from the fire heat release rate.",
"In performance-based design, verify that the clear height is above the occupant activity zone to ensure evacuation visibility.",
"For renovation projects, re-check whether the existing number of exhaust openings/airflow meets the code requirements.",
"Exhaust volume for Qc=3500 kW and clear height 3 m",
"With the default parameters (convective heat release rate 3500 kW, clear height 3 m, smoke-layer bottom 5.0 m): plume mass flow 35.38 kg/s, ",
"39.4 m³/s, exhaust volume 141972 m³/h; the smoke-layer bottom 5.0 m ≥ clear height 3.0 m, so smoke-layer control meets the requirement. The design recommends 10 exhaust openings at 14197 m³/h each; if currently insufficient, increase to 10.",
"What is the clear height?",
"The clear height is the minimum clearance from the smoke-layer bottom to the occupant activity floor and must ensure a breathable, visible space below the smoke layer in the evacuation route; it is generally not less than 2.1 m (above the occupant activity zone), and this project takes 3.0 m as the design value.",
"What happens if the exhaust volume is insufficient?",
"Insufficient exhaust volume makes the smoke-layer bottom keep descending and intrude into the clear height, rapidly worsening visibility and toxicity and directly compressing the available safe ",
"evacuation time",
" ASET, so the number of exhaust openings and the per-opening airflow must be increased as calculated.",
'About "Smoke Control Designer"',
"Based on the NFPA 92 axisymmetric plume model, compute the plume mass flow, smoke volume flow and temperature to aid mechanical smoke-exhaust system design.",
"Axisymmetric plume model",
"Mass/volume flow conversion",
"Smoke temperature estimation",
"Exhaust-opening count recommendation",
"Large-space smoke-exhaust design",
"Mechanical exhaust volume calculation",
"Smoke-layer control assessment",
],
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
        if it.get('src_diff') and it.get('zh_src'):
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
    return mp

def write(slug, mp):
    os.makedirs(OUT, exist_ok=True)
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('name', slug)
    out = {'slug': slug, 'industry': 'fire-rescue', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

for slug, en_list in EN.items():
    write(slug, build(slug, en_list))

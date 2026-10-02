#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'welding')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'welding')
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
    out = {'slug': slug, 'industry': 'welding', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
#!/usr/bin/env python3
def main():
    write('flow-ratio', build('flow-ratio', [
"🧮 Shielding Gas Mix Ratio Calculator",
"Choose the welding process, enter the total flow rate and the mixing ratios, then compute the flow of each component and the shielding effectiveness",
"Core formulas (by input variable): π×(d÷2)^2÷100; flow×1000÷60÷area",
"MIG/MAG gas-shielded",
"TIG gas tungsten arc",
"Gas cup diameter (mm)",
"Total flow rate (L/min)",
"Ar ratio (%)",
"CO₂ ratio (%)",
"💡 Recommended flow rate: 15~20 L/min for MIG/MAG and 8~15 L/min for TIG; the gas cup exit velocity should stay in the 8~15 m/s range.",
"The ratios do not need to sum to exactly 100%; the tool normalizes them automatically",
"In outdoor or windy environments the flow rate should be increased accordingly",
"📚 In-depth analysis: shielding gas mix ratio calculation",
"Split the total flow rate into the individual component flows according to the set Ar/CO₂ ratios, and configure the gas mixture proportioner accordingly.",
"Estimate the exit velocity from the gas cup bore to judge whether the shielding flow is laminar or turbulent and prone to entraining air.",
"Compare against the recommended flow ranges of different welding processes to quickly see whether the current setting is appropriate.",
"Mix Ratio and Exit Velocity",
"Component flow = total flow × ratio of that component ÷ sum of all component ratios (normalized automatically when the ratios do not sum to 100%). Gas cup cross-section (cm²) = π × (bore mm / 2)² ÷ 100. Exit velocity = flow (L/min) × 1000 ÷ 60 ÷ gas cup cross-section, giving a result in cm/s; divide by 100 again to convert to m/s. Recommended total flow: TIG 8~15 L/min, MIG/MAG 15~20 L/min.",
"Total flow 18 L/min, Ar:CO₂ = 80:20: Ar flow = 18×80/100 = 14.4 L/min, CO₂ = 3.6 L/min. With a 16 mm gas cup: cross-section = π×8²/100 ≈ 2.01 cm²; exit velocity = 18×1000/60/2.01 ≈ 149 cm/s ≈ 1.49 m/s. A flow of 18 L/min falls inside the recommended MIG/MAG range, so the result is rated good.",
"Why does the flow rate depend on the process?",
"TIG uses an inert gas with a soft arc, so an excessive flow disturbs the arc; MIG/MAG needs stronger wind resistance and droplet transfer protection, hence the larger recommended flow. Exceeding the range can cause porosity in either case.",
"Why does too large a flow rate actually worsen protection?",
"When the flow is too high the exit velocity rises and the flow easily turns from laminar to turbulent, entraining air from outside the gas cup into the shielding zone and carrying nitrogen and oxygen into the weld pool to form porosity. So a larger flow is not necessarily better.",
"About the Shielding Gas Mix Ratio Calculator",
"The shielding gas mix ratio calculator lets you pick MIG/MAG or TIG, enter the gas cup diameter, total flow rate and Ar/CO₂ mixing ratios, and then computes the flow of each component, the gas cup exit velocity and the shielding effectiveness, helping you set parameters for gas-shielded welding.",
"Supports both MIG/MAG and TIG",
"Mix ratios are normalized automatically",
"Gas cup exit velocity calculation",
"Shielding effectiveness rating",
"Tuning parameters for gas-shielded welding",
"Designing mixed gas ratios",
"Matching gas cups and flow rates",
"Optimizing welding quality and process",
"How to Use the Shielding Gas Mix Ratio Calculator",
"What does the shielding gas mix ratio calculator do?",
"Choose MIG/MAG or TIG, enter the gas cup diameter, total flow rate and Ar/CO₂ mixing ratios, and compute the flow of each component, the gas cup exit velocity and the shielding effectiveness to tune the gas mixture.",
"How do I use the shielding gas mix ratio calculator?",
"Which scenarios suit the shielding gas mix ratio calculator?",
"Gas cup diameter",
"Ar ratio",
"CO₂ ratio",
    ]))

    write('detector-25', build('detector-25', [
"🔍 Non-Destructive Testing (RT/UT/MT/PT) Methods",
"Choose a non-destructive testing method (RT/UT/MT/PT), enter the defect parameters, and rate the weld quality level to NB/T 47013",
"Weld defect rating (NB/T 47013): graded by the ratio of defect length to evaluation area length; Class I allows no linear defects, Classes II to IV are judged by the defect length ratio and the per-defect limit; round defects are converted to point counts, and anything beyond Class III is judged non-conforming; RT, UT, MT and PT each have their own acceptance tables.",
"Radiographic testing RT",
"Ultrasonic testing UT",
"Magnetic particle testing MT",
"Penetrant testing PT",
"Plate thickness (mm)",
"Round defect major diameter (mm)",
"Linear defect length (mm)",
"Evaluation area size (mm²)",
"📚 In-depth analysis: non-destructive testing (RT/UT/MT/PT) methods",
"Rate the weld quality level (Class I to IV) from the testing method and defect dimensions, to decide whether acceptance is allowed.",
"Pick a suitable non-destructive testing method for butt welds or fillet welds (surface vs internal defects).",
"Give the defect rating basis per NB/T 47013 to support rework decisions.",
"Grading rules (NB/T 47013)",
"Radiographic testing RT: with round defect major diameter cd and linear defect length sd (mm), the ratio = sd/plate thickness. Class I: cd≤2, sd≤6 and ratio≤0.25; Class II: cd≤4, sd≤12, ratio≤0.5; Class III: cd≤6, sd≤20, ratio≤0.8; otherwise Class IV. Ultrasonic testing UT: Class I sd≤8 and cd≤3; Class II sd≤15 and cd≤6; Class III sd≤25 and cd≤10; otherwise Class IV. Magnetic particle MT and penetrant PT: Class I cd≤1.5 and sd≤3; Class II cd≤3 and sd≤6; Class III cd≤6 and sd≤12; otherwise Class IV. Classes I and II pass; Classes III and IV need rework followed by re-inspection.",
"A 20 mm plate butt weld tested by RT finds a 3 mm round defect and a 10 mm linear defect: ratio = 10/20 = 0.5, which satisfies Class II (cd≤4, sd≤12, ratio≤0.5), so it is judged acceptable. If the linear defect were 18 mm: ratio 0.9, above the Class III limit of 0.8, so it is rated Class IV and needs rework. For surface testing by MT/PT: a 2 mm round defect and a 4 mm linear defect are Class II and acceptable.",
"How to choose between RT and UT?",
"Both detect internal defects: RT produces an imaging record and shows volumetric defects (porosity, slag) directly; UT is more sensitive to planar defects (lack of fusion, cracks), has no radiation and can measure thickness, but relies heavily on operator experience. Critical welds often use the two in a complementary way.",
"What is the difference between MT and PT?",
"MT applies only to ferromagnetic materials and can reveal surface and near-surface defects; PT works on any material (including stainless steel and non-ferrous metals) but can only detect surface-breaking defects. Neither can detect internal defects.",
"This tool rates weld quality levels in accordance with the NB/T 47013 standard for non-destructive testing of pressure equipment",
"RT is graded by round defects and linear defects; UT by wave-amplitude zone and indication length; MT/PT by magnetic trace and indication size",
"Class I is the highest quality, Class II passes, Class III passes conditionally, Class IV fails and needs rework",
"Practical ratings should also consider defect spacing, cluster defects and the overall rating",
"Inspectors must hold a special-equipment non-destructive testing certificate of Level II or above for the relevant method",
"About Non-Destructive Testing (RT/UT/MT/PT) Methods",
"The weld non-destructive testing rating tool supports radiographic (RT), ultrasonic (UT), magnetic particle (MT) and penetrant (PT) methods, and automatically rates the weld quality level to NB/T 47013.",
"Supports four testing methods: RT/UT/MT/PT",
"Graded to the NB/T 47013 standard",
"Round and linear defects rated separately",
"Automatic pass or fail decision",
"Weld quality acceptance",
"Pipe welding inspection",
"Steel structure weld inspection",
"How to Use Non-Destructive Testing (RT/UT/MT/PT) Methods",
"What do non-destructive testing (RT/UT/MT/PT) methods do?",
"How do I use non-destructive testing (RT/UT/MT/PT) methods?",
"Which scenarios suit non-destructive testing (RT/UT/MT/PT) methods?",
    ]))

    write('hanjiezidonghuapinggu', build('hanjiezidonghuapinggu', [
"📋 Welding Automation Assessment",
"Enter production volume, weld type and costs to assess automation feasibility and the return on investment",
"Core formulas (by input variable): robotHours×lb×0.6+rc×0.02×10000; out×robotSec÷3600; out×ms÷3600",
"Annual output (pieces/year)",
"Weld length per piece (m)",
"Manual welding time per piece (s)",
"Manual hourly wage (CNY/h)",
"Robot investment (10k CNY)",
"Working days per year (days)",
"💡 Robot welding time is about 40% of manual time; a payback under 3 years is recommended, under 2 years is strongly recommended.",
"The robot cost is an estimate; in reality it covers equipment, fixtures, programming and commissioning",
"A payback over 5 years calls for careful review or optimizing the production mix",
"📚 In-depth analysis: welding automation assessment",
"Estimate the manual welding cost from annual output, weld length per piece and manual hours, then compare it with the robot option.",
"Compute the payback period from the annual saving and the equipment investment",
"to judge whether the automation retrofit pays off.",
"Estimate the robot's annual working hours and check whether capacity matches the shift schedule.",
"Economic model",
"Annual total weld length (m) = annual output × weld length per piece; manual annual hours (h) = annual output × manual seconds per piece ÷ 3600; manual annual cost = manual hours × hourly wage. Robot time per piece is estimated at 40% of manual time, so robot annual hours = annual output × robot seconds per piece ÷ 3600; annual running cost = robot annual hours × hourly wage × 0.6 + equipment investment (10k CNY) × 0.02 × 10000 (maintenance taken as 2% of investment per year). Annual saving = manual annual cost − robot annual running cost; payback (years) = equipment investment (CNY) ÷ annual saving. Assessment: under 2 years strongly recommended, 2~3 years recommended, 3~5 years feasible, 5 years or more needs caution.",
"With 20,000 pieces a year, 2 m weld per piece, 600 s manual per piece, CNY 60 per hour and CNY 300,000 robot investment: manual hours = 20000×600/3600 ≈ 3333 h, manual cost ≈ 200,000 CNY; robot time 240 s per piece → annual hours ≈ 1333 h, running cost = 1333×60×0.6 + 30×0.02×10000 = 48,000+6,000 = 54,000 CNY; annual saving ≈ 146,000 CNY, payback ≈ 300,000/146,000 ≈ 2.1 years, rated as recommended. If annual output is only 5,000 pieces, the saving drops to about 25,700 CNY and the payback stretches to about 11.7 years, which calls for caution.",
"Is 40% of manual time reasonable for the robot?",
"The robot can strike continuously without pauses for slag removal or wire changes, so it is typically 2~3 times faster than manual work, and 40% is a common rough estimate. The actual figure depends on weld complexity, positioner coordination and programming quality, and should be calibrated by test welding measurements.",
"Does a short payback mean you must install a robot?",
"You also need stable product batches and consistent weld seams: with many varieties in small batches the programming and fixture changeover cost can noticeably stretch the real payback. Repetitive welds with large volume are the scenarios that suit automation best.",
"About the Welding Automation Assessment",
"The welding automation assessment tool takes annual output, weld length per piece, manual welding time and hourly wage, and robot investment, then computes the annual total weld length, manual and robot annual costs, annual saving and the payback period to assess automation feasibility.",
"Manual versus robot cost comparison",
"Payback period calculation",
"Automation level assessment",
"Daily working hour accounting",
"Decisions on welding automation retrofits",
"Robot welding investment analysis",
"Production line upgrade evaluation",
"Capacity expansion planning",
"Annual output",
"Weld length per piece",
"Manual welding time per piece",
"Manual hourly wage",
"Robot investment",
"Working days per year",
    ]))

    write('hanjiegongzhuangjiajusheji', build('hanjiegongzhuangjiajusheji', [
"📐 Welding Fixture Design",
"Enter the workpiece dimensions, weight and weld position to get a recommended fixture scheme and locating method",
"Core formulas (by input variable): wt×9.8×safety÷clampN; Math.ceil(L÷500)+2; wt×9.8×safety",
"Workpiece length (mm)",
"Workpiece width (mm)",
"Workpiece weight (kg)",
"Weld position",
"Horizontal weld",
"Vertical weld",
"💡 Place a clamping point every 300~500 mm; take a 1.5x safety factor on the workpiece weight for the clamping force; size the positioner for 1.5x the weight.",
"The clamping scheme here is a conventional recommendation; complex workpieces need a dedicated fixture design",
"Clamping force must avoid deforming the workpiece, which matters especially for thin plate",
"📚 In-depth analysis: welding fixture design",
"Determine the number of clamping points and the required clamping force from the workpiece size and weight, then lay out the fixture.",
"Choose the positioner type and load capacity from the workpiece weight so that rotation is safe.",
"Set the locating method and datum face from the weld form (horizontal, vertical or fillet welding).",
"Fixture model",
"Number of clamping points = ceil(workpiece length mm ÷ 500) + 2 (one every 500 mm plus one at each end); safety factor 1.5; total clamping force (N) = weight (kg) × 9.8 × 1.5; force per point = total clamping force ÷ number of clamping points. Positioner selection: under 50 kg use a manual flip fixture or benchtop fixture; 50~500 kg use a rotary positioner; 500 kg or more use a two-axis CNC positioner with a load capacity of ceil(weight × 1.5) kg. Locating method: for horizontal welds use bottom support + top clamps + side locating pins; for vertical welds use side support + locating stops + bottom datum face; for fillet welds use L-shaped locating blocks + quick clamps to set the 45° datum.",
"A workpiece of 2000×1000 mm weighing 300 kg: clamping points = ceil(2000/500)+2 = 6; total clamping force = 300×9.8×1.5 = 4410 N; force per point = 4410/6 = 735 N; choose a rotary positioner with a load capacity of ceil(300×1.5) = 450 kg. If the workpiece grows to 800 kg, a two-axis CNC positioner is needed with a capacity chosen at 1200 kg.",
"Why multiply the clamping force by a safety factor of 1.5?",
"Welding involves thermal deformation force, rotation inertia force and additional operator force, and the friction coefficient varies with surface condition. Taking 1.5x the weight as margin prevents the workpiece from shifting while welding or being rotated.",
"Why use a 500 mm spacing between clamping points?",
"This spacing gives enough restraint on long workpieces to suppress angular and wavy deformation without over-inflating fixture cost. For thin or easily distorted parts the spacing should be tightened.",
"About the Welding Fixture Design",
"The welding fixture design tool takes the workpiece length and width, weight and weld position, then recommends the number of clamping points, per-point and total clamping force, the locating method and positioner selection to support welding fixture design.",
"Clamping point count and spacing calculation",
"Clamping force safety factor calculation",
"Locating method recommendation",
"Positioner selection advice",
"Positioner selection",
"Production fixture scheme planning",
"Welding production line design",
"How to Use the Welding Fixture Design",
"What does the welding fixture design tool do?",
"Enter the workpiece length and width, weight and weld position, then get the recommended number of clamping points, per-point and total clamping force, the locating method and positioner selection for your fixture scheme.",
"How do I use the welding fixture design tool?",
"Which scenarios suit the welding fixture design tool?",
"Workpiece length",
"Workpiece width",
"Workpiece weight",
    ]))

    write('stress', build('stress', [
"🔮 Welding Distortion and Residual Stress Estimation",
"Enter plate thickness, weld length, leg size and restraint conditions to estimate shrinkage distortion and residual stress",
"Core formulas (by input variable): 0.15×(1-r)×L÷1000×1000; 0.1×leg+0.2; 0.02×leg÷th×57.3",
"Weld length (mm)",
"Leg size (mm)",
"Restraint condition",
"Weak restraint",
"Moderate restraint",
"Strong restraint",
"💡 The longitudinal shrinkage coefficient is about 0.1~0.3 mm/m; transverse shrinkage of a fillet weld is about 0.1×leg; residual stress can reach the yield strength.",
"The estimate is based on empirical formulas; actual distortion is strongly affected by process and structure",
"Distortion can be reduced by reverse deformation, symmetric welding and back-step welding",
"📚 In-depth analysis: welding distortion and residual stress estimation",
"Estimate longitudinal shrinkage, transverse shrinkage and angular distortion from weld length, leg size and restraint degree.",
"Estimate the residual stress level from the restraint degree to judge whether post-weld stress relief is needed.",
"Compare distortion under different restraint conditions and choose measures such as reverse deformation or symmetric welding.",
"Distortion and stress model",
"Transverse shrinkage (mm) ≈ 0.1 × leg size + 0.2; angular distortion (°) ≈ 0.02 × leg size ÷ plate thickness × 57.3; residual stress (MPa) ≈ yield strength × restraint degree; longitudinal shrinkage grows with (1 − restraint degree) and with weld length. Distortion grading: longitudinal shrinkage under 0.5 mm is small, 0.5~1.5 mm moderate, above 1.5 mm large; residual stress under 100 MPa is low, 100~180 MPa medium, above 180 MPa high.",
"Weld length 1000 mm, leg 6 mm, plate thickness 10 mm, restraint degree 0.5, yield strength 345 MPa: transverse shrinkage = 0.1×6+0.2 = 0.8 mm; angular distortion = 0.02×6/10×57.3 ≈ 0.69°; residual stress = 345×0.5 ≈ 173 MPa (medium). If the restraint degree rises to 0.8, the residual stress climbs to about 276 MPa (high) while longitudinal shrinkage shrinks correspondingly, which shows that tighter clamping suppresses distortion at the cost of higher residual stress.",
"Why does tighter restraint mean less distortion but more stress?",
"External restraint limits how freely the material can shrink, so the macroscopic distortion is suppressed while the internal elastic strain has nowhere to go and turns into higher residual stress. Excessive residual stress reduces fatigue performance and may initiate cracks.",
"How can welding distortion be reduced?",
"Common measures are preset reverse deformation, symmetric welding and segment back-step welding (to spread the heat), smaller leg size (as long as strength requirements are met), rigid fixturing, and a sensible assembly sequence. Heavy parts may also use post-weld heat treatment to relieve stress.",
"About the Welding Distortion and Residual Stress Estimation",
"The welding distortion and residual stress estimation tool takes plate thickness, weld length, leg size, material yield strength and restraint conditions, then estimates longitudinal shrinkage, transverse shrinkage, angular distortion and the residual stress level to support distortion control and process design.",
"Longitudinal and transverse shrinkage estimation",
"Angular distortion calculation",
"Residual stress level assessment",
"Dual distortion and stress grading",
"Predicting and controlling welding distortion",
"Reference for choosing process measures",
"Post-weld straightening assessment",
"Welding process optimization",
"Plate thickness",
"Weld length",
"Leg size",
"Material yield strength",
    ]))

    write('ventilation-protection', build('ventilation-protection', [
"🧮 Welding Safety Ventilation Calculation",
"Enter the welding consumable consumption and workshop volume to calculate the required airflow and protection advice",
"Core formulas (by input variable): fumeMass÷allowConc×60; con×coef×1000×hs; con×coef×1000",
"Consumable consumption (kg/h)",
"Workshop volume (m³)",
"Consumable type",
"Coated electrode",
"Solid welding wire",
"Flux-cored wire",
"Daily welding duration (h)",
"💡 Fume generation coefficients: coated electrode 0.8%, solid wire 0.5%, flux-cored wire 1.0%; the workshop air change rate should be at least 6 per hour.",
"The permissible fume concentration references GBZ 2.1, and this calculation applies a safety margin",
"Welding in confined spaces requires dedicated fume extraction and respiratory protection",
"📚 In-depth analysis: welding safety ventilation calculation",
"Estimate the fume generation from the consumable type and consumption rate, then compute the required airflow and the workshop air change rate.",
"Assess whether the existing ventilation meets the requirement and decide if local exhaust or a fume purifier is needed.",
"Estimate the daily total fume mass to support occupational health checks and protective equipment selection.",
"Ventilation model",
"Fume generation (mg/min) = consumable consumption × fume coefficient × 1000; fume coefficients: coated electrode 0.008, solid wire 0.005, flux-cored wire 0.01. Required airflow Q (m³/h) = fume generation ÷ permissible concentration × 60, taking the permissible concentration as 2 mg/m³ (a safety margin against the GBZ 2.1 total dust limit of 4 mg/m³). Air change rate = Q ÷ workshop volume (m³). Assessment: under 6 per hour is insufficient, 6~10 basically meets requirements, 10~20 is good, 20 or more is excellent.",
"With coated electrode consumption of 5 (tool input unit) and a workshop volume of 300 m³: fume generation = 5×0.008×1000 = 40 mg/min; required airflow = 40/2×60 = 1200 m³/h; air change rate = 1200/300 = 4 per hour, rated insufficient ventilation, so a local exhaust hood or mobile fume purifier is needed. Switching to flux-cored wire raises the coefficient to 0.01, increasing fume generation and the required airflow by 25%.",
"Why take the permissible concentration as 2 rather than the standard value?",
"GBZ 2.1 sets the total dust limit at 4 mg/m³, and engineering design often takes half of that as a safety margin to absorb the effects of multiple workstations working together, uneven airflow and real-world condition variation, reducing the risk of exceeding the limit.",
"How should general ventilation and local exhaust be combined?",
"Fume should be captured at the source whenever possible (local exhaust hoods, fume extraction integrated into the torch), with general ventilation as a supplement to dilute the residual concentration. Relying on general ventilation alone often costs a lot of energy while the breathing-zone concentration may still exceed the limit.",
"About the Welding Safety Ventilation Calculation",
"The welding safety ventilation calculation tool takes consumable consumption, workshop volume and consumable type, then computes fume generation, required airflow and air change rate, rates the ventilation level and gives protection advice to support safe workshop design.",
"Fume generation calculation",
"Required airflow calculation",
"Air change rate and ventilation rating",
"Graded protection advice",
"Workshop ventilation design",
"Occupational health and safety assessment",
"Fume purification equipment selection",
"Workplace environment improvement",
"Consumable consumption",
"Workshop volume",
"Daily welding duration",
    ]))


if __name__ == '__main__':
    main()
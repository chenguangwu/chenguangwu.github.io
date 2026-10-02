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
    write('index', build('index', [
"🔥 Welding Engineering Tools",
"Welding Engineering",
"Welding Engineering Tools",
"Enter plate thickness and carbon equivalent (estimable from C, Mn, Cr, Mo via the IIW formula), decide whether preheat is needed, and compute the recommended preheat temperature and hold time for cold cracking prevention.",
"Choose MIG/MAG or TIG, enter the gas cup diameter, total flow rate and Ar/CO₂ mixing ratios, compute the flow of each component and the gas cup exit velocity and rate the shielding effectiveness for gas mix tuning.",
"Enter plate thickness, material (carbon steel, stainless steel, aluminium alloy), welding position and method to get a recommended welding current range, arc voltage, travel speed, heat input and consumable diameter for initial process parameter selection.",
"Enter the material type (low-carbon steel, low-alloy steel, austenitic stainless steel, etc.), plate thickness and preheat temperature to calculate the recommended interpass temperature range for multi-pass temperature control and crack prevention.",
"Welding Safety Ventilation Calculation",
"Enter consumable consumption and workshop volume to compute the required ventilation air change rate and give protection advice (referencing the GBZ 2.1 fume concentration limit), for workshop dust control and occupational health protection.",
"Enter the base material (Q235/Q345/304/316/20 steel), plate thickness and welding position to get a matching electrode or wire grade, diameter and reference current range for consumable selection and process preparation.",
"An online welding current selector that recommends a suitable current range from the electrode diameter and material, helping set manual arc welding parameters and improve weld quality, running entirely in the browser.",
"Choose a non-destructive testing method (RT/UT/MT/PT), enter the defect parameters, and rate the weld quality level to the NB/T 47013 standard.",
"Enter welding current, voltage, welding time, electricity price, duty cycle and machine efficiency to compute arc power, arcing and average energy and electricity cost, and estimate total energy including no-load loss for welding cost management.",
"Enter the welding method, base material and welding parameters to compute the heat input and auto-generate a welding procedure specification (WPS) summary card for procedure qualification documents and shop-floor guidance.",
"Welding defect analysis tool: reviews common weld defect types, appearance and causes to support weld quality judgement and improvement.",
"Welding metallurgy analysis tool: analyses metallurgy, phase transformation and microstructure evolution in the weld zone to support process selection and joint performance assessment.",
"Enter annual output, weld length per piece, manual welding time and hourly wage, and robot investment to compute annual total weld length, manual and robot annual costs, annual saving and payback period, assessing automation feasibility.",
"Enter plate thickness, weld length, leg size, material yield strength and restraint conditions to estimate longitudinal or transverse shrinkage, angular distortion and residual stress level for distortion control and reverse deformation design.",
"Enter workpiece length and width, weight and weld position to get the recommended number of clamping points, per-point and total clamping force, locating method and positioner selection for welding fixture scheme design.",
"About the Welding Engineering Tools",
"The welding engineering tool collection brings together 15 free online tools covering the common calculation, conversion and lookup needs in welding engineering scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you will find ready-to-use utilities here. Every tool runs entirely in the browser, uploads no data to a server, and keeps your privacy secure.",
"The welding engineering tools collected on this page include (some representative tools):",
"These tools help you finish common welding engineering tasks quickly, with no need to memorize complex formulas or do manual conversions, just enter and get the result.",
"Do the Welding Engineering Tools need a download or registration?",
"No. All welding engineering tools on this page are pure front-end online tools: open the page and use them directly, with no software to install, no account to register, and no data uploaded.",
"Are the Welding Engineering Tools results accurate? Is my data safe?",
"The tools compute locally in your browser from public mathematical formulas and general industry standards, so results are available instantly. All computation happens on your own device, data is never uploaded to a server, and your privacy is protected.",
    ]))

    write('analysis-37', build('analysis-37', [
"📊 Welding Defect Analysis (Type / Cause)",
"Defect / type / cause",
"Item share = count of that item ÷ total defects × 100%; sorting by count in descending order and accumulating gives the cumulative share.",
"Types within a cumulative share of 80% are Class A major defects and the priority targets for rework and rectification.",
"Harmful defects such as cracks should be tracked separately even when few, so a ranking by share alone is not enough.",
"Defect data (one 'type,count' pair per line)",
"Porosity,18\nSlag inclusion,10\nLack of fusion,6\nCrack,4\nUndercut,3",
"Pareto analysis",
"📚 In-depth analysis: welding defect statistics and Pareto analysis",
"Weld rework defect statistics",
"Monthly welding quality analysis",
"Locating process improvement priorities",
"Item share = count of that item ÷ total defects ×100%; accumulating in descending count order gives the cumulative share, and items within a cumulative share of 80% are Class A major defects.",
"Porosity 45, slag inclusion 20, incomplete penetration 15, cracks 8, undercut 6, other 6 → total 100, cumulative shares 45.00%, 65.00%, 80.00%, so Class A covers 3 items: porosity, slag inclusion and incomplete penetration.",
"Why use Pareto analysis?",
"A few defect types often account for most of the rework volume, so fixing the Class A major defects first reduces rework cost and schedule loss most effectively.",
"Can cracks be ignored because they are few?",
"No. Cracks are harmful defects that directly affect structural safety, so even a small number should be tracked separately and the cause investigated.",
"About the Welding Defect Analysis (Type / Cause)",
"Welding defect analysis (type / cause). Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
"Porosity,45",
    ]))

    write('analysis-38', build('analysis-38', [
"👥 Welding Metallurgy / Phase Transformation / Microstructure Analysis",
"Welding heat input and t8/5 cooling time",
"Enter welding current, voltage, travel speed and preheat temperature (thermal efficiency defaults to 0.8). Heat input Q＝ηUI÷v; for three-dimensional heat conduction in thick plate t8/5＝Q÷(2πλ)×[1/(500−T₀)−1/(800−T₀)], with λ taken as 0.025 J/(mm·s·K); average cooling rate＝300÷t8/5.",
"Welding travel speed (mm/s)",
"Preheat temperature (°C)",
"Thermal efficiency η (0~1)",
"Compute cooling time",
"📚 In-depth analysis: welding heat input and t8/5 cooling time",
"Before welding procedure qualification, check the heat input from current, voltage and speed to see whether it falls inside the line energy range allowed by the procedure.",
"Use the t8/5 cooling time to predict heat-affected zone phase transformation and assess hardening and cold cracking risk.",
"When adjusting the preheat temperature, watch how t8/5 changes with this tool to fix the minimum preheat temperature.",
"Trial calculation for thick plate welding",
"Current 220 A, voltage 26 V, speed 5 mm/s, preheat 25°C, ",
"thermal efficiency",
"0.8, heat input Q=915.20 J/mm, t8/5=4.75 s, average cooling rate 63.18 °C/s, judged as rather fast cooling with attention needed to hardening microstructure and cold cracking risk.",
"What is the appropriate range for t8/5?",
"The tool takes 8~25 s as a reference suitable range for general structural steel; the exact range depends on the steel grade and joint requirements, and low-temperature and high-strength steels demand tighter control.",
"Why use the thick plate formula?",
"This tool uses the three-dimensional thick plate conduction formula, which suits relatively thick plate where heat flow spreads in three dimensions; thin plate needs the two-dimensional formula, whose results would be noticeably larger.",
"What value should the thermal efficiency take?",
"Submerged arc welding is about 0.95~0.99, manual arc welding about 0.7~0.85, and gas-shielded welding about 0.6~0.8. This tool defaults to 0.8 and can be adjusted to the actual process.",
"About the Welding Metallurgy / Phase Transformation / Microstructure Analysis",
"Welding metallurgy / phase transformation / microstructure analysis. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
    ]))

    write('wps-hanjiegongyiguichengbianzhi', build('wps-hanjiegongyiguichengbianzhi', [
"🔥 WPS Welding Procedure Specification Builder",
"Enter welding parameters to compute the heat input and generate a welding procedure specification (WPS) summary",
"Core formulas (by input variable): U×I÷vMmS÷1000; v÷6",
"GTAW gas tungsten arc welding",
"Base material grade",
"20 steel",
"Consumable grade",
"Consumable diameter (mm)",
"Welding travel speed (cm/min)",
"Number of weld passes",
"💡 Heat input HI = U×I/v ÷1000 (kJ/mm); deposition rate depends on the welding method and current.",
"The WPS summary is for reference only; the official specification must be backed by procedure qualification (PQR)",
"Heat input must be tightly controlled against material property requirements",
"📚 In-depth analysis: WPS welding procedure specification builder",
"Compute the heat input from current, voltage and travel speed as a key WPS parameter and qualification basis.",
"Estimate the deposition rate of different welding methods for labour hour and consumable consumption estimates.",
"Generate WPS summary text for archiving, issuing and comparison against the procedure qualification (PQR).",
"Heat input and deposition",
": v(mm/s) = v(cm/min) ÷ 6. Heat input HI (kJ/mm) = voltage × current ÷ travel speed (mm/s) ÷ 1000. Deposition rate (kg/h): manual arc welding SMAW = current × 0.0035; gas tungsten arc welding GTAW = current × 0.0025; gas metal arc welding GMAW/flux-cored = current × 0.005. Heat input assessment: below 1.0 is low, 1.0~2.5 moderate, 2.5~4.0 high, 4.0 or more excessive.",
"Current 200 A, voltage 24 V, speed 30 cm/min: v = 30/6 = 5 mm/s; heat input = 24×200/5/1000 = 0.96 kJ/mm (low). Switching to GMAW, the deposition rate = 200×0.005 = 1.0 kg/h; at the same current SMAW gives 200×0.0035 = 0.70 kg/h and GTAW gives 0.50 kg/h, so gas metal arc welding is the most efficient.",
"Why is heat input an important WPS parameter?",
"Heat input determines the cooling rate of the weld and heat-affected zone, directly affecting microstructure and properties: too little promotes hardening and cold cracking, too much coarsens grains and reduces toughness, so procedure qualification normally limits the heat input range.",
"Is deposition rate the same as deposition efficiency?",
"No. Deposition rate here means the mass of metal deposited into the weld per unit time (kg/h), used for labour hour estimates; deposition efficiency also involves consumable utilization rate and spatter loss, which is a different concept.",
"About the WPS Welding Procedure Specification Builder",
"The WPS builder takes the welding method, base material, consumable, current, voltage, speed and preheat parameters, then computes the heat input and deposition rate and generates a welding procedure specification (WPS) summary text to support procedure document preparation.",
"Heat input computed automatically",
"Deposition rate estimation",
"Heat input level assessment",
"WPS summary text generation",
"Previewing parameters for procedure qualification",
"Heat input control and verification",
"Standardizing procedure documents",
"Consumable diameter",
"Welding current",
"Arc voltage",
"Welding travel speed",
"Preheat temperature",
    ]))


if __name__ == '__main__':
    main()
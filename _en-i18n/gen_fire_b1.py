#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'fire')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'fire')
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
    out = {'slug': slug, 'industry': 'fire', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('hydrant-pressure', build('hydrant-pressure', [
        "Hydrant Pressure at the Most Unfavourable Point",
        "H = Hgeo + Hq + Hd + Hw, estimating the pressure required by the hydrant at the most unfavourable point",
        "Hydrant Pressure",
        "/ Hydrant Pressure",
        "View the Hydrant Pressure at the Most Unfavourable Point User Guide",
        "Nozzle dynamic pressure = geometric elevation difference + friction loss in transit + local loss",
        "Elevation difference Hgeo between the most unfavourable point and the water source (m)",
        "Nozzle pressure Hq corresponding to the effective water jet (mH2O)",
        "Hose length Ld (m)",
        "50 mm (liner)",
        "65 mm (liner)",
        "80 mm (liner)",
        "Design flow q (L/s)",
        "Network calculation pipe length Lw (m)",
        "Network pipe diameter d (mm)",
        "Hazen-Williams coefficient C",
        "100 (old steel pipe)",
        "120 (cast iron)",
        "140 (galvanised steel pipe)",
        "150 (plastic pipe)",
        "Required pressure formula",
        "H = Hgeo (elevation difference) + Hq (nozzle pressure) + Hd (hose loss) + Hw (network loss)",
        "Hose friction loss Hd = A x Ld x q^2  (A is the hose resistance coefficient)",
        "Network friction loss hf = 10.67 x Lw x Q^1.852 / (C^1.852 x D^4.87)  (Hazen-Williams, Q = m3/s, D = m)",
        "Hw = 1.1 x hf (including 10% local loss)",
        "Hose resistance coefficient A (liner hose)",
        "Nozzle pressure Hq reference (19mm water gun): an effective jet of 10m is about 13.5 mH2O, 13m about 16 mH2O, 15m about 20 mH2O.",
        "The result unit is mH2O (metre of water column), 1 mH2O = about 0.01 MPa. This calculation is an engineering estimate; the formal design should be checked against the current fire code and a detailed hydraulic calculation.",
        "In-Depth Analysis: Hydrant Pressure at the Most Unfavourable Point",
        "In the hydraulic calculation of a hydrant system, the pressure required at the most unfavourable point is found (elevation difference + nozzle + hose friction loss + network loss).",
        "The choice of pipe diameter and material (C value) directly affects the friction loss, which is the key to design optimisation.",
        "Total",
        "pressure conversion",
        "is MPa for comparison with the",
        "pump head",
        "/ network static pressure check.",
        "Worked example: elevation difference 10m, nozzle 20m, hose 20m/Φ65, flow 5L/s, network 50m/Φ100/C=100",
        "Hose friction loss Hd = AxLxq^2 = 0.0017x20x25 = 0.85 m; friction loss hf = 10.67x50x0.005^1.852/(100^1.852x0.1^4.87) = 0.428 m; Hw = 1.1x0.428 = 0.471 m; total H = 10+20+0.85+0.471 = 31.32 m (= about 0.313 MPa).",
        "Worked example: loss composition",
        "H = Hgeo + Hq + Hd + Hw. The hose friction coefficient is taken by Φ (Φ50/65/80 correspond to 0.00712/0.0017/0.00075); the network friction uses the Hazen-Williams equation, and the larger D and C, the smaller the loss.",
        "How is the hose friction coefficient taken?",
        "Look it up by hose diameter: Φ50->0.00712, Φ65->0.0017, Φ80->0.00075 (unit m/(L/s)^2·m). The larger the diameter the smaller the unit loss, which is why a large-diameter hose is preferred during firefighting.",
        "Which formula is used for network friction loss?",
        "Hazen-Williams is common: hf = 10.67·L·Q^1.852/(C^1.852·D^4.87), with Q in m3/s and D in m. C is the pipe roughness coefficient (higher for PE pipe, lower for old steel pipe), and the loss is extremely sensitive to diameter and C.",
        "About Hydrant Pressure",
        "Estimates the pressure required by the hydrant at the most unfavourable point using H = Hgeo + Hq + Hd + Hw, breaking down the hose and network head losses.",
        "Automatic hose resistance coefficient lookup",
        "Hazen-Williams network loss",
        "Visual breakdown of the pressure components",
        "Dual units of mH2O and MPa",
        "Fire water supply design",
        "Most unfavourable point pressure check",
        "Fire pump head estimation",
    ]))

    write('extinguisher-calc', build('extinguisher-calc', [
        "Extinguisher Configuration Calculation (GB 50140)",
        "Computes the required quantity and fire rating from the Code for Design of Fire Extinguishers",
        "Extinguisher Configuration Calculation (Fire Protection)",
        "View the Extinguisher Configuration Calculation (GB 50140) User Guide",
        "Maximum protection distance of the extinguisher / configuration baseline (GB 50140)",
        "Calculation unit area S (m2)",
        "Class A (solid substances)",
        "Class E (electrical fires)",
        "Correction factor K",
        "1.0 (no fixed fire protection facilities)",
        "0.9 (indoor hydrant installed)",
        "0.7 (extinguishing system installed)",
        "0.5 (hydrant + extinguishing system)",
        "1.3 (underground / entertainment venue)",
        "Selected single extinguisher fire rating",
        "Configuration baseline (Class A / Class E)",
        "Minimum configuration baseline (GB 50140 Table 6.2.1)",
        "Severe hazard level: minimum 3A per unit, maximum protected area per A of 50 m2",
        "Medium hazard level: minimum 2A per unit, maximum protected area per A of 75 m2",
        "Light hazard level: minimum 1A per unit, maximum protected area per A of 100 m2",
        "Required fire rating Q = K · S / U",
        "Number of extinguishers N = ceil(Q / single extinguisher rating)",
        "Per configuration point: 2 <= count <= 5",
        "Class E (electrical) fire places take the configuration baseline from the hazard level of the place they are in (Class A or Class B), and non-conductive extinguisher types should be selected (such as carbon dioxide or dry powder). For Class B/C fires refer to GB 50140 Table 6.2.2.",
        "In-Depth Analysis: Extinguisher Configuration Calculation (GB 50140)",
        "In extinguisher configuration design, the required fire rating and number of units are computed from the fire hazard level, the protected area and the single extinguisher rating.",
        "Severe, medium and light hazard levels correspond to different minimum single-unit ratings and maximum protected area per A.",
        "Each calculation unit has at least 2 units, reasonably distributed over several configuration points.",
        "Worked example: medium hazard level, area 300 m2, K=1.0, single unit 2A",
        "Required fire rating Q = KxS/U = 1.0x300/75 = 4.0 A; number N = ceil(4.0/2) = 2 units (>=2); 1 configuration point x 2 units per point = 2 units. Formula: Q=K·S/U, N=⌈Q/single rating⌉.",
        "Worked example: light hazard level, area 600 m2, single unit 1A",
        "Q = 1.0x600/100 = 6.0 A; N = ⌈6.0/1⌉ = 6 units; configuration points = ⌈6/5⌉ = 2, each with ⌈6/2⌉ = 3 units, totalling 6 units. When the single-unit rating is below the minimum required for the level, check against the minimum rating.",
        "How does the hazard level affect the configuration?",
        "Severe, medium and light hazard levels correspond to U (maximum protected area per A) of 50/75/100 m2 and minimum single-unit ratings of 3/2/1A. The higher the level the smaller the protected area and the higher the single-unit requirement, so the count increases accordingly.",
        "Why at least 2 units per unit?",
        "To prevent a single unit failing or extinguishers near a fire point being unreachable. The code requires at least 2 units per calculation unit, distributed over several points at 2-5 units per point, balancing accessibility and redundancy.",
        "About Extinguisher Configuration Calculation",
        "Computes the required fire rating and quantity of building extinguishers from GB 50140, gives configuration point suggestions, and supports hazard levels and correction factors.",
        "Automatic check of the minimum fire rating",
        "Selectable correction factor",
        "Configuration point count suggestion",
        "Building fire protection design",
        "Extinguisher configuration acceptance",
    ]))

    write('detector-176', build('detector-176', [
        "Detection (Interlock/Alarm/Maintenance) Service",
        "Interlock/alarm/maintenance",
        "View the Detection (Interlock/Alarm/Maintenance) Service User Guide",
        "The fire interlock system is evaluated item by item across 6 detections (fire detectors, sprinkler system, smoke control system, fire curtains and fire doors, emergency broadcast and fire telephone, elevator emergency descent), with 1 point counted per abnormality; a total of 0 means the interlock is normal, 1 to 2 abnormalities is a minor hazard, and 3 or more is a major hazard; the interlock response is required to act within 30 seconds after alarm confirmation, detectors must be cleaned and calibrated at least once every 2 years, and the sprinkler terminal test pressure must be not lower than 0.05 MPa.",
        "Fire interlock system detection assessment (6-item system interlock detection)",
        "1. Fire detector interlock",
        "Normal interlock (0 points)",
        "Partially delayed (2 points)",
        "Interlock failure (3 points)",
        "2. Sprinkler system interlock",
        "Normal start (0 points)",
        "Start delay (2 points)",
        "Unable to start (3 points)",
        "3. Smoke control system interlock",
        "Partially abnormal (2 points)",
        "4. Fire curtain/door interlock",
        "Normal descent (0 points)",
        "Partially jammed (2 points)",
        "Unable to descend (3 points)",
        "5. Emergency broadcast/telephone",
        "Normal broadcast (0 points)",
        "Complete failure (3 points)",
        "6. Elevator emergency descent interlock",
        "Normal emergency descent (0 points)",
        "Delayed/partial (2 points)",
        "Unable to descend (3 points)",
        "In-Depth Analysis: Detection (Interlock/Alarm/Maintenance) Service",
        "In fire interlock control system detection, scores are given item by item for fire detectors, sprinklers, smoke control, fire curtains, broadcast telephone and elevator emergency descent.",
        "During annual detection and fault troubleshooting, the scoring quickly judges whether the interlock is normal, basically normal or seriously faulty.",
        "The higher the score the more subsystems have failed, so the specific repair items must be listed and handled within a deadline.",
        "Worked example: all normal (all items 0 points)",
        "Fault score = 0 / 18 -> 'interlock normal', all interlock systems test normal, and regular detection and maintenance on schedule is recommended.",
        "Worked example: single system fault (2 points)",
        "For example, if only 'fire detectors' scores 2 points, the total = 2 <= 4 -> 'basically normal', that item needs repair and re-inspection; any item >=2 is flagged as 'needs repair'.",
        "Above how many points counts as a serious fault?",
        "This tool uses a total of 0 for interlock normal, <=4 for basically normal, and >4 for serious fault (18 in total, 0 = all normal). A single subsystem item scoring >=2 is treated as needing repair.",
        "How often is the interlock detection done?",
        "Usually per fire regulations and the maintenance contract, the interlock control system needs a full detection at least once a year; after major modifications or fault repairs a specific re-inspection is also needed, and records should be kept.",
        "About Detection (Interlock/Alarm/Maintenance) Service",
        "Detection (Interlock/Alarm/Maintenance) Service. Free online tool, pure front-end processing, data is not uploaded, privacy and security protected.",
    ]))


if __name__ == '__main__':
    main()

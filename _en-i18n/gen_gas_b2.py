#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'gas')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'gas')
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
    out = {'slug': slug, 'industry': 'gas', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('current-2', build('current-2', [
        "Cathodic Protection Monitoring Calculation",
        "Enter the pipe material, soil resistivity and area to compute the protection potential and current",
        "Core formula (by input variable): Ax iDen/1000",
        "View the Buried Pipeline Cathodic Protection Current and Status User Guide",
        "Pipe material",
        "Soil resistivity (Ω·m)",
        "Measured potential (V)",
        "Carbon steel protection potential <= -0.85V (CSE); the current density decreases as soil resistivity rises; high resistivity calls for impressed current.",
        "The protection potential is referenced to the CSE (copper sulfate electrode)",
        "Over-protection (<-1.2V) may cause cathodic disbonding of the coating",
        "In-Depth Analysis: Cathodic Protection Current and Status of Buried Pipelines",
        "Impressed current or sacrificial anode design for long-distance and urban buried steel pipelines",
        "Protection potential measurement and status assessment of existing pipelines",
        "Soil",
        "resistivity",
        "zoned selection of the anode scheme",
        "Take the current density iDen by soil resistivity ρ",
        "current density",
        "(ρ<20->50, <50->30, <100->20, otherwise 10 mA/m2), total protection current iTotal = area x iDen / 1000; the carbon steel protection potential should be <= -0.85V (CSE), <=-0.90V is over-protection, <=-0.85V is adequate protection, <=-0.75V is marginal, otherwise protection is insufficient.",
        "Carbon steel ρ=50 Ω·m, area 100 m2, potential -0.95V: iDen=20 mA/m2, iTotal=100x20/1000=2.0 A; -0.95V <= -0.90V is over-protection (should be raised or checked for coating defects); ρ=50<60 recommends a magnesium alloy sacrificial anode or impressed current.",
        "What are the hazards of over-protection?",
        "A potential that is too negative (<-1.2V) may trigger cathodic disbonding of the coating and damage the anti-corrosion layer; the power supply or the number of anodes must be adjusted to return to the code range.",
        "How does resistivity affect anode selection?",
        "ρ<15 suits magnesium alloy sacrificial anodes; 15~60 magnesium alloy or impressed current; >60 impressed current (external power source + auxiliary anode) is more economical and reliable.",
        "About Cathodic Protection Monitoring Calculation",
        "Cathodic protection monitoring calculation tool; enter the pipe material, soil resistivity, protection area and measured potential, and compute the protection potential standard, current density, total protection current and protection status, and recommend an anode scheme, assisting cathodic protection design and monitoring.",
        "Protection potential standard judgement",
        "Graded current density calculation",
        "Protection status assessment",
        "Anode scheme recommendation",
        "Buried pipeline cathodic protection design",
        "Cathodic protection effectiveness monitoring",
        "Sacrificial anode selection",
        "Impressed current system configuration",
        "Soil resistivity",
        "Protection area",
        "Measured potential",
    ]))

    write('flow-4', build('flow-4', [
        "Gas Flow Metering Calculation",
        "Select the metering method, enter the parameters and compute the volume flow, mass flow and velocity",
        "Core formula (by input variable): Cxπ/4x(d/1000)^2x√(2xdPa/rho); π/4x(D/1000)^2; Qls/1000/area",
        "Metering method",
        "Orifice flow meter",
        "Turbine flow meter",
        "Orifice bore diameter (mm)",
        "Pressure difference (kPa)",
        "Meter coefficient (1/L)",
        "Frequency (Hz)",
        "Orifice Q=C·(π/4)·d²·√(2ΔP/ρ); turbine Q=f/K; the β ratio (d/D) should be 0.2~0.7.",
        "The orifice flow coefficient C actually needs to be corrected per the standard (GB/T 2624)",
        "A turbine flow meter must be used within its turndown ratio range",
        "In-Depth Analysis: Gas Orifice/Turbine Metering Flow",
        "Metering device design for gas flow at regulating stations and industrial and commercial users",
        "On-site verification by the orifice differential pressure method or the turbine frequency method",
        "Trade settlement metering parameter review",
        "Orifice method Q=C·(π/4)·d²·√(2ΔP/ρ) (C≈0.6, d is the bore in m); turbine method Qls = frequency / meter coefficient, Qh = Qlsx3.6;",
        "converting to mass flow = Qh x density. The β ratio (d/D) should be 0.2~0.7.",
        "Orifice D=100mm, d=50mm, ΔP=10kPa, ρ=0.7: Q≈0.199 m3/s = 716.9 m3/h, mass flow 501.8 kg/h, velocity 25.35 m/s, β=0.50 (reasonable within 0.2~0.7).",
        "Why must the β ratio be 0.2~0.7?",
        "Too small limits the turndown, too large makes the discharge coefficient unstable and demands long straight runs; 0.2~0.7 is the balance zone between accuracy and pressure loss.",
        "How to choose between turbine and orifice?",
        "Use a turbine for trade settlement/large flow (high accuracy, long straight runs); for dirty or impurity-containing gas an orifice is more resistant to fouling but has a larger pressure loss.",
        "About Gas Flow Metering Calculation",
        "Gas flow metering calculation tool; select the orifice or turbine metering method, enter parameters such as bore/pressure difference or meter coefficient/frequency, and compute the volume flow, mass flow and velocity, assisting gas metering design and verification.",
        "Two methods: orifice and turbine",
        "Volume/mass flow calculation",
        "Pipeline velocity accounting",
        "β ratio and turndown notes",
        "Gas metering system design",
        "Flow meter selection and verification",
        "Metering data conversion",
        "Operating condition flow accounting",
        "Pipeline inner diameter",
        "Orifice bore diameter",
        "Meter coefficient",
        "Gas density",
    ]))

    write('length-pipeline', build('length-pipeline', [
        "Pipeline Crossing Length Calculation",
        "Enter the crossing distance, pipe diameter and geological conditions to compute the directional drilling construction length",
        "Core formula (by input variable): dep/Math.sin(enRad); dep/Math.sin(exRad); totalLen+depx2",
        "Crossing distance (m)",
        "Entry angle (°)",
        "Exit angle (°)",
        "Burial depth (m)",
        "Entry angle 8°~18°, exit angle 6°~12°; the reaming diameter is 1.2~1.5 times the pipe diameter.",
        "The crossing length is a geometric estimate; in reality the curvature radius and geology must be considered",
        "Large diameter or long distance crossings should have a dedicated design",
        "In-Depth Analysis: Directional Drilling Crossing Length and Reaming",
        "Road/river non-trench gas pipeline crossing design",
        "Assessment of the effect of the entry/exit angles and burial depth on the construction length",
        "Large diameter crossing difficulty and reaming diameter determination",
        "Entry section length = depth / sin(entry angle), exit section length = depth / sin(exit angle); total construction length = crossing distance + entry section + exit section; drilled length = total length + 2 x depth; reaming diameter = pipe diameter x 1.4. D<=400 is conventional, <=800 is medium, otherwise a large diameter crossing.",
        "Crossing distance 200m, pipe diameter 300mm, entry angle 10°, exit angle 8°, depth 5m: entry section 5/sin10°=28.8m, exit section 5/sin8°=35.9m, total length 264.7m, drilled 274.7m, reaming 420mm, D=300<=400 is a conventional crossing.",
        "What values are usually taken for the entry and exit angles?",
        "Commonly 8°~18°; too small makes the drilled length excessive, too large gives a large curvature that easily sticks the drill; it must be set together with the burial depth and the pipe bend radius.",
        "Why is the reaming taken at 1.4 times the pipe diameter?",
        "To leave clearance for pullback and space for the mud ring, ensuring the pipe pulls back smoothly and reducing the risk of pipe binding; it can be raised appropriately for large diameters.",
        "About Pipeline Crossing Length Calculation",
        "Pipeline crossing length calculation tool; enter the crossing distance, pipe diameter, entry angle, exit angle and burial depth, and compute the entry section, exit section, total construction length and reaming diameter, assess crossing difficulty, and assist directional drilling crossing design.",
        "Entry/exit section length calculation",
        "Total construction length calculation",
        "Reaming diameter recommendation",
        "Crossing difficulty assessment",
        "Directional drilling crossing construction design",
        "Pipeline crossing scheme planning",
        "Drill rig selection and schedule estimation",
        "Crossing quantity accounting",
        "Crossing distance",
        "Pipe diameter",
        "Entry angle",
        "Exit angle",
        "Burial depth",
    ]))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# gen_electromagnetism_head.py — shared head for electromagnetism batches b1..b6
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'electromagnetism')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'electromagnetism')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
DISCL = "This tool provides auxiliary calculations for electromagnetics and circuit fundamentals. Results are for educational and preliminary design reference only, and do not replace formal engineering design, EMC standards, or the judgment of a certified engineer."
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
    out = {'slug': slug, 'industry': 'electromagnetism', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('coil-torque', build('coil-torque', [
        "Magnetic torque from turns, current, area, and field",
        "Enter turns N, current I, area A, flux density B, and angle \u03b8 to find magnetic torque.",
        "Coil Magnetic Torque Calculator",
        "/ Coil Magnetic Torque Calculator",
        'View "Magnetic torque from turns, current, area, and field" guide',
        "Deep dive: Coil torque",
        "DC motor: the armature coil rotates under torque in a magnetic field.",
        "Galvanometer: pointer deflection measures current.",
        "Loudspeaker: the voice coil is driven by Ampere force in a field.",
        "Torque sensor: measures Earth's field or magnetic dipole moment.",
        "When does \u03c4 reach its maximum?",
        "At \u03b8 = 90\u00b0 (coil plane parallel to field) sin\u03b8 = 1, \u03c4 = N\u00b7I\u00b7A\u00b7B; at \u03b8 = 0\u00b0 or 180\u00b0 \u03c4 = 0.",
        "How is motor starting torque calculated?",
        "\u03c4 = N\u00b7I\u00b7A\u00b7B\u00b7sin\u03b8; larger I gives larger torque, so high starting current yields high starting torque.",
        "What is the relation between magnetic moment \u03bc = NIA and \u03c4 = \u03bcB?",
        DISCL,
    ]))
    write('current-density', build('current-density', [
        "Current density from current and cross-section",
        "Enter current I and conductor cross-section A to find current density.",
        "Current Density Calculator",
        "/ Current Density Calculator",
        'View "Current density from current and cross-section" guide',
        "Deep dive: Current density",
        "PCB trace ampacity: 1 oz copper, 1 mm wide, 10 \u2103 rise, about 1 A continuous.",
        "Busbar selection: copper busbars in HV switchgear run at 1\u20133 A/mm\u00b2.",
        "Li-ion tabs: locally high current density causes heating failure.",
        "Motor windings: current density sets temperature rise and insulation life.",
        "I = 10 A, cross-section 2 mm\u00b2",
        "J = 10/2e-6 = 5\u00d710\u2076 A/m\u00b2 = 5 A/mm\u00b2; copper busbars should stay \u2264 3 A/mm\u00b2 (natural cooling).",
        "What are the effects of high current density?",
        "Joule heat P = I\u00b2R = J\u00b2\u00b7\u03c1\u00b7V; volumetric heating scales with J\u00b2, raising temperature and accelerating insulation aging.",
        "Why does high-frequency current concentrate on the surface?",
        "Skin effect: AC crowds into a thin surface layer (skin depth \u03b4 = \u221a(2\u03c1/(\u03c9\u03bc))); for copper at 1 MHz \u03b4 \u2248 66 \u00b5m.",
        "How to reduce current density?",
        DISCL,
    ]))
    write('drift-velocity', build('drift-velocity', [
        "Drift velocity from current and material parameters",
        "Enter current I, carrier density n, and cross-section A to find drift velocity.",
        "Electron Drift Velocity Calculator",
        "/ Electron Drift Velocity Calculator",
        'View "Drift velocity from current and material parameters" guide',
        "v_d = I/(n\u00b7A\u00b7e), copper n \u2248 8.5\u00d710\u00b2\u2078. In copper wire v_d is tiny (order of 10\u207b\u2074 m/s).",
        "Carrier density n (m\u207b\u00b3)",
        "v_d = I/(n\u00b7A\u00b7e), copper n \u2248 8.5\u00d710\u00b2\u2078.",
        "In copper wire v_d is tiny (order of 10\u207b\u2074 m/s).",
        "Deep dive: Drift velocity",
        "Semiconductor physics: understand the gap between conduction and microscopic carrier motion.",
        "Electromigration: prolonged high",
        "current density",
        "drives metal-atom migration that causes open circuits.",
        "PCB trace electromigration: high temperature and density accelerate failure.",
        "Plasma physics: electron and ion drift-velocity differences.",
        "Copper wire, 1 A, cross-section 1 mm\u00b2",
        "n \u2248 8.5\u00d710\u00b2\u2078 /m\u00b3; v = 1/(8.5e28\u00b71.6e-19\u00b71e-6) \u2248 0.07 mm/s; the signal itself travels at light speed.",
        "Why does the electrical signal travel near light speed?",
        DISCL,
        "Why does electromigration cause open circuits?",
        "Electrons transfer momentum to metal atoms, which migrate toward the anode forming voids (hillocks); sustained high current density accelerates failure.",
        "How does n relate to temperature?",
        DISCL,
    ]))
    write('electric-potential-point', build('electric-potential-point', [
        "Electric potential from a point charge and distance",
        "Enter point charge q and distance r to find electric potential.",
        "Point Charge Potential Calculator",
        "/ Point Charge Potential Calculator",
        'View "Electric potential from a point charge and distance" guide',
        "V = k\u00b7q/r (reference at infinity = 0). q = 1 \u00b5C, r = 1 m \u2192 8.99\u00d710\u00b3 V.",
        "V = k\u00b7q/r (reference at infinity = 0).",
        "Deep dive: Point-charge potential",
        "Charged conductor potential: for a sphere V = Q/(4\u03c0\u03b5\u2080R).",
        "Battery voltage: a chemical potential difference from electrochemical reaction.",
        "Scope probe: high impedance measures node potential.",
        "Lightning-rod design: tip corona potential under high field.",
        "V = 9e9\u00b71e-6/0.1 = 9\u00d710\u2074 V = 90 kV, near transmission-voltage level.",
        "What is the relation between potential and field strength?",
        "V is a scalar and E is a vector; E = -dV/dr (potential drops fastest along the field).",
        "Why take potential zero at infinity?",
        "A mathematical convention for normalizing finite-charge potential; in practice Earth or a reference point is taken as zero.",
        "What is an equipotential surface?",
        DISCL,
    ]))
    write('electric-power', build('electric-power', [
        "Electric power (P = V\u00b7I = V\u00b2/R = I\u00b2R)",
        "Find electric power from voltage and current.",
        "/ Electric Power",
        "Electric Power",
        'View "Electric power (P = V\u00b7I = V\u00b2/R = I\u00b2R)" guide',
        "P = V\u00b7I; also V\u00b2/R or I\u00b2R.",
        "12 V and 2 A gives 24 W.",
        "Deep dive: Electric power",
        "Household appliances: 220 V \u00d7 10 A = 2200 W = 2.2 kW.",
        "Resistive heating: P = V\u00b2/R; a \u00b110% voltage swing changes power by \u00b121%.",
        "Battery power: P = V\u00b7I; an EV at 400 V \u00d7 200 A = 80 kW.",
        "LED drive: constant-current power P = Vf\u00b7If.",
        "220 V, 100 \u03a9 resistor",
        "P = 220\u00b2/100 = 484 W; I = 2.2 A; half-hour consumption 242 Wh = 0.24 kWh.",
        "Three-phase power",
        "How does it differ from single-phase?",
        "Three-phase P = \u221a3\u00b7U_line\u00b7I_line\u00b7cos\u03c6 (line voltage, line current); single-phase P = U\u00b7I\u00b7cos\u03c6.",
        "What is the relation between apparent power S and active power P?",
        "P = S\u00b7cos\u03c6; at cos\u03c6 = 1, P = S (purely resistive); at cos\u03c6 < 1 there is reactive power.",
        "Electric power",
        "1 kW = 1000 W; 1 kWh (unit) = 1 kW\u00b7h = 3.6\u00d710\u2076 J.",
    ]))

if __name__ == "__main__":
    main()

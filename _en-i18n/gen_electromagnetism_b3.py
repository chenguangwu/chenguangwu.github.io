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
    write('energy-capacitor', build('energy-capacitor', [
        "Stored energy from capacitance and voltage",
        "Enter capacitance C (farads) and voltage V to find electric-field energy.",
        "Capacitor Energy Calculator",
        "/ Capacitor Energy Calculator",
        'View "Stored energy from capacitance and voltage" guide',
        "Capacitance C (F)",
        "Deep dive: Capacitor energy",
        "Flash / camera: a high-voltage capacitor releases stored energy instantly to fire.",
        "Defibrillator: about 360 J stored, the shock restores heart rhythm.",
        "Railgun: pulse capacitors release energy instantly to accelerate a projectile.",
        "PV inverter DC-Link: stored energy stabilizes voltage.",
        "W = 0.5\u00d71e-3\u00d7160000 = 80 J; can strike an arc instantly or drive a small railgun.",
        "Why can capacitor energy deliver instant high power?",
        DISCL,
        "How large is the charging current?",
        DISCL,
        "Can a capacitor replace a battery?",
        "A supercapacitor can replace a battery briefly (e.g., car start-stop);",
        DISCL,
    ]))
    write('energy-inductor', build('energy-inductor', [
        "Stored energy from inductance and current",
        "Enter inductance L (henries) and current I to find magnetic-field energy.",
        "Inductor Energy Calculator",
        "/ Inductor Energy Calculator",
        'View "Stored energy from inductance and current" guide',
        "Deep dive: Inductor energy",
        "Switched-mode power supply: the inductor sustains current during switching.",
        "Inductive ignition: field energy releases instantly into a high-voltage arc.",
        "Maglev: superconducting coils store energy to sustain levitation.",
        "Induction heating: an alternating field induces eddy currents that heat metal.",
        "W = 0.5\u00d70.01\u00d725 = 0.125 J; if the switch opens without a freewheel diode, the inductive voltage L\u00b7dI/dt can reach kV level.",
        "Why is opening an inductor dangerous?",
        DISCL,
        "Why add a freewheel diode?",
        DISCL,
        "How does a superconducting coil store energy long term?",
        DISCL,
        "How to use stored energy from inductance and current",
        "Inductor energy is used for SMPS ripple suppression, demagnetizing inductive loads with freewheel current, maglev superconducting-coil storage, and electromagnetic launch devices.",
        "What does stored energy from inductance and current do?",
        "Inductor energy calculator: enter L and I to compute magnetic-field energy via E = \u00bdLI\u00b2, for inductor energy evaluation.",
        "How do you use stored energy from inductance and current?",
        "Which scenarios suit stored energy from inductance and current?",
        "Inductor energy E = \u00bd\u00b7L\u00b7I\u00b2: the energy stored in the magnetic field when current I flows through inductance L.",
        "E in joules (J), L in henries (H), I in amperes (A). Energy grows with the square of current; on power-off it releases through a diode or resistor.",
    ]))
    write('faraday-induction', build('faraday-induction', [
        "Induced EMF (\u03b5 = N\u00b7|\u0394\u03a6| / \u0394t)",
        "The rate of magnetic-flux change in a coil produces an induced EMF.",
        "Faraday's Electromagnetic Induction Calculator",
        "/ Faraday's Electromagnetic Induction",
        "Faraday's Electromagnetic Induction",
        'View "Induced EMF (\u03b5 = N\u00b7|\u0394\u03a6| / \u0394t)" guide',
        "\u03b5 = N\u00b7|\u0394\u03a6|/\u0394t (Faraday's law). 100 turns, 0.001 Wb over 0.1 s gives 1 V.",
        "Turns",
        "Flux change (Wb)",
        "Time interval (s)",
        "\u03b5 = N\u00b7|\u0394\u03a6|/\u0394t (Faraday's law).",
        "100 turns, 0.001 Wb over 0.1 s gives 1 V.",
        "Deep dive: Faraday's electromagnetic induction",
        "Generator: a rotating coil in a field produces AC.",
        "Wireless charging: changing current in the transmitter coil induces current in the receiver coil.",
        "Induction heating: eddy currents heat the metal.",
        "Transformer: changing primary current induces voltage in the secondary.",
        "\u03b5 = 200\u00d70.01/0.1 = 20 V; increasing flux by 0.01 Wb in 100 ms produces 20 V.",
        "How to determine direction by Lenz's law?",
        DISCL,
        "Why must a transformer use AC?",
        DISCL,
        "How does electromagnetic induction differ from electrostatic induction?",
        DISCL,
    ]))
    write('force-wire-field', build('force-wire-field', [
        "Ampere force from field, current, and length",
        "Enter flux density B, current I, wire length L, and angle \u03b8 to find the Ampere force.",
        "Current-Carrying Wire Force Calculator",
        "/ Current-Carrying Wire Force Calculator",
        'View "Ampere force from field, current, and length" guide',
        "F = BIL\u00b7sin\u03b8, maximal when perpendicular. B = 0.5 T, I = 10 A, L = 0.2 m, \u03b8 = 90\u00b0 \u2192 1 N.",
        "Wire length L (m)",
        "F = BIL\u00b7sin\u03b8, maximal when perpendicular.",
        "Deep dive: Force on a current-carrying wire",
        "DC motor: the armature is driven by the force.",
        "Loudspeaker: the voice coil pushes the diaphragm.",
        "Magnetic damper: a conductor moving in a field feels eddy-current damping.",
        "Railgun: superconducting-coil fields accelerate the projectile.",
        "F = 0.5\u00d72\u00d70.2\u00d71 = 0.2 N; thumb = field, fingers = current, palm = force.",
        "How to use the left-hand rule?",
        DISCL,
        "How do two parallel wires interact?",
        "Same-direction currents attract, opposite repel; F/L = \u03bc\u2080I\u2081I\u2082/(2\u03c0d).",
        "What is the relation between Lorentz force and Ampere force?",
        DISCL,
    ]))
    write('free-space-impedance', build('free-space-impedance', [
        "Vacuum electromagnetic wave impedance",
        "From vacuum permeability and permittivity, find the free-space wave impedance.",
        "Free-Space Impedance Calculator",
        "/ Free-Space Impedance Calculator",
        'View "Vacuum electromagnetic wave impedance" guide',
        "(no input required)",
        "Free space is about 377 \u03a9.",
        "Deep dive: Free-space impedance",
        "Antenna matching: how 50 \u03a9 / 75 \u03a9 systems radiate into Z\u2080 = 377 \u03a9 free space.",
        "Satellite links: free-space path loss FSPL relates to Z\u2080.",
        "Microwave transmission: waveguide characteristic impedance is set by geometry.",
        "EMC testing: radiated-emission field-strength calculations.",
        "Z\u2080 \u2248 376.7 \u03a9; a half-wave dipole's theoretical impedance \u2248 73 \u03a9, matched to a 50 \u03a9 system via a balun.",
        "Does Z\u2080 depend on frequency?",
        DISCL,
        "Why is 50 \u03a9 common in RF rather than 377 \u03a9?",
        DISCL,
        "Where does the FSPL formula come from?",
        DISCL,
    ]))

if __name__ == "__main__":
    main()

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
    write('b-field-wire', build('b-field-wire', [
        "Ampere's Law (B = \u03bc\u2080\u00b7I / (2\u03c0\u00b7r))",
        "Magnetic field around an infinitely long straight wire.",
        "Magnetic Field of a Straight Wire Calculator",
        "/ Straight Wire Magnetic Field",
        "Straight Wire Magnetic Field",
        'View "Ampere\'s Law (B = \u03bc\u2080\u00b7I / (2\u03c0\u00b7r))" guide',
        "At 10 A and 1 cm away, about 2\u00d710\u207b\u2074 T.",
        "Deep dive: Magnetic field of a straight wire",
        "Estimate busbar field: at 1 m from a 1000 A busbar, the power-frequency field is about 2 mT.",
        "Lab HV-line magnetic deflection: keep CRTs and oscilloscopes away from 50 Hz fields.",
        "EMC design: estimate magnetic interference from power lines on nearby sensitive instruments.",
        "Magnetic sensor calibration: use a wire with known current to calibrate Hall probes.",
        "10 A infinite straight wire, r = 0.05 m",
        "B = 4\u03c0\u00d710\u207b\u2077\u00d710/(2\u03c0\u00b70.05) = 4\u00d710\u207b\u2075 T = 40 \u00b5T, comparable to Earth's field of 50 \u00b5T.",
        "Why is B inversely proportional to r?",
        DISCL,
        "How to compute a finite-length wire?",
        DISCL,
        "Where is \u03bc\u2080 = 4\u03c0\u00d710\u207b\u2077 H/m used?",
        DISCL,
    ]))
    write('capacitance-parallel-plate', build('capacitance-parallel-plate', [
        "Capacitance from plate area and spacing",
        "Enter relative permittivity \u03b5r, plate area A, and spacing d to find capacitance.",
        "Parallel Plate Capacitor Calculator",
        "/ Parallel Plate Capacitor Calculator",
        'View "Capacitance from plate area and spacing" guide',
        "Relative permittivity \u03b5r",
        "Plate area A (m\u00b2)",
        "Deep dive: Parallel plate capacitance",
        "PCB planar capacitance: the dielectric layer between double-sided copper forms a tiny high-frequency decoupling capacitance.",
        "Touch keys: the sensing pad under the glass and ground form a variable capacitor.",
        "High voltage",
        "Voltage divider",
        "Multi-stage",
        "Capacitor series",
        "voltage division.",
        "Dielectric characterization: measure C to infer \u03b5r.",
        "10\u00d710 cm copper plates, d = 1 mm, air",
        "C = 8.85e-12\u00d71\u00d70.01/(1e-3) = 8.85e-11 F \u2248 88.5 pF; add a polyimide film (\u03b5r = 3.5) \u2192 310 pF.",
        "When should edge effects be corrected?",
        DISCL,
        "Is a larger \u03b5r always better?",
        DISCL,
        "Why does C change after applying voltage?",
        DISCL,
    ]))
    write('capacitive-reactance', build('capacitive-reactance', [
        "Capacitive reactance (X_C = 1 / (2\u03c0\u00b7f\u00b7C))",
        "A capacitor's opposition to AC decreases as frequency rises.",
        "Capacitive Reactance Calculator",
        "/ Capacitive Reactance",
        "Capacitive Reactance",
        'View "Capacitive reactance (X_C = 1 / (2\u03c0\u00b7f\u00b7C))" guide',
        "X_C = 1/(2\u03c0fC); reactance decreases as frequency rises.",
        "At 60 Hz and 1 \u00b5F, about 2653 \u03a9.",
        "Deep dive: Capacitive reactance",
        "Power EMI filtering: X-class (across-line) and Y-class (common-mode) capacitors.",
        "Audio crossover: high-pass / low-pass filter design.",
        "Ballast / fluorescent lamps: reactance limits current in place of an inductor.",
        "Find the capacitance needed to correct to target cos\u03c6.",
        "Xc = 1/(2\u03c0\u00b750\u00b710e-6) \u2248 318 \u03a9; for the same capacitor at f = 1 kHz Xc = 15.9 \u03a9, at 10 kHz Xc = 1.59 \u03a9.",
        "How does reactance vary with frequency?",
        DISCL,
        "How does reactance differ from resistance?",
        DISCL,
        "Why do real capacitors have ESR?",
        DISCL,
    ]))
    write('capacitors-parallel', build('capacitors-parallel', [
        "Parallel equivalent (C = C\u2081 + C\u2082)",
        "The sum of parallel capacitors is the equivalent capacitance.",
        "Capacitors in Parallel Calculator",
        "/ Capacitors in Parallel",
        "Capacitors in Parallel",
        'View "Parallel equivalent (C = C\u2081 + C\u2082)" guide',
        "Deep dive: Capacitors in parallel",
        "Energy banks: parallel capacitors raise stored energy.",
        "Decoupling: multiple capacitors in parallel at a chip's VCC pin (different bands).",
        "Power filtering: parallel low-ESR large capacitors reduce ripple.",
        "Motor start: a parallel start capacitor boosts starting torque.",
        "C1 = 10 \u00b5F, C2 = 22 \u00b5F, C3 = 47 \u00b5F in parallel",
        "C = 10 + 22 + 47 = 79 \u00b5F; voltage rating is the lowest of the three; add 100 nF for high-frequency decoupling.",
        "How is the parallel voltage rating determined?",
        "Take the smallest: if 16 V + 25 V + 50 V are in parallel, the overall rating is only 16 V.",
        "How does ESR change after paralleling?",
        "ESR in parallel is like",
        "resistors in parallel",
        ": 1/R_total = \u03a3 1/Ri, which significantly lowers equivalent resistance and improves ripple.",
        "Why use different capacitors for multi-band decoupling?",
        DISCL,
    ]))
    write('capacitors-series', build('capacitors-series', [
        "Series equivalent (1/C = 1/C\u2081 + 1/C\u2082)",
        "Series capacitors reduce total capacitance.",
        "Capacitors in Series Calculator",
        "/ Capacitors in Series",
        "Capacitors in Series",
        'View "Series equivalent (1/C = 1/C\u2081 + 1/C\u2082)" guide',
        "Two 2 \u00b5F in series = 1 \u00b5F.",
        "Deep dive: Capacitors in series",
        "High-voltage capacitive divider: measure high-voltage AC (e.g., resistive-capacitive",
        "voltage divider",
        "High-voltage energy storage: a Marx generator stacks series capacitors into high-voltage pulses.",
        "DC-blocking capacitor: series blocks DC but passes AC.",
        "Coupling capacitor: blocks DC between stages.",
        "C1 = 10 \u00b5F, C2 = 10 \u00b5F in series",
        "C = 5 \u00b5F; voltage ratings add (e.g., 25 V + 25 V \u2192 50 V); charge is equal: Q = C\u2081V\u2081 = C\u2082V\u2082.",
        "Do series capacitors divide voltage equally?",
        "Equal capacitors share voltage equally; unequal ones put higher voltage on the smaller capacitor (Q equal, V = Q/C), risking breakdown.",
        "Why add parallel balancing resistors in series?",
        "Real capacitors differ greatly in leakage; over time the one with lower leakage takes more voltage, so add balancing resistors (hundreds of k\u03a9 to M\u03a9).",
        "Why is the series equivalent smaller than the smallest capacitor?",
        DISCL,
    ]))

if __name__ == "__main__":
    main()

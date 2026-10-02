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
    write('ohms-law', build('ohms-law', [
        "\u26a1 Ohm's Law",
        "V = I \u00d7 R and its variants",
        'View "Ohm\'s Law (V = I\u00b7R)" guide',
        "Given any two quantities, find the rest and the power.",
        "Solve for",
        "\U0001F447 Select the quantity to solve",
        "Deep dive: Ohm's Law",
        "Circuit analysis",
        "Fundamentals: both nodal voltage and mesh current rely on it",
        "Fuse selection: the fusing current is set by I\u00b2R heating.",
        "Voltage sampling divider: read V via a high-resistance divider.",
        "Current-limiting resistor: series limit protects LED/chips.",
        "I = 12/100 = 0.12 A = 120 mA; P = 12\u00d70.12 = 1.44 W; pick a 100 \u03a9 2 W resistor.",
        "Does Ohm's law apply to all devices?",
        DISCL,
        "How is Ohm's law used under AC?",
        DISCL,
        "What are some nonlinear resistors?",
        DISCL,
        'About "Ohm\'s Law"',
        DISCL,
    ]))
    write('resistivity-law', build('resistivity-law', [
        "Resistance from resistivity, length, and area",
        "Enter resistivity \u03c1, length L, and area A to find conductor resistance.",
        "Resistance Law Calculator",
        "/ Resistance Law Calculator",
        'View "Resistance from resistivity, length, and area" guide',
        "R = \u03c1L/A. Copper (\u03c1 = 1.68e-8), L = 1 m, A = 1 mm\u00b2 \u2192 0.0168 \u03a9.",
        "Resistivity \u03c1 (\u03a9\u00b7m)",
        "Copper (\u03c1 = 1.68e-8), L = 1 m, A = 1 mm\u00b2 \u2192 0.0168 \u03a9.",
        "Deep dive: Resistivity law",
        "Wire resistance",
        ": 100 m copper core 1.5 mm\u00b2, R \u2248 1.15 \u03a9.",
        "PCB trace resistance: 1 oz copper, 1 mm wide, 100 mm long, R \u2248 0.5 \u03a9.",
        "Grounding resistance: electrode material and soil",
        "resistivity",
        "determines it.",
        "Precision resistors: manganin/constantan have low temperature coefficient.",
        "Copper \u03c1 = 1.724e-8 \u03a9\u00b7m, L = 1 m, A = 1 mm\u00b2",
        "R = 1.724e-8\u00d71/1e-6 = 0.0172 \u03a9; 100 m of the same \u2248 1.72 \u03a9.",
        "How does resistivity relate to temperature?",
        DISCL,
        "What about superconducting resistivity?",
        DISCL,
        "How does skin effect affect it?",
        DISCL,
    ]))
    write('resistors-parallel', build('resistors-parallel', [
        "Parallel equivalent (1/R = 1/R\u2081 + 1/R\u2082)",
        "Parallel resistors sum their conductances.",
        "Resistors in Parallel Calculator",
        "/ Resistors in Parallel",
        "Resistors in Parallel",
        'View "Parallel equivalent (1/R = 1/R\u2081 + 1/R\u2082)" guide',
        "Two 10 \u03a9 in parallel = 5 \u03a9.",
        "Deep dive: Resistors in parallel",
        "Shunt: a large resistor in parallel with a small one lowers total resistance.",
        "Current sensing: a small resistor in parallel with the meter extends its range.",
        "Pull-up / pull-down: parallel resistors set logic levels.",
        "Power sharing: multiple resistors in parallel reduce each one's power.",
        "R1 = 100 \u03a9, R2 = 200 \u03a9 in parallel",
        "R = 100\u00d7200/300 \u2248 66.7 \u03a9; current splits I\u2081/I\u2082 = R\u2082/R\u2081 = 2:1.",
        "Why is parallel resistance smaller than the smallest?",
        DISCL,
        "How does power distribution relate to resistance?",
        DISCL,
        "Why should an ammeter have minimal internal resistance?",
        DISCL,
    ]))
    write('resistors-series', build('resistors-series', [
        "Series equivalent (R = R\u2081 + R\u2082 + R\u2083)",
        "The sum of series resistors is the equivalent.",
        "Resistors in Series Calculator",
        "/ Resistors in Series",
        "Resistors in Series",
        'View "Series equivalent (R = R\u2081 + R\u2082 + R\u2083)" guide',
        "Resistor R\u2083 (\u03a9)",
        "Deep dive: Resistors in series",
        "Current-limiting resistor: series limits LED/transistor current.",
        "Voltage divider",
        ": high-resistance series with a tap takes voltage.",
        "Source internal resistance: battery/supply resistance is in series with the load.",
        "Fuse resistance: fusing protection.",
        "R1 = 1 k\u03a9, R2 = 2 k\u03a9 in series, V = 12 V",
        "Series voltage division and power?",
        DISCL,
        "Why choose different power ratings in series?",
        DISCL,
        "Why should a voltmeter have high internal resistance?",
        DISCL,
    ]))
    write('rl-time-constant', build('rl-time-constant', [
        "Time constant from inductance and resistance",
        "Enter inductance L and resistance R to find the RL circuit time constant.",
        "RL Time Constant Calculator",
        "/ RL Time Constant Calculator",
        'View "Time constant from inductance and resistance" guide',
        "Deep dive: RL time constant",
        "Relay demagnetization: the coil produces an inductive spike at power-off.",
        "SMPS inductor: sets ripple and response speed.",
        "Motor start: inductance integrates and delays current rise.",
        "DC filtering: the L/R time constant affects transient response.",
        "\u03c4 = 0.01/100 = 100 \u00b5s; at 5\u03c4 = 500 \u00b5s current reaches about 99% of final; typical SMPS switching period 10 \u00b5s to 1 ms.",
        "Why is there high voltage across an inductor at power-off?",
        DISCL,
        "How does \u03c4 differ from the RC time constant?",
        DISCL,
        "How to design inductor reverse-spike protection?",
        DISCL,
    ]))

if __name__ == "__main__":
    main()

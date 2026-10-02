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
    write('inductance-solenoid', build('inductance-solenoid', [
        "Inductance from turns, area, and length",
        "Enter turns N, cross-section A, and length l to find solenoid inductance.",
        "Solenoid Inductance Calculator",
        "/ Solenoid Inductance Calculator",
        'View "Inductance from turns, area, and length" guide',
        "Length l (m)",
        "Deep dive: Solenoid inductance",
        "Air-core coil: RF choke, electromagnet.",
        "Core inductor: adding a ferrite core with \u03bc\u1d63 multiplies L.",
        "Transformer design: primary-secondary coupling sets the ratio.",
        "Resonant circuit: LC resonance selects frequency.",
        "N = 1000, A = 1 cm\u00b2, l = 10 cm, air core",
        "L = 4\u03c0\u00d710\u207b\u2077\u00d710\u2076\u00d710\u207b\u2074/0.1 \u2248 12.6 mH; with \u03bc\u1d63 = 100 core \u2192 1.26 H.",
        "How to correct a short solenoid when l \u226a R?",
        DISCL,
        "Why does an iron core greatly increase inductance?",
        DISCL,
        "How large is the unit henry?",
        DISCL,
    ]))
    write('inductors-parallel', build('inductors-parallel', [
        "Parallel equivalent (1/L = 1/L\u2081 + 1/L\u2082)",
        "Parallel inductors reduce total inductance.",
        "Inductors in Parallel Calculator",
        "/ Inductors in Parallel",
        "Inductors in Parallel",
        'View "Parallel equivalent (1/L = 1/L\u2081 + 1/L\u2082)" guide',
        "Two 2 mH in parallel = 1 mH.",
        "Deep dive: Inductors in parallel",
        "Power sharing: two parallel inductors share current.",
        "EMI suppression: high and low inductors in parallel cover a wide band.",
        "Resonant circuit: parallel LC resonance (analogous to",
        "resistors in parallel",
        ").",
        "Inductance precision: paralleling small inductors for fine adjustment.",
        "L1 = 10 mH, L2 = 10 mH in parallel",
        "L = 5 mH (mutual inductance ignored); in practice coupling shifts L.",
        "Why is parallel inductance error-prone?",
        DISCL,
        "How is current shared in parallel inductors?",
        DISCL,
        "Does parallel inductance change the voltage rating?",
        DISCL,
    ]))
    write('inductors-series', build('inductors-series', [
        "Series equivalent (L = L\u2081 + L\u2082)",
        "The sum of series inductors is the equivalent (mutual ignored).",
        "Inductors in Series Calculator",
        "/ Inductors in Series",
        "Inductors in Series",
        'View "Series equivalent (L = L\u2081 + L\u2082)" guide',
        "L_eq = L\u2081 + L\u2082 (no mutual inductance).",
        "Deep dive: Inductors in series",
        "Multi-winding transformer: primary-secondary leakage inductance adds up.",
        "Motor windings: multiple pole coils in series form poles.",
        "Power inductor: low DCR, large L often uses multiple coils in series.",
        "Decoupling inductor: series reduces ripple.",
        "L1 = 10 mH, L2 = 20 mH in series (no mutual)",
        "L = 30 mH; wound same-direction on a core, L \u2248 \u221a(L\u2081\u00b2+L\u2082\u00b2+2k\u221aL\u2081L\u2082) with coupling k \u2248 0.9.",
        "How to determine mutual-inductance direction?",
        "Aiding flux (series-aiding) gives L = L\u2081+L\u2082+2M; opposing flux (series-opposing) gives L = L\u2081+L\u2082-2M.",
        "Does series inductance change the voltage rating?",
        "Yes, series voltage ratings add (e.g., 50 V + 50 V = 100 V), but current capability is the smallest.",
        "Why must a power-filter inductor have low DCR?",
        DISCL,
    ]))
    write('lc-resonance', build('lc-resonance', [
        "Resonant frequency (f = 1 / (2\u03c0\u00b7\u221a(L\u00b7C)))",
        "The natural resonant frequency of a lossless LC circuit.",
        "LC Resonant Frequency Calculator",
        "/ LC Resonant Frequency",
        "LC Resonant Frequency",
        'View "Resonant frequency (f = 1 / (2\u03c0\u00b7\u221a(L\u00b7C)))" guide',
        "Inductance (mH)",
        "At 1 mH and 1 \u00b5F, about 5033 Hz.",
        "Deep dive: LC resonance",
        "Radio tuning: a variable capacitor selects frequency.",
        "Wireless charging: 13.56 MHz resonant coupling.",
        "RFID tags: LC resonance for readout.",
        "Notch filter: very low impedance at a point rejects interference.",
        "f = 1/(2\u03c0\u221a(100e-6\u00b7100e-12)) \u2248 1.59 MHz; at R = 10 \u03a9, Q = 100 and BW \u2248 16 kHz.",
        "How does Q affect frequency selection?",
        DISCL,
        "Why does the real resonance deviate from the calculation?",
        DISCL,
        "Crystal oscillator vs LC resonance?",
        DISCL,
    ]))
    write('magnetic-flux', build('magnetic-flux', [
        "Magnetic flux (\u03a6 = B\u00b7A)",
        "Flux through an area perpendicular to a uniform field.",
        "Magnetic Flux Calculator",
        "/ Magnetic Flux",
        "Magnetic Flux",
        'View "Magnetic flux (\u03a6 = B\u00b7A)" guide',
        "Magnetic flux density (T)",
        "\u03a6 = B\u00b7A (B perpendicular to A).",
        "At 1 mT and 0.01 m\u00b2, \u03a6 = 1\u00d710\u207b\u2075 Wb.",
        "Deep dive: Magnetic flux",
        "Magnetic circuit design: core flux sets the cross-section.",
        "Generator: flux per pole sets the rated voltage.",
        "Hall sensor: measure \u03a6 to infer B.",
        "Magnetic shielding: low-flux-density design.",
        "B = 1 T, A = 0.01 m\u00b2, perpendicular",
        "\u03a6 = 1\u00d70.01 = 0.01 Wb; typical per-pole flux of a 50 Hz generator.",
        "Magnetic flux density B and",
        "magnetic field strength",
        "H: what is the difference?",
        DISCL,
        "What is the flux continuity principle?",
        DISCL,
        "What is magnetic saturation?",
        DISCL,
        "How to use magnetic flux (\u03a6 = B\u00b7A)",
        "Flux is used for motor/generator stator magnetic-circuit design, transformer core cross-section selection, Hall-sensor field measurement, magnetic shielding, and magnetic-circuit simulation.",
        "What does magnetic flux (\u03a6 = B\u00b7A) do?",
        "Magnetic flux calculator: enter flux density B and perpendicular area A (and angle) to compute \u03a6 = B\u00b7A\u00b7cos\u03b8 through a loop, for motor/transformer flux estimates and teaching Faraday's law.",
        "How do you use magnetic flux (\u03a6 = B\u00b7A)?",
        "Which scenarios suit magnetic flux (\u03a6 = B\u00b7A)?",
        "Flux \u03a6 = B\u00b7A\u00b7cos\u03b8: total field lines perpendicular through area A, where \u03b8 is the angle between field and surface normal.",
        "\u03a6 in webers (Wb); B in tesla (T), A in square meters (m\u00b2). The flux rate of change sets the induced EMF (Faraday's law).",
    ]))

if __name__ == "__main__":
    main()

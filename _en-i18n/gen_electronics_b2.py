#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'electronics')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'electronics')
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
    out = {'slug': slug, 'industry': 'electronics', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
#!/usr/bin/env python3

DISCL_E = " This is a basic electronics calculation aid; results are for circuit design and teaching reference only and do not replace formal PCB design, EMC and product reliability requirements."


def main():
    write('calc-frequency', build('calc-frequency', [
        "\U0001F4E1 Inductive reactance against frequency",
        "Enter the inductance and frequency to compute the inductive reactance XL.",
        "\U0001F4D6 View the inductive reactance usage guide",
        "Inductive reactance XL = 2\u03C0 \u00D7 f \u00D7 L, with L in henries (1 \u03BCH = 10\u207B\u2076 H). For example a 100 \u03BCH inductor gives XL \u2248 0.628 \u03A9 at 1 kHz and \u2248 6.28 \u03A9 at 10 kHz, proportional to frequency. Inductive and capacitive reactance have opposite directions (XC = 1 \u00F7 (2\u03C0fC)), and in series resonance XL equals XC at f\u2080 = 1 \u00F7 (2\u03C0\u221A(LC)).",
        "Inductance (\u03BCH)",
        "\U0001F4A1 XL = 2\u03C0 \u00D7 f \u00D7 L, converting L to henries (H)",
        "Inductive reactance grows linearly with frequency",
        "A pure inductor consumes no real power",
        "\U0001F4DA In-depth analysis: inductive reactance against frequency",
        "EMC filtering: class X and class Y power-line capacitors work with inductors to suppress conducted interference.",
        "RF matching: LC matching networks between a 50\u03A9 network and the antenna.",
        "Audio crossovers: second and third order high-pass and low-pass filters.",
        "Regulation: boost inductor ripple current control.",
        "XL = 2\u03C0\u00B71000\u00B70.01 = 62.8\u03A9; at f = 100 Hz it is only 6.28\u03A9.",
        "How do inductive and capacitive reactance correspond?",
        "Inductive reactance rises with frequency (high-pass) while capacitive reactance falls with frequency (low-pass); XL and Xc are mirror images of each other." + DISCL_E,
        "How is the inductor Q value used?",
        "Q = XL/R determines selectivity. A high Q suits resonance and notch filters, a low Q suits wideband filtering." + DISCL_E,
        "How does inductor heating relate to reactance?",
        "Reactance has no direct relation to temperature rise; the rise is set by I\u00B2\u00B7ESR. A ferrite inductor loses saturation current at high temperature." + DISCL_E,
        "About the Inductive reactance against frequency",
        "The inductive reactance tool computes the reactance XL of an inductor from its inductance and operating frequency. It is a fundamental tool for AC circuit, filter and RF analysis.",
        "Automatic reactance calculation",
        "Real-time computation",
        "AC circuit impedance analysis",
        "RF circuit calculation",
        "Resonance frequency analysis",
        "Inductance (\u03BCH)",
    ]))

    write('calc-time-2', build('calc-time-2', [
        "\U0001F4E1 RC charge and discharge time constant",
        "Enter the resistance and capacitance to compute the time constant \u03C4 and the charge and discharge times at each stage.",
        "\U0001F4D6 View the RC time constant usage guide",
        "Time constant \u03C4 = R \u00D7 C (R in ohms, C in farads, 1 \u03B5F = 10\u207B\u2076 F). The charging voltage is v(t) = V \u00D7 (1 \u2212 e to the power of \u2212t/\u03C4), reaching 63.2% at 1\u03C4, 95% at 3\u03C4 and 99.3% at 5\u03C4, which is treated as fully charged. The cutoff frequency is fc = 1 \u00F7 (2\u03C0RC); for example with R = 10 k\u03A9 and C = 100 nF, \u03C4 = 1 ms and fc \u2248 159 Hz.",
        "Capacitance (\u03B5F)",
        "\U0001F4A1 \u03C4 = R \u00D7 C; 1\u03C4 charges to 63%, 3\u03C4 to 95%, 5\u03C4 to 99%; cutoff frequency fc = 1\u00F7(2\u03C0RC)",
        "Charging is regarded as complete after 5\u03C4 (99%)",
        "The larger \u03C4 is, the slower the charge and discharge",
        "\U0001F4DA In-depth analysis: RC charge and discharge time constant",
        "Timing circuits: NE555 monostable delay.",
        "Debounce circuits: RC filtering on a button input.",
        "Integration and differentiation: signal processing in circuits.",
        "Filters: low-pass and high-pass cutoff frequency setting.",
        "\u03C4 = 0.1 s; charging to 63% takes 0.1 s, to 95% takes 0.3 s and to 99% takes 0.5 s (5\u03C4).",
        "What is the 5\u03C4 rule?",
        "After 5\u03C4 the capacitor reaches 99.3% of the final value on charge or discharge; in real engineering 3\u03C4 (95%) is usually enough." + DISCL_E,
        "How does the cutoff frequency relate to the time constant?",
        "f-3dB = 1/(2\u03C0RC) = 1/(2\u03C0\u03C4); the larger \u03C4 is, the lower f is." + DISCL_E,
        "What is the charging current of an RC series circuit?",
        "I(t) = V/R\u00B7e^(\u2212t/\u03C4); the initial current is the largest (V/R) and then decays exponentially." + DISCL_E,
        "About the RC charge and discharge time constant",
        "The RC time constant tool computes the time constant \u03C4, the charge and discharge times at each stage and the cutoff frequency from the resistance and capacitance. It is a fundamental tool for circuit transient analysis and filter design.",
        "Automatic time constant calculation",
        "Multi-stage charge and discharge times",
        "Cutoff frequency included",
        "RC circuit transient analysis",
        "Delay circuit calculation",
        "Decoupling capacitor selection",
        "Resistance (\u03A9)",
        "Capacitance (\u03B5F)",
    ]))

    write('capacitance', build('capacitance', [
        "\u26A1 Crystal load capacitance matching",
        "Two equal capacitors in series plus the stray capacitance C_s give the standard value C that matches the target.",
        "\U0001F4D6 View the crystal load capacitance guide",
        "When C\u2081 = C\u2082 = C: C_L = C \u00F7 2 + C_s, so C = 2 \u00D7 (C_L \u2212 C_s)",
        "Enter the crystal load capacitance CL and the stray capacitance to compute the matching capacitors",
        "Crystal CL (pF)",
        "Stray capacitance (pF)",
        "\U0001F4A1 When C1 = C2 = C: CL = C\u00F72 + Cs, so C = 2\u00D7(CL \u2212 Cs)",
        "Stray capacitance includes lead and trace parasitics, roughly 3 to 7 pF",
        "C1 and C2 are usually taken equal",
        "Poor matching shifts the crystal frequency or prevents oscillation",
        "\U0001F4DA In-depth analysis: crystal load capacitance matching",
        "MCU clock: an 8 MHz crystal with CL = 20 pF and CS = 5 pF gives C1 = C2 = 30 pF (take the standard 27 pF or 33 pF).",
        "Real-time clock RTC: a 32.768 kHz crystal with CL = 12.5 pF gives C1 = C2 \u2248 15 pF.",
        "Bluetooth module: a 26 MHz crystal with CL = 10 pF gives C1 = C2 \u2248 10 pF.",
        "Ethernet PHY: 25 MHz with CL = 16 pF gives C1 = C2 \u2248 22 pF.",
        "C1 = C2 = 2\u00D7(20\u22125) = 30 pF; take the standard 27 pF (a smaller value shifts the crystal frequency slightly upward) or 33 pF.",
        "How is CS estimated?",
        "PCB traces, leads and the IC's internal capacitance; typically 2 to 8 pF. When CL is known, follow the datasheet recommendation." + DISCL_E,
        "How does capacitance tolerance affect frequency error?",
        "A 1 pF error in load capacitance gives a few ppm of frequency error; a high-precision RTC needs \u00B15% matching capacitors." + DISCL_E,
        "Why might the crystal fail to start?",
        "Capacitance too large, ESR too high, crystal load capacitance mismatched, or insufficient negative resistance. Check the application note." + DISCL_E,
        "About the Crystal load capacitance matching",
        "The crystal load capacitance matching tool computes the required external matching capacitors from the crystal's nominal load capacitance CL and the circuit stray capacitance, ensuring the crystal starts reliably and runs at its nominal frequency.",
        "Automatic matching capacitance calculation",
        "Recommended standard values",
        "Adjustable stray capacitance",
        "Microcontroller crystal circuit design",
        "Troubleshooting a crystal that will not start",
        "Frequency accuracy calibration",
        "PCB layout assessment",
        "Crystal CL (pF)",
        "Stray capacitance (pF)",
    ]))


if __name__ == '__main__':
    main()

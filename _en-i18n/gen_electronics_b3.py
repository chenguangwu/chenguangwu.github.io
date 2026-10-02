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
    write('capacitor-calculator', build('capacitor-calculator', [
        "\U0001F9EE Capacitance Calculator",
        "Series/parallel/charging/RC time constant",
        "Core formulas (by input): 1 / (2 \u00D7 \u03C0 \u00D7 tau); tau \u00D7 0.693; R \u00D7 C / 1e6",
        "Capacitance Calculation",
        " / Capacitance Calculation",
        "\U0001F4D6 See the \"Capacitance Calculator User Guide\"",
        "\U0001F4DA In-depth analysis: Capacitance Calculator",
        "Power filtering: 100\u03BCF/25V aluminium electrolytic + 100nF ceramic for high-frequency decoupling.",
        "High-frequency DC-DC: multiple MLCC/X7R in parallel to cut ESR and ripple.",
        "Energy storage: film capacitors handle high ripple current and long life.",
        "Sample and hold: polypropylene/polystyrene give low leakage and high stability.",
        "5V 100mA supply decoupling",
        "10\u03BCF MLCC + 100nF ceramic; self-resonance at roughly MHz, covering switching ripple and high-frequency noise.",
        "Does MLCC capacitance drop?",
        "X7R loses 50%~80% at high bias (e.g. 10\u03BCF rated at 1V only gives 4\u03BCF at 5V); C0G/NP0 stay stable but hold far less capacitance." + DISCL_E,
        "How is electrolytic capacitor life calculated?",
        "L=L0\u00B72^((T0-T)/10), halving the life for every 10\u00B0C drop; 105\u00B0C/3000h parts last 30 years after a 50\u00B0C derating." + DISCL_E,
        "Why decouple across multiple frequency bands?",
        "Capacitor ESL+ESR sets the self-resonance frequency; multiple values (10\u03BCF+100nF+10pF) cover a wide band." + DISCL_E,
        "About \"Capacitance Calculation\"",
        "Capacitance Calculation covers series/parallel equivalent capacitance, RC time constants and stored energy in one place, making it a handy aid for circuit design and capacitor selection; it runs entirely in the browser and uploads no data.",
    ]))

    write('circuit-calculator', build('circuit-calculator', [
        "\U0001F4CA Circuit Analysis Calculator",
        "RLC resonance/power/decibels/reactance",
        "Core formulas (by input): 10 \u00D7 Math.log10(val \u00D7 1000); 20 \u00D7 Math.log10(val); \u221A(max(0, S\u00D7S - P\u00D7P))",
        "Circuit Analysis",
        " / Circuit Analysis",
        "\U0001F4D6 See the \"Circuit Analysis Calculator User Guide\"",
        "\U0001F4DA In-depth analysis: Circuit Analysis Calculator",
        "RLC filtering: find the resonance point, bandwidth and impedance extremes.",
        "Resonant amplification: tuned circuits for frequency selection.",
        "Power distribution: transformer impedance matching.",
        "EMC filtering: insertion loss of \u03C0-type LC networks.",
        "R=50\u03A9 L=10\u03BCH C=100pF in series",
        "How do I use complex impedance Z=R+jX?",
        "R is the real part (resistance) and X the imaginary part (positive inductive, negative capacitive); sum them over the series-parallel network to get the total Z." + DISCL_E,
        "Impedance matching and power transfer?",
        "Maximum power transfer happens at conjugate matching (load = conjugate of the source impedance); antennas and power lines follow this rule." + DISCL_E,
        "How should the Q factor be chosen?",
        "Frequency-selective and resonant circuits need a high Q (narrow and sharp); power filtering and wideband uses need a low Q (wide band, less prone to resonance)." + DISCL_E,
        "About \"Circuit Analysis\"",
        "Circuit Analysis quickly solves series-parallel resistance, voltage division, Thevenin equivalents and other common circuit quantities, serving as a basic aid for electronic circuit design; it runs entirely in the browser and uploads no data.",
    ]))

    write('convert-capacitance', build('convert-capacitance', [
        "\U0001F4BB Capacitance (code/voltage) Conversion",
        "Capacitor EIA code \u2192 capacitance (3-digit: first 2 significant, 3rd is the power of 10; R marks the decimal point)",
        "\U0001F4D6 See the \"Capitance (code/voltage) Conversion User Guide\"",
        "Capacitor code conversion: a three-digit code abc means a b \u00D7 10^c pF (e.g. 104 = 10\u00D710^4 pF = 100 nF); in codes containing R, R is the decimal point (e.g. 4R7 = 4.7 pF); with 1 nF = 1000 pF, 1 \u00B5F = 10^6 pF and 1 F = 10^12 pF you can derive the \u00B15% and \u00B110% tolerance ranges.",
        "Capacitor code (e.g. 104 / 4R7)",
        "\U0001F4DA In-depth analysis: Capacitance (code/voltage) Conversion",
        "Reading codes: 104=10\u00D710\u2074pF=0.1\u03BCF; 472=47\u00D710\u00B2pF=4.7nF.",
        "Voltage derating: pick a rating \u22651.5\u00D7 the working voltage (switching spikes).",
        "Package mapping: 0402/0603/0805 sizes and their power handling.",
        "Decoding a 105 code",
        "105=10\u00D710\u2075 pF=1\u03BCF; widely used for supply decoupling; choose 6.3V/10V/16V by application.",
        "What does the third digit mean?",
        "The first two digits are",
        "significant figures;",
        " and the third is the power of ten (in pF); e.g. 475=4.7\u00D710\u2075pF=470nF." + DISCL_E,
        "Why derate the rated voltage of MLCCs?",
        "Capacitance falls under DC bias and temperature, especially in small high-voltage packages (0201/0402); leaving 50% headroom is advised." + DISCL_E,
        "Can a tantalum capacitor be fitted backwards?",
        "Never: reverse current causes failure or even ignition; the end marked with the bar is the positive terminal." + DISCL_E,
        "About \"Capitance (code/voltage) Conversion\"",
        "Capacitance (code/voltage) Conversion quickly converts between pF/nF/\u00B5F/mF/F units, EIA codes and voltage ratings, helping with part selection and code reading; it runs entirely in the browser and uploads no data.",
    ]))

    write('crystal-divider', build('crystal-divider', [
        "\U0001F9EE Crystal Divider Calculator",
        "Divider ratio and output frequency, with PLL multiplication/division",
        "Core formulas (by input): Math.round(tgt\u00F7xr); Math.round(ratio)",
        "\U0001F4D6 See the \"Crystal Divider Calculator User Guide\"",
        "Simple division",
        "PLL multiply/divide",
        "Solve for the divider",
        "Crystal frequency",
        "Divider ratio N",
        "Multiplier M",
        "Divider ratio N (pre)",
        "Output divider OD",
        "PLL output = crystal \u00F7 N \u00D7 M \u00F7 OD",
        "Target output frequency",
        "Output frequency",
        "Common crystal references",
        "\U0001F4DA In-depth analysis: Crystal Divider Calculator",
        "MCU clock: 8MHz crystal \u00D7 6 via PLL = 48MHz system clock.",
        "FPGA: a 100MHz clock divided by 1/2/4 feeds different modules.",
        "Audio sampling: 12.288MHz \u00F7 256 = 48kHz.",
        "Communications: a PLL multiplies a low-frequency reference up to the RF carrier.",
        "8MHz\u219248MHz multiplication",
        "Divider ratio = 48/8 = 6; set M=6, N=1 in the PLL for a 48MHz output.",
        "Integer vs fractional division?",
        "Integer division is simple but coarse (e.g. 1MHz steps); fractional division (N.M) hits any frequency but adds spurious tones." + DISCL_E,
        "PLL lock time?",
        "It is set by the loop bandwidth and filter; typically 100\u03BCs~10ms, with fast lock costing phase noise." + DISCL_E,
        "Why use a crystal as the reference?",
        "Crystals hold 10\u207B\u2076~10\u207B\u2079 stability and the PLL output inherits that; RC oscillators are far less stable." + DISCL_E,
        "About \"Crystal Divider Calculation\"",
        "Crystal Divider Calculation derives PLL multiplication and division ratios from the target output and crystal frequency, and can solve for the divider in reverse, making it a basic clock-design tool; it runs entirely in the browser and uploads no data.",
    ]))


if __name__ == '__main__':
    main()

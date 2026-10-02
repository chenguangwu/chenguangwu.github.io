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
    write('frequency-12', build('frequency-12', [
        "\U0001F4E1 Oscillation Frequency Calculator",
        "Pick the oscillator type (RC Wien bridge / LC Colpitts / crystal), enter the parameters and calculate the oscillation frequency",
        "Core formulas (by input): c\u00F71e6",
        "\U0001F4D6 See the \"Oscillation Frequency Calculator User Guide\"",
        "Oscillation type",
        "RC Wien bridge",
        "LC Colpitts",
        "Crystal oscillator",
        "Crystal frequency (MHz)",
        "\U0001F4A1 RC Wien: f=1/(2\u03C0RC); LC Colpitts: f=1/(2\u03C0\u221A(L\u00D7Ceq)) with Ceq=C1\u00D7C2/(C1+C2); crystal: f = the crystal's nominal frequency",
        "An RC Wien bridge needs positive feedback and an amplitude-stabilising circuit",
        "In LC Colpitts, Ceq is the equivalent of the two series capacitors",
        "Crystal frequency is set by the quartz resonator, so accuracy is high",
        "\U0001F4DA In-depth analysis: Oscillation Frequency Calculator",
        "RC Wien bridge: audio/low frequency (0.1Hz~1MHz), common in 1kHz signal generators.",
        "LC Colpitts: high frequency (1MHz~GHz), used for RF local oscillators.",
        "Crystal oscillator: very high stability (10\u207B\u2076~10\u207B\u2079) for clock and communication references.",
        "RC ring oscillator: on-chip clock inside digital chips.",
        "RC Wien bridge with R=10k\u03A9, C=10nF",
        "f=1/(2\u03C0RC)=1.59kHz; the amplifier needs a gain of at least 3 for stable startup.",
        "Why does a Wien bridge need in-phase amplification?",
        "The RC series-parallel network gives 0\u00B0 phase shift at the centre frequency, so the amplifier must add no phase shift to satisfy the Barkhausen startup condition." + DISCL_E,
        "Why are crystal oscillators so stable?",
        "The quartz resonator has a mechanical Q as high as 10\u2074~10\u2076, making frequency selection extremely sharp and frequency accuracy high." + DISCL_E,
        "How does oscillator loading affect the result?",
        "The load capacitance sets the frequency offset; it must match the crystal's nominal CL, and a Colpitts load coupling needs an impedance transformation." + DISCL_E,
        "About \"Oscillation Frequency Calculation\"",
        "This tool supports RC Wien bridge, LC Colpitts and crystal oscillators, computing the oscillation frequency from the component values, making it a basic tool for signal source and clock circuit design.",
        "Three oscillator types",
        "Equivalent capacitance computed automatically",
        "Frequency shown in multiple units",
        "Oscillator circuit design",
        "Clock signal generation",
        "Frequency calibration",
        "Oscillation type",
        "Resistance R (\u03A9)",
        "Capacitance C (\u03BCF)",
        "Inductance L (\u03BCH)",
        "Crystal frequency (MHz)",
    ]))

    write('frequency-13', build('frequency-13', [
        "\U0001F4E1 Antenna Frequency Gain",
        "Enter frequency and antenna length, choose the antenna type, and calculate wavelength, gain and VSWR",
        "Core formulas (by input): 1+dev\u00D710",
        "\U0001F4D6 See the \"Antenna Frequency Gain User Guide\"",
        "Antenna length (m)",
        "Antenna type",
        "1/4 wavelength",
        "1/2 wavelength",
        "Full wavelength",
        "\U0001F4A1 Wavelength \u03BB = 300\u00F7f(MHz); ideal length = \u03BB\u00F74 (1/4 wave), \u03BB\u00F72 (1/2 wave) or \u03BB (full wave); VSWR is estimated from how well the length matches",
        "The closer VSWR is to 1, the better the match",
        "VSWR below 2 is acceptable",
        "Length away from the ideal value causes mismatch",
        "\U0001F4DA In-depth analysis: Antenna Frequency Gain",
        "Wi-Fi 2.4GHz: \u03BB=12.5cm, half-wave dipole 6.25cm.",
        "GSM 900MHz: \u03BB=33.3cm, omnidirectional antenna 1/4\u03BB=8.3cm.",
        "Amateur radio 144MHz: \u03BB=2.08m, a 5/8\u03BB high-gain antenna is 1.3m.",
        "GPS L1 1575MHz: \u03BB=19cm, ceramic patch antenna 25\u00D725mm.",
        "2.4GHz half-wave dipole",
        "\u03BB=300/2400=12.5cm; in practice L\u2248\u03BB/2\u00B70.95 (end-effect correction) = 5.9cm; typical gain 2.15dBi.",
        "What do VSWR=1 and VSWR=2 mean?",
        "VSWR=1 is a perfect match radiating full power; VSWR=2 reflects 11% of the power; keeping VSWR below 1.5 is advised." + DISCL_E,
        "Antenna gain and directivity?",
        "High-gain antennas such as the Yagi are strongly directional and reach further in one direction; omnidirectional antennas have lower gain but even coverage." + DISCL_E,
        "Why does antenna length affect impedance?",
        "The resonant length is L=\u03BB/(2n) (n=1,2,...); when detuned the impedance moves away from 50\u03A9, so reflection increases." + DISCL_E,
        "About \"Antenna Frequency Gain\"",
        "This tool computes wavelength, ideal length, gain and VSWR from the operating frequency and antenna length, helping with RF antenna design, matching and tuning.",
        "Wavelength and ideal length",
        "Gain and VSWR estimate",
        "Three antenna types",
        "RF antenna design",
        "Antenna length verification",
        "VSWR tuning",
        "Wireless link planning",
        "Antenna length (m)",
        "Antenna type",
    ]))

    write('index', build('index', [
        "\u26A1 Electronics Circuit Tools",
        "Electronics Circuits",
        "Electronics Circuit Tools",
        "Crystal divider calculator: find the divider ratio and output frequency with PLL multiply/divide support, for clock and frequency synthesis design.",
        "Capacitance Calculation",
        "An all-in-one capacitance calculator covering series, parallel, RC charging/discharging and time constants; enter the capacitance values to get the equivalent value or time constant at once.",
        "Resistance Calculation",
        "An all-in-one resistance calculator with series, parallel, colour-code reading and voltage-divider modes; enter several resistors or code colours to get the equivalent resistance or dividing ratio, useful for resistor selection and matching.",
        "RC time constant calculator: enter R and C to get the RC time constant \u03C4, charging/discharging curves at each stage and the cutoff frequency, a basic tool for transient analysis, delay circuits and filter design.",
        "Decodes the pF value behind three-digit capacitor codes and converts between pF, nF and \u03BCF, while explaining common voltage-rating markings, for part selection and reading components.",
        "PCB trace width current calculator, deriving the minimum trace width from current, copper thickness and allowed temperature rise per IPC-2221, for PCB routing design.",
        "Pick an oscillator type (RC Wien bridge, LC Colpitts or crystal), enter the matching component values and calculate the oscillation frequency, a basic tool for signal source and clock design.",
        "Diode Forward Voltage Drop",
        "Diode forward drop calculator estimating drop and dissipation from forward current, temperature and type, helping with power supply and rectifier design.",
        "PCB power/temperature-rise estimator, using an empirical model based on copper area and convection to estimate board temperature rise for thermal design.",
        "SMT Stencil Design",
        "SMT stencil designer computing aperture size, area ratio, width-to-thickness ratio and solder paste volume, for surface-mount stencil design.",
        "Circuit Analysis",
        "Circuit analysis calculator covering RLC resonance, real/reactive/apparent power, decibels and reactance; enter the circuit parameters and the result appears immediately, handy for electronics teaching and quick debugging calculations.",
        "Computes inductive reactance from inductance and frequency, checks the unit conversion (1\u03BCH=10\u207B\u2076H) and shows how reactance varies with frequency, for filter and oscillator estimates; runs entirely in the browser.",
        "Enter supply voltage and load impedance, choose single-ended or BTL topology, calculate the theoretical maximum output power and get a low-distortion working power recommendation for amplifier design and selection.",
        "Choose an LDO or DCDC supply type, enter input and output voltage and current, and calculate conversion efficiency and dissipation for each, helping with topology selection and thermal assessment.",
        "Filter cutoff frequency calculator supporting RC and LC filters, deriving the \u22123dB cutoff from the component values for filter design.",
        "Antenna frequency gain calculator deriving wavelength, ideal length, gain and VSWR from frequency and antenna length, helping with RF antenna design and matching.",
        "Resistor colour code reader: pick the colours for each of 4 or 5 bands and the resistance and tolerance are computed automatically, helping identify colour-coded resistors.",
        "Crystal load capacitance matching calculator. Enter the crystal's nominal load capacitance CL and the stray circuit capacitance to get the required external matching capacitor, keeping the crystal starting and running at its nominal frequency; useful for clock debugging.",
        "Op-amp gain-bandwidth design tool. Enter the required closed-loop gain and signal frequency to compute the needed gain-bandwidth product GBP with selection advice, speeding up bandwidth checks and circuit design.",
        "PCB impedance stackup calculator deriving microstrip characteristic impedance from dielectric constant, trace width, dielectric thickness and copper thickness per IPC-2141, for impedance control.",
        "About \"Electronics Circuit Tools\"",
        "This collection holds 21 free online tools covering the common calculations, conversions and lookups of electronics work. Whether you are a practitioner, a student or an everyday user, you will find ready-to-use utilities here. Everything runs in the browser, uploads nothing to a server and keeps your privacy safe.",
        "The electronics circuit tools collected on this page include (a few representative tools):",
        "These tools help you finish common electronics tasks quickly, with no need to memorise formulas or convert units by hand.",
        "Do the Electronics Circuit Tools need a download or registration?",
        "No. Every tool on this page is a pure front-end online utility: open the page and use it straight away, with no software to install, no account to create and no data uploaded.",
        "Are the Electronics Circuit Tools accurate, and is my data safe?",
        "Each tool computes locally in your browser from public mathematical formulas and general industry standards, so results are immediate. All arithmetic runs on your own device and no data is uploaded to any server, so your privacy is protected.",
    ]))


if __name__ == '__main__':
    main()

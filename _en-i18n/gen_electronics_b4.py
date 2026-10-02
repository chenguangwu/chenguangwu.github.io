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
    write('current-pressure-drop', build('current-pressure-drop', [
        "\U0001F39A\uFE0F Diode Forward Voltage Drop",
        "Enter forward current and operating temperature, pick a diode type, and calculate forward drop and power dissipation",
        "Core formulas (by input): v0-0.002\u00D7(tp-25)+0.026\u00D7Math.log(im\u00F710); vd\u00D7im\u00F71000",
        "\U0001F4D6 See the \"Diode Forward Voltage Drop User Guide\"",
        "Forward current (mA)",
        "Diode type",
        "Silicon diode",
        "Germanium diode",
        "Schottky diode",
        "\U0001F4A1 Vd = V0 \u2212 0.002\u00D7(T\u221225) + 0.026\u00D7ln(I\u00F710); power P = Vd \u00D7 I",
        "Temperature coefficient about \u22122mV/\u00B0C",
        "Drop rises slightly with current (logarithmic)",
        "Schottky has lower drop and faster switching",
        "\U0001F4DA In-depth analysis: Diode Forward Voltage Drop",
        "Rectified supply: silicon 1N4007 at If=1A gives Vf\u22480.93V, P\u22480.93W (needs a heatsink).",
        "Switching supply: Schottky Vf\u22480.3V (low drop, high efficiency).",
        "Low-drop rectification: synchronous rectifier MOSFET Vds\u22480.05V.",
        "Signal detection: germanium Vf\u22480.3V suits small signals.",
        "Silicon 1N4148 at If=10mA, 25\u00B0C",
        "Vf\u22480.65V; Vf falls about 2mV per \u00B0C, so at high temperature the lower Vf helps current sharing in paralleled parts.",
        "How does Vf vary with temperature?",
        "The silicon temperature coefficient is about \u22122mV/\u00B0C (reverse leakage also grows with temperature); Schottky is similar but leaks more." + DISCL_E,
        "Why is Schottky Vf low?",
        "The metal-semiconductor junction barrier is lower than a PN junction and electrons are the majority carriers, so there is no minority-carrier storage and reverse recovery is fast." + DISCL_E,
        "Does reverse recovery of power diodes matter?",
        "Fast-recovery and Schottky diodes have short reverse recovery times and low switching loss; a slow recovery rectifier bridge means high switching loss." + DISCL_E,
        "About \"Diode Forward Voltage Drop\"",
        "This Diode Forward Voltage Drop tool estimates forward drop and conduction loss from forward current, operating temperature and diode type (silicon/germanium/Schottky), helping with power supply and rectifier design.",
        "Three diode types to choose from",
        "Temperature and current correction",
        "Automatic power calculation",
        "Rectifier circuit design",
        "Power supply loss estimate",
        "Thermal design assessment",
        "Diode selection",
        "Forward current (mA)",
        "Operating temperature (\u00B0C)",
        "Diode type",
    ]))

    write('dianyuanxiaolvldo-dcdc', build('dianyuanxiaolvldo-dcdc', [
        "\u2699\uFE0F Power Supply Efficiency LDO/DCDC",
        "Choose the supply type (LDO/DCDC), input voltage and current, then calculate efficiency and dissipation",
        "\"Choose the supply type (LDO/DCDC), input voltage and current, then calculate efficiency and dissipation\" is computed from the input parameters and the result is reported.",
        "\U0001F4D6 See the \"Power Supply Efficiency LDO/DCDC User Guide\"",
        "Supply type",
        "LDO linear regulator",
        "DCDC switching supply",
        "Input voltage (V)",
        "Output voltage (V)",
        "Output current (A)",
        "DCDC efficiency (%)",
        "\U0001F4A1 LDO: efficiency = Vout/Vin, dissipation = (Vin\u2212Vout)\u00D7I; DCDC: input power = output power \u00F7 efficiency, dissipation = input power \u2212 output power",
        "LDO efficiency scales with the voltage drop, so a large drop means low efficiency",
        "DCDC efficiency is usually 85%~95%",
        "All LDO dissipation turns into heat, so thermal design matters",
        "\U0001F4DA In-depth analysis: Power Supply Efficiency LDO/DCDC",
        "5V\u21923.3V LDO at 100mA: efficiency 66%, dissipation 0.17W.",
        "5V\u21923.3V Buck at 100mA: efficiency about 90%, dissipation 0.07W (DCDC is preferred).",
        "12V\u21925V Buck at 500mA: efficiency about 92%, dissipation 0.43W.",
        "High-drop LDO: Vin=24V, Vout=5V, 100mA gives only 21% efficiency, so DCDC is mandatory.",
        "92% efficiency with 5W output means 0.43W loss; a 0.5W heatsink is enough (a small SMD LDO will do).",
        "LDO or DCDC?",
        "Small drop, light current and low noise call for an LDO; large drop, heavy current or efficiency-critical loads call for DCDC." + DISCL_E,
        "DCDC ripple versus LDO?",
        "DCDC carries switching ripple (tens of mV) and needs LC filtering; an LDO outputs very low noise but is less efficient." + DISCL_E,
        "Buck-Boost versus Buck?",
        "Buck only steps down; Buck-Boost (SEPIC) accepts a Vin above or below Vout, at the cost of a more complex topology." + DISCL_E,
        "About \"Power Supply Efficiency LDO/DCDC\"",
        "This tool computes the conversion efficiency and dissipation of LDO linear regulators and DCDC switching supplies from input/output voltage and current, helping with topology selection and thermal design.",
        "Dual LDO/DCDC mode",
        "Efficiency and dissipation together",
        "Input current computed automatically",
        "Supply topology selection",
        "Efficiency and thermal assessment",
        "Power budget",
        "Battery-powered design",
        "Supply type",
        "Input voltage (V)",
        "Output voltage (V)",
        "Output current (A)",
        "DCDC efficiency (%)",
    ]))

    write('estimate-power-1', build('estimate-power-1', [
        "\u26A1 Amplifier Power Distortion",
        "Enter the supply voltage and load impedance, choose the amplifier topology, and calculate maximum output power with a distortion guide",
        "Core formulas (by input): pmax\u00D70.5",
        "\U0001F4D6 See the \"Amplifier Power Distortion User Guide\"",
        "Load impedance (\u03A9)",
        "Amplifier topology",
        "Single-ended push-pull (single supply)",
        "BTL bridged (single supply)",
        "\U0001F4A1 Single-ended: Pmax = Vcc\u00B2\u00F7(8R); BTL: Pmax = Vcc\u00B2\u00F7(2R); keep working power \u22640.5\u00D7Pmax to limit distortion",
        "Maximum power is the ideal value; real parts are limited by device voltage drops",
        "THD rises sharply near full power",
        "Rating working power within 0.5\u00D7Pmax is advised",
        "\U0001F4DA In-depth analysis: Amplifier Power Distortion",
        "Single-ended OTL: Vcc=24V, Z=8\u03A9 gives Pmax=18W; staying within 10W keeps distortion low.",
        "BTL (bridged): Vcc=24V, Z=8\u03A9 gives Pmax=72W, four times the single-ended value.",
        "Class D: switching amplification above 90% efficiency, with the same theoretical Pmax as BTL.",
        "Headphone amps: 32\u03A9 is a low impedance that \u00B15V can drive.",
        "Pmax=Vcc\u00B2/(2\u00B7Z)=324/8=40.5W; limiting to 20W~25W keeps THD low.",
        "How does THD+N relate to power?",
        "THD is higher at small signal (switching and zero-crossing distortion), best at mid power, and climbs sharply near Pmax." + DISCL_E,
        "Why is Class D efficient?",
        "The transistors work in switching states (saturation/cutoff) so loss is limited to transition time, giving 90%+ efficiency." + DISCL_E,
        "Does speaker impedance vary with frequency?",
        "Yes. The Z curve peaks at resonance and rises inductively at high frequency; size the amp from the nominal rated impedance." + DISCL_E,
        "About \"Amplifier Power Distortion\"",
        "This tool computes the theoretical maximum output power from supply voltage and load impedance for single-ended or BTL topologies, and suggests a low-distortion working power, helping with audio amplifier design and selection.",
        "Single-ended and BTL modes",
        "Maximum power computed automatically",
        "Low-distortion power guidance",
        "Audio amplifier design",
        "Amplifier selection",
        "Distortion control",
        "Supply voltage planning",
        "Supply voltage (V)",
        "Load impedance (\u03A9)",
        "Amplifier topology",
    ]))

    write('frequency-11', build('frequency-11', [
        "\U0001F4E1 Filter Cutoff Frequency",
        "Pick the filter type (RC/LC), enter the component values and calculate the cutoff frequency",
        "Core formulas (by input): c\u00F71e6",
        "\U0001F4D6 See the \"Filter Cutoff Frequency User Guide\"",
        "Filter type",
        "RC filter",
        "LC filter",
        "\U0001F4A1 RC cutoff fc = 1\u00F7(2\u03C0RC); LC cutoff fc = 1\u00F7(2\u03C0\u221A(LC))",
        "RC is a first-order filter, simple in structure",
        "LC suits high-frequency and high-power cases",
        "Cutoff is the \u22123dB attenuation point",
        "\U0001F4DA In-depth analysis: Filter Cutoff Frequency",
        "Audio low-pass: 20kHz cutoff removes high-frequency noise.",
        "Power filtering: a \u03C0-type LC stage removes switching ripple.",
        "ADC anti-aliasing: cut off below the Nyquist frequency.",
        "RF front-end filtering: image rejection.",
        "f-3dB=1/(2\u03C0\u00B710\u2074\u00B710\u207B\u2078)=1.59kHz; roll-off is 6dB per octave.",
        "First-order versus second-order filtering?",
        "First order falls 6dB per octave, second order 12dB; higher order is steeper but degrades phase response." + DISCL_E,
        "How is the LC filter Q chosen?",
        "Q=\u03C9L/R; Q=0.707 gives Butterworth (flattest), and Q above 0.707 introduces a peak." + DISCL_E,
        "Phase at the cutoff point?",
        "A first-order RC lags 45\u00B0 at fc, a second order lags 90\u00B0." + DISCL_E,
        "About \"Filter Cutoff Frequency\"",
        "This tool supports both RC and LC filters and computes the \u22123dB cutoff from the component values, making it a basic tool for filter design and frequency-response analysis.",
        "RC and LC types",
        "Cutoff frequency computed automatically",
        "Low-pass / high-pass design",
        "Signal anti-aliasing",
        "Power filter design",
        "Frequency-response analysis",
        "Filter type",
        "Resistance R (\u03A9)",
        "Capacitance C (\u03BCF)",
        "Inductance L (\u03BCH)",
    ]))


if __name__ == '__main__':
    main()

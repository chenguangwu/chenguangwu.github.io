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
    write('analysis-22', build('analysis-22', [
        "\u26A1 Power consumption (dynamic / static) analysis",
        "Dynamic / static",
        " / Power consumption (dynamic / static) analysis",
        "\U0001F4D6 View the analysis-22 usage guide",
        "\u26A1 Power consumption (dynamic / static) analysis",
        "This tool computes the average current as I_avg = I_active \u00D7 duty cycle + I_sleep \u00D7 (1 \u2212 duty cycle) and the average power as P_avg = V \u00D7 I_avg (with V in volts and I in mA the result is in mW). Given a battery capacity C (mAh), the runtime is t = C / I_avg in hours. Everything runs locally in the browser and no data is uploaded.",
        "Supply voltage V (V)",
        "Dynamic (active) current I_active (mA)",
        "Static (sleep) current I_sleep (mA)",
        "Duty cycle (%) \u2014 share of time spent working",
        "Battery capacity C (mAh, optional \u2014 used to estimate runtime)",
        "\U0001F4DA In-depth analysis: power consumption (dynamic / static) analysis",
        "Sleep and wake current budget for an IoT node: the device draws only microamps while asleep and milliamps while working, so weighting by the",
        "duty cycle",
        "gives the average current and shows the impact on runtime.",
        "Runtime estimate for battery-powered products: given the capacity",
        "(mAh) and the average current, estimate the working time to guide capacity selection and the charging cycle plan.",
        "Duty cycle versus power trade-off: lowering the duty cycle within the allowable response latency extends runtime significantly, which is useful for order-of-magnitude validation of a low-power strategy.",
        "Example: a coin-cell IoT node",
        "With V = 3.7 V, I_active = 25 mA, I_sleep = 0.05 mA, duty cycle 5% and a 2000 mAh battery: average current \u2248 1.27 mA, average power \u2248 4.7 mW and theoretical runtime \u2248 65 days.",
        "How is the average current computed?",
        "I_avg = I_active \u00D7 duty cycle + I_sleep \u00D7 (1 \u2212 duty cycle), weighting the dynamic and static currents by the share of time spent working, in the same unit as the input current (mA).",
        "Can the result drive the final battery selection?",
        "It suits concept study and order-of-magnitude estimates. Final selection should add power conversion efficiency, self-discharge, temperature and ageing derating, and should be confirmed by measurement.",
        "Why does the static current matter so much?",
        "A low-duty-cycle device spends most of its time asleep, so the static current dominates the average current and the runtime even though it is small. Differences at the microamp level can significantly change battery life.",
        "About the Power consumption (dynamic / static) analysis",
        "The power consumption (dynamic / static) analysis tool is an embedded system power assessment tool. Enter the supply voltage, dynamic and static currents and the duty cycle to estimate the average current, average power and battery runtime, supporting low-power design and battery capacity selection. It runs entirely in the browser and uploads no data.",
        "Sleep and wake current budget for a low-power MCU",
        "Runtime estimate for battery-powered devices",
        "Duty cycle versus power trade-off optimisation",
        "Energy efficiency assessment of an IoT node",
    ]))

    write('bandwidth', build('bandwidth', [
        "\U0001F310 Op-amp gain bandwidth design",
        "Enter the closed-loop gain and signal frequency to compute the required gain-bandwidth product (GBP) and recommend an op-amp.",
        "\U0001F4D6 View the op-amp gain bandwidth design usage guide",
        "Gain-bandwidth product GBP = closed-loop gain \u00D7 signal frequency; the GBP needed for selection is target gain \u00D7 highest signal frequency, with a 2 to 5 times margin reserved (a 1 MHz signal at gain 100 needs GBW of at least 100 MHz, so choose a 200 MHz or better part); closed-loop bandwidth = GBW \u00F7 closed-loop gain. When the required GBP is below 10\u2076 an LM358 works, from 10\u2076 to 10\u2077 choose an NE5532 or TL072, and above 10\u2077 a high-speed op-amp is required.",
        "Closed-loop gain (times)",
        "Signal frequency (Hz)",
        "\U0001F4A1 Required GBP = gain \u00D7 frequency; allow a selection margin \u2265 the calculated value \u00D7 2; the \u22123dB bandwidth = GBP \u00F7 gain",
        "GBP is the op-amp gain-bandwidth product, a core datasheet parameter",
        "Real selection should leave a 2 to 10 times margin",
        "High-frequency signals also require attention to slew rate SR",
        "\U0001F4DA In-depth analysis: op-amp gain bandwidth design",
        "Low-frequency signal amplification: 100 Hz \u00D7 gain 1000 calls for GBP \u2265 100 kHz, a general-purpose op-amp.",
        "Audio amplification: 20 kHz \u00D7 gain 10 calls for GBP \u2265 200 kHz and a low-noise op-amp.",
        "High-speed ADC buffering: 1 MHz \u00D7 gain 1 calls for GBP \u2265 1 MHz, a wideband op-amp.",
        "Video amplification: 5 MHz \u00D7 gain 6 calls for GBP \u2265 30 MHz, a video op-amp.",
        "GBP = 10 \u00B7 100 kHz = 1 MHz; an OPA227 (GBP = 1 MHz, low noise) or an LM358 (GBP = 1 MHz, general purpose) is recommended.",
        "How do GBP and slew rate relate?",
        "GBP sets the small-signal bandwidth while the slew rate SR sets large-signal slewing; together they determine the usable bandwidth of the op-amp." + DISCL_E,
        "Why is the gain-bandwidth product a constant?",
        "It is set by the transistor transition frequency fT inside the op-amp, with fT = Aol\u00B7fAol-3dB. The higher the closed-loop gain, the narrower the usable bandwidth." + DISCL_E,
        "Why choose Rail-to-Rail?",
        "With a low-voltage single supply the output only swings to Vcc/Vee, so a rail-to-rail part uses the whole input range, for example the OPA2333." + DISCL_E,
        "About the Op-amp gain bandwidth design",
        "The op-amp gain bandwidth design tool computes the required gain-bandwidth product (GBP) from the closed-loop gain and signal frequency and recommends suitable op-amp models, helping engineers complete op-amp selection and bandwidth checks quickly.",
        "Automatic GBP calculation",
        "Smart op-amp model recommendation",
        "Selection margin guidance",
        "Op-amp selection and design",
        "Bandwidth margin verification",
        "High-frequency circuit design",
        "Closed-loop gain (times)",
        "Signal frequency (Hz)",
    ]))

    write('calc-63', build('calc-63', [
        "\u26A1 PCB trace current capacity",
        "Enter the current, copper thickness and allowable temperature rise to compute the minimum trace width per IPC-2221.",
        "Core formulas (by input variable): (i\u00F7(0.024\u00D7dt^0.44), 1\u00F70.725); wmil\u00D70.0254; oz\u00D71.378",
        "\U0001F4D6 View the PCB trace current capacity usage guide",
        "Copper thickness (oz)",
        "Allowable temperature rise (\u00B0C)",
        "\U0001F4A1 IPC-2221 outer layer: I = 0.024\u00D7\u0394T^0.44\u00D7A^0.725, where A is the cross-sectional area in mil\u00B2; trace width = A \u00F7 copper thickness",
        "Based on the IPC-2221 outer layer trace formula",
        "1 oz copper \u2248 1.378 mil \u2248 0.035 mm",
        "Inner layer traces need extra width, so consult the tables for correction",
        "\U0001F4DA In-depth analysis: PCB trace current capacity",
        "Power traces: 5 A on 1 oz copper with a 10 \u00B0C rise needs at least 5 mm on the outer layer.",
        "Signal traces: 100 mA is already carried by 0.3 mm, so no great width is needed.",
        "High-current LEDs: a 350 mA constant-current driver is fine with 0.5 mm.",
        "High-voltage isolation: use wide spacing and creepage distances meeting IEC 60950/62368.",
        "I = 3 A, t = 1 oz, \u0394T = 10 \u00B0C on the outer layer",
        "A = I/(k\u00B7\u0394T^b); the IPC-2221 table gives about 4.0 mm, reducible to 2.5 mm with good heat sinking.",
        "Where does IPC-2221 apply?",
        "General PCB design. High-frequency microwave and differential impedance control need IPC-2141 or Polar SI9000 simulation." + DISCL_E,
        "Why are inner layer traces narrower than outer ones?",
        "Inner layers dissipate heat poorly because they are surrounded by dielectric, so the same current needs more width; 2 oz copper carries twice the current of 1 oz." + DISCL_E,
        "Why widen power traces?",
        "To reduce resistance, voltage drop and temperature rise. For high currents use copper pours plus multiple vias for the current path." + DISCL_E,
        "About the PCB trace current capacity",
        "The PCB trace current capacity tool follows the IPC-2221 standard to compute the minimum outer layer trace width from the current, copper thickness and allowable temperature rise. It is a fundamental tool for PCB layout design.",
        "IPC-2221 standard formula",
        "Dual mil and mm display",
        "Automatic copper thickness conversion",
        "PCB layout trace width design",
        "Power trace capacity verification",
        "Copper thickness selection",
        "Temperature rise control design",
        "Current (A)",
        "Copper thickness (oz)",
        "Allowable temperature rise (\u00B0C)",
    ]))


if __name__ == '__main__':
    main()

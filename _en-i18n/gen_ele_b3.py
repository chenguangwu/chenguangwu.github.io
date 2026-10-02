#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'electrical')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'electrical')
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
    out = {'slug': slug, 'industry': 'electrical', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('home-load-estimate', build('home-load-estimate', [
        "\"Home Load Estimate\" runs a professional calculation from the input parameters and outputs the result.",
        "/ Household Load Estimate",
        "🔮 Household Load Estimate",
        "Work out the load before wiring a renovation: tick the appliances you use, enter the quantities, and estimate the total load from the power ratings and the demand factor, then judge whether 2.5/4/6/10mm² incoming lines and a 40/60A meter are enough.",
        "Refrigerator (units, 200W)",
        "Air conditioner (units, 1200W)",
        "Washing machine (units, 500W)",
        "Electric water heater (units, 2000W)",
        "Kitchen appliances (microwave/oven/rice cooker combined, W)",
        "Lighting and others (W)",
        "📚 Deep dive: Home Load Estimate",
        "New home distribution: for an 80-120㎡ three-bedroom unit, design the distribution board for 8-12kW.",
        "Photovoltaic sizing match: for 300kWh of monthly consumption, 3-5kW of PV is recommended.",
        "Storage backup: keeping the refrigerator, lighting and network running for ≥8h during an outage is",
        "Rental unit metering: estimating the per-unit peak power and the meter size.",
        "Monthly electricity estimate for a 100㎡ three-bedroom home",
        "Air conditioners 2×1.5kW×120h + refrigerator 0.1kW×720h + lighting 0.4kW×120h + others ≈ 530kWh/month.",
        "How do I choose the simultaneity factor?",
        "For housing it is generally 0.6-0.8 (except at the summer air-conditioning peak); you can count circuit by circuit or follow the NEC load calculation table. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "Why does monthly consumption vary so much?",
        "Season (winter/summer air conditioning or heating), household size and appliance habits; it is best to design around the 12-month average of your bills. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "How do I size the photovoltaic installation?",
        "Use average daily generation = installed kW × 4h (southern China) to 3.5h (northern China), so monthly generation = installed × 120-105kWh. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "Installed power × demand factor (0.6) ≈ calculated load",
        "Current = load ÷ 220V (single-phase)",
        "Incoming line recommendation: 2.5mm²/32A → 4mm²/40A → 6mm²/50A → 10mm²/63A",
        "The conclusion is for reference only; for formal electrical work consult a licensed electrician and follow the applicable codes",
    ]))

    write('breaker-sizing', build('breaker-sizing', [
        "/ Circuit Breaker Sizing Calculator",
        "⚡ Circuit Breaker Sizing Calculator",
        "A breaker rated too large fails to protect, and one rated too small keeps tripping. Enter the circuit load current and its purpose to get a recommended rated current based on the 1.25 factor (common standard rating series), together with a pole-count suggestion.",
        "Circuit load current (A)",
        "Circuit purpose",
        "Kitchen and bathroom appliances",
        "Number of poles",
        "1P (single-phase lighting)",
        "2P (single-phase high power)",
        "3P (three-phase)",
        "📚 Deep dive: Breaker Sizing",
        "Residential distribution board: 2.5mm² copper with a C16 breaker, verifying overload protection and short-circuit breaking.",
        "Industrial motor circuit: C25 with a D trip curve, handling 6-8 times the starting current.",
        "Photovoltaic DC side: selecting a 1000V DC breaker and verifying the reverse current and breaking capacity.",
        "Data centre rack: 32A C-type breaker at the end of the line, with capacity derating for the harmonic load of IT equipment.",
        "Breaker for a 7kW single-phase water heater",
        "I = 7000/220 ≈ 31.8A; applying a 1.25 margin gives a C40 breaker, paired with 6mm² copper.",
        "How do I choose between C and D trip curves?",
        "The C curve suits ordinary loads (lighting and sockets) with a magnetic trip at 5-10In; the D curve suits motors and transformers with a magnetic trip at 10-20In, withstanding starting inrush. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "How do I choose the breaking capacity Icu?",
        "Choose it from the prospective short-circuit current at the installation point: 6kA for residential, 10-25kA for commercial and industrial, and 25-50kA near a transformer. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "Why verify the sensitivity?",
        "The minimum short-circuit current of the final circuit should be at or above the breaker's magnetic setting; otherwise the breaker refuses to trip on a short circuit, causing cascading trips or fire. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "Breaker rated current ≈ load current × 1.25, rounded up to a common standard size (6/10/16/20/25/32/40…)",
        "Shock loads such as motors (air conditioners) need the starting current considered, so a D trip curve is the right choice",
        "A rating that is too high loses overload protection, and one that is too low causes frequent nuisance tripping",
        "The result is for reference only; formal design should follow GB 50054 and the manufacturer's selection catalogue",
    ]))

    write('wire-gauge-selector', build('wire-gauge-selector', [
        "\"Wire Gauge Selector\" runs a professional calculation from the input parameters and outputs the result.",
        "/ Wire Gauge Selector",
        "🔌 Wire Gauge Selector",
        "Do not pick a wire size by feel: enter the load current, conductor material and installation method to get a recommended minimum safe cross-section (the BV copper wire series), with a margin note against the ampacity table.",
        "Load current (A)",
        "Copper conductor",
        "Aluminium conductor",
        "Line length (m, optional)",
        "📚 Deep dive: Wire Gauge Selector",
        "Power cord selection: a 5A load over a 10m run calls for 1.5mm² or AWG 16.",
        "PCB trace width: for 10A continuous current at a 10℃ rise, 1oz copper needs about 4mm width.",
        "Automotive low-voltage cable: a 12V system drawing 30A over a short distance needs 6mm² or more.",
        "AWG to metric conversion: 14AWG ≈ 2.08mm², 12AWG ≈ 3.31mm², 10AWG ≈ 5.26mm².",
        "AWG 12 to mm²",
        "AWG 12 ≈ 3.31mm²; at 25℃ the copper ampacity is about 25A (PVC conduit), so it can carry a 16A continuous load.",
        "Does a larger AWG number mean a thinner wire?",
        "Yes. The larger the AWG number the smaller the cross-section, the higher the resistance and the lower the ampacity; AWG 24 is commonly used for network cables and control signals. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "What is the relationship between temperature rise and ampacity?",
        "The allowed temperature rise of the conductor (70℃ for PVC, 90℃ for XLPE) determines the ampacity, and the same cross-section must be derated in a hot environment. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "How does the installation method affect ampacity?",
        "Conduit, tray, direct burial and overhead have different cooling conditions, and the ampacity differs by 30%-50% across installation methods. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "The ampacity references common BV/BVR conductor data and already leaves a 1.25x margin on the current",
        "At the same cross-section an aluminium conductor carries about 75-80% of the ampacity of copper",
        "Conduit installation cools poorly, so its ampacity is lower than surface mounting",
        "Long runs need a voltage drop check (≤5% recommended); the result is for reference only and formal design should follow GB 50303",
    ]))

    write('led-resistor', build('led-resistor', [
        "⚡ LED Current-Limiting Resistor Calculation (Electrical)",
        "Computes the required current-limiting resistance and its power dissipation from the supply voltage, the LED forward voltage and the rated current.",
        "LED Current-Limiting Resistor Calculation",
        "Supply voltage V_s (V)",
        "LED forward voltage V_f (V)",
        "Forward current I_f (mA)",
        "The chosen resistance should be ≥ the calculated value with a margin (to guard against over-current)",
        "Power P = I_f²·R, so pick the resistor power rating accordingly",
        "📚 Deep dive: LED Current-Limiting Resistor Calculation (Electrical)",
        "5V Arduino driving a red LED: Vf=2V, If=10mA → R=300Ω, so pick the standard 330Ω.",
        "12V indicator lamp: Vf=3.2V, If=20mA → R=440Ω, so pick 470Ω.",
        "24V supply driving several LEDs in series, which avoids individual current limiting.",
        "High-power LED: Vf=3.5V, If=350mA → R=(12-3.5)/0.35 = 24Ω at 2W.",
        "A 3.0V 20mA LED driven from 5V",
        "R=(5-3.0)/0.02 = 100Ω; P=I²R=0.04W, so a 100Ω 1/4W resistor is enough.",
        "How do I choose the resistor power rating?",
        "The real dissipation is P=I²R, so pick a resistor rated at 4 times or more of that (long-term derating to 25%). This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "Why do LEDs need current limiting?",
        "An LED is a current-driven device, so a small voltage swing causes a large current surge; current limiting prevents rapid light decay and burnout. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "How do I choose the resistor for PWM dimming?",
        "The PWM average current = If ×",
        "duty cycle",
        "; size the resistor for the peak current If (to avoid peak over-current). This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
    ]))

if __name__ == '__main__':
    main()

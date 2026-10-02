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
    write('index', build('index', [
        "🔌 Electrical Engineering Tools",
        "Electrical Engineering",
        "Electrical engineering tools",
        "Circuit Breaker Sizing Calculator",
        "The circuit breaker sizing calculator is a free online electrical engineering tool. A breaker rated too large fails to protect, and one rated too small keeps tripping. Enter the circuit load current and its purpose to get a recommended rated current based on the 1.25 factor (common standard rating series), together with a pole-count suggestion. Runs entirely in the front end with no data uploaded ...",
        "LED Current-Limiting Resistor Calculation",
        "Enter the supply voltage, the LED forward voltage and the rated current to compute the required current-limiting resistance and its power dissipation by Ohm's law, with a recommended common nominal power rating so the LED circuit operates stably and safely.",
        "RLC Series Resonant Frequency Calculation",
        "Enter the inductance L and capacitance C to compute the resonant frequency of an RLC series circuit with f = 1/(2π√LC), as a reference for filter and frequency-selective circuit design.",
        "Current Divider Calculation",
        "Enter the total current and the parallel branch resistances to compute each branch current with the divider formula I_x = I·R_total/R_x, for circuit analysis and divider design.",
        "RC Low-Pass Cutoff Frequency Calculation",
        "An RC low-pass cutoff frequency calculator that finds the -3dB cutoff from the resistance and capacitance, for filter and signal conditioning design.",
        "Conductor Resistance Calculation",
        "A wire resistance calculator that derives DC resistance from material resistivity, length and cross-section, for conductor selection and line loss assessment.",
        "Op-Amp Gain Calculation",
        "An op-amp gain calculator that solves the closed-loop voltage gain of inverting and non-inverting amplifier circuits, for analog circuit design.",
        "Enter the individual cell voltage, capacity and the series/parallel counts to compute the pack's total voltage, total capacity and total energy, and estimate the runtime under a given load, for energy storage, UPS and EV power design.",
        "A voltage drop calculator that finds the voltage drop from low-voltage line parameters and selects the conductor cross-section, supporting single-phase and three-phase systems for distribution design.",
        "Cable Ampacity Calculation",
        "Estimates the continuous ampacity of a cable from conductor material, cross-section, installation method, ambient temperature and correction factors, following the IEC 60364 approach.",
        "Three-Phase Power Calculation",
        "Computes active power, reactive power, apparent power and the current deviation from the three-phase voltage, current and power factor.",
        "Household Load Estimate",
        "Work out the load before wiring a renovation: tick the appliances you use, enter the quantities, and estimate the total load from the power ratings and the demand factor, then judge whether 2.5/4/6/10mm² incoming lines and a 40/60A meter are enough.",
        "Wire Gauge Selector",
        "The wire gauge selector is a free online electrical engineering tool. Do not pick a wire size by feel: enter the load current, conductor material and installation method to get a recommended minimum safe cross-section (the BV copper wire series), with a margin note against the ampacity table. Runs entirely in the front end, uploads no data and needs no registration — open the browser ...",
        "Enter the hourly load (kW) for each period of a 24-hour day to automatically compute the load factor and peak-valley difference and draw the daily load curve.",
        "Power Factor Compensation is a free online electrical engineering tool that computes the compensation capacitor capacity needed to raise the power factor from its current value to a target value. Runs entirely in the front end, uploads no data, needs no registration and works as soon as you open the browser.",
        "Enter the calculated load (active, reactive or apparent power) and the power factor to compute the required distribution transformer capacity and recommend a suitable model against the standard kVA series, helping with power distribution design and equipment selection.",
        "Voltage Divider",
        "A resistor voltage divider calculator that derives the divider output voltage from two series resistors, for reference voltage and signal attenuation design.",
        "About \"Electrical Engineering Tools\"",
        "This collection gathers 17 free online tools covering the common calculations, conversions and lookups of electrical engineering. Whether you are a practitioner, a student or an ordinary user, you will find practical ready-to-use mini tools here. Every tool runs entirely in the browser, no data is uploaded to a server, and your privacy is protected.",
        "The electrical engineering tools collected on this page include (a few representative ones):",
        "These tools help you finish common electrical engineering tasks quickly, with no need to memorize complex formulas or convert anything by hand — type and you get the result.",
        "Do the electrical engineering tools need a download or registration?",
        "No. Every tool on this page is a pure front-end online tool: open the page and start using it. No software to install, no account to register, and no data is uploaded.",
        "Are the results accurate? Is the data safe?",
        "The tools compute locally in your browser from public mathematical formulas and general industry standards, so results are instant. All computation happens on your own device, no data is uploaded to a server, and your privacy is fully protected.",
    ]))

    write('calc-1', build('calc-1', [
        "💧 Cable Ampacity Calculation",
        "Estimates the continuous ampacity of a cable from conductor material, cross-section, installation method, ambient temperature and correction factors, following the IEC 60364 approach.",
        "Conductor material",
        "Copper Cu",
        "Aluminium Al",
        "Cross-section S (mm²)",
        "Insulation type",
        "Conduit, surface mounted",
        "Wall mounted",
        "Cable tray",
        "Direct buried in soil",
        "Free air",
        "Number of cores",
        "2 cores",
        "3 cores",
        "4 cores",
        "Ambient temperature θₐ (℃)",
        "Group circuit correction k₂",
        "Soil thermal resistance correction k₃",
        "Depth of burial correction k₄",
        "Calculated ampacity",
        "The base ampacity I₀ is estimated from an empirical formula based on conductor material, cross-section and insulation class",
        "Temperature correction k₁: PVC uses 30℃ as the base, XLPE/EPR uses 30℃ as the base",
        "Total ampacity Iz = I₀ × k₁ × k₂ × k₃ × k₄",
        "The result is for reference only; for engineering work consult the tables in IEC 60364-5-52 or GB/T 16895",
        "📚 Deep dive: Cable Ampacity Calculation",
        "Industrial plant distribution: 35mm² copper PVC in conduit at an ambient 40℃ gives an estimated ampacity of about 96A.",
        "Outdoor direct-buried cable: 4×120mm² aluminium XLPE with soil",
        "resistivity",
        "of 1.2K·m/W gives an estimated ampacity of about 220A.",
        "Dense tray installation: 10 circuits laid in parallel derate by 30% to 9/10.",
        "High ambient temperature: in a 50℃ boiler room, the IEC correction factor of 0.82 derates the rating.",
        "95mm² copper XLPE three-phase ampacity",
        "Method B1 at 30℃ gives a standard ampacity of 232A; the 40℃ correction of 0.94 brings it to 218A; 3 circuits in parallel at 0.87 brings it to 189A, so the final recommendation is ≤170A.",
        "Why does the real value differ from the catalogue?",
        "Installation method, ambient temperature, soil resistivity, altitude and harmonics all stack up as correction factors applied one by one. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "How do I choose between copper and aluminium?",
        "At the same ampacity copper needs a smaller cross-section and offers higher mechanical strength and longer life; aluminium is cheaper but has higher contact resistance and its joints need anti-oxidation treatment. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "Does the ampacity determine the protection setting?",
        "Yes. The overload protection setting current must be ≤ 1.45 × the ampacity (IEC 60364-43), and the breaker In is usually taken at 1.0 to 1.25 times the ampacity. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
    ]))

    write('load-curve', build('load-curve', [
        "🔌 Electrical Load Curve",
        "Enter the hourly load (kW) for each period of a 24-hour day to automatically compute the load factor and peak-valley difference and draw the daily load curve.",
        "Energy consumption = Σ(load of each period × 1h)",
        "Calculate and plot",
        "Typical factory",
        "Office and commercial",
        "Residential",
        "Copy data",
        "Daily load curve",
        "Peak load",
        "Valley load",
        "General period",
        "📋 Load characteristic indicators",
        "Load factor = average load / maximum load",
        ", which reflects how steady the load is; the closer to 1 the steadier it is.",
        "Peak-valley difference = maximum load - minimum load",
        ", which reflects how much the load fluctuates.",
        "Peak-valley difference rate = peak-valley difference / maximum load",
        ", and a larger value means a stronger need for peak shaving.",
        "Demand factor = maximum load / installed capacity",
        "(an estimate of installed capacity is required).",
        ", in kWh.",
        "📚 Deep dive: Electrical Load Curve",
        "Factory daily load analysis: identify peak and valley periods and schedule production away from the peak.",
        "Residential communities",
        ": when the daily peak-valley difference is too large, storage or a capacity-adjusted transformer is needed.",
        "Time-of-use tariff optimization: overlay the load curve with peak and off-peak prices to find the optimal usage plan.",
        "Photovoltaic self-consumption rate: compare the daily load curve with the PV output curve to derive the self-consumption rate and the curtailment rate.",
        "Factory 24h load (kW) analysis",
        "Peak 580kW (10:00 / 14:00), valley 120kW (04:00), load factor 65%, peak-valley difference 460kW.",
        "How do I use the load factor?",
        "Load factor = average daily load / maximum daily load; the higher it is the better the equipment utilization, and low-load-factor circuits deserve priority attention in energy-saving retrofits. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "What impact does an excessive peak-valley difference have?",
        "It raises transformer no-load losses, sizes distribution equipment for the peak while it runs lightly loaded for long stretches, and lowers line utilization; storage or scheduling can smooth it out. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "What is a good minimum load factor?",
        "Generally ≥ 60% is good; below 40% means violent fluctuation and optimization with time-of-use tariffs or storage is worth considering. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "About \"Electrical Load Curve\"",
        "The Electrical Load Curve is an online tool for power systems. Enter 24-hour load data and it automatically computes the load factor and peak-valley difference and plots the curve, running entirely in the front end with no data uploaded.",
    ]))

    write('battery-bank', build('battery-bank', [
        "🧮 Battery Bank Calculation",
        "Computes the total voltage, total capacity, total energy and discharge runtime of a battery bank after series and parallel connection.",
        "\"Computes the total voltage, total capacity, total energy and discharge runtime of a battery bank after series and parallel connection.\" It runs a professional calculation from the input parameters and outputs the result.",
        "Individual cell voltage (V)",
        "Individual cell capacity (Ah)",
        "Number in series (S)",
        "Number in parallel (P)",
        "Discharge efficiency η (%)",
        "📋 Calculation notes",
        "Basic formulas:",
        "• Total voltage = cell voltage × number in series",
        "• Total capacity = cell capacity × number in parallel (Ah does not change with series connection)",
        "• Total energy = total voltage × total capacity (Wh)",
        "• Usable energy = total energy × DoD × η",
        "• Runtime = usable energy / load power (h)",
        "Series and parallel rules:",
        "Series connection raises the voltage and parallel connection raises the capacity; total energy = series × parallel × cell energy.",
        "📚 Deep dive: Battery Bank Calculation",
        "Server room UPS backup time check: a 48V system needing 30 minutes of backup uses series/parallel group sizing based on 12V100Ah cells.",
        "Off-grid photovoltaic storage: a 48V DC bus with a 5kW load and 4h backup needs lead-acid or lithium series/parallel capacity estimated.",
        "Automotive starter battery: a 12V cell in N series and N parallel handles high-current cranking at -18℃.",
        "Telecom base station backup battery: a -48V system sized for 6h of BTS runtime after an outage.",
        "48V 100Ah UPS with 30 minutes of backup",
        "With 12V100Ah cells, 4 series and 1 parallel gives 48V100Ah; it can deliver 100A × 0.5h = 50Ah within 30 minutes, which sustains a 30A load for about 100 minutes.",
        "What do series and parallel connection each determine?",
        "Series determines the voltage (V_series = V_cell × N_series) and parallel determines the capacity (Ah_parallel = Ah_cell × N_parallel), so total energy = Ah_parallel × V_series. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "Why is the usable capacity lower than the rated one?",
        "The discharge rate (the Peukert effect), temperature (capacity loss when cold) and the cutoff voltage all limit it: lead-acid gives about 50-80% and lithium 80-95%. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "How do I choose the series and parallel counts?",
        "First fix the number in series from the system voltage (V_system / V_cell), then fix the parallel Ah from the required backup duration and load current. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "About \"Battery Bank Calculation\"",
        "The Battery Bank Calculation is an online tool for electrical engineering, focused on lead-acid and lithium series/parallel capacity and voltage verification, running entirely in the front end with no data uploaded.",
        "How to use the Battery Bank Calculation",
        "Series and parallel capacity and voltage verification for battery banks, usable in UPS, off-grid photovoltaic, telecom base station and EV scenarios.",
        "What does the Battery Bank Calculation do?",
        "Enter the individual cell voltage, capacity and the series/parallel counts to compute the pack's total voltage, total capacity and total energy and estimate the runtime under a given load, for energy storage, UPS and EV power design.",
        "How do I use the Battery Bank Calculation?",
        "Which scenarios suit the Battery Bank Calculation?",
    ]))

if __name__ == '__main__':
    main()

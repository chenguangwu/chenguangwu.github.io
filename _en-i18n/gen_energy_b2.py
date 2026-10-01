#!/usr/bin/env python3
# energy batch2 (5 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'energy')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'energy')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'water-tds-evaluator': [
"📋 Water Quality TDS Assessment",
"Enter the water TDS value (total dissolved solids) to assess the water quality grade, applicable scenarios and health advice",
'📖 View the "Water Quality TDS Assessment User Guide"',
"TDS total dissolved solids (mg/L) reflects the total amount of dissolved inorganic salts and organic matter in water; graded as ≤50 very low (pure water), 50-300 high-quality drinking water, 300-600 acceptable (slightly poor taste), 600-1000 poor (not advised for long-term direct drinking), over 1000 substandard (needs treatment); freshwater aquaculture is suitable at 200-500; the approximate relationship between TDS and conductivity is TDS ≈ EC × 0.55 to 0.7, which can be used for cross-verification.",
"Enter the TDS value to start the assessment",
"TDS value (ppm / mg/L)",
"📋 WHO Drinking Water TDS Standard Comparison",
"Standard/Region",
"Maximum limit (ppm)",
"WHO guideline value",
"Comprehensive recommendation based on taste and health",
"China GB5749",
"Drinking water hygiene standard",
"US EPA",
"Secondary drinking water standard",
"EU",
"No unified TDS limit, per member state",
"Purified water/distilled water",
"Contains almost no minerals",
"Mineral water",
"Contains beneficial minerals",
"📚 TDS Grading Standard Details",
"📚 In-Depth Analysis: Water Quality TDS Assessment",
"Compare the inlet and outlet TDS of a water purifier to see the purification effect.",
"Determine whether the RO membrane needs replacement.",
"Suitability of water for fish tanks/planting.",
"RO purifier performance",
"Raw water TDS 300 mg/L, outlet water 12 mg/L: rejection rate=(300−12)/300=96%, the RO membrane is working normally (usually >95%). If the outlet rises to 50+ with a notable drop, it indicates membrane aging or a blocked pre-filter. Tip: TDS does not include microorganisms and volatile pollutants and cannot replace a full test panel.",
"Is a TDS of 0 the best?",
"Pure water has a TDS near 0, but for long-term drinking it is advisable to retain a small amount of minerals; the key is that harmful substances and microorganisms meet the standard, not that lower is always better.",
"Why are TDS readings higher in winter?",
"Temperature affects conductivity measurement; most pens have temperature compensation. Without compensation, low-temperature readings are lower, so use the compensated value.",
'About the "Water Quality TDS Assessment"',
"Water Quality TDS Assessment is an online tool in the energy and power domain. Based on standard physical and engineering formulas, it calculates accurately with reliable results.",
"Based on standard physical and engineering formulas",
"Electricity and energy data analysis",
"Electric power and energy conversion",
"Energy solution assessment assistance",
"Learning energy and electricity knowledge",
],
'estimate-area': [
"⚡ Solar Power Generation Estimation",
"Enter the PV panel area, sunshine hours, conversion efficiency and system efficiency to estimate the annual generation and economic revenue",
'📖 View the "Solar Power Generation Estimation User Guide"',
"Generation = area × irradiance × efficiency × hours",
"PV panel area (m²)",
"Average daily peak sunshine (h/day)",
"Photoelectric conversion efficiency (%)",
"System efficiency (%)",
"Feed-in tariff (CNY/kWh)",
"💡 Formula: annual generation = area × average daily peak sunshine × 365 × conversion efficiency × system efficiency; installed capacity = area × conversion efficiency (kWp).",
"Average daily peak sunshine hours reference: Northwest 5-6h, North China 4-5h, East China 3.5-4.5h, South China 3-4h",
"Monocrystalline silicon conversion efficiency is about 20-22%, polycrystalline about 16-18%, thin film about 10-12%",
"System efficiency is about 75-85%, including inverter loss, line loss, temperature degradation, etc.",
"📚 In-Depth Analysis: Solar Power Generation Estimation",
"Calculate the installable PV capacity from the roof area.",
"Calculate the purifier applicable area from CADR and ceiling height.",
"Estimate the space requirement for equipment layout.",
"Installable rooftop PV capacity",
"Usable roof 30 m², module power density about 200 W/m²: can install about 6 kWp, annual generation about 7800 kWh. Tip: accounting for walkways, shading and orientation derating, the actual installable amount is often less than the theoretical.",
"How to take the power density?",
"For PV use the module layout density; for a purifier use CADR/(ceiling height × air changes); different products vary greatly, so refer to the manufacturer's parameters.",
"What happens if the area is underestimated?",
"Insufficient capacity fails to reach the target; overestimating leaves no room or causes shading, so reserve spacing and maintenance walkways.",
'About the "Solar Power Generation Estimation"',
"Solar power generation estimation tool: enter the PV panel area, sunshine hours, photoelectric conversion efficiency and system efficiency to estimate the annual generation, installed capacity and economic revenue, suitable for distributed PV planning.",
"Estimate annual generation by the area method",
"Automatically compute the installed capacity (kWp)",
"25-year lifetime cumulative revenue forecast",
"Annual equivalent utilization hours calculation",
"Household distributed PV planning",
"Commercial and industrial rooftop PV assessment",
"PV investment return analysis",
"PV system scheme comparison",
"PV panel area",
"Average daily peak sunshine",
"Photoelectric conversion efficiency",
"System efficiency",
"Feed-in tariff",
],
'assessor-water-quality': [
"📋 Water Quality TDS Assessment (Value Input)",
"Enter the TDS value (total dissolved solids) to assess the water quality grade and judge whether it is suitable for drinking against the GB 5749 drinking water standard",
'📖 View the "Water Quality TDS Assessment (Value Input) User Guide"',
"TDS rating: determine the water quality by threshold segments",
"TDS value (mg/L or ppm)",
"Domestic drinking water",
"Direct drinking water/purified water",
"Industrial water",
"Agricultural irrigation",
"Assess water quality",
"📚 In-Depth Analysis: Water Quality TDS Assessment (Value Input)",
"Quick assessment of tap water/well water before entering the home.",
"Check the compliance of water purifier outlet water.",
"Suitability of water quality for aquaculture/irrigation.",
"Well water drinking assessment",
"TDS 350 mg/L (compliant), pH 7.2 (compliant), turbidity 3 NTU (slightly high), residual chlorine 0 (not disinfected): can be used for general household purposes, and before drinking it is advisable to filter + disinfect (boiling/UV). Tip: microorganisms and heavy metals must also be tested; the indicators are only at the physical and chemical level.",
"Is low TDS necessarily good-tasting?",
"TDS reflects the total dissolved solids; too low tastes flat and too high tastes off. Drinking water of 300-600 mg/L is common; the key is that harmful substances meet the standard.",
"What is the risk of high turbidity?",
"Water with high turbidity easily carries pathogenic microorganisms and impairs disinfection; drinking water must have low turbidity and undergo microbial testing.",
"TDS (total dissolved solids) reflects the total amount of dissolved inorganics in water; the GB 5749 limit is ≤500mg/L",
"TDS is positively correlated with conductivity: conductivity ≈ TDS/0.55 (μS/cm)",
"TDS too low (<30mg/L) contains almost no minerals and needs supplementation for long-term drinking",
"TDS cannot reflect harmful substances such as bacteria and heavy metals and needs to be combined with other indicators",
"Water temperature affects the TDS measurement; it is recommended to measure at the standard temperature of 25°C",
'About the "Water Quality TDS Assessment (Value Input)"',
"Water quality TDS assessment tool: enter the total dissolved solids (TDS) value and it automatically determines the water quality grade and suitable uses against the GB 5749 drinking water standard.",
"Instant TDS value assessment",
"Based on the GB 5749-2022 standard",
"Automatic conductivity estimation",
"Adapted to four use scenarios",
"Household drinking water quality assessment",
"Water purifier performance testing",
"Industrial water determination",
"Agricultural irrigation water quality assessment",
],
'estimate-time-current': [
"⚡ Charging Time Estimation",
"Enter the battery capacity, charging current and charging efficiency to compute the charging time, battery energy and charging power",
'📖 View the "Charging Time Estimation User Guide"',
"Charging time = capacity / current",
"Charging current (mA)",
"Charging efficiency (%)",
"Current charge level (%)",
"💡 Formula: charging time = battery capacity × (1 - current charge %) ÷ (charging current × charging efficiency). Lithium battery charging efficiency is about 80-90%, with a voltage usually of 3.7V.",
"Charging efficiency reference: lithium battery about 80-90%, NiMH battery about 65-70%, lead-acid battery about 75-80%",
"The fast-charge stage (0-80%) is quick while the trickle stage (80-100%) is slow, so the actual time will be longer",
"The charging current should not exceed 1C of the battery capacity (e.g., no more than 3000mA for a 3000mAh battery)",
"📚 In-Depth Analysis: Charging Time Estimation",
"Estimate the full charge time of a power bank by current.",
"Battery discharge rate and usable time.",
"PV charge controller time estimation.",
"Power bank charging time",
"10000 mAh (10 Ah), 5 V, input 2 A: energy 50 Wh, charging at 2 A×5 V=10 W gives an ideal 5 h; accounting for 0.9 efficiency and the slower constant-current/constant-voltage tail, the actual time is about 5.5-6 h. Tip: a high current is faster but generates heat, and overcharge protection reduces the current.",
"Is the time simply the capacity in Ah divided by the current?",
"It holds approximately for constant current; but batteries have a cutoff voltage and efficiency, and the final stage switches to constant voltage with a reduced current, so the actual time is longer.",
"What is the C rate?",
"The C rate is capacity divided by current; 1C means fully discharged in 1 hour. The higher the rate, the greater the power, but the usable capacity often drops slightly and heat generation increases.",
'About the "Charging Time Estimation"',
"Charging time estimation tool: enter the battery capacity, charging current, battery voltage and charging efficiency to compute the charging time, battery energy and charging power, suitable for lithium battery charging planning for phones, laptops, power banks, etc.",
"Supports custom charging efficiency and current charge level",
"Charging time displayed in hours + minutes",
"Battery energy (Wh) and charging power (W) calculation",
"Charge rate (C) and charging mode determination",
"Phone/tablet charging time planning",
"Power bank charging time estimation",
"Charger power selection reference",
"Battery charging scheme design",
"Charging current",
"Charging efficiency",
"Current charge percentage",
],
'heat-pump-cop': [
"⚡ Heat Pump Efficiency Ratio Calculator",
"Compute the heat pump's COP (heating efficiency ratio) and EER (cooling efficiency ratio) and compare the energy-saving benefits",
'📖 View the "Heat Pump Efficiency Ratio Calculator User Guide"',
"🔥 Heating COP",
"❄️ Cooling EER",
"Heating capacity (kW)",
"Input power (kW)",
"Cooling capacity (kW)",
"Annual operating hours (h)",
"COP (heating efficiency ratio)",
"⚡ Energy-Saving Benefit Comparison",
"Compare the energy consumption and electricity cost of a heat pump with an electric/gas boiler (based on the same heating output)",
"📋 COP/EER Energy Efficiency Grading Standard",
": heating efficiency ratio = heating output ÷ input power. The higher the value, the more energy-efficient.",
": cooling efficiency ratio = cooling output ÷ input power. The higher the value, the more energy-efficient.",
"The COP of a heat pump is usually 2.5-5.0, far higher than an electric boiler (COP≈0.95) and a gas boiler (COP≈0.85).",
"📚 In-Depth Analysis: Heat Pump Efficiency Ratio Calculator",
"Use EER in cooling mode to estimate air conditioner power consumption.",
"Compare the energy efficiency of a heating/cooling heat pump and a split air conditioner.",
"Evaluate the annual cost by SCOP/SEER.",
"Cooling EER estimation",
"Cooling 5 kW, input 1.5 kW: EER≈3.33 (about new national standard grade 3). Running at 1.5 kW for 8 h consumes 12 kWh, costing about 7 CNY. Tip: an inverter unit has a higher EER at part load, so the actual annual cost is lower than the fixed-speed estimate.",
"Are EER and COP the same thing?",
"The numerical method is the same (output/input), but EER refers to cooling and COP to heating; the seasonal versions are SEER and SCOP respectively.",
"Does grade 1 always save the most?",
"A high-efficiency unit costs more upfront; with high usage hours the difference in electricity cost is recovered faster, while with low usage the payback period is long, so weigh it by usage hours.",
'About the "Heat Pump Efficiency Ratio Calculator"',
"The Heat Pump Efficiency Ratio Calculator is an online tool in the energy and power domain. Based on standard physical and engineering formulas, it calculates accurately with reliable results.",
"Based on standard physical and engineering formulas",
"Electricity and energy data analysis",
"Electric power and energy conversion",
"Energy solution assessment assistance",
"Learning energy and electricity knowledge",
],
}

def build(slug, en_list):
    path = os.path.join(WORK, slug + '.json')
    wj = json.load(open(path, encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('!! %s length mismatch %d vs %d' % (slug, len(en_list), len(items)))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src'):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if not en or not isinstance(en, str):
            print('!! %s empty translation' % slug)
            sys.exit(1)
        if CJK.search(en) or CNP.search(en):
            print('!! %s CJK/CNP violation: %s' % (slug, en[:60]))
            sys.exit(1)
        mp[z] = en
    return mp

def write(slug, mp):
    os.makedirs(OUT, exist_ok=True)
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('name', slug)
    out = {'slug': slug, 'industry': 'energy', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

for slug, en_list in EN.items():
    write(slug, build(slug, en_list))

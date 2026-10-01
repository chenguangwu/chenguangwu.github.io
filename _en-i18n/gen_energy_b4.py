#!/usr/bin/env python3
# energy batch4 (5 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'energy')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'energy')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'joule-heating': [
"Heat Power from Current and Resistance",
"Enter the current I and resistance R to compute the Joule heating power.",
"Joule Heating Power Calculator",
"/ Joule Heating Power Calculator",
'📖 View the "Heat Power from Current and Resistance User Guide"',
"Resistance R (Ω)",
"Loss from the current's heating effect.",
"📚 In-Depth Analysis: Heat Power from Current and Resistance",
"Heat power accounting for electric water heaters/electric heaters.",
"Verifying conductor ampacity and heat safety.",
"Assessing line loss I²R.",
"2Ω heating wire power",
"Current 5 A, resistance 2 Ω: P=25×2=50 W. If a 0.5 mm² long wire with resistance 4 Ω is used by mistake at current 10 A: line loss P=100×4=400 W, and the cable heats up severely with a fire hazard. Tip: high-current circuits must have their cross-section and joints verified.",
"Why is line loss I²R rather than IR?",
"Power = voltage × current, line voltage drop = IR, loss = voltage drop × current = I²R, so the loss rises with the square of the current.",
"Is Joule heat always wasted?",
"Electric heating appliances make use of it, but Joule heat in transmission/distribution and motors is a loss that needs dissipation, i.e., an efficiency loss.",
"How to use Heat Power from Current and Resistance",
"Heat power accounting for electric heating appliances, verification of conductor ampacity and heat safety, and line loss I²R assessment.",
"What does Heat Power from Current and Resistance do?",
"Enter the current (A) and resistance (Ω); the tool computes the conductor's Joule heating power using P=I²·R, for assessing heat generation or circuit loss.",
"How do I use Heat Power from Current and Resistance?",
"What scenarios is Heat Power from Current and Resistance suitable for?",
"Joule heating power P = I²R (current squared × resistance), in watts; appliance heat generation is proportional to the square of the current.",
"Estimate the heat generation and loss of conductors/components; doubling the current increases the heat to 4 times, the core of overload risk.",
"Boundary",
"Applicable to steady resistive heating; the result is heat power, and the actual temperature rise also depends on heat dissipation; electrical safety follows the ampacity code.",
],
'energy-efficiency': [
"🧮 Energy Efficiency Calculation",
"Compute the equipment efficiency ratio (COP/EER/SEER)",
'📖 View the "Energy Efficiency Calculation User Guide"',
"Efficiency = output / input",
"Output energy (kWh)",
"Input energy (kWh)",
"Operating time (hours)",
"📚 In-Depth Analysis: Energy Efficiency Calculation",
"Compare the energy efficiency grades and annual consumption of different appliances.",
"Estimate the energy-saving ratio of a motor VFD retrofit.",
"Compare energy consumption before and after a building envelope retrofit.",
"Motor VFD energy-saving estimation",
"Constant-speed operation at 80% load, 4000 h/year, power 30 kW, average power savings 18% after VFD retrofit: annual savings ≈30×4000×0.18≈21600 kWh, about 12,500 CNY saved at 0.58 CNY. Tip: the lower the load factor and the longer the running time, the greater the VFD benefit.",
"Are energy efficiency and",
"the same thing?",
"No. Energy efficiency is the energy utilization rate, while the power factor is the phase matching of current and voltage; a low PF affects grid quality but does not directly equal low energy efficiency.",
"Why do grade-1 rated appliances save more?",
"For the same function their energy per unit output is lower, and the accumulated electricity savings over long-term use can exceed the price difference.",
'About the "Energy Efficiency Calculation"',
"Energy Efficiency Calculation is an online tool in the energy and power domain. An energy and power tool that helps compute energy consumption and power parameters.",
"How to use Energy Efficiency Calculation",
"Compare appliance and motor efficiency, estimate the energy-saving returns of VFD and envelope retrofits, and identify high-consumption items.",
"What does Energy Efficiency Calculation do?",
"Enter the cooling/heating output and input power of an air conditioner or heat pump; the tool computes the efficiency ratios COP/EER/SEER to conveniently compare the energy-saving level of different devices.",
"How do I use Energy Efficiency Calculation?",
"What scenarios is Energy Efficiency Calculation suitable for?",
],
'electrical-power': [
"Electric Power from Voltage and Current",
"Enter the voltage U and current I to compute the electric power.",
"/ Electric Power Calculator",
'📖 View the "Electric Power from Voltage and Current User Guide"',
"Voltage U (V)",
"Basic DC power formula.",
"📚 In-Depth Analysis: Electric Power from Voltage and Current",
"Verify the rated power of appliances and the circuit capacity.",
"Compute the active power of an AC load by cosφ.",
"Estimate whether a socket/breaker is overloaded.",
"220V 10A circuit power",
"Resistive load cosφ≈1: P=220×10=2200 W. With a motor cosφ=0.8: active power ≈1760 W, apparent 2200 VA, and the breaker is selected by the apparent current of 10 A. Tip: the total load of multiple circuits must be less than the incoming line capacity.",
"What is the difference between active and apparent power?",
"Active power is the power that actually does work (W), apparent power is voltage × current (VA); the difference between them for inductive loads is caused by reactive power, PF = active/apparent.",
"Are appliances rated in W or VA?",
"Resistive ones are rated in W, those with reactance are rated in VA/W with a PF; for selecting the breaker/cable it is safer to look at the current (apparent).",
"How to use Electric Power from Voltage and Current",
"Power accounting for household and workshop distribution circuits, breaker and cable capacity selection, and equipment simultaneity and load assessment.",
"What does Electric Power from Voltage and Current do?",
"Electric power calculator. Enter voltage U and current I to compute the electric power using P = U·I, suitable for instant calculation of equipment power consumption, distribution design and energy efficiency assessment.",
"How do I use Electric Power from Voltage and Current?",
"What scenarios is Electric Power from Voltage and Current suitable for?",
"Electric power P = U×I (voltage × current), applicable to DC and resistive AC; unit is watts (W).",
"Estimate the electric power and wiring/socket load from voltage and current; the larger P is, the higher the consumption.",
"Boundary",
"AC circuits with reactance require apparent/active power (P=UI·cosφ); the result is only an estimate, and electrical retrofits must follow the code and be done by professionals.",
],
'thermal-efficiency': [
"Output / Input",
"η = useful output / energy input.",
"Thermal Efficiency",
"/ Thermal Efficiency",
'📖 View the "Output / Input User Guide"',
"η = output / input",
"Useful output (kJ)",
"Energy input (kJ)",
"Constrained by the Carnot efficiency upper limit.",
"Raising η is the key to energy saving.",
"📚 In-Depth Analysis: Output / Input",
"Compare the efficiency of internal combustion engines/steam turbines/fuel cells.",
"Estimate the overall efficiency improvement from waste heat recovery.",
"Boiler thermal efficiency testing and energy-saving retrofits.",
"Boiler thermal efficiency estimation",
"Fuel heat input 100 kW, useful heat supply 85 kW: thermal efficiency 85%. If 8 kW of flue gas waste heat is recovered by a condenser, the useful heat supply rises to 93 kW and the efficiency to 93%. Tip: the lower the flue gas temperature, the more can be recovered, but it is limited by dew point corrosion.",
"Why is the actual efficiency far below Carnot?",
"Carnot efficiency",
"is the ideal upper limit; reality is limited by irreversible losses, materials and friction; combined cycles approach the limit through cascaded utilization.",
"Does waste heat recovery count as an efficiency improvement?",
"The efficiency of the original equipment is unchanged, but the overall system energy efficiency improves; it is more reasonable to compute the system efficiency from the total input and total useful output.",
],
'solar-calculator': [
"🧮 Solar Power Generation Calculation",
"Estimate the PV system's generation and revenue",
"/ Solar Power Generation",
'📖 View the "Solar Power Generation Calculation User Guide"',
"Generation = area × irradiance × efficiency",
"City selection (peak sunshine hours)",
"Module power (W)",
"System efficiency (%)",
"Subsidy (CNY/kWh)",
"📚 In-Depth Analysis: Solar Power Generation Calculation",
"Assess whether installing PV is worthwhile when the household monthly electricity bill is high.",
"Compare the two revenue models: full feed-in versus self-consumption with surplus feed-in.",
"Assess the economics of raising the self-consumption rate by adding storage.",
"Household PV estimation for 600 kWh monthly electricity use",
"Monthly electricity 600 kWh, local annual generation 1300 kWh/kWp, module price 3.5 CNY/W, electricity price 0.58 CNY/kWh: recommended capacity about 5.5 kWp, annual generation about 7150 kWh, covering about 80% of consumption, initial investment about 19250 CNY, payback about 7-9 years. Tip: with subsidies and escalating tariffs the payback is shorter.",
"Which yields more, self-consumption or surplus feed-in?",
"Self-consumption saves the retail electricity price, usually higher than the feed-in tariff, so raising the self-use rate (adding storage, shifting usage off-peak) yields better returns; feed-in serves only to dispose of surplus power.",
"Which factors most affect the payback period?",
"Local irradiation, self-use ratio, initial investment unit price and electricity price/subsidy policy; with high irradiation and a high self-use ratio the payback period shortens notably.",
'About the "Solar Power Generation Calculation"',
"Solar Power Generation Calculation. An energy and power tool that helps compute energy consumption and power parameters.",
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

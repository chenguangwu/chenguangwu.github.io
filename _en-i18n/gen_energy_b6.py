#!/usr/bin/env python3
# energy batch6 (5 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'energy')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'energy')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'energy-cost': [
"Electricity Cost from Power, Duration and Tariff",
"Enter the power P (watts), usage duration h (hours) and electricity price to compute the electricity cost.",
"Cost = P(kW)·h·unit price",
"/ Electricity Cost Calculator",
"Electricity Cost Calculator",
'📖 View the "Electricity Cost from Power, Duration and Tariff User Guide"',
"Electricity cost = P × t × price",
"Duration h (hours)",
"Convert to kilowatt-hours first, then bill.",
"1.5kW×24h×0.6 → 21.6 CNY.",
"📚 In-Depth Analysis: Electricity Cost from Power, Duration and Tariff",
"Estimate the monthly bill and the tiered impact.",
"Compare peak-valley time-of-use pricing strategies.",
"Estimate the cost savings of an energy-saving retrofit.",
"Time-of-use tariff optimization",
"Daily usage 30 kWh, of which 20 kWh is shifted to the valley segment (0.3 CNY) instead of the peak segment (0.9 CNY): original 30×0.58=17.4 CNY, after optimization 10×0.9+20×0.3=15 CNY, saving 2.4 CNY/day, about 876 CNY/year. Tip: storage/smart scheduling can amplify the returns.",
"How is the tiered tariff calculated?",
"Priced in segments by cumulative usage, with the incremental portion at a higher unit price, so the cost in high-usage months rises non-linearly.",
"Who is peak-valley pricing suitable for?",
"Users with shiftable loads (storage, water heating, EV chargers) benefit greatly; rigid real-time loads benefit little.",
],
'energy-payback': [
"Investment / Annual Savings",
"Payback period = initial investment / annual savings.",
"/ Energy-Saving Payback Period",
"Energy-Saving Payback Period",
'📖 View the "Investment / Annual Savings User Guide"',
"Payback period = investment / annual savings",
"Annual savings (CNY/year)",
"Static payback ignores discounting.",
"With discounting, use the dynamic payback period.",
"📚 In-Depth Analysis: Investment / Annual Savings",
"Compare the PV system EPT and financial payback period.",
"Compare the EPT of different technology routes (monocrystalline vs thin film).",
"Assess the impact of adding storage on the overall EPT.",
"PV system energy payback time",
"Module manufacturing energy about 400 kWh/kWp, system annual generation 1300 kWh/kWp: EPT≈400/1300≈0.31 years (about 4 months), far shorter than the 25-year lifespan, giving a high net energy return. Tip: even including the manufacturing energy of brackets/inverters, the EPT is usually <2 years.",
"Which is longer, EPT or the financial payback period?",
"The financial payback period is usually longer (affected by the electricity price and initial investment); EPT looks only at energy and is an environmental sustainability indicator.",
"What affects the EPT?",
"Manufacturing energy, system lifespan and local solar/wind resources; high-resource areas have a shorter EPT.",
],
'convert-emission': [
"🌾 Greenhouse Gas Emission Conversion (CO₂ Equivalent)",
"Greenhouse gas CO₂ equivalent (CO₂e = mass × GWP, IPCC AR5 100-year values; conversion at equal mass)",
'📖 View the "Greenhouse Gas Emission Conversion (CO₂ Equivalent) User Guide"',
"CO₂ equivalent = mass × GWP",
"CO₂ equivalent",
"CH₄ (100-year)",
"N₂O (100-year)",
"📚 In-Depth Analysis: Greenhouse Gas Emission Conversion (CO₂ Equivalent)",
"Convert between kg and t CO₂e.",
"Convert methane to CO₂e by GWP.",
"Unify units across activity data.",
"Methane GWP conversion",
"Methane 1 t, 100-year GWP=28: CO₂e=28 t. If a process emits 0.5 t CH₄, that is equivalent to 14 t CO₂e. Tip: the GWP value (20/100-year) makes a large difference, so the basis must be stated.",
"What is GWP?",
"Global Warming Potential, measuring the warming capacity of a unit mass of gas relative to CO₂; CH₄ and N₂O are far higher than CO₂ and are used to convert to CO₂e.",
"Why use CO₂e?",
"It unifies the warming effects of different greenhouse gases into CO₂ equivalent, making it easy to sum and compare emission reductions.",
'About the "Greenhouse Gas Emission Conversion (CO₂ Equivalent)"',
"Greenhouse Gas Emission Conversion (CO₂ Equivalent). An energy and power tool that helps compute energy consumption and power parameters.",
],
'wind-power-physics': [
"Wind Power from Air Density, Swept Area and Wind Speed",
"Enter the air density ρ, swept area A and wind speed v to compute the wind power.",
"Wind Power Density Calculator",
"/ Wind Power Density Calculator",
'📖 View the "Wind Power from Air Density, Swept Area and Wind Speed User Guide"',
"Swept area A (m²)",
"Wind speed v (m/s)",
"Power is proportional to the cube of the wind speed.",
"📚 In-Depth Analysis: Wind Power from Air Density, Swept Area and Wind Speed",
"Understand the theoretical maximum wind energy capture with the Betz limit.",
"Optimize blade speed and noise by tip speed ratio.",
"Interpret the difference between the manufacturer's power curve and actual generation.",
"Betz limit example",
"An ideal rotor can capture at most 59.3% of the incoming kinetic energy (the Betz limit); a real three-blade horizontal-axis turbine is limited by aerodynamic losses, drivetrain and generator efficiency, so the overall efficiency is often 35%-45%. After the rated wind speed the power curve limits the output to the rated value up to the cut-out wind speed.",
"Why shut down at the cut-out wind speed?",
"Above the design wind speed the loads are too large, so shutdown protects structural safety; the cut-out wind speed is usually around 25 m/s.",
"What is the tip speed ratio?",
"The ratio of the blade tip linear speed to the wind speed; an optimal range keeps the blades at an efficient angle of attack; too small is inefficient and too large raises noise and loads.",
],
'solar-panel-power': [
"Area × Irradiance × Efficiency",
"PV Array Power",
"/ PV Array Power",
'📖 View the "Area × Irradiance × Efficiency User Guide"',
"PV output power: P = module area A (m²) × irradiance G (W/m²) × module efficiency η; the actual system generation must also be multiplied by the system efficiency and converted by peak sunshine hours; for example, at the standard irradiance of 1000 W/m² a 2 m² module with 20% efficiency outputs about 400 W.",
"Array area A (m²)",
"Standard test condition G=1000 W/m².",
"Actual results are affected by temperature and shading.",
"📚 In-Depth Analysis: Area × Irradiance × Efficiency",
"When designing the number of strings, verify that the array total power matches the inverter's rated input.",
"Estimate the power derating from the temperature coefficient in a high-temperature environment.",
"Compare the power per unit area of monocrystalline/polycrystalline/thin-film modules.",
"Array of 10 × 400W modules",
"10 monocrystalline 400 W modules in series: STC total power 4000 W; at an ambient temperature of 45℃ with a 20℃ rise and a temperature coefficient of −0.35%/℃, the power derates by about 7% to about 3720 W. It is recommended that the inverter rating be slightly above 4000 W with an MPPT voltage window covering the string open-circuit voltage.",
"Under what conditions is the module rated power measured?",
"Measured under STC (irradiance 1000 W/m², cell temperature 25℃, AM1.5); actual outdoor conditions are often below the rating due to high temperature and low irradiance, so leave a design margin.",
"Why doesn't the inverter power have to equal the array power?",
"Because sunlight rarely reaches STC simultaneously and there are line losses/mismatch, sizing the inverter at 0.8-1.0 of the array power balances cost and generation and avoids long-term light-load inefficiency.",
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

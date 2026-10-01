#!/usr/bin/env python3
# energy batch7 (5 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'energy')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'energy')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'heat-energy-q': [
"Heat from Mass, Specific Heat and Temperature Rise",
"Enter the mass m, specific heat c and temperature difference ΔT to compute the heat.",
"Sensible Heat (Specific Heat) Calculator",
"/ Sensible Heat (Specific Heat) Calculator",
'📖 View the "Heat from Mass, Specific Heat and Temperature Rise User Guide"',
"Specific heat c (J/(kg·K))",
"The specific heat of water is about 4186 J/(kg·K).",
"📚 In-Depth Analysis: Heat from Mass, Specific Heat and Temperature Rise",
"Energy needed to boil water/heat a liquid.",
"Estimate the thermal storage of building envelopes.",
"Process cooling load accounting.",
"Heat for boiling water",
"2 kg water, specific heat 4.186 kJ/(kg·℃), heating up 80℃ (20→100): Q=2×4.186×80≈669 kJ≈0.186 kWh. Tip: a phase change (boiling) also requires a latent heat of vaporization of about 2260 kJ/kg, so continued boiling after it reaches the boil consumes more heat.",
"What is specific heat capacity?",
"The heat needed to raise a unit mass by 1℃; water is about 4.186 kJ/(kg·℃), far greater than most solids, which is why water is often used as a heat storage medium.",
"Why does boiling cost more heat than raising the temperature?",
"Latent heat of phase change",
"It absorbs heat without rising in temperature; the latent heat of vaporization of water is about 2260 kJ/kg, far greater than that needed to raise liquid temperature.",
],
'energy-from-power': [
"Electric Energy from Power and Duration",
"Enter the power P (watts) and usage duration t (hours) to compute the electric energy (kWh).",
"Electric Energy (Consumption) Calculator",
"/ Electric Energy (Consumption) Calculator",
'📖 View the "Electric Energy from Power and Duration User Guide"',
"Duration t (hours)",
"📚 In-Depth Analysis: Electric Energy from Power and Duration",
"Estimate daily/monthly energy from the rated power.",
"Charging",
"electric power",
"× time gives the energy charged in.",
"Integrating the generation power curve gives the daily generation.",
"5kW unit generating for 8h",
"P=5 kW, t=8 h: E=40 kWh. If for 2 h it is only 2 kW, then E=5×6+2×2=34 kWh. Tip: with fluctuating power, piecewise accumulation is more accurate; multiplying over the whole period overestimates.",
"How to distinguish the units of power and energy?",
"Power in kW is a rate, while energy in kWh is power × time; like vehicle speed and distance.",
"Can the peak power be multiplied by time directly?",
"No. It is actually often at part load, so compute by the operating curve or average power, otherwise you overestimate the energy.",
],
'carnot-efficiency': [
"Theoretical Maximum Thermal Efficiency from Hot/Cold Source Temperatures",
"Enter the cold source temperature T_c and hot source temperature T_h (Kelvin) to compute the Carnot efficiency.",
"Carnot Efficiency Calculator",
"/ Carnot Efficiency Calculator",
'📖 View the "Theoretical Maximum Thermal Efficiency from Hot/Cold Source Temperatures User Guide"',
"Cold temperature T_c (K)",
"Hot temperature T_h (K)",
"The actual heat engine efficiency is below the Carnot limit.",
"📚 In-Depth Analysis: Theoretical Maximum Thermal Efficiency from Hot/Cold Source Temperatures",
"Understand the efficiency upper limit of thermal/nuclear units.",
"Compare the theoretical gain of different temperature tiers (e.g., supercritical).",
"Teaching demonstration: the temperature ratio determines the efficiency.",
"600℃ steam cycle upper limit",
"Th=600+273=873 K, Tc=30+273=303 K: η_carnot=1−303/873≈65.3%. Actual supercritical units are about 45%-47%, below the Carnot limit due to irreversible losses. Tip: raising Th (higher steam parameters) is the main path to improving efficiency.",
"Can the Carnot efficiency be achieved?",
"No, it is the ideal reversible cycle upper limit; actual cycle efficiency must be below it, and it is used to judge the room for improvement.",
"Why is raising the heat source temperature most effective?",
"η rises monotonically with Th and is sensitive to a decrease in Tc, so parameter-raising technologies such as supercritical/double reheat have long dominated thermal power efficiency improvements.",
],
'fuel-heat-value': [
"Mass × Lower Heating Value",
"Fuel Calorific Energy",
"/ Fuel Calorific Energy",
'📖 View the "Mass × Lower Heating Value User Guide"',
"Heat = mass × lower heating value",
"Lower heating value (kJ/kg)",
"The calorific value of standard coal is about 29307 kJ/kg.",
"📚 In-Depth Analysis: Mass × Lower Heating Value",
"Estimate the fuel quantity for coal/gas boilers.",
"Compare the heat per unit cost of different fuels.",
"Convert to standard coal consumption.",
"Natural gas calorific value conversion",
"The lower heating value of natural gas is about 9.6 kWh/m³, with a daily use of 20 m³: heat supply ≈192 kWh (≈173 kWh at 90% boiler efficiency). Converted to standard coal: 1 kgce≈8.14 kWh, about 21 kgce/day. Tip: the difference between higher and lower heating values lies in the latent heat of vaporization of water.",
"What is the difference between higher and lower heating values?",
"The higher heating value includes the latent heat of condensation of the combustion water vapor, the lower does not; engineering commonly uses the lower heating value (LHV) as it is closer to the actually usable heat.",
"Why convert to standard coal?",
"To unify the energy accounting basis for side-by-side comparison and statistics; 1 kgce=29307 kJ≈8.14 kWh.",
],
'energy-consumption': [
"Power × Time",
"Energy Consumption Calculation",
"/ Energy Consumption Calculation",
'📖 View the "Power × Time User Guide"',
"Energy consumption = power (W) × usage time (hours) ÷ 1000, i.e., 1 kWh equals running 1000 W for 1 hour; electricity cost = energy consumption × price; average hourly consumption = energy consumption ÷ usage hours; monthly cost can be estimated on a 30-day basis.",
"Note the W→kW conversion by dividing by 1000.",
"Peak and valley prices differ.",
"📚 In-Depth Analysis: Power × Time",
"Break down the household energy bill.",
"Itemized metering for shops/workshops to find waste.",
"Compare before and after an energy-saving retrofit.",
"Household itemized energy consumption",
"Fridge 1 kWh/day, air conditioner 9 kWh/day, others 5 kWh/day: daily total 15 kWh, monthly 450 kWh, annual 5475 kWh. The fridge accounts for about 6.7% while the air conditioner is nearly 60%, so prioritize optimizing the air conditioner and standby. Tip: only itemized metering enables precise energy saving.",
"How to quickly reduce energy consumption?",
"First find the largest share (often air conditioning/heating/hot water), optimize its usage and equipment efficiency, then clear standby—this yields the highest returns.",
"How to estimate annual energy consumption more accurately?",
"Weight itemized data by season (high in summer/winter, low in spring/autumn), or use actual smart meter measurements; both are more accurate than simply multiplying by 12.",
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

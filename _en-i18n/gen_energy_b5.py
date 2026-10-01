#!/usr/bin/env python3
# energy batch5 (5 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'energy')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'energy')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'fuel-cost': [
"Quantity × Unit price",
"Cost = quantity × unit price.",
"Fuel Cost",
"/ Fuel Cost Calculation",
"Fuel Cost Calculation",
'📖 View the "Quantity × Unit Price User Guide"',
"Cost = quantity × unit price",
"Fuel quantity (L)",
"Unit price (CNY/L)",
"Cost per 100 km = 10 × unit distance cost.",
"For electricity/gas, substitute the units similarly.",
"📚 In-Depth Analysis: Quantity × Unit Price",
"Estimate the gas heating season cost.",
"Unit electricity cost of a diesel/gas generator.",
"Compare the cost of electric heating and gas heating.",
"Gas heating cost",
"Natural gas 2.8 CNY/m³, calorific value 9.6 kWh/m³, boiler efficiency 90%: effective heat cost ≈2.8/(9.6×0.9)=0.324 CNY/kWh heat. At the same heat, electric heating is 0.58 CNY/kWh, so gas is cheaper. Tip: when the electricity price is low or a heat pump has COP>1.8, electric heating may overtake.",
"Why is conversion by calorific value fairer?",
"Unit prices of different fuels are not comparable; only by converting to unit energy cost can they be compared side by side.",
"How to choose between a heat pump and gas?",
"A heat pump is cheaper when COP > gas efficiency / gas price · electricity price; in low-temperature zones heat pump performance degrades, so field comparison is needed.",
],
'daily-irradiation': [
"Peak × Equivalent Sunshine Hours",
"Daily Irradiation",
"/ Daily Irradiation Estimation",
"Daily Irradiation Estimation",
'📖 View the "Peak × Equivalent Sunshine Hours User Guide"',
"Daily irradiation = peak × equivalent sunshine hours",
"Peak irradiance (W/m²)",
"Equivalent full-load hours (h)",
"China's class-1 resource zones have about 1600 equivalent hours/year.",
"The equivalent hours include weather derating.",
"📚 In-Depth Analysis: Peak × Equivalent Sunshine Hours",
"Before installing household rooftop PV, use the local peak sunshine to estimate the system capacity and payback period.",
"Compare the tilt-plane irradiation gain under different orientations/tilt angles to optimize the array layout.",
"Match storage when designing an off-grid PV system",
"with the average daily generation.",
"Rooftop PV irradiation estimation for a location",
"Input: monthly average peak sunshine 4.2 h/day, module area 20 m², efficiency 21%, system loss 15%: average daily generation ≈20×4.2×0.21×0.85≈15.0 kWh/day, annual generation about 5475 kWh. Tip: actual results are affected by shading, dust and the temperature coefficient, so using a performance ratio of about 0.8 is safer.",
"Are peak sunshine hours the same as actual sunshine time?",
"No. Peak sunshine hours convert the whole day's irradiation into equivalent hours at the standard 1 kW/m², usually far less than the daylight duration, and are the core input for PV capacity estimation.",
"How to choose the tilt angle?",
"Approximately using the local latitude gives a good year-round result; if winter usage dominates, increasing the tilt slightly can raise cold-season irradiation, but consider shading and snow load.",
],
'battery-life': [
"⚡ Battery Life Calculation",
"Compute the device battery usage time",
"/ Battery Life",
'📖 View the "Battery Life Calculation User Guide"',
"Runtime = capacity (Wh) / power (W)",
"Common devices",
"Battery capacity (mAh)",
"Average power (W)",
"Battery efficiency (%)",
"📚 In-Depth Analysis: Battery Life Calculation",
"Estimate the single-charge usage time of portable devices by typical power.",
"Estimate the off-grid support time of a storage system by the load profile.",
"Compare the runtime difference of batteries of different capacities.",
"Laptop battery life estimation",
"Battery 60 Wh, average power 15 W, power efficiency 0.9: usable ≈60×0.9/15=3.6 h. Tip: under high load (gaming/rendering) the power doubles and the runtime halves, and low temperature also reduces the usable capacity.",
"Why is the actual runtime often below the rated one?",
"The rating is mostly under light load/ideal conditions; actual results are affected by screen brightness, temperature rise, aging and the discharge cutoff; deep discharge also accelerates degradation.",
"Does the depth of discharge affect the lifespan?",
"Yes. Shallow charge/discharge of a lithium battery (e.g., 20%-80%) gives a notably longer cycle life than full charge/discharge; storage systems often limit the DoD to extend life.",
'About the "Battery Life Calculation"',
"Battery Life Calculation. An energy and power tool that helps compute energy consumption and power parameters.",
],
'three-phase-power': [
"Three-phase P = √3 × line voltage × line current × power factor.",
"Three-Phase Power",
"/ Three-Phase Active Power",
"Three-Phase Active Power",
'📖 View the "Three-Phase Power User Guide"',
"Line voltage U (V)",
"Line current I (A)",
"A line voltage of 380 V is a common low voltage.",
"Line loss is ignored.",
"📚 In-Depth Analysis: Three-Phase Power",
"Three-phase",
"and current accounting.",
"Evaluation of the distribution transformer load rate.",
"Approximate power estimation for unbalanced loads.",
"380V motor power",
"U_L=380 V, I_L=30 A, cosφ=0.85: P=1.732×380×30×0.85≈16770 W≈16.8 kW. Tip: three-phase imbalance increases the neutral current and losses, so distribute the load evenly.",
"Why does three-phase power have a √3?",
"It is derived from the three-phase phasor relationships; the line voltage is √3 times the phase voltage, and the total power is the sum of the three phases, which simplifies to √3·U_L·I_L·cosφ.",
"When does the neutral wire become live?",
"When the three phases are unbalanced or single-phase loads are concentrated, the neutral carries current; a broken neutral even causes the phase voltage to drift and burn equipment, so reliable grounding and balancing are essential.",
],
'power-consumption': [
"🧮 Electricity Usage Calculation",
"Compute home appliance energy consumption and electricity cost",
'📖 View the "Electricity Usage Calculation User Guide"',
"Usage = P × t",
"Quick add",
"hours/day",
"+ Add appliance",
"👆 Add appliance",
"📚 In-Depth Analysis: Electricity Usage Calculation",
"Estimate the monthly consumption of home appliances.",
"Statistics of standby and operating energy of office equipment.",
"Compare the electricity cost difference between different usage habits.",
"Air conditioner monthly consumption",
"A 1.5 kW air conditioner running 6 h/day: daily consumption 9 kWh, monthly 270 kWh, electricity cost about 157 CNY (0.58 CNY/kWh). Switching to a more efficient unit or raising the temperature by 1℃ saves 10%, about 16 CNY/month. Tip: an inverter unit is more efficient at part load.",
"Is power × time the electricity cost?",
"It gives the energy in kWh; multiply by the electricity price to get the cost. Note that under tiered tariffs the incremental price is higher.",
"Does standby count as power consumption?",
"Yes. Standby is small but accumulates considerably over the year; a centralized switch can save it.",
'About the "Electricity Usage Calculation"',
"Electricity Usage Calculation is an online tool in the energy and power domain. An energy and power tool that helps compute energy consumption and power parameters.",
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

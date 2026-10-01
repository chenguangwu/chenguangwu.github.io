#!/usr/bin/env python3
# eco batch1 (5 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'eco')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'eco')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

# 行业级固定尾句（全站 FAQ dd 统一后缀，逐条拼接保持一致）
BOIL = ("Results are estimated according to public standards and environmental factors, "
        "for science outreach, teaching and emission-reduction estimates; actual accounting "
        "should follow official guidelines (such as the GHG Protocol and provincial carbon "
        "emission factors) and measured data.")

EN = {
'afforestation-cost': [
"🌳 Afforestation Carbon Sink Investment",
"Estimate the investment and annual carbon uptake of a forestation project.",
'📖 View the "Afforestation Carbon Sink Investment Guide"',
"Number of trees",
"Cost per tree (CNY)",
"Project term (years)",
"Investment = trees × cost per tree; annual uptake = trees × 18.3",
"A carbon sink project also needs to account for maintenance and monitoring costs.",
"📚 In-Depth Analysis: Afforestation Carbon Sink Investment",
"Carbon sink project sizing: enter the forestation area and expected annual carbon sequestration, then estimate project revenue and payback period using the carbon price.",
"Investment comparison: enter management costs for different species or densities and compare the cost per unit of carbon sink.",
"Teaching demo: show how carbon price volatility affects project feasibility.",
"Example: forestation of 100 mu with annual sequestration of 5 tCO₂/mu and a carbon price of 60 CNY/tCO₂ gives annual carbon revenue = 100×5×60 = 30000 CNY; deduct management costs to obtain the net return.",
"Where does the carbon sink volume come from?",
"It is determined by species, stand age and site conditions; common afforestation carbon-sink methodologies give the annual sequestration rate, with the value filed with the competent authority taking precedence. " + BOIL,
"Which carbon price should be used?",
"You may reference CCER (Chinese Certified Emission Reduction) or local carbon market prices; they fluctuate widely, so quoting a range is more prudent in a calculation. " + BOIL,
"Is only the forestation cost counted?",
"Tending and management, monitoring and verification, and transaction costs should also be included; only a complete accounting approaches the true unit carbon cost. " + BOIL,
],
'aqi': [
"🌱 AQI Health Level",
"Give a health impact level and advice based on the AQI value.",
'📖 View the "AQI Health Level Guide"',
"AQI value",
"Outdoor activity hours",
"AQI level: Excellent / Good / Light / Moderate / Heavy / Severe pollution",
"The PM2.5 estimate is an empirical formula, not an official conversion.",
"📚 In-Depth Analysis: AQI Health Level",
"Daily health: enter the day's AQI to judge whether outdoor exercise is suitable and whether sensitive groups need protection.",
"Alert interpretation: enter hourly AQI during a pollution episode to observe the points where the level jumps.",
"Teaching demo: explain the meaning of the AQI categories (0–50 Excellent, 51–100 Good, 151–200 Moderate, etc.).",
"Example: AQI=158 is moderate pollution (level 4); reduce strenuous outdoor exercise and keep children and the elderly indoors as much as possible.",
"How do you remember the AQI categories?",
"0–50 Excellent, 51–100 Good, 101–150 Light, 151–200 Moderate, 201–300 Heavy, >300 Severe — six levels in total. " + BOIL,
"What is the relation to PM2.5?",
"AQI is converted from several pollutants such as PM2.5, PM10 and ozone; PM2.5 is often the primary pollutant and the two correspond non-linearly. " + BOIL,
"Who should be most careful?",
"The elderly, children, pregnant women and people with heart or lung disease are more sensitive to health impacts and should take protective measures early when the level rises. " + BOIL,
],
'aqi-converter': [
"🔄 AQI Category Conversion",
"Convert between the air quality index (AQI) and pollutant concentrations (HJ 633-2012)",
'📖 View the "AQI Category Conversion Guide"',
"AQI → concentration",
"Pollutant type",
"Pollutant concentration",
"📊 AQI category standards",
"AQI range",
"Health impact",
"Excellent",
"Air quality is satisfactory",
"Good",
"Acceptable; sensitive groups should take care",
"Light pollution",
"Symptoms worsen in sensitive groups",
"Moderate pollution",
"Affects people with heart or respiratory disease",
"Heavy pollution",
"Health is affected for everyone",
"Severe pollution",
"Maroon",
"Health alert; avoid outdoor activity",
"📚 In-Depth Analysis: AQI Category Conversion",
"Concentration to AQI: enter a PM2.5 or other concentration and apply the piecewise linear formula to obtain the IAQI.",
"Reverse lookup: back-calculate the pollutant concentration cap from a target AQI level to help judge compliance.",
"Teaching demo: illustrate the piecewise breakpoint interpolation algorithm.",
"Example: PM2.5=75 μg/m³ falls in the 35.5–75.5 band, giving IAQI≈100 (the boundary between Good and Light pollution), indicating a level close to light pollution.",
"How is the IAQI computed?",
"For each pollutant, interpolate linearly between adjacent breakpoints: IAQI=(Ihi−Ilo)/(Chi−Clo)×(C−Clo)+Ilo. " + BOIL,
"Is the AQI the maximum or the average?",
"The daily AQI is the maximum IAQI across pollutants, and that pollutant is the primary pollutant. " + BOIL,
"Are different standards interchangeable?",
"China's HJ 633 and the US standard use different bands, so conversions across standards must be recomputed rather than reused directly. " + BOIL,
'About "AQI Category Conversion"',
"AQI Category Conversion is an online tool in the scientific research field. A scientific research tool using standard scientific formulas for accurate calculation.",
],
'battery-storage': [
"🧊 Battery Storage Capacity",
"Estimate usable energy from capacity, voltage and depth of discharge.",
'📖 View the "Battery Storage Capacity Guide"',
"Capacity (Ah)",
"Depth of discharge (%)",
"E = capacity (Ah) × voltage (V) / 1000 × depth of discharge",
"A higher DoD gives more usable capacity but shortens battery life.",
"📚 In-Depth Analysis: Battery Storage Capacity",
"Home backup: enter the ",
" and the daily electricity curve to estimate the supported duration.",
"Off-grid sizing: enter PV + storage parameters to judge whether the night-time load can be covered.",
"Teaching demo: show the relation capacity (kWh) = power (kW) × duration (h).",
"Example: a 10 kWh battery with a 1 kW average load supplies about 10 h (ignoring losses); in practice the depth of discharge limits it to about 8–9 h.",
"What is the difference between capacity and power?",
"kWh is energy (how much can be stored) while kW is power (how fast it can be delivered); the same battery lasts a shorter time at high power. " + BOIL,
"How does depth of discharge matter?",
"Lithium batteries are usually limited to 80–90% DoD, so usable capacity is below the nominal value and sizing should be based on usable energy. " + BOIL,
"What about efficiency losses?",
"Charging and discharging have an 85–95% round-trip efficiency, and long-duration storage must include those losses. " + BOIL,
],
'carbon-forest': [
"📐 Carbon-Neutral Forest Area",
"Estimate the trees and forest land needed to offset annual emissions.",
'📖 View the "Carbon-Neutral Forest Area Guide"',
"Annual emissions (kgCO₂)",
"Annual uptake per tree (kg)",
"Trees = annual emissions / uptake per tree; forest land = trees / density",
"This is a rough estimate and does not account for forest carbon sink decay.",
"📚 In-Depth Analysis: Carbon-Neutral Forest Area",
"Event carbon neutrality: enter the emissions and use the annual forest sequestration rate to find the required forestation area and number of years.",
"Option comparison: compare the cost and area of forestation against buying CCER and other offset paths.",
"Teaching demo: show the balance between emissions and the carbon sequestration capacity of forest land.",
"Example: with annual emissions of 1000 tCO₂ and forest sequestration of 5 tCO₂/mu·year, about 200 mu of forest land sequestering continuously is needed to offset that year.",
"What sequestration rate should be used?",
"It varies with species and stand age; common methodologies give a range (for example 1–10 tCO₂/mu·year), and the filed value takes precedence. " + BOIL,
"Can planting this year offset this year?",
"Trees grow in cycles and the carbon sink is credited in stages; neutralizing the current year usually requires pre-purchased carbon credits or multi-year accumulation. " + BOIL,
"Is forestation alone enough?",
"Emission reduction takes priority over offsetting; carbon sinks are mainly used to neutralize the remaining hard-to-abate emissions and should not replace direct reductions. " + BOIL,
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
    out = {'slug': slug, 'industry': 'eco', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

for slug, en_list in EN.items():
    write(slug, build(slug, en_list))

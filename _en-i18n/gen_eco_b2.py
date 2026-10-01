#!/usr/bin/env python3
# eco batch2 (5 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'eco')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'eco')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

BOIL = ("Results are estimated according to public standards and environmental factors, "
        "for science outreach, teaching and emission-reduction estimates; actual accounting "
        "should follow official guidelines (such as the GHG Protocol and provincial carbon "
        "emission factors) and measured data.")

EN = {
'carbon-offset': [
"♻️ Carbon Footprint Calculation and Offsetting",
"Calculate your carbon emissions and get offsetting recommendations",
"Carbon Footprint Offsetting",
"/ Carbon Footprint Offsetting",
'📖 View the "Carbon Footprint Calculation and Offsetting Guide"',
"🚗 Transport (unit: km/month)",
"Monthly emissions = transport + energy + diet + takeaway + shopping + clothing; annual emissions = monthly emissions × 12",
"Transport = private car×0.192 + bus×0.089 + short-haul flight×0.255 + long-haul flight×0.195 (kg/km, by distance); energy = electricity×0.583 (kg/kWh) + natural gas×2.04 (kg/m³); diet is an annual value (vegan 100 / mostly vegan 150 / low meat 250 / average 330 / high meat 500 kg) divided by 12 for the monthly figure; takeaway 1.5 kg per order, shopping 5 kg per order, new clothes 25 kg per item (annual value divided by 12). Determination: <2000 kg low carbon, <5000 kg in line with the global average, <8000 kg slightly high, otherwise high; offset estimate: trees = ⌈annual emissions/21⌉ (each tree absorbs about 21 kg per year), PV = ⌈annual emissions/1300⌉ kW (each kW cuts about 1300 kg per year).",
"Driving",
"Bus / metro",
"Short-haul flight",
"Long-haul flight",
"⚡ Energy use (unit: kWh/month)",
"Electricity",
"Natural gas (m³)",
"🍽️ Diet",
"Diet type",
"Vegan (lowest)",
"Vegetarian",
"Low meat",
"Average meat",
"High meat",
"Takeaway / dine-out times per month",
"🛍️ Consumption",
"Online orders per month",
"New clothes (items/year)",
"Calculate carbon footprint",
"📚 In-Depth Analysis: Carbon Footprint Calculation and Offsetting",
"Personal annual review: enter commuting distance, electricity and gas use, diet composition and consumption counts to pinpoint the biggest emission sources.",
"Household comparison: switch a petrol car to an EV or skip one flight, recalculate, and quantify the annual reduction.",
"Organizational outreach: use the monthly estimate as a baseline for staff low-carbon activities and present tree-planting and PV offset options.",
"Reproducible example: a typical daily setup",
'Input: private car 500 km/month, bus 200 km/month, electricity 200 kWh/month, natural gas 20 m³, diet "low meat", takeaway 10 times/month, shopping 5 orders/month, new clothes 8 items/year.\nTransport = 500×0.192+200×0.089 = 96+17.8 = 113.8 kg; energy = 200×0.583+20×2.04 = 116.6+40.8 = 157.4 kg;\ndiet = 250/12 ≈ 20.8 kg; takeaway = 10×1.5 = 15 kg; shopping = 5×5 = 25 kg; clothing = 8×25/12 ≈ 16.7 kg;\nmonthly total ≈ 348.7 kg, about 4.18 t per year → rated "fairly green, in line with the global average". Offset estimate: about ceil(4184/21) ≈ 200 trees, or ceil(4184/1300) ≈ 4 kW of PV.',
"How many trees are needed to offset this?",
"Based on a tree absorbing about 21 kg CO₂ per year; it can also be converted into PV capacity at about 1300 kg saved per kW per year. Both are public rule-of-thumb coefficients, for planning estimates and science outreach only; formal accounting should follow the GHG Protocol and measured data.",
"Which category usually dominates emissions?",
"For most urban households transport and electricity dominate: a private car at 0.192 kg/km and a short-haul flight at 0.255 kg/km are far above a bus at 0.089 kg/km; moving from a high-meat to a low-meat diet can cut several hundred kg more per year.",
"Can the result be used directly for carbon verification?",
"No. This tool makes a rough estimate with generic emission factors covering transport, energy, diet and consumption, and households vary widely; for disclosure or trading, use official methodologies and certified factors.",
"Air Quality Index (AQI) Category Conversion",
"Waste Reduction Calculation",
"Waste generation calculator",
'About "Carbon Footprint Offsetting"',
"Carbon Footprint Offsetting is an online tool in the environmental and ecological field. An environmental and ecological tool that helps calculate environmental indicators.",
],
'convert-air-aqi': [
"⚖️ Air Quality Index (AQI) Category Conversion",
"PM2.5 (24h, µg/m³) → AQI (US EPA piecewise linear)",
"Air Quality Index (AQI) Category Conversion",
"/ Air Quality Index (AQI) Category Conversion",
'📖 View the "Air Quality Index (AQI) Category Conversion Guide"',
"China's ambient air quality index",
"(per HJ 633-2012) divides pollution into six levels: Excellent (0–50), Good (51–100), Light pollution (101–150), Moderate pollution (151–200), Heavy (201–300), Severe (>300).",
"The AQI is obtained by taking, across pollutants, the ",
"maximum of the individual IAQI sub-indices",
"; the IAQI is linearly interpolated between the category breakpoints:",
"Pollutants included: PM₂.₅, PM₁₀, SO₂, NO₂, CO, O₃. ⚠️ For health and travel reference only; the official data released by the ecological and environmental authority prevails.",
"PM2.5 concentration",
"📚 In-Depth Analysis: Air Quality Index (AQI) Category Conversion",
"Reading a monitoring bulletin: apply ",
"Concentration Conversion",
" to the PM2.5 24h value to obtain the AQI and quickly read the pollution level and health advice.",
"Data display: convert a concentration series into AQI values and matching colour bands for an environmental dashboard or report.",
"Reproducible example: PM2.5 35 µg/m³",
'Concentration 35 falls in the breakpoint band [12.1, 35.4] → [51, 100].\nAQI = (100−51)/(35.4−12.1)×(35−12.1)+51 = 49/23.3×22.9+51 ≈ 48.2+51 = 99.2 → rounded to 99, which is "Good".\nIf the concentration is 150, it falls in [55.5, 150.4] → [151, 200]: AQI = (200−151)/(150.4−55.5)×(150−55.5)+151 ≈ 49/94.9×94.5+151 ≈ 199.8 → 200, which is "Moderate pollution".',
"Which breakpoint table is used?",
"The US EPA piecewise linear breakpoint table for 24-hour PM2.5. China's HJ 633-2012 uses different PM2.5 bands (for example 0–35 is Excellent), so the same concentration converts to a different AQI; choose the convention that suits your purpose.",
'Why does it show "over limit (>500)" at very high concentrations?',
"The breakpoint table tops out at 500.4 µg/m³; higher concentrations are beyond its range, so the tool flags them as over limit instead of extrapolating, avoiding unsupported numbers.",
"Waste Reduction Calculation",
"Waste generation calculator",
"Carbon Footprint Offsetting",
"Carbon footprint calculation and offsetting",
'About "Air Quality Index (AQI) Category Conversion"',
"Air Quality Index (AQI) Category Conversion. An environmental and ecological tool that helps calculate environmental indicators.",
],
'eco': [
"♻️ Carbon Emission Estimation",
"Estimate carbon dioxide emissions from energy consumption.",
'📖 View the "Carbon Emission Estimation Guide"',
"Coal (kg)",
"Petrol (L)",
"CO₂ = electricity×0.5703 + coal×2.62 + natural gas×2.16 + petrol×2.31",
"Coefficient unit kgCO₂e",
"Emission factors are common approximations; actual factors vary with the regional power grid.",
"📚 In-Depth Analysis: Carbon Emission Estimation",
"Personal estimate: enter annual electricity use, travel distance and diet to estimate total annual emissions.",
"Reduction priorities: compare each contribution to locate the main sources in electricity, travel and diet.",
"Teaching demo: show the ",
"Carbon Footprint",
" differences between lifestyles (for example meat-based vs vegetarian).",
"Example: 2000 kWh of electricity per year (factor 0.58 kg/kWh ≈ 1160 kg) + 10000 km of driving (about 1700 kg) + diet, totalling about 4–5 tCO₂/year.",
"Which emission factor should be used?",
"Use the local grid factor for electricity (about 0.5–0.6 kgCO₂/kWh) and fuel factors for travel, following official publications. " + BOIL,
"How does it compare with the global average per person?",
"The global average is about 4–5 tCO₂ per person, higher in developed countries; the result can be used for comparison and for setting reduction targets. " + BOIL,
"What cuts emissions fastest?",
"Prioritise high-emitting travel (drive petrol cars less) and diet (moderately reduce red meat), where each unit of effort cuts emissions more noticeably. " + BOIL,
],
'eco-10': [
"🔮 PV Emission Reduction Estimation",
"Estimate the emission-reduction benefit of solar PV generation.",
'📖 View the "PV Emission Reduction Estimation Guide"',
"Installed capacity (kW)",
"Annual equivalent full-load hours",
"Grid emission factor (kgCO₂/kWh)",
"Annual generation = installed capacity × full-load hours",
"Reduction = generation × emission factor",
"Equivalent trees are estimated at 18 kg CO₂ absorbed per tree per year.",
"📚 In-Depth Analysis: PV Emission Reduction Estimation",
"Household PV: enter the installed kW and annual equivalent utilisation hours to obtain annual generation, bill savings and emission reduction.",
"Reduction accounting: generation × grid emission factor gives the annual CO₂ reduction, used for green certificates or carbon accounting.",
"Teaching demo: show how the resource zone (equivalent hours) dominates generation.",
"Example: 10 kW, 1200 equivalent hours per year and a system efficiency of 0.8 gives annual generation ≈ 10×1200×0.8 = 9600 kWh and a reduction of ≈ 9600×0.58 ≈ 5.6 tCO₂.",
"What are equivalent full-load hours?",
"The theoretical hours of full-power generation in a year, reflecting resource quality (about 1000–1300 h in a class-III resource zone). " + BOIL,
"Why multiply by the system efficiency?",
"Module degradation, line losses, inverter losses and shading make actual generation lower than theoretical, so a performance ratio of about 0.75–0.85 is applied. " + BOIL,
"Which reduction factor?",
"Use the average emission factor of the grid where the project is located (about 0.5–0.6 kgCO₂/kWh), following official publications. " + BOIL,
],
'eco-11': [
"🌱 Traffic Congestion Carbon Emissions",
"Estimate the extra fuel and carbon emissions caused by congestion.",
'📖 View the "Traffic Congestion Carbon Emissions Guide"',
"Number of vehicles in congestion",
"Average delay (minutes)",
"Idling fuel consumption (L/h)",
"Congestion days per year",
"Extra fuel = vehicles × delay hours × idling fuel consumption",
"Emissions = fuel × 2.31 kg/L",
"Used to assess the environmental benefit of congestion management.",
"📚 In-Depth Analysis: Traffic Congestion Carbon Emissions",
"Commute estimate: enter the congested-section distance and the extra idling fuel to estimate additional emissions.",
"Management assessment: compare fuel use before and after signal optimisation to quantify the emission-reduction benefit.",
"Teaching demo: show that crawling at low speed uses markedly more fuel than steady cruising.",
"Example: 0.5 L of extra fuel per day over 250 ",
"Working Days",
" gives 125 L of extra fuel and about 125×2.3 ≈ 288 kgCO₂ of emissions per year.",
"Why does congestion burn more fuel?",
"Frequent stop-start and inefficient low-speed operation raise fuel consumption, so emissions per kilometre are clearly higher than at steady cruising speed. " + BOIL,
"Petrol or diesel factor?",
"It depends on the actual fuel: about 2.3 kgCO₂/L for petrol and about 2.7 for diesel; choose according to the vehicle type. " + BOIL,
"Can it cut emissions directly?",
"Travelling off-peak, using public transport and carpooling can noticeably cut congestion emissions and are more economical than end-of-pipe measures. " + BOIL,
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
        # 坑 28：关联卡片（related-tool）名在 EN 态被 cleanRelatedName() 截断成短形态，
        # 运行时查表键是「短形态」而非 zh_src 的长形态（`X - 领域在线工具`）⇒ 此类条目以 zh 为键。
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
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

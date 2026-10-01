#!/usr/bin/env python3
# eco batch8 (4 tools, final)
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
'wastewater-calc': [
"🧮 Wastewater Discharge Calculator",
"Compute daily wastewater discharge and total pollutant load for environmental compliance and discharge permit accounting.",
'📖 View the "Wastewater Discharge Calculator Guide"',
"Base Discharge",
"Daily discharge = flow (m³/h) × operating hours; annual discharge = daily discharge × operating days; pollutant load (kg) = concentration (mg/L) × volume (m³) / 1000",
"Unit conversion: 1 m³ = 1000 L; concentration mg/L × 1000 L = 1000 mg = 1 g, hence kg = mg/L × m³ / 1000. The six items COD, BOD₅, ammonia nitrogen, total phosphorus, suspended solids and total nitrogen are each converted by the formula above into daily discharge and annual total load, for corporate environmental compliance, discharge permits and total-load accounting; the results are not a basis for monitoring reports.",
"Discharge flow Q (m³/h)",
"Daily operating hours (h/day)",
"Operating days per year (days/year)",
"Pollutant concentration (mg/L)",
"COD concentration",
"BOD5 concentration",
"Ammonia nitrogen NH₃-N",
"Total phosphorus TP",
"Suspended solids SS",
"Total nitrogen TN",
"Daily discharge",
"= flow × daily operating hours",
"Annual discharge",
"= daily discharge × operating days",
"Pollutant load",
"= discharge volume × concentration (unit conversion: mg/L × m³ = g)",
"COD: chemical oxygen demand, a measure of organic pollution in water",
"BOD5: five-day biochemical oxygen demand, reflecting the biodegradable organic content",
"Ammonia nitrogen / total nitrogen / total phosphorus: key indicators of water eutrophication",
"⚠️ Data are for estimation reference only; the actual discharge is subject to the test results of the environmental monitoring authority.",
"📚 In-Depth Analysis: Wastewater Discharge Calculation",
"Emission accounting: enter the flow and concentrations to obtain the annual loads of COD, ammonia nitrogen and other pollutants.",
"Permit comparison: compare with the permitted discharge amount to judge whether the total load is exceeded.",
"Teaching demo: demonstrate that flow × concentration gives the load.",
"Example: a discharge of 500 m³/d at COD 300 mg/L gives a daily load of 500×0.3 = 150 kg COD.",
"How does it differ from pollution load?",
"This tool itself computes the load (flow × concentration), sharing the same basis as eco-3 and focused on the discharge side. " + BOIL,
"Is meeting the concentration limit enough?",
"Permits often limit both concentration and total amount at once; a compliant concentration with a large water volume may still exceed the total amount. " + BOIL,
"How can the discharge be reduced?",
"Source reduction plus end-of-pipe treatment (such as biological or advanced treatment) must work together. " + BOIL,
'About "Wastewater Discharge Calculation"',
"Wastewater Discharge Calculation is an online tool in the scientific research field. A scientific research tool using standard scientific formulas for accurate calculation.",
],
'water-footprint': [
"🌱 Product Water Footprint",
"Estimate the virtual water consumption of a product from its type and output for product water footprint and supply-chain assessment.",
'📖 View the "Product Water Footprint Guide"',
"Beef (kg)",
"Cotton shirts (pcs)",
"Coffee (cups)",
"Beef ≈ 15415 L/kg, cotton shirt ≈ 2700 L/piece, coffee ≈ 140 L/cup",
"Virtual water consumption is often far higher than direct water use.",
"📚 In-Depth Analysis: Product Water Footprint",
"Product accounting: enter the water use per unit product and the dilution water for pollution to obtain the water footprint.",
"Supply-chain assessment: enter data for multiple stages to locate the most water-intensive processes.",
"Teaching demo: demonstrate the concept of virtual water (water consumed in production).",
"Example: 1 kg of cotton consumes about 10000 L of water (blue + green), and beverage production involves even more virtual water from raw materials.",
"What are blue, green and grey water?",
"Blue = irrigation withdrawal, green = stored rainwater, grey = the water needed to dilute pollution; the three together make up the water footprint. " + BOIL,
"How does it differ from water use?",
"The water footprint includes the virtual water of the supply chain and is far larger than the direct end-use volume, giving a fuller picture. " + BOIL,
"How can it be reduced?",
"Choosing low-water raw materials, improving process water efficiency and reusing reclaimed water can lower a product's water footprint. " + BOIL,
],
'water-saving': [
"🌱 Daily Water Saving Calculator",
"Estimate cumulative water saved by efficient fixtures and habits in homes and public buildings.",
'📖 View the "Daily Water Saving Calculator Guide"',
"Daily water use per capita (L)",
"Water-saving share (%)",
"Saving = per capita × people × days × water-saving share",
"Replacing fixtures with water-saving ones and taking shorter showers both raise the share.",
"📚 In-Depth Analysis: Daily Water Saving",
"Fixture replacement: enter the difference between water-saving and conventional fixtures plus the usage count to obtain daily and annual savings.",
"Behavioural saving: enter parameters such as shorter showers and double-sided printing to estimate the total.",
"Teaching demo: show how small habits add up to large water savings.",
"Example: a water-saving toilet saves 4 L per flush and 8 flushes a day, giving an annual saving of ≈4×8×365 = 11680 L ≈ 11.7 m³.",
"Does it only count fixtures?",
"Fixtures and habits together determine the result; this tool lets you enter them separately and add them up for a fuller picture. " + BOIL,
"How does it relate to the ",
"Water-Saving Rate",
"?",
"The water-saving rate = (original − current) / original, while this tool computes the absolute volume; the two are complementary. " + BOIL,
"Can reclaimed water be used?",
"Using reclaimed water for flushing and greening can further reduce fresh water use, but requires supporting pipe networks and water-quality assurance. " + BOIL,
],
'wind-power': [
"⛅ Wind Power Output Calculator",
"Compute wind turbine output power from swept area, wind speed and air density, with cut-in and cut-out speed limits.",
'📖 View the "Wind Power Output Calculator Guide"',
"Wind speed (m/s)",
"Rotor diameter (m)",
"Power coefficient",
"In practice it is limited by cut-in and cut-out wind speeds and turbulence.",
"📚 In-Depth Analysis: Wind Power Estimation",
"Wind farm estimate: enter the installed capacity and the capacity factor to estimate annual generation and revenue.",
"Resource comparison: enter parameters for different wind resource zones to compare the output.",
"Teaching demo: demonstrate the key role of the capacity factor (actual vs theoretical full output).",
"Example: 2 MW, a capacity factor of 0.3 and 8760 h a year give annual generation ≈ 2×0.3×8760 ≈ 5256 MWh.",
"How is the capacity factor estimated?",
"It is determined by the wind frequency and the cut-in/cut-out speeds of the turbine (about 0.25–0.35 onshore and higher offshore); consult wind measurement data. " + BOIL,
"Is it more stable than PV?",
"Wind output fluctuates greatly within a day and has seasonal variation, so grid connection needs supporting regulation; with good resources the output is considerable. " + BOIL,
"How is the emission reduction calculated?",
"Generation × grid factor gives the reduction, as in the wind power emission reduction tool; the two share the same basis. " + BOIL,
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
        # 运行时查表键是短形态而非 zh_src 的长形态 ⇒ 此类条目以 zh 为键。
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

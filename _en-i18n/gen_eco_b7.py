#!/usr/bin/env python3
# eco batch7 (5 tools)
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
'recycle-rate': [
"♻️ Waste Sorting Recovery Rate",
"Calculate the recovery rate and landfill volume from waste sorting.",
'📖 View the "Waste Sorting Recovery Rate Guide"',
"Recycled amount (kg)",
"Total amount (kg)",
"Period (days)",
"Recovery rate = recycled amount / total amount × 100%",
"Raising the recovery rate markedly reduces landfill.",
"📚 In-Depth Analysis: Waste Sorting Recovery Rate",
"Performance assessment: enter the recycled and generated amounts to obtain the recovery rate and compare it with the target.",
"Component analysis: calculate the rate for each stream (paper, plastic, metal, food waste) to identify weak spots.",
"Teaching demo: show the relation between the recovery rate and final disposal reduction.",
"Example: 100 t generated and 35 t recycled in a month gives a recovery rate of 35%; separating food waste can raise it further.",
"Is there an upper limit to the recovery rate?",
"It is limited by composition and purity; beyond the theoretically recoverable share there is always a non-recyclable part, so targets must be realistic. " + BOIL,
"How does it differ from the utilisation rate?",
"The recovery rate is the share sorted out while the utilisation rate is the share actually reprocessed, which better reflects real performance. " + BOIL,
"How can it be raised?",
"Accurate sorting at the source, backstop collection of low-value items and quality improvement at the end of the chain are all indispensable. " + BOIL,
],
'recycling-guide': [
"♻️ Waste Sorting Guide",
"Search a waste item to find out which category it belongs to",
"/ Waste Sorting Guide",
'📖 View the "Waste Sorting Guide"',
"Four-category disposal: recyclables (paper, plastic, metal, glass, textiles), hazardous waste (batteries, lamps, medicines, paint), food waste (food scraps, fruit shells, vegetable leaves) and residual waste (tissues, ceramics, disposables); correct disposal rate = correctly sorted items ÷ total items × 100%; recyclables recovery rate = recycled amount ÷ generated amount × 100%; drain food waste before disposal, and collect hazardous waste separately to avoid contaminating other categories.",
"♻️ Recyclables",
"🥗 Food waste",
"🗑️ Residual waste",
"⚠️ Hazardous waste",
"🌟 Common categories",
"📚 In-Depth Analysis: Waste Sorting Guide",
"Household sorting: when unsure which bin an item goes in, enter a keyword for an instant answer.",
"Community outreach: show residents the four categories and the disposal tips for commonly confused items.",
"Event preparation: when setting up sorting points, check whether an item counts as a recyclable.",
"Reproducible queries: plastic bottle and battery",
'Enter "plastic bottle" → matches "Recyclables"; the disposal tip is to empty the residue and flatten it.\nEnter "battery" → matches "Hazardous waste"; take it to a hazardous waste collection point and never mix it with residual or food waste.\nEnter "leftovers" → matches "Food waste"; drain the liquid before disposal.',
"How many items are covered? What if my item is not found?",
"Built-in entries cover common household waste and support fuzzy keyword matching. If nothing is found, decide in order: is it toxic or hazardous → is it recyclable → is it perishable → otherwise put it in residual waste.",
"Local standards differ; which one prevails?",
"Entries follow China's four categories of household waste (recyclables / hazardous waste / food waste / residual waste) as a general convention; detailed rules and names differ slightly in cities such as Shanghai and Beijing, so local regulations prevail in practice.",
"Air Quality Index (AQI) Category Conversion",
"Waste Reduction Calculation",
"Waste generation calculator",
"Carbon Footprint Offsetting",
"Carbon footprint calculation and offsetting",
'About "Waste Sorting Guide"',
"Waste Sorting Guide. An environmental and ecological tool that helps calculate environmental indicators.",
"🔍 Enter a waste item (e.g. plastic bottle, battery, leftovers...)",
],
'solar-output': [
"⚡ Solar Power Generation",
"Estimate the generation of a PV panel over a period.",
'📖 View the "Solar Power Generation Guide"',
"Panel area (m²)",
"Daily average irradiation (kWh/m²)",
"E = area × efficiency × daily irradiation × days",
"In practice it is affected by tilt, shading and temperature.",
"📚 In-Depth Analysis: Solar Power Generation",
"Plant estimate: enter the installed capacity and the equivalent hours for the resource zone to estimate annual generation and revenue.",
"Return assessment: enter the tariff for self-consumption or surplus feed-in to calculate the payback period.",
"Teaching demo: show how tilt and orientation affect the equivalent hours.",
"Example: 5 kW with 1100 equivalent hours and a performance ratio of 0.82 gives annual generation ≈ 5×1100×0.82 = 4510 kWh.",
"Where do the equivalent hours come from?",
"They are derived from local irradiation and system losses (about 1000–1300 h in a class-III zone); consult a solar resource map. " + BOIL,
"What does the performance ratio include?",
"Module degradation, temperature, line losses, inverter losses and shading, so multiply by 0.75–0.85 to obtain the actual figure. " + BOIL,
"What is the relation to PV emission reduction?",
"Generation × grid factor gives the reduction, as in the PV emission reduction tool; the two share the same basis. " + BOIL,
],
'solid-waste': [
"🌱 Solid Waste Generation Coefficient Estimation",
"Estimate solid waste generation from industry pollutant generation coefficients",
"Solid Waste Generation Coefficient",
"/ Solid Waste Generation Coefficient",
'📖 View the "Solid Waste Generation Coefficient Estimation Guide"',
"Solid waste generated = product output × pollutant generation coefficient; recycled = total × recovery share; disposed = total × disposal share; stockpiled = total − recycled − disposed (negative values set to zero)",
'The coefficient takes a typical industry value (kg/unit): coal mining and washing 300, metal ore mining and processing 1000, iron and steel smelting 400, thermal power 250, chemicals 150, building materials 50, paper 200, textiles 60, food processing 100; switch to "custom" to enter your own. Totals are in kg and shown in tonnes at 1000 kg or more; recovery and disposal split the flow by percentage and the remainder is stockpiled or discharged, for reference in industrial solid waste ledgers and compliance accounting.',
"Industry type",
"Coal mining and washing",
"Metal ore mining and processing",
"Iron and steel smelting",
"Thermal power",
"Chemicals",
"Paper",
"Textiles",
"Product output / throughput (units below)",
"Solid waste generation coefficient (kg/unit)",
"Comprehensive utilisation share (%)",
"Disposal share (%)",
"📖 Common industry solid waste coefficients",
"Typical solid waste",
"Coefficient range",
"Coal gangue",
"kg/t coal",
"Iron ore mining",
"Tailings",
"kg/t ore",
"Blast furnace slag / steel slag",
"kg/t steel",
"Fly ash / furnace slag",
"Chemical waste residue",
"kg/t product",
"Waste / dust",
"White mud / alkali residue",
"kg/t paper",
"Waste / sludge",
"Organic waste residue",
"kg/t raw material",
"Data source: National Pollution Source Census manual of industrial solid waste generation and discharge coefficients (reference values)",
"📚 In-Depth Analysis: Solid Waste Generation Coefficient Estimation",
"Industry estimate: enter the output and unit waste coefficient to obtain the solid waste volume.",
"Management planning: enter parameters for different industries and aggregate the regional total.",
"Teaching demo: show how convenient the coefficient method is for macro estimates.",
"Example: 1 million t of steel output with a waste coefficient of 0.3 t per tonne gives ≈ 300000 t of solid waste (to be corrected by the actual composition).",
"Are the coefficients reliable?",
"They are industry averages, lower for advanced processes; accurate work needs measurement, but coefficients suffice for planning. " + BOIL,
"Does it include hazardous waste?",
"General solid waste and hazardous waste are listed separately; hazardous waste must be managed individually under the catalogue and cannot be lumped together. " + BOIL,
"How can it be reduced?",
"Cleaner production, circular use and process improvement are the main paths to reduction at source. " + BOIL,
'About "Solid Waste Generation Coefficient"',
"Solid Waste Generation Coefficient is an online tool in the scientific research field. A scientific research tool using standard scientific formulas for accurate calculation.",
],
'waste-calculator': [
"♻️ Waste Generation Calculator",
"Estimate household waste generation and get reduction advice",
"Waste Reduction Calculation",
"/ Waste Reduction Calculation",
'📖 View the "Waste Generation Calculator Guide"',
"Monthly waste = base + food scraps + packaging + disposables + clothing; per capita per day = (monthly amount × 12 / household size) / 365",
"Base = household size × 1.2 kg/person/day × (1 + regional adjustment) (urban 0, suburban −0.1, rural −0.2); food scraps = household size × (cooking factor + leftovers factor) × 30 (cooking: daily 2.5 / often 1.5 / occasionally 0.8 / rarely 0.3; leftovers: none 0 / occasionally 0.3 / a lot 0.7, in kg/person/day); packaging = takeaway orders×4×0.4 + parcels×4×0.15 kg; disposables = household size × factor × 30 (low 0.5 / medium 1.0 / high 2.0); clothing = none 0 / a little 5 / a lot 15 kg. Rated per capita per day: <0.5 very low, <1.0 fairly low, <1.5 close to average, otherwise high.",
"Household size",
"Residential area",
"Suburban",
"Rural",
"🍽️ Kitchen / food",
"Cooking frequency",
"Almost daily",
"Several times a week",
"Never",
"Leftovers",
"Do not leave leftovers",
"📦 Packaging consumption",
"Takeaway orders per week",
"Parcels per week",
"🧴 Other",
"Disposable items",
"Old clothes disposed per year",
"None",
"A lot",
"Calculate waste",
"📚 In-Depth Analysis: Waste Generation Calculator",
"Household self-check: estimate monthly waste from household size and habits and compare it with the 1–1.2 kg per person per day benchmark.",
"Reduction planning: compare how much packaging waste falls after fewer takeaways and consolidated deliveries.",
"Community outreach: use different parameters to show how disposable tableware and clothing consumption affect waste volume.",
"Reproducible example: a 3-person urban household",
'Input: 3 people, urban, cooking several times a week, occasional leftovers, 3 takeaways/month, 2 parcels/month, occasional disposable tableware, a little clothing added.\nBase = 3×1.2×(1+0) = 3.6 kg; food scraps = 3×(1.5+0.3)×30 = 162 kg;\npackaging = (3×4×0.4)+(2×4×0.15) = 4.8+1.2 = 6 kg; disposables = 3×1.0×30 = 90 kg; clothing = 5 kg;\nmonthly total ≈ 266.6 kg, about 3.20 t per year, ≈ 2.92 kg per person per day → rated "high, needs reduction". Fewer takeaways and less disposable tableware are the most direct ways to cut the volume.',
"What per-capita amount is normal?",
"China's per-capita household waste is about 1–1.2 kg/day. Below 1.0 indicates good environmental performance, 1.0–1.5 is close to average, and above 1.5 signals a need to reduce.",
"Which items affect the result most?",
"By coefficient, disposable tableware at the high setting is 2.0 kg/person/day and cooking every meal is 2.5 kg/person/day, the two biggest contributors to the total; takeaways and parcels add linearly with frequency, so cutting frequency brings quick results.",
"Air Quality Index (AQI) Category Conversion",
"Carbon Footprint Offsetting",
"Carbon footprint calculation and offsetting",
'About "Waste Reduction Calculation"',
"Waste Reduction Calculation. An environmental and ecological tool that helps calculate environmental indicators.",
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

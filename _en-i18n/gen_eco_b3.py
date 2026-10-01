#!/usr/bin/env python3
# eco batch3 (5 tools)
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
'eco-14': [
"⚡ Building Energy Use Index",
"Calculate the building energy use index per unit of floor area.",
'📖 View the "Building Energy Use Index Guide"',
"Annual electricity use (kWh)",
"Floor area (m²)",
"Energy use per unit area = annual electricity use / floor area",
"Used for benchmarking in building energy-efficiency assessment.",
"📚 In-Depth Analysis: Building Energy Use Index",
"Benchmarking: enter the area and annual energy use per unit area and compare against efficiency standards (such as 65% energy saving) to judge compliance.",
"Retrofit assessment: enter parameters before and after an efficiency retrofit to quantify the savings.",
"Teaching demo: show the linear relation between the unit index × area and total energy use.",
"Example: a 10000 m² building with a unit energy use of 80 kWh/m²·year consumes 800000 kWh per year; lowering it to 50 saves 300000 kWh per year.",
"Where does the unit index come from?",
"Energy consumption caps are set by building type and climate zone, and your own historical consumption can also be used to back-calculate it. " + BOIL,
"What is the relation to carbon emissions?",
"Multiplying by the grid factor gives the building's operational carbon emissions, the main source during the operating phase. " + BOIL,
"Does it cover operation only?",
"Operational energy is easy to account for; materials and construction (embodied carbon) are counted separately, so a full boundary must include embodied carbon. " + BOIL,
],
'eco-15': [
"⚡ Wastewater Treatment Plant Energy Use",
"Estimate the specific energy consumption of wastewater treatment.",
'📖 View the "Wastewater Treatment Plant Energy Use Guide"',
"Daily average electricity use (kWh)",
"Daily average throughput (m³)",
"Pumping head (m)",
"Specific electricity use = total daily electricity / daily throughput",
"Pumping energy is roughly proportional to the head.",
"📚 In-Depth Analysis: Wastewater Treatment Plant Energy Use",
"Energy audit: enter the throughput and specific electricity use (kWh/m³) to obtain annual electricity consumption and cost.",
"Upgrade assessment: compare specific electricity use before and after an upgrade to quantify the trade-off between extra energy and emission reduction.",
"Teaching demo: show the effect of economies of scale on specific electricity use.",
"Example: a throughput of 50000 m³/day at 0.3 kWh/m³ gives annual electricity use ≈ 5×10⁴×365×0.3 ≈ 5.48 million kWh.",
"What specific electricity use is reasonable?",
"Conventional activated sludge uses about 0.2–0.4 kWh/m³, and upgraded treatment (nitrogen and phosphorus removal) and water reuse push it higher. " + BOIL,
"How can energy be saved?",
"High-efficiency aeration, intelligent chemical dosing and variable-frequency pumps are the main saving points and can clearly lower specific electricity use. " + BOIL,
"Does it also consume chemicals and water?",
"Besides electricity there is also the energy used for chemicals and sludge disposal, which a complete accounting should include. " + BOIL,
],
'eco-16': [
"🌱 Wind Power Emission Reduction",
"Estimate the emission reduction from wind power generation.",
'📖 View the "Wind Power Emission Reduction Guide"',
"Installed capacity (MW)",
"Capacity factor (%)",
"Grid emission factor",
"Annual generation = installed capacity × capacity factor × 8760 hours",
"Reduction = generation × emission factor",
"Equivalent cars are calculated at 15000 km driven per year and 4.6 tonnes of emissions.",
"📚 In-Depth Analysis: Wind Power Emission Reduction",
"Wind benefit: enter annual generation and convert it at the grid factor into an emission reduction, used for green power certificates or carbon accounting.",
"Comparison with PV: enter generation for different renewables and compare the cost per unit of reduction.",
"Teaching demo: show the effect of the capacity factor on actual generation.",
"Example: annual generation of 20 million kWh at a factor of 0.58 gives a reduction ≈ 2000×10⁴×0.58 = 11600 tCO₂.",
"What is the capacity factor?",
"Actual generation / (installed capacity × 8760 h); about 0.25–0.35 onshore and higher offshore, it determines the real output. " + BOIL,
"How does it compare with PV reduction?",
"The reduction is the same for the same amount of electricity (both displace grid power); the difference lies in the resource and utilisation hours, not the energy type. " + BOIL,
"Which reduction factor?",
"Use the average factor of the grid the project feeds into (about 0.5–0.6 kgCO₂/kWh), following official figures. " + BOIL,
"How to use Wind Power Emission Reduction",
"Estimates related to energy consumption, carbon emissions and environmental protection.",
"What is Wind Power Emission Reduction for?",
"Enter the annual wind generation to convert it into the CO₂ reduction at the equivalent car's annual emissions, for estimating the environmental benefit of a wind project.",
"How do I use Wind Power Emission Reduction?",
"Which scenarios suit Wind Power Emission Reduction?",
],
'eco-3': [
"🌱 Wastewater Treatment Load",
"Estimate the influent pollutant load of a wastewater treatment plant.",
'📖 View the "Wastewater Treatment Load Guide"',
"Flow rate (m³/d)",
"Influent COD (mg/L)",
"Effluent COD (mg/L)",
"Load = flow × concentration / 1000",
"Removal rate = (influent − effluent) / influent × 100%",
"COD is chemical oxygen demand.",
"📚 In-Depth Analysis: Wastewater Treatment Load",
"Discharge accounting: enter the flow and COD concentration to obtain the daily/annual pollutant load (kg).",
"Treatment sizing: back-calculate the removal capacity the facility needs from the load.",
"Teaching demo: show the multiplicative relation load = flow × concentration.",
"Example: a flow of 1000 m³/d at COD 400 mg/L gives a daily load = 1000×0.4 = 400 kg COD/d.",
"How are the concentration units used?",
"mg/L is the same as g/m³; load (kg/d) = flow (m³/d) × concentration (mg/L) / 1000. " + BOIL,
"What is the difference between COD and BOD?",
"COD measures all oxidisable organics while BOD measures the biodegradable part; COD ≥ BOD, and the ratio reflects biodegradability. " + BOIL,
"For compliance, do we look at concentration or load?",
"The discharge standard sets concentration limits, but the treatment scale is determined by the load, so both matter. " + BOIL,
],
'eco-4': [
"🌱 Solid Waste Generation",
"Estimate total municipal solid waste from the population and the per-capita generation rate.",
'📖 View the "Solid Waste Generation Guide"',
"Population",
"Waste per capita (kg/d)",
"Total = population × per-capita amount × days",
"Suitable for a quick estimate of municipal waste volume.",
"📚 In-Depth Analysis: Solid Waste Generation",
"Generation forecast: enter the served population and per-capita daily waste to obtain the annual total.",
"Stream estimate: enter the share of each sorted component to estimate recyclables, food waste and other amounts.",
"Teaching demo: show how convenient the coefficient method is for macro-level estimates.",
"Example: a population of 100000 at 1.1 kg/d per capita gives about 10×10⁴×1.1×365 ≈ 4015 t of solid waste per year.",
"What waste generation coefficient should be used?",
"About 0.8–1.2 kg/d per urban resident; it varies with living standards and collection methods, so local statistics prevail. " + BOIL,
"What is the relation to the recycling rate?",
"For a fixed generation amount, a higher recycling rate means less final disposal; estimates must distinguish generation from collection. " + BOIL,
"Is the coefficient method accurate?",
"It suits macro-level estimates; accurate work needs measured composition, but the coefficient method is sufficient for planning purposes. " + BOIL,
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

#!/usr/bin/env python3
# eco batch4 (5 tools)
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
'eco-5': [
"🧮 Water Saving Rate Calculation",
"Calculate the water use and saving rate after water-saving measures are adopted.",
'📖 View the "Water Saving Rate Calculation Guide"',
"Original water use (m³)",
"Water use after saving (m³)",
"Water price (CNY/m³)",
"Saving rate = (original − after saving) / original × 100%",
"Useful for evaluating the effect of water-saving fixtures.",
"📚 In-Depth Analysis: Water Saving Rate Calculation",
"Retrofit results: enter water use before and after to obtain the saving rate and the annual volume saved.",
"Quota benchmarking: compare against the industry water-use quota to judge compliance.",
"Teaching demo: show the difference between the saving rate and the absolute volume saved.",
"Example: 1000 m³/month before and 700 m³/month now gives a saving rate = (1000−700)/1000 = 30%, saving 300 m³ per month.",
"Can the saving rate exceed 100%?",
"No; a value above 100% means the baseline is defined incorrectly, and a negative value means water use increased. " + BOIL,
"Look at the rate or the volume?",
"The rate shows relative improvement while the volume shows absolute benefit; report both to avoid the misleading effect of a high rate on a small base. " + BOIL,
"What about seasonal effects?",
"Water use fluctuates seasonally, so compare a full year or the same season; a single-month comparison can be distorted. " + BOIL,
"How to use Water Saving Rate Calculation",
"Estimates related to energy consumption, carbon emissions and environmental protection.",
"What is Water Saving Rate Calculation for?",
"Enter the water use before and after water-saving measures to compute the volume saved and the saving rate, for evaluating the actual effect of fixtures and management.",
"How do I use Water Saving Rate Calculation?",
"Which scenarios suit Water Saving Rate Calculation?",
],
'eco-6': [
"🌱 Green Coverage Ratio",
"Calculate the green coverage ratio of an area.",
'📖 View the "Green Coverage Ratio Guide"',
"Green space area (m²)",
"Total site area (m²)",
"Tree canopy projection area (m²)",
"Green coverage ratio = green space area / total area × 100%",
"Counting tree canopy projection at half its area is a common practice.",
"📚 In-Depth Analysis: Green Coverage Ratio",
"Indicator accounting: enter the green space and the total site area to obtain the coverage ratio and compare it with the planning target.",
"Compliance check: enter parameters for a residential community or industrial park to judge whether the greening requirement is met.",
"Teaching demo: show how the coverage ratio is affected by the underlying surface (hard paving).",
"Example: 3000 m² of green space on a 10000 m² site gives a coverage ratio of 30%.",
"Are the greening rate and the ",
"Green Space Ratio",
" the same thing?",
"The terms are often mixed up; the green space ratio is usually based on land-use share while the green coverage ratio includes vertical greening projection, so the local code governs the definition. " + BOIL,
"Does roof greening count?",
"It depends on the standard; some count roof or vertical greening at a reduced factor, so check the local landscaping regulations. " + BOIL,
"Is higher always better?",
"Moderation is best; an excessive ratio can affect parking and site functions, so it must be balanced with the master plan. " + BOIL,
],
'eco-7': [
"⚡ Energy Efficiency Conversion",
"Convert different energy units into standard coal equivalent or kWh.",
'📖 View the "Energy Efficiency Conversion Guide"',
"Electricity (kWh)",
"Standard coal (kg)",
"1 m³ of natural gas ≈ 1.2143 kgce ≈ 9.88 kWh",
"The coefficients are common approximations.",
"📚 In-Depth Analysis: Energy Efficiency Conversion",
": enter kWh to obtain MJ (×3.6), or the reverse, to keep a consistent accounting basis.",
"Equipment comparison: enter the COP/EER of an air conditioner or heat pump and compare energy efficiency grades.",
"Teaching demo: show the energy equivalence 1 kWh = 3.6 MJ.",
"Example: an air conditioner with 3500 W of cooling output and 1000 W of input has an EER of 3.5, reaching grade 3; COP is used analogously for heating.",
"How do you convert between kWh and MJ?",
"Use this coefficient, and do not confuse it with power (kW). " + BOIL,
"What is the difference between EER and COP?",
"EER is for cooling (cooling output / electrical input) and COP for heating (heat output / electrical input); the higher the ratio, the more efficient. " + BOIL,
"What determines the energy efficiency grade?",
"It follows the national energy efficiency label (grade 1 is best); at the same cooling capacity, the lower the input power, the higher the grade. " + BOIL,
],
'eco-8': [
"🌳 Carbon Sink Afforestation Estimation",
"Estimate the annual carbon sink of a forest or afforestation project.",
'📖 View the "Carbon Sink Afforestation Estimation Guide"',
"Area (hectares)",
"Planting density (trees/hectare)",
"Annual carbon sequestration per tree (kg)",
"Term (years)",
"Annual carbon sink = area × density × sequestration per tree",
"Actual sequestration depends on species, climate and stand age.",
"📚 In-Depth Analysis: Carbon Sink Afforestation Estimation",
"Carbon sink calculation: enter the area and annual sequestration rate to obtain the total annual sequestration.",
"Offset accounting: compare with company emissions to find how much sink area is needed to neutralise them.",
"Teaching demo: show how the sequestration rate rises and then levels off with stand age.",
"Example: 500 mu at 5 tCO₂/mu per year gives an annual carbon sink of 2500 tCO₂, offsetting emissions of a comparable magnitude.",
"Is the sequestration rate stable?",
"Young stands grow fast and mature stands level off; accounting usually uses an average or the value given by the methodology, with the filed figure prevailing. " + BOIL,
"Can the carbon sink be sold immediately?",
"It must go through validation, monitoring and issuance (such as CCER) to become tradeable carbon credits; it is not counted as soon as the trees are planted. " + BOIL,
"How does it differ from Carbon Forest?",
"This tool measures sequestration, whereas carbon-neutral forest focuses on offsetting specific emissions with forest land; the concepts are similar but the uses differ. " + BOIL,
],
'eco-9': [
"📏 Noise Attenuation Distance",
"Estimate the sound pressure level attenuation of a point source with distance.",
'📖 View the "Noise Attenuation Distance Guide"',
"Sound pressure level at the source (dB)",
"Reference distance (m)",
"Target distance (m)",
"Barrier attenuation (dB)",
"Point source attenuation = 20·log₁₀(r/r₀)",
"Air absorption and ground effects are not considered.",
"📚 In-Depth Analysis: Noise Attenuation Distance",
"Boundary prediction: enter the source strength and distance to estimate whether the level at a given point complies.",
"Attenuation demo: show that doubling the distance lowers the level by about 6 dB.",
"Teaching demo: illustrate the free-field point-source attenuation model.",
"Example: 80 dB at the source gives about 80−20lg(10/r₁) at 10 m; with r₁=1 the level at 10 m is ≈ 60 dB (a 20 dB drop).",
"Why does doubling the distance drop the level by 6 dB?",
"Point-source intensity falls with area as 1/r², so the level is 10lg(1/r²) = −20lg r; doubling the distance gives −6 dB. " + BOIL,
"Does this hold in practice?",
"It is a free-field approximation; reflections, absorption or weather cause deviations, and boundary predictions need corrections. " + BOIL,
"Can dB be added or subtracted directly?",
"They cannot be added linearly; for multiple sources use energetic summation (10lgΣ10^(L/10)), see the ",
"Noise Superposition",
" tool. " + BOIL,
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

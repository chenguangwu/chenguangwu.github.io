#!/usr/bin/env python3
# eco batch6 (5 tools)
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
'landfill-methane': [
"♻️ Landfill Methane Generation",
"Estimate the methane production and its equivalent from organic waste in a landfill.",
'📖 View the "Landfill Methane Generation Guide"',
"Organic waste (kg/year)",
"Degradable carbon fraction",
"Methane correction factor",
"Methane volume fraction",
"CH₄ = organic matter × degradable fraction × MCF × volume fraction × 16/12",
"Collected methane can be used for power generation, reducing emissions.",
"📚 In-Depth Analysis: Landfill Methane Generation",
"Biogas potential: enter the landfilled volume and degradable fraction to estimate annual methane production.",
"Reduction accounting: compare collection and flaring with uncontrolled release to quantify the GWP benefit.",
"Teaching demo: show that the GWP of methane is far higher than that of CO₂.",
"Example: 10000 t landfilled per year with 40% degradable organic content and a yield of 0.05 m³CH₄/t gives about 2 million m³ of methane per year (to be corrected by the model).",
"How is the methane yield determined?",
"It is given by the organic composition and a degradation model (such as IPCC) and is affected by temperature and moisture; the methodology governs. " + BOIL,
"Why collect it?",
"Methane has a high GWP (about 28–34 times CO₂ over 100 years), so collecting and using it cuts emissions sharply and produces energy. " + BOIL,
"How serious is uncontrolled release?",
"Methane released directly from open landfills has a strong greenhouse effect and is a priority reduction source in the sanitation field. " + BOIL,
],
'methane-equivalent': [
"🌾 Methane Greenhouse Gas Equivalent",
"Convert methane emissions into CO₂ equivalent.",
'📖 View the "Methane Greenhouse Gas Equivalent Guide"',
"Methane amount (kg)",
"Time horizon (years)",
"CO₂e = CH₄ × GWP₁₀₀ (methane ≈ 28)",
"GWP100 is the global warming potential over a 100-year horizon.",
"📚 In-Depth Analysis: Methane Greenhouse Gas Equivalent",
"Equivalent conversion: enter the CH₄ mass and GWP (28 or 84) to obtain CO₂e.",
"Disclosure integration: convert methane and nitrous oxide into CO₂e and report the total.",
"Teaching demo: show the difference between GWP time horizons (20 and 100 years).",
"Example: 1 t of CH₄ at a 100-year GWP of 28 gives CO₂e = 28 t; using the 20-year GWP of 84 gives 84 t.",
"Should GWP be 28 or 84?",
"IPCC AR5 gives 28 over 100 years and 84 over 20 years; international inventories mostly use the 100-year value, and the horizon must be stated. " + BOIL,
"Why is the methane equivalent so high?",
"Methane absorbs heat strongly in the short term but has a short lifetime, so a high GWP reflects its strong but temporary warming effect. " + BOIL,
"Are other gases converted too?",
"Yes; nitrous oxide has a GWP of about 265 and HFCs are higher still, so converting everything to CO₂e is what makes them comparable and addable. " + BOIL,
],
'noise-addition': [
"🔊 Noise Summation Calculation",
"The total sound pressure level after several sources are combined.",
'📖 View the "Noise Summation Calculation Guide"',
"Source 1 (dB)",
"Source 2 (dB)",
"Source 3 (dB)",
"Decibels are a logarithmic unit and cannot be added directly.",
"📚 In-Depth Analysis: Noise Summation Calculation",
"Multi-source summation: enter each source level to obtain the combined total level.",
"Noise reduction assessment: switch a source off and recalculate to quantify its contribution.",
"Teaching demo: show that two equally strong sources only raise the level by 3 dB (not double).",
"Example: two sources both at 80 dB combine to 10lg(10^8+10^8) = 83 dB, only a 3 dB rise.",
"Why is it not simple addition?",
"dB is a logarithmic unit, so sound intensity can be added but sound levels cannot be added directly; convert to intensity first and then sum. " + BOIL,
"What if they differ by more than 10 dB?",
"The louder source dominates and the quieter one can be ignored (a 10 dB difference only raises the total by 0.4 dB). " + BOIL,
"How does it differ from the ",
"Noise Superposition",
" tool?",
"This tool performs generic multi-source energy summation, while the Noise Superposition tool focuses on combining multiple periods or sources in one scenario; the algorithm is the same. " + BOIL,
],
'noise-superposition': [
"🔊 Noise Summation Calculation",
"Sum the decibel levels of multiple noise sources, with support for adding and removing sources",
'📖 View the "Noise Summation Calculation Guide"',
"+ Add source",
"Calculate sum",
"📖 Calculation principle",
"Noise summation",
": decibels (dB) are a logarithmic quantity and cannot be added directly",
"Summation formula",
": Ltotal = 10·lg(Σ10^(Li/10))",
"Two identical sound pressure levels combine to add 3 dB",
"For two sources differing by 10 dB, the sum is approximately the larger value",
"Noise attenuation",
": for a point source, the level drops by 6 dB each time the distance doubles",
"📊 Common sound pressure level reference",
"- Whisper",
"- Quiet room",
"- Normal conversation",
"- City street",
"- Factory workshop",
"- Tractor",
"- Pain threshold",
"- Jet aircraft",
"📚 In-Depth Analysis: Noise Summation Calculation",
"Boundary summation: enter each item of equipment's level after distance attenuation to obtain the total level.",
"Room acoustics: enter the levels of several noise sources to judge whether the standard is exceeded.",
"Teaching demo: show the non-linear nature of summation.",
"Example: source A at 75 dB and source B at 78 dB combine to ≈ 80.2 dB (dominated by the 78 dB source).",
"Is the formula the same?",
"It is the same as noise summation: Ltotal = 10lg(Σ10^(Li/10)), essentially energy summation of sound intensity. " + BOIL,
"A-weighting or C-weighting?",
"Environmental noise usually uses A-weighting (dB(A)) as it reflects the human ear, while C-weighting can be used for low-frequency machinery. " + BOIL,
"For compliance, peak or average?",
"Most noise standards set day and night limits, so use a representative value for the relevant period, with peak values for special periods. " + BOIL,
'About "Noise Summation Calculation"',
"Noise Summation Calculation is an online tool in the scientific research field. A scientific research tool using standard scientific formulas for accurate calculation.",
],
'rainwater-harvest': [
"🌱 Rainwater Harvesting Volume",
"Estimate the collectable rainwater from roof area and rainfall.",
"Rainwater Harvesting Volume (Environmental)",
'📖 View the "Rainwater Harvesting Volume Guide"',
"Roof area (m²)",
"Rainfall (mm)",
"Collection efficiency (%)",
"Every 1 mm of rain on 1 m² gives ≈ 1 L; collection volume = area × rainfall × efficiency",
"Suitable for designing roof rainwater recovery systems.",
"📚 In-Depth Analysis: Rainwater Harvesting Volume",
"Volume calculation: enter annual rainfall, roof or site area and the runoff coefficient to obtain the collectable volume.",
"Sponge-city design: enter parameters for a community to assess rainwater reuse potential.",
"Teaching demo: show the effect of the runoff coefficient (high on hard surfaces, low on green space).",
"Example: 1000 mm of annual rainfall on a 1000 m² roof with a runoff coefficient of 0.9 gives 1000×1×0.9 = 900 m³/year.",
"What runoff coefficient should be used?",
"About 0.8–0.95 for roofs, 0.1–0.3 for green space and in between for hard surfaces; choose by the combination of underlying surfaces. " + BOIL,
"What rainfall unit is used?",
"mm is the same as L/m²; 1000 mm of annual rainfall equals 1000 L/m² or 1 m³/m², which makes multiplication by area easy. " + BOIL,
"Is it drinkable?",
"Collected rainwater needs filtration and disinfection for toilet flushing or irrigation, and must meet the relevant water quality standard for drinking. " + BOIL,
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

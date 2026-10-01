#!/usr/bin/env python3
# fishery batch7 (4 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'fishery')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'fishery')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'estimate-23': [
"🔮 Growth Estimation Calculator",
"Enter two parameters to automatically compute the common result.",
'📖 View the "Plankton Biomass (Microscope Count) Estimation Guide"',
"Result = base value × (1 + growth rate/100)",
"Linear growth estimation of the base value by a percentage growth rate.",
"💡 Formula note: result = base value × (1 + growth rate/100).",
"📚 In-Depth Analysis: Growth Estimation",
"Estimate the future value of yield, body weight or scale from a growth rate",
"Compute the total after stocking and the expected weight gain",
"Compare the results of different growth-rate scenarios",
"Yield growth estimate",
"Base value 100 and growth rate 20%: estimated result = 100 × (1 + 20/100) = 120, a gain of 20. Suitable for a quick estimate of linear proportional growth.",
"What scenarios is it suitable for?",
"Suitable for cases of fixed ",
" linear growth, such as estimating the total after stocking from a weight-gain rate; for compound growth use repeated multiplication instead.",
"How is a negative growth rate handled?",
"Just enter a negative value, for example -10% means a 10% reduction, result = base × (1-10%).",
'About "Plankton Biomass (Microscope Count) Estimation"',
"Plankton Biomass (Microscope Count) Estimation. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
"Base value",
"Growth rate (%)",
],
'ratio-hormone': [
"⚗️ Ratio and Proportion Calculator",
"Enter two parameters to automatically compute the common result.",
'📖 View the "Ratio and Proportion Calculation Guide"',
"Simplest ratio = a/g : b/g (g is the greatest common divisor)",
"For quick conversion in scenarios such as reagent mixing and concentration ratios.",
"💡 Formula note: simplest integer ratio = A/g : B/g, share = A/B×100%.",
"📚 In-Depth Analysis: Ratio and Proportion Calculation",
"Converting the mixing ratio of two components of a drug/feed additive",
"Checking the proportional relationship between concentrations or doses",
"Prepare a mixed solution by the simplest integer ratio",
"Two-component mixing ratio",
"Values A=100 and B=50: ",
"greatest common divisor",
" 50, the simplest integer ratio = 2:1; A is 200% of B, i.e. A is twice B. For a quick conversion of reagent or nutrient ratios.",
"Where does the simplest integer ratio come from?",
"First find the greatest common divisor g of the two numbers, then reduce to A/g : B/g; for example 100:50 reduces to 2:1.",
"What is the difference between share and multiple?",
"Share = A/B×100% (a percentage relative to B), multiple = A/B (a pure ratio); both describe the same proportional relationship from different angles.",
'About "Artificial Breeding Spawning (Hormone Dose) Ratio"',
"Artificial Breeding Spawning (Hormone Dose) Ratio. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
],
'temp-density': [
"🌡️ Water Temperature - Saturated DO and Saturation",
"Enter two parameters to automatically compute the common result.",
'📖 View the "Water Temperature - Saturated DO and Saturation Guide"',
"Saturated DO ≈ 14.652 − 0.41022T + 0.007991T² − 0.000077774T³",
"Saturated DO falls as temperature rises; saturation = measured ÷ saturated.",
"Measured DO (mg/L)",
"💡 Formula note: saturation = measured DO ÷ saturated DO at that temperature ×100%.",
"📚 In-Depth Analysis: Water Temperature - Saturated DO and Saturation",
"Estimate the reference saturated DO at a given water temperature",
"Compute saturation from the measured DO to judge whether DO is sufficient",
"Quick assessment of night-time hypoxia risk in the hot season",
"DO saturation at 25℃",
"Water temperature 25℃ and measured DO 6.5 mg/L: the saturated DO at that temperature is about 8.18 mg/L, so saturation = 6.5 / 8.18 × 100% ≈ 79.5%, an acceptable range; it tends to keep falling at night and before dawn, so watch it closely.",
"How does saturated DO change with temperature?",
"It falls as water temperature rises (gas solubility decreases), so hypoxia is more likely at high summer temperatures, and aeration and pond patrols must be stepped up.",
"What saturation counts as safe?",
"It is generally required to be ≥5 mg/L with saturation as high as possible, ≥70%-80%; the hours before dawn and high-density periods are the most hypoxia-prone, so leave a margin.",
'About "Fry Transport Survival Rate (Temperature/Density)"',
"Fry Transport Survival Rate (Temperature/Density). A fishery and aquaculture tool that helps calculate farming parameters and yields.",
],
'calc-39': [
"⚖️ Percentage Calculator (Fishery)",
"Compute the percentage, share, growth rate and more of a value",
"Feed Rate (Percentage of Body Weight) Calculation",
"/ Feed Rate (Percentage of Body Weight) Calculation",
'📖 View the "Percentage Calculator (Fishery) Guide"',
"📚 In-Depth Analysis: Quick Percentage Calculation (Fishery)",
"Quickly find the ",
" of a number in the total, or back-calculate a part from a percentage, for everyday accounting such as ratios, shares and dilution.",
"Instant conversion for scenarios such as feed ratios, drug addition proportions and sample shares.",
"A basic percentage-operation complement to the other tools.",
"Find 20% of 100",
"Default parameters: 20% of 100 = 20.00. That is, the part that is 20% of a total of 100 is 20; you can also back-calculate what percent 20 is of 100 = 20%.",
"How is a percentage calculated?",
"Part ÷ total × 100%; to find the part from a known percentage, total × percentage.",
"What is the difference from the ratio tools?",
"This tool focuses on single percentage conversion; for ratio/proportion cases use the corresponding ratio tool.",
],
}

# term-link nodes missed by extract: zh -> en
EXTRA = {
'estimate-23': {'百分比': 'percentage'},
'calc-39': {'百分比': 'percentage'},
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
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('!! %s EXTRA CJK/CNP violation: %s' % (slug, en[:60]))
            sys.exit(1)
        mp[z] = en
    return mp

def write(slug, mp):
    os.makedirs(OUT, exist_ok=True)
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('name', slug)
    out = {'slug': slug, 'industry': 'fishery', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

for slug, en_list in EN.items():
    write(slug, build(slug, en_list))

#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'gardening')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'gardening')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
DISCL = "Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected."
EXTRA = {}
def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items)); sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en)); sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en)); sys.exit(1)
        mp[z] = en
    return mp
def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'gardening', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('pest-identifier', build('pest-identifier', [
        "🔍 Pest and Disease Identifier",
        "Look up symptoms, affected parts and control methods for common plant diseases and pests",
        "📖 Read the \"Common Pest and Disease Identification and Control Usage Guide\"",
        "Search (disease name / symptom / plant)",
        "🦠 Diseases",
        "🐛 Pests",
        "Part:",
        "🍃 Leaf",
        "🌿 Stem",
        "🌱 Root",
        "🍅 Fruit",
        "🌸 Flower",
        "Symptom:",
        "⚫ Spots",
        "🌫️ Mould layer",
        "🥀 Wilt",
        "💧 Rot",
        "🐛 Insect body",
        "🌀 Deformity",
        "🕳️ Holes",
        "This tool covers 22 common diseases and pests and is for reference only. Read the label carefully before applying any pesticide and observe the safety interval.",
        "📚 In-Depth Analysis: Common Pest and Disease Identification and Control",
        "Identify leaf spots / powdery growth",
        "Identify pests (aphids / spider mites / scale insects)",
        "Choose a control method by affected part",
        "Locate by plant and symptom: powdery mildew (white coating on leaf undersides), downy mildew (yellow spots with mould on the underside), aphids (clustering on tender shoots), spider mites (fine webbing plus yellow specks on leaf undersides), scale insects (hard shells on stems); control splits into physical (water jet / sticky traps), biological (ladybirds / matrine) and chemical (registered pesticides).",
        "When rose tender shoots show dense small green insects plus honeydew → aphids: first spray water to wash them off or use yellow sticky traps, and in severe cases spray imidacloprid or matrine. At the same time, if a white powder appears on leaf undersides → powdery mildew: remove diseased leaves, increase ventilation and spray thiophanate-methyl or similar. When both occur together, treat the pest first then the disease and avoid stacking pesticide damage.",
        "Can I rely on physical control alone?",
        "For light infestations water jets, hand picking and yellow/blue sticky traps work; at high density or fast spread you still need registered pesticides, observing the safety interval.",
        "How does prevention beat treatment?",
        "Reasonable spacing and ventilation, avoiding standing water on leaves, crop rotation and strong plants (adequate fertiliser and water) significantly reduce disease.",
        "About \"Pest and Disease Identifier\"",
        "Pest and Disease Identifier is an online tool for the gardening and planting field. A gardening planting tool for computing planting parameters and quantities.",
        "e.g.: yellow leaves, aphids, powdery mildew, rose...",
    ]))

    write('plant-calendar', build('plant-calendar', [
        "📅 Vegetable Planting Calendar",
        "View vegetable sowing times by month, season or category, including sowing, transplanting, harvest, growing period and temperature",
        "📖 Read the \"Vegetable Planting Calendar Usage Guide\"",
        "Category filter",
        "Season filter",
        "📅 Month view",
        "📋 List view",
        "📅 Month notes:",
        "• Sowing period: the time range for raising seedlings or direct sowing",
        "• Transplanting period: the time to move seedlings after raising to their final position",
        "• Harvest period: the time range in which the crop can be picked",
        "• North China / Central China / South China differ greatly in climate; this table is based on the Yangtze River basin, with northern areas 2-4 weeks later and southern areas 2-4 weeks earlier",
        "• A \"/\" mark means the crop can be grown in both spring and autumn, the first for spring and the second for autumn",
        "🥬 Vegetable Sowing Quick Reference Table",
        "Vegetable",
        "Sowing period",
        "Growing period (days)",
        "📚 In-Depth Analysis: Vegetable Planting Calendar",
        "Look up sowing periods by month and season",
        "Arrange by vegetable category (leaf / fruit / root)",
        "Optimal temperature and growing period tips",
        "Plan by vegetable category and the local frost-free period: leafy greens (Chinese cabbage / spinach) are sown in spring and autumn with a 30-60 day growing period; fruiting crops (tomato / cucumber) are transplanted in late spring and prefer warmth; root crops (radish / carrot) are sown in summer and autumn and must not be transplanted.",
        "Temperate regions: tomato sown in March and transplanted after the last frost (around early April to early May), growing about 110 days and harvested July-September; spinach sown twice, in March and August, best below 20-25℃; radish sown in August and harvested September-October. In subtropical regions the same crop is about 30 days earlier.",
        "What if I miss the sowing window?",
        "Choose fast varieties with short growing periods (choy sum 20 days, cherry radish 30 days), or use a greenhouse/balcony with temperature control to extend the season.",
        "Why can't root crops be transplanted?",
        "The taproot is easily damaged and forks or deforms, so they should be sown directly; fruiting crops and some leafy greens can be raised first and transplanted with their root ball to reduce damage.",
        "About \"Vegetable Planting Calendar\"",
        "Vegetable Planting Calendar. A gardening planting tool for computing planting parameters and quantities.",
        "🔍 Search vegetable name...",
    ]))

    write('plant-care', build('plant-care', [
        "📚 Plant Care Guide",
        "Look up the care essentials for common ornamental plants: light, watering, fertilising, temperature, humidity and propagation",
        "📖 Read the \"Ornamental Plant Care Essentials Lookup Usage Guide\"",
        "Search plant (name / alias)",
        "Category:",
        "🍃 Foliage",
        "🌵 Succulent",
        "🌸 Flowering",
        "🍅 Fruits and vegetables",
        "🌳 Woody",
        "Light:",
        "☀️ Abundant",
        "⛅ Partial shade",
        "🌑 Shade tolerant",
        "🟢 Easy",
        "🔴 Difficult",
        "Covers 32 common plants. Care data is general reference; in practice fine-tune it by variety, plant age and environment.",
        "📚 In-Depth Analysis: Ornamental Plant Care Essentials Lookup",
        "Look up light, water, temperature and fertiliser by plant",
        "Seasonal care adjustments",
        "Choosing a propagation method",
        "Query by plant name for light (full sun / partial shade / shade tolerant), watering (moisture loving / water when the top dries / soak then dry), fertilising (nitrogen, phosphorus and potassium in the growing season), temperature and humidity, and propagation (cutting / division / sowing) essentials.",
        "Pothos: moisture loving and partial shade, water when the top dries, frequent leaf misting, 20-30℃, stem cuttings root easily. Snake plant: drought tolerant, soak then dry, keep dry in winter, propagate by division. Gardenia: acid loving and moisture loving, ferrous sulphate solution to prevent chlorosis, propagated by cutting or layering.",
        "What should I check first when leaves yellow?",
        "First tell water yellowing (waterlogging and root rot) from drought yellowing (long dry spell), then look at fertiliser damage / nutrient deficiency / light; yellowing in acid-loving plants (gardenia, azalea) is mostly iron deficiency, so acidify and supply iron.",
        "How do plants get through winter?",
        "Most are brought indoors with temperature controlled, less water and no fertiliser; succulents and cacti are kept dry to prevent frost damage; tropical foliage plants (pothos, areca palm) need above 10℃ with extra humidity.",
        "About \"Plant Care Guide\"",
        "Plant Care Guide. A gardening planting tool for computing planting parameters and quantities.",
        "e.g.: pothos, rose, succulent...",
    ]))

    write('compost-calculator', build('compost-calculator', [
        "🌷 Compost C:N Ratio Calculator",
        "Compute the overall C:N ratio of a mix of several compost raw materials; the ideal range is 25-35:1 (best 30:1)",
        "📖 Read the \"Compost C:N Ratio Calculator Usage Guide\"",
        "➕ Add material",
        "🧮 Compute the C:N ratio",
        "Mix C:N = total weight ÷ Σ(weight of each material ÷ that material's C:N)",
        "Principle:",
        "Treat the weight of each material as a proxy for carbon, nitrogen = weight ÷ C:N, and the mix ratio = total carbon ÷ total nitrogen.",
        "Ideal range:",
        "A C:N between 25-35:1 gives the highest microbial decomposition efficiency; too high (>40) decomposes slowly and too low (<20) easily produces ammonia odour.",
        "📚 Reference Table of Common Compost Material C:N Ratios",
        "C:N ratio",
        "💾 Saved recipes",
        "💾 Save the current recipe",
        "📚 In-Depth Analysis: Compost C:N Ratio Calculator",
        "Mixing kitchen scraps with fallen leaves for home compost",
        "Adjusting when carbon is excessive (high sawdust/cardboard share)",
        "Adjusting when nitrogen is excessive (much manure/grass clippings)",
        "Convert carbon and nitrogen for each material by weight and its own C:N ratio (nitrogen = weight ÷ C:N), and mix C:N = total carbon ÷ total nitrogen; the ideal range is 25-35:1 with about 30:1 best.",
        "Fallen leaves 10kg (C:N 60, nitrogen 0.167kg) + chicken manure 2kg (C:N 10, nitrogen 0.200kg): total weight 12kg, total nitrogen 0.367kg, mixed C:N = 12÷0.367 ≈ 32.7, inside the ideal range so it can be composted directly; with fallen leaves alone C:N≈60 is carbon-heavy, so chicken manure/grass clippings should be added to raise nitrogen.",
        "What happens when C:N is too high or too low?",
        "Too much carbon decomposes slowly with low heat; too much nitrogen causes odour and attracts pests. Centring on 30:1, add leaves/sawdust to raise carbon and kitchen scraps/manure to raise nitrogen.",
        "How long until compost is usable?",
        "Aerobic turning gives dark brown loose humus in about 2-3 months; a balanced C:N, 50-60% moisture and regular turning speed it up.",
        "About \"Compost C:N Ratio Calculator\"",
        "Compost C:N Ratio Calculator. A gardening planting tool for computing planting parameters and quantities.",
        "Recipe name (e.g.: standard vegetable leaf compost)",
    ]))


if __name__ == '__main__':
    main()
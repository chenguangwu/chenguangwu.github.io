#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'baking')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'baking')
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
    out = {'slug': slug, 'industry': 'baking', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('dough-hydration', build('dough-hydration', [
        "🧁 Dough Hydration Calculator",
        "Enter the weight of flour and water to calculate dough hydration and determine the suitable bread type",
        "Dough hydration",
        "/ Dough hydration",
        "Hydration = water weight / flour weight × 100%",
        "Water weight (g)",
        "Suitable for toast, baguette, etc.",
        "Standard hydration",
        "📊 Hydration and Bread Texture Correlation Table",
        "Dough texture",
        "Suitable bread",
        "Tight and firm, hard to knead",
        "Bagel, pretzel",
        "Fairly firm, slightly elastic",
        "Italian bread, some sweet breads",
        "Soft and moderate, easy to handle",
        "Basic white bread, dinner rolls",
        "Soft and somewhat wet, requires kneading skill",
        "Toast, baguette, sourdough",
        "Wet and sticky, requires stretch and fold",
        "Ciabatta, focaccia",
        "Extremely wet and soft, almost batter-like",
        "High-hydration sourdough",
        "💡 Hydration = water weight / flour weight × 100%. Liquid ingredients (milk, egg wash, etc.) can be counted as equivalent water.",
        "🔍 Details of Each Hydration Range",
        "50-55% Bagel",
        "Tight and firm",
        "56-60% Low hydration",
        "Slightly elastic",
        "61-65% Standard",
        "Soft and easy to handle",
        "66-72% Toast",
        "Soft and somewhat wet",
        "73-80% Ciabatta",
        "Wet and sticky, needs folding",
        "81-90% Very high",
        "Almost batter-like",
        "📚 In-Depth: Dough Hydration Calculator",
        "Back-calculate how much water to add from the recipe's target hydration.",
        "Compare hydration ranges of different breads to judge dough feel and crumb structure.",
        "Convert the water amount for high-hydration (80%+) European bread formulas.",
        "1000g flour with 72% hydration",
        "Hydration (",
        "baker's percentage",
        ") = water weight / flour weight × 100%. Flour 1000g, target 72%, so water added = 1000 × 72% = 720g. This falls in the higher-hydration range for European breads, giving a more open crumb.",
        "What is the typical hydration of common breads?",
        "Baguette about 65%-70%, toast (sweet bread) about 60%-68%, European country bread often 70%-80%, ciabatta and other high-hydration breads can reach 80%-85%. Higher hydration is harder to handle but gives a more open crumb.",
        "What does hydration level mainly affect?",
        "Higher hydration makes dough stickier, ferments faster, and yields a larger, moister crumb; lower hydration gives a tighter, denser texture. When adjusting, also consider fermentation time and handling technique.",
        "About 'Dough Hydration'",
        "A dough hydration reference table and calculator: enter the weight of flour and water to get the hydration, and correlate it with the corresponding bread texture and suitable type.",
        "Real-time dough hydration calculation",
        "Automatic hydration-level judgment",
        "Complete hydration-texture correlation table",
        "Visualized hydration-range display",
        "Adjusting bread recipe hydration",
        "Determining the bread type suited to the dough",
        "Learning baking hydration knowledge",
        "Reference for new recipe development",
    ]))
    write('fermentation-time', build('fermentation-time', [
        "🏋️ Fermentation Time Adjuster",
        "Adjust the standard fermentation time based on actual temperature and humidity (reference temperature 27°C)",
        "Core formula (by input variables): max(0.7, min(1.3, humFactor)); (q10)^(temp - refTemp / 10); 1 + humDiff × 0.008",
        "Fermentation time adjustment",
        "/ Fermentation time adjustment",
        "Standard fermentation time (minutes)",
        "Actual temperature (°C)",
        "Actual humidity (%)",
        "Fermentation type",
        "Yeast fermentation",
        "Sourdough fermentation",
        "Cold slow fermentation",
        "📊 Temperature-Fermentation Speed Reference Table",
        "Relative speed",
        "Cold slow fermentation, flavor development",
        "Low-temperature fermentation, suitable for overnight",
        "Cool environment, time extended",
        "Slightly low room temperature, slightly extended",
        "Reference temperature (ideal)",
        "Warm, fermentation accelerates",
        "High temperature, needs monitoring",
        "Overheated, yeast starts to deactivate",
        "Yeast dies, fermentation stops",
        "💡 Fermentation speed changes with temperature following the Q10 coefficient (about 2-3): for every 10°C rise, fermentation speed roughly doubles to triples. The reference temperature is set to 27°C.",
        "📚 In-Depth: Fermentation Time Adjuster",
        "When room temperature deviates from the standard bread fermentation temperature (about 26°C), adjust the time needed for the first fermentation.",
        "In winter the room is cold, in summer it is warm; adjust fermentation duration by the temperature difference.",
        "Estimate the total duration of overnight refrigeration (low-temperature) fermentation.",
        "Correction for 20°C room temperature vs the 26°C standard",
        "By the Q10 rule, every 10°C drop roughly halves the fermentation rate (Q10≈2). Standard 26°C needs 60min; at 20°C: t = 60 × 2^((26-20)/10) = 60 × 2^0.6 ≈ 60 × 1.52 ≈ 91min, i.e. extend to about 91 minutes.",
        "What is Q10 and how is it used in baking?",
        "Q10 is the factor by which a physiological/chemical reaction rate increases per 10°C rise; yeast fermentation generally uses 2-3. Use t₂ = t₁ × Q10^((T₁-T₂)/10) to estimate fermentation time at different temperatures.",
        "How to calculate cold-retard fermentation time?",
        "At around 4°C yeast activity is very low; first fermentation often takes 8-12 hours or overnight, with better flavor. The same Q10 formula can extend the low-temperature duration, but at low temperature it is only approximate; judge by dough state (risen about 1x, finger poke does not spring back).",
        "About 'Fermentation Time Adjustment'",
        "The fermentation time adjuster, based on the Q10 temperature coefficient and a humidity factor, adjusts the standard fermentation time according to the actual environment.",
        "Temperature Q10 coefficient adjustment",
        "Humidity impact factor calculation",
        "Supports yeast / sourdough / cold fermentation",
        "Provides fermentation time ranges and tips",
        "Adjusting fermentation at different ambient temperatures",
        "Cold slow fermentation time estimation",
        "Sourdough fermentation time planning",
        "Learning fermentation principles",
    ]))

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'food')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'food')
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
    out = {'slug': slug, 'industry': 'food', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
#!/usr/bin/env python3
# body for food b5: stats-simulator-flavor / syrup-brix-converter / vitamin-c-compare / wine-alcohol-converter

def main():
    # stats-simulator-flavor (19)
    write('stats-simulator-flavor', build('stats-simulator-flavor', [
"Customer Flavor Preference Chart (Local Simulation)",
"Enter sample votes for each flavor to generate a local preference distribution and bar chart",
"View the Flavor Preference Statistics (Local Simulation) Guide",
"Share = category votes / total votes x 100%; the highest-share item is the most preferred flavor. The distribution is shown as bars for visual comparison; data comes from your locally entered sample and is for directional reference only.",
"Enter one line per 'flavor,votes', e.g.: sweet,40",
"sweet,40\nsalty,25\nspicy,20\nsour,15",
"In-Depth: Flavor Preference Statistics (Local Simulation)",
"New-product flavor research",
"Menu optimization direction",
"Preference distribution visualization",
"Enter sample data to generate a local flavor preference distribution (share = category sample / total sample).",
"Sample of 100 people: 40 sweet-leaning, 25 salty-leaning, 20 spicy-leaning, 15 sour-leaning -> sweet 40% highest, salty 25%, spicy 20%, sour 15%.",
"Data source?",
"Simulated from your locally entered sample data; not a real market survey, for directional reference only.",
"Use?",
"Used to visualize preferences for menu structure and new-product R&D, aiding decisions.",
"About the Customer Flavor Preference Chart (Local Simulation)",
"Customer flavor preference chart (local simulation). A cooking tool to help master ingredient ratios and nutrition precisely.",
"e.g.: sweet,40 salty,25 spicy,20 sour,15",
    ]))

    # syrup-brix-converter (34)
    write('syrup-brix-converter', build('syrup-brix-converter', [
"Syrup Concentration Converter",
"Convert between syrup Brix, sugar content, specific gravity, refractive index and Baumé",
"The syrup Brix / sugar content / specific gravity / refractive index / Baumé converter performs professional calculation and outputs results based on the input parameters.",
"View the Syrup Concentration Converter (Brix/SG/Baumé/RI) Guide",
"Brix input",
"Specific gravity (SG) input",
"Baumé input",
"Baumé (°Bé)",
"Common syrup concentration reference",
"Thin syrup",
"Good for lightly sweet drinks",
"Medium syrup",
"Good for brushing pastry surfaces",
"Thick syrup",
"Good for jam cooking",
"High-concentration syrup",
"Good for candied fruit and preserves",
"The syrup concentration converter supports quick conversion between Brix, specific gravity (SG), Baumé (°Bé) and refractive index (RI), suitable for baking, beverages, food processing and more.",
"Specific gravity SG = 1 + (Brix/258.6 - (Brix/258.2)^2)",
"Baumé °Bé = Brix / 1.8 (approx.)",
"Refractive index RI ≈ 1.3330 + Brix × 0.00146",
"In-Depth: Syrup Concentration Converter (Brix/SG/Baumé/RI)",
"Brewing sugar-level reference",
"Beverage sugar-level blending",
"Refractometer reading conversion",
"Brix and SG relation?",
"Brix is the sugar",
"mass fraction",
"approximation; SG is specific gravity, the two convert via the formula above, with slight deviation by sugar type.",
"Refractive index",
"How to use RI?",
"A handheld refractometer reads RI or Brix directly, commonly used for quick on-site sugar measurement.",
"About the Syrup Concentration Converter",
"The syrup concentration converter is an online tool for daily life. A practical and convenient daily-life tool.",
    ]))

    # vitamin-c-compare (27)
    write('vitamin-c-compare', build('vitamin-c-compare', [
"Vitamin C Content Comparison",
"Compare vitamin C content of common foods; pick 2-5 foods to generate a comparison chart",
"View the Vitamin C Content Comparison Guide",
"Vitamin C content per 100 g edible portion (mg/100g): fresh jujube ~243, green pepper ~72, kiwi ~62, broccoli ~51, strawberry ~47, orange ~33, tomato ~14, apple ~4; comparison ratio = higher content / lower content; adult RDA 100 mg/day; actual intake = food amount (g) x content / 100; cooking loss ~30% to 50%, raw or quick-fried retains more.",
"Daily RDA (mg)",
"Generate comparison",
"Clear selection",
"Select foods to compare (selected",
"Click to select; data is vitamin C content per 100 g edible portion",
"Vitamin C (ascorbic acid) is an essential water-soluble vitamin involved in immunity, collagen synthesis and antioxidant defense. This tool has built-in vitamin C data for 30+ foods.",
"Recommended intake",
"Adult: 100 mg/day",
"Pregnant: 115 mg/day",
"Lactating: 150 mg/day",
"Smoker: +35 mg/day",
"In-Depth: Vitamin C Content Comparison",
"Fruit/veggie choices for vitamin C",
"Daily intake planning",
"Intuitive bar comparison",
"Compare selected foods' vitamin C per 100 g and generate a bar chart; adult RDA 100 mg/day.",
"Green pepper (~80), kiwi (62), orange (53), strawberry (59) mg/100 g -> green pepper highest; an adult needs 100 mg, about 130-160 g kiwi (62-92 mg/100 g by variety) suffices.",
"Recommended intake?",
"Adult 100 mg/day; pregnant 115, lactating 150, smoker extra +35 mg/day.",
"Does cooking lose vitamin C?",
"Vitamin C is heat- and acid-sensitive and easily lost to oxidation; quick-fry or eat raw (e.g. bell pepper, kiwi) retains more.",
"About the Vitamin C Content Comparison",
"The vitamin C content comparison is an online tool for daily life. A practical and convenient daily-life tool.",
    ]))

    # wine-alcohol-converter (38)
    write('wine-alcohol-converter', build('wine-alcohol-converter', [
"Wine Alcohol Content Converter",
"Calculate alcohol by specific-gravity method; supports SG/Brix/Plato conversion",
"The specific-gravity alcohol calculator with SG/Brix/Plato conversion performs professional calculation and outputs results based on the input parameters.",
"View the Wine Alcohol Content Converter (Balling) Guide",
"Alcohol calculation",
"SG/Brix/Plato conversion",
"Enter fermentation parameters",
"Original gravity (OG)",
"OG unit",
"Plato (Plato)",
"Final gravity (FG)",
"FG unit",
"Calculate alcohol",
"Unit conversion",
"Common drink reference",
"Dry red wine",
"Sweet wine",
"Beer (pale)",
"Beer (IPA)",
"Cider",
"Mead",
"By measuring the specific gravity before and after fermentation, the alcohol content can be calculated. This tool uses the Balling formula and also supports conversion among the three common concentration units SG, Brix and Plato.",
"Simplified formula: ABV = (OG - FG) × 131.25",
"Brix ≈ ((SG - 1) × 259 - 2.5) (approx.)",
"In-Depth: Wine Alcohol Content Converter (Balling)",
"Home-brew alcohol estimate",
"Sugar-alcohol monitoring",
"Brix/Plato/SG conversion",
"Simplified ABV = (OG - FG) × 131.25; Balling: ABV = (76.08×(OG-FG)/(1.775-OG)) × (FG/0.794); Brix ≈ (SG-1)×259 - 2.5.",
"OG=1.050, FG=1.010 -> simplified ABV = (0.050-0.010) × 131.25 = 5.25%; Brix ≈ (1.050-1)×259 - 2.5 = 10.45.",
"Is the Balling formula more accurate?",
"It accounts for alcohol-density correction and is slightly more accurate than the simplified formula; both are empirical approximations, with the measured value as the true reference.",
"How to convert units?",
"Brix and Plato are roughly equivalent (sugar",
"mass fraction",
"), and convert to SG via empirical formulas.",
"About the Wine Alcohol Content Converter",
"The wine alcohol content converter is an online tool for daily life. A practical and convenient daily-life tool.",
    ]))

if __name__ == '__main__':
    main()

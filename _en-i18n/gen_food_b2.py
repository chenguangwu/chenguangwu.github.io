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
def main():
    # convert-19 (17)
    write('convert-19', build('convert-19', [
"Red Wine ABV Converter (Specific Gravity Method)",
"ABV (% vol) ~ (original gravity - final gravity) / 0.00736 (empirical approx, 20 C)",
"View the Red Wine ABV Converter (Specific Gravity Method) Guide",
"Specific-gravity estimation of ABV: ABV (% vol) ~ (OG - FG) / 0.00736; apparent attenuation = (OG - FG) / OG x 100%; mass fraction = ABV x 0.789 / FG. Empirical approximation; actual value by test.",
"Original gravity (OG)",
"Final gravity (FG)",
"In-Depth: Red Wine ABV Converter (Specific Gravity Method)",
"Quick homebrew ABV estimation",
"Fermentation sugar-alcohol monitoring",
"Recipe sugar level adjustment",
"Simplified ABV = (OG - FG) x 131.25; OG/FG are pre/post-fermentation specific gravity (SG).",
"How large is the specific-gravity error?",
"About +/-0.3% vol, affected by fermentation by-products; precise ABV by distillation-density method or alcoholmeter.",
"How to measure OG/FG?",
"Read with a hydrometer (saccharometer) before and after fermentation, applying temperature correction to the standard 20 C.",
"About the Red Wine ABV Converter (Specific Gravity Method)",
"Red wine ABV converter (specific gravity method). A cooking tool to help master ingredient ratios and nutrition precisely.",
    ]))

    # convert-20 (35)
    write('convert-20', build('convert-20', [
"Chili Heat Converter (Scoville Units)",
"Scoville Heat Units (SHU) approximate public reference values",
"View the Chili Heat Converter (Scoville) Guide",
"Dish heat (SHU) = chili Scoville index x chili amount / total dish weight; capsaicin concentration (ppm) = SHU / 15; total capsaicin (mg) = ppm x amount / 1000; max amount = target heat cap x total dish weight / SHU; dilution factor = current dish heat / target heat cap. Heat grade by dish heat: mild, light, medium, high, extra-hot, extreme, brutal.",
"Conversion mode",
"By chili variety and amount",
"Enter SHU directly",
"Chili variety",
"Bell pepper",
"Banana pepper",
"Jalapeno",
"Serrano",
"Cayenne",
"Thai chili",
"Habanero",
"Ghost pepper (Bhut Jolokia)",
"Carolina Reaper",
"Chili amount (g)",
"Total dish weight (g)",
"Target heat cap (SHU)",
"Common chili Scoville heat (SHU)",
"Scoville heat note",
"Scoville index (SHU) public reference range; values vary by variety and origin as ranges, for reference only.",
"In-Depth: Chili Heat Converter (Scoville)",
"Recipe heat labeling",
"Common chili grade comparison",
"Heat batch scaling",
"SHU ~ capsaicin content (ppm) x 15; 1 mg/g = 1000 ppm.",
"A chili with capsaicin 0.5 mg/g (=500 ppm) -> SHU ~ 500 x 15 = 7500; vs jalapeno about 2500-8000 SHU.",
"What is SHU?",
"The Scoville index is the sugar-water dilution multiple needed to no longer taste heat; the larger the number, the hotter.",
"How to convert to mg capsaicin?",
"Empirically SHU ~ capsaicin ppm x 15; different capsaicin profiles cause deviation in the approximation.",
"About the Chili Heat Converter (Scoville Units)",
"Chili heat converter (Scoville units). A cooking tool to help master ingredient ratios and nutrition precisely.",
    ]))

    # convert-concentration (19)
    write('convert-concentration', build('convert-concentration', [
"Syrup Concentration Converter (Brix)",
"Brix <-> Specific Gravity (SG) empirical conversion",
"View the Syrup Concentration Converter (Brix) Guide",
"Brix and SG conversion: from Bx to SG = 1 + Bx / (258.6 - (Bx / 258.2) x 227.1); from SG to Bx = ((182.4601 x SG - 775.6821) x SG + 1262.7794) x SG - 669.5622. At 20 C approximate density = SG x 998.2 kg/m3.",
"Specific gravity (SG)",
"In-Depth: Syrup Concentration Converter (Brix)",
"Jam / syrup sugar control",
"Brewing sugar cross-reference",
"Sugar",
"Mass fraction",
"Conversion",
"Brix ~ sugar mass fraction %; Baume degB ~ Brix / 1.8; SG = 1 + Brix/258.6 - (Brix/258.2)^2.",
"Brix=20 -> sugar mass fraction ~20%; degB ~20/1.8~11.1; SG~1+20/258.6-(20/258.2)^2~1.0713.",
"Is Brix the same as sugar content?",
"For pure sucrose solution Brix ~ sucrose mass fraction; for mixed sugars or solids it is only approximate.",
"What is Baume used for?",
"Baume is often used for quick liquid relative-density reading, convenient for on-site sugar estimates in brewing and chemical industries.",
"About the Syrup Concentration Converter (Brix)",
"Syrup concentration converter (Brix). A cooking tool to help master ingredient ratios and nutrition precisely.",
    ]))

    # convert-ratio-seasoning (18)
    write('convert-ratio-seasoning', build('convert-ratio-seasoning', [
"Seasoning Ratio Scaling (Batch Conversion)",
"Ingredient ratio scaling: new amount = base amount x scale factor",
"View the Seasoning Ratio Scaling (Batch Conversion) Guide",
"Seasoning ratio: seasoning amount = main ingredient weight x factor; total weight = main + seasoning; seasoning per 100 g main = factor x 100; main share = main / total x 100%, seasoning share is the rest.",
"Base amount (g)",
"Scale factor (x)",
"In-Depth: Seasoning Ratio Scaling (Batch Conversion)",
"Central-kitchen recipe upscaling",
"Home-banquet batch adjustment",
"Standardized seasoning",
"New amount = original amount x (target batch / original batch).",
"Original recipe salt 10 g for 4 people, target 12 people -> salt = 10 x (12/4) = 30 g; other seasonings scale proportionally.",
"Do all seasonings scale linearly?",
"Salty-umami base can scale linearly, but spices, Sichuan pepper etc. should be slightly reduced to avoid over-intensity; season in stages and taste.",
"What to note when doubling batches?",
"Large batches heat and absorb flavor more slowly; add in stages and unify the taste adjustment at the end.",
"About the Seasoning Ratio Scaling (Batch Conversion)",
"Seasoning ratio scaling (batch conversion). A cooking tool to help master ingredient ratios and nutrition precisely.",
    ]))

    # cooking-converter (44)
    write('cooking-converter', build('cooking-converter', [
"Cooking Unit Converter",
"Conversion logic",
"Convert between measuring cups / spoons / weight / temperature by standard factors: 1 US cup = 240 ml, 1 tbsp = 15 ml, 1 tsp = 5 ml, degF = degC x 9/5 + 32.",
"Please select an ingredient",
"/ Cooking Unit Converter",
"View the Cooking Unit Converter Guide",
"Volume conversion",
"Weight conversion",
"Ingredient conversion",
"Temperature conversion",
"Portion adjustment",
"Select ingredient",
"Common oven temperatures",
"Recipe ingredients (one per line, format: amount unit ingredient name)",
"100 g flour\n50 g sugar\n2 eggs\n100 ml milk\n1 tbsp butter\n1 tsp salt",
"Calculate portions",
"Cooking tips",
"Measuring cup standard",
": 1 US cup = 240 ml, 1 imperial cup = 250 ml, China commonly about 240 ml",
"Measuring spoon standard",
": 1 tbsp = 15 ml, 1 tsp = 5 ml, 1 tbsp = 3 tsp",
"Flour",
": 1 cup about 120-130 g (depends on sifting)",
"White sugar",
": 1 cup about 200 g, brown sugar about 220 g",
"Oven temperature",
": home ovens generally 150-220 C, baking commonly 180 C",
"Oil temperature reference",
": low 120 C, medium 150-170 C, high 180-200 C",
"Meat doneness temperature",
": well done 75 C, medium 70 C, rare 60 C",
"In-Depth: Cooking Unit Conversion",
"Imperial recipe to metric",
"Baking volume / weight / temperature conversion",
"Cross-unit measurement conversion",
"Temp degF = degC x 9/5 + 32; 1 cup~240 ml, 1 tbsp~15 ml, 1 tsp~5 ml; volume<->weight needs ingredient density.",
"180 C = 180x9/5+32 = 356 F; flour density~0.53 g/ml, 1 cup (240 ml)~127 g.",
"Why do volume and weight need density?",
"Ingredient densities differ greatly (flour~0.53, water=1, sugar~0.85 g/ml); same volume weighs differently.",
"Common conversions?",
"1 cup=240 ml, 1 tbsp=15 ml, 1 tsp=5 ml; baking is more accurate weighed in grams.",
"About the Cooking Unit Converter",
"Cooking unit converter. A practical daily-life tool, close to life, convenient and handy.",
"100 g flour\n50 g sugar\n2 eggs\n100 ml milk",
    ]))

if __name__ == "__main__":
    main()

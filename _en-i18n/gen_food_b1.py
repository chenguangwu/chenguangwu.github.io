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
    # analysis-cost-6 (22)
    write('analysis-cost-6', build('analysis-cost-6', [
"Cost (Accounting / Control / Gross Margin) Analysis",
"Accounting / Control / Gross Margin",
"View the Cost (Accounting / Control / Gross Margin) Analysis Guide",
"Total cost = main ingredient + auxiliary + seasoning + other costs; gross profit = price - total cost; gross margin = gross profit / price; cost ratio = total cost / price; suggested price = total cost / (1 - target margin).",
"Dish selling price (yuan)",
"Main ingredient cost (yuan)",
"Auxiliary material cost (yuan)",
"Seasoning cost (yuan)",
"Other cost (yuan)",
"Target gross margin (%)",
"In-Depth: Dish Cost Accounting and Gross Margin Analysis",
"Catering items are costed item by item (main, auxiliary, seasoning, other) to obtain the true gross profit and",
"Given a target gross margin, back-calculate the suggested price to aid menu pricing and promotion decisions.",
"Compare each dish's cost ratio to find under-estimated or under-priced dishes for optimization.",
"Example: Signature dish",
"Price 58 yuan, main 15 yuan, auxiliary 5 yuan, seasoning 2 yuan, other 4 yuan: total cost 26 yuan, gross profit 32 yuan, gross margin 55.17%, cost ratio 44.83%; if target margin 55%, suggested price ~57.78 yuan.",
"What is the relation between gross margin and cost ratio?",
"They sum to 100%; gross margin = (price - total cost) / price, cost ratio = total cost / price; the lower the cost ratio, the more room left for profit.",
"How to use the target gross margin?",
"Enter the desired margin; the tool back-calculates the suggested price by total cost / (1 - target margin); target margin must be below 100%, otherwise costs cannot be covered.",
"About the Cost (Accounting / Control / Gross Margin) Analysis",
"Cost (accounting / control / gross margin) analysis. A cooking tool to help master ingredient ratios and nutrition precisely.",
    ]))

    # analysis-menu (24)
    write('analysis-menu', build('analysis-menu', [
"Menu Gross Margin Auto-Analysis",
"Menu Gross Margin Auto-Analysis Online Tool",
"Enter each dish's cost, price and sales line by line; compute per-dish gross profit and margin, then a sales-weighted store-wide composite margin, and flag the highest and lowest margin dishes. Data is processed locally in the browser only, never uploaded.",
"View the Menu Gross Margin Auto-Analysis Guide",
"Per-dish margin = (price - cost) / price x 100%",
"Composite margin = sum(price x sales - cost x sales) / sum(price x sales) x 100%",
"Compute each dish's gross profit and margin, then a sales-weighted store-wide composite margin, flagging the highest and lowest margin dishes. All data is processed locally only, never uploaded.",
"Dish list (one per line: name, cost, price, sales)",
"Kung Pao Chicken,12,32,180\nStir-fried Vegetables,5,18,150\nFish with Pickled Cabbage,26,68,95\nTomato Beef Brisket,22,58,80\nSteamed Rice,1.5,3,420",
"Analyze Margin",
"In-Depth: Menu Gross Margin Auto-Analysis",
"Identify high / low margin dishes",
"Menu structure optimization and pricing",
"Overall profitability assessment",
"Per dish",
"= (price - cost) / price; overall margin = sum(margin) / sum(price) x 100%.",
"Three dishes (cost/price): (10,28)(6,18)(15,40) -> margin 18/12/25, total 55; total sales 86 -> overall margin = 55/86 ~ 64.0%.",
"How to balance high and low margins?",
"Use high-margin dishes to lift average ticket; use high-traffic low-margin dishes to drive volume; avoid an all-low-margin menu that fails to profit.",
"What does overall margin represent?",
"Reflects the menu's composite profitability, a core metric for pricing and structure adjustment; catering usually targets ~60% composite margin.",
"About the Menu Gross Margin Auto-Analysis",
"Menu gross margin auto-analysis. A cooking tool to help master ingredient ratios and nutrition precisely.",
"Kung Pao Chicken,12,32,180",
    ]))

    # beer-gravity-estimator (49)
    write('beer-gravity-estimator', build('beer-gravity-estimator', [
"Beer Original Gravity Estimator",
"Estimate original gravity (OG), final gravity (FG) and alcohol by volume (ABV) from malt amount, water and mash efficiency",
"Core formula (by input variables): (-1 x 616.868 + 1111.14 x og - 630.272 x og x og + 135.997 x og x og x og) / (1); ((og - 1) x 259) / (og x 259 + 0) x 100; 1 + (totalPoints x eff / water) x 0.0038",
"View the Beer Original Gravity Estimator Guide",
"Total water (L)",
"Mash efficiency (%)",
"Expected attenuation (%)",
"Malt recipe",
"Add multiple malts; choose a type or customize the sugar",
"+ Add malt",
"Common malt reference data",
"Malt type",
"Max yield (PPG)",
"Color (SRM)",
"Pale malt",
"Base malt",
"Munich malt",
"Malt flavor",
"Vienna malt",
"Pale ale",
"Crystal malt",
"Caramel sweetness",
"Chocolate malt",
"Dark beer",
"Black malt",
"Stout / Porter",
"Wheat malt",
"Wheat beer",
"Oat flakes",
"Increase body and fullness",
"This tool helps homebrewers estimate key beer parameters from the recipe. Enter malt recipe, water and efficiency to compute original gravity, final gravity and ABV.",
"OG = 1 + (total sugar x efficiency / water) x 0.038",
"FG = 1 - (OG - 1) x attenuation",
"Beer type reference",
"Pale Lager",
"IPA (India Pale Ale)",
"Stout",
"In-Depth: Beer Original Gravity Estimator",
"Homebrew original gravity (OG) estimation",
"Attenuation and final gravity (FG) assessment",
"Alcohol by volume (ABV) estimate",
"OG = 1 + (total sugar x efficiency / water) x 0.038; FG = 1 - (OG-1) x attenuation; ABV = (OG - FG) x 131.25.",
"OG=1.050, FG=1.010 -> ABV = (0.050-0.010) x 131.25 = 5.25%; attenuation = (0.050-0.010)/0.050 = 80%.",
"What are OG and FG?",
"OG is the pre-fermentation original gravity, FG is the post-fermentation final gravity; their difference reflects how much sugar converted to alcohol.",
"Is the ABV empirical formula accurate?",
"ABV=(OG-FG)x131.25 is a common approximation with error about +/-0.3% vol; the precise value should be measured by an alcohol hydrometer or distillation.",
"About the Beer Original Gravity Estimator",
"Beer original gravity estimator is an online tool in daily life. A practical daily-life tool, close to life, convenient and handy.",
    ]))

    # calc-concentration (16)
    write('calc-concentration', build('calc-concentration', [
"Percentage Calculator (Food)",
"Calculate percentages, proportions, growth rates and more",
"Salt concentration calculation (curing concentration)",
"/ Salt concentration calculation (curing concentration)",
"View the Salt Concentration (Curing) Calculator Guide",
"Curing saltiness = salt (g) / (salt + water) total mass (g) x 100%; if counted by water alone it is salt / water x 100%, the two bases differ in value and the recipe must state which; common concentrations: vegetable pickling 3%-5%, cured meat 6%-8%, brine preservation 10%+ inhibits bacteria; salt amount = target concentration x total mass / (1 - target concentration) back-calculated.",
"In-Depth: Salt Concentration (Curing) Calculator",
"Pickles / cured meat salt concentration control",
"Recipe reproduction and standardization",
"Salt-reduction health adjustment",
"Salt % = salt mass / (salt mass + water mass) x 100% (by total weight).",
"Salt 200 g + water 5 kg (5000 g) -> saltiness = 200 / (200+5000) x 100% ~ 3.85%.",
"Saltiness by total weight or by water weight?",
"This tool calculates by total weight (salt + water), closer to the actual brine ratio; by water weight it runs higher, so watch the basis.",
"What is a safe salt concentration?",
"Curing preservation generally needs >=3% to inhibit most bacteria; long-term storage often uses 5%-10%, depending on process and storage conditions.",
    ]))

    # checker-13 (40)
    write('checker-13', build('checker-13', [
"Sanitation (Standard / Inspection / Rectification) System",
"Food production sanitation compliance check, scoring across six dimensions against GB 14881-2013 and generating rectification advice",
"Core formula (by input variables): total / maxScore x 100",
"View the Food Production Sanitation Compliance Check Guide",
"1. Site environment and facility sanitation (1-10)",
"2. Production workshop sanitation management (1-10)",
"3. Equipment and utensil cleaning and disinfection (1-10)",
"4. Personnel sanitation management (1-10)",
"5. Raw material and storage sanitation (1-10)",
"6. Inspection and record management (1-10)",
"Total plate count result (CFU/g)",
"Coliform detection status",
"Not detected",
"Detected (unqualified)",
"Run sanitation check",
"About the Sanitation (Standard / Inspection / Rectification) System",
"Food production sanitation compliance check tool, scoring across six dimensions - site facilities, workshop management, equipment disinfection, personnel sanitation, raw storage, inspection records - against GB 14881-2013, generating rectification advice.",
"Six-dimension sanitation check scoring",
"GB 14881 standard cross-reference",
"Inspection report export",
"Rectification tracking management",
"Food manufacturer self-inspection",
"Regulatory inspection",
"HACCP system verification",
"Food safety monthly audit",
"In-Depth: Food Production Sanitation Compliance Check",
"Food enterprise six-dimension self-inspection",
"Inspection preparation and rectification",
"Inspection report and rectification tracking",
"Each of six dimensions 0-10, total = sum; pass rate = total / 60 x 100%; TVC <=10000 CFU/g and coliform = 0 is microbiologically qualified.",
"Six-dim scores [9,8,9,10,8,7] = total 51 -> pass rate = 51/60 = 85%; TVC=5000 <= 10000 qualified.",
"What do the six dimensions mean?",
"Against GB 14881-2013 dimensions: site layout, plant facilities, equipment, sanitation management, personnel, management system.",
"How to set the pass line?",
"Recommend composite pass rate >=85% and microbiological indicators met; any critical item (e.g. coliform) unqualified must be rectified.",
"Total plate count judged per GB 14881-2013 general food production sanitation standard",
"Coliform must not be detected (GB 29921 pathogen limits)",
"Food contact surface temperature <=25 C, humidity <=65%",
"Personnel health certificate holding rate must be 100%",
"Rectification should be completed and rechecked within 48 hours",
    ]))

if __name__ == "__main__":
    main()

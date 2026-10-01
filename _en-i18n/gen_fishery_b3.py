#!/usr/bin/env python3
# fishery batch3 (6 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'fishery')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'fishery')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'assessor-risk-4': [
"♻️ Fish Disease Risk Assessor (Environmental)",
"Assess fish disease risk from environmental factors such as temperature and water quality.",
'📖 View the "Farming Environment Risk Score Guide"',
"Fish disease risk = f(water temperature, density, water quality)",
"Dissolved oxygen DO (mg/L)",
"Ammonia nitrogen NH3-N (mg/L)",
"Nitrite NO2 (mg/L)",
"Stocking density (fish/mu)",
"📚 In-Depth Analysis: Farming Environment Risk Score",
"Before stocking or at the change of season, score environmental factors such as water temperature, DO, pH, ammonia nitrogen, nitrite and density to anticipate disease risk.",
"Refer to water-quality baselines such as GB 11607 and NY 5051 to identify out-of-range factors.",
"When the risk is high, give management advice such as water exchange, adsorption and reducing density.",
"Common carp, 25 ℃, DO 5, pH 7.5, ammonia nitrogen 0.5, nitrite 0.1, density 1500 fish/mu",
"With the default parameters all factors are in the safe range and the risk score is low (level 1 in the example), indicating safe water-quality parameters and low risk; if ammonia nitrogen or nitrite rises or the density is too high, the score and level rise accordingly and water-exchange or adsorption advice is given.",
"What is the score based on?",
"It combines the suitable water-temperature range, the dissolved-oxygen lower limit, the ammonia nitrogen and nitrite thresholds and",
"stocking density",
"and scores them against fishery water-quality standards.",
"Is a low score enough?",
"The risk score is an early warning; daily pond patrols and pathogen monitoring are still needed, and re-assess promptly when the environment changes abruptly.",
"An abrupt water-temperature change of >3°C alone can trigger stress, lowering immunity and easing infection",
"At DO <3 mg/L fish gasp at the surface, and <1 mg/L can cause pond-wide death",
"Ammonia nitrogen is directly toxic to fish, and un-ionised ammonia (NH3) is even more toxic",
'Nitrite causes "brown blood disease", impairing oxygen-carrying capacity',
"The hot season (July to September) is a peak period for fish disease, so strengthen water-quality monitoring",
'About "Fish Disease Risk Assessor (Environmental)"',
"A fish disease risk assessment tool: enter water-quality parameters such as temperature, dissolved oxygen, pH and ammonia nitrogen to assess the fish disease risk level comprehensively and receive management advice.",
"Comprehensive assessment of six water-quality parameters",
"Adapted to four farmed species",
"Factor-by-factor risk analysis",
"Targeted water-quality management advice",
"Farm water-quality monitoring",
"Fish disease prevention and warning",
"Stocking density optimisation",
"Aquaculture management",
],
'tank-volume': [
"🧊 Tank Volume Calculator",
"Compute the volume of a water tank or pond from its dimensions.",
'📖 View the "Culture Tank / Pond Volume and Water Capacity Guide"',
"V = length × width × height",
"Rectangular box",
"Cylinder",
"Cone",
"Hemisphere",
"Trapezoidal pond",
"Recommended stocking density (kg/m³)",
"Fill ratio (%)",
"• Rectangular box: V = length × width × height, surface area = length × width",
"• Cylinder: V = π × R² × H, surface area = π × R²",
"• Cone: V = (1/3) × π × R² × H, surface area = π × R²",
"• Hemisphere: V = (2/3) × π × R³, surface area = 2 × π × R²",
"• Trapezoidal pond: V = (top width + bottom width) / 2 × height × length, surface area = (top width + bottom width) / 2 × length",
"Stocking density reference:",
"Conventional ponds 5-15 kg/m³, industrial systems 20-50 kg/m³. 1 kg/m³ is a conservative value.",
"🔄 Unit Converter",
"Litres (L)",
"Gallons (US)",
"Mu·metre (mu × water depth)",
"📚 In-Depth Analysis: Culture Tank / Pond Volume and Water Capacity",
"Compute the geometric volume for rectangular, cylindrical, conical, hemispherical and trapezoidal shapes, then multiply by the fill ratio to get the actual water capacity.",
"Combine the stocking density (kg/m³) to estimate the maximum carrying capacity and guide stocking planning.",
"Quickly verify the effective water volume when converting or building a tank.",
"Rectangular tank 10×5×2 m, 90% fill, density 0.8 kg/m³",
"Default example: geometric volume = 10×5×2 = 100 m³; actual water capacity = 100×90% = 90 m³ (≈ 90,000 L); at 0.8 kg/m³ the maximum carrying capacity is ≈ 72 kg. Cylinders, cones and other shapes convert the same way with their own formulas (πr²h, (1/3)πr²h and so on).",
"Why multiply by the fill ratio?",
"A tank should not be filled to the brim; leaving a safety margin prevents overflow and eases aeration and gas distribution, so the actual water capacity is less than the geometric volume.",
"How should a density of 0.8 kg/m³ be understood?",
"It is an empirical upper limit on carrying density, constrained by aeration and water-exchange capacity; intensive farming can go higher but needs the matching equipment.",
'About "Tank Volume Calculator"',
"Tank Volume Calculator. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
],
'fish-weight': [
"⚖️ Fish Weight Estimator",
"Estimate fish weight from body length, girth and species coefficient.",
'📖 View the "Fish Length-Weight Estimation (W=aLᵇ) and Condition Factor Guide"',
"Fish weight = a·body length^b",
"Custom parameters",
"Body length (cm)",
"Parameter a",
"Parameter b",
"Measured weight (g, optional)",
"⚖️ Estimate weight",
"Length-weight relationship:",
"where W is weight (g), L is body length (cm) and a and b are intraspecific regression parameters",
"Condition factor:",
"K < 1.0: thin; 1.0-1.2: fair; 1.2-1.5: good; > 1.5: excellent",
"The a and b values vary with region, season and age; this table gives common reference values. b is usually close to 3, indicating isometric growth; a deviation from 3 indicates allometric growth.",
"🐟 a and b Parameters for Common Species",
"Applicable body-length range",
"Isometric growth",
"Negative allometric growth",
"Near-isometric",
"Positive allometric growth",
"📚 In-Depth Analysis: Fish Length-Weight Estimation (W=aLᵇ) and Condition Factor",
"When there is no scale on site, estimate weight quickly from body length for grading, feed-amount estimation and growth monitoring.",
"Take the empirical parameters a and b for the species (or custom ones) and apply W = a·Lᵇ.",
"Compute the condition factor K to assess the fish's plumpness and health.",
"Grass carp 30 cm long, a=0.0207, b=3.05",
"With the default parameters: W = 0.0207 × 30^3.05 ≈ 673 g (about 1.35 jin); the condition factor K = (673/30³)×100 ≈ 2.49, within the usual healthy range for grass carp. If a measured weight is available, compare the deviation.",
"Where do the a and b parameters come from?",
"They come from a length-weight regression (W=aLᵇ) over many samples of that species; values differ widely between species, so use the empirical values for the species in question.",
"What do high and low condition factors K indicate?",
"A low K means the fish is thin and a high K means it is fat; combine with water temperature and feeding to judge nutritional status, and check for disease or density problems when it is abnormal.",
'About "Fish Weight Estimator"',
"Fish Weight Estimator is an online tool in the fishery and aquaculture field. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
"Leave blank to see the estimate only",
],
'feed-protein-fat': [
"🥗 Feed Protein and Fat Ratio",
"Look up the protein and fat requirement ratio of aquaculture feed by species and stage.",
'📖 View the "Feed Protein-to-Fat Ratio Guide"',
"Protein-to-fat ratio = nutritional requirement",
"Farm species",
"Eel",
"Growth stage",
"Fry stage",
"Fingerling stage",
"Adult stage",
"🔍 Query and calculate",
"Basis:",
"Protein and fat requirements follow empirical values from the NRC aquaculture nutrition standards; digestible energy is calculated at 16.7 kJ/g for protein, 37.7 kJ/g for fat and 16.7 kJ/g for carbohydrate (estimated at 25%); protein-to-fat ratio = protein% / fat%.",
"Protein and Fat Requirements by Species Group",
"Protein (%)",
"Fat (%)",
"Warm-water fish",
"Fry / fingerling / adult",
"Cold-water fish",
"📚 In-Depth Analysis: Feed Protein-to-Fat Ratio",
"Set the protein-to-fat ratio when formulating compound feed to avoid nutritional imbalance",
"Assess whether the nutritional profile of a commercial feed suits the target species and growth stage",
"Use the protein-to-fat ratio and digestible energy to judge a fattening or maintenance formula",
"Formula check for warm-water fish at the adult stage",
"Entering 30% protein and 6% fat: the protein-to-fat ratio = 30 / 6 = 5.00 : 1 and the digestible energy is about 1.14 kJ/g. This indicates a high-protein high-energy feed that promotes growth, but excess fat easily causes fatty liver, so combine it with",
"feeding rate",
"and water-quality adjustment.",
"What protein-to-fat ratio is suitable?",
"For most warm-water farmed fish at the adult stage a ratio of 4:1 to 6:1 is reasonable; the fry and fingerling stages favour protein, while the fattening stage can raise fat somewhat, adjusted to the species and stage.",
"Is more fat always better?",
"No. Fat supplies much energy, but excess deposits in the liver causing fatty liver and affects feed palatability and water quality, so it must be matched to protein with an upper limit.",
'About "Feed Protein and Fat Ratio"',
"Feed Protein and Fat Ratio - look up the protein and fat requirements by fish or shrimp species and growth stage and compute the ratio, an online fishery and aquaculture tool. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
],
'feeding-rate': [
"🐟 Feeding Rate Calculator",
"Compute the daily feeding rate from fish biomass and feeding percentage.",
'📖 View the "Feeding Rate Recommendation (by Size and Water Temperature) Guide"',
"Feeding rate = body weight × daily rate",
"Size class",
"Fry/fingerling",
"Small",
"Medium",
"Large",
"Size class reference:",
"• Fry/fingerling: fish <50 g / shrimp <1 g",
"• Small: fish 50-200 g / shrimp 1-5 g",
"• Medium: fish 200-500 g / shrimp 5-10 g",
"• Large: fish >500 g / shrimp >10 g",
"Feeding principles:",
"• Feed more in warm weather and less in cold; more on sunny days and less on cloudy or rainy days",
"• Fry have a high feeding rate and large fish a low one",
"• Best consumed within 30 minutes; excess pollutes the water",
"📊 Feeding Rate Lookup Table (% body weight/day)",
"📚 In-Depth Analysis: Feeding Rate Recommendation (by Size and Water Temperature)",
"By species, size stage and water temperature, get the body weight",
"feeding rate, which guides the daily feed amount.",
"Split the daily feed amount across the recommended meals to avoid a single excess that pollutes the water.",
"Adjust dynamically with the feeding response, following the little-and-often principle.",
"Feeding plan for medium grass carp at 25 ℃",
"With the default parameters: medium grass carp at 25 ℃ has a recommended feeding rate of about 3.50% body weight per day; for a total fish weight of 1000 kg the daily feed is about 35.00 kg, split into 2-3 meals of about 11.67 kg each, best consumed within 30 minutes.",
"Why does the feeding rate vary with water temperature?",
"Fish metabolism increases as the water warms, so the feeding rate rises within the optimum range; at too high or too low a temperature, reduce it or stop feeding.",
"How much is right per meal?",
"Aim for everything eaten within 30 minutes with no leftover feed; excess spoils the water and wastes feed.",
'About "Feeding Rate Calculator"',
"Feeding Rate Calculator. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
],
'feed-calculator': [
"🐄 Feed Calculator",
"Compute feed requirement and feed conversion ratio for fish farming.",
'📖 View the "Feed Amount and Feed Cost Guide"',
"Feed amount = body weight × feeding rate",
"Total fish weight (kg)",
"Auto-match the feeding rate by water temperature and species",
"Feeding rate (%)",
"Feed unit price (CNY/kg)",
"Farming days (a month counts as 30 days)",
"Daily feed amount = total fish weight × feeding rate (%)",
"Monthly feed requirement = daily feed amount × 30",
"Stage feed cost = daily feed amount × days × feed unit price",
"The feeding rate follows common aquaculture values, but adjust in practice for weather, dissolved oxygen and the fish's feeding response. Usually feed 2-4 times a day, with everything eaten within 30 minutes.",
"📊 Feeding Rate Reference by Species and Water Temperature (% body weight/day)",
"📚 In-Depth Analysis: Feed Amount and Feed Cost Accounting",
"From the total fish weight and the",
"feeding rate",
"estimate the daily, monthly and stage feed requirements to guide purchasing and feeding plans.",
"The feeding rate is matched automatically when the water temperature or species changes (low and high temperatures and different species differ markedly).",
"Combine with the feed unit price to work out the stage feed cost and bring it into the farming cost budget.",
"Grass carp 1000 kg, water temperature 25 ℃, feeding rate 3%, 30 days, unit price 8 CNY/kg",
"With the default parameters: daily feed amount = 1000×3% = 30 kg; monthly requirement ≈ 900 kg; the 30-day feed requirement is 900 kg; cost = 900×8 = 7200 CNY. With auto-matching enabled the feeding rate for grass carp at 25 ℃ is about 3%, giving a similar result.",
"How is the feeding rate usually set?",
"Usually by body-weight",
'; from 15-30 ℃ it rises with temperature, higher for small fish and during the peak growing season, and follow the rule of "little and often, eight-tenths full".',
"Is the automatic feeding rate reliable?",
"The automatic value is an empirical reference; in practice adjust dynamically for feeding response, weather and water quality, and treat the tool only as a budgeting baseline.",
'About "Feed Calculator"',
"Feed Calculator is an online tool in the fishery and aquaculture field. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
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
    out = {'slug': slug, 'industry': 'fishery', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

for slug, en_list in EN.items():
    write(slug, build(slug, en_list))

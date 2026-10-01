#!/usr/bin/env python3
# gen_food-testing_b1.py — food-testing b1 (5 slugs): acid-peroxide-titration/aflatoxin-limit/allergen-cross-risk/assessor-risk-6/coliform-mpn
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'food-testing')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'food-testing')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

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
    out = {'slug': slug, 'industry': 'food-testing', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))


B = {}

B['acid-peroxide-titration'] = [
 '🧪 Acid Value and Peroxide Value Titration Converter',
 'Based on GB 5009.229 (acid value) and GB 5009.227 (peroxide value), it computes the acid value and peroxide value of fats and oils.',
 'Based on GB 5009.229 (acid value) and GB 5009.227 (peroxide value), it computes the acid value and peroxide value of fats and oils. It runs a professional calculation on the input parameters and outputs the result.',
 '📖 Read the "Acid Value and Peroxide Value Titration Usage Guide"',
 'Acid value AV',
 'Peroxide value POV',
 'KOH volume consumed V (mL)',
 'KOH concentration c (mol/L)',
 'Type of fat or oil',
 'Vegetable oil (≤3 mg/g)',
 'Animal fat (≤2.5 mg/g)',
 'Frying oil (≤5 mg/g)',
 'Limit standard (mg KOH/g)',
 'Calculate acid value',
 'Sample Na₂S₂O₃ volume V₁ (mL)',
 'Blank Na₂S₂O₃ volume V₀ (mL)',
 'Na₂S₂O₃ concentration c (mol/L)',
 'Vegetable oil (≤0.25 g/100g)',
 'Animal fat (≤0.20 g/100g)',
 'Frying oil (≤0.50 g/100g)',
 'Limit standard (g/100g)',
 'Calculate peroxide value',
 'Acid value AV (mg KOH/g)',
 'Peroxide value POV (g/100g)',
 'Peroxide value (meq/kg)',
 '📚 Deep Dive: Acid Value and Peroxide Value Titration of Fats and Oils',
 'Quality and rancidity judgement of edible oils',
 'Shelf-life compliance testing of fats and oils',
 'Critical assessment for discarding frying oil',
 'Acid value AV (mg KOH/g) = V × c × 56.1 / m; peroxide value POV (g/100g) = (V₁ − V₀) × c × 1000 / m, where V is the titration volume, c the concentration and m the sample mass.',
 'Acid value: titrating 2.50 mL of 0.1000 mol/L NaOH with a 5.00 g sample gives AV = (2.50 × 0.1000 × 56.1)/5.00 ≈ 2.81 mg KOH/g (passes the ≤3 limit). Peroxide value: blank 0.20, sample 12.50 mL at 0.0020 mol/L, 5.00 g gives POV = (12.30 × 0.0020 × 1000)/5.00 ≈ 4.92 g/100g.',
 'What does a high acid value mean?',
 'Free fatty acids build up as the fat hydrolyses and goes rancid; exceeding the limit points to deterioration or adulteration, so store it cool and away from light.',
 'How do POV and acid value relate?',
 'POV reflects early-stage oxidation (hydroperoxides) while acid value reflects later hydrolysis and oxidation products, so the two together indicate the degree of oxidation.',
 'About the Acid Value and Peroxide Value Titration Converter',
 'An acid value and peroxide value titration converter. A cooking helper for keeping ingredient ratios and nutrition precise.',
]

B['aflatoxin-limit'] = [
 '⚖️ Aflatoxin B1 Limit Comparison Tool',
 'Based on GB 2761, the national food safety standard for mycotoxin limits, it compares a measured value against the limit.',
 'Core formula (by input variables): min(100, ratio × 100)',
 '📖 Read the "Aflatoxin Limit Comparison Usage Guide"',
 'Measured value (μg/kg)',
 'Peanut oil (≤20 μg/kg)',
 'Peanuts and their products (≤20 μg/kg)',
 'Corn and its products (≤20 μg/kg)',
 'Corn oil (≤20 μg/kg)',
 'Rice (≤10 μg/kg)',
 'Rice oil (≤10 μg/kg)',
 'Other edible vegetable oils (≤10 μg/kg)',
 'Soybeans (≤5 μg/kg)',
 'Other cereals (≤5 μg/kg)',
 'Other cereal products (≤5 μg/kg)',
 'Nuts (≤5 μg/kg)',
 'Fermented foods (≤5 μg/kg)',
 'Condiments (≤5 μg/kg)',
 'Infant and young children food (≤0.5 μg/kg)',
 'Food for special medical purposes (≤0.5 μg/kg)',
 'Limit standard (μg/kg)',
 'Compare and interpret',
 '📋 Aflatoxin B1 limit standards (GB 2761)',
 'Limit (μg/kg)',
 'Peanuts, corn and their products, peanut oil, corn oil',
 'Rice, rice oil, other vegetable oils',
 'Soybeans, other cereals and their products, nuts, fermented foods, condiments',
 'Infant food, food for special medical purposes',
 '⚠️ Aflatoxin B1 is a Group 1 carcinogen, so any detection deserves attention. This tool compares values against the GB 2761 limits; an actual judgement must also account for the detection limit of the method.',
 '📚 Deep Dive: Aflatoxin Limit Comparison',
 'Compliance checks for toxins in peanuts and corn',
 'Release inspection of nut products',
 'Pass/fail judgement of sampling results',
 'Judgement rule',
 'Per GB 2761: compare the measured value with the limit for the matching food category (for example, the aflatoxin B₁ limit for peanuts and their products is 20 μg/kg); anything not above the limit passes.',
 'A batch of peanut butter tests at aflatoxin B₁ = 5.0 μg/kg against a limit of 20 μg/kg: 5.0 < 20, so it passes; at 25 it exceeds the limit and the batch must be withdrawn and traced.',
 'Do limits differ by category?',
 'Yes. Limits differ across cereals, legumes, nuts and dairy, and some products such as infant food are stricter, so check GB 2761 by category.',
 'Does any detection mean failure?',
 'No, the value must be compared with the matching limit; the toxin is cumulatively toxic though, so the further below the limit the safer.',
 'About the Aflatoxin B1 Limit Comparison Tool',
 'An aflatoxin B1 limit comparison tool. A cooking helper for keeping ingredient ratios and nutrition precise.',
]

B['allergen-cross-risk'] = [
 '📋 Allergen Cross-Contamination Risk Scorer',
 'It assesses the risk of allergen cross-contamination on a production line, scoring factors such as shared equipment, cleaning method and allergen type.',
 '📖 Read the "Allergen Cross-Contamination Risk Scoring Usage Guide"',
 'Risk assessment factors',
 '1. Allergen type',
 'Peanut (high risk)',
 'Tree nuts (high risk)',
 'Dairy (medium-high risk)',
 'Egg products (medium-high risk)',
 'Soy (medium risk)',
 'Wheat/gluten (medium risk)',
 'Crustaceans/fish (high risk)',
 'Sesame (medium risk)',
 '2. Equipment sharing',
 'Dedicated equipment, not shared',
 'Shared equipment run in sequence',
 'Shared equipment run at the same time',
 '3. Cleaning verification method',
 'Validated CIP plus ATP testing',
 'CIP cleaning, not validated',
 'Manual cleaning',
 'Dry cleaning (wiping or vacuuming)',
 'No cleaning procedure',
 '4. Product changeover interval',
 'At least 24 hours, fully segregated',
 '4-24 hours',
 '1-4 hours',
 'No interval, continuous changeover',
 '5. Physical form (allergen)',
 'Liquid/solution',
 'Paste/puree',
 'Powder/dust (high spreading risk)',
 'Solid particles',
 '6. Amount of allergen added',
 'Trace (<1%)',
 'Small (1-10%)',
 'Medium (10-30%)',
 'Large (>30%)',
 '7. Airborne spread risk',
 'No dust spread',
 'A small amount of dust',
 'Moderate dust spread',
 'Heavy dust or open feeding',
 '8. Packaging segregation',
 'Independent packaging area',
 'Shared packaging line',
 'Shared open area',
 '📚 Deep Dive: Allergen Cross-Contamination Risk Scoring',
 'Allergen control on shared lines',
 'Cleaning validation and changeover assessment',
 'Deciding on a "may contain" statement',
 'Scoring rule',
 'The eight factors (allergen type / equipment sharing / cleaning validation / changeover interval / form / amount added / airborne spread / packaging segregation) each score 0–5, for a maximum of 40; ≤8 is low risk, ≤16 medium-low, ≤24 medium and above 24 high risk.',
 'Shared equipment 4 + cleaning validation 3 + changeover 2 + form 3 + amount 2 + air 1 + packaging 1 + type 2 = 18 points, which is medium risk; strengthen cleaning validation and changeover intervals and consider a "may contain" statement.',
 'When should "may contain" be labelled?',
 'When a line is shared and trace cross-contamination cannot be fully ruled out (medium risk or above), regulations advise an allergen advisory statement.',
 'Is dedicated equipment the safest option?',
 'Yes. A dedicated line or running high-risk allergens (peanut, nuts, milk, egg) last lowers the risk to low and avoids cross-contact.',
 'About the Allergen Cross-Contamination Risk Scorer',
 'An allergen cross-contamination risk scorer. A cooking helper for keeping ingredient ratios and nutrition precise.',
]

B['assessor-risk-6'] = [
 '📋 Microbiological (Pathogen) Risk Assessment',
 'Enter the pathogen test results for a food and grade its food safety risk against GB 29921.',
 '/ Microbiological (Pathogen) Risk Assessment',
 '📖 Read the "Microbiological (Pathogen) Risk Assessment Usage Guide"',
 '📋 Microbiological (Pathogen) Risk Assessment',
 'The microbiological risk score assigns points item by item under GB 29921: Salmonella and E. coli O157 each add 5 points when detected, Staphylococcus aureus or Shigella above the limit each add 3, and an aerobic plate count above the limit adds 2. A total of 5 or more fails, 3 to 4 needs retesting, and 0 to 2 passes.',
 'Meat products',
 'Dairy products',
 'Aquatic products',
 'Ready-to-eat foods',
 'Salmonella (CFU/g)',
 'Staphylococcus aureus (CFU/g)',
 'Escherichia coli O157 (CFU/g)',
 'Listeria monocytogenes (CFU/g)',
 'Vibrio parahaemolyticus (MPN/g)',
 '📚 Deep Dive: Microbiological (Pathogen) Risk Assessment',
 'Pass/fail judgement in release testing',
 'Risk grading for market surveillance sampling',
 'Batch release in factory quality control',
 'Scoring rule',
 'Per GB 29921-2021: Salmonella and O157 must not be detected (+5 each when detected); S. aureus, Listeria and V. parahaemolyticus above 100 CFU(MPN)/g each add 3–4; an aerobic plate count above the category limit (meat and aquatic 5×10⁴, dairy and ready-to-eat 1×10⁴) adds 2. Total rs: 0 is safe, ≤3 low risk, ≤8 medium risk and above 8 high risk.',
 'Ready-to-eat food: Salmonella 0, S. aureus 50, O157 0, Listeria 0, Vibrio 0 and a plate count of 8000 (≤1×10⁴) gives rs = 0, safe and passing. Meat product: Salmonella detected (+5), Listeria 250 (+4), S. aureus 150 (+3) and a plate count of 6×10⁴ (+2) gives rs = 14, high risk, so the batch fails and must not be sold.',
 'Why must pathogens not be detected?',
 'Salmonella and E. coli O157 are pathogens with zero tolerance; GB 29921 sets n = 0 (not detectable in 25 g), so any detection means failure.',
 'How are the plate count limits set?',
 'By food category: meat and aquatic products ≤5×10⁴ CFU/g, dairy and ready-to-eat foods ≤1×10⁴ CFU/g; exceeding the limit indicates poor hygiene.',
 'GB 29921-2021 sets limits for five pathogens in prepackaged foods',
 'Salmonella and E. coli O157 must not be detected (0/25 g)',
 'The S. aureus limit is ≤100 CFU/g and V. parahaemolyticus ≤100 MPN/g',
 'Listeria must be ≤100 CFU/g in ready-to-eat foods, and pregnant women are a high-risk group',
 'The aerobic plate count reflects overall hygiene but is not directly the same as pathogenic risk',
 'About Microbiological (Pathogen) Risk Assessment',
 'A microbiological pathogen risk assessment tool for food: enter Salmonella, S. aureus and other test results and grade the food safety risk against GB 29921.',
 'Limit testing for five pathogens',
 'Based on GB 29921-2021',
 'Aerobic plate count as a hygiene indicator',
 'Automatic risk grading',
 'Release testing of food products',
 'Food safety risk monitoring',
 'Market surveillance sampling',
 'Quality control in food manufacturers',
]

B['coliform-mpn'] = [
 '🏋️ Coliform MPN Retrieval Table',
 'Per the GB 4789.3 MPN counting method, enter the number of positive tubes at three dilutions to look up the MPN value and its 95% confidence interval.',
 'Per the GB 4789.3 MPN counting method, enter the number of positive tubes at three dilutions to look up the MPN value and its 95% confidence interval. It runs a professional calculation on the input parameters and outputs the result.',
 '📖 Read the "Coliform MPN Retrieval Usage Guide"',
 'Positive tubes at the first dilution (0-5)',
 'Positive tubes at the second dilution (0-5)',
 'Positive tubes at the third dilution (0-5)',
 'Inoculum at the first dilution (g/tube)',
 'Solid sample (MPN/g)',
 'Liquid sample (MPN/mL)',
 'Look up MPN',
 'This table applies to the MPN method with 5 tubes per dilution (15 tubes in total): five tubes are inoculated at each dilution, with the inoculum falling tenfold at each step.',
 'Standard inoculum: 0.1 g, 0.01 g, 0.001 g (solid); 1 mL, 0.1 mL, 0.01 mL (liquid).',
 'Result calculation: MPN = table MPN value × (standard inoculum at the first dilution / actual inoculum).',
 '📚 Deep Dive: Coliform MPN Retrieval',
 'Coliform counting in food',
 'Monitoring of hygiene indicator bacteria',
 'Judging water and food sampling results',
 'Retrieval rule',
 'Per GB 4789.3, with three tubes at each of three dilutions (inoculum 0.1/0.01/0.001 g·mL), look up the MPN value for the positive-tube combination and its 95%',
 'Positive tube counts of 3-2-1 across the three dilutions (inoculum 0.1/0.01/0.001): the MPN table gives about 150 MPN/100 mL (95% CI 30–440), indicating poor hygiene.',
 'How do MPN and plate counts differ?',
 'MPN is a most probable number, a probability estimate suited to low counts, while a plate count is a measured CFU; the two differ in dimension and meaning.',
 'How can the confidence interval be narrowed?',
 'Use 5-tube or 10-tube methods and set the dilution steps so positives land in the middle dilution, which gives a narrower interval.',
 'About the Coliform MPN Retrieval Table',
 'A coliform MPN retrieval table. A cooking helper for keeping ingredient ratios and nutrition precise.',
]

for s, lst in B.items():
    write(s, build(s, lst))

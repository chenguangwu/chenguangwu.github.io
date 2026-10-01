#!/usr/bin/env python3
# gen_food-testing_b4.py — food-testing b4 (5 slugs): ingredient-sorter/irradiation-dose/nitrite-colorimetric/nutrition-label-nrv/packaging-migration
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

B['ingredient-sorter'] = [
 '🍳 Ingredient List Descending-Order Sorter',
 'Per GB 7718, the general standard for prepackaged food labelling, it arranges ingredients in descending order of the amount added and can expand compound ingredients.',
 '📖 Read the "Sorting Ingredients in Descending Order of Amount Usage Guide"',
 'Enter the ingredients (one per line, format: name, percent%)',
 'Ingredient list',
 'Wheat flour, 55\nWater, 20\nWhite sugar, 10\nVegetable oil, 8\nYeast, 2\nSalt, 1\nFlavouring, 0.5',
 'Descending by amount (standard, GB 7718)',
 'Ascending by amount',
 'Compound ingredient handling',
 'Mark compound ingredients with brackets (contents of 2% or less need not be sorted)',
 'Expand the components of compound ingredients',
 'Do not process',
 'Ingredients at 2% or less',
 'Place at the end (need not follow descending order)',
 'Keep the original order (still descending)',
 'Generate the ingredient list',
 'Copy the ingredient list',
 '📋 GB 7718 ingredient list labelling rules',
 'Descending order',
 ': ingredients must be listed in descending order of the amount added when the food was manufactured or processed',
 ': ingredients added at no more than 2% need not follow the descending order',
 'Compound ingredients',
 ': their original components must be declared in the list; when the amount added is 25% or less and the standard conditions are met, the declaration may be omitted',
 'Water',
 ': water lost through evaporation need not be declared, while added water must appear in the ingredient list',
 'Food additives',
 ': must be declared under their generic names',
 '📚 Deep Dive: Sorting Ingredients in Descending Order of Amount',
 'Ordering ingredients on prepackaged food labels',
 'Checking the expansion of compound ingredients',
 'Self-checking label compliance',
 'Per GB 7718, ingredients are ordered from high to low by the amount added (',
 'mass fraction',
 '); those at 2% or less may sit at the end in any order, and compound ingredients that meet the conditions may be declared as a whole.',
 'Recipe: flour 500 g, white sugar 200 g, vegetable oil 80 g, salt 10 g gives the order flour, white sugar, vegetable oil, salt; salt at 2% or less may be put at the end.',
 'When must compound ingredients be expanded?',
 'When a compound ingredient is added at more than 25% and the national standard sets out its original components separately, it must be expanded; otherwise it may be declared as a whole.',
 'What if two amounts are the same?',
 'Ingredients of similar mass may be listed side by side, ordered by custom or function; the production record governs.',
 'About the Ingredient List Descending-Order Sorter',
 'The ingredient list descending-order sorter is an online tool for cooking. A cooking helper for keeping ingredient ratios and nutrition precise.',
 'Optional',
 'Wheat flour, 55\nWater, 20\nWhite sugar, 10\nVegetable oil, 8\nYeast, 2\nSalt, 1\nFlavouring, 0.5',
]

B['irradiation-dose'] = [
 '🏦 Irradiation Dose Microbial Inactivation Estimator',
 'It estimates the dose needed for radiation sterilization from the D10 value, supporting inactivation calculations for common foodborne microorganisms.',
 'Core formulas (by input variables): Math.round(dose×10000)÷10000; (1-(10)^-logReduction)×100; Math.log10(n0÷n)',
 '📖 Read the "Irradiation Sterilization Dose (D10) Estimation Usage Guide"',
 'Microorganism type',
 'Salmonella (D10 = 0.5 kGy)',
 'E. coli O157:H7 (D10 = 0.3 kGy)',
 'Listeria monocytogenes (D10 = 0.4 kGy)',
 'Campylobacter (D10 = 0.2 kGy)',
 'Yeast (D10 = 0.5 kGy)',
 'Mold (D10 = 0.5 kGy)',
 'Bacillus spores (D10 = 2.0 kGy)',
 'Virus (D10 = 3.0 kGy)',
 'Clostridium botulinum (D10 = 2.5 kGy)',
 'Bacillus subtilis (D10 = 1.8 kGy)',
 'D10 value (kGy)',
 'Initial count N₀ (CFU/g)',
 'Target surviving count N (CFU/g)',
 'Calculate the dose required',
 'Calculate survivors at a given dose',
 'Irradiation dose D (kGy)',
 'Dose required',
 'Surviving count',
 'Log reduction',
 'D10 is the irradiation dose (kGy) that cuts the microbial population by 90%, that is, by one log cycle',
 '⚠️ China caps the maximum total average absorbed dose of irradiated food at 10 kGy, except for specific products. Different food types have different permitted doses.',
 '📚 Deep Dive: Irradiation Sterilization Dose (D10) Estimation',
 'Designing doses for irradiation sterilization processes',
 'Accounting for the inactivation of foodborne pathogens',
 'Validating irradiation processes',
 'The dose for n log reductions is D = D₁₀ × log₁₀(N₀/N); D₁₀ is the dose that inactivates 90%.',
 'D₁₀ = 0.5 kGy, initial count 1×10⁵, target residual 1: log reduction = log₁₀(1×10⁵) = 5, so the dose = 0.5 × 5 = 2.5 kGy, within the usual pasteurizing irradiation range of 3–10 kGy.',
 'Where do I look up D10?',
 'Look it up in the literature or standards by species (Salmonella D₁₀ ≈ 0.2–0.6 kGy); it varies widely between organisms and food matrices.',
 'Is a bigger dose better?',
 'Too high a dose harms flavour and nutrition and is capped by regulation, so keep the dose to the minimum that meets the target reduction.',
 'About the Irradiation Dose Microbial Inactivation Estimator',
 'An irradiation dose microbial inactivation estimator. A cooking helper for keeping ingredient ratios and nutrition precise.',
]

B['nitrite-colorimetric'] = [
 '🧮 Nitrite Content Colorimetric Calculator',
 'Per the GB 5009.33 naphthylethylenediamine colorimetric method, it computes the nitrite content of a sample from a standard curve.',
 'Core formula (by input variables): Math.round(content×1000)÷1000',
 '📖 Read the "Nitrite Colorimetric Determination Usage Guide"',
 'Standard curve parameters',
 'Standard curve slope k',
 'Standard curve intercept b',
 'Standard curve equation: A = k·C + b, where C is the sodium nitrite concentration in μg/mL and A the absorbance',
 'Sample parameters',
 'Sample absorbance A',
 'Sample mass (g)',
 'Volume made up to (mL)',
 'Aliquot volume taken for measurement (mL)',
 'Final volume after colour development (mL)',
 'Sauced and braised meat products (≤30 mg/kg)',
 'Smoked sausage (≤30 mg/kg)',
 'Cured meat products (≤150 mg/kg)',
 'Vegetables (≤4 mg/kg)',
 'Infant and young children food (≤2 mg/kg)',
 'Limit standard (mg/kg)',
 'Curve concentration',
 'Nitrite content',
 '= (C × colour development volume × volume made up) / (aliquot volume × sample mass), in mg/kg',
 'Results are expressed as sodium nitrite (NaNO₂).',
 '📚 Deep Dive: Nitrite Colorimetric Determination',
 'Nitrite testing of meat products',
 'Quantification by the naphthylethylenediamine colour reaction',
 'Limit compliance judgement',
 'Per GB 5009.33, the standard curve gives c = (A − intercept)/slope, where A is the absorbance; combined with the sampling and test',
 'volume conversion',
 'it gives the nitrite content of the sample.',
 'Sample absorbance 0.210, curve slope 0.0185, intercept 0.002: c = (0.210 − 0.002)/0.0185 ≈ 11.24 mg/L; converting by the aliquot volume gives about 11.2 mg/kg of nitrite in the sample, below the limit of 30, so it passes.',
 'Why test for nitrite?',
 'It fixes colour and inhibits bacteria in meat products, but an excess forms carcinogenic nitrosamines, so the amount added must be tightly controlled and declared.',
 'What is the limit?',
 'Nitrite residue in cooked meat products is capped at 30 mg/kg (as NaNO₂), with stricter limits for products such as Western-style ham, under GB 2760.',
 'About the Nitrite Content Colorimetric Calculator',
 'A nitrite content colorimetric calculator. A cooking helper for keeping ingredient ratios and nutrition precise.',
]

B['nutrition-label-nrv'] = [
 '🥗 Nutrition Label NRV% Automatic Calculator',
 'Per GB 28050, enter the nutrient content per 100 g of a food and it computes NRV% and generates a nutrition label.',
 'Core formulas (by input variables): val×servingSize÷100; (val÷nrv.nrv)×100; min(100, n.nrvPct)',
 '📖 Read the "Nutrition Label NRV% Calculation Usage Guide"',
 'Serving size (g)',
 'Core nutrients (content per 100 g)',
 'Energy (kJ)',
 'Protein (g)',
 'Fat (g)',
 'Saturated fatty acids (g)',
 'Carbohydrate (g)',
 'Sugars (g)',
 'Sodium (mg)',
 'Optional nutrients (content per 100 g)',
 'Dietary fibre (g)',
 'Calcium (mg)',
 'Iron (mg)',
 'Vitamin A (μg RE)',
 'Vitamin C (mg)',
 'Generate the nutrition label',
 '📋 NRV reference values (GB 28050)',
 'Energy',
 'Saturated fatty acids',
 'Dietary fibre',
 'Vitamin A',
 '📚 Deep Dive: Nutrition Label NRV% Calculation',
 'Nutrition labels for prepackaged foods',
 'Nutrient accounting per 100 g',
 'Generating NRV% and checking compliance',
 'NRV% = content per 100 g ÷ NRV reference value × 100% (energy 2000 kJ, protein 60 g, fat 60 g, carbohydrate 300 g, sugars 50 g, sodium 2000 mg and so on).',
 'Per 100 g: energy 800 kJ, protein 5 g, fat 10 g, carbohydrate 60 g, sugars 15 g gives NRV% of 40%, 8%, 17%, 20% and 30% respectively; saturated fat 3 g gives 15%.',
 'Where do the NRV reference values come from?',
 'From the annex of GB 28050: energy 2000 kJ with fixed reference values for each nutrient, and labels must state NRV%.',
 'How are low or free claims used?',
 'Combine the content thresholds (for example, sugars of 5 g or less per 100 g may be called low sugar) with the NRV% statement, and avoid misleading claims.',
 'About the Nutrition Label NRV% Automatic Calculator',
 'A nutrition label NRV% automatic calculator. A cooking helper for keeping ingredient ratios and nutrition precise.',
]

B['packaging-migration'] = [
 '📦 Packaging Material Migration Calculator',
 'It computes the migration of specific substances from food contact materials into food simulants and compares it with the SML, following the GB 31604 series.',
 'Core formulas (by input variables): Math.round(migrationDM×100000)÷100000; Math.round(migrationKg×100000)÷100000; (conc×volume)÷area÷1000',
 '📖 Read the "Specific Substance Migration (SML Comparison) Usage Guide"',
 '10% ethanol (water-soluble foods)',
 '20% ethanol (alcoholic foods)',
 '50% ethanol (foods containing alcohol)',
 '95% ethanol (fat-soluble foods)',
 '3% acetic acid (acidic foods)',
 'Isooctane (a substitute for fat-soluble foods)',
 'Vegetable oil (fat-soluble foods)',
 'Water (neutral water-soluble foods)',
 'Migrating substance',
 'DEHP, di(2-ethylhexyl) phthalate (SML = 1.5 mg/kg)',
 'DBP, dibutyl phthalate (SML = 0.3 mg/kg)',
 'BPA, bisphenol A (SML = 0.6 mg/kg)',
 'BADGE, bisphenol A diglycidyl ether (SML = 9 mg/kg)',
 'Caprolactam (SML = 15 mg/kg)',
 'Formaldehyde (SML = 15 mg/kg)',
 'Styrene (SML = 6 mg/kg)',
 'Total phthalates (SML = 0.3 mg/kg)',
 'Migration (mg/dm²)',
 '= (concentration × simulant volume) / contact area / 1000',
 'Converted into content in food (mg/kg)',
 '= migration × (6 dm²/kg), the standard conversion ratio',
 'Standard conversion ratio: 6 dm² of contact area corresponds to 1 kg of food. Correct the result when the area to volume ratio differs.',
 '📚 Deep Dive: Specific Substance Migration (SML Comparison)',
 'Assessing the migration of plastic additives',
 'Comparing migration with the SML limit',
 'Compliance of food contact materials',
 'Migration (mg/dm²) = substance concentration in the simulant × volume / contact area ÷ 1000; convert to mg/kg of food by multiplying by 6, taking 6 dm²/kg.',
 'Simulant concentration 0.5 mg/L, volume 200 mL, area 3 dm², SML 1.5 mg/kg: migration 0.5 × 200/3/1000 ≈ 0.033 mg/dm² or 0.20 mg/kg, far below the SML of 1.5, so it passes.',
 'What is the basis for the ×6 conversion?',
 'GB 31604 defaults to an empirical ratio of 6 dm² of contact area per 1 kg of food; correct it using the real area and food amount.',
 'How do SML and QM differ?',
 'SML is the specific migration limit while QM is the maximum amount of the substance in the material; they control migration and total content respectively.',
 'About the Packaging Material Migration Calculator',
 'The packaging material migration calculator is an online tool for cooking. A cooking helper for keeping ingredient ratios and nutrition precise.',
]

for s, lst in B.items():
    write(s, build(s, lst))

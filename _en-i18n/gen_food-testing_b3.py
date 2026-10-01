#!/usr/bin/env python3
# gen_food-testing_b3.py — food-testing b3 (5 slugs): fat-soxhlet/foreign-matter-density/generator-27/generator-31/heavy-metal-migration
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

B['fat-soxhlet'] = [
 '🔎 Soxhlet Extraction Fat Yield Calculator',
 'Per the GB 5009.6 Soxhlet extraction method, it computes the fat content of a food and the extraction yield.',
 'Core formulas (by input variables): Math.round(extractionRate×100)÷100; Math.round(dryBasis×10000)÷10000; Math.round(fatMass×10000)÷10000',
 '📖 Read the "Soxhlet Extraction Fat Content Usage Guide"',
 'Empty extraction flask mass m₁ (g)',
 'Flask plus fat mass after extraction m₂ (g)',
 'Theoretical fat content (%)',
 'Calculate fat content',
 'Fat content (wet basis)',
 'Fat content (dry basis)',
 '= wet basis content / (1 - moisture %) × 100%',
 'Extraction yield',
 '= measured fat content / theoretical fat content × 100%',
 'm₁ is the empty extraction flask mass, m₂ the flask plus fat mass after extraction and m the sample mass',
 '📚 Deep Dive: Soxhlet Extraction Fat Content',
 'Determining fat (crude fat) in food',
 'Fat accounting for nutrition labels',
 'Assessing the fat content of oilseeds and meat products',
 'Fat mass = m₂ − m₁ (the gain in flask mass); wet basis % = fat mass / sample mass × 100%; dry basis % = wet basis / (1 − moisture) × 100%.',
 'Sample 2.000 g, flask 60.000 g before extraction and 61.250 g after: fat 1.250 g, wet basis = 1.250/2.000 × 100% = 62.5%; with 5.0% moisture the dry basis = 62.5%/(1 − 0.05) = 65.8%.',
 'Does Soxhlet measure true fat?',
 'It measures crude fat, the ether-soluble fraction, which includes free lipids and pigments; keep it distinct from the acid hydrolysis method.',
 'Why is the dry basis higher?',
 'Removing moisture raises the fat share, and the dry basis lets samples with different moisture levels be compared side by side.',
 'About the Soxhlet Extraction Fat Yield Calculator',
 'A Soxhlet extraction fat yield calculator. A cooking helper for keeping ingredient ratios and nutrition precise.',
 'Optional, used to compute the extraction yield',
]

B['foreign-matter-density'] = [
 "🏎️ Food Foreign Body Density and Settling Velocity Calculator",
 "Based on Stokes' law, it computes the settling velocity of foreign particles in a liquid food and helps select foreign body detection equipment.",
 'Core formulas (by input variables): |(velocity)|; d÷1000; absV×100×60',
 '📖 Read the "Foreign Body Settling Velocity (Stokes) Usage Guide"',
 'Foreign body type',
 'Stainless steel (7800 kg/m³)',
 'Iron (7870 kg/m³)',
 'Copper (8960 kg/m³)',
 'Aluminium (2700 kg/m³)',
 'Glass (2500 kg/m³)',
 'Bone (1800 kg/m³)',
 'Plastic (1100 kg/m³)',
 'Rubber (1200 kg/m³)',
 'Wood (600 kg/m³)',
 'Ceramic (2300 kg/m³)',
 'Foreign body density ρp (kg/m³)',
 'Particle diameter d (mm)',
 'Food medium type',
 'Water (ρ=1000, η=0.001)',
 'Milk (ρ=1030, η=0.003)',
 'Edible oil (ρ=920, η=0.08)',
 'Honey (ρ=1420, η=10)',
 'Fruit juice (ρ=1050, η=0.005)',
 'Sauce (ρ=1100, η=0.5)',
 'Fluid density ρf (kg/m³)',
 'Fluid viscosity η (Pa·s)',
 'Calculate settling velocity',
 "📋 Stokes' Law",
 'v = settling velocity (m/s), d = particle diameter (m), g = 9.81 m/s²',
 'ρp = particle density, ρf = fluid density, η = dynamic viscosity (Pa·s)',
 'When ρp < ρf the particle floats; when ρp > ρf it settles.',
 '💡 Metal detectors are highly sensitive to ferromagnetic materials; X-ray inspection works well for foreign bodies with a large density difference (metal, glass, stone) and poorly for low-density ones such as wood and plastic.',
 "📚 Deep Dive: Foreign Body Settling Velocity (Stokes)",
 'Selecting metal and foreign body detection equipment',
 'Assessing settling in liquid foods',
 'Designing filtration and centrifugation',
 'Settling velocity v = d²·g·(ρ_p − ρ_f)/(18·η), where d is the particle size, ρ_p and ρ_f the particle and liquid densities and η the viscosity; valid for Re < 0.2.',
 'A 2 mm steel fragment (ρ = 7800) in clean water (ρ = 1000, η = 0.001): v = (0.002² × 9.81 × 6800)/(18 × 0.001) ≈ 14.8 mm/s; Re ≈ 30 > 0.2, beyond the Stokes range, so a correction is needed.',
 'What if Re is outside the range?',
 'Switch to the Newtonian drag formula or CFD: Stokes suits only small, slow particles and overestimates settling for large ones.',
 'Why does it matter for detection?',
 'The faster a particle settles the easier it sinks and can be removed; suspended particles need filtration, centrifugation or magnetic separation.',
 'About the Food Foreign Body Density and Settling Velocity Calculator',
 'A food foreign body density and settling velocity calculator. A cooking helper for keeping ingredient ratios and nutrition precise.',
]

B['generator-27'] = [
 '✨ Aerobic Plate Count (Plate Count) Report Generation',
 'Plate count',
 '📖 Read the "Aerobic Plate Count Report Generation Usage Guide"',
 'The aerobic plate count follows the GB 4789.2 plate count method: take plates with colony counts between 30 and 300, and aerobic plate count = plate colony count × dilution factor ÷ sample volume; when plates at two adjacent dilutions both fall in the counting range they are combined with the weighted formula, and the result is reported in CFU/g or CFU/mL to two significant figures.',
 '📚 Deep Dive: Aerobic Plate Count Report Generation',
 'Reporting microbiological test records',
 'Formatting reports for batches of samples',
 'Generating laboratory ledgers',
 'Report result = mean plate colony count × dilution factor, taking the valid dilution per GB 4789.2.',
 'A mean of 156 at a dilution of 10⁻¹ gives a reported result of 156 × 10 = 1560 CFU/g; generating five sample reports applies each sample mean and dilution in turn.',
 'How is the dilution chosen?',
 'Take the dilution whose plate shows 30–300 colonies; with several dilutions use weighting or the main dilution, and keep the method consistent throughout.',
 'What does the report contain?',
 'Sample name, dilution, colony count, result unit and the judgement, for traceability and regulatory reporting.',
 'About Aerobic Plate Count (Plate Count) Report Generation',
 'An aerobic plate count (plate count) report generator. A free online tool that runs entirely in the browser: data is never uploaded, so your privacy stays safe.',
 'Generating plate count reports for release testing and sampling',
 'Compliance judgement against microbial limits for raw and cooked foods',
 'Recording cold chain and hygiene monitoring trends',
 'Teaching demos of colony counting and reporting',
]

B['generator-31'] = [
 '🔤 Food (Traceability) Code Generation',
 'Traceability',
 '/ Food (Traceability) Code Generation',
 '📖 Read the "Food Traceability Code Generation Usage Guide"',
 '🔤 Food (Traceability) Code Generation',
 'Food traceability codes are assembled from elements: a company prefix of 7 to 10 digits plus an item reference and a check digit, or a batch code built from the production date, batch number and serial number. The check digit follows the GS1 mod-10 weighted algorithm digit by digit, and the code is globally unique and maps one-to-one to the production batch and raw material source for backward tracing.',
 '📚 Deep Dive: Food Traceability Code Generation',
 'Batch generation of label traceability codes',
 'Batch coding for production ledgers',
 'Recall and traceability code management',
 'Code structure',
 'Traceability code = GTIN (690 + 8 digits) − batch (B + 6 digits) − date (YYYYMMDD) − serial (L + 4 digits), generated locally at random and never uploaded to a server.',
 'One example: 69012345678-B120908-20260908-L0007; when n codes are generated in a batch the serial increments each time, so a code can be traced back to the GTIN, batch and production date, supporting both forward tracking and backward tracing.',
 'Can the code be used as an official GS1 barcode?',
 'This tool produces local demo codes and the GTIN prefix 690 is only an example; official product barcodes need a prefix registered with GS1 so they do not clash with codes already on the market.',
 'Is any data uploaded?',
 'No. The codes are assembled at random in the browser for label and ledger support only, and nothing is uploaded to any server.',
 'About Food (Traceability) Code Generation',
 'A food (traceability) code generator. A free online tool that runs entirely in the browser: data is never uploaded, so your privacy stays safe.',
 'Generating GS1-128 / SSCC logistics unit barcode codes',
 'Coding that combines the batch number with the production date and line',
 'Arranging cold chain traceability labels (GTIN + batch + shelf life)',
 'Printing and checking traceability codes at goods-in, goods-out and sorting',
]

B['heavy-metal-migration'] = [
 '🔮 Heavy Metal Migration Estimator',
 'It computes the migration of heavy metals (lead, cadmium, chromium and so on) from food contact materials and compares it with the specific migration limit (SML), following the GB 31604 series.',
 'Core formulas (by input variables): (conc×volume)÷foodVol×1000; area÷foodVol×1000',
 '📖 Read the "Heavy Metal Migration from Food Contact Materials Usage Guide"',
 'Heavy metal',
 'Lead (Pb), SML = 0.01 mg/kg',
 'Cadmium (Cd), SML = 0.002 mg/kg',
 'Chromium (Cr), SML = 0.1 mg/kg',
 'Arsenic (As), SML = 0.01 mg/kg',
 'Mercury (Hg), SML = 0.005 mg/kg',
 'Antimony (Sb), SML = 0.04 mg/kg',
 'Barium (Ba), SML = 1.0 mg/kg',
 'Food simulant volume (equivalent to 1 kg of food)',
 'Migration (mg/dm²)',
 '= (concentration × simulant volume) / contact area',
 'Converted into content in food (mg/kg)',
 '= (concentration × simulant volume) / food simulant volume × 1000',
 'When the contact area to food volume ratio differs from 6 dm²/kg, convert using the actual ratio.',
 '⚠️ This tool is for estimation only; actual testing must follow the matching GB 31604 method. 6 dm²/kg is the standard conversion ratio.',
 '📚 Deep Dive: Heavy Metal Migration from Food Contact Materials',
 'Assessing lead and cadmium migration from plastic and metal packaging',
 'Comparing migration with the SML limit',
 'Compliance judgement and material selection',
 'Estimated from the material concentration conc (mg/kg): migration (mg/dm²) = conc × simulant volume / contact area; migration (mg/kg) = conc × simulant volume / food amount × 1000.',
 'Material with 0.05 mg/kg of lead, 100 mL of simulant, 2 dm² of area, 1000 mL of food and an SML of 0.01 mg/kg: migration 0.05 × 100/2 = 2.5 mg/dm² and 0.05 × 100/1000 × 1000 = 5.0 mg/kg, far above the SML of 0.01, so it fails.',
 'What is SML?',
 'The specific migration limit: the GB 31604 series sets the maximum amount of each substance allowed to migrate into food.',
 'Why measure both by area and by food amount?',
 'mg/dm² is the intensity on the material side and mg/kg the exposure on the food side; they have different bases and both criteria must be met.',
 'About the Heavy Metal Migration Estimator',
 'A heavy metal migration estimator. A cooking helper for keeping ingredient ratios and nutrition precise.',
]

for s, lst in B.items():
    write(s, build(s, lst))

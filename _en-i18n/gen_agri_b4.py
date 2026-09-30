# -*- coding: utf-8 -*-
import os, sys, json, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'agriculture')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'agriculture')
os.makedirs(OUT, exist_ok=True)

CJK = re.compile(r'[\u4e00-\u9fff]')
CN_PUNCT = re.compile(r'[，。、；：！？（）「」『』]')

def validate(slug, mp):
    for k, v in mp.items():
        if CJK.search(v):
            print('!! %s CJK in value for key %r -> %r' % (slug, k, v)); sys.exit(1)
        if CN_PUNCT.search(v):
            print('!! %s CN punctuation in value for key %r -> %r' % (slug, k, v)); sys.exit(1)

def build(slug, en_list):
    path = os.path.join(WORK, slug + '.json')
    with open(path, encoding='utf-8') as f:
        wj = json.load(f)
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('!! %s length mismatch: en=%d items=%d' % (slug, len(en_list), len(items))); sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src'):
            z = it['zh_src'].strip()
        else:
            z = it['zh'].strip()
        if not en or not isinstance(en, str):
            print('!! %s empty translation for key %r' % (slug, z)); sys.exit(1)
        mp[z] = en
    return mp

def write(slug, name, mp):
    validate(slug, mp)
    obj = {'slug': slug, 'industry': 'agriculture', 'name': name, 'map': mp}
    out = os.path.join(OUT, slug + '.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

# ---- dli-calculator (28) ----
dli = [
 '🧮 Daily Light Integral (DLI) Calculator',
 'Calculate the Daily Light Integral (DLI) to assess greenhouse supplemental-lighting demand and photosynthetically active radiation',
 'Daily Light Integral (DLI) Calculator',
 '/ Daily Light Integral (DLI) Calculator',
 '📖 View the "Daily Light Integral (DLI) Calculator User Guide"',
 'DLI = PPFD (umol/m2/s) x light hours (h) x 3600 / 1 000 000 (mol/m2/d); total DLI = natural DLI + supplemental DLI',
 'The Daily Light Integral (DLI) integrates light intensity over time: PPFD times lit seconds divided by 1 000 000 gives mol/m2/d. Natural and supplemental light are computed separately and summed into the total DLI, then compared with the crop target range: >= upper limit means abundant light, >= lower limit means adequate, >= 70% of lower limit means weak, otherwise severely deficient. The shortfall can be back-calculated into the needed supplemental duration or intensity.',
 'PPFD - Photosynthetic Photon Flux Density (umol/m2/s)',
 'Effective light duration (hours/day)',
 'Supplemental-light PPFD (umol/m2/s)',
 'Supplemental-light duration (hours/day)',
 'Shade crops (5-10)',
 'Moderate crops (10-20)',
 'Light crops (20-30)',
 'High-light crops (30+)',
 '📚 Deep Dive: Daily Light Integral (DLI) Calculator',
 'DLI = PPFD x light hours (h) x 3600 / 1e6 (mol/m2/d).',
 'Evaluate whether facility supplemental lighting meets the target (fruit and vegetable seedlings 12~20 mol/m2/d).',
 'Used for supplemental-lighting strategies in low-light seasons.',
 'Winter supplemental lighting for leafy greens',
 'Natural PPFD average 200, daylight 8 h, DLI = 200x8x3600/1e6 = 5.76 mol. Lettuce needs 12~17, shortfall about 8 mol; 150 umol supplemental light for 15 h adds 8.1 mol, reaching the target.',
 'Is supplemental lighting always needed when DLI is insufficient?',
 'It depends on crop and season. Weak-light leafy greens are little affected; fruiting vegetables that stretch or differentiate flower buds poorly must be supplemented. Calculate natural DLI first, then decide, to avoid needless power use.',
 'Is 24-hour supplemental lighting better?',
 'Most plants need a dark period to complete their physiological rhythm; continuous light may not raise yield and instead wastes energy. Designing the light-dark ratio by crop photoperiod (long-day/short-day) is more scientific.',
 'About the "Daily Light Integral (DLI) Calculator"',
 '️ Daily Light Integral (DLI) Calculator. An agricultural tool that helps calculate planting parameters and yield.',
 'How to use the Daily Light Integral (DLI) Calculator',
]

# ---- dry-matter-conversion (34) ----
dmc = [
 '🔄 Agricultural Dry-Matter Content Converter',
 'Quick conversion among fresh weight, dry weight, moisture content, and dry-matter content, with standard moisture normalization',
 '📖 View the "Agricultural Dry-Matter Content Converter Guide"',
 'Fresh weight to dry matter',
 'Dry weight to fresh weight',
 'Standard moisture normalization',
 'Dry matter = fresh weight x (1 - moisture% / 100); fresh weight = dry weight / (1 - moisture% / 100); standard weight = actual weight x (100 - actual moisture%) / (100 - target moisture%)',
 'Three conversions: 1) from fresh weight and moisture find dry-matter and water weight (dry-matter rate = dry weight / fresh weight x 100%); 2) from dry weight and moisture back-calculate fresh weight; 3) standard-moisture normalization - actual weight is converted by "(100 - actual moisture%) / (100 - target moisture%)" into a pricing standard weight, used for grain purchase, forage metering, and processing-material accounting.',
 'Fresh weight (kg)',
 'Dry weight (kg)',
 'Target moisture (%)',
 'Actual weight (kg)',
 'Actual moisture (%)',
 'Standard moisture (%)',
 'Reference moisture of common produce',
 'Fresh corn grain: 25-35%',
 'Fresh forage: 70-85%',
 'Silage corn: 65-75%',
 'Grain standard moisture: wheat 13% | corn 14% | rice 14%',
 'Fresh vegetables: 90-95%',
 'Fruit: 80-90%',
 '📚 Deep Dive: Agricultural Dry-Matter Converter',
 'Dry-matter weight = fresh weight x (1 - moisture%).',
 'Conversion between moisture levels uses dry-matter conservation.',
 'Used for silage and forage trade pricing.',
 'Silage corn conversion',
 'Fresh weight 20 t, moisture 65%, dry matter = 20 x (1 - 0.65) = 7 t. If another batch has moisture 70%, the same dry matter needs fresh weight 7 / (1 - 0.70) = 23.3 t, showing high-moisture material "looks more but has less dry matter".',
 'Why does silage care about dry matter?',
 'Silage fermentation needs raw material dry matter 30%~40%; too low easily sours, too high ferments slowly. Formulating by dry matter rather than fresh weight keeps quality stable.',
 'How to calibrate an inaccurate moisture reading?',
 'The oven-drying method (65C or 105C to constant weight) is the standard; NIR/microwave quick tests need calibration. High-moisture samples spatter when dried and should be pre-dried or mixed with sand.',
 'About the "Agricultural Dry-Matter Content Converter"',
 '️ Agricultural Dry-Matter Content Converter. An agricultural tool that helps calculate planting parameters and yield.',
 'How to use the Agricultural Dry-Matter Content Converter',
]

# ---- estimate-3 (38) ----
est3 = [
 '🔮 Irrigation Water Estimator (Evapotranspiration)',
 'Based on the crop coefficient (Kc) and reference evapotranspiration (ET0), estimate crop water demand and irrigation volume over a period.',
 '📖 View the "Irrigation Water Estimator (Evapotranspiration) Guide"',
 'ETc = Kc x ET0; total water depth = ETc x days; net irrigation depth = max(0, total depth - effective rainfall); volume (m3) = depth (mm) x area (m2) / 1000',
 'Multiply the crop coefficient Kc by reference evapotranspiration ET0 to get daily demand ETc, then by days to get the period total water depth (mm). Subtract effective rainfall for net irrigation depth. Multiply depth by area (m2) and divide by 1000 for cubic-meter volume. Convert by mu (1 mu = 666.67 m2) for irrigation quotas and pump scheduling.',
 'Crop type (quick Kc pick)',
 'Wheat (growth-period average)',
 'Corn (growth-period average)',
 'Rice (flooded period)',
 'Forage / lawn',
 'Tomato (peak fruit)',
 'Citrus',
 'Reference evapotranspiration ET0 (mm/day)',
 'Estimation days',
 'Effective rainfall (mm, optional)',
 '🧮 Calculate irrigation demand',
 '💡 Formula: crop water demand ETc = ET0 x Kc; total volume = ETc x days x area / 1000 (m3). After deducting effective rainfall it is the net irrigation demand.',
 'ET0 can be obtained from local weather stations, the FAO Penman-Monteith formula, or an evapotranspiration estimator.',
 'Kc varies with the crop growth stage; the table shows averages, and peak bloom/peak fruit are usually higher.',
 'Irrigation efficiency does not deduct conveyance loss and field nonuniformity; actual intake should combine the irrigation water-use coefficient.',
 '📚 Deep Dive: Irrigation Water Estimator (Evapotranspiration)',
 'Net irrigation = (ETc - Pe) x area / 0.667 (m3, Pe is effective rainfall mm).',
 'Build rolling irrigation plans by ten-day or monthly ETc.',
 'Used for water allocation under limited supply in arid areas.',
 'Ten-day irrigation plan',
 'One ten-day period ETc 40 mm, effective rainfall 10 mm, net demand 30 mm = 20 m3/mu. 100 mu needs 2000 m3 that period; at 80 m3/h pump it takes 25 h, split into morning and evening to avoid high-temperature evaporation.',
 'Why is effective rainfall not equal to actual rainfall?',
 'Part of rainfall runs off or percolates deep and is not used by crops. Effective rainfall Pe is usually a fraction of actual rainfall or a threshold method (e.g., daily rain above a value is excess and invalid).',
 'When is irrigation most water-saving?',
 'Early morning or evening has low soil temperature, low evaporation, and little wind, and avoids midday leaf scorch. Drip can run all day but is still most efficient in low-evaporation periods.',
 'About the "Irrigation Water Estimator (Evapotranspiration)"',
 'From reference evapotranspiration (ET0), crop coefficient (Kc), planting area, estimation days, and effective rainfall, compute crop water demand and net irrigation volume to help plan irrigation.',
 'Built-in quick Kc selection for common crops',
 'Supports custom crop coefficient and ET0',
 'Auto-deducts effective rainfall and outputs net irrigation volume',
 'Drip and sprinkler system water budgeting',
 'Rotation-cycle and pump-flow planning',
 'Supplemental-irrigation decisions for dryland farming',
]

# ---- estimate-area-density (40) ----
ead = [
 '📐 Livestock Stocking Estimator (Area x Density)',
 'Enter farming area, stocking density, and average weight to quickly estimate total stock count, total biomass, and yield per area.',
 '📖 View the "Livestock Stocking Estimator (Area x Density) Guide"',
 'Stock count = area x density x unit factor x survival%; total biomass = stock count x average weight; converted density = stock count / area',
 'First normalize area to square meters by the chosen unit (mu / 666.67, ha / 10 000, m2 as-is), multiply by stocking density for theoretical stock, then by survival rate for actual stock count. Total biomass is stock count x average weight; convert stock count to "head/m2" and "head/mu" densities for comparison, aiding farm capacity and feed planning.',
 'Farming area (m2)',
 'Density unit',
 'head / m2',
 'head / mu',
 'head / hectare',
 'Stocking density',
 'Average weight (kg/head, optional)',
 'Survival / market rate (%)',
 '🧮 Calculate stocking',
 '💡 Formula: total stock = area x density (by unit conversion) x survival rate; total biomass = total stock x average weight.',
 'When density unit is "head/mu", area is still entered in square meters and the tool auto-converts (1 mu = 666.67 m2).',
 'Survival rate estimates the actually marketable or surviving count.',
 'Average weight is optional; if left blank only the stock count is output.',
 '📚 Deep Dive: Livestock Stocking Estimator (Area x Density)',
 'Stock = barn area x design density (head/m2).',
 'Adjust density by animal stage (piglet / finishing).',
 'Used for barn acceptance and manure-support accounting.',
 'Finishing-pig barn design',
 'Barn 500 m2, finishing density 0.8 head/m2, stock = 500 x 0.8 = 400 head. At higher density 1.0 head/m2 it could hold 500 head, but ventilation and manure surplus must be checked.',
 'Does higher density raise profit?',
 'Short-term more stock, but overcrowding raises disease and lowers daily gain and feed',
 'conversion rate',
 ', so overall benefit may fall. Compute "profit per area" not "head count".',
 'How to match manure treatment?',
 'Stock determines manure output (head-day), which sets digester / manure-pit volume and land area for spreading; doubling density doubles treatment scale.',
 'About the "Livestock Stocking Estimator (Area x Density)"',
 'From farming area, density unit, average weight, and survival rate, estimate total stock count and biomass and convert to common head/m2, head/mu densities, for poultry, livestock, aquaculture, and specialty farming planning.',
 'Supports head/m2, head/mu, head/hectare density units',
 'Optional average weight auto-estimates total biomass',
 'Considers survival rate and outputs actual stockable count',
 'Large-scale farm stocking planning',
 'Fish pond and shrimp pond stocking-density estimation',
 'Pasture carrying capacity and grassland load assessment',
 'How to use the Livestock Stocking Estimator (Area x Density)',
 'Short-term more stock, but overcrowding raises disease and lowers daily gain and feed conversion, so overall benefit may fall. Compute "profit per area" not "head count".',
]

# ---- estimate-area-yield (34) ----
eay = [
 '📐 Forage Yield Estimator (Yield per Mu x Area)',
 'Enter fresh-grass yield per mu, planting area, and dry-matter rate to auto-estimate total fresh and dry grass and the number of bales.',
 '📖 View the "Forage Yield Estimator (Yield per Mu x Area) Guide"',
 'Total fresh grass = yield/mu x area x unit factor; dry grass = total fresh x dry-matter%; bales = dry grass / bale weight',
 'The unit factor converts yield/mu into total (kg/mu direct, t/ha x 0.0001, kg/m2 direct by area). Total fresh times dry-matter rate gives air-dried grass; divided by bale weight gives bale count, with converted mu and hectare figures, for forage yield estimation and baling plans.',
 'Yield unit',
 'kg / mu',
 'ton / hectare',
 'Fresh-grass yield per mu',
 'Dry-matter rate (%)',
 'Dry-bale weight (kg/bale, optional)',
 '🧮 Calculate yield',
 '💡 Formula: total fresh grass = yield/mu x area (by unit conversion); dry grass = fresh yield x dry-matter rate; bale count = dry grass / bale weight.',
 'When yield unit is "ton/hectare" or "kg/m2", area is still entered in square meters and the tool auto-converts.',
 'Dry-matter rate varies widely by forage type, cutting time, and drying; the default 30% is for reference only.',
 'Bale count assumes 25 kg small square bales; adjust bale weight for large round bales or silage packs.',
 '📚 Deep Dive: Forage Yield Estimator (Yield per Mu x Area)',
 'Total output = measured yield/mu x area x cutting-count factor.',
 'Measure fresh or dry grass separately.',
 'Used for grass-livestock balance and silage planning.',
 'Alfalfa annual yield',
 'Measured fresh yield 1500 kg/mu, area 30 mu, 4 cuts/year: total fresh = 1500 x 30 x 4 = 180,000 kg = 180 t. As dry grass (water 20% vs fresh 70%) about 60 t.',
 'Why do fresh and dry yields differ so much?',
 'Fresh grass is 60%~80% water, dry 15%~20%; "dry matter" is the comparable base. Trade and feed formulas should use dry matter to avoid water misleading.',
 'How to set cutting count?',
 'Depends on accumulated temperature and rainfall, generally 3~5 cuts. Over-cutting harms roots and lowers next-year yield; cut before first bloom to balance yield and quality.',
 'About the "Forage Yield Estimator (Yield per Mu x Area)"',
 'From forage fresh yield per mu, planting area, dry-matter rate, and bale weight, estimate total fresh grass, dry grass, and bale count, for alfalfa, ryegrass, silage corn, and similar forage planning.',
 'Supports kg/mu, ton/hectare, kg/m2 yield units',
 'Auto-converts dry grass by dry-matter rate',
 'Estimates bale count for storage and transport planning',
 'Pasture hay yield estimation',
 'Forage planting scale and storage planning',
 'Forage product cost accounting',
]

# ---- estimate-content-soil (37) ----
ecs = [
 '🌾 Soil Organic Matter (Loss-on-Ignition) Estimator',
 'Enter dry-soil weights before and after ignition to estimate soil organic matter and organic carbon (LOI method)',
 '📖 View the "Soil Organic Matter (Loss-on-Ignition) Estimator Guide"',
 'LOI = (pre-weight - post-weight) / pre-dry-soil net x 100%; pre-dry-soil net = pre-weight - crucible tare; organic carbon = LOI x 0.58',
 'Same source as LOI: first subtract crucible tare for pre-dry-soil net, then "(pre-weight - post-weight) / dry-soil net x 100%" gives LOI, an approximation of organic matter; organic carbon is organic matter x 0.58. Grade by organic matter (very low <1%, low <2%, medium <3%, fairly high <5%, high >=5%) to assess arable fertility.',
 'Pre-weight (crucible + dry soil) g',
 'Post-weight (crucible + ash) g',
 'Crucible tare g (optional, default 0)',
 'Ignition temperature C (optional, reference)',
 '💡 Formula: loss on ignition = pre-weight - post-weight; organic matter (%) = LOI / pre-dry-soil net x 100; organic carbon (%) = organic matter % x 0.58 (Van Bemmelen factor)',
 'LOI ignites at 375-550C; loss includes organic matter and bound water, so the result is slightly higher than true organic matter',
 'If the weighing is net (without crucible), just enter 0 for "crucible tare"',
 'The Van Bemmelen factor 0.58 assumes organic matter is 58% carbon and fits general mineral soils',
 '📚 Deep Dive: Soil Organic Matter (Loss-on-Ignition) Estimator',
 'Organic matter = loss on ignition / dry soil weight (empirical, not directly equal).',
 'The potassium dichromate oxidation method is a more accurate chemical measurement.',
 'Used for arable-quality monitoring and fertility-building effect evaluation.',
 'Vegetable-field organic matter test',
 'Air-dried soil 5.000 g leaves 4.320 g after ignition, loss 0.680 g. Rough organic matter = organic part of loss; by experience organic matter = 0.68/5 x factor = 13.6% (high; needs potassium dichromate correction since ignition includes bound-water error).',
 'Is the LOI method accurate?',
 'Only an estimate, because ignition also loses bound water and carbonates, overstating organic matter. Research and soil testing use potassium dichromate oxidation with external heating; LOI suits quick rough judgment.',
 'How much organic matter is good soil?',
 'Arable organic matter under 2% is lean, 2%~4% good, above 4% very fertile (by soil type). Raising it relies on straw return, manure, and green manure - a slow variable.',
 'About the "Soil Organic Matter (Loss-on-Ignition) Estimator"',
 'This tool estimates soil organic matter and organic carbon via the loss on ignition (LOI) from dry-soil weight change before and after burning; a common soil-fertility assessment method.',
 'Supports crucible-tare deduction and auto dry-soil net weight',
 'Uses Van Bemmelen factor to convert organic carbon',
 'Auto-grades organic-matter fertility (very low to high)',
 'Pure front-end processing, no upload; usable in field or lab',
 'Soil-fertility evaluation and formula fertilization',
 'Farmland, orchard, and facility soil organic-matter monitoring',
 'Organic-transition soil-quality tracking',
 'Soil physical-chemical analysis in research and teaching',
 'Pre-weight',
 'Post-weight',
 'Crucible tare',
 'Ignition temperature',
]

# ---- estimate-fuel-engine-oil (38) ----
efo = [
 '🔮 Farm-Machinery Fuel Estimator (Fuel per Mu)',
 'Enter working area and total fuel to compute fuel per mu and fuel cost; add working hours and fuel price for further estimates',
 '📖 View the "Farm-Machinery Fuel Estimator (Fuel per Mu) Guide"',
 'Fuel/mu = total fuel / area; hourly fuel = total fuel / hours; work efficiency = area / hours; fuel cost = total fuel x price',
 'Directly convert total fuel and area into fuel per mu (L/mu), the core machinery-economy metric. With working hours you also get hourly fuel and efficiency; with fuel price you get total fuel cost and per-mu cost, aiding machinery pricing and cost comparison.',
 'Working area (mu)',
 'Total fuel (L)',
 'Working hours (optional)',
 'Fuel price (yuan/L, optional)',
 '💡 Formula: fuel/mu = total fuel / area; hourly fuel = total fuel / hours; total cost = total fuel x price; per-mu cost = fuel/mu x price',
 'Fuel per mu is the core indicator of machinery fuel economy, easing cross-field comparison',
 'Fuel price and hours are optional; left blank (0) only fuel/mu is computed',
 'Actual fuel is affected by soil texture, slope, machine condition, and load; results are for reference',
 '📚 Deep Dive: Farm-Machinery Fuel Estimator (Fuel per Mu)',
 'Fuel use = working area x fuel-per-mu coefficient (L/mu).',
 'Take coefficients by operation type (till / sow / harvest).',
 'Used for operation cost and fuel-subsidy accounting.',
 'Combine harvester for wheat',
 'Wheat machine harvest fuel about 1.2 L/mu; 500 mu gives 500 x 1.2 = 600 L. At 7.5 yuan/L, fuel cost 4500 yuan, 12.5% of the harvest fee (about 60 yuan/mu).',
 'Why does fuel per mu vary so much by operation?',
 'Till depth, resistance, and speed set the load. Subsoiling/rotary tillage use the most, transport the least. For the same model, higher load raises per-unit fuel but also efficiency; look at "mu" not "hours".',
 'How to lower fuel per mu?',
 'Keep tools sharp, tire pressure normal, gear-RPM matched (avoid high throttle at low speed), and plan to cut empty runs. Regular maintenance saves more fuel than a bigger engine.',
 'About the "Farm-Machinery Fuel Estimator (Fuel per Mu)"',
 'This tool computes fuel per mu from working area and total fuel, and with hours and price gives hourly fuel, efficiency, and fuel cost, helping farmers and operators assess machinery fuel economy.',
 'One-click fuel/mu, hourly fuel, and efficiency',
 'Supports fuel price for total and per-mu cost',
 'Optional hours and price fit different scenarios',
 'Pure front-end, no upload; ready in the field',
 'Tractor, harvester, transplanter cost accounting',
 'Cross-region cooperative quoting reference',
 'Cross comparison of machines and fields',
 'Machinery energy-saving and emission assessment',
 'How to use the Farm-Machinery Fuel Estimator (Fuel per Mu)',
 'Working area',
 'Total fuel',
 'Working hours',
 'Fuel price',
]

# ---- estimate-soil (37) ----
eso = [
 '📋 Continuous-Cropping Obstacle Index (Soil Pathogen Buildup) Estimator',
 'From continuous-cropping years and annual pathogen growth rate, estimate soil pathogen buildup and the obstacle-risk level',
 '📖 View the "Continuous-Cropping Obstacle Index (Soil Pathogen Buildup) Estimator Guide"',
 'Current pathogen density = initial density x (1 + annual rate%)^years; obstacle index = current density / threshold density x 100',
 'Pathogens accumulate compound-style with cropping years: initial density times (1 + annual rate) to the year power. The obstacle index is benchmarked to threshold density (current / threshold x 100) with accumulation multiple (current / initial). Index <30 safe, 30~60 warning, >60 severe, suggesting routine monitoring, rotation/soil disinfection, or rotation with bio-fumigation or resistant varieties.',
 'Continuous-cropping years',
 'Initial pathogen density (CFU/g)',
 'Annual growth rate (%)',
 'Threshold density (CFU/g)',
 '💡 Formula: current density = initial density x (1 + annual rate)^years; obstacle index = current density / threshold density x 100; <30 safe, 30-60 warning, >60 severe',
 'This tool uses an exponential-growth model, suited to approximate year-by-year pathogen buildup under continuous cropping',
 'Threshold density is the critical value causing significant yield loss; it varies by crop and pathogen, so consult local plant-protection data',
 'Actual obstacles are also shaped by soil physics/chemistry, root exudates, and microbial communities',
 'Pure front-end, no upload; results are for risk assessment only',
 '📚 Deep Dive: Continuous-Cropping Obstacle Index (Pathogen Buildup) Estimator',
 'Score by cropping years, previous-host consistency, and soil-borne disease history.',
 'A high index signals autotoxicity and pathogen-base buildup.',
 'Used for soil-treatment decisions (disinfection / rotation / grafting).',
 'Facility cucumber continuous cropping',
 '5 years continuous, same family yearly, positive wilt history; weighted score 75/100. Suggestion: graft next crop onto black-seed pumpkin rootstock (wilt-resistant) and solar-disinfect 20 days in summer, or fallow with onion/garlic to suppress nematodes.',
 'Why is pathogen buildup hard to detect?',
 'Mostly in soil and residues, invisible from the surface; symptoms appear only when diseased and too late. Predicting by cropping years and previous-crop records is more reliable than the naked eye.',
 'How to do solar disinfection?',
 'In midsummer, saturate with water, cover with clear film and seal 2~4 weeks, using accumulated heat to kill surface pathogens and weed seeds. A low-cost physical method but dependent on hot season.',
 'About the "Continuous-Cropping Obstacle Index (Soil Pathogen Buildup) Estimator"',
 'This estimator uses an exponential-growth model from cropping years, initial pathogen density, and annual rate to estimate soil pathogen buildup, then compares with threshold density for an obstacle index and risk level, aiding continuous-cropping risk assessment and rotation decisions.',
 'Exponential model estimates current pathogen density',
 'Auto-computes accumulation multiple and obstacle index',
 'Three-level risk grading (safe/warning/severe) with advice',
 'Facility vegetables, strawberries, herbs obstacle assessment',
 'Rotation-cycle planning decisions',
 'Soil-disinfection and bio-fumigation timing',
 'Plant-protection research and teaching demos',
 'Cropping years',
 'Initial pathogen density',
 'Annual growth rate',
 'Threshold density',
]

# ---- estimate-yield-rate (41) ----
eyr = [
 '🌾 Fertilizer Use Efficiency (NPK Uptake) Estimator',
 'Use the difference method to compute apparent recovery of N, P, K nutrients and assess fertilization effect and losses',
 '📖 View the "Fertilizer Use Efficiency (NPK Uptake) Estimator Guide"',
 'Fertilizer uptake = crop uptake - soil baseline supply; apparent recovery = fertilizer uptake / applied x 100%; unrecovered = applied - fertilizer uptake',
 'The difference method measures the current-season apparent recovery: first subtract soil baseline supply to get fertilizer-contributed uptake, then divide by applied amount for recovery. The unrecovered part is residue plus loss. Recovery >=40% high, 25%~40% normal, 15%~25% low, <15% too low, each with optimization advice.',
 'Nutrient element',
 'Nitrogen (N)',
 'Phosphorus (P2O5)',
 'Potassium (K2O)',
 'Applied amount (kg/ha)',
 'Crop nutrient uptake (kg/ha)',
 'Soil baseline supply (kg/ha)',
 '💡 Difference-method formula: apparent recovery (%) = (crop uptake - soil baseline supply) / applied x 100; enter N, P2O5, K2O data separately to compute each nutrient recovery',
 'The difference method needs an unfertilized control plot to measure soil baseline supply; the result is apparent recovery',
 'Typical crop N recovery 30%~45%, P 15%~25%, K 40%~60%; too low means large losses',
 'Applied amount should be pure nutrient (e.g., 100 kg urea contains about 46 kg N)',
 'Pure front-end, no upload; results are for fertilization-effect evaluation only',
 '📚 Deep Dive: Fertilizer Use Efficiency (NPK Uptake) Estimator',
 'Fertilizer recovery = (fertilized-plot uptake - unfertilized-plot uptake) / applied x 100%.',
 'Current-season N recovery is often 30%~45%, P and K lower.',
 'Used to judge fertilization rationality and reduction potential.',
 'Wheat nitrogen recovery',
 'N-fertilized plot uptake 12 kg/mu, control 6 kg/mu, applied pure N 15 kg/mu. N recovery = (12-6)/15 = 40%. At the normal level, with deep and split application there is room to reach 45%+.',
 'Why is nitrogen recovery so low?',
 'Large losses from ammonia volatilization, nitrification-denitrification leaching, and surface runoff. Deep placement, split topdressing, and slow-release fertilizer significantly cut losses - the core lever of "zero growth in fertilizer use".',
 'Why are P and K recovery harder to compute?',
 'Phosphorus fixes in soil and potassium releases slowly from mineral K, so current-season uptake poorly tracks application; only tracers (15N/32P) are accurate, while the ordinary difference method overstates error.',
 'About the "Fertilizer Use Efficiency (NPK Uptake) Estimator"',
 'This tool uses the difference method to compute apparent recovery of N, P, K, assessing the share of fertilizer taken up by crops from applied amount, crop uptake, and soil baseline supply, aiding formula fertilization and fertilizer-effect evaluation.',
 'Computes N, P (P2O5), K (K2O) separately',
 'Difference method for apparent recovery and unrecovered amount',
 'Auto-rates recovery level (high/normal/low/too low)',
 'Formula-fertilization effect evaluation',
 'Fertilizer type and method comparison',
 'Farmland nutrient management and nonpoint pollution control',
 'Agronomic trial data analysis',
 'How to use the Fertilizer Use Efficiency (NPK Uptake) Estimator',
 'Nutrient element',
 'Applied amount',
 'Crop nutrient uptake',
 'Soil baseline supply',
]

if __name__ == '__main__':
    write('dli-calculator', '光照累积量(DLI)计算器', build('dli-calculator', dli))
    write('dry-matter-conversion', '农产品干物质含量换算器', build('dry-matter-conversion', dmc))
    write('estimate-3', '灌溉用水量估算（蒸发蒸腾）', build('estimate-3', est3))
    write('estimate-area-density', '养殖存栏量估算（面积×密度）', build('estimate-area-density', ead))
    write('estimate-area-yield', '牧草产量估算（亩产×面积）', build('estimate-area-yield', eay))
    write('estimate-content-soil', '土壤有机质含量（烧失法）估算', build('estimate-content-soil', ecs))
    write('estimate-fuel-engine-oil', '农机油耗估算（亩耗油）', build('estimate-fuel-engine-oil', efo))
    write('estimate-soil', '连作障碍指数（土壤病原菌积累）估算', build('estimate-soil', eso))
    write('estimate-yield-rate', '化肥利用率（氮磷钾吸收率）估算', build('estimate-yield-rate', eyr))
    print('gen_agri_b4 done')

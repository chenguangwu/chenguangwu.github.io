#!/usr/bin/env python3
# fishery batch4 (7 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'fishery')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'fishery')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'fish-disease-risk': [
"📋 Fish Disease Risk Evaluator",
"Evaluate fish disease occurrence risk from environmental and management factors.",
'📖 View the "Fish Disease Risk Composite Score Guide"',
"Fish disease risk = composite score",
"Dissolved oxygen (mg/L)",
"Total ammonia nitrogen (mg/L)",
"Nitrite (mg/L)",
"Transparency (cm)",
"Stocking density (times the optimum)",
"Water-exchange frequency (times/week)",
"Temperature swing this week (℃)",
"🔍 Assess risk",
"Basis:",
"Each factor is scored 0-100 by its risk contribution and summed with weights (dissolved oxygen 0.2, ammonia nitrogen 0.15, nitrite 0.15, pH 0.1, temperature 0.1, density 0.1, water exchange 0.1, transparency 0.05, temperature swing 0.05). The total score maps to four levels: low / medium / high / very high.",
"📚 In-Depth Analysis: Fish Disease Risk Composite Score",
"Assess the day's disease risk quickly from multiple factors before the daily pond patrol",
"Re-assess water-quality risk after heavy rain, water exchange or heavy feeding",
"Establish an environmental baseline before stocking a new pond",
"Default baseline scores for nine indicators",
"Dissolved oxygen 46 (weight 20% → 9.2), ammonia nitrogen 48 (15% → 7.2), nitrite 38 (15% → 5.6), pH 9 (10% → 0.9), water temperature 18 (10% → 1.8),",
"stocking density",
"24 (10% → 2.4), water-exchange frequency 50 (10% → 5.0), transparency 10 (5% → 0.5) and recent temperature swing 48 (5% → 2.4), giving a composite risk score of 35.0, a medium risk; strengthen aeration and water exchange and apply preventive disinfection.",
"How is the composite score calculated?",
"Each indicator is scored 0-100, multiplied by its weight and summed; the weights reflect that dissolved oxygen, ammonia nitrogen and nitrite have a greater influence on disease.",
"What score counts as high risk?",
"≥50 calls for immediate action, 35-50 is medium and needs tighter management, and <25 is low risk; the score is only a warning, and abnormal mortality must be confirmed with microscopy.",
'About "Fish Disease Risk Evaluator"',
"Fish Disease Risk Evaluator - weighs multiple factors such as water temperature, dissolved oxygen, ammonia nitrogen, density and water exchange to assess fish disease risk, an online fishery and aquaculture tool. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
],
'winter-heating': [
"⚡ Overwinter Heating Power Calculator",
"Compute the heating power needed to keep a pond or tank above a target temperature in winter.",
'📖 View the "Overwinter Insulation Heating Power Guide"',
"Heating power = V·ρ·c·ΔT/t",
"Water surface area (m²)",
"Target water temperature (℃)",
"Ambient air temperature (℃)",
"Cover/insulation method",
"No cover (open)",
"Single-layer film greenhouse",
"Double-layer film greenhouse",
"Insulated-panel greenhouse",
"Wind speed factor",
"Basis:",
"Heat loss Q = U × A × ΔT × wind factor; U is the heat-transfer coefficient (W/m²·℃): about 10 for an open water surface, 6 for single-layer film, 3 for double-layer film and 1.5 for insulated panels. Required power = Q × (1 + margin%) ÷ 1000 (kW). An open surface loses far more heat through evaporation, so covering the pond is recommended.",
"📚 In-Depth Analysis: Overwinter Insulation Heating Power",
"Overwinter insulation design for greenhouse and shed aquaculture",
"Selecting heating equipment (heat pump / electric heating)",
"Estimating energy use and operating cost",
"Double-layer film greenhouse insulation",
"Double-layer film with U = 3 and an indoor-outdoor temperature difference of 18.0 ℃: heat loss is about 12960 W; with a 30% margin the required heating power is about 16.85 kW and daily consumption about 404.4 kWh, a moderate energy use, so strengthen insulation to cut heat loss.",
"What is the U value?",
"The heat-transfer coefficient U is the rate of heat transfer per unit area and unit temperature difference of the enclosure (W/m²·℃); the smaller U is, the better the insulation, and double layers or added insulation cut heat loss markedly.",
"How can heating energy use be reduced?",
"Better insulation (double-layer film plus an inner thermal blanket), a smaller temperature difference, heat pumps instead of direct electric heating and extra night covers can greatly cut daily consumption.",
'About "Overwinter Heating Power Calculator"',
"Overwinter Heating Power Calculator - computes the heating power needed for overwintering from the water surface area, cover method and temperature difference, an online fishery and aquaculture tool. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
],
'spawning-hormone': [
"⚗️ Induced Spawning Hormone Dose Calculator",
"Compute induced-spawning hormone dosage for fish artificial breeding.",
'📖 View the "Broodstock Spawning Hormone Dose (Two-Injection Method) Guide"',
"Spawning dose = body weight × coefficient",
"Four major Chinese carps (black, grass, silver, bighead)",
"Catfish / longsnout catfish",
"Mandarin fish",
"Spawning protocol",
"HCG alone",
"Female broodstock weight (kg/fish)",
"Number of female broodstock",
"🔍 Calculate dosage",
"Basis:",
"Doses follow common aquaculture breeding protocols: LRH-A 10-20 μg/kg, DOM 5-10 mg/kg, HCG 800-1500 IU/kg; injections: first 10-20%, second 80-90% (8-12 h apart); the response time shortens as water temperature rises, about 10-16 h. Halve the dose for males.",
"📚 In-Depth Analysis: Broodstock Spawning Hormone Dose (Two-Injection Method)",
"From the total weight of the females and the per-fish dose, compute the total amount of spawning agent (LRH-A, DOM and so on) and split it into 15% for the first injection and 85% for the second.",
"Estimate the response time (from the second injection to spawning) and the interval between injections from the water temperature.",
"Males are usually given half the dose, injected at the time of the females' second injection.",
"Preparing the spawning agent for 50 kg of females",
"With the default parameters: 50 kg of females, 75 μg LRH-A and 35 mg DOM per fish; totals of 750 μg LRH-A and 350 mg DOM; first injection 15% (LRH-A 112.5 μg, DOM 52.5 mg) and second injection 85% (LRH-A 637.5 μg, DOM 297.5 mg); the injections are about 10 h apart and spawning occurs about 10.8 h after the second (faster at higher water temperature); the male dose is halved (LRH-A 37.5 μg, DOM 17.5 mg per fish).",
"Why split the dose into two injections?",
"The two-injection method gives the broodstock time to prepare for oestrus and ovulation, improving the fertilisation rate and spawning synchrony.",
"Can the dose be applied directly?",
"Adjust it with the gonad maturity of the broodstock, the species and the water temperature; this tool gives a basic calculation, and in practice follow veterinary advice and technical standards.",
'About "Induced Spawning Hormone Dose Calculator"',
"Induced Spawning Hormone Dose Calculator - computes the dose of spawning hormones (HCG / LRH-A / DOM) and the split-injection plan from the species and body weight, an online fishery and aquaculture tool. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
],
'plankton-biomass': [
"🔮 Plankton Biomass Estimator",
"Estimate plankton biomass from count and cell volume data.",
'📖 View the "Plankton Biomass Estimator Guide"',
"Plankton biomass = count × volume",
"Count (individuals)",
"Counting chamber volume (mL)",
"Concentration/dilution factor",
"Cell volume (μm³)",
"Conversion factor (pg/μm³)",
"Conversion type",
"Carbon biomass (0.11)",
"Wet weight (1.0)",
"Basis:",
"Cell density (cells/mL) = count ÷ chamber volume × factor; single-cell mass = volume × factor; biomass (mg/L) = density × single-cell mass (pg) × 1e-6. The carbon biomass factor is 0.11 pg C/μm³ (Menden-Deuer & Lessard) and wet weight is estimated at a density of 1.0.",
"📚 In-Depth Analysis: Phytoplankton Biomass Estimation",
"Assess water fertility and the effect of fertilising the pond",
"Monitor the standing stock of phytoplankton and its oxygen-production capacity",
"A reference for adjusting fertiliser dose and the algal community",
"Converting microscope counts to biomass",
"Cell density 120 cells/mL and single-cell mass 55 pg: biomass = 120 × 55 pg ≈ 0.0066 mg C/L, a low level, so fertilise moderately to promote the algal community.",
"What does a low biomass indicate?",
"The water may be too lean, short of nutrients or dominated by a single algal group, limiting oxygen production and natural food supply; use transparency and nutrients to judge whether top-dressing is needed.",
"How is water fertility judged?",
"It is usually graded by chlorophyll a or phytoplankton carbon biomass; too low means lean water and too high risks algal collapse and oxygen depletion, so keeping it moderate and the algal community stable matters most.",
'About "Plankton Biomass Estimator"',
"Plankton Biomass Estimator - estimates plankton biomass from microscope counts and cell volume, an online fishery and aquaculture tool. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
],
'fry-transport-survival': [
"🚚 Fry Transport Survival Rate Calculator",
"Estimate fry survival during transport from density, temperature and duration.",
'📖 View the "Fry Transport Survival Estimation Guide"',
"Transport survival rate = f(density, temperature, time)",
"Loading density (g/L)",
"Transport duration (h)",
"Aeration method",
"Pure oxygen",
"Air aeration",
"No aeration",
"Target survival rate (%)",
"Basis:",
"Risk rate = 0.02 × (density/100) × (duration/6) × exp((water temperature - 15)/12) × aeration coefficient; survival rate = 100 × exp(-risk rate). The coefficient is 0.5 for pure oxygen, 1.0 for air and 2.0 for no aeration. The recommended density is back-calculated from the target survival rate.",
"📚 In-Depth Analysis: Fry Transport Survival Estimation",
"Design the bagging or loading density before long-distance fry transport",
"Assess how transport duration and aeration conditions affect survival",
"Back-calculate the maximum loading density from the target survival rate on arrival",
"Estimate for a routine transport plan",
"Density 80 g/L, duration 8 h, water temperature 18 ℃ and an aeration coefficient of 1: the estimated survival rate is 97.3% (risk rate 0.0274); to reach a 95% target survival rate, keep the density ≤ 150 g/L.",
"What are the key factors affecting survival?",
"Mainly density, water temperature, transport duration and dissolved oxygen. The higher the density, the higher the temperature and the longer the time, the greater the metabolism and oxygen consumption, and the lower the survival rate.",
"How is the aeration coefficient used?",
"Take 1 for a pure-oxygen bag and <1 for open or weak aeration; better aeration markedly extends the safe transport time.",
'About "Fry Transport Survival Rate Calculator"',
"Fry Transport Survival Rate Calculator - estimates fry transport survival from the transport density, duration, water temperature and aeration method, an online fishery and aquaculture tool. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
],
'drug-withdrawal-fish': [
"🌡️ Fish Drug Withdrawal Calculator",
"Compute the drug withdrawal period with temperature correction for fish.",
'📖 View the "Fish Drug Withdrawal Temperature Correction (Degree-Day Model) Guide"',
"Withdrawal period = baseline × (temperature correction)",
"Drug type",
"Sulfonamides",
"Actual water temperature (℃)",
"Standard withdrawal period (days)",
"Reference temperature (℃)",
"Lower temperature limit (℃)",
"🔍 Calculate correction",
"Basis:",
"A degree-day model is used: the degree-days needed for elimination K = standard days × (reference temperature - lower temperature limit); corrected days = K ÷ (actual water temperature - lower temperature limit). The higher the water temperature, the faster the metabolism and the shorter the withdrawal period; below the limit the drug is metabolised very slowly, so extend the period and strengthen testing.",
"📚 In-Depth Analysis: Fish Drug Withdrawal Temperature Correction (Degree-Day Model)",
"Before harvest and sale, correct the withdrawal period for the actual water temperature to keep drug residues below the MRL and avoid failing a drug test.",
"Warmer water speeds up drug metabolism, so the period can be shorter than standard; colder water (especially near the lower limit) extends it greatly.",
"Different drugs (enrofloxacin, oxytetracycline, florfenicol, sulfonamides, formalin) are corrected with their own standard withdrawal period and reference temperature.",
"Correcting a standard 14 days @15 ℃ at a water temperature of 22 ℃",
"With the default parameters (standard withdrawal period 14 days @ a reference temperature of 15 ℃, lower temperature limit 5 ℃, actual water temperature 22 ℃): the degree-day requirement K = 14×(15−5) = 140 ℃·days; the effective temperature = 22−5 = 17 ℃; the corrected withdrawal period = 140 / 17 ≈ 8.2 days, about 0.59 times the standard, shortened by the warmer water. If the water temperature falls to 8 ℃, the corrected value = 140/3 ≈ 46.7 days, markedly longer.",
'What is a "degree-day"?',
"A degree-day (℃·day) measures the driving effect of accumulated temperature on drug metabolism; the withdrawal period is inversely proportional to the effective temperature, a common simplified model for drug-residue control in aquaculture.",
"What if the water temperature is below the limit?",
"When the effective temperature is ≤0 the metabolism is extremely slow; the tool warns you to extend the withdrawal period and send samples for residue testing, and the formula must not be applied directly.",
'About "Fish Drug Withdrawal Calculator"',
"Fish Drug Withdrawal Calculator - corrects the fish drug withdrawal period for water temperature based on a degree-day model, an online fishery and aquaculture tool. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
],
'stocking-density': [
"🐟 Shrimp Stocking Density Optimizer",
"Optimize shrimp stocking density from pond area and target survival.",
'📖 View the "Shrimp Stocking Density Optimisation (Power / Volume Dual Constraint) Guide"',
"Stocking density = optimised carrying capacity",
"Total aeration power (kW)",
"Target harvest size (g/shrimp)",
"Expected survival rate (%)",
"🔍 Optimise",
"Basis:",
"The carrying capacity is estimated from the aeration power (intensive supports about 700 kg/mu of yield per kW, semi-intensive 450 and extensive 200); a safety ceiling is also set by the water volume (intensive ≤60 kg/m³ of standing biomass). The recommended density takes the smaller of the two, and density = carrying capacity ÷ (size × survival rate).",
"📚 In-Depth Analysis: Shrimp Stocking Density Optimisation (Power / Volume Dual Constraint)",
"For species such as Pacific white shrimp, find a safe",
"stocking density",
"ceiling before stocking, subject to the dual constraints of aeration power and water volume.",
"Re-assess the carrying capacity and risk when switching between farming modes (extensive / semi-intensive / intensive).",
"Convert the carrying capacity into the number of juveniles to stock using the target size and expected survival rate.",
"5 mu, 1.2 m deep, 4 kW aeration, semi-intensive, target 15 g, survival rate 75%",
"With the default parameters: the power-based carrying capacity = (4/5)×450 = 360 kg/mu; the volume-based carrying capacity = 3×(5×1.2×666.67)/5 = 2400 kg/mu; take the smaller 360 kg/mu; stocking density = 360/(15/100)/0.75 ≈ 3200 shrimp/mu, a total stocking of ≈ 16000, with an expected yield of 1800 kg; aeration of 0.8 kW/mu reaches the low-risk line.",
"Why take the smaller of the power and volume ceilings?",
"Either one becoming a bottleneck limits production; taking the smaller value ensures neither constraint is breached, a conservative and safe choice.",
"What happens if the aeration power is insufficient?",
"The power-based carrying capacity falls; below 0.5 kW/mu the risk rises, so reduce the density or add aerators.",
'About "Shrimp Stocking Density Optimizer"',
"Shrimp Stocking Density Optimizer - optimises the shrimp stocking density from pond area, water depth, aeration capacity, target size and survival rate, an online fishery and aquaculture tool. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
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

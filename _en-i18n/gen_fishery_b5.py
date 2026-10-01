#!/usr/bin/env python3
# fishery batch5 (6 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'fishery')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'fishery')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'dissolved-oxygen': [
"🐟 Pond Dissolved Oxygen Predictor",
"Compute saturated dissolved oxygen from water temperature, air pressure and salinity, and predict the pre-dawn minimum to prevent fish from gasping at the surface.",
'📖 View the "Pond Dissolved Oxygen and Pre-Dawn Hypoxia Prediction Guide"',
"DO prediction = f(temperature, pressure)",
"Air pressure (kPa)",
"Salinity (‰)",
"Current measured DO (mg/L)",
"Hours until dawn (h)",
"Night-time oxygen consumption rate (mg/L·h)",
"🔍 Predict",
"Basis:",
"Freshwater saturated DO uses the empirical polynomial DO = 14.652 - 0.41022T + 0.007991T² - 0.000077774T³; salinity is corrected with the Benson-Krause formula (T in kelvin); pressure is corrected as DO(P) = DO(1atm) × P/P₀. Pre-dawn DO = current DO - consumption rate × time.",
"📚 In-Depth Analysis: Pond Dissolved Oxygen and Pre-Dawn Hypoxia Prediction",
"Anticipate the lowest DO before dawn (photosynthesis stops while respiration continues) during farm management, and decide in advance when to switch on the aerators to prevent a pond turnover and fish kills.",
"Re-check whether the current DO saturation falls in the safe range after a sudden salinity or temperature change from filling, draining or water exchange (generally ≥5 mg/L, and not below 3 mg/L before dawn).",
"Evaluate aerator operating strategy: combine the night-time consumption rate with the hours until dawn to quantify how much longer the pond can hold out.",
"DO accounting at 26℃, salinity 0 and 101.3 kPa",
"With the default parameters (water temperature 26℃, salinity 0‰, air pressure 101.3 kPa, current DO 6.5 mg/L, 9 h until dawn and a night-time consumption rate of 0.35 mg/L·h): saturated DO is about 8.02 mg/L and the current saturation is 81.1%; with continuous consumption of 0.35 mg/L·h for 9 h, the pre-dawn DO is about 6.5 - 0.35×9 = 3.35 mg/L, in the low range, so switch on the aerators early.",
"Why does saturated DO fall as water temperature rises?",
"Higher water temperature lowers the solubility of oxygen in water; saturated DO is about 8.0 mg/L at 26℃ but above 11 mg/L at 10℃; high salinity also pushes the saturation value down further.",
"Why is hypoxia most likely before dawn?",
"There is no photosynthesis producing oxygen at night, but fish, shrimp and microbes keep consuming it through respiration, so DO reaches its daily minimum in the early morning, the peak time for pond turnover, and should be monitored closely.",
'About "Pond Dissolved Oxygen Predictor"',
"Pond Dissolved Oxygen Predictor - predicts saturated dissolved oxygen from water temperature, air pressure and salinity and forecasts the pre-dawn minimum from night-time consumption, an online fishery and aquaculture tool. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
],
'water-exchange-rate': [
"🐟 Pond Water-Exchange Rate and Water-Quality Stability Calculator",
"Compute the steady-state pollutant concentration, water-quality stabilisation time and effective exchange rate from the exchanged volume.",
'📖 View the "Water-Exchange Rate and Steady-State Concentration Estimation Guide"',
"Exchange rate = flow / pond volume",
"Pond water volume (m³)",
"Daily exchanged volume (m³/day)",
"Pollutant generation rate (mg/L·day)",
"Inlet pollutant concentration (mg/L)",
"Target pollutant concentration (mg/L)",
"Basis:",
"Daily exchange rate = exchanged volume ÷ water volume; time constant τ = water volume ÷ exchanged volume; steady-state concentration C_ss = C_in + generation rate × τ; approaching the steady state from an initial concentration C₀: C(t) = C_ss + (C₀-C_ss)e^(-t/τ); the time to reach the target is solved from the exponential approach.",
"📚 In-Depth Analysis: Water-Exchange Rate and Steady-State Concentration Estimation",
"Steady-state pollutant concentration accounting for closed/semi-closed water bodies",
"Water-exchange scheme design and target-compliant exchange volume estimation",
"Balancing emission reduction and water exchange",
"Steady state at a 10% daily exchange rate",
"At a daily exchange rate of 10% and a time constant of 10 days: the steady-state concentration is about 5.10 mg/L (target 2 mg/L), already over the limit; reaching the target requires a higher exchange rate or cutting the pollution source, and the minimum exchange volume is about 211 m³/day.",
"What is steady-state concentration?",
"The pollutant concentration reached at equilibrium between continuous pollution and a fixed-proportion water exchange; keeping below it maintains water quality, and above it calls for more exchange or less pollution.",
"How should the time constant be understood?",
"Time constant = 1 / daily exchange rate; the larger it is, the slower water quality responds to exchange and the longer it takes to reach the steady state.",
'About "Pond Water-Exchange Rate and Water-Quality Stability Calculator"',
"Pond Water-Exchange Rate and Water-Quality Stability Calculator - computes the exchange rate, steady-state pollutant concentration and target-compliant time to assess water-quality stability, an online fishery and aquaculture tool. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
],
'parasite-lifecycle': [
"🌡️ Parasite Life-Cycle Temperature-Dependence Simulator",
"Simulate the development time and life-cycle period of common fish parasites with a degree-day model and assess outbreak risk.",
'📖 View the "Parasite Life-Cycle Period Estimation Guide"',
"Parasite cycle = temperature-dependent simulation",
"Parasite species",
"Ichthyophthirius (white spot disease)",
"Dactylogyrus",
"Fish louse",
"Trichodina",
"Basis:",
"Degree-day model: development time = K ÷ (T - T₀), where T₀ is the development threshold temperature and K is the effective accumulated temperature (℃·day). One full life cycle = the sum of the development times of all stages. The higher the water temperature, the faster the development, the shorter the generation and the higher the outbreak risk.",
"📚 In-Depth Analysis: Parasite Life-Cycle Period Estimation",
"Set deworming and preventive disinfection cycles according to water temperature",
"Early warning of parasite outbreaks in the warming season",
"A design reference for the interval between pond clearing and restocking",
"Life-cycle period at 25℃",
"By the accumulated-temperature model: theront infection 0.2 days (accumulated temperature 3 ℃·day), trophont parasitism 8.6 days (120) and tomont reproduction 4.1 days (57), a total life-cycle period of about 12.0 days, a medium risk; at 31℃ it shortens to about 8.6 days and the risk rises.",
"How does temperature affect the cycle?",
"Parasite development follows the accumulated-temperature rule: the higher the temperature, the faster the development, the shorter the life cycle and the more generations per unit time, so the outbreak risk rises.",
"How do I use the cycle to schedule deworming?",
"Arrange a preventive treatment around the end of one life-cycle period (e.g. about 12 days at 25℃) and adjust the water and substrate to lower host density.",
'About "Parasite Life-Cycle Temperature-Dependence Simulator"',
"Parasite Life-Cycle Temperature-Dependence Simulator - simulates parasite development time and life cycle against temperature with a degree-day model, an online fishery and aquaculture tool. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
],
'harvest-size-price': [
"📊 Harvest Size-Price Relationship Analyzer",
"Analyze returns by size-price tier and find the best market size from growth rate and feed cost.",
'📖 View the "Delayed-Harvest Size-Price Net Return Analysis Guide"',
"Size price = average weight × unit price",
"Size-price tiers (body weight g → unit price CNY/kg)",
"➕ Add tier",
"Current total standing stock (kg)",
"Current average weight (g)",
"SGR (%/day)",
"Basis:",
"Linear interpolation of the size price; number of fish = standing stock × 1000 ÷ average weight; extra yield from growing to the target size = fish number × (target weight - current weight) ÷ 1000; days needed = ln(target weight / current weight) × 100 ÷ SGR; extra feed = extra yield × FCR; net return comparison = delayed-harvest revenue - current-harvest revenue - feed cost.",
"📚 In-Depth Analysis: Delayed-Harvest Size-Price Net Return Analysis",
"Compare the net return of selling now at the current size with growing on to a larger size, to support the harvest decision.",
"Estimate the extra yield, days needed and feed cost from the price ladder (larger size, higher unit price), SGR and FCR.",
"Pick the target size tier with the largest delayed net return.",
"Net return illustration for 1000 kg, 500 g/fish delayed to 800 g",
"Illustration (using the actual price ladder and parameters): number of fish = 1000×1000/500 = 2000; at a target of 800 g the extra yield = 2000×(800-500)/1000 = 600 kg; at an SGR of 2%/day it takes about 23.5 days; extra feed = 600×FCR(assume 1.5) = 900 kg, costing about 7200 CNY; if the unit price is 16 at 500 g and 20 CNY/kg at 800 g, the extra revenue is about 32000-16000 = 16000 CNY and the net return about 8800 CNY, so this tier is worth delaying for. In practice refer to the price ladder you enter in this tool.",
"Why compute net return instead of just the unit price?",
"A larger size commands a higher unit price but needs more feed, more pond space and more risk, so the net return is the basis for the decision.",
"How much does the feed conversion ratio FCR matter?",
"The higher the FCR, the greater the feed cost of delaying and the lower the net return; species with a low FCR are better suited to delayed harvest.",
'About "Harvest Size-Price Relationship Analyzer"',
"Harvest Size-Price Relationship Analyzer - analyzes the price and return of different harvest sizes and finds the best market timing from growth and feed cost, an online fishery and aquaculture tool. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
],
'fish-growth-curve': [
"👶 Fish Growth Curve Fitter",
"Enter multiple (farming days, body weight g) data points to fit the specific growth rate SGR and forecast growth.",
'📖 View the "Fish Growth Curve Fitting (Exponential / Specific Growth Rate SGR) Guide"',
"Growth curve = specific growth rate fit",
"Weighing data points (at least 2 sets)",
"➕ Add data point",
"📊 Fit and forecast",
"Target body weight to forecast (g)",
"Predict body weight on day N",
"Basis:",
"Regress ln(body weight) on farming days; the slope × 100 is the specific growth rate SGR (%/day, exponential model W = W₀·e^(SGR·t/100)). R² assesses the goodness of fit. Weight-doubling time = ln2 × 100 ÷ SGR.",
"📚 In-Depth Analysis: Fish Growth Curve Fitting (Exponential / Specific Growth Rate SGR)",
"Fit the exponential growth equation W = W0·e^(k·t) to body-weight samples at several time points to estimate the specific growth rate SGR and the days to reach the target size.",
"Assess the goodness of fit (R²) to judge whether the samples support this growth model and avoid distortion when extrapolating.",
"Generate a growth forecast table to support feeding plans and the choice of harvest timing.",
"SGR fitting and the forecast days to reach 500 g",
"The default samples give the equation W = 5.45 × e^(3.705·t/100), a specific growth rate SGR ≈ 3.705%/day and a goodness of fit R² ≈ 0.995; on this basis it takes about 122 days to reach 500 g, and the forecast weight on day 90 is about 152.8 g (starting from 5.4 g). The high R² shows the exponential model applies over this range.",
"What is SGR?",
"The specific growth rate, the relative rate of body-weight gain per unit time (%/day); it is a common index describing fish growth, and the higher the SGR the faster the growth.",
"What does a low R² indicate?",
"The samples deviate from the exponential model (for example a growth inflection point or data noise); the day forecast is then only indicative, and you should add samples or switch to another growth model.",
'About "Fish Growth Curve Fitter"',
"Fish Growth Curve Fitter - fits the specific growth rate SGR from repeated weighing data and predicts future body weight and the time to reach the target, an online fishery and aquaculture tool. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
],
'feed-rate-calculator': [
"🐟 Feed Rate Calculator",
"Compute the feeding rate (as a percentage of body weight) and daily feed amount from average fish weight, water temperature and farming type.",
'📖 View the "Fine Feed Rate Calculation (Base Rate × Temperature Factor) Guide"',
"Feeding rate = body weight × rate%",
"Farming type",
"Total standing stock (kg)",
"Average fish weight (g)",
"Basis:",
"Base feeding rate FR = 8.0×W⁻⁰·³³ (W is the average weight in g); the temperature factor is corrected by a Gaussian-type function around the optimum temperature; the optimum is 16℃ for cold-water fish, 28℃ for warm-water fish and 30℃ for shrimp. In practice also adjust for feeding response.",
"📚 In-Depth Analysis: Fine Feed Rate Calculation (Base Rate × Temperature Factor)",
"Taking the base ",
"feeding rate",
" as the reference, corrected by the temperature factor for the actual water temperature to get the daily feeding rate.",
"Combine the average fish weight and the number of meals to split the daily feed amount and the amount per meal.",
"Used for precision feeding, balancing growth rate and the feed conversion ratio (FCR).",
"Feed accounting for warm-water fish at an average weight of 100 g and 26℃",
"Default parameters: base feeding rate 1.75%, a temperature factor of 0.92 at 26℃, so the corrected feeding rate = 1.75%×0.92 ≈ 1.61%; if the total fish weight is 1000 kg, the daily feed amount is about 16.13 kg, split into 3 meals of about 5.38 kg each.",
"Where does the temperature factor come from?",
"It comes from an empirical curve of the effect of water temperature on metabolism, usually highest at the optimum temperature and falling when too cold or too hot, with slight differences between species.",
"How is the base feeding rate set?",
"Look it up by species and average weight or use an empirical value, then correct it with the temperature factor according to the actual feeding response and water quality.",
'About "Feed Rate Calculator"',
"Feed Rate Calculator - computes the daily feeding rate and amount by fish body weight, water temperature and species, and gives meal-splitting advice, an online fishery and aquaculture tool. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
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

#!/usr/bin/env python3
# fishery batch2 (5 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'fishery')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'fishery')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'oxygen-machine': [
"🧮 Aerator Configuration Calculator",
"Size the number and power of aerators required for a pond.",
'📖 View the "Aerator Configuration Calculator Guide"',
"Aerator configuration = oxygen demand / power per unit",
"Water volume (m³)",
"Fish biomass (kg)",
"Aerator model",
"Impeller type 3 kW (2.5 kg O₂/h)",
"Impeller type 1.5 kW (1.2 kg O₂/h)",
"Paddlewheel type 1.1 kW (0.9 kg O₂/h)",
"Jet type 0.75 kW (0.6 kg O₂/h)",
"Nano-tube bottom aerator 1 kW (1.5 kg O₂/h)",
"Fish oxygen consumption (g/h) = fish biomass (kg) × unit oxygen consumption rate (mg/kg·h) ÷ 1000",
"Water oxygen consumption (g/h) = water volume (m³) × water oxygen consumption rate (mg/L·h)",
"Total oxygen demand (kg/h) = (fish + water oxygen consumption) ÷ 1000",
"Number of aerators = ceil(total oxygen demand / capacity per unit)",
"The oxygen consumption rate rises with water temperature, estimated at about a Q10 = 2 ratio (doubling for every 10 ℃ rise). The aerator configuration includes a 1.5× safety margin.",
"🐟 Oxygen Consumption Rates of Common Species (25 ℃)",
"Oxygen consumption rate (mg/kg·h)",
"Temperature coefficient",
"Mid-upper layer, relatively high oxygen consumption",
"Tolerates low oxygen, relatively low consumption",
"Tolerates low oxygen",
"High oxygen demand, sensitive to low oxygen",
"Highest oxygen consumption per unit weight",
"⚙️ Performance Comparison of Common Aerators",
"Oxygen-transfer capacity",
"Impeller type",
"Large ponds, the mainstream choice",
"Small and medium ponds",
"Paddlewheel type",
"Shrimp and crab ponds, good water flow",
"Jet type",
"Deep water, high density",
"Nano-tube bottom aerator",
"Industrial systems and shrimp ponds, high efficiency",
"📚 In-Depth Analysis: Aerator Configuration Calculation",
"Selecting aerator types and numbers for new or renovated ponds",
"Checking whether the aeration capacity suffices under high-density intensive farming",
"Assessing the aeration margin for the night and pre-dawn hours when oxygen depletion peaks",
"Aeration configuration for a medium-density grass carp pond",
"Grass carp at 25 ℃ and a density of 0.5 kg/m³: fish oxygen consumption 125 g/h + water oxygen consumption 600 g/h = 725 g/h in total; with a 1.5× safety margin the total oxygen demand is 1.087 kg/h; one 3 kW impeller aerator (total power 3.00 kW) covers it.",
"Why keep a 1.5× margin?",
"At night and before dawn photosynthesis stops while respiration continues, so dissolved oxygen often falls to its daily minimum; the margin covers the oxygen-consumption peaks caused by high density, high temperature and sudden weather changes.",
"How to choose between impeller aerators and fine-bubble aeration?",
"Impeller aerators lift and mix the water with even aeration and suit medium and large surfaces; fine-bubble aeration is efficient and suits bottom aeration in intensive ponds; combine them according to surface area and density.",
'About "Aerator Configuration Calculator"',
"Aerator Configuration Calculator. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
],
'profit-calculator': [
"💰 Aquaculture Profit Calculator",
"Compute farming profit from revenue, feed, fry and operating costs.",
'📖 View the "Farming Profit and Cost Structure Guide"',
"Profit = revenue − cost",
"📊 Revenue",
"Output (kg)",
"Unit price (CNY/kg)",
"By-product revenue (CNY)",
"💸 Costs (CNY)",
"Fry",
"Feed",
"Electricity",
"Medicine",
"Labour",
"Pond rent",
"💰 Calculate profit",
"Formula description:",
"Direct cost = fry + feed + electricity + medicine",
"Indirect cost = labour + pond rent + other",
"Total cost = direct cost + indirect cost",
"Total revenue = output × unit price + by-product revenue",
"Gross profit = total revenue - direct cost",
"Net profit = total revenue - total cost",
"Profit margin = net profit / total revenue × 100%",
"Return on investment ROI = net profit / total cost × 100%",
"📚 In-Depth Analysis: Farming Profit and Cost Structure",
"Before harvest, work out the net profit and",
"profit margin",
"of one farming cycle to assess profitability.",
"Break down direct costs (fry, feed, electricity, medicine) and indirect costs (labour, pond rent, other) to locate the biggest cost items.",
"Back-calculate the unit cost (CNY/kg) and compare it with the selling price to judge",
"break-even",
"Output 5000 kg, unit price 20 CNY/kg, other costs as defaults",
"With the default parameters: revenue = 5000×20 = 100000 CNY; direct cost = 3000+30000+2000+1000 = 36000 CNY; indirect cost = 5000+4000+1000 = 10000 CNY; total cost 46000 CNY; net profit = 100000−46000 = 54000 CNY; profit margin 54%,",
"≈ 117%, unit cost 9.2 CNY/kg.",
"What is the difference between gross and net profit?",
"Gross profit subtracts direct production costs, while net profit further subtracts indirect costs such as labour and pond rent, reflecting true profitability better.",
"Why does unit cost matter?",
"When the selling price approaches the unit cost you are near break-even; a rising unit cost eats directly into profit, so cut the feed share first.",
'About "Aquaculture Profit Calculator"',
"Aquaculture Profit Calculator. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
],
'seafood-cold-storage': [
"🌡️ Seafood Cold Storage Reference",
"Look up cold-storage temperature and shelf life for seafood products.",
'📖 View the "Seafood Cold Storage Shelf-Life Guide"',
"Cold-storage temperature ↔ shelf life",
"Seafood type",
"Fresh fish (ice-chilled)",
"Fresh shrimp",
"Shellfish",
"Frozen fish (-18 ℃)",
"Dried seafood",
"Surimi products",
"Storage temperature (℃)",
"Q10 factor",
"Basis:",
"Shelf life = t_ref × Q10^((T_ref-T)/10); for every 10 ℃ rise the spoilage rate becomes Q10 times faster. The reference shelf life is the value at the standard storage temperature (about 7 days for fresh fish at 0 ℃, about 180 days for frozen fish at -18 ℃, and so on). In practice it also depends on initial freshness and hygiene.",
"Cold-Storage Reference for Common Seafood",
"Reference shelf life",
"Keep cold and moist",
"Prone to blackening",
"Keep alive",
"Frozen fish",
"180 days",
"Avoid repeated freeze-thaw",
"Dry at room temperature",
"180-365 days",
"Moisture-proof",
"📚 In-Depth Analysis: Seafood Cold-Storage Shelf-Life Estimation",
"Estimating the shelf life and safe-eating window of ice-chilled fish",
"Cold-chain temperature management and stock rotation planning",
"Comparing preservation time at different storage temperatures",
"Shelf life of ice-chilled fish at 0 ℃",
"Fresh fish held ice-chilled at 0 ℃, corrected with Q10 = 3: the reference shelf life is about 8.0 days, a time-limited product, so watch freshness and microbial changes.",
"What is Q10?",
"Q10 is the factor by which the rate of a chemical reaction (such as spoilage or enzyme activity) increases for every 10 ℃ rise; here it is used to derive the shelf life at different storage temperatures from the reference temperature.",
"How much does temperature affect shelf life?",
"For every 10 ℃ drop the shelf life extends by roughly Q10 times; ice-chilled storage (0 ℃) therefore far outlasts room temperature, though it is still time-limited and needs hygiene and antimicrobial control.",
'About "Seafood Cold Storage Reference"',
"Seafood Cold Storage Reference - estimates the shelf life of seafood at different chilled temperatures using a Q10 model, an online fishery and aquaculture tool. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
],
'water-oxygen': [
"📚 Dissolved Oxygen Reference Table",
"Look up dissolved oxygen saturation values in water by temperature and salinity.",
'📖 View the "Dissolved Oxygen Reference and Saturation Guide"',
"< 2 mg/L Dangerous",
"2-4 mg/L Low",
"4-8 mg/L Normal",
"> 8 mg/L Supersaturated",
"Saturated DO DO_sat = two-dimensional linear interpolation (temperature t, salinity s); saturation = measured DO / DO_sat × 100%",
"First locate the temperature interval by water temperature and the salinity interval by salinity, then perform bilinear interpolation to obtain the theoretical saturated dissolved oxygen under those conditions; saturation = measured ÷ saturated × 100%. Grading: <2 dangerous (surface gasping), <4 low (turn on aerators), ≤8 normal, >8 supersaturated (guard against gas bubble disease).",
"Salinity (‰)",
"Measured dissolved oxygen (mg/L)",
"📊 Show the full reference table",
"Saturated dissolved oxygen falls as temperature and salinity rise; values at standard atmospheric pressure. Linear interpolation formula: DO = DO",
"), interpolating temperature and salinity together.",
"🐟 Suitable Dissolved Oxygen Ranges for Common Farmed Fish",
"Minimum DO (mg/L)",
"Suitable DO (mg/L)",
"Prone to surface gasping at low oxygen",
"Strong tolerance of low oxygen",
"Tolerates low oxygen, suits high density",
"Mid-upper layer fish",
"Disease outbreaks are likely at low oxygen",
"Chinese mitten crab",
"High dissolved-oxygen requirement",
"📋 Full Saturated Dissolved Oxygen Table (mg/L)",
"📚 In-Depth Analysis: Dissolved Oxygen Reference and Saturation Lookup",
"Quickly look up the saturated dissolved oxygen by water temperature and salinity, and the saturation of the current measured value, to judge whether it is safe.",
"Use it as a reference baseline for dissolved-oxygen management together with aerators and water-quality monitoring.",
"Use it for a safety re-check when salinity or temperature changes abruptly after filling or draining.",
"Saturation at 25 ℃, salinity 0 and a measured value of 6.5 mg/L",
"With the default parameters: at 25 ℃ and salinity 0‰ the saturated dissolved oxygen is about 8.2 mg/L; a measured 6.5 mg/L corresponds to a saturation of ≈ 79%, in the safe range but below saturation, so watch the night-time drop. The usual requirement is ≥5 mg/L and no lower than 3 mg/L before dawn.",
"What does saturated dissolved oxygen vary with?",
"It falls as water temperature rises and as salinity rises; at standard atmospheric pressure use the table or a solubility formula.",
"What if the saturation is low?",
"Turn on aerators, exchange water for more flow or lower the density; night and pre-dawn are peak oxygen-depletion hours, so monitor more closely.",
'About "Dissolved Oxygen Reference Table"',
"Dissolved Oxygen Reference Table. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
],
'breeding-cycle': [
"🐟 Breeding Cycle Management",
"Plan the breeding cycle and grow-out schedule for aquaculture.",
'📖 View the "Farming Cycle and Market-Timing Plan (by Stage) Guide"',
"Farming cycle = nursing + grow-out + harvest",
"Stocking date",
"Initial size (g/fish)",
"Water temperature range",
"Low (10-18 ℃) - slow growth",
"Optimal (20-28 ℃) - fast growth",
"High (28-32 ℃) - slightly slower",
"Project name (optional)",
"🐟 Calculate cycle",
"Stage notes:",
"Stocking stage",
"the acclimation period after stocking; watch the survival rate and feed training",
"Nursing stage",
"fry are nursed to a medium size; nutrition and the water environment matter most",
"Grow-out stage",
"the main weight-gain phase; step up feeding and dissolved-oxygen management",
"Harvest stage",
"stop feeding, clear the bottom and prepare for market",
"The daily growth rate is an empirical value, affected by water temperature, feed, density and water quality. Growth is fastest at the optimal temperature, while low temperatures slow metabolism and require more time.",
"📜 My Farming Plan",
"📚 In-Depth Analysis: Farming Cycle and Market-Timing Plan (by Stage)",
"Before stocking, divide the cycle into stocking / nursing / grow-out / harvest stages according to the typical growth rhythm of the species, and work backwards to the best stocking date to hit the market window.",
"Combine the expected daily growth rate to estimate the total farming cycle and the expected market date, supporting cash flow and pond turnover planning.",
"Stage lengths differ widely between species (grass carp, common carp, crucian carp and others), so plan with the actual species parameters.",
"Typical farming cycle for grass carp",
"Taking grass carp as an example (default parameters): the total cycle is about 138 days with a daily growth rate of about 2.50%; the stocking stage is 14 days, the nursing stage 34 days (to about 165 g), the grow-out stage 76 days (to about 1073 g) and the harvest stage 28 days (to a market size of about 1500 g); if stocking takes place on 2026-09-08 the expected market date is 2027-02-07. Each stage requires matching adjustments to water depth, dissolved oxygen, feed protein and water-exchange frequency.",
"Why plan the cycle separately by species?",
"Growth rate, optimum temperature range and market size differ markedly between species; using one cycle for all leads to off-spec sizes or missing the price peak.",
"Can the daily growth rate simply be extrapolated?",
"It can only give a stage-level estimate, since in practice water temperature, dissolved oxygen, density and disease all matter; growth slows in the cold season, so adjust dynamically with on-pond measurements.",
'About "Breeding Cycle Management"',
"Breeding Cycle Management. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
"e.g. Pond 1",
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

#!/usr/bin/env python3
# fishery batch1 (4 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'fishery')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'fishery')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'salinity-calculator': [
"🐟 Salinity Calculator",
"Compute and convert water salinity for aquaculture ponds and tanks.",
'📖 View the "Salinity Mixing Calculator Guide"',
"Salinity S",
"(Practical Salinity Scale, PSU) is the grams of dissolved salt per kilogram of water. Salinity meters usually derive it from electrical conductivity EC:",
"The freshwater/seawater boundary is about 0.5 PSU; the open ocean averages about 35 PSU.",
"Approximate specific gravity relation:",
"(e.g. 35 PSU ≈ 1.035).",
"Freshwater fish prefer <0.5 PSU; euryhaline species (tilapia, salmon) tolerate more; marine culture usually stays at 25–35 PSU.",
"Salinity changes directly affect dissolved oxygen, osmotic pressure and survival, so monitor it when exchanging or topping up water.",
"Salinity = salt mass / water volume",
"Existing water volume V1 (L)",
"Existing water salinity S1 (‰)",
"Added water salinity S2 (‰)",
"Target salinity St (‰)",
"🔄 Switch dilution / salting",
"Mixing formula:",
"Derived: V2 = V1 × (St - S1) / (S2 - St)",
"Tips:",
"• Salting (target salinity > existing): S2 should be greater than St",
"• Dilution (target salinity < existing): S2 should be less than St",
"• The switch button automatically reverses the roles of S1 and S2",
"🐟 Suitable Salinity Ranges for Common Farmed Species",
"Salinity range (‰)",
"Optimum salinity (‰)",
"Grass carp / common carp / crucian carp",
"Freshwater fish, low salt tolerance",
"Euryhaline, fairly salt-tolerant",
"Rainbow trout",
"Cold-water fish, tolerates short-term high salinity",
"Euryhaline, seawater/freshwater",
"Strongly euryhaline, optimum in brackish water",
"Chinese white shrimp",
"Prefers seawater",
"Black tiger shrimp",
"Euryhaline marine shrimp",
"Sea bass / sea bream",
"Marine fish",
"Large yellow croaker",
"Chinese mitten crab (adult)",
"Freshwater; brackish water is needed for larval rearing",
"Mud crab",
"Euryhaline marine crab",
"📚 In-Depth Analysis: Salinity Mixing Calculation",
"For seawater or brackish-water culture and water adjustment, compute the volume V2 needed to bring existing water from S1 to the target salinity St.",
"Decide whether to salt or to dilute, avoiding the wrong direction that pushes salinity away from the target.",
"Verify that the actual salinity after mixing lands on the target (a mass-balance check).",
"1000 L (0‰) + 35‰ seawater → target 15‰",
"With the default parameters: V2 = 1000×(15−0)/(35−15) = 1000×15/20 = 750 L; the total volume after mixing is 1750 L; the actual salinity = (1000×0 + 750×35)/1750 = 15.0‰, matching the target. To lower salinity, add low-salinity water and compute V2 the same way.",
"What is the principle behind the formula?",
"It rests on conservation of salt mass, V1·S1 + V2·S2 = (V1+V2)·St, solved for V2; this is linear mixing.",
"What if the computed V2 is negative?",
"It means the direction is reversed (for example the target is above the current value but low-salinity water is added); use higher-salinity water instead or reverse the operation.",
'About "Salinity Calculator"',
"Salinity Calculator is an online tool in the fishery and aquaculture field. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
],
'pond-capacity': [
"🐟 Pond Stocking Capacity Calculator",
"Estimate the carrying capacity of a pond from volume, oxygen and species.",
'📖 View the "Pond Carrying Capacity Estimation Guide"',
"Carrying capacity = f(area, dissolved oxygen, water exchange)",
"Pond area (mu)",
"Water depth (m)",
"Extensive",
"Semi-intensive",
"Intensive",
"High density",
"Survival rate (%)",
"Custom unit yield (kg/m³)",
"Water volume = pond area × 666.67 m²/mu × water depth",
"Maximum carrying capacity = water volume × yield per unit volume",
"Recommended stocking count = (maximum carrying capacity × 1000) ÷ target size ÷ survival rate",
"Recommended stocking density = stocking count ÷ pond area (fish/mu)",
"Yield reference by farming mode:",
"Extensive 200-400 kg/mu; semi-intensive 500-800 kg/mu; intensive 1000-1500 kg/mu; high density 1500-2500+ kg/mu (needs aerators plus water exchange).",
"📊 Yield Reference by Farming Mode",
"Unit yield (kg/m³)",
"Yield (kg/mu, 1.5 m depth)",
"Support requirements",
"Low input, low output",
"No or little feeding, relying on natural food",
"Artificial feeding with regular water exchange",
"Aerators, artificial feeding and water-quality monitoring",
"High-density intensive",
"Ultra-high density",
"Multiple aerators, recirculating water and continuous monitoring",
"🐟 Target Market Sizes for Common Species",
"Market size (g)",
"Farming cycle",
"8-12 months",
"6-10 months",
"6-8 months",
"4-6 months",
"90-120 days",
"📚 In-Depth Analysis: Pond Carrying Capacity Estimation",
"Before stocking, estimate the maximum biomass the pond can carry from area, depth and farming mode (extensive / semi-intensive / intensive / high density) to avoid overloading.",
"Set the target market size and survival rate to back-calculate the number of fish to stock, guiding fry purchase.",
"For high-density modes (>2.5 kg/m³), assess the needs for aeration, backup power and water quality.",
"5 mu, 1.5 m deep, semi-intensive, target 1000 g per fish, survival rate 90%",
"With the default parameters: water volume = 5×666.67×1.5 ≈ 5000 m³; at a semi-intensive unit yield of 0.8 kg/m³ the maximum carrying capacity is ≈ 4000 kg; the per-mu yield is ≈ 800 kg/mu; at a 90% survival rate the recommended stocking count is ≈ 4000×1000/(1000×0.9) ≈ 4444 fish,",
"Stocking density",
"≈ 889 fish/mu.",
"How should the unit yield (kg/m³) be chosen?",
"About 0.3 for extensive, 0.8 for semi-intensive, 1.5 for intensive and 3.0 kg/m³ for high density; these are empirical carrying densities, limited in practice by aeration and water-exchange capacity.",
"Why does aeration matter too?",
"The carrying-capacity limit is set jointly by water volume and aeration capacity; a high density beyond the aeration capacity is very prone to oxygen depletion and pond die-off.",
'About "Pond Stocking Capacity Calculator"',
"Pond Stocking Capacity Calculator. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
"Leave blank to use the mode default",
],
'cycle-6': [
"⏱️ Pond Desilting Cycle (Organic Matter)",
"Compute the pond desilting cycle from organic matter accumulation.",
'📖 View the "Pond Desilting Cycle Management Guide"',
"Desilting cycle = f(siltation rate)",
"➕ Add pond record",
"Pond name",
"Area (mu)",
"Water depth (m)",
"Stocking density (fish/mu)",
"Daily feeding rate (%)",
"Last desilting date",
"➕ Add pond",
"🐟 Pond Desilting Management",
"No ponds yet, please add one first",
"📐 Calculation Principle",
"Organic matter accumulation model:",
"1. Daily feed per mu = stocking density × average body weight (assumed 0.5 kg) × feeding rate",
"2. The organic matter residual rate is about 30% (uneaten feed and excretion converted)",
"3. Monthly accumulation = daily feed × 30 × residual rate",
"4. Accumulated concentration = accumulation ÷ (area × depth × 667), in mg/L",
"5. When the concentration exceeds 15 mg/L, desilting is recommended; back-calculate the cycle from this",
"Note: this is a simplified estimation model; in practice judge together with sediment thickness, water temperature, dissolved oxygen and other factors.",
"This tool uses a simplified estimation model; actual desilting decisions should combine sediment thickness tests, water-quality indicators, farmed species and other factors.",
"The organic matter residual rate is assumed to be 30%; in practice it varies widely with feed type, feeding behaviour and water temperature.",
"The 15 mg/L critical concentration is an empirical reference; high-density farming may lower the threshold.",
'After desilting, click "Mark desilted today" to reset the countdown.',
"📚 In-Depth Analysis: Pond Desilting Cycle Management",
"Manage multiple ponds centrally and estimate organic matter accumulation from area, depth, density and feeding rate.",
"Warn on the critical sediment concentration and plan desilting and restocking intervals.",
"Combine the last desilting date to project the next desilting time and risk level.",
"Monthly accounting for a 10-mu intensive pond",
"Taking 10 mu, 2 m deep, 500 fish per mu and a 1% daily feeding rate: daily feed is about 25 kg, the monthly organic matter residue (at 30%) is about 225 kg, the water body is 13340 m³ and the monthly concentration increase is about 16.9 mg/L; at the critical 15 mg/L this reaches the limit in about 27 days, so desilt monthly and strengthen sludge discharge.",
"How is the desilting cycle calculated?",
"Multiply the feed by the residual rate to get the monthly organic matter accumulation, divide by the water volume to get the monthly concentration increase, then use the critical concentration (15 mg/L) to back-calculate the allowed number of months; high-density intensive farming shortens this markedly.",
"What determines the risk level?",
"The ratio of the concentration accumulated since the last desilting to the critical value (15 mg/L): <60% low, 60-90% medium, ≥90% high; a high level calls for immediate desilting or strong sludge discharge.",
'About "Pond Desilting Cycle (Organic Matter)"',
"An aquaculture pond substrate management tool. By entering pond area, water depth, stocking density and feeding rate it estimates the sediment organic matter accumulation rate and concentration increase, computes the recommended desilting cycle, tracks progress since the last desilting and gives three-level low/medium/high risk warnings, helping farmers schedule desilting scientifically and prevent water-quality deterioration.",
"Organic matter accumulation estimate",
"Recommended desilting cycle calculation",
"Three-level risk warning",
"Desilting countdown tracking",
"Accumulation progress visualisation",
"Multi-pond management",
"Fish pond substrate maintenance planning",
"Desilting scheduling for shrimp and crab farming",
"High-density farming risk monitoring",
"Multi-pond farm management",
"e.g. Pond 1",
"e.g. 10",
"e.g. 1.5",
"e.g. 1000",
],
'index': [
"🎣 Fishery & Aquaculture Tools",
"Fishery & Aquaculture",
"Fishery & Aquaculture Tools",
"Enter the water-exchange flow or the volume fraction exchanged each time to compute the residual concentration of pollutants (such as ammonia nitrogen) after the water exchange reaches steady state, the time needed for water quality to stabilise, and the effective exchange rate after accounting for evaporation and top-up, helping farmers set a sensible exchange frequency and sludge discharge plan.",
"Combine transport density, duration, water temperature and aeration method to estimate fry transport survival and suggest a density, reducing transport losses and improving fry survival.",
"Enter the culture water volume, the target dissolved-oxygen gap and the aerator's oxygen-transfer capacity; the tool computes the running time needed, helping aerate on schedule and avoid oxygen depletion and fish gasping at the surface.",
"Enter water temperature and fish size (weight range); the tool looks up the corresponding feeding-rate table and computes the daily feed as a share of body weight, with a detailed reference table for field use.",
"Based on average fish weight, water temperature and farming type, compute the daily feeding rate (as a percentage of body weight) and daily feed amount for scientific feeding and better feed conversion.",
"Enter the cost of fry, feed, water and electricity plus sales revenue; the tool computes total farming cost, net profit, profit margin and ROI to support business decisions.",
"Enter the salinity and volume of seawater and freshwater; the tool computes the mixing ratio to reach a target salinity and also solves the required addition in reverse, for water adjustment and hatching.",
"Enter fish biomass, current water temperature and species; the tool automatically matches a feeding rate to compute the daily feed amount, helping feed precisely and lower the feed conversion ratio.",
"Enter the water volume, current and target overwintering temperatures, the heat-loss coefficient and the covering/insulation method to compute the heating power and continuous heat supply needed to offset heat loss and maintain the overwintering temperature, supporting equipment selection and energy estimates for greenhouses and overwintering ponds.",
"Enter the sediment deposition rate and the allowable silt thickness; the tool computes the desilting cycle, the volume per desilting and a cost estimate, helping plan pond substrate maintenance.",
"Feed Feeding Rate (Percent of Body Weight) Calculator",
"Feed feeding rate (percent of body weight) calculator. Enter the farmed organism's weight, water temperature and feeding rate to compute the daily feed amount and share, for instant conversion in precise feeding and cost control in aquaculture.",
"Enter pond area, average water depth and farming mode; the tool computes the maximum carrying capacity and recommended stocking count, with reference plans for several modes.",
"Enter the water volume and expected carrying capacity; the tool computes the required aeration capacity and recommends the number and model of aerators, avoiding oxygen depletion from under-sized equipment.",
"Enter the geometry of cylindrical, rectangular or frustum-shaped tanks or ponds (radius or side length, depth and so on) to compute the water volume and inner surface area, and estimate the total fish mass the water can safely carry under the stocking density and dissolved-oxygen conditions, for capacity planning of aquariums, ponds and recirculating aquaculture.",
"Overwintering heating power calculator. Enter the culture water volume, target temperature difference and insulation conditions to estimate the heating power needed to maintain the water temperature, for energy planning of aquaculture overwintering sheds and greenhouse ponds.",
"Plankton biomass estimator. Enter the counts and volumes of each group recorded under the microscope to estimate plankton biomass and community structure by standard formulas, for water eutrophication and feed assessment.",
"Enter the fish body length; the tool estimates body weight from an empirical formula and evaluates nutritional status and grade via the condition factor, for growth monitoring.",
"Enter the species, actual water temperature and the drug used; the tool corrects the withdrawal period using a degree-day model, ensuring the drug is fully metabolised before market and safeguarding seafood safety.",
"Analyse farming returns by size-price tiers, combining growth rate and feed cost to find the most profitable market size, supporting sales decisions.",
"Spawning hormone dosage ratio calculator. Enter the broodstock weight and spawning protocol to compute the suitable dose and ratio of spawning hormones (such as PG, HCG and LRH-A), for standardised use in artificial fish breeding.",
"Enter the species and broodstock weight; the tool computes the spawning hormone dose from empirical values and gives a split-injection scheme and response time, supporting artificial breeding operations.",
"Estimate plankton biomass (mg/L) from microscope counts, cell volume and a conversion factor, for water-quality monitoring and eutrophication assessment.",
"Compute the saturated dissolved oxygen of the water from temperature, pressure and salinity, and predict the pre-dawn minimum to warn of oxygen depletion in good time, safeguarding pond farming.",
"Weight multiple environmental factors such as temperature, dissolved oxygen and ammonia nitrogen to grade the risk of fish disease and give specific prevention and medication advice.",
"Enter water-quality parameters such as temperature, dissolved oxygen, pH and ammonia nitrogen; the tool grades the risk of environment-induced fish disease, prompting timely water conditioning and disease prevention.",
"Enter the seafood type and chilled temperature; the tool estimates the shelf life at different temperatures using a Q10 model, guiding cold-chain storage and freshness management.",
"Fry transport survival estimator. Enter transport water temperature, density and duration to estimate fry survival and indicate the best density and temperature range, for optimising fry transport plans.",
"Based on a degree-day model, simulate the development time and life cycle of common fish parasites by water temperature, assess outbreak risk and guide parasite control in farming.",
"Enter the species and growth stage; the tool looks up protein and fat requirement standards and computes the protein-to-fat ratio and digestible energy, guiding compound feed formulation.",
"Compute the share of toxic un-ionised ammonia (NH₃) and the safe threshold from water temperature, pH and chloride, and assess nitrite risk",
"Enter multiple (days of farming, body weight g) data points to fit the specific growth rate SGR and predict growth",
"Mesh size query tool: look up the minimum catchable size by species, or work back from mesh size to the target body length.",
"Choose water temperature and salinity to look up the reference saturated dissolved oxygen under those conditions; the tool interpolates for non-integer temperatures and gives oxygen-depletion warnings by dissolved-oxygen grade, for aerator control and dissolved-oxygen monitoring in aquaculture.",
"Estimate the COD concentration of aquaculture wastewater from the feed amount and discharge volume, and check it against relevant discharge standards, supporting pollution control in aquaculture.",
"Enter the aeration equipment capacity and water volume; the tool recommends a sensible shrimp stocking density (per mu), balancing yield and oxygen-depletion risk to optimise returns.",
"Enter the farmed species and stocking date; the tool estimates the farming cycle from stocking to market and lists feeding and management notes for each growth stage.",
"Shrimp stocking density optimiser. Enter pond area, yield target and size to compute a sensible shrimp stocking density (per mu), balancing unit yield and survival rate, supporting density decisions.",
"Estimate the organic matter accumulation rate from pond area, water depth, stocking density and feeding rate, compute the recommended desilting cycle and track the desilting countdown and water-quality risk level.",
'About "Fishery & Aquaculture Tools"',
"The fishery and aquaculture tool collection brings together 38 free online tools covering common calculation, conversion and lookup needs in fishery and aquaculture scenarios. Whether you are a professional in the field, a student or an ordinary user, you will find ready-to-use practical mini tools here. All tools run fully client-side, upload no data to a server and protect your privacy.",
"The fishery and aquaculture tools on this page include (selected representative tools):",
"These tools help you quickly complete common fishery and aquaculture tasks, with no need to memorise complex formulas or convert by hand; just enter your values and get results.",
"Do the fishery and aquaculture tools require downloading or registration?",
"No. All fishery and aquaculture tools on this page are purely client-side online tools; open the page and use them directly, with no software to install, no account to register and no data uploaded.",
"Are the calculation results accurate? Is my data safe?",
"The tools compute locally in your browser based on public mathematical formulas and common industry standards, with results available instantly. All computation happens on your device, no data is uploaded to a server and your privacy is protected.",
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
        # 坑 28：关联卡片（related-tool）名在 EN 态被 cleanRelatedName() 截断成短形态，
        # 运行时查表键是短形态而非 zh_src 的长形态 ⇒ 此类条目以 zh 为键。
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

#!/usr/bin/env python3
# fishery batch6 (7 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'fishery')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'fishery')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'density-1': [
"🐟 Stocking Density Calculator",
"Enter two parameters to automatically compute the common result.",
'📖 View the "Stocking Density Calculation Guide"',
"Density = number / area",
"Stocking density = total number ÷ area; 1 mu ≈ 666.67 m².",
"Total number (fish)",
"Area (mu)",
"💡 Formula note: density = number ÷ area (fish/mu), convertible to fish/m².",
"📚 In-Depth Analysis: Stocking Density Calculation",
"Plan the total number by area before stocking a new pond",
"Assess whether the current density exceeds the carrying capacity of the water body",
"Recompute the density when splitting or merging ponds",
"Typical",
"stocking density",
"With 1000 fish over an area of 1 mu: stocking density = 1000 / 1 = 1000 fish/mu, about 1.5 fish/m² (1 mu ≈ 666.67 m²). In practice decide it together with species, size and aeration capacity.",
"How is stocking density set?",
"It is jointly determined by the species, target size, water depth, aeration and water-exchange capacity; a higher density raises yield but also risk, and must match the oxygen supply and waste-removal capacity.",
"How do I convert fish/mu and fish/m²?",
"1 mu ≈ 666.67 m², fish/m² = fish/mu ÷ 666.67; for small water bodies (such as tanks) fish/m² is usually more intuitive.",
'About "Shrimp Fry Stocking Density (Fish/mu) Optimizer"',
"Shrimp Fry Stocking Density (Fish/mu) Optimizer. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
"fish",
"mu",
],
'aerator-duration': [
"⏱️ Aerator Runtime Calculator",
"Compute the required runtime from the water volume, the DO deficit and the oxygenation capacity of the aerator.",
'📖 View the "Aerator Runtime Calculation Guide"',
"Aerator runtime = DO deficit / (power × efficiency)",
"Current DO (mg/L)",
"Target DO (mg/L)",
"Aerator power (kW)",
"Oxygenation efficiency (kgO₂/kW·h)",
"Natural oxygen consumption rate (mg/L·h)",
"Basis:",
"Water volume = area × 666.67 × depth (m³); aerator oxygenation rate (mg/L·h) = power × SAE × 1000 ÷ volume; net oxygenation = oxygenation rate - consumption rate; required runtime = (target DO - current DO) ÷ net oxygenation. The SAE of a paddlewheel aerator is typically 1.2-2.0.",
"📚 In-Depth Analysis: Aerator Runtime Calculation",
"Given the water volume and the DO deficit, estimate the required runtime from the net oxygenation rate of the aerator, avoiding blind long running or under-running.",
"Make a quick decision on the supplementary oxygenation time when DO drops sharply after water exchange or medication.",
"Convert by the total net oxygenation rate when several units run in parallel.",
"4000 m³ of water, DO raised from 3 to 5 mg/L, net oxygenation 0.825 mg/L·h",
"Default parameters: DO deficit = 5−3 = 2.00 mg/L; for 4000 m³ the concentration deficit to be made up is 2.00 mg/L; at a net oxygenation rate of 0.825 mg/L·h the estimated runtime is ≈ 2.42 hours (deficit / net rate).",
"How should the net oxygenation rate be understood?",
"It is the effective rate after subtracting the natural oxygen consumption of the water from the oxygen output of the aerator, and is affected in practice by water temperature, air pressure and machine condition.",
"The computed runtime comes out very short/long?",
"Too short means the deficit is small or the machine is powerful; too long means severe hypoxia, calling for several units in parallel or a water exchange first.",
'About "Aerator Runtime Calculator"',
"Aerator Runtime Calculator - computes the runtime needed from the pond water volume, current DO, target DO and aerator efficiency, an online fishery and aquaculture tool. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
],
'water-quality-threshold': [
"📚 Water-Quality Ammonia and Nitrite Safety Threshold Lookup",
"Compute the proportion of toxic un-ionised ammonia (NH₃) and its safety threshold from water temperature, pH and chloride, and assess nitrite risk.",
'📖 View the "Water-Quality Safety Thresholds (Un-ionised Ammonia / Nitrite Nitrogen) Guide"',
"Ammonia / nitrite safety threshold = lookup",
"Chloride Cl⁻ (mg/L)",
"Measured total ammonia nitrogen TAN (mg/L)",
"Measured nitrite NO₂⁻-N (mg/L)",
"🔍 Look up and assess",
"Basis:",
"NH₄⁺ pKa = 9.25 - 0.031 × (T - 25); un-ionised ammonia fraction = 1 / (1 + 10^(pKa - pH)); the NH₃ safety threshold is taken as 0.02 mg/L, from which the TAN safety limit is back-calculated. The nitrite safety limit is estimated from a Cl⁻/NO₂⁻-N molar ratio ≥30: NO₂⁻-N ≤ Cl⁻ × 0.0132.",
"📚 In-Depth Analysis: Water-Quality Safety Thresholds (Un-ionised Ammonia / Nitrite Nitrogen)",
"Ammonia toxicity assessment and re-checking water quality after feeding",
"Monitoring during the sensitive fry stage and the midnight hypoxia period",
"Quantitative verification of the effect of water and substrate conditioning",
"Toxicity conversion at 26℃ and pH 8",
"At a water temperature of 26℃ and pH 8, NH₄⁺ pKa ≈ 9.219 and the un-ionised ammonia fraction is about 5.70%; a measured TAN of 0.8 mg/L gives toxic NH₃ of 0.0456 mg/L (228% of the 0.35 mg/L safety limit, near the threshold) and NO₂⁻-N of 0.1 mg/L (38% of the 0.26 mg/L limit, safe).",
"Why is un-ionised ammonia more toxic?",
"Un-ionised ammonia (NH₃) readily crosses the gill membrane into the blood and is far more toxic than the ammonium ion (NH₄⁺); its fraction rises markedly with higher pH and temperature.",
"What is the role of pKa here?",
"pKa determines the NH₄⁺ ⇌ NH₃ + H⁺ equilibrium; from pKa and pH you can compute the share of un-ionised ammonia in total ammonia, which is central to the toxicity assessment.",
'About "Water-Quality Ammonia and Nitrite Safety Threshold Lookup"',
"Water-Quality Ammonia and Nitrite Safety Threshold Lookup - computes un-ionised ammonia and nitrite safety thresholds from water temperature, pH and chloride, an online fishery and aquaculture tool. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
],
'wastewater-cod': [
"🐟 Aquaculture Effluent COD Estimator",
"Estimate the COD concentration of aquaculture effluent from the feed amount and discharge volume and compare it with the discharge standard.",
'📖 View the "Aquaculture Effluent COD Estimation Guide"',
"COD estimate = feed × discharge coefficient",
"Average daily feed amount (kg/day)",
"Average daily discharge volume (m³/day)",
"COD generation coefficient (kgCOD/kg feed)",
"Discharge standard (mg/L)",
"Basis:",
"Each kilogram of feed produces about 0.3-0.4 kg of COD (uneaten feed + faeces, adjustable by coefficient); COD load = feed amount × COD coefficient; concentration = load ÷ discharge volume. Compare with standards such as the Requirements for Water Discharge from Freshwater Pond Aquaculture (COD limit about 30 mg/L) to assess compliance.",
"📚 In-Depth Analysis: Aquaculture Effluent COD Estimation",
"Self-check whether COD exceeds the limit before discharge",
"Selecting treatment process load and a compliance scheme",
"Accounting for dilution water volume and emission reduction",
"Discharge accounting for 50 kg of feed per day",
"A daily feed amount of 50 kg (COD generation coefficient 0.35) gives a COD load of 17.5 kg/day; a discharge of 200 m³/day gives an estimated COD of 87.5 mg/L, 2.92 times the 30 mg/L standard, requiring treatment or about 383 m³ of extra dilution water to comply.",
"What is the COD standard for aquaculture effluent?",
"Common freshwater aquaculture discharge requirements set COD at no more than 30 mg/L (Grade I), subject to the local discharge standard; exceeding it requires treatment or dilution before discharge.",
"How can COD be reduced?",
"Reduce feed at source to control leftovers, add sedimentation/ecological ponds/aerated biological treatment, or recirculate the tail water; the key is less feed residue and better water exchange.",
'About "Aquaculture Effluent COD Estimator"',
"Aquaculture Effluent COD Estimator - estimates the COD concentration of aquaculture effluent from the feed amount, feed coefficient and discharge volume, an online fishery and aquaculture tool. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
],
'pond-desilting': [
"⏱️ Pond Desilting Cycle Calculator",
"Compute the desilting cycle, volume and cost estimate from the silt deposition rate and the allowed thickness.",
'📖 View the "Pond Desilting Cycle and Cost Estimation Guide"',
"Desilting cycle = accumulation / removal rate",
"Annual deposition rate (cm/year)",
"Allowed silt thickness (cm)",
"Current silt thickness (cm)",
"Desilting unit price (CNY/m³)",
"Basis:",
"Remaining deposit thickness = allowed thickness - current thickness; desilting cycle = remaining thickness ÷ annual deposition rate. Desilting volume = area × 666.67 × (current silt thickness + new deposit within the cycle)/100 converted to m³. Silt that is too thick spoils water quality and breeds pathogens, so desilt before the cycle ends.",
"📚 In-Depth Analysis: Pond Desilting Cycle and Cost Estimation",
"Annual aquaculture facility maintenance and budget planning",
"Estimate the next desilting time from the silt deposition rate",
"Desilting workload and cost estimation",
"Desilting estimate for a typical intensive pond",
"Current silt 8 cm, allowed upper limit 20 cm and a deposition rate of 3 cm/year: 12 cm remains, so desilting is needed in about 4.0 years; the desilting volume at that time is about 667 m³ and the cost about 10000 CNY.",
"What harm does silt do?",
"Silt that is too thick keeps releasing toxic substances such as ammonia nitrogen and hydrogen sulphide, consumes oxygen and breeds pathogens, and a rainstorm that stirs up the bottom easily causes a pond turnover, so its thickness must be controlled and desilting done regularly.",
"How thick should silt be before desilting?",
"For typical intensive ponds silt is best kept below 15-20 cm; beyond that both toxicity and oxygen consumption rise markedly, so arrange desilting or in-place rotary tillage and oxidation.",
'About "Pond Desilting Cycle Calculator"',
"Pond Desilting Cycle Calculator - computes the desilting cycle and volume from the deposition rate and allowed silt thickness, an online fishery and aquaculture tool. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
],
'mesh-size-guide': [
"📚 Fishing Mesh Size and Minimum Catchable Size Lookup",
"Cross-reference mesh size with the minimum catchable length/weight, with selectivity and size estimation for common fish.",
'📖 View the "Fishing Mesh Size Lookup Guide"',
"Mesh size = minimum catchable size",
"Find minimum size by mesh",
"Find mesh by target size",
"Mesh size (mm)",
"Target minimum body length (cm)",
"Basis:",
"Gillnet selectivity L50 ≈ k × mesh, where k is the body-length/mesh coefficient (about 0.45-0.55 for cyprinids); body weight is converted from body length via the length-weight relationship W = aLᵇ. The data are empirical references and in practice depend on the gear type and regulations.",
"📚 In-Depth Analysis: Net Mesh Size Selection (Catchable Size L50)",
"Choose the mesh size from the target catch size so that fish smaller than that size pass through the mesh and are retained selectively.",
"Use the length-weight relationship W = a·Lᵇ to estimate the catchable weight from the catchable length L50 corresponding to the mesh.",
"Balance production needs and resource conservation, avoiding the capture of excessively small individuals.",
"Catchable size accounting for a carp mesh of 50 mm",
"Default parameters: a mesh of 50 mm corresponds to a catchable length L50 ≈ 2.5 cm; by the carp length-weight relationship W = 0.0223·L^3.01 (L in cm), 2.5 cm corresponds to a weight of about 0 g (a juvenile, showing that this mesh catches adults while juveniles escape). In practice the mesh should be chosen so that L50 is close to about half the target market size.",
"What is L50?",
"The body length at which half escape and half are retained, the core parameter of gear selectivity: the larger the mesh, the larger L50 and the more easily small individuals escape.",
"How are the parameters a and b obtained?",
"They come from the length-weight regression for that species; they differ greatly between species, and the empirical values for the corresponding species should be used to improve estimation accuracy.",
'About "Fishing Mesh Size and Minimum Catchable Size Lookup"',
"Fishing Mesh Size and Minimum Catchable Size Lookup - looks up the minimum catchable length and weight for a mesh size, or the mesh for a target size, an online fishery and aquaculture tool. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
],
'calc-power': [
"⚡ Electrical Power Calculator",
"Enter voltage and current to compute the electrical power (P = V × I).",
'📖 View the "Electrical Power Calculation Guide"',
"Electrical power equals the product of voltage and current; 1 kW = 1000 W.",
"💡 Formula note: power P = V × I (W), divide by 1000 for kW.",
"📚 In-Depth Analysis: Electrical Power Calculation",
"Farmers estimate the ",
"electrical power",
" and electricity cost of equipment such as aerators and water pumps",
"Check whether the nameplate voltage/current matches the line capacity",
"Total power accounting when several devices run at the same time",
"Aerator power accounting",
"With an input of 220 V and 10 A: power P = 220 × 10 = 2200 W = 2.2 kW. Note that 1 kW = 1000 W; when selecting cables and earth-leakage protection leave enough margin for the power.",
"How is power calculated?",
"For DC or purely resistive loads power P = voltage × current; induction motors and similar have a ",
", the actual input power is slightly higher, and for a rough estimate you can first round P=V×I.",
"Why leave a margin?",
"The starting current is often several times the rated value, and several devices together easily overload the line; switches, cables and generators should be selected at 1.2-1.5 times the total power.",
'About "Overwinter Insulation (Heating Power) Calculation"',
"Overwinter Insulation (Heating Power) Calculation. A fishery and aquaculture tool that helps calculate farming parameters and yields.",
"Voltage (V)",
"Current (A)",
],
}

# term-link nodes missed by extract: zh -> en
EXTRA = {
'calc-power': {'功率因数': 'Power Factor'},
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
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('!! %s EXTRA CJK/CNP violation: %s' % (slug, en[:60]))
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

#!/usr/bin/env python3
# geology batch1 (5 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'geology')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'geology')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'dizhibianlujilubiao': [
"🪨 Geological Logging Record Sheet",
"Enter borehole layer information to generate a standardised geological logging record, with multi-layer accumulation and export.",
'📖 View the "Geological Logging Record Sheet Guide"',
"Logging parameter = layer computation",
"Hole No.",
"Run",
"Start depth (m)",
"End depth (m)",
"Lithology name",
"Structure and texture",
"Lithology description",
"The rock is strongly weathered; feldspar is largely kaolinised, quartz grains are loose, a little biotite remains, and the sample crumbles easily when squeezed by hand.",
"🧮 Generate log",
"➕ Add layer",
"💡 Layer thickness = end depth − start depth; the generated record contains the standard logging fields of hole No., run, layer, lithology and description.",
"Layer depths should be continuous, avoiding overlap or omission",
"The lithology description should include colour, mineral composition, structure and texture, and weathering degree",
"After adding layers you can one-click copy the complete logging table",
"Logging data is stored locally in the browser and is not uploaded to a server",
"🗂️ Logged layers",
"No layer records yet",
"📚 In-Depth Analysis: Borehole Geological Logging Record Sheet Generation",
"Layer logging: enter the start/end depth, lithology, colour and structure of each run and the layer thickness is computed automatically",
"Record archiving: multiple layers accumulate into a standardised logging table, exported for survey reports",
"On-site check: verify in real time whether the sum of layer thicknesses matches the drilling footage",
"Algorithm: single-layer thickness = end depth dTo − start depth dFrom (requires dTo ≥ dFrom); enter the hole No., run, lithology, colour, structure and description for each run, and the tool accumulates them into a layer table, automatically producing a standardised record of hole No. / start-end depth / thickness / lithology / colour / structure / description, which can be copied or exported (depth accurate to 0.01 m).",
"Example: hole No. ZK101, run 3, dFrom=12.50 m, dTo=15.80 m, lithology=strongly weathered granite → layer thickness = 15.80 − 12.50 = 3.30 m, the record containing colour \"grey-yellow brown\" and structure \"medium-grained, massive\". After entering several layers, copy a tab-separated layer summary for easy pasting into Excel or a report.",
"Must the sum of layer thicknesses equal the drilling footage?",
"In principle the sum of the layer thicknesses of each run should equal that run's footage; a gap or overlap indicates a missing record or a wrong depth entry that must be corrected on site, otherwise the resource estimate and section continuity are affected.",
"Can the logging table serve directly as a survey report?",
"The logging table is raw data; the report also needs core photographs, sampling positions, test results and integrated interpretation. This tool only standardises the record format and thickness calculation and draws no geological conclusions.",
'About "Geological Logging Record Sheet"',
"A geological logging record generator: enter the hole No., run, layer depth, lithology and description to automatically produce the layer thickness and a standardised logging format; multiple layers can be accumulated into a logging table and one-click copied as tab-separated text.",
"Automatically computes layer thickness",
"Multi-layer accumulation with per-row deletion",
"One-click copy of a tab-separated logging table, easy to paste into Excel",
"Logging data stored locally in the browser",
"Core borehole geological logging",
"Trench/pit logging compilation",
"Digitisation of raw exploration data",
"Compilation of appendix tables for geological reports",
"Hole No.",
"Run",
"Start depth",
"End depth",
"Lithology name",
"Colour",
"Structure and texture",
"Lithology description",
],
'weight-sample': [
"📡 Sample Representativeness Calculator",
"Based on the Gy sampling formula: enter particle size, sample mass and target grade to compute the relative sampling error and the minimum representative sample mass.",
'📖 View the "Gy Sampling Formula Representativeness (Minimum Sample Mass / Relative Error) Guide"',
"σ² = C · d³ · (1/w − 1) / m; enrichment factor (1/w − 1) = (1 − w) / w; σ_rel = √σ²; m_min = C · d³ · (1/w − 1) / (tol_rel)²",
"According to Gy sampling theory the relative sampling variance is proportional to the cube of the particle size d and inversely proportional to the sample mass m (d in cm, m in g, w the target grade as a decimal, C the sampling constant); when the relative error σ_rel exceeds the allowed value tol, the minimum sample mass is back-calculated from m_min.",
"Maximum particle size d (mm)",
"Sample mass m (kg)",
"Target component grade w (%)",
"Material type (sampling constant C)",
"Precious-metal ore (Au/Ag, C=0.1)",
"Non-ferrous metal ore (Cu/Pb/Zn, C=0.25)",
"General ore/soil (C=0.5)",
"Iron ore/uniform material (C=1.0)",
"Coal/organic matter (C=0.05)",
"Custom sampling constant C",
"Allowed relative error (%)",
"💡 Gy formula: relative sampling variance σ²=C·d³·(1/w−1)/m; relative error σ_rel=√σ²; minimum sample mass m_min=C·d³·(1/w−1)/σ²_tol. d in cm, m in g.",
"The Gy formula applies to representativeness assessment of particulate-material sampling",
"The sampling constant C depends on mineral density and grade distribution; this tool provides typical reference values",
"The particle size d is the sieve aperture through which 95% of the material passes",
"The grade w is the mass fraction of the target component (entered in %, converted internally to a decimal)",
"Results are for reference only; an actual sampling plan must follow the standards and site conditions",
"📚 In-Depth Analysis: Gy Sampling Formula Representativeness (Minimum Sample Mass / Relative Error)",
"Mass calculation: compute the minimum representative sample mass from particle size, grade and allowed error, and judge whether the current mass is sufficient",
"Error assessment: give the relative sampling error σ_rel and an error grade (excellent to poor)",
"Plan optimisation: recompute m_min when the particle size increases or the requirement tightens, guiding the crushing-and-splitting process",
"Formula (Gy): relative variance σ²=C·d³·(1/w−1)/m, d the maximum particle size (cm), w the target grade (decimal), m the sample mass (g), C the material constant (commonly 0.5 for metal ores). Relative error σ_rel=√(σ²)×100%; minimum sample mass m_min=C·d³·(1/w−1)/(allowed relative error)². Computed locally, with unit conversion d (mm→/10), m (kg→×1000 g).",
"Example: d=2 mm (0.2 cm), m=5 kg (5000 g), w=1.5%, allowed error 10%, C=0.5 → σ²=0.5×0.2³×65.667/5000=5.253×10⁻⁵, σ_rel=0.725% (excellent), m_min=26.27 g (0.0263 kg); the current 5000 g is 190.4 times the minimum sample mass, so representativeness is satisfied.",
"Why does a larger particle size require a larger sample?",
"In the Gy formula m_min∝d³, so a larger particle size requires the sample mass to grow with the cube to keep the same error. Sampling must therefore be followed by stage-wise crushing and splitting rather than taking one large sample, otherwise the fine fraction is over-represented.",
"Is an error of 0.725% too conservative?",
"The relative error depends on the ratio of sample mass to particle size. The current 5 kg far exceeds the minimum sample mass, so the error is very small; taking only 20 g would raise σ_rel to about 11% (the lower bound of good). Relaxing the allowed error markedly reduces the required mass.",
'About "Sample Representativeness Calculator"',
"A representativeness assessment tool based on Pierre Gy's sampling theory: enter the maximum particle size, sample mass, target component grade and sampling constant to compute the relative sampling error, absolute error and the minimum sample mass that meets the representativeness requirement, and judge whether the current sampling plan is representative.",
"Built-in sampling constants for typical materials such as precious-metal, non-ferrous and general ores",
"Outputs relative error, absolute error and minimum sample mass together",
"Automatically assesses whether sampling representativeness is met and gives adjustment advice",
"Supports a custom sampling constant C for special materials",
"Fully client-side computation; sampling data is not uploaded",
"Mine sampling plan design and sample mass determination",
"Representativeness assessment of geochemical exploration samples",
"Verification of sampling representativeness at ore-dressing plants",
"Analysis of ore grade fluctuation and sampling error",
"Maximum particle size",
"Sample mass",
"Target component grade",
"Custom C value",
"Allowed relative error",
],
'wutanyichangjieyi': [
"🪨 Geophysical Anomaly Interpretation",
"Enter the anomaly amplitude, half-width and gradient to infer the likely geological body from the morphological characteristics.",
'📖 View the "Geophysical Anomaly Interpretation Guide"',
"Estimated burial depth ≈ anomaly half-width W / 1.31 (Peters half-width method)",
"A magnetic anomaly amplitude > 500 nT is high, > 100 nT medium; a gravity anomaly > 5 mGal is high, > 1 mGal medium; combined with half-width (> 200 m large) and gradient grading, the type and depth of the geological body are interpreted.",
"Anomaly type",
"Magnetic anomaly (nT)",
"Gravity anomaly (mGal)",
"Anomaly amplitude A",
"Anomaly half-width W (m)",
"Maximum gradient G",
"🧮 Interpret",
"💡 The burial depth and size of the geological body are inferred from amplitude strength, extent and gradient steepness; the gradient G=ΔA/Δx reflects the lateral rate of change of the anomaly.",
"The interpretation is qualitative and must be verified against geological data",
"A high-amplitude magnetic anomaly usually corresponds to a magnetic ore body or rock mass",
"A gravity high often corresponds to a dense rock mass or metal mineralisation",
"Actual interpretation should include quantitative inversion",
"🕘 Recent interpretations",
"No interpretation records yet",
"📚 In-Depth Analysis: Geophysical Anomaly Morphology Interpretation and Depth Estimation (Peters Method)",
"Morphology grading: judge the anomaly characteristics from amplitude, half-width and gradient (high/medium/low amplitude, large/medium/small extent, steep/gentle gradient)",
"Depth estimation: use the Peters half-width method depth ≈ half-width / 1.31 to estimate the burial depth of the top of the magnetic/density body",
"Target screening: give a likely geological-body inference with a confidence level, aiding prospecting and further engineering layout",
"Interpretation logic: amplitude thresholds are set by anomaly type (magnetic >500 nT high, >100 medium; gravity >5 mGal high, >1 medium), half-width >200 m large, 50-200 medium, <50 small, and gradient >5 steep. Depth ≈ half-width W / 1.31 (Peters half-width method, suitable for near-equidimensional magnetic bodies). Computed locally; the ambiguity must be resolved with geology.",
"Example: magnetic anomaly A=500 nT, half-width W=80 m, gradient=6 → medium amplitude, medium extent, steep gradient; depth ≈80/1.31=61.07 m (medium depth). With medium amplitude and 50<W≤200, it is inferred to be a medium-scale dyke/contact zone (medium confidence); verify with a geological section and a small amount of drilling.",
"Is the Peters-method depth accurate?",
"It is accurate only for near-equidimensional magnetic bodies of simple attitude and without interference, and it often overestimates (because the background and superposition are not removed). The true depth should come from inversion or quantitative section interpretation; this estimate is only a preliminary ranking and is for reference.",
"Does an anomaly always correspond to an ore body?",
"Not necessarily. Magnetic/density anomalies also come from rock masses, structures or interference. Surface interference must be excluded and the host rock and alteration considered; low-confidence inferences need particular care to avoid the misjudgement of \"ore at every anomaly\".",
'About "Geophysical Anomaly Interpretation"',
"A qualitative geophysical anomaly interpretation tool: from morphological characteristics such as anomaly amplitude, half-width and gradient, infer the likely type and depth of the geological body and give an ambiguous inference with a confidence level, aiding the interpretation of geophysical results.",
"Dual mode for magnetic and gravity anomalies",
"Automatic feature grading and depth estimation",
"Ambiguous inference with labelled confidence",
"Fully client-side inference; data processed locally",
"Preliminary qualitative interpretation of geophysical anomalies",
"Anomaly screening and target delineation",
"Reference for prospecting prediction and drilling deployment",
"Geophysical teaching and case demonstration",
"Anomaly type",
"Anomaly amplitude",
"Anomaly half-width",
"Maximum gradient",
],
'shuiwendizhishentoushiyan': [
"🪨 Hydrogeological Permeability Test",
"Compute the aquifer permeability coefficient K from the Dupuit steady-flow formula for a fully penetrating well",
'📖 View the "Dupuit Fully Penetrating Well Pumping Test Permeability K Guide"',
"Permeability coefficient k = Q/(A·i)",
"Aquifer type",
"Confined aquifer, fully penetrating well",
"Unconfined aquifer, fully penetrating well",
"Pumping rate Q (m³/d)",
"Drawdown s (m)",
"Well radius r₀ (m)",
"Aquifer thickness M (m)",
"Radius of influence R (m)",
"💡 Confined fully penetrating well: K = Q·ln(R/r₀)/(2π·M·s); unconfined fully penetrating well: K = 2Q·ln(R/r₀)/(π·(2H−s)·s).",
"Applies to steady-flow pumping tests in fully penetrating wells",
"The radius of influence R can be estimated by the empirical formula R=2s√(HK)",
"For an unconfined aquifer the drawdown s should be less than the aquifer thickness H",
"Partially penetrating wells or leaky recharge require other formulas",
"📚 In-Depth Analysis: Dupuit Fully Penetrating Well Pumping Test Permeability K",
"Confined well: use the confined fully penetrating well formula to find K from the pumping rate, drawdown and radius of influence",
"Unconfined well: use the unconfined fully penetrating well formula (accounting for (2H−s)) to find K",
"Water-yield grading: classify the aquifer by K as weakly/medium/strongly/very strongly permeable and evaluate its water-transmitting capacity",
"Formula: confined fully penetrating well K = Q·ln(R/r₀) / (2π·M·s); unconfined fully penetrating well K = 2Q·ln(R/r₀) / (π·(2H−s)·s). Here Q is the pumping rate (m³/d), s the drawdown (m), r₀ the well radius (m), M (confined) or H (unconfined) the aquifer thickness (m), R the radius of influence (m). cm/s = K(m/d)/86400×100 (computed locally; requires R>r₀, s>0).",
"Example: confined fully penetrating well Q=500 m³/d, s=3 m, r₀=0.15 m, M=20 m, R=200 m → ln(200/0.15)=7.195, K=500×7.195/(2π×20×3)=9.543 m/d (≈0.01105 cm/s), specific capacity = Q/s = 166.67 m³/d/m, strongly permeable.",
"How is the radius of influence R chosen?",
"It can be back-calculated from the drawdown measured at observation wells, or estimated by an empirical formula (such as Kusakin R=2s√K·H). A biased R directly affects K, so at least one observation well is recommended rather than applying an empirical value directly.",
"Why does the unconfined-well formula contain (2H−s)?",
"Integrating the Dupuit assumption for an unconfined fully penetrating well gives a flow proportional to (2H−s)·s, where H is the aquifer thickness and s the drawdown; when s approaches H the formula fails and a partially penetrating well or numerical method must be used.",
'About "Hydrogeological Permeability Test"',
"Based on the Dupuit steady well-flow formula, compute the aquifer permeability coefficient K from pumping-test data; supports both confined and unconfined fully penetrating wells and automatically converts m/d and cm/s units and derives the permeability grade.",
"Dual formulas for confined/unconfined fully penetrating wells",
"Outputs both m/d and cm/s units",
"Automatically determines the permeability grade",
"Fully client-side computation; pumping data processed locally",
"Permeability coefficient from pumping tests",
"Water-supply hydrogeological survey",
"Reference for foundation-pit dewatering design",
"Hydrogeology teaching demonstration",
"Aquifer type",
"Pumping rate",
"Drawdown",
"Well radius",
"Aquifer thickness",
"Radius of influence",
],
'dizhiyijipinggu': [
"📋 Geological Relic Assessment",
"Enter the relic type, scale, integrity and scientific value to comprehensively assess the protection grade of a geological relic.",
'📖 View the "Geological Relic Assessment Guide"',
"Composite score = type score × 0.3 + scale score × 0.2 + integrity score × 0.2 + scientific-value score × 0.3",
"The scale score is graded by area (> 10 km² scores 5, > 1 km² scores 4, > 0.1 km² scores 3, otherwise 2), the integrity score = integrity / 20, and the scientific-value score ranges 0-5; a total ≥ 4.2 is Grade I (national protection), decreasing to Grade V.",
"Relic type",
"Palaeontological fossils (important)",
"Geological section/structural relic",
"Landform landscape",
"Mineral/rock locality",
"Geological hazard relic",
"Scale (km²)",
"Integrity (%)",
"Scientific value (1-5)",
"💡 Weighted scoring: type (0.3) + scale (0.2) + integrity (0.2) + scientific value (0.3); after normalisation a five-level protection grade is assigned.",
"The assessment is a comprehensive quantitative method; actual grading requires expert review",
"Scientific value covers typicality, rarity and representativeness",
"Scale covers the distribution extent and volume of the relic",
"Protection grades follow the Provisions on the Administration of Geological Relic Protection",
"📚 In-Depth Analysis: Composite Scoring of Geological Relic Protection Grades (National to Ordinary, Five Levels)",
"Application pre-assessment: enter the relic type, scale, integrity and scientific value to preliminarily judge which protection level (national/provincial/municipal/county) it could apply for",
"Comparative ranking: rank several candidate sites in the same area by composite score and prioritise the high-scoring ones for application",
"Science-popularisation filing: write the score and grade into the geopark/science-base archive to support protection planning",
"Algorithm: composite score = type score×0.3 + scale score×0.2 + integrity score×0.2 + scientific-value score×0.3. The scale score is graded by area (>10→5, >1→4, >0.1→3, otherwise 2), the integrity score = integrity%/20, and the scientific-value score ranges 0-5. Grades: ≥4.2 Grade I national, ≥3.6 Grade II provincial, ≥2.8 Grade III municipal, ≥2.0 Grade IV county, otherwise Grade V ordinary (computed locally, not uploaded).",
"Example: a palaeontological fossil site with type score=5, scale=2.5 km² (tier 4), integrity=80% (score 4), scientific value=4 → composite = 5×0.3+4×0.2+4×0.2+4×0.3=4.30, reaching ≥4.2 → Grade I national protection; apply as a national geopark.",
"How is the type score determined?",
"The type score is determined by the relic category (such as stratigraphic section, palaeontological fossil, landform landscape), with a value 1-5 representing scientific representativeness from weak to strong, according to the category scoring table in the industry technical requirements for relic surveys. This tool takes the input value directly; the application must attach the classification basis.",
"Does a high composite score guarantee approval?",
"The score is a pre-screening reference; formal protected-area approval also requires expert review, public participation and planning alignment. A low score (such as below 2.8) indicates insufficient representativeness, so it is better to improve protection first or shift to ordinary protection with rational use rather than forcing an application.",
'About "Geological Relic Assessment"',
"A geological relic protection-grade assessment tool: weighted scoring by relic type, scale, integrity and scientific value, outputting a composite score and a five-level protection grade (national to ordinary) with protection advice.",
"Four-factor weighted scoring model",
"Automatic five-level protection grading",
"Graded protection advice",
"Fully client-side assessment; data processed locally",
"Geopark application and grading",
"Geological relic protection zoning",
"Tourism geological resource evaluation",
"Geological relic protection planning",
"Relic type",
"Scale",
"Integrity",
"Scientific value",
],
}

# term-link nodes missed by extract: zh -> en
EXTRA = {
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
    out = {'slug': slug, 'industry': 'geology', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

for slug, en_list in EN.items():
    write(slug, build(slug, en_list))

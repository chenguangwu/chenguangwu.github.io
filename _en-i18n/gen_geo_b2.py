#!/usr/bin/env python3
# geology batch2 (5 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'geology')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'geology')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'tester-16': [
"📝 Rock Mechanics Parameter Calculator",
"Compute rock parameters such as uniaxial compressive strength (mechanical), dry density (physical), water absorption and softening coefficient (hydraulic): enter the test data and the tool calculates automatically and gives a rock quality assessment.",
"Rock (mechanical/physical/hydraulic) Testing",
"/ Rock (mechanical/physical/hydraulic) Testing",
'📖 View the "Rock Mechanics Three Parameters (Compressive/Density/Softening) Calculation Guide"',
"Rock mechanics parameters = strength/deformation computation",
"Uniaxial compressive strength",
"Density and water absorption",
"Softening coefficient",
"Failure load P (kN)",
"Specimen diameter d (mm)",
"Dry mass m₁ (g)",
"Saturated mass m₂ (g)",
"Buoyant mass m₃ (g, weighed in water)",
"Dry density ρd = m₁/(m₂-m₃)×ρw; water absorption Wa = (m₂-m₁)/m₁×100%",
"Dry compressive strength σcd (MPa)",
"Saturated compressive strength σcw (MPa)",
"Softening coefficient K = σcw / σcd; K<0.75 indicates a softening rock",
"Calculate and assess",
"Uniaxial compressive strength: σc = P/A, where A is the loaded area; a height-to-diameter ratio of 2:1 is recommended",
"Dry density by the water-weighing method: ρd = m₁/(m₂-m₃)×ρw (ρw=1.0 g/cm³)",
"Water absorption reflects rock porosity; Wa<1% generally indicates a dense rock",
"K<0.75 indicates a softening rock (strength drops markedly on wetting) and needs particular attention in engineering",
"📚 In-Depth Analysis: Rock Mechanics Three Parameters (Compressive/Density/Softening) Calculation",
"Compressive strength: compute the uniaxial compressive strength σc from the failure load and specimen diameter and classify the hardness",
"Physical parameters: compute dry density, saturated density and water absorption from the dry/saturated/wet masses to assess the pore characteristics",
"Hydraulic parameters: compute the softening coefficient from the dry/saturated compressive strengths to judge the strength reduction on wetting",
"Formula: ① uniaxial compressive σc=P×1000/A, A=πd²/4 (P the failure load in N, d the diameter in mm, σc in MPa); hardness grading σc≥120 hard, 60-120 fairly hard, 30-60 fairly soft, 5-30 soft, <5 very soft. ② dry density ρd=md/(ms−mw), water absorption Wa=(ms−md)/md×100% (md dry mass, ms saturated mass, mw wet mass, in g). ③ softening coefficient K=σcw/σcd (computed locally, units unified to g and mm).",
"Example: P=120 kN, d=50 mm → A=1963.5 mm², σc=120000/1963.5=61.11 MPa (fairly hard rock); md=250, ms=255, mw=158 → ρd=2.577 g/cm³, ρs=2.629 g/cm³, Wa=2.00% (medium porosity); dry/saturated compressive cd=85, cw=55 → K=0.647 (weak softening, strength reduced by about 35.3% on wetting).",
"Below what softening coefficient is a rock unusable?",
"Generally K<0.75 is treated as a softening rock; in water-saturated environments such as hydraulic engineering the design must use the saturated strength. K≥0.75 indicates good water resistance. The exact threshold depends on the project type and code (such as dam foundations and slopes); results are for reference.",
"Does the specimen diameter affect σc?",
"σc is normalised by A=πd²/4, so in theory it is independent of diameter; however the height-to-diameter ratio must meet the code (usually ≥2), otherwise end effects make it low. This tool only computes the strength; shape correction must follow the test code.",
'About "Rock Mechanics Parameter Calculator"',
"A rock mechanics parameter calculator supporting the computation and assessment of three common rock test parameters: uniaxial compressive strength (mechanical), dry density and water absorption (physical), and softening coefficient (hydraulic).",
"Uniaxial compressive strength calculation and hardness classification",
"Dry/saturated density and water absorption by the water-weighing method",
"Softening coefficient calculation and water-resistance assessment",
"Geotechnical laboratory data processing",
"Rock parameter calculation for engineering geological surveys",
"Rock mechanics teaching experiment",
"Aid for rock mass quality classification",
],
'soil-sample': [
"📡 Geochemical Sampling Design",
"Enter the survey area and sampling density to compute the number of sampling points, the grid spacing and a workload estimate.",
'📖 View the "Geochemical Sampling Design Guide"',
"Sampling design = grid layout",
"Survey area A (km²)",
"Sampling density D (points/km²)",
"Sampling scale",
"1:50000 (1-2 points/km²)",
"1:25000 (4-8 points/km²)",
"1:10000 (25-50 points/km²)",
"1:5000 (100 points/km²)",
"Cost per point (CNY)",
"💡 Formula: number of sampling points N = A × D; grid spacing (square grid) L = √(1/D)×1000 (m); line spacing = point spacing = L.",
"For 1:50,000 geochemical reconnaissance, a density of 1-2 points/km² is common",
"For 1:25,000 detailed survey, a density of 4-8 points/km² is typical",
"The grid spacing assumes a square grid; for a rectangular grid the line and point spacings may differ",
"Actual point placement must also consider transport and terrain accessibility",
"📚 In-Depth Analysis: Regional Geochemical Sampling Point Count and Grid Spacing Design",
"Point estimate: derive the total number of sampling points and the grid spacing from the survey area and sampling density",
"Option comparison: adjust the density (such as 1/4/16 points/km²) to compare cost and precision",
"Budgeting: multiply by the per-point cost to obtain the total workload and a budget estimate",
"Algorithm: number of points N = area A (km²) × density D (points/km²); grid spacing L = √(1/D)×1000 (m); estimated cost = N × cost per point (CNY). Line spacing ≈ point spacing ≈ L, and a uniform grid covers A km² (computed locally; D>0, A≥0).",
"Example: survey area A=20 km², density D=4 points/km², cost per point 80 CNY → N=20×4=80 points, grid spacing=√(1/4)×1000=500 m, estimated cost=80×80=6400 CNY, with line and point spacing both about 500 m covering 20 km².",
"What is the relationship between grid spacing and density?",
"For a uniform square grid L=√A/N=√(1/D), so a higher density gives a smaller spacing. D=4 points/km² corresponds to a 500 m grid and D=16 to a 250 m grid; precision improves but the cost is about four times.",
"How is a non-uniform grid (line spacing ≠ point spacing) handled?",
"When line spacing × point spacing = 1/D in area, N=A×D still holds, and the two spacings are taken separately. Stream-sediment surveys often use a linear grid, with the line spacing set by the code and the points laid along each line.",
'About "Geochemical Sampling Design"',
"A geochemical sampling layout design tool: from the survey area and sampling density, compute the number of sampling points, the square-grid spacing and the workload cost, with built-in densities for common scales, easing reconnaissance and detailed survey design.",
"One-click conversion of point count, grid spacing and cost",
"Built-in densities for common scales from 1:50,000 to 1:5,000",
"Supports custom density and cost per point",
"Fully client-side computation; design parameters stored locally",
"Regional geochemical reconnaissance design",
"Detailed geochemical survey layout in mining areas",
"Sampling workload and budget estimation",
"Compilation of exploration implementation plans",
"Survey area",
"Sampling density",
"Sampling scale",
"Cost per point",
],
'hazard': [
"📋 Geological Hazard Risk Assessment",
"Enter slope angle, lithology, rainfall and slope height to comprehensively assess the hazard grade of geohazards such as landslides and collapses.",
'📖 View the "Geological Hazard Risk Assessment Guide"',
"Geological hazard risk = f(slope, lithology, rainfall)",
"Slope angle (°)",
"Slope height (m)",
"Daily rainfall (mm)",
"Lithology type",
"Hard rock (granite/limestone)",
"Fairly hard rock (sandstone/metamorphic)",
"Soft rock (mudstone/shale)",
"Loose deposit (colluvial/residual)",
"Soft soil (silt/clayey silt)",
"💡 A weighted scoring model is used: slope (0.35) + lithology (0.25) + rainfall (0.25) + slope height (0.15); the composite score is divided into four hazard grades.",
"This assessment is a qualitative/semi-quantitative method and only a preliminary reference",
"Rainfall is a triggering factor; the alert level must be raised during heavy rain",
"An actual hazard assessment should also consider hydrogeology, vegetation and human engineering activity",
"Soft soil and loose deposits markedly raise the risk at the same slope angle",
"📚 In-Depth Analysis: Slope Geohazard Danger Grade Scoring (slope/rock/rain/height multi-factor)",
"Slope screening: enter slope angle, slope height, daily rainfall and lithology to quickly obtain a composite danger index and grade",
"Disaster prevention zoning: batch-score several slope points to delineate high/very-high danger zones for priority treatment",
"Evacuation advice: give engineering avoidance or monitoring advice by grade to aid emergency plans",
"Algorithm: slope score (<10→1, <25→2, <45→3, otherwise 4), slope-height score (<10→1, <30→2, <50→3, otherwise 4), rainfall score (<25→1, <50→2, <100→3, otherwise 4), lithology score (1 hard to 5 soft soil). Composite danger index = slope×0.35 + lithology×0.25 + rainfall×0.25 + slope height×0.15. Grades: <1.8 I low, <2.6 II medium, <3.4 III high, otherwise IV very high (computed locally).",
"Example: slope 35° (score 3), slope height 40 m (score 3), daily rainfall 80 mm (score 3), soft rock (score 3) → composite = 3×0.35+3×0.25+3×0.25+3×0.15=3.00, Grade III high danger; large-scale construction is inadvisable and dedicated treatment is required.",
"Can the scoring weights be changed?",
"This tool uses fixed weights (slope 0.35/rock 0.25/rain 0.25/height 0.15), an empirical weighting. For a specific region you can refer to the industry code (such as landslide susceptibility assessment) and recompute after adjustment; changing the weights markedly shifts the grade boundaries.",
"Can the grade result directly decide relocation?",
"No. The score is preliminary screening; a very-high danger zone should be supplemented with geological mapping and stability calculation, and relocation or engineering treatment decided together with population and assets. Results are for reference.",
'About "Geological Hazard Risk Assessment"',
"A four-factor weighted scoring model based on slope angle, lithology, rainfall and slope height that comprehensively assesses the hazard grade of geohazards such as landslides and collapses, outputting a composite danger index and graded advice; suitable for preliminary geohazard susceptibility screening.",
"Four-factor weighted scoring with clear grading",
"Automatically gives Grades I-IV danger levels and handling advice",
"Supports a lithology dropdown for convenient operation",
"Preliminary geohazard susceptibility zoning",
"Rapid stability assessment of engineering sites",
"Emergency geohazard inspection during the flood season",
"Reference for county/township geohazard risk census",
"Slope angle",
"Slope height",
"Daily rainfall",
"Lithology type",
],
'sanweidizhijianmocanshu': [
"🧠 3D Geological Modelling Parameters",
"Enter the borehole apparent thickness, strata dip and ore-body size to compute modelling parameters such as true thickness, true area and volume.",
'📖 View the "3D Geological Modelling Parameters Guide"',
"3D modelling parameters = grid/interpolation",
"Borehole apparent thickness h (m)",
"Strata dip θ (°)",
"Strike length L (m)",
"Dip extent S (m)",
"💡 True thickness t = h×cosθ (vertical hole); true area A = L×S; volume V = A×t; horizontal projected area A_h = L×S×cosθ.",
"This calculation assumes a vertical borehole; an inclined hole needs separate conversion",
"The dip is the true dip; an apparent dip must be converted",
"The dip extent is the true length along the bedding plane",
"The volume is a geological volume; the reserve requires multiplying by bulk density and grade",
"📚 In-Depth Analysis: Borehole True Thickness and 3D Modelling Volume Parameter Conversion",
"True-thickness conversion: derive the true thickness from the apparent thickness and strata dip to correct the reserve volume",
"Modelling volume: enter the strike length, dip extent and true thickness to get the block volume and ore tonnage",
"Projection comparison: compare the true area with the horizontal projected area to aid 3D modelling accuracy control",
"Formula: true thickness t = apparent thickness h × cos(dip θ); true area A = strike length L × dip extent S; volume V = A × t; horizontal projected area Ah = L×S×cosθ; vertical thickness = h×sinθ; ore tonnage Q = V × bulk density D. Dip θ ranges 0-89° (computed locally; units m, t/m³).",
"Example: borehole apparent thickness h=5 m, θ=25°, L=300 m, S=200 m, D=2.7 t/m³ → t=5×cos25°=4.532 m, A=60000 m², V=60000×4.532=271892 m³ (0.2719 million m³), Ah=54378 m², vertical thickness=2.113 m, Q=271892×2.7=734109 t.",
"How much do the apparent and true thicknesses differ?",
"The difference lies in cosθ and grows with the dip: at θ=25° the true thickness is about 90.6% of the apparent thickness, and at θ=60° only 50%. For a steeply dipping ore body, mistaking the apparent for the true thickness greatly overestimates the volume.",
"When are the true area and the horizontal projected area equal?",
"Only when θ=0 (horizontal ore body). The larger the dip the smaller Ah relative to A; 3D modelling must use the true area to keep the volume correct.",
'About "3D Geological Modelling Parameters"',
"A 3D geological modelling parameter calculator: from the borehole apparent thickness, strata dip and ore-body size, compute key modelling parameters such as true thickness, true area, horizontal projected area and volume, with ore-tonnage estimation.",
"Automatically converts true and vertical thickness",
"Outputs the true area, horizontal projection and volume together",
"Supports ore-tonnage estimation",
"Fully client-side computation; modelling data processed locally",
"3D geology/ore-body modelling parameter calculation",
"Aid for reserve estimation",
"Spatial correction of borehole data",
"Geological modelling teaching demonstration",
"Borehole apparent thickness",
"Strata dip",
"Strike length",
"Dip extent",
"Ore bulk density",
],
'dizhiwurandiaochapinggu': [
"📋 Geological Contamination Survey Assessment",
"Enter the measured contaminant concentration, background value and assessment standard to compute the pollution index, exceedance factor and geo-accumulation index.",
'📖 View the "Geological Contamination Survey Assessment (Pollution Index / Geo-accumulation Index) Guide"',
"Single-factor pollution index Pi = Cn / Sn; exceedance factor = (Cn − Sn) / Sn; geo-accumulation index Igeo = log₂( Cn / (1.5 × Bn) )",
"Cn is the measured concentration, Bn the background value and Sn the assessment standard; Igeo < 0 uncontaminated, 0-1 uncontaminated to moderate, 1-2 moderate, 2-3 moderate to strong, ≥ 3 strongly contaminated (Müller geo-accumulation index grading).",
"Contaminant name",
"Measured concentration Cn (mg/kg)",
"Background value Bn (mg/kg)",
"Assessment standard Sn (mg/kg)",
"💡 Single-factor pollution index Pi=Cn/Sn; exceedance factor=(Cn−Sn)/Sn; geo-accumulation index Igeo=log₂(Cn/(1.5×Bn)).",
"The geo-accumulation factor 1.5 is a variability background correction",
"Igeo<0 uncontaminated, 0-1 uncontaminated to moderate, 1-2 moderate, 2-3 moderate to strong, >3 strongly contaminated",
"The background value should adopt the regional soil geochemical background",
"The standard value follows the Soil Environmental Quality Risk Control Standard for Agricultural Land GB15618",
"📚 In-Depth Analysis: Geological Contamination Survey Assessment (Pollution Index / Geo-accumulation Index)",
"Single-factor assessment: compute the pollution index Pi and exceedance factor from the measured concentration, background value and assessment standard",
"Enrichment judgement: use the geo-accumulation index Igeo to assess the degree of anthropogenic contamination",
"Site grading: grade by Igeo to guide remediation priority",
"Algorithm: pollution index Pi=Cn/Sn (Sn the assessment standard), exceedance factor=(Cn−Sn)/Sn, enrichment factor=Cn/Bn (Bn the background value), geo-accumulation index Igeo=log₂(Cn/(1.5·Bn)). Müller grading: Igeo<0 uncontaminated, 0-1 uncontaminated to moderate, 1-2 moderate, 2-3 moderate to strong, 3-4 strong, ≥4 very strong contamination. Requires Cn≥0, Bn>0, Sn>0.",
"Example: cadmium Cd measured Cn=0.6 mg/kg, background Bn=0.2, standard Sn=0.3 → Pi=0.6/0.3=2.000, exceedance factor=(0.6−0.3)/0.3=1.000, enrichment factor=0.6/0.2=3.000, Igeo=log₂(0.6/(1.5×0.2))=log₂(2.0)=1.000, judged \"moderate contamination\" and included in remediation assessment. If Cn=0.25, Bn=0.2, Sn=0.3 → Pi=0.833, exceedance factor=−0.167 (not exceeded), Igeo=log₂(0.25/0.3)=−0.263, judged \"uncontaminated\".",
"Which is more authoritative, Pi or Igeo?",
"Pi is the basis of the single-factor/Nemerow index commonly used in domestic site surveys and is intuitive against the standard; Igeo (Müller) introduces the background value and a factor of 1.5 to distinguish natural background from anthropogenic enrichment, making it suitable for identifying the contamination source. The two are complementary and are often reported side by side.",
"What does a negative Igeo indicate?",
"Igeo<0 means the measured concentration is below 1.5 times the background, treated as free of anthropogenic contamination (even below natural background fluctuation) and within the safe range; but this does not mean other contaminants are safe, so each contaminant of concern must be assessed separately.",
'About "Geological Contamination Survey Assessment"',
"A geological contamination survey assessment tool: from the measured contaminant concentration, soil background value and assessment standard, compute the single-factor pollution index, exceedance factor, enrichment factor and geo-accumulation index, and grade the contamination degree by Igeo.",
"Outputs the pollution index, exceedance factor and geo-accumulation index in one go",
"Automatically grade contamination into six levels by Igeo",
"Supports a custom contaminant name",
"Fully client-side computation; survey data processed locally",
"Soil contamination survey and assessment",
"Soil environmental assessment of mining areas and surroundings",
"Heavy-metal contamination grading of farmland soil",
"Environmental geological survey report",
"Contaminant name",
"Measured concentration",
"Background value",
"Assessment standard",
],
}

EXTRA = {
# extract 漏抓的 `公式：` 前缀公式小节（EN 态该节点已无汉字，仅剩全角逗号）
'tester-16': {'公式：σc = P / A，A = π×d²/4': 'Formula: σc = P / A, A = π×d²/4'},
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

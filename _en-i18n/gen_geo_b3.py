#!/usr/bin/env python3
# geology batch3 (5 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'geology')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'geology')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'dijichengzailijisuan': [
"🧮 Foundation Bearing Capacity Calculator",
"Compute the ultimate bearing capacity and characteristic value of a strip footing from the Terzaghi formula (safety factor 2).",
'📖 View the "Ultimate Bearing Capacity and Characteristic Value Calculation (Terzaghi Formula) Guide"',
"Bearing capacity = f(soil properties, depth, width)",
"Cohesion c (kPa)",
"Unit weight γ (kN/m³)",
"Foundation width B (m)",
"Foundation depth Df (m)",
"💡 Terzaghi strip footing: qu = c·Nc + γ·Df·Nq + 0.5·γ·B·Nγ; characteristic bearing capacity fa = qu / K. The bearing-capacity factors are derived from φ.",
"This formula applies to strip footings with general shear failure",
"When φ=0, Nγ=0, so a soft-soil correction formula must be used instead",
"The safety factor is generally 2-3, taken higher for important projects",
"Actual design must follow the Code for Design of Building Foundations GB50007",
"📚 In-Depth Analysis: Ultimate Bearing Capacity and Characteristic Value Calculation (Terzaghi Formula)",
"Strip footing design: compute the Terzaghi ultimate bearing capacity qu and characteristic value fa from cohesion, internal friction angle and unit weight",
"Foundation check: enter the actual footing width and depth to judge whether fa meets the superstructure load",
"Option comparison: vary φ, c, B and Df to observe the trend of bearing capacity",
"Algorithm (Terzaghi strip footing, general shear): bearing-capacity factors Nq=exp(π·tanφ)·tan²(π/4+φ/2), Nc=(Nq−1)/tanφ (5.14 when φ=0), Nγ=2(Nq+1)·tanφ; ultimate bearing capacity qu=c·Nc+γ·Df·Nq+0.5·γ·B·Nγ; characteristic value fa=qu/K (K the safety factor, default 2). Also outputs the bearing capacity per linear metre fa·B. Requires c≥0, φ≥0, γ>0, B>0, K>0.",
"Example: c=15 kPa, φ=20°, γ=18 kN/m³, B=2 m, Df=1.5 m, K=2 → Nq=6.40, Nc=14.83, Nγ=5.39; qu=15×14.83+18×1.5×6.40+0.5×18×2×5.39=222.5+172.8+96.9=492.26 kPa; fa=492.26/2=246.13 kPa, 492.26 kN/m per linear metre. If c=10, φ=30, γ=19, B=3, Df=2, K=2 → Nq=18.40, Nc=30.14, Nγ=22.40; qu=1639.11 kPa, fa=819.55 kPa, showing that a larger φ markedly raises the bearing capacity.",
"What conditions does the Terzaghi formula apply to?",
"It applies to strip footings with general shear failure of the subsoil, a modest foundation depth and the effective unit weight below the water table. Circular/square footings, deep foundations or weak underlying layers need correction factors or other formulas (such as Hansen or Vesic); results from this tool are for reference.",
"Is a safety factor K of 2 reasonable?",
"K=2-3 is the common range for building foundations, determined by the code and structural importance. It can be lowered for temporary works and raised for sensitive buildings; fa is only the bearing capacity at the footing base, so settlement and weak underlying layers must also be checked, and fa alone cannot determine the foundation.",
'About "Foundation Bearing Capacity Calculator"',
"Based on Terzaghi's ultimate bearing capacity theory, compute the ultimate and characteristic bearing capacity of a strip footing from the soil shear-strength indices (cohesion, internal friction angle) and foundation parameters, automatically solving the factors Nc, Nq and Nγ.",
"Automatically derives the three bearing-capacity factors from the internal friction angle",
"Outputs the ultimate bearing capacity and characteristic value together",
"Supports a custom safety factor",
"Fully client-side computation; survey data processed locally",
"Preliminary foundation design",
"Bearing capacity estimate in geotechnical surveys",
"Foundation scheme comparison and optimisation",
"Geotechnical teaching and design demonstration",
"Cohesion",
"Internal friction angle",
"Unit weight",
"Foundation width",
"Foundation depth",
],
'estimate-reserve-1': [
"🔮 Cross-Section Method Reserve Estimation",
"Enter two adjacent section areas, the section spacing, ore bulk density and grade to compute the volume and reserve by the cross-section (parallel section) method.",
'📖 View the "Cross-Section Method Reserve Estimation Guide"',
"Cross-section method V = Σ(A_i×L_i)",
"Section 1 area S₁ (m²)",
"Section 2 area S₂ (m²)",
"Section spacing L (m)",
"💡 Formula: volume V = (S₁+S₂)/2 × L; ore tonnage Q = V × D; metal content P = Q × C/100 (trapezoidal formula).",
"The trapezoidal method is used when S₁/S₂ is close to 1; when the difference is large the frustum formula may be used instead",
"Sections should be parallel to each other and perpendicular to the ore-body strike",
"The reserve category depends on the degree of engineering control; this tool only computes the volume",
"Grade is entered in %; precious metals in g/t must be converted first",
"📚 In-Depth Analysis: Parallel Section (Cross-Section) Ore-Body Reserve Estimation",
"Volume between two sections: from the adjacent section areas and spacing, find the block volume and ore tonnage",
"Boundary extrapolation: when one side has no engineering control, use wedge/cone end-angle extrapolation and discount the result",
"Preliminary metal content: combine with the average grade to obtain the metal content, aiding economic evaluation",
"Algorithm: average section = (S₁+S₂)/2; volume V = average section × section spacing L; ore tonnage Q = V × bulk density D; metal content P = Q × grade C / 100. Suitable for layered or vein ore bodies of fairly stable attitude with a linear transition between the two sections (computed locally).",
"Example: two parallel sections S₁=800 m², S₂=600 m², L=50 m, D=2.8 t/m³, C=0.8% → average section=700 m², V=35000 m³, Q=98000 t (98,000 tonnes), P=784 t.",
"Can it still be used when the two sections differ greatly in shape?",
"A large difference means the ore-body shape changes sharply and the average-section method becomes less accurate. The block method or geostatistics can be used instead, with the wedge-out/extrapolated ends treated separately.",
"What if the grade is missing?",
"When the grade is left blank, the metal content is treated as 0. Formal estimation should interpolate or take the grade of adjacent workings; leaving it blank systematically underestimates the metal content.",
'About "Cross-Section Method Reserve Estimation"',
"Estimate ore-body reserves by the parallel section (trapezoidal) method. Enter two adjacent exploration section areas, the section spacing, ore bulk density and grade to compute the ore-body volume, ore tonnage and metal content; a common reserve calculation method in the exploration stage.",
"Trapezoidal method to compute the ore-body volume between two sections",
"Outputs ore tonnage and metal content together",
"Supports conversion to units of 10,000 tonnes",
"Fully client-side computation; data processed locally",
"Reserve calculation on exploration-line sections",
"Deposit reserve estimation report",
"Mining design and block delineation",
"Geological reserve verification",
"Section 1 area",
"Section 2 area",
"Section spacing",
"Ore bulk density",
"Average grade",
],
'dizhishujutongji': [
"📊 Geological Data Statistics",
"Enter a set of geological data (comma- or space-separated) to compute the mean, standard deviation, coefficient of variation, confidence interval and other statistics.",
'📖 View the "Geological Data Statistics Guide"',
"Data series (comma- or space-separated)",
"Sample (n-1)",
"Population (N)",
"💡 Mean x̄=Σxi/n; standard deviation σ=√[Σ(xi−x̄)²/(n−1)] (sample) or /N (population); coefficient of variation CV=σ/x̄×100%; confidence interval = x̄±t·σ/√n.",
"The sample standard deviation uses n−1 as denominator (unbiased estimate); the population standard deviation uses N",
"The coefficient of variation CV reflects the dispersion; CV<15% is uniform and >30% is non-uniform",
"The confidence interval is based on the t-distribution and requires a sample size n≥3",
"Non-numeric characters in the data are filtered out automatically",
"Results are for reference; formal statistics require a distribution test",
"📚 In-Depth Analysis: Geological Data Statistical Analysis (Mean/Standard Deviation/Confidence Interval)",
"Sample overview: enter data to compute the mean, ",
"Uniformity judgement: use the coefficient of variation CV to classify the data as uniform/fairly uniform/non-uniform",
"Inferential estimate: give the confidence interval of the population mean from the t-distribution",
"Algorithm: n, sum, mean x̄; variance switches between population (N) and sample (n−1), standard deviation σ=√variance; coefficient of variation CV=σ/x̄×100%; minimum, maximum, range, ",
"; standard error SE=σ/√n; confidence interval = x̄ ± t(α/2,n−1)·SE (t looked up from the t-table by confidence level and degrees of freedom). Dispersion: CV<15% uniform, 15-30% fairly uniform, ≥30% non-uniform.",
"Example: 10 rock-density measurements 12.5,13.2,11.8,12.7,13.1,12.9,12.3,13.0,12.6,12.8 (g/cm³, 95% confidence, sample) → mean=12.6900, standard deviation=0.4175, CV=3.29%, median=12.7500, range=1.4000, SE=0.1320, t(0.025,9)=2.262, margin of error=0.2987, 95% confidence interval [12.3913, 12.9887], judged \"uniform\". If instead ",
"ore grade",
"1.2,1.8,0.9,2.3,1.5,1.1,0.7,2.0,1.6,3.1 → mean=1.6200, σ=0.7193, CV=44.40%, judged \"non-uniform\".",
"How should the 95% confidence interval be understood?",
"Under repeated sampling, about 95% of such intervals would cover the true population mean; it describes the uncertainty range of the estimate, not that \"the true value has a 95% probability of lying in this interval\". The larger the sample and the smaller the dispersion, the narrower the interval.",
"Should I choose the population or sample variance?",
"If the n values are the entire population of interest (such as a whole batch of samples), use the population (N) variance; if they are a sample drawn from a larger population, use the sample (n−1) variance for an unbiased estimate. For inferential statistics, always choose sample.",
'About "Geological Data Statistics"',
"A descriptive statistics tool for geological exploration, geochemical analysis and rock/mineral testing: enter a set of geological data to quickly compute the mean, standard deviation, variance, coefficient of variation, median, range, interquartile range and confidence interval, helping assess the central tendency and dispersion of the data.",
"Automatically parses multiple separators: comma, space and semicolon",
"Choose the sample standard deviation (n−1) or the population standard deviation (N)",
"Built-in t-table to compute 80/90/95/99% confidence intervals",
"Automatically assesses data dispersion (uniform/fairly uniform/non-uniform)",
"Fully client-side computation; experimental data is not uploaded",
"Statistical analysis of geochemical element content data",
"Repeatability check of rock/mineral tests",
"Dispersion assessment of reserve-estimation grade data",
"Statistics of geotechnical test parameters and outlier screening",
"Data series",
],
'huanjingdizhipingjia': [
"♻️ Environmental Geological Assessment",
"Enter the measured values and assessment standards of each environmental factor and use the Nemerow composite index method to compute the composite environmental quality index.",
'📖 View the "Nemerow Composite Index Method Environmental Quality Assessment Guide"',
"Environmental geological assessment = composite grading",
"💡 Nemerow composite index: P = √((Pmax² + Pavg²)/2), Pi = Ci/Si (measured/standard value).",
"All indicators must use a unified assessment standard",
"Blank indicator rows are skipped automatically",
"P<0.7 clean, 0.7-1 light pollution, 1-2 moderate pollution, >2 heavy pollution",
"An actual assessment should follow the Environmental Quality Standards series",
"📚 In-Depth Analysis: Nemerow Composite Index Method Environmental Quality Assessment",
"Multi-factor assessment: enter the measured and standard values of several indicators such as water quality, soil and noise to obtain a composite pollution index",
"Source tracing: the largest single-factor index identifies the primary pollutant and guides treatment priority",
"Compliance judgement: grade by composite index (clean/light/moderate/heavy pollution) and produce an assessment conclusion",
"Algorithm: single-factor index Pi = measured Ci / standard Si; average index Pavg = ΣPi/n; composite index P = √((Pmax² + Pavg²)/2). Grading: P<0.7 clean (I), <1 light pollution (II), <2 moderate pollution (III), ≥2 heavy pollution (IV) (standard values must be >0; computed locally).",
"Example: five indicators — COD 18/20, ammonia nitrogen 1.0/1.0, soil cadmium 0.4/0.3, soil lead 60/90, daytime noise 65/60 → Pi are 0.90, 1.00, 1.333, 0.667 and 1.083, Pavg=0.997, Pmax=1.333, P=√((1.333²+0.997²)/2)=1.177, Grade III moderate pollution, with soil cadmium as the primary factor (largest Pi).",
"Why use the Nemerow method rather than a simple average?",
"The Nemerow method uses the sum of squares and square root to emphasise the largest single-factor pollution (Pmax), preventing the average from diluting an outstanding exceedance factor and making it easier to identify the primary pollution source; it is a common approach in the Technical Guidelines for Environmental Impact Assessment.",
"How is a missing measured value handled?",
"An indicator whose value is missing or whose standard value is ≤0 is excluded from the average (skipped). But a missing key factor distorts Pmax, so the conclusion is for reference and a formal assessment should complete the monitoring data.",
'About "Environmental Geological Assessment"',
"Using the Nemerow composite index method, comprehensively assess multiple environmental factor indicators such as water quality, soil and noise, outputting the composite environmental quality index and single-factor pollution indices and determining the environmental quality grade.",
"Parallel multi-indicator assessment balancing the maximum and average",
"Automatically determines four levels from clean to heavy pollution",
"Indicator names are customisable",
"Fully client-side computation; monitoring data processed locally",
"Comprehensive environmental quality assessment of mining areas",
"Assessment of the current water and soil pollution status",
"Reference for construction project environmental impact assessment",
"Compilation of environmental geological survey reports",
"How to use the Environmental Geological Assessment",
"Indicator '+(i+1)+'",
"Measured value Ci",
"Standard value Si",
"What does the Environmental Geological Assessment do?",
"How do I use the Environmental Geological Assessment?",
"What scenarios is the Environmental Geological Assessment suitable for?",
],
'estimate-grade-reserve': [
"🔮 Ore Grade Reserve Estimation",
"Enter the ore-body area, average thickness, ore bulk density and average grade to estimate the ore tonnage and metal content.",
'📖 View the "Ore Grade Reserve Estimation Guide"',
"Grade reserve = grade × volume × bulk density",
"Ore-body area S (m²)",
"Average thickness M (m)",
"💡 Formula: ore tonnage Q = S × M × D (tonnes); metal content P = Q × C% (when the grade is entered in %, P = Q × C/100).",
"The grade is entered as a mass percentage; for precious metals in g/t, convert to %",
"The area and thickness should be the projected values of the true thickness of the same ore body",
"The bulk density should be the small-sample density measured in the laboratory",
"This estimate uses the geological block method and does not account for mining loss and dilution",
"📚 In-Depth Analysis: Block Method Ore Grade Reserve Preliminary Estimation",
"Preliminary resource: enter the ore-body area, average thickness, bulk density and grade to quickly obtain the ore tonnage and metal content",
"Ore blending assessment: compare the grades of adjacent blocks to judge whether they can be mined together or must be mined separately",
"Preliminary report calculation: use this tool for a preliminary resource estimate in early exploration to support the next detailed survey",
"Algorithm: volume V = area S × average thickness M; ore tonnage Q = V × bulk density D; metal content P = Q × grade C / 100. Also gives the metal grade kg/t = P/Q×1000 and g/t = P/Q×10⁶ (computed locally; units must be unified to m, t/m³ and %).",
"Example: ore body S=50000 m², M=3.5 m, D=2.7 t/m³, C=1.2% → V=175000 m³, Q=472500 t (472,500 tonnes), P=5670 t (5,670 tonnes), metal grade 12.0 kg/t (=12000 g/t).",
"Is the area the horizontal projection or the true area?",
"The block method generally uses the horizontal projected area of the level or bench. If the ore body dips steeply, convert the true thickness to the true area first (see ",
"tool); otherwise the volume is underestimated.",
"Can the result be used for reserve filing?",
"This tool provides a preliminary estimate; formal reserves/resources must be classified (measured/indicated/inferred) per GB/T 17766 and filed after review. The preliminary value is only for early target selection and engineering deployment.",
'About "Ore Grade Reserve Estimation"',
"A mineral reserve estimation tool based on the geological block method: enter the ore-body area, average thickness, ore bulk density and average grade to quickly obtain the ore tonnage, metal content and several grade expressions; suitable for resource estimation in the reconnaissance and detailed survey stages.",
"Outputs the volume, ore tonnage and metal content together",
"Supports units of 10,000 tonnes and g/t grade conversion",
"Real-time calculation on input, with one-click copy of the result",
"Runs fully client-side; exploration data is not uploaded",
"Metal deposit reserve estimation and report compilation",
"Preliminary resource assessment in the exploration stage",
"Reference for mining rights valuation and feasibility studies",
"Teaching demonstration of reserve calculation principles",
"Ore-body area",
"Average thickness",
"Ore bulk density",
"Average grade",
],
}

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

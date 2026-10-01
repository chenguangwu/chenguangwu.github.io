#!/usr/bin/env python3
# geology batch4 (5 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'geology')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'geology')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'calc-87': [
"🧮 Geochemical Anomaly Contrast Calculation",
"Enter the background value, anomaly value (and optional standard deviation) to compute the contrast coefficient, enrichment factor, anomaly threshold and anomaly intensity.",
'📖 View the "Geochemical Anomaly Contrast Calculation Guide"',
"Contrast coefficient Ac = anomaly value / background value; anomaly threshold T = background value + 2 × standard deviation; anomaly intensity = anomaly value / T",
"Ac > 1 is a positive anomaly and < 1 a negative anomaly; intensity ≥ 2 strong anomaly, ≥ 1.5 moderate anomaly, ≥ 1 weak anomaly, otherwise within the background range.",
"Anomaly value C (μg/g)",
"💡 Formula: contrast coefficient Ac = C/B; anomaly threshold T = B + 2σ; anomaly intensity = C/T; enrichment factor = C/B (dimensionless).",
"The background value usually takes the mean or median of the statistical population",
"The anomaly threshold is often the background + 2 standard deviations (about 95% confidence)",
"A contrast coefficient > 1 is a positive anomaly and < 1 a negative anomaly",
"Elements differ greatly in geochemical behaviour, so the background should be computed by zone",
"📚 In-Depth Analysis: Geochemical Anomaly Contrast and Intensity Calculation",
"Anomaly screening: compute the contrast coefficient from the background and anomaly values to quickly identify positive/negative anomalies",
"Anomaly grading: use the anomaly threshold and intensity to classify weak/moderate/strong anomalies and guide verification order",
"Section interpretation: compute the contrast point by point along the survey line to delineate the anomaly centre and concentration centre",
"Algorithm: contrast coefficient Ac = anomaly value C / background value B; anomaly threshold T = B + 2σ (σ is the ",
", treated as 0 if blank); anomaly intensity = C / T; enrichment factor = C / B. Judgement: Ac>1 positive anomaly, <1 negative anomaly; intensity ≥2 strong anomaly, ≥1.5 moderate anomaly, ≥1 weak anomaly, otherwise background range.",
"Example: background B=40 μg/g, anomaly C=120 μg/g, σ=10 → Ac=120/40=3.000, threshold T=40+2×10=60, intensity=120/60=2.000, judged \"strong anomaly\" (clear concentration centre). If B=30, C=90, σ=10 → Ac=3.000, T=30+20=50, intensity=90/50=1.800, judged \"moderate anomaly\".",
"Why is the anomaly threshold B+2σ?",
"When the background is approximately ",
", about 95% of background points fall within mean±2σ and a value beyond that is treated as a statistical anomaly. If the background is clearly skewed, it is better to switch to ",
" + multiple, or iteratively remove high values and recompute, avoiding ore-induced high values being included in the background and raising the threshold.",
"What is the difference between contrast and intensity?",
"The contrast Ac=C/B reflects the ratio to the background; the intensity = C/T is based on the anomaly threshold and better indicates the enrichment of an anomaly above the threshold. Combined, they distinguish \"overall high but weak\" from \"locally very strong\" anomalies.",
'About "Geochemical Anomaly Contrast Calculation"',
"A common anomaly-contrast calculation tool in geochemical exploration: from the element background value, anomaly value and standard deviation, compute the contrast coefficient, enrichment factor, anomaly threshold and anomaly intensity, automatically determining the anomaly class and intensity grade.",
"Computes the four indicators contrast, enrichment, threshold and intensity at once",
"Automatically determines positive/negative anomalies and strong/moderate/weak grades",
"The standard deviation is optional for quick estimation",
"Fully client-side computation; data stored locally",
"Delineating the anomaly threshold of geochemical data",
"Analysis of element enrichment patterns in mining areas",
"Geochemical anomaly assessment and grading",
"Geochemical report compilation and data organisation",
"Background value",
"Anomaly value",
],
'diqiuwulishujujisuan': [
"🧮 Geophysical Data Calculation",
"Choose a geophysical method and enter the corresponding parameters to compute gravity/magnetic/electrical/seismic anomaly values.",
'📖 View the "Geophysical Data Calculation Guide"',
"Gravity anomaly (Bouguer slab)",
"Magnetic anomaly (sphere)",
"Electrical (apparent resistivity, Wenner)",
"Seismic (velocity/reflection depth)",
"💡 Gravity Bouguer slab: Δg = 0.0419 × ρ × h (mGal), ρ the density contrast (g/cm³), h the thickness (m).",
"The gravity Bouguer slab formula applies to a horizontal layered-medium approximation",
"The magnetic sphere formula gives the maximum directly above; the magnetisation direction must be considered in practice",
"The apparent resistivity is based on a homogeneous half-space assumption",
"Seismic velocity = distance/time, reflection depth = v×t/2",
"📚 In-Depth Analysis: Forward Modelling Data Calculation in Geophysical Exploration",
"Gravity anomaly estimate: compute the Bouguer/residual gravity anomaly from the residual density contrast and thickness",
"Magnetic forward modelling: compute the magnetic anomaly ΔT from susceptibility, magnetising field, volume and depth",
"Electrical/seismic: compute the apparent ",
"resistivity",
" and seismic velocity and reflection depth",
"Algorithm (four methods optional): gravity Δg=0.0419·Δρ·h (mGal, ×10 to get g.u.); magnetic ΔT=200·κ·H·V/z³ (nT), with magnetisation M=κ·H; electrical array factor K=2πa, apparent resistivity ρa=K·ΔV/I; seismic velocity v=d/t, reflection depth H=v·t/2. Each method forward-models in real time from the chosen parameters for comparison with the measured curve.",
"Example (gravity): residual density contrast Δρ=0.3 g/cm³, thickness h=100 m → Δg=0.0419×0.3×100=1.257 mGal (=12.57 g.u.). Example (electrical): electrode spacing a=10 m, potential difference ΔV=0.05 V, current I=1 A → K=2π×10=62.83 m, ρa=62.83×0.05/1=3.14 Ω·m, a low-resistivity layer characteristic.",
"What if the forward model does not match the measurements?",
"Forward modelling uses an ideal model (uniform slab/point source), while measurements are affected by the host rock, topography and noise. First check whether the parameters (density contrast, depth, array) are reasonable, then perform inversion or 2D forward modelling; a single-point formula can only check the order of magnitude.",
"How do g.u. and mGal convert?",
"1 g.u. (gravity unit) = 0.1 mGal; the tool converts automatically (Δg×10). Domestic geophysical reports often use g.u. and international literature mostly uses mGal; the two differ only by a factor of 10.",
'About "Geophysical Data Calculation"',
"An anomaly-value calculation tool integrating four common geophysical methods — gravity, magnetic, electrical and seismic — switching input parameters by method and using the Bouguer slab, magnetic sphere, Wenner apparent resistivity and velocity/reflection-depth formulas respectively.",
"One-stop calculation for four geophysical methods",
"Switching method auto-loads typical parameters",
"Formulas and units are clearly annotated",
"Fully client-side computation; raw data is not uploaded",
"Preliminary geophysical data organisation and anomaly estimation",
"Reference for rapid field inversion",
"Geophysical teaching and experiment demonstration",
"Aid for geophysical report compilation",
"Geophysical method",
],
'diqiuhuaxueyichangjieshi': [
"🪨 Geochemical Anomaly Interpretation",
"Enter the element content, background value and standard deviation to compute the standardised anomaly value (Z value) and determine the anomaly class and intensity.",
'📖 View the "Geochemical Anomaly Interpretation Guide"',
"Geochemical anomaly interpretation = background + contrast value",
"Element name",
"Element content C (μg/g)",
"💡 Standardised anomaly value Z = (C−B)/σ; contrast coefficient Ac = C/B. Z<2 background, 2-3 weak anomaly, 3-4 moderate anomaly, >4 strong anomaly.",
"The Z-value method requires the background to be approximately normally distributed",
"The anomaly intensity is graded by multiples of the standard deviation",
"A negative anomaly (Z<−2) indicates depletion and needs separate interpretation",
"The interpretation should consider the geological setting and multi-element association",
"📚 In-Depth Analysis: Geochemical Anomaly Interpretation (Standardised Z-Value Method)",
"Anomaly identification: from the content, background value and ",
"compute the standardised Z value and grade it",
"Concentration-centre location: compute Z and contrast point by point along the survey line to delineate the strong-anomaly centre",
"Negative-anomaly detection: Z<−2 indicates significant depletion, aiding the search for alteration or lean-ore zones",
"Algorithm: standardised anomaly value Z=(C−B)/σ, contrast coefficient Ac=C/B, absolute anomaly = C−B. Grading: Z<−2 significant depletion, −2 to 2 background, 2 to 3 weak anomaly, 3 to 4 moderate anomaly, ≥4 strong anomaly; intensity |Z|<2 no obvious enrichment, <3 low, <4 moderate, ≥4 high. Requires B>0, σ>0.",
"Example: copper Cu content C=80 μg/g, background B=30, σ=10 → Z=(80−30)/10=5.000, Ac=80/30=2.667, judged \"strong anomaly, high intensity\" (clear concentration centre, verify first). If C=50, B=30, σ=10 → Z=2.000, Ac=1.667, judged \"weak anomaly, low intensity\" and put on the secondary verification list.",
"What does each of the Z value and contrast Ac show?",
"Z measures the statistical significance of the deviation from the background in units of standard deviation and suits cross-element comparison; Ac=C/B is a ratio, intuitive but ignoring the background dispersion. Strong anomalies usually have both high, but a high Ac with a low Z (a very dispersed background) may just be noise.",
"Does Z≥4 necessarily mean ore?",
"Not necessarily. A high Z only means the element is significantly enriched; it may be mineralisation, supergene enrichment or anthropogenic contamination. Judge together with the element association, geological setting and surface outcrops, deploying trenches or boreholes for verification when necessary.",
'About "Geochemical Anomaly Interpretation"',
"A geochemical anomaly interpretation tool: from the element content, background value and standard deviation, compute the standardised anomaly value Z and contrast coefficient, classify the anomaly (background/weak/moderate/strong) and its intensity by multiples of the standard deviation, and automatically detect positive and negative anomalies.",
"Outputs the Z value, contrast coefficient and absolute anomaly together",
"Grades anomalies by 2σ, 3σ and 4σ",
"Automatically detects depletion negative anomalies",
"Fully client-side computation; geochemical data processed locally",
"Delineating the geochemical anomaly threshold and grading",
"Multi-element anomaly comparison and screening",
"Prospecting prediction in mining areas",
"Anomaly interpretation in geochemical reports",
"Element name",
"Element content",
"Background value",
],
'calc-25': [
"🌋 Earthquake Epicentral Distance Calculator",
"Enter the arrival-time difference between the P and S waves to estimate the epicentral distance (P-wave velocity 6 km/s, S-wave velocity 3.5 km/s).",
'📖 View the "Earthquake Epicentral Distance Calculation Guide"',
"Epicentral distance D = Δt × Vp × Vs / (Vp − Vs); angular distance = D / 111.32; P-wave travel distance = Δt × Vp",
"Δt is the arrival-time difference between the S and P waves, Vp and Vs the P- and S-wave velocities; D / 111.32 converts kilometres to spherical degrees (1° ≈ 111.32 km).",
"P-S arrival-time difference Δt (s)",
"P-wave velocity Vp (km/s)",
"S-wave velocity Vs (km/s)",
"💡 Formula: epicentral distance D = Δt × Vp × Vs / (Vp − Vs); the P wave reaches the observation point before the S wave and their arrival-time difference is proportional to the epicentral distance.",
"This formula assumes a homogeneous medium; actual formation velocity varies with depth",
"Applies to near earthquakes (generally < 1000 km); distant earthquakes need a spherical path",
"The P-S arrival-time difference usually takes the first-arrival difference; 0.1 s precision is recommended",
"Results are for reference; official bulletins follow seismic network determinations",
"📚 In-Depth Analysis: Earthquake Epicentral Distance Calculation (P-S Time-Difference Method)",
"Rapid location: estimate the epicentral distance from the P- and S-wave arrival-time difference recorded at a station, aiding rapid locating",
"Teaching demonstration: show the relationship between epicentral distance and angular distance for given time difference and velocities",
"Multi-station intersection: the single-station epicentral distance is a basic input for circle-intersection location",
"Algorithm: epicentral distance D = Δt·Vp·Vs/(Vp−Vs), where Δt is the S minus P arrival-time difference and Vp, Vs the P/S wave velocities (default Vp=6.0, Vs=3.5 km/s). Angular distance (great-circle distance) = D/111.32 (°), 111.32 km being the approximate arc length of 1° on the surface. Requires Δt>0, Vp>Vs>0.",
"Example: Δt=20 s, Vp=6.0 km/s, Vs=3.5 km/s → D=20×6.0×3.5/(6.0−3.5)=420/2.5=168.00 km, angular distance=168/111.32=1.51°. If Δt=30 s with the same velocities → D=252.00 km, angular distance=2.26°. Note that using a regional average velocity makes the result approximate; a higher Vp in hard-rock areas gives a larger epicentral distance for the same Δt.",
"Why is the result only approximate?",
"The formula assumes a homogeneous medium from the epicentre to the station and straight-line wave propagation. Real crustal velocity varies with depth and rays bend, so the single-station time-difference method gives an approximate straight-line distance to the epicentre; precise location needs at least three intersecting stations.",
"How much does an incorrect Vp/Vs matter?",
"D is extremely sensitive to the velocity difference (Vp−Vs). If Vs is overestimated, the smaller denominator greatly exaggerates the epicentral distance; take values from tables according to the lithology beneath the station, as sedimentary basins and bedrock areas differ markedly.",
'About "Earthquake Epicentral Distance Calculator"',
"Quickly estimate the earthquake epicentral distance from the arrival-time difference of the P and S waves at the observation point. Based on the velocity difference between P and S waves in a homogeneous medium; suitable for near-earthquake locating and teaching demonstrations.",
"Supports custom P/S wave velocities for the media of different regions",
"Outputs the epicentral distance, angular distance and P-wave travel distance together",
"History can be restored for repeated comparison",
"Seismology teaching and experiment demonstration",
"Preliminary epicentral distance for near-earthquake rapid reporting",
"Reference for engineering seismic safety evaluation",
"Explaining earthquake principles in science-popularisation activities",
"P-S arrival-time difference",
"P-wave velocity",
"S-wave velocity",
],
'diqiuwuliyingyong': [
"🪨 Geophysical Applications",
"Choose a geophysical method and enter the array parameters to estimate the depth of investigation and vertical resolution.",
'📖 View the "Geophysical Applications Guide"',
"Geophysical applications = inversion and interpretation",
"Electrical (DC resistivity)",
"Magnetic (magnetic anomaly half-width)",
"Seismic (reflection method)",
"💡 Electrical: depth of investigation ≈ AB/2; vertical resolution ≈ electrode spacing a (Wenner).",
"The depth of investigation is an empirical estimate, affected by geoelectric/magnetic conditions",
"The electrical depth of investigation deepens as the electrode spread increases",
"Magnetic depth estimation uses the Peters half-width method",
"Seismic resolution takes λ/4 (Widess criterion)",
"📚 In-Depth Analysis: Estimating Applied Parameters in Geophysical Exploration (Depth of Investigation / Resolution)",
"Electrical array design: estimate the depth of investigation and vertical resolution from the current electrode spread AB",
"Magnetic inversion: estimate the burial depth of the magnetic body from the anomaly half-width by the Peters method",
"Seismic resolution: estimate the reflection depth and vertical resolution from velocity, dominant frequency and travel time",
"Algorithm (three methods optional): electrical depth of investigation ≈ AB/2, vertical resolution ≈ electrode spacing a, depth-to-spacing ratio = depth/a; magnetic (Peters method) depth h ≈ anomaly half-width hw/1.31, resolution ≈ h/4, anomaly full width = 2·hw; seismic reflection depth H=v·t/2, wavelength λ=v/f, vertical resolution ≈ λ/4. Used to assess scheme feasibility and survey-line layout.",
"Example (electrical): AB=200 m, a=20 m → depth of investigation ≈100.00 m, resolution ≈20.00 m, depth-to-spacing ratio=5.00 (a larger ratio helps resolve deep thin layers). Example (magnetic): anomaly half-width hw=40 m → depth h≈40/1.31=30.53 m, resolution ≈7.63 m, anomaly full width 80.00 m, indicating a shallow magnetic source.",
"Can the depth of investigation and resolution be improved at the same time?",
"They usually trade off: increasing the electrode spacing/offset deepens but lowers the resolution. The electrical depth-to-spacing ratio (depth/resolution) is a compromise indicator; design should derive the required spacing from the target size rather than simply seeking depth.",
"Is the Peters-method depth accurate?",
"The Peters method assumes a slab-like magnetic body with a nearly symmetric anomaly and suits simple isolated magnetic sources; a dipping attitude or overlapping anomalies distort the half-width, so the result should be used with the section shape and inversion as a preliminary estimate.",
'About "Geophysical Applications"',
"An applied-parameter estimation tool for engineering geophysics: for electrical, magnetic and seismic reflection methods, enter the array parameters to estimate the depth of investigation and vertical resolution, providing a reference for geophysical scheme design and result interpretation.",
"Depth-of-investigation and resolution estimation for three methods",
"Electrical method includes a depth-to-spacing ratio assessment",
"Seismic uses the Widess λ/4 criterion",
"Fully client-side computation; parameters stored locally",
"Engineering geophysical scheme design",
"Justification of exploration depth and accuracy",
"Geophysical method comparison",
"Geophysical teaching and training",
"Geophysical method",
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

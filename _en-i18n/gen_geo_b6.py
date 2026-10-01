#!/usr/bin/env python3
# geology batch6 (5 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'geology')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'geology')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'stratum-correlation': [
"⚖️ Stratigraphic Correlation",
"A Chinese chronostratigraphic standard correlation table, matching erathem (era) to system (period), age range and typical rocks and fossils.",
'📖 View the "Stratigraphic Correlation Guide"',
"Chinese chronostratigraphy matches erathem (era) to system (period): the Palaeozoic Erathem contains the Cambrian, Ordovician, Silurian, Devonian, Carboniferous and Permian systems (about 541 to 252 Ma); the Mesozoic Erathem contains the Triassic, Jurassic and Cretaceous systems (252 to 66 Ma); the Cenozoic Erathem contains the Palaeogene, Neogene and Quaternary systems (66 Ma to present); the correlation is based on index-fossil assemblages, lithological characteristics and isotopic ages, with erathem-system boundaries drawn at abrupt biological-evolution interfaces.",
"All erathems (eras)",
"Cenozoic Erathem",
"Mesozoic Erathem",
"Palaeozoic Erathem",
"Precambrian",
"Chronostratigraphic units from largest to smallest: eonothem (eon) / erathem (era) / system (period) / series (epoch) / stage (age). Geological ages are given in millions of years (Ma).",
"📚 In-Depth Analysis: Chinese Chronostratigraphic (Erathem-System) Standard Correlation",
"Mapping correlation: in the field, assign strata to the standard chronostratigraphic units (systems) by rock association and fossils",
"Age conversion: look up the geological age range (Ma) and the erathem (era) of a system",
"Science teaching: build a \"system-period-age\" correspondence framework to aid the study of Earth history and the time scale",
"The correlation table is organised by erathem (era): Cenozoic (2.58 Ma to present), Mesozoic (252-66 Ma), Palaeozoic (541-252 Ma), Precambrian (>541 Ma). Each system lists its age range, typical rocks and index fossils, e.g. the Cambrian 541-485 Ma (trilobites, Chengjiang biota) and the Cretaceous 145-66 Ma (dinosaur extinction, birds). Correlation is local and does not rely on the network.",
"Example: a section with trilobites and graptolite shale → assigned to the Cambrian (541-485 Ma, Palaeozoic); red sandstone with dinosaur fossils → Cretaceous (145-66 Ma, Mesozoic); human fossils and loess → Quaternary (2.58 Ma to present, Cenozoic). Their age spans are about 56 Ma, 79 Ma and 2.58 Ma respectively, from which the relative order can be set.",
"What is the relationship between a system and a period?",
"A system is a chronostratigraphic unit (a rock body) and a period is a geochronological unit (time). They correspond one to one: the Cambrian System corresponds to the Cambrian Period. Use the system for mapping and the period (Ma) for dating.",
"Is the Sinian System Precambrian?",
"Yes. The Sinian System, 635-541 Ma, belongs to the Neoproterozoic (Precambrian) and is characterised by tillite, dolomite and the Ediacaran biota, lying below the Cambrian System (the start of the Phanerozoic at 541 Ma).",
'About "Stratigraphic Correlation"',
"Stratigraphic Correlation is an online tool in the scientific research field. A scientific research tool that uses standard scientific formulas for accurate calculation.",
"Search system / period / rock / fossil...",
],
'sample-1': [
"📡 Trenching (Trench/Channel/Sampling) Design",
"Estimate the trenching excavation volume, number of sampling intervals and cost from the trench length and cross-sectional area, for exploration engineering budgeting.",
'📖 View the "Trenching (Trench/Channel/Sampling) Design Guide"',
"Excavation volume (m³) = length × section; sampling intervals ≈ length ÷ 2; cost ≈ excavation volume × 150 CNY/m³",
"The trenching volume is trench length × section: excavation volume (m³) = length × section, with one sample per 2 m (sampling intervals ≈ length ÷ 2) and cost ≈ excavation volume × 150 CNY/m³. Use this to prepare the trenching construction plan and budget and control the stripping and channel-sampling workload.",
"Trench length (m)",
"Trench cross-section (m²)",
"💡 Excavation volume = length × section (m³); cost ≈ excavation volume × 150 CNY/m³.",
"📚 In-Depth Analysis: Trenching (Trench/Channel) Sampling Engineering Design",
"Trench specification: design the trench section (bottom width, depth) according to the overburden thickness and the need to expose bedrock",
"Channel layout: place channel samples on the trench wall at a fixed section and sample length to control the representative mineralised interval",
"Engineering budget: count the trenching volume and sample count to estimate the workload and cost",
"Design points: the trench section bottom width is generally ≥0.6-1.2 m and the depth is set to cut through the weathered crust to 0.5 m below bedrock, with side slopes cut by soil type (such as 1:0.5 to 1:1); the channel section is commonly 10×5 cm with a sample length of 1-2 m, cut continuously along the mineralised zone (local reference; must comply with the DZ/T 0078 trenching specification).",
"Example: overburden 2 m thick, designed trench section 1.2×1.0 m (top width × depth), length 100 m → excavation about 120 m³ (1.2×1.0×100); with a trench-wall channel section of 10×5 cm and a sample length of 2 m, one sample per 2 m gives 50 samples over the 100 m trench to control mineralisation.",
"What limits the trench depth?",
"Mainly safety and drainage; trenching is economical at shallow depths (generally <3-5 m), and beyond that a shallow shaft or drilling is preferable. Depths beyond the code limit require support and a safety justification.",
"How do channel samples differ from grab samples?",
"A channel sample is cut continuously along a fixed section and is representative and quantifiable; a grab sample is picked at random, strongly biased and only for reconnaissance. Formal evaluation gives priority to systematic sampling such as channel sampling.",
'About "Trenching (Trench/Channel/Sampling) Design"',
"Trenching (Trench/Channel/Sampling) Design. A free online tool, processed fully client-side, with no data uploaded, protecting your privacy.",
"Trench",
"Channel",
],
'kengtan-chuanmai-yanmai-quyang-fangshi': [
"🪨 Underground Exploration (Cross-cut/Drift/Sampling) Method",
"Estimate the underground exploration excavation volume, muck volume and support quantity from the gallery length and cross-sectional area.",
'📖 View the "Underground Exploration (Cross-cut/Drift/Sampling) Method Guide"',
"Excavation volume = length × section; muck ≈ excavation × 1.3 (loose volume); support ≈ length × 2√section",
"The underground exploration (cross-cut/drift) volume is gallery length × section: excavation volume (m³) = length × section, muck volume ≈ excavation × 1.3 (loose factor), support area ≈ length × 2√section (approximate perimeter × length). Use this to prepare the underground exploration organisation and cost.",
"Gallery length (m)",
"Cross-sectional area (m²)",
"💡 Excavation volume = length × section (m³); muck ≈ excavation × 1.3; support ≈ length × 2√section.",
"📚 In-Depth Analysis: Underground Exploration Engineering (Cross-cut/Drift/Channel Sampling) Layout",
"Cross-cut layout: drive a cross-cut perpendicular to the ore-body strike to cut through the full thickness and determine the thickness and attitude",
"Drift layout: drive a drift along the ore-body strike to control the strike extension and grade variation",
"Channel sampling: cut channels on the gallery wall at a fixed section and control the sample length to obtain representative samples",
"Layout principles: the cross-cut spacing follows the exploration-line spacing (such as 40-80 m) to control thickness; the drift spacing follows the ore-body stability (such as 50-100 m); the channel section is commonly 10×5 cm (width × depth) with a sample length of generally 1-2 m, cut continuously along the ore-body hanging wall and footwall (local reference; must comply with underground exploration specifications such as DZ/T 0078).",
"Example: a vein ore body with a strike length of 200 m and thickness 3 m, with cross-cuts spaced 40 m (5 cross-cuts to expose the thickness) and a drift spacing of 50 m to control the extension; with a gallery-wall channel section of 10×5 cm and a sample length of 2 m, a single sample volume is about 0.001 m³ (10 cm×5 cm×200 cm), representing the average grade of a 2 m ore interval.",
"How do a cross-cut and a drift differ?",
"A cross-cut is perpendicular to the ore-body strike and exposes the full thickness; a drift is parallel to the strike and controls the extension and grade variation. Only together do they reveal both the thickness and the along-strike variation.",
"Why is the channel sample length limited to 1-2 m?",
"An over-long sample hides mineralisation heterogeneity and an over-short one is unrepresentative. 1-2 m is an empirical value balancing representativeness and precision; for very heterogeneous mineralisation it can be shortened to 0.5-1 m and densified.",
'About "Underground Exploration (Cross-cut/Drift/Sampling) Method"',
"Underground Exploration (Cross-cut/Drift/Sampling) Method. A free online tool, processed fully client-side, with no data uploaded, protecting your privacy.",
"Cross-cut",
"Drift",
],
'stats-density-1': [
"📊 Joint (Density/Strike/Filling) Statistics",
"Density/strike/filling",
'📖 View the "Joint (Density/Strike/Filling) Statistics Guide"',
"Count joints along a scanline: enter the length of each survey line and the number of joints on it, compute the linear density (joints/m) and average spacing (m/joint) of each line, and aggregate them into an overall density as an aid to rock-mass integrity assessment; data is processed only locally in the browser and is not uploaded.",
"Linear density λ = joint count / survey-line length (joints/m)　·　average spacing x̄ = 1 / λ = survey-line length / joint count (m/joint)",
"Survey-line data (one per line: survey-line length (m), joint count)",
"Compute joint density",
"📚 In-Depth Analysis: Joint (Density/Strike/Filling) Statistics and Preferred Orientation",
"Joint density: count the joints per unit length on a survey line or outcrop to assess rock-mass integrity",
"Preferred strike: statistically analyse joint strike data to determine the dominant joint set and the rose diagram",
"Slope reference: combine attitude and filling to identify the controlling structural plane, aiding slope stability analysis",
"Algorithm: enter a set of joint data (such as a linear density in /m, or a series of strike angles) to automatically obtain the count n, mean, ",
", minimum, maximum, range, variance and ",
". Linear density = joint count / survey-line length; intact rock is often <1 /m while a crushed zone can reach 5-10 /m (computed locally, no data uploaded).",
"Example: on a slope, five survey lines have joint linear densities (joints/m) 3.2, 4.0, 2.8, 5.1, 3.5 → n=5, mean=3.72 joints/m, median=3.5 joints/m, standard deviation σ=0.84 joints/m, range=2.3 joints/m. A high linear density (>3 joints/m) indicates a fairly fractured rock mass, and the slope must be checked against multiple controlling joint planes.",
"How do the linear density and volumetric joint count convert?",
"The linear density is a 1D measurement; the volumetric joint count Jv (joints/m³) requires 3D statistics. A high linear density generally indicates a large Jv and a low RQD, but a precise Jv requires 3D statistics per the ISRM standard.",
"Does the filling strongly affect stability?",
"Yes. Joints filled with clay or chlorite have a shear strength far lower than unfilled ones and easily soften and slip when wet. The filling type and thickness should be recorded during statistics; this tool only computes density, and stability must be judged together with the material and attitude.",
'About "Joint (Density/Strike/Filling) Statistics"',
"Joint (Density/Strike/Filling) Statistics. A free online tool, processed fully client-side, with no data uploaded, protecting your privacy.",
],
'spacing-4': [
"📏 Exploration (Grid/Spacing/Engineering) Layout",
"Estimate the number of grid engineering works and the grid density from the exploration area and engineering spacing, for exploration layout design.",
'📖 View the "Exploration (Grid/Spacing/Engineering) Layout Guide"',
"Number of works ≈ area ÷ spacing²; grid cell area = spacing²; engineering density = 1 / spacing²",
"In square-grid exploration the engineering spacing d determines the grid cell d². Number of works ≈ exploration area ÷ d², grid density = 1/d² (works per unit area). A larger spacing gives a lower density and sparser control and must match the resource reliability category.",
"Exploration area (m²)",
"Engineering spacing (m)",
"💡 Number of works ≈ area ÷ spacing²; grid cell area = spacing².",
"📚 In-Depth Analysis: Exploration Engineering Grid and Spacing Layout",
"Grid conversion: back-solve the exploration grid density from the controlling engineering spacing (line spacing × point spacing) to match the resource reliability category",
"Engineering layout: determine the trench/borehole spacing by the ore-body shape and stability to control the strike and depth extension",
"Grading reference: different grids correspond to inferred/indicated/measured resources, aiding the justification of exploration level",
"Layout principles: the exploration line spacing and in-line engineering spacing are determined by the ore-body stability and exploration stage, the grid being line spacing × point spacing. Sedimentary/layered deposits generally use a denser regular grid (such as 200×100 m for inferred, 100×50 m for indicated), while vein/irregular deposits use a sparser grid or geostatistics. The spacing must allow the ore body to be correlated continuously between adjacent works (local reference; must comply with solid mineral exploration specifications such as GB/T 33444).",
"Example: a sedimentary iron deposit with an exploration line spacing of 200 m and a borehole spacing of 100 m on each line → grid 200×100 m (2×10⁴ m²/work); raising it to 100×50 m (5×10³ m²/work) increases the engineering density fourfold, raising the resource reliability from inferred to indicated and increasing the workload by about four times.",
"Is a denser grid always better?",
"No. Too dense wastes investment and too sparse fails to reach the reliability category. Choose the minimum feasible grid by deposit type and exploration stage and verify with interpolation error and ore-body continuity rather than simply densifying.",
"What determines the resource estimation category?",
"Mainly the degree of engineering control (spacing, number), sampling quality and geological continuity. The grid is only one quantitative indicator; the final category requires comprehensive expert review, and the result is for reference.",
'About "Exploration (Grid/Spacing/Engineering) Layout"',
"Exploration (Grid/Spacing/Engineering) Layout. A free online tool, processed fully client-side, with no data uploaded, protecting your privacy.",
"Grid",
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

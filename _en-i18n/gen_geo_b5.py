#!/usr/bin/env python3
# geology batch5 (5 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'geology')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'geology')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'analysis-cost-2': [
"⚡ Exploration (Equipment/Efficiency/Cost) Analysis",
"Equipment/efficiency/cost",
"Start by putting the workload and inputs of an exploration project side by side: total cost = shifts × shift rate + mobilisation cost + materials and other direct costs, effective footage = total footage − abandoned footage. Dividing the total cost by the effective footage gives the cost per metre of footage, and dividing the effective footage by the net drilling shifts gives the shift efficiency; a high cost and a low efficiency together mean you spent money but progressed slowly. The abandonment rate is the abandoned footage as a proportion of the total footage and is the cost driver most easily overlooked beyond shift efficiency. All calculations are done locally in the browser and no data is uploaded.",
'📖 View the "Exploration (Equipment/Efficiency/Cost) Analysis Guide"',
"Cost per metre of exploration (CNY/m) = total cost ÷ total effective footage; net drilling efficiency (m/shift) = total effective footage ÷ net drilling shifts",
"Completed boreholes (count)",
"Total drilling footage (m)",
"Abandoned (voided) footage (m)",
"Net drilling shifts (shifts)",
"Shift rate (CNY/shift)",
"Total mobilisation cost (CNY)",
"Materials and other direct costs (CNY)",
"Exploration cost and efficiency analysis",
"📚 In-Depth Analysis: Exploration Equipment Efficiency and Unit Cost Statistics",
"Before project settlement, enter the borehole count, total footage, abandoned footage and shift input of a work area to compute the cost per metre for budget review.",
"Compare the shift efficiency (m/shift) of different rigs and drilling techniques in the same formation to judge whether the formation is hard to drill or the equipment configuration is unreasonable.",
"Use the abandonment rate to separately account for the \"extra cost caused by abandonment\", quantifying the amount lost to hole failure as evidence for changing the technique or adjusting wall-protection measures.",
"Unit cost accounting",
"A work area has 8 completed holes, total footage 2400 m, abandoned 240 m, 60 net drilling shifts at a shift rate of 2800 CNY, mobilisation cost 72000 CNY and other direct costs 108000 CNY. Total cost = 60 × 2800 + 72000 + 108000 = 348000 CNY, effective footage 2160 m, cost per metre of exploration = 348000 ÷ 2160 = 161.11 CNY/m; with zero abandonment it would be 145.00 CNY/m, and the difference is the cost pushed up by this hole failure.",
"Attributing efficiency differences",
"In the same formation, rig A has a shift efficiency of 36.00 m/shift while rig B has only 24.5 m. Look first not at the unit price but at the shift records: if rig B has a similar number of shifts but less net drilling time, it is usually excessive auxiliary time (tripping, waiting for materials or water); if the footage is similar but the hole count is higher, the hole depth may be designed too shallow, causing frequent mobilisation.",
"Using it for budget review",
"The settlement report gives a unit cost of 175 CNY/m while the tool computes 161.11 CNY/m from the entered workload. When a difference appears, first check whether the total investment includes overheads and taxes: this tool only counts shifts, mobilisation and other direct costs, so if the settlement also includes temporary roads and crop compensation, remove them before comparing.",
"Why use the effective footage rather than the total footage?",
"Abandoned footage consumes shifts and materials but produces no effective result; including it in the denominator artificially lowers the unit cost. Using \"total cost ÷ effective footage\" reflects the true cost better, and the cost of the abandoned part can be quantified separately through the tool's \"extra cost caused by abandonment\".",
"What should the shift rate be?",
"Enter the comprehensive shift rate including the crew and fuel/power, consistent with the settlement basis. If the contract prices by rig model tier, enter one tier at a time; with mixed models, compute separately and then weight, which reflects the true cost better than a simple average.",
"Can the result be used directly for a bid?",
"No. The tool only computes cost on a machinery-and-direct-cost basis; a formal bid must also add overheads, profit, risk factors and regional adjustments. It is better used as a pre-bid floor-cost check to identify quotes clearly below the cost line.",
'About "Exploration (Equipment/Efficiency/Cost) Analysis"',
"Exploration (Equipment/Efficiency/Cost) Analysis. A free online tool, processed fully client-side, with no data uploaded, protecting your privacy.",
],
'calc-1': [
"🪨 Rock RQD Index Calculator",
"Compute the rock quality designation (RQD) from core-run lengths and assess the rock mass quality by the Deere grading standard.",
"Rock RQD Index",
"/ Rock RQD Index",
'📖 View the "Rock RQD Index Calculation Guide"',
"RQD = Σ(intact core runs with length ≥ threshold) / total borehole length × 100%",
"Core runs break at fractures and crushed zones; only intact runs not shorter than the threshold (default 100 mm) are counted, and this tool grades the rock mass quality by the Deere standard.",
"Total borehole length L (m)",
"Effective length threshold (mm)",
"Millimetre (mm)",
"Centimetre (cm)",
"Add core run",
"Compute RQD",
"RQD = Σ(intact core runs with length ≥ 100 mm) / total borehole length × 100%",
"Core-run lengths break at fractures and crushed zones",
"Deere grading: 0-25 very poor, 25-50 poor, 50-75 fair, 75-90 good, 90-100 excellent",
"📚 In-Depth Analysis: Rock Quality Designation (RQD) Calculation and Deere Grading",
"Rock mass assessment: enter the length of each intact core run ≥ the threshold to compute RQD and grade it by the Deere standard",
"Slope/foundation-pit design: RQD is a basic input to rock mass classification (RMR/Q)",
"Borehole acceptance: quickly compute RQD on site to judge whether the core recovery quality meets the standard",
"Algorithm: RQD = Σ(effective core runs with length ≥ threshold) / total borehole length × 100% (core runs are converted from the chosen unit mm/cm/m to mm, and the total borehole ",
"length conversion",
" to mm). Deere grading: RQD≥90% excellent, 75-90% good, 50-75% fair, 25-50% poor, <25% very poor. Default effective-run threshold 100 mm (adjustable).",
"Example: total borehole length 2.0 m, core runs (mm) 120, 85, 250, 60, 180, 95, 310, 40, 150, threshold 100 mm → effective runs (≥100 mm) are 120+250+180+310+150=1010 mm, total effective core length 1.010 m, RQD=1010/2000×100%=50.5%, 5 of 9 runs effective, graded \"fair (Fair)\". For a high-quality hole: total length 5.0 m with 10 runs of 400 mm each → effective 4000 mm, RQD=4000/5000×100%=80.0%, graded \"good (Good)\".",
"Is an RQD above 100% normal?",
"Mathematically, if the total effective core length exceeds the total borehole length, >100% appears, usually because core-run lengths are entered twice or ",
"wrong. Check whether the sum of the runs exceeds the total footage; physically the RQD upper limit is 100%.",
"Does a low RQD mean a poor rock mass?",
"RQD mainly reflects the core integrity and is affected by fracture density and orientation; a strongly weathered but intact soft rock can also have a high RQD. Judge together with the RMR and Q systems and field descriptions; RQD alone cannot determine the grade.",
],
'analysis-grade-ore': [
"🔎 Ore Grade and Cut-off Grade Screening",
"Grade screening and ore delineation",
"Ore Grade and Cut-off Grade Screening",
"/ Ore Grade and Cut-off Grade Screening",
'📖 View the "Ore Grade and Cut-off Grade Screening Guide"',
"Sample mean x̄ = Σxᵢ/n; sample standard deviation s = √[Σ(xᵢ−x̄)²/(n−1)]. By the cut-off grade C and industrial grade I, samples are classed as waste (<C), marginal ore (C≤x<I) and ore (≥I).",
"In mineral exploration and mine design, the cut-off grade is the minimum standard for delineating an ore body and separating ore from waste; the industrial grade (minimum industrial grade) distinguishes rich ore from marginal ore. This tool screens automatically by the entered thresholds, counting the number and proportion of each class, with the whole-sample mean/median/standard deviation characterising the grade distribution. Results are for techno-economic evaluation reference only.",
"Sample grade series (%, comma- or newline-separated)",
"Cut-off grade C (%)",
"Industrial grade I (%)",
"Compute and screen",
"📚 In-Depth Analysis: Ore Grade and Cut-off Grade Screening",
"Ore delineation and body division: given a cut-off grade, quickly screen waste, marginal ore and ore samples, counting each class and its proportion to support ore-body delineation.",
"Ore blending and grade control: compare the grade distribution of samples from different mining areas/levels (mean, ",
"), providing a basis for ore blending and feed-grade control.",
"Techno-economic evaluation: use the industrial grade to distinguish rich ore from marginal ore, and assess mining economics together with reserves and market prices.",
"Worked example (10 samples, C=1.0%, I=1.5%)",
"Grade series (%): 1.2, 1.5, 0.9, 2.1, 1.8, 1.3, 0.8, 1.6, 1.1, 1.4. Mean x̄≈1.37%, median 1.35%, ",
"s≈0.39%; ≥ cut-off grade (1.0%) 9 samples (90%), of which ≥ industrial grade (1.5%) 4 (40%), marginal ore 5, waste 1; the subset ≥ cut-off grade has mean ≈1.48%.",
"What is the difference between the cut-off grade and the industrial grade?",
"The cut-off grade is the minimum grade standard for delineating an ore body and separating ore from waste; the industrial grade (minimum industrial grade) distinguishes rich ore from marginal ore and is usually higher than the cut-off grade. Together they determine the boundary and economics of the mineable reserve.",
"Why use the sample standard deviation rather than the ",
"population variance",
"The samples are a limited sampling of the ore body, so the sample standard deviation with n−1 better estimates the population dispersion unbiasedly; using the population variance with n alone underestimates the fluctuation, especially with few samples.",
'About "Ore Grade and Cut-off Grade Screening"',
"Ore Grade and Cut-off Grade Screening. A free online tool, processed fully client-side, with no data uploaded, protecting your privacy.",
"e.g. 1.2,1.5,0.9,2.1,1.8",
],
'analysis-32': [
"📊 Fold (Anticline/Syncline/Axial Plane) Analysis",
"Fold geometry and axial-plane attitude",
'📖 View the "Fold (Anticline/Syncline/Axial Plane) Analysis Guide"',
"Enter the attitude of the two limbs (dip direction and dip angle). From the limb normals n₁ and n₂, the hinge (fold axis) = n₁×n₂, and the axial-plane normal is taken as n₁−n₂ orthogonalised to the hinge; then the axial-plane dip direction and dip angle are converted. The interlimb angle = 180° − arccos(n₁·n₂) is used to classify tight/close/open/gentle; the axial-plane dip angle distinguishes upright/inclined/recumbent.",
"Limb attitudes (each line \"limb name,dip direction,dip angle\", at least two lines)",
"West limb,270,40\nEast limb,90,40",
"Solve fold geometry",
"📚 In-Depth Analysis: How to Solve Fold Geometry and Axial-Plane Attitude",
"In geological mapping and field interpretation, the hinge (fold axis) and axial-plane attitude are back-solved from the measured limb attitudes to determine the spatial attitude of the fold.",
"In structural geology teaching, the limb attitudes demonstrate the axial-plane difference between symmetric and asymmetric folds and the tightness corresponding to the interlimb angle.",
"Before drawing a section, check the axial-plane dip direction and angle to keep the fold shape on the section consistent with the measured data.",
"Asymmetric fold trial",
"With the two limbs entered as \"West limb,270,30\" and \"East limb,90,60\", the interlimb angle is 90.0°, the axial-plane dip angle 75.0°, the axial-plane dip direction 90.0° and the hinge horizontal (plunge 0.0°); the 30.0° difference in limb dip marks it as asymmetric, the axial plane as inclined and the tightness as open.",
"How many input lines are needed?",
"At least two; the tool takes the first two lines as the limbs. Parallel limb attitudes cannot form a fold and a prompt is shown.",
"What is the relation between the interlimb angle and the limb dip angles?",
"When the two limb dip directions are exactly opposite, the interlimb angle equals 180° minus the sum of the limb dip angles; when the directions are not orthogonal the tool computes the normal-angle precisely.",
"Can it tell an anticline from a syncline?",
"The limb attitudes alone cannot distinguish them; the age relation between the core and limb strata is needed. This tool only solves the geometry, outputting the axial-plane attitude, interlimb angle and symmetry as geometric parameters.",
'About "Fold (Anticline/Syncline/Axial Plane) Analysis"',
"Fold (Anticline/Syncline/Axial Plane) Analysis. A free online tool, processed fully client-side, with no data uploaded, protecting your privacy.",
"How to use the Fold (Anticline/Syncline/Axial Plane) Analysis",
"What does the Fold (Anticline/Syncline/Axial Plane) Analysis do?",
"A Fold (Anticline/Syncline/Axial Plane) Analysis tool. Enter the strata attitude and geometric parameters to determine the fold type (anticline/syncline) and estimate the axial-plane attitude, for geological structure teaching and field interpretation reference.",
"How do I use the Fold (Anticline/Syncline/Axial Plane) Analysis?",
"What scenarios is the Fold (Anticline/Syncline/Axial Plane) Analysis suitable for?",
"West limb,270,30",
],
'dip-strike': [
"📐 Strike and Dip Calculator",
"Compute strata attitude by the three-point method: enter the coordinates and elevations of three points on the same rock surface to find the strike, dip direction and dip angle.",
'📖 View the "Strike and Dip Calculation Guide"',
"Strike/dip = survey conversion",
"Point A",
"East coordinate x (m)",
"North coordinate y (m)",
"Elevation z (m)",
"Point B",
"Point C",
"Compute attitude",
"Coordinate system: x=east, y=north, z=elevation (upward). The three points must be non-collinear and on the same rock surface. The strike is the azimuth of the horizontal line, the dip direction is the direction of maximum dip, and the dip angle is the angle between the stratum and the horizontal plane.",
"📚 In-Depth Analysis: Three-Point Method for Strata Attitude (Strike/Dip Direction/Dip Angle)",
"Field interpretation: given the coordinates and elevations of three points on the same surface, find the surface normal to obtain the attitude",
"Section preparation: use the attitude for geological sections and joint statistics",
"Teaching demonstration: move the three points to observe changes in strike/dip",
"Algorithm: take three points P1, P2, P3 (x,y,z), form the vectors v1=P2−P1 and v2=P3−P1, and the normal n=v1×v2 made upward (C>0). Dip dip=arccos(C/|n|); dip direction azimuth dipDir=atan2(A,B) (east and north components, reduced to 0-360°); strike=(dipDir−90) mod 360 (equivalent to strike+180). Collinear points or a horizontal plane give no definite attitude.",
"Example: P1(0,0,100), P2(50,0,80), P3(0,40,90) → n=(800,500,2000), |n|=2211.33; dip=arccos(2000/2211.33)=25.3°, dip direction dipDir=atan2(800,500)=58.0°, strike=(58.0−90+360)%360=328.0°. The attitude is written 328.0°∠25.3° (dip direction NE). If P1(0,0,50), P2(100,0,40), P3(100,100,30) → strike=315.0°, dipDir=45.0°, dip=8.0°, a gently dipping near-horizontal bed.",
"Must the three points be strictly on the same surface?",
"They must lie on the same structural surface; otherwise the computed normal is the plane fitted to the three points rather than the true surface. If the points are offset by a fault or belong to different strata interfaces, the result is distorted; confirm the continuity of the horizon on site before using it.",
"Why are two strike values given?",
"The strike is the direction of the line of intersection between the stratum and the horizontal plane, and a line has two opposite azimuths (differing by 180°), so strike and strike+180 are equivalent; what actually indicates the \"dip direction\" is the dip direction dipDir (the downdip azimuth), which differs from the strike by 90°.",
'About "Strike and Dip Calculator"',
"Strike and Dip Calculator is an online tool in the scientific research field. A scientific research tool that uses standard scientific formulas for accurate calculation.",
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

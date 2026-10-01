#!/usr/bin/env python3
# optical batch5 (5 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'optical')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'optical')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'convergence-near-point': [
"📏 Convergence (Collection) Near Point Distance Calculator",
"Compute the convergence demand from interpupillary distance and fixation distance, and assess the near point of convergence (NPC) and convergence function",
"Convergence Near Point Distance Calculator",
"/ Convergence Near Point Distance Calculator",
'📖 View the "Convergence (Collection) Near Point Distance Calculator User Guide"',
"Near point convergence prism demand P(Δ) = interpupillary distance (cm) ÷ target distance (m); P = PD (cm) ÷ distance (m); use it to assess whether positive/negative relative convergence and the near point of convergence (NPC) meet the standard.",
"Fixation distance (cm)",
"Measured NPC break point (cm, optional)",
"Convergence demand (prism diopters) = PD (cm) / fixation distance (m) = PD (mm) / fixation distance (cm) × 10",
"Example: PD = 62 mm, distance 40 cm → 6.2 / 0.4 = 15.5Δ",
"Normal NPC: break point ≤ 5-10 cm, recovery point ≤ 7-12 cm. NPC > 10 cm suggests convergence insufficiency.",
"📋 Convergence Demand Reference by Distance",
"Convergence demand (Δ)",
"A near point of convergence that is too far (> 10 cm) suggests convergence insufficiency, often seen with reading fatigue and diplopia; too near (< 3 cm) may indicate over-convergence. Evaluate together with vergence function.",
"This tool computes a rough convergence demand and does not account for accommodation-convergence linkage or heterophoria. Clinical NPC testing should use an accommodative target/penlight; the result is for reference only.",
"📚 In-Depth Analysis: Near Point of Convergence Measurement",
"Measure the NPC (near point of convergence) to assess convergence function.",
"A receded NPC suggests convergence insufficiency.",
"Track the effectiveness of vision training.",
"Normal values",
"The near point of convergence (NPC) is usually ≤ 10 cm (some use 5-8 cm); if > 15 cm it is receded, suggesting convergence insufficiency with reading fatigue and double vision.",
"Recovery point",
"Measure both the break point (diplopia) and the recovery point (return to single vision); the recovery point should be clearly nearer than the break point. A large difference suggests instability.",
"What to do about a receded NPC?",
"Start with convergence training (pen-tip push-up / prism); if ineffective and symptoms persist, base-in prism can relieve it.",
"How is it related to convergence insufficiency?",
"A receded NPC is a core sign of convergence insufficiency, often with low AC/A and exophoria; comprehensive assessment is needed.",
'About the "Convergence Near Point Distance Calculator"',
"Compute the convergence demand from interpupillary distance and fixation distance, and assess the near point of convergence and convergence function.",
"Real-time convergence demand calculation",
"Evaluation of the measured NPC value",
"Multi-distance reference table",
"Convergence function assessment",
"Reading fatigue screening",
"Convergence insufficiency diagnosis",
"Vision training reference",
"Convergence near point distance calculator: compute the convergence demand from interpupillary distance and distance, and assess the near point of convergence and convergence function. A professional medical tool based on authoritative medical standards, for reference only.",
],
'calc-47': [
"🧮 Aspheric (Spherical Aberration) Correction Calculator",
"Enter the refractive index, radius of curvature, clear semi-aperture and conic constant (K) to compute third-order spherical aberration and the optimal conic constant (infinite object distance, single refracting surface)",
'📖 View the "Aspheric (Spherical Aberration) Correction Calculator User Guide"',
"Spherical aberration LSA = (n−1)·h² / (2·n·R) · (1 + k/n²); k is the conic constant",
"Aspheric correction relative to spherical aberration: the spherical contribution is (n−1)h²/(2nR), multiplied by (1+k/n²); k=0 reduces to a spherical surface, k=−n² is the optimal compensation.",
"Clear semi-aperture h (mm)",
"Conic constant K",
"✨ Apply optimal K",
"📐 Conic Surface Data (at different aperture positions)",
"📊 Transverse Aberration Curve (relative to the paraxial focal plane)",
"Vertical axis = relative aperture (hᵢ/h), horizontal axis = transverse aberration TRA (μm); blue is spherical (K=0), orange is the current conic (K)",
"💡 Third-order spherical aberration formula (infinite object distance, single refracting surface air→glass): longitudinal spherical aberration LSA = (n−1)·h² / (2nR) × (1 + K/n²); optimal conic constant K_opt = −n²; transverse aberration TRA = LSA × (h/f), f = nR/(n−1)",
"Applicable to a single refracting surface at infinite object distance (parallel incident light) approximation, using third-order aberration theory",
"Conic constant K: K=0 spherical, K=−1 parabolic, K<−1 hyperbolic, −1<K<0 ellipsoidal",
"Conic equation: z = c·r² / (1 + √(1 − (1+K)·c²·r²)), where c = 1/R",
"📚 In-Depth Analysis: Aspheric (Spherical Aberration) Correction and the Optimal Conic Constant",
"Single refracting surface design: according to",
"refractive index",
"derive the optimal conic constant K and use the aspheric surface to cancel third-order spherical aberration.",
"Parameter check: compare the longitudinal spherical aberration and marginal transverse aberration of the spherical surface (K=0) and the current K.",
"Manufacturing communication: hand off the optimal K and sag to the aspheric fabricator as the surface form target.",
"Algorithm: paraxial focal length f = nR/(n−1); spherical longitudinal spherical aberration LSA = (n−1)h²/(2nR); after applying conic constant K, LSA = LSA_spherical×(1+K/n²); setting the bracket to zero gives the optimal conic constant K = −n²; marginal transverse aberration TRA = LSA×(h/f); F-number = f/(2h), NA = h/f. Conic type: K<−1 hyperboloid, K=−1 paraboloid, −1<K<0 ellipsoid, K>0 oblate ellipsoid.",
"Example: n=1.5, R=100 mm, h=10 mm → f = 1.5×100/0.5 = 300 mm, F/15, NA=0.0333; spherical (K=0) longitudinal spherical aberration LSA = 0.5×100/(2×1.5×100) = 0.1667 mm = 166.7 μm; with the optimal K = −n² = −2.25 the aberration term goes to zero and the marginal transverse aberration drops sharply.",
"What surface forms are K = 0 and K = −1 respectively?",
"K=0 is spherical, K=−1 is parabolic; −1<K<0 is ellipsoidal (most common for reflecting surfaces at infinite object distance), K<−1 is hyperbolic, K>0 is oblate ellipsoidal. This tool uses K = −n² as the optimal value that nulls third-order spherical aberration.",
"Why doesn't spherical aberration change linearly with aperture?",
"The longitudinal magnitude of third-order (Seidel) spherical aberration is proportional to the square of the clear semi-aperture, and the transverse aberration to the cube; doubling the aperture roughly quadruples the longitudinal spherical aberration. So stopping down the aperture is very effective, while aspheric surfaces suppress spherical aberration even at large apertures.",
'About the "Aspheric (Spherical Aberration) Correction Calculator"',
"Enter the refractive index, radius of curvature, clear semi-aperture and conic constant to compute the third-order longitudinal spherical aberration of a single refracting surface, the optimal conic constant, the marginal sag and the aspheric departure, and display a sag table at different aperture positions and a transverse aberration curve.",
"Uses third-order aberration theory to compute the longitudinal spherical aberration of spherical and conic surfaces",
"One-click application of the optimal conic constant K = −n² to eliminate third-order spherical aberration",
"Displays the conic sag table and aspheric departure",
"Visualizes the transverse aberration curve, comparing spherical and conic surfaces",
"Aspheric lens design and optimization",
"Optical system spherical aberration assessment",
"Conic constant selection and surface form design",
"Optics teaching and aberration analysis",
],
'report-cost-profit-1': [
"💰 Financial (Cost/Profit/Report) Accounting",
"Cost/Profit/Report",
"The per-pair cost of making glasses must be fully accounted for: beyond the lens, frame and processing fee, consumables such as cleaning solution, screws and nose pads, plus packaging, should also be counted under other materials; otherwise the gross margin rate will be overestimated. Monthly fixed costs are the parts that do not change with volume, such as rent, staff wages, depreciation and amortization; dividing them by the gross margin per pair gives the minimum number of pairs you must make each month to avoid a loss. For a promotional price, enter it separately as the selling price and then look at the break-even volume to see directly how much the discount amplifies the required volume. All calculations are done in the local browser and no data is uploaded.",
'📖 View the "Financial (Cost/Profit/Report) Accounting User Guide"',
"Gross margin per pair = selling price − (lens + frame + processing + other materials); break-even volume = monthly fixed costs ÷ gross margin per pair",
"Lens cost (CNY/pair)",
"Frame cost (CNY/pair)",
"Processing fee (CNY/pair)",
"Other material cost (CNY/pair)",
"Package price (CNY/pair)",
"Monthly sales volume (pairs)",
"Monthly fixed costs (CNY)",
"Glasses profit accounting",
"📚 In-Depth Analysis: Glasses Cost and Profit Accounting",
"From the purchase costs of lens, frame, processing and other materials, combined with the package price, compute the gross margin per pair and the true",
"Before running a promotion, enter the discounted price as the selling price to directly see the gross margin and",
"break-even",
"changes in volume, and judge whether the discount level is still acceptable.",
"In the monthly review, use the actual monthly volume and fixed costs to compute operating profit and margin of safety, and check whether the incremental volume from promotions truly restores profit.",
"Per-pair accounting",
"Lens cost 150 CNY, frame 220 CNY, processing 50 CNY, other materials 30 CNY, total per-pair cost 450 CNY; with a package price of 760 CNY the gross margin per pair = 310 CNY, gross margin rate = 310 ÷ 760 ≈ 40.79%. Looking only at the lens markup clearly overestimates profit; adding all four cost categories shows the true gross margin potential.",
"Is it still viable after a discount?",
"With the same data at a 20% discount, the price drops to 608 CNY, the gross margin per pair to 158 CNY, the gross margin rate to about 25.99%, and the break-even volume rises from 77.42 to 24000 ÷ 158 ≈ 151.9 pairs. In other words, after discounting you must sell nearly twice as many per month to maintain the same profit, so always compute this before running a promotion.",
"The real cost of a promotion",
'Combining the two examples above: net profit drops from 5450 CNY to about −1210 CNY (based on 95 pairs and 24000 CNY fixed costs). If the incremental volume from the promotion cannot cover the gap from 78 to 152 pairs, the promotion reduces profit on net, which is why many stores are "busy with promotions but not profitable".',
"How should the gross margin rate be calculated?",
"Gross margin rate = (selling price − total cost) ÷ selling price × 100%, where the total cost must include the lens, frame, processing fee and other materials such as cleaning solution, screws and nose pads. Computing the markup based only on the lens purchase price systematically overestimates the gross margin, which is the most common pitfall in pricing.",
"Does discounting always cause a loss?",
"Not necessarily; the key is whether the discounted price is still above the per-pair cost. In the example above, after a 20% discount the per-pair gross margin of 158 CNY is still positive, so it can be sold in theory; the real problem is that the break-even volume is pushed to about 152 pairs, and if the incremental volume does not reach that scale, the books turn from profit to loss.",
"How should optometry and after-sales labor be included?",
'If the wages of optometrists and technicians do not vary with volume, they should be included in "monthly fixed costs" and covered together with rent and depreciation via the break-even volume; if paid per piece, they belong in the other-material item of the per-pair cost. Mixing them together leads to an incorrect break-even volume.',
"Can the result be used directly for quoting?",
"It can serve as a floor-price reference, but a formal quote should also add equipment depreciation, the loss/scrap rate and a positioning factor for the surrounding business district. The value of the tool is in giving a clear profit-and-loss boundary and identifying promotions that fall clearly below the cost line.",
'About the "Financial (Cost/Profit/Report) Accounting"',
"Financial (Cost/Profit/Report) Accounting. A free online tool processed purely on the front end; data is not uploaded, protecting your privacy and security.",
],
'aspheric-design': [
"🧮 Aspheric Lens Spherical Aberration Correction Calculator",
"Based on third-order aberration theory, compute the longitudinal spherical aberration of a spherical lens and the aspheric conic constant K needed to eliminate spherical aberration",
'📖 View the "Aspheric Lens Spherical Aberration Correction Calculator User Guide"',
"Lens aperture (mm)",
"Radius of curvature R (mm) = 1000×(n−1) / F",
"Semi-aperture h (mm) = aperture / 2",
"Longitudinal spherical aberration LSA (mm) = h²×n² / [2×R×(n−1)²] (spherical surface, third-order approximation)",
"Aplanatic conic constant K = −n² / (n−1)² (single refracting surface, parallel incident light)",
"This tool uses a third-order aberration approximation; real aspheric design must also consider coma, field curvature and other factors. The result is for teaching and preliminary design reference only.",
"📚 In-Depth Analysis: Aspheric Lens Design",
"Use an aspheric surface to reduce edge aberration and thickness.",
"Thinner, less distorted lenses for high prescriptions.",
"Compare spherical and aspheric edge aberration.",
"Thinner and less distortion",
"A −6.00D spherical lens has a thick edge and makes objects appear smaller; an aspheric lens uses a gradual curvature change to make the edge about 15% thinner with less peripheral distortion, improving appearance and comfort.",
"Aberration improvement",
"Aspheric surfaces reduce aberrations from clearly visible coma at the edge to the paraxial level, giving a clearer wide-angle field, especially for high",
"refractive index",
"thin lenses, which rely more on aspheric surfaces.",
"Are aspheric lenses thinner?",
"At the same power and refractive index the edge is thinner and flatter; the advantage is clear at high powers, while the difference is small at low powers.",
"Are aspheric lenses hard to adapt to?",
"Peripheral vision differs slightly; most people adapt within a few days. Switching from spherical to aspheric requires a short period to rebuild spatial perception.",
'About the "Aspheric Lens Spherical Aberration Correction Calculator"',
"Compute the longitudinal spherical aberration of a spherical lens and the aspheric conic constant needed to eliminate it, assisting aspheric lens design and teaching.",
"Real-time third-order spherical aberration calculation",
"Automatic solution of the conic constant K",
"Comparison across refractive indices",
"Transparent, traceable formulas",
"Aspheric lens design reference",
"Ophthalmic optics teaching demonstration",
"Spherical aberration assessment and correction scheme",
"Lens base curve optimization",
"Aspheric spherical aberration correction calculator: compute the lens spherical aberration and the aspheric coefficient (conic constant K), assisting aspheric lens design. A professional medical tool based on authoritative medical standards, for reference only.",
],
'frame-pupillary': [
"👓 Frame Size and Pupillary Distance Calculator",
"From the lens rim width A, bridge width DBL and pupillary distance PD, compute the per-eye decentration and the minimum required lens diameter",
'📖 View the "Frame Size and Pupillary Distance Calculator User Guide"',
"Per-eye decentration = (A + DBL) / 2 − PD / 2",
"Lens rim width A (mm)",
"Bridge width DBL (mm)",
"Maximum effective diameter ED (mm, optional)",
"Geometric center distance = A + DBL (distance between the geometric centers of the two rims)",
"Per-eye decentration = (A + DBL) / 2 − PD / 2; a positive value means decentration toward the nose (in), a negative value toward the temple (out)",
"Minimum uncut lens diameter = ED + 2×|decentration| + 2 mm edging allowance",
"Excessive decentration requires a larger diameter lens or a custom lens; in practice the astigmatism axis and prism decentration must also be considered. The result is a reference for lens processing.",
"📚 In-Depth Analysis: Frame and Pupillary Distance Fitting",
"Set the optical center distance according to the binocular pupillary distance when making glasses.",
"The frame's geometric center often differs from the pupillary distance and requires decentration.",
"Decentration error causes a prismatic effect.",
"Decentration calculation",
"Pupillary distance PD=64 mm, frame geometric center distance 70 mm → each lens decentered inward (70−64)/2=3 mm; if the prescription is not decentered it produces base-out prism.",
"Impact of error",
"Each 1 mm of decentration at −3.00D produces 0.3Δ of prism; beyond 2 mm there is noticeable image displacement, so precise decentration or a narrower frame is required.",
"Why must the frame match the pupillary distance?",
"If the optical center is not aligned with the pupil, a prismatic effect causes eye strain and oblique viewing; when the difference between PD and frame distance is large you must decenter or change the frame.",
"Should the monocular pupillary distance also be measured?",
"Yes. Splitting the binocular PD evenly is not always correct, especially with facial asymmetry; for progressive lenses the monocular PD and height must be measured.",
'About the "Frame Size and Pupillary Distance Calculator"',
"From the rim width, bridge width and pupillary distance, compute the per-eye decentration and the minimum required lens diameter, assisting frame selection and processing.",
"Per-eye decentration calculation",
"Automatic minimum lens diameter calculation",
"Decentration direction determination",
"Frame selection and fitting",
"Lens diameter ordering",
"Processing decentration positioning",
"Large-frame, small-PD assessment",
"Frame size and pupillary distance calculator: compute the decentration and minimum lens diameter from the rim width, bridge width and pupillary distance. A professional medical tool based on authoritative medical standards, for reference only.",
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
        if it.get('src_diff') and it.get('zh_src'):
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
    out = {'slug': slug, 'industry': 'optical', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

for slug, en_list in EN.items():
    write(slug, build(slug, en_list))

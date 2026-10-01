#!/usr/bin/env python3
# optical batch4 (5 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'optical')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'optical')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'progressive-corridor': [
"📏 Progressive Corridor Length Calculator",
"Recommend the progressive corridor length from the near addition ADD and the lens rim height, and check the minimum fitting height",
'📖 View the "Progressive Corridor Length Calculator User Guide"',
"Near addition ADD (D)",
"Lens rim height B (mm)",
"Pupillary height (mm, pupil center to lower rim)",
"Standard corridor (~14 mm)",
"Short corridor (~11 mm)",
"Long corridor (~17 mm)",
"📋 Corridor Length Selection Reference",
"Corridor type",
"Minimum rim height",
"Ultra-short corridor",
"Small frames, first-time wearers",
"Short corridor",
"Mid-low ADD, small frames",
"Standard corridor",
"General, mid-high ADD",
"Long corridor",
"High ADD, high reading demand",
"Required minimum rim height = pupillary height + near zone margin (≈5 mm); the corridor length is determined by the design (short/standard/long) and the near addition",
"ADD≥2.50D recommends a standard corridor (14 mm), ADD≥3.00D recommends a long corridor (17 mm), and the near zone center must leave a margin of about 5 mm.",
"Corridor length = the distance from the fitting cross (pupil center) to the near zone center (near test circle).\n      The near zone needs about 5 mm of height to accommodate the reading field, so the minimum fitting height must satisfy pupillary height + corridor length + a 5 mm margin.",
"This tool is based on general progressive design empirical values; different brands differ in design parameters, so for actual lens selection refer to the manufacturer's corridor length specification.",
"📚 In-depth: Progressive Corridor Length",
"Determine the corridor length (14/17 mm) by design and check the pupillary height.",
"The pupillary height must be ≥ corridor length + near zone margin.",
"Progressive lens fitting compatibility.",
"Height verification",
"Design corridor 17 mm, pupillary height PH=22 mm → near zone center distance from lower rim = 22−17=5 mm, meeting the ≥5 mm reading zone; assembly qualified.",
"Handling insufficiency",
"PH=20, corridor 17 → near zone only 3 mm, too short and the reading zone is cut; switch to a short corridor design or raise the frame.",
"Is a longer corridor better?",
"A long corridor gives a flatter field but places the near zone lower and needs a tall frame; a short corridor reaches near vision easily but has a narrow intermediate distortion band; choose by wearing habits.",
"How is the pupillary height determined?",
"At fitting, measure the monocular pupil center to the lower rim; progressive lenses need sufficient height to accommodate the corridor and near zone.",
'About the "Progressive Corridor Length Calculator"',
"Recommend the progressive corridor length from the near addition ADD and lens rim height and check the minimum fitting height, supporting progressive multifocal lens selection.",
"Intelligent corridor length recommendation",
"Automatic fitting height verification",
"Visual corridor diagram",
"Comparison of multiple design types",
"Progressive lens selection and fitting",
"Near addition and corridor trade-off",
"Fitting height verification",
"Multifocal Progressive Corridor Length Calculator; compute the progressive corridor length and minimum fitting height from the ADD near addition and rim height. A professional medical tool based on authoritative medical standards, for reference only.",
],
'frame-tilt': [
"📐 Frame Pantoscopic Tilt Adjuster",
"Compute the effect of the pantoscopic tilt on the optical center position and the adjustment amount",
'📖 View the "Frame Pantoscopic Tilt Adjuster User Guide"',
"Frame pantoscopic tilt compensation: each 1° of tilt requires lowering the optical center by about 0.5 mm; the adjusted pupillary height = original pupillary height + tilt × 0.5; the decentration prism effect P(Δ) = c(cm) × D is estimated by Prentice's rule.",
"Tilt (°)",
"Pupillary height (mm)",
"📋 Tilt Reference Standards",
"Tilt",
"Optical center lowering",
"Too small",
"Increase the tilt",
"Too large",
"Decrease appropriately",
"Excessive",
"Adjust the frame",
"For each 1° increase in tilt, the optical center must be lowered by about 0.5 mm to keep the visual axis through the lens optical center, avoiding prism effects and aberrations.",
"📐 Frame Adjustment Points",
"Pantoscopic tilt",
"The angle between the lens front surface and the vertical plane, normally 5°-9°. The tilt makes the lens conform better to the facial contour and expands the lower field of view.",
"Face form angle",
"The angle between the planes of the left and right rims, normally 170°-180°. Too large or too small causes pupillary distance deviation.",
"Vertex distance",
"The distance from the lens back surface to the corneal vertex, standard 12-14 mm. It affects the effective power, and high powers need attention for compensation.",
"Tilt adjustment requires considering the wearer's facial features and lens type; high astigmatism and progressive lenses are more sensitive to tilt.",
"📚 In-depth: Frame Pantoscopic Tilt",
"Compute the optical center lowering by tilt to keep the visual axis aligned.",
"A tilt of 5-9° is appropriate.",
"Progressive lenses are more sensitive to tilt.",
"Optical center lowering",
"Tilt 8° → optical center lowering = 8×0.5=4 mm; without the corresponding lowering, the line of sight is too high, producing prism and aberration.",
"Recommended range",
"A tilt <5° shifts the field upward, and >9° increases aberration and protrudes the lens; 5-9° balances lower reading and aesthetics.",
"What is the tilt for?",
"Makes the lens more perpendicular to the visual axis, optimizes the lower reading area (especially for progressives) and improves aesthetics and fit.",
"How is the tilt measured?",
"The angle between the lens plane and the facial vertical; measure with a fitting instrument or protractor; for progressive fitting it must be precise and the optical center shifted accordingly.",
'About the "Frame Pantoscopic Tilt Adjuster"',
"Compute the effect of the frame pantoscopic tilt on the optical center position, determine the optical center lowering and ensure the visual axis passes through the lens optical center.",
"Tilt-optical center lowering calculation",
"Prism effect assessment",
"Visual angle diagram",
"Frame adjustment reference standard",
"Frame adjustment and fitting",
"Progressive lens positioning",
"Optical center positioning",
"Frame Pantoscopic Tilt Adjuster; compute the effect of tilt on the optical center position, with each degree of tilt requiring a 0.5 mm optical center lowering. A professional medical tool based on authoritative medical standards, for reference only.",
],
'polarized-axis': [
"👓 Polarized Lens Axis Compensator",
"Compute the tilt-induced cylinder and effective axis change from the frame pantoscopic tilt and face form (wrap)",
'📖 View the "Polarized Lens Axis Compensator User Guide"',
"Sphere power SPH (D)",
"Original cylinder CYL (D, optional)",
"Original axis AXIS (°, optional)",
"Pantoscopic tilt (°)",
"Face form wrap (°)",
"Tilt-induced cylinder (Martin's rule, third-order approximation):",
"Induced cylinder C = D × tan²(θ), where D is the equivalent sphere power and θ the tilt angle",
"Sphere increment ΔS = D × tan²(θ) / 3",
"The pantoscopic tilt produces a 90°-axis cylinder (vertical meridian); the face form produces a 180°-axis cylinder (horizontal meridian).",
"📋 Standard Fitting Angles",
"Standard range",
"Pantoscopic tilt",
"Too large induces a vertical cylinder and increases aberration",
"Face form wrap",
"Too large induces a horizontal cylinder and peripheral prism",
"Vertex distance",
"Affects the effective power",
"Sports eyewear face form often reaches 8-15°, requiring pre-compensation of the cylinder and axis in the prescription, otherwise vision drops and discomfort occurs after wearing.",
"This tool uses a third-order tilt aberration approximation; actual compensation must consider vertex distance and the lens-eye relationship, and for high-curvature sports lenses an optometrist should customize the compensation prescription.",
"📚 In-depth: Polarized Axis Induction",
"Compute the induced cylinder axis from the frame pantoscopic/wrap angle.",
"Polarized lens assembly axis compensation.",
"Avoid conflict between the polarization and astigmatism axes.",
"Induced axis",
"Given the frame pantoscopic angle (panto) and wrap, the induced cylinder axis = atan2(panto, wrap); e.g. panto=10, wrap=17 → axis ≈30.5°, and assembly compensates accordingly.",
"Conflict avoidance",
"If the polarization vibration direction is nearly perpendicular to the astigmatism axis, unusable glare arises; adjust the axis or choose a non-polarized design.",
"Is the polarization axis important?",
"Yes. A wrong axis weakens the anti-glare effect and can even conflict with the astigmatism lens causing blurred vision; wraparound lenses are more sensitive.",
"What is the induced axis?",
"Frame bending makes incident light produce an equivalent cylinder; the equivalent axis is the induced axis, which must be included in the prescription.",
'About the "Polarized Lens Axis Compensator"',
"Compute the tilt-induced cylinder and effective axis change from the frame pantoscopic tilt and face form, aiding fitting compensation for sports eyewear and polarized lenses.",
"Tilt-induced cylinder calculation",
"Pantoscopic tilt and face form composition",
"Axis change estimation",
"Compensation prescription advice",
"Sports eyewear fitting compensation",
"Custom large face-form polarized lenses",
"Tilt aberration assessment",
"Fitting angle adjustment",
"Polarized Lens Axis Compensator; compute the tilt-induced cylinder and effective axis change from the frame pantoscopic tilt and face form. A professional medical tool based on authoritative medical standards, for reference only.",
],
'checker-stress': [
"✅ Photoelastic Stress Analysis",
"Enter the polarized light interference fringe order and the material fringe value to compute the birefringence stress difference of a transparent part (glass/plastic/optical element), automatically determine the stress grade and give a quality evaluation.",
"Polarized Light (Stress) Inspection",
"/ Polarized Light (Stress) Inspection",
'📖 View the "Photoelastic Stress Analysis User Guide"',
"Glass internal stress (optical path difference method): principal stress difference σ = N × f ÷ d, where N is the photoelastic fringe number, f the stress-optic constant (nm/cm·MPa) and d the plate thickness (cm); a stress difference below 5 MPa is very small, 5-15 moderate, above 15 large (tempered glass needs over 90 MPa).",
"Borosilicate glass (f=14.5 MPa·mm/order)",
"Soda-lime glass (f=12.0 MPa·mm/order)",
"PMMA acrylic (f=7.0 MPa·mm/order)",
"PC polycarbonate (f=5.5 MPa·mm/order)",
"Custom material fringe value",
"Material fringe value f (MPa·mm/order)",
"Fringe order N (order)",
"Optical path thickness d (mm)",
"Stress-optic law: σ₁ - σ₂ = N × f / d (MPa)",
"The fringe order N is read via a polarized light interferometer (crossed polariscope)",
"Tempered glass residual stress: surface compressive stress should be >90 MPa, center tensile stress <45 MPa",
"Optical element birefringence: precision grade <10 nm/cm, ordinary grade <50 nm/cm",
"📚 In-depth: Lens Stress Inspection",
"After assembly, view stress spots under a polariscope to judge assembly qualification.",
"Excessive stress easily chips the edge/causes distortion.",
"Accept lens assembly quality.",
"Stress interpretation",
"No color fringes/local bright spots under a polariscope = qualified; obvious color fringes at the edge = over-tight clamping, requiring looser reassembly to avoid edge chipping from long-term stress.",
"Stress grades 0-3: ≤1 qualified, 2 needs re-inspection, 3 unqualified; plastic frames are more prone to over-clamping than metal frames, so torque must be controlled.",
"Why check stress?",
"Over-tight assembly produces birefringence and distortion and can crack the lens over time, especially on stress-sensitive PC/high-index lenses.",
"Can I see it myself?",
"It requires a polarizer + standard light source and is invisible to the naked eye; stores use a stress meter for objective grading.",
'About the "Photoelastic Stress Analysis"',
"A polarized light stress analysis tool that uses the stress-optic law (σ=N×f/d) to compute the principal stress difference of transparent parts, supporting materials such as borosilicate glass/soda-lime glass/PMMA/PC and automatically determining the stress grade.",
"One-click principal stress difference via the stress-optic law",
"Four common material fringe value presets",
"Automatic five-level stress grade determination",
"Optical path difference conversion and quality evaluation",
"Glass product residual stress inspection",
"Optical element birefringence assessment",
"Tempered glass quality inspection",
"Plastic injection-molded part stress analysis",
],
'lens-refractive-index': [
"📚 Lens Refractive Index Selector",
"Recommend a suitable refractive index from the power and estimate the edge thickness, Abbe number and lens weight",
'📖 View the "Lens Refractive Index Selector User Guide"',
"Prescription power SPH (D, negative for myopia)",
"Lens diameter (mm)",
"Center thickness (mm, for plus lens estimation)",
"Prioritize thin and light",
"Prioritize value for money",
"Prioritize optical quality (high Abbe number)",
"📋 Refractive Index Parameter Comparison",
"Recommend a refractive index tier (1.50 / 1.56 / 1.60 / 1.67 / 1.71 / 1.74) by |power| and the target (thin/value/optical) threshold",
"Low powers choose a low index (less dispersion), high powers choose a high index (thinner), and optical priority skips the high-dispersion tiers (1.67/1.74) at high powers in favor of 1.70/1.71.",
"Edge thickness estimation (minus lens): t_edge = ct + D²×|F| / (2000×(n−1)), where D is the diameter (mm) and F the power (D).\n      The higher the Abbe number the lower the dispersion and the better the optical quality; the higher the refractive index the thinner the lens but the lower the Abbe number usually.",
"The estimation results are for reference only; actual lens thickness is affected by center thickness, base curve, frame shape and other factors, so refer to the data from the fitting institution.",
"📚 In-depth: Lens Refractive Index Effects",
"Same power, different",
"refractive index",
"compare edge thickness.",
"High index reduces thickness but trades off dispersion.",
"Choose the refractive index by power and frame style.",
"Thickness comparison",
"−6.00D: 1.50 edge 8.0 mm, 1.60 about 7.0 mm, 1.74 about 5.8 mm; the higher the refractive index the thinner, reducing 12%-27%.",
"Dispersion trade-off",
"As the refractive index rises the Abbe number usually drops (1.50 Abbe 58, 1.74 about 33); high index shows obvious color fringing, and mid-low powers choose 1.60 for balance.",
"Is a higher refractive index more expensive?",
"Generally the higher the more expensive and thinner, but dispersion increases; higher is not always better, choose by power.",
"What is the Abbe number?",
"The reciprocal of dispersion; the higher it is the lower the dispersion and the sharper the vision; low-Abbe lenses show color fringes at the edge.",
'About the "Lens Refractive Index Selector"',
"Recommend a suitable lens refractive index from the prescription power and estimate the edge thickness, Abbe number and lens weight, helping you choose the most suitable lens material.",
"Supports full refractive index comparison from 1.50 to 1.74",
"Real-time edge thickness estimation",
"Abbe number and dispersion reference",
"Multi-dimensional recommendation strategy",
"Material selection during optometric fitting",
"High-power lens optimization",
"Lens thinning scheme assessment",
"Optical quality and thickness trade-off",
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

if __name__ == '__main__':
    for slug, en_list in EN.items():
        mp = build(slug, en_list)
        write(slug, mp)
    print('gen_optical_b4 done')

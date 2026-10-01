#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ophthalmology 第2批：visual-acuity-converter / corneal-curvature / corneal-endothelium / axial-length / pterygium-measurement"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'ophthalmology')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'ophthalmology')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        for i, it in enumerate(items):
            print('   ', i, repr((it.get('zh') or it.get('zh_src', ''))[:50]))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    return mp


def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'ophthalmology', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))


# ---------------- visual-acuity-converter (55) ----------------
write('visual-acuity-converter', build('visual-acuity-converter', [
    "\U0001F441\uFE0F Vision Chart (Snellen/logMAR) Converter",
    "Enter any one vision expression and it auto-converts to Snellen, decimal, logMAR, ETDRS letter count and the Chinese standard logMAR chart (5-point record).",
    "Vision chart converter",
    "/ Vision Chart Converter",
    '\U0001F4D6 View the "Vision Chart (Snellen/logMAR) Converter User Guide"',
    "logMAR = -log10(decimal vision)",
    "Input vision type",
    "Snellen 20 feet (20/x)",
    "Snellen 6 m (6/x)",
    "Snellen 5 m (5/x)",
    "Decimal vision (0.x)",
    "Chinese 5-point record (5.x)",
    "ETDRS letter count",
    "(e.g. 1.0)",
    "Special vision:",
    "Counting fingers (CF)",
    "Hand motion (HM)",
    "Light perception (LP)",
    "No light perception (NPL)",
    "\U0001F4CB Vision grading reference",
    "Standard vision",
    "Mild decrease",
    "Acceptable for daily life",
    "Moderate decrease",
    "Severe decrease",
    "Low vision",
    "Blindness (WHO)",
    "Better-eye best corrected vision <0.05",
    "\u26A0\uFE0F This tool is for vision-record conversion; ETDRS letter count follows the standard 5-letters-per-row chart (20/20\u224855 letters), and charts vary slightly. For reference only, not a substitute for professional exam.",
    'About "Vision Chart Converter"',
    "The vision chart converter supports mutual conversion among Snellen (20 ft / 6 m / 5 m), decimal, logMAR, ETDRS letter count and the Chinese standard logMAR chart (5-point record), and supports special records like counting fingers, hand motion and light perception.",
    "Conversion formula",
    "Chinese 5-point = 5 - logMAR",
    "\U0001F4DA Deep Dive: Vision Notation Interconversion (Decimal/logMAR/Snellen)",
    "Decimal = base/value; logMAR = -log10(decimal); 5-point record = 5 - logMAR.",
    "Interconvert Snellen 20/6/5 and ETDRS row number.",
    "Unify vision units in research and clinic.",
    "Decimal 1.0, logMAR 0, 5-point record 5.0, ETDRS row 55 correspond to normal vision.",
    "Decimal 0.1, logMAR 1.0, 5-point record 4.0, ETDRS row (1.10-1.0)/0.02 = 5, is low vision.",
    "Larger logMAR means worse vision?",
    "Yes, logMAR is inversely related to the log of vision; larger is worse; each 0.1 is about one row.",
    "How is the ETDRS row number obtained?",
    "By linear mapping from logMAR (e.g. (1.10-logMAR)/0.02), used for reading-chart grading.",
    'About "Vision Chart Converter - Snellen/logMAR/ETDRS"',
    "Free online vision chart converter, supporting mutual conversion among Snellen (20/6), decimal, logMAR, ETDRS letter count and the Chinese standard logMAR chart (5-point record). A medical professional tool based on authoritative standards, for reference only.",
    "How to use the vision chart (Snellen/logMAR) converter",
    "Value (e.g. 1.0)",
    "What does the vision chart (Snellen/logMAR) converter do?",
    "The vision chart converter interconverts Snellen (20/6/5 m), decimal, logMAR, ETDRS letter count, the Chinese standard logMAR (5-point record) and special records like light perception; suited for refraction and vision records.",
    "How do I use the vision chart (Snellen/logMAR) converter?",
    "What scenarios is the vision chart (Snellen/logMAR) converter suitable for?",
    "Three scales",
    "Snellen (20/20, 6/6), decimal (1.0) and logMAR (0.0) equivalently express the same vision: 20/20=6/6=1.0=0.0 logMAR; a larger numerator (e.g. 20/40) means worse vision.",
    "Interconvert charts across countries; logMAR eases statistics and research (larger is worse).",
    "Conversion is a mathematical correspondence; actual vision is affected by lighting, distance and correction state; defer to professional refraction.",
]))

# ---------------- corneal-curvature (45) ----------------
write('corneal-curvature', build('corneal-curvature', [
    "\U0001F441\uFE0F Corneal Curvature (K1/K2) and Astigmatism Calculator",
    "Enter the two principal meridian curvatures and K1 axis to compute astigmatism magnitude, axis and radius of curvature.",
    "/ Corneal Curvature and Astigmatism Calculator",
    '\U0001F4D6 View the "Corneal Curvature (K1/K2) and Astigmatism Calculator User Guide"',
    "Corneal astigmatism = steep K - flat K (diopters D); flat/steep K take the smaller/larger of the two meridians, mean K = (K1 + K2) / 2; steep axis = flat axis + 90\u00b0, with-the-rule (60-120\u00b0) / against-the-rule (150-30\u00b0) / oblique; astigmatism <0.5D physiological, <1 mild, <2 moderate, >=2 severe.",
    "K1 flat (D)",
    "K2 steep (D)",
    "K1 axis (\u00b0)",
    "\U0001F4D0 Conversion tool (D <-> mm)",
    "Curvature value",
    "Diopters D",
    "Radius of curvature mm",
    "1.3375 (common for cornea)",
    "\U0001F4CB Astigmatism axis judgment",
    "Steep axis",
    "With-the-rule astigmatism (WTR)",
    "More common, mostly in young",
    "Against-the-rule astigmatism (ATR)",
    "More seen in elderly",
    "Oblique astigmatism",
    "30-60\u00b0 or 120-150\u00b0",
    "Formula: r = (n-1)/K; astigmatism = K2-K1; mean curvature = (K1+K2)/2.",
    "\u26A0\uFE0F This tool is for corneal curvature parameter conversion; clinical interpretation needs corneal topography and refraction.",
    'About "Corneal Curvature and Astigmatism Calculator"',
    "Computes corneal astigmatism magnitude, axis and radius, and provides D-to-mm radius conversion.",
    "\U0001F4DA Deep Dive: Corneal Curvature and Astigmatism Analysis",
    "From K1/K2 derive flat/steep axis, astigmatism ast = steep - flat, mean K and simulated K (SimK).",
    "Determine corneal astigmatism axis (with/against-the-rule/oblique).",
    "Preoperative planning for IOL and corneal cross-linking.",
    "Flat axis 43.5, steep axis 44.0, astigmatism ast=0.5D (physiological); rFlat=0.3375/43.5\u22487.76mm, rSteep\u22487.67mm; mean K=43.75D.",
    "Astigmatism 2.0D",
    "If K difference is 2.0D it is moderate astigmatism; SimK is used for Toric IOL power calculation.",
    "What is 0.3375?",
    "Cornea",
    "refractive index",
    "n\u22481.3375, so radius r = 0.3375/K (K in mm^-1), used for keratometer conversion.",
    "How to judge with/against-the-rule?",
    "Steep axis near 180\u00b0 is WTR, near 90\u00b0 is ATR, otherwise oblique.",
    'About "Corneal Curvature (K1/K2) and Astigmatism Calculator"',
    "Corneal curvature and astigmatism calculator: enter K1/K2 and axis to compute corneal astigmatism magnitude and axis, mean curvature, SimK, and convert between diopters (D) and radius (mm). A medical professional tool based on authoritative standards, for reference only.",
    "How to use the corneal curvature (K1/K2) and astigmatism calculator",
    "What does the corneal curvature (K1/K2) and astigmatism calculator do?",
    "The corneal curvature and astigmatism calculator uses r=(n-1)/K for radius and K1, K2 for astigmatism magnitude, axis and diopter conversion, suited for refraction and contact-lens fitting.",
    "How do I use the corneal curvature (K1/K2) and astigmatism calculator?",
    "What scenarios is the corneal curvature (K1/K2) and astigmatism calculator suitable for?",
]))

# ---------------- corneal-endothelium (48) ----------------
write('corneal-endothelium', build('corneal-endothelium', [
    "\u2699\uFE0F Corneal Endothelial Cell Density and Morphology Counter",
    "Based on endothelial microscope photos, compute endothelial cell density (CD), coefficient of variation (CV) and hexagon ratio (6A) to assess corneal endothelial function.",
    "Corneal endothelium (density/morphology) counter",
    "/ Corneal Endothelial Cell Count",
    '\U0001F4D6 View the "Corneal Endothelial Cell Density and Morphology Counter User Guide"',
    "\U0001F522 Cell counting method",
    "\U0001F4D0 Fixed-frame method",
    "Cell counting and morphology analysis",
    "Cell density CD = cell count / frame area (cells/mm\u00b2); coefficient of variation CV = SD / mean cell area; hexagon ratio 6A = hexagon count / total cells \u00d7 100%",
    "CD >= 2500 normal, 1500-2500 borderline, < 1500 low; CV < 0.30 normal, 0.30-0.40 borderline, > 0.40 abnormal; hexagon ratio >= 55% normal, 50%-55% borderline.",
    "Total cells in count frame",
    "Count frame area (mm\u00b2)",
    "Cell area measurement (for CV)",
    "Enter areas of at least 5 cells (\u00b5m\u00b2) for CV.",
    "Hexagon cell ratio (6A)",
    "Count cells by edge number and compute the share of hexagonal (6-edge) cells.",
    "4 edges",
    "5 edges",
    "6 edges",
    "7 edges",
    "8 edges",
    "Fixed-frame method",
    "Cells in frame",
    "Frame area (mm\u00b2)",
    "\u2705 Compute analysis",
    "\U0001F4CB Endothelial assessment standard",
    "CD (cells/mm\u00b2)",
    "CV (coefficient of variation)",
    "6A (hexagon ratio)",
    "Normal adult CD is about 2500-3000 cells/mm\u00b2, declining with age. Pre-cataract CD<1000 is high surgical risk.",
    "\u26A0\uFE0F Corneal endothelial counting needs an endothelial microscope (e.g. NIDEK CEM-530); this tool only assists computation and cannot replace instrument auto-analysis.",
    'About "Corneal Endothelial Cell Count"',
    "Based on endothelial microscope images, compute CD, CV and 6A; the three indicators jointly assess endothelial function.",
    "\U0001F4DA Deep Dive: Corneal Endothelial Cell Density Analysis",
    "Specular photo count and area give cell density CD = count/area (cells/mm\u00b2).",
    "/ mean area assesses polymegathism.",
    "Hexagon ratio assesses stability.",
    "Count 2500, area 1 mm\u00b2",
    "CD = 2500 / 1 = 2500 cells/mm\u00b2 (normal adult about 2000-3000); if CV is low and hexagons >60%, morphology is good.",
    "Density decline",
    "If CD<1000 it signals endothelial decompensation risk; cataract surgery needs careful assessment.",
    "What is normal endothelial density?",
    "Newborn about 3000-4000, adult about 2000-3000, declining with age and after surgery.",
    "What does high CV mean?",
    "High CV means uneven cell sizes (polymegathism), an early sign of endothelial dysfunction.",
    'About "Corneal Endothelium (Density/Morphology) Counter"',
    "Corneal endothelial cell density and morphology counter: based on endothelial microscope photos, computes CD, CV and 6A to assess endothelial function. A medical professional tool based on authoritative standards, for reference only.",
    "One area per line, e.g.:",
]))

# ---------------- axial-length (46) ----------------
write('axial-length', build('axial-length', [
    "\U0001F4CF Ocular A-Scan (Axial Length) Calculator",
    "Correct the effect of sound velocity and measurement method on axial length, and estimate the deviation in IOL power.",
    "/ Axial Length Calculator",
    '\U0001F4D6 View the "Ocular A-Scan (Axial Length) Calculator User Guide"',
    "AL_true = AL_meas \u00d7 (V_true/V_assumed) - applanation offset",
    "Sound-velocity / method correction",
    "Segmented calculation",
    "Measured axial length AL (mm)",
    "Measurement sound velocity (m/s)",
    "Eye type (correction velocity)",
    "Phakic eye 1555",
    "Aphakic eye 1534",
    "Pseudophakic eye 1532",
    "Silicone-oil eye 1641",
    "Contact method (applanation ~0.15mm)",
    "Enter each segment length and velocity to compute total axial length:",
    "Anterior chamber depth ACD (mm)",
    "Sound velocity",
    "Lens thickness LT (mm)",
    "Vitreous length VL (mm)",
    "\U0001F4CB Reference sound velocity",
    "Medium",
    "Cornea",
    "Aqueous",
    "Lens",
    "Vitreous",
    "Phakic eye average",
    "About 987 (measured needs correction)",
    "Correction formula: AL_true = AL_meas \u00d7 (V_true/V_assumed) - applanation offset. Each 1mm axial error affects IOL by about 2.5D.",
    "\u26A0\uFE0F A-scan measurement is highly operator-dependent; optical methods (IOLMaster/LENSTAR) are more precise. Silicone-oil eyes need special handling; this tool is for teaching estimates.",
    'About "Axial Length Calculator"',
    "Correct sound-velocity and method effects on axial length; supports segmented velocity calculation to aid biometry interpretation.",
    "\U0001F4DA Deep Dive: Axial Length Measurement and Correction",
    "Correct axial length by device ultrasound velocity: alCorr = al \u00d7 (vTrue/vMeas).",
    "Compute the axial-length correction and contact-lens compensation needed for IOL power.",
    "Segmented velocity method restores geometric length.",
    "Measured 23.5mm, device velocity 1532, true value 1555",
    "Corrected alCorr = 23.5 \u00d7 (1555/1532) \u2248 23.86mm; iolDelta = (23.86-23.5)\u00d72.5 \u2248 0.9 D, suggesting IOL should be reduced by about 0.9D.",
    "Segmented-method check",
    "ACD+lens+vitreous geometric sum should equal the measured; read with mean velocity 1555 = 1555\u00d7(tACD+tL+tV) and compare with the geometric sum.",
    "Why correct sound velocity?",
    "Different devices default to different velocities (e.g. 1532/1555), so direct readings deviate and must be converted to the true value.",
    "Where does the 2.5 iolDelta factor come from?",
    "Empirically each 1mm axial deviation affects IOL by about 2.5D, so axial correction \u00d72.5 gives the power compensation.",
    'About "Ocular A-Scan (Axial Length) Calculator"',
    "Ocular A-scan axial length calculator: corrects axial length by sound velocity and method, estimates the effect on IOL power, and supports segmented velocity calculation. A medical professional tool based on authoritative standards, for reference only.",
]))

# ---------------- pterygium-measurement (46) ----------------
write('pterygium-measurement', build('pterygium-measurement', [
    "\U0001F441\uFE0F Pterygium Measurer",
    "Enter pterygium measurements at each site to compute corneal invasion ratio and grade. All units are millimeters (mm).",
    "Pterygium (head/body) measurer",
    "/ Pterygium Measurement",
    '\U0001F4D6 View the "Pterygium Measurer User Guide"',
    "Pterygium is graded by corneal invasion distance head (mm): <1.5 T1 quiescent, <=3 T2 moderate, <=4.5 T3 severe, >4.5 T4 critical (reaching pupil); corneal coverage = head \u00f7 (corneal diameter \u00f7 2) \u00d7 100% (cap 100), area \u2248 head \u00d7 width.",
    "Corneal horizontal diameter (mm)",
    "Pterygium head-to-limbus distance (mm)",
    "Body base width (mm)",
    "Body length (mm)",
    "Nasal",
    "Temporal",
    "Both sides (nasal + temporal)",
    "Injection degree",
    "Grade 0 no injection",
    "Grade 1 mild",
    "Grade 2 moderate",
    "Grade 3 severe",
    "\U0001F4D0 Compute measurement",
    "Body",
    "Head",
    "Limbus",
    "Diagram: the orange triangle is the pterygium, invading the cornea",
    "\U0001F4CB Pterygium grading standard",
    "Corneal invasion",
    "Quiescent, thin body",
    "Moderate invasion, medium body",
    "Severe invasion, thick body",
    "Critical invasion reaching pupil",
    "Grading is based on corneal invasion distance. Covering the pupil (T4) needs surgical intervention.",
    "\u26A0\uFE0F Measurement must be done under a slit lamp. Surgery is advised when the pterygium invades the pupil or affects vision.",
    'About "Pterygium Measurement"',
    "Measure pterygium head invasion distance, body width and length, compute corneal coverage ratio and grade by T to assess severity and aid surgical decisions.",
    "\U0001F4DA Deep Dive: Pterygium Invasion Measurement",
    "Measure corneal transverse diameter cd and invasion distance head; compute coverage ratio and area.",
    "Surgical indication and extent planning.",
    "Record injection grading.",
    "Corneal radius = 11.5/2 = 5.75mm; coverage ratio = 2/5.75\u00d7100 \u2248 34.8%; area = 2\u00d73 = 6mm\u00b2.",
    "Invasion reaching the pupil margin",
    "Head near the radius (coverage \u2192 high) and involving the optical zone gives a stronger surgical indication.",
    "What coverage ratio needs surgery?",
    "No absolute threshold, but invasion of the pupil, vision impact or recurrent inflammation usually suggests surgery.",
    "How is area estimated?",
    "Approximated as invasion distance \u00d7 neck width (head \u00d7 width), a simplified model for planning.",
    'About "Pterygium (Head/Body) Measurer"',
    "Pterygium measurer: measures pterygium head position, body length and width and corneal invasion range, computes grade and corneal coverage ratio. A medical professional tool based on authoritative standards, for reference only.",
]))

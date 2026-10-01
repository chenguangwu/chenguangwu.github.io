#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ophthalmology 第5批：strabismus-angle / calc-length-1 / pupil-reflex / fluorescein-staining / rater-7"""
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


# ---------------- strabismus-angle (35, src_diff idx8) ----------------
write('strabismus-angle', build('strabismus-angle', [
    "\U0001F4D0 Strabismus Angle (Prism/Synoptophore) Calculator",
    "Prism diopter (PD) and angle (\u00b0) conversion, Krimsky/Hirschberg estimation and multi-prism stacking.",
    "/ Strabismus Angle Calculator",
    '\U0001F4D6 View the "Strabismus Angle (Prism/Synoptophore) Calculator User Guide"',
    "Strabismus angle conversion: 1 prism diopter (PD) ~ arctan(0.01) ~ 0.573\u00b0 (1 cm deviation at 100 cm); Hirschberg: each 1 mm corneal-reflex deviation ~ 15 PD (~7.5\u00b0), deviation angle ~ deviation amount x 15 PD; Krimsky neutralizes the reflex with a prism, the prism amount equals the deviation.",
    "Unit conversion",
    "Prism stacking",
    "Prism diopter PD (\u0394)",
    "Relation: PD = 100\u00b7tan(\u00b0); \u00b0 = arctan(PD/100). 1\u0394 shifts 1 cm at 1 m. At small angles 1\u00b0 ~ 1.75\u0394.",
    "Corneal reflex point offset (mm)",
    "Pupil diameter (mm, optional)",
    "Hirschberg rule of thumb: reflex at pupil margin ~15\u00b0 (30\u0394), mid-iris ~30\u00b0 (60\u0394), limbus ~45\u00b0 (100\u0394). About 1 mm ~ 7\u00b0 ~ 12\u0394.",
    "Enter stacking prism degrees (same direction), auto-sum:",
    "Prism 1 (\u0394)",
    "Prism 2 (\u0394)",
    "Prism 3 (\u0394, optional)",
    "Same-direction stacking is roughly linear addition; large angles need the prism-stacking nonlinearity (converted in angle units).",
    "\u26A0\uFE0F Strabismus measurement is affected by the Kappa angle and fixation distance; this tool is an estimate, final results rest on prism cover test and synoptophore exam.",
    'About "Strabismus Angle Calculator"',
    "Performs prism-diopter/angle mutual conversion, Hirschberg reflex estimation and prism stacking, aiding quantitative strabismus assessment.",
    "\U0001F4DA Deep Dive: Deviation-Angle Conversion (Prism \u2194 Degree \u2194 mm)",
    "Prism diopter pd = 100\u00d7tan(deg); mm method ~7\u00b0/mm; prism neutralization gives total angle.",
    "Strabismus surgery amount planning.",
    "Prism cover-test record conversion.",
    "Measured 20\u0394",
    "Angle = atan(20/100) = 11.3\u00b0; by mm estimate (7\u00b0/mm) ~1.6 mm offset.",
    "Prism neutralization 3+4+5=12\u0394",
    "Total = 12\u0394, corresponding to ~ atan(0.12)=6.8\u00b0, for surgery-amount estimate.",
    "Prism diopter and",
    "angle conversion",
    "1\u0394 deflects light 1 cm per meter, i.e. tan\u03b8=pd/100, so \u03b8=atan(pd/100).",
    "Why mm method is 7\u00b0/mm?",
    "Clinical empirical approximation (~7\u00b0 per mm of extraocular muscle/fixation offset), for rough angle estimate.",
    'About "Strabismus Angle (Prism/Synoptophore) Calculator"',
    "Strabismus angle calculator: mutual conversion of prism diopter (PD) and degree (\u00b0), Krimsky/Hirschberg reflex-offset estimation, and multi-prism stacking calculation. A medical professional tool based on authoritative standards, for reference only.",
]))

# ---------------- calc-length-1 (33) ----------------
write('calc-length-1', build('calc-length-1', [
    "\U0001F4CF Ocular A-Scan / IOL Power Calculation",
    "Enter axial length, corneal curvature, anterior-chamber depth and lens thickness, choose an IOL formula, estimate emmetropic target IOL power.",
    "Ocular A-Scan (Axial Length) Calculation",
    "/ Ocular A-Scan (Axial Length) Calculation",
    '\U0001F4D6 View the "Ocular A-Scan / IOL Power Calculation User Guide"',
    "K\u0304 = (K1 + K2)/2; SRK II: P = A' \u2212 2.5\u00b7AL \u2212 0.9\u00b7K\u0304; SRK/T: P = A \u2212 2.5\u00b7AL \u2212 0.9\u00b7K\u0304 (segment-corrected by axial length); Hoffer Q approx: P = 5.45 \u2212 0.87\u00b7AL \u2212 0.22\u00b7K\u0304 + 0.5\u00b7ACD",
    "All three formulas center on axial length AL (mm) and mean corneal curvature K\u0304 (D); the A constant is segment-corrected by axial length; the result is an emmetropic (target refraction 0 D) IOL-power estimate.",
    "Axial length AL (mm)",
    "Corneal K1 (D)",
    "Corneal K2 (D)",
    "Anterior chamber depth ACD (mm)",
    "Lens thickness LT (mm)",
    "IOL A constant",
    "\U0001F4A1 IOL power formula: SRK II P=A\u22122.5AL\u22120.9K; SRK-T and Hoffer Q are more complex geometric-optics formulas; this tool uses a simplified version for reference.",
    "This tool is for education/estimation; for actual surgery use a calibrated biometer and a professional IOL formula.",
    "Special axial lengths (too short or too long), post-corneal-refractive surgery, etc. need special formulas.",
    "\U0001F4DA Deep Dive: Biometry IOL Power (SRK-II)",
    "SRK-II: Power = A \u2212 2.5\u00d7AL \u2212 0.9\u00d7Km (mean corneal curvature).",
    "Pre-cataract IOL power estimation.",
    "Compare results across different A constants.",
    "Axial length lengthens",
    "If AL=24.5, then Power ~ 118.4 \u2212 61.25 \u2212 39.375 ~ 17.78 D; each 1 mm AL gain lowers power ~2.5 D.",
    "SRK-II vs SRK/T difference?",
    "SRK-II empirically corrects A by axial length; SRK/T introduces effective lens position ELP for more accuracy, see iol-power.",
    "Km uses mean curvature?",
    "Yes, the mean of the two principal meridians' K approximates spherical-equivalent corneal power.",
    'About "Ocular A-Scan (Axial Length) Calculation"',
    "From ocular A-scan or optical biometry axial length, corneal curvature, anterior-chamber depth and lens thickness, estimate the intraocular lens (IOL) power.",
    "Supports SRK II, SRK/T and Hoffer Q, three common formulas",
    "Enter axial length, corneal K, ACD, LT and other key parameters",
    "Auto-calculate emmetropic target IOL power",
    "Rapid pre-op IOL power estimate",
    "Biometry report review",
]))

# ---------------- pupil-reflex (34) ----------------
write('pupil-reflex', build('pupil-reflex', [
    "\U0001F4CB Pupil (Light Reflex) Response Grader",
    "Grade direct light reflex on a 0-4 scale and choose RAPD (swinging-flashlight test) grading, aiding afferent/efferent lesion localization.",
    "/ Pupil Light Reflex Grader",
    '\U0001F4D6 View the "Pupil (Light Reflex) Response Grader User Guide"',
    "Pupil light reflex: direct reflex graded 0-3 (3 normal, 2 reduced, 1 sluggish, 0 no response); RAPD positive suggests afferent weakness (retina/optic nerve) on the weak side; bilateral reduction suggests oculomotor efferent lesion; interpret with inter-eye symmetry.",
    "Right eye (OD) direct light reflex",
    "Left eye (OS) direct light reflex",
    "RAPD (relative afferent pupillary defect, swinging light)",
    "\U0001F4CB Grading standard",
    "Light reflex",
    "Brisk",
    "0 No RAPD",
    "1+ Initial constriction then dilation",
    "Sluggish",
    "2+ Immediate dilation",
    "Absent",
    "3+ No constriction, direct dilation / 4+ Fixed dilated",
    "Direct reflex = response of the illuminated eye; consensual = response of the fellow eye when the other is illuminated. RAPD positive suggests afferent lesion of that retina/optic nerve.",
    "\u26A0\uFE0F Pupil exam needs dim light; note physiologic anisocoria (difference <0.4 mm with normal reflex). Results are for teaching only.",
    'About "Pupil Reflex Grader"',
    "Grades direct light reflex and RAPD, aiding optic-nerve afferent and oculomotor efferent lesion localization.",
    "\U0001F4DA Deep Dive: Pupil Light Reflex and RAPD Assessment",
    "Direct light 0-4 grades, RAPD 0-4+ grades.",
    "Relative afferent pupillary defect (RAPD) laterality.",
    "Optic nerve and visual pathway lesion screening.",
    "Right direct response reduced (2<3), RAPD positive localizes to right eye (OD<OS), suggests right optic-nerve afferent damage.",
    "Both eyes 3, RAPD=0",
    "Both normal, no RAPD, pupil pathway intact.",
    "How to elicit RAPD?",
    "Alternately illuminate both eyes; the affected eye still dilates (relative) when going from dark to light, i.e. positive.",
    "Which diseases show RAPD?",
    "Optic neuritis, significant optic-nerve compression, retinopathy and other unilateral afferent lesions.",
    'About "Pupil (Light Reflex) Response Grader"',
    "Pupil light reflex response grader: grades direct/consensual light reflex and RAPD (relative afferent pupillary defect), aiding pupil-abnormality localization. A medical professional tool based on authoritative standards, for reference only.",
]))

# ---------------- fluorescein-staining (32) ----------------
write('fluorescein-staining', build('fluorescein-staining', [
    "\U0001F9F5 Ocular Surface Fluorescein Staining Scorer",
    "Based on the NEI (National Eye Institute) zone scoring. Cornea in 5 zones, nasal/temporal conjunctiva each 3 zones, each zone 0-3. Cornea and conjunctiva scored separately.",
    "Ocular Surface (Fluorescein Staining) Scorer",
    "/ Fluorescein Staining Score",
    '\U0001F4D6 View the "Ocular Surface Fluorescein Staining Scorer User Guide"',
    "Corneal fluorescein score = sum of superior-nasal/inferior-nasal/superior-temporal/inferior-temporal/central zones (0-3) (0-15); conjunctiva 0-18; total 0-33; cornea 0 no stain, <=3 mild, <=6 moderate, >6 severe.",
    "\U0001F9F5 Cornea (5 zones)",
    "\U0001F9F5 Conjunctiva (6 zones)",
    "\U0001F4CB NEI Scoring Standard",
    "Staining degree",
    "No punctate stain",
    "1-5 punctate stains",
    "6-15 punctate stains",
    ">=16 punctate stains or confluent sheet",
    "Corneal total (0-15), nasal + temporal conjunctiva total (0-18).",
    "\u26A0\uFE0F Fluorescein staining needs slit-lamp cobalt-blue light; this tool only aids scoring records, cannot replace clinical exam.",
    'About "Fluorescein Staining Score"',
    "Uses the NEI zoning method to standardize corneal and conjunctival fluorescein staining scoring, quantify ocular-surface epithelial damage, often used for dry eye and corneal epithelial lesion assessment.",
    "\U0001F4DA Deep Dive: Fluorescein Corneal Staining Score",
    "Score 5 corneal zones 0-3 each, total 0-15.",
    "Dry eye, corneal epithelial defect, limbal inflammation assessment.",
    "Follow staining-range change.",
    "Central 2 + superior zone 1, rest 0",
    "Corneal total = 2+1 = 3/15, mild punctate stain; conjunctiva scored separately 0-18.",
    "Whole cornea 3 x 5",
    "Total 15/15 is diffuse severe staining, suggests widespread epithelial damage.",
    "How to set 0-3?",
    "0 no stain, 1 scattered dots, 2 confluent patches, 3 large absence, by stain range and density.",
    "Cornea and conjunctiva scored separately?",
    "Yes, cornea 0-15, conjunctiva separately 0-18, reflecting different-site damage.",
    'About "Ocular Surface (Fluorescein Staining) Scorer"',
    "Ocular surface fluorescein staining scorer: scores corneal and conjunctival zones by NEI grading standard, computes total fluorescein score and assesses ocular-surface damage. A medical professional tool based on authoritative standards, for reference only.",
]))

# ---------------- rater-7 (25) ----------------
write('rater-7', build('rater-7', [
    "\U0001F9F5 Ocular Surface (Fluorescein Staining) Score",
    "van Bijsterveld ocular-surface fluorescein staining score (3 zones, total 0-9, higher means worse damage)",
    '\U0001F4D6 View the "Ocular Surface (Fluorescein Staining) Score User Guide"',
    "van Bijsterveld ocular-surface stain total = nasal conjunctiva + cornea + temporal conjunctiva (each 0-3, max 9); <=3 mild, <=6 moderate, >6 severe corneal epithelial damage.",
    "1. Nasal conjunctiva staining",
    "0 - No stain",
    "1 - Minimal punctate stain",
    "2 - Large punctate stain",
    "3 - Confluent stain",
    "2. Corneal staining",
    "3. Temporal conjunctiva staining",
    "\U0001F4DA Deep Dive: van Bijsterveld Dry-Eye Score",
    "Nasal conjunctiva/cornea/temporal conjunctiva three items each 0-3, total 0-9.",
    "Sjogren's-syndrome-related ocular-sign screening.",
    "Objective sign quantification.",
    "Three items 2/1/2",
    "Total = 5/9, reaches the dry-eye suspicious threshold (>=4 often suggests further Schirmer etc. exam).",
    "Total 1",
    "Mild (1/9), little conjunctival/corneal staining, limited clinical significance.",
    "Difference from OSDI?",
    "This score is an objective sign (staining), OSDI is a subjective symptom; combining both is more complete.",
    "Meaning of full 9?",
    "All three 3 means severe widespread staining, suggests significant ocular-surface inflammation/dryness.",
    'About "Ocular Surface (Fluorescein Staining) Score"',
    "Ocular surface (fluorescein staining) score. Free online tool, pure front-end processing, data not uploaded, privacy-safe.",
]))

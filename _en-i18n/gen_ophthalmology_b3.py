#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ophthalmology 第3批：refraction-error / visual-field-analysis / iop-correction / rater-8 / oct-rnfl"""
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


# ---------------- refraction-error (44) ----------------
write('refraction-error', build('refraction-error', [
    "\U0001F441\uFE0F Refractive Error (Sphere/Cylinder/Axis) Cross-Cylinder Calculator",
    "Supports plus/minus cylinder conversion, spherical equivalent and power-vector decomposition, and combined calculation of two cylinders (over-correction / stacking).",
    "Refractive error cross-cylinder calculator",
    "/ Refractive Error Cross-Cylinder Calculator",
    '\U0001F4D6 View the "Refractive Error (Sphere/Cylinder/Axis) Cross-Cylinder Calculator User Guide"',
    "Single-lens conversion",
    "Two-lens combination",
    "Spherical equivalent SE = S + C/2; power vector M = S + C/2, J0 = -(C/2)\u00b7cos2\u03b1, J45 = -(C/2)\u00b7sin2\u03b1; cylinder transpose: S' = S + C, C' = -C, \u03b1' = \u03b1 + 90\u00b0",
    "Spherical equivalent and power vector decompose a prescription into spherical (M) and two astigmatic components (J0/J45), for plus/minus cylinder interchange, two-cylinder stacking (over-correction) and axis normalization.",
    "Sphere S (D)",
    "Cylinder C (D)",
    "Axis (\u00b0)",
    "Prescription 1 (e.g. original lens / base refraction)",
    "Axis 1 (\u00b0)",
    "Prescription 2 (e.g. cross-cylinder / over-refraction)",
    "Axis 2 (\u00b0)",
    "\U0001F4DA Formula and notes",
    "Power-vector decomposition (Thibos)",
    "- Spherical equivalent M = S + C/2",
    "- Jackson 0\u00b0 component J0 = -(C/2)\u00b7cos(2\u03b1)",
    "- Jackson 45\u00b0 component J45 = -(C/2)\u00b7sin(2\u03b1)",
    "- Back-calc: C = -2\u00b7sqrt(J0\u00b2+J45\u00b2), axis = \u00bd\u00b7atan2(J45,J0), S = M - C/2",
    "Plus/minus cylinder conversion",
    "- New sphere = S + C, new cylinder = -C, new axis = axis \u00b1 90\u00b0 (take 1-180)",
    "Two-lens combination (power-vector addition)",
    "Convert each of the two prescriptions to M/J0/J45, add, then back-calc to sphere/cylinder/axis. For over-refraction and double-cylinder stacking.",
    "\u26A0\uFE0F This tool is for refraction-prescription conversion teaching; results are for reference only and cannot replace comprehensive or medical refraction.",
    'About "Refractive Error Cross-Cylinder Calculator"',
    "Based on the Thibos power-vector method, it performs sphere/cylinder conversion, spherical-equivalent calculation and dual-prescription combination; an aid for cross-cylinder fine-tuning and over-refraction analysis in comprehensive refraction.",
    "Plus/minus cylinder prescription interchange",
    "Cross-cylinder over-refraction analysis",
    "Estimate of double-cylinder stacking effect",
    "\U0001F4DA Deep Dive: Refractive Error and Cylinder Conversion (Power Vector)",
    "Sphere/cylinder to power vector: M = S + C/2, J0 = -(C/2)cos2ax, J45 = -(C/2)sin2ax.",
    "Plus/minus cylinder interchange, two-prescription vector addition.",
    "With/against-the-rule and oblique astigmatism judgment.",
    "M = -3.5; J0 = -(-0.5)cos360 = -0.5; J45 = 0; SE = -3.5; against-the-rule (ATR, axis near 180\u00b0). Negative to positive cylinder: S=-4.0, C=+1.0@90.",
    "Adding two prescriptions",
    "Add the power vectors of two glasses and revert to get the equivalent combined prescription for easy comparison.",
    "Why use J0/J45?",
    "The power vector expresses astigmatism as orthogonal components, easing statistics and addition and avoiding the 180\u00b0 axis jump.",
    "What is SE?",
    "Spherical equivalent SE = S + C/2, measures overall refractive error, used for screening and statistics.",
    "Refractive error sphere/cylinder/axis cross-cylinder calculator: sphere/cylinder conversion, spherical equivalent, power-vector (J0/J45) decomposition and dual-cylinder combination (over-refraction). A medical professional tool based on authoritative standards, for reference only.",
]))

# ---------------- visual-field-analysis (40) ----------------
write('visual-field-analysis', build('visual-field-analysis', [
    "\U0001F4CA Visual Field Defect (MD/PSD) Analyzer",
    "Enter standard white-on-white perimetry (Humphrey 24-2/30-2) metrics to analyze glaucoma visual-field damage. MD/PSD may be negative or positive; enter by convention (e.g. MD = -6.5).",
    "/ Visual Field Defect Analyzer",
    '\U0001F4D6 View the "Visual Field Defect (MD/PSD) Analyzer User Guide"',
    "Visual-field analysis (HAP staging): stage by MD negative value, > -6 early, > -12 moderate, <= -12 late; PSD <2 no local defect, <5 suspect, >=5 marked; VFI >=95 normal, >=80 mild, >=50 moderate, <50 severe.",
    "Mean deviation MD (dB)",
    "Pattern standard deviation PSD (dB)",
    "Visual field index VFI (%)",
    "GHT (glaucoma hemifield test):",
    "Normal",
    "Borderline",
    "\U0001F4CB Hodapp-Anderson-Parrish (HAP) grading",
    "Only paracentral scotoma or nasal step",
    "Moderate",
    "Absolute defect, central 5\u00b0 spared",
    "Late",
    "Residual central or temporal island",
    "PSD reflects local defect (p<5% is meaningful); VFI is a percentage overall metric, often used to track progression. MD's p-value needs the age-normal database.",
    "\u26A0\uFE0F Visual-field analysis is only auxiliary interpretation; a single field has large variance, so combine OCT/optic-nerve and repeated exams, and follow up with ophthalmology.",
    'About "Visual Field Defect Analyzer"',
    "Based on HAP grading, PSD significance and GHT result, stage glaucoma visual-field damage and aid report interpretation.",
    "Visual-field report staging interpretation",
    "Glaucoma damage assessment",
    "Progression monitoring aid",
    "\U0001F4DA Deep Dive: Visual Field Analysis (MD/PSD/VFI/GHT)",
    "Combine MD, PSD, VFI and GHT pattern for glaucoma grading.",
    "MD>-2 and PSD<2 and VFI>=95 is judged normal.",
    "Progression staging (early/middle/late).",
    "MD clearly negative, PSD high, VFI down, judged moderate glaucoma field damage; pct = (-6)/30\u00d7100 = 20% defect.",
    "All near normal, GHT normal, no clear visual-field damage.",
    "What is VFI?",
    "Visual Field Index, converting sensitivity into the equivalent of a healthy field's",
    "Which is more intuitive, MD or VFI?",
    "MD is mean deviation (dB), VFI is a percentage; the latter is easier to explain overall preservation to patients.",
    'About "Visual Field Defect (MD/PSD) Analyzer"',
    "Visual field defect analyzer: enter mean deviation (MD), pattern standard deviation (PSD) and visual field index (VFI), and assess glaucoma damage by Hodapp grading and GHT. A medical professional tool based on authoritative standards, for reference only.",
    "How to use the visual field defect (MD/PSD) analyzer",
    "What does the visual field defect (MD/PSD) analyzer do?",
    "How do I use the visual field defect (MD/PSD) analyzer?",
    "What scenarios is the visual field defect (MD/PSD) analyzer suitable for?",
]))

# ---------------- iop-correction (42) ----------------
write('iop-correction', build('iop-correction', [
    "\U0001F441\uFE0F Intraocular Pressure (Goldmann/NCT) Corrector",
    "Enter measured IOP and central corneal thickness (CCT) to estimate true IOP and assess CCT's effect on the reading.",
    "/ IOP Corrector",
    '\U0001F4D6 View the "Intraocular Pressure (Goldmann/NCT) Corrector User Guide"',
    "Multi-formula IOP/CCT correction: Ehlers = IOP + (520 - CCT) \u00d7 0.071; Doughty = IOP + (542 - CCT) \u00d7 0.020; Feltgen = IOP + (550 - CCT) \u00d7 0.030; ratio method = IOP \u00d7 520 / CCT; take the mean and extremes of the four; CCT <500\u00b5m makes the reading biased low.",
    "Measured IOP (mmHg)",
    "Central corneal thickness CCT (\u00b5m)",
    "Measurement method",
    "Goldmann applanation (GAT)",
    "Non-contact tonometry (NCT)",
    "\U0001F4D0 Correction formulas",
    "Note: Goldmann's design baseline is about 520\u00b5m; thicker overestimates and thinner underestimates IOP. The coefficients come from different studies and are for reference.",
    "\U0001F4CB CCT grading and risk",
    "Effect on measurement",
    "Too thin",
    "Underestimates IOP",
    "Beware missing glaucoma",
    "Normal-thin",
    "Mild underestimation",
    "Reading fairly reliable",
    "Routine evaluation",
    "Normal-thick",
    "Mild overestimation",
    "Watch pseudo-hypertension",
    "Too thick",
    "Overestimates IOP",
    "Beware pseudo-glaucoma",
    "\u26A0\uFE0F Corneal-thickness correction is only an estimate with large individual variation; diagnosis or exclusion of glaucoma cannot rest on it alone. Combine optic nerve, visual field, etc., and see an ophthalmologist.",
    'About "IOP Corrector"',
    "Corrects applanation / non-contact IOP readings by central corneal thickness to help spot misjudged IOP from too-thin or too-thick corneas.",
    "\U0001F4DA Deep Dive: Multi-Formula IOP Correction (CCT)",
    "Give all four corrections (Ehlers/Doughty/Feltgen and ratio) and take the mean.",
    "Systematic-bias correction of Goldmann IOP for thick/thin corneas.",
    "Cross-validation for glaucoma diagnosis.",
    "Ehlers=18+(520-550)\u00d70.071=15.87; Doughty=18+(542-550)\u00d70.02=17.84; Feltgen=18; ratio=18\u00d7520/550=17.02; mean\u224817.2 mmHg.",
    "Ehlers=18+(520-600)\u00d70.071=12.32 (thick cornea greatly overestimates, corrected much lower).",
    "What does a large four-formula difference mean?",
    "The farther CCT deviates from the mean and the larger the empirical-coefficient differences, the more the mean reduces single-formula bias.",
    "Can correction replace true IOP?",
    "No, it is only an estimate; rely on repeated measurements and clinical judgment.",
    'About "Intraocular Pressure (Goldmann/NCT) Corrector"',
    "IOP corrector: corrects Goldmann applanation (GAT) or non-contact (NCT) IOP by central corneal thickness (CCT), providing Ehlers and other formula estimates. A medical professional tool based on authoritative standards, for reference only.",
]))

# ---------------- rater-8 (28) ----------------
write('rater-8', build('rater-8', [
    "\U0001F634 Visual Fatigue (VAS Score) Questionnaire",
    "Visual Analog Scale (VAS) visual-fatigue score: 8 symptoms, 0-10 each, total 0-80",
    '\U0001F4D6 View the "Visual Fatigue (VAS Score) Questionnaire User Guide"',
    "Visual-fatigue VAS total = 8 symptom items (0-10 each, max 80); average = total / 8; average <=1 none, <=3 mild, <=6 moderate, >6 severe.",
    "1. Dry eyes",
    "3 - mild",
    "10 - extreme",
    "2. Eye ache",
    "3. Blurred vision",
    "4. Headache",
    "5. Eye fatigue",
    "6. Photophobia",
    "7. Tearing",
    "8. Foreign-body sensation",
    "\U0001F4DA Deep Dive: Visual-Fatigue Symptom VAS Scoring",
    "8 visual-fatigue symptoms each 0-10, total 0-80 (or VAS 0-10 weighted).",
    "Digital eye-strain (computer vision syndrome) assessment.",
    "Before/after intervention comparison.",
    "8 items 3 each",
    "Total = 24/80, mild-to-moderate; if VAS slider 6\u00d75=30 plus symptoms 24 = 54 composite (0-110) is moderate.",
    "Total 10",
    "Mild (10/80); rest and eye hygiene suffice.",
    "Relation between VAS and total?",
    "This tool may include a 0-10 slider (\u00d75 gives 0-50) plus 12 symptoms (0-60) to form a 0-110 composite.",
    "High score necessarily pathological?",
    "Short-term intense use can also raise it; judge by duration and relief after rest.",
    'About "Visual Fatigue (VAS Score) Questionnaire"',
    "Visual fatigue (VAS score) questionnaire. Free online tool, pure front-end processing, data not uploaded, privacy-safe.",
]))

# ---------------- oct-rnfl (41) ----------------
write('oct-rnfl', build('oct-rnfl', [
    "\U0001F4CF OCT (RNFL Thickness) Glaucoma Assessor",
    "Enter RNFL global and four-quadrant thickness (\u00b5m) and age to compare with the normal database and validate the ISNT rule.",
    "/ OCT-RNFL Assessor",
    '\U0001F4D6 View the "OCT (RNFL Thickness) Glaucoma Assessor User Guide"',
    "OCT retinal nerve fiber layer (RNFL) quadrant thickness vs age-expected values (temporal expected lowest); ISNT rule: superior > nasal > inferior > temporal; any quadrant below threshold is abnormal, borderline prompts recheck; overall thinning suggests glaucoma.",
    "Global RNFL G (\u00b5m)",
    "Superior S (\u00b5m)",
    "Inferior I (\u00b5m)",
    "Nasal N (\u00b5m)",
    "Temporal T (\u00b5m)",
    "\U0001F4CB RNFL normal reference and zones",
    "Normal mean (\u00b5m)",
    "Yellow (borderline)",
    "Red (abnormal)",
    "Global G",
    "<1% or <80",
    "Superior S",
    "Inferior I",
    "Nasal N",
    "Temporal T",
    "Normal RNFL declines ~2\u00b5m per decade. ISNT rule: S>I>N>T; violation suggests possible glaucoma.",
    "\u26A0\uFE0F RNFL assessment is affected by age, refraction and disc-macula distance; color scales follow each instrument's normal database. This tool uses empirical thresholds and cannot replace the OCT instrument report.",
    'About "OCT-RNFL Assessor"',
    "Color-zone assessment of retinal nerve fiber layer thickness and ISNT-rule validation, aiding early glaucoma screening.",
    "Age-corrected expected thickness",
    "Four-quadrant ISNT rule validation",
    "Red/yellow/green three-color grading",
    "\U0001F4DA Deep Dive: OCT Retinal Nerve Fiber Layer (RNFL) Analysis",
    "Age-correct each quadrant's expected RNFL thickness and interpret.",
    "ISNT rhythm (inferior>superior>nasal>temporal) conformity check.",
    "Early glaucoma damage screening.",
    "Age 60, measured G95/S110/I105/N60/T55",
    "Expected G=100-(60-50)\u00d70.2=98, S/I120, N70, T60; measured basically matches and ISNT holds, RNFL essentially normal.",
    "Superior markedly thinned",
    "If S drops to 80 and violates ISNT, suggests superior-quadrant defect, beware glaucoma.",
    "Why age-correct?",
    "RNFL thins with age (~0.2\u00b5m/year); correcting improves interpretation.",
    "ISNT violation means disease for sure?",
    "It is an important sign but not absolute; combine cup-disc ratio and visual field.",
    'About "OCT (RNFL Thickness) Glaucoma Assessor"',
    "OCT RNFL thickness assessor: enter retinal nerve fiber layer (RNFL) global and quadrant thickness, assess glaucoma damage against age normals and validate the ISNT rule. A medical professional tool based on authoritative standards, for reference only.",
]))

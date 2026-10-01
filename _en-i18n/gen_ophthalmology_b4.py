#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ophthalmology 第4批：osdi-scale / visual-fatigue-vas / vision-screening-21 / cd-ratio / detector-6"""
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


# ---------------- osdi-scale (41) ----------------
write('osdi-scale', build('osdi-scale', [
    "\U0001F4CB Dry Eye (OSDI) Self-Assessment Scale",
    "Recall the past week and choose the frequency for each question. OSDI = (sum of scores x 100) / (number of answered questions x 4).",
    "/ Dry Eye (OSDI) Scale",
    '\U0001F4D6 View the "Dry Eye (OSDI) Self-Assessment Scale User Guide"',
    "OSDI = (sum of scores x 100) / (answered questions x 4)",
    "\u2705 Calculate OSDI",
    "\U0001F4CB OSDI Grading",
    "Mild dry eye",
    "Moderate dry eye",
    "Severe dry eye",
    "\u26A0\uFE0F OSDI is a subjective self-assessment affected by mood and comprehension; it cannot replace clinical dry-eye exams (BUT, Schirmer, staining, etc.).",
    'About "OSDI Scale"',
    "Standard 12-item OSDI questionnaire; computes total and subscale scores and grades them for subjective dry-eye symptom assessment.",
    "\U0001F4DA Deep Dive: Ocular Surface Disease Index (OSDI)",
    "12 items scored 0-4 by frequency; OSDI = total/(answered x 4) x 100 (0-100).",
    "Quantify dry-eye severity.",
    "Before/after treatment follow-up.",
    "Answered 10 questions, total 18",
    "OSDI = 18/(10 x 4) x 100 = 45, moderate-to-severe dry eye (>=33 moderate-to-severe).",
    "Total 8",
    "OSDI = 8/(12 x 4) x 100 ~ 17, mild dry eye (12-22 mild).",
    "OSDI cut-offs?",
    "Commonly 0-11 normal, 12-22 mild, 23-32 moderate, >=33 severe (varies slightly by study).",
    "How if not all answered?",
    "Normalize by actual answered count (total/answered x 4 x 100) to avoid missing-data bias.",
    'About "Dry Eye (OSDI) Self-Assessment Scale"',
    "Dry Eye OSDI self-assessment scale: a 12-item standard Ocular Surface Disease Index questionnaire that computes the OSDI total and subscale scores and grades dry-eye severity. A medical professional tool based on authoritative standards, for reference only.",
    "How to use the Dry Eye (OSDI) Self-Assessment Scale",
    "What does the Dry Eye (OSDI) Self-Assessment Scale do?",
    "The Dry Eye OSDI self-assessment scale provides a standard 12-item questionnaire, computing total and subscale scores and grading for subjective dry-eye symptom assessment and severity screening.",
    "How do I use the Dry Eye (OSDI) Self-Assessment Scale?",
    "Which scenarios suit the Dry Eye (OSDI) Self-Assessment Scale?",
    "Total score and grading",
    "Ocular Surface Disease Index (OSDI) total score 0-100:",
    "Normal;",
    "Mild dry eye;",
    "Moderate dry eye;",
    "Severe dry eye.",
    "Assesses dry-eye-related symptoms, visual-function interference and environmental impact; higher scores mean heavier burden, often used in efficacy follow-up.",
    "Applicability boundary",
    "OSDI is a self-screening tool; thresholds are for reference. Confirmation needs objective exams such as tear secretion, tear-film break-up time and corneal staining.",
]))

# ---------------- visual-fatigue-vas (38) ----------------
write('visual-fatigue-vas', build('visual-fatigue-vas', [
    "\U0001F634 Visual Fatigue VAS Score Questionnaire",
    "VAS visual analog scale (0-10) quantifies fatigue level plus a 12-item visual-fatigue symptom questionnaire for comprehensive assessment.",
    "Visual Fatigue (VAS Score) Questionnaire",
    "/ Visual Fatigue VAS Score",
    '\U0001F4D6 View the "Visual Fatigue VAS Score Questionnaire User Guide"',
    "Visual-fatigue composite = VAS slider value x 5 + symptom questionnaire total (0-60), max 110; <=15 none/mild, <=30 mild, <=50 moderate, >50 severe.",
    "\U0001F4CA VAS Visual Analog Scale",
    "Drag the slider to choose your current visual fatigue (0=no fatigue, 10=extreme fatigue).",
    "0 No fatigue",
    "5 Moderate",
    "10 Extreme fatigue",
    "\U0001FDDD\uFE0F Visual Fatigue Symptom Questionnaire (past week)",
    "\u2705 Comprehensive assessment",
    "\U0001F4CB Assessment notes",
    "Visual fatigue level",
    "None/mild",
    "Keep good eye-use habits",
    "Increase rest, 20-20-20 rule",
    "Reduce screen time, refractions if needed",
    "Consider ophthalmology visit to rule out causes",
    "VAS points x 5 plus 12 symptom points (0-5 each); composite full score 70.",
    "\u26A0\uFE0F Visual-fatigue VAS is subjective; persistent severe fatigue needs ruling out organic causes like refractive error, dry eye and accommodative dysfunction.",
    'About "Visual Fatigue VAS Score"',
    "Combines the VAS visual analog scale with a 12-item visual-fatigue symptom questionnaire to quantify fatigue and provide eye-use advice and intervention reference.",
    "\U0001F4DA Deep Dive: Visual Fatigue Composite Score (VAS)",
    "VAS slider 0-10 (x 5 gives 0-50) plus 12 symptoms 0-5 (0-60) combine to 0-110.",
    "Quantify digital eye strain.",
    "Before/after intervention comparison.",
    "VAS=6, symptom total=18",
    "Composite = 6 x 5 + 18 = 48/110, moderate; if VAS=2, symptom total=6 then 16 mild.",
    "Maximum scenario",
    "VAS=10 (50) + all symptoms 5 (60) = 110, extreme fatigue, adjust eye use immediately.",
    "VAS vs symptom weight?",
    "This tool: VAS 0-50, symptoms 0-60, balancing subjective intensity and multi-dimensional symptoms.",
    "High score means see a doctor?",
    "Short-term can be from overuse; persistent high score with vision drop should see a doctor.",
    'About "Visual Fatigue (VAS Score) Questionnaire"',
    "Visual Fatigue VAS Score Questionnaire: includes a visual analog scale (VAS) and a visual-fatigue symptom questionnaire, quantifying fatigue and giving intervention advice. A medical professional tool based on authoritative standards, for reference only.",
]))

# ---------------- vision-screening-21 (37) ----------------
write('vision-screening-21', build('vision-screening-21', [
    "\U0001F50D 21-Item Adaptive Vision Screening: Single-Eye Refraction Estimate",
    "21 adaptive questions assess each eye separately, covering frequency and scenarios of near-reading blur, distance blur, night glare, squinting and headache; with age stratification, weighted scoring and simple regression estimate each eye's approximate myopia range, flag astigmatism signs and give refraction grading advice.",
    "21-Item Adaptive Vision Screening (Single-Eye Refraction Estimate)",
    "/ 21-Item Adaptive Vision Screening",
    "21-Item Adaptive Vision Screening",
    '\U0001F4D6 View the "21-Item Adaptive Vision Screening User Guide"',
    "\U0001F4D0 Estimation Method (Non-Diagnostic)",
    "Each eye scored independently: S = sum(symptom frequency 0-4 x its weight) / (sum weights x 4), giving a 0-1 'symptom load ratio' r. Approx. myopia spherical-equivalent magnitude D = 8.0 x r^1.25 x age factor (child 1.15 / teen 1.10 / adult 1.00 / older 0.85), with +(0.6 + (1-r^1.25) x 1.2) D as uncertainty interval. Astigmatism flag uses load ratio of astigmatism-related symptoms; beyond threshold gives axis direction words (with-the-rule / against-the-rule / oblique). This is a questionnaire-based statistical approximation,",
    "cannot replace medical refraction",
    "\u2460 First choose age stratification",
    "Age stratification",
    "Child (<= 12 yrs)",
    "Teen (13-17 yrs)",
    "Adult (18-54 yrs)",
    "Older adult (>= 55 yrs)",
    "Note: questions will",
    "dynamically adjust order based on your answers",
    "- if early signals are weak, high-weight distance symptoms are asked first; if astigmatism signs appear, astigmatism follow-ups are prioritized. The whole flow has 21 questions, asked separately for",
    "Left eye",
    "Right eye",
    ".",
    "\u25B6 Start screening (21 questions)",
    "\U0001F441\uFE0F Left eye",
    "\U0001F441\uFE0F Right eye",
    "\u2190 Previous question",
    "\U0001F4DA Deep Dive: 21-Item Adaptive Vision Self-Test and Single-Eye Refraction Estimate",
    "Independent adaptive Q&A for each eye, estimate myopia spherical equivalent.",
    "Estimate astigmatism axis direction, assess symptom load.",
    "Provide pre-visit preliminary reference and medical disclaimer.",
    "Left eye clear, right eye blur deepens question by question",
    "Right eye needs closer or blurrier, choice groups lean toward higher load -> estimate right-eye myopia spherical equivalent high, suggesting a refraction visit.",
    "Both eyes close",
    "Both eyes' estimates are close and symptom load is low, suggesting symmetric refraction, continue routine observation.",
    "Is the estimated degree accurate?",
    "Adaptive Q&A only gives rough spherical-equivalent estimate, affected by subjective judgment, cannot replace refraction.",
    "Why test each eye separately?",
    "Separate testing reveals anisometropia (inter-eye degree difference), an important clue for monocular amblyopia and visual fatigue.",
]))

# ---------------- cd-ratio (35) ----------------
write('cd-ratio', build('cd-ratio', [
    "\U0001F9E0 Fundus (C/D Ratio) and Optic Nerve Assessor",
    "Enter vertical cup-disc ratio (C/D) of both eyes to assess glaucoma optic-nerve damage, asymmetry and the ISNT rule.",
    "Fundus (C/D Ratio) Optic Nerve Assessor",
    "/ C/D Ratio Optic Nerve Assessor",
    '\U0001F4D6 View the "Fundus (C/D Ratio) and Optic Nerve Assessor User Guide"',
    "Cup-disc ratio C/D ranges 0 to 1; glaucoma risk = C/D > 0.5 or inter-eye difference > 0.2 or violation of ISNT rule (superior>=nasal, nasal>=inferior, inferior>=temporal); any one met suggests optic-nerve change needing further assessment.",
    "Right eye OD vertical C/D",
    "Left eye OS vertical C/D",
    "ISNT rule violated (inferior rim thinning)",
    "\U0001F4CB C/D Ratio Grading",
    "Vertical C/D",
    "Routine follow-up",
    "Borderline/suspect",
    "Glaucoma suspect",
    "Visual field + OCT recheck",
    "Actively rule out glaucoma",
    "Inter-eye difference >0.2",
    "Assess the larger side",
    "ISNT rule: normal rim inferior>superior>nasal>temporal; inferior/superior rim thinning suggests glaucoma. Disc size affects C/D interpretation.",
    "\u26A0\uFE0F C/D assessment is affected by disc size and refraction; combine OCT, visual field and IOP for judgment; recommend ophthalmology follow-up.",
    'About "C/D Ratio Assessor"',
    "Grades vertical cup-disc ratio and validates the ISNT rule and inter-eye asymmetry, aiding glaucoma optic-nerve assessment.",
    "\U0001F4DA Deep Dive: Cup-Disc Ratio (C/D) Assessment",
    "Enter optic-disc cup/disc ratio OD, OS to assess glaucoma optic-nerve change.",
    "Judge asymmetry (difference >0.2) and ISNT rule.",
    "Follow up cup-disc ratio progression.",
    "Asymmetry = |0.6-0.3| = 0.3 > 0.2, and OD>0.5, suggests glaucoma optic-nerve change to investigate.",
    "Both eyes 0.4",
    "Asymmetry 0, both <0.5, no obvious abnormality, but combine RNFL and visual field.",
    "What C/D is abnormal?",
    "Single eye >0.5 or inter-eye difference >0.2 is suspect, must combine visual field and OCT-RNFL.",
    "What is ISNT?",
    "Normal disc temporal thinnest, superior/inferior thicker (Inferior>Superior>Nasal>Temporal) rhythm; violation suggests glaucoma.",
    'About "Fundus (C/D Ratio) Optic Nerve Assessor"',
    "Fundus cup-disc ratio (C/D) assessor: enters vertical C/D ratio, assesses glaucoma optic-nerve damage and validates ISNT rule and inter-eye asymmetry. A medical professional tool based on authoritative standards, for reference only.",
]))

# ---------------- detector-6 (36) ----------------
write('detector-6', build('detector-6', [
    "\U0001F476 Pediatric Amblyopia (Stereoscopic Acuity) Detector",
    "Stereoscopic acuity detection: assess children's stereoscopic visual development and amblyopia risk by age and measured stereoscopic acuity.",
    '\U0001F4D6 View the "Pediatric Amblyopia (Stereoscopic Acuity) Detector User Guide"',
    "Stereo screening thresholds by age: 3 yrs 200, 5 yrs 100, 7 yrs 60 arcsec; measured acuity <= threshold normal, <=2x borderline, <=400 amblyopia risk, >400 severe abnormality.",
    "1. Child age",
    "7 yrs and above",
    "2. Test method",
    "Titmus stereogram",
    "TNO random-dot stereogram",
    "Lang stereogram",
    "Yan random-dot stereogram",
    "3. Measured stereoscopic acuity",
    "40 arcsec (normal upper limit)",
    "50 arcsec",
    "60 arcsec (normal threshold)",
    "80 arcsec",
    "100 arcsec",
    "200 arcsec",
    "400 arcsec",
    "800 arcsec",
    "3000 arcsec (only rough stereo sense)",
    "Unrecognizable",
    "\U0001F4DA Deep Dive: Pediatric Stereoscopic Screening (Arcsec Thresholds)",
    "Interpret random-dot stereo measured values (arcsec) by age thresholds.",
    "Normal thresholds at 3/5/7 yrs are 200/100/60 arcsec respectively.",
    "Disposition advice for borderline and missing values.",
    "6 yrs measured 120 arcsec",
    "Threshold 100; 120 slightly exceeds but within 2x (<=200) judged borderline, suggest ruling out refractive error, recheck in 3-6 months.",
    "Measured 9999 (unrecognizable)",
    "Stereo loss suggests severe binocular vision disorder; immediate full eye exam to rule out amblyopia/strabismus.",
    "Why differ by age?",
    "Stereo matures with visual system development; young age has wide thresholds, school age approaches adult 60\" level.",
    "Does borderline matter?",
    "Not necessarily pathological, but with vision difference must watch for amblyopia, should follow up.",
    'About "Pediatric Amblyopia (Stereoscopic Acuity) Detector"',
    "Pediatric amblyopia (stereoscopic acuity) detector. Free online tool, pure front-end processing, data not uploaded, privacy-safe.",
]))

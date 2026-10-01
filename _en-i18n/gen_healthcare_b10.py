#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""healthcare 第10批：healthcare-5 / egfr / egfr-calculator / bsa-calculator / bmr-calculator"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'healthcare')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'healthcare')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        for i, it in enumerate(items):
            print('   ', i, repr((it.get('zh') or '')[:50]))
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
    out = {'slug': slug, 'industry': 'healthcare', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))


# ---------------- healthcare-5 (17) ----------------
write('healthcare-5', build('healthcare-5', [
    "🥗 Daily Protein Requirement Calculator",
    "Derive the daily protein target in grams from body weight and activity goal, from sedentary maintenance through endurance training to resistance training and cutting.",
    '📖 View the "Daily Protein Requirement User Guide"',
    "Activity factor 1=sedentary 1.2=light 1.5=moderate 2=high",
    "Goal 1=maintain 1.2=muscle gain 0.8=fat loss",
    "Protein requirement = weight × 0.8 g/kg × activity factor × goal factor",
    "Athletes or specific conditions require adjustment.",
    "📚 Deep Dive: Daily Protein Requirement Estimation",
    "Nutrition planning: estimate protein intake from weight and activity",
    "Muscle gain / recovery: high-intensity trainees and post-surgery patients need more",
    "Meal distribution: split the daily target across meals for easier execution",
    "Algorithm (this tool's convention): maintenance need = weight (kg) × 0.8 × activity factor; goal need = maintenance × goal multiple; per meal = goal need ÷ 4. Activity factor / goal multiple are user-entered (e.g. sedentary ~1.2, training ~1.5-1.6).",
    "Example 1 (70 kg, activity 1.2, goal 1.2): maintenance 70×0.8×1.2 = 67.2 g, goal 67.2×1.2 = 80.6 g, per meal 20.2 g. Example 2 (60 kg, activity 1.5, goal 1.6): maintenance 72.0 g, goal 115.2 g, per meal 28.8 g.",
    "Is more protein always better?",
    "No; excess protein adds to the kidney burden without building more muscle. A regular adult needs about 0.8-1.0 g/kg, exercisers/muscle-builders about 1.2-1.7 g/kg, and those with kidney disease need to limit protein and follow medical advice.",
    "Why multiply by activity?",
    'This tool takes 0.8 g/kg as the base, multiplies by the activity factor to estimate "maintenance", then by the goal multiple to get the "goal"; this is a simplified convention for rough estimation only, and precise needs depend on training volume and weight target.',
]))

# ---------------- egfr (16) ----------------
write('egfr', build('egfr', [
    "🫘 Estimated Glomerular Filtration Rate Calculator",
    "Estimate eGFR from serum creatinine, age and sex using the CKD-EPI equation, and stage the result from G1 to G5 with the chronic kidney disease category.",
    '📖 View the "eGFR Estimated Glomerular Filtration Rate (CKD-EPI) User Guide"',
    "Race coefficient",
    "CKD-EPI formula (simplified version)",
    "The result is for reference only; a medical diagnosis must consider the clinical picture.",
    "📚 Deep Dive: eGFR Estimated Glomerular Filtration Rate (CKD-EPI)",
    "Kidney function assessment: estimate eGFR from serum creatinine, age and sex to determine the CKD stage",
    "Dosing reference: adjust doses for chronic kidney disease patients and avoid nephrotoxic drugs",
    "Follow-up monitoring: track the eGFR trend and detect acute kidney injury",
    "Algorithm (CKD-EPI 2009, with race coefficient): κ = 0.9 for men and 0.7 for women (in mg/dL; this tool takes serum creatinine in µmol/L, converted by ÷88.4 first); eGFR = 141 × min(SCr/κ,1)^α × max(SCr/κ,1)^(-1.209) × 0.993^age × (female ×1.018) × (Black ×1.0+). Staging: ≥90 stage 1, 60-89 stage 2, 30-59 stage 3, 15-29 stage 4, <15 stage 5. Note: the 2021 new equation has dropped the race coefficient.",
    "Example 1 (serum creatinine 80 µmol/L, age 50, male): SCr = 80/88.4×0.9 = 0.814, eGFR = 141×0.814^(-0.411)×0.993^50 = 108.0 mL/min/1.73m², stage 1 (normal). Example 2 (serum creatinine 200 µmol/L, age 65, female): SCr = 200/88.4×0.7 = 1.583, eGFR = 141×1.583^(-1.209)×0.993^65×1.018 = 52.2, stage 3 (moderate decline).",
    "Which is more accurate, eGFR or creatinine?",
    "Serum creatinine is affected by muscle mass and diet; eGFR corrects for age and sex, comes closer to true kidney function and is the main basis for CKD staging and dosing, but it still needs to be combined with cystatin C, urine protein and more.",
    "What happens if the unit is wrong?",
    "This tool takes serum creatinine in µmol/L (÷88.4 to convert to mg/dL), while the egfr-calculator version takes mg/dL; the units differ between the two, and entering the wrong one is off by about 88 times, so check the unit carefully.",
]))

# ---------------- egfr-calculator (16) ----------------
write('egfr-calculator', build('egfr-calculator', [
    "🫘 eGFR Calculator with CKD-EPI and MDRD",
    "Compare the CKD-EPI and MDRD study estimates of glomerular filtration rate side by side from creatinine, age and sex, and read the matching kidney function stage.",
    '📖 View the "eGFR Glomerular Filtration Rate User Guide"',
    "Serum creatinine (mg/dL)",
    "CKD-EPI simplified: 175·Scr⁻¹·¹⁵⁴·age⁻⁰·²⁰³·(female ×0.742)",
    "An eGFR <60 for three months suggests chronic kidney disease; seek medical care.",
    "📚 Deep Dive: Simplified eGFR Estimation (CKD-EPI 175 Equation)",
    "Quick screening: estimate eGFR from serum creatinine (mg/dL), age and sex",
    "Education: understand the relationship between creatinine and kidney function",
    "Reference boundary: an eGFR <60 for three months suggests chronic kidney disease and requires medical care",
    "Algorithm (simplified): eGFR = 175 × SCr^(-1.154) × age^(-0.203) × (female ×0.742). Serum creatinine in mg/dL. SCr must be >0 and age >0.",
    "Example 1 (SCr 1.0 mg/dL, age 50, male): eGFR = 175×1.0^(-1.154)×50^(-0.203) = 79.1 mL/min. Example 2 (SCr 1.5 mg/dL, age 65, female): eGFR = 175×1.5^(-1.154)×65^(-0.203)×0.742 = 34.9 mL/min (below 60, indicating reduced kidney function; a nephrology visit is advised).",
    "How is it different from the egfr version?",
    "This version uses the simplified 175 equation with serum creatinine in mg/dL, whereas the egfr version uses the full CKD-EPI with µmol/L. The formulas and units differ, so the numbers are not directly comparable; enter values in the unit shown on the page.",
    "Does a low eGFR always mean kidney disease?",
    "Not necessarily; dehydration, infection and drugs can lower it transiently. Chronic kidney disease is defined as eGFR <60 for ≥3 months, requiring re-testing and judgement together with urine protein.",
]))

# ---------------- bsa-calculator (16) ----------------
write('bsa-calculator', build('bsa-calculator', [
    "📐 Body Surface Area Calculator",
    "Estimate body surface area with the DuBois equation from height and weight, used to size chemotherapy doses, burn fluid plans and paediatric drug dosing.",
    '📖 View the "Body Surface Area BSA User Guide"',
    "For medical calculations such as chemotherapy dosing.",
    "📚 Deep Dive: Body Surface Area BSA (DuBois Formula)",
    "Chemotherapy dosing: most cytotoxic drugs are dosed by BSA (mg/m²)",
    "Burn assessment: the burn area as a proportion of BSA guides fluid resuscitation and care",
    "Dose standardisation: remove the effect of weight and height differences to make dosing more comparable",
    "Algorithm (DuBois): BSA = 0.007184 × weight (kg)^0.425 × height (cm)^0.725, in m². Weight and height must be >0.",
    "Example 1 (65 kg / 170 cm): BSA = 0.007184 × 65^0.425 × 170^0.725 = 1.754 m². Example 2 (80 kg / 185 cm): BSA = 0.007184 × 80^0.425 × 185^0.725 = 2.036 m².",
    "Why is dosing based on ",
    "body surface area",
    "?",
    "Many drugs' clearance correlates better with body surface area, so dosing by BSA reduces individual differences between thin and heavy patients and improves the therapeutic index; the simplified Mosteller formula √(weight × height / 3600) can also be used.",
    "Does BSA have errors?",
    "DuBois works well for ordinary adults; obese patients or children need dedicated formulas (such as Haycock), and the error grows with extreme body types.",
]))

# ---------------- bmr-calculator (16) ----------------
write('bmr-calculator', build('bmr-calculator', [
    "🏋️ Basal Metabolic Rate Calculator",
    "Estimate resting daily calorie burn with the Mifflin-St Jeor equation from height, weight, age and sex, as the baseline for any nutrition or weight plan.",
    '📖 View the "BMR Basal Metabolic Rate Calculator User Guide"',
    "Mifflin-St Jeor: male 10W+6.25H−5A+5, female −161",
    "The baseline resting burn, not total daily expenditure.",
    "📚 Deep Dive: Basal Metabolic Rate BMR (Mifflin-St Jeor)",
    "Nutrition assessment: estimate the minimum resting calorie burn to plan a fat-loss/muscle-gain diet",
    "Calorie budget: multiply BMR by the activity factor to get the ",
    ", then set the intake target",
    "Education: understand how age and sex affect metabolism",
    "Algorithm (Mifflin-St Jeor): BMR = 10×weight (kg) + 6.25×height (cm) − 5×age + (male +5 / female −161), in kcal/day. All values must be >0.",
    "Example 1 (65 kg / 170 cm / age 30 / male): BMR = 10×65 + 6.25×170 − 5×30 + 5 = 650 + 1062.5 − 150 + 5 = 1568 kcal/day. Example 2 (55 kg / 160 cm / age 25 / female): BMR = 550 + 1000 − 125 − 161 = 1264 kcal/day.",
    "What is the difference between BMR and TDEE?",
    "BMR is the minimum burn while lying still; TDEE = BMR × activity factor (about 1.2 sedentary, 1.55 moderate, 1.9 high intensity) is the total daily expenditure. Fat-loss intake should be slightly below TDEE.",
    "Is the formula suitable for everyone?",
    "Mifflin-St Jeor is fairly accurate for ordinary adults; athletes, pregnant women and special situations such as hyperthyroidism/hypothyroidism deviate a lot, so it is only an estimate.",
]))

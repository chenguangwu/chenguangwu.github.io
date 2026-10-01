#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""healthcare 第11批（收尾）：antipyretic-dose / blood-pressure-grade / index"""
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


# ---------------- antipyretic-dose (15) ----------------
write('antipyretic-dose', build('antipyretic-dose', [
    "👶 Pediatric Antipyretic Liquid Dose Calculator",
    "Compute the single antipyretic dose in millilitres from a child's weight and the suspension concentration, with minimum and maximum dosing interval warnings included.",
    '📖 View the "Paediatric Antipyretic Liquid Dose User Guide"',
    "Volume = weight × dose (mg/kg) / concentration",
    "The daily limit for paracetamol is about 75 mg/kg; always follow the label.",
    "📚 Deep Dive: Pediatric Antipyretic Liquid Dose (Paracetamol)",
    "At-home dosing: convert the volume of paracetamol suspension by weight instead of pouring by eye",
    "Safety limit: work back from the maximum daily dose of 75 mg/kg to find the maximum number of doses per day",
    "Medication education: highlight the dosing interval and total dose to avoid double dosing and liver damage",
    "Algorithm: single volume = weight (kg) × dose (mg/kg) ÷ concentration (mg/mL); maximum doses per day = floor(daily limit 75 mg/kg ÷ single dose). Weight, dose and concentration must all be > 0. The result is a conversion reference only; actual dosing must follow the label and medical advice.",
    "Example 1 (weight 15 kg, dose 15 mg/kg, concentration 32 mg/mL): single dose = 15×15/32 = 7.0 mL; daily limit = floor(75/15) = 5 doses (that is, once every 4 hours, no more than 5 doses a day). Example 2 (weight 10 kg, dose 10 mg/kg, concentration 32 mg/mL): single dose = 10×10/32 = 3.1 mL; daily limit = floor(75/10) = 7 doses.",
    "How do I read the concentration?",
    'The suspension label shows mg/mL (or mg/5 mL); if it says "160 mg per 5 mL" the concentration is 32 mg/mL. Always check the concentration before converting the volume, as brands vary widely.',
    "Why is there a daily limit?",
    "A cumulative intake of more than 75 mg/kg of paracetamol in a day carries a risk of liver damage; working back from the limit to the number of doses helps prevent overdose from repeated dosing. Many cold medicines contain this ingredient, so the total must be added up.",
]))

# ---------------- blood-pressure-grade (15) ----------------
write('blood-pressure-grade', build('blood-pressure-grade', [
    "❤️ Blood Pressure Grade Classifier",
    "Classify a systolic and diastolic reading into the normal, elevated or hypertension grade bands, and show pulse pressure and mean arterial pressure for context.",
    '📖 View the "Blood Pressure Grade User Guide"',
    "Pulse pressure = systolic − diastolic",
    "Grades: normal <120/80, elevated 120-139/80-89, grade 1 140-159/90-99, grade 2 ≥160/100. For reference only; a doctor's diagnosis prevails.",
    "📚 Deep Dive: Adult Blood Pressure Grades and Pulse Pressure",
    "Home self-measurement: grade a reading from systolic/diastolic to spot high blood pressure",
    "Pulse pressure watch: a wide pulse pressure suggests arteriosclerosis and other conditions, useful as a reference when seeing a doctor",
    "Risk stratification: use the grade to decide between lifestyle changes and seeing a doctor",
    "Algorithm: pulse pressure = systolic − diastolic; grades follow the Chinese guideline: <120/80 normal, 120-129/<80 high-normal, 130-139/80-89 grade 1, 140-159/90-99 grade 2, ≥180/≥120 grade 3. This tool's thresholds: diastolic ≥80 is grade 1, systolic ≥140 is grade 2, systolic ≥180 is grade 3.",
    "Example 1 (120/80): pulse pressure 40 mmHg, graded level 3 by this tool's rules (Note: under the Chinese guideline 120/80 is high-normal; the tool's thresholds are stricter, for reference only). Example 2 (158/96): pulse pressure 62 mmHg → level 4 (grade 2 hypertension); medical attention is advised.",
    "What does a wide pulse pressure indicate?",
    "A pulse pressure >60 mmHg is commonly seen in arteriosclerosis, aortic regurgitation and other conditions; in older adults a widened pulse pressure is mostly related to reduced vascular elasticity and should be assessed as a whole.",
    "What should I watch for when self-measuring at home?",
    "Rest seated for 5 minutes, sit with your back supported and the cuff at heart level, and only elevations on three different days are more meaningful; a single high reading is no cause for alarm.",
]))

# ---------------- index (59) ----------------
write('index', build('index', [
    "🩺 Medical & Healthcare Tools",
    "Medical & Healthcare",
    "Medical & Healthcare Tools",
    "BMI Calculator",
    "Enter height and weight to compute BMI and grade weight status against the Chinese standard (<18.5 underweight, 18.5-24 normal, 24-28 overweight, ≥28 obese), for an initial screen of overweight and obesity in adults.",
    "Using the Mifflin-St Jeor equation, enter height, weight, age and sex to estimate the basal metabolic rate (BMR) - the minimum calories needed to sustain life at rest - for nutritional assessment and diet planning.",
    "TDEE Calculator",
    "Estimate total daily energy expenditure (TDEE) by multiplying BMR by an activity factor, and get calorie intake advice for fat loss (about 20% below TDEE), maintenance or muscle gain, for weight management and nutrition planning.",
    "Heart Rate Zone Calculator",
    "Heart rate training zone calculator. Estimate fat-burning, aerobic and other training zones using the maximum heart rate method, noting individual variation, for exercise intensity zoning and training plan reference.",
    "IV drip rate calculator. Enter the prescribed total volume and infusion time to compute the drip rate and total drops from the drop factor, for reference when adjusting clinical infusion rates (always combined with the patient's condition).",
    "Gestational week and due date calculator. Estimate the current gestational week and expected date of confinement (EDC) from the last menstrual period, noting that actual delivery may vary by about two weeks either way, for pregnancy self-management reference.",
    "Paediatric dose conversion tool. Convert an adult dose to a child dose by weight, noting that actual dosing must follow medical advice and must not be decided on your own, for paediatric dosing reference.",
    "Estimate adult ideal body weight with the Devine formula; just enter height and sex to get a reference value, used mainly for clinical drug dosing and nutritional assessment and only as a reference rather than a strict criterion of a healthy weight.",
    "Weight-based dosing calculator. Enter weight and the mg/kg dosing strength to compute the daily dose, noting that the specific medication must follow medical advice and this tool only performs the calculation, for dose estimation reference.",
    "Enter a child's age, sex, height and weight to estimate BMI and compare it against the percentile curve for that age and sex, giving a weight-status reference (a simplified teaching version); using it together with the CDC/WHO growth charts is recommended.",
    "Using the Devine formula, enter height and sex to compute adult ideal body weight (IBW), often used as a reference baseline for clinical drug dose adjustment and nutritional support, rather than a criterion for judging healthy weight.",
    "Finance (Cost / Profit / Report) Analysis",
    'Enter one "department, revenue, cost" line per row. Surplus = revenue − cost; cost ratio = cost ÷ revenue × 100%; surplus ratio = surplus ÷ revenue × 100%. The totals give the hospital-wide revenue, cost and net surplus, and identify the department with the highest surplus and the number of loss-making departments.',
    "Body Fat Percentage Estimation",
    "Enter height, weight, age and sex to estimate body fat percentage with the Deurenberg formula, giving a rough reference for body composition and helping track body fat changes during a fitness or fat-loss programme (a rough estimate only).",
    "Fat loss calorie deficit calculator. Estimate the daily calorie deficit from a target weight loss and a number of days (a safe range of 500-1000 kcal/day is suggested), for calorie planning in a fat-loss programme.",
    "GFR Creatinine Clearance Cockcroft",
    "Using the Cockcroft-Gault equation, enter age, weight, serum creatinine and sex to estimate creatinine clearance, often used for drug dose adjustment in kidney patients and as a clinical reference for renal function status.",
    "Paediatric antipyretic liquid dose calculator. Convert the volume of paracetamol suspension by weight, noting a daily limit of about 75 mg/kg, for dosing reference when treating a child's fever (follow the label).",
    "CHADS2-VASc score tool. Enter the risk factors of an atrial fibrillation patient - congestive heart failure, hypertension, age and so on - to total the stroke risk score, for reference in anticoagulation decisions.",
    "Daily water intake recommendation calculator. Estimate daily water intake from weight and activity/climate (including water from food; needs rise in hot weather and with exercise), for daily hydration management reference.",
    "Body surface area (BSA) calculator. Estimate body surface area with the DuBois formula, for medical calculation reference in chemotherapy dosing, burn area and drug administration.",
    "eGFR Glomerular Filtration Rate",
    "Using the simplified CKD-EPI equation, enter serum creatinine, age and sex to estimate the glomerular filtration rate (eGFR), assess kidney function and flag abnormalities (for example, an eGFR <60 persisting for three months suggests chronic kidney disease and a need to see a doctor).",
    "Using the Widmark formula, enter the amount of alcohol consumed, the ABV, weight and sex to estimate blood alcohol concentration (BAC) and the time to metabolise back to zero, flagging drink-driving risk; the result is for health and legal awareness reference only.",
    "Nutritional risk NRS2002 screening tool. Enter the scoring items - impaired nutrition, disease severity, age and so on - to total the nutritional risk score, for nutritional risk screening of inpatients (always combined with clinical judgement).",
    "Hyponatraemia correction rate estimator. Enter the serum sodium and a target value to estimate the rate of sodium rise during treatment, making clear it is a teaching estimate only and that clinical treatment must be individualised, for medical teaching reference.",
    "Wells Pulmonary Embolism Score",
    "Wells pulmonary embolism score tool. Enter the clinical suspicion items (such as signs of lower-limb deep vein thrombosis and heart rate) to total the Wells score and judge the likelihood of pulmonary embolism; it must be combined with D-dimer or imaging tests, for emergency triage reference.",
    "MAP mean arterial pressure calculator. Enter systolic and diastolic pressure to estimate mean arterial pressure as MAP ≈ diastolic + (systolic − diastolic)/3, reflecting organ perfusion pressure, for circulatory monitoring reference.",
    "Parkland Burn Fluid Resuscitation",
    "Enter the burn area (rule of nines/LBSA) and weight to estimate the total 24-hour fluid volume and the first 8-hour amount after an adult burn using the Parkland formula, giving an initial reference for the fluid resuscitation plan in burn rescue.",
    "QTc Corrected Heart Rate",
    "Using the Bazett formula, enter the measured QT interval and heart rate to compute the corrected QTc, assess whether the QT interval is prolonged and its link to arrhythmia risk, for ECG result and medication monitoring.",
    "eGFR Estimated Glomerular Filtration Rate",
    "Using the full CKD-EPI equation, enter serum creatinine, age, sex, race and so on to estimate the glomerular filtration rate (eGFR) and assess the kidney function stage; the result is for reference only and a medical diagnosis requires clinical tests.",
    "Assess the Apgar score from five items - heart rate, respiration, muscle tone, reflex and skin colour - at 1 and 5 minutes after birth to judge the degree of asphyxia and the effect of resuscitation, for initial newborn assessment in the delivery room.",
    "Based on weight and activity level (sedentary, exercising, high-intensity training), estimate the recommended daily protein intake and give a distribution suggestion, for nutrition planning in scenarios such as fitness muscle gain and post-operative recovery.",
    "Based on the Morse Fall Scale, enter items such as recent fall history, gait and whether aids are needed to quickly compute a fall risk score, for fall screening of inpatients and determining the level of nursing intervention.",
    "Quality (Management / System / Check) Mechanism",
    "Quality (Management / System / Check) Mechanism is a free online medical & healthcare tool - a GSP quality management compliance self-check tool for pharmaceutical operations, scoring across eight dimensions: quality system, staff training, facilities and equipment, purchasing and acceptance, storage and maintenance, sales and after-sales, transport and delivery, and information management. Runs entirely in the front end...",
    "Blood Pressure Grade",
    "Blood pressure grade tool. Enter systolic/diastolic pressure to grade the reading and compute pulse pressure against the standard (normal <120/80, grade 1 140-159/90-99 and so on); for self-check only, with a doctor's diagnosis prevailing.",
    "Respiratory rate assessment tool. Enter the resting respiratory rate to judge whether it is normal or an abnormal level, flagging that you should see a doctor promptly if it is abnormal, for vital-sign self-check reference.",
    "NYHA heart function classification tool. Assess the heart function class (I-IV) by the degree of activity limitation, for evaluating heart failure severity and as a reference for exercise tolerance.",
    'About "Medical & Healthcare Tools"',
    "The Medical & Healthcare Tools collection includes 35 free online tools covering common calculation, conversion and lookup needs in medical and healthcare settings. Whether you are a practitioner, a student or a general user, you will find handy tools here that are ready to use instantly. All tools run entirely in the front end, upload no data to any server and keep your privacy safe.",
    "The medical and healthcare tools on this page include (a selection of representative tools):",
    "These tools help you complete common medical and healthcare tasks quickly, with no need to memorise complex formulas or convert by hand - just enter your values and get results.",
    "Do the medical and healthcare tools require downloading or registration?",
    "No. All the medical and healthcare tools on this page are pure front-end online tools that work as soon as you open the page - no software to install, no account to register and no data uploaded.",
    "Are the results of the medical and healthcare tools accurate? Is the data safe?",
    "The tools compute locally in your browser based on public mathematical formulas and common industry standards, with results available instantly. All calculations are performed on your device; no data is uploaded to any server, so your privacy is protected.",
]))

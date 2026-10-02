#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'cardiology')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'cardiology')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
DISCL = "Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected."
EXTRA = {}
def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items)); sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en)); sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en)); sys.exit(1)
        mp[z] = en
    return mp
def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'cardiology', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # calc-3 (28)
    write('calc-3', build('calc-3', [
        "❤️ MI TIMI Risk Stratification (STEMI 30-day mortality)",
        "Assess acute STEMI prognosis by age, vitals, Killip class, weight, infarct site, presentation time and comorbidities.",
        "MI TIMI Risk Stratification",
        " / MI TIMI Risk Stratification",
        "📖 View 'MI TIMI Risk Stratification (STEMI 30-day mortality) User Guide'",
        "This tool sums TIMI risk score (STEMI 30-day mortality) items, giving risk stratification and reperfusion reference; calculation is local, data not uploaded, results for reference only, treatment follows guidelines and bedside assessment.",
        "Age group",
        "Under 65",
        "Heart rate >100 bpm",
        "Systolic BP <100 mmHg",
        "Killip class",
        "Class II-IV",
        "Weight <67 kg",
        "Anterior STEMI or LBBB",
        "Symptom-to-treatment >4 h",
        "Diabetes / hypertension / angina history",
        "📚 In-depth: MI TIMI Risk Stratification (STEMI 30-day mortality)",
        "TIMI scoring (STEMI 30-day mortality): age >=75, >=65 and <75, diabetes/hypertension/angina history, SBP <100, HR >100, Killip >=2, weight <67 kg, anterior ST elevation or LBBB, presentation >=4h each 1 point (0-14).",
        "Risk stratification: higher score means greater 30-day mortality (e.g. >=4 is high risk), guiding reperfusion strategy and monitoring intensity.",
        "Reperfusion aid: high-risk patients get priority emergency PCI or thrombolysis, with stronger ICU monitoring and complication prevention.",
        "Default demonstration (STEMI TIMI risk score)",
        "Input: male, 72, hypertension, SBP 96 mmHg, HR 104, Killip II, anterior ST elevation, 3.5h. Output: TIMI 7 (>=4 high), 30-day mortality ~10%-15% range, advice immediate reperfusion (PCI first) + ICU. Note: score is for triage; treatment follows guidelines and bedside.",
        "What items does TIMI score include?",
        "8 items total: age tier, risk factors (diabetes/hypertension/angina), shock signs (low SBP, fast HR), Killip >=2, low weight, anterior ST elevation or LBBB, presentation delay >=4h, each 1 point, total 0-14 mapping rising 30-day mortality.",
        "High score means surgery for sure?",
        "High score suggests high risk; reperfusion (PCI or thrombolysis) and intensified monitoring help more, but surgery also depends on time window, bleeding risk and imaging. Score is an aid, not the sole basis.",
        "What is the STEMI-time relationship?",
        "Myocardial necrosis progresses with occlusion time; shorter door-to-balloon time means better outcome; guidelines stress opening the vessel within 12h of onset, especially ASAP; beyond window but with ischemia can be individualized.",
    ]))

    # cardiac-rehab-mets (57)
    write('cardiac-rehab-mets', build('cardiac-rehab-mets', [
        "🦿 Cardiac Rehab (METs) Equivalence Converter",
        "Convert metabolic equivalents (METs) to equivalent daily activity/exercise and VO2, aiding cardiac rehab exercise prescription",
        " / Cardiac Rehab METs Converter",
        "📖 View 'Cardiac Rehab (METs) Equivalence Converter User Guide'",
        "Target heart rate = resting HR + (max HR - resting HR) x 40-80%",
        "Enter METs value",
        "Weight (kg, for VO2)",
        "📋 METs Activity Levels & Equivalent Activities",
        "Equivalent activity",
        "Very light",
        "Sleep, sitting, watching TV, reading, eating",
        "Light",
        "Slow walk (2km/h), cooking, light housework, shopping",
        "Moderate-light",
        "Walk (4km/h), golf, tai chi, light gardening",
        "Brisk walk (5.5km/h), cycling (15km/h), table tennis, stairs",
        "Moderate-heavy",
        "Jog (8km/h), singles tennis, swimming (leisure), aerobics",
        "Heavy",
        "Run (10km/h), basketball, swimming (fast), hiking",
        "Very heavy",
        "Run (12km/h), soccer, fast rope skipping",
        "Extreme",
        "Run (>=14km/h), HIIT",
        "📊 Cardiac Rehab Exercise Prescription Target METs",
        "Rehab phase",
        "Target METs",
        "Inpatient (Phase I)",
        "Bedside activity, slow walking",
        "Early (Phase II)",
        "Walking, ergometer, light resistance",
        "Mid (Phase III)",
        "Brisk walk, jog, swim, cycle",
        "Maintenance (Phase IV)",
        "Jog, ball sports, aerobics",
        "Note: 1 MET = 3.5 mL/kg/min VO2 = resting seated oxygen uptake. Prescription should use the safe METs range from CPET or 6MWT. Intensity usually 40-80% of peak VO2 or AT level. Target HR = resting HR + (max HR - resting HR) x 40-80%. For clinical reference only.",
        "📚 In-depth: Cardiac Rehab (METs) Equivalence Converter",
        "Prescription METs conversion: convert METs of running, cycling, brisk walking (1 MET ~ resting VO2 3.5 ml/kg/min) to training intensity, setting Phase I (inpatient), II (outpatient), III (community) goals.",
        "Daily activity equivalence: convert chores like mopping, stairs, shopping to METs-minutes, estimating energy cost and cardiac load, guiding return to work and life.",
        "Rehab phases and cautions: set target HR and ceiling from LVEF and exercise test, recognize warning signs like chest tightness/dyspnea, ensuring safe progression.",
        "Default demonstration (daily activity METs conversion)",
        "Input: activity moderate cycling 30 min, ~6 METs, weight 70 kg. Output: energy ~6x3.5x70x30/1000 = 44.1 kcal, METs-minutes 180, cardiac load moderate, advice include in Phase II aerobic prescription, caution HR not exceed ischemic threshold. Note: exact intensity by treadmill test.",
        "What are METs?",
        "Metabolic equivalent (MET) is an exercise intensity unit; 1 MET ~ resting seated VO2 3.5 ml/(kg-min). Higher means harder: walk ~2-3 METs, jog ~7-8, intense sport >10.",
        "Who is cardiac rehab for?",
        "Stable patients post-MI, post-PCI/CABG, stable heart failure, transplant and some valve surgeries. Contraindicated in acute phase, uncontrolled arrhythmia, severe aortic stenosis; start after rehab physician assessment.",
        "How to set exercise intensity safely?",
        "Base on ischemic-threshold HR and anaerobic threshold from exercise test, set target HR zone and RPE; follow warm-up-aerobic-cool-down; on chest pain, obvious dyspnea or dizziness, slow down and seek care.",
        "About 'Cardiac Rehab (METs) Equivalence Converter'",
        "Cardiac rehab METs equivalence converter - converts METs to daily activity, sports and VO2, guiding cardiac rehab exercise prescription.",
        "Calculations follow international/Chinese cardiovascular guidelines and published formulas (ESC/ACC/AHA, etc.)",
        "Outputs risk stratification, key thresholds and grading in real time",
        "Inputs are verifiable, the process is transparent and traceable",
        "Data processed locally, not uploaded to server",
        "Exercise prescription METs conversion",
        "Daily activity equivalence",
        "Rehab phases and cautions",
    ]))

    # chads2-vasc (51)
    write('chads2-vasc', build('chads2-vasc', [
        "📋 AF CHA2DS2-VASc Thromboembolic Risk Assessor",
        "For non-valvular atrial fibrillation (NVAF) patients: stroke annual incidence assessment and oral anticoagulant (OAC) decisions",
        "AF (CHA2DS2-VASc) Thromboembolic Risk Assessor",
        " / CHA2DS2-VASc Scorer",
        "📖 View 'AF CHA2DS2-VASc Thromboembolic Risk Assessor User Guide'",
        "This tool sums CHA2DS2-VASc score to assess NVAF stroke risk and suggests balancing bleeding with HAS-BLED; calculation is local, data not uploaded, results for reference only, anticoagulation decided by doctor.",
        "Under 65",
        "65-74",
        "75 and over",
        "Components (check all that apply)",
        "C - Congestive heart failure / LV dysfunction",
        "H - Hypertension",
        "D - Diabetes",
        "S2 - Stroke/TIA/thromboembolism history",
        "V - Vascular disease (MI/PAD/aortic plaque)",
        "📋 CHA2DS2-VASc Score Components",
        "Congestive heart failure / LV dysfunction",
        "Age >=75",
        "Stroke/TIA/thromboembolism",
        "Vascular disease",
        "Age 65-74",
        "Sex (female)",
        "📊 Anticoagulation Decision (2023 ESC/AHA)",
        "Annual stroke risk",
        "Male recommendation",
        "Female recommendation",
        "No OAC needed",
        "No OAC (female 1 point = 0)",
        "Consider OAC",
        "Note: the lone female 1 point (Sc) does not raise stroke risk, so female 0 and 1 point both need no OAC. Valvular AF (moderate-severe mitral stenosis/mechanical valve) needs no scoring, all require warfarin. Assess HAS-BLED bleeding risk before anticoagulation. For clinical reference only.",
        "📚 In-depth: AF CHA2DS2-VASc Thromboembolic Risk Assessor",
        "CHA2DS2-VASc scoring: CHF, hypertension, age >=75 (2), diabetes, stroke/TIA history (2), vascular disease, age 65-74, female each 1 point (0-9).",
        "Anticoagulation indication: male >=2, female >=3 recommend OAC; male 1 or female 2 can be individualized; 0 (male)/1 (female) generally no anticoagulation.",
        "Bleeding risk: assess HAS-BLED before starting; high bleeding risk (>=3) does not mean stop anticoagulation but correct reversible factors (BP, INR, drugs).",
        "Default demonstration (NVAF stroke",
        "Input: female, 73, hypertension, no diabetes, no stroke history, no heart failure, no vascular disease. Output: CHA2DS2-VASc 3 (age 2 + hypertension 1), anticoagulation advice recommend oral anticoagulation (female >=3), HAS-BLED needs separate assessment, note monitor bleeding regularly. Note: specific drug (warfarin/DOAC) chosen by doctor with renal function and adherence.",
        "Why do sex scores differ between male and female?",
        "The lone female as a risk factor has lower weight; guidelines remove 'female only' from the anticoagulation indication: male >=2, female >=3 recommend anticoagulation; male 1 or female 2 is a gray zone, decide individually after weighing benefit and bleeding.",
        "What anticoagulant to take?",
        "Options: warfarin (monitor INR 2.0-3.0) or DOAC (e.g. dabigatran/rivaroxaban, by renal function). Choice depends on renal function, adherence, cost and bleeding history; do not switch or stop on your own.",
        "What else to check after anticoagulation?",
        "Regularly review renal function and blood count, watch for black stool/hematuria/gum bleeding; combo drugs (antiplatelet, NSAID) need physician assessment. Even with high bleeding risk, prioritize controlling reversible factors rather than blindly stopping anticoagulation.",
        "About 'AF (CHA2DS2-VASc) Thromboembolic Risk Assessor'",
        "CHA2DS2-VASc scorer - for NVAF patients' stroke risk assessment and anticoagulation decisions, scoring heart failure, hypertension, age, diabetes, stroke history, vascular disease.",
        "Calculations follow international/Chinese cardiovascular guidelines and published formulas (ESC/ACC/AHA, etc.)",
        "Outputs risk stratification, key thresholds and grading in real time",
        "Inputs are verifiable, the process is transparent and traceable",
        "Data processed locally, not uploaded to server",
        "CHA2DS2-VASc score accumulation",
        "Anticoagulation indication",
        "Bleeding risk weighing",
    ]))

    # ckd-epi (40)
    write('ckd-epi', build('ckd-epi', [
        "🫘 eGFR (CKD-EPI 2021) & Cardio-Renal Assessor",
        "Use CKD-EPI 2021 (race-free) equation to estimate GFR, combined with albuminuria staging for CKD staging and cardio-renal risk",
        "Core formulas (by input variables): 142 x min(Scr/k, 1)^alpha x max(Scr/k, 1)^(-1.200) x 0.9938^Age x (1.012 if female); 142 x (minPart)^alpha x (maxPart)^-1.200 x (0.9938)^age; Math.round(egfr*10)/10",
        "GFR (CKD-EPI) & Cardio-Renal Assessor",
        " / eGFR Cardio-Renal Assessor",
        "📖 View 'eGFR (CKD-EPI 2021) & Cardio-Renal Assessor User Guide'",
        "Serum creatinine Scr (mg/dL)",
        "Urine albumin/creatinine UACR (mg/g)",
        "Normal or high",
        "Mildly decreased",
        "Mild-moderate decreased",
        "Moderate-severe decreased",
        "Kidney failure",
        "📊 Albuminuria Staging (by UACR)",
        "Normal to mildly increased",
        "Moderately increased (microalbuminuria)",
        "Severely increased (macroalbuminuria)",
        "🔥 Cardio-Renal Risk Heatmap (KDIGO)",
        "Note: CKD-EPI 2021 equation removes the race coefficient, more applicable worldwide. Heart failure with CKD (cardio-renal syndrome) patients use ACEI/ARB/MRA cautiously or at reduced dose; SGLT2i has cardio-renal protection. eGFR<30 needs dose adjustment of many drugs. For clinical reference only.",
        "📚 In-depth: eGFR (CKD-EPI 2021) & Cardio-Renal Assessor",
        "eGFR calculation (CKD-EPI 2021): estimate GFR from serum creatinine (or cystatin C, or both), age and sex; 2021 formula removed the Black race coefficient, fairer.",
        "CKD staging: by eGFR into G1(>=90)-G5(<15) with albuminuria A1-A3 overlay, assessing chronic kidney disease progression and cardiovascular risk.",
        "Cardio-renal syndrome assessment: with heart failure/CAD, falling eGFR and albuminuria signal worse prognosis, guiding diuretic dose and contrast use.",
        "Default demonstration (eGFR estimation)",
        "Input: female, 68, serum creatinine 110 umol/L, cystatin C 1.3 mg/L. Output: eGFR ~48 ml/min/1.73m2 (G3a), combined class moderate-severe decrease, cardiovascular note cardio-renal co-management, advice control BP (target by albuminuria), limit salt, avoid nephrotoxic drugs. Note: eGFR affected by muscle mass; sarcopenia lowers creatinine and overestimates.",
        "How does the 2021 formula differ from the old one?",
        "CKD-EPI 2021 dropped the 'Black' race correction coefficient, using a unified formula, reducing estimation bias from racial assumptions; it also offers creatinine, cystatin C and combined algorithms, the combined being more accurate.",
        "Does low eGFR always mean dialysis?",
        "Not necessarily. G5 (<15) with uremic symptoms/severe complications considers dialysis or transplant; G3-G4 focuses on BP, glucose, kidney protection and cardiovascular risk management; trend over time matters more than a single value.",
        "Why check renal function in cardiovascular patients?",
        "Heart failure and CAD often coexist with CKD; eGFR and albuminuria are key for prognosis and dosing of contrast, digoxin, glucose-lowering drugs; when cardio-renal worsen together, multidisciplinary management is needed to avoid nephrotoxic drug stacking.",
        "About 'GFR (CKD-EPI) & Cardio-Renal Assessor'",
        "CKD-EPI 2021 equation GFR (eGFR) calculator - with albuminuria staging assesses chronic kidney disease and cardio-renal syndrome risk.",
        "Calculations follow international/Chinese cardiovascular guidelines and published formulas (ESC/ACC/AHA, etc.)",
        "Outputs risk stratification, key thresholds and grading in real time",
        "Inputs are verifiable, the process is transparent and traceable",
        "Data processed locally, not uploaded to server",
        "eGFR calculation (CKD-EPI 2021)",
        "CKD staging",
        "Cardio-renal syndrome assessment",
    ]))

    # coronary-calcium (41)
    write('coronary-calcium', build('coronary-calcium', [
        "🫀 Coronary Calcium Score (Agatston) Interpreter",
        "By cardiac CT Agatston calcium score and age-sex percentile, assess coronary atherosclerosis degree and cardiovascular risk",
        "Core formulas (by input variables): min(8,max(3,Math.floor(age/10)))",
        " / Coronary Calcium Score Interpreter",
        "📖 View 'Coronary Calcium Score (Agatston) Interpreter User Guide'",
        "Agatston calcium score (CACS)",
        "Interpretation",
        "📋 Agatston Calcium Score Grading",
        "CHD risk",
        "Statin advice",
        "Very low (5-10y event rate <1%)",
        "Consider not starting / stopping statin",
        "Suggest moderate-intensity statin",
        "Recommend statin therapy",
        "Extensive",
        "Intensify statin + assess ischemia",
        "Intensify statin + coronary angiography / CTA",
        "📊 MESA cohort: CACS value for risk reclassification",
        "10-year CHD event rate (approx.)",
        "Note: CACS=0 (zero score) has very low 5-10y cardiovascular event rate, consider not starting or cautiously stopping statin (CAC Consortium consensus). CACS>=100 or >=75th percentile means significantly higher risk, recommend starting/intensifying statin. CACS not for known CAD or symptomatic patients. For clinical reference only.",
        "📚 In-depth: Coronary Calcium Score (Agatston) Interpreter",
        "Agatston scoring: by CT plaque area and peak CT value (130-199/200-399/400+ HU map to 1/2/3) sum weighted per vessel to total score.",
        "Risk stratification: 0 very low; 1-99 mild; 100-399 moderate; >=400 severe; higher score means greater future CHD event risk.",
        "Statin decision aid: intermediate-risk patients with score >=100 lean toward intensive lipid lowering; score 0 with no other high-risk factors can defer statin and reinforce lifestyle.",
        "Default demonstration (Agatston score grading)",
        "Input: LAD plaque area 40 mm2, peak 320 HU (factor 2); circumflex area 15 mm2, peak 160 HU (factor 1); RCA area 20 mm2, peak 250 HU (factor 2). Output: Agatston total 40x2+15x1+20x2 = 155, grade moderate (100-399), advice intermediate-risk consider moderate-high intensity statin + lifestyle. Note: only suggests risk; drug use by doctor.",
        "Does a calcium score of 0 mean no disease?",
        "Not entirely. 0 suggests very low CHD risk for the next 5-10 years, but non-calcified (soft) plaques can still cause acute events; with typical symptoms or high-risk factors like diabetes, still combine with clinical and other exams.",
        "High score means statin for sure?",
        "Not absolute. Score refines risk: intermediate-risk with >=100 often leans to lipid intervention; already high-risk (diabetes, family early history) already on statin. Final by overall risk stratification and doctor decision.",
        "How often to recheck?",
        "CACS grows slowly and is generally not checked yearly; mostly used once",
        "for assessment and decisions.",
        "About 'Coronary Calcium Score (Agatston) Interpreter'",
        "Coronary calcium score (Agatston) interpreter - by CT calcium score and age-sex percentile assesses cardiovascular risk and guides statin therapy decisions.",
        "Calculations follow international/Chinese cardiovascular guidelines and published formulas (ESC/ACC/AHA, etc.)",
        "Outputs risk stratification, key thresholds and grading in real time",
        "Inputs are verifiable, the process is transparent and traceable",
        "Data processed locally, not uploaded to server",
        "Agatston score calculation",
        "Statin decision aid",
    ]))

if __name__ == "__main__":
    main()

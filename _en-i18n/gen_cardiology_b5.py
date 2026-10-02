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
    # rater-risk-3 (41)
    write('rater-risk-3', build('rater-risk-3', [
"GRACE Ischemic Event Risk Score",
"Predicts in-hospital mortality risk for acute coronary syndrome (ACS) patients. Based on the GRACE registry, integrating 8 indicators by table lookup with summation; higher score means higher risk.",
"GRACE (Coronary Death Risk) Score",
"/ GRACE (Coronary Death Risk) Score",
"View the GRACE Ischemic Event Risk Score User Guide",
"This tool assesses ACS ischemic and mortality risk by GRACE registry score summation; scoring runs locally, data is not uploaded, results are for reference only, and invasive timing follows the guidelines.",
"Admission heart rate (beats/min)",
"Systolic blood pressure (mmHg)",
"Serum creatinine (mg/dL)",
"Class I (no heart failure)",
"Class II (bilateral crackles / S3)",
"Class III (acute pulmonary edema)",
"Class IV (cardiogenic shock)",
"Cardiac arrest before admission",
"ST-segment deviation",
"Elevated cardiac enzymes / troponin",
"GRACE score is used for prognostic risk stratification in ACS (unstable angina / NSTEMI / STEMI) patients",
"Low risk <=108, intermediate 109-140, high >140; high-risk patients are advised early revascularization",
"Serum creatinine 1 mg/dL ~ 88.4 micromol/L; please note unit conversion when entering",
"This tool is for clinical reference only and cannot replace comprehensive physician judgment; it runs purely client-side and uploads no data",
"In-Depth: GRACE Ischemic Event Risk Score",
"GRACE ischemic event score: age, heart rate, SBP, creatinine, Killip, biomarkers, ST deviation and arrest history weighted and summed to predict in-hospital and long-term death / ischemia in ACS.",
"Risk stratification and invasive timing: high score (mostly >140) favors angiography + PCI within 24h; very high risk intervenes immediately.",
"Prognosis and follow-up: the score links to 6-month event risk, guiding post-discharge dual antiplatelet duration, statin intensity and rehabilitation.",
"Default Data Walkthrough (GRACE Ischemic Risk)",
"Inputs: Male, 61 y, HR 96, SBP 118, creatinine 100, Killip I, troponin +, ST depression, no arrest. Output: GRACE ~109, Stratification Intermediate, Advice Early invasive (angiography within 24h), Follow-up DAPT + high-intensity statin. Note: Value varies with indicators; use the latest.",
"How to choose between GRACE and TIMI?",
"Both are used for ACS risk; GRACE has more items (BP / renal / Killip) and more stable mortality prediction, guidelines often use it to set invasive timing; TIMI has fewer items and leans toward ischemic events. They are complementary, not mutually exclusive.",
"Is an invasive strategy always better?",
"Early angiography improves outcomes in high / very-high-risk NSTE-ACS; low-risk with high bleeding risk may start conservative therapy + stress testing. Timing depends on stability, bleeding and team conditions, per chest-pain-center protocol.",
"What else to manage after discharge?",
"Dual antiplatelet (duration by disease), high-intensity statin, beta-blocker / ACEI and other secondary prevention, combined with cardiac rehab; tailor follow-up intensity by GRACE risk and control risk factors to reduce recurrence.",
"About the GRACE Ischemic Event Risk Score",
"The GRACE score originates from the Global Registry of Acute Coronary Events, integrating 8 indicators - age, heart rate, blood pressure, renal function, Killip class, cardiac arrest, ST changes and cardiac enzymes - to assess in-hospital and long-term mortality risk in ACS patients, a key basis for guiding revascularization timing.",
"Table lookup summation per the GRACE registry",
"Real-time total score and in-hospital mortality rate",
"Low / intermediate / high risk stratification and management advice",
"Acute coronary syndrome prognostic assessment",
"Revascularization timing decision aid",
"CCU / chest-pain-center risk stratification",
"Cardiovascular clinical teaching practice",
    ]))

    # statin-dose (60)
    write('statin-dose', build('statin-dose', [
"Statin (LDL-C Lowering) Dose Converter",
"Calculates the required LDL-C reduction from baseline and target, matching statin intensity grade and specific drug dosage regimen",
"/ Statin Dose Converter",
"View the Statin (LDL-C Lowering) Dose Converter User Guide",
"Required LDL-C reduction = (baseline LDL - target LDL) / baseline LDL x 100%; reduction >=50% matches high-intensity statin (atorvastatin 40-80 mg or rosuvastatin 20-40 mg), 30%-49% matches moderate (atorvastatin 10-20 mg, rosuvastatin 5-10 mg, simvastatin 20-40 mg), <30% matches low intensity (simvastatin 10 mg, pravastatin 10-20 mg); recheck lipids and monitor liver enzymes and creatine kinase 4-6 weeks after starting.",
"Target LDL-C (mmol/L)",
"2.6 - low-risk target",
"1.8 - high-risk / ASCVD target",
"1.4 - very-high-risk target",
"1.0 - very-high-risk + recurrent events",
"Statin Intensity Grading (ACC/AHA)",
"LDL-C reduction",
"Drug and dosage",
"Atorvastatin 40-80 mg",
"Rosuvastatin 20-40 mg",
"Moderate intensity",
"Atorvastatin 10-20 mg",
"Rosuvastatin 5-10 mg",
"Simvastatin 20-40 mg",
"Pravastatin 40-80 mg",
"Fluvastatin 40-80 mg",
"Pitavastatin 2-4 mg",
"Low intensity",
"Simvastatin 10 mg",
"Pravastatin 10-20 mg",
"Fluvastatin 20-40 mg",
"Single-Agent Equivalent Dose Conversion",
"Atorvastatin",
"Rosuvastatin",
"Simvastatin",
"-(80 mg contraindicated)",
"Pitavastatin",
"Pravastatin",
"Note: Simvastatin 80 mg is restricted by the FDA due to high myopathy risk. When monotherapy misses target, combine ezetimibe (additional ~20% LDL-C reduction) or PCSK9 inhibitor (additional 50-60%). If maximal statin + ezetimibe still misses target, add PCSK9i. Monitor liver enzymes and CK. For clinical reference only.",
"In-Depth: Statin (LDL-C Lowering) Dose Converter",
"Lowering-grade classification: High-intensity statin lowers LDL-C >=50% (e.g. atorvastatin 40-80, rosuvastatin 20-40 mg), moderate 30%-49%, low <30%.",
"LDL-C target: Very high risk (ASCVD, diabetes + target-organ damage) mostly <1.4 mmol/L and >=50% below baseline; moderate-high risk sets target by stratification.",
"Goal attainment and monitoring: Choose intensity by baseline LDL-C and gap to target, recheck liver enzymes / creatine kinase at 4-12 weeks, watch for myalgia and other adverse effects.",
"Default Data Walkthrough (Statin Intensity and Goal)",
"Inputs: Male, 60 y, MI history (very high risk), baseline LDL-C 3.0 mmol/L, target <1.4. Output: Required reduction >=53%, Recommend High-intensity statin (e.g. rosuvastatin 20 mg), Expected LDL-C ~1.3-1.5, Advice Recheck liver enzymes / CK at 4-12 weeks, Alert Report myalgia promptly. Note: Target and dosage set by physician.",
"Is high-intensity statin always better?",
"For ASCVD very-high-risk patients, large LDL-C lowering more markedly reduces events, so high intensity is often preferred; but the elderly, small/frail, renal/hepatic abnormality or myopathy history require careful weighing - moderate intensity + ezetimibe / PCSK9i may reach target, avoiding blind dose escalation.",
"What to check when taking statins?",
"Baseline liver enzymes and creatine kinase before medication; recheck LDL-C goal attainment and liver enzymes / CK at 4-12 weeks; seek care promptly for myalgia, fatigue or tea-colored urine. Most tolerate well; do not stop on rumors and cause event rebound.",
"What if LDL-C will not come down?",
"First confirm adherence and dosage; if still high, combine ezetimibe or PCSK9 inhibitor; also manage diet, exercise and smoking cessation. Target depends on risk stratification (very high risk mostly <1.4), set individually by cardiology.",
"About the Statin (LDL-C Lowering) Dose Converter",
"Statin LDL-C lowering amplitude and dose converter, calculating the required reduction from baseline and target LDL-C and recommending high / moderate intensity statin regimens.",
"Calculated item by item per international / Chinese cardiovascular guidelines and published formula standards (ESC/ACC/AHA, etc.)",
"Real-time output of risk stratification, key cutoff values and grading",
"Input values are verifiable; the process is transparent and traceable",
"Data is processed locally and not uploaded to any server",
"Lowering-amplitude grading",
"LDL-C target value",
"Goal attainment and monitoring",
"Intensity grading",
"Statins by LDL-C reduction: high intensity (average daily LDL-C reduction >=50%, e.g. atorvastatin 40-80 mg, rosuvastatin 20-40 mg), moderate (30%-49%), low (<30%).",
"Choose intensity target by cardiovascular risk stratification; doubling the dose lowers LDL-C by about an extra 6% (the 6% rule).",
"Boundary",
"Intensity varies greatly by specific statin and individual metabolism; dosage and medication must be prescribed by a physician, do not self-adjust, and watch for myopathy / liver enzyme monitoring.",
    ]))

    # timi-score (59)
    write('timi-score', build('timi-score', [
"MI TIMI Risk Stratification Tool",
"Thrombolysis In Myocardial Infarction - for risk stratification and treatment strategy guidance in NSTEMI/UA and STEMI patients",
"MI (TIMI) Risk Stratification Tool",
"/ TIMI Risk Stratification Tool",
"View the MI TIMI Risk Stratification Tool User Guide",
"1 point each item, total score 0-7",
"Age >=65 years",
">=3 CAD risk factors",
"Known coronary artery disease (stenosis >=50%)",
"Aspirin use within 7 days",
">=2 angina episodes within 24h",
"ST-segment deviation >=0.5 mm",
"Elevated cardiac biomarkers",
"Total score 0-14",
"<65 years (0 points)",
"65-74 years (2 points)",
">=75 years (3 points)",
"Systolic BP / heart rate",
"SBP>=100 and HR<100 (0 points)",
"SBP<100 or HR>100 (1 point)",
"SBP<100 and HR>100 (2 points)",
"Class I (0 points)",
"Class II-III (1 point)",
"Class IV (2 points)",
">=67 kg (0 points)",
"<67 kg (1 point)",
"Anterior MI or LBBB",
"Diabetes / hypertension / angina",
"Time from presentation to treatment >4h",
"NSTE-ACS TIMI Score and Risk",
"14-day death / MI / urgent revascularization",
"Strategy recommendation",
"Conservative management, elective evaluation",
"Early invasive strategy (angiography within 72h)",
"Urgent invasive strategy (angiography within 24h)",
"STEMI TIMI Score and 30-Day Mortality",
"30-day mortality",
"Note: The TIMI score is simple but rough; for NSTE-ACS it is recommended to combine with the GRACE score. STEMI TIMI is for prognostic assessment and does not replace emergency PCI decisions. For clinical reference only.",
"In-Depth: MI TIMI Risk Stratification Tool",
"TIMI risk score (STEMI 30-day death): age strata, risk factors, shock signs, Killip >=2, low weight, anterior ST elevation / LBBB, presentation delay >=4h - 8 items of 1 point each (0-14).",
"Risk stratification: >=4 points is high risk, 30-day mortality rises markedly, prioritize reperfusion and intensive monitoring.",
"Reperfusion and monitoring: High score supports emergency PCI / thrombolysis and ICU management, with preventive complication handling.",
"Default Data Walkthrough (STEMI TIMI Risk Score)",
"Inputs: Male, 66 y, diabetes, SBP 104, HR 98, Killip I, anterior ST elevation, onset 2.5h. Output: TIMI 4 points (high risk), 30-day mortality Elevated, Advice Immediate PCI + monitoring, Follow-up Post-discharge secondary prevention. Note: Score is for triage; treatment follows guidelines.",
"Are both TIMI and GRACE used for MI?",
"TIMI leans toward STEMI 30-day death and reperfusion decisions, fewer items; GRACE covers NSTE-ACS and broader prognosis. Acute chest pain often uses multiple scores complementarily, chosen by chest-pain-center protocol.",
"Why is presentation delay scored?",
"The longer from onset to reperfusion, the larger the infarct size and the worse the prognosis, so >=4h counts 1 point, emphasizing time is muscle, open the vessel as early as possible.",
"Can one be conservative after scoring?",
"STEMI recommends early reperfusion regardless of score (PCI preferred; if beyond window or unavailable, thrombolysis); high score only suggests more intensive monitoring and complication prevention, not changing reperfusion principle.",
"About the MI (TIMI) Risk Stratification Tool",
"The TIMI risk scorer is used for risk stratification in acute MI (NSTEMI/STEMI) patients, assessing death and ischemic event risk and guiding early invasive strategy decisions.",
"Calculated item by item per international / Chinese cardiovascular guidelines and published formula standards (ESC/ACC/AHA, etc.)",
"Real-time output of risk stratification, key cutoff values and grading",
"Input values are verifiable; the process is transparent and traceable",
"Data is processed locally and not uploaded to any server",
"TIMI Risk Score (STEMI 30-day death)",
"Risk stratification",
"Reperfusion and monitoring",
    ]))

if __name__ == "__main__":
    main()

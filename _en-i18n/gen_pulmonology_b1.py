#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'pulmonology')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'pulmonology')
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
    out = {'slug': slug, 'industry': 'pulmonology', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('anti-tb-dosing', build('anti-tb-dosing', [
        "💊 Anti-TB Quadruple Dosing and Hepatotoxicity Calculator",  # 0
        "Weight-based dosing of the HRZE quadruple regimen (isoniazid + rifampicin + pyrazinamide + ethambutol) and assessment of drug-induced liver injury (DILI) risk",  # 1
        "Anti-TB (Quadruple) Dosing and Hepatotoxicity Calculator",  # 2
        "/ Anti-TB (Quadruple) Dosing and Hepatotoxicity Calculator",  # 3
        "📖 View the Anti-TB Quadruple Dosing and Hepatotoxicity Calculator user guide",  # 4
        "Anti-TB dosing by weight: isoniazid INH = weight x 5 mg (cap 300 mg); rifampicin RIF = 450 mg for <50 kg, 600 mg for >=50 kg; pyrazinamide PZA = 1500 mg <50 kg, 1750 mg 50-75 kg, 2000 mg >=75 kg; ethambutol EMB = 750 mg <50 kg, 1000 mg 50-75 kg, 1250 mg >=75 kg; plus hepatotoxicity risk assessment (age >=35 / liver disease / alcohol / hepatitis / HIV / pregnancy).",  # 5
        "Baseline liver function",  # 6
        "Mild abnormality (ALT 1-2x ULN)",  # 7
        "Marked abnormality (ALT >2x ULN)",  # 8
        "Alcohol history",  # 9
        "Yes (long-term drinking)",  # 10
        "Coexisting hepatitis B/C",  # 11
        "Coexisting HIV",  # 12
        "Pregnancy",  # 13
        "📋 Standard HRZE dosing (daily)",  # 14
        "Dose (mg/kg)",  # 15
        "Daily maximum",  # 16
        "Main toxicity",  # 17
        "Isoniazid (H)",  # 18
        "Hepatotoxicity, peripheral neuropathy",  # 19
        "Rifampicin (R)",  # 20
        "Hepatotoxicity, orange-red body fluids",  # 21
        "Pyrazinamide (Z)",  # 22
        "Hepatotoxicity, hyperuricemia",  # 23
        "Ethambutol (E)",  # 24
        "Optic neuritis",  # 25
        "Note: anti-TB DILI means ALT >3x ULN with symptoms or ALT >5x ULN without. If DILI occurs, stop drugs, give liver support and reintroduce one by one. Baseline liver abnormality, older age, alcoholism, hepatitis B/C and HIV are risk factors needing closer monitoring (liver tests at baseline and every 2-4 weeks). Check visual acuity, fields and color vision before and during ethambutol. Clinical reference only.",  # 26
        "📚 Deep Dive: Anti-TB Quadruple Dosing and Hepatotoxicity",  # 27
        "Newly treated pulmonary TB, weight 55 kg",  # 28
        "Baseline liver disease needs hepatotoxicity assessment",  # 29
        "Monitor liver function during treatment",  # 30
        "Standard dosing at 55 kg",  # 31
        "High hepatotoxicity risk",  # 32
        "Three risk factors - abnormal baseline liver tests + long-term drinking + HCV: high risk; recheck liver tests every 1-2 weeks; if needed reduce Z or switch to a lower-hepatotoxicity regimen (HRE + fluoroquinolone).",  # 33
        "Why is INH capped at 300?",  # 34
        "INH is 5 mg/kg by weight but capped at 300 mg; higher doses add no efficacy and raise hepatotoxicity.",  # 35
        "How to handle abnormal liver tests?",  # 36
        "For marked abnormality (ALT markedly raised / jaundice), stop hepatotoxic drugs first, give liver support and consult a specialist; rebuild the regimen stepwise once stable.",  # 37
        "About the Anti-TB (Quadruple) Dosing and Hepatotoxicity Calculator",  # 38
        "Anti-TB (Quadruple) Dosing and Hepatotoxicity Calculator computes weight-based HRZE doses and assesses DILI risk. A medical professional tool based on authoritative medical standards, for reference only.",  # 39
    ]))
    write('bronchoscopy-grading', build('bronchoscopy-grading', [
        "⚡ Bronchoscopic Grading Reference",  # 0
        "Look up grading standards and clinical meaning of common bronchoscopic findings (airway tumor, mucosal inflammation, airway stenosis)",  # 1
        "Bronchoscopy (Endoscopic Grading) Reference",  # 2
        "/ Bronchoscopy (Endoscopic Grading) Reference",  # 3
        "📖 View the Bronchoscopic Grading Reference user guide",  # 4
        "Airway tumor",  # 5
        "Mucosal inflammation",  # 6
        "Airway stenosis",  # 7
        "Tumor growth pattern",  # 8
        "0 - in situ / superficial",  # 9
        "1 - nodular protruding",  # 10
        "2 - polypoid",  # 11
        "3 - infiltrative",  # 12
        "4 - ulceronecrotic",  # 13
        "Inflammatory findings",  # 14
        "0 - normal mucosa",  # 15
        "1 - congestion and edema",  # 16
        "2 - erosion and exudate",  # 17
        "3 - ulceration and necrosis",  # 18
        "4 - granulation / scar stenosis",  # 19
        "Stenosis degree (Cotton grading)",  # 20
        "Grade I - lumen stenosis <25%",  # 21
        "Grade II - stenosis 25%-75%",  # 22
        "Grade III - stenosis 75%-90%",  # 23
        "Grade IV - near total / total occlusion",  # 24
        "📋 Quick view of common endoscopic grades",  # 25
        "Endoscopic features",  # 26
        "Nodular/polypoid protrusion, smooth or lobulated surface",  # 27
        "Wall infiltration/thickening or ulceronecrosis, lumen narrowing",  # 28
        "Inflammation",  # 29
        "Congestion/edema or erosion/exudate, may have purulent secretion",  # 30
        "Ulceronecrosis or granulation with scar formation",  # 31
        "Stenosis",  # 32
        "Mild stenosis, airflow maintained",  # 33
        "Severe stenosis/occlusion, needs intervention",  # 34
        "Note: bronchoscopic grading aids lesion description and treatment decisions; malignant lesions need biopsy confirmation. Grade III-IV stenosis may be treated with balloon dilation, stenting, laser or cryotherapy. Clinical reference only.",  # 35
        "📚 Deep Dive: Bronchoscopic Grading",  # 36
        "Endoscopic typing of central lung cancer",  # 37
        "Airway inflammation grading",  # 38
        "Stenosis assessment",  # 39
        "Tumor-type proliferation",  # 40
        "Tumor type: endoluminal growth / wall infiltration / extrinsic compression - three patterns guiding biopsy and stenting strategy.",  # 41
        "Stenosis grading",  # 42
        "Stenosis graded mild/moderate/severe; severe (>75%) needs balloon or stent opening.",  # 43
        "What is grading for?",  # 44
        "Typing guides biopsy site and airway reconstruction, and allows follow-up comparison.",  # 45
        "How to distinguish inflammation from tumor?",  # 46
        "Combine congestion/edema, necrosis, neoplasm morphology and pathology; naked-eye view alone is not diagnostic.",  # 47
        "About the Bronchoscopy (Endoscopic Grading) Reference",  # 48
        "Bronchoscopy (Endoscopic Grading) Reference looks up grading standards and clinical meaning of common bronchoscopic findings (tumor, inflammation, stenosis). A medical professional tool based on authoritative medical standards, for reference only.",  # 49
    ]))
    write('calc-48', build('calc-48', [
        "📋 Oxygenation Index (PaO2/FiO2) Calculation",  # 0
        "Compute the P/F oxygenation ratio and grade ARDS severity by the Berlin criteria; mean airway pressure can optionally be entered to calculate the oxygenation index OI.",  # 1
        "Core formula (by input variable): pao2/(fio2/100)",  # 2
        "📖 View the Oxygenation Index (PaO2/FiO2) Calculation user guide",  # 3
        "PaO2 arterial oxygen tension (mmHg)",  # 4
        "FiO2 inspired oxygen concentration (%)",  # 5
        "Mean airway pressure MAP (cmH2O, optional)",  # 6
        "PaCO2 (mmHg, optional)",  # 7
        "🧮 Calculate oxygenation index",  # 8
        "P/F ratio and Berlin ARDS grading",  # 9
        "P/F ratio",  # 10
        "Normal oxygenation",  # 11
        "Mild ARDS",  # 12
        "Caution needed; PEEP/CPAP can improve",  # 13
        "Moderate ARDS",  # 14
        "Usually needs mechanical ventilation",  # 15
        "Severe ARDS",  # 16
        "High mortality; prone positioning / ECMO needed",  # 17
        "Formula: P/F = PaO2 / FiO2 (FiO2 as a decimal, e.g. 40% = 0.4); OI = (MAP x FiO2 x 100) / PaO2; OI >40 suggests severe respiratory failure.",  # 18
        "P/F is affected by PEEP, altitude and hemoglobin; SpO2-based P/F estimation is less accurate at high SpO2, so arterial blood gas is preferred.",  # 19
        "📚 Deep Dive: Oxygenation Index PaO2/FiO2",  # 20
        "ARDS severity stratification",  # 21
        "Oxygenation monitoring during mechanical ventilation",  # 22
        "Computing OI with PEEP",  # 23
        "PF=80/0.40=200 mmHg: moderate ARDS (100-200).",  # 24
        "Computing OI with MAP",  # 25
        "MAP 13, FiO2 0.40, PaO2 80: OI=(13x40)/80=6.5; OI >10 suggests severe.",  # 26
        "ARDS grading cutoffs?",  # 27
        "PF <100 severe, 100-200 moderate, 200-300 mild (requires PEEP >=5).",  # 28
        "SF ratio?",  # 29
        "Noninvasive substitute: SpO2/FiO2; SF <315 approximates PF <300.",  # 30
        "Used to calculate the OI oxygenation index",  # 31
        "Used to assess ventilation",  # 32
    ]))
    write('copd-cat', build('copd-cat', [
        "⚡ COPD CAT Assessment Questionnaire",  # 0
        "COPD Assessment Test (CAT): 8 items scored 0-5, total 0-40, assessing the impact of COPD on health status",  # 1
        "COPD (CAT Score) Questionnaire",  # 2
        "/ COPD (CAT Score) Questionnaire",  # 3
        "📖 View the COPD CAT Assessment Questionnaire user guide",  # 4
        "CAT total = sum of 8 questions (0 to 5 each), max 40; <=10 mild impact, <=20 moderate, <=30 severe, >30 very severe.",  # 5
        "Please rate",  # 6
        "the past 2 weeks",  # 7
        "and choose (0=no impact, 5=most severe impact):",  # 8
        "📋 Clinical meaning of the CAT score",  # 9
        "Minimal impact; maintain treatment, watch for exacerbations",  # 10
        "Moderate impact; optimize treatment, strengthen pulmonary rehab",  # 11
        "Severe impact; intensify medication and supportive care",  # 12
        "Very severe impact; comprehensive assessment, multidisciplinary management",  # 13
        "Note: CAT is a brief tool for COPD health status; repeat at each visit. A CAT change >=2 points is clinically meaningful. GOLD recommends combining CAT, mMRC and exacerbation history for ABE grouping to guide treatment. Clinical reference only.",  # 14
        "📚 Deep Dive: COPD CAT Questionnaire",  # 15
        "COPD symptom burden assessment",  # 16
        "Guiding treatment intensity",  # 17
        "Comparing response at follow-up",  # 18
        "8 items, 2 points each",  # 19
        "Total = 8 x 2 = 16: 10-20 is moderate impact; long-acting bronchodilator therapy advised.",  # 20
        "Severe impact",  # 21
        "Total >=20: severe symptoms; consider LAMA+LABA or adding ICS.",  # 22
        "CAT vs mMRC?",  # 23
        "CAT covers symptoms/activity/psychology broadly, mMRC only breathlessness; the two complement each other.",  # 24
        "What score needs follow-up?",  # 25
        "Reassess every 3 months; a change >=2 points is clinically meaningful.",  # 26
        "About the COPD (CAT Score) Questionnaire",  # 27
        "COPD (CAT Score) Questionnaire: the 8-item COPD Assessment Test evaluating COPD impact on health status and guiding treatment adjustment. A medical professional tool based on authoritative medical standards, for reference only.",  # 28
    ]))
    write('curb65', build('curb65', [
        "🫁 Pneumonia CURB-65 Severity Assessor",  # 0
        "Assesses severity of community-acquired pneumonia (CAP), estimating mortality risk and care setting (outpatient / ward / ICU)",  # 1
        "Pneumonia (CURB-65) Severity Assessor",  # 2
        "/ Pneumonia (CURB-65) Severity Assessor",  # 3
        "📖 View the Pneumonia CURB-65 Severity Assessor user guide",  # 4
        "CURB-65 score = confusion + urea >7 mmol/L + respiratory rate >=30/min + blood pressure (systolic <90 or diastolic <=60 mmHg) + age >=65 years, 1 point each, max 5; 0-1 low risk (outpatient), 2 moderate (admit), >=3 high risk (admit, consider ICU).",  # 5
        "C - Confusion (new onset)",  # 6
        "U - Urea >7 mmol/L",  # 7
        "R - Respiratory rate >=30/min",  # 8
        "B - Systolic BP <90 mmHg",  # 9
        "B - Diastolic BP <=60 mmHg",  # 10
        "65 - Age >=65 years",  # 11
        "📋 CURB-65 Score and Disposition Advice",  # 12
        "Mortality risk",  # 13
        "Care setting",  # 14
        "Low (1.5%)",  # 15
        "Outpatient treatment feasible",  # 16
        "Moderate (9.2%)",  # 17
        "Admit (consider short stay)",  # 18
        "High (>=15%)",  # 19
        "Admit; >=4 consider ICU",  # 20
        "Note: CURB-65 applies to community-acquired pneumonia; either blood-pressure criterion scores 1 point (still 1 point total). Severe pneumonia should also use PSI and IDSA/ATS severe criteria (e.g. need for mechanical ventilation, septic shock). Clinical reference only.",  # 21
        "📚 Deep Dive: Pneumonia CURB-65 Score",  # 22
        "Community pneumonia severity",  # 23
        "Admission decision",  # 24
        "ICU assessment",  # 25
        "3 items positive",  # 26
        "Confusion + urea + age >=65 positive -> 3 points, mortality about 15%; admit and assess for ICU.",  # 27
        "0-1 low risk",  # 28
        "0-1: mortality <3%, can be treated as outpatient with antibiotics and follow-up.",  # 29
        "Meaning of each item?",  # 30
        "C confusion, U urea >7 mmol/L, R respiratory rate >=30, B systolic <90 or diastolic <=60, age >=65.",  # 31
        "How to manage a score of 2?",  # 32
        "Score 2 is moderate risk (about 9%); admit and give IV antibiotics.",  # 33
        "About the Pneumonia (CURB-65) Severity Assessor",  # 34
        "Pneumonia (CURB-65) Severity Assessor uses confusion, urea, respiratory rate, blood pressure and age to grade CAP severity and care setting. A medical professional tool based on authoritative medical standards, for reference only.",  # 35
    ]))


if __name__ == '__main__':
    main()

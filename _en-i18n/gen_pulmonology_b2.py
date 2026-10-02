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
    write('feigongneng-fev1-fvc-fenji', build('feigongneng-fev1-fvc-fenji', [
        "🫁 Pulmonary Function (FEV1/FVC) Grading",  # 0
        "Compute the FEV1/FVC ratio to identify obstructive ventilatory defect and grade severity by GOLD criteria (FEV1 percent predicted).",  # 1
        "Core formula (by input variable): fev1/fev1pred*100; fvc/fvcpred*100; ratio*100",  # 2
        "📖 View the Pulmonary Function (FEV1/FVC) Grading user guide",  # 3
        "FEV1 predicted (L)",  # 4
        "FVC predicted (L, optional)",  # 5
        "🧮 Calculate grading",  # 6
        "Interpretation criteria",  # 7
        "FEV1/FVC ratio: normal >= 0.70 (may be slightly lower in the elderly); < 0.70 suggests obstructive ventilatory defect.",  # 8
        "GOLD grading (by FEV1% predicted when obstructive): GOLD 1 mild >=80%; GOLD 2 moderate 50-79%; GOLD 3 severe 30-49%; GOLD 4 very severe <30%.",  # 9
        "FVC < 80% predicted suggests a possible restrictive ventilatory defect.",  # 10
        "FEV1% predicted = measured FEV1 / predicted FEV1 x 100%.",  # 11
        "Results must be combined with bronchodilator testing, vital capacity and diffusion capacity. This tool does not replace a professional pulmonary function report.",  # 12
        "📚 Deep Dive: Pulmonary Function FEV1/FVC Grading",  # 13
        "COPD airflow limitation assessment",  # 14
        "GOLD grading",  # 15
        "Combining FVC to identify restriction",  # 16
        "Ratio = 2.1/3.5 = 60%, LLN 0.70 for age <60 -> obstructive; FEV1%pred = 2.1/3.0 = 70% -> GOLD 2 moderate.",  # 17
        "Restrictive hint",  # 18
        "If FVC < 80% predicted: low ratio plus low FVC -> mixed or restrictive; check TLC/DLCO.",  # 19
        "LLN vs the 0.70 cutoff?",  # 20
        "LLN is more accurate in the young, 0.70 is common in the elderly; this tool uses age-based LLN, 0.66 for age >=65.",  # 21
        "GOLD stages?",  # 22
        "GOLD 1 >=80%, 2 50-79%, 3 30-49%, 4 <30% (all based on FEV1%pred).",  # 23
        "Used to identify restriction",  # 24
    ]))
    write('gina-asthma', build('gina-asthma', [
        "📋 Asthma GINA Control Level Assessor",  # 0
        "Based on GINA 4-week control assessment and the ACT (Asthma Control Test), it grades asthma control and guides step-up/step-down treatment",  # 1
        "Asthma (GINA Control) Assessor",  # 2
        "/ Asthma (GINA Control) Assessor",  # 3
        "📖 View the Asthma GINA Control Level Assessor user guide",  # 4
        "Asthma control: GINA 4 items over the past 4 weeks (daytime symptoms / night waking / reliever use / activity limitation) all 'no' means well controlled; ACT total = 5 items (1 to 5 each, max 25), >=20 well controlled, 16-19 not well controlled, <=15 very poorly controlled.",  # 5
        "GINA control assessment",  # 6
        "ACT scale",  # 7
        "Assess the past",  # 8
        "4 weeks",  # 9
        "frequency of the following:",  # 10
        "Daytime asthma symptoms >2 times/week?",  # 11
        "Waking at night due to asthma?",  # 12
        "Reliever (SABA) needed >2 times/week?",  # 13
        "Activity limited by asthma?",  # 14
        "GINA assessment",  # 15
        "ACT scale (5 questions, 1-5 points each, max 25)",  # 16
        "1. How much asthma interferes with work/school/housework",  # 17
        "1 Completely",  # 18
        "2 Severely",  # 19
        "3 Moderately",  # 20
        "4 Slightly",  # 21
        "5 Not at all",  # 22
        "2. Frequency of breathlessness",  # 23
        "1 >3 times/day",  # 24
        "2 1-3 times/day",  # 25
        "3 3-6 times/week",  # 26
        "4 1-2 times/week",  # 27
        "5 None at all",  # 28
        "3. Frequency of night waking from asthma symptoms",  # 29
        "1 >=4 times/week",  # 30
        "2 2-3 times/week",  # 31
        "3 1 time/week",  # 32
        "4 1-2 times/month",  # 33
        "4. Reliever use frequency",  # 34
        "5. Self-rated asthma control",  # 35
        "1 Not controlled at all",  # 36
        "2 Poorly controlled",  # 37
        "3 Somewhat controlled",  # 38
        "4 Well controlled",  # 39
        "5 Completely controlled",  # 40
        "ACT assessment",  # 41
        "📋 GINA Asthma Control Levels",  # 42
        "Well controlled",  # 43
        "All four items 'no'",  # 44
        "1-2 items 'yes'",  # 45
        "Consider stepping up treatment",  # 46
        "3-4 items 'yes'",  # 47
        "Step up treatment, review triggers and adherence",  # 48
        "📊 ACT Score Interpretation",  # 49
        "ACT score",  # 50
        "Complete control",  # 51
        "Maintain treatment, follow up in 3-6 months",  # 52
        "Maintain or cautiously step down",  # 53
        "Step up treatment, assess adherence and triggers",  # 54
        "Note: GINA recommends a control-based cycle - assess control, adjust treatment, review response. Acute exacerbations need separate severity assessment. Regular ICS-formoterol serves as both maintenance and reliever (MART). Clinical reference only.",  # 55
        "📚 Deep Dive: Asthma GINA/ACT Control",  # 56
        "GINA four-question control",  # 57
        "ACT 5-item scoring",  # 58
        "Step adjustment",  # 59
        "GINA four items negative",  # 60
        "GINA four questions all negative -> well controlled; maintain current step, review every 3-6 months.",  # 61
        "ACT 20 points",  # 62
        "ACT 5-item total 20/25 -> partly controlled; step up treatment and follow up.",  # 63
        "GINA or ACT?",  # 64
        "GINA is a control questionnaire, ACT covers symptoms plus activity; combining them is more comprehensive.",  # 65
        "What if partly controlled?",  # 66
        "Partial control means stepping up or correcting inhaler technique, then review in 2-4 weeks.",  # 67
        "About the Asthma (GINA Control) Assessor",  # 68
        "Asthma (GINA Control) Assessor grades asthma control across four dimensions over the past 4 weeks: daytime symptoms, night waking, reliever use and activity limitation (ACT/control level). A medical professional tool based on authoritative medical standards, for reference only.",  # 69
    ]))
    write('light-criteria', build('light-criteria', [
        "🔢 Pleural Fluid Light Criteria Exudate/Transudate Differentiator",  # 0
        "Uses Light's criteria (pleural/serum protein ratio, LDH ratio, pleural LDH) to classify pleural effusion",  # 1
        "Pleural Fluid (Light Criteria) Exudate/Transudate Differentiator",  # 2
        "/ Pleural Fluid (Light Criteria) Exudate/Transudate Differentiator",  # 3
        "📖 View the Pleural Fluid Light Criteria Differentiator user guide",  # 4
        "Light's criteria for exudate (any one suffices): pleural/serum protein ratio >0.5; pleural/serum LDH ratio >0.6; pleural LDH > 2/3 of the upper limit of normal serum LDH; if none is met, it is a transudate.",  # 5
        "Pleural fluid protein (g/L)",  # 6
        "Serum protein (g/L)",  # 7
        "Pleural fluid LDH (U/L)",  # 8
        "Serum LDH (U/L)",  # 9
        "Serum LDH upper limit of normal (U/L)",  # 10
        "📋 Light's Criteria (any one means exudate)",  # 11
        "Pleural protein / serum protein",  # 12
        "Protein criteria exudate",  # 13
        "Pleural LDH / serum LDH",  # 14
        "Enzymatic criteria exudate",  # 15
        "Pleural fluid LDH",  # 16
        "> 2/3 of serum LDH upper limit of normal",  # 17
        "📊 Common Causes: Exudate vs Transudate",  # 18
        "Exudate",  # 19
        "Parapneumonic effusion, tuberculosis, malignancy, pulmonary embolism, autoimmune disease",  # 20
        "Transudate",  # 21
        "Heart failure, cirrhosis, nephrotic syndrome, hypoalbuminemia",  # 22
        "Note: Light's criteria are sensitive but less specific; after diuresis for heart failure a transudate may be misread as exudate - a serum-pleural albumin gradient >12 g/L supports transudate. Pleural NT-proBNP >1500 pg/mL also supports a cardiac transudate. Clinical reference only.",  # 23
        "📚 Deep Dive: Pleural Fluid Light's Criteria",  # 24
        "Differentiating exudate from transudate",  # 25
        "Protein and LDH ratios",  # 26
        "Combined with serum upper limit",  # 27
        "Protein ratio 0.583",  # 28
        "Pleural protein 3.5 / serum 6.0 = 0.583 > 0.5 -> one criterion met, classified as exudate.",  # 29
        "LDH ratio above threshold",  # 30
        "Pleural LDH 250 / serum LDH 200 = 1.25 > 0.6, or pleural LDH > 2/3 of serum upper limit -> exudate.",  # 31
        "How many of the three must be met?",  # 32
        "Any one means exudate; a transudate meets none.",  # 33
        "Pseudo-exudate?",  # 34
        "Heart failure or low albumin can produce a 'pseudo-exudate'; combine with clinical context and NT-proBNP.",  # 35
        "About the Pleural Fluid (Light Criteria) Differentiator",  # 36
        "Pleural Fluid (Light Criteria) Differentiator uses the pleural/serum protein ratio, pleural/serum LDH ratio and pleural LDH to distinguish exudate from transudate. A medical professional tool based on authoritative medical standards, for reference only.",  # 37
    ]))
    write('lung-cancer-tnm', build('lung-cancer-tnm', [
        "🏠 Lung Cancer TNM Staging Lookup",  # 0
        "Based on the 8th edition IASLC/AJCC lung cancer TNM, enter a T/N/M combination to look up anatomic stage and treatment direction",  # 1
        "Lung Cancer (TNM Staging) Lookup",  # 2
        "/ Lung Cancer (TNM Staging) Lookup",  # 3
        "📖 View the Lung Cancer TNM Staging Lookup user guide",  # 4
        "Lung cancer TNM staging: T (primary tumor), N (regional nodes) and M (distant metastasis) combine to define stage I to IV; stage I/II is mainly surgical, stage III needs multidisciplinary assessment (resectable: surgery plus adjuvant; unresectable: concurrent chemoradiotherapy then immunotherapy consolidation), stage IV systemic therapy (targeted if driver-positive, immunotherapy if PD-L1 high, otherwise immunotherapy plus chemotherapy).",  # 5
        "T (primary tumor)",  # 6
        "T2a - >3-4 cm / main bronchus",  # 7
        "T3 - >5-7 cm / chest wall / phrenic nerve",  # 8
        "T4 - >7 cm / mediastinum / heart / great vessels",  # 9
        "N (lymph nodes)",  # 10
        "N0 - no regional nodes",  # 11
        "N1 - ipsilateral bronchial / hilar",  # 12
        "N2 - ipsilateral mediastinal / subcarinal",  # 13
        "N3 - contralateral / supraclavicular",  # 14
        "M (distant metastasis)",  # 15
        "M0 - no distant metastasis",  # 16
        "M1a - contralateral lung / pleural / pericardial nodules",  # 17
        "M1b - single metastasis in one organ",  # 18
        "M1c - multiple extrapulmonary metastases",  # 19
        "Look up stage",  # 20
        "📋 8th Edition TNM Stage Combination Overview",  # 21
        "Stage",  # 22
        "Typical combination",  # 23
        "5-year survival",  # 24
        "Stage IA",  # 25
        "Stage IB",  # 26
        "Stage IIIA",  # 27
        "Stage IIIB",  # 28
        "Stage IIIC",  # 29
        "Any T any N M1",  # 30
        "Note: this is anatomic staging; combine with pathology (non-small cell / small cell) and molecular typing (EGFR/ALK/ROS1/PD-L1) for individualized planning. Stage I-II prefers surgery, stage III needs multidisciplinary therapy (chemo/radio/immuno), stage IV is systemic therapy (targeted/immuno/chemo). Clinical reference only.",  # 31
        "📚 Deep Dive: Lung Cancer TNM Staging",  # 32
        "Non-small cell lung cancer staging",  # 33
        "T/N/M combinations",  # 34
        "Treatment pathway guidance",  # 35
        "T2a (3-4 cm) + N0 + M0 -> stage IB; surgical resection with lymph node dissection preferred.",  # 36
        "N3 locally advanced",  # 37
        "N3 regardless of T -> stage IIIC; unresectable cases get concurrent chemoradiotherapy plus immunotherapy consolidation.",  # 38
        "How is M1 staged?",  # 39
        "M1a/M1b -> stage IVA, M1c -> stage IVB; systemic therapy is the mainstay.",  # 40
        "What does staging determine?",  # 41
        "Staging drives resectability assessment and adjuvant/neoadjuvant strategy.",  # 42
        "About the Lung Cancer (TNM Staging) Lookup",  # 43
        "Lung Cancer (TNM Staging) Lookup uses the 8th edition lung cancer TNM standard to look up anatomic stage and treatment strategy from a T/N/M combination. A medical professional tool based on authoritative medical standards, for reference only.",  # 44
    ]))
    write('lung-rads', build('lung-rads', [
        "📋 Lung Nodule Lung-RADS Risk Stratifier",  # 0
        "Based on Lung-RADS 2022, classifies by nodule type and size and gives follow-up/management advice (baseline screening)",  # 1
        "Nodule (Lung-RADS) Risk Stratifier",  # 2
        "/ Nodule (Lung-RADS) Risk Stratifier",  # 3
        "📖 View the Lung Nodule Lung-RADS Risk Stratifier user guide",  # 4
        "Lung-RADS nodule stratification: solid nodules <6 mm are category 2, 6-8 mm category 3, 8-15 mm category 4A, >=15 mm category 4B; part-solid or ground-glass nodules are upgraded by solid-component size and malignant features; growth and suspicious features raise the category.",  # 5
        "Nodule type",  # 6
        "Solid nodule",  # 7
        "Part-solid nodule",  # 8
        "Ground-glass nodule (GGO)",  # 9
        "Mean nodule diameter (mm)",  # 10
        "Growth vs prior / solid component increased",  # 11
        "Typical malignant features on imaging (lobulation / spiculation / vacuole)",  # 12
        "New nodule",  # 13
        "📋 Lung-RADS 2022 Categories (baseline)",  # 14
        "Negative (no nodule / benign such as fully calcified)",  # 15
        "Annual repeat",  # 16
        "Benign appearance or small nodule",  # 17
        "Probably benign",  # 18
        "Repeat CT in 6 months",  # 19
        "Suspicious for malignancy",  # 20
        "Repeat CT / PET-CT / biopsy in 3 months",  # 21
        "Very suspicious for malignancy",  # 22
        "Biopsy / surgical resection assessment",  # 23
        "Note: this is a simplified baseline-screening version; real classification needs nodule morphology, growth rate and prior history. Diameter is the mean of long and short axes. Part-solid nodules need the solid component measured separately. Clinical reference only.",  # 24
        "📚 Deep Dive: Lung Nodule Lung-RADS",  # 25
        "Low-dose CT follow-up",  # 26
        "Solid / part-solid stratification",  # 27
        "Malignant",  # 28
        "Solid 6 mm",  # 29
        "Solid nodule 6 mm -> category 2; low-dose CT follow-up in 12 months.",  # 30
        "Part-solid >10 mm",  # 31
        "Part-solid component >10 mm -> category 4A/4B; repeat in 3 months or PET-CT/biopsy advised.",  # 32
        "Is category 4 cancer?",  # 33
        "Category 4 is suspicious for malignancy and needs action, but is not a diagnosis; pathology is definitive.",  # 34
        "Follow-up interval?",  # 35
        "Ranges 3-12 months by category; new or growing nodules prompt escalation.",  # 36
        "About the Nodule (Lung-RADS) Risk Stratifier",  # 37
        "Nodule (Lung-RADS) Risk Stratifier classifies lung nodules by type (solid / part-solid / ground-glass) and size with Lung-RADS follow-up advice. A medical professional tool based on authoritative medical standards, for reference only.",  # 38
        "How to use the Lung Nodule Lung-RADS Risk Stratifier",  # 39
        "What does the Lung Nodule Lung-RADS Risk Stratifier do?",  # 40
        "How do I use the Lung Nodule Lung-RADS Risk Stratifier?",  # 41
        "When is the Lung Nodule Lung-RADS Risk Stratifier useful?",  # 42
    ]))


if __name__ == '__main__':
    main()

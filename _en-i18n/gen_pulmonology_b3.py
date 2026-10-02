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
    write('niv-settings', build('niv-settings', [
        "🫁 Noninvasive Ventilation IPAP/EPAP Setting Tool",  # 0
        "Pressure parameter relationships in noninvasive ventilation; IPAP/EPAP titrated by condition.",  # 1
        "Noninvasive Ventilation (IPAP/EPAP) Setting Tool",  # 2
        "/ Noninvasive Ventilation (IPAP/EPAP) Setting Tool",  # 3
        "📖 View the Noninvasive Ventilation IPAP/EPAP Setting Tool user guide",  # 4
        "Pressure support PS = IPAP - EPAP",  # 5
        "Computes initial NIV IPAP/EPAP settings and pressure support from condition type and target tidal volume",  # 6
        "COPD exacerbation (type II respiratory failure)",  # 7
        "Cardiogenic pulmonary edema (type I)",  # 8
        "Obstructive sleep apnea (OSA)",  # 9
        "Neuromuscular disease (type II)",  # 10
        "Immunosuppressed pneumonia (type I)",  # 11
        "Target tidal volume (mL/kg ideal body weight)",  # 12
        "Ideal body weight IBW (kg)",  # 13
        "Current pH (optional)",  # 14
        "Calculate settings",  # 15
        "📋 Initial NIV Settings by Indication",  # 16
        "COPD exacerbation",  # 17
        "Low pH (<7.35): start low and titrate up",  # 18
        "Cardiogenic pulmonary edema",  # 19
        "CPAP also works; higher EPAP relieves edema",  # 20
        "As needed",  # 21
        "Often APAP/Bi-level to abolish AHI",  # 22
        "Neuromuscular disease",  # 23
        "Ensure adequate target tidal volume",  # 24
        "Note: NIV needs titration; monitor tidal volume (>=6 mL/kg), pH improvement and comfort. Pressure support (PS) = IPAP - EPAP. Leaks and mask intolerance are common causes of failure. NIV is unsuitable for COPD with severe impaired consciousness or high aspiration risk; consider invasive ventilation. Clinical reference only.",  # 25
        "📚 Deep Dive: Noninvasive Ventilation Settings",  # 26
        "COPD respiratory failure",  # 27
        "OSA / neuromuscular",  # 28
        "COPD with hypercapnia",  # 29
        "EPAP 8, PS 5, IPAP = 13 cmH2O; higher EPAP helps recruit alveoli.",  # 30
        "How is IPAP derived?",  # 31
        "IPAP = EPAP + PS; PS is adjusted by indication and blood gases, aiming to lower PaCO2.",  # 32
        "Why PEEP?",  # 33
        "EPAP keeps the airway open and counteracts intrinsic PEEP, especially in COPD/pulmonary edema.",  # 34
        "About the Noninvasive Ventilation (IPAP/EPAP) Setting Tool",  # 35
        "Noninvasive Ventilation (IPAP/EPAP) Setting Tool computes initial NIV IPAP/EPAP settings from condition (COPD / cardiogenic pulmonary edema / OSA) and target tidal volume. A medical professional tool based on authoritative medical standards, for reference only.",  # 36
        "How to use the Noninvasive Ventilation IPAP/EPAP Setting Tool",  # 37
        "What does the Noninvasive Ventilation IPAP/EPAP Setting Tool do?",  # 38
        "The Noninvasive Ventilation IPAP/EPAP Setting Tool computes initial NIV pressure and support from condition (COPD / cardiogenic pulmonary edema / OSA) and target tidal volume, assisting respiratory therapy parameter setting.",  # 39
        "How do I use the Noninvasive Ventilation IPAP/EPAP Setting Tool?",  # 40
        "When is the Noninvasive Ventilation IPAP/EPAP Setting Tool useful?",  # 41
    ]))
    write('oxygenation-index', build('oxygenation-index', [
        "📋 Oxygenation Index PaO2/FiO2 Calculator",  # 0
        "Computes the oxygenation index (P/F) and oxygen saturation index (S/F), grading ARDS severity by the Berlin criteria",  # 1
        "Oxygenation Index (PaO2/FiO2) Calculator",  # 2
        "/ Oxygenation Index (PaO2/FiO2) Calculator",  # 3
        "📖 View the Oxygenation Index PaO2/FiO2 Calculator user guide",  # 4
        "This health tool estimates using general physiological constants and empirical formulas; results are for reference only and do not replace professional medical diagnosis or advice. Tool name: Oxygenation Index (PaO2/FiO2) Calculator - computes the oxygenation index (P/F) and oxygen saturation index (SF).",  # 5
        "Positive-pressure ventilation established (PEEP/CPAP >=5)",  # 6
        "Respiratory failure confirmed as non-cardiogenic",  # 7
        "📋 Berlin ARDS Criteria (requires PEEP/CPAP >=5)",  # 8
        "No ARDS",  # 9
        "Normal oxygenation / mild injury",  # 10
        "Acute lung injury (ALI)",  # 11
        "Needs higher FiO2 / PEEP",  # 12
        "Consider prone positioning / ECMO",  # 13
        "📊 S/F Substitute Thresholds for P/F (accurate when SpO2 <=97%)",  # 14
        "P/F threshold",  # 15
        "Corresponding S/F",  # 16
        "Note: the oxygenation index must be assessed at PEEP/CPAP >=5 cmH2O. Berlin criteria also require onset within 1 week, bilateral infiltrates and non-cardiogenic edema. S/F discrimination falls when SpO2 >97%. Clinical reference only.",  # 17
        "📚 Deep Dive: PaO2/FiO2 and SF",  # 18
        "Oxygenation monitoring",  # 19
        "ARDS stratification",  # 20
        "Noninvasive SF substitute",  # 21
        "PF=80/0.40=200 mmHg: moderate ARDS.",  # 22
        "SF ratio",  # 23
        "SpO2 90 / FiO2 40%: SF=90/0.40=225, approximating mild-moderate PF.",  # 24
        "Difference between PF and OI?",  # 25
        "PF does not use PEEP, OI includes MAP; OI is more sensitive in children and at high PEEP.",  # 26
        "Is SF reliable?",  # 27
        "SF is affected by pulse oximetry error and is only a noninvasive screen.",  # 28
        "About the Oxygenation Index (PaO2/FiO2) Calculator",  # 29
        "Oxygenation Index (PaO2/FiO2) Calculator computes the oxygenation index (P/F) and oxygen saturation index (SF), grading ARDS severity by the Berlin criteria. A medical professional tool based on authoritative medical standards, for reference only.",  # 30
        "Is this tool free?",  # 31
        "Completely free, no registration, use it directly in your browser.",  # 32
    ]))
    write('pneumothorax', build('pneumothorax', [
        "🫁 Pneumothorax Lung Compression % Estimator",  # 0
        "Measures pleural distances on an upright PA chest film and estimates pneumothorax lung compression percentage by the Rhea method",  # 1
        "Pneumothorax (Lung Compression %) Estimator",  # 2
        "/ Pneumothorax (Lung Compression %) Estimator",  # 3
        "📖 View the Pneumothorax Lung Compression Estimator user guide",  # 4
        "Pneumothorax compression ratio ~ mean of three interpleural measurements x 10 (capped at 100%); compression <20% and asymptomatic can be observed with high-concentration oxygen; secondary or tension pneumothorax needs chest tube drainage or urgent decompression.",  # 5
        "Measure three pleural distances (cm) on the film: A = apex of lung to pleural apex; B = pleural distance at the midpoint of the upper lung field; C = midpoint of the lower lung field",  # 6
        "A apical distance (cm)",  # 7
        "B upper midpoint distance (cm)",  # 8
        "C lower midpoint distance (cm)",  # 9
        "Pneumothorax type",  # 10
        "Primary spontaneous pneumothorax (PSP)",  # 11
        "Secondary spontaneous pneumothorax (SSP)",  # 12
        "Traumatic pneumothorax",  # 13
        "Mild / asymptomatic",  # 14
        "Dyspnea / chest pain",  # 15
        "Severe dyspnea / hemodynamic instability",  # 16
        "Estimate compression",  # 17
        "📋 Pneumothorax Management Reference (BTS)",  # 18
        "Compression degree",  # 19
        "Asymptomatic PSP",  # 20
        "<2 cm (small)",  # 21
        "Observation / consider simple aspiration",  # 22
        "Symptomatic",  # 23
        ">=2 cm (moderate-large)",  # 24
        "Aspiration or chest tube drainage",  # 25
        "Any amount",  # 26
        "Usually needs chest tube drainage",  # 27
        "Tension pneumothorax",  # 28
        "Immediate decompression (large-bore needle) plus drainage; do not wait for imaging",  # 29
        "Note: Rhea formula - compression % ~ (A+B+C)/3 x 10. It is an estimate; error grows in large pneumothorax (complete collapse). Tension pneumothorax is a clinical diagnosis and must be treated immediately without waiting for imaging. A 2 cm pleural distance corresponds to about 20% compression. Clinical reference only.",  # 30
        "📚 Deep Dive: Pneumothorax Lung Compression %",  # 31
        "Primary pneumothorax",  # 32
        "Secondary pneumothorax",  # 33
        "Symptoms and compression in decision-making",  # 34
        "Three-distance mean 2",  # 35
        "a=b=c=2 cm, mean 2, compression ~ 2 x 10 = 20%: borderline, observe or use a small-bore drain.",  # 36
        "Severe symptoms",  # 37
        "Compression >20% with dyspnea -> chest tube drainage preferred.",  # 38
        "Is the estimate accurate?",  # 39
        "The linear method is a rough estimate; CT volumetry is more accurate; symptoms come first clinically.",  # 40
        "How to manage 20%?",  # 41
        "Asymptomatic primary can be observed; secondary or symptomatic cases need drainage.",  # 42
        "About the Pneumothorax (Lung Compression %) Estimator",  # 43
        "Pneumothorax (Lung Compression %) Estimator uses pleural distances on chest film with the Rhea method to estimate compression percentage in spontaneous pneumothorax and suggests management. A medical professional tool based on authoritative medical standards, for reference only.",  # 44
    ]))
    write('pulmonary-function', build('pulmonary-function', [
        "🫁 Pulmonary Function FEV1/FVC Grader",  # 0
        "Computes the FEV1/FVC ratio from spirometry data to classify ventilatory defect type and GOLD severity",  # 1
        "Core formula (by input variable): ratio*100",  # 2
        "Pulmonary Function (FEV1/FVC) Grader",  # 3
        "/ Pulmonary Function (FEV1/FVC) Grader",  # 4
        "📖 View the Pulmonary Function FEV1/FVC Grader user guide",  # 5
        "FEV1 percent predicted (%)",  # 6
        "FVC percent predicted (%)",  # 7
        "Fixed threshold lower limit",  # 8
        "FEV1/FVC < 0.70 (GOLD fixed)",  # 9
        "FEV1/FVC < 0.75 (common for age >=50)",  # 10
        "📋 Ventilatory Defect Interpretation Logic",  # 11
        "FEV1/FVC >= threshold and FVC >= 80% predicted",  # 12
        "Normal ventilatory function",  # 13
        "Obstructive",  # 14
        "FEV1/FVC < threshold",  # 15
        "Airflow limitation, common in COPD/asthma",  # 16
        "Restrictive",  # 17
        "FEV1/FVC >= threshold and FVC < 80% predicted",  # 18
        "Needs TLC confirmation; seen in pulmonary fibrosis / chest wall disease",  # 19
        "Mixed",  # 20
        "FEV1/FVC < threshold and FVC < 80% predicted",  # 21
        "Both obstruction and restriction present",  # 22
        "📊 GOLD Severity of Obstructive Airflow Limitation (based on FEV1% predicted)",  # 23
        "FEV1 % predicted",  # 24
        "Note: the fixed 0.70 FEV1/FVC cutoff may overestimate obstruction in the young and underestimate it in the elderly; interpret together with LLN (lower limit of normal). Restrictive defects need TLC confirmation. Post-bronchodilator FEV1/FVC <0.70 indicates incompletely reversible airflow limitation (COPD). Clinical reference only.",  # 25
        "📚 Deep Dive: FEV1/FVC Grading",  # 26
        "Obstructive determination",  # 27
        "Restrictive determination",  # 28
        "Custom cutoff",  # 29
        "Ratio = 1.5/3.0 = 50% < 0.7 -> obstructive; FVC%pred >=80 does not support restriction.",  # 30
        "Normal ratio but FVC%pred <80 -> restrictive defect; check TLC.",  # 31
        "Is the cutoff adjustable?",  # 32
        "The cutoff is configurable (default 0.7); LLN is advised for the elderly.",  # 33
        "Obstruction plus restriction?",  # 34
        "Low ratio plus low FVC is mixed; confirm with TLC/DLCO.",  # 35
        "About the Pulmonary Function (FEV1/FVC) Grader",  # 36
        "Pulmonary Function (FEV1/FVC) Grader computes the FEV1/FVC ratio from measured and predicted values, classifying obstructive/restrictive defects and GOLD grade. A medical professional tool based on authoritative medical standards, for reference only.",  # 37
    ]))
    write('pulmonary-rehab', build('pulmonary-rehab', [
        "🦿 Pulmonary Rehab Respiratory Muscle Training Intensity Calculator",  # 0
        "Computes respiratory muscle training (RMT) intensity, frequency and prescription from maximal inspiratory pressure (MIP) and maximal expiratory pressure (MEP), for pulmonary rehab in COPD etc.",  # 1
        "Core formula (by input variable): Math.round(mip*lo); Math.round(mip*hi); Math.round(mep*lo)",  # 2
        "Pulmonary Rehab (Respiratory Muscle Training) Intensity Calculator",  # 3
        "/ Pulmonary Rehab (Respiratory Muscle Training) Intensity Calculator",  # 4
        "📖 View the Pulmonary Rehab Respiratory Muscle Training Intensity Calculator user guide",  # 5
        "Maximal inspiratory pressure MIP (cmH2O)",  # 6
        "Maximal expiratory pressure MEP (cmH2O)",  # 7
        "Strength training",  # 8
        "Calculate prescription",  # 9
        "📋 MIP/MEP Lower Limits of Normal (cmH2O)",  # 10
        "MIP lower limit",  # 11
        "MEP lower limit",  # 12
        "≈ 75 - 0.5 x age",  # 13
        "≈ 140 - 0.6 x age",  # 14
        "≈ 50 - 0.3 x age",  # 15
        "≈ 95 - 0.5 x age",  # 16
        "📊 Respiratory Muscle Training (RMT) Prescription Principles",  # 17
        "Strength type",  # 18
        "Endurance type",  # 19
        "Per set",  # 20
        "10-15 repetitions",  # 21
        "Sustained 15-30 minutes",  # 22
        "1-2 sets daily",  # 23
        "Course",  # 24
        ">=8 weeks",  # 25
        "Note: MIP <60 cmH2O (men) / <45 (women) suggests inspiratory muscle weakness. Start training at low intensity and progress gradually (+5% weekly). Pulmonary rehab should integrate exercise training (aerobic + resistance), education, nutrition and psychological support. Assess cardiovascular safety before training. Clinical reference only.",  # 26
        "📚 Deep Dive: Respiratory Muscle Training Intensity",  # 27
        "COPD respiratory muscle weakness",  # 28
        "Strength vs endurance goals",  # 29
        "MIP/MEP weak",  # 30
        "Male 60, MIP 60",  # 31
        "Lower limit = 75 - 0.5 x 60 = 45; MIP 60 > 45, not weak; strength target = 60 x 0.35 ≈ 21 cmH2O.",  # 32
        "Respiratory muscle weakness",  # 33
        "MIP < lower limit -> weak inspiratory muscles; start at 30-50% MIP and load progressively.",  # 34
        "Strength vs endurance intensity?",  # 35
        "Strength 30-50% MIP, endurance 20-30% MIP, split into daily sessions.",  # 36
        "Why measure MIP?",  # 37
        "MIP/MEP reflect inspiratory/expiratory muscles; below the age lower limit suggests easy fatigability.",  # 38
        "About the Pulmonary Rehab (Respiratory Muscle Training) Intensity Calculator",  # 39
        "Pulmonary Rehab (Respiratory Muscle Training) Intensity Calculator computes RMT intensity and frequency prescription from MIP/MEP. A medical professional tool based on authoritative medical standards, for reference only.",  # 40
    ]))


if __name__ == '__main__':
    main()

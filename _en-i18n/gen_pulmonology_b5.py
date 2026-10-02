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
    write('stop-bang', build('stop-bang', [
        "🔍 OSA STOP-BANG Screener",  # 0
        "8-item questionnaire screening for obstructive sleep apnea (OSA) risk to decide whether polysomnography (PSG) is needed",  # 1
        "OSA (STOP-BANG) Screener",  # 2
        "/ OSA (STOP-BANG) Screener",  # 3
        "📖 View the OSA STOP-BANG Screener user guide",  # 4
        "STOP-BANG OSA screen = snoring + daytime tiredness + observed apnea + hypertension + BMI >35 + age >50 + neck circumference >40 cm + male, 1 point each, max 8; <=2 low risk, 3-4 moderate, >=5 high risk OSA.",  # 5
        "S - Snoring loud (heard through a closed door)",  # 6
        "T - Daytime tiredness / sleepiness",  # 7
        "O - Observed apnea",  # 8
        "P - Hypertension",  # 9
        "A - Age > 50 years",  # 10
        "N - Neck circumference > 40 cm",  # 11
        "G - Male",  # 12
        "Risk screening",  # 13
        "📋 STOP-BANG Score and OSA Risk",  # 14
        "Low OSA likelihood; follow up clinically",  # 15
        "PSG or portable monitoring advised",  # 16
        "PSG strongly advised; caution in the perioperative period",  # 17
        "Note: STOP-BANG >=3 indicates raised risk of moderate-severe OSA; when two of male sex, BMI >35 and neck circumference >40 cm are present, sensitivity for moderate-severe OSA is higher. Perioperative screening is especially important. Clinical reference only.",  # 18
        "📚 Deep Dive: STOP-BANG Screening",  # 19
        "OSA high-risk screening",  # 20
        "Preoperative assessment",  # 21
        "Snoring population",  # 22
        "All 8 items positive",  # 23
        "Snoring + tiredness + apnea + hypertension +",  # 24
        ">35 + age >50 + thick neck + male = 8 points -> high-risk OSA.",  # 25
        "0-2 low risk; 3-4 moderate risk, sleep study advised.",  # 26
        "What score warrants a sleep study?",  # 27
        "Moderate-high risk (>=3) should be confirmed by polysomnography.",  # 28
        "Is sensitivity high?",  # 29
        "STOP-BANG is highly sensitive for moderate-severe OSA; a negative result reasonably excludes it.",  # 30
        "About the OSA (STOP-BANG) Screener",  # 31
        "OSA (STOP-BANG) Screener: an 8-item questionnaire screening for high OSA risk including snoring, tiredness, apnea, hypertension, BMI, age, neck circumference and sex. A medical professional tool based on authoritative medical standards, for reference only.",  # 32
    ]))
    write('tb-resistance', build('tb-resistance', [
        "📊 TB Smear/Culture Drug Resistance Analyzer",  # 0
        "Analyzes the drug-resistant TB type from sputum smear, culture and first/second-line susceptibility results, and indicates treatment direction",  # 1
        "TB (Smear/Culture) Drug Resistance Analyzer",  # 2
        "/ TB (Smear/Culture) Drug Resistance Analyzer",  # 3
        "📖 View the TB Smear/Culture Drug Resistance Analyzer user guide",  # 4
        "TB resistance typing: no rifampicin or isoniazid resistance is drug-susceptible TB (DS-TB, 2HRZE/4HR); rifampicin resistance is RR-TB; with isoniazid resistance too it is MDR-TB; plus fluoroquinolone and second-line injectable resistance is XDR-TB - the regimen follows the resistance pattern.",  # 5
        "I. Bacteriological tests",  # 6
        "Sputum smear for acid-fast bacilli",  # 7
        "1+ (bacilli/300 fields)",  # 8
        "2+ (1-10 bacilli/field)",  # 9
        "3+ (>10 bacilli/field)",  # 10
        "Mycobacterial culture",  # 11
        "Culture in progress",  # 12
        "Molecular test (GeneXpert)",  # 13
        "Rifampicin susceptible",  # 14
        "Rifampicin resistant",  # 15
        "II. Drug susceptibility (tick resistant drugs)",  # 16
        "Rifampicin (RIF)",  # 17
        "Isoniazid (INH)",  # 18
        "Fluoroquinolone (levofloxacin / moxifloxacin)",  # 19
        "Second-line injectable (amikacin / capreomycin)",  # 20
        "Pyrazinamide (PZA)",  # 21
        "Ethambutol (EMB)",  # 22
        "Resistance analysis",  # 23
        "📋 TB Drug Resistance Categories (WHO 2021)",  # 24
        "Treatment recommendation",  # 25
        "Rifampicin resistant (regardless of INH)",  # 26
        "Manage with an MDR-TB regimen",  # 27
        "Resistant to at least INH + RIF",  # 28
        "Short or long regimen including bedaquiline",  # 29
        "MDR/RR plus fluoroquinolone or second-line injectable resistance",  # 30
        "Long individualized regimen (BPaLM not applicable)",  # 31
        "MDR/RR plus fluoroquinolone resistance plus resistance to at least one second-line injectable",  # 32
        "Individualized long regimen with multidisciplinary review",  # 33
        "Note: smear positivity indicates high infectivity and requires respiratory isolation. GeneXpert rifampicin resistance must be confirmed by phenotypic susceptibility. BPaL/BPaLM (bedaquiline + pretomanid + linezolid +/- moxifloxacin) suits MDR/RR-TB patients aged >=6 without fluoroquinolone or injectable resistance. Clinical reference only.",  # 34
        "📚 Deep Dive: TB Drug Resistance Analysis",  # 35
        "Smear, culture and Xpert",  # 36
        "Tick resistant drugs",  # 37
        "Infectivity and isolation",  # 38
        "Smear positive + Xpert rif_r",  # 39
        "Smear positive and infectious; Xpert reports rifampicin resistance -> RR-TB, isolate and treat per the drug-resistant pathway.",  # 40
        "Low infectivity",  # 41
        "Smear negative + culture negative -> low infectivity, but still complete the course and recheck.",  # 42
        "RR-TB vs MDR?",  # 43
        "RR-TB covers rifampicin resistance (including MDR); treatment is mainly all-oral short regimens.",  # 44
        "How long to isolate?",  # 45
        "After smear conversion and 2 weeks of treatment infectivity drops sharply; de-isolate per medical advice.",  # 46
        "About the TB (Smear/Culture) Drug Resistance Analyzer",  # 47
        "TB (Smear/Culture) Drug Resistance Analyzer analyzes M. tuberculosis resistance (RR-TB / MDR-TB / XDR-TB) from smear, culture and susceptibility results, and guides regimen choice. A medical professional tool based on authoritative medical standards, for reference only.",  # 48
    ]))
    write('vibration-percussion', build('vibration-percussion', [
        "📡 Vibration Percussion Frequency and Positioning Guide",  # 0
        "Looks up postural drainage position, percussion frequency and technique by affected lung segment to aid airway clearance",  # 1
        "Vibration Percussion (Frequency/Positioning) Guide",  # 2
        "/ Vibration Percussion (Frequency/Positioning) Guide",  # 3
        "📖 View the Vibration Percussion Frequency and Positioning Guide user guide",  # 4
        "Vibration percussion: choose the drainage position and percussion zone by affected lobe; frequency <=15 Hz is low (loosens thick mucus plugs), <=25 Hz medium (routine drainage), >25 Hz high (promotes thick sputum clearance, watch tolerance).",  # 5
        "Right upper lobe apical segment",  # 6
        "Right upper lobe posterior segment",  # 7
        "Right upper lobe anterior segment",  # 8
        "Right middle lobe",  # 9
        "Right lower lobe lateral basal segment",  # 10
        "Right lower lobe posterior basal segment",  # 11
        "Left upper lobe apicoposterior segment",  # 12
        "Left upper lobe anterior segment",  # 13
        "Left lingula",  # 14
        "Left lower lobe lateral basal segment",  # 15
        "Left lower lobe posterior basal segment",  # 16
        "Vibration frequency (Hz)",  # 17
        "Low 15 Hz (loosen thick sputum)",  # 18
        "Medium 25 Hz (routine)",  # 19
        "High 35 Hz (viscous sputum)",  # 20
        "Look up guidance",  # 21
        "📋 General Postural Drainage Points",  # 22
        "Timing",  # 23
        "1-2 h before or 2 h after meals, 2-3 times daily",  # 24
        "5-15 minutes per position, 20-40 minutes total",  # 25
        "Vibration percussion",  # 26
        "Frequency 15-35 Hz, performed during expiration with abdominal breathing",  # 27
        "Contraindications",  # 28
        "Unstable fracture, active bleeding, severe hemoptysis, hemodynamic instability",  # 29
        "Note: postural drainage places the affected area high, using gravity to aid clearance. Percussion frequency is adjustable: low frequency loosens, high frequency promotes clearance. Encourage effective coughing or suction before and after. Patients with COPD / bronchiectasis / lung abscess benefit most. Clinical reference only.",  # 30
        "📚 Deep Dive: Vibration Percussion Guidance",  # 31
        "Chronic bronchitis / bronchiectasis clearance",  # 32
        "Lobe positioning",  # 33
        "Frequency choice",  # 34
        "Lower lobe 20 Hz",  # 35
        "Lower lobe disease: head-down prone position, 20 Hz medium frequency for routine drainage.",  # 36
        "High frequency for viscous sputum",  # 37
        "For viscous sputum choose >25 Hz high frequency to promote clearance; watch tolerance and heart rate.",  # 38
        "How to choose frequency?",  # 39
        "<=15 low loosens plugs, 15-25 medium routine, >25 high promotes clearance; adjust by tolerance.",  # 40
        "Contraindications?",  # 41
        "Use cautiously with hemoptysis, pneumothorax, osteoporosis or unstable cardiovascular disease.",  # 42
        "About the Vibration Percussion (Frequency/Positioning) Guide",  # 43
        "Vibration Percussion (Frequency/Positioning) Guide looks up postural drainage and percussion frequency, position and technique by affected site (lobe / segment). A medical professional tool based on authoritative medical standards, for reference only.",  # 44
    ]))
    write('wells-pe', build('wells-pe', [
        "📋 Pulmonary Embolism Wells Score Probability Assessor",  # 0
        "Wells score predicts the clinical probability of pulmonary thromboembolism (PE) and guides D-dimer testing and CTPA strategy",  # 1
        "Pulmonary Embolism (Wells Score) Probability Assessor",  # 2
        "/ Pulmonary Embolism (Wells Score) Probability Assessor",  # 3
        "📖 View the Pulmonary Embolism Wells Score Probability Assessor user guide",  # 4
        "Wells PE score = DVT clinical signs (3) + alternative diagnosis less likely than PE (3) + heart rate >100 (1.5) + immobilization / recent surgery (1.5) + previous VTE (1.5) + hemoptysis (1) + malignancy (1); <=1 low risk (about 1.3%), <=6 moderate (about 16.2%), >6 high (about 37.5%).",  # 5
        "DVT clinical signs (leg swelling and tenderness)",  # 6
        "Alternative diagnosis less likely than PE",  # 7
        "Heart rate >100/min",  # 8
        "Immobilization >=3 days or surgery within 4 weeks",  # 9
        "Previous VTE history",  # 10
        "Hemoptysis",  # 11
        "Malignancy (on treatment / within 6 months / palliative)",  # 12
        "📋 Wells Score and PE Probability",  # 13
        "Three-tier",  # 14
        "PE probability",  # 15
        "High-sensitivity D-dimer first; negative excludes PE",  # 16
        "Positive D-dimer -> CTPA",  # 17
        "Direct CTPA, no D-dimer needed",  # 18
        "Note: hemodynamically unstable patients (shock / hypotension) are managed as high-risk PE: bedside ultrasound / emergency CTPA first, thrombolysis if needed. Wells two-tier: <=4 'PE unlikely', >4 'PE likely'. Age-adjusted D-dimer threshold (age x 10 ug/L, >50 years) improves exclusion in the elderly. Clinical reference only.",  # 19
        "📚 Deep Dive: Wells Pulmonary Embolism Score",  # 20
        "Suspected PE in clinic / emergency",  # 21
        "Probability stratification",  # 22
        "Imaging decision",  # 23
        "Clinically moderate probability",  # 24
        "No DVT signs but high D-dimer, fast heart rate etc. -> total 4-6 moderate probability; do CTPA.",  # 25
        "Excluding low probability",  # 26
        "<=4 with negative D-dimer -> PE excluded, no imaging needed.",  # 27
        "Difference from rater-13?",  # 28
        "Both are the Wells PE score; this tool is the clinical-decision version; total >6 means high probability and imaging directly.",  # 29
        "Pregnancy / cancer?",  # 30
        "Active cancer and recent surgery are scoring items that raise the prior probability.",  # 31
        "About the Pulmonary Embolism (Wells Score) Probability Assessor",  # 32
        "Pulmonary Embolism (Wells Score) Probability Assessor uses the Wells score to predict PE clinical probability and guide D-dimer and imaging strategy. A medical professional tool based on authoritative medical standards, for reference only.",  # 33
        "How to use the Pulmonary Embolism Wells Score Probability Assessor",  # 34
        "What does the Pulmonary Embolism Wells Score Probability Assessor do?",  # 35
        "How do I use the Pulmonary Embolism Wells Score Probability Assessor?",  # 36
        "When is the Pulmonary Embolism Wells Score Probability Assessor useful?",  # 37
    ]))


if __name__ == '__main__':
    main()

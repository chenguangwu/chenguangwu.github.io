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
    write('rater-13', build('rater-13', [
        "✅ Pulmonary Embolism (Wells Score) Probability",  # 0
        "Wells clinical probability score for pulmonary embolism: 7 indicators assess PE likelihood and guide imaging strategy",  # 1
        "📖 View the Pulmonary Embolism (Wells Score) Probability user guide",  # 2
        "Wells PE score = weighted sum of items; three-tier: <2 low risk (PE probability about 3.6%), 2-6 moderate (about 20.5%), >6 high (about 49.9%); two-tier: <=4 PE unlikely (do D-dimer first), otherwise PE likely (confirm with CTPA).",  # 3
        "Select whether each item is present based on the patient's clinical picture",  # 4
        "Calculate Wells score",  # 5
        "This tool runs on the Wells pulmonary embolism score entirely in your browser; data is never uploaded to any server",  # 6
        "Three-tier: <2 low risk, 2-6 moderate risk, >6 high risk",  # 7
        "Two-tier: <=4 PE unlikely (probability about 1-5%), >4 PE likely (about 20-50%)",  # 8
        "This tool is a clinical reference; combine with D-dimer and imaging for a comprehensive judgment",  # 9
        "📚 Deep Dive: Wells Pulmonary Embolism Score",  # 10
        "Suspected pulmonary embolism",  # 11
        "Clinical probability stratification",  # 12
        "D-dimer strategy",  # 13
        "DVT symptoms +3",  # 14
        "Lower-limb DVT signs +3; with other items total >6 -> high probability, go straight to CTPA.",  # 15
        "Low probability",  # 16
        "Total <=4 and D-dimer negative -> PE excluded, no imaging needed.",  # 17
        "What to do with a high score?",  # 18
        ">6 high probability: imaging directly; 4-6 moderate: D-dimer or CTPA.",  # 19
        "Difference from simplified Wells?",  # 20
        "This version uses weighted scoring; the simplified version counts one positive item as moderate/high probability.",  # 21
        "About the Pulmonary Embolism (Wells Score) Probability",  # 22
        "Wells clinical probability score for PE uses 7 clinical indicators to assess PE likelihood, offering both three-tier (low/moderate/high risk) and two-tier (PE likely/unlikely) interpretations with testing strategy advice.",  # 23
        "Standardized Wells 7-item clinical score",  # 24
        "Dual three-tier and two-tier interpretation",  # 25
        "PE probability estimation and testing strategy advice",  # 26
        "D-dimer / CTPA decision pathway",  # 27
        "PE screening in emergency / respiratory departments",  # 28
        "Pre-D-dimer clinical probability assessment",  # 29
        "CTPA testing decision",  # 30
        "PE risk assessment in inpatients",  # 31
    ]))
    write('respiratory-failure', build('respiratory-failure', [
        "🔢 Respiratory Failure Blood Gas Differentiator",  # 0
        "Assesses oxygenation disorder; <300 suggests ALI, <200 (new standard <100) suggests severe ARDS.",  # 1
        "Blood Gas (Type I/II Respiratory Failure) Differentiator",  # 2
        "/ Blood Gas (Type I/II Respiratory Failure) Differentiator",  # 3
        "📖 View the Respiratory Failure Blood Gas Differentiator user guide",  # 4
        "Oxygenation index P/F = PaO2 / FiO2",  # 5
        "Uses arterial blood gas (ABG) to distinguish type I (hypoxemic) / type II (hypercapnic) respiratory failure and computes the oxygenation index and alveolar-arterial oxygen gradient (A-a gradient)",  # 6
        "Age (years, for the A-a gradient)",  # 7
        "PaCO2 respiratory failure threshold",  # 8
        "45 mmHg (sea level standard)",  # 9
        "50 mmHg (commonly used in China)",  # 10
        "📋 Respiratory Failure Types",  # 11
        "Blood gas features",  # 12
        "Type I (hypoxemic)",  # 13
        "PaO2 <60, PaCO2 normal or low",  # 14
        "Lung parenchymal disease: pneumonia, ARDS, pulmonary edema, pulmonary embolism",  # 15
        "Type II (hypercapnic)",  # 16
        "PaO2 <60 and PaCO2 > threshold",  # 17
        "Hypoventilation: COPD, neuromuscular disease, central depression",  # 18
        "📊 A-a Gradient Reference (room air)",  # 19
        "Upper limit of normal A-a gradient",  # 20
        "Young adults",  # 21
        "≈ [2.5 + 0.21 x age] mmHg",  # 22
        "Note: a widened A-a gradient suggests a gas-exchange disorder (parenchyma/vascular); a normal gradient means hypoxemia comes from hypoventilation or low inspired oxygen. The oxygenation index (P/F) = PaO2/FiO2; <300 suggests acute lung injury, <200 (new standard <100) severe ARDS. Clinical reference only.",  # 23
        "📚 Deep Dive: Respiratory Failure Blood Gas Differentiation",  # 24
        "Type I / type II respiratory failure",  # 25
        "Alveolar-arterial gradient",  # 26
        "Interpretation while on oxygen",  # 27
        "FiO2 0.21: PAO2 = 0.21 x 713 = 149.7; A-a = 149.7 - 60/0.8 - 50 = 24.7 > 15.1 -> type II respiratory failure with widened gradient.",  # 28
        "Pure hypoxemia",  # 29
        "PaO2 <60 with normal PaCO2 -> type I respiratory failure; increase inspired oxygen.",  # 30
        "Type I vs type II?",  # 31
        "PaO2 <60 is diagnostic; with PaCO2 >50 it is type II (hypoventilation).",  # 32
        "A-a gradient formula?",  # 33
        "PAO2 = FiO2 x (760 - 47) - PaCO2/0.8; the gradient widens with age.",  # 34
        "About the Blood Gas (Type I/II Respiratory Failure) Differentiator",  # 35
        "Blood Gas (Type I/II Respiratory Failure) Differentiator uses arterial PaO2 and PaCO2 to distinguish type I (hypoxemic) from type II (hypercapnic) respiratory failure and computes the oxygenation index and A-a gradient. A medical professional tool based on authoritative medical standards, for reference only.",  # 36
    ]))
    write('self-assess-3', build('self-assess-3', [
        "📋 Smoking Cessation (Nicotine Dependence) Self-Assessment",  # 0
        "Fagerstrom Test for Nicotine Dependence (FTND): 6 items assessing nicotine dependence to guide cessation planning",  # 1
        "📖 View the Smoking Cessation (Nicotine Dependence) Self-Assessment user guide",  # 2
        "FTND total = weighted sum of items (0-10); <=2 very low dependence, <=4 low dependence, >4 moderate/high dependence; higher scores mean stronger physical dependence.",  # 3
        "Please answer honestly and choose the option that best fits you",  # 4
        "Assess dependence level",  # 5
        "This tool runs on the Fagerstrom Test for Nicotine Dependence (FTND) entirely in your browser; data is never uploaded to any server",  # 6
        "FTND has 6 items, total 0-10; higher scores mean more severe nicotine dependence",  # 7
        "0-2 very low, 3-4 low, 5 moderate, 6-7 high, 8-10 very high dependence",  # 8
        "This tool is a cessation assessment reference; visit a cessation clinic for professional support",  # 9
        "📚 Deep Dive: FTND Nicotine Dependence",  # 10
        "Pre-cessation assessment",  # 11
        "Dependence stratification",  # 12
        "Setting intervention intensity",  # 13
        "Total 5 points",  # 14
        "FTND 5 -> moderate dependence; medication (varenicline / patch) plus behavioral support advised.",  # 15
        "Severe dependence",  # 16
        ">=7 is severe; willpower alone rarely works, intensive medication and follow-up needed.",  # 17
        "What FTND score?",  # 18
        "6 items, 0-10 points; <=3 low, 4-6 moderate, >=7 high dependence.",  # 19
        "What is the score for?",  # 20
        "Higher dependence calls for medication support and frequent follow-up.",  # 21
        "About the Smoking Cessation (Nicotine Dependence) Self-Assessment",  # 22
        "Fagerstrom Test for Nicotine Dependence (FTND): 6 items assessing physical nicotine dependence, total 0-10, auto-grading dependence and giving personalized cessation advice.",  # 23
        "Internationally standardized FTND 6-item scale",  # 24
        "Five-level dependence grading on 0-10",  # 25
        "Personalized cessation plan advice",  # 26
        "Reference for medication decisions",  # 27
        "Nicotine dependence assessment in cessation clinics",  # 28
        "Formulating cessation treatment plans",  # 29
        "Tracking cessation treatment effect",  # 30
        "Smoker assessment in respiratory / cardiology departments",  # 31
    ]))
    write('smoking-cessation', build('smoking-cessation', [
        "🫁 Nicotine Dependence Self-Rating Tool (FTND)",  # 0
        "Fagerstrom Test for Nicotine Dependence (6 items) assessing tobacco dependence and guiding cessation medication and behavioral intervention",  # 1
        "Smoking Cessation (Nicotine Dependence) Self-Rating Tool",  # 2
        "/ Smoking Cessation (Nicotine Dependence) Self-Rating Tool",  # 3
        "📖 View the Nicotine Dependence Self-Rating Tool (FTND) user guide",  # 4
        "FTND total = sum of 6 questions (0-10); <=3 mild dependence, <=6 moderate, >6 severe; this selects treatment intensity: behavioral intervention / nicotine replacement / varenicline etc.",  # 5
        "1. How soon after waking do you smoke your first cigarette?",  # 6
        "<=5 minutes",  # 7
        "6-30 minutes",  # 8
        "31-60 minutes",  # 9
        ">60 minutes",  # 10
        "2. Do you find it hard to refrain in no-smoking places?",  # 11
        "3. Which cigarette would you hate most to give up?",  # 12
        "The first one in the morning",  # 13
        "4. How many cigarettes per day?",  # 14
        "<=10",  # 15
        "11-20",  # 16
        "21-30",  # 17
        ">=31",  # 18
        "5. Do you smoke more in the morning than at other times?",  # 19
        "6. Do you still smoke when ill and confined to bed?",  # 20
        "Assess dependence",  # 21
        "📋 FTND Score and Dependence Level",  # 22
        "Dependence level",  # 23
        "Intervention advice",  # 24
        "Mainly behavioral intervention; short-course NRT acceptable",  # 25
        "NRT / varenicline with intensified follow-up",  # 26
        "Combined medication (varenicline + NRT) with long-term follow-up",  # 27
        "Note: FTND >=4 suggests moderate-to-severe dependence where medication clearly helps. First-line drugs include nicotine replacement (NRT patch / gum), varenicline and bupropion. Quitting markedly lowers the risk of COPD, lung cancer and cardiovascular disease. The 5 A's (Ask-Advise-Assess-Assist-Arrange) structure cessation intervention. Clinical reference only.",  # 28
        "📚 Deep Dive: FTND Dependence Self-Rating",  # 29
        "Initial screening in cessation clinics",  # 30
        "Dependence grading",  # 31
        "Follow-up reassessment",  # 32
        "Sum of 6 items",  # 33
        "Sum the 6 item scores; e.g. 4+1+0+0+0+0 = 5 -> moderate dependence.",  # 34
        "Low dependence",  # 35
        "<=3 is low dependence; start with behavioral intervention plus brief follow-up.",  # 36
        "Difference from self-assess-3?",  # 37
        "Both are FTND; this tool is the simplified self-rating version for quick stratification.",  # 38
        "How often to reassess?",  # 39
        "Reassess dependence and withdrawal at 2 weeks and 1 month after quitting.",  # 40
        "About the Smoking Cessation (Nicotine Dependence) Self-Rating Tool",  # 41
        "Smoking Cessation (Nicotine Dependence) Self-Rating Tool uses the Fagerstrom Test for Nicotine Dependence (FTND) to assess tobacco dependence and guide cessation drug choice. A medical professional tool based on authoritative medical standards, for reference only.",  # 42
    ]))
    write('sputum-analysis', build('sputum-analysis', [
        "🎨 Sputum Character and Color Clinical Meaning Lookup",  # 0
        "Select sputum character and color to look up clinical meaning and likely causes, aiding initial interpretation of respiratory disease",  # 1
        "Sputum (Character/Color) Clinical Meaning Lookup",  # 2
        "/ Sputum (Character/Color) Clinical Meaning Lookup",  # 3
        "📖 View the Sputum Character and Color Clinical Meaning Lookup user guide",  # 4
        "Sputum analysis identifies causes by character/color/volume/odor: pink frothy sputum suggests acute pulmonary edema, rusty sputum suggests lobar pneumonia, foul-smelling sputum suggests anaerobes (lung abscess / bronchiectasis), bloody sputum needs TB / lung cancer / bronchiectasis workup, and volume >100 mL/24h suggests bronchiectasis or lung abscess.",  # 5
        "Sputum character",  # 6
        "Serous (thin, watery)",  # 7
        "Mucoid (clear, viscous)",  # 8
        "Purulent (yellow-green, thick)",  # 9
        "Mucopurulent",  # 10
        "Pink frothy sputum",  # 11
        "Sputum color",  # 12
        "Rusty",  # 13
        "Red / bloody",  # 14
        "Pink",  # 15
        "Brown",  # 16
        "Sputum volume (mL/24h)",  # 17
        "No special odor",  # 18
        "Foul-smelling",  # 19
        "Wine-like odor",  # 20
        "Look up meaning",  # 21
        "📋 Sputum Character and Color Quick Table",  # 22
        "Common indication",  # 23
        "White mucoid sputum",  # 24
        "Chronic bronchitis, asthma, viral infection",  # 25
        "Yellow purulent sputum",  # 26
        "Bacterial infection (e.g. pneumococcus)",  # 27
        "Green purulent sputum",  # 28
        "Pyocyanic infection, Pseudomonas aeruginosa",  # 29
        "Rusty sputum",  # 30
        "Lobar pneumonia (pneumococcus)",  # 31
        "Acute pulmonary edema",  # 32
        "Large amount of foul purulent sputum",  # 33
        "Lung abscess, bronchiectasis with anaerobes",  # 34
        "Anchovy-paste / wine-like odor",  # 35
        "Amebic lung abscess",  # 36
        "Brown sputum",  # 37
        "Amebiasis, pulmonary hemosiderosis",  # 38
        "Black sputum",  # 39
        "Anthracosis (smoking / dust)",  # 40
        "Note: sputum character is only an ancillary clue; diagnosis needs imaging and microbiology (smear / culture / nucleic acid testing). Volume >100 mL/24h is copious sputum, seen in bronchiectasis and lung abscess. Clinical reference only.",  # 41
        "📚 Deep Dive: Clinical Meaning of Sputum Character",  # 42
        "Interpreting sputum color and character",  # 43
        "Emergency warning",  # 44
        "Pathogen direction clues",  # 45
        "Rusty sputum strongly suggests lobar pneumonia (pneumococcus); with high fever and chest pain start empirical antibiotics.",  # 46
        "Pink frothy sputum indicates acute pulmonary edema - an emergency; sit the patient up, give oxygen, diuretics and vasodilators immediately.",  # 47
        "Meaning of foul-smelling sputum?",  # 48
        "Foul odor suggests anaerobes (lung abscess / bronchiectasis); cover with metronidazole / clindamycin.",  # 49
        "Workup for bloody sputum?",  # 50
        "Hemoptysis in middle-aged or older patients needs chest CT and bronchoscopy to exclude TB / lung cancer.",  # 51
        "About the Sputum (Character/Color) Clinical Meaning Lookup",  # 52
        "Sputum (Character/Color) Clinical Meaning Lookup uses sputum character (mucoid / purulent / bloody) and color to look up clinical meaning and likely causes. A medical professional tool based on authoritative medical standards, for reference only.",  # 53
    ]))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'urology')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'urology')
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
    out = {'slug': slug, 'industry': 'urology', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('ipss-score', build('ipss-score', [
        "🚻 IPSS Score (International Prostate Symptom) Auto Calculator",
        "International Prostate Symptom Score (7 symptom questions plus 1 quality-of-life question), assessing lower urinary tract symptoms over the past month",
        "/ IPSS Score Calculator",
        "IPSS = sum of 7 questions (0 to 5 each, maximum 35) plus the quality-of-life QOL score (0 to 6); a total not above 7 is mild, 8 to 19 moderate, not below 20 severe.",
        "Part 1: symptom score (0-5 points per question)",
        "Part 2: quality-of-life index (QOL, 0-6 points)",
        "If you were to spend the rest of your life with your present urinary condition, how would you feel about it?",
        "0 - Delighted",
        "1 - Pleased",
        "2 - Mostly satisfied",
        "3 - Mixed, about equally satisfied and dissatisfied",
        "4 - Mostly dissatisfied",
        "5 - Unhappy",
        "6 - Terrible",
        "IPSS severity grading",
        "Watchful waiting is acceptable, with regular follow-up",
        "Consider medication (alpha-blockers/5-alpha reductase inhibitors)",
        "Medication or surgical evaluation",
        "IPSS consists of 7 symptom questions, each scored 0-5, for a total of 0-35.\nQOL (0-6) reflects the patient's subjective perception of symptoms and is independent of the symptom score. The two are combined for BPH assessment and treatment follow-up.",
        "⚠️ This score is for clinical reference only and cannot replace a physician's diagnosis. The score must be interpreted together with prostate volume, PSA, urine flow rate and residual urine.",
        "📚 Deep dive: IPSS (International Prostate Symptom Score) automatic calculation",
        "Outpatient self-assessment",
        "Follow-up record",
        "Study enrollment",
        "Total score 14",
        "2 points each x 7 = 14 (moderate), QoL 2, indicating moderate symptoms; recheck in 3-6 months; nocturia twice is counted in item 7.",
        "Total score 25",
        "Items of 3-4 points totaling 25 (severe), QoL 5; urodynamics and prostate evaluation are recommended.",
        "What are the 7 items?",
        "Incomplete emptying, re-voiding within 2 h, intermittency, urgency, weak stream, straining and nocturia; each 0-5, plus QoL 0-6, total 35.",
        "Why should the quality-of-life score (QoL) be viewed separately?",
        "QoL reflects the patient's subjective bother and does not run parallel to the symptom total: someone with a symptom score of 15 may have a QoL of only 2, while another with 8 may have a QoL of 5. Whether to start treatment should consider both - when QoL >= 4, intervention can be considered even if symptoms are only moderate.",
        "About the IPSS Score (International Prostate Symptom) Auto Calculator",
        "IPSS Score (International Prostate Symptom) Auto Calculator - 7 symptom questions plus quality of life, automatically grading the severity of lower urinary tract symptoms. A medical professional tool based on authoritative medical standards, for reference only.",
        "How to use the IPSS Score (International Prostate Symptom) Auto Calculator",
        "What does the IPSS Score (International Prostate Symptom) Auto Calculator do?",
        "How to use the IPSS Score (International Prostate Symptom) Auto Calculator?",
        "What scenarios is the IPSS Score (International Prostate Symptom) Auto Calculator suitable for?",
        "Total score and grading",
        "IPSS has 7 items each scored 0-5; total score",
        "Mild;",
        "Moderate;",
        "Severe lower urinary tract symptoms.",
        "For assessing benign prostatic hyperplasia (BPH) symptom severity and following up drug or surgical efficacy; the single quality-of-life item helps judge whether intervention is needed.",
        "Scope and limits",
        "Self-assessment screening cannot replace PSA, ultrasound, uroflowmetry and other tests; sudden worsening of symptoms or urinary retention requires prompt medical care.",
    ]))

    write('penile-rigidity', build('penile-rigidity', [
        "📋 Penile Rigidity (Nocturnal Erection) Grader",
        "The EHS erection hardness score combined with NPT nocturnal penile tumescence monitoring to assess erection hardness and differentiate the nature of ED",
        "/ Penile Rigidity Grader",
        "Erection hardness score (EHS) is graded 1 to 4 (grade 4 fully rigid); normal criteria for NPT nocturnal erection monitoring: frequency not below 3, each episode not below 10 minutes, maximum rigidity not below 70%; meeting all three suggests psychogenic ED, otherwise organic ED is suggested.",
        "1. Erection Hardness Score (EHS)",
        "Current erection hardness",
        "Grade 1 - penis enlarged but not hard",
        "Grade 2 - hard but not enough for penetration",
        "Grade 3 - hard enough for penetration but not fully rigid",
        "Grade 4 - fully rigid",
        "2. NPT nocturnal penile tumescence monitoring (optional)",
        "Nocturnal erection frequency (times/night)",
        "Duration of each episode (minutes)",
        "Maximum rigidity (%, tip)",
        "EHS erection hardness grading standard",
        "Penis enlarged but not hard",
        "Severe ED (congestion only, no rigidity)",
        "Hard, but not enough for vaginal penetration",
        "Hard enough for penetration, but not fully rigid",
        "Fully rigid",
        "Normal erection",
        "NPT normal reference",
        "Abnormal (suggests organic)",
        "Nocturnal erection frequency",
        ">= 3 times/night",
        "< 3 times",
        "Duration of each episode",
        "> 10 minutes",
        "< 10 minutes",
        "Maximum rigidity",
        "Tip/base rigidity",
        "Basically consistent",
        "Tip markedly reduced",
        "Differential significance:",
        "Normal NPT suggests psychogenic ED; abnormal NPT suggests organic ED (vascular/neurogenic/endocrine).\nNPT is the 'gold standard' for distinguishing psychogenic from organic ED and requires continuous monitoring for at least 2-3 nights.",
        "⚠️ This tool is for clinical reference only; the etiologic diagnosis of ED requires a comprehensive assessment combining history, physical examination, hormones and vascular ultrasound.",
        "📚 Deep dive: penile rigidity (EHS) grading",
        "ED grading",
        "NPT assessment",
        "Treatment efficacy",
        "EHS grade 3",
        "EHS grade 3 (hard enough for penetration but not fully rigid) equals mild ED; NPT frequency >= 3, duration >= 10 min and rigidity >= 70% is normal.",
        "EHS grade 1",
        "EHS grade 1 (enlarged but not hard) equals severe ED; combined treatment such as medication, vacuum devices or a prosthesis is recommended.",
        "What are the NPT normal criteria?",
        "Nocturnal erections >= 3 times, each >= 10 min, rigidity >= 70% and base diameter >= 3 cm indicate a low likelihood of organic ED.",
        "What is the EHS erection hardness grade?",
        "EHS grade 1: the penis is enlarged but not hard; grade 2: there is hardness but not enough for penetration; grade 3: hard enough for penetration but not fully rigid; grade 4: completely hard. If NPT is normal while EHS is low, psychogenic or situational factors usually predominate.",
        "About the Penile Rigidity (Nocturnal Erection) Grader",
        "Penile Rigidity (Nocturnal Erection) Grader - EHS erection hardness scoring and NPT nocturnal penile tumescence grading, to differentiate psychogenic from organic ED. A medical professional tool based on authoritative medical standards, for reference only.",
        "How to use the Penile Rigidity (Nocturnal Erection) Grader",
        "What does the Penile Rigidity (Nocturnal Erection) Grader do?",
        "How to use the Penile Rigidity (Nocturnal Erection) Grader?",
        "What scenarios is the Penile Rigidity (Nocturnal Erection) Grader suitable for?",
    ]))

    write('prostate-volume', build('prostate-volume', [
        "🧊 Prostate Volume (Ultrasound Dimensions) Calculator",
        "Enter three transrectal or transabdominal ultrasound dimensions and use the ellipsoid formula to estimate prostate volume and the degree of hyperplasia",
        "/ Prostate Volume Calculator",
        "Prostate volume (ellipsoid formula) = coefficient k x transverse x anteroposterior x longitudinal diameter, commonly k about 0.52 (pi/6); a volume less than 20mL is normal, 20 to 50 mild-to-moderate enlargement, not below 80 very large; PSA density PSAD = PSA ÷ volume, greater than 0.25 is high risk.",
        "Longitudinal diameter (length L, cm)",
        "Anteroposterior diameter (height H, cm)",
        "Transverse diameter (width W, cm)",
        "Serum PSA (ng/mL, optional)",
        "Ellipsoid pi/6 ~ 0.524 (recommended)",
        "Modified coefficient 0.7 (common for transabdominal)",
        "Volume grading reference (Chinese urology guidelines)",
        "Normal prostate size",
        "Mild enlargement",
        "Observation is acceptable; watch the symptoms",
        "Moderate enlargement",
        "Assess treatment together with IPSS",
        "Severe enlargement",
        "Medication effect is limited; surgery may be considered",
        "Very large prostate",
        "Stronger indication for open or minimally invasive surgery",
        "V = coefficient x L x H x W (cm). The ellipsoid coefficient pi/6 ~ 0.524 is most commonly used; some authors use 0.7 for transabdominal ultrasound.\nIf PSA is entered, PSA density PSAD = PSA ÷ volume is calculated at the same time (PSAD > 0.15 warrants vigilance for prostate cancer and further evaluation is advised).",
        "⚠️ This tool is for clinical reference only; volume estimation carries error and cannot replace the physician's comprehensive judgment.",
        "📚 Deep dive: prostate volume (ellipsoid formula) calculation",
        "BPH assessment",
        "PSA density",
        "Surgical planning",
        "Ellipsoid 30.6mL",
        "4.0 x 3.5 x 4.2 x 0.52 = 30.6mL; PSA 3.0, PSAD = 3.0/30.6 = 0.098, below 0.15 means low risk.",
        "When the dimensions enlarge to a volume of 80 mL with PSA 8, PSAD = 0.10; with volume >80 mL the bleeding risk of monopolar TURP rises, so enucleation is preferred.",
        "What does the 0.52 coefficient mean?",
        "Ellipsoid volume",
        "V = pi/6 x a x b x c ~ 0.52 x d1 x d2 x d3; transrectal measurement of the three dimensions is most commonly used.",
        "How large counts as enlargement?",
        "The normal adult prostate is about 20 mL; a measured volume >30 mL is usually regarded as prostatic enlargement and is one of the imaging criteria for BPH; >80 mL is severe enlargement, where medication has limited effect and enucleation (HoLEP/ThuLEP) is usually recommended.",
        "About the Prostate Volume (Ultrasound Dimensions) Calculator",
        "Prostate Volume (Ultrasound Dimensions) Calculator - based on three transrectal ultrasound dimensions, the ellipsoid formula estimates prostate volume and the degree of hyperplasia. A medical professional tool based on authoritative medical standards, for reference only.",
        "How to use the Prostate Volume (Ultrasound Dimensions) Calculator",
        "What does the Prostate Volume (Ultrasound Dimensions) Calculator do?",
        "Prostate volume calculator: enter three ultrasound dimensions and estimate prostate volume (mL) with the ellipsoid formula, as a reference for benign hyperplasia assessment.",
        "How to use the Prostate Volume (Ultrasound Dimensions) Calculator?",
        "What scenarios is the Prostate Volume (Ultrasound Dimensions) Calculator suitable for?",
    ]))

    write('psa-density', build('psa-density', [
        "📋 PSA Density (PSAD) and Biopsy Indication Assessor",
        "Calculates PSA density (PSAD) and, combining PSA, age and prostate volume, assesses the indication for prostate needle biopsy",
        "/ PSA Density Assessor",
        "PSA density PSAD = serum PSA ÷ prostate volume; less than 0.15 low risk, 0.15 to 0.25 intermediate risk, not below 0.25 high risk (biopsy recommended). Age-specific PSA upper limits: under 50 years 2.5, under 60 years 3.5, under 70 years 4.5, not below 70 years 6.5 ng/mL.",
        "Serum PSA (ng/mL)",
        "Abnormal digital rectal examination (DRE)",
        "MRI suggests a suspicious lesion (PI-RADS >= 3)",
        "Previous negative biopsy",
        "PSAD grading and biopsy indication",
        "Follow-up recheck is fine; MRI if necessary",
        "Comprehensive judgment combining MRI/DRE is recommended",
        "Systematic prostate biopsy is recommended",
        "Age-specific PSA reference range",
        "PSA upper limit of normal (ng/mL)",
        "40 - 49 years",
        "50 - 59 years",
        "60 - 69 years",
        "70 - 79 years",
        "Biopsy indications:",
        "(1) PSA > 10 ng/mL; (2) PSA 4-10 ng/mL with PSAD > 0.15, or abnormal DRE, or suspicious MRI;\n(3) PSA 4-10 ng/mL with a negative initial evaluation may be rechecked with f/tPSA, PSAD and MRI before deciding. PSAD reduces false-positive PSA elevation caused by BPH.",
        "⚠️ This tool is for clinical reference only; the biopsy decision requires the physician to integrate imaging, digital rectal examination and past history.",
        "📚 Deep dive: PSA density (PSAD) and biopsy indication",
        "Elevated PSA",
        "Gray zone",
        "Biopsy decision",
        "PSA 6, volume 50 mL: PSAD = 6/50 = 0.12 < 0.15, low risk; but at age 65 the age limit is 4.5 and PSA 6 > 4.5, so biopsy after MRI is still recommended.",
        "PSA 10, volume 33 mL: PSAD = 10/33 = 0.30 > 0.25, high risk; biopsy is directly recommended.",
        "How is the age limit used?",
        "PSA thresholds by age: <50 to 2.5, <60 to 3.5, <70 to 4.5, >=70 to 6.5; when the threshold is exceeded, decide by combining PSAD, DRE and MRI.",
        "How is the PSAD threshold set?",
        "A cutoff of 0.15 ng/mL/mL is commonly used clinically: >0.15 suggests an increased risk of clinically significant cancer, and multiparametric MRI (PI-RADS) is advised to decide on biopsy; when <0.10, biopsy can be deferred relatively safely with regular rechecks. The gray zone (0.10-0.15) requires judgment combining DRE, MRI and the PSA change rate.",
        "About the PSA Density (PSAD) and Biopsy Indication Assessor",
        "PSA Density (PSAD) and Biopsy Indication Assessor - calculates PSA density (PSAD) and combines PSA, age and prostate volume to assess the indication for biopsy. A medical professional tool based on authoritative medical standards, for reference only.",
        "How to use the PSA Density (PSAD) and Biopsy Indication Assessor",
        "What does the PSA Density (PSAD) and Biopsy Indication Assessor do?",
        "How to use the PSA Density (PSAD) and Biopsy Indication Assessor?",
        "What scenarios is the PSA Density (PSAD) and Biopsy Indication Assessor suitable for?",
    ]))

    write('rater-4', build('rater-4', [
        "📋 Erectile Function (IIEF-5) Score",
        "IIEF-5 International Index of Erectile Function (5 items, 0-5 points each, total 0-25, assessing the past 6 months)",
        "IIEF-5 total score = sum of 5 questions (1 to 5 each, maximum 25); not below 22 normal, 17 to 21 mild, 12 to 16 mild-to-moderate, 8 to 11 moderate, 5 to 7 severe, less than 5 means no sexual activity or not assessable.",
        "1. Confidence in getting and keeping an erection",
        "1 - Very low",
        "5 - Very high",
        "2. How often erections were hard enough for penetration during intercourse",
        "0 - No intercourse",
        "1 - Almost always or always",
        "2 - Most times",
        "4 - A few times",
        "5 - Almost never or never",
        "3. How often the erection was maintained after penetration during intercourse",
        "4. Difficulty of maintaining the erection to completion of intercourse",
        "1 - Extremely difficult",
        "2 - Very difficult",
        "3 - Difficult",
        "4 - Slightly difficult",
        "5 - Not difficult",
        "5. Satisfaction when attempting intercourse",
        "1 - Very dissatisfied",
        "2 - Dissatisfied",
        "3 - About equally satisfied and dissatisfied",
        "4 - Satisfied",
        "5 - Very satisfied",
        "Calculate IIEF-5",
        "📚 Deep dive: IIEF-5 total score (sum of 5 items)",
        "Quick scoring",
        "Teaching",
        "Erection confidence 4 + hardness sufficient 4 + maintaining penetration 4 + completing intercourse 4 + satisfaction 4 = 20 (mild), close to normal.",
        "Items of 1-2 points totaling 8 (severe); specialist care is recommended.",
        "Versus the full scale?",
        "This tool reports the total of 5 items (0-25); the full IIEF-15 also has ejaculation and satisfaction domains, and the direction of the conclusion is consistent.",
        "Does a low score definitely mean erectile dysfunction?",
        "IIEF-5 <= 21 suggests ED, but recent fatigue, mood, antidepressants and some antihypertensive drugs must first be excluded, and it must be confirmed as a stable state over the past 6 months. A repeat assessment is advised, together with NPT, blood glucose, lipids and sex hormone levels to determine the cause.",
        "About the Erectile Function (IIEF-5) Score",
        "Erectile Function (IIEF-5) Score. A free online tool with pure front-end processing; data is not uploaded, protecting your privacy and security.",
        "How to use the Erectile Function (IIEF-5) Score",
        "What does the Erectile Function (IIEF-5) Score do?",
        "How to use the Erectile Function (IIEF-5) Score?",
        "What scenarios is the Erectile Function (IIEF-5) Score suitable for?",
    ]))


if __name__ == '__main__':
    main()

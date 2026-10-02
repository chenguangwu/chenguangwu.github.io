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
    write('urine-flow-rate', build('urine-flow-rate', [
        "📚 Urine Flow Rate (Qmax) Normal Reference Tool",
        "Enter the maximum flow rate Qmax and voided volume to assess voiding function and obstruction risk according to sex",
        "/ Qmax Reference Tool",
        "Interpreting maximum flow rate Qmax: in men not below 15 mL/s is normal, 10 to 15 suspicious, less than 10 obstructive; in women not below 20 is normal, 15 to 20 suspicious, less than 15 obstructive; when the voided volume is less than 150 mL the result is unreliable and must be repeated.",
        "Qmax normal reference (adult free uroflowmetry)",
        "Possible obstruction",
        "Note: Qmax is strongly affected by the voided volume, so a volume >= 150 mL is needed for a reliable result; in older men Qmax declines with age.",
        "Key interpretation points:",
        "Qmax <10 mL/s in men or <15 mL/s in women suggests obstruction or reduced detrusor contractility, and further urodynamic testing is advised.\nCauses of a reduced Qmax include BOO (bladder outlet obstruction) and DUA (detrusor underactivity), which urodynamics can differentiate.",
        "⚠️ Uroflowmetry is a screening test; the result must be interpreted together with residual urine and symptoms, and cannot alone serve as an indication for surgery.",
        "📚 Deep dive: urine flow rate (Qmax) normal reference",
        "Male voiding assessment",
        "Female voiding assessment",
        "BPH screening in the elderly",
        "Male Qmax 12 mL/s",
        "The male normal threshold is >= 15, so 12 < 15 indicates a weakened stream; interpret it together with IPSS and residual urine; if the voided volume is <150 mL, reliability is reduced.",
        "Female Qmax 22 mL/s",
        "The female normal threshold is >= 20, so 22 >= 20 is a normal flow rate with no signs of obstruction.",
        "Does a low Qmax always mean obstruction?",
        "Not necessarily. A voided volume <150 mL, voiding by abdominal pressure, prostatic hyperplasia or detrusor weakness can all lower Qmax, so the curve and residual urine must be considered together.",
        "How is a slightly low Qmax in older men interpreted?",
        "A physiological decline in Qmax is common in men aged >= 60 years; if it is 10-15 with no symptoms, observation is acceptable, while <10 warrants further testing.",
        "About the Urine Flow Rate (Qmax) Normal Reference Tool",
        "Urine Flow Rate (Qmax) Normal Reference Tool - enter the maximum flow rate and voided volume to assess obstruction or suspicion against sex and age references. A medical professional tool based on authoritative medical standards, for reference only.",
    ]))

    write('urodynamics', build('urodynamics', [
        "🎚️ Urodynamics (Detrusor Pressure) Assessor",
        "Enter pressure-flow study parameters to calculate BOOI (obstruction index) and BCI (contractility index)",
        "/ Urodynamics Assessor",
        "Pressure-flow study parameters",
        "Detrusor pressure at maximum flow Pdet@Qmax (cmH2O)",
        "Maximum detrusor pressure Pdet.max (cmH2O, optional)",
        "Volume at first desire to void (mL, optional)",
        "Maximum cystometric capacity (mL, optional)",
        "Detrusor overactivity (DO)",
        "Reduced compliance",
        "BOOI bladder outlet obstruction index grading (men)",
        "Obstruction",
        "BCI bladder contractility index grading",
        "Strong contractility",
        "Normal contractility",
        "Weak contractility (DUA)",
        "Key interpretation points:",
        "BOOI assesses bladder outlet obstruction in men (BPH and others); BCI assesses detrusor contractility.\nObstruction plus normal contractility means relieving the obstruction works well; obstruction plus weak contractility (DUA) means the improvement in voiding after surgery is limited, so surgery requires caution.\nDO and reduced compliance suggest a possible neurogenic bladder.",
        "⚠️ This tool is based on pressure-flow studies and is for clinical reference only; full urodynamic interpretation requires the physician's comprehensive judgment.",
        "📚 Deep dive: urodynamic BOOI/BCI assessment",
        "BOO judgment",
        "Detrusor contractility",
        "Neurogenic",
        "Pdet@Qmax=70, Qmax=15: BOOI = 70 - 2 x 15 = 40 > 40 suggests bladder outlet obstruction; BCI = 70 + 5 x 15 = 145, normal contractility.",
        "Pdet=40, Qmax=10: BOOI = 40 - 20 = 20 (borderline), BCI = 90, suggesting possible obstruction or weak contractility; imaging correlation is needed.",
        "What are the BOOI/BCI thresholds?",
        "BOOI >40 means obstruction, <40 means no obstruction (20-40 is borderline and needs correlation); BCI >100 means normal contraction, <100 means weak contraction.",
        "What should be noted before a urodynamic study?",
        "Usually drugs that affect voiding (alpha-blockers, anticholinergics, diuretics and others) must be stopped as instructed and the rectum emptied beforehand; during the study stay as close to natural voiding as possible and avoid excessive tension, otherwise distorted Pdet and Qmax will directly cause BOOI misjudgment.",
        "About the Urodynamics (Detrusor Pressure) Assessor",
        "Urodynamics (Detrusor Pressure) Assessor - calculates the bladder outlet obstruction index (BOOI) and bladder contractility index (BCI) to assess obstruction and detrusor contractility. A medical professional tool based on authoritative medical standards, for reference only.",
    ]))

    write('uti-diagnosis', build('uti-diagnosis', [
        "🔍 Urinary Tract Infection (Colony Count) Diagnostic Tool",
        "Urine culture colony count combined with symptoms and urinalysis to help diagnose and localize urinary tract infection",
        "/ UTI Diagnostic Tool",
        "UTI diagnosis: a high colony count (not below 10^5) plus urinary symptoms or fever establishes the diagnosis; with fever it is acute pyelonephritis, with only LUTS or suprapubic pain it is acute cystitis, and without symptoms it is asymptomatic bacteriuria; a mid-range count plus symptoms plus pyuria is suspicious, and a low count indicates contamination.",
        "1. Urine culture colony count (clean midstream urine)",
        "Colony count (CFU/mL)",
        "Pathogen",
        "Escherichia coli",
        "Klebsiella",
        "Proteus",
        "Staphylococcus saprophyticus",
        "2. Urinalysis",
        "Leukocyte esterase positive / WBC >5/HPF",
        "Nitrite positive",
        "Microscopic hematuria",
        "3. Symptoms and signs",
        "Lower urinary tract symptoms (frequency/urgency/dysuria)",
        "Suprapubic tenderness",
        "Fever (>= 38 C) / flank pain / costovertebral angle tenderness",
        "Clinical significance of the colony count",
        "Colony count",
        "Confirmed urinary tract infection",
        "Anti-infective therapy guided by susceptibility testing",
        "Recheck together with symptoms; repeat culture if necessary",
        "Mostly contamination",
        "Repeat with a properly collected specimen",
        "Note: in women with acute uncomplicated cystitis and typical symptoms, >= 10^3 CFU/mL is sufficient for diagnosis; for catheterized specimens >= 10^4 CFU/mL is significant.",
        "Infection localization:",
        "Fever, flank pain and costovertebral angle tenderness indicate upper urinary tract infection (pyelonephritis); bladder irritation alone plus suprapubic tenderness usually indicates lower urinary tract infection (cystitis).",
        "⚠️ This tool is for clinical reference only; antibiotic use must follow susceptibility results, and complicated or recurrent UTI requires further investigation.",
        "📚 Deep dive: diagnosing urinary tract infection by colony count",
        "Midstream urine",
        "Catheter urine",
        "Symptom interpretation",
        ">= 10^5 plus symptoms",
        "A colony count >= 10^5 CFU/mL plus positive leukocyte esterase or nitrite plus LUTS: UTI is diagnosed and empiric anti-infective therapy is given; Escherichia coli is the most common pathogen.",
        "10^4 midstream urine",
        "10^4-10^5 CFU/mL is suspicious; it must be combined with symptoms and microscopy, and asymptomatic carriers may not need treatment.",
        "What is the standard for catheter urine?",
        "Catheter-associated UTI commonly uses a >= 10^3 CFU/mL threshold (because of catheter contamination); treat when symptoms are present.",
        "What colony count is significant?",
        ">= 10^5 CFU/mL in clean midstream urine is the classic threshold; in women with typical lower urinary tract symptoms >= 10^2-10^3 CFU/mL can also be diagnostic; catheter-associated infection is easily contaminated, so >= 10^3 CFU/mL is commonly used. In every case the final judgment should combine symptoms, leukocyte esterase and nitrite.",
        "About the Urinary Tract Infection (Colony Count) Diagnostic Tool",
        "Urinary Tract Infection (Colony Count) Diagnostic Tool - urine culture colony count combined with symptoms and urinalysis leukocytes and nitrite to assist UTI diagnosis. A medical professional tool based on authoritative medical standards, for reference only.",
    ]))

    write('varicocele-grading', build('varicocele-grading', [
        "🩺 Varicocele (Ultrasound) Grading Tool",
        "Enter color Doppler ultrasound measurements and combine them with the physical examination to grade varicocele",
        "/ Varicocele Grading Tool",
        "Varicocele ultrasound grading (vein diameter): not below 4mm grade 3, 3 to 4 grade 2, 2 to 3 grade 1, less than 2 grade 0; Valsalva reflux of not below 2 seconds is diagnostically significant; clinical grading is subclinical / I / II / III.",
        "1. Color Doppler ultrasound data",
        "Maximum pampiniform plexus diameter (mm)",
        "Reflux duration during Valsalva (seconds)",
        "Reflux during quiet breathing",
        "2. Physical examination (Dubin-Amelar clinical grading)",
        "Physical examination findings",
        "Not palpable, Valsalva also negative (subclinical)",
        "Palpable only during Valsalva (grade I)",
        "Palpable at rest but not visible (grade II)",
        "Varicose vein mass visible on the scrotal surface (grade III)",
        "Grading assessment",
        "Varicocele ultrasound grading standard",
        "Vein diameter",
        "Reflux status",
        "Clinical correspondence",
        "Grade 0 (normal)",
        "No reflux",
        "No varicocele",
        "Grade 1 (subclinical/mild)",
        "Valsalva reflux",
        "Grade 2 (moderate)",
        "Palpable on examination",
        "Grade 3 (severe)",
        "Reflux even at rest",
        "Visible on the scrotal surface",
        "Clinical key points:",
        "The left side is most common (about 90%), related to the left spermatic vein draining at a right angle into the left renal vein.\nReflux lasting >= 2 seconds is diagnostically significant. The prevalence of varicocele among infertile men is about 40%; surgery (microsurgical ligation/embolization) is recommended for severe cases or those with abnormal semen parameters.",
        "⚠️ This tool is for clinical reference only; surgical indications must integrate symptoms, infertility, semen quality and the status of the contralateral side.",
        "📚 Deep dive: varicocele (ultrasound) grading",
        "Infertility assessment",
        "Found on physical examination",
        "Surgical indication",
        "Diameter 3.2mm with reflux",
        "At rest and with Valsalva the diameter is 3.2 mm with reflux >= 2 s, and reflux also occurs during quiet breathing: ultrasound grade 3 / clinical grade III, most often on the left; surgery is recommended.",
        "Diameter 2.0mm",
        "Diameter 2.0 mm with reflux <2 s: grade 1 (subclinical); observation is fine if asymptomatic, and semen should be assessed in infertile men.",
        "What are the surgical indications?",
        "Scrotal pain, infertility (abnormal semen), testicular atrophy or progressive grading should be actively managed, especially bilateral or right-sided cases in adolescents.",
        "What are the commonly used ultrasound grading criteria?",
        "Subclinical type: pampiniform plexus diameter 2-3 mm, reflux appears with the Valsalva maneuver but the physical examination is negative; clinical grade I is palpable on examination, grade II is visible and palpable, grade III is visible to the naked eye. A diameter >3 mm with reflux lasting >2 seconds supports the clinical diagnosis.",
        "About the Varicocele (Ultrasound) Grading Tool",
        "Varicocele (Ultrasound) Grading Tool - enter the pampiniform plexus diameter and reflux status and grade in combination with the clinical physical examination. A medical professional tool based on authoritative medical standards, for reference only.",
    ]))


if __name__ == '__main__':
    main()

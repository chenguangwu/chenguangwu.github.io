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
    write('assessor-pressure', build('assessor-pressure', [
        "🎚️ Urodynamics (Detrusor Pressure) Assessment",  # 0
        "Urodynamic pressure-flow analysis: enter detrusor pressure and flow rate to compute the BOOI obstruction index and BCI contractility index",  # 1
        "Bladder outlet obstruction index BOOI = detrusor pressure pdet - 2 x maximum flow rate Qmax; contractility index BCI = pdet + 5 x Qmax. BOOI >40 obstructed, 20-40 equivocal, <20 no obstruction; BCI >150 strong, 100-150 normal, <100 weak; PVR grading: <50 / 50-100 / 100-200 / >=200 mL.",  # 2
        "1. Detrusor pressure at Qmax Pdet (cmH2O)",  # 3
        "2. Maximum flow rate Qmax (mL/s)",  # 4
        "3. Post-void residual PVR (mL)",  # 5
        "4. Detrusor overactivity",  # 6
        "Yes (low pressure <20 cmH2O)",  # 7
        "Yes (high pressure >20 cmH2O)",  # 8
        "5. Bladder compliance (mL/cmH2O)",  # 9
        "Normal (>20)",  # 10
        "Reduced (10-20)",  # 11
        "Severely reduced (<10)",  # 12
        "📚 Deep Dive: Detrusor Pressure Grading (BOOI/BCI)",  # 13
        "Obstruction grading",  # 14
        "Contractility grading",  # 15
        "Reporting",  # 16
        "Obstruction + normal contractility",  # 17
        "BOOI 50 (obstructed), BCI 130 (normal contractility); management focuses on relieving obstruction (e.g. TURP).",  # 18
        "Weak contractility",  # 19
        "BOOI 10 (no obstruction), BCI 80 (weak); difficulty voiding stems from detrusor weakness, so intermittent catheterization rather than surgery.",  # 20
        "How is PVR graded?",  # 21
        "<50 normal, 50-100 mild, 100-200 moderate, >200 severe; decide together with BOOI.",  # 22
        "How are BOOI and BCI calculated?",  # 23
        "BOOI = Pdet@Qmax - 2 x Qmax; >40 obstructed, 20-40 equivocal, <20 no obstruction. BCI = Pdet@Qmax + 5 x Qmax; >100 normal contractility, <100 reduced. The two must be read together: high pressure with low flow is obstruction, low pressure with low flow is weak contractility - the treatments differ completely.",  # 24
        "About the Urodynamics (Detrusor Pressure) Assessment",  # 25
        "Urodynamics (Detrusor Pressure) Assessment. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",  # 26
        "How to use the Urodynamics (Detrusor Pressure) Assessment",  # 27
        "What does the Urodynamics (Detrusor Pressure) Assessment do?",  # 28
        "How do I use the Urodynamics (Detrusor Pressure) Assessment?",  # 29
        "When is the Urodynamics (Detrusor Pressure) Assessment useful?",  # 30
    ]))
    write('bladder-capacity', build('bladder-capacity', [
        "🧊 Bladder Capacity (Residual + Voided Volume) Measurer",  # 0
        "Computes bladder capacity from voided volume plus residual urine and compares it with expected capacity (including the Koff formula for children)",  # 1
        "/ Bladder Capacity Measurer",  # 2
        "Bladder capacity = voided volume + residual urine; expected capacity in children = (age + 2) x 30 mL, in adults about 300-600 mL (median 400); actual/expected ratio <0.7 is small, >1.5 large; emptying efficiency = voided volume / capacity x 100%.",  # 3
        "Residual urine volume (mL)",  # 4
        "Expected bladder capacity reference",  # 5
        "Expected capacity",  # 6
        "About 400 mL (voided + residual)",  # 7
        "Children (<=12 years)",  # 8
        "(age + 2) x 30 mL",  # 9
        "Koff formula",  # 10
        "Children (>12 years)",  # 11
        "Close to adult 300-500 mL",  # 12
        "Normal adult voided volume is 200-400 mL per void, 4-6 voids by day; residual urine <50 mL is normal.",  # 13
        "Abnormal bladder capacity hints",  # 14
        "Common causes",  # 15
        "Markedly below expected",  # 16
        "Reduced bladder capacity",  # 17
        "Cystitis, tuberculosis, radiation cystitis, OAB, repeated surgery",  # 18
        "Markedly above expected",  # 19
        "Increased capacity / urinary retention",  # 20
        "Lower urinary tract obstruction, neurogenic bladder, detrusor weakness",  # 21
        "Bladder capacity = voided volume + residual urine. Measure when the patient has a strong urge to reflect maximum capacity; measure residual by transabdominal ultrasound or catheterization. Capacity assessment is used to evaluate and follow neurogenic bladder, OAB and lower urinary tract obstruction.",  # 22
        "This tool is a clinical reference only; bladder function assessment must be combined with urodynamic testing.",  # 23
        "📚 Deep Dive: Bladder Capacity (Voided + Residual) Measurement",  # 24
        "Urinary retention assessment",  # 25
        "Intermittent catheterization planning",  # 26
        "Capacity training",  # 27
        "Capacity 350 mL",  # 28
        "Voided 300 + residual 50 = 350 mL, 87.5% of the expected 400 mL, low-normal; efficiency 300/350 x 100 = 85.7%.",  # 29
        "Small capacity 180 mL",  # 30
        "Voided 120 + residual 60 = 180 mL (45% of expected 400), indicating reduced capacity, common in interstitial cystitis or fibrosis.",  # 31
        "How is expected capacity set?",  # 32
        "Adult expected is about 400 mL, adjusted by age and sex; an actual/expected ratio <50% indicates a marked capacity drop.",  # 33
        "What residual volume needs treatment?",  # 34
        "In adults residual <50 mL is normal, 50-100 mL needs recheck and follow-up, >100 mL suggests incomplete emptying, >200 mL often indicates retention. The decision is not based on the number alone but also symptoms, renal function and recurrent infection; a single abnormal reading should be repeated another day.",  # 35
        "About the Bladder Capacity (Residual + Voided Volume) Measurer",  # 36
        "Bladder Capacity (Residual + Voided Volume) Measurer - measures voided volume plus residual urine to compute bladder capacity and compares with expected capacity (including the Koff formula for children). A medical professional tool based on authoritative medical standards, for reference only.",  # 37
    ]))
    write('calc-1', build('calc-1', [
        "🚻 IPSS Prostate Symptom Score",  # 0
        "The International Prostate Symptom Score (IPSS) assesses the severity of lower urinary tract symptoms (LUTS).",  # 1
        "IPSS total = sum of 7 LUTS questions (0 to 5 each, max 35); total <=7 mild, 8-19 moderate, >=20 severe; higher scores mean worse obstructive symptoms.",  # 2
        "Quality-of-life score (QoL, not counted in IPSS)",  # 3
        "0 Delighted",  # 4
        "1 Pleased",  # 5
        "2 Mostly satisfied",  # 6
        "3 Mixed, about equally satisfied and dissatisfied",  # 7
        "4 Mostly dissatisfied",  # 8
        "5 Unhappy",  # 9
        "6 Terrible",  # 10
        "📚 Deep Dive: IPSS International Prostate Symptom Score",  # 11
        "BPH screening",  # 12
        "Medication response follow-up",  # 13
        "Preoperative assessment",  # 14
        "IPSS 19",  # 15
        "7 symptom items total 19 (moderate 8-19) with QoL 3, overall 22/35, indicating moderate LUTS; alpha-blocker therapy and flow-rate follow-up advised.",  # 16
        "IPSS 7",  # 17
        "Total 7 (mild 0-7), QoL 1, overall 8/35, mild symptoms; lifestyle guidance suffices.",  # 18
        "Grading criteria?",  # 19
        "0-7 mild, 8-19 moderate, 20-35 severe; QoL >=4 or total >=20 suggests active intervention.",  # 20
        "Does a high IPSS always mean BPH?",  # 21
        "Not necessarily. IPSS measures LUTS severity; urethral stricture, overactive bladder, diabetic cystopathy, anticholinergics or diuretics can all raise the score. Combine history, digital rectal exam, residual urine and flow rate to differentiate before choosing treatment.",  # 22
        "How to use the IPSS Prostate Symptom Score",  # 23
        "What does the IPSS Prostate Symptom Score do?",  # 24
        "How do I use the IPSS Prostate Symptom Score?",  # 25
        "When is the IPSS Prostate Symptom Score useful?",  # 26
        "Total score and grading",  # 27
        "The IPSS sums 7 voiding symptom items scored 0-5 each; the total",  # 28
        "indicates mild symptoms;",  # 29
        "moderate symptoms;",  # 30
        "severe symptoms.",  # 31
        "Quality of life",  # 32
        "A single 0-6 quality-of-life item is usually attached; higher scores mean LUTS (frequency, nocturia, difficulty voiding) weigh more heavily on life.",  # 33
        "Scope and limits",  # 34
        "IPSS is a self-report screen and cannot replace digital rectal exam, PSA or uroflowmetry; moderate-severe cases or those with hematuria / retention should see urology.",  # 35
    ]))
    write('calc-volume', build('calc-volume', [
        "🧊 Prostate Volume (Ultrasound Dimensions) Calculation",  # 0
        "Enter the three prostate diameters from transrectal / transabdominal ultrasound to estimate volume with the ellipsoid formula, and compute PSA density to help distinguish benign from malignant.",  # 1
        "Enter the three prostate diameters from transrectal / transabdominal ultrasound to estimate volume with the ellipsoid formula, and compute PSA density to help distinguish benign from malignant. Performs a professional calculation from the inputs and outputs the result.",  # 2
        "This tool is only an imaging aid and does not replace urological image interpretation or clinical decisions. Combine the sonographer's conclusion with prostate biopsy assessment.",  # 3
        "Transverse diameter D1 (cm)",  # 4
        "Anteroposterior diameter D2 (cm)",  # 5
        "Longitudinal diameter D3 (cm)",  # 6
        "Serum PSA (ng/mL, optional)",  # 7
        "Ellipsoid formula 0.52 (recommended)",  # 8
        "Spherical approximation 0.7",  # 9
        "🧮 Calculate volume",  # 10
        "Ellipsoid formula: volume = 0.52 x D1 (transverse) x D2 (anteroposterior) x D3 (longitudinal), in mL ≈ cm³.",  # 11
        "Normal prostate volume is about 20-30 mL; > 40 mL suggests benign prostatic hyperplasia (BPH).",  # 12
        "PSA density (PSAD) = PSA / prostate volume. PSAD < 0.15 is usually benign; > 0.15 suggests biopsy is needed.",  # 13
        "Transition-zone PSA density > 0.2 ng/mL/cc suggests a raised prostate cancer risk.",  # 14
        "Measurement error in ultrasound diameters affects the volume estimate; transrectal ultrasound is more accurate than transabdominal. This tool does not replace imaging or pathology diagnosis.",  # 15
        "📚 Deep Dive: Prostate Volume (Ultrasound Dimensions) Calculation (selectable coefficient)",  # 16
        "Transrectal",  # 17
        "Transabdominal",  # 18
        "Research",  # 19
        "0.52 x 4.5 x 3.5 x 4.0 = 32.8 mL; if PSA is entered PSAD is computed too - here PSA was omitted so only volume is given.",  # 20
        "Spherical approximation",  # 21
        "Using the pi/6 coefficient gives the same 32.8 mL, matching the ellipsoid; clinical reports use the ellipsoid.",  # 22
        "How to choose the coefficient?",  # 23
        "0.52 ellipsoid, 0.5236 = pi/6 and the spherical approximation reflect different assumptions; with all three diameters available prefer the ellipsoid.",  # 24
        "How is PSA density computed and what is it for?",  # 25
        "PSAD = serum PSA / prostate volume (ng/mL per mL). A larger prostate secretes more PSA, so PSA alone gives false positives; after density correction, PSAD >0.15 suggests a higher risk of clinically significant cancer and >0.20 argues more strongly for biopsy.",  # 26
        "How to use the Prostate Volume (Ultrasound Dimensions) Calculation",  # 27
        "What does the Prostate Volume (Ultrasound Dimensions) Calculation do?",  # 28
        "How do I use the Prostate Volume (Ultrasound Dimensions) Calculation?",  # 29
        "When is the Prostate Volume (Ultrasound Dimensions) Calculation useful?",  # 30
        "Used to compute PSA density",  # 31
    ]))
    write('canyuniaoliang-jingfubchao-tuisuan', build('canyuniaoliang-jingfubchao-tuisuan', [
        "🚻 Residual Urine Volume (Transabdominal Ultrasound) Estimation",  # 0
        "Enter the three bladder diameters (width x depth x height) from transabdominal ultrasound to estimate post-void residual (PVR) with an empirical formula.",  # 1
        "Enter the three bladder diameters (width x depth x height) from transabdominal ultrasound to estimate post-void residual (PVR) with an empirical formula. Performs a professional calculation from the inputs and outputs the result.",  # 2
        "/ Residual Urine Volume (Transabdominal Ultrasound) Estimation",  # 3
        "This tool is an ultrasound estimation reference and cannot replace a urologist's examination conclusion. Patients with severe retention and retention symptoms should seek hospital assessment promptly.",  # 4
        "Bladder width W (cm)",  # 5
        "Bladder depth D (cm)",  # 6
        "Bladder height H (cm)",  # 7
        "Transabdominal formula 0.75 x W x D x H (recommended)",  # 8
        "Ellipsoid formula 0.52 x W x D x H",  # 9
        "Formula 0.7 x W x D x H",  # 10
        "🧮 Calculate residual urine",  # 11
        "Transabdominal formula: residual urine = 0.75 x width (W) x depth (D) x height (H), in mL ≈ cm³.",  # 12
        "Normal residual: < 50 mL; 50-100 mL is suspiciously abnormal; > 100 mL suggests urinary retention.",  # 13
        "Large residual volumes are common in BPH, neurogenic bladder and urethral stricture.",  # 14
        "The 0.52 ellipsoid formula often underestimates; the 0.75 transabdominal formula is closer to measured values.",  # 15
        "Ultrasound estimation is approximate and error grows when bladder shape is irregular. Measure immediately after voiding to improve accuracy.",  # 16
        "📚 Deep Dive: Residual Urine Estimation by Transabdominal Ultrasound (dual coefficient)",  # 17
        "Quick outpatient calculation",  # 18
        "Bedside ultrasound",  # 19
        "Follow-up comparison",  # 20
        "Transabdominal formula 60 mL",  # 21
        "5.0 x 4.0 x 4.0 x 0.75 = 60.0 mL (transabdominal); ellipsoid 0.52 x 5 x 4 x 4 = 41.6 mL - the difference reflects the measurement assumption and both are shown side by side.",  # 22
        "Decline on recheck",  # 23
        "80 mL before treatment, 35 mL after: the fall indicates improved voiding and the catheterization interval can be extended.",  # 24
        "Why two results?",  # 25
        "The 0.75 transabdominal and 0.52 ellipsoid formulas rest on different geometric assumptions; the transabdominal one is more conservative, and clinically the trend comparison matters most.",  # 26
        "Is ultrasound-estimated residual accurate?",  # 27
        "It is a geometric approximation; compared with catheter-measured values the error is often around ±20%, larger when bladder shape is irregular. Clinically the before/after trend with the same method matters more; a single value alone should not justify surgery or catheter removal.",  # 28
    ]))


if __name__ == '__main__':
    main()

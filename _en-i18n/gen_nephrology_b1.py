#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'nephrology')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'nephrology')
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
    out = {'slug': slug, 'industry': 'nephrology', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
DISCL_M = " A professional medical tool based on authoritative medical standards, for reference only."

def main():
    write('aki-kdigo', build('aki-kdigo', [
        "\U0001F3E0 Acute Kidney Injury (AKI) KDIGO Staging Tool",
        "KDIGO diagnosis and staging of AKI based on serum creatinine change and/or reduced urine output",
        "Core calculation formula (by input variables): max(scrStage,urineStage)",
        "Acute Kidney Injury (KDIGO Staging) Tool",
        "/ AKI Staging Tool",
        "Serum creatinine criteria",
        "Urine output (mL/kg/h)",
        "Low urine output duration (hours)",
        "\U0001F4CB KDIGO diagnostic and staging criteria for acute kidney injury",
        "\u2191\u226526.5 \u03bcmol/L (within 48h) or \u21911.5-1.9 times baseline",
        "<0.5 mL/kg/h for 6-12h",
        "\u21912.0-2.9 times baseline",
        "<0.5 mL/kg/h for \u226512h",
        "\u2191\u22653 times baseline or \u2265353.6 \u03bcmol/L or dialysis required",
        "<0.3 mL/kg/h for \u226524h or anuria \u226512h",
        "AKI diagnosis: Scr rises \u226526.5 \u03bcmol/L within 48h, or rises \u22651.5 times baseline within 7 days, or urine output falls to the above criteria.",
        "Note: AKI staging takes the higher of the creatinine criterion and the urine output criterion. AKI stage 3 requires urgent nephrology consultation to assess dialysis indications. Common causes: prerenal (hypovolemia, heart failure), renal (ATN, AGN, AIN), postrenal (obstruction)." + DISCL_M,
        "\U0001F4DA In-depth analysis: acute kidney injury KDIGO staging",
        "Creatinine rise from baseline",
        "Persistently low urine output",
        "RRT assessment needed",
        "Baseline 80 rising to 180",
        "Ratio=180/80=2.25 (\u22652.0) \u2192 AKI stage 2; the increment of 100 \u03bcmol/L is also >26.5, so the more severe stage applies.",
        "Ratio 1.8 times",
        "Baseline 80, current 144: ratio 1.8 (1.5\u20131.9) \u2192 stage 1; monitor urine output and avoid nephrotoxic drugs.",
        "Which criterion sets the stage?",
        "Take the more severe of the creatinine stage and the urine output stage; if RRT is needed, it is stage 3.",
        "Which creatinine unit?",
        "Compare in the same unit as baseline; note the conversion between \u03bcmol/L and mg/dL (\u00d788.4).",
        "About \"Acute Kidney Injury (KDIGO Staging) Tool\"",
        "KDIGO staging tool for acute kidney injury (AKI): diagnosis and staging based on serum creatinine change and urine output. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))
    write('ca-p-product', build('ca-p-product', [
        "\U0001F4CB Calcium-Phosphorus Product (Ca\u00d7P) Target Assessor",
        "Compute corrected serum calcium and the calcium-phosphorus product, and assess CKD-MBD and vascular calcification risk",
        "Core calculation formula (by input variables): calcium+0.02\u00d7(40-albumin); caP\u00d712.4",
        "Calcium-Phosphorus Product (Ca\u00d7P) Target Assessor",
        "/ Calcium-Phosphorus Product Assessor",
        "Total serum calcium (mmol/L)",
        "iPTH (pg/mL, optional)",
        "\U0001F4CB CKD-MBD calcium and phosphorus targets (KDIGO)",
        "G5/dialysis",
        "Corrected serum calcium (mmol/L)",
        "Normal range 2.10-2.50",
        "Lower limit of normal",
        "2-9 times upper limit of normal",
        "Calcium-phosphorus product",
        "Conversion: calcium-phosphorus product in mmol\u00b2/L\u00b2 \u00d7 12.45 = mg\u00b2/dL\u00b2. Target <55 mg\u00b2/dL\u00b2 (4.4 mmol\u00b2/L\u00b2).",
        "Note: corrected calcium = measured calcium + 0.02 \u00d7 (40 \u2212 albumin). A high calcium-phosphorus product is an independent risk factor for vascular calcification and death. Lowering serum phosphorus is the priority strategy in managing CKD-MBD. This tool is for learning reference only.",
        "\U0001F4DA In-depth analysis: calcium-phosphorus product assessment",
        "CKD mineral assessment",
        "Dialysis patient targets",
        "iPTH linkage",
        "Corrected calcium 2.2 (albumin 40), Ca\u00d7P=3.52 mmol\u00b2/L\u00b2\u00d712.4=43.6 mg\u00b2/dL\u00b2: <55 meets the target (dialysis goal).",
        "High phosphorus above target",
        "Serum phosphorus >1.78 (dialysis) or >1.45 (non-dialysis): a phosphate-restricted diet plus phosphate binders is needed, with iPTH assessed at the same time.",
        "Why correct calcium?",
        "With low albumin, measured calcium reads low; correcting by 40 \u2212 albumin brings it closer to ionized calcium.",
        "Upper limit of the product?",
        "In dialysis patients Ca\u00d7P<55 mg\u00b2/dL\u00b2, to reduce the risk of vascular calcification.",
        "About \"Calcium-Phosphorus Product (Ca\u00d7P) Target Assessor\"",
        "Calcium-phosphorus product (Ca\u00d7P) target assessor: computes the calcium-phosphorus product from corrected serum calcium and serum phosphorus to assess vascular calcification risk in CKD-MBD patients. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))
    write('calc-1', build('calc-1', [
        "\U0001FAD8 Glomerular Filtration Rate eGFR (CKD-EPI)",
        "Estimate adult eGFR with the CKD-EPI creatinine equation (without the race coefficient) and give the CKD stage.",
        "\"Estimate adult eGFR with the CKD-EPI creatinine equation (without the race coefficient) and give the CKD stage.\" Perform the professional calculation from the input parameters and output the result.",
        "Glomerular filtration rate eGFR calculation",
        "/ Glomerular filtration rate eGFR calculation",
        "Serum creatinine (Scr)",
        "Calculate eGFR",
        "\U0001F4DA In-depth analysis: eGFR (CKD-EPI) calculation",
        "Estimate the glomerular filtration rate",
        "CKD staging",
        "Follow-up comparison",
        "Male, 60 years old, Scr 133",
        "Scr 133 \u03bcmol/L = 1.5 mg/dL: eGFR\u224850.7 mL/min/1.73m\u00b2 \u2192 stage G3a.",
        "Female example",
        "Female, 55 years old, Scr 106 \u03bcmol/L: CKD-EPI 2021 gives eGFR\u224853.5 \u2192 G3a.",
        "CKD-EPI versus MDRD?",
        "CKD-EPI is more accurate at higher eGFR and is now the standard; the race coefficient has been removed.",
        "Scr in \u03bcmol/L \u00f788.4 = mg/dL before substituting into the equation.",
        "for example 88.4",
        "for example 58",
    ]))
    write('ckd-staging', build('ckd-staging', [
        "\U0001F3E0 Chronic Kidney Disease (CKD) CGA Staging Manager",
        "CKD risk stratification and follow-up recommendations based on eGFR (G stage) and albuminuria (A stage)",
        "Chronic Kidney Disease (CKD Staging) Manager",
        "/ CKD Staging Manager",
        "CKD staging: by eGFR, G1 (90 or above) / G2 (60\u201389) / G3a (45\u201359) / G3b (30\u201344) / G4 (15\u201329) / G5 (below 15); by urine albumin-creatinine ratio UACR, A1 (below 30) / A2 (30\u2013300) / A3 (above 300) mg/g; the combination of G and A determines risk.",
        "\U0001F4CB CKD risk stratification (KDIGO heat map)",
        "\U0001F4CB Recommended follow-up frequency (times per year)",
        "Follow-up frequency",
        "Referral advice",
        "1 time/year",
        "Community follow-up",
        "Community follow-up, referral if necessary",
        "2 times/year",
        "Nephrology follow-up recommended",
        "\u22653 times/year",
        "Nephrology follow-up mandatory",
        "Note: CKD diagnosis requires eGFR<60 and/or albuminuria (UACR\u226530) persisting for \u22653 months. G3b or above, or A3, both warrant nephrology referral. This tool is for learning reference only and cannot replace clinical judgment.",
        "\U0001F4DA In-depth analysis: CKD CGA staging",
        "G stage + A stage",
        "Follow-up and referral",
        "G3a+A2 \u2192 moderate risk, annual follow-up, referral to nephrology if necessary.",
        "G4 (15\u201329)+A3 \u2192 high risk, actively manage complications and prepare for renal replacement.",
        "What does CGA mean?",
        "G is based on eGFR and A on albuminuria; together they determine risk and the timing of referral.",
        "When to refer to nephrology?",
        "Assessment is recommended from G3 onwards; G4/G5 or A3 should see a specialist as early as possible.",
        "About \"Chronic Kidney Disease (CKD Staging) Manager\"",
        "Chronic kidney disease CKD staging manager: performs CGA staging based on eGFR (G stage) and albuminuria (A stage), and assesses CKD progression risk and follow-up recommendations. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))
    write('creatinine-clearance', build('creatinine-clearance', [
        "\U0001FAD8 24-Hour Creatinine Clearance (Ccr) Calculator",
        "Compute endogenous creatinine clearance from 24h urine creatinine, urine volume and serum creatinine, with body surface area correction",
        "Glomerular filtration rate (24h creatinine clearance) calculator",
        "/ 24h creatinine clearance",
        "Endogenous creatinine clearance Ccr (mL/min) = [urine creatinine (\u03bcmol/L) \u00d7 urine flow (mL/min)] \u00f7 serum creatinine (\u03bcmol/L); Ccr is also corrected for body surface area as Ccr \u00d7 1.73 \u00f7 BSA.",
        "Total 24h urine creatinine (mmol)",
        "Body surface area BSA (m\u00b2, optional)",
        "\U0001F4CB Creatinine clearance reference range",
        "Reference range (mL/min)",
        "Normal kidney function",
        "Elderly",
        "Declines with age",
        "About 6-7 per 10 years",
        "Ccr 50-80 indicates mild impairment, 25-50 moderate, 10-25 severe, and <10 end-stage renal disease.",
        "Note: for the 3 days before 24h urine collection a low-protein diet (<40 g/d) is required, with no meat and no strenuous exercise, to keep creatinine excretion stable. Ccr reflects glomerular filtration, but the tubules also secrete a small amount of creatinine, so Ccr is slightly higher than true GFR. This tool is for learning reference only.",
        "\U0001F4DA In-depth analysis: 24h creatinine clearance Ccr",
        "Clearance measured by urine collection",
        "Body surface area",
        "Correction",
        "Comparison with eGFR",
        "Urine Cr 8.8 mmol/L, urine volume 1500 mL, Scr 80: urine flow 1.042 mL/min, Ccr=8800\u00d71.042/80\u2248114.6 mL/min; with BSA 1.73 no correction is needed.",
        "Small body size correction",
        "When BSA<1.73, correct as Ccr\u00d7(1.73/BSA) to remove body size bias.",
        "Ccr versus eGFR?",
        "Ccr is biased upward by age and muscle mass, while eGFR is more stable; interpret the two together.",
        "Incomplete urine collection?",
        "Incomplete collection leads to underestimation; repeat the test or switch to a serum-based formula.",
        "About \"Glomerular Filtration Rate (24h Creatinine Clearance) Calculator\"",
        "24-hour creatinine clearance (Ccr) calculator: computes endogenous creatinine clearance from 24h urine creatinine, urine volume and serum creatinine, with support for body surface area correction. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))

if __name__ == '__main__':
    main()

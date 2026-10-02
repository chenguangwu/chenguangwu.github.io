#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'pediatrics')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'pediatrics')
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
    out = {'slug': slug, 'industry': 'pediatrics', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
#!/usr/bin/env python3
# body for pediatrics b1: assessor-13 / assessor-spo2 / chd-assessment / ddst-screening / dehydration-assessment

def main():
    # assessor-13 (33)
    write('assessor-13', build('assessor-13', [
"Dehydration (Body Fluid Loss) Assessment",
"Assess pediatric dehydration severity from WHO/IMCI clinical signs, and estimate fluid loss from body weight",
"Core formula (by input): (prevWt-wt)/prevWt×100",
"Child age (months)",
"Usual weight (kg, optional)",
"Days of diarrhea",
"WHO/IMCI clinical signs assessment",
"Choose the option that best matches the child's current condition for each item",
"Based on WHO/IMCI pediatric dehydration criteria, for quick clinical triage reference",
"Severe dehydration needs immediate IV rehydration; mild-to-moderate can use oral rehydration salts (ORS)",
"This tool is for healthcare professionals' reference only and cannot replace professional medical judgment",
"In-Depth: Dehydration Assessment (Signs)",
"Sign score",
"Mild/moderate/severe",
"Rehydration volume",
"10 kg moderate",
"Sign score corresponding to moderate loss ~6%: cumulative loss = 10×0.06 = 600 mL, replenished by IV or oral.",
"Lethargy, cold limbs, refill >3s -> severe (~10%), urgent IV volume expansion.",
"Compared with dehydration-assessment?",
"Both are dehydration assessments; this tool scores by sign items, same algorithm.",
"Gold standard?",
"Pre/post weight change is most accurate; signs are for rapid on-site staging.",
"About the Dehydration (Body Fluid Loss) Assessment",
"A WHO/IMCI-based pediatric dehydration tool that quickly gauges severity via 8 clinical signs (mental status, eye sockets, drinking, skin turgor, mucosa/tears, fontanelle, urine, pulse) and estimates fluid loss and rehydration plan.",
"WHO/IMCI standardized clinical-sign assessment",
"Body-weight loss percentage calculation",
"Fluid loss estimation",
"WHO Plan A/B/C rehydration recommendations",
"Emergency/outpatient rapid pediatric dehydration triage",
"Fluid management for diarrheal disease",
"Primary-care initial assessment",
"Parent education on dehydration recognition",
"e.g. if pre-illness weight is known",
    ]))

    # assessor-spo2 (39)
    write('assessor-spo2', build('assessor-spo2', [
"Congenital Heart Disease (Murmur/SpO2) Assessment",
"Neonatal/infant CHD screening by pulse oximetry (SpO2) and heart murmur, referencing CCHD screening guidelines",
"Core formula (by input): |(rh-ft)|; min(rh,ft)",
"Age (days)",
"Term/preterm",
"Term infant (≥37 weeks)",
"Preterm infant (<37 weeks)",
"Pulse oximetry measurement (SpO2)",
"Right-hand SpO2 (%)",
"Right-foot/left-foot SpO2 (%)",
"Repeat measurement done (after 1 hour)",
"Heart murmur and signs",
"Other high-risk factors",
"Based on AHA/AAP CCHD pulse-oximetry screening guideline, recommended at 24-48 hours after birth",
"SpO2 <90% (any site): CCHD screen positive, needs urgent evaluation",
"SpO2 90-94% or difference >3%: repeat after 1 hour, positive if still abnormal",
"This tool is for screening reference only; diagnosis needs echocardiography",
"In-Depth: CHD Screening (SpO2)",
"Right upper limb/foot SpO2",
"Difference judgment",
"Repeat confirmation",
"Right hand 95, foot 90",
"Diff=5%>3% and lowest 90 -> high risk, echo needed to rule out duct-dependent CHD.",
"Both ≥95",
"Both hands/feet ≥95 and diff <3% -> screen negative, still follow up feeding and growth.",
"Screening timing?",
"Measure at 24-48h after birth in a calm state; crying causes falsely low values.",
"Difference from chd-assessment?",
"This tool focuses on pulse-oximetry difference; chd-assessment combines murmur and symptoms.",
"About the Congenital Heart Disease (Murmur/SpO2) Assessment",
"A CHD screening tool based on AHA/AAP CCHD guidelines, combining pulse oximetry (right-hand + foot SpO2), heart murmur and other clinical signs with high-risk factors for comprehensive CHD risk assessment.",
"CCHD pulse-oximetry screening standard workflow",
"Heart murmur and sign grading assessment",
"High-risk factor screening (7 items)",
"Comprehensive risk grading and management advice",
"Routine newborn screening at 24-48 hours after birth",
"Pediatric clinic initial heart-murmur assessment",
"Primary-care CHD screening",
"Follow-up of high-risk CHD newborns",
    ]))

    # chd-assessment (42)
    write('chd-assessment', build('chd-assessment', [
"Congenital Heart Disease (Murmur/SpO2) Assessor",
"Screen neonatal CHD by combining heart-murmur features and pulse oximetry saturation",
"Core formula (by input): |(rh-ll)|",
" / CHD Assessor",
"Day of age",
"Right-hand (pre-ductal) SpO2 (%)",
"Lower-limb (post-ductal) SpO2 (%)",
"Heart murmur",
"No murmur",
"Soft/physiologic",
"Harsh/pathologic",
"Central cyanosis",
"Tachypnea",
"Feeding difficulty",
"Excessive sweating",
"Newborn pulse-oximetry screening standard",
"Right-hand SpO2",
"Lower-limb SpO2",
"Difference",
"Negative (pass)",
"Repeat measurement",
"or 3-4%",
"Positive (refer)",
"Note: pulse-oximetry screening after 24h of birth detects >75% of critical CHD (CCHD). Right hand (pre-ductal) samples left subclavian artery (aortic blood); lower limb (post-ductal) samples iliac artery (aorta + ductal blood). Difference ≥5% suggests duct-dependent lesions (e.g. coarctation/interruption). Harsh holosystolic/diastolic murmurs are mostly pathologic. Cyanotic CHD (tetralogy of Fallot/transposition) needs PGE1 to keep the ductus open. This tool is for screening reference only.",
"In-Depth: CHD Murmur/SpO2 Assessment",
"Harsh murmur",
"Upper/lower limb SpO2 difference",
"Cyanosis/tachypnea",
"Harsh murmur + difference",
"Harsh pathologic murmur + upper/lower limb SpO2 difference >3% -> high-risk CHD, urgent echo.",
"Isolated soft",
"Soft murmur, normal SpO2, no cyanosis -> low risk, follow up to distinguish benign murmur.",
"Meaning of SpO2 difference?",
"Pre-ductal (right arm) vs post-ductal (lower limb) difference >3% suggests coarctation/duct-dependent CHD.",
"What is an emergency?",
"Cyanosis + tachypnea + feeding difficulty + harsh murmur needs neonatal intervention.",
"About the Congenital Heart Disease (Murmur/SpO2) Assessor",
"The CHD (murmur/SpO2) assessor screens neonatal CHD by heart-murmur features and oxygen saturation. A medical professional tool based on authoritative standards, for reference only.",
"How to use the CHD (Murmur/SpO2) Assessor",
"What does the CHD (Murmur/SpO2) Assessor do?",
"How to use the CHD (Murmur/SpO2) Assessor?",
"Which scenarios is the CHD (Murmur/SpO2) Assessor suitable for?",
    ]))

    # ddst-screening (31)
    write('ddst-screening', build('ddst-screening', [
"DDST Developmental Screening Tool",
"Denver Developmental Screening Test (DDST): screen four domains - personal-social, fine-motor-adaptive, language, gross-motor - by age lines",
"The DDST developmental screening tool screens the four domains - personal-social, fine-motor-adaptive, language, gross-motor - by age lines, and outputs results based on the input parameters.",
" / DDST Developmental Screener",
"Corrected gestational age (weeks, for preterm infants)",
"Generate screening report",
"DDST result interpretation",
"All domain items pass on the left of the age line",
"Regular follow-up",
"≥1 item fails completely to the right of the age line / ≥2 items fail within the age-line zone",
"Re-check after 2-3 weeks",
"≥2 items fail completely to the right of the age line / ≥2 delays in one domain",
"Refer for developmental assessment",
"Unable to test",
"Non-cooperative/too rejecting",
"Re-test another day",
"Note: DDST is a screening, not a diagnostic tool, for children 0-6 years. To the left of the age line, 75% of children pass = 'pass'; on the line = 'age-line item'; to the right = 'harder item'. Preterm infants are assessed by corrected age until age 2. A positive screen needs referral to diagnostic assessments such as the Gesell or Bayley scales. This tool is for screening reference only.",
"In-Depth: DDST Developmental Screening",
"4 domains",
"Month-age adaptation",
"Abnormal/suspect",
"18 months, 2 domains delayed",
"Personal-social/fine-motor etc. 2 domains fail -> abnormal; re-check after 2-3 weeks, refer if still abnormal.",
"Each domain ≥80% pass -> normal, regular check-up follow-up.",
"What are the domains?",
"Personal-social, fine-motor, language, gross-motor; delay in any 2 domains is abnormal.",
"Screening is not diagnosis",
"DDST is screening; abnormalities need further pediatric neuro/developmental specialist evaluation.",
"About the DDST Developmental Screening Tool",
"The Denver Developmental Screening (DDST) tool assesses the four domains - personal-social, fine-motor, language, gross-motor - by age lines. A medical professional tool based on authoritative standards, for reference only.",
"e.g. 34",
    ]))

    # dehydration-assessment (29)
    write('dehydration-assessment', build('dehydration-assessment', [
"Dehydration (Body Fluid Loss) Assessor",
"Quantify pediatric dehydration by Gorelick clinical-sign score and compute a rehydration plan",
"Core formula (by input): ((prevWeight-weight)/prevWeight×100); weight×deficitPercent×1000; weightLoss/100",
" / Dehydration Assessor",
"Pre-illness weight (kg, optional)",
"Clinical-sign assessment (Gorelick criteria, check present signs)",
"Dehydration severity grading standard",
"Thirst, slightly reduced urine",
"Oral rehydration (ORS)",
"Poor skin turgor, sunken eyes, oliguria",
"Oral/IV rehydration",
"Lethargy/coma, anuria, shock",
"Urgent IV rehydration",
"Note: the Gorelick score has 10 signs, 1 point each. ≥3 = moderate dehydration (sensitivity 74%, specificity 86%), ≥7 = severe. Rehydration principle: replace fast then slow, salt before sugar, add potassium once urine appears. Moderate-severe dehydration needs prompt medical care. This tool is for clinical reference only.",
"In-Depth: Dehydration Gorelick Assessment",
"Gorelick score",
"Cumulative loss volume",
"Oral/IV",
"10 kg, score 4",
"Gorelick 4 points -> loss ~7.5%: cumulative loss = 10×0.075 = 750 mL, needs replenishment.",
"Mild/moderate/severe",
"Score ≤2 ~4%, 3-6 ~7.5%, ≥7 ~12% fluid deficit.",
"When is Gorelick applicable?",
"For rapid staging of diarrheal children aged 1 month-5 years; combined with weight change is more accurate.",
"Rehydration principle?",
"First replace cumulative loss, then give maintenance (100 mL/kg for first 10 kg); IV if oral not tolerated.",
"About the Dehydration (Body Fluid Loss) Assessor",
"The pediatric dehydration (fluid-loss) assessor quantifies severity by Gorelick criteria and computes fluid requirement and rehydration plan. A medical professional tool based on authoritative standards, for reference only.",
"e.g. 10.5",
    ]))

if __name__ == '__main__':
    main()

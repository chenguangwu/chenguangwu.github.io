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
# body for pediatrics b4: pediatric-asthma / pediatric-fever / pediatric-fracture / pediatric-pneumonia / rater-27

def main():
    # pediatric-asthma (21)
    write('pediatric-asthma', build('pediatric-asthma', [
"Childhood Asthma Control Test Tool",
"Childhood Asthma Control Test (C-ACT 4-11 yr) / ACT (≥12 yr) to assess asthma control over the past 4 weeks",
" / Childhood Asthma Control Tool",
"Asthma Control Level Grading",
"Maintain current plan, regular follow-up",
"Step up treatment, strengthen management",
"Urgently adjust plan / seek care",
"Note: C-ACT is for 4-11 yr (7 items: child self + parent); ACT for ≥12 yr. Assess past 4 weeks. Long-term goal: achieve and maintain control, prevent attacks, keep normal lung function. ICS (inhaled corticosteroids) is first-line controller. Acute PEF <60% predicted needs care. This tool is for clinical reference, not a substitute for professional evaluation.",
"In-Depth: Childhood Asthma Control (C-ACT)",
"C-ACT 7 items",
"Child + parent",
"Control grading",
"C-ACT 25 points",
"Full 25 -> well controlled, maintain current step, re-evaluate in 3 months.",
"19-22 -> partly controlled, step up and check inhaler technique.",
"When is C-ACT used?",
"4-11 yr, child self-report + parent observation combined, more sensitive.",
"Score meaning?",
"≥20 controlled, 13-19 partly, ≤12 uncontrolled, guides step up/down.",
"About the Childhood Asthma Control Test Tool",
"The childhood asthma control tool (C-ACT/ACT) assesses control in 4-11 yr and ≥12 yr children and guides treatment adjustment. A medical professional tool based on authoritative standards, for reference only.",
    ]))

    # pediatric-fever (35)
    write('pediatric-fever', build('pediatric-fever', [
"Fever (Axillary/Rectal Temp) Care Guide",
"By measured temperature type and value, assess fever degree and give care advice and when to seek care",
"The fever-care guide assesses fever degree from temperature type and value and gives care advice and when to seek care, outputting results from the input parameters.",
" / Fever Care Guide",
"Axillary",
"Rectal",
"Ear (tympanic)",
"Oral",
"Forehead",
"Temperature value (°C)",
"Fever >3 days",
"Fever >5 days",
"Antibiotics used without effect",
"Generate care plan",
"Normal Values and Conversion by Site",
"Measurement site",
"Fever criterion",
"≈ axillary +0.3°C",
"≈ axillary +0.5°C",
"≈ rectal",
"≈ axillary (easily affected)",
"Note: infants <3 months with fever ≥38°C (rectal) need immediate care. Antipyretic first choice: acetaminophen (≥2 mo) or ibuprofen (≥6 mo). Do not alternate/combine two antipyretics. Physical cooling: tepid sponge bath; no alcohol rub. Fever is an immune response; do not chase a fully normal temperature - focus on comfort. This tool is for care reference only.",
"In-Depth: Pediatric Fever Care",
"Axillary/oral/rectal correction",
"Danger signs",
"Antipyresis and hydration",
"Axillary 38.5",
"Axillary 38.5°C is fever (rectal correction +0.5 = 39.0); if alert, observe and hydrate.",
"Young infant, fever >3-5 days, poor spirits, seizures -> seek care promptly, do not blindly antipyrese.",
"Difference by site?",
"Rectal/ear ~0.5°C and oral ~0.3°C higher than axillary; convert uniformly before judging fever.",
"When to medicate?",
"≥38.5°C or clearly unwell; antipyretic; focus on fluids and watching alertness.",
"About the Fever (Axillary/Rectal Temp) Care Guide",
"The pediatric fever-care guide assesses fever degree from axillary/rectal/ear temperature and gives physical cooling, medication and care-seeking guidance. A medical professional tool based on authoritative standards, for reference only.",
    ]))

    # pediatric-fracture (48)
    write('pediatric-fracture', build('pediatric-fracture', [
"Pediatric Fracture (Epiphyseal) Considerations Tool",
"Salter-Harris physeal-injury classification: judge type, prognosis and management of pediatric growth-plate injury",
" / Pediatric Epiphyseal Fracture Tool",
"Injury site",
"Distal radius",
"Distal humerus (supracondylar)",
"Distal femur",
"Proximal tibia",
"Distal tibia",
"Finger/toe bones",
"Salter-Harris type (select fracture type)",
"Epiphyseal separation + metaphysis fracture",
"Epiphyseal fracture",
"Epiphyseal + metaphysis fracture",
"Physis crush injury",
"Significant displacement",
"Open fracture",
"Neurovascular injury",
"Salter-Harris Type Quick Reference",
"Fracture line",
"Growth-disturbance risk",
"Type I",
"Through physis only (separation)",
"Type II",
"Physis + metaphyseal triangle",
"Good (most common)",
"Type III",
"Physis + epiphysis (intra-articular)",
"Moderate (needs anatomic reduction)",
"Type IV",
"Physis + epiphysis + metaphysis",
"Poor (bone-bridge risk)",
"Type V",
"Physis crush (compression)",
"Poor (easily missed)",
"Note: pediatric bone features: thick tough periosteum (greenstick common), epiphyses (growth plates) prone to injury. Epiphyseal injury can cause growth disturbance (limb-length discrepancy/angular deformity). Higher Salter-Harris type (III-V) -> greater growth-disturbance risk. Key sites: distal femur, distal tibia (triplane), distal radius physis need special attention. Premature physeal closure usually appears 6-12 months post-injury; long follow-up until skeletal maturity. This tool is for clinical reference only.",
"In-Depth: Pediatric Fracture Epiphysis",
"Salter-Harris types",
"Site growth risk",
"Open/vascular",
"Distal-femur physis is 70% of lower-limb growth; Salter IV almost always causes disturbance, needs anatomic reduction.",
"Adolescent triplane (Tillaux) fracture involves the physis; CT assesses articular surface before fixation.",
"Why care about epiphysis?",
"Physis relates to future height and alignment; injury can cause unequal legs/varus.",
"Emergency?",
"Open, neurovascular compromise, significant displacement need emergency care.",
"About the Pediatric Fracture (Epiphyseal) Considerations Tool",
"The pediatric (epiphyseal) fracture considerations tool classifies Salter-Harris physeal injury and judges growth-plate prognosis and management. A medical professional tool based on authoritative standards, for reference only.",
    ]))

    # pediatric-pneumonia (37)
    write('pediatric-pneumonia', build('pediatric-pneumonia', [
"Pneumonia (Tachypnea/Indrawing) Severity Assessor",
"WHO pneumonia-management standard: assess severity by respiratory rate and clinical signs, give management advice",
"The pneumonia severity assessor, based on WHO pneumonia-management standard, assesses severity by respiratory rate and clinical signs and gives management advice, outputting results from the input parameters.",
" / Pneumonia Severity Assessor",
"Respiratory rate (breaths/min)",
"SpO2 (%)",
"Clinical signs (check present)",
"WHO Pediatric Pneumonia Grading",
"Tachypnea criterion",
"Other signs",
"Management",
"No pneumonia",
"Cough / no tachypnea",
"Home observation",
"Pneumonia",
"2-11 mo ≥50; 1-5 yr ≥40",
"No severe signs",
"Oral antibiotics",
"Severe pneumonia",
"Chest indrawing/nasal flaring/SpO2<90%",
"Admit + IV antibiotics",
"Very severe pneumonia",
"Central cyanosis/refusal to feed/lethargy/convulsions",
"Emergency + ICU",
"Note: tachypnea is the most sensitive sign of pneumonia. Chest indrawing (lower chest wall retraction) suggests severe disease. Hypoxemia (SpO2<90%) needs oxygen. Neonatal pneumonia is atypical (bubbling/periodic breathing). Severe pneumonia needs complication workup (empyema/pneumothorax/ARDS). This tool is for clinical reference only.",
"In-Depth: Pediatric Pneumonia Severity",
"Tachypnea threshold",
"SpO2 grading",
"Indrawing sign",
"2-mo infant RR≥60 is tachypnea; this case 50 exceeds and SpO2 88<90 -> severe pneumonia, admit for oxygen.",
"No tachypnea, SpO2≥95, feeding OK -> community oral antibiotics follow-up.",
"RR threshold?",
"<2 mo ≥60, 2-12 mo ≥50, 1-5 yr ≥40 breaths/min is tachypnea.",
"Severe criteria?",
"SpO2<90, chest indrawing, feeding refusal, cyanosis, lethargy - any one means severe.",
"About the Pneumonia (Tachypnea/Indrawing) Severity Assessor",
"The pediatric pneumonia (tachypnea/indrawing) severity assessor, based on WHO standard, assesses severity and admission indications. A medical professional tool based on authoritative standards, for reference only.",
    ]))

    # rater-27 (37)
    write('rater-27', build('rater-27', [
"Growth Curve (Height/Weight/Head) Z-Score",
"Compute Z-scores from WHO growth standards to assess physical growth (for 0-60 months)",
"Core formula (by input): wt÷(ht÷100)^2",
"Measurement data",
"Length/height (cm)",
"Head circumference (cm)",
"Measured as standing height (select for ≥24 months)",
"Calculate Z-scores",
"Z = (measured - median) / SD, based on WHO 2006 growth standard",
"Z < -3: severely below; Z < -2: moderately below; Z > 2: above; Z > 3: severely above",
"0-24 months use recumbent length; ≥24 months standing height",
"For reference only; growth assessment needs full exam and history",
"In-Depth: Growth Curve Z-Score",
"WHO data",
"Month-age interpolation",
"Boy 18 mo, height 76",
"Interpolated WHO median 82.3, SD≈3.2: Z=(76−82.3)/3.2≈−2.0 -> stunting borderline, needs nutrition assessment.",
"Normal range",
"Z within −2~+2 normal; <-2 stunting, >2 overweight/obesity.",
"Relation to growth-curve-zscore?",
"Both are growth Z-scores; this is the old slug, same algorithm.",
"Percentile conversion?",
"Z converts to percentile via error function, easier for parents (e.g. Z−2≈2.3%).",
"About the Growth Curve (Height/Weight/Head) Z-Score",
"A WHO 2006-based pediatric Z-score tool: input sex, age and measurements (weight/length-height/head) to compute Z-scores and percentiles and assess growth (stunting/underweight/wasting/overweight etc.).",
"WHO 2006 reference data",
"Weight/age, length(height)/age, head/age Z-scores",
"BMI Z-score estimate and nutritional status",
"Percentile calculation and visualization",
"Routine growth assessment in well-child clinics",
"Malnutrition screening and grading",
"Child overweight/obesity screening",
"Growth follow-up trend monitoring",
"How to use the Growth Curve (Height/Weight/Head) Z-Score",
"What does the Growth Curve (Height/Weight/Head) Z-Score do?",
"How to use the Growth Curve (Height/Weight/Head) Z-Score?",
"Which scenarios is the Growth Curve (Height/Weight/Head) Z-Score suitable for?",
    ]))

if __name__ == '__main__':
    main()

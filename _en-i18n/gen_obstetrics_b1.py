#!/usr/bin/env python3
# gen_obstetrics_b1.py — obstetrics b1 (5 slugs): afi-normal/bishop-score/calc-50/calc-risk/ctg-fhr
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'obstetrics')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'obstetrics')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

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
    out = {'slug': slug, 'industry': 'obstetrics', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

# body: obstetrics b1
def main():
    afi_normal_en = [
        '🏋️ Amniotic Fluid Index (AFI) Normal Range Assessor',
        'Sum of the deepest vertical pockets in four quadrants to assess amniotic fluid volume, diagnosing oligo-/polyhydramnios',
        '/ AFI Assessor',
        '📖 View "Amniotic Fluid Index (AFI) Normal Range Assessor User Guide"',
        'Amniotic Fluid Index (AFI)',
        'Deepest Vertical Pocket (DVP)',
        'Divide the abdomen into four quadrants using the umbilicus as a cross, and measure the deepest vertical pocket in each (excluding limbs/umbilical cord)',
        'AFI = Dα + Dβ + Dγ + Dδ (sum of the deepest vertical pockets in four quadrants); SDP = single deepest pocket',
        'AFI sums the four-quadrant depths; AFI 5–24 cm is normal, <5 cm oligohydramnios, >24 cm polyhydramnios; SDP 2–8 cm is normal.',
        'Right Upper Quadrant (RUQ) (cm)',
        'Left Upper Quadrant (LUQ) (cm)',
        'Right Lower Quadrant (RLQ) (cm)',
        'Left Lower Quadrant (LLQ) (cm)',
        'Assess amniotic fluid volume',
        'Single deepest vertical pocket (SDP)',
        'Deepest pocket depth (cm)',
        '📊 Amniotic Fluid Volume Criteria',
        'Oligohydramnios',
        'Polyhydramnios',
        'AFI (sum of four quadrants)',
        'Borderline AFI',
        'SDP (single deepest depth)',
        'Note: AFI ≤ 5 indicates oligohydramnios; 5.1–8 is borderline low. Reference ranges vary slightly by gestational week.',
        '🔬 Causes of Abnormal Amniotic Fluid Volume',
        'Oligohydramnios (AFI ≤ 5)',
        'Fetal factors: urinary tract anomalies (renal agenesis, urethral obstruction), FGR, premature rupture of membranes',
        'Maternal factors: dehydration, preeclampsia, post-term pregnancy, drugs (ACE inhibitors/NSAIDs)',
        'Placental factors: placental insufficiency',
        'Polyhydramnios (AFI ≥ 25)',
        'Fetal factors: GI/CNS malformations, chromosomal abnormalities, fetal hydrops',
        'Maternal factors: gestational diabetes (most common), Rh incompatibility',
        'Idiopathic: about 30% have no identifiable cause',
        'Tip: amniotic fluid reflects fetal renal and digestive function and placental status. Oligohydramnios is associated with fetal distress and pulmonary hypoplasia; polyhydramnios raises the risk of preterm birth and malpresentation. This tool is for ultrasound assessment reference only.',
        '📚 In-Depth: AFI Measurement and Interpretation',
        'In the third trimester, ultrasound measures the largest pocket in four quadrants; summing them yields AFI to judge whether fluid is too low or too high.',
        'Use AFI to quickly screen for oligohydramnios when premature rupture of membranes or fetal growth restriction is suspected.',
        'Monitor AFI to rule out polyhydramnios during work-up of gestational diabetes or fetal anomalies.',
        'Normal amniotic fluid',
        'Quadrants are 4, 5, 4 and 5 cm; AFI = 4+5+4+5 = 18 cm, within the normal 8–25 cm range.',
        'Oligohydramnios warning',
        'Quadrants 2, 1, 1 and 1 cm; AFI = 5 cm, right at the cutoff, classified as oligohydramnios by guideline; rule out PROM and placental insufficiency.',
        'What is the difference between AFI and the single deepest pocket (SDP)?',
        'AFI is the sum of four quadrants and is more sensitive to low fluid; SDP looks at the single largest pocket. Generally AFI <5 cm or SDP <2 cm both indicate oligohydramnios; clinical diagnosis often combines both.',
        'Does a high AFI always mean a problem?',
        '25–30 cm is mild increase, >30 cm is polyhydramnios; investigate gestational diabetes, fetal GI anomalies or chromosomal abnormalities, but isolated mild increase can occur in normal pregnancy.',
        'About the "Amniotic Fluid Index (AFI) Normal Range Assessor"',
        'The AFI Normal Range Assessor measures the four-quadrant amniotic fluid index to evaluate oligo- and polyhydramnios and guide clinical intervention. A professional medical tool based on authoritative standards, for reference only.',
    ]
    bishop_score_en = [
        '📋 Bishop Cervical Score Labor Induction Predictor',
        'The Bishop score assesses cervical ripeness to predict induction success and delivery mode',
        '/ Bishop Scoring Tool',
        '📖 View "Bishop Cervical Score Labor Induction Predictor User Guide"',
        'Bishop cervical maturity score = dilatation + effacement + station + position + consistency (each 0–3), max 13; ≥8 mature (high induction success), 6–8 fairly mature, <6 immature needing cervical ripening.',
        'Cervical dilatation (cm)',
        '0 (closed)',
        'Cervical effacement (%)',
        'Fetal station',
        'Cervical position',
        'Posterior',
        'Mid',
        'Anterior',
        'Cervical consistency',
        'Firm',
        'Soft',
        '📋 Bishop Scoring Criteria',
        'Effacement (%)',
        'Station',
        '📊 Score Meaning and Induction Strategy',
        'Cervical maturity',
        'Induction success rate',
        'Mature',
        'High (similar to spontaneous labor)',
        'May induce directly with oxytocin',
        'Inducible; ripening as needed',
        'Immature',
        'Need cervical ripening first (prostaglandin/Foley balloon)',
        'Note: the modified Bishop score (position/consistency max 2 each) totals 0–13. A low Bishop score raises induction failure and cesarean rates, with higher predictive value in nulliparae.',
        'Tip: the Bishop score is the classic method to assess cervical maturity. A score ≥6 means mature with high induction success; ≤5 needs ripening first (e.g. dinoprostone, misoprostol, Foley balloon). For clinical reference only.',
        '📚 In-Depth: Bishop Cervical Maturity Score',
        'Assess cervical condition before induction to predict oxytocin induction success.',
        'Decide whether cervical ripening (e.g. prostaglandin) is needed before induction.',
        'Determine candidacy for trial of labor versus cesarean.',
        'Mature cervix: induce directly',
        'Dilatation 3 cm (3 pts), effacement 100% (3 pts), station −1 (2 pts), moderate (1 pt), anterior (2 pts): total 3+3+2+1+2 = 11/13, ≥8 mature with high induction success.',
        'Immature: needs ripening',
        'Dilatation 0 cm (0 pts), effacement 30% (1 pt), station −3 (0 pts), posterior (0 pts), firm (0 pts): total 1, <6 needs ripening first.',
        'What Bishop score allows induction?',
        '≥8 is considered mature and allows direct oxytocin induction; 6–7 has higher success; <6 suggests ripening agents (prostaglandins) before re-evaluation.',
        'What is the maximum score?',
        'The max is 13, from five items—dilatation, effacement, station, consistency, position—each scored 0–2 or 0–3.',
        'About the "Bishop Cervical Score Labor Induction Predictor"',
        'The Bishop score predictor assesses cervical maturity to predict induction success and guide the choice of induction method. A professional medical tool based on authoritative standards, for reference only.',
    ]
    calc_50_en = [
        '🔮 Postpartum Hemorrhage (Estimated Blood Loss) Calculator',
        'Estimate blood volume and postpartum blood loss from height, weight and hematocrit change to support clinical grading.',
        '📖 View "Postpartum Hemorrhage (Estimated Blood Loss) Calculator User Guide"',
        'Blood loss = blood volume × (pre-Hct − post-Hct) / pre-Hct',
        'Delivery mode',
        'Vaginal delivery',
        'Cesarean section',
        'Pre-delivery Hct (%)',
        'Post-delivery Hct (%)',
        '💡 Formula: blood volume (Nadler) = 0.3561 × H³(m) + 0.03308 × W(kg) + 0.1833; blood loss = blood volume × (pre-Hct − post-Hct) / pre-Hct.',
        'PPH grading: vaginal loss ≥500 mL, cesarean ≥1000 mL; severe PPH >1500 mL.',
        'Pre- and post-delivery Hct must be comparable venous samples from the same time window.',
        'This tool is an estimation aid and cannot replace clinical assessment and lab tests.',
        '📚 In-Depth: Postpartum Blood Loss Estimation (Hematocrit Method)',
        'Postpartum, infer actual loss from pre/post Hct change—more accurate than visual estimate.',
        'For occult bleeding (retained clot), estimate from hemoglobin/Hct drop.',
        'Quantify blood loss before activating a massive transfusion protocol.',
        'Occult blood loss estimation',
        'Maternal blood volume ~5000 mL, pre-Hct 35% to post 25%: loss = 5000 × (35−25) ÷ 35 ≈ 1428.6 mL, ≥1000 mL is severe PPH needing active management.',
        'Mild blood loss',
        'Hct 38% to 34%: loss = 5000 × (38−34) ÷ 38 ≈ 526.3 mL, just over 500 mL; start monitoring and uterotonics per PPH protocol.',
        'Why infer from Hct instead of weighing swabs?',
        'Visual and weighing methods underestimate occult loss (especially intrauterine clot); the Hct method reflects overall red-cell loss and better shows whether the transfusion threshold is reached.',
        'What is the normal upper limit of postpartum loss?',
        'Vaginal ≥500 mL or cesarean ≥1000 mL defines PPH; ≥1500 mL is refractory, needing massive transfusion and surgical intervention.',
        'About the "Postpartum Hemorrhage (Estimated Blood Loss) Calculator"',
        'Use the Nadler formula to estimate maternal blood volume, combine pre- and post-delivery hematocrit changes to estimate blood loss, and grade PPH by vaginal/cesarean criteria.',
        'Estimate blood volume with the Nadler formula',
        'Estimate blood loss and its percentage of blood volume from Hct change',
        'Supports both vaginal and cesarean grading criteria',
        'Rapid intrapartum blood-loss assessment',
        'Perioperative blood-loss estimation',
        'Obstetric emergency training and teaching',
    ]
    calc_risk_en = [
        '📋 Down Syndrome Screening (AFP/free β-hCG) Risk Calculator',
        'Estimate Down syndrome risk from age-based prior risk and AFP, free β-hCG MoM values using the likelihood-ratio method.',
        '📖 View "Down Syndrome Screening (AFP/free β-hCG) Risk Calculator User Guide"',
        'Risk = background risk (maternal age/weight/gestation) × MoM correction; MoM = measured value / median for age (AFP, free β-hCG)',
        'Screening risk is computed from age-based background risk combined with serum-marker MoM values, output as a 1:N birth-defect risk.',
        'Maternal age (years)',
        'Gestational week (weeks)',
        '💡 Method: age prior risk × AFP likelihood ratio × free β-hCG likelihood ratio. High-risk cutoff 1/270, low-risk cutoff 1/1000. Follow laboratory and clinical standards in practice.',
        'This tool is for education/auxiliary calculation and cannot replace a formal prenatal screening report.',
        'MoM values are already corrected by the lab for gestation, weight, etc.; enter the corrected value.',
        'A high-risk result warrants genetic counseling and further prenatal diagnosis.',
        '📚 In-Depth: Down Syndrome Serologic Risk Stratification (Bayesian)',
        'First/second-trimester serologic screening (age + markers) computes fetal Down syndrome risk.',
        'Explain likelihood ratios and combined risk to borderline-risk women.',
        'Decide whether to proceed to NIPT or amniocentesis.',
        'Woman 30 yrs, 60 kg, 16 wks, AFP 1.0 MoM, free β-hCG 1.5 MoM: age background ~1/963, combined LR ≈1.0, posterior ≈1/963, below 1/1000 = low risk.',
        'Borderline-risk example',
        'If free β-hCG rises to 2.5 MoM (LR up ~4), posterior ≈1/240, crossing the 1/270 cutoff into high risk; suggest amniocentesis or NIPT review.',
        'What does a risk of 1/270 mean?',
        'It means about 1 affected fetus per 270 comparable pregnancies; the traditional second-trimester high-risk cutoff—≥1/270 is high risk and needs diagnostic testing.',
        'Can serologic screening confirm the diagnosis?',
        'No, it only gives a risk probability. Confirmation needs amniocentesis (karyotype) or CVS; NIPT is advanced screening, not diagnosis.',
        'About the "Down Syndrome Screening (AFP/free β-hCG) Risk Calculator"',
        'Combines maternal age, gestation, and AFP/free β-hCG MoM values to estimate Down syndrome screening risk via the likelihood-ratio method.',
        'Age-related prior risk with smooth interpolation',
        'Combined AFP and free β-hCG likelihood-ratio assessment',
        'Stratified by 1/270 and 1/1000 cutoffs',
        'Rapid prenatal screening risk estimation',
        'Helps interpret formal screening reports',
    ]
    ctg_fhr_en = [
        '❤️ Fetal Heart Rate (CTG) Baseline Variability Analyzer',
        'Analyze the four CTG elements per FIGO/NICE standards to assess fetal in-utero status',
        '/ CTG Analyzer',
        '📖 View "Fetal Heart Rate (CTG) Baseline Variability Analyzer User Guide"',
        'Baseline rate 110–160 bpm normal; baseline variability 5–25 bpm is moderate (normal)',
        'Assess baseline, variability, decelerations and accelerations: if abnormal items ≥0 and suspicious items ≥0 → normal; otherwise grade as suspicious/abnormal.',
        'Baseline fetal heart rate (bpm)',
        'Baseline variability (bpm)',
        'Acceleration',
        'Present (≥15 bpm, ≥15 s)',
        'Absent',
        'Prolonged (≥2 min)',
        'No deceleration',
        'Early deceleration (with contractions)',
        'Prolonged deceleration (≥2 min, <10 min)',
        'Recurrent deceleration (>50% of contractions)',
        'Contraction frequency (per 10 min)',
        'Analyze CTG',
        'Abnormal example',
        '📊 Four CTG Elements (FIGO Standard)',
        'Baseline rate',
        '100–110 or >160',
        '<100 or >160',
        'Variability',
        '<5 (within 40 min)',
        '<5 (>40 min) or >25',
        'Deceleration',
        'None/early',
        'Late/prolonged/recurrent variable',
        'Present',
        'No acceleration: judge with variability',
        '🎯 CTG Result Classification (NICE Three-Tier)',
        'All four elements normal',
        'Continue monitoring',
        'One element non-normal, rest normal',
        'Intensify monitoring, find cause, treat symptomatically',
        'One abnormal + one suspicious, or two abnormal',
        'Assess immediately, prepare cesarean, emergency delivery if needed',
        '📉 Deceleration Type Interpretation',
        'Early deceleration:',
        'Appears with contractions, U-shaped, mostly fetal head compression, usually benign',
        'Variable deceleration:',
        'Not fixed to contractions, V- or U-shaped, suggests umbilical cord compression',
        'Late deceleration:',
        'Appears after contraction peak, suggests reduced placental perfusion/fetal hypoxia',
        'Prolonged deceleration:',
        'Lasts 2–10 min; watch for placental abruption, cord prolapse, etc.',
        'Tip: CTG interpretation needs clinical context (gestation, risk factors, labor). Variability is the most important indicator of fetal acid-base status. Abnormal CTG warrants fetal scalp blood pH or further assessment. For reference only.',
        '📚 In-Depth: CTG Interpretation and Grading',
        'Use CTG baseline, variability and accelerations to read fetal status during labor or with reduced fetal movement.',
        'Recognize normal/suspicious/pathological patterns to time intervention.',
        'Interpret remote fetal monitoring reports.',
        'Normal CTG',
        'Baseline 140 bpm, variability 6 ms (moderate), 1 acceleration: fits Normal CTG, continue observation.',
        'Suspicious CTG',
        'Baseline 175 (tachycardia), variability <5 ms (reduced), no acceleration: falls into Suspicious CTG; change position, give oxygen and recheck, fetal scalp stimulation if needed.',
        'Does reduced variability always mean danger?',
        'Reduced variability (<5 ms) is a suspicious signal, but may be due to the fetus',
        'sleep cycle',
        'or maternal sedatives; judge with accelerations, decelerations and recheck—only persistent reduction suggests hypoxia risk.',
        'What to do for pathological CTG?',
        'Sinusoidal pattern or absent variability with recurrent late decelerations calls for immediate intrauterine resuscitation and preparation for emergency delivery (cesarean).',
        'About the "Fetal Heart Rate (CTG) Baseline Variability Analyzer"',
        'The CTG Baseline Variability Analyzer evaluates fetal monitoring baseline rate, variability, accelerations and decelerations per FIGO/NICE standards to identify fetal distress. A professional medical tool based on authoritative standards, for reference only.',
    ]
    write('afi-normal', build('afi-normal', afi_normal_en))
    write('bishop-score', build('bishop-score', bishop_score_en))
    write('calc-50', build('calc-50', calc_50_en))
    write('calc-risk', build('calc-risk', calc_risk_en))
    write('ctg-fhr', build('ctg-fhr', ctg_fhr_en))

if __name__ == '__main__':
    main()

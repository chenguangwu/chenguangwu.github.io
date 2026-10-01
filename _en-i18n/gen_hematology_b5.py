#!/usr/bin/env python3
# gen_hematology_b5.py — hematology b5 (5 slugs): pnh-flow/rater-5/rater-6/rater-risk-1/thrombin-generation
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'hematology')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'hematology')

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
    out = {'slug': slug, 'industry': 'hematology', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))


B = {}

B['pnh-flow'] = [
 '🔍 PNH Flow Cytometry (CD55/CD59) Detector',
 'Interprets flow cytometry results and assesses PNH clone size and clinical significance.',
 'PNH Flow CD55/CD59 Detector',
 '/ PNH Flow Cytometry',
 '📖 Read the "PNH Flow Cytometry (CD55/CD59) Detector Usage Guide"',
 'PNH clone size = proportion of CD55- or CD59-deficient cells, measured separately for granulocytes and monocytes (monocytes more sensitive); clone at least 50% is large, 10-50% medium, below 10% small; a granulocyte clone above 20% with haemolysis suggests high risk, thrombosis risk rises with clone size, and LDH with D-dimer can be combined.',
 'FLAER assay (recommended method)',
 'Granulocyte FLAER-negative clone (%)',
 'Monocyte FLAER-negative clone (%)',
 'CD55/CD59 assay (traditional method)',
 'Red cell CD59-negative (%)',
 'Red cell CD55-negative (%)',
 'Granulocyte CD59-negative (%)',
 'Granulocyte CD55-negative (%)',
 'Evidence of haemolysis present',
 'History of thrombosis',
 'Coexisting aplastic anaemia',
 '📋 PNH clone grading',
 'Clone size',
 'Granulocytes',
 'Usually no haemolysis symptoms',
 'Small clone',
 'Mild or no haemolysis, common in AA/PNH syndrome',
 'Medium clone',
 'Possible haemolysis, needs monitoring',
 'Large clone',
 'Classic PNH, high haemolysis and thrombosis risk',
 '📊 PNH triad',
 'Complement-sensitive haemolytic anaemia',
 ': raised LDH, lowered haptoglobin, raised indirect bilirubin',
 'Thrombotic tendency',
 ': thrombosis at atypical sites such as visceral / hepatic / portal veins',
 'Bone marrow failure',
 ': pancytopenia, often overlapping with AA/MDS',
 'Method comparison',
 'Target cells',
 'Granulocytes / monocytes',
 'High sensitivity, unaffected by transfusion',
 'Not applicable to red cells',
 'Red cells / granulocytes',
 'Classic method, can measure red cells',
 'Transfusion affects red cell results',
 'Note: PNH clone detection must be combined with clinical presentation. A small clone in AA/MDS patients is common and not necessarily classic PNH. Complement inhibitors (e.g. eculizumab) suit PNH patients with haemolysis or thrombosis. For study reference only.',
 '📚 Deep Dive: PNH Flow Cytometry (CD55/CD59) Detector',
 'Use FLAER / granulocyte clone size to assess PNH burden (most reliable).',
 'Grade by clone size (subclinical <1 / small 1-10 / medium 10-50 / large >50) to set treatment indication.',
 'Combine thrombosis history, haemolysis and coexisting AA for warnings.',
 'Clone grading: largest clone (granulocyte line, FLAER most sensitive) = proportion of type I+II+III deficient cells. <1% subclinical, 1-10% small, 10-50% medium, >50% large. Red-cell clone is often underestimated by transfusion dilution, so the granulocyte line is the standard; large clones carry high thrombosis risk and need screening for visceral venous thrombosis.',
 'Example (granulocyte CD59 deficiency = 30%, others 0, with haemolysis): largest clone = 30% → medium clone (10-50%), haemolysis suggests monitoring LDH and iron metabolism; if clone >50% with haemolysis / thrombosis history, consider complement inhibitor (e.g. eculizumab).',
 'Where is FLAER better than CD55/CD59?',
 'FLAER (fluorescently labelled aerolysin) binds the GPI anchor directly, is unaffected by transfusion dilution and highly sensitive, making it the gold standard for granulocyte PNH clones; traditional CD55/CD59 still helps but is easily affected by red-cell transfusion.',
 'Does a subclinical clone need treatment?',
 'Usually no complement inhibition; the focus is whether aplastic anaemia coexists (AA/PNH syndrome), and repeat flow cytometry every 3-6 months to monitor clone change.',
 'About the PNH Flow CD55/CD59 Detector',
 'A paroxysmal nocturnal haemoglobinuria (PNH) flow cytometry detector: it reads CD55/CD59 and FLAER results and assesses PNH clone size and clinical significance. A professional medical tool based on authoritative medical standards, for reference only.',
]

B['rater-5'] = [
 '📋 Myelofibrosis (MPN) Scoring System',
 'MPN-10 symptom scale plus DIPSS prognostic score, assessing myelofibrosis symptom burden and prognostic risk.',
 '"MPN-10 symptom scale plus DIPSS prognostic score, assessing myelofibrosis symptom burden and prognostic risk" is computed from the input parameters and the result is output.',
 '📖 Read the "Myelofibrosis (MPN) Scoring System Usage Guide"',
 'MPN-10 symptom assessment scale',
 'Rate the severity of the following symptoms over the past week (0 = none at all, 10 = worst imaginable)',
 'DIPSS prognostic score parameters',
 '< 60 years (0 points)',
 '≥ 60 years (1 point)',
 'Constitutional symptoms (night sweats / weight loss / fever)',
 'None (0 points)',
 'Present (1 point)',
 'Peripheral blood blasts (%)',
 'White blood cell count (×10⁹/L)',
 'MPN-10: 10 core symptoms, total 0-100, higher score means heavier symptom burden',
 'DIPSS: dynamic international prognostic scoring system, for MF risk stratification',
 'MPN-10 ≥20 suggests moderate-to-severe symptom burden, intervention should be considered',
 'Results are for reference only; diagnostic and treatment decisions must be made by a haematologist.',
 '📚 Deep Dive: Myelofibrosis (MPN) Scoring System',
 'MPN-10 scale assesses symptom burden (0-100, intervene at ≥20).',
 'DIPSS sets prognostic risk (low ~185 months / high ~16 months).',
 'Symptom + prognosis two dimensions guide JAK2 inhibitor and transplant decisions.',
 'DIPSS: age ≥60 (+1), HGB <100 (+1), peripheral blasts ≥1% (+1), WBC >25 (+1), constitutional symptoms (+1). 0-1 low, 2 intermediate-1, 3 intermediate-2, 4-5 high. MPN-10 ten items each 0-10, total ≥20 is moderate-or-above symptom burden, JAK2 inhibitor advised.',
 'Example (age <60, HGB=105, blasts=2%, WBC=15, no constitutional symptoms, MPN-10=0): DIPSS = 0(age)+0(symptoms)+0(HGB≥100 no add)+1(blasts≥1)+0(WBC≤25) = 1 → low-risk group (median survival ~185 months); MPN-10 no symptom burden, observe for now. If MPN-10 ≥20, add JAK2 inhibitor to improve symptoms.',
 'Which precedes treatment, MPN-10 or DIPSS?',
 'They complement: DIPSS decides "transplant / intensify or not", MPN-10 decides "medicate symptoms or not". Even at DIPSS low risk, if MPN-10 ≥20 a JAK2 inhibitor can still improve splenomegaly and symptoms.',
 'Does DIPSS duplicate IPSS-MF?',
 'Similar thinking but different timing: IPSS-MF is for initial diagnosis including age, DIPSS for re-stratification after diagnosis (adding dynamic items like platelet / transfusion); the same patient can be scored by both systems and cross-checked.',
 'About the Myelofibrosis (MPN) Scoring System',
 'A myelofibrosis (MF) integrated scoring tool: it includes the MPN-10 symptom scale (10 core symptoms, 0-100) and the DIPSS dynamic international prognostic scoring system, assessing symptom burden, prognostic risk stratification and giving treatment advice.',
 'MPN-10 symptom assessment (10 items, 0-10 each)',
 'DIPSS prognostic risk stratification',
 'Median survival estimate',
 'JAK2 inhibitor indication judgement',
 'Myelofibrosis symptom burden assessment',
 'MF prognostic risk stratification',
 'JAK2 inhibitor treatment decision',
 'Treatment efficacy follow-up monitoring',
]

B['rater-6'] = [
 '📋 DIC (3P test / FDP) Score',
 'ISTH overt DIC scoring system, assessing disseminated intravascular coagulation from platelets, D-dimer/FDP, PT and fibrinogen.',
 '"ISTH overt DIC scoring system, assessing disseminated intravascular coagulation from platelets, D-dimer/FDP, PT and fibrinogen" is computed from the input parameters and the result is output.',
 '📖 Read the "DIC (3P test / FDP) Score Usage Guide"',
 'ISTH DIC scoring parameters',
 'Platelet count (×10⁹/L)',
 'D-dimer (mg/L FEU)',
 'Prothrombin time prolongation (seconds)',
 'Fibrinogen (g/L)',
 '3P test (protamine paracoagulation test)',
 'Is there a known DIC-related underlying disease?',
 'Yes (sepsis / trauma / obstetric emergency / malignancy, etc.)',
 'Calculate DIC score',
 'ISTH overt DIC score: total ≥5 suggests overt DIC, needs repeat assessment',
 'Score <5 suggests non-overt DIC, recheck after 24-48 hours',
 'A positive 3P test suggests soluble fibrin monomer complex (SFMC), supporting DIC diagnosis',
 'Results are for reference only; DIC diagnosis needs clinical picture and dynamic monitoring',
 '📚 Deep Dive: DIC (3P test / FDP) Score',
 'Use the ISTH overt DIC score (platelets / D-dimer / PT / fibrinogen) to judge DIC.',
 'Combine the 3P test and FDP to add fibrin monomer and fibrinolysis information.',
 '≥5 overt DIC starts replacement + anticoagulation; <5 non-overt, dynamic recheck.',
 'ISTH score: platelets <50 (+2), 50-100 (+1); D-dimer >10 (+3), 5-10 (+2), >1 (+1); PT prolongation >6s (+2), 3-6s (+1); fibrinogen <1.0 (+1). Prerequisite: a DIC underlying disease; ≥5 overt DIC, <5 non-overt. Added: a positive 3P suggests soluble fibrin monomer (SFMC), raised FDP supports hyperfibrinolysis.',
 'Example (platelets=45, D-dimer=8.5, PT prolongation=5s, fibrinogen=0.9): platelets <50 (+2), D-dimer 5-10 (+2), PT 3-6s (+1), fibrinogen <1.0 (+1) → ISTH = 6 → overt DIC; treat the underlying disease and give platelets / cryoprecipitate / FFP, with anticoagulation if needed.',
 'Does a positive 3P test always mean DIC?',
 'Not necessarily. A positive 3P suggests soluble fibrin monomer, supporting DIC but with limited sensitivity and specificity; late hyperfibrinolysis or prolonged sample standing can give false negative/positive, so combine with the ISTH score and clinical picture.',
 'Can "normal" fibrinogen rule out DIC?',
 'No. In early DIC fibrinogen can be raised by liver disease / inflammation and mask the drop; a dynamic fall or persistently <1.0 g/L is more meaningful, so recheck and combine with the D-dimer trend.',
 'About the DIC (3P test / FDP) Score',
 'An ISTH overt DIC scoring tool: it scores standardisedly from four indicators — platelet count, D-dimer, PT prolongation and fibrinogen — and, with FDP and 3P results, judges whether the overt DIC criteria are met and gives treatment advice.',
 'ISTH standardised DIC score (0-8)',
 'FDP and 3P test supplementary assessment',
 'Overt / non-overt DIC judgement',
 'Blood product transfusion indication advice',
 'ICU sepsis-related DIC assessment',
 'Obstetric massive haemorrhage DIC screening',
 'Trauma / surgery DIC monitoring',
 'DIC dynamic score tracking',
]

B['rater-risk-1'] = [
 '💊 Drug-Induced (ITP) Risk Score',
 'Drug-induced immune thrombocytopenia (DITP) risk assessment, judging causality from drug history and platelet dynamics.',
 'Core formula (by input): totalScore÷maxScore×100',
 '📖 Read the "Drug-Induced (ITP) Risk Score Usage Guide"',
 'Suspected drug information',
 'Suspected drug name',
 'High risk (quinine / quinidine / sulphonamides / vancomycin / rifampicin)',
 'Moderate risk (heparin / carbamazepine / valproate / linezolid)',
 'Low risk (penicillins / cephalosporins / NSAIDs / PPI)',
 'Other / uncertain',
 'Platelet dynamic change',
 'Platelet before dosing (×10⁹/L)',
 'Nadir platelet (×10⁹/L)',
 'Days from dosing to platelet drop',
 'Days to platelet recovery after stopping',
 'Clinical feature assessment',
 'Assess DITP risk',
 'Classic DITP (drug-induced immune thrombocytopenia) features: drop 5-10 days after dosing, recovery 5-7 days after stopping',
 'Heparin-induced thrombocytopenia (HIT) has its own scoring system (4Ts); this tool does not apply to HIT',
 'Platelet <30×10⁹/L with bleeding needs urgent handling',
 'Results are for reference only; confirmation needs drug-dependent antibody testing',
 '📚 Deep Dive: Drug-Induced (ITP) Risk Score',
 'When thrombocytopenia occurs, assess DITP likelihood from drug history and PLT dynamics.',
 'Weight by drug class (heparin / quinine / antibiotics, etc.) + drop magnitude + time window + recovery pattern.',
 'For high-risk drugs (heparin), use 4Ts separately to assess HIT.',
 'DITP weighting: drug class (high 4 / moderate 3 / low 2 / other 1), platelet drop magnitude (≥80%→4, ≥50%→3, ≥30%→2, <30%→1), time window (dosing 1-14 days→3), recovery (stop 1-7 days→3), positive clinical features weighted; combined',
 'gives high / moderate / low possibility.',
 'Example (high-risk drug, PLT 180→15 i.e. drop 91.7%, onset day 5, recovery day 7 after stop, no extra features): class 4 + drop 4 + window 3 + recovery 3 + features 0 = 14 points (max 14, 100%) → "highly likely", stop the drug permanently at once and record the allergy history.',
 'Do all drugs use this score?',
 'Heparins do not use this tool; the 4Ts score must assess HIT separately (heparin-induced thrombosis risk is special and thrombosis can occur even without very low PLT); other drugs can use this weighting for a causal first judgement.',
 'Why does a ≥80% drop weigh most?',
 'A rapid platelet plunge over a short time (especially with bleeding) best supports a drug-destruction mechanism; a slow small drop is more likely from the underlying disease or other factors, so drop magnitude is a core clue to causality.',
 'About the Drug-Induced (ITP) Risk Score',
 'A drug-induced immune thrombocytopenia (DITP) risk assessment tool: it scores comprehensively from multi-dimensional factors — drug class, platelet drop magnitude, onset and recovery time windows, clinical features — to judge the causal link between the drug and thrombocytopenia.',
 'Drug class risk grading assessment',
 'Platelet dynamic time-window analysis',
 '8-item clinical feature weighted scoring',
 'DITP possibility grading and handling advice',
 'Post-dosing thrombocytopenia cause investigation',
 'Drug-induced ITP causality judgement',
 'Stopping-decision aid',
 'Drug allergy history record reference',
 'e.g. quinine / sulphonamides / heparin',
]

B['thrombin-generation'] = [
 '🩸 Thrombin Generation (TG) Curve Analyzer',
 'Enters thrombin generation assay parameters and analyses overall haemostasis and thrombotic tendency.',
 '"Enters thrombin generation assay parameters and analyses overall haemostasis and thrombotic tendency" is computed from the input parameters and the result is output.',
 'Thrombin Generation TG Curve Analyzer',
 '/ Thrombin Generation Analysis',
 '📖 Read the "Thrombin Generation (TG) Curve Analyzer Usage Guide"',
 'Parameter analysis',
 'Curve plotting',
 'Lag Time, delay (min) 1-5',
 'Peak, peak value (nM) 100-400',
 'ttPeak, time to peak (min) 4-10',
 'ETP, endogenous thrombin potential (nM·min) 800-1800',
 'Start Tail, tail start time (min) 15-30',
 'Trigger',
 'Low TF (1 pM) - overall coagulation',
 'High TF (5 pM) - extrinsic pathway',
 '📋 TG parameter clinical meaning',
 'Decrease suggests',
 'Coagulation factor deficiency, anticoagulation',
 'Hypercoagulable tendency',
 'Hypercoagulable state',
 'Coagulation factor deficiency',
 'Coagulation delay',
 'Thrombosis risk',
 'Bleeding risk / anticoagulation effect',
 'Active anticoagulant proteins',
 '📊 Clinical application scenarios',
 'Haemophilia assessment',
 ': Peak and ETP lowered, can guide individualized replacement therapy',
 'Anticoagulation monitoring',
 ': warfarin / DOACs lower ETP, more comprehensive than routine coagulation',
 'Thrombosis risk assessment',
 ': raised ETP correlates with VTE risk',
 'Liver disease coagulation assessment',
 ': reflects the overall procoagulant-anticoagulant balance',
 'Surgical bleeding prediction',
 ': supplements the gaps of routine coagulation tests',
 'Note: the TG assay (e.g. CAT method) is the most comprehensive way to assess overall coagulation, reflecting the combined action of procoagulant and anticoagulant systems. Normal values vary by laboratory and reagent, so follow each lab reference range. For study reference only.',
 '📚 Deep Dive: Thrombin Generation (TG) Curve Analyzer',
 'Enter the four TGA parameters (Lag / Peak / ttPeak / ETP) to judge hyper- or hypocoagulable tendency.',
 'In haemophilia, use ETP / Peak to assess whether factor replacement is sufficient.',
 'For thrombosis risk, see whether Peak and ETP are raised.',
 'TGA reading: Lag time normal 1-5 min (shortening suggests fast hypercoagulable start); Peak normal 100-400 nM (>400 hypercoagulable, <100 hypocoagulable / bleeding); ttPeak normal 4-10 min; ETP normal 800-1800 nM·min (>1800 too much total thrombin, <800 insufficient). Combine the four to set the "hypercoagulable / hypocoagulable / normal" tendency.',
 'Example (Lag=3 min, Peak=180 nM, ttPeak=6.5 min, ETP=1200 nM·min): all four normal → balanced coagulation. Contrast: Peak=450 nM, ETP=2000 nM·min → Peak and ETP raised → hypercoagulable tendency (increased thrombosis risk), combine with D-dimer / anticoagulant proteins.',
 'Does low ETP always mean bleeding?',
 'Low ETP suggests insufficient total thrombin generation, seen in haemophilia, anticoagulation or liver disease; but combine with Peak and clinical bleeding, a single low ETP does not equal active bleeding, and haemophilia can adjust replacement by ETP target.',
 'Can TGA replace routine coagulation screening?',
 'No replacement; they complement. TGA gives a "total thrombin amount" view and is more sensitive to hypercoagulable state and replacement sufficiency; routine PT/APTT see the initiation phase. Reading must combine clinical context and standardised reference ranges.',
 'About the Thrombin Generation TG Curve Analyzer',
 'A thrombin generation TG curve analyzer: it reads thrombin generation assay parameters (lag time, peak, ETP, ttPeak, startTail) and assesses overall coagulation. A professional medical tool based on authoritative medical standards, for reference only.',
]

for s, lst in B.items():
    write(s, build(s, lst))

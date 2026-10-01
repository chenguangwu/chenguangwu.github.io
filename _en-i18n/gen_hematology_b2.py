#!/usr/bin/env python3
# gen_hematology_b2.py — hematology b2 (5 slugs): cml-monitoring/coagulation-factor/detector-5/dic-scoring/generator-analysis
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

B['cml-monitoring'] = [
 '⚙️ CML BCR-ABL Ratio Monitor',
 'It assesses the response to TKI therapy (based on the ELN 2020 criteria) and tracks the trend of the molecular response.',
 'It assesses the response to TKI therapy (based on the ELN 2020 criteria) and tracks the trend of the molecular response, running a professional calculation on the input parameters and outputting the result.',
 'CML BCR-ABL ratio monitor',
 '/ CML BCR-ABL Monitoring',
 '📖 Read the "CML BCR-ABL Ratio Monitor Usage Guide"',
 'Months of treatment',
 'Transcript type',
 'p210 (e13a2/e14a2, the major type)',
 'p190 (e1a2, rare)',
 'p230 (e19a2, rare)',
 '+ Add a tracking record',
 'View the trend',
 '📈 BCR-ABL tracking trend',
 '📋 ELN 2020 treatment response milestones (p210)',
 'Optimal response',
 'BCR-ABL of 1% or less, or Ph+ of 35% or less',
 'BCR-ABL above 10%, or Ph+ above 95%',
 'BCR-ABL of 0.1% or less, or Ph+ 0%',
 'BCR-ABL above 1%, or Ph+ above 0%',
 '12 months',
 'BCR-ABL of 0.1% or less (MMR maintained)',
 'BCR-ABL above 1%, mutation, or CML progression',
 '📊 Definitions of the molecular response',
 'Response level',
 'CCyR (complete cytogenetic response)',
 'Ph chromosome = 0%',
 'MMR (major molecular response)',
 'Transcript reduced by at least 3 logs',
 'Reduced by at least 4 logs',
 'Reduced by at least 4.5 logs',
 'DMR (deep molecular response)',
 'MR4 or deeper, the precondition for stopping treatment',
 'Note: BCR-ABL on the international scale must be calibrated by the laboratory conversion factor. Maintaining DMR (MR4 or deeper) for at least 2 years is the precondition for attempting treatment-free remission (TFR). For clinical reference only.',
 '📚 Deep Dive: CML BCR-ABL Ratio Monitor',
 'Grade the BCR-ABL international scale molecular response during TKI therapy under the ELN 2020 criteria.',
 'Read the treatment response as optimal, warning or failure against the number of months on treatment.',
 'Once a deep response is reached (MR4 or deeper for at least 2 years), assess whether the conditions for treatment-free remission (TFR) are met.',
 'BCR-ABL international scale levels: 0.0032% or less is MR4.5, 0.01% or less is MR4/DMR, 0.1% or less is MMR, 1% or less is the CCyR range, 10% or less means CCyR not reached, and above 10% is high risk. Time-dependent response (ELN 2020): 1% or less at 3 months, 0.1% or less at 6 and 12 months; missing the matching threshold is graded as warning or treatment failure.',
 'Example (12 months of treatment, BCR-ABL international scale = 0.5%): the level is the CCyR range (0.1 < 0.5 ≤ 1); the 12-month target is 0.1% or less and 0.5% is above it, so the response is a warning, calling for a review of adherence and resistance and shorter monitoring intervals. Another example (6 months, 0.05%): the level is MMR and the 6-month target of 0.1% or less is met, so the response is optimal.',
 'What unit is BCR-ABL on the international scale?',
 'IS stands for International Scale, which calibrates results from different laboratories to a common standard in percent. It removes platform differences so results can be compared across centres; always state IS on the reading and in the report.',
 'Are MR4 and DMR the same?',
 'MR4 means 0.01% or less, a 4-log reduction from baseline, while DMR (deep molecular response) usually means MR4 or deeper such as MR4.5. Patients who keep MR4 or deeper for at least 2 years and meet the other conditions can be assessed for TFR, stopping treatment under observation.',
 'About the CML BCR-ABL Ratio Monitor',
 'A BCR-ABL monitor for chronic myeloid leukaemia (CML): enter the BCR-ABL/ABL transcript ratio and it grades the treatment response as optimal, warning or failure and tracks the molecular response trend. A professional medical tool based on authoritative medical standards, for reference only.',
]

B['coagulation-factor'] = [
 '🩸 Coagulation Factor Activity and Inhibitor Calculator',
 'It supports factor activity assessment, Bethesda inhibitor titre calculation and recovery analysis.',
 'It supports factor activity assessment, Bethesda inhibitor titre calculation and recovery analysis, running a professional calculation on the input parameters and outputting the result.',
 '/ Coagulation Factor Calculator',
 '📖 Read the "Coagulation Factor Activity and Inhibitor Calculator Usage Guide"',
 'Factor activity assessment',
 'Bethesda inhibitor',
 'Recovery calculation',
 'FVIII (reference 50-150%)',
 'FIX (reference 50-150%)',
 'FXI (reference 70-120%)',
 'FXII (reference 50-150%)',
 'FVII (reference 55-170%)',
 'FX (reference 70-120%)',
 'Factor activity (%)',
 'Bethesda method: after 2 hours of incubation at 37 °C the residual factor activity is measured; 1 BU is the amount of inhibitor that lowers factor activity by 50%.',
 'Residual activity in patient plasma (%)',
 'Calculate the titre',
 'Recovery = (activity after infusion - activity before infusion) / expected rise × 100%',
 'FVIII (1 IU/kg raises activity by 2%)',
 'FIX (1 IU/kg raises activity by 1%)',
 'Infusion dose (IU)',
 'Activity before infusion (%)',
 'Activity 15 min after infusion (%)',
 'Calculate recovery',
 '📋 Grading of haemophilia severity',
 'FVIII/FIX activity',
 'Severe',
 'Spontaneous bleeding (joints, muscles, internal organs)',
 'Bleeding after injury or surgery',
 'Mild',
 'Bleeding after injury or major surgery',
 'Bleeding only after severe trauma or major surgery',
 '📊 Clinical meaning of the inhibitor titre',
 'Titre',
 'Low responder',
 'Increasing the factor dose can reach therapeutic levels',
 'High responder',
 'Bypassing agents are needed (rFVIIa/APCC)',
 'High-titre inhibitor',
 'Immune tolerance induction (ITI) therapy',
 'Note: recovery below 66% suggests an inhibitor. The half-life of FVIII is about 8-12 hours and that of FIX about 18-24 hours. For study reference only; it cannot replace clinical decisions.',
 '📚 Deep Dive: Coagulation Factor Activity and Inhibitor Calculator',
 'In haemophilia, grade the severity from the activity of FVIII or FIX',
 'as severe, moderate or mild and set the target for replacement therapy.',
 'Use the Bethesda method to derive the inhibitor titre in BU/mL and separate low responders, high responders and high-titre cases.',
 'Use recovery (actual rise divided by expected rise) to judge whether an inhibitor is present.',
 'Activity grading: FVIII/FIX below 1% severe, below 5% moderate, below 40% mild and 40% or more subclinical. Inhibitor Bethesda BU/mL = (−ln(residual activity fraction)/ln2) × dilution factor, where the residual activity fraction is the residual percentage divided by 100. Recovery (%) = (activity after − activity before infusion) / (IU/kg × the rise per IU/kg, 2% for FVIII and 1% for FIX) × 100; 66% or more is normal, 50–66% low and below 50% suggests an inhibitor.',
 'Example 1 (inhibitor: residual activity 25%, dilution 1:1): BU = (−ln 0.25/ln 2) × 1 = 2.0 BU/mL, a low responder. Example 2 (recovery: body weight 70 kg, FVIII 1400 IU, 1% before and 35% after infusion): IU/kg = 20, expected rise = 20 × 2% = 40%, actual rise 34%, so recovery = 34/40 × 100 = 85%, which is normal with no evidence of an inhibitor.',
 'How do the Bethesda and Nijmegen methods differ?',
 'Classic Bethesda incubates at 37 °C for 2 hours and measures residual activity; the modified Nijmegen method uses a buffered system and room-temperature incubation, which is more sensitive and less time dependent. Both report in BU/mL, but the results are not directly interchangeable, so the method must be stated.',
 'Why does each IU/kg of FVIII raise activity by about 2%?',
 'It is an empirical conversion: 1 IU/kg of FVIII raises circulating activity by about 2% because',
 'the half-life is short and the volume of distribution large, while FIX gives about 1% because it distributes differently between the intravascular and extravascular pools. Actual recovery is affected by blood group, inhibitors and blood volume, and varies widely between individuals.',
 'About the Coagulation Factor Activity and Inhibitor Calculator',
 'A coagulation factor activity and inhibitor calculator: it supports FVIII and FIX activity measurement, Bethesda inhibitor titre calculation, mixing study interpretation and recovery calculation. A professional medical tool based on authoritative medical standards, for reference only.',
]

B['detector-5'] = [
 '🔍 PNH Testing by Flow Cytometry for CD55/CD59',
 'Interpretation of paroxysmal nocturnal haemoglobinuria (PNH) flow cytometry results and assessment of clone size.',
 'Interpretation of paroxysmal nocturnal haemoglobinuria (PNH) flow cytometry results and assessment of clone size, running a professional calculation on the input parameters and outputting the result.',
 '/ PNH flow cytometry for CD55/CD59',
 '📖 Read the "PNH Flow Cytometry for CD55/CD59 Usage Guide"',
 'Flow cytometry results',
 'Total granulocyte clone with CD59 loss (%)',
 'Total granulocyte clone with CD55 loss (%)',
 'Red cell clone with CD59 loss (%)',
 'Monocyte clone with CD59 loss (%)',
 'PNH clone typing (granulocytes)',
 'Type II clone with partial loss (%)',
 'Type III clone with complete loss (%)',
 'LDH (lactate dehydrogenase, U/L)',
 'Interpret the results',
 'PNH clone typing: type I is normal expression, type II partial loss (weak CD55/CD59 expression) and type III complete loss.',
 'Granulocyte clone size is the best indicator for judging PNH severity and the risk of hemolysis.',
 'FLAER testing is superior to CD55/CD59, so use FLAER where available.',
 'The results are for reference only, and specific diagnosis and treatment must be decided by a haematologist.',
 '📚 Deep Dive: PNH Flow Cytometry for CD55/CD59',
 'When flow cytometry shows a population lacking CD55/CD59, type it by granulocyte clone size and judge the clinical significance.',
 'Combine LDH, Hb and a history of thrombosis to assess the hemolytic burden and the indications for treatment.',
 'Separate large clones (50% or more), significant clones (10–50%) and small clones (1–10%) to decide on complement inhibition.',
 'Clone typing: type I normal plus type II (partial loss) plus type III (complete loss) = 100%, and the total PNH clone = type II + type III. Grading: 50% or more a large clone, 10–50% clinically significant, 1–10% small and below 1% subclinical. Type III cells are the most complement sensitive and the main source of hemolysis; LDH above 250 indicates active hemolysis and above 500 a marked rise.',
 'Example (type II = 10%, type III = 25%, LDH = 450, Hb = 85): total clone = 10 + 25 = 35%, a clinically significant PNH clone, and type I = 100 − 35 = 65%; type III at 25%, which is at least 20%, means a high hemolysis risk, and LDH 450 is a mild to moderate rise with Hb 85 indicating moderate anemia. Taken together, complement inhibitor treatment should be assessed.',
 'Why look at the granulocyte clone rather than red cells?',
 'Granulocytes are short lived and not diluted by transfusion, so the FLAER or granulocyte clone is the most reliable; red cell CD55/CD59 is diluted by transfused normal red cells and often underestimates the true PNH clone, so the granulocyte line is taken as standard.',
 'Does a small clone (below 10%) need treatment?',
 'Usually no PNH-targeted therapy is needed; the focus is on checking for coexisting aplastic anemia (AA/PNH syndrome) and monitoring clone evolution regularly, intervening if cytopenias appear or the clone grows.',
 'About PNH Testing by Flow Cytometry for CD55/CD59',
 'An interpretation tool for paroxysmal nocturnal haemoglobinuria (PNH) flow cytometry: from the proportion of CD55/CD59-deficient clones it assigns type I, II and III, assesses PNH clone size and hemolysis risk, and gives advice on anti-complement therapy.',
 'CD55/CD59 clone analysis across cell lines',
 'Type I, II and III clone typing',
 'Assessment of hemolysis and thrombosis risk',
 'Judging the indications for anti-C5 complement inhibitor therapy',
 'Interpreting PNH flow cytometry reports',
 'Screening for PNH clones in aplastic anemia and MDS patients',
 'Monitoring the evolution of the PNH clone',
 'Assessing the response to anti-complement therapy',
]

B['dic-scoring'] = [
 '📋 DIC Scoring Tool for Disseminated Intravascular Coagulation (ISTH)',
 'Based on the ISTH overt DIC scoring system, for assessing a DIC diagnosis in patients with an underlying disorder.',
 'DIC scoring tool for disseminated intravascular coagulation (ISTH)',
 '/ DIC Scoring Tool',
 '📖 Read the "DIC Disseminated Intravascular Coagulation ISTH Scoring Tool Usage Guide"',
 'ISTH overt DIC score = platelet score (below 50 adds 2, 50 to 100 adds 1, at least 100 adds 0) + D-dimer score (above 10 adds 3, 2.5 to 10 adds 2, below 2.5 adds 0) + PT prolongation score (more than 6 seconds adds 2, 3 to 6 seconds adds 1) + fibrinogen score (below 1 g/L adds 1); a total of 5 or more meets overt DIC.',
 'D-dimer (mg/L FEU)',
 'PT prolongation (seconds versus the normal control)',
 'An underlying disorder that can trigger DIC is present',
 '📋 ISTH overt DIC scoring criteria',
 'D-dimer (mg/L)',
 'No rise',
 'Mild rise',
 'Moderate rise (5-10 times)',
 'Marked rise (more than 10 times)',
 'PT prolongation (seconds)',
 'No prolongation',
 'A total of 5 or more suggests overt DIC; below 5 suggests non-overt DIC and needs dynamic monitoring. Precondition: an underlying disorder that can trigger DIC must be present.',
 '📊 Common triggers of DIC',
 'Infection: sepsis, most often with Gram-negative bacteria',
 'Obstetric: amniotic fluid embolism, placental abruption, HELLP syndrome',
 'Trauma: severe trauma, burns, crush injury',
 'Malignancy: solid tumours and leukaemia, APL being the most typical',
 'Vascular abnormalities: giant haemangioma, aortic aneurysm',
 'Severe allergy or poisoning: snake bite, transfusion reactions',
 'Note: for D-dimer, a mild rise is taken as below 1 mg/L, moderate as 5-10 mg/L and marked as above 10 mg/L. A positive 3P test can support the diagnosis but is no longer an ISTH scoring item. For clinical reference only.',
 '📚 Deep Dive: DIC Disseminated Intravascular Coagulation ISTH Scoring Tool',
 'Apply the ISTH overt score in patients with a DIC-predisposing disorder such as infection, trauma, malignancy or an obstetric emergency.',
 'Add up the four items: platelets, D-dimer, PT prolongation and fibrinogen.',
 'A score of 5 or more starts comprehensive treatment for overt DIC; 3–4 is non-overt and should be repeated in 8–12 hours.',
 'ISTH overt DIC score: platelets below 50 (+2) or 50–100 (+1); D-dimer above 10 (+3), 5–10 (+2) or above 1 (+1); PT prolongation above 6 s (+2) or 3–6 s (+1); fibrinogen below 1.0 (+1). Precondition: an underlying disorder that can trigger DIC must be present; a total of 5 or more is overt DIC, 3–4 non-overt and below 3 does not support it.',
 'Example (platelets = 45, D-dimer = 8.5, PT prolongation = 6 s, fibrinogen = 1.2): platelets below 50 (+2), D-dimer 5–10 (+2), PT 3–6 s (+1) and fibrinogen at least 1.0 (+0) gives a total of 5, reaching the overt DIC threshold, so treat the underlying disease at once and give replacement and anticoagulation.',
 'How do the ISTH and JAAM scores differ?',
 'ISTH confirms overt DIC, requiring an existing underlying disease plus signs of SIRS, while JAAM from Japan focuses on early screening for preclinical or non-overt DIC, with higher sensitivity and slightly lower specificity; the two suit different settings.',
 'Is a score below 5 safe?',
 'No. Non-overt DIC (3–4 points) still carries a risk of progression and should be reassessed every 8–12 hours; when the underlying disease is severe or clinical suspicion is high, do not wait for the full score before intervening.',
 'About the DIC Disseminated Intravascular Coagulation ISTH Scoring Tool',
 'A DIC scoring tool for disseminated intravascular coagulation (ISTH): it scores the DIC diagnosis from the platelet count, PT prolongation, fibrinogen and D-dimer or FDP. A professional medical tool based on authoritative medical standards, for reference only.',
]

B['generator-analysis'] = [
 '🩸 Thrombin Generation (TG) Curve Analysis',
 '📖 Read the "Thrombin Generation (TG) Curve Analysis Usage Guide"',
 'The thrombin generation curve is measured by the fluorogenic substrate method and gives these parameters: lag time, thrombin peak, time to peak (ttPeak) and the endogenous thrombin potential (ETP, the area under the curve); ETP = the sum of the thrombin concentration at each time point × the sampling interval. The curve is derived from the fluorescence intensity after tissue factor triggers plasma, then normalized and corrected.',
 '📚 Deep Dive: Thrombin Generation (TG) Curve Analysis',
 'Enter the TGA parameters (lag time, peak, ttPeak, ETP, start tail) to assess the overall haemostatic phenotype.',
 'For a hypercoagulable or thrombotic tendency, see whether peak and ETP are raised; for a bleeding tendency, see whether they are low.',
 'In haemophilia, factor replacement can be individualized from TGA to check whether thrombin generation is adequate.',
 'Key parameters of the thrombin generation assay (TGA): lag time, the delay before thrombin starts, normally about 1–5 min; peak, the thrombin burst, normally about 100–400 nM; ttPeak, the time to peak, about 4–10 min; ETP, the endogenous thrombin potential, normally about 800–1800 nM·min; and start tail, which reflects anticoagulant inactivation. The four are read together, since looking at one alone easily misleads.',
 'Example (lag = 3 min, peak = 180 nM, ttPeak = 6.5 min, ETP = 1200 nM·min): all four fall in the normal range, so coagulation is balanced. By contrast, peak = 450 nM and ETP = 2000 nM·min means peak and ETP are raised, a hypercoagulable or thrombotic tendency that should be assessed together with D-dimer and the anticoagulant proteins.',
 'How does TGA differ from routine coagulation tests?',
 'Routine PT and APTT only look at the initiation phase, while TGA reflects the whole course of thrombin generation from initiation through the peak to inactivation, as ETP. It is more sensitive to a hypercoagulable state and to whether factor replacement is sufficient, but standardization and reference ranges vary widely with reagent and instrument.',
 'Which matters more, peak or ETP?',
 'Peak reflects the instantaneous burst and ties more closely to thrombosis, while ETP reflects the total amount generated and ties more closely to whether haemostasis is adequate. Replacement therapy in haemophilia usually aims to bring ETP and peak above the lower limit of normal, though the target depends on the centre and the protocol.',
 'About Thrombin Generation (TG) Curve Analysis',
 'A thrombin generation (TG) curve analysis. A free online tool that runs entirely in the browser: data is never uploaded, so your privacy stays safe.',
 'Plot the thrombin generation curve against tissue factor concentration and time, and read off the peak concentration, lag time, time to peak and ETP',
 'Assess the anticoagulation to haemostasis balance: too high a peak suggests thrombosis risk and too low a bleeding tendency',
 'Monitor how anticoagulant drugs (heparin, direct oral anticoagulants) affect thrombin generation parameters',
 'Interpret acquired thrombophilia together with lupus anticoagulant and protein C or S deficiency',
]

for s, lst in B.items():
    write(s, build(s, lst))

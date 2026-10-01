#!/usr/bin/env python3
# gen_hematology_b1.py — hematology b1 (5 slugs): anemia-classification/anemia-differential/aps-diagnosis/calc-1/cd34-count
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

B['anemia-classification'] = [
 '🩸 Anemia MCV/MCH/MCHC Morphological Classifier',
 'Enter the red blood cell parameters and it computes the red cell indices and classifies the anemia morphologically.',
 'Core formulas (by input variables): hgb×100÷hct; hgb×10÷rbc; hct×10÷rbc',
 'Anemia MCV/MCH/MCHC Morphological Classifier',
 '/ Anemia Morphological Classifier',
 '📖 Read the "Anemia MCV/MCH/MCHC Morphological Classifier Usage Guide"',
 'Calculated from RBC, HGB and HCT',
 'Enter MCV, MCH and MCHC directly',
 'Haemoglobin HGB (g/L)',
 'Red blood cell count RBC (×10¹²/L)',
 'Haematocrit HCT (%)',
 'MCV (fL), reference 80-100',
 'MCH (pg), reference 27-34',
 'MCHC (g/L), reference 320-360',
 'Male (normal HGB at least 120)',
 'Female (normal HGB at least 110)',
 '📋 Reference table for the morphological classification of anemia',
 'Macrocytic anemia',
 'Megaloblastic anemia, liver disease, MDS',
 'Normocytic normochromic',
 'Aplastic anemia, acute blood loss, hemolysis',
 'Microcytic normochromic',
 'Mild thalassemia, anemia of chronic disease',
 'Microcytic hypochromic',
 'Iron deficiency anemia, thalassemia',
 '📊 Grading of anemia severity (HGB g/L)',
 'Note: MCV = HCT(%) × 10 / RBC; MCH = HGB(g/L) × 10 / RBC; MCHC = HGB(g/L) × 100 / HCT(%). This tool is for study reference only and cannot replace a clinical diagnosis.',
 '📚 Deep Dive: Anemia MCV/MCH/MCHC Morphological Classifier',
 'With RBC, HGB and HCT known, first grade the severity of the anemia (by the sex-specific HGB threshold), then make the morphological classification.',
 'Microcytic, macrocytic and hypochromic clues: use the three red cell indices MCV, MCH and MCHC to locate the anemia type.',
 'Combine iron studies, vitamin B12 and folate, and reticulocytes to separate iron deficiency, megaloblastic and hemolytic causes.',
 'Red cell indices (standard formulas): MCV (fL) = HCT(%) × 10 / RBC (×10¹²/L); MCH (pg) = HGB(g/L) / RBC (×10¹²/L); MCHC (g/L) = HGB(g/L) × 100 / HCT(%). Reference ranges: MCV 80–100 fL, MCH 27–34 pg, MCHC 320–360 g/L. Morphological classification: MCV below 80 is microcytic and above 100 macrocytic, while low MCH and MCHC indicate hypochromia.',
 'Example (HGB = 85 g/L, RBC = 3.5×10¹²/L, HCT = 27%): MCV = 27 × 10/3.5 = 77.1 fL (low, microcytic), MCH = 85/3.5 = 24.3 pg (low) and MCHC = 85 × 100/27 = 314.8 g/L (low). With all three low it is microcytic hypochromic anemia, most often caused by iron deficiency; confirm with serum iron, ferritin and total iron-binding capacity.',
 'Does a normal MCV rule out iron deficiency?',
 'Not necessarily. In early iron deficiency, or when it coexists with anemia of chronic disease, MCV can still be normal (normocytic); a raised RDW (anisocytosis) is often the earlier signal, so read it together with the iron studies.',
 'Which is more sensitive, MCH or MCHC?',
 'A low MCHC appears later but is more specific, while a low MCH appears earlier. When both are low along with MCV, the call of hypochromic microcytic anemia is fairly reliable. This tool only performs',
 'index calculation',
 ', and a diagnosis must combine iron studies and other tests.',
 'About the Anemia MCV/MCH/MCHC Morphological Classifier',
 'An anemia morphology classifier: from the red cell count, haemoglobin and haematocrit it derives MCV, MCH and MCHC and classifies the anemia morphologically, supporting the differentiation of normocytic, macrocytic and microcytic hypochromic anemia. A professional medical tool based on authoritative medical standards, for reference only.',
]

B['anemia-differential'] = [
 '🔬 Laboratory Differentiator for Iron Deficiency, Megaloblastic and Hemolytic Anemia',
 'Enter the laboratory values and it assesses which anemia type they point to (you may fill in only the items you have).',
 'Core formula (by input variables): siron÷tibc×100',
 '/ Anemia Laboratory Differentiator',
 '📖 Read the "Iron Deficiency / Megaloblastic / Hemolytic Anemia Laboratory Differentiator Usage Guide"',
 'Basic indices',
 'Reticulocyte percentage (0.5-1.5)',
 'Iron studies',
 'Serum iron (μmol/L)',
 'Total iron-binding capacity TIBC (μmol/L)',
 'Megaloblastic anemia indices',
 'Vitamin B12 (pmol/L)',
 'Folate (nmol/L)',
 'Hemolysis indices',
 'Haptoglobin (g/L)',
 '📋 Comparison of laboratory features across the three anemia types',
 'Iron deficiency anemia',
 'Megaloblastic anemia',
 'Hemolytic anemia',
 'Reticulocytes',
 'Normal or low',
 'Serum ferritin',
 'Transferrin saturation',
 'Vitamin B12',
 'Folate',
 'Raised (indirect)',
 'Haptoglobin',
 'Note: this tool gives a tendency assessment from common laboratory indices; the final diagnosis must combine bone marrow aspiration, a peripheral blood smear and other tests. For study reference only.',
 '📚 Deep Dive: Iron Deficiency / Megaloblastic / Hemolytic Anemia Laboratory Differentiator',
 'Given a set of anemia-related laboratory values, quickly see how strongly the evidence supports each of the three categories: iron deficiency, megaloblastic and hemolytic.',
 'Single-variable sensitivity: hold the other indices fixed and change only MCV or LDH to watch how the classification tendency shifts.',
 'The tendency score only ranks a screen; the final diagnosis rests on bone marrow, iron studies and hemolysis evidence.',
 'Weighted scoring: points are added for iron deficiency (MCV low, ferritin below 15 or below 30, transferrin saturation TSAT below 15%, TIBC raised), for megaloblastic anemia (MCV above 100, B12 below 148 pmol/L, folate below 7 nmol/L, LDH above 500) and for hemolysis (reticulocytes above 2%, LDH above 400, bilirubin above 20, haptoglobin below 0.3); the totals are ranked to give a tendency score.',
 'Example (MCV = 72, ferritin = 8, serum iron = 6, TIBC = 75, B12 = 200, folate = 10, LDH = 250, bilirubin = 12, haptoglobin = 1.0, reticulocytes = 1.2): TSAT = 6/75 × 100 = 8%, below 15; the iron deficiency items add to 3 (MCV) + 4 (ferritin below 15) + 2 (ferritin below 30) + 3 (TSAT) + 2 (TIBC) = 14 points, with 0 for megaloblastic and 0 for hemolytic. A total of 14 points means a strong tendency to iron deficiency anemia.',
 'Does a high score definitely mean that disease?',
 'No. The score only quantifies and ranks several pieces of laboratory evidence to show how likely each is; ferritin, for example, can rise falsely with inflammation or liver disease, so it must be read with the clinical picture. Confirming iron deficiency requires absent marrow stainable iron or a markedly low ferritin.',
 'Can transfusion distort the indices?',
 'Yes. Transfusion raises HGB and masks the anemia morphology, and changes the relative meaning of the reticulocyte count; hemolysis markers such as LDH, bilirubin and haptoglobin may also change around transfusion, so interpret them against the timing of sampling.',
 'About the Iron Deficiency / Megaloblastic / Hemolytic Anemia Laboratory Differentiator',
 'An anemia laboratory differentiator: using MCV, reticulocytes, iron studies, vitamin B12, folate, LDH and bilirubin it separates iron deficiency anemia, megaloblastic anemia and hemolytic anemia. A professional medical tool based on authoritative medical standards, for reference only.',
]

B['aps-diagnosis'] = [
 '🔍 Antiphospholipid Syndrome (APS) Diagnostic Criteria Tool',
 'Based on the revised Sydney 2006 classification criteria, it evaluates an APS diagnosis; at least one clinical and one laboratory criterion are needed.',
 'Antiphospholipid antibody APS diagnostic criteria tool',
 '/ APS Diagnostic Tool',
 '📖 Read the "Antiphospholipid Syndrome (APS) Diagnostic Criteria Tool Usage Guide"',
 'Clinical criteria',
 '1. Vascular thrombosis',
 'Arterial thrombosis (stroke, myocardial infarction, limb ischaemia and so on)',
 'Venous thrombosis (DVT, PE, splanchnic vein thrombosis and so on)',
 'Microvascular thrombosis',
 '2. Pathological pregnancy',
 'Unexplained fetal death at or beyond 10 weeks of gestation with normal morphology',
 'Preterm birth before 34 weeks for eclampsia, severe pre-eclampsia or placental insufficiency',
 'Three or more consecutive unexplained miscarriages before 10 weeks',
 'Laboratory criteria (two positive results at least 12 weeks apart)',
 'Lupus anticoagulant (LA) positive',
 'aCL IgG positive at medium or high titre (>40 GPL)',
 'aCL IgM positive at medium or high titre (>40 MPL)',
 'Anti-β2-GPI IgG positive',
 'Anti-β2-GPI IgM positive',
 'The two positive results are at least 12 weeks apart',
 'Testing done within 5 years before or after the clinical event',
 '📋 Key points of the Sydney 2006 APS classification criteria',
 'At least',
 'one clinical criterion',
 'one laboratory criterion',
 'is required to classify a case as APS',
 'Timing requirements for laboratory testing',
 'Two positive results, at least 12 weeks apart',
 'Testing must be done within 5 years before or after the clinical event',
 'Positive results from more than 5 years ago do not count',
 'APS classification',
 'Primary APS',
 ': no underlying autoimmune disease',
 'Secondary APS',
 ': with SLE or another autoimmune disease',
 'Catastrophic APS',
 ': multi-organ thrombosis within a short period, with high mortality',
 'Note: LA is the most specific laboratory marker. Only medium or high titres of aCL or anti-β2-GPI are meaningful, and a low-titre aCL positive does not meet the criteria. For study reference only; it cannot replace a clinical diagnosis.',
 '📚 Deep Dive: Antiphospholipid Syndrome (APS) Diagnostic Criteria Tool',
 'From the clinical event (thrombosis or pathological pregnancy) plus the laboratory antibodies, judge whether both sets of criteria are met.',
 'Check whether antibody testing satisfies the timing requirement of two positive results at least 12 weeks apart.',
 'Separate thrombotic from obstetric APS and give the matching anticoagulation strategy for reference.',
 'Revised Sydney 2006 criteria: at least one clinical plus one laboratory criterion. Clinical criteria: arterial, venous or microvascular thrombosis, or pathological pregnancy (fetal death at or beyond 10 weeks, preterm birth before 34 weeks for eclampsia or placental insufficiency, or three or more consecutive early miscarriages). Laboratory criteria: LA positive, or aCL IgG/IgM at medium or high titre, or anti-β2-GPI IgG/IgM positive, with two positive results at least 12 weeks apart and within 5 years.',
 'Example (venous thrombosis positive plus LA positive plus two confirmatory tests at least 12 weeks apart and within 5 years): the clinical criterion is met, the laboratory criterion is met and the timing is compliant, so the case meets the APS classification criteria, and long-term anticoagulation with rheumatology follow-up is advised. With only one positive antibody result (less than 12 weeks apart) it is judged possible APS, needing confirmation on repeat testing.',
 'Can a single positive antibody test diagnose APS?',
 'No. Antiphospholipid antibodies can be transiently positive because of infection or drugs, so the criteria require two positive results at least 12 weeks apart and within 5 years to exclude false positives.',
 'Does a positive antibody without thrombosis or pregnancy events count as APS?',
 'No. A matching clinical event is needed to meet the criteria; those with laboratory evidence alone are advised to be followed up and some may be regarded as antiphospholipid antibody carriers, without starting long-term anticoagulation.',
 'About the Antiphospholipid Antibody APS Diagnostic Criteria Tool',
 'An antiphospholipid syndrome (APS) diagnostic criteria tool based on the revised Sydney 2006 classification criteria: it evaluates the clinical and laboratory criteria to support an APS diagnosis. A professional medical tool based on authoritative medical standards, for reference only.',
]

B['calc-1'] = [
 '🩸 Anemia MCV/RDW Classification',
 'A preliminary morphological classification of anemia from the mean corpuscular volume (MCV) and the red cell distribution width (RDW), using the Bessman classification.',
 '📖 Read the "Anemia MCV/RDW Classification Usage Guide"',
 'The Bessman classification combines MCV and RDW: MCV below 80 fL is microcytic, 80 to 100 fL normocytic and above 100 fL macrocytic, while an RDW above 14.5% indicates anisocytosis. Microcytic with a raised RDW is usually iron deficiency anemia, normocytic with a raised RDW suggests a mixed anemia, and macrocytic with a raised RDW suggests folate or vitamin B12 deficiency.',
 '📚 Deep Dive: Anemia MCV/RDW Classification',
 'Given MCV and RDW, make the preliminary Bessman morphological classification (microcytic, normocytic or macrocytic combined with homogeneous or heterogeneous).',
 'Use whether RDW exceeds 15% to judge the spread of red cell size and to locate iron deficiency or thalassemia.',
 'Use it as the first screening step for anemia, then target iron studies, haemoglobin electrophoresis, or folate and B12.',
 'Bessman classification: first split by MCV into microcytic (below 80), normocytic (80–100) and macrocytic (above 100); then by RDW (reference 15% or less) into homogeneous or heterogeneous, giving six combinations: microcytic heterogeneous (typical iron deficiency), microcytic homogeneous (thalassemia or chronic disease), normocytic heterogeneous (early iron deficiency or mixed), normocytic homogeneous (acute blood loss or renal anemia), macrocytic heterogeneous (megaloblastic) and macrocytic homogeneous (alcohol, liver disease or drugs).',
 'Example (MCV = 70 fL, RDW = 18%): MCV below 80 means microcytic and RDW of 18%, above 15%, means heterogeneous, so this is microcytic heterogeneous anemia, most often caused by iron deficiency, which can be distinguished from the microcytic homogeneous pattern of thalassemia.',
 'Can MCV and RDW distinguish iron deficiency from thalassemia?',
 'They give a hint: iron deficiency is usually microcytic with a raised RDW (heterogeneous), while typical thalassemia is microcytic with a normal RDW (homogeneous). The overlap is considerable though, and the diagnosis rests on serum iron and ferritin together with haemoglobin electrophoresis or genetic testing.',
 'Why is the RDW reference 15% or less?',
 'RDW reflects the spread of red cell volumes,',
 'and most laboratories set the upper reference limit at about 14–15%; instruments and populations differ slightly, so interpret it against your own laboratory reference interval. This tool is for morphological screening only.',
 'For example 78',
 'For example 16',
]

B['cd34-count'] = [
 '🩸 Peripheral Blood Stem Cell CD34+ Counter',
 'It computes the CD34+ cell dose in peripheral blood and in the collection product, and judges whether the stem cell collection meets the target.',
 'It computes the CD34+ cell dose in peripheral blood and in the collection product and judges whether the stem cell collection meets the target, running a professional calculation on the input parameters and outputting the result.',
 'Peripheral blood stem cell CD34+ counter',
 '/ CD34+ Stem Cell Count',
 '📖 Read the "Peripheral Blood Stem Cell CD34+ Counter Usage Guide"',
 'Peripheral blood CD34+ assessment',
 'CD34+ calculation in the product',
 'Peripheral blood CD34+ cells per μL = (CD34+% × WBC × 10) / 100',
 'Planned blood volume to process (mL)',
 'Expected collection efficiency (%)',
 'CD34+ dose in the product = (CD34+% × WBC × product volume × 10) / (body weight × 100)',
 'Product WBC (×10⁹/L)',
 'Product CD34+ (%)',
 'Product volume (mL)',
 '📋 CD34+ collection targets and interpretation',
 'CD34+ dose (×10⁶/kg)',
 'Supports a double transplant or rapid engraftment',
 'Meets the minimum for a single autologous transplant',
 'Higher risk of delayed engraftment',
 'Collection not advised, continue mobilization',
 '📊 Reference timing for peripheral blood CD34+ collection',
 'Peripheral blood CD34+ (cells/μL)',
 'Ideal conditions for collection',
 'Suitable for collection',
 'Collectable but the yield may be low',
 'Not suitable, continue mobilization',
 'Mobilization regimens for reference',
 'Autologous transplant',
 ': during haematological recovery after chemotherapy, plus G-CSF 5-10 μg/kg a day',
 'Plerixafor',
 ': added when G-CSF mobilization is inadequate, 0.24 mg/kg the night before collection',
 'Allogeneic donor',
 ': G-CSF 10 μg/kg a day for 4-5 days, collecting on day 5',
 'Note: CD34+ counting uses the ISHAGE/ISH gating strategy. Collection efficiency is affected by blood flow rate, separator settings and venous access, and is usually 30-50%. For study reference only.',
 '📚 Deep Dive: Peripheral Blood Stem Cell CD34+ Counter',
 'Judging collection timing after mobilization: check whether the absolute peripheral blood CD34+ count reaches the collection threshold.',
 'Estimate the reinfusion dose (×10⁶/kg) from the product CD34+ percentage, WBC, volume and body weight.',
 'Judge whether the dose meets the requirement for a single or a double autologous transplant (at least 2 or at least 5 ×10⁶/kg).',
 'CD34+/μL = CD34% × WBC (×10⁹/L) × 10 / 100; total CD34+ in the product = CD34+/μL × volume (mL) × 1000; expected yield = total × collection efficiency; dose (×10⁶/kg) = yield / body weight / 10⁶. Timing: a CD34+ count of at least 10/μL is ideal, at least 5/μL suitable, at least 2/μL low, and below 2/μL means mobilization should continue.',
 'Example (peripheral blood CD34% = 0.8, WBC = 25×10⁹/L, blood volume processed = 12000 mL, collection efficiency = 40%, body weight = 70 kg): CD34+/μL = 0.8 × 25 × 10/100 = 2.0/μL; total = 2.0 × 12000 × 1000 = 2.4×10⁷; yield = 2.4×10⁷ × 0.4 = 9.6×10⁶; dose = 9.6×10⁶/70/10⁶ = 0.14×10⁶/kg, which is low, so more collection cycles or stronger mobilization is needed.',
 'Why is a CD34+ count of at least 10 per μL considered ideal?',
 'The higher the absolute peripheral blood CD34+ count, the easier it is to reach the transplant dose in a single collection; clinics often treat 10–20/μL or more as the best collection window, while below 5/μL the yield is low and more cycles are needed.',
 'Where does the threshold of 2×10⁶/kg come from?',
 'It is an empirical threshold from autologous hematopoietic stem cell transplantation: 2×10⁶/kg or more usually engrafts reliably, and 5×10⁶/kg or more allows a double transplant or faster haematopoietic recovery; below that, further collection is needed. In practice the transplant protocol and centre standards govern.',
 'About the Peripheral Blood Stem Cell CD34+ Counter',
 'A peripheral blood stem cell CD34+ counter: from the CD34+ percentage, white cell count, blood volume and body weight it computes the CD34+ collection dose and judges whether the collection meets the target. A professional medical tool based on authoritative medical standards, for reference only.',
]

for s, lst in B.items():
    write(s, build(s, lst))

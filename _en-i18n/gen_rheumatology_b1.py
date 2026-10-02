#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'rheumatology')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'rheumatology')
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
    out = {'slug': slug, 'industry': 'rheumatology', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
#!/usr/bin/env python3

def main():
    # anca-classification (56)
    write('anca-classification', build('anca-classification', [
        "🦴 ANCA (cANCA/pANCA) Classification",
        "Classifies ANCA-associated vasculitis (AAV) by IIF immunofluorescence pattern + ELISA target antigen (MPO/PR3)",
        "/ ANCA Classifier",
        "IIF immunofluorescence pattern",
        "Ethanol-fixed neutrophil IIF",
        "cANCA (cytoplasmic)",
        "pANCA (perinuclear)",
        "Atypical (aANCA)",
        "IIF titer",
        "ELISA target antigen antibody",
        "Anti-PR3 (MPO-ANCA)",
        "Anti-MPO (PR3-ANCA)",
        "ENT involvement (nose/sinus/larynx)",
        "Pulmonary involvement (nodules/cavities/hemorrhage)",
        "Renal involvement (hematuria/proteinuria/rapidly progressive GN)",
        "Cutaneous purpura/ulcer",
        "Neurological involvement",
        "Asthma/eosinophilia",
        "Classification diagnosis",
        "📋 ANCA IIF Pattern vs Target Antigen",
        "IIF pattern",
        "Main target antigen",
        "GPA (Wegener's granulomatosis)",
        "MPA (microscopic polyangiitis), EGPA",
        "aANCA (atypical)",
        "Variable (BPI/lactoferrin etc.)",
        "IBD/PSC/infection/drug",
        "Rare, MPA or GPA-MPO type",
        "Rare, GPA-PR3 type",
        "📊 AAV Three Subtype Comparison",
        "ANCA positivity rate",
        "Mainly cANCA",
        "Mainly pANCA",
        "Mainly PR3",
        "Mainly MPO",
        "ENT",
        "Nodules/cavities",
        "Alveolar hemorrhage",
        "Asthma/eosinophilic infiltrate",
        "++ (necrotizing GN)",
        "+++ (necrotizing GN)",
        "+ (less common)",
        "Eosinophils",
        "Note: 2017 EULAR/ACR emphasizes antigen-specific ELISA (PR3/MPO) over IIF as first-line testing. PR3-ANCA and MPO-ANCA subtyping predicts phenotype and prognosis better than disease classification (GPA/MPA). PR3-ANCA positive: more ENT/pulmonary involvement, higher relapse risk; MPO-ANCA positive: heavier renal involvement, lower relapse risk. ANCA-negative does not exclude AAV (especially EGPA). For clinical reference only.",
        "📚 In-depth: ANCA Classification (GPA/MPA/EGPA)",
        "Titer and organs",
        "Type",
        "PR3 positive, MPO negative, IIF cANCA, high titer (>=1:320), with renal+pulmonary involvement -> supports granulomatosis with polyangiitis (GPA), needs induction remission therapy.",
        "MPA type",
        "MPO positive, PR3 negative, pANCA -> microscopic polyangiitis, mainly renal/pulmonary small-vessel vasculitis.",
        "PR3/MPO significance?",
        "PR3-ANCA mostly corresponds to GPA, MPO-ANCA to MPA/EGPA; titer level suggests activity and relapse risk.",
        "IIF pattern?",
        "cANCA often relates to PR3, pANCA to MPO, but confirmation relies on antigen-specific ELISA.",
        "About the ANCA (cANCA/pANCA) Classifier",
        "ANCA (cANCA/pANCA) classifier, classifies ANCA-associated vasculitis by immunofluorescence pattern (IIF) and target antigen (MPO/PR3) ELISA. A medical professional tool based on authoritative medical standards, for reference only.",
    ]))

    # anti-ccp (52)
    write('anti-ccp', build('anti-ccp', [
        "📋 Anti-CCP Antibody (Rheumatoid) Specificity Assessor",
        "Interprets anti-cyclic citrullinated peptide (CCP) antibody in rheumatoid arthritis (RA) diagnosis, prognosis and treatment decisions",
        'This tool performs professional calculation and outputs results based on input parameters for "interpreting anti-CCP antibody in RA diagnosis, prognosis and treatment decisions".',
        "Anti-CCP (Rheumatoid) Specificity Assessor",
        "/ Anti-CCP Assessor",
        "Anti-CCP antibody (U/mL, normal <20)",
        "RF rheumatoid factor (IU/mL, normal <20)",
        "Joint symptoms",
        "Morning stiffness >=30 min",
        "Small joint involvement (hand/wrist)",
        "Symmetric arthritis",
        "Radiographic bone erosion",
        ">=3 joints swollen",
        "Early (<6 months)",
        "Established (6 months - 2 years)",
        "Chronic (>2 years)",
        "📋 Anti-CCP vs RF Comparison",
        "Anti-CCP",
        "RA sensitivity",
        "RA specificity",
        "Early RA detection",
        "Excellent (may precede symptoms)",
        "Bone erosion prediction",
        "Positive in non-RA diseases",
        "Common (SS/SLE/infection/liver disease)",
        "Positive in healthy population",
        "3-5% (increases with age)",
        "Titer correlates with activity",
        "Weak correlation",
        "Some correlation",
        "📊 Anti-CCP Antibody Level Clinical Significance",
        "Anti-CCP (U/mL)",
        "RA possibility reduced (not excluded)",
        "Need clinical correlation, possible seronegative RA",
        "Supports RA diagnosis",
        "High-titer positive",
        "RA specificity >98%, poor prognosis",
        "Note: anti-CCP is the most important serological marker for RA, specificity 95-98%. Anti-CCP can be positive years before RA symptoms, valuable for early diagnosis. High-titer anti-CCP + bone erosion + RF positive = poor-prognosis triad, suggests erosive progressive RA needing early aggressive DMARDs. About 20-30% of RA patients are anti-CCP negative (seronegative RA). ACPA positive (anti-CCP/anti-citrullinated protein) may rarely appear in other autoimmune diseases or healthy people (low titer), needs clinical judgment. For clinical reference only.",
        "📚 In-depth: Anti-CCP/RF Rheumatoid Arthritis Assessment",
        "High-titer antibody",
        "Small joint symmetric",
        "Erosion and prognosis",
        "RA high, poor prognosis",
        "Anti-CCP 200 (>=160), RF 120 (>=60), bilateral small joint symmetric swelling >=6 weeks, morning stiffness, X-ray bone erosion -> high RA score and poor prognosis, start DMARD+biologic early to prevent disability.",
        "Early, no erosion",
        "CCP 80, RF 40, small joint swelling but no erosion -> early RA, aggressive csDMARD to achieve target.",
        "Scoring?",
        "High-titer autoantibody (+3) + disease duration >=6 weeks (+1) + small joint/symmetric/morning stiffness/erosion combination; 2010 ACR criteria >=6 classifies RA.",
        "Prognosis?",
        "High-titer CCP/RF, early erosion, polyarticular, acute phase -> poor prognosis, needs intensive therapy and close follow-up.",
        "About the Anti-CCP (Rheumatoid) Specificity Assessor",
        "Anti-CCP antibody (rheumatoid) specificity assessor, interprets anti-CCP antibody clinical significance in RA diagnosis, prognosis and comparison with RF. A medical professional tool based on authoritative medical standards, for reference only.",
    ]))

    # assessor-10 (33)
    write('assessor-10', build('assessor-10', [
        "🛡️ Sjogren's Syndrome (ESSDAI) Systemic Assessment",
        "EULAR Sjogren's Syndrome Disease Activity Index (ESSDAI), weighted score of 12 organ systems, assesses systemic organ involvement activity",
        "ESSDAI Organ System Assessment",
        "Select a grade per organ system by current activity (0=none, 1=low, 2=moderate, 3=high), the system auto-weights",
        "Calculate ESSDAI score",
        "📚 In-depth: ESSDAI Systemic Assessment (scoring)",
        "Grade item by item",
        "Activity stratification",
        "Total 14",
        "12 systems dropdown: lymph node 2 + lung 2 + renal (weight 4) + hematologic 1 + articular 1 + skin 1 + peripheral nerve 1 + central 1 + glandular 1 = 14, >=14 is high activity, suggests systemic immunosuppression.",
        "Low 3",
        "Total 3 (e.g. articular 1 + skin 1 + glandular 1) -> low activity, symptomatic mainly.",
        "Difference from essdai?",
        "This page is scoring (assessor), essdai is display, scoring rules identical.",
        "Weighted items?",
        "Renal, pulmonary, nervous etc. 'high' grade takes that domain's weight (e.g. renal weight 4), others low/mod/high = 1/2/weight.",
        "This tool is based on EULAR Sjogren's Disease Activity Index (ESSDAI), runs entirely in-browser, data is not uploaded to any server",
        "ESSDAI has 12 organ-system domains with different weights (1-5), activity 0-3 levels, max total ~96",
        "Disease activity grading: 0=no activity, 1-5=low, 6-13=moderate, >=14=high",
        "This tool is for clinical assessment reference; treatment decisions need comprehensive judgment by a rheumatologist",
        "About the Sjogren's Syndrome (ESSDAI) Systemic Assessment",
        "EULAR Sjogren's Disease Activity Index (ESSDAI) assesses activity of 12 organ systems (systemic, lymph node, glandular, articular, skin, pulmonary, renal, muscular, peripheral nerve, central nerve, hematologic, biological), weighted total quantifies systemic involvement.",
        "12 organ systems standardized assessment",
        "Each domain weighted score (weight 1-5)",
        "Four-level disease activity grading",
        "Affected organ visualization and treatment suggestions",
        "Primary Sjogren's systemic assessment",
        "Baseline activity before immunosuppression",
        "Rheumatology clinical research standardization",
        "How to use the Sjogren's Syndrome (ESSDAI) Systemic Assessment",
        "What does the Sjogren's Syndrome (ESSDAI) Systemic Assessment do?",
        "How to use the Sjogren's Syndrome (ESSDAI) Systemic Assessment?",
        "What scenarios is the Sjogren's Syndrome (ESSDAI) Systemic Assessment suitable for?",
    ]))

    # basdai (43)
    write('basdai', build('basdai', [
        "🛡️ Ankylosing Spondylitis BASDAI Activity Assessor",
        "Bath Ankylosing Spondylitis Disease Activity Index, assesses AS disease activity over the past week",
        "Ankylosing Spondylitis (BASDAI) Activity Assessor",
        "/ BASDAI Assessor",
        "ASDAS-CRP = 0.12 x back pain + 0.06 x morning stiffness duration + 0.07 x patient global + 0.11 x CRP (sqrt)",
        "Please rate",
        "Past week",
        "rate each of the following (0-10, 0=none, 10=very severe):",
        "1. Fatigue/tiredness level",
        "2. Neck/back/hip AS pain level",
        "3. Other joint pain/swelling (excluding neck/back/hip)",
        "4. Localized tenderness discomfort level",
        "5. Morning stiffness severity",
        "6. Morning stiffness duration (0=0h, 10=>=2h)",
        "Calculate BASDAI",
        "📋 BASDAI Calculation Method",
        "Items 5 and 6 (morning stiffness severity and duration) averaged, then summed with the other 4 items, divided by 5.",
        "📊 BASDAI Clinical Significance",
        "Clinical decision",
        "Maintain NSAIDs + exercise",
        "Consider starting anti-TNF biologic",
        "High activity (confirmed)",
        "Recommend biologic / JAK inhibitor",
        "Note: BASDAI>=4 is one of the main ASAS/EULAR criteria to start anti-TNF biologic. BASDAI is subjective; combine with ASDAS (objective CRP/ESR) for comprehensive assessment. ASDAS-CRP = 0.12 x back pain + 0.06 x morning stiffness duration + 0.07 x patient global + 0.11 x CRP (sqrt). For clinical reference only.",
        "📚 In-depth: BASDAI AS Activity",
        "Fatigue",
        "Spinal pain",
        "Morning stiffness",
        "High activity 4.8",
        "6 items 0-10: fatigue 6, spinal pain 4, joint swelling 5, tendinitis 3, morning stiffness 7 and 5 -> stiffness mean 6; BASDAI=(6+4+5+3+6)/5=4.8 >4, high activity.",
        "Low activity 2.0",
        "Each symptom ~2 -> 2.0, low activity, maintain TNF/IL-17 inhibitor.",
        "Interpretation?",
        "0-4 low activity, >4 high activity; >4 often suggests adjusting biologic. Morning stiffness is the mean of two items, then averaged with the first 4.",
        "Self-assessment limitation?",
        "BASDAI includes subjective symptoms, combine with CRP/imaging and function (BASFI) for effect judgment.",
        "About the Ankylosing Spondylitis (BASDAI) Activity Assessor",
        "Ankylosing spondylitis BASDAI activity assessor, calculates the BASDAI index via 6 VAS items (fatigue, pain, joint swelling, tenderness, morning stiffness severity and duration). A medical professional tool based on authoritative medical standards, for reference only.",
        "How to use the Ankylosing Spondylitis BASDAI Activity Assessor",
        "What does the Ankylosing Spondylitis BASDAI Activity Assessor do?",
        "AS BASDAI assessor: input 6 symptom VAS scores (0-10), compute the BASDAI activity index by the standard weighted formula, helping AS patients and rheumatologists assess disease.",
        "How to use the Ankylosing Spondylitis BASDAI Activity Assessor?",
        "What scenarios is the Ankylosing Spondylitis BASDAI Activity Assessor suitable for?",
    ]))

    # behcet-hla (48)
    write('behcet-hla', build('behcet-hla', [
        "🦴 Behcet's Disease HLA-B51 Clinical Assessor",
        "Assesses clinical manifestations and HLA-B51 association by the international Behcet's criteria (ICBD 2014)",
        "Behcet's Disease (HLA-B51) Clinical Assessor",
        "/ Behcet's Disease Assessor",
        "Major clinical manifestations (2 points each)",
        "Oral aphthous ulcer",
        "Genital ulcer",
        "Ocular lesions (uveitis/retinal vasculitis)",
        "Minor clinical manifestations (1 point each)",
        "Skin lesions (erythema nodosum/folliculitis/acne)",
        "Neurological involvement",
        "Vascular involvement (venous thrombosis/aneurysm/arterial occlusion)",
        "Joint pain/arthritis",
        "Gastrointestinal involvement (intestinal ulcer)",
        "Epididymitis",
        "Auxiliary tests",
        "Pathergy test positive",
        "HLA-B51 positive",
        "<25 years (early onset)",
        "25-40 years (typical)",
        ">40 years (late onset)",
        "📋 ICBD 2014 Diagnostic Criteria",
        "Ocular lesions",
        "Skin lesions",
        "Vascular involvement",
        "1 (optional)",
        "Total >=4 points diagnoses Behcet's. HLA-B51 is not directly scored but serves as supporting evidence.",
        "📊 HLA-B51 and Behcet's Disease Association",
        "HLA-B51 positivity: 50-80% in Behcet's (10-20% in general population), especially Mediterranean/East Asian",
        "HLA-B51 positive: onset risk increased 5-10 fold",
        "HLA-B51 correlates positively with ocular involvement and severity",
        "Male, early onset (<40), HLA-B51 positive = poor-prognosis triad",
        "HLA-B51 negative does not exclude Behcet's diagnosis",
        "Note: Behcet's diagnosis is by comprehensive clinical judgment, no specific lab marker. HLA-B51 is a genetic susceptibility marker, not a diagnostic one. Ocular involvement (posterior uveitis) is the main cause of blindness, needs early ophthalmology. Vascular (venous thrombosis/aneurysm) and neuro-Behcet have poor prognosis, need aggressive immunosuppression. Treatment: colchicine for skin-mucosa, corticosteroids + immunosuppressants/biologics (anti-TNF) for visceral. For clinical reference only.",
        "📚 In-depth: Behcet's Disease HLA-B51 Assessment",
        "Oral/genital ulcers",
        "Eye/skin",
        "Vascular/nerve",
        "High diagnostic score",
        "Recurrent oral ulcers + genital ulcers + ocular uveitis + skin erythema nodosum + pathergy + HLA-B51 positive + male -> meets international criteria with many prognostic factors, clear Behcet's, prone to visceral involvement.",
        "Incomplete type",
        "Only oral + skin manifestations, HLA-B51 negative -> incomplete type, follow eye/vascular complications.",
        "Diagnostic criteria?",
        "Recurrent oral ulcers + any 2 (genital/eye/skin/pathergy) -> suspected; HLA-B51 relates to vascular/neuro types.",
        "Prognostic factors?",
        "Male, early onset, eye/vascular/neuro involvement suggest worse, need aggressive immunosuppression to prevent blindness and stroke.",
        "About the Behcet's Disease (HLA-B51) Clinical Assessor",
        "Behcet's HLA-B51 clinical assessor, assesses Behcet's clinical manifestations and HLA-B51 association by the international Behcet's criteria (ICBD). A medical professional tool based on authoritative medical standards, for reference only.",
    ]))

if __name__ == "__main__":
    main()

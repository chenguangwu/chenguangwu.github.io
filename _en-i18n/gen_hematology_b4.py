#!/usr/bin/env python3
# gen_hematology_b4.py — hematology b4 (5 slugs): leukemia-classification/lymphoma-staging/m-protein/mm-staging/mpn-scoring
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

B['leukemia-classification'] = [
 '📚 Leukemia FAB/MICM Classification Reference',
 'Look up the FAB morphological classification and MICM integrated classification of acute leukaemia.',
 'Leukaemia FAB/MICM Classification Reference',
 '/ Leukaemia Classification Reference',
 '📖 Read the "Leukemia FAB/MICM Classification Reference Usage Guide"',
 'Acute leukaemia classification follows MICM: morphology (FAB: AML M0-M7, ALL L1-L3), immunology (flow markers: myeloid CD13/CD33/MPO, lymphoid CD19/CD10/CD3), cytogenetics (t(15;17), t(8;21), inv(16), etc.) and molecular biology (PML-RARA, BCR-ABL1); bone marrow blasts at least 20% is the diagnostic threshold for acute leukaemia.',
 'MICM classification',
 'Select subtype',
 'M0 - acute myeloid leukaemia, minimally differentiated',
 'M1 - acute myeloid leukaemia without maturation',
 'M2 - acute myeloid leukaemia with maturation',
 'M3 - acute promyelocytic leukaemia',
 'M4 - acute myelomonocytic leukaemia',
 'M4Eo - with eosinophilia',
 'M5 - acute monoblastic/monocytic leukaemia',
 'M6 - acute erythroid leukaemia',
 'M7 - acute megakaryoblastic leukaemia',
 'L1 - small, uniform cells',
 'L2 - large, heterogeneous cells',
 'L3 - Burkitt type (large cells, vacuoles)',
 '📋 WHO 2022 core concepts of acute leukaemia',
 'MICM classification system',
 'Morphology: FAB typing, bone marrow smear cytology',
 'Immunology: flow cytometry immunophenotype (CD markers)',
 'Cytogenetics: chromosome karyotype analysis (G-banding)',
 'Molecular biology: fusion genes, gene mutation testing',
 'Common AML cytogenetic / molecular abnormalities',
 'FAB correspondence',
 'FLT3-ITD mutation',
 'All subtypes',
 'Adverse',
 'NPM1 mutation (without FLT3-ITD)',
 'CEBPA double mutation',
 'Complex / monosomal karyotype',
 'Note: the WHO 2016/2022 classifications divide AML into "recurrent genetic abnormalities" and "AML defined by myelodysplasia-related changes", among others. FAB typing remains the morphological basis. For study reference only.',
 '📚 Deep Dive: Leukemia FAB/MICM Classification Reference',
 'For AML, look up typical indicators and thresholds by FAB morphology (M0-M7).',
 'For ALL, use FAB (L1/L2/L3) together with immunophenotyping.',
 'Combine MICM (morphology / immunology / cytogenetics / molecular) for an integrated diagnosis.',
 'FAB morphological typing: AML by blast proportion and differentiation (M0 minimally differentiated, M1 immature, M2 granulocytic, M3 promyelocytic (APL), M4 myelomonocytic, M5 monocytic, M6 erythroid, M7 megakaryoblastic); ALL split L1 (small uniform), L2 (large heterogeneous), L3 (Burkitt-like). Modern diagnosis uses MICM: immunophenotyping assigns lineage, karyotype / fusion genes (e.g. PML-RARA, AML1-ETO) assign prognosis and targets.',
 'Example (AML: marrow blasts 45%, Auer rods positive, t(15;17) positive): FAB is M3 (acute promyelocytic leukaemia APL), immunology/molecular confirms PML-RARA fusion → high risk but curable, first-line all-trans-retinoic acid (ATRA) plus arsenic, avoid plain chemotherapy that can trigger differentiation syndrome.',
 'Is FAB still used?',
 'FAB remains the morphological communication basis, but current WHO/ICC classifications stress genetics (e.g. RUNX1::RUNX1T1, PML-RARA) and molecular markers; morphology alone misclassifies, so MICM must be combined.',
 'Why is APL special?',
 'M3/APL, driven by t(15;17) and PML-RARA, is highly sensitive to ATRA plus arsenic and curable, but the induction phase risks differentiation syndrome and bleeding (DIC); management differs from other AML, so it must be recognised early.',
 'About the Leukemia FAB/MICM Classification Reference',
 'A leukaemia FAB and MICM classification reference: it provides the FAB typing and MICM integrated diagnostic reference for acute myeloid leukaemia (AML M0-M7) and acute lymphoblastic leukaemia (ALL L1-L3). A professional medical tool based on authoritative medical standards, for reference only.',
]

B['lymphoma-staging'] = [
 '🏠 Lymphoma Ann Arbor Staging Tool',
 'Based on the Cotswold-modified Ann Arbor staging system, for Hodgkin and non-Hodgkin lymphoma.',
 '"Based on the Cotswold-modified Ann Arbor staging system, for Hodgkin and non-Hodgkin lymphoma" is computed from the input parameters and the result is output.',
 'Lymphoma Ann Arbor Staging Tool',
 '/ Lymphoma Staging Tool',
 '📖 Read the "Lymphoma Ann Arbor Staging Tool Usage Guide"',
 'Lymph node regions involved (tick all affected sites)',
 'Above diaphragm: neck / supraclavicular',
 'Above diaphragm: axilla / epitrochlear',
 'Above diaphragm: mediastinum',
 'Above diaphragm: hilar',
 'Below diaphragm: para-aortic',
 'Below diaphragm: iliac / inguinal / femoral',
 'Below diaphragm: mesenteric',
 'Spleen involvement',
 'Extranodal involvement',
 'Localized extranodal involvement (E)',
 'Diffuse / multifocal extranodal involvement',
 'Systemic symptoms (B symptoms)',
 'Fever >38°C of unknown cause',
 'Drenching night sweats',
 'Weight loss >10% / 6 months',
 'Bulky disease',
 'Mediastinal tumour / thoracic diameter ratio (MT ratio)',
 'Largest mass diameter (cm)',
 '📋 Ann Arbor / Cotswold staging criteria',
 'Single lymph node region (I) or single extranodal organ/site (IE)',
 '≥2 node regions on the same side of diaphragm (II), may have localized extranodal (IIE)',
 'Node regions on both sides of diaphragm (III), may have spleen (IIIS) / extranodal (IIIE) / both (IIIES)',
 'Diffuse / multifocal extranodal organs involved, regardless of nodes',
 'Modifier symbols',
 'No systemic symptoms',
 'With fever / night sweats / weight loss',
 'Localized extranodal involvement',
 'Bulky (mediastinal MT >1/3 or mass >10 cm)',
 'Note: the Lugano staging system simplifies Ann Arbor I-II to "limited stage" and III-IV to "advanced stage". PET-CT is the core of modern lymphoma staging and response assessment. For study reference only.',
 '📚 Deep Dive: Lymphoma Ann Arbor Staging Tool',
 'Assign Ann Arbor stage (I-IV) by involved nodal regions and their relation to the diaphragm.',
 'Add modifiers: A/B symptoms, extranodal (E), spleen (S), bulky (X).',
 'Distinguish treatment strategy differences between Hodgkin and NHL.',
 'Ann Arbor (Cotswold-modified): I single node region; II ≥2 regions same side of diaphragm; III both sides; IV diffuse extranodal. Modifiers: A none / B systemic symptoms (fever >38°C, night sweats, >10% weight loss in 6 months), E localized extranodal, S spleen, X bulky (mediastinal ratio ≥1/3 or mass ≥10 cm).',
 'Example 1 (2 node regions above diaphragm, no B symptoms): stage IIA (limited-advanced). Example 2 (1 region above + 1 below diaphragm): stage III (both sides). Example 3 (multifocal extranodal + bulky): stage IV (advanced). Treatment escalates from radiotherapy / chemo to autologous transplant.',
 'Why mark bulky X separately?',
 'Bulky disease (mediastinal ratio ≥1/3 or largest diameter ≥10 cm) has worse prognosis and higher local relapse; it often needs consolidative radiotherapy or intensified chemo, so X is added after staging to guide radiotherapy decisions.',
 'Do B symptoms always mean advanced stage?',
 'Not necessarily. B symptoms are an adverse factor but independent of stage; early (I/II) with B symptoms stays in the corresponding early stage, just treated more aggressively (often as "poor-prognosis early").',
 'About the Lymphoma Ann Arbor Staging Tool',
 'A lymphoma Ann Arbor staging tool: it assigns Ann Arbor/Cotswold stage from nodal regions, extranodal involvement and systemic symptoms, covering stages I-IV and A/B symptom classification. A professional medical tool based on authoritative medical standards, for reference only.',
]

B['m-protein'] = [
 '📚 M-Protein (Serum Protein Electrophoresis) Identifier',
 'Interprets serum protein electrophoresis, assesses the M-protein peak and helps differentiate monoclonal gammopathy.',
 '"Interprets serum protein electrophoresis, assesses the M-protein peak and helps differentiate monoclonal gammopathy" is computed from the input parameters and the result is output.',
 'M-Protein Serum Protein Electrophoresis Identifier',
 '/ M-Protein Identifier',
 '📖 Read the "M-Protein (Serum Protein Electrophoresis) Identifier Usage Guide"',
 'Total protein (g/L) 60-80',
 'Albumin (g/L) 35-50',
 'M-protein concentration (g/L)',
 'M-protein band region',
 'γ region (most common)',
 'β region',
 'α2 region',
 'No obvious M peak seen',
 'Immunofixation electrophoresis result',
 'IgG positive',
 'IgA positive',
 'IgM positive',
 'IgD positive',
 'κ light chain',
 'λ light chain',
 'Serum IgG (g/L) 7-16',
 'Serum IgA (g/L) 0.7-4',
 'Serum IgM (g/L) 0.4-2.3',
 'Serum κ light chain (mg/L) 3.3-19.4',
 'Serum λ light chain (mg/L) 5.7-26.3',
 '📋 Differential of monoclonal gammopathy',
 'M-protein',
 'Bone marrow plasma cells',
 'Smouldering MM',
 'Multiple myeloma',
 'WM (Waldenström macroglobulinaemia)',
 'IgM type',
 'Lymphoplasmacytic cells',
 'Symptom-related',
 '📊 CRAB criteria (IMWG)',
 '(Calcium): serum calcium >2.75 mmol/L',
 '(Renal): creatinine clearance <40 mL/min or serum creatinine >177 μmol/L',
 '(Anemia): haemoglobin <100 g/L or >20 g/L below the lower limit',
 '(Bone): lytic lesions or diffuse osteoporosis',
 'Note: the normal κ/λ ratio is 0.26-1.65; an abnormal ratio suggests monoclonality. An IgM-type M protein should raise WM / lymphoma. For study reference only.',
 '📚 Deep Dive: M-Protein (Serum Protein Electrophoresis) Identifier',
 'An M peak on serum protein electrophoresis grades MGUS / SMM / MM by concentration and type.',
 'Compute the κ/λ light-chain ratio to judge monoclonal skew.',
 'Combine CRAB and marrow plasma cells to assess multiple myeloma.',
 'M-protein grading: <15 g/L usually MGUS; 15-30 needs discrimination of MGUS from smouldering (SMM, plasma cells ≥10% and no CRAB); ≥30 strongly suggests multiple myeloma (needs plasma cells ≥10% + CRAB). Normal κ/λ ratio 0.26-1.65; deviation suggests monoclonal light-chain skew. Auxiliary: globulin = total protein − albumin, M% = M / total protein × 100%.',
 'Example (total protein 75, albumin 35, M protein 25, κ=500, λ=30): globulin = 75−35 = 40 g/L, κ/λ = 500/30 = 16.67 (κ skew up), M% = 25/75×100 = 33.3%; M in 15-30 → need marrow biopsy to tell MGUS from smouldering MM; if plasma cells ≥10% and no CRAB, classify as SMM.',
 'Does MGUS need treatment?',
 'Usually not, but regular follow-up is needed (~1%/year progresses to MM or related disease); re-evaluate when CRAB appears, M protein rises markedly or the light-chain ratio deviates extremely.',
 'Normal κ/λ ratio yet called monoclonal?',
 'Possible. In a few cases the total light-chain ratio is normal but immunofixation shows a single light-chain band (e.g. low-secreting light-chain type); the ratio is only auxiliary, and diagnosis rests on electrophoresis / immunofixation combined with free light chains.',
 'About the M-Protein Serum Protein Electrophoresis Identifier',
 'An M-protein serum protein electrophoresis identifier: it reads serum protein electrophoresis (SPEP), assesses the M-protein peak and distinguishes monoclonal gammopathies such as multiple myeloma and MGUS. A professional medical tool based on authoritative medical standards, for reference only.',
]

B['mm-staging'] = [
 '🏠 Multiple Myeloma R-ISS Staging Tool',
 'Revised International Staging System, based on ISS + LDH + high-risk cytogenetics',
 '"Revised International Staging System, based on ISS + LDH + high-risk cytogenetics" is computed from the input parameters and the result is output.',
 'Multiple Myeloma R-ISS Staging Tool',
 '/ Multiple Myeloma R-ISS Staging',
 '📖 Read the "Multiple Myeloma R-ISS Staging Tool Usage Guide"',
 'β2-microglobulin (mg/L)',
 'LDH (U/L) upper limit of normal',
 'LDH measured value (U/L)',
 'Cytogenetics (FISH)',
 'del(17p) / TP53 deletion',
 '1q gain / amplification',
 'del(17p), t(4;14), t(14;16), t(14;20) are high-risk cytogenetic abnormalities in ISS/R-ISS',
 '📋 R-ISS staging criteria',
 'R-ISS stage',
 'Median OS (months)',
 'ISS I + normal LDH + no high-risk genetics',
 'Neither stage I nor III',
 'ISS III + raised LDH and/or high-risk genetics',
 '📊 ISS staging',
 'ISS stage',
 'Albumin ≥35 g/L and β2-MG <3.5 mg/L',
 'Neither I nor III',
 'Note: R-ISS adds LDH and high-risk FISH to ISS for more accurate prognosis. 1q amplification is also listed as intermediate-high risk in the newer Mayo mSMART. For clinical reference.',
 '📚 Deep Dive: Multiple Myeloma R-ISS Staging Tool',
 'For newly diagnosed MM, assign R-ISS stage by ISS (β2-MG, albumin) + LDH + high-risk FISH.',
 'Use R-ISS to communicate median overall survival and risk (I not reached / II ~83 / III ~43 months).',
 'Combine intermediate-high risk markers such as 1q21 amplification for an integrated judgement.',
 'ISS: β2-MG <3.5 and albumin ≥35 g/L is I; β2-MG ≥5.5 is III; between is II. R-ISS integrates LDH and cytogenetics on ISS: high-risk FISH = del(17p), t(4;14), t(14;16), t(14;20). R-ISS I = ISS I and normal LDH and no high-risk genetics; III = ISS III and raised LDH and/or high-risk genetics; the rest is II.',
 'Example 1 (β2-MG=2.8, albumin=42 g/L, normal LDH, no high-risk FISH): ISS I + normal LDH + no high-risk → R-ISS I (median OS not reached). Example 2 (β2-MG=6.0, albumin=30, raised LDH, del(17p)): ISS III + raised LDH and high-risk → R-ISS III (median OS ~43 months).',
 'Where is R-ISS better than ISS?',
 'R-ISS adds LDH and high-risk cytogenetics to separate patients who share ISS but differ in prognosis, giving finer risk distinction; it is one of the mainstream standards for MM prognosis communication.',
 'Is 1q21 amplification high risk?',
 '1q21 amplification is listed as intermediate-high risk in newer versions such as Mayo mSMART, but is not directly in the classic R-ISS high-risk FISH; if combined with other adverse factors the overall risk should be raised, and interpretation follows the centre and version.',
 'About the Multiple Myeloma R-ISS Staging Tool',
 'A multiple myeloma R-ISS revised international staging tool: it assigns R-ISS stage from albumin, β2-microglobulin, LDH and high-risk cytogenetics. A professional medical tool based on authoritative medical standards, for reference only.',
]

B['mpn-scoring'] = [
 '📋 Myelofibrosis MPN Scoring System',
 'Supports IPSS-MF / DIPSS / DIPSS-plus prognostic scores for survival risk stratification in primary myelofibrosis.',
 '"Supports IPSS-MF / DIPSS / DIPSS-plus prognostic scores for survival risk stratification in primary myelofibrosis" is computed from the input parameters and the result is output.',
 'Myelofibrosis MPN Scoring System',
 '/ Myelofibrosis Score',
 '📖 Read the "Myelofibrosis MPN Scoring System Usage Guide"',
 'IPSS-MF (at diagnosis)',
 'DIPSS (during follow-up)',
 'Peripheral blood blasts (%)',
 'Constitutional symptoms (night sweats / fever / weight loss)',
 'DIPSS-plus additional items',
 'Transfusion dependence',
 'Unfavourable karyotype (+8, −7/7q−, i(17q), −5/5q−, etc.)',
 '📋 IPSS-MF risk stratification',
 'Risk group',
 'Median survival (months)',
 'Intermediate-1',
 'Intermediate-2',
 'IPSS variables: age >65 (1), HGB <100 (1), WBC >25 (1), peripheral blasts >1% (1), constitutional symptoms (1)',
 'DIPSS is for follow-up assessment, HGB <100 scores 2 (other variables 1 each). DIPSS-plus adds platelet <100, transfusion dependence and unfavourable karyotype, 1 each, on top of DIPSS. For clinical reference.',
 '📚 Deep Dive: Myelofibrosis MPN Scoring System',
 'Primary myelofibrosis is risk-stratified by IPSS-MF / DIPSS / DIPSS-plus.',
 'Look at median survival and transplant indication (high-risk / intermediate-2 consider allogeneic transplant).',
 'Heavy symptom burden (high MPN-10) favours a JAK2 inhibitor first.',
 'IPSS-MF: age >65 (+1), HGB <100 (+1), WBC >25 (+1), peripheral blasts >1% (+1), constitutional symptoms (+1); 0 low, 1 intermediate-1, 2-3 intermediate-2, 4-6 high. DIPSS/DIPSS-plus are similar but HGB <100 scores +2, and add platelet / transfusion / karyotype items.',
 'Example (age 65, HGB=95, WBC=15, blasts=2%, no constitutional symptoms): IPSS-MF = 0(age not over) +1(HGB) +0(WBC) +1(blasts) +0 = 2 → intermediate-2 group (median survival ~48 months); assess JAK2 inhibitor and transplant indication.',
 'How to choose IPSS-MF versus DIPSS?',
 'IPSS-MF is for initial diagnosis (includes age); DIPSS/DIPSS-plus better fit established cases needing dynamic re-stratification (adding platelet, transfusion dependence, karyotype); clinically both are often reported.',
 'Why do blasts >1% score high?',
 'Rising peripheral blasts signal disease progression / blast transformation risk and are a strong adverse marker; if ≥2% some systems add further weight, so watch for blast crisis.',
 'About the Myelofibrosis MPN Scoring System',
 'A myelofibrosis MPN scoring system: it supports the three prognostic scores IPSS-MF, DIPSS and DIPSS-plus to risk-stratify survival in primary and post-PV myelofibrosis. A professional medical tool based on authoritative medical standards, for reference only.',
]

for s, lst in B.items():
    write(s, build(s, lst))

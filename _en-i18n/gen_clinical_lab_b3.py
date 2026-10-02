#!/usr/bin/env python3
# gen_clinical_lab_head.py — shared head for clinical-lab batches b1..bN
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'clinical-lab')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'clinical-lab')
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
    out = {'slug': slug, 'industry': 'clinical-lab', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('flow-cytometry-ratio', build('flow-cytometry-ratio', [
        "Flow Cytometry (CD4/CD8) Ratio Calculator",
        "Compute T-cell subset CD4/CD8 ratio and absolute counts to assess immune status.",
        "Core formulas (by input): wbc × (lpct÷100) × 1000; absLymph × (cd19÷100); absLymph × (cd4÷100)",
        "Flow Cytometry CD4/CD8 Ratio Calculator",
        "/ Flow Cytometry CD4/CD8 Ratio Calculator",
        'View "Flow Cytometry (CD4/CD8) Ratio Calculator User Guide"',
        "Lymphocyte Count (for absolute value)",
        "Lymphocyte %",
        "Flow Cytometry % Results",
        "CD3+ T Cells (%)",
        "CD3+CD4+ Helper T (%)",
        "CD3+CD8+ Suppressor T (%)",
        "CD3-CD19+ B Cells (%)",
        "T-Cell Subset Reference (Adult)",
        "Reference %",
        "Reference Absolute",
        "CD3+ Total T",
        "Overall Cellular Immunity",
        "Key HIV-Monitoring Indicator",
        "Cytotoxic T Cells",
        "CD4/CD8 Ratio",
        "Immune-Regulation Balance",
        "Humoral Immunity",
        "Innate Immunity",
        "Clinical Significance:",
        "• CD4/CD8↓: common in AIDS (CD4<200 is AIDS stage), post-chemo, immunosuppression",
        "• CD4/CD8↑: autoimmune disease (SLE, RA), allergic disease, chronic infection",
        "• CD4<500: immune suppression in HIV; <200: high opportunistic-infection risk, needs prophylaxis",
        "📚 In-Depth: Flow Cytometry (CD4/CD8) Ratio Calculator",
        "In HIV follow-up, compute CD4/CD8 ratio and absolute-count trends.",
        "For immune-function assessment, view T/B/NK subset distribution.",
        "Teach flow-cytometry gating and ratio meaning.",
        "CD4/CD8 Ratio Example",
        "CD4 400, CD8 800, ratio 0.5 (below the common 1–2), suggesting immunosuppression tendency; but correlate with CD4 absolute count and cause.",
        "Is a ratio below 1 always disease?",
        "Not necessarily; age, infection and stress can affect it; trends and absolute counts matter more.",
        "Are results comparable across instruments?",
        "Different gating and antibody panels differ; for longitudinal comparison use the same platform when possible.",
        "Can immunotherapy be decided from this?",
        "No, treatment is decided jointly by infectious-disease/rheumatology physicians.",
        "About the Flow Cytometry CD4/CD8 Ratio Calculator",
        "A flow-cytometry CD4/CD8 ratio and lymphocyte-subset calculator. Enter each subset percentage or absolute count to compute the CD4/CD8 ratio against reference ranges, aiding immune-status assessment; results for review only, not a specialty substitute.",
        "Auto CD4/CD8 Ratio",
        "Subset % & Absolute Compare",
        "Reference-Range Highlight",
        "HIV Follow-up Immune Monitor",
        "Lymphocyte-Subset Assessment",
        "Teaching: Gating Logic",
    ]))
    write('hba1c-converter', build('hba1c-converter', [
        "HbA1c and Blood Glucose Converter",
        "Convert HbA1c and estimated average glucose (eAG) to assess blood-glucose control over the last 2–3 months.",
        "HbA1c Glucose Converter",
        "/ HbA1c Converter",
        'View "HbA1c and Blood Glucose Converter User Guide"',
        "HbA1c → Glucose",
        "Glucose → HbA1c",
        "Estimated Average Glucose (mmol/L)",
        "Glycemic Control Target (HbA1c)",
        "Target HbA1c",
        "Corresponding eAG",
        "Most T2DM patients",
        "Relaxed Target",
        "Elderly / Multiple Comorbidities",
        "Strict Target",
        "Young / No Complications",
        "Pregnancy",
        "GDM / Pre-pregnancy DM",
        "Diagnosing Diabetes",
        "Needs Repeated Confirmation",
        "Fasting / Impaired Glucose Tolerance",
        "Conversion Formulas:",
        "• Reverse: HbA1c = (eAG_mgdl + 46.7) ÷ 28.7",
        "HbA1c reflects average glucose over the last 2–3 months (RBC lifespan ~120 days) and is unaffected by a single meal.",
        "📚 In-Depth: HbA1c and Blood Glucose Converter",
        "Convert between domestic reports (%) and foreign literature (mmol/mol) for understanding.",
        "Unify diabetes-management targets (e.g. <7% or <53 mmol/mol) for comparison.",
        "Teach the relationship between the two units.",
        "HbA1c Conversion Example",
        "NGSP 7.0% → IFCC (7.0−2.15)×10.93 ≈ 53 mmol/mol, near the common upper target for diabetes management.",
        "Is the conversion exact?",
        "Use the official approximate relation, enough for comparison; exact reports follow the testing system, and methods differ slightly.",
        "Does anemia affect HbA1c?",
        "Yes; hemolytic anemia and kidney disease can raise or lower it; in such cases use fructosamine/glucose as adjuncts.",
        "Can it alone diagnose diabetes?",
        "HbA1c ≥6.5% can be one diagnostic basis, but needs venous glucose and guidelines; reassess when anemia etc. interferes.",
        "About the HbA1c Glucose Converter",
        "An HbA1c NGSP% ↔ IFCC mmol/mol conversion tool. For cross-report and guideline comparison; pure conversion.",
        "Dual-Unit Conversion",
        "Management-Target Compare",
        "Instant Display",
        "Domestic/Foreign Report Compare",
        "Unified Management Target",
        "Teaching: The Relation",
    ]))
    write('mic-breakpoint', build('mic-breakpoint', [
        "Microbiology MIC Breakpoint Comparator",
        "Compare CLSI breakpoints; enter MIC to auto-classify Susceptible (S)/Intermediate (I)/Resistant (R).",
        "MIC Breakpoint Comparator",
        "/ MIC Breakpoint Comparator",
        'View "Microbiology MIC Breakpoint Comparator User Guide"',
        "Compare measured MIC with breakpoints per CLSI/EUCAST to read S/I/R; for review only, medication is decided by infectious-disease and pharmacy.",
        "Bacterial Type",
        "Gram-negative Enterobacterales",
        "Gram-positive (Staphylococci)",
        "Pseudomonas aeruginosa",
        "Streptococcus pneumoniae",
        "Enter MIC Value (μg/mL)",
        "Interpretation Criteria (CLSI 2023):",
        "• S Susceptible: MIC ≤ S breakpoint, suppressible at standard dose",
        "• I Intermediate: MIC between S and R, may need higher dose or restricted use",
        "• R Resistant: MIC ≥ R breakpoint, high risk of standard-therapy failure",
        "Breakpoints vary by organism-drug pair; this tool's data are based on CLSI M100; follow your local lab report clinically.",
        "📚 In-Depth: Microbiology MIC Breakpoint Comparator",
        "After blood/urine culture reports MIC, look up the matching breakpoint by organism and drug to read S/I/R.",
        "Compare breakpoint differences between standards (CLSI vs EUCAST).",
        "Teach the relation between breakpoints and PK/PD targets (e.g. %fT>MIC).",
        "E. coli Levofloxacin Example",
        "Measured MIC 0.06 mg/L vs EUCAST E. coli susceptibility breakpoint (≤1): classified S; if MIC 8 then ≥2 gives R, requiring a switch.",
        "Does S always mean effective?",
        "Not necessarily; also consider site concentration, patient immunity and PK/PD; breakpoints are population probabilities, not individual guarantees.",
        "Are CLSI and EUCAST the same?",
        "They differ; the same MIC may be read differently, so reports should state the standard used.",
        "Can antibiotics be chosen directly?",
        "No, empirical/targeted therapy is decided by physician and clinical pharmacist; this tool only compares breakpoints.",
        "About the Microbiology MIC Breakpoint Comparator",
        "An MIC breakpoint comparator. Enter organism, drug and measured MIC to read S/I/R per CLSI/EUCAST; for review only, medication by infectious-disease and pharmacy.",
        "CLSI/EUCAST Compare",
        "Auto S/I/R Read",
        "Multi-Standard Diff Hint",
        "Susceptibility Report Review",
        "Cross-Standard Breakpoint",
        "Teaching: PK/PD Breakpoint",
        "Enter MIC vs Breakpoint",
    ]))
    write('parasite-egg-id', build('parasite-egg-id', [
        "Parasite Egg Morphology Identifier",
        "Query morphologic features of common intestinal parasite eggs to aid microscopy identification.",
        'View "Parasite Egg Morphology Identifier User Guide"',
        "Structured comparison of common fecal parasite-egg features to aid microscopy review; confirmation is by the parasitology lab.",
        "Search Egg Name",
        "Identification Key:",
        "Egg identification uses size (μm), shape, color, shell features (thickness/texture), operculum presence and contents (ovum/miracidium/oncosphere). Measure size with a micrometer and avoid confusion with pollen or plant fibers.",
        "📚 In-Depth: Parasite Egg Morphology Identifier",
        "Review microscopy differentiation of Ascaris/hookworm/pinworm/tapeworm/schistosome eggs.",
        "Teach egg-form differences and confusing points.",
        "Refresh methods before epidemiological screening.",
        "Hookworm vs Ascaris Egg Example",
        "Hookworm eggs are smaller, oval, thin-shelled with several blastomeres; Ascaris eggs are larger, thick-shelled with a bumpy protein coat; the tool lists points side by side to avoid confusion.",
        "Does seeing an egg confirm infection?",
        "It is usually important evidence, but exclude contamination and misidentification; a negative result also cannot fully rule out (oviposition rhythm varies).",
        "Can medication be taken based on this?",
        "No, anthelmintic choice is decided by the physician based on species and liver/kidney function.",
        "Is morphology enough?",
        "For difficult cases use immunologic or molecular confirmation; microscopy is the primary screen.",
        "About the Parasite Egg Morphology Identifier",
        "A parasite-egg morphology reference tool. Structurally prompts common egg differentiation points; confirmation by the parasitology lab.",
        "Morphology Key Compare",
        "Confusing-Item Hint",
        "Atlas Review",
        "Stool-Exam Review",
        "Teaching: Egg Differences",
        "Pre-Screening Refresh",
        "e.g. Ascaris, hookworm, schistosome",
    ]))
    write('pcr-ct-interpretation', build('pcr-ct-interpretation', [
        "PCR Amplification Curve (Ct) Interpreter",
        "Enter Ct to interpret amplification; supports qualitative/quantitative PCR analysis and standard-curve calculation.",
        "Enter Ct to interpret amplification; supports qualitative/quantitative PCR analysis and standard-curve calculation; the tool computes and outputs results from the inputs.",
        "PCR Amplification Curve Ct Interpreter",
        "/ PCR Amplification Curve Ct Interpreter",
        'View "PCR Amplification Curve (Ct) Interpreter User Guide"',
        "Qualitative PCR Reading",
        "Quantitative PCR Calculation",
        "Sample Ct",
        "Internal Control (β-actin) Ct",
        "Negative Control Ct",
        "Positive Control Ct",
        "Threshold (default 40 if blank)",
        "Enter standard data (concentration and Ct) to plot a standard curve and compute unknown concentration",
        "+ Add Standard",
        "Plot Standard Curve",
        "Unknown Sample Ct",
        "Ct Value (Cycle Threshold):",
        "The cycle number at which fluorescence crosses the threshold line.",
        "• Ct<29: strong positive, high template concentration",
        "• Ct 30–37: positive, medium template concentration",
        "• Ct 38–40: weak positive / gray zone, needs repeat confirmation",
        "• Ct>40 or no Ct: negative",
        "ΔCt Method:",
        "ΔΔCt Method:",
        "Relative expression = 2^(-ΔΔCt)",
        "📚 In-Depth: PCR Amplification Curve (Ct) Interpreter",
        "Understand nucleic-acid report Ct values (e.g. Ct 25 means higher load than Ct 38).",
        "Risk hints and retest advice for gray-zone (near-cutoff) results.",
        "Teach the relationship between amplification efficiency and Ct.",
        "Ct Interpretation Example",
        "Report Ct 28, cutoff 40: below threshold so positive with medium load; Ct 39 near cutoff is gray zone, advising retest or clinical correlation.",
        "Can Ct quantify viral load?",
        "It only roughly reflects load; precise quantitation needs a standard curve and known concentration; Ct across platforms is not directly comparable.",
        "Does positive mean contagious?",
        "Not necessarily; high Ct may mean low load or residual nucleic acid; contagiousness is judged by disease course and symptoms.",
        "Can it replace the nucleic-acid report?",
        "No, this tool only explains Ct meaning; the lab result is final.",
        "About the PCR Amplification Curve (Ct) Interpreter",
        "A qPCR Ct interpreter. Explains the Ct–template relation and compares qualitative thresholds to aid nucleic-acid report understanding; for review only.",
        "Ct Meaning Explained",
        "Pos/Neg Reading",
        "Gray-Zone Hint",
        "Nucleic-Acid Report",
        "Gray-Zone Retest Advice",
        "Teaching: Amplification",
        "Enter 0 if no amplification",
    ]))

if __name__ == "__main__":
    main()

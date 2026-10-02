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
    write('coagulation-inr', build('coagulation-inr', [
        "Coagulation INR Converter",
        "Convert PT/APTT/INR to assess warfarin anticoagulation goal.",
        "Core formulas (by input): ptN ÷ (ptN + 0.6×(pt-ptN)) × 100; ptN × (inrIn)^1÷isi; (pt÷ptN)^isi",
        "Coagulation INR Converter",
        "/ Coagulation INR Converter",
        'View "Coagulation INR Converter User Guide"',
        "Patient PT Prothrombin Time (s)",
        "Normal Control PT (s)",
        "ISI International Sensitivity Index",
        "Known INR (optional reverse PT)",
        "APTT (s)",
        "APTT Normal Control (s)",
        "Warfarin Target INR",
        "INR = (Patient PT / Normal PT)^ISI",
        "PT Activity (PTA)",
        "= Control PT / (Control PT + 0.6×(Patient PT − Control PT)) × 100%, <40% suggests severe liver damage",
        "APTT ratio = Patient APTT / Normal APTT; 1.5–2.5 is the heparin-treatment target range",
        "📚 In-Depth: Coagulation INR Converter",
        "For AFib/valve patients on anticoagulation, unify different-reagent PT into INR against the target range (usually 2.0–3.0).",
        "Handle cross-lab comparability (different ISI reagents).",
        "Demonstrate ISI's effect on INR in teaching.",
        "INR Calculation Example",
        "Patient PT 30s, Normal PT 12s, ISI 1.0: INR = (30/12)^1.0 = 2.5, within the common anticoagulation target; a different ISI changes the result, so use the same batch ISI.",
        "Is a higher INR always better?",
        "No. Too high raises bleeding risk, too low raises thrombosis risk; the target range is set by the disease and physician.",
        "Can you eat foods or drugs that affect INR?",
        "Vitamin-K-rich foods, some antibiotics and herbs affect it; monitor regularly while on therapy and tell your physician about all medications.",
        "Can this tool adjust medication?",
        "No, it only converts; the dose is adjusted by the anticoagulation clinic or physician.",
        "About the Coagulation INR Converter",
        "An INR converter. Computes the international normalized ratio from PT and ISI for anticoagulation-intensity conversion; dose is set by the physician.",
        "PT-INR Conversion",
        "Cross-Reagent Comparable",
        "Target-Range Hint",
        "AFib Anticoagulation",
        "Cross-Lab Compare",
        "Teaching: ISI Effect",
        "Leave blank to compute INR",
    ]))
    write('convert-39', build('convert-39', [
        "Coagulation (PT/APTT) INR Conversion",
        "INR (International Normalized Ratio) = (Subject PT / Normal Control PT) ^ ISI",
        'View "Coagulation (PT/APTT) INR Conversion User Guide"',
        "INR = (Subject PT ÷ Normal Control PT) to the power ISI; PT ratio = Subject PT ÷ Normal Control PT; ISI is the reagent's international sensitivity index, closer to 1.0 means closer to reference thromboplastin. The common therapeutic range is 2.0 to 3.0.",
        "Subject PT (s)",
        "Normal Control PT (s)",
        "ISI (Reagent Sensitivity Index)",
        "📚 In-Depth: Coagulation (PT/APTT) INR Conversion",
        "Convert foreign-literature values (mg/dL) to local reports (mmol/L) for comparison.",
        "Unify different-instrument units (IU/L ↔ ng/mL) for trend tracking.",
        "Unit proofreading for teaching and paper writing.",
        "Cholesterol Conversion Example",
        "Total cholesterol 200 mg/dL ÷ 38.67 ≈ 5.17 mmol/L, for comparison with domestic report ranges.",
        "Are conversion factors universal?",
        "Each substance",
        "molecular weight",
        "/ definition differs, so the factor differs; the tool picks the factor by substance, and mixing them is wrong.",
        "Can clinical decisions use the converted value?",
        "You can compare ranges, but the report should use the testing lab's value and unit; conversion is only auxiliary.",
        "Does rounding matter much?",
        "It may affect near-cutoff items; keep enough decimals and label the unit.",
        "About Coagulation (PT/APTT) INR Conversion",
        "About 39 classes of lab-unit conversion tools. Unify units across reports and literature; pure conversion, no diagnosis.",
        "mmol/L ↔ mg/dL etc.",
        "Auto-select substance factor",
        "Batch Conversion",
        "Foreign Literature Compare",
        "Cross-Instrument Trend",
        "Paper Unit Proofread",
    ]))
    write('convert-glucose-1', build('convert-glucose-1', [
        "HbA1c and Blood Glucose Conversion",
        'View "HbA1c and Blood Glucose Conversion User Guide"',
        "HbA1c in mmol/mol",
        "HbA1c in %",
        "Blood Glucose Conversion",
        "Glucose in mmol/L",
        "Glucose in mg/dL",
        "📚 In-Depth: HbA1c and Blood Glucose Conversion",
        "Compare imported glucometer readings (mg/dL) with domestic reports (mmol/L).",
        "Convert foreign-guideline thresholds (e.g. fasting 126 mg/dL) to 7.0 mmol/L for understanding.",
        "Unify units in diabetes follow-up.",
        "Fasting Glucose Conversion Example",
        "126 mg/dL ÷ 18 = 7.0 mmol/L, the diabetes fasting diagnostic cutoff; conversely 7.0 mmol/L × 18 = 126 mg/dL.",
        "Is the factor exact?",
        "18 is glucose's",
        "180 g/mol approximation (mg/dL→mmol/L divide by 18), enough for clinical comparison; papers use exact values.",
        "Can fingerstick and venous blood be compared?",
        "Values are close but not identical, and are affected by food; diagnosis uses venous plasma glucose.",
        "Can conversion diagnose diabetes?",
        "No, diagnosis needs repeated testing and OGTT/HbA1c synthesis, per guideline standards.",
        "About HbA1c and Blood Glucose Conversion",
        "A glucose mg/dL ↔ mmol/L conversion tool. For cross-system and report unification; pure conversion.",
        "Bidirectional Conversion",
        "Diagnostic Cutoff Compare",
        "Instant Display",
        "Imported Glucometer Compare",
        "Foreign Guideline Threshold",
        "Diabetes Follow-up",
    ]))
    write('csf-analysis', build('csf-analysis', [
        "CSF Routine Differentiator",
        "Enter CSF routine/biochemistry to differentiate purulent/tuberculous/viral meningitis.",
        "Enter CSF routine/biochemistry to differentiate purulent/tuberculous/viral meningitis; the tool computes and outputs results from the inputs.",
        'View "CSF Routine Differentiator User Guide"',
        "Appearance & Pressure",
        "Clear & Transparent",
        "Slightly Cloudy / Ground-glass",
        "Purulent Turbid",
        "Pressure (mmH2O)",
        "Cytology",
        "WBC (×10⁶/L)",
        "Polymorphonuclear %",
        "Protein (g/L)",
        "Glucose (mmol/L)",
        "Paired Blood Glucose (mmol/L)",
        "Chloride (mmol/L)",
        "Purulent Example",
        "Tuberculous Example",
        "Viral Example",
        "Key Differentiation of the Three Meningitides",
        "Purulent",
        "Tuberculous",
        "Viral",
        "Ground-glass",
        "Clear",
        "Pressure",
        "Cell Differential",
        "Mostly Polymorphs",
        "Mostly Lymphocytes",
        "Protein (g/L)",
        "↓↓ (markedly low)",
        "↓ (low)",
        "Chloride",
        "CSF differentiation needs synthesis: purulent shows 'high protein, low glucose, mostly polymorphs'; tuberculous shows 'low glucose/low chloride, mostly lymphocytes, moderate protein rise'; viral shows 'normal glucose, mostly lymphocytes, mild protein rise'. Final diagnosis needs microbiology (smear/culture/PCR) and clinical picture.",
        "📚 In-Depth: CSF Routine Differentiator",
        "Meningitis differentiation: compare CSF cell differential, glucose/chloride and protein patterns.",
        "Post-op or follow-up CSF routine rechecks.",
        "Teach CSF features of different meningitis types.",
        "Bacterial vs Viral CSF Example",
        "High neutrophils, markedly low glucose and high protein suggest purulent; high lymphocytes and near-normal glucose lean viral; correlate with smear and culture.",
        "Does low CSF glucose mean bacterial infection?",
        "Most common with pyogenic bacteria, but TB and fungi can also lower it; correlate with cells and microbiology.",
        "How to read lumbar-puncture pressure?",
        "Lateral recumbent normal is ~80–180 mmH2O; elevation suggests raised intracranial pressure etc., but is affected by position and anxiety.",
        "Can antibiotics be started on this?",
        "No, treatment is decided by the physician with imaging, culture and condition; this tool only explains indicators.",
        "About the CSF Routine Differentiator",
        "A CSF routine reference tool. Flags common patterns by pressure/cells/protein/glucose-chloride ranges; for review only.",
        "Multi-Parameter Range",
        "Pattern Hint",
        "Meningitis Differentiation",
        "Post-op Recheck",
        "Teaching: CSF Features",
    ]))
    write('electrophoresis-analysis', build('electrophoresis-analysis', [
        "Serum Protein Electrophoresis Band Analyzer",
        "Enter each protein band percentage and total protein to compute absolute values and analyze abnormal bands.",
        "Enter each protein band percentage and total protein to compute absolute values and analyze abnormal bands; the tool computes and outputs results from the inputs.",
        'View "Serum Protein Electrophoresis Band Analyzer User Guide"',
        "Total Protein TP (g/L)",
        "Albumin ALB (g/L, optional)",
        "Band Percentages (%)",
        "Albumin",
        "Alpha-1 Globulin",
        "Alpha-2 Globulin",
        "Beta Globulin",
        "Gamma Globulin",
        "Gamma zone has M-protein peak (monoclonal)",
        "Beta zone has M-protein peak",
        "Reference Ranges & Clinical Meaning",
        "Band",
        "Reference %",
        "Absolute Value",
        "Major Component",
        "↓: liver disease, kidney disease, inflammation; ↑: dehydration",
        "Alpha-1-antitrypsin",
        "↓: AAT deficiency; ↑: acute inflammation",
        "Haptoglobin, ceruloplasmin",
        "↑: acute inflammation, nephrotic syndrome",
        "Transferrin, C3",
        "↑: iron deficiency, hyperlipidemia; ↓: liver failure",
        "↑: polyclonal (infection/autoimmune); M peak (monoclonal)",
        "M-protein (monoclonal immunoglobulin):",
        "A narrow sharp peak (M peak) on electrophoresis occurs in multiple myeloma, monoclonal gammopathy of undetermined significance (MGUS) and Waldenstrom macroglobulinemia. Immunofixation electrophoresis (IFE) is needed to confirm the type.",
        "📚 In-Depth: Serum Protein Electrophoresis Band Analyzer",
        "In liver/kidney follow-up, watch Alb and globulin ratio changes.",
        "Screen for myeloma via a gamma-zone monoclonal band (M-protein).",
        "Teach electrophoresis pattern reading.",
        "Gamma-Zone Monoclonal Rise Example",
        "A narrow high M band in the gamma zone with low Alb: the tool suggests screening for plasma-cell disease (e.g. multiple myeloma) and advises immunofixation electrophoresis.",
        "Does an M-protein mean myeloma?",
        "Not necessarily; benign monoclonal gammopathy can also have it, but it must be differentiated; confirmation needs marrow, immunofixation and clinical data.",
        "Each band",
        "how is it computed?",
        "Multiply the scanned peak-area percentage by total protein to get absolute concentration, which is more intuitive.",
        "Can it replace immunofixation electrophoresis?",
        "No, routine electrophoresis only screens; monoclonal needs immunofixation to confirm typing.",
        "About the Serum Protein Electrophoresis Band Analyzer",
        "A serum-protein electrophoresis band analyzer. Computes each band percentage and flags low albumin/monoclonal rise; not a hematology substitute.",
        "Five-Band % Compute",
        "M-Protein Hint",
        "Absolute Concentration",
        "Liver/Kidney Follow-up",
        "Myeloma Screening",
        "Teaching: Patterns",
    ]))

if __name__ == "__main__":
    main()

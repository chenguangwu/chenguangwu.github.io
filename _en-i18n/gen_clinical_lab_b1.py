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
    write('autoantibody-interpretation', build('autoantibody-interpretation', [
        "Autoantibody Panel (ANA/ENA) Result Interpreter",
        "Enter ANA pattern and ENA antibody results to interpret clinical significance and related diseases.",
        "Autoantibody Panel Result Interpreter",
        "/ Autoantibody Panel Result Interpreter",
        'View "Autoantibody Panel (ANA/ENA) Result Interpreter User Guide"',
        "ANA (Antinuclear Antibody)",
        "ANA Titer",
        "ANA Pattern",
        "Homogeneous",
        "Speckled",
        "Nucleolar",
        "Centromere",
        "Nuclear Membrane",
        "Cytoplasmic",
        "ENA Antibody Panel",
        "Anti-dsDNA (ELISA, +/-)",
        "Anti-CCP Antibody (+/-)",
        "Interpret Results",
        "Interpretation Principles:",
        "A positive ANA (>1:80) suggests possible autoimmune disease and needs correlation with pattern and specific antibodies. Low-titer positives also occur in healthy people (elderly, infection, tumors). Antibody combinations are more diagnostic than a single antibody.",
        "📚 In-Depth: Autoantibody Panel (ANA/ENA) Result Interpreter",
        "In rheumatology clinics, correlate ANA titer with fluorescence pattern (e.g. homogeneous/speckled) to understand screening-positive meaning.",
        "When multiple ENA are positive, map each item to possible connective-tissue disease spectra.",
        "Demonstrate the report-reading logic of autoantibodies in teaching.",
        "Example: ANA 1:320 Speckled",
        "The tool notes 1:320 is a moderate titer and speckled is a common screening pattern; correlate with ENA/dsDNA and symptoms — do not diagnose lupus on this alone.",
        "Does a positive ANA mean lupus?",
        "No. Low-to-moderate ANA positivity also occurs in healthy people and other autoimmune diseases; confirmation needs antibody panel + clinical + biopsy.",
        "Is a higher titer always more severe?",
        "Titer indicates antibody amount but is not simply proportional to disease activity; trends and specific antibody types matter more.",
        "Can this tool issue a diagnostic report?",
        "No, it only explains items and aids review; the immunologist makes the final call.",
        "About the Autoantibody Panel Result Interpreter",
        "A structured prompt tool for autoantibody (ANA/ENA/dsDNA etc.) titers and patterns. It helps understand report items, needs clinical correlation, and does not replace diagnosis.",
        "Titer vs Fluorescence Pattern",
        "Multiple ENA Mapping",
        "Reference Hints",
        "Rheumatology First Read",
        "Antibody-Spectrum Mapping",
        "Teaching: Report Logic",
    ]))
    write('biochemistry-ratio', build('biochemistry-ratio', [
        "Biochemistry Ratio Calculator",
        "Compute liver/kidney function ratios such as AST/ALT (De Ritis) and BUN/Cr to aid etiologic differentiation.",
        "Core formulas (by input): ÷88.4); ×2.8; bun × 2.8",
        'View "Biochemistry Ratio Calculator User Guide"',
        "Liver Function Indicators",
        "ALT Alanine Aminotransferase (U/L)",
        "AST Aspartate Aminotransferase (U/L)",
        "ALP Alkaline Phosphatase (U/L)",
        "GGT Gamma-Glutamyl Transferase (U/L)",
        "Kidney Function Indicators",
        "BUN Urea Nitrogen (mmol/L)",
        "Cr Creatinine (μmol/L)",
        "UA Uric Acid (μmol/L)",
        "ALB Albumin (g/L)",
        "Clinical Significance of Ratios:",
        "• AST/ALT (De Ritis): <1 suggests acute viral hepatitis; >1 suggests alcoholic liver disease, chronic liver disease or cirrhosis",
        "• BUN/Cr (mmol/L ÷ μmol/L): ×1000 to convert; ratio >20 (converted) suggests prerenal azotemia; <10 suggests renal cause or low-protein diet",
        "• ALB/ALP: R factor assesses the type of drug-induced liver injury",
        "📚 In-Depth: Biochemistry Ratio Calculator",
        "In liver-disease follow-up, compute albumin/globulin (A/G) to gauge synthetic-function trend.",
        "For renal function or hyperparathyroidism, compute calcium-phosphorus product to assess ectopic-calcification risk.",
        "For metabolic acidosis, compute anion gap (AG) to distinguish high- vs normal-AG types.",
        "Anion Gap (AG) Example",
        "Na 140, Cl 104, HCO3 22: AG = 140 − (104+22) = 14, mildly elevated, suggesting possible high-AG metabolic acidosis; correlate with lactate/ketones.",
        "What does A/G below 1 indicate?",
        "Suggests reversed albumin/globulin ratio, common in liver/kidney disease, malnutrition or chronic inflammation; but review Alb and Glob values and trends.",
        "What is the normal AG range?",
        "Commonly 8–16 mmol/L (varies by formula/units); elevation indicates more unmeasured anions like lactate/ketones/uremia.",
        "Can an abnormal ratio be treated directly?",
        "No, the ratio is a clue; treat the underlying cause, decided by the physician.",
        "About the Biochemistry Ratio Calculator",
        "A calculator for biochemical ratios (A/G, Na/K, Ca×P, anion gap). Quickly flags protein/electrolyte imbalance patterns; for guidance only.",
        "One-Click Multi-Ratio",
        "Abnormal Highlight",
        "Liver Follow-up A/G",
        "Renal Ca×P Product",
        "Metabolic Acidosis AG Typing",
    ]))
    write('blood-gas-analysis', build('blood-gas-analysis', [
        "Blood Gas Compensation Evaluator",
        "Enter pH/PaCO2/HCO3- to classify acid-base disorder and assess compensation adequacy.",
        "Enter pH/PaCO2/HCO3- to classify acid-base disorder and assess compensation adequacy; the tool computes and outputs results from the inputs.",
        'View "Blood Gas Compensation Evaluator User Guide"',
        "Resp Acidosis Example",
        "Metabolic Acidosis Example",
        "Compensation Formulas:",
        "• Metabolic acidosis: PaCO2 = 1.5×HCO3 + 8 ± 2 (Winter's formula)",
        "• Metabolic alkalosis: PaCO2 = 0.7×HCO3 + 20 ± 5",
        "• Acute resp acidosis: HCO3 rise = 0.1×ΔPaCO2",
        "• Chronic resp acidosis: HCO3 rise = 0.35×ΔPaCO2",
        "• Acute resp alkalosis: HCO3 fall = 0.2×ΔPaCO2",
        "• Chronic resp alkalosis: HCO3 fall = 0.5×ΔPaCO2",
        "📚 In-Depth: Blood Gas Compensation Evaluator",
        "ICU/ER blood-gas check: enter pH, PaCO2, HCO3- to auto-classify primary and compensatory types.",
        "Teach the HCO3- compensation-range difference between acute vs chronic respiratory disorders.",
        "Pre-op assessment of electrolytes and acid-base status.",
        "Chronic Resp Acidosis Compensation Example",
        "pH 7.33, PaCO2 60, HCO3- 34: acidemia + high PaCO2 suggests respiratory acidosis; HCO3- rise fits chronic compensation (ΔHCO3 ≈ 0.35×ΔPaCO2), so chronic resp acidosis.",
        "Can compensation formulas directly diagnose mixed disorders?",
        "They can hint. If measured HCO3-/PaCO2 falls outside the simple-compensation expected range, suspect a mixed disorder and correlate clinically.",
        "Does sampling error matter much?",
        "Significantly. Air bubbles, non-airtight handling and delayed transport alter PaCO2/pH; if results look off, check sampling and transport first.",
        "Can this tool replace the arterial blood-gas report?",
        "No, it only rechecks the classification logic; the analyzer result and physician reading are final.",
        "About the Blood Gas Compensation Evaluator",
        "An acid-base disorder classifier. Uses pH/PaCO2/HCO3- and compensation formulas to type disorders, aiding report review; not a bedside substitute.",
        "Three-Factor Compensation",
        "Acute/Chronic & Mixed Hints",
        "ER/ICU Blood-Gas Check",
        "Teaching: Compensation Formulas",
        "Pre-op Assessment",
    ]))
    write('blood-routine-reference', build('blood-routine-reference', [
        "Blood Count Reference Range Lookup",
        "Look up reference ranges for RBC/WBC/Plt/HGB and other blood-count indicators, with multi-population groups.",
        'View "Blood Count Reference Range Lookup User Guide"',
        "Lists WBC/RBC/Hb/PLT reference ranges by age and sex and flags out-of-range items for first reading; ranges follow your lab, results for reference only.",
        "Select Indicator",
        "All Indicators",
        "Enter Measured Value (optional)",
        "Ranges are based on Clinical Laboratory Science and industry standard WS/T 405-2012. Instruments/reagents vary by lab; always follow the range printed on your report.",
        "📚 In-Depth: Blood Count Reference Range Lookup",
        "Children and adults have different Hb ranges; after entering age and sex, anemia is judged by the matching range.",
        "Track PLT/WBC trends in chemotherapy or chronic-disease follow-up.",
        "Demonstrate age-related range differences in teaching.",
        "Adult Female Hb Example",
        "Female Hb 110 g/L is below the common adult-female lower limit (~115 g/L); the tool flags it low, suggesting possible anemia and advising MCV and iron-metabolism workup.",
        "Are pregnant-women ranges the same?",
        "No; pregnancy physiology lowers the Hb floor, so use pregnancy-specific ranges.",
        "Is a slightly low single item serious?",
        "Mild shifts may reflect hydration, exercise or menstruation; persistent or multi-item abnormalities warrant further workup.",
        "Can this diagnose a blood disease?",
        "No, it only compares ranges; blood diseases need marrow/flow-cytometry and specialist tests.",
        "About the Blood Count Reference Range Lookup",
        "A blood-count reference-range lookup. Lists WBC/RBC/Hb/PLT ranges by age and sex and flags out-of-range items; ranges follow your lab.",
        "Age/Sex Range Mapping",
        "Out-of-Range Highlight",
        "Trend Hint",
        "Child/Adult Anemia Check",
        "Chemo Follow-up",
        "Teaching: Range Differences",
        "Enter Value to Flag Abnormality",
    ]))
    write('cardiac-marker-curve', build('cardiac-marker-curve', [
        "Cardiac Marker Trend Curve Analyzer",
        "Enter serial cTnI/cTnT values and times to plot a trend curve and analyze changes.",
        "Enter serial cTnI/cTnT values and times to plot a trend curve and analyze changes; the tool computes and outputs results from the inputs.",
        'View "Cardiac Marker Trend Curve Analyzer User Guide"',
        "Marker Type",
        "cTnI (Cardiac Troponin I)",
        "cTnT (Cardiac Troponin T)",
        "MYO (Myoglobin)",
        "Upper Reference (99th percentile)",
        "Time Points",
        "+ Add Time Point",
        "Analyze Curve",
        "Load AMI Example",
        "Cardiac Marker Kinetics:",
        "• cTnI/cTnT: rise 3–6h, peak 10–24h, persist 7–14 days; Δ (1h change) is valuable for early diagnosis",
        "• CK-MB: rise 3–8h, peak 12–24h, recover 48–72h, good for detecting reinfarction",
        "• MYO: rise 1–2h, peak 6–8h, recover 24h; high early sensitivity but low cardiac specificity",
        "📚 In-Depth: Cardiac Marker Trend Curve Analyzer",
        "For chest-pain patients, serial troponin at 0/3/6h to see a rise-then-fall pattern.",
        "In heart-failure follow-up, relate BNP trend to symptoms.",
        "Teach kinetic differences (cTn vs CK-MB time windows).",
        "Troponin 6h Trend Example",
        "0h 0.02, 3h 0.08, 6h 0.15 ng/mL (99th ~0.04): rising and above cutoff, fitting acute myocardial injury; correlate with ECG and clinical picture.",
        "Can a single normal troponin rule out MI?",
        "It may not have risen early; recheck at 3–6h is common; with typical symptoms, even a first normal should be monitored serially.",
        "Does high BNP mean heart failure?",
        "Not always; age, renal function and pulmonary hypertension can raise it; correlate clinically and with echo.",
        "Can it replace ECG and angiography?",
        "No, markers are only supportive; ACS diagnosis relies on ECG, angiography and physician synthesis.",
        "About the Cardiac Marker Trend Curve Analyzer",
        "A cardiac-marker time-series viewer. Shows cTn/CK-MB/BNP changes and 99th cutoffs to aid review; not a cardiology substitute.",
        "Time-Series Plot",
        "99th Cutoff Mark",
        "Rise-then-Fall Hint",
        "Chest-Pain 0/3/6h Monitor",
        "HF BNP Trend",
        "Teaching: Kinetics",
    ]))

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'nephrology')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'nephrology')
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
    out = {'slug': slug, 'industry': 'nephrology', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
DISCL_M = " A professional medical tool based on authoritative medical standards, for reference only."

def main():
    write('microalbuminuria', build('microalbuminuria', [
        "\U0001F4CB Morning Urine Microalbumin Evaluator",
        "Evaluate early kidney injury from morning urine albumin excretion, supporting multiple testing methods",
        "This tool performs professional calculations and outputs results based on the input parameters.",
        "Morning Urine Microalbumin Significance Evaluator",
        "/ Microalbumin Evaluator",
        "UACR (Albumin/Creatinine Ratio)",
        "Urine Albumin Concentration",
        "24h Urine Albumin Total",
        "UACR (mg/mmol, optional)",
        "Urine Albumin Concentration (mg/L)",
        "24h Urine Albumin Total (mg/d)",
        "Other / Health Check",
        "\U0001F4CB Microalbuminuria Diagnostic Criteria",
        "Microalbuminuria",
        "Macroalbuminuria",
        "24h Urine Albumin (mg/d)",
        "Morning Urine Albumin Concentration (mg/L)",
        "Diagnosing microalbuminuria requires at least 2 positive results out of 3 tests within 3-6 months, excluding interference from urinary tract infection, strenuous exercise, or heart failure.",
        "Note: Microalbuminuria is the earliest marker of diabetic kidney disease and also signals increased cardiovascular risk. ACEI/ARB agents can reduce proteinuria and delay renal function decline. For learning reference only." + DISCL_M,
        "\U0001F4DA Deep Dive: Microalbuminuria Assessment",
        "Diabetic Kidney Disease Screening",
        "Hypertensive Kidney Injury",
        "Morning Urine UACR",
        "30-300 indicates microalbuminuria \u2192 stage III diabetic kidney disease; initiate ACEI/ARB and control glycemia and blood pressure.",
        "UACR <30 is normal; diabetics/hypertensives should recheck annually.",
        "Why test for microalbumin?",
        "Appears before macroproteinuria; a sensitive marker of early kidney injury.",
        "What affects the result?",
        "Exercise/infection/hematuria can cause false positives; confirm with morning urine or repeat testing.",
        "About the Morning Urine Microalbumin Significance Evaluator",
        "The Morning Urine Microalbumin evaluator assesses early kidney injury from morning urine albumin concentration and UACR, used for early screening of diabetic and hypertensive kidney disease. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))
    write('nephrotic-syndrome', build('nephrotic-syndrome', [
        "\U0001FA7A Nephrotic Syndrome (Pathological Typing) Tool",
        "Interpret the pathological type and treatment direction of nephrotic syndrome from clinical features and pathological findings",
        "Nephrotic Syndrome (Pathological Typing) Tool",
        "/ Nephrotic Syndrome Typing Tool",
        "Children (<15 yr)",
        "Youth (15-40 yr)",
        "Middle age (40-65 yr)",
        "Elderly (>65 yr)",
        "Onset pattern",
        "Insidious onset",
        "Acute onset (post-infection)",
        "Rapidly progressive (rapid renal decline)",
        "Hematuria",
        "Hypertension",
        "Declining renal function",
        "Typical nephrotic syndrome (proteinuria \u22653.5 g/d + hypoalbuminemia)",
        "Basement membrane thickening / spikes",
        "Membranoproliferative (double contour)",
        "IgA mesangial deposits",
        "IgG granular along GBM",
        "Subepithelial spikes / deposits",
        "Steroid-sensitive",
        "Steroid-dependent",
        "Steroid-resistant",
        "\U0001F4CB Primary Nephrotic Syndrome Pathology Comparison",
        "Age predominance",
        "Steroid response",
        "Minimal change disease (MCD)",
        "90% sensitive",
        "Mesangioproliferative GN",
        "Young to middle age",
        "Mesangial deposits",
        "Partially sensitive",
        "Membranous nephropathy (MN)",
        "Middle-aged and elderly",
        "IgG along GBM",
        "All ages",
        "Segmental sclerosis",
        "Note: Diagnosing nephrotic syndrome requires heavy proteinuria (\u22653.5 g/d) and hypoalbuminemia (<30 g/L). Renal biopsy is the gold standard for defining pathology. Children with first-episode nephrotic syndrome may trial steroids first, with biopsy if unresponsive; adults should undergo biopsy early. For learning reference only." + DISCL_M,
        "\U0001F4DA Deep Dive: Nephrotic Syndrome Pathological Typing",
        "Age and onset",
        "Light microscopy / immunofluorescence",
        "Electron microscopy podocyte foot processes",
        "Middle-aged/elderly membranous nephropathy",
        "Middle-aged/elderly + membranous change + IgG granular deposits + subepithelial spikes \u2192 membranous nephropathy, match ~85%.",
        "Childhood minimal change disease",
        "Childhood + near-normal light microscopy + foot process effacement + immunonegative \u2192 minimal change disease, steroid-sensitive.",
        "What defines the typing?",
        "Light + immunofluorescence + electron microscopy triad, combined with age and onset rapidity.",
        "Why classify?",
        "Different pathologies require different treatments and prognoses, guiding immunosuppression strategy.",
        "About the Nephrotic Syndrome (Pathological Typing) Tool",
        "The Nephrotic Syndrome typing tool interprets primary and secondary nephrotic syndrome pathological types from clinical features, light microscopy, immunofluorescence, and electron microscopy. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))
    write('peritoneal-equilibrium', build('peritoneal-equilibrium', [
        "\U0001FA7A Peritoneal Equilibrium Test (PET) Typing Tool",
        "Assess peritoneal transport characteristics from standard PET results (4h D/P Cr and D/D0 Glu)",
        "This tool performs professional calculations and outputs results based on the input parameters.",
        "Peritoneal Equilibrium Test (PET) Typing Tool",
        "/ PET Typing Tool",
        "4h Dialysate Creatinine (\u03bcmol/L)",
        "Plasma Creatinine (\u03bcmol/L)",
        "4h Dialysate Glucose (mmol/L)",
        "Initial Dialysate Glucose (mmol/L)",
        "4h Dialysate/Plasma Albumin Ratio",
        "\U0001F4CB PET Classification (Twardowski)",
        "Peritoneal Transport Type",
        "High Transport (H)",
        "Fast solute clearance, fast glucose absorption",
        "High Average (HA)",
        "Good solute clearance",
        "Low Average (LA)",
        "Moderate solute clearance",
        "Low Transport (L)",
        "Slow solute clearance, less glucose absorption",
        "Note: Standard PET uses 2.5% glucose dialysate with a 4h dwell before sampling. High transporters suit short-dwell APD; low transporters suit long-dwell CAPD or consider hemodialysis. Recheck PET every 6-12 months to assess peritoneal function. For learning reference only." + DISCL_M,
        "\U0001F4DA Deep Dive: Peritoneal Equilibrium Test (PET)",
        "Dialysate/Plasma Creatinine Ratio",
        "Glucose Absorption",
        "Transport Typing",
        "4h D/P creatinine 0.65 \u2192 high average transport; choose short-dwell prescription.",
        "High glucose absorption",
        "Low D/D0 glucose \u2192 high transport; ultrafiltration relies on short dwell, avoid glucose overload.",
        "What does high transport mean?",
        "Fast solute clearance but ultrafiltration easily lost; adjust dwell time and concentration.",
        "How often to do it?",
        "Recheck PET when condition/prescription changes or ultrafiltration declines.",
        "About the Peritoneal Equilibrium Test (PET) Typing Tool",
        "The PET typing tool classifies peritoneal transport characteristics from the 4h dialysate/plasma creatinine ratio (D/P Cr) and the 4h dialysate/initial dialysate glucose ratio (D/D0 Glu). A professional medical tool based on authoritative medical standards, for reference only.",
        "How to Use the Peritoneal Equilibrium Test (PET) Typing Tool",
        "What does the PET typing tool do?",
        "How to use the PET typing tool?",
        "Which scenarios suit the PET typing tool?",
    ]))

if __name__ == '__main__':
    main()

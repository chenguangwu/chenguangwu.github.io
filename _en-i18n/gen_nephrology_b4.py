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
    write('jixingshensunshang-kdigo-fenqi', build('jixingshensunshang-kdigo-fenqi', [
        "\U0001F3E0 Acute Kidney Injury (KDIGO Staging)",
        "Based on KDIGO criteria, assess the acute kidney injury stage (stage 1/2/3) through the fold change of serum creatinine and urine output.",
        "Acute Kidney Injury (KDIGO Staging)",
        "/ Acute Kidney Injury (KDIGO Staging)",
        "Based on the KDIGO 2012 AKI guideline, the diagnosis is met if any one is satisfied: serum creatinine (Scr) rises \u22650.3 mg/dL within 48h; or Scr rises to \u22651.5 times baseline within 7d; or urine output <0.5 mL/kg/h for 6h. The stage is the most severe of:",
        "Stage 1",
        "=Scr 1.5\u20131.9\u00d7 baseline or rise \u22650.3;",
        "Stage 2",
        "Stage 3",
        "=Scr \u22653.0\u00d7 baseline or \u22654.0 mg/dL or urine output <0.3 for 24h / anuria for 12h.",
        "When no baseline Scr is available, back-calculate with a population estimation formula (e.g. based on eGFR).",
        "This tool is for clinical reference only and cannot replace physician judgment and laboratory review.",
        "Urine output in the last 6 hours (mL)",
        "Urine output in the last 12 hours (mL)",
        "Urine output in the last 24 hours (mL)",
        "Has renal replacement therapy (RRT) been started",
        "\U0001F9EE Calculate stage",
        "KDIGO acute kidney injury staging criteria",
        "Serum creatinine criteria",
        "Rises to 1.5-1.9\u00d7 baseline or rises \u226526.5 \u03bcmol/L",
        "<0.5 mL/kg/h for 6-12h",
        "Rises to 2.0-2.9\u00d7 baseline",
        "<0.5 mL/kg/h for \u226512h",
        "Rises to \u22653.0\u00d7 baseline or \u2265353.6 \u03bcmol/L or RRT started",
        "<0.3 mL/kg/h for \u226524h or anuria \u226512h",
        "Take the more severe of the serum creatinine and urine output criteria as the final stage.",
        "\u26A0\uFE0F AKI diagnosis requires Scr rising \u226526.5 \u03bcmol/L within 48h or rising to 1.5\u00d7 baseline within 7 days. This tool only assists staging and does not replace clinical judgment.",
        "\U0001F4DA In-depth analysis: acute kidney injury KDIGO staging",
        "Creatinine rise from baseline",
        "Urine output at 6/12/24h",
        "Indications for RRT",
        "Baseline 80, current 180",
        "Ratio 2.25 (\u22652.0) \u2192 AKI stage 2; urine output <0.5 mL/kg/h over the last 12h also supports it.",
        "Low urine output at 6h",
        "70 kg, urine 150 mL over last 6h (0.36 mL/kg/h<0.5) for 6\u201312h \u2192 stage 1.",
        "How does it differ from aki-kdigo?",
        "Both belong to KDIGO AKI staging; this tool has separate 6/12/24h urine output inputs.",
        "What is the definition of stage 3?",
        "Ratio \u22653.0 or rise \u2265354 \u00b5mol/L or RRT or eGFR<18 with an acute 50% drop \u2192 stage 3.",
        "Optional",
    ]))
    write('manager-1', build('manager-1', [
        "\U0001F3E0 Chronic Kidney Disease (CKD Staging) Management",
        "Compute eGFR with the CKD-EPI 2021 equation, perform GFR staging, albuminuria grading and CGA risk stratification",
        "\"Compute eGFR with the CKD-EPI 2021 equation, perform GFR staging, albuminuria grading and CGA risk stratification.\" Perform the professional calculation from the input parameters and output the result.",
        "Patient name/ID",
        "Serum creatinine Scr",
        "Cystatin C Scys (optional)",
        "Urine albumin/creatinine ratio ACR",
        "\U0001F50D Calculate eGFR & stage",
        "\U0001F4BE Save patient",
        "\U0001F4C2 Patient list",
        "Patient records",
        "\U0001F4CB CKD staging criteria (KDIGO 2024)",
        "GFR staging (G):",
        "G1: eGFR \u226590 (normal or increased)",
        "G2: eGFR 60-89 (mild decrease)",
        "G3a: eGFR 45-59 (mild-moderate decrease)",
        "G3b: eGFR 30-44 (moderate-severe decrease)",
        "G4: eGFR 15-29 (severe decrease)",
        "G5: eGFR <15 (kidney failure)",
        "Albuminuria staging (A):",
        "A1: ACR <30 mg/g (normal to mildly increased)",
        "A2: ACR 30-300 mg/g (moderately increased)",
        "A3: ACR >300 mg/g (severely increased)",
        "This tool uses the CKD-EPI 2021 equation (race-free version) to compute eGFR, for reference only",
        "Cannot replace clinical diagnosis; defer to nephrologist assessment",
        "CKD diagnosis requires eGFR<60 for >3 months, or kidney damage markers (albuminuria, etc.) for >3 months",
        "During acute kidney injury eGFR does not accurately reflect kidney function",
        "\U0001F4DA In-depth analysis: CKD staging management",
        "eGFR with multiple formulas",
        "Patient profile retention",
        "Risk and follow-up",
        "CKD-EPI 2021 gives G3a, ACR 30 \u2192 A2, moderate risk with annual follow-up.",
        "Combined formula",
        "The creatinine + cystatin C combined eGFR is more accurate, especially for patients with abnormal muscle mass.",
        "What is the management tool for?",
        "It can store multiple patients' Scr/cystatin C/ACR, with automatic staging and follow-up advice.",
        "What about ACR staging?",
        "A1<30, A2 30\u2013300, A3>300 mg/g (albuminuria).",
        "About \"Chronic Kidney Disease (CKD Staging) Management\"",
        "Enter serum creatinine (or cystatin C), age and sex, and use the CKD-EPI 2021 equation to compute eGFR, automatically performing GFR staging (G1-G5) and albuminuria grading (A1-A3), outputting CGA classification and risk stratification and providing follow-up advice. Supports patient record management.",
        "CKD-EPI 2021 equation",
        "Creatinine/cystatin C dual formula",
        "G1-G5 GFR staging",
        "A1-A3 albuminuria grading",
        "CGA risk heat map",
        "Patient record management",
        "Chronic kidney disease screening assessment",
        "Regular renal function follow-up",
        "Diabetic nephropathy management",
        "Hypertensive kidney damage monitoring",
        "e.g. Zhang San / P001",
        "e.g. 55",
        "e.g. 120",
        "e.g. 1.2",
        "e.g. 30",
    ]))

if __name__ == '__main__':
    main()

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
    write('proteinuria-24h', build('proteinuria-24h', [
        "\U0001F4CB Proteinuria (24h Quantification) Severity Assessor",
        "Enter the total 24-hour urine protein to assess the proteinuria grade and clinical significance",
        "Proteinuria (24h Quantification) Severity Assessor",
        "/ 24h Proteinuria Assessor",
        "24-hour urine protein grading: <0.15 g normal, 0.15\u20130.5 mild, 0.5\u20133.5 moderate, \u22653.5 g nephrotic-range proteinuria.",
        "Total 24h urine protein (g/d)",
        "24h urine volume (mL, optional)",
        "\U0001F4CB Proteinuria grading criteria",
        "24h urine protein (g/d)",
        "Physiological proteinuria",
        "Mild proteinuria",
        "Early or mild kidney injury",
        "Moderate proteinuria",
        "Significant glomerular injury",
        "Heavy proteinuria (nephrotic-range)",
        "Nephrotic syndrome range",
        "\U0001F4CB Diagnostic criteria for nephrotic syndrome",
        "Heavy proteinuria: \u22653.5 g/d (or \u22653.5 g/1.73m\u00b2/d)",
        "Hypoalbuminemia: serum albumin <30 g/L",
        "Edema: most patients have variable degrees of edema",
        "Hyperlipidemia: total cholesterol and triglycerides elevated",
        "Note: heavy proteinuria and hypoalbuminemia are the necessary conditions",
        "Note: 24h urine protein quantification is the gold standard for assessing proteinuria, but it is affected by urine collection accuracy. It is recommended to check UACR at the same time for cross-validation. Exercise, fever and orthostatic position can cause physiological proteinuria. This tool is for learning reference only.",
        "\U0001F4DA In-depth analysis: 24h urine protein quantification",
        "Quantitative severity",
        "Concentration conversion",
        "Nephrotic-range determination",
        "24h protein 1.5 g, urine volume 1500 mL \u2192 concentration about 1.0 g/L, not reaching the nephrotic range (<3.5 g).",
        "Nephrotic range",
        "\u22653.5 g/24h with hypoalbuminemia \u2192 nephrotic syndrome criteria, requiring pathological assessment.",
        "Incomplete urine collection?",
        "Insufficient collection days will underestimate it; a complete 24h collection with total volume recorded is recommended.",
        "What is the relationship with UPCR?",
        "UPCR \u2248 0.7 \u00d7 24h g/24h, usable as a screening substitute.",
        "About \"Proteinuria (24h Quantification) Severity Assessor\"",
        "24-hour urine protein quantification severity assessor: assesses the severity of proteinuria from the total 24h urine protein, supporting selective proteinuria and nephrotic syndrome judgment." + DISCL_M,
    ]))
    write('renal-anemia-epo', build('renal-anemia-epo', [
        "\U0001FA78 Renal Anemia (EPO) Dose Calculator",
        "Compute the erythropoietin dose and iron supplementation advice from the HGB target and body weight",
        "\"Compute the erythropoietin dose and iron supplementation advice from the HGB target and body weight.\" Perform the professional calculation from the input parameters and output the result.",
        "Renal Anemia (EPO) Dose Calculator",
        "/ EPO Dose Calculator",
        "Current hemoglobin HGB (g/L)",
        "Target hemoglobin (g/L)",
        "110 g/L (lower limit for dialysis patients)",
        "115 g/L (non-dialysis CKD)",
        "120 g/L (target upper limit)",
        "Dialyzer mode",
        "Hemodialysis (HD)",
        "Peritoneal dialysis (PD)",
        "Non-dialysis CKD",
        "Ferritin (\u00b5g/L, optional)",
        "Transferrin saturation TSAT (%, optional)",
        "\U0001F4CB Renal anemia treatment targets (KDIGO)",
        "HGB target (g/L)",
        "When to start EPO",
        "100-120 (not exceeding 130)",
        "HGB <100 (individualized)",
        "\U0001F4CB Iron status targets",
        "Target range",
        "Indications for supplementation",
        "\u2265200 (HD) / \u2265100 (non-dialysis)",
        "<500 generally no IV iron needed",
        "<20% iron supplementation needed",
        "Note: before EPO therapy, exclude other causes of anemia (bleeding, hemolysis, nutritional deficiency). The HGB rise rate is recommended at 10-20 g/L per month; too fast increases the risk of thrombosis and hypertension. HGB should not exceed 130 g/L. All CKD patients should have iron status assessed before using EPO. This tool is for learning reference only; follow medical advice for actual medication.",
        "\U0001F4DA In-depth analysis: renal anemia EPO dose",
        "Hemodialysis starting dose",
        "Peritoneal dialysis maintenance dose",
        "Iron status linkage",
        "Hgb 85, weight 60, hemodialysis",
        "Initial 50 IU/kg\u00d760=3000 IU per dose, 3 times a week = 9000 IU; effective only when iron is sufficient (ferritin\u2265200, TSAT\u226520).",
        "Maintenance dose",
        "After Hgb approaches target (100\u2013110), reduce to 30 IU/kg for maintenance, to avoid overshoot.",
        "Target Hgb?",
        "Both non-dialysis and dialysis recommend 100\u2013110 g/L, avoiding >130 to increase thrombosis risk.",
        "Why is iron important?",
        "With iron deficiency EPO is ineffective; correct iron to target first, then adjust EPO.",
        "About \"Renal Anemia (EPO) Dose Calculator\"",
        "Renal anemia EPO dose calculator: computes the recommended erythropoietin (EPO) dose and iron supplementation advice from the HGB target, current HGB and body weight." + DISCL_M,
    ]))
    write('renal-tubular-acidosis', build('renal-tubular-acidosis', [
        "\U0001FAD8 Renal Tubular Acidosis (RTA) Typing Tool",
        "Distinguish type I (distal), type II (proximal) and type IV RTA from blood gas, urine pH, electrolytes and other indicators",
        "\"Distinguish type I (distal), type II (proximal) and type IV RTA from blood gas, urine pH, electrolytes and other indicators.\" Perform the professional calculation from the input parameters and output the result.",
        "Renal Tubular Acidosis Typing Tool",
        "/ Renal Tubular Acidosis Typing Tool",
        "Blood pH",
        "Serum bicarbonate HCO\u2083\u207b (mmol/L)",
        "Urine pH (minimum)",
        "Serum potassium K\u207a (mmol/L)",
        "Urine anion gap (mmol/L)",
        "Fractional excretion of HCO\u2083\u207b FE-HCO\u2083\u207b (%)",
        "\U0001F4CB Comparison of RTA type features",
        "Type I (distal RTA)",
        "Type II (proximal RTA)",
        "Type IV RTA",
        "Defect site",
        "Distal tubule H\u207a excretion impaired",
        "Proximal tubule HCO\u2083\u207b reabsorption impaired",
        "Hypoaldosteronism/aldosterone resistance",
        "Serum potassium",
        "Hypokalemia (often <3.5)",
        "Hyperkalemia (often >5.0)",
        "Urine pH (during acidosis)",
        ">5.5 (cannot acidify)",
        "<5.5 (can acidify)",
        "<5.5 (usually)",
        "Urine anion gap",
        "Positive (+)",
        ">15% (often >30%)",
        "Kidney stones/calcification",
        "Rare",
        "Autoimmune disease, drugs, genetics",
        "Fanconi syndrome, drugs",
        "Diabetic nephropathy, drugs (spironolactone)",
        "Note: the core feature of RTA is normal anion gap metabolic acidosis (normal AG). Type I urine pH is always >5.5, type II urine pH may be <5.5 in severe acidosis, type IV is characterized by hyperkalemia. The bicarbonate loading test (FE-HCO\u2083\u207b) helps confirm the diagnosis. This tool is for learning reference only.",
        "\U0001F4DA In-depth analysis: renal tubular acidosis typing",
        "Metabolic acidosis + hyperchloremia",
        "Urine pH and potassium",
        "Anion gap",
        "Distal type I RTA",
        "pH 7.3, HCO\u2083 16, urine pH 6.5 (no acidification), hypokalemia \u2192 distal (type I) RTA.",
        "Proximal type II",
        "Low HCO\u2083, urine pH may be <5.5, high FE-HCO\u2083 \u2192 proximal (type II), often with other tubular disorders.",
        "What is the difference between I and II?",
        "Type I cannot acidify urine (pH>5.5), type II has impaired bicarbonate reabsorption (high FE-HCO\u2083).",
        "Notes on alkali supplementation?",
        "Correct acidosis with citrate/sodium bicarbonate; type I often needs potassium supplementation, monitor serum calcium.",
        "About \"Renal Tubular Acidosis Typing Tool\"",
        "Renal tubular acidosis (RTA) typing tool: distinguishes type I (distal), type II (proximal) and type IV RTA from blood gas analysis, urine pH, urine anion gap and other indicators." + DISCL_M,
    ]))
    write('shenxiaoqiulvguolv-24h-jiganqingchu-ccr', build('shenxiaoqiulvguolv-24h-jiganqingchu-ccr', [
        "\U0001FAD8 Glomerular Filtration Rate (24h Creatinine Clearance Ccr)",
        "Compute endogenous creatinine clearance (Ccr) from 24-hour urine creatinine concentration, urine volume and serum creatinine, corrected by body surface area (BSA).",
        "Core calculation formula (by input variables): (ucrM\u00d7vol)\u00f7(scrM\u00d71440); \u221a(h\u00d7w\u00f73600)",
        "Glomerular Filtration Rate (24h Creatinine Clearance)",
        "/ Glomerular Filtration Rate (24h Creatinine Clearance)",
        "\u26A0\uFE0F This tool is only for kidney function estimation and teaching assistance, and does not constitute a basis for kidney diagnosis. Decide staging and treatment in combination with physician assessment and test results.",
        "Serum creatinine concentration",
        "Serum creatinine unit",
        "24h urine creatinine concentration",
        "Urine creatinine unit",
        "\U0001F9EE Calculate clearance",
        "Ccr (mL/min) = (urine creatinine concentration \u00d7 24h urine volume) \u00f7 (serum creatinine concentration \u00d7 1440)",
        "BSA-corrected Ccr = Ccr \u00d7 (1.73 \u00f7 patient BSA)",
        "Body surface area BSA (Mosteller) = \u221a(height(cm)\u00d7weight(kg)\u00f73600)",
        "Unit conversion: serum creatinine 1 mg/dL = 88.4 \u03bcmol/L; urine creatinine 1 mg/dL = 0.0884 mmol/L (i.e. 1 mmol/L = 11.3 mg/dL)",
        "Normal reference: adults about 80-120 mL/min, slightly lower in women, declining about 6.5 mL/min per decade of age.",
        "\u26A0\uFE0F Accurate 24h urine collection is required; meat intake and strenuous exercise affect the result. In severe renal insufficiency Ccr overestimates GFR.",
        "\U0001F4DA In-depth analysis: 24h creatinine clearance Ccr",
        "GFR by urine collection method",
        "BSA correction",
        "Ccr=(8.8\u00d711.312\u00d71500/1000)/(80\u00d71440)=114.6 mL/min; CG=(140\u221240)\u00d765/(72\u00d70.905)=... BSA corrected to 1.73.",
        "CG formula",
        "CG=((140\u2212age)\u00d7kg)/(72\u00d7Scr), \u00d70.85 for women; rough dose estimate but biased high.",
        "What is the difference from creatinine clearance?",
        "This tool gives both Ccr and Cockcroft-Gault, the latter commonly used for dose adjustment.",
        "BSA correction?",
        "Ccr\u00d7(1.73/BSA) removes body size effect, standard.",
        "Body surface area",
        "How to use Glomerular Filtration Rate (24h Creatinine Clearance Ccr)",
        "What does Glomerular Filtration Rate (24h Creatinine Clearance Ccr) do?",
        "How do you use Glomerular Filtration Rate (24h Creatinine Clearance Ccr)?",
        "What scenarios is Glomerular Filtration Rate (24h Creatinine Clearance Ccr) suitable for?",
    ]))

if __name__ == '__main__':
    main()

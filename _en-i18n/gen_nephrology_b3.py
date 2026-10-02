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
    write('edema-grading', build('edema-grading', [
        "\U0001F4CB Edema (Pitting) Grading Tool",
        "Grading assessment based on pitting depth, recovery time and extent of edema",
        "Edema (Pitting) Grading Tool",
        "/ Edema Grading Tool",
        "Edema grading (by pitting depth): 1+ up to 2 mm mild, 2+ 2\u20134 mm moderate, 3+ 4\u20136 mm severe, 4+ 6 mm or more very severe; the cause is assessed together with the site and whether it is symmetrical.",
        "Pitting edema examination",
        "Pitting depth (mm)",
        "Pitting recovery time (seconds)",
        "Edema site",
        "Lower limbs/ankles",
        "Pretibial",
        "Face/eyelids",
        "Symmetrical on both sides",
        "Bilateral and symmetrical",
        "Unilateral/asymmetrical",
        "\U0001F4CB Grading criteria for pitting edema",
        "Pitting depth",
        "Immediate recovery",
        "Slight local edema",
        "Recovery in 10-15 seconds",
        "Recovery in over 30 seconds",
        "Deep pitting, limb swelling",
        "4+ very severe",
        "Recovery in over 1 minute",
        "Very deep pitting, skin tight and shiny",
        "\U0001F4CB Differential diagnosis of renal edema",
        "Nephritic edema",
        "Mechanism: decreased glomerular filtration rate, water and sodium retention",
        "Starting site: eyelids and face (obvious in the morning)",
        "Often accompanied by: hematuria, proteinuria, hypertension",
        "Common diseases: acute glomerulonephritis, rapidly progressive nephritis",
        "Nephrotic edema",
        "Mechanism: massive proteinuria \u2192 hypoalbuminemia \u2192 decreased plasma colloid osmotic pressure",
        "Starting site: lower limbs (milder in the morning, worse in the evening), may progress to the whole body",
        "Often accompanied by: massive proteinuria (\u22653.5 g/d), hypoalbuminemia, hyperlipidemia",
        "Common diseases: nephrotic syndrome (minimal change disease, membranous nephropathy, etc.)",
        "Cardiogenic/hepatic edema to be distinguished",
        "Cardiogenic: leg edema with jugular venous distension, hepatomegaly and heart failure signs",
        "Hepatic: mainly ascites, with abnormal liver function and low albumin",
        "Unilateral edema: deep vein thrombosis and lymphatic drainage disorders must be excluded",
        "Note: pitting edema is usually examined by pressing over the pretibial area or above the medial malleolus for 5 seconds. Record the pitting depth, recovery time and extent. Renal edema should be assessed together with urinalysis, renal function and plasma albumin." + DISCL_M,
        "\U0001F4DA In-depth analysis: pitting edema grading",
        "Leg edema assessment",
        "Pitting depth and recovery",
        "Bilateral symmetry",
        "Pitting 2 mm, recovery in 1 minute \u2192 grade 1 (mild) edema.",
        "Pitting >4 mm, recovery >2 minutes \u2192 grade 2\u20133, suggesting hypoalbuminemia or a cardiogenic/renal cause.",
        "What are the grading criteria?",
        "Grades 1\u20133 (or 1\u20134) by pitting depth in mm and recovery time in seconds.",
        "Unilateral edema?",
        "Unilateral edema warns of venous or lymphatic drainage obstruction rather than systemic disease.",
        "About \"Edema (Pitting) Grading Tool\"",
        "Edema (pitting) grading tool: grades edema by pitting depth, recovery time and extent, assessing the severity of renal edema and its differential diagnosis." + DISCL_M,
        "How to use the Edema (Pitting) Grading Tool",
        "What does the Edema (Pitting) Grading Tool do?",
        "Enter the pitting depth, rebound recovery time and extent of pitting edema, and grade severity by the standard scale (e.g. 1+ to 4+). Used to judge the degree of fluid retention in patients with heart failure, nephrotic syndrome and similar conditions.",
        "How do you use the Edema (Pitting) Grading Tool?",
        "What scenarios is the Edema (Pitting) Grading Tool suitable for?",
    ]))
    write('hematuria-source', build('hematuria-source', [
        "\U0001FA78 Hematuria (Dysmorphic Red Cells) Source Determinator",
        "Determine the source of hematuria from urine red cell morphology and clinical features: glomerular vs non-glomerular",
        "\"Determine the source of hematuria from urine red cell morphology and clinical features: glomerular vs non-glomerular.\" Perform the professional calculation from the input parameters and output the result.",
        "Hematuria (Dysmorphic Red Cells) Source Determinator",
        "/ Hematuria Source Determinator",
        "Urine red cell morphology analysis",
        "Urine red cell count (cells/\u03bcL)",
        "Proportion of dysmorphic red cells (%)",
        "Acanthocytes (G1 cells) (%)",
        "Urine protein (g/d)",
        "Accompanying findings",
        "Red cell casts",
        "Proteinuria (>0.5 g/d)",
        "Hypertension",
        "Frequency/dysuria",
        "Blood clots",
        "Flank pain/colic",
        "Determine the source",
        "\U0001F4CB Key points for distinguishing the source of hematuria",
        "Glomerular",
        "Non-glomerular",
        "Mainly dysmorphic red cells (\u226570%)",
        "Mainly normal red cells",
        "Acanthocytes (G1)",
        "Often present (>0.5 g/d)",
        "None or mild",
        "May be present",
        "Dysuria/frequency",
        "May be present (infection/stones)",
        "Glomerulonephritis, IgA nephropathy",
        "Stones, tumors, infection",
        "Note: hematuria is defined as \u22653 red cells per high-power field on urine sediment microscopy. Acanthocytes (G1 cells) \u22655% are highly specific for glomerular hematuria. Painless gross hematuria warrants vigilance for urinary tract tumors. This tool is for learning reference only.",
        "\U0001F4DA In-depth analysis: determining the source of hematuria",
        "Proportion of dysmorphic red cells",
        "Casts and protein",
        "Extrarenal signs",
        "Dysmorphic red cells 80%",
        "Dysmorphic (acanthocyte) red cells \u226580% \u2192 glomerular hematuria, suggesting nephritis.",
        "Clots + pain",
        "Gross hematuria with clots and flank pain \u2192 mostly urinary tract (stones/tumors) rather than glomerular.",
        "What is the significance of dysmorphic red cells?",
        "They are deformed by squeezing through the glomerular basement membrane, indicating a renal source.",
        "Which tests are needed?",
        "Urine red cell phase microscopy, urine protein/casts, imaging and cystoscopy, stratified by age.",
        "About \"Hematuria (Dysmorphic Red Cells) Source Determinator\"",
        "Hematuria (dysmorphic red cells) source determinator: determines the source of hematuria (glomerular vs non-glomerular) from urine red cell morphology, red cell count and accompanying findings." + DISCL_M,
    ]))
    write('index', build('index', [
        "\U0001FA7A Nephrology Tools",
        "Nephrology",
        "Nephrology Tools",
        "Renal Anemia (EPO) Dose Calculator",
        "Urine Electrolyte (Sodium, Potassium, Chloride) Excretion Calculator",
        "Enter blood and urine electrolytes to compute 24h urine sodium/potassium/chloride excretion and the fractional excretion FE, assess electrolyte balance and tubular reabsorption, and assist kidney disease diagnosis.",
        "Glomerular Filtration Rate (24h Creatinine Clearance) Calculator",
        "24-Hour Creatinine Clearance (Ccr) Calculator",
        "Urine Albumin-Creatinine Ratio (UACR) Calculator",
        "UACR Calculator: enter urine albumin and urine creatinine to obtain the ratio and compare it with the staging criteria.",
        "Diuretic (Furosemide-Hydrochlorothiazide) Converter",
        "Diuretic (Loop/Thiazide) Converter",
        "Glomerular filtration rate eGFR calculation",
        "Glomerular filtration rate eGFR (CKD-EPI)",
        "Dialysis (Kt/V) Adequacy Assessor",
        "Calcium-Phosphorus Product (Ca\u00d7P) Target Assessor",
        "Calcium-Phosphorus Product (Ca\u00d7P) Target Assessor",
        "Acute Kidney Injury (KDIGO Staging)",
        "Acute Kidney Injury (KDIGO Staging) Tool",
        "Acute Kidney Injury (AKI) KDIGO Staging Tool",
        "Chronic Kidney Disease (CKD Staging) Manager",
        "Compute eGFR with the CKD-EPI 2021 equation, perform GFR staging, albuminuria grading and CGA risk stratification",
        "Glomerular filtration rate (24h creatinine clearance)",
        "Vascular Calcification (Abdominal X-ray) Scoring Tool",
        "The vascular calcification scoring tool grades calcification of the anterior and posterior walls of the abdominal aorta at segments L1-L4 (0-3), totals 0-24 points and flags the severe threshold, assisting vascular calcification assessment in chronic kidney disease.",
        "Edema (Pitting) Grading Tool",
        "Enter the pitting depth, rebound recovery time and extent of pitting edema, and grade severity by the standard scale (e.g. 1+ to 4+). Used to judge the degree of fluid retention in patients with heart failure, nephrotic syndrome and similar conditions.",
        "Renal Tubular Acidosis Typing Tool",
        "Nephrotic Syndrome (Pathological Typing) Tool",
        "Enter clinical features such as massive proteinuria and hypoalbuminemia plus renal biopsy pathology findings to assist in interpreting the pathological type of nephrotic syndrome (e.g. membranous, minimal change) and give treatment direction hints. For reference by nephrologists.",
        "Proteinuria (24h Quantification) Severity Assessor",
        "Enter the total 24-hour urine protein value to classify normal, micro, moderate and heavy proteinuria and explain the clinical significance. Used for monitoring and severity assessment in patients with chronic kidney disease and nephritis.",
        "Urine Osmolality (Normal Value) and Concentration Assessor",
        "Enter the measured urine osmolality, compare it with the normal range to assess renal concentrating and diluting function, and support calculation of free water clearance (CH\u2082O). Used to judge diabetes insipidus and renal concentration disorders.",
        "Hematuria (Dysmorphic Red Cells) Source Determinator",
        "Determine the source of hematuria from urine red cell morphology and clinical features: glomerular vs non-glomerular",
        "Peritoneal Equilibration Test (PET) Typing Tool",
        "Peritoneal Equilibration Test (PET) Typing Tool",
        "Renal Biopsy (Light Microscopy/Immunofluorescence) Interpreter",
        "Renal Biopsy (Light Microscopy/Immunofluorescence) Interpreter",
        "Microalbuminuria (Morning Urine) Significance Assessor",
        "Enter the morning urine protein/creatinine ratio or urine albumin concentration, assess the significance of early kidney injury (microalbuminuria) in light of the test method, and note that repeated tests within 3\u20136 months are needed for confirmation. Used for diabetic/hypertensive nephropathy screening.",
        "About \"Nephrology Tools\"",
        "This collection of nephrology tools includes 23 free online tools covering the common calculations, conversions and lookups needed in nephrology. Whether you are a practitioner in the field, a student or an ordinary user, you will find ready-to-use utilities here. All tools run purely in the browser, data is not uploaded to any server, and your privacy and security are protected.",
        "The nephrology tools collected on this page include (some representative tools):",
        "These tools help you quickly complete common nephrology tasks: no need to memorize complex formulas or convert manually, just enter values and get results.",
        "Do the nephrology tools need to be downloaded or registered?",
        "No. All nephrology tools on this page are pure front-end online tools: open the page and use them directly. No software to install, no account to register, and no data is uploaded.",
        "Are the calculation results accurate? Is the data secure?",
        "The tools compute locally in your browser based on public mathematical formulas and common industry standards, with instant results. All calculations are performed on your own device and data is never uploaded to a server, so your privacy and security are guaranteed.",
    ]))

if __name__ == '__main__':
    main()

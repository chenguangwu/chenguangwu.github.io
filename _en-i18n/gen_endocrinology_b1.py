#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'endocrinology')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'endocrinology')
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
    out = {'slug': slug, 'industry': 'endocrinology', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
#!/usr/bin/env python3

def main():
    write('homa-ir', build('homa-ir', [
        "\u2697\uFE0F Insulin Resistance (HOMA-IR) Calculator",
        "Compute HOMA-IR (the steady-state model of insulin resistance) and HOMA-\u03B2 to assess insulin sensitivity and beta-cell function",
        "Core formulas (by input): (20 \u00D7 insulin) \u00F7 (fpg - 3.5); min(100, (homaIR \u00F7 8) \u00D7 100); (insulin \u00D7 fpg) \u00F7 22.5",
        "\U0001F4D6 See the \"Insulin Resistance (HOMA-IR) Calculator User Guide\"",
        "Fasting insulin (mIU/L)",
        "General population",
        "PCOS assessment",
        "Fatty liver assessment",
        "Insulin resistance example",
        "HOMA-IR assessment bands",
        "Insulin sensitivity",
        "High sensitivity",
        "Excellent insulin sensitivity",
        "Normal insulin sensitivity",
        "Needs attention, lifestyle intervention advised",
        "Insulin resistance",
        "Severe resistance",
        "Marked IR, high risk of T2DM/PCOS",
        "Note: in Chinese populations HOMA-IR \u22652.69 is often used as the insulin-resistance cut-off. Cut-offs vary by laboratory and population, so local standards are the reference.",
        "Clinical use of HOMA-IR across populations",
        "IR cut-off",
        "\u22652.5 or 2.69",
        "Indicates insulin resistance",
        "IR is the core pathology of PCOS and guides metformin treatment",
        "IR is a key driver of NAFLD",
        "Paediatric cut-offs are higher and need age-specific standards",
        "HOMA-IR = (fasting insulin \u00D7 fasting glucose) \u00F7 22.5",
        "HOMA-\u03B2 = (20 \u00D7 fasting insulin) \u00F7 (fasting glucose - 3.5)",
        "Glucose is in mmol/L and insulin in mIU/L. 22.5 is the conversion constant for a normal glucose of 3.5 mmol/L.",
        "Cautions:",
        "HOMA-IR applies to fasting assessment and is not suitable for type 1 diabetes, gestational diabetes or patients on insulin. HOMA-\u03B2 accuracy falls when hyperglycaemia is severe; an OGTT insulin release test or clamp study is better for marked hyperglycaemia. Fasting for 8-12 hours is required before the blood draw.",
        "\U0001F4DA In-depth analysis: Insulin Resistance (HOMA-IR) Calculator",
        "Stratifying insulin resistance in population cross-sectional metabolic studies.",
        "Tracking beta-cell function trends in prediabetes populations.",
        "Comparing insulin sensitivity before and after weight-loss or exercise intervention.",
        "HOMA model example",
        "Fasting glucose 5.8 mmol/L and fasting insulin 15 mU/L: HOMA-IR=(5.8\u00D715)/22.5=3.87 (indicating resistance); HOMA-\u03B2=(20\u00D715)/(5.8\u22123.5)=130% (beta cells still compensating). Values shift with the reagent and the population cut-off.",
        "Should HOMA-IR and HOMA-\u03B2 be read together?",
        "Yes. High HOMA-IR indicates resistance and high HOMA-\u03B2 means beta cells are still compensating; if beta-cell function declines while IR persists, this points towards impaired glucose tolerance or diabetes.",
        "What should be watched when using it in studies?",
        "Standardise the fasting conditions and the insulin assay method (RIA and CLIA results are not directly comparable), and report the source of the cut-off in the paper.",
        "About \"Insulin Resistance (HOMA-IR) Calculator\"",
        "HOMA-IR is the most widely used clinical index of insulin resistance and needs only fasting glucose and insulin, fitting the assessment of metabolic syndrome, PCOS and NAFLD.",
        "HOMA-IR and HOMA-\u03B2 together",
        "Cut-offs for several populations (general/PCOS/NAFLD)",
        "Beta-cell function assessment",
        "Graded interpretation and advice",
        "Metabolic syndrome assessment",
        "Insulin resistance diagnosis in PCOS",
        "NAFLD cause assessment",
    ]))

    write('frax-score', build('frax-score', [
        "\U0001F4CB Osteoporosis (FRAX) Fracture Risk Assessor",
        "Estimate 10-year major osteoporotic and hip fracture probability from the FRAX model to support treatment decisions",
        "Core formulas (by input): min(100, (hipFxProb \u00F7 30) \u00D7 100); min(35, majorFxProb \u00D7 0.30); min(60, baseScore \u00D7 2.2)",
        "\U0001F4D6 See the \"Osteoporosis (FRAX) Fracture Risk Assessor User Guide\"",
        "Femoral neck BMD T-score",
        "Any previous fracture",
        "Yes (adult fragility fracture)",
        "Clinical risk factors",
        "Parental history of hip fracture",
        "Currently smoking",
        "Glucocorticoids (prednisone \u22655mg/d for over 3 months)",
        "Rheumatoid arthritis",
        "Secondary osteoporosis (hypogonadism, hyperthyroidism, etc.)",
        "Excessive alcohol (\u22653 units/day)",
        "FRAX treatment thresholds and management",
        "10-year hip fracture probability",
        "Lifestyle intervention, no drug treatment needed",
        "Consider drug intervention, individualise the decision",
        "\u2265 10% hip / \u226520% major",
        "Antiosteoporotic drug treatment recommended",
        "Treatment thresholds (NOGG / Chinese guidelines):",
        "A hip fracture probability \u22653% or a major osteoporotic fracture \u226520% is the drug-treatment threshold. FRAX is more accurate with femoral neck BMD; if no BMD is given the risk-factor calculation is unaffected (treated as no BMD).",
        "\U0001F4DA In-depth analysis: Osteoporosis (FRAX) Fracture Risk Assessor",
        "Using FRAX to stratify 10-year fracture risk in postmenopausal women whose bone density T-score falls in the osteopenia range, to decide whether drug treatment is needed.",
        "Opportunistic fracture risk screening in patients on long-term oral glucocorticoids (such as prednisone \u22655 mg/day for more than 3 months).",
        "Screening community osteoporosis high-risk groups (low body weight, fall history, early menopause) and planning calcium/vitamin D advice.",
        "FRAX example for a 65-year-old woman",
        "Inputs: age 65, female,",
        "24, one previous fragility fracture, no parental hip fracture, non-smoker, no glucocorticoids, no alcohol. The tool returns the 10-year major osteoporotic and hip fracture probabilities and compares them with national intervention thresholds (such as \u226520% major or \u22653% hip) to suggest starting antiosteoporotic therapy alongside the BMD T-score.",
        "Who is FRAX for?",
        "It suits people aged 40-90 who have not started antiosteoporotic treatment; results are underestimated for those already treated. It does not replace bone density testing or overall clinical judgement.",
        "FRAX has no fall factor, so how should I use it?",
        "FRAX measures the intrinsic bone-strength fracture risk; anyone at high fall risk (older adults, neuromuscular disease) needs separate clinical assessment, and results near the threshold favour acting earlier.",
        "About \"Osteoporosis (FRAX) Fracture Risk Assessment\"",
        "FRAX is the fracture risk tool recommended by the WHO; it combines clinical risk factors with BMD to estimate 10-year fracture probability and support osteoporosis treatment decisions.",
        "Seven clinical risk factors integrated",
        "Hip and major fractures assessed together",
        "Drug intervention threshold check",
        "BMD-based grading",
        "Osteoporosis risk screening",
        "Antiosteoporotic drug decisions",
        "Postmenopausal women assessment",
        "Fracture prevention in older adults",
    ]))

    write('metabolic-syndrome', build('metabolic-syndrome', [
        "\U0001F9EC Metabolic Syndrome (ATP III) Quick Screener",
        "Based on the NCEP ATP III criteria (Chinese revision), meeting 3 of 5 items diagnoses metabolic syndrome",
        "\"Based on the NCEP ATP III criteria (Chinese revision), meeting 3 of 5 items diagnoses metabolic syndrome\" is computed from the input parameters and the result is reported.",
        "\U0001F4D6 See the \"Metabolic Syndrome (ATP III) Quick Screener User Guide\"",
        "Blood pressure - systolic (mmHg)",
        "Blood pressure - diastolic (mmHg)",
        "Triglycerides TG (mmol/L)",
        "Taking antihypertensive / antidiabetic / lipid-lowering drugs",
        "Yes (counted as an abnormality)",
        "Metabolic syndrome example",
        "Diagnostic criteria comparison",
        "ATP III (US)",
        "Chinese revision",
        "IDF (international)",
        "Waist (male)",
        "Waist (female)",
        "Triglycerides",
        "HDL-C (male)",
        "HDL-C (female)",
        "\u22653 of the 5 items",
        "Central obesity required plus 2 items",
        "*IDF waist cut-offs vary by ethnicity. This tool defaults to the Chinese revision.",
        "Why metabolic syndrome matters:",
        "In MS patients the risk of cardiovascular disease doubles and the risk of type 2 diabetes rises fivefold. The core pathology is insulin resistance and visceral obesity. Treatment rests on lifestyle intervention (5-10% weight loss, 150 min/week of aerobic exercise, a Mediterranean diet), bringing each component under target and using drugs when needed.",
        "\U0001F4DA In-depth analysis: Metabolic Syndrome (ATP III) Quick Screener",
        "Combined assessment of several borderline metabolic markers found at a health check.",
        "Cardiovascular risk stratification in prediabetes populations.",
        "Deciding on and following up lifestyle intervention (weight loss and exercise) indications.",
        "ATP III example",
        "Male, waist 95 cm, TG 2.0 mmol/L, HDL 0.9 mmol/L, blood pressure 135/88 mmHg, fasting glucose 6.0 mmol/L: all 5 of 5 items are met, so metabolic syndrome is diagnosed. Chinese waist cut-offs are commonly \u226590 cm for men and \u226585 cm for women.",
        "How do ATP III and the Chinese",
        "criteria differ?",
        "The core 5 items are the same; the abdominal obesity waist cut-off differs (China \u226590 cm men, \u226585 cm women) and the fasting glucose cut-off is often \u22655.6 mmol/L. Follow the domestic guideline clinically.",
        "What is the core of intervention?",
        "Start with lifestyle change: 5%-10% weight loss, regular aerobic exercise, better diet structure with less salt and sugar; when targets are hard to reach, use drugs as indicated to control each component.",
        "About \"Metabolic Syndrome (ATP III) Quick Screener\"",
        "Metabolic syndrome is a pathological state in which several cardiovascular and metabolic risk factors cluster, centred on insulin resistance and abdominal obesity. The ATP III criteria are a commonly used diagnostic tool.",
        "Item-by-item reading of the 5 criteria",
        "Chinese revision cut-offs",
        "Sex-specific criteria",
        "Cardiovascular risk assessment",
        "Health-check metabolic markers",
        "Cardiovascular risk screening",
        "Prediabetes detection",
        "Health management follow-up",
    ]))


if __name__ == '__main__':
    main()

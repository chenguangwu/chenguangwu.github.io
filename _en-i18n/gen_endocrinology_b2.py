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
    write('ogtt-interpretation', build('ogtt-interpretation', [
        "\U0001F9EC Glucose Tolerance (OGTT) Time-Point Interpreter",
        "Enter the blood glucose at each time point of an oral glucose tolerance test and get an automatic reading of diabetes or impaired glucose tolerance",
        "\"Enter the blood glucose at each time point of an oral glucose tolerance test and get an automatic reading of diabetes or impaired glucose tolerance\" is computed from the input parameters and the result is reported.",
        "\U0001F4D6 See the \"Glucose Tolerance (OGTT) Time-Point Interpreter User Guide\"",
        "75g OGTT (adult standard)",
        "100g OGTT (pregnancy)",
        "1h after glucose (mmol/L)",
        "2h after glucose (mmol/L)",
        "3h after glucose (mmol/L)",
        "Diabetes example",
        "Gestational diabetes example",
        "OGTT reading criteria comparison",
        "Fasting FPG",
        "2h glucose",
        "Normal glucose tolerance",
        "Impaired fasting glucose (IFG)",
        "Impaired glucose tolerance (IGT)",
        "Diabetes (DM)",
        "Unit: mmol/L. Refer to the WHO 1999 criteria.",
        "Gestational diabetes (GDM) diagnostic criteria - IADPSG/ADA",
        "75g OGTT; meeting any one item is enough to diagnose GDM:",
        "Glucose threshold (mmol/L)",
        "Equivalent mg/dL",
        "1h after glucose",
        "2h after glucose",
        "OGTT precautions:",
        "Eat normally for 3 days beforehand (at least 150g carbohydrate daily) with normal activity; fast 8-12 hours before the test; no smoking, eating or vigorous exercise during the test; drink 75g anhydrous glucose dissolved in 250-300ml water within 5 minutes.",
        "\U0001F4DA In-depth analysis: Glucose Tolerance (OGTT) Time-Point Interpreter",
        "Gestational diabetes (GDM) screening at 24-28 weeks of pregnancy.",
        "Confirming a diabetes diagnosis in people with borderline fasting glucose.",
        "Identifying impaired glucose tolerance (IGT) and its lifestyle intervention indications.",
        "OGTT reading example",
        "At 26 weeks with a 75g OGTT: fasting 5.3, 1h 9.8, 2h 8.8 mmol/L. IADPSG diagnoses if any one is met (fasting \u22655.1, 1h \u226510.0, 2h \u22658.5); this case meets 2 items, so GDM is diagnosed.",
        "Do the cut-offs differ in and out of pregnancy?",
        "Yes. Outside pregnancy the WHO criteria apply: 2h \u226511.1 indicates diabetes and 7.8-11.0 indicates IGT. In pregnancy IADPSG is stricter (any one of fasting \u22655.1, 1h \u226510.0, 2h \u22658.5 means GDM).",
        "How should I prepare before the test?",
        "At least 150g carbohydrate daily for 3 days before, 8-14 hours of fasting the night before, then no food, sitting quietly, no smoking or vigorous activity during the test, and draw the blood on time.",
        "About \"Glucose Tolerance (OGTT) Reading\"",
        "This oral glucose tolerance test (OGTT) reading tool supports both the adult 75g and the pregnancy 100g standards, reading each time point automatically and giving a diagnostic conclusion.",
        "Supports both WHO and IADPSG standards",
        "Point-by-point reading of normal/IFG/IGT/DM",
        "Dedicated gestational diabetes diagnosis",
        "Glucose curve visualisation",
        "Reading health-check OGTT reports",
        "Gestational diabetes diagnosis",
    ]))

    write('pcos-diagnosis', build('pcos-diagnosis', [
        "\U0001F50D Polycystic Ovary Syndrome (PCOS) Diagnostic Criteria Tool",
        "Assess PCOS from the Rotterdam criteria (2 of 3 required), with phenotype classification and metabolic risk stratification",
        "\"Assess PCOS from the Rotterdam criteria (2 of 3 required), with phenotype classification and metabolic risk stratification\" is computed from the input parameters and the result is reported.",
        "\U0001F4D6 See the \"Polycystic Ovary Syndrome (PCOS) Diagnostic Criteria Tool User Guide\"",
        "Diagnostic criteria",
        "Rotterdam criteria (2 of 3)",
        "NIH criteria",
        "AES criteria (hyperandrogenism required)",
        "Oligo-ovulation / anovulation",
        "Oligomenorrhoea (over 35 days) or amenorrhoea (no period for over 3 months)",
        "Menses per year",
        "Signs of hyperandrogenism",
        "Clinical hyperandrogenism (hirsutism Ferriman-Gallwey \u22658 / acne / alopecia)",
        "Biochemical hyperandrogenism (total testosterone over 60ng/dL or raised free testosterone)",
        "Total testosterone (ng/dL)",
        "F-G hirsutism score",
        "Polycystic ovarian morphology (PCOM)",
        "Ultrasound shows polycystic ovaries (unilateral/bilateral)",
        "Follicle count per ovary (2-9mm)",
        "Ovarian volume (mL)",
        "Excluding other causes",
        "Congenital adrenal hyperplasia excluded (17-OHP normal)",
        "Hyper/hypothyroidism, hyperprolactinaemia and Cushing excluded",
        "Typical PCOS",
        "Mild PCOS",
        "Comparison of the three diagnostic criteria",
        "2 of 3 items met",
        "4 phenotypes (A-D)",
        "Hyperandrogenism + ovulatory dysfunction (required)",
        "2 phenotypes (A, B)",
        "Hyperandrogenism required plus one more item",
        "3 phenotypes (A, B, D)",
        "PCOS phenotypes and metabolic risk",
        "Metabolic risk",
        "Type A (classic)",
        "Hyperandrogenism + ovulatory dysfunction + PCOM",
        "Highest (IR/MS/DM risk)",
        "Type B (classic)",
        "Type C (non-classic)",
        "Hyperandrogenism + PCOM",
        "Type D (ovulatory)",
        "Ovulatory dysfunction + PCOM",
        "PCOM ultrasound criteria:",
        "\u226520 follicles of 2-9mm diameter in one or both ovaries (updated in the 2023 international consensus, previously \u226512) and/or an ovarian volume \u226510mL. Perform the scan on cycle day 3-5, or at any time when amenorrheic.",
        "\U0001F4DA In-depth analysis: Polycystic Ovary Syndrome (PCOS) Diagnostic Criteria Tool",
        "Cause screening for oligomenorrhoea combined with acne or hirsutism.",
        "Judging ovulatory function and ovarian morphology during infertility workup.",
        "First-line screening for metabolic complications (insulin resistance, NAFLD).",
        "Rotterdam criteria example",
        "Oligomenorrhoea plus raised total testosterone plus bilateral polycystic ovarian changes on ultrasound (at least 12 small follicles per ovary): 2 of the 3 items are met, so PCOS is diagnosed (phenotype A or B); thyroid disease, hyperprolactinaemia and congenital adrenal hyperplasia must be excluded.",
        "How do the Rotterdam and Androgen Excess Society criteria differ?",
        "Rotterdam asks for 2 of 3 items and is therefore more sensitive; the AES criteria put hyperandrogenism at the centre. Both still require exclusion of other causes of hyperandrogenism or ovulatory dysfunction.",
        "What is the point of phenotype classification?",
        "Type A (ovulatory dysfunction, hyperandrogenism and PCOM all present) carries the highest metabolic risk and type D (ovulatory dysfunction plus PCOM) the lowest; the phenotype guides how intensive metabolic screening and fertility management should be.",
        "About \"Polycystic Ovary Syndrome (PCOS) Diagnostic Criteria\"",
        "PCOS is a common endocrine disease in women of reproductive age; the Rotterdam criteria (2 of 3 required) are the international standard, and other causes of hyperandrogenism must be excluded.",
        "Switch between three diagnostic criteria",
        "Automatic A-D phenotype classification",
        "Metabolic risk stratification",
        "Exclusion cause reminders",
        "Infertility assessment",
        "Differential diagnosis of hyperandrogenism",
        "Long-term PCOS management",
    ]))

    write('calcium-pth-axis', build('calcium-pth-axis', [
        "\U0001F9EC Calcium/PTH (Parathyroid) Feedback Axis Assessor",
        "Enter calcium and PTH levels together with phosphate and vitamin D to read the parathyroid feedback axis and its causes",
        "Core formulas (by input): ca + 0.02 \u00D7 (40 - alb)",
        "\U0001F4D6 See the \"Calcium/PTH (Parathyroid) Feedback Axis Assessor User Guide\"",
        "Serum total calcium (mmol/L)",
        "Reference population",
        "Primary hyperparathyroidism example",
        "Secondary hyperparathyroidism example",
        "Hypocalcaemia example",
        "Four-quadrant reading of the calcium-PTH axis",
        "High calcium + high PTH",
        "Primary hyperparathyroidism",
        "FHH (familial hypocalciuric hypercalcaemia)",
        "High calcium + low PTH",
        "Malignancy",
        "Vitamin D intoxication / granulomatous disease",
        "Low calcium + high PTH",
        "Secondary hyperparathyroidism",
        "Vitamin D deficiency",
        "Low calcium + low PTH",
        "Hypoparathyroidism",
        "Postoperative / autoimmune",
        "Calcium/PTH reference ranges",
        "Serum total calcium (corrected)",
        "Ionised calcium",
        "Serum phosphate (adult)",
        "Serum phosphate (child)",
        "\u2265 30 (sufficient)",
        "Corrected calcium formula:",
        "Correction is needed when albumin is below 40g/L.",
        "Corrected calcium = measured calcium + 0.02 \u00D7 (40 - albumin)",
        "Unit: mmol/L (albumin in g/L)",
        "\U0001F4DA In-depth analysis: Calcium/PTH (Parathyroid) Feedback Axis Assessor",
        "Differential diagnosis of hypercalcaemia (hyperparathyroidism versus malignancy/granulomatous disease).",
        "PTH assessment in the mineral and bone disorder of chronic kidney disease.",
        "Reading raised PTH alongside osteoporosis.",
        "Calcium-PTH axis examples",
        "Calcium 2.9 mmol/L (high after correction) with PTH 120 pg/mL (high) points to primary hyperparathyroidism; another case of calcium 2.0 with PTH 220 (high) points to secondary hyperparathyroidism (vitamin D deficiency or CKD). Low calcium with low PTH suggests hypoparathyroidism.",
        "Does calcium need correcting?",
        "Yes. A low albumin falsely lowers total calcium; the usual correction is corrected calcium = total calcium + 0.02\u00D7(40 \u2212 albumin g/L). Ionised calcium is more direct.",
        "How should PTH be read against calcium?",
        "High calcium with PTH that is not suppressed (still high) points to primary hyperparathyroidism; high calcium with suppressed PTH is usually non-parathyroid hypercalcaemia (malignancy, granulomatous disease).",
        "About \"Calcium/PTH (Parathyroid) Feedback Axis Assessor\"",
        "The parathyroid-calcium feedback axis is the central regulator of calcium and phosphate metabolism; this tool reads the axis state from corrected calcium, PTH, phosphate and vitamin D together.",
        "Automatic calcium correction for albumin",
        "Four-quadrant cause reading",
        "Vitamin D status assessment",
        "Differential diagnosis check suggestions",
        "Differential diagnosis of hypercalcaemia",
        "Hyper/hypoparathyroidism diagnosis",
        "CKD-MBD management",
        "Metabolic bone disease assessment",
        "How to use the Calcium/PTH (Parathyroid) Feedback Axis Assessor",
        "To differentiate the causes of hypercalcaemia (primary hyperparathyroidism versus malignancy/granulomatous disease) and disorders of calcium and phosphate metabolism such as secondary hyperparathyroidism in chronic kidney disease.",
        "What does the Calcium/PTH (Parathyroid) Feedback Axis Assessor do?",
        "How do I use the Calcium/PTH (Parathyroid) Feedback Axis Assessor?",
        "Which scenarios suit the Calcium/PTH (Parathyroid) Feedback Axis Assessor?",
    ]))


if __name__ == '__main__':
    main()

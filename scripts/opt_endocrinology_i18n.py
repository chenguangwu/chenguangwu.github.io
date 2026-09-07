#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清除 endocrinology 在 _en_override.json / slug-en.json 中 ed 字段的英文套话，
补真实专业英文标题(en)与描述(ed)。ind 字段保留不变。
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# slug -> (en 英文标题, ed 英文描述) 真实专业内容，不含套话
EN = {
"frax-score": ("FRAX Fracture Risk Assessment", "Estimate 10-year major osteoporotic and hip fracture probability with the WHO FRAX model from age, BMI, fracture history and lifestyle factors."),
"insulin-adjustment": ("Insulin Dose Adjustment", "Estimate correction or meal-time insulin dose from current and target glucose using an insulin sensitivity factor (1800/1700/2200 rule) or carb ratio (500 rule)."),
"short-stature-prediction": ("Adult Height Prediction (Target Height)", "Estimate mid-parental target height and adult height range from parents' heights and child sex, with bone-age context for short-stature screening."),
"glycated-albumin": ("Glycated Albumin (GA) Calculator", "Compute glycated albumin percentage from glycoalbumin and serum albumin, reflecting about 2-4 weeks of mean glycemia for anemia, pregnancy or dialysis."),
"homa-ir": ("HOMA-IR Calculator", "Calculate HOMA-IR and HOMA-beta from fasting glucose and insulin to quantify insulin resistance and beta-cell compensation in research or clinics."),
"mage-index": ("MAGE (Mean Amplitude of Glycemic Excursions)", "Compute MAGE from continuous glucose monitoring data after excluding fluctuations below 1 SD, quantifying glycemic variability."),
"aldosterone-renin": ("Aldosterone-Renin Ratio (ARR)", "Calculate the aldosterone-to-renin ratio to screen for primary aldosteronism; a positive ratio requires confirmatory testing."),
"metabolic-syndrome": ("Metabolic Syndrome Assessment (ATP III)", "Apply the ATP III criteria (waist, lipids, blood pressure, glucose) to classify metabolic syndrome when 3 of 5 components are met."),
"graves-trab": ("TRAb (TSH Receptor Antibody) Test", "Interpret thyrotropin receptor antibody results for Graves' disease diagnosis, relapse prediction after antithyroid drugs, and pregnancy risk."),
"pcos-diagnosis": ("PCOS Diagnosis (Rotterdam Criteria)", "Apply the Rotterdam criteria (oligo-ovulation, hyperandrogenism, polycystic ovaries; 2 of 3) and assign A/B/C/D phenotypes after excluding other causes."),
"pituitary-tumor": ("Pituitary Adenoma Evaluation", "Evaluate pituitary adenoma phenotype and mass effect from prolactin, GH/IGF-1, ACTH, cortisol and visual symptoms to guide workup."),
"thyroid-cancer-risk": ("Thyroid Nodule Cancer Risk", "Estimate malignant risk of a thyroid nodule from ultrasound features, size and suspicious nodes, with FNA indication guidance."),
"whipple-triad": ("Whipple's Triad (Insulinoma)", "Assess Whipple's triad (hypoglycemic symptoms, glucose <2.8 mmol/L, relief after glucose) for insulin-mediated hypoglycemia such as insulinoma."),
"catecholamine-test": ("Catecholamine Metabolism Test", "Interpret 24-hour urine VMA/HVA and plasma/urine fractionated catecholamines for pheochromocytoma and paraganglioma screening."),
"gh-stimulation-test": ("GH Stimulation Test", "Interpret growth hormone stimulation test peaks (arginine/clonidine/insulin) against cutoffs to assess growth hormone deficiency."),
"ogtt-interpretation": ("OGTT Interpretation", "Interpret the 75 g oral glucose tolerance test by WHO and IADPSG (pregnancy) criteria for diabetes, IGT and gestational diabetes."),
"sex-hormone-cycle": ("Sex Hormone Cycle Interpretation", "Match LH/FSH/E2/P/T/PRL values to follicular, ovulatory or luteal reference ranges by cycle day for ovarian and ovulation assessment."),
"ti-rads": ("ACR TI-RADS Scoring", "Score thyroid nodule ultrasound features (composition, echogenicity, shape, margins, echogenic foci) for malignant risk and FNA/follow-up guidance."),
"cortisol-rhythm": ("Cortisol Rhythm & Suppression", "Assess circadian cortisol rhythm and dexamethasone suppression for Cushing syndrome screening versus pseudo-Cushing."),
"calcium-pth-axis": ("Calcium-PTH Axis Evaluation", "Use calcium, phosphate and PTH to differentiate primary, secondary and tertiary hyperparathyroidism and vitamin D deficiency."),
"cycle-hormone": ("Cycle Hormone Interpretation", "Map sex hormone levels to the menstrual phase by cycle day and interpret follicular/ovulatory/luteal patterns for ovulation tracking."),
"detector-metabolism": ("Catecholamine Metabolite Detection", "Interpret 24-hour urine VMA/HVA and blood catecholamines against reference ranges for catecholamine-secreting tumors."),
}

def update(fn):
    p = os.path.join(ROOT, fn)
    d = json.load(open(p, encoding="utf-8"))
    n = 0
    for slug, (en, ed) in EN.items():
        key = "endocrinology/" + slug
        if key not in d:
            d[key] = {}
        d[key]["en"] = en
        d[key]["ed"] = ed
        n += 1
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return n

def main():
    for fn in ["i18n/tools/slug-en.json", "i18n/tools/_en_override.json"]:
        n = update(fn)
        print(f"{fn}: 更新 {n} 个")
    # 校验无套话
    bad = []
    for fn in ["i18n/tools/slug-en.json", "i18n/tools/_en_override.json"]:
        d = json.load(open(os.path.join(ROOT, fn), encoding="utf-8"))
        for k, v in d.items():
            if k.startswith("endocrinology/") and "free online tool" in (v.get("ed") or "").lower():
                bad.append((fn, k))
    print("残留套话:", bad if bad else "无")

if __name__ == "__main__":
    main()

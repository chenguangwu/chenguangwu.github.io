#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""healthcare 第7批：gfr-cockcroft / body-fat-estimator / bac-calculator / ibw"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'healthcare')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'healthcare')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        for i, it in enumerate(items):
            print('   ', i, repr((it.get('zh') or '')[:50]))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    return mp


def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'healthcare', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))


# ---------------- gfr-cockcroft (18) ----------------
write('gfr-cockcroft', build('gfr-cockcroft', [
    "🫘 Cockcroft-Gault Creatinine Clearance Calculator",
    "Estimate creatinine clearance with the Cockcroft-Gault equation from age, weight, sex and serum creatinine, the estimate still used for many renal drug dose adjustments.",
    '📖 View the "GFR Creatinine Clearance Cockcroft User Guide"',
    "CrCl = (140 − age) × weight / [72 × (serum creatinine µmol/L ÷ 88.4)] × sex factor (female 0.85)",
    "Female ×0.85",
    "For drug dose adjustment.",
    "📚 Deep Dive: Cockcroft-Gault Creatinine Clearance",
    "Dose adjustment: use CrCl to adjust for patients with kidney disease",
    "drug dose",
    "Initial renal assessment: a quick clinical estimate of creatinine clearance",
    "Teaching demo: understand the formula and ",
    "Algorithm (standard Cockcroft-Gault): CrCl = (140−age) × weight (kg) ÷ (72 × SCr_mg/dL) × (female ×0.85), in mL/min; body-surface normalised CrCl × 1.73/BSA. The implementation on this tool's page omits the division by 72, so the displayed value is about 72 times the standard (e.g. roughly 6961 mL/min by default, clearly distorted); the standard value is given below.",
    "Worked example (standard value)",
    "Example 1 (age 50, 70 kg, serum creatinine 80 µmol/L = 0.905 mg/dL, male): CrCl = (140−50)×70 ÷ (72×0.905) = 96.7 mL/min. Example 2 (age 65, 60 kg, 120 µmol/L = 1.357 mg/dL, female): CrCl = (140−65)×60 ÷ (72×1.357) × 0.85 = 39.1 mL/min (low, indicating reduced kidney function).",
    "What is the difference between CrCl and eGFR?",
    "CrCl is estimated by Cockcroft-Gault in mL/min and is commonly used for dosing; eGFR is estimated by CKD-EPI, body-surface normalised to mL/min/1.73 m², and is commonly used for CKD staging. The two are close but not identical.",
    "Why is this tool's number unusually large?",
    "The implementation omits the /72 divisor of the standard formula, so the result is about 72 times the true value; rely on the standard Cockcroft-Gault formula (with /72), or use the site's eGFR tool instead.",
]))

# ---------------- body-fat-estimator (18) ----------------
write('body-fat-estimator', build('body-fat-estimator', [
    "🏋️ Body Fat Percentage Estimator",
    "Estimate body fat percentage from waist, neck, hip and height using the US Navy circumference method, with the sex-specific formula and fitness band shown.",
    '📖 View the "Body Fat Percentage Estimation User Guide"',
    "BF% = 1.2·BMI + 0.23·age − 10.8·sex (male 1) − 5.4",
    "The Deurenberg formula, for rough estimation only.",
    "📚 Deep Dive: Body Fat Percentage Estimation (Deurenberg)",
    "Body composition tracking: from ",
    ", age and sex, estimate the ",
    "body fat percentage",
    ", to support fat loss",
    'Fitness reference: look at fat, not weight alone, to avoid being "light but fat"',
    "Education: understand how age and sex affect body fat",
    "Algorithm (Deurenberg): body fat % = 1.2×BMI + 0.23×age − 10.8×(male 1 / female 0) − 5.4; BMI = weight ÷ height². All values must be >0. A rough estimate with an error of about ±3.5%.",
    "Example 1 (65 kg / 170 cm / age 30 / male): BMI = 22.5, body fat = 1.2×22.5 + 0.23×30 − 10.8 − 5.4 = 17.7%. Example 2 (55 kg / 160 cm / age 40 / female): BMI = 21.5, body fat = 1.2×21.5 + 0.23×40 − 0 − 5.4 = 29.6%.",
    "Is the estimate accurate?",
    "The formula has a fairly large error and is only for trend reference; more accurate methods are skinfold thickness, bioelectrical impedance (BIA) and DXA (dual-energy X-ray). Gym-goers with a lot of muscle tend to have their body fat overestimated.",
    "Why do the male and female formulas differ?",
    "At the same BMI, men have less essential fat than women, so the formula corrects for sex with −10.8 (male) / 0 (female); healthy body fat for women is usually higher than for men.",
]))

# ---------------- bac-calculator (18) ----------------
write('bac-calculator', build('bac-calculator', [
    "🧮 Blood Alcohol Content Calculator",
    "Estimate blood alcohol concentration from the number of standard drinks, body weight, sex and elapsed hours, applying the Widmark factor and hourly elimination rate.",
    '📖 View the "Blood Alcohol Content BAC User Guide"',
    "Drink volume (mL)",
    "Alcohol by volume (%)",
    "Hours since drinking",
    "Widmark: BAC = A/(r·W) − β·t; A = volume × ABV × 0.789 (g)",
    "r is 0.68 for men / 0.55 for women, β ≈ 0.015/h. Do not drink and drive; this result is for reference only.",
    "📚 Deep Dive: Blood Alcohol Content BAC (Widmark Formula)",
    "Drink-driving awareness: estimate BAC from volume, ABV, body weight and sex to judge whether the limit is exceeded",
    'Health education: see metabolism fall over time and understand the "morning-after" risk',
    "Safety boundary: a reminder that individual variation is large and the result is only for awareness",
    "Algorithm: BAC = max(0, drink volume (mL) × ABV × 0.789 ÷ (distribution factor r × weight kg) − 0.015 × hours); r = 0.68 for men and 0.55 for women, 0.789 is the density of ethanol and 0.015 is the elimination rate in g/100mL/h. All values must be ≥0.",
    "Example 1 (350 mL × 5% × 70 kg male, 2h): (350×0.05×0.789)/(0.68×70) − 0.03 = 0.260 g/100mL (far above the driving limit of 0.02). Example 2 (500 mL × 4% × 60 kg female, 3h): (500×0.04×0.789)/(0.55×60) − 0.045 = 0.433 g/100mL.",
    "What is 0.789?",
    "The density of ethanol (g/mL), used to convert volume × ABV into pure alcohol mass; ABV is used as a decimal (5% = 0.05).",
    "Can the result be used as legal evidence?",
    "No; individual variation (stomach contents, metabolic enzymes, body build) is large. It is only for health and legal awareness, and whether you are over the limit is determined by a breath or blood test.",
]))

# ---------------- ibw (18) ----------------
write('ibw', build('ibw', [
    "⚖️ Ideal Body Weight Calculator",
    "Estimate ideal body weight from height and sex with the Devine and Robinson formulas, and display the healthy weight range and adjusted body weight for dosing.",
    '📖 View the "Ideal Body Weight IBW (Devine Formula) User Guide"',
    "Male IBW = 50 + 0.91×(height cm − 152.4)",
    "Female IBW = 45.5 + 0.91×(height cm − 152.4)",
    "Commonly used as a reference for drug dose adjustment.",
    "📚 Deep Dive: Ideal Body Weight IBW (Devine Formula)",
    "Dosing baseline: clinically, many ",
    "drug doses",
    "Nutritional support: mechanical ventilation tidal volume, etc., are set by IBW",
    "Reference value: IBW is a clinical baseline, not a healthy-weight standard",
    "Algorithm (Devine): male IBW = 50 + 0.91×(height cm−152.4); female IBW = 45.5 + 0.91×(height cm−152.4); upper = IBW×1.1, lower = IBW×0.9. Height must be >0.",
    "Example 1 (170 cm, male): IBW = 50 + 0.91×17.6 = 66.0 kg, range 59.4-72.6 kg. Example 2 (160 cm, female): IBW = 45.5 + 0.91×7.6 = 52.4 kg, range 47.2-57.7 kg.",
    'Is IBW a "standard weight"?',
    "It is not a health judgement but a reference baseline for clinical calculation (especially dosing and ventilator parameters); the actual ",
    "varies from person to person, and it is normal for a muscular person to have a low IBW.",
    "For obese patients, dose by IBW or actual body weight?",
    "It depends on the drug and guideline: lipophilic or widely distributed drugs may use adjusted body weight, while water-soluble drugs or those designed by IBW use IBW; follow the specific drug label and clinical decision.",
]))

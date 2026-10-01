#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cosmetic-derm 第7批：sebumeter / skin-ph / spf-pa-calculator / telangiectasia-area"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'cosmetic-derm')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'cosmetic-derm')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        for i, it in enumerate(items):
            print('   ', i, repr((it.get('zh') or it.get('zh_src', ''))[:50]))
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
    out = {'slug': slug, 'industry': 'cosmetic-derm', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))


# ---------------- sebumeter (47) ----------------
write('sebumeter', build('sebumeter', [
    "\U0001F9B4 Sebumeter Sebum Output Assessor",
    "Based on Sebumeter readings (μg/cm²), assess regional sebum secretion levels and classify skin type.",
    "Sebum Output Assessor",
    "/ Sebum Output Assessor",
    '\U0001F4D6 View the "Sebumeter Sebum Output Assessor User Guide"',
    "Regional sebum readings (μg/cm²)",
    "T-zone = (forehead + nose) / 2; U-zone = (cheek + chin) / 2; temperature-corrected mean = overall mean × (1 − (temperature − 25) × 0.01)",
    "Sebum secretion rises ~10% per 1 °C, so a reverse correction is applied against the standard 25 °C. Combination skin: |T-zone − U-zone| > 60 μg/cm², with T/U zones classified separately. Skin grading: <70 dry, <120 normal, <180 mildly oily, ≥180 oily. Used to convert multi-site Sebumeter readings and determine skin type.",
    "Forehead",
    "Nose",
    "Cheek",
    "Chin",
    "Measurement time point",
    "30 min after cleansing",
    "2 h after cleansing",
    "4 h after cleansing",
    "8 h after cleansing (full day)",
    "\U0001F9B4 Sebumeter Grading Standard (μg/cm²)",
    "Reference values based on 2 h post-cleanse measurement (T-zone)",
    "Sebum value",
    "Skin type",
    "Dry",
    "Tight, prone to flaking",
    "Slightly dry / normal",
    "Comfortable, occasional tightness",
    "Balanced",
    "Mildly oily",
    "Afternoon shine",
    "Oily",
    "Noticeably greasy",
    "Extremely oily",
    "Whole-face greasy, enlarged pores",
    "\u26A0\uFE0F Sebum secretion is affected by season, temperature, hormones and more; measure several times and average. For skincare reference only.",
    "\U0001F4DA Deep Dive: Sebumeter Sebum Output Assessor",
    "Oil-acne control: a high T-zone value suggests stronger oil control and moderate acids.",
    "Product test: compare readings before and after 4 weeks of an oil-control product to see if it meets the goal.",
    "Zonal care: high T-zone, normal U-zone suggests zonal skincare.",
    "T-zone sebum on the high side",
    "Input: T-zone reading high, U-zone normal → classify as oily zoning; recommend T-zone oil control + salicylic acid, U-zone hydration without stacking.",
    "Does high sebum mean dirty?",
    "No. Sebum is a normal part of the barrier; only excess needs management.",
    "Are the readings accurate?",
    "Affected by time of day and post-cleanse wait; measure under fixed conditions for stability.",
    "Can it diagnose acne?",
    "No. Sebum reference only; see a dermatologist for acne.",
    'About "Sebum Output Assessor"',
    "Sebumeter sebum output assessor: assess skin sebum secretion online and determine dry / normal / oily skin type. A medical professional tool based on authoritative medical standards; for reference only.",
]))

# ---------------- skin-ph (41) ----------------
write('skin-ph', build('skin-ph', [
    "\U0001F9AA Skin pH (Normal 4.5\u20135.5) Meter",
    "Enter a skin pH reading to assess acid-base balance and barrier health (normal range 4.5\u20135.5).",
    "Skin pH Meter",
    "/ Skin pH Meter",
    '\U0001F4D6 View the "Skin pH (Normal 4.5\u20135.5) Meter User Guide"',
    "pH reading",
    "Measurement site",
    "Axilla",
    "Time after cleansing before measurement",
    "Just cleansed (inaccurate)",
    "15\u201330 min after cleansing",
    "1\u20132 h after cleansing",
    "Current skincare state",
    "Bare / unmoisturized",
    "Products applied",
    "\U0001F4CB Skin pH Grading and Meaning",
    "pH range",
    "Excessively acidic",
    "Possible barrier damage, stinging",
    "Slightly acidic (low normal)",
    "Healthy, intact acid mantle",
    "Healthy barrier, balanced flora",
    "Slightly alkaline (high)",
    "Weakened barrier, prone to dryness and sensitivity",
    "Damaged barrier, dry and flaky",
    "Severe barrier injury",
    "\u26A0\uFE0F Skin pH is affected by cleansers, environment, sweat and more. Measure with a pH meter under standardized conditions. Persistent abnormality warrants a dermatology barrier assessment.",
    "\U0001F4DA Deep Dive: Skin pH (Normal 4.5\u20135.5) Meter",
    "Sensitive-skin care: frequent flushing with high pH suggests an 'over-cleansing \u2014 weak barrier' loop.",
    "Baby / mature care: skin trends more neutral; choose gentler formulas.",
    "Teaching demo: explain the meaning of the acid mantle to customers.",
    "Mature-skin pH interpretation",
    "Input: pH 5.8 → slightly alkaline but still acceptable; with dryness/tightness, suggest moderate lipid replenishment and avoid over-exfoliation.",
    "Why emphasize weakly acidic?",
    "A weakly acidic environment helps barrier enzymes and flora stability; too alkaline tends to dry and itch.",
    "Is one measurement enough?",
    "No. Affected by time of day and sweat; average several readings for stability.",
    "Can the result diagnose skin disease?",
    "No. It is only a pH interpretation reference; see a doctor for lesions.",
    'About "Skin pH Meter"',
    "Skin pH (normal 4.5\u20135.5) meter: assess skin acidity online and judge barrier health. A medical professional tool based on authoritative medical standards; for reference only.",
]))

# ---------------- spf-pa-calculator (56) ----------------
write('spf-pa-calculator', build('spf-pa-calculator', [
    "\U0001F9EE Sunscreen Factor (SPF/PA) Calculator",
    "Based on skin phototype, UV intensity and outdoor time, calculate the needed SPF/PA level and sun protection duration.",
    "Sunscreen Factor Calculator",
    "/ Sunscreen Factor Calculator",
    '\U0001F4D6 View the "Sunscreen Factor (SPF/PA) Calculator User Guide"',
    "Effective MED = MED × 5 / UVI; theoretical protection time = effective MED × SPF; actual protection time = theoretical × activity factor; required SPF = ⌈outdoor time / (effective MED × activity factor)⌉",
    "UVI is corrected against a baseline of 5 (higher UVI shortens effective MED). The activity factor reflects sweat / water wash-off weakening sunscreen. UVA protection time = effective MED × PPD × activity factor; PPD by PA level: PA+ 3, PA++ 6, PA+++ 12, PA++++ 20. Recommended SPF: need ≤15 → SPF 15+, ≤30 → SPF 30+, ≤50 → SPF 50+, otherwise SPF 50+ (needs physical cover + reapplication); recommended PA: UVI ≤2 → PA++, ≤5 → PA+++, >5 → PA++++. Used for outdoor sunscreen specs and reapplication interval.",
    "Skin phototype (Fitzpatrick)",
    "Type I \u2014 always burns",
    "Type II \u2014 easily burns",
    "Type III \u2014 medium",
    "Type IV \u2014 deeper",
    "Type V \u2014 dark brown",
    "Type VI \u2014 deeply pigmented",
    "Personal MED estimate (min)",
    "UV index (UVI)",
    "0\u20132 low (cloudy / indoor by window)",
    "3\u20135 moderate (spring/autumn daily)",
    "6\u20137 high (summer daytime)",
    "8\u201310 very high (midsummer noon)",
    "11+ extreme (plateau / tropics)",
    "Planned outdoor duration (min)",
    "Sunscreen SPF value",
    "PA level",
    "Outdoor sports (heavy sweat)",
    "Swimming / water activity",
    "Reapplication interval (min)",
    "\U0001F4CB SPF / PA Level Explanation",
    "UVB protection rate",
    "≈93%",
    "Daily indoor / short outings",
    "≈97%",
    "≈98%",
    "Outdoor activity / summer",
    "Plateau / seaside / strong UV",
    "UVA protection",
    "Basic",
    "Moderate",
    "High",
    "Very high",
    "\u26A0\uFE0F SPF calculation is theoretical; real protection is affected by application amount (need 2 mg/cm²), sweat and friction. Adequate application + timed reapplication is key.",
    "\U0001F4DA Deep Dive: Sunscreen Factor (SPF/PA) Calculator",
    "Travel planning: back-calculate the needed SPF/PA and amount from the destination UV index and stay duration.",
    "Parent-child sun care: estimate the small facial amount a child needs, avoiding excess or shortfall.",
    "Teaching demo: explain to customers 'why labeled SPF50 may actually only reach SPF20'.",
    "3-hour seaside activity",
    "Input: UVI 8, 3 h outdoors, full amount → recommend SPF50+ PA++++ and reapply every 2 h, immediately after water exit.",
    "Do I need sunscreen on a cloudy day?",
    "Yes. Clouds don't block all UVA; long-term accumulation still causes photo-aging.",
    "Is makeup with SPF enough?",
    "Usually not enough. Foundation / primer amounts are far lower; apply adequate sunscreen first, then makeup.",
    "Does this tool give medical advice?",
    "No. Results are only estimates of amount and parameters; follow your doctor for special skin.",
    'About "Sunscreen Factor Calculator"',
    "Sunscreen factor (SPF/PA) calculator: compute sun protection time online and assess whether SPF and PA levels are sufficient. A medical professional tool based on authoritative medical standards; for reference only.",
    "Time skin starts to redden",
]))

# ---------------- telangiectasia-area (44) ----------------
write('telangiectasia-area', build('telangiectasia-area', [
    "\U0001F4D0 Telangiectasia (Capillary) Area Assessor",
    "Assess the area proportion, vessel type and severity of facial telangiectasia (broken capillaries), and provide treatment reference.",
    "Telangiectasia Area Assessor",
    "/ Telangiectasia Area Assessor",
    '\U0001F4D6 View the "Telangiectasia (Capillary) Area Assessor User Guide"',
    "Telangiectasia score = min(100, area×2.5 + density×2 + diameter×15 + symptoms×5); severity and treatment plan are determined from the score together with vessel type and region.",
    "Affected area (%)",
    "Vessel density (vessels/cm²)",
    "Vessel diameter (mm)",
    "Vessel type",
    "Telangiectasia (linear / reticular)",
    "Venular ectasia (blue)",
    "Arterial ectasia (bright red, pulsatile)",
    "Spider angioma (central red dot, radiating)",
    "Diffuse flushing (erythema)",
    "Main distribution region",
    "Central cheeks",
    "Diffuse whole face",
    "Nose (rosacea)",
    "Occasional flushing",
    "Frequent flushing and burning",
    "Persistent erythema with papules",
    "\U0001F4CB Telangiectasia Severity Grading",
    "Vessel density",
    "Few fine lines, faintly visible",
    "Clearly visible, reticular",
    "Dense, pronounced color",
    "Diffuse, with papules and pustules",
    "\u26A0\uFE0F Facial telangiectasia may relate to rosacea, steroid-dependent dermatitis and more. The result is for reference; confirm with a dermatologist before treatment.",
    "\U0001F4DA Deep Dive: Telangiectasia (Capillary) Area Assessor",
    "Laser pre-planning: divide the treatment area into small grids by area to estimate the number of pulses and total energy.",
    "Efficacy quantification: measure the area difference the same way before and after treatment, using",
    "to show the improvement magnitude.",
    "Daily tracking: turn telangiectasia changes into trackable numbers, reducing subjective 'seems lighter' misjudgment.",
    "Cheek erythema before-after comparison",
    "Area 12% before, 5% after treatment → relative retreat 58%, recorded as effective; remaining can use maintenance therapy.",
    "Is every telangiectasia suitable for laser?",
    "Not necessarily. Fine superficial dilation responds well to dye / IPL; deep or inflamed ones need cause control first, per physician.",
    "Do I need to avoid certain foods based on the area?",
    "This tool gives no medical advice. Rosacea-related dilation usually suggests avoiding heat, spice and alcohol; follow your doctor.",
    "Can self-measurement be used as a follow-up basis?",
    "It can be a reference, but follow-up relies on clinic VISIA / professional imaging; self-test only tracks trends.",
    'About "Telangiectasia Area Assessor"',
    "Telangiectasia (capillary) area assessor: online assess facial telangiectasia / capillary dilation area and severity. A medical professional tool based on authoritative medical standards; for reference only.",
]))

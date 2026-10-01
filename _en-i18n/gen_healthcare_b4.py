#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""healthcare 第4批：bmi-2 / morse / due-date-calc"""
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


# ---------------- bmi-2 (23) ----------------
write('bmi-2', build('bmi-2', [
    "👶  BMI Percentile Estimator for Children",
    "Estimate the BMI percentile for a child or adolescent from age, sex, height and weight, and map the result to the underweight, healthy, overweight or obesity band.",
    "/  BMI Percentile Estimator for Children",
    '📖 View the "BMI Percentile Estimator for Children User Guide"',
    "Z ≈ (BMI − reference mean) / standard deviation",
    "The reference mean varies with age and sex",
    "This tool is a simplified teaching version; please use the CDC/WHO growth charts.",
    "📚 Deep Dive: Child BMI Percentile Estimation",
    "Growth: from age, sex, ",
    "estimate the percentile to see where the weight sits relative to peers of the same age and sex",
    "Initial screening: z<−2 suggests underweight and >2 suggests overweight, for parents and school doctors to reference",
    "Simplified teaching: grasp the percentile concept quickly, with the CDC/WHO charts for formal use",
    "Algorithm (simplified teaching version): z = (BMI − baseline − age × 0.35) / 2.2, with a male baseline of 16.5 and a female baseline of 16.2; percentile ≈ standard normal CDF(z) × 100; z<−2 underweight, >2 overweight. Note: the Math.erf used on this tool's page is not a standard JS function (browsers would return NaN), so the error function approximation is used here to give the correct percentile.",
    "Example 1 (boy aged 10, BMI 18): z = (18−16.5−3.5)/2.2 = −0.91, percentile ≈ 34%, normal. Example 2 (girl aged 8, BMI 20): z = (20−16.2−2.8)/2.2 = 0.45, percentile ≈ 58%, normal.",
    "How is it different from adult BMI?",
    'Child BMI varies with age and sex, so a raw number is meaningless: it must be converted into a percentile for the same age and sex (e.g. "the 85th percentile"); adults, by contrast, use fixed cut-offs directly.',
    "How do I read the percentile?",
    "The 50th percentile is average; <3 underweight, ≥85 overweight, ≥95 obese (CDC criteria). This tool uses a simplified normal approximation; check the official growth charts for exact values.",
    "How to Use the BMI Percentile Estimator for Children",
    "What does the BMI Percentile Estimator for Children do?",
    "Enter the child's age, sex, height and weight to estimate BMI and compare it against the percentile curve for that age and sex, giving a weight-status reference (simplified teaching version); use it together with the CDC/WHO growth charts.",
    "How do I use the BMI Percentile Estimator for Children?",
    "What scenarios is the BMI Percentile Estimator for Children best for?",
]))

# ---------------- morse (22) ----------------
write('morse', build('morse', [
    "📻 Morse Fall Risk Assessment",
    "Score the six Morse fall scale items including fall history, secondary diagnosis, ambulatory aid, IV therapy, gait and mental status, and read the risk level.",
    '📖 View the "Morse Fall Risk User Guide"',
    "Fall history",
    "Secondary diagnosis",
    "Ambulatory aid 0=none 15=crutches 30=holds furniture",
    "IV therapy",
    "Gait 0=normal 10=weak 20=impaired",
    "Mental status 0=normal 15=overestimates/forgets",
    "Morse scale total = sum of all item scores",
    "≤24 low risk, 25-50 moderate risk, >50 high risk",
    "For fall screening of inpatients.",
    "📚 Deep Dive: Morse Fall Risk",
    "Inpatient screening: assess Morse fall risk on admission or when condition changes",
    "Care grading: set the intensity of fall-prevention interventions by the score",
    "Quality improvement: track the high-risk rate to improve the workflow",
    "Algorithm (Morse scale): total = recent fall history + secondary diagnosis + ambulatory aid + IV therapy/heparin lock + gait + mental status, the sum of six items; grading: ≤24 low risk, 25-50 moderate risk, >50 high risk. Each item is scored per the scale (e.g. recent fall history 0/25, gait 0/10/20).",
    "Example 1 (all high-risk items at default 25+15+15+20+10+15): total 100, high risk. Example 2 (all 0): 0 points, low risk. Example 3 (10×5+0=50): 50 points, the moderate-risk boundary.",
    "What is the difference between Morse and Hendrich?",
    "Morse is for adult inpatient fall screening (6 items), while Hendrich II includes consciousness and medication; different departments choose different scales, and Morse is the most commonly used.",
    "How to manage once high risk is assessed?",
    "Add bed rails, fall-prevention signs, accompany the patient, tidy the environment, review medication (sedatives/antihypertensives) and assess restraints if needed; this is outside the tool's scope and must follow nursing standards.",
]))

# ---------------- due-date-calc (22) ----------------
write('due-date-calc', build('due-date-calc', [
    "📅 Pregnancy Week and Due Date Calculator",
    "Enter the last menstrual period or a known conception date to derive gestational age, the estimated due date and the current trimester with a week-by-week table.",
    '📖 View the "Pregnancy Week and Due Date User Guide"',
    "Days since last menstrual period",
    "Cycle length (days)",
    "Ovulation day (day of cycle)",
    "EDD = LMP + 280 days (40 weeks); current gestational age = days since LMP / 7",
    "For estimation only; actual delivery may vary by about two weeks either way.",
    "📚 Deep Dive: Pregnancy Week and Due Date (Last Menstrual Period Method)",
    "Pregnancy management: estimate the current gestational age from the last menstrual period and the ",
    "due date",
    ", then schedule antenatal checks",
    'Self-tracking: follow "days since your period stopped" and understand the due-date variation',
    "Education: understand the Naegele 280-day rule and its link to the ovulation day",
    "Algorithm: gestational age = days since period stopped ÷ 7; days to due date = 280 − days since period stopped (Naegele rule, pregnancy of about 280 days); days to ",
    "ovulation",
    "= days since period stopped − ovulation day. Actual delivery is usually within ±2 weeks of the due date.",
    "Example 1 (100 days since period stopped, ovulation day 14): gestational age = 100/7 = 14.3 weeks, 280−100 = 180 days to due date, 100−14 = 86 days since ovulation. Example 2 (200 days since period stopped): 28.6 weeks, 80 days to due date, 186 days since ovulation.",
    "What if my periods are irregular?",
    "Early ultrasound (especially crown-rump length at 7-13 weeks) is more accurate for dating; the last-menstrual-period method assumes a regular cycle of about 28 days with ovulation around day 14.",
    "Is the due date always accurate?",
    "Only about 5% of babies are born exactly on the due date, and most arrive within ±2 weeks; it is a reference point for planning antenatal checks and delivery, not an exact date.",
]))

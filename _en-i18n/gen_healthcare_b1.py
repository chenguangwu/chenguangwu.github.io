#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""healthcare 第1批：tdee-calculator / bmi-calculator"""
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


# ---------------- tdee-calculator (48) ----------------
write('tdee-calculator', build('tdee-calculator', [
    "🧮 Total Daily Energy Expenditure Calculator",
    "Multiply your basal metabolic rate by an activity factor to get total daily energy expenditure, then show the cut, maintain and bulk calorie targets derived from it.",
    "TDEE Calculator",
    "/ TDEE Calculator",
    "📖 View the User Guide",
    "BMR (Mifflin-St Jeor) = 10W + 6.25H − 5A + (men +5 / women −161)",
    "TDEE = BMR × activity factor; cut target = TDEE − 500, bulk target = TDEE + 300; thermic effect of food TEF = TDEE × 0.1",
    "👨 Male",
    "👩 Female",
    "Sedentary (little or no exercise)",
    "Lightly active (1-3 days/week)",
    "Moderately active (3-5 days/week)",
    "Very active (6-7 days/week)",
    "Extra active (physical labour / 2 training sessions)",
    "kcal / day · maintenance calories",
    "🎯 Goal Calorie Plans",
    "🏃 Cut",
    "⚖️ Maintain",
    "💪 Bulk",
    "📊 Visual Analysis",
    "Calorie Breakdown",
    "Macronutrients",
    "Weight Projection",
    "📋 Activity Level Guide",
    "Sedentary",
    "Desk job, little or no exercise, very low daily activity",
    "Lightly active",
    "Light exercise 1-3 times a week, or plenty of daily walking",
    "Moderately active",
    "Moderate exercise 3-5 times a week, or a fairly active daily routine",
    "Very active",
    "Exercise 6-7 times a week, or physical work plus exercise",
    "Extra active",
    "Heavy physical labour, or two high-intensity workouts a day",
    "⚠️ This tool is for reference only and cannot replace professional medical advice. Actual calorie needs are affected by many factors such as genetics, hormones and medication.",
    "📚 Deep Dive: Daily Energy Expenditure TDEE",
    "Weight management: use TDEE to set cut / maintain / bulk intake",
    "Nutrition planning: estimate the deficit from your target weekly weight loss",
    "Education: understand BMR and activity factors",
    "Algorithm: TDEE = BMR × activity factor; cut intake ≈ TDEE × 0.8 (about 20% less); weekly deficit needed = target weekly weight loss (kg) × 7700. Common activity factors are 1.2 sedentary, 1.375 light, 1.55 moderate, 1.725 high. All values must be >0.",
    "Example 1 (BMR 1500, activity 1.5, weekly loss 0.5 kg): TDEE = 1500 × 1.5 = 2250 kcal, cut intake 1800 kcal/day, weekly deficit 0.5 × 7700 = 3850 kcal. Example 2 (BMR 1400, activity 1.375): TDEE = 1925 kcal.",
    "How do I choose an activity factor?",
    "By your total daily energy expenditure: 1.2 sedentary, 1.375 light exercise, 1.55 moderate, 1.725 high intensity, higher for physical labour; choosing too high overestimates intake, so err on the low side.",
    "Is a 20% cut enough?",
    "Losing about 0.25-0.5 kg a week is fairly safe; more than 25% tends to lose muscle and slow metabolism. 7700 kcal ≈ 1 kg of fat is a convenient estimate.",
    'About the "TDEE Calculator"',
    "TDEE Calculator. A health-metric calculation tool based on authoritative medical standards; data is processed locally to protect privacy.",
    "Optional, used for the Katch formula",
]))

# ---------------- bmi-calculator (47) ----------------
write('bmi-calculator', build('bmi-calculator', [
    "🧮 Body Mass Index Calculator",
    "Compute BMI from height and weight in metric or imperial units, then place the value in the standard adult bands with the healthy weight range shown alongside.",
    "BMI Calculator",
    "/ BMI Calculator",
    "BMI = weight (kg) ÷ height (m)²",
    "Devine ideal weight = (men 50 / women 45.5) + 2.3 × (height in − 60); Robinson = (men 52 / women 49) + (men 1.9 / women 1.7) × (height in − 60)",
    "👨 Male",
    "👩 Female",
    "Metric (cm / kg)",
    "Imperial (in / lb)",
    "Height",
    "Waist (cm, optional)",
    "Target weight (kg, optional)",
    "Enter your height and weight",
    "📊 BMI History",
    "📋 Details",
    "Classification standard",
    "Ideal weight",
    "Health advice",
    "🏥 WHO International Standard",
    "Class II obesity",
    "🇨🇳 Chinese Adult Standard (WS/T 428-2013)",
    "Normal weight",
    "Overweight",
    "Obesity",
    "Enter your height first to calculate the ideal weight range",
    "Enter your data first to get personalised advice",
    "⚠️ This tool is for reference only and cannot replace professional medical advice. If you have a health concern, consult a doctor or dietitian.",
    "📚 Deep Dive: Adult BMI Body Mass Index",
    "Weight screening: calculated from height and weight",
    ", giving a first read of underweight / normal / overweight / obese",
    "Health management: track BMI changes alongside diet and exercise",
    "Education: understand the Chinese adult BMI cut-offs",
    "Algorithm: BMI = weight (kg) ÷ height (m)²; Chinese adult standard: <18.5 underweight, 18.5-24 normal, 24-28 overweight, ≥28 obese. Height and weight must be >0.",
    "Example 1 (65 kg / 170 cm): BMI = 65 ÷ 1.7² = 65 ÷ 2.89 = 22.5 → normal. Example 2 (80 kg / 175 cm): BMI = 80 ÷ 1.75² = 80 ÷ 3.0625 = 26.1 → overweight.",
    "Is BMI accurate?",
    'BMI does not distinguish muscle from fat: a gym-goer with a lot of muscle can be "overweight" yet have normal body fat. It is a population screening tool, so individuals should combine it with waist circumference and ',
    "body fat percentage",
    "judgement.",
    "Why is the Chinese standard stricter?",
    "At the same BMI, Asians carry more visceral fat and a higher risk of chronic disease, so the Chinese standard is stricter than the WHO (25/30), using cut-offs of 24/28.",
    'About the "BMI Calculator - Online Body Mass Index Calculation"',
    "Free online BMI calculator: compute your body mass index from height and weight, assess whether your weight is healthy and see the recommended healthy ranges. A health-metric calculation tool based on authoritative medical standards; data is processed locally to protect privacy.",
    "e.g. 170",
    "e.g. 65",
    "Used for the waist-to-height ratio calculation",
    "Calculate weight change",
]))

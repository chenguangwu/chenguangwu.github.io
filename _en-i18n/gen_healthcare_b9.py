#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""healthcare 第9批：fat-loss-deficit / resp-rate / ideal-weight / water-intake"""
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


# ---------------- fat-loss-deficit (17) ----------------
write('fat-loss-deficit', build('fat-loss-deficit', [
    "⚡ Fat Loss Calorie Deficit Planner",
    "Set a daily calorie deficit from your maintenance level and target weekly weight loss, then see the projected timeline and the safe lower bound for intake.",
    '📖 View the "Fat Loss Calorie Deficit User Guide"',
    "Target weight loss (kg)",
    "Target weight (kg)",
    "1 kg of fat ≈ 7700 kcal; daily deficit = total deficit / days",
    "For safe fat loss, a daily deficit of 500-1000 kcal is advised.",
    "📚 Deep Dive: Fat Loss Calorie Deficit Planning",
    "Plan making: estimate the daily deficit from the target weight loss and days",
    "Safe range: 500-1000 kcal/day is advised; too fast tends to lose muscle",
    "Weight calculation: work back from the target weight to the starting weight",
    "Algorithm: total deficit = weight loss (kg) × 7700 (1 kg of fat ≈ 7700 kcal); daily deficit = total deficit ÷ days; starting weight = target weight + weight loss. Weight loss, days and target weight must be >0.",
    "Example 1 (lose 5 kg / 60 days / target 60 kg): total deficit 5×7700 = 38500 kcal, daily deficit 38500/60 = 642 kcal/day, starting weight 65.0 kg. Example 2 (lose 3 kg / 30 days / 55 kg): total deficit 23100 kcal, daily deficit 770 kcal/day, starting 58.0 kg.",
    "Is a bigger deficit better?",
    "No; more than 1000 kcal/day tends to lose muscle, slow metabolism and is hard to sustain; 500-1000 kcal/day is safer, losing about 0.5-1 kg a week.",
    "Is 7700 accurate?",
    "1 kg of pure fat is about 7700 kcal, but human weight loss includes water and muscle, so the actual amount needed is a little higher; this figure is a convenient estimate, not exact.",
]))

# ---------------- resp-rate (17) ----------------
write('resp-rate', build('resp-rate', [
    "📡 Respiratory Rate Assessor",
    "Enter an observed breathing rate with the patient's age band to judge whether it is normal, bradypnoeic or tachypnoeic, with the reference ranges shown per age.",
    '📖 View the "Respiratory Rate Assessment User Guide"',
    "Respiratory rate (breaths/min)",
    "State 1=rest / 2=exercise",
    "Normal adult resting breathing 12-20 breaths/min",
    "Seek medical assessment promptly for abnormal breathing.",
    "📚 Deep Dive: Respiratory Rate Assessment",
    "Vital signs: resting respiratory rate is an important early-warning indicator",
    "Detecting abnormality: too slow or too fast signals illness",
    "Exercise reference: gives the exercise ceiling by state",
    "Algorithm: state = 3 (abnormal) if respiratory rate <12 or >20, otherwise 1 (normal); deviation from normal = |RR−16|; exercise ceiling = 40 breaths/min in the exercise state, otherwise 20 breaths/min as a reference. RR must be >0.",
    "Example 1 (RR 16): normal state (level 1), deviation 0. Example 2 (RR 24): abnormal (level 3), deviation 8. Example 3 (RR 10, exercise state): abnormal (level 3), exercise ceiling 40 breaths/min.",
    "What is a normal respiratory rate?",
    "About 12-20 breaths/min at rest in adults; >20 is tachypnoea (e.g. fever, heart failure, anxiety) and <12 is bradypnoea (e.g. sedation, raised intracranial pressure); seek medical care if it persists.",
    "Is the deviation from normal clinically meaningful?",
    "It only gives an intuitive sense of how far you are from the normal midpoint of 16; the real judgement looks at the absolute value and accompanying symptoms (cyanosis, chest retraction, drowsiness). This tool does not replace a doctor.",
]))

# ---------------- ideal-weight (17) ----------------
write('ideal-weight', build('ideal-weight', [
    "⚖️ Devine Ideal Weight Estimator",
    "Compute ideal body weight with the Devine formula plus the Hamwi, Miller and Robinson variants, and compare your current weight against each estimate.",
    '📖 View the "Ideal Weight Calculator User Guide"',
    "Devine: male 50+2.3×(in−60), female 45.5+2.3×(in−60)",
    "For nutritional assessment reference only, not a health standard.",
    "📚 Deep Dive: Ideal Weight Devine",
    "Dosing baseline: clinically, ",
    "is used to estimate some of the ",
    "drug doses",
    "Ventilator parameters: mechanical ventilation tidal volume is set by IBW",
    "Reference value: IBW is a clinical baseline, not a healthy-weight standard",
    "Algorithm (Devine, in inches): convert height to inches hIn = height cm / 2.54; male IBW = 50 + 2.3×(hIn−60), female IBW = 45.5 + 2.3×(hIn−60), in lb, ÷2.2 gives kg. Height must be >0.",
    "Example 1 (170 cm, male): hIn = 66.93, IBW = 50+2.3×6.93 = 65.9 kg. Example 2 (160 cm, female): hIn = 62.99, IBW = 45.5+2.3×2.99 = 52.4 kg. Example 3 (180 cm, male): IBW = 50+2.3×10.87 = 75.0 kg.",
    'Is IBW a "standard weight"?',
    "It is not a health judgement but a clinical calculation baseline (especially dosing and ventilators); it is normal for a muscular person to have a low IBW, and actual weight varies with body build.",
    "For obese patients, dose by IBW or actual body weight?",
    "It depends on the drug: lipophilic or widely distributed drugs may use adjusted body weight, while water-soluble drugs or those designed by IBW use IBW; follow the drug label and clinical decision.",
]))

# ---------------- water-intake (17) ----------------
write('water-intake', build('water-intake', [
    "🩺 Daily Water Intake Recommender",
    "Estimate daily fluid needs from body weight, activity duration and climate, and break the total between plain water, beverages and the water held in food.",
    '📖 View the "Daily Water Intake Recommendation User Guide"',
    "Activity factor 1-1.5",
    "Climate factor 1-1.3",
    "Water ≈ weight (kg) × 35 mL × activity × climate factor",
    "Includes water from food; more is needed in hot weather or with exercise.",
    "📚 Deep Dive: Daily Water Intake Recommendation",
    "Hydration management: estimate daily water intake from body weight",
    "Exercise / heat: increase to compensate for sweating",
    "Correcting a myth: more water is not always better",
    "Algorithm: recommended water = weight (kg) × 35 × activity factor × climate factor (mL); cups = recommended ÷ 250. Activity/climate factors are ≥1 (e.g. 1.2, 1.1). About 20-30% comes from food water. All values must be >0.",
    "Example 1 (65 kg, activity 1.2, climate 1): recommended 65×35×1.2×1 = 2730 mL, about 10.9 cups (250 mL). Example 2 (70 kg, activity 1.35, climate 1.1): recommended 70×35×1.35×1.1 = 3641 mL.",
    'Is "8 cups a day" accurate?',
    "It is a rough rule; more accurately, estimate by weight × 30-35 mL, adding more for exercise, heat or breastfeeding. But the total includes water from food, so you need not drink it all.",
    "Is drinking too much water harmful?",
    "There is a risk of water intoxication (low sodium), especially with a large amount in a short time; people with normal kidney function are generally not at risk, but long-duration exercise such as a marathon requires some salt replacement.",
]))

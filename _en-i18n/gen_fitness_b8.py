#!/usr/bin/env python3
# fitness batch8 (index only)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'fitness')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'fitness')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'index': [
"🏋️ Fitness & Exercise Tools",
"Fitness & Exercise",
"Fitness & Exercise Tools",
"Exercise Calorie Burn Calculator",
"Estimate calorie burn from MET (metabolic equivalent) values combined with body weight and exercise duration, covering 20+ common activities.",
"Body Fat Percentage (Skinfold Method) Calculator",
"Based on the Jackson-Pollock three-site skinfold method, combine sex and age to estimate body density and then convert to body-fat percentage with the Siri equation.",
"Enter your age to estimate maximum heart rate using several formulas (Fox, Tanaka, Gellish, Arena) and get training zones based on the average.",
"BMI Calculator",
"Enter height and weight to compute body mass index (BMI) and get a body-assessment grade and healthy weight range against the Chinese adult standard.",
"Daily Calorie Needs Calculator",
"Barbell and dumbbell plate combination generator. Enter the target weight and the available plate sizes to generate, in the front end, a loading scheme that reaches that weight, making it quick to set up training loads, with data generated locally.",
"Compute total training volume (weight × sets × reps), estimate 1RM with the Epley formula, and classify the intensity zone and training goal by reps.",
"Aerobic heart rate zone calculator. Uses the Karvonen heart rate reserve method, combining age and resting heart rate to divide 5 aerobic training zones, helping control exercise intensity precisely and improve fat-burning and endurance training efficiency.",
"Body Fat Percentage Calculation (Navy Formula)",
"Use the US Navy circumference formula to estimate body-fat percentage from neck, waist and hip measurements.",
"Based on the energy-conservation principle of 1 kg of fat ≈ 7700 kcal, compute the daily calorie deficit needed to reach a fat-loss goal and a diet/exercise allocation plan.",
"Convert between pace (minutes:seconds per kilometre) and speed (km/h), and enter a target pace to estimate finish time; suited to running training and race pacing.",
"1RM Max Weight Estimation",
"Enter the weight lifted and the reps performed, and use several classic formulas to estimate one-rep max (1RM), useful for strength-training programming.",
"Basal Metabolic Rate (BMR)",
"Basal metabolic rate (BMR) calculator. Enter height, weight, age and sex to estimate daily basal metabolic calories with formulas such as Mifflin-St Jeor, for calorie management and setting the energy baseline for fat loss and muscle gain.",
"Enter body weight, daily activity level (sedentary to very intense) and training goal (muscle gain, fat loss or maintenance) to estimate the recommended daily protein intake range in grams from physiological constants and empirical factors, helping gym-goers plan dietary protein.",
"Recommend static stretch hold time, sets, weekly frequency and dynamic/PNF options from the target muscle group and current flexibility level.",
"Measure subcutaneous fat thickness with skinfold callipers and estimate body-fat percentage using the Jackson-Pollock formulas",
"Enter body weight and a muscle-gain goal to compute daily protein, carbohydrate and fat grams and their calorie shares, useful for fitness diet planning.",
"Data Analysis (Memberships / Courses / Retention)",
"Enter the starting number of users (members), the number retained at the end and the number of months in the period to automatically compute the overall retention rate, churn rate and average monthly churn, for membership/course stickiness analysis. The computation runs locally in the browser.",
"Based on the Cooper 12-minute run test, estimate maximal oxygen uptake VO₂max from the running distance to assess cardiorespiratory endurance",
"Body Fat Estimation",
"Based on the US Navy body fat formula, estimate body-fat percentage from waist, neck and height (plus hip for women), with no equipment and suited to everyday self-testing.",
"Body Fat Resistance Estimate",
"Based on bioelectrical impedance analysis (BIA), estimate total body water and fat-free mass from the impedance index and then derive body-fat percentage.",
"Enter the left and right upper arm, thigh and calf girth to compute each site's symmetry difference and an overall score, assessing how balanced your muscle development is.",
"Circuit Training Timer",
"HIIT / circuit training timer with custom work, rest and round settings and automatic interval switching reminders",
"Log weight × sets × reps for each exercise, accumulate training volume and chart the progress curve to track strength gains",
"VO2max Estimation",
"Based on the Cooper 12-minute run test, estimate maximal oxygen uptake (VO2max) from the running distance and grade aerobic endurance.",
"Generate a weekly increasing plan from your current training data, with a deload week every four weeks, to progress strength scientifically.",
"Enter the target muscle group, tenderness level (VAS 0–10) and session length to get pressure, hold time, sets and frequency advice following myofascial release principles",
"Set a daily hydration goal with timed reminders to drink, log each drink and store data locally, helping build a regular hydration habit.",
"The Quality (Assessment/Optimisation/Improvement) mechanism is a free online fitness and exercise tool — a comprehensive quality assessment tool for yoga courses that scores four dimensions (instructor strength, course content, teaching environment and student outcomes) and generates improvement suggestions and upgrade plans. Runs purely in the front end, uploads no data, no registration required, open…",
"Core stability assessment tool. Scores 4 tests (plank, dead bug, etc.) to assess core muscle stability and strength weaknesses, outputting a grade and training advice for improving exercise movement quality.",
"Fitness assessment quality-optimisation mechanism tool. Quantitatively evaluates training-plan quality across 5 dimensions (1–5 points each), aggregates the score and gives improvement advice, for standardising and continuously improving fitness programmes.",
"An online rounded-shoulder (tight pectoralis minor) test tool that assesses the severity of postural issues with 3 tests and gives stretching advice; suited to fitness self-checks and running purely in the front end.",
"Enter joint angle, external moment arm and load to estimate net joint torque and the muscle force required (a simplified biomechanical model).",
"Create personal training courses, schedule weekly sessions, check in completed sessions, and report the completion rate with a monthly calendar view.",
'About "Fitness & Exercise Tools"',
"The fitness and exercise tools collection brings together 34 free online tools covering common calculation, conversion and lookup needs in fitness and exercise scenarios. Whether you are a professional in the field, a student or an ordinary user, you will find handy, no-fuss utilities here. All tools run purely in the front end, upload no data to a server and protect your privacy.",
"The fitness and exercise tools on this page include (a selection of representative tools):",
"These tools help you quickly complete common fitness and exercise tasks without memorising complex formulas or doing manual conversions — just enter your values and get the result.",
"Do the fitness and exercise tools require downloading or registration?",
"No. All the fitness and exercise tools on this page are pure client-side online tools: just open the page and use them, with no software to install, no account to register and no data uploaded.",
"Are the results of the fitness and exercise tools accurate? Is my data safe?",
"The tools compute locally in your browser based on public mathematical formulas and general industry standards, giving instant results. All computations are done locally on your device, data is not uploaded to a server, and your privacy is protected.",
],
}

EXTRA = {
}

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
            print('BAD EN', slug, repr(en)); sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(en)); sys.exit(1)
        mp[z] = en
    return mp

def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'fitness', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, slug + '.json')
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

for slug, en_list in EN.items():
    write(slug, build(slug, en_list))

#!/usr/bin/env python3
# fitness batch7 (5 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'fitness')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'fitness')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'time-stretch': [
"🏋️ Stretching Duration Advisor",
"Recommend static stretch hold time, sets and weekly frequency from the target muscle group and current flexibility level, including dynamic and PNF options.",
'📖 View the "Stretch Plan Generation (Hold Time / Sets / Weekly Duration) Guide"',
"Target muscle group",
"Calf (gastrocnemius/soleus)",
"Hip flexors",
"Chest (pectorals)",
"Flexibility level",
"Beginner (poor flexibility / easily tight)",
"Intermediate (average)",
"Advanced (good flexibility)",
"Training phase",
"Warm-up (before training)",
"Cool-down (after training)",
"Dedicated flexibility training",
"Recovery / rehabilitation",
"💡 ACSM recommendation: hold a static stretch for 15-60 seconds, 2-4 sets per muscle group, at least 2-3 times a week; those with poor flexibility should start with short holds and more sets.",
"Stretch to the point of tension but not pain, and never bounce forcefully",
"Muscle temperature is low before a warm-up, so 5 minutes of low-intensity cardio first is recommended",
"Before training, focus on dynamic stretching; after training, focus on static stretching",
"Those with restricted joint range of motion or injuries should follow medical advice; PNF stretching needs a partner",
"📚 In-Depth Analysis: Stretch Plan Generation (Hold Time / Sets / Weekly Duration)",
"Generates a personalised stretch plan by target muscle, flexibility level and training phase (warm-up/cool-down/dedicated/rehab).",
"Tight muscle groups get an extra set automatically, and the PNF phase adds isometric holds, systematically improving range of motion.",
"Outputs the per-session and weekly total duration, making it easy to plan into your",
"training plan",
"Reproducible example: hamstrings, intermediate, post-training cool-down",
"Input: muscle=hamstrings (tightness 1.2), level=intermediate (hold 30 seconds/3 sets/4 times a week), phase=cool-down (static-based, factor 1.0).\nStatic hold=round(30×1.2×1.0)=36 seconds/set; tightness >1.1 and not a warm-up → sets +1=4 sets.\nSession static subtotal=36×4=144 seconds; no dynamic/PNF (cool-down phase) → session total=144 seconds.\nWeekly total=144×4/60=9.6 minutes.\nConclusion: the intermediate cool-down plan for the hamstrings is a 36-second static hold × 4 sets (about 2.4 minutes) per session, about 9.6 minutes total across 4 sessions a week.",
"How long should each static stretch be held?",
"Generally 15–60 seconds per set and 2–4 sets effectively improves flexibility; this tool derives it by multiplying the level (beginner 15 / intermediate 30 / advanced 45 seconds) by the muscle tightness and the phase factor. Tight muscle groups get an extra set, and the PNF phase adds an isometric hold of about 1.2×.",
"Is static stretching suitable before training?",
"Dynamic stretching activation is more recommended before training (this tool's warm-up phase is mainly dynamic), as long static stretching may briefly reduce explosive power; static/PNF is better after training or in dedicated flexibility training.",
'About "Stretching Duration Advisor"',
"Based on the ACSM (American College of Sports Medicine) flexibility training guidelines, and combining muscle-group characteristics with flexibility level, it intelligently recommends the hold time, sets and weekly frequency of static, dynamic and PNF stretching.",
"Targeted advice for 9 major muscle groups",
"Adaptive adjustment for 3 flexibility levels",
"Distinguishes warm-up/cool-down/dedicated/recovery scenarios",
"Includes PNF progression and specialised tips",
"Planning pre-training warm-up stretching",
"Scheduling post-training cool-down recovery",
"Dedicated flexibility improvement plan",
"Daily stretching guidance for desk-bound people",
"Muscle group",
"Flexibility level",
"Training phase",
],
'training-volume': [
"🧊 Training Volume Progress Curve",
"Log weight × sets × reps for each exercise, accumulate training volume and chart the progress curve to track strength gains.",
'📖 View the "Training Volume Logging and Statistics (Weight × Sets × Reps) Guide"',
"Add exercise",
"Sets",
"Weight (kg)",
"+ Add set",
"Save this workout",
"Delete this exercise",
"📈 Volume progress curve",
"Session training volume = Σ(weight × sets × reps); estimated 1RM ≈ weight × (1 + reps / 30) (Epley)",
"Log the sets and reps of each workout by exercise; the session volume is the sum of weight × reps across sets, accumulated to draw the volume progress curve. The Epley formula estimates 1RM from that session's weight and reps, for comparing strength gains over time; rising volume with a higher 1RM shows the training is effective.",
"Training volume = weight × reps, and the session total volume is the sum of volume across sets. Continuously tracking volume growth assesses training progress, and progressive overload is the key to strength gains. RPE is the rating of perceived exertion (1-10).",
"📚 In-Depth Analysis: Training Volume Logging and Statistics (Weight × Sets × Reps)",
"Record weight, sets and reps exercise by exercise, automatically accumulating the per-exercise and session total volume (Volume Load).",
"Compare volume changes across cycles to judge whether progressive overload is achieved.",
"Export or screenshot the day's volume, and use it with",
"to evaluate the intensity distribution.",
"Reproducible example: bench press + squat two-exercise volume",
"Record: bench press 60 kg×4 sets×8 reps; squat 80 kg×5 sets×5 reps.\nBench press volume=60×4×8=1920 kg; squat volume=80×5×5=2000 kg.\nPer-exercise volume: bench press 1920, squat 2000; this session's total volume=1920+2000=3920 kg, total reps=32+25=57.\nConclusion: using the weight × sets × reps measure, the bench press is 1920 kg and the squat 2000 kg, 3920 kg in total for the day, making it easy to track volume growth week over week.",
"training volume",
"What is it for?",
"Volume Load = weight × sets × reps, the core metric for quantifying training amount. Hypertrophy training often focuses on progressive volume; a sudden volume spike easily causes injury and a sudden drop causes regression. Keeping the weekly volume increase at 5–10% and judging recovery with RPE is recommended.",
"Which matters more, volume or reps?",
"They are complementary. Volume reflects the total load, while reps reflect the endurance/hypertrophy bias (e.g. 8–12 reps leans hypertrophic). This tool records the raw volume, and combined with intensity % you can pin down the training purpose (strength/hypertrophy/endurance).",
'About "Training Volume Progress Curve"',
"The Training Volume Progress Curve is an online tool in the health and medical field. A health-metric calculator based on authoritative medical standards, processing data locally to protect privacy.",
"e.g. bench press, squat",
],
'vo2max-12min': [
"🏋️ 12-Minute Run VO2max",
"Based on the Cooper 12-minute run test, estimate maximal oxygen uptake VO₂max from the running distance to assess cardiorespiratory endurance.",
'📖 View the "12-Minute Run VO₂max (Cooper Test) Guide"',
"Distance estimate",
"Pace estimate",
"Rating table",
"12-minute running distance",
"Kilometres (km)",
"Miles (mile)",
"Enter the time to run 1.5 miles (about 2.4 km) and estimate VO₂max with the Cooper pace formula",
"1.5-mile run time (minutes)",
"📊 Men's VO₂max rating table (ml/kg/min)",
"📊 Women's VO₂max rating table (ml/kg/min)",
"VO₂max = (running distance (m) − 504.9) / 44.73 (Cooper 12-minute run); average pace = 12 minutes / distance",
"The Cooper 12-minute run test is commonly used on a track or treadmill: record the maximum distance covered in 12 minutes and plug it into the formula to get maximal oxygen uptake (ml/kg/min); the other mode works backwards from the finish time (VO₂max = 483 / time + 3.5). Results give an endurance grade by sex and age band.",
"Cooper test: run all-out for 12 minutes on flat ground and record the total distance. Formula: VO₂max = (distance in metres − 504.9) / 44.73. 1.5-mile run formula: VO₂max = (483 / time in minutes) + 3.5.",
"This test is maximal-intensity exercise; those with cardiovascular disease or who have not exercised for a long time should do it under medical supervision and must not push themselves.",
"📚 In-Depth Analysis: 12-Minute Run VO₂max (Cooper Test)",
"Run / brisk-walk all-out for 12 minutes on flat ground, record the total distance, and estimate maximal oxygen uptake with the Cooper formula.",
"You can also derive VO₂max from the 1.5-mile run time, cross-validating with the two measures.",
"Look up the rating table by age/sex, assess cardiorespiratory endurance and set aerobic goals.",
"Reproducible example: 2800 m in 12 minutes (man aged 30)",
"Input: distance 2800 m, age 30, sex male.\nCooper distance formula: VO₂max=(2800−504.9)/44.73=2295.1/44.73≈51.3 ml/kg/min.\nAverage pace=720/(2800/1000)=720/2.8≈257 seconds/km≈4:17/km.\nRating: male, 30 years, 51.3 ml/kg/min is in the excellent band (men 30–39 excellent line about 47.9+).\nSupplemental 1.5-mile formula: if 1.5 miles takes 11 minutes, VO₂max=483/11+3.5=43.9+3.5=47.4 ml/kg/min, of the same order as the distance method.\nConclusion: 2800 m in 12 minutes corresponds to VO₂max≈51.3 ml/kg/min, an excellent level, at a pace of about 4:17/km.",
"Is the Cooper formula accurate?",
"The Cooper 12-minute run formula is a classic field estimate (error about ±5–10%) and suits self-testing trends for the general public; a laboratory gas analysis measuring VO₂max directly is the most accurate. A thorough warm-up and flat ground before running reduce error.",
"What if the distance method and the 1.5-mile method differ?",
"Both are empirical regressions, and different samples and formulas cause deviations, so a similar order of magnitude is enough. This tool gives both and looks up each rating; if they differ a lot, prefer the one on the day you are stronger and steadier, and use the same method for long-term tracking.",
'About "12-Minute Run VO2max"',
"12-Minute Run VO2max. A health-metric calculator based on authoritative medical standards, processing data locally to protect privacy.",
],
'weight-capacity-training': [
"🧊 Training Volume Calculator",
"Compute total training volume (weight × sets × reps), estimate 1RM with the Epley formula, and classify the intensity zone and training goal by reps.",
'📖 View the "Training Volume and 1RM Conversion (Intensity Zone Classification) Guide"',
"Total training volume = weight × sets × reps; estimated 1RM ≈ weight × (1 + reps / 30) (Epley); intensity % = current weight / 1RM × 100",
"Volume (tonnage) reflects the total load of a session; relative intensity is set by the ratio of the current weight to 1RM, and the intensity zone determines the training goal (strength / hypertrophy / endurance). For warm-up ramping sets, take 50% / 70% / 80% / 90% of 1RM as reference weights.",
"Training weight (kg)",
"Known 1RM (kg, optional)",
"💡 Training volume = weight × sets × reps; Epley formula: 1RM = weight × (1 + reps/30); intensity % = training weight / 1RM × 100%.",
"The Epley formula is fairly accurate in the 1-15 rep range, overestimating at high reps",
"Training volume is the core metric for quantifying training amount, and progressively increasing volume is key to hypertrophy",
"A weekly volume increase of no more than 10% is recommended to avoid overtraining and injury",
"For compound lifts (squat/deadlift/bench press), measuring 1RM is recommended; for small muscle groups, an estimate is fine",
"📚 In-Depth Analysis: Training Volume and 1RM Conversion (Intensity Zone Classification)",
"Enter an exercise's weight, sets and reps to compute the total training volume and estimate",
" (Epley variant: w×(1+reps/30)).",
"Convert the current intensity",
" to pin down the training zone (maximal strength / high intensity / hypertrophy / endurance).",
"Generate a weight ladder from warm-up to working sets (50%/70%/80%/90% 1RM) to standardise progression.",
"Reproducible example: 60 kg × 4 sets × 10 reps",
"Input: weight 60 kg, 4 sets, 10 reps, no measured 1RM entered.\nTotal training volume=60×4×10=2400 kg; total reps=40.\nEstimated 1RM=60×(1+10/30)=60×1.333=80 kg.\nIntensity percentage=60/80×100=75% → zone hypertrophy (70–80%), 8–12 reps recommended.\nWeight ladder: warm-up 80×0.5≈40 kg, ramp 80×0.7≈56 kg, 80×0.8≈64 kg, working set 80×0.9≈72 kg.\nConclusion: this set's intensity is 75% (hypertrophy zone); warm up progressively from 40→56→64→72 kg to the working set.",
"Is the 1RM estimation formula reliable?",
"This tool uses w×(1+reps/30) (simplified Epley), suitable for reps≤10; the more reps, the larger the error. If you have a measured 1RM, enter it in the leave-blank-to-auto-estimate field and the tool uses it directly for a more accurate intensity. Beyond 10 reps, deriving 1RM is not recommended.",
"What should I train at 75% intensity?",
"70–80% is the hypertrophy sweet spot, with 8–12 reps recommended, mainly growing muscle-fibre cross-sectional area; to chase strength use ≥85% (1–5 reps), and to train endurance use 50–65% (15+ reps). This tool automatically marks the zone and recommended reps by intensity %.",
'About "Training Volume Calculator"',
"Compute total training volume (weight × sets × reps), use the Epley formula to estimate one-rep max (1RM), and classify the training zone by intensity percentage, supporting strength and hypertrophy programming.",
"Training volume = weight × sets × reps",
"Estimating 1RM with the Epley formula",
"Matching the intensity zone to the training goal",
"1RM percentage load reference table",
"Tracking strength-training volume",
"Programming for hypertrophy/strength",
"1RM estimation and percentage conversion",
"Progressive management of training load",
"Training weight",
"Sets",
"Reps per set",
"Leave blank to auto-estimate",
"Known 1RM",
],
'zuidasheyanglianggusuan': [
"🔮 VO2max Estimation (Cooper Test)",
"Based on the Cooper 12-minute run test, estimate maximal oxygen uptake (VO2max) from the running distance and grade aerobic endurance.",
"VO2max Estimation",
"/ VO2max Estimation",
'📖 View the "VO2max Estimation (Cooper Distance Method) Guide"',
"VO₂max = (distance (m) − 504.9) / 44.73; absolute oxygen uptake = VO₂max × weight / 1000 (L/min); average speed = distance / 12 (m/min); equivalent distance = VO₂max × 44.73 + 504.9",
"Estimate maximal oxygen uptake from the Cooper 12-minute run distance, then multiply by weight to get the absolute oxygen uptake per minute (litres). The equivalent distance converts how many extra metres are needed to raise VO₂max by a given ml/kg/min, useful for setting stage goals; results are rated by sex and age, with a percentage relative to the excellent line (70 ml/kg/min).",
"12-minute run distance (metres)",
"💡 Cooper formula: VO2max = (distance in metres − 504.9) ÷ 44.73, units ml/kg/min. The farther the distance, the stronger the aerobic capacity.",
"The 12-minute run should be done on a standard 400 m track, recording the total distance covered",
"Warm up thoroughly before the test; it is best done after building an aerobic base, and beginners should test with caution",
"The Cooper formula is an estimate, laboratory gas analysis is the gold standard, and the error is about ±5-8%",
"Heat, high altitude, illness and other states affect the result, so the test should be done when you are in good condition",
"📚 In-Depth Analysis: VO2max Estimation (Cooper Distance Method)",
"Run / brisk-walk all-out for 12 minutes and record the distance, then estimate VO₂max and absolute oxygen uptake with the Cooper formula.",
"Look up the aerobic capacity rating by age/sex and quantify the gap to the excellent line (70 ml/kg/min).",
"Given an improvement goal, work backwards to the running distance needed and set training milestones.",
"Reproducible example: man 30 years, 2400 m in 12 minutes, 70 kg",
"Input: male, 30 years, distance 2400 m, weight 70 kg.\nVO₂max=(2400−504.9)/44.73=1895.1/44.73≈42.4 ml/kg/min.\nAbsolute oxygen uptake=42.4×70/1000≈2.97 L.\nRating: male 30 years, 42.4 ml/kg/min → good (men 30–35 good line 42).\nRelative to the excellent line (70)",
"=42.4/70×100≈61%.\nRaising by 2 ml/kg/min needs distance≈(42.4+2)×44.73+504.9≈2489 m.\nConclusion: this man's VO₂max≈42.4 ml/kg/min (good) and absolute oxygen uptake≈2.97 L; to gain another 2 units he needs to run about 2489 m in 12 minutes.",
"How should VO₂max be understood?",
"Maximal oxygen uptake is the peak oxygen consumed per kilogram per minute (ml/kg/min), the gold standard of cardiorespiratory endurance. Ordinary people are about 35–45, and endurance athletes can reach 60–70+. It is influenced by both genetics and training, and regular aerobic work for 8–12 weeks can raise it by 10–20%.",
"What is the relationship between the distance method and body weight?",
"The Cooper distance formula outputs a relative value (ml/kg/min) that already includes body weight; the absolute oxygen uptake then multiplies by weight to give L/min, reflecting total aerobic output. People who are much overweight have a low relative value but possibly a not-low absolute value, and the relative value usually rises after fat loss.",
'About "VO2max Estimation"',
"Using the Cooper 12-minute run test formula, it estimates maximal oxygen uptake (VO2max) from the total running distance and grades aerobic endurance by sex and age — a classic aerobic-capacity assessment method.",
"Cooper 12-minute run formula",
"Grading by sex and age",
"Pace and absolute oxygen uptake conversion",
"Improvement targets and gap analysis",
"Aerobic capacity assessment for runners",
"Reference for meeting military-training fitness tests",
"Tracking the effect of endurance training cycles",
"Athlete selection and fitness screening",
"12-minute run distance",
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

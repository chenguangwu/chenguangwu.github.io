#!/usr/bin/env python3
# fitness batch5 (5 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'fitness')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'fitness')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'estimate': [
"🏋️ Body Fat Estimation (Navy Method)",
"Based on the US Navy body fat formula, estimate body fat from waist, neck and height (plus hip circumference for women), with no equipment needed and suited to everyday self-testing.",
"Body Fat Estimation",
'📖 View the "Body Fat Calculation (US Navy Formula) Guide"',
"Waist circumference (cm)",
"Men: BF% = 495 ⁄ [1.0324 − 0.19077·log10(waist−neck) + 0.15456·log10(height)] − 450; women: BF% = 495 ⁄ [1.29579 − 0.35004·log10(waist+hip−neck) + 0.22100·log10(height)] − 450 (units cm, log10 = base-10 logarithm)",
"💡 Navy formula (units cm): men = 495 / [1.0324 − 0.19077·log10(waist−neck) + 0.15456·log10(height)] − 450; women include hip circumference.",
"Measure in a naturally standing position, with the tape horizontal against the body but not compressing it",
"Take the waist at navel level, the neck at the narrowest point below the Adam's apple, and the hip at the fullest point of the buttocks",
"For men the waist must be larger than the neck, otherwise the formula is meaningless",
"The Navy formula is sensitive to abdominal fat, and accuracy declines for athletes and pregnant women",
"📚 In-Depth Analysis: Body Fat Calculation (US Navy Formula)",
"With no callipers, use a tape measure for waist/neck (plus hip for women) to estimate",
"body-fat percentage",
", which suits home self-testing.",
"Compared with the skinfold method and body-fat scales, the Navy method needs only circumferences, making it the simplest to use.",
"Track how body-fat percentage changes as the waist shrinks during a fat-loss phase, quantifying the fat-loss effect.",
"Reproducible example: Navy body fat for a man 175/70 and a woman 165/55",
"Man: height 175 cm, neck 38 cm, waist 82 cm.\nwaist−neck=44; log10(44)=1.6435, log10(175)=2.2430.\nd=1.0324−0.19077×1.6435+0.15456×2.2430=1.0655; bf=495/1.0655−450=14.5%. Men's grading 14≤14.5<18 → healthy.\nWoman: height 165 cm, neck 33 cm, waist 75 cm, hip 95 cm.\nwaist+hip−neck=137; log10(137)=2.1367, log10(165)=2.2175.\nd=1.29579−0.35004×2.1367+0.22100×2.2175=1.0379; bf=495/1.0379−450=27.0%. Women's grading 25≤27.0<32 → acceptable.\nConclusion: the two examples are about 14.5% and 27.0%, both in reasonable ranges; the circumference measurements are extremely sensitive to input, so always measure strictly at the labelled sites.",
"What is the difference between the Navy method and the skinfold method?",
"The Navy method needs only circumferences (waist + neck for men, waist + hip + neck for women), while the skinfold method needs callipers at several sites; both are estimates (±3-4% error), and the Navy method is more sensitive to ",
"waist-to-hip ratio",
" and measurement technique, which makes it suited to self-testing when no callipers are available.",
"Why must women measure hip circumference?",
"Women's fat distribution differs from men's, so hip circumference is needed to derive body fat reasonably from circumferences; missing the hip measurement or misaligning the waist and hip will bias the result, so hip circumference is required for women.",
'About "Body Fat Estimation"',
"The US Navy body fat formula estimates body-fat percentage from simple circumference measurements, with no equipment, and is suited to everyday self-testing and tracking fat-loss progress.",
"Navy body fat circumference formula",
"Automatically switches the algorithm by sex",
"Includes body-fat rating and composition",
"Estimate from circumference measurements alone",
"Body fat self-testing without equipment",
"Tracking progress over a fat-loss cycle",
"Assessing abdominal fat",
"Estimating body fat for enlistment physicals",
"Height",
"Waist circumference",
"Neck circumference",
"Hip circumference",
],
'generator': [
"✨ Barbell and Dumbbell Plate Combination Generator",
"Barbell and dumbbell plate combination generator — an online tool",
'📖 View the "Barbell/Dumbbell Plate Combination Generator Guide"',
"Plate combination generation: solve a subset against the target weight and the available plate sizes (e.g. one pair each of 25/20/15/10/5/2.5/1.25 kg), outputting a loading scheme that reaches the target weight.",
"📚 In-Depth Analysis: Barbell/Dumbbell Plate Combination Generator",
"Quickly generate several plate schemes for target weights before training, removing the mental arithmetic of plate combinations.",
"Beginners can learn how standard plates (1.25/2.5/5/10/15/20/25 kg) stack up to a target weight.",
"Generate several different target weights in one batch, handy for super-sets / drop-sets.",
"Walkthrough: generating 5 plate combinations",
"Steps: count cnt=5, click Generate. The tool randomly gives 5 target weights from 5 to 85 kg and automatically loads the bar and plates for each.\nExample output (illustrative, random each time): group 3, target 52.5 kg → bar 20 kg + plates 25+5+2.5 kg = actual 52.5 kg.\nNote: the plate library is fixed at [1.25, 2.5, 5, 10, 15, 20, 25] kg, with a limit of 6 plates stacked per side; the results are random illustrations that refresh on every click, intended to inspire loading ideas rather than form a fixed plan.",
"Why is the result different every time?",
"The generator uses random target weights and random plate combinations to give you many loading ideas; if you need a fixed plan, write down a particular result or plan it manually — this tool does not save generation history.",
"How do I read the loading?",
"It outputs bar X kg + plates A+B+… kg = actual Y kg, where the plate weight is the total on both sides (including left and right); during training, simply load plates symmetrically on both sides according to that combination.",
'About "Barbell and Dumbbell Plate Combination Generator"',
"Barbell and dumbbell plate combination generator. A free online tool that runs entirely in the front end, uploading no data and protecting your privacy.",
],
'jianzhinengliangquekoujisuan': [
"⚡ Fat Loss Calorie Deficit",
"Based on the energy-conservation principle of 1 kg of fat ≈ 7700 kcal, compute the daily calorie deficit needed to reach a fat-loss goal and a diet/exercise allocation plan.",
'📖 View the "Fat Loss Calorie Deficit Guide"',
"Daily calorie deficit = target fat loss (kg) × 7700 / (weeks × 7); weekly fat loss = target / weeks; weight-loss rate % = weekly fat loss / body weight × 100; diet deficit = daily deficit × diet share, exercise deficit = daily deficit × (1 − share)",
"Derived by energy conservation with 1 kg of fat ≈ 7700 kcal: first divide the total energy by the number of days to get the daily deficit, then split it by the set ratio into a diet reduction and an exercise burn, and give a safety assessment and advice based on the weight-loss rate.",
"Target fat loss (kg)",
"Planned duration (weeks)",
"Diet / exercise split",
"Diet 75% + exercise 25%",
"Diet 60% + exercise 40%",
"Diet 50% + exercise 50%",
"Diet 40% + exercise 60%",
"💡 1 kg of body fat ≈ 7700 kcal. Safe fat-loss rate: 0.5-1.0 kg per week (daily deficit 500-1000 kcal), and it should not exceed 1% of body weight.",
"The daily calorie deficit is best kept under 1000 kcal, with women not below 1200 kcal/day and men not below 1500 kcal/day",
"Early fat loss includes water loss, so rapid weight drop in the first 1-2 weeks does not mean pure fat loss",
"For the exercise part, combine strength and cardio to avoid muscle loss lowering your basal metabolism",
"A plateau calls for adjusting diet and training; simply enlarging the deficit can cause metabolic adaptation",
"📚 In-Depth Analysis: Fat Loss Calorie Deficit",
"Set a goal of how many kilograms to lose in how many weeks, and work backwards to how much",
"calorie deficit",
" you need to create each day, then break it down into diet and exercise.",
"Use the safe-rate threshold (weekly weight loss as a share of body weight) to assess whether the plan is too fast and how high the muscle-loss risk is.",
"Give the kcal each side needs to cut/burn according to the diet/exercise split (default diet 75% + exercise 25%), and project the completion date.",
"Reproducible example: lose 5 kg / 8 weeks / 75 kg / diet 75%",
"Input: target target=5 kg, period weeks=8, body weight w=75 kg, diet/exercise split ratio=0.75.\nTotal energy deficit totalKcal=5×7700=38500 kcal (1 kg of fat ≈ 7700 kcal).\nDaily deficit dailyDeficit=38500/(8×7)=687.5→688 kcal.\nWeekly fat loss weeklyKg=5/8=0.625 kg; share of body weight ratePct=0.625/75×100=0.83%/week → safeCheck judges safe (≥0.5).\nSplit: diet reduction dietKcal=688×0.75≈516, exercise burn exerKcal=688×0.25≈172 kcal/day.\nFinal weight=75−5=70 kg; expected completion date=today+56 days.",
"Why use 7700 kcal?",
"A widely used international approximation: 1 kg of human fat tissue holds about 7700 kcal of energy, so losing 1 kg of fat requires creating a cumulative deficit of about 7700 kcal; this is an estimate and in reality includes water fluctuations.",
"How do I set the diet/exercise split?",
"The default diet 75% + exercise 25% is easier to sustain; those with good exercise capacity can raise the exercise share (e.g. 50/50). Safety line: losing 0.5-1.0% of body weight per week is the recommended range, >1.0% is on the fast side and >1.5% is too fast (high muscle-loss risk); this tool flags it in red.",
'About "Fat Loss Calorie Deficit"',
"Based on the principle that 1 kg of body fat holds about 7700 kcal, combined with the target fat loss and time period, it computes the daily calorie deficit required, splits it by the diet and exercise ratio, and adds exercise-duration suggestions.",
"Energy-conservation calculation at 7700 kcal/kg",
"Flexible diet and exercise share allocation",
"Safety assessment and risk warnings",
"Duration conversion for 6 activities by MET",
"Designing a science-based fat-loss plan",
"Planning the diet-to-exercise ratio",
"Setting the fat-loss cycle and goal",
"Choosing exercise duration and activities",
"Target fat loss",
"Planned duration",
"Current body weight",
"Diet and exercise split",
],
'load': [
"🏋️ Progressive Overload Planner",
"Generate a weekly increasing plan from your current training data, with a deload week every four weeks to progress strength scientifically.",
'📖 View the "Progressive Overload Weight Planning (Linear Progression + Deload Week) Guide"',
"Non-deload week w_k = w_(k−1) × 1.025; every 4 weeks deload w = w_(k−1) × 0.9; weekly volume = w × sets × reps",
"Rising by a weekly +2.5% progressive overload, with a deload week every 4th week (weight reduced to 90%) to promote recovery. Total training volume counts only non-deload weeks; total gain = final-week weight − starting weight, gain% = gain / starting weight × 100.",
"Current weight (kg)",
"Planned weeks",
"💡 Increase the weight by about 2.5% per week (compound lifts) and deload 10% every 4 weeks to promote recovery. Volume = weight × sets × reps.",
"Progressive overload is the core principle of strength gain, but it needs to be paired with adequate recovery",
"If you cannot complete the planned sets and reps, reduce the weight or add rest",
"A deload week helps reduce fatigue and prevent overtraining",
"The plan is for reference only; adjust flexibly according to your body's feedback",
"📚 In-Depth Analysis: Progressive Overload Weight Planning (Linear Progression + Deload Week)",
"Before powerlifting/hypertrophy training, plan each week's training weight with a linear progression model to keep a continuous overload stimulus.",
"Insert a deload week every 4 weeks (weight dipping about 10%) to avoid overtraining and promote supercompensation.",
"Export the result as a week-by-week weight table and follow it directly or fine-tune it according to how you feel that day.",
"Reproducible example: an 8-week progression starting at 60 kg",
"Input: starting weight 60 kg, 4 sets × 8 reps, period 8 weeks, weekly increase rate 2.5%.\nWeek by week (cur is the end-of-week weight for non-deload weeks, deloading back 10% every 4 weeks):\nWeek 1 60×1.025=61.5, week 2 63.0, week 3 64.6, week 4 deload=64.6×0.9=58.2, week 5 66.2, week 6 67.9, week 7 69.6, week 8 deload=69.6×0.9=62.6 kg.\nEnding weight endW≈69.6 kg, +9.6 kg from the start (+16.0%); weekly volume 61.5×4×8=1968 in the first week and 69.6×4×8≈2227 kg in the last training week.\nConclusion: the 8-week linear plan pushes the main lift from 60 kg to about 69.6 kg, with weeks 4 and 8 as deload weeks for recovery.",
"Is a 2.5% increase rate suitable?",
"For beginners/intermediate lifters a 2-5% weekly linear increase is common and safe; advanced lifters, being close to their limits, often switch to periodisation (e.g. 3 weeks up, 1 week deload) or undulating loads. This tool uses a fixed 2.5% as a clear demonstration, and in practice you can lower it at a plateau.",
"Will a deload week cancel out progress?",
"No. A deload week only dips about 10% temporarily and reduces volume, to relieve central-nervous-system and joint fatigue; afterwards recovery brings back a higher starting point (e.g. week 5 above is already higher than week 3), which over the long run favours continued progress.",
'About "Progressive Overload Planner"',
"Progressive overload is the core principle of strength training. This tool generates a weekly increasing plan from your current training data and schedules a deload week every 4 weeks, helping you progress training intensity scientifically.",
"Weekly 2.5% progression plan",
"Automatic deload week every 4 weeks",
"Week-by-week training volume calculation",
"Summary of total weight gain and percentage",
"Strength-training cycle planning",
"Progressing the squat/bench/deadlift",
"Training-volume management",
"Breaking through training plateaus",
"Current weight",
"Sets",
"Reps",
"Planned weeks",
],
'macro-ratio': [
"🥗 Muscle Gain Macro Ratio",
"Compute daily protein, carbohydrate and fat grams and their calorie shares for a muscle gain goal from body weight and goal.",
'📖 View the "Macro Ratio (Protein/Carb/Fat Gram Split) Guide"',
"Macro ratio: first compute the basal metabolic rate BMR (Katch-McArdle if body fat is known, otherwise Mifflin-St Jeor), multiply by the activity factor to get TDEE; adjust calories for muscle gain/fat loss/maintenance, then distribute the three macronutrient ratios by intensity.",
"Body-fat percentage (%, optional)",
"Training intensity",
"Light (≤3 times a week)",
"Moderate (4-5 times a week)",
"Heavy (6+ times a week / professional)",
"Muscle-gain phase (calorie surplus)",
"Fat-loss phase (calorie deficit)",
"🍗 Protein intake recommendations",
"Protein per kilogram of body weight (g)",
"Average adult",
"Fitness enthusiast",
"Muscle-preserving fat-loss phase",
"📋 Comparison of ratio plans",
"Balanced muscle gain",
"General muscle gain",
"High-carb muscle gain",
"High training volume",
"High-protein fat loss",
"Low-carb cycling",
"Low-carb day",
"Muscle gain requires a calorie surplus of about 300-500 kcal/day, with protein spread across 4-5 meals. Getting carbs + protein around training works even better.",
"📚 In-Depth Analysis: Macro Ratio (Protein/Carb/Fat Gram Split)",
"In fat-loss / muscle-gain / maintenance phases, first compute BMR from body weight and body fat, then apply the activity factor to get",
", and finally split the target calories into gram amounts of the three macronutrients.",
"When body fat is provided, the Katch-McArdle formula (based on lean body mass) estimates BMR, which is more accurate than using body weight alone.",
"Switch the protein and fat factors by goal (muscle gain/maintenance/fat loss), and carbs automatically fill the remaining calories.",
"Reproducible example: 70 kg, 18% body fat, moderate activity, maintenance phase",
"Input: body weight 70 kg, body fat 18%, activity=moderate (×1.55), goal=maintenance (protein 1.6, fat 0.9, calorie adjustment 0).\nLean body mass=70×(1−0.18)=57.4 kg; BMR (Katch-McArdle)=370+21.6×57.4≈1610 kcal.\nTDEE=1610×1.55≈2495 kcal; target calories=2495+0=2495 kcal.\nProtein=70×1.6=112 g (448 kcal), fat=70×0.9=63 g (567 kcal), carbs filling in=(2495−448−567)/4=370 g (1480 kcal).\nShares: protein 18% / carbs 59% / fat 23%.\nConclusion: in the maintenance phase, about 2495 kcal per day, with a macronutrient split of 112 g protein / 370 g carbs / 63 g fat.",
"How is BMR calculated without measuring body fat?",
"When body fat is not provided, the tool falls back to a simplified 22×body weight estimate (about 1540 kcal in this example), slightly below Katch-McArdle. It is advisable to measure body fat once with callipers/InBody so that BMR sits closer to actual resting expenditure.",
"During fat loss, is lower carb always better?",
"No. Too little carbohydrate hurts training performance and thyroxine; in this example the fat-loss protein factor rises to 2.2 g/kg to preserve muscle and fat to 0.8 g/kg to maintain hormones, while carbs still supply most of the calories. In general, keeping the fat-loss deficit at 300-500 kcal/day is enough.",
'About "Muscle Gain Macro Ratio"',
"Muscle Gain Macro Ratio is an online tool in the health and medical field. A health-metric calculator based on authoritative medical standards, processing data locally to protect privacy.",
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

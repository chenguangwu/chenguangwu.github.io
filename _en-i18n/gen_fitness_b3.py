#!/usr/bin/env python3
# fitness batch3 (5 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'fitness')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'fitness')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'calc-5': [
"🥗 Daily Protein Requirement",
"Estimate the recommended daily protein intake range from body weight, activity level and training goal.",
'📖 View the "Daily Protein Requirement Guide"',
"Daily protein requirement: pick a factor from body weight and goal — sedentary 0.8 to 1.0, regular training 1.4 to 2.0, muscle gain 1.6 to 2.2, muscle-preserving fat loss 1.8 to 2.4 g/kg — and multiply to get the recommended daily intake range.",
"Regular training",
"High intensity / muscle gain",
"Protein factor (g/kg)",
"Calculate requirement",
"Reference factors",
"Average adult: 0.8 g/kg",
"Regular exercise: 1.2 - 1.6 g/kg",
"Muscle gain / fat loss: 1.6 - 2.2 g/kg",
"Endurance athletes: 1.2 - 1.4 g/kg",
"📚 In-Depth Analysis: Daily Protein Requirement",
"Determine your daily protein intake range from body weight and training volume.",
"Raise the factor by +0.2 to preserve muscle during fat loss (and likewise for muscle gain).",
"Convert grams into food portions (eggs / chicken breast) to make it easy to follow day to day.",
"Reproducible example: protein needs of a 70 kg regular trainee",
"Input: body weight 70 kg, activity level \"Regular training\" 1.6 g/kg, goal \"Muscle gain\" +0.2.\nFactor factor=1.6+0.2=1.8 g/kg; lower bound minFactor=max(0.8, 1.8−0.2)=1.6, upper bound maxFactor=1.8+0.2=2.0.\nDaily protein range=70×1.6 ~ 70×2.0 = 112–140 g.\nRoughly equivalent to 112/6≈19 ~ 140/6≈23 eggs' worth of protein (about 6 g per egg), or 112/30≈4 ~ 140/30≈5 servings of chicken breast (about 30 g protein each).",
"How do I choose the protein factor?",
"Sedentary 0.8, light 1.0, moderate 1.3, regular training 1.6, high intensity / muscle gain 2.0 g/kg; add +0.2 for muscle-preserving fat loss or muscle gain. This tool gives a range rather than a fixed value, so you can fine-tune it to your training volume that day.",
"Is too much protein harmful?",
"High protein is generally safe for healthy people, but those with impaired kidney function need to limit protein. Protein itself does not directly cause weight gain (1 g ≈ 4 kcal); excess gives no extra muscle-building benefit and instead adds metabolic and fluid-intake burden. Prefer getting it from whole foods.",
"Leave blank to use the recommended value",
],
'calc-heart-rate': [
"❤️ Aerobic Heart Rate Zone Calculator",
"Based on the Karvonen (heart rate reserve) formula, compute 5 aerobic training heart-rate zones to guide fat-burning and endurance training scientifically.",
'📖 View the "Aerobic Heart Rate Zone Calculator (Karvonen) Guide"',
"Target heart rate = (maximum heart rate − resting heart rate) × intensity% + resting heart rate",
"Resting heart rate (bpm)",
"💡 Karvonen formula: target heart rate = (maximum heart rate − resting heart rate) × intensity% + resting heart rate; maximum heart rate = 220 − age.",
"Zone percentages are based on heart rate reserve (HRR), making them more individualised than a plain percentage of maximum heart rate",
"Zone 1 warm-up/recovery 50-60%, Zone 2 fat burning 60-70%, Zone 3 aerobic 70-80%, Zone 4 anaerobic threshold 80-90%, Zone 5 maximum 90-100%",
"Heart-rate responses are affected in people with cardiovascular disease or those taking blood-pressure medication; consult a doctor",
"Results are for reference only; in practice combine them with perceived exertion (RPE)",
"📚 In-Depth Analysis: Aerobic Heart Rate Zone Calculator (Karvonen)",
"Set running / cycling / HIIT by target zone (fat burning / endurance / anaerobic threshold)",
"heart-rate zones",
", avoiding inappropriate intensity.",
"Replace \"by feel\" with heart-rate zones to quantify training intensity and build an aerobic base.",
"For rehabilitation or beginners, start safely at low intensity in Z1/Z2 and progress gradually.",
"Reproducible example: Karvonen heart-rate zones",
"Input: age 30, resting heart rate 60. Heart rate reserve HRR=220−30−60=130 bpm.\nZone 2 (fat-burning base 60–70%): lower=130×0.6+60=138, upper=130×0.7+60=151 → 138–151 bpm.\nZone 4 (anaerobic threshold 80–90%): lower=130×0.8+60=164, upper=130×0.9+60=177 → 164–177 bpm.\nFive zones: Z1 50–60%→125–138, Z2 138–151, Z3 151–164, Z4 164–177, Z5 177–190 bpm.",
"Why use the heart rate reserve method (Karvonen)?",
"Karvonen uses the difference between ",
"maximum heart rate",
" and resting heart rate as the baseline and then adds resting back, which is more individualised than using maximum heart rate",
" alone — a lower resting rate (better cardio fitness) gives more accurate zones, avoiding a one-size-fits-all approach.",
"Is maximum heart rate 220 − age accurate?",
"220 − age is a population average, with individual variation of ±10-12 bpm; the Tanaka formula 208 − 0.7×age is more accurate. This tool estimates the ceiling with 220 − age and uses resting heart rate for individualised zones.",
'About "Aerobic Heart Rate Zone Calculator"',
"Uses the Karvonen heart rate reserve method, combining age and resting heart rate to divide 5 aerobic training zones, helping you control exercise intensity precisely and improve fat-burning and endurance training efficiency.",
"Karvonen heart rate reserve formula",
"5 training zones at a glance",
"Labels the training purpose of each zone",
"Aerobic training such as running, cycling and rowing",
"Intensity control during fat loss",
"Setting endurance training zones",
"Configuring target zones on heart-rate devices",
"Resting heart rate",
],
'calculator-calc-13': [
"📏 Body Fat Percentage (Skinfold Method)",
"Based on the Jackson-Pollock three-site skinfold method, combine sex and age to estimate body density and then convert to body-fat percentage using the Siri equation.",
"Body Fat Percentage (Skinfold Method) Calculator",
'📖 View the "Body Fat Percentage (Skinfold Method) Guide"',
"Body fat % = 495 / D − 450 (Siri); Σ₃ = s₁ + s₂ + s₃; men D = 1.109380 − 0.0008267Σ + 0.0000016Σ² − 0.0002574×age; women D = 1.0994921 − 0.0009929Σ + 0.0000023Σ² − 0.0001392×age",
"Jackson-Pollock three-site skinfold method: for men, chest, abdomen and thigh; for women, triceps, suprailiac and thigh (units mm). First obtain body density D from Σ, then convert to body-fat percentage with the Siri equation; combined with body weight, it further gives fat mass and lean body mass.",
"Body weight (kg, used to compute fat / lean mass)",
"Chest skinfold (mm)",
"Abdominal skinfold (mm)",
"Thigh skinfold (mm)",
"💡 Men: chest + abdomen + thigh; women: triceps + anterior superior iliac spine + thigh. Siri formula: body fat % = 495 / body density − 450.",
"Requires a trained person to measure at standard anatomical sites with skinfold callipers; error can be ±3-5%",
"Measurement sites: for men, chest (midaxillary at the nipple), abdomen (2 cm beside the navel) and front of thigh; for women, triceps, anterior superior iliac spine and thigh",
"Take the average of 2-3 measurements per site, pinching the skin and subcutaneous fat without including muscle",
"This formula applies to the general population aged 18-80; accuracy declines for athletes and older adults",
"📚 In-Depth Analysis: Body Fat Percentage (Skinfold Method)",
"Estimate from 3 skinfold sites (triceps / subscapular / suprailiac)",
"body-fat percentage",
" and fat / lean body mass.",
"Gym-goers track body composition to distinguish fat loss from muscle loss.",
"Uses a different regression for each sex (men's and women's measurement sites and constants differ).",
"Reproducible example: 3-site measurement for a man",
"Input: male, age 30, body weight 70 kg, skinfolds s1/s2/s3=10/10/10 mm (sum=30).\nBody density D=1.109380−0.0008267×30+0.0000016×30²−0.0002574×30=1.109380−0.024801+0.00144−0.007722=1.07830 g/cm³.\nBody fat bf=495/1.07830−450≈459.1−450=9.1% (athlete range).\nFat mass=70×9.1%=6.37 kg, lean body mass=63.6 kg.\nFor women, convert likewise using D=1.0994921−0.0009929×sum+0.0000023×sum²−0.0001392×age.",
"Which three sites are measured?",
"The sites usually measured are triceps, subscapular and anterior superior iliac spine (abdomen); men can also use chest + abdomen + thigh. Pinch the skinfold and subcutaneous fat (not including the muscle fascia), read in mm, average 2-3 readings, and keep the same measurer for the most stable results.",
"How does this differ from bodyfat-caliper?",
"Both use the skinfold method. This tool fixes 3 sites (Durnin-Womersley regression for men/women), while bodyfat-caliper supports switching between 3/4/7 sites; the formulas and sites differ slightly, so treat the results as a trend reference and do not expect the two tools to match exactly.",
'About "Body Fat Percentage (Skinfold Method)"',
"Uses the classic Jackson-Pollock three-site skinfold method, selecting three measurement sites according to sex, combining age to estimate body density and then converting to body-fat percentage with the Siri equation — one of the common methods used in physical assessments.",
"Jackson-Pollock three-site formula",
"Automatically switches measurement sites by sex",
"Converts body-fat percentage with the Siri equation",
"Includes body-fat rating and composition breakdown",
"Gym body assessments and tracking",
"Body-composition monitoring during fat loss",
"Athlete selection and fitness assessment",
"Baseline data for nutrition consultation",
"Skinfold 1",
"Skinfold 2",
"Skinfold 3",
],
'calculator-calc-constitution': [
"🧮 BMI Calculator",
"Enter height and weight to compute body mass index (BMI), and get a body-assessment grade and healthy weight range based on the Chinese adult standard.",
"BMI Calculator",
"/ BMI Calculator",
'📖 View the "BMI Calculator (Chinese Standard) Guide"',
"BMI = weight (kg) / height (m)²; <18.5 underweight, 18.5–24 normal, 24–28 overweight, ≥28 obese.",
"💡 BMI = weight (kg) ÷ height² (m²). Chinese adult standard: 18.5-23.9 normal, 24-27.9 overweight, ≥28 obese.",
"BMI does not distinguish muscle from fat; muscular people may score high yet not be overweight",
"This standard applies to Chinese adults over 18; it does not apply to children or pregnant women",
"Waist circumference is also an important indicator: ≥90 cm for men and ≥85 cm for women suggests central obesity",
"Results are for reference only; for body composition, judge together with body-fat percentage",
"📚 In-Depth Analysis: BMI Calculator (Chinese Standard)",
"Quickly calculate BMI and compare with the Chinese standard after a health check",
" range.",
"Distinguish muscular pseudo-overweight from true obesity (combining waist circumference / body fat).",
"Set weight-management goals and clinical reference points by BMI.",
"Reproducible example: BMI and ideal weight for 175 cm / 70 kg",
"Input: height 175 cm, weight 70 kg.\nBMI=70/(1.75²)=70/3.0625=22.86 (normal on the Chinese standard, 18.5–23.9).\nIdeal weight range: lower 18.5×3.0625≈56.7 kg, upper 23.9×3.0625≈73.2 kg; the commonly used ideal value is 22×3.0625≈67.4 kg.\nConclusion: 70 kg falls in the healthy range, and a target can be set within 56.7–73.2 kg.",
"What is the difference between the Chinese standard and WHO?",
"Asians develop metabolic risk at a lower BMI, so the Chinese standard sets the overweight line at 24 and the obesity line at 28, lower than the WHO's 25/30; this tool uses the Chinese standard (18.5–23.9 normal).",
"Does a normal BMI mean you are healthy?",
"Not necessarily. BMI does not distinguish fat from muscle: gym-goers may have a high BMI but low body fat (pseudo-overweight), while a \"skinny fat\" person has a normal BMI but high visceral fat. It is advisable to combine waist circumference, ",
"body-fat percentage",
" for a comprehensive assessment.",
'About "BMI Calculator"',
"Body mass index (BMI) is a common indicator of the ratio of weight to height. This tool grades body assessment against the Chinese adult standard and gives a healthy weight range and an ideal-weight reference.",
"Chinese adult BMI standard",
"Healthy weight range calculation",
"Ideal weight (BMI 22) reference",
"Clear display of the body-assessment grade",
"Everyday self-assessment of weight",
"Setting fat-loss goals",
"Interpreting health-check reports",
"Recording a health profile",
"Height",
],
'calculator-calc-heart-rate': [
"❤️ Maximum Heart Rate Calculator",
"Enter your age to estimate maximum heart rate using several formulas (Fox, Tanaka, Gellish, Arena) and get training zones based on the average.",
'📖 View the "Maximum Heart Rate Estimation (Multi-Formula Cross-Check) Guide"',
"Maximum heart rate estimation: Fox 220 − age, Tanaka 208 − 0.7×age, Gellish 207 − 0.7×age, Arena 209 − 0.6×age, averaged over the four; training zones are divided from 50% to 95% of maximum heart rate.",
"💡 Fox: 220 − age; Tanaka: 208 − 0.7×age; Gellish: 207 − 0.7×age; Arena: 209 − 0.6×age.",
"Individual maximum heart rate can vary by ±10 bpm; the formulas are only population estimates",
"The Tanaka formula is more accurate for middle-aged and older adults",
"The high-intensity training zone (85-95%) should not be sustained for long",
"People taking beta-blockers and similar medication have a lower heart-rate ceiling; follow medical advice",
"📚 In-Depth Analysis: Maximum Heart Rate Estimation (Multi-Formula Cross-Check)",
"Before aerobic training such as running, cycling or HIIT, first determine your personal maximum heart rate (HRmax) as the ceiling reference for each intensity zone.",
"Cross-check with the four formulas Fox/Tanaka/Gellish/Arena to avoid the individual-variation bias of a single \"220 − age\".",
"Convert the estimated average maximum heart rate into fat-burning / aerobic / anaerobic training zones to quantify intensity.",
"Reproducible example: maximum heart rate and zones for a 30-year-old",
"Input: age 30.\nFour formulas: Fox=220−30=190; Tanaka=208−0.7×30=187; Gellish=207−0.7×30=186; Arena=209−0.6×30=191.\nAverage maximum heart rate avg=round((190+187+186+191)/4)=round(188.5)=189 bpm.\nFive zones (of avg's",
"): warm-up/recovery 50–60%→95–113, fat burning/base 60–70%→113–132, aerobic endurance 70–80%→132–151, anaerobic threshold 80–90%→151–170, VO2max 90–95%→170–180 bpm.\nConclusion: a 30-year-old's aerobic endurance zone is about 132–151 bpm; use it to pace or to control intensity from a heart-rate strap.",
"Which of the four formulas is the most accurate?",
"Fox (220 − age) is the most classic but has large individual variation; Tanaka (208 − 0.7×age), Gellish (207 − 0.7×age) and Arena (209 − 0.6×age) are more modern regressions and generally run 1-5 bpm higher than Fox. Averaging the four is the safest, and this tool gives the average and each zone directly.",
"How do I use the zones?",
"Fat burning/base (60–70%) suits fat-loss cardio; aerobic endurance (70–80%) improves cardiorespiratory fitness; anaerobic threshold (80–90%) raises the lactate threshold. Beginners should start from Z1–Z2 and progress gradually, not sprint into the high zone every time.",
'About "Maximum Heart Rate Calculator"',
"Maximum heart rate (HRmax) is an important parameter for setting training intensity. This tool gives estimates from the Fox, Tanaka, Gellish and Arena formulas at the same time, and provides training zones based on the average.",
"Comparison of four maximum heart rate formulas",
"Averaging reduces the bias of a single formula",
"5 levels of training heart-rate zones",
"Suitable for different age groups",
"Setting aerobic training intensity",
"Configuring the ceiling on heart-rate devices",
"Comparing results across formulas",
"Reference for designing exercise prescriptions",
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

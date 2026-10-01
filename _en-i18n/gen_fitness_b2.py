#!/usr/bin/env python3
# fitness batch2 (5 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'fitness')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'fitness')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'bodyfat-caliper': [
"🏋️ Skinfold Body-Fat Percentage",
"Measure subcutaneous fat thickness with skinfold callipers and estimate body-fat percentage using the Jackson-Pollock formulas",
'📖 View the "Skinfold Body-Fat Percentage (Skinfold Calliper Method) Guide"',
"Number of measurement sites",
"3-site method (recommended)",
"4-site method",
"7-site method (precise)",
"📏 Skinfold measurements (mm)",
"📍 Measurement site description",
"Body-fat % = 495 / D − 450 (Siri); D is body density, taken from the Jackson-Pollock regression by sex and number of sites",
"3-site (men) D = 1.10938 − 0.0008267Σ + 0.0000016Σ² − 0.0002574×age; 3-site (women) D = 1.0994921 − 0.0009929Σ + 0.0000023Σ² − 0.0001392×age; 7-site men D = 1.112 − 0.00043499Σ + 0.00000055Σ² − 0.00028826×age, women D = 1.097 − 0.00046971Σ + 0.00000056Σ² − 0.00012828×age; Σ is the sum of the skinfold thicknesses at all sites (mm). Having found the body density, convert to body-fat percentage with the Siri formula.",
"Measurement method: pinch the skin and subcutaneous fat (not muscle) between thumb and forefinger, clamp the callipers 1 cm below the pinch point and read after 2 seconds. Measure each site 2-3 times and take the average. Fasting and the same time of day are recommended.",
"The skinfold method has a 3%-5% error; results are for reference only. For a professional body-fat assessment, DEXA or underwater weighing is recommended.",
"📚 In-Depth Analysis: Skinfold Body-Fat Percentage (Skinfold Calliper Method)",
"Gym-goers use skinfold callipers to measure 3/4/7-site skinfold thickness and estimate",
"body-fat percentage",
", tracking body-composition changes during fat-loss and muscle-gain phases.",
"Compared with a BIA body-fat scale, the skinfold method has better repeatability with a fixed measurer/site/timing and suits long-term self-tracking of trends.",
"Choose the site method by goal: 3 sites for beginners, 4 for advanced, 7 for research, to improve precision.",
"Reproducible example: 3-site skinfold body-fat percentage",
"Using the men's 3-site method: skinfold sum=30 mm (e.g. chest+abdomen+thigh 10 mm each), age 30. Body density D=1.0994921−0.0009929×30+0.0000023×30²−0.0001392×30=1.0994921−0.029787+0.00207−0.004176=1.06760 g/cm³. Body-fat bf=495/D−450=495/1.0676−450≈463.7−450=13.7%. Conclusion: this man's body-fat percentage is about 13.7% (athlete range); fat changes can be compared by retesting periodically with the same method.",
"Which is more accurate, the skinfold method or a body-fat scale?",
"The skinfold method has an error of about ±3-4% and depends on measurement technique; a BIA scale fluctuates greatly with hydration, meals and exercise. With a fixed measurer, site and timing (e.g. morning fasted), the long-term trend is more valuable than a single absolute value.",
"How is the sum taken and where do you measure?",
"Clamp the skinfold with the callipers (pinching skin and subcutaneous fat), read in mm, average 2-3 readings, reading about 2 seconds after clamping. The men's 3 sites are usually chest+abdomen+thigh and the women's are usually triceps+suprailiac+thigh; when switching formulas (4/7-site) the sites must match the tool description.",
'About "Skinfold Body-Fat Percentage"',
"The skinfold body-fat percentage tool is an online tool in the health and medical field. A health-metric calculator based on authoritative medical standards, processing data locally to protect privacy.",
],
'calc': [
"⚡ Daily Calorie Needs (TDEE)",
"Compute the basal metabolic rate (BMR) using the Mifflin-St Jeor formula and combine it with an activity factor to obtain the total daily energy expenditure (TDEE).",
"Daily Calorie Needs Calculator",
"/ Daily Calorie Needs Calculator",
'📖 View the "Daily Calorie Needs (TDEE) Guide"',
"BMR = 10×weight + 6.25×height − 5×age + sex constant; TDEE = BMR × activity factor",
"Uses the Mifflin-St Jeor formula: sex constant +5 for men and −161 for women (weight in kg, height in cm, age in years). TDEE (total daily energy expenditure) = BMR × activity factor (1.2 sedentary to 1.9 very intense). Target calories: fat loss = TDEE − 500 kcal/day, maintenance = TDEE, muscle gain = TDEE + 300 kcal/day.",
"Sedentary (little or no exercise)",
"Light (1-3 times a week)",
"Moderate (3-5 times a week)",
"High (6-7 times a week)",
"Extreme (manual labour / athlete)",
"💡 Mifflin-St Jeor: men BMR = 10×kg + 6.25×cm − 5×age + 5; women = 10×kg + 6.25×cm − 5×age − 161. TDEE = BMR × activity factor.",
"For fat loss a daily calorie deficit of 300-500 kcal is recommended, and for muscle gain a surplus of 200-400 kcal",
"The activity factor is an empirical estimate; actual expenditure varies from person to person",
"Pregnant, breastfeeding, adolescent and ill individuals should follow medical advice; this formula does not apply to them",
"Long-term calorie intake should not fall below BMR, to avoid affecting basal metabolism",
"📚 In-Depth Analysis: Daily Calorie Needs (TDEE)",
"Measure total daily expenditure before fat loss / muscle gain",
", and set three calorie targets for fat loss / maintenance / muscle gain.",
"Compare BMR with TDEE to understand the effect of the activity factor on total expenditure.",
"Allocate macros (protein/fat/carbs) by goal and put the diet plan into practice.",
"Reproducible example: TDEE and three target tiers for a 30-year-old man",
"Input: male, 30 years, 175 cm, 70 kg, activity factor 1.55 (moderate). BMR=10×70+6.25×175−5×30+5=1648.75≈1649 kcal; TDEE=1649×1.55=2556 kcal; TDEE (kJ)=2556×4.184≈10690 kJ. Three tiers: fat loss=2556−500=2056, maintenance=2556, muscle gain=2556+300=2856 kcal/day. Macros (maintenance): protein=70×1.6=112 g, fat=2556×0.25/9≈71 g, carbs=(2556−112×4−71×9)/4≈367 g.",
"What deficit/surplus is appropriate?",
"For fat loss a daily deficit of 300-500 kcal is recommended (about 0.3-0.5 kg/week) and for muscle gain a surplus of 200-400 kcal. Too large a deficit easily costs muscle and is hard to sustain; intake should not stay below BMR for long.",
"How are macro ratios set?",
"In maintenance, a common split is protein 1.6 g/kg, fat 25% of calories and the rest carbs; during fat loss, raise the protein share to preserve muscle and slightly lower carbs; during muscle gain, raise carbs. The ratios can be fine-tuned to the training goal; this tool gives maintenance reference values.",
'About "Daily Calorie Needs"',
"Uses the internationally common Mifflin-St Jeor formula to estimate the basal metabolic rate and combines it with the daily activity level to compute the total daily energy expenditure (TDEE), providing calorie-target references for fat loss, maintenance and muscle gain.",
"Mifflin-St Jeor formula",
"5 selectable activity levels",
"Three target tiers: fat loss / maintenance / muscle gain",
"Includes macronutrient allocation references",
"Calorie-target setting during fat loss",
"Diet planning during muscle gain",
"Daily energy-expenditure estimation",
"Calorie baseline for a food diary",
"Height",
"Activity level",
],
'calc-2': [
"🏋️ Basal Metabolic Rate (BMR)",
"Using the Mifflin-St Jeor formula, compute the calories the body burns per day at rest.",
"Basal Metabolic Rate (BMR)",
"/ Basal Metabolic Rate (BMR)",
'📖 View the "Basal Metabolic Rate BMR Guide"',
"BMR = 10×weight (kg) + 6.25×height (cm) − 5×age (years) + 5",
"Enter the data and click Calculate.",
"Men: BMR = 10×weight (kg) + 6.25×height (cm) − 5×age (years) + 5",
"Women: BMR = 10×weight (kg) + 6.25×height (cm) − 5×age (years) − 161",
"BMR is the minimum calories needed to sustain life; the actual daily expenditure is BMR multiplied by an activity factor.",
"📚 In-Depth Analysis: Basal Metabolic Rate BMR (Mifflin-St Jeor)",
"Measure before fat loss / muscle gain",
", then multiply by the activity factor to get",
", and set calorie targets.",
"Compare the total daily expenditure at different activity levels to see directly how exercise contributes to total expenditure.",
"In long-term weight-management follow-up, track BMR changes (with weight/age) and adjust the diet in time.",
"Reproducible example: Mifflin-St Jeor BMR",
"Input: male, 30 years, height 175 cm, weight 70 kg. BMR=10×70+6.25×175−5×30+5=700+1093.75−150+5=1648.75≈1649 kcal. TDEE at different activity levels: sedentary 1.2→1979, light 1.375→2267, moderate 1.55→2556, high 1.725→2845, very high 1.9→3133 kcal. Conclusion: this man burns about 1649 kcal/day at rest and about 2556 kcal with moderate activity; for fat loss set about 2050-2250 kcal/day.",
"What is the difference between Mifflin and Harris-Benedict?",
"This tool uses Mifflin-St Jeor (1990), which is more accurate for modern populations than the classic Harris-Benedict and is recommended by most guidelines; the two usually differ by <5% and can serve as cross-references.",
"Can intake be below BMR?",
"Not recommended. BMR is the minimum expenditure at complete rest; long-term intake below BMR triggers a metabolic slowdown and muscle loss. For fat loss, create a 300-500 kcal deficit based on TDEE rather than dieting below BMR.",
],
'calc-3': [
"🏋️ Body-Fat Percentage Calculator (Navy Formula)",
"Use the US Navy circumference formula to estimate body-fat percentage from neck, waist and hip measurements.",
"Body-Fat Percentage Calculator (Navy Formula)",
"/ Body-Fat Percentage Calculator (Navy Formula)",
'📖 View the "Body-Fat Percentage Calculator (Navy Formula) Guide"',
"Men body-fat % = 86.010×log₁₀(waist−neck) − 70.041×log₁₀(height) + 36.76; women body-fat % = 163.205×log₁₀(waist+hip−neck) − 97.684×log₁₀(height) − 78.387",
"The US Navy circumference method, in cm. Men need only neck and waist, while women add the hip term. After truncating the result to the 2%-60% range, a rating by sex is given: essential fat / healthy / acceptable / high / obese.",
"Waist (cm, at the navel)",
"Enter the circumferences and click Calculate.",
"Reference ranges (adults)",
"Essential fat",
"Athlete",
"📚 In-Depth Analysis: Body-Fat Percentage Calculator (US Navy Formula)",
"When no callipers are available, use a tape to measure the waist/neck (plus hip for women) and estimate",
"body-fat percentage",
", suitable for home self-testing.",
"Compared with the skinfold method and BIA, the Navy method needs only circumferences and is the simplest to perform.",
"Track the body-fat change from a shrinking waist during fat loss to quantify the effect.",
"Reproducible example: US Navy formula (metric)",
"Men: height 175 cm, neck 38 cm, waist 85 cm. waist−neck=47; log10(47)=1.6721, log10(175)=2.2430. bf=86.010×1.6721−70.041×2.2430+36.76=143.81−157.08+36.76=23.49%. By the men's scale: <14 healthy, <18 acceptable, <25 high → 23.5% is \"high\". Women: bf=163.205×log10(waist+hip−neck)−97.684×log10(height)−78.387, requiring the hip measurement too; the formula is extremely sensitive to circumference conventions, so measure strictly at the sites marked by the tool (in cm); if the result is abnormally high, first check the waist/hip/neck measurement positions and tightness.",
"How does the Navy method differ from the skinfold method?",
"The Navy method needs only circumferences (waist+neck for men, waist+hip+neck for women), while the skinfold method needs multiple calliper sites; both are estimates (±3-4% error), and the Navy method is more sensitive to the",
"waist-to-hip ratio",
"and measurement conventions, making it suitable for self-testing when no callipers are available.",
"Why must women measure the hip?",
"Women's fat distribution differs from men's, and adding the hip allows a reasonable estimate of body fat from circumferences; a missing hip measurement or a misplaced waist/hip measurement causes bias, so the hip input is required for women.",
],
'calc-4': [
"⚖️ 1RM Maximum Weight Estimation",
"From a known weight and completed reps, estimate the one-rep max using several classic formulas.",
"1RM Maximum Weight Estimation",
"/ 1RM Maximum Weight Estimation",
'📖 View the "1RM Maximum Weight Estimation Guide"',
"1RM maximum weight estimation: Epley 1RM = W × (1 + R ÷ 30); Brzycki 1RM = W × 36 ÷ (37 − R); Lombardi 1RM = W × R^0.10; W is the weight and R the number of reps completed.",
"Weight lifted (kg)",
"Reps (1-12)",
"Enter the weight and reps and click Calculate.",
"Training-load reference (relative to the estimated 1RM)",
"1-5 reps",
"Strength",
"6-12 reps",
"Hypertrophy",
"8-15 reps",
"15+ reps",
"📚 In-Depth Analysis: 1RM Maximum Weight Estimation",
"Strength trainees use a submaximal weight to estimate",
", avoiding direct maximal attempts that risk injury.",
"In periodised training, retest the 1RM regularly to quantify strength gains and adjust the training load.",
"Based on the 1RM",
", set intensity (e.g. 80% for 5-6 reps, 90% for 2-3 reps).",
"Reproducible example: estimating 1RM from 100 kg × 5 reps",
"Input: weight 100 kg, reps 5. Epley=100×(1+5/30)=116.7 kg; Brzycki=100/(1.0278−0.0278×5)=100/0.8888=112.5 kg; Lombardi=100×5^0.10=100×1.1746=117.5 kg; Mayhew=100×100/(52.2+41.9×e^(−0.055×5))=100×100/(52.2+31.82)=119.0 kg. Average 1RM=(116.7+112.5+117.5+119.0)/4≈116.4 kg. Conclusion: the max here is about 116 kg; for training use 80%≈93 kg for 5-6 reps and 90%≈105 kg for 2-3 reps.",
"Which of the four formulas is most accurate?",
"Epley is the most common and fairly accurate for reps≤10; Brzycki is close to it; Lombardi is more conservative; Mayhew is steadier at higher reps. Averaging smooths single-formula bias, but all are estimates.",
"How many reps give the most accurate estimate?",
"Estimates are reliable within 1-10 reps, with greater error at higher reps; fewer reps (e.g. 3) are closer to the true 1RM. This tool limits reps to 1-12; beyond that, test with fewer reps or lower expectations.",
],
}

# term-link nodes missed by extract: zh -> en
EXTRA = {
}

def build(slug, en_list):
    path = os.path.join(WORK, slug + '.json')
    wj = json.load(open(path, encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('!! %s length mismatch %d vs %d' % (slug, len(en_list), len(items)))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if not en or not isinstance(en, str):
            print('!! %s empty translation' % slug)
            sys.exit(1)
        if CJK.search(en) or CNP.search(en):
            print('!! %s CJK/CNP violation: %s' % (slug, en[:60]))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('!! %s EXTRA CJK/CNP violation: %s' % (slug, en[:60]))
            sys.exit(1)
        mp[z] = en
    return mp

def write(slug, mp):
    os.makedirs(OUT, exist_ok=True)
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('name', slug)
    out = {'slug': slug, 'industry': 'fitness', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

for slug, en_list in EN.items():
    write(slug, build(slug, en_list))

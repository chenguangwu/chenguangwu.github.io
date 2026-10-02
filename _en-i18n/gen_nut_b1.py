#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'nutrition')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'nutrition')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
DISCL = "Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected."
EXTRA = {}
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
            print('BAD EN', slug, repr(z), repr(en)); sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en)); sys.exit(1)
        mp[z] = en
    return mp
def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'nutrition', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('rater-32', build('rater-32', [
        "📋 DASH (Blood Pressure Control) Diet Score",
        "Blood pressure control",
        "The DASH diet score = whole grains + vegetables + fruit + low-fat dairy + sodium intake + nuts and beans + red meat + sweets and sugary drinks (8 items scored 1 to 5 each, 40 points total). Adherence = total score ÷ 40 × 100%. At least 80% means high adherence, 60% to 79% means moderate, and below 60% means low. The key to qualifying is plenty of vegetables and fruit plus limited sodium.",
        "DASH blood pressure control diet score (8 items, assessing adherence to a blood pressure control diet)",
        "1. Whole grains (servings per day)",
        "More than 6 servings (5 points)",
        "3 to 5 servings (3 points)",
        "1 to 2 servings (1 point)",
        "Almost never (0 points)",
        "2. Vegetables (servings per day)",
        "4 to 5 servings (5 points)",
        "2 to 3 servings (3 points)",
        "1 serving (1 point)",
        "3. Fruit (servings per day)",
        "4. Low-fat dairy",
        "2 to 3 servings (5 points)",
        "1 serving (3 points)",
        "None (0 points)",
        "5. Sodium intake (mg per day)",
        "Below 1500 mg (5 points)",
        "1500 to 2300 mg (3 points)",
        "2300 to 3500 mg (1 point)",
        "Above 3500 mg (0 points)",
        "6. Nuts and beans (times per week)",
        "4 to 5 times (5 points)",
        "2 to 3 times (3 points)",
        "1 time (1 point)",
        "7. Red meat (times per week)",
        "Fewer than 2 times (5 points)",
        "3 to 4 times (3 points)",
        "5 to 6 times (1 point)",
        "Every day (0 points)",
        "8. Sweets and sugary drinks",
        "Fewer than once a week (5 points)",
        "1 to 3 times a week (3 points)",
        "4 to 6 times a week (1 point)",
        "Every day (0 points)",
        "Compute the DASH Score",
        "📚 Deep Dive: DASH Blood Pressure Control Diet Score",
        "Score adherence to a blood pressure control diet across 8 indicators to get a total",
        "Optimize the sodium to potassium ratio and the proportion of whole grains, vegetables and fruit for people with hypertension",
        "Track the score to see how dietary improvement supports blood pressure",
        "Scoring Dimensions",
        "DASH focuses on sodium below 2300 mg (ideally below 1500 mg), potassium at 4700 mg, whole grains, 8 to 10 servings of vegetables and fruit, 2 to 3 servings of low-fat milk, nuts and beans, less red meat and sweets, and less saturated fat. The more of the 8 items you meet, the higher the score.",
        "Adjusting Sodium and Potassium",
        "Replace lunch meats and pickles with steamed vegetables plus a banana, which is high in potassium. Sodium drops from 2300 to within 1500 while potassium rises above 4000, improving both the score and blood pressure support.",
        "What Is the Relationship Between DASH and Salt Reduction?",
        "Salt reduction is the core, but DASH also adjusts the whole pattern: high potassium, magnesium and calcium plus whole grains, vegetables, fruit and low-fat dairy work together to lower blood pressure better than simply eating less salt.",
        "Can a High Score Replace Medication?",
        "No. DASH is a lifestyle aid and cannot replace medication. Anyone already taking antihypertensive drugs should still follow medical advice and use the diet as support.",
        "About DASH (Blood Pressure Control) Diet Score",
        "DASH (Blood Pressure Control) Diet Score. A free online tool, processed entirely in the browser, uploads no data and protects your privacy and security.",
    ]))
    write('calc-60', build('calc-60', [
        "⚡ Weight Loss Energy Deficit Calculator",
        "Computes basal metabolic rate and daily total expenditure (TDEE) with the Mifflin-St Jeor formula, plans the daily energy deficit and intake needed to reach a target weight, and outputs a weekly weight loss trajectory.",
        "Core formulas (by input variable): (w−target)×7700; dailyDeficit×7÷7700; weeks×7",
        "Target weight (kg)",
        "Sedentary (desk job, no exercise)",
        "Light (1 to 3 times a week)",
        "Moderate (3 to 5 times a week)",
        "Active (6 to 7 times a week)",
        "Very active (manual labor or athlete)",
        "Planned duration (weeks)",
        "Custom TDEE (optional; overrides the calculated value when greater than 0)",
        "💡 BMR (Mifflin): male = 10W+6.25H−5A+5, female = 10W+6.25H−5A−161; 1 kg of fat ≈ 7700 kcal; safe weight loss is 0.5 to 1 kg per week.",
        "Daily intake should never fall below BMR, since staying below basal metabolic rate long term harms health",
        "Losing 0.5 to 1 kg per week is recommended, because faster loss tends to lose muscle and rebound",
        "Actual weight loss is also affected by diet structure, exercise, sleep and hormones",
        "This tool gives estimates and does not replace advice from a professional nutritionist or physician",
        "📚 Deep Dive: Weight Loss Energy Deficit Calculator (Weekly Trajectory)",
        "Set a target weight and compute the daily deficit and the estimated weeks to reach it",
        "Convert the deficit into weekly loss using 7700 kcal ≈ 1 kg of fat",
        "Judge whether the deficit is safe (0.5 to 1 kg per week is preferable)",
        "Weekly Loss Estimate",
        "At 2400 kcal with a daily deficit of 500 kcal, the weekly loss = 500×7/7700 ≈ 0.45 kg per week; losing 7 kg takes about 15 to 16 weeks, while a deficit of 1000 gives about 0.91 kg per week, close to the upper limit.",
        "Safety Check",
        "A deficit of 1200 kcal per day gives a weekly loss of 1200×7/7700 ≈ 1.09 kg, and exceeding 1 kg per week risks losing muscle and rebounding, so the deficit should be reduced to 500 to 750 kcal per day.",
        "Is 7700 kcal Accurate?",
        "It is roughly the energy in 1 kg of body fat, but actual weight change also involves water and muscle, so treat it as a planning approximation. Real weight loss tends to be fast at first and slower later.",
        "Is Faster Weight Loss Better?",
        "No. More than 1 kg per week mostly loses water and muscle and rebounds. A rate of 0.5 to 1 kg per week preserves muscle better and is sustainable.",
        "About Weight Loss Energy Deficit Calculation",
        "A weight loss energy deficit planning tool that computes BMR and TDEE with the Mifflin-St Jeor formula, plans the daily energy deficit and intake needed to reach a target weight, outputs a weekly weight loss trajectory and flags a safe rate of loss.",
        "Automatic BMR and TDEE calculation",
        "Daily energy deficit planning",
        "Weekly weight loss trajectory",
        "Safe rate and intake validation",
        "Building a personal fat loss plan",
        "Fitness and diet planning",
        "Assisting a nutritionist with calculations",
        "Setting weight management goals",
    ]))
    write('calc-2', build('calc-2', [
        "⚡ Food Calorie Calculator",
        "Quickly compute the calories of a meal from a common food database or by entering macronutrients manually.",
        "\"Quickly compute the calories of a meal from a common food database or by entering macronutrients manually.\" performs a professional calculation from the input parameters and outputs the result.",
        "Method 1: Choose a common food",
        "Rice (100 g)",
        "Whole wheat bread (100 g)",
        "Egg (100 g)",
        "Chicken breast (100 g)",
        "Beef (100 g)",
        "Pork (100 g)",
        "Salmon (100 g)",
        "Tofu (100 g)",
        "Apple (100 g)",
        "Banana (100 g)",
        "Broccoli (100 g)",
        "Carrot (100 g)",
        "Milk (100 ml)",
        "Mixed nuts (100 g)",
        "Yogurt (100 g)",
        "Weight (g)",
        "Add to list",
        "Method 2: Enter nutrients manually",
        "Carbohydrate (g)",
        "Protein (g)",
        "Fat (g)",
        "Click Calculate after adding a food or entering the nutrients.",
        "📚 Deep Dive: Food Calorie Calculator (Accumulating by Portion)",
        "Record the multiple foods in one meal and scale calories and macronutrients from a 100 g baseline to the actual weight",
        "Check the nutrition label on the packaging to see what share of the daily budget the actual intake takes",
        "Back out carbohydrate when adding protein and fat manually: carbs = (kcal − protein×4 − fat×9)/4",
        "Scaling by Portion",
        "Chicken breast per 100 g = 165 kcal / 31 g protein / 3.6 g fat; eating 150 g gives ratio=1.5, so 247.5 kcal, 46.5 g protein and 5.4 g fat; carbs = (247.5 − 46.5×4 − 5.4×9)/4 ≈ 0.",
        "Meal Total",
        "Rice 200 g (232 kcal) + chicken breast 150 g (247.5) + broccoli 100 g (34) ≈ 513.5 kcal; total protein is about 46.5+2.8 ≈ 49 g and total fat about 5.4+0.4 ≈ 5.8 g.",
        "What Are the Calorie Coefficients of the Three Macronutrients?",
        "Protein 4, carbohydrate 4, fat 9 and alcohol 7 kcal/g. Carbohydrate can be derived by subtracting the calories of protein and fat from the total.",
        "Why Does the Computed Carbohydrate Come Out Negative?",
        "It means the protein and fat calories on the package already exceed the total calories, which means the label is rounded or mislabeled. Trust the measured label and take 0 when necessary.",
    ]))

if __name__ == '__main__':
    main()
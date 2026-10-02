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
    write('calc-1', build('calc-1', [
        "🥗 Daily Nutrient Requirements",
        "Estimates daily calories and the three macronutrient requirements from body data, activity level and goal.",
        "\"Estimates daily calories and the three macronutrient requirements from body data, activity level and goal.\" performs a professional calculation from the input parameters and outputs the result.",
        "⚠️ This tool serves only as a reference for dietary nutrition estimates and does not replace individualized nutrition therapy from a nutritionist or physician. Pregnant people, those with chronic disease and those on medication should consult a professional.",
        "Light activity (1 to 3 times a week)",
        "Moderate activity (3 to 5 times a week)",
        "High activity (6 to 7 times a week)",
        "Very high activity (manual labor or athlete)",
        "Fat loss",
        "Compute Requirements",
        "Click Calculate after filling in your data to see your daily nutrient requirements.",
        "Basal metabolic rate is computed with the Mifflin-St Jeor formula.",
        "Daily total expenditure (TDEE) = BMR × the activity factor.",
        "Protein is estimated at 1.8 g/kg of body weight, fat takes 25%, and the remaining calories go to carbohydrate.",
        "📚 Deep Dive: Daily Nutrient Requirements (BMR, TDEE, Macronutrients)",
        "Before gaining muscle or losing fat, compute from body data",
        "and set daily calorie and protein targets",
        "Estimate basal metabolism with Mifflin-St Jeor and multiply by the activity factor for total expenditure",
        "Allocate the three macronutrients with protein at 1.8 g/kg, fat at 25% of calories and carbohydrate taking the remainder",
        "Calculating Requirements for Men",
        "A man of 65 kg, 170 cm, age 28, moderate activity: BMR = 10×65+6.25×170−5×28+5 = 1577.5 kcal; TDEE = 1577.5×1.55 ≈ 2445 kcal. Protein = 65×1.8 = 117 g (468 kcal), fat = 2445×25%÷9 ≈ 68 g, carbohydrate = (2445−468−611)÷4 ≈ 342 g.",
        "Activity Factors",
        "Sedentary 1.2, light 1.375, moderate 1.55, high 1.725, very high 1.9. The same BMR of 1577.5 gives only 1893 with 1.2 but reaches 2997 with 1.9, a difference of about 1100 kcal.",
        "Which BMR Formula Is More Accurate?",
        "Mifflin-St Jeor fits modern people better than Harris-Benedict. It adds 5 for men and subtracts 161 for women, and takes age, height (cm) and weight (kg) as inputs.",
        "Who Is Protein at 1.8 g/kg Suited For?",
        "Athletes and people gaining muscle commonly use 1.6 to 2.2 g/kg, while sedentary adults need only about 0.8 to 1.0 g/kg, and people with kidney disease should lower it under medical advice.",
    ]))
    write('assessor-17', build('assessor-17', [
        "📋 Additive (Intake Assessment) Safety Amount",
        "Intake assessment",
        "The acceptable daily intake (ADI) is given per kilogram of body weight. Intake (mg) = food amount (g) × additive concentration (mg/kg) ÷ 1000; intake per kg of body weight = intake ÷ weight (kg); percentage of ADI = intake per kg ÷ ADI × 100%. Below 50% is safe, 50% to 100% needs attention and above 100% exceeds the limit. Compound additives are assessed by summing each share of ADI.",
        "Daily intake safety assessment of food additives (based on ADI and actual intake)",
        "Additive type",
        "Sodium benzoate (preservative)",
        "Potassium sorbate (preservative)",
        "Sodium nitrite (color fixative)",
        "Sodium saccharin (sweetener)",
        "Aspartame (sweetener)",
        "Sunset Yellow (coloring)",
        "Daily intake of food containing this additive (g)",
        "Additive content in the food (mg/kg)",
        "Assess Safety",
        "📚 Deep Dive: Food Additive ADI Safety Assessment",
        "Compute the safety margin (%ADI) from the ADI and actual intake",
        "When compound additives stack up, check whether total exposure exceeds ADI × body weight",
        "Flag the risk of exceeding limits for food development and compliance self-checks",
        "The ADI for benzoic acid is 0 to 5 mg/kg body weight, so a 60 kg adult can take 5×60 = 300 mg per day. If actual intake is 90 mg, then %ADI = 90/300×100% = 30%, which is safe, while reaching 300 mg hits the 100% ceiling.",
        "Cumulative Assessment",
        "For multiple substances sharing an ADI, such as different preservatives, compute each intake and sum them; if total exposure exceeds ADI × body weight there is a risk, so the formula or the dosage needs adjusting.",
        "What Is ADI?",
        "The acceptable daily intake is the amount that does not pose a health risk when consumed every day for a lifetime (mg/kg body weight). %ADI below 100% is generally considered safe.",
        "How Is Actual Intake Estimated?",
        "Sum the maximum permitted usage of that additive in each food × the amount consumed. Compliant products usually stay within the ADI, and excess usually comes from long-term heavy consumption of a single food.",
        "About Additive (Intake Assessment) Safety Amount",
        "Additive (Intake Assessment) Safety Amount. A free online tool, processed entirely in the browser, uploads no data and protects your privacy and security.",
    ]))
    write('calc-3', build('calc-3', [
        "💪 Carbohydrate / Protein / Fat Ratio",
        "Enter a daily calorie target and the ratio of the three macronutrients to automatically compute the grams and calories of each.",
        "\"Enter a daily calorie target and the ratio of the three macronutrients to automatically compute the grams and calories of each.\" performs a professional calculation from the input parameters and outputs the result.",
        "Balanced diet",
        "Low carb",
        "High carb",
        "Ketogenic diet",
        "Daily calorie target (kcal)",
        "Carbohydrate (%)",
        "Compute Ratio",
        "Click Calculate after entering calories and ratios.",
        "Common references: balanced diet 50/20/30, low carb 20/30/50, high carb 60/20/20, ketogenic 5/25/70 (carbohydrate / protein / fat).",
        "📚 Deep Dive: Converting Macronutrient Ratios into Grams",
        "Given a daily calorie target and the carbohydrate, protein and fat",
        "ratios, compute the grams of each",
        "Apply a preset (balanced, low carb, ketogenic) to see the macronutrient distribution quickly",
        "Adjust the ratios for an energy share sensitivity analysis, such as raising protein to 30%",
        "Computing Grams from the Ratio",
        "For a target of 2000 kcal with 50% carbohydrate, 20% protein and 30% fat: protein = 2000×20%÷4 = 100 g, carbohydrate = 2000×50%÷4 = 250 g and fat = 2000×30%÷9 ≈ 66.7 g.",
        "Preset Comparison",
        "Ketogenic (5 carbohydrate / 25 protein / 70 fat) at 2000 kcal gives 25 g carbohydrate, 125 g protein and 156 g fat, while balanced (50/20/30) gives 250 g carbohydrate and 67 g fat, a whole order of magnitude apart.",
        "How Do Grams Follow from Percentages?",
        "The calories of a nutrient = the target × its ratio; the grams = those calories ÷ the calorie coefficient (protein and carbohydrate ÷ 4, fat ÷ 9). The ratios must sum to 100%.",
        "Is Such a Low Carbohydrate Level in Ketogenic Diets Safe?",
        "Short term it suits specific groups such as those with refractory epilepsy. Long-term very low carbohydrate intake for the general population requires monitoring blood lipids and electrolytes, so a long-term ketogenic diet on your own is not recommended.",
    ]))

if __name__ == '__main__':
    main()
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
    write('rater-33', build('rater-33', [
        "📋 Mediterranean Diet Adherence Score",
        "Score",
        "The Mediterranean diet adherence score = the sum of 14 items scored 0 to 1 each (olive oil as the main fat, adequate olive oil intake, adequate vegetables, adequate fruit, little red meat, little butter, few sugary drinks, few sweets, adequate fish, adequate beans, adequate nuts, adequate whole grains, poultry over red meat, moderate red wine), for a maximum of 14. Adherence = total score ÷ 14 × 100%. At least 70% means high, 40% to 69% means moderate and below 40% means low.",
        "Mediterranean diet adherence score across 14 items (0 to 1 point each, 14 points maximum)",
        "1. Use olive oil as the main cooking fat",
        "2. Use at least 4 tablespoons of olive oil per day",
        "3. At least 2 servings of vegetables per day (200 g each)",
        "4. At least 3 servings of fruit per day (including 1 serving of citrus)",
        "5. Red meat or processed meat fewer than once a week",
        "6. Butter or cream fewer than once a week",
        "7. Sugary drinks fewer than once a week",
        "8. Sweets or pastries fewer than twice a week",
        "9. Fish or seafood at least 3 times a week",
        "10. Beans at least 3 times a week",
        "11. Nuts at least 3 times a week (30 g each)",
        "12. Whole grains or pasta at least 3 times a week",
        "13. Poultry preferred over red meat each week (poultry > red meat)",
        "14. Moderate red wine with meals each day (1 glass for women, 2 for men, optional)",
        "Compute Adherence",
        "📚 Deep Dive: Mediterranean Diet Adherence Score",
        "Score how closely your diet pattern matches across 14 indicators, each 0 to 1 points, for 14 points maximum",
        "A behavioral self-assessment for chronic disease prevention and health management",
        "Targeted improvement of low-scoring items such as olive oil, fish, vegetables and fruit",
        "The 14-Item Scale",
        "A PREDIMED-style 14-point scale: more olive oil, vegetables, fruit, fish and seafood, beans, nuts and whole grains, and less red meat, processed meat, sugary drinks and cream. A score of 9 or more indicates good adherence, while below 6 is low.",
        "Improving the Score",
        "Going from 5 to 9 points: switch to olive oil (1), eat fish 3 times a week (1), nuts every day (1), increase vegetables and fruit (1) and halve red meat (1), which adds 5 points.",
        "What Is the Core of the Mediterranean Diet?",
        "Mostly plant-based, with olive oil as the main fat, moderate fish and poultry, and little red meat, processed meat or added sugar. Multiple studies have confirmed that it lowers cardiovascular risk.",
        "Does a Low Score Mean You Are Unhealthy?",
        "It only reflects how closely you follow this particular pattern. Other healthy diets such as DASH are effective too, so use the score as a reference for your own improvement.",
        "About Mediterranean Diet Adherence Score",
        "Mediterranean Diet Adherence Score. A free online tool, processed entirely in the browser, uploads no data and protects your privacy and security.",
    ]))
    write('index', build('index', [
        "🥗 Nutrition and Diet Tools",
        "Nutrition and Diet",
        "Nutrition and Diet Tools",
        "Calorie Deficit Calculator",
        "The Calorie Deficit Calculator is a free online nutrition and diet tool that returns results in real time as soon as you enter your parameters. It runs entirely in the browser, uploads no data, needs no registration and works the moment you open a browser. Suitable for engineering estimates, everyday conversions and quick verification, with results you can copy in one click.",
        "Choose dishes from a common food database or enter macronutrients manually to quickly accumulate the total calories and macronutrient composition of a meal. Used for everyday diet tracking and calorie control.",
        "Computes the glycemic load (GL) from the GI of a food and the carbohydrate intake, evaluates the post-meal blood glucose impact and gives a high or low classification. Suited to blood glucose control planning, entirely in the browser.",
        "The nutrition label generator automatically lays out a compliant food nutrition label from nutrition data, supporting energy and nutrient declaration. Suitable for prepackaged food compliance.",
        "Computes basal metabolic rate and daily total expenditure (TDEE) with the Mifflin-St Jeor formula, plans the daily energy deficit and intake needed to reach a target weight, and outputs a weekly weight loss trajectory.",
        "Nutrient Intake Reference Percentage",
        "The nutrient percentage calculator computes the percentage of a nutrient's intake relative to its daily reference value (NRV), taking the actual intake and the reference value and returning the share. Suitable for diet tracking and nutrition assessment.",
        "Enter a daily calorie target and the distribution ratio of carbohydrate, protein and fat (such as 5:3:2), and it automatically converts to grams and calories for each nutrient. Used for meal planning and fitness diet design.",
        "Enter sex, age, height, weight, activity level and goal (fat loss, muscle gain or maintenance) to estimate the total daily calorie need plus recommended carbohydrate, protein and fat intake. Used for personalized diet planning.",
        "Estimates recommended vitamin C and zinc intake by population group, lists food sources and upper limits, and is used for immune nutrition self-checks. Pure front-end reference, not a diagnosis.",
        "Estimates daily protein and key vitamin needs from age and weight, and gives dietary source suggestions for nutrition management in older adults. Pure front-end reference, not medical advice.",
        "The dietary fiber recommendation tool sets a daily fiber target from sex and energy intake, then assesses whether current intake meets it. Suitable for balanced diet planning.",
        "The DASH diet score tool assesses adherence to a blood pressure control diet across 8 indicators and gives a score, helping people with hypertension optimize sodium and potassium intake and the proportion of whole grains, vegetables and fruit.",
        "The Mediterranean diet adherence tool assesses how closely your diet pattern matches across 14 indicators (each 0 to 1 point, 14 points maximum), which suits behavioral self-assessment for chronic disease prevention and health management.",
        "The food additive intake safety tool uses ADI and actual intake to assess the safety margin of a single or compound additive and flags the risk of exceeding the limit. Suitable for food development and compliance self-checks.",
        "The Chinese residents balanced diet online self-assessment tool scores the reasonableness of your diet structure across 8 indicators (each 0 to 2 points) and gives improvement suggestions, running entirely in the browser.",
        "Common Food Calorie Lookup",
        "The Common Food Calorie Lookup is a free online nutrition and diet tool, and the Common Food Calorie Lookup is a free online nutrition and diet tool that returns results in real time as soon as you enter your parameters. It runs entirely in the browser, uploads no data, needs no registration and works the moment you open a browser. Running entirely in the browser, uploads no data, no...",
        "Select the high-sodium foods you ate today (pickled items, processed meat, sauces and so on) to estimate sodium and the equivalent amount of salt, then compare against the daily salt limit to help control salt intake. Used for dietary sodium management in people with hypertension or kidney disease.",
        "Tick the high-fiber foods you ate today (whole grains, vegetables, beans and so on) to estimate total dietary fiber, compare it with the recommended intake and get a verdict on whether it is sufficient. Used for gut health and diet management.",
        "About Nutrition and Diet Tools",
        "This collection gathers 18 free online tools covering the common calculation, conversion and lookup needs of nutrition and diet scenarios. Whether you are a practitioner, a student or an ordinary user, you will find a ready-to-use utility here. Every tool runs entirely in the browser and uploads no data to the server, so your privacy is protected.",
        "The nutrition and diet tools included on this page are (representative tools):",
        "These tools help you finish common nutrition and diet tasks quickly, with no formulas to memorize and no manual conversion needed. Enter and you get the result.",
        "Do the nutrition and diet tools require a download or registration?",
        "No. Every tool on this page runs entirely in the browser. Open the page and use it right away, with nothing to install, no account to create, and no data uploaded.",
        "Are the results of the nutrition and diet tools accurate? Is my data safe?",
        "Each tool computes locally in your browser from public mathematical formulas and general industry standards, so results are available instantly. All computation happens on your own device, nothing is uploaded to the server, and your privacy is fully protected.",
    ]))
    write('calorie-deficit', build('calorie-deficit', [
        "⚡ Calorie Deficit Calculator",
        "Enter your basic information to get TDEE and target ranges for fat loss or muscle gain.",
        "/ Calorie Deficit Calculator",
        "Basal metabolic rate follows the Mifflin-St Jeor formula: for men BMR = 10 × weight(kg) + 6.25 × height(cm) − 5 × age + 5; for women = 10 × weight + 6.25 × height − 5 × age − 161. Daily total expenditure TDEE = BMR × activity factor (bed rest 1.2, light 1.375, moderate 1.55, high 1.725, very high 1.9). The calorie deficit = TDEE − target intake, and a deficit of 7700 kcal roughly loses 1 kg of fat.",
        "Sedentary (rarely exercises)",
        "Light activity (1 to 3 times a week)",
        "Moderate (3 to 5 times a week)",
        "High intensity (6 to 7 times a week)",
        "Very high (intense training)",
        "Fat loss (mild)",
        "Fat loss (faster)",
        "BMR uses the Mifflin-St Jeor formula.",
        "TDEE is the basal metabolic rate × the activity factor.",
        "Not medical advice. When cutting fat, always leave enough room for baseline nutrition.",
        "📚 Deep Dive: Calorie Deficit Calculator (Target Range)",
        "Enter age, height, weight and activity level to get BMR and",
        "Choose fat loss, muscle gain or maintenance to get a recommended daily intake range",
        "Work backwards from the deficit to the weekly change, avoiding intake that is too low",
        "TDEE and the Target",
        "For a woman of 55 kg, 162 cm, age 30, light activity: BMR = 10×55+6.25×162−5×30−161 = 1222.5; TDEE = 1222.5×1.375 ≈ 1681 kcal; the recommended intake for fat loss is ≈ 1380 to 1480 kcal (a deficit of 200 to 300).",
        "Deficit Lower Bound",
        "Intake below BMR (1222) harms metabolism over the long term; as a rule, women should stay above 1200 and men above 1500 kcal per day.",
        "How Large Should the Deficit Be?",
        "A common deficit for fat loss is 300 to 500 kcal per day. Going larger causes hunger, muscle loss and difficulty sticking with it, while a smaller deficit is steadier.",
        "Why Can't Intake Fall Below BMR?",
        "BMR is the minimum energy needed to sustain basic life functions. Staying below it long term makes the body lower its metabolism and lose muscle, which works against healthy fat loss.",
        "How to Use the Calorie Deficit Calculator",
        "What Does the Calorie Deficit Calculator Do?",
        "This health tool estimates values from general physiological constants and empirical formulas, so the results are for reference only and do not replace professional medical diagnosis or advice. Tool name: Calorie Deficit Calculator.",
        "How Do I Use the Calorie Deficit Calculator?",
        "What Scenarios Suit the Calorie Deficit Calculator?",
    ]))
    write('self-assess-5', build('self-assess-5', [
        "📚 Dietary Guidelines (Chinese Balanced Diet) Self-Assessment",
        "Chinese residents balanced",
        "The balanced diet self-assessment total = grains and tubers + vegetables + fruit + meat, poultry, fish and eggs + dairy + soybeans and nuts + oil and salt control + water intake (8 items scored 0 to 2 each, 16 points maximum). The attainment rate = total score ÷ 16 × 100%. At least 80% means a balanced diet, 50% to 79% means basically balanced and below 50% means unbalanced. Compare low-scoring items against the Chinese Dietary Guidelines to adjust.",
        "Self-assessment of balanced eating against the Chinese Dietary Guidelines (8 items, 0 to 2 points each)",
        "1. Grains and tubers (250 to 400 g per day)",
        "Partially met (1 point)",
        "Not met (0 points)",
        "2. Vegetables (300 to 500 g per day)",
        "3. Fruit (200 to 350 g per day)",
        "4. Meat, poultry, fish and eggs (120 to 200 g per day)",
        "5. Dairy (300 g per day)",
        "6. Soybeans and nuts (25 to 35 g per day)",
        "7. Oil and salt control (oil 25 to 30 g, salt under 5 g)",
        "8. Water intake (1500 to 1700 ml per day)",
        "Self-assess Your Diet",
        "📚 Deep Dive: Balanced Diet (Chinese Residents) Self-Assessment",
        "Self-assess the reasonableness of your diet structure across 8 indicators, each 0 to 2 points",
        "Compute the total score out of 16 to see whether you are excellent, good or in need of improvement",
        "Get improvement suggestions for low-scoring items, such as adding whole grains or dairy",
        "Scoring Example",
        "The 8 items are scored 0 to 2: grains, tubers and beans, vegetables and fruit, dairy and soybeans, fish, poultry and eggs, low oil and salt, water, regular meals and low refined sugar. Scoring 2 on all 8 gives 16 points (excellent). Typical urban white-collar workers score 9 to 11, with vegetables, fruit and dairy low.",
        "Improvement",
        "A score below 10 usually means low vegetables and fruit (under 300 g per day), low dairy (under 300 g per day) and insufficient whole grains. Try adding one serving of vegetables or fruit, one glass of milk and one meal of mixed grains each day.",
        "What Do the 8 Items Cover?",
        "They cover the core of the dietary pagoda: varied staples, plenty of vegetables and fruit, dairy and soybeans, quality protein, controlled oil and salt, enough water, regular eating and limited added sugar.",
        "Can Self-Assessment Replace Nutrition Consulting?",
        "No. It is only a behavioral self-check and prompt. People with disease or special needs (pregnancy, diabetes, kidney disease) should combine it with clinical nutrition assessment.",
        "About Dietary Guidelines (Chinese Balanced Diet) Self-Assessment",
        "Dietary Guidelines (Chinese Balanced Diet) Self-Assessment. A free online tool, processed entirely in the browser, uploads no data and protects your privacy and security.",
    ]))

if __name__ == '__main__':
    main()
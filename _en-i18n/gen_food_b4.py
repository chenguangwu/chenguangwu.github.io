#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'food')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'food')
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
    out = {'slug': slug, 'industry': 'food', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # oil-absorption-estimator (48)
    write('oil-absorption-estimator', build('oil-absorption-estimator', [
"Fried Food Oil Absorption Estimator",
"Estimate fried food oil absorption and calorie increase from ingredient type, weight, time and oil temperature",
"Core formula (by input variables): 1 + max(0, (time - baseTime) / baseTime) x 0.2; (f.baseCal x weight / 100) + oilCal; 1 + (tempDiff / 50) x 0.3",
"View the Fried Food Oil Absorption Estimator Guide",
"Select ingredient type",
"Ingredient weight (g)",
"Frying time (min)",
"Common fried ingredient oil-absorption reference",
"Ingredient",
"Base absorption rate",
"Optimal oil temp",
"Suggested time",
"Calorie increase",
"Potato (fries)",
"3-5 min",
"Chicken (fried chicken)",
"8-15 min",
"Fish (fried fish)",
"5-8 min",
"Tofu",
"3-6 min",
"Batter type (tempura)",
"2-4 min",
"Spring roll / dumpling",
"4-8 min",
"Onion rings",
"Shrimp (tempura)",
"2-3 min",
"Fried food oil absorption is affected by ingredient type, water content, oil temperature, frying time and batter thickness. This tool gives estimates from built-in empirical data.",
"Higher oil temp, less absorption (surface sets fast)",
"Longer time, more absorption",
"Thicker batter, higher absorption rate",
"Higher water-content ingredients absorb more oil",
"Oil-reduction tips",
"How to reduce fried food oil absorption?",
"1) Keep oil temp in the optimal range 2) Drain on paper towel after frying 3) Do not add too many at once 4) Dry the surface before frying",
"In-Depth: Fried Food Oil Absorption Estimator",
"Fried food nutrition assessment",
"Oil-reduction health control",
"Process oil-absorption comparison",
"Oil amount ~ ingredient weight x absorption rate (empirical 5%-25%); calorie increase ~ oil amount x 9 kcal/g (oil ~9 kcal/g).",
"Potato 200 g, absorption 15% -> oil 30 g, calorie increase ~ 30 x 9 = 270 kcal.",
"How to reduce oil absorption?",
"High-temp quick fry sets the surface fast, moderate batter, drain after frying - all lower absorption.",
"What is a typical absorption rate?",
"By ingredient and process about 5%-25%; thick batter, long time, low temp run higher.",
"About the Fried Food Oil Absorption Estimator",
"Fried food oil absorption estimator is an online tool in daily life. A practical daily-life tool, close to life, convenient and handy.",
    ]))

    # recipe-generator (42)
    write('recipe-generator', build('recipe-generator', [
"Recipe Generator",
"Generate recipes by ingredients, cuisine and difficulty",
"View the Recipe Generator Guide",
"Main ingredients",
"Cuisine",
"Chinese",
"Sichuan",
"Cantonese",
"Western",
"Japanese",
"Korean",
"Easy (beginner)",
"Complex (chef)",
"1 serving",
"2 servings",
"3 servings",
"4 servings",
"6 servings (family)",
"Cooking method",
"Stir-fry",
"Steam",
"Boil / stew",
"Pan-fry / deep-fry",
"Bake",
"Cold dish / salad",
"Within 15 min",
"Within 30 min",
"Within 1 hour",
"Generate recipe",
"In-Depth: Recipe Generator",
"Solve 'what to eat today'",
"Scrap / existing ingredient use",
"Generate by cuisine and difficulty",
"Based on a built-in ingredient-recipe map, generate feasible recipes and steps on the front end by selected ingredients, cuisine and difficulty.",
"Input 'egg + tomato' -> generate 'tomato scrambled eggs': beat eggs with salt, cube tomato, fry eggs in hot oil and set aside, fry tomato to release juice then return and season.",
"What is the generation basis?",
"Uses a local built-in ingredient-recipe mapping rule; data not uploaded, instant front-end generation.",
"Can it replace a professional recipe?",
"Only for inspiration and step reference; heat and seasoning follow actual cooking experience.",
"About the Recipe Generator",
"Recipe generator is an online tool in the cooking field. A cooking tool to help master ingredient ratios and nutrition precisely.",
"e.g. chicken, tofu",
    ]))

    # report-cost-profit (27, item 10 is src_diff -> key = zh_src "其他费用（元）")
    write('report-cost-profit', build('report-cost-profit', [
"Restaurant Revenue / Cost / Profit Report",
"Measure gross profit, net profit and break-even revenue from sales, ingredient cost and expenses",
"A restaurant profit statement has two layers: the first is 'gross profit', deducting only the ingredient cost that moves with sales, reflecting dish pricing and output control; the second is 'period expenses' (labor, rent, utilities, other), which in the short term do not move with sales and are the store's fixed burden. Operating profit = gross profit - period expenses; net margin = operating profit / sales. Dividing period expenses by gross margin gives 'break-even revenue' - below it the store loses money, above it is the safety margin. All calculations run locally in the browser, data not uploaded.",
"View the Revenue / Cost / Profit Report Guide",
"Gross profit = sales - ingredient cost; gross margin = gross profit / sales x 100%; operating profit = gross profit - period expenses; break-even revenue = period expenses / gross margin",
"Sales (yuan)",
"Ingredient cost (yuan)",
"Labor cost (yuan)",
"Rent (yuan)",
"Utilities (yuan)",
"Other expenses (yuan)",
"In-Depth: Restaurant Revenue / Cost / Profit Report",
"Store monthly performance review",
"New-store break-even estimate",
"Cost-structure optimization and pricing",
"Gross profit = sales - ingredient cost;",
"= gross profit / sales; operating profit = gross profit - period expenses (labor + rent + utilities + other);",
"Break-even",
"Revenue = period expenses / gross margin.",
"Sales 50000, ingredient 18000, labor 9000, rent 6000, utilities 2000, other 1500 -> gross profit 32000 (gross margin 64.00%), period expenses 18500, operating profit 13500 (27.00%); break-even revenue = 18500 / 64% = 28906.25 yuan, safety margin 21093.75 yuan (42.19%).",
"27.00%); break-even revenue = 18500 / 64% = 28906.25 yuan, safety margin 21093.75 yuan (42.19%).",
"Where do gross and net margin differ?",
"Gross margin only deducts variable costs like ingredients, reflecting pricing and output control; net margin further deducts period expenses like labor, rent and utilities, reflecting the store's final profit.",
"What restaurant net margin is healthy?",
"Normally 8%-15%; fast food and delivery may be slightly higher due to lower rent share, while dine-in and mall stores run lower under rent and labor pressure; judge by category and location.",
"About the Finance (Revenue / Cost / Profit) Report",
"Finance (revenue / cost / profit) report. A cooking tool to help master ingredient ratios and nutrition precisely.",
    ]))

    # soup-ratio-optimizer (37)
    write('soup-ratio-optimizer', build('soup-ratio-optimizer', [
"Soup Ratio Optimizer",
"Optimize salty-umami-sour balance of soup; recommend salt, MSG and vinegar amounts by soup volume and taste preference",
"View the Soup Ratio Optimizer Guide",
"Select target taste",
"Light",
"Moderate",
"Rich",
"Soup volume (ml)",
"Taste preference fine-tune",
"Saltiness preference",
"Umami preference",
"Sourness preference",
"Ratio rule reference",
"Taste",
"Salt (% of soup weight)",
"MSG (% of soup weight)",
"Vinegar (% of soup weight)",
"Original flavor",
"Home-style",
"Appetizing",
"This tool recommends the salt, MSG and vinegar ratio by soup volume and target taste. The ratio is based on traditional cooking experience and can be fine-tuned to personal taste.",
"Ratio principles",
"Salt: 0.8%-1.2% of soup weight",
"MSG: 0.1%-0.3% of soup weight",
"Vinegar: 1%-3% of soup weight",
"In-Depth: Soup Ratio Optimizer",
"Home soup seasoning",
"Foodservice standardized recipe",
"Salty-umami-sour balance",
"Salt ~ soup weight x 0.8%-1.2%; MSG ~ soup weight x 0.1%-0.3%; vinegar ~ soup weight x 1%-3%.",
"Soup 2 kg (2000 g) -> salt = 2000 x 1% = 20 g; MSG = 2000 x 0.2% = 4 g; vinegar = 2000 x 2% = 40 g.",
"What is the salt ratio range?",
"Normally 0.8%-1.2%; heavy taste can go higher; hypertension patients should keep lower and follow medical advice.",
"How to fine-tune?",
"Add in small amounts and taste repeatedly to avoid overuse; sourness can be balanced at the end.",
"About the Soup Ratio Optimizer",
"Soup ratio optimizer is an online tool in daily life. A practical daily-life tool, close to life, convenient and handy.",
    ]))

    # stats-ingredient (19)
    write('stats-ingredient', build('stats-ingredient', [
"Dietary Fiber Intake Statistics (Built-in Ingredient Library)",
"Accumulate dietary fiber by ingredient and amount, compared to the daily recommendation",
"View the Dietary Fiber Intake Statistics Guide",
"Per-item fiber = amount(g) / 100 x fiber per 100g; total fiber = sum of items. Adult daily recommended dietary fiber is 25-30 g; results are compared against this. Built-in common ingredient fiber per 100g (e.g. oats 10, apple 2.4, broccoli 2.6, black bean 8.7).",
"Enter each line 'ingredient name, amount(g)', e.g.: Oats,50",
"Oats,50\nApple,150\nBroccoli,100",
"In-Depth: Dietary Fiber Intake Statistics",
"Daily dietary fiber tracking",
"Balanced diet management",
"Constipation / sugar-control diet reference",
"Total fiber = sum(ingredient weight/100 x fiber per 100 g); compare to adult recommendation 25-30 g/day.",
"Oats 50 g (10 g/100 g) -> 5 g + apple 150 g (2.4) -> 3.6 g + broccoli 100 g (2.6) -> 2.6 g = 11.2 g, about 37%-45% of recommendation.",
"What is the recommended intake?",
"Adult daily dietary fiber recommended 25-30 g; pregnant women / elderly may adjust by condition.",
"High-fiber ingredients?",
"Whole grains, legumes, tubers and vegetables/fruits (especially with skin) are higher.",
"About the Dietary Fiber Intake Statistics (Built-in Ingredient Library)",
"Dietary fiber intake statistics (built-in ingredient library). A cooking tool to help master ingredient ratios and nutrition precisely.",
"e.g.: Oats,50 Apple,150 Broccoli,100",
    ]))

if __name__ == "__main__":
    main()

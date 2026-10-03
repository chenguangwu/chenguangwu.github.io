#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'baking')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'baking')
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
    out = {'slug': slug, 'industry': 'baking', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('baker-percentage', build('baker-percentage', [
        "🔄 Baker's Percentage Converter",
        "Using flour weight as 100%, convert each ingredient to its actual amount by ratio; supports recipe scaling.",
        "Performs professional calculation from the input parameters and outputs the result, based on 'flour weight as 100%, convert each ingredient by ratio, supports recipe scaling'.",
        "📖 View 'Baker's Percentage Converter User Guide'",
        "Ingredient",
        "Baker's percentage (%)",
        "Actual weight (g)",
        "⚖️ Scale Recipe",
        "Enter the target total dough weight; the tool back-calculates the flour amount and scales all ingredients automatically.",
        "Target total dough weight (g)",
        "📖 Common Bread Formula Reference",
        "Basic white bread",
        ": flour 100% / water 65% / salt 2% / yeast 1.5%",
        "Toast bread",
        ": flour 100% / water 70% / sugar 8% / salt 1.5% / yeast 1.2% / butter 10%",
        ": flour 100% / water 70% / salt 2% / yeast 0.8%",
        "Ciabatta",
        ": flour 100% / water 80% / salt 2% / yeast 0.5%",
        "Bagel",
        ": flour 100% / water 55% / salt 2% / sugar 3% / yeast 1.5%",
        "Sweet bread",
        ": flour 100% / water 60% / sugar 15% / salt 1% / yeast 1.5% / butter 12%",
        "💡 In baker's percentage, flour is always 100%; each other ingredient's percentage = ingredient weight / flour weight × 100%. This makes it easy to scale recipes by ratio.",
        "📚 In-Depth: Baker's Percentage Conversion",
        "Given the target total dough weight and each ingredient's",
        "percentage, back-calculate each ingredient's amount.",
        "Scale a recipe up to a production batch as a whole while keeping the baker's percentage unchanged.",
        "Quickly find the gram weight of water, salt, yeast, etc. from the existing flour amount.",
        "Back-calculate ingredients from total weight",
        "Target total dough 1000g, formula: flour 100%, water 70%, salt 2%, yeast 1%. Flour = 1000 / (1 + 0.70 + 0.02 + 0.01) = 1000 / 1.73 ≈ 578g; water ≈ 405g, salt ≈ 12g, yeast ≈ 6g.",
        "Why does the sum of baker's percentages often exceed 100%?",
        "Because flour is the 100% baseline, and other ingredients such as water, egg and milk are all expressed relative to flour, water alone often reaches 60%-80%, so the total usually far exceeds 100%. This is a baking-industry convention, not an error.",
        "How to back-calculate flour amount from total dough weight?",
        "Flour weight = total weight / (1 + sum of all other ingredient percentages). For example, water 70%, salt 2%, yeast 1%, the denominator is 1.73; multiply by each percentage to get each ingredient's gram weight.",
        "About 'Baker's Percentage Converter'",
        "The baker's percentage converter uses flour as the 100% baseline to convert each ingredient to its actual amount, supports custom ingredients and recipe scaling.",
        "Flour 100% baseline, ingredients converted by ratio",
        "Supports adding custom ingredients",
        "One-click scaling by target dough weight",
        "Built-in common bread formula reference",
        "Bread recipe scaling and adjustment",
        "Baking ingredient amount calculation",
        "Making dough of different sizes",
        "Learning baker's percentage principles",
        "Ingredient name (e.g. honey)",
        "Percentage",
    ]))
    write('convert-28', build('convert-28', [
        "🍳 Ingredient Conversion by Baker's Percentage (flour = 100%)",
        "Baker's percentage: ingredient weight = flour weight × percentage% / 100 (flour = 100%)",
        "Baker's percentage uses flour weight as the 100% baseline: an ingredient's percentage = that ingredient's weight / flour weight × 100%. Enter the flour amount to get the amounts of water, sugar, yeast, etc., convenient for recipe scaling and ratio checking.",
        "Ingredient percentage (%)",
        "📚 In-Depth: Baker's Percentage Conversion",
        "Given the flour weight and an ingredient's",
        "percentage, find that ingredient's actual gram weight.",
        "Rewrite any recipe to use flour as 100%",
        "baker's percentage",
        ", making it easy to compare and scale across recipes.",
        "Back-calculate the water addition from the target hydration to control bread softness.",
        "Find water from flour weight and water %",
        "Flour 500g, formula water 65% (baker's percentage). Water added = 500 × 65% = 325g. Total weight counting only water = 500 + 325 = 825g; if yeast 1% and salt 2% are also included, multiply those percentages by the flour weight and add them.",
        "Why use flour as 100% in baker's percentage?",
        "Flour is the structural body of bread and used in the largest amount; using it as the baseline keeps the recipe ratio stable and easy to scale and replicate. Other ingredients are all expressed relative to flour weight and are unaffected by total-weight changes.",
        "What are the common percentage ranges for yeast and salt?",
        "Instant yeast is generally 1%-2% (fresh yeast about 2%-3%), salt about 1.8%-2.2%. Too little salt ferments too fast, too much inhibits yeast; strictly control per the recipe.",
        "About 'Ingredient Conversion by Baker's Percentage (flour = 100%)'",
        "Ingredient conversion by baker's percentage (flour = 100%). Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
    ]))
    write('convert-temp', build('convert-temp', [
        "🌡️ Oven Temperature (Celsius/Fahrenheit) Converter and Convection Compensation",
        "Celsius / Fahrenheit",
        "Temperature conversion uses standard formulas: Celsius = (Fahrenheit − 32) × 5 / 9, Fahrenheit = Celsius × 9 / 5 + 32. A convection oven (forced air) needs a 10-20°C reduction or 10-15% shorter time versus a conventional oven (traditional top/bottom heat); the result area shows the compensated value.",
        "Celsius oven temperature conversion",
        "Fahrenheit oven temperature conversion",
        "Convection temperature compensation",
        "Celsius convection compensation",
        "Fahrenheit convection compensation",
        "📚 In-Depth: Oven Temperature Conversion and Convection Compensation",
        "Two-way conversion between Celsius and Fahrenheit, matching Chinese and foreign recipes.",
        "Apply temperature compensation when switching from a conventional oven (traditional top/bottom heat) to a convection oven (forced air).",
        "At high altitudes the boiling point drops, requiring fine-tuning of baking temperature.",
        "Convert 180°C to Fahrenheit and apply convection compensation",
        "°F = 180 × 9 / 5 + 32 = 392°F. For the same setting using a convection oven, reduce by 10-20°C (use 160-170°C) or shorten time by 10-15%, to avoid the hot air accelerating browning and causing a burnt outside with an undercooked inside.",
        "Why is a convection oven set lower than a conventional oven?",
        "A convection oven uses a fan for forced convection, with higher heat-exchange efficiency; at the same setting it heats faster and browns more aggressively. Reducing by 10-20°C or time by 10-15% yields results comparable to a conventional oven.",
        "How to adjust temperature at high altitude?",
        "As altitude rises, water's boiling point drops and evaporation speeds up, so cakes easily collapse or dry out. Generally lower the temperature slightly, extend time slightly and reduce leavening, but specifics depend on the recipe and local measurement.",
        "About 'Oven Temperature (Celsius/Fahrenheit) Converter and Convection Compensation'",
        "Oven temperature (Celsius/Fahrenheit) conversion and convection compensation. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
    ]))

if __name__ == '__main__':
    main()

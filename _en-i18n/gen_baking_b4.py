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
    write('oven-temp', build('oven-temp', [
        "🌡️ Oven Temperature Converter",
        "Two-way Celsius/Fahrenheit conversion, and calculation of the convection oven (forced-air) compensation temperature",
        "Temperature conversion uses standard formulas: Celsius = (Fahrenheit − 32) × 5 / 9, Fahrenheit = Celsius × 9 / 5 + 32. A convection (forced-air) oven accelerates heat transfer via hot air, so it is usually 10-20°C lower than a conventional oven or 10-15% shorter in time; the result area gives compensation advice.",
        "Use convection oven (forced-air mode)",
        "🌡️ Common Oven Temperature Quick-Pick",
        "📖 Temperature and Baking Guide",
        ": slow cooking, warming, drying ingredients",
        ": low-temperature slow roasting, cookies, dried fruit",
        ": cakes, muffins, pound cake",
        ": bread, pizza, cookies (most common)",
        ": European bread, roasted meat, puff pastry",
        ": baguette, European bread steam baking",
        ": high-temperature quick browning, pizza stone",
        "💡 A convection oven (forced-air) is recommended to be about 20°C lower than the regular temperature, because the hot-air circulation makes heating more even and faster.",
        "📚 In-Depth: Oven Temperature Conversion",
        "American recipes give Fahrenheit (e.g. 350°F), which needs to be converted to the Celsius scale of a home oven.",
        "Apply temperature compensation when switching between a conventional oven (traditional top/bottom heat) and a convection oven (forced air), to prevent over-baking or under-baking.",
        "Different brands of ovens have large actual temperature differences; calibrate using the conversion result together with an oven thermometer.",
        "Convert 350°F to Celsius with convection compensation",
        "Fahrenheit to Celsius: °C = (°F − 32) × 5 / 9 = (350 − 32) × 5 / 9 ≈ 176.7°C, round to 177°C. If using a convection oven, usually lower by 10-20°C, i.e. 157-167°C, or shorten time by about 10-15%.",
        "Why do convection (forced-air) ovens generally need a temperature reduction?",
        "Forced hot-air circulation significantly speeds up heat transfer; at the same temperature it heats faster and browns more aggressively than a conventional oven. Lowering by 10-20°C (or reducing time by 10-15%) avoids a burnt surface with an undercooked inside.",
        "What are the Celsius and Fahrenheit conversion formulas?",
        "°C = (°F − 32) × 5 / 9; °F = °C × 9 / 5 + 32. Common baking settings: 180°C ≈ 356°F, 200°C ≈ 392°F, 350°F ≈ 177°C.",
        "About 'Oven Temperature Converter'",
        "The oven temperature converter supports two-way Celsius/Fahrenheit conversion and calculates the convection oven (forced-air) compensation temperature.",
        "Real-time two-way Celsius/Fahrenheit conversion",
        "Convection oven temperature compensation calculation",
        "One-click common oven temperature quick-pick",
        "Temperature and baking-type reference guide",
        "Overseas recipe temperature conversion",
        "Convection oven temperature adjustment",
        "Choosing a suitable baking temperature",
        "Learning oven temperature knowledge",
    ]))
    write('recipe-scaler', build('recipe-scaler', [
        "/ Recipe Scaler",
        "📖 View 'Recipe Scaler User Guide'",
        "🖼️ Recipe Scaler",
        "When changing a recipe from 2 servings to 6, or from small batch to large batch, all ingredients scale by the same ratio. Enter the original amounts and the factor to convert in bulk, avoiding manual errors.",
        "Recipe scaling uses ratio conversion: each ingredient's new amount = original amount × (target servings / original servings), all ingredients scale synchronously to keep the ratio. Calculation is done locally in the browser, no data uploaded.",
        "Ingredients (one per line: name=amount, unit after the number)",
        "flour=200g\nsugar=100g\neggs=2\nmilk=150ml\nbutter=50g",
        "Scaling factor",
        "Scaling only changes the usage ratio, not the process (baking temperature and time may need fine-tuning by mold size, not simple linear).",
        "Integer ingredients (e.g. 2 eggs) may become 3 by ratio; in practice round or adjust the total recipe amount.",
        "Baking is sensitive to ratios; for large scaling keep the key ratios (flour : liquid : yeast).",
        "📋 Example",
        "Original",
        "3 pcs",
        "📚 In-Depth: Recipe Scaler",
        "Scale a 2-serving home recipe up to an 8-serving party amount, enlarging all ingredients by the same factor, avoiding manual ratio errors.",
        "After a small-batch trial to confirm taste, scale up to a production batch while keeping ingredient ratios and texture unchanged.",
        "When existing ingredient stock is limited, back-calculate each ingredient's required amount from the target number of servings.",
        "Ratio scaling from 4 to 10 pieces",
        "Original recipe makes 4: butter 100g, cake flour 200g, sugar 80g. Target 10, scaling factor = 10 / 4 = 2.5. So butter 250g, flour 500g, sugar 200g; the ratio is exactly the same and the size and taste of the product are unchanged.",
        "Should baking time change after scaling?",
        "When volume clearly increases, the center heats slower, so usually extend baking time or slightly lower temperature to avoid a burnt outside with an undercooked inside; if the change is small (±20%), you can basically keep the original time and watch the browning.",
        "Can I scale only some ingredients?",
        "No. Recipe scaling must multiply all ingredients by the same factor; otherwise the ratio of flour, liquid and leavening becomes unbalanced and changes the product's structure and taste. Only when separately adjusting sweetness or flavor is a small change to the proportion of sugar or spices allowed.",
    ]))

if __name__ == '__main__':
    main()

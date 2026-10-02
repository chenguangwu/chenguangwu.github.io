#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'food-processing')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'food-processing')
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
    out = {'slug': slug, 'industry': 'food-processing', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
#!/usr/bin/env python3

def main():
    write('fermentation-brix', build('fermentation-brix', [
        "\U0001F3CB\uFE0F Fermenter Brix and Alcohol Conversion Calculator",
        "Derive sugar consumption, alcohol production and alcohol by volume (ABV) from the change in Brix before and after fermentation",
        "Fermenter Brix and Alcohol Conversion Calculator",
        " / Fermentation Brix Alcohol Conversion",
        "\U0001F4D6 See the \"Fermentation Brix and Alcohol Conversion User Guide\"",
        "Alcohol produced = sugar consumed \u00D7 0.511 \u00D7 fermentation efficiency",
        "Fermentation volume (L)",
        "Initial Brix (\u00B0P)",
        "Final Brix (\u00B0P)",
        "Theoretical sugar to alcohol conversion (g/g)",
        "The Gay-Lussac theoretical value 0.511 (glucose to ethanol plus CO\u2082)",
        "Actual fermentation efficiency (%)",
        "Actual alcohol as a share of the theoretical value, typically 88-95% for brewing yeast",
        "The Brix difference \u0394Brix reflects the fermentable sugar consumed. Sugar consumed \u2248 \u0394Brix \u00D7 10 \u00D7 volume(L) in grams (assuming density about 1kg/L). Alcohol produced = sugar consumed \u00D7 0.511 \u00D7 efficiency. ABV = alcohol mass \u00F7 0.789 \u00F7 volume \u00D7 100%. Note that alcohol affects Brix, so a low final Brix makes this an approximation.",
        "\U0001F4DA In-depth analysis: Fermentation Brix and Alcohol Conversion",
        "Monitoring progress in fruit and rice wine fermentation",
        "Estimating expected alcohol from the sugar charge",
        "Benchmarking actual yield against theory",
        "Sugar consumed = volume \u00D7(initial Brix \u2212 final Brix)/100; alcohol produced = sugar consumed \u00D70.511 \u00D7efficiency (the Gay-Lussac coefficient is 0.511).",
        "For 100 L of fermenting must at an initial 20\u00B0Bx and a final 6\u00B0Bx: 14 kg of sugar is consumed and at 92% efficiency the alcohol is 14\u00D70.511\u00D70.92\u22486.58% by volume, close to the actual alcohol of the finished wine.",
        "Where does 0.511 come from?",
        "C\u2086H\u2081\u2082O\u2086\u21922C\u2082H\u2085OH+2CO\u2082: 180 g of sugar theoretically yields 92 g of ethanol, that is about 0.511 g of ethanol per g of sugar.",
        "Why is the actual yield below theory?",
        "Yeast respiration, side metabolism and residual sugar consumption; actual yield is typically 88%-95% and lower at high Brix.",
        "About \"Fermenter Brix and Alcohol Conversion Calculator\"",
        "Fermenter Brix and alcohol conversion calculator. A food and cooking tool that helps you master ingredient ratios and nutrition precisely.",
    ]))

    write('filling-volume', build('filling-volume', [
        "\U0001F9CA Filling Volume Calibrator",
        "Convert between the inner diameter of a cylindrical bottle and the fill height to get the filling volume, or work backwards from a target volume to the fill level",
        "Core formulas (by input): \u03C0 \u00D7 r \u00D7 r; area \u00F7 10; h \u00D7 10",
        " / Filling Volume Calibration",
        "\U0001F4D6 See the \"Filling Volume (Cylindrical Bottle) Calibration User Guide\"",
        "Cylinder volume V = \u03C0 \u00D7 r\u00B2 \u00D7 h. 1 mL = 1 cm\u00B3. The actual fill volume follows from the inner diameter and level; the nominal volume and negative tolerance can be checked against the metrology requirements for prepackages. Note that a real bottle shape includes the neck and base sections that are not straight, so the result applies only to the straight-walled section.",
        "\U0001F4DA In-depth analysis: Filling Volume (Cylindrical Bottle) Calibration",
        "Calibrating fill levels on the filling line",
        "Working backwards from a target volume to a fill height",
        "Net content compliance checks",
        "Cylinder volume V = \u03C0\u00B7(inner diameter/2)\u00B2\u00B7fill height; working backwards, h = V \u00F7 [\u03C0\u00B7(inner diameter/2)\u00B2].",
        "With an inner diameter of 62 mm and a fill height of 120 mm: V=\u03C0\u00D731\u00B2\u00D7120\u2248362.3 mL; a target fill of 330 mL needs a level of about 109.3 mm (before bottle shape correction).",
        "Why is the actual fill above nominal?",
        "Net content must meet the average quantity requirement of the metrology supervision measures for prepackaged goods, so a positive deviation is usually left while the spread is controlled.",
        "What about irregular bottle shapes?",
        "For non-cylindrical bottles integrate the real cross-sectional area or use a calibration curve; this tool only applies to the straight-walled section.",
        "About \"Filling Volume Calibrator\"",
        "The Filling Volume Calibrator is an online tool in the field of food and cooking. A food and cooking tool that helps you master ingredient ratios and nutrition precisely.",
    ]))

    write('recipe-cost-calculator', build('recipe-cost-calculator', [
        "\U0001F4B0 Recipe Cost Calculator",
        "Account for the total and unit cost of a recipe from the unit price, quantity and loss rate of each ingredient, with entries you can add and remove dynamically",
        "Core formulas (by input): price \u00D7 actual \u00F7 1000",
        " / Recipe Cost Accounting",
        "\U0001F4D6 See the \"Recipe Cost Accounting User Guide\"",
        "Unit price (CNY/kg)",
        "Account for the cost",
        "Theoretical finished yield (g, used to work out unit cost)",
        "Actual amount used = recipe quantity \u00F7 (1 \u2212 loss rate), and the cost of one ingredient = unit price \u00D7 actual amount used (kg). The loss rate is the share lost in processing (peeling, shrinkage and so on). Unit cost = total cost \u00F7 finished yield.",
        "\U0001F4DA In-depth analysis: Recipe Cost Accounting",
        "Cost control in baking recipes",
        "Restaurant",
        "Dish pricing",
        "Accounting",
        "Effect of loss on unit cost",
        "Actual amount used = quantity \u00F7(1 \u2212 loss rate/100); cost of one item = unit price \u00D7 actual amount used \u00F71000 (CNY); unit cost = total cost \u00F7 yield \u00D71000 (CNY/kg).",
        "Flour 500 g at \u00A56/kg + sugar 200 g at \u00A58/kg + butter 300 g at \u00A540/kg (5% loss so 315.8 g actually used): total cost=3.0+1.6+12.63\u2248\u00A517.23, so at a 1000 g yield the unit cost is about \u00A517.23/kg.",
        "How do I enter the loss rate?",
        "It means the unrecoverable loss in processing (peeling, evaporation, sticking), so enter the measured value; 0 means costing by the recipe quantity alone.",
        "Why is the unit cost higher than total cost divided by yield?",
        "Because loss makes the actual amount used greater than the recipe quantity, which inflates the unit cost and puts it closer to the real cost.",
        "About \"Recipe Cost Calculator\"",
        "The Recipe Cost Calculator is an online tool in the field of food and cooking. A food and cooking tool that helps you master ingredient ratios and nutrition precisely.",
    ]))


if __name__ == '__main__':
    main()

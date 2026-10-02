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
    write('freeze-thaw-loss', build('freeze-thaw-loss', [
        "\U0001F9EE Freeze-Thaw Drip Loss Calculator",
        "Basic drip loss rate; repeated freeze-thaw cycles accumulate by cycle (see the result table).",
        " / Freeze-Thaw Drip Loss",
        "\U0001F4D6 See the \"Freeze-Thaw Drip Loss User Guide\"",
        "Thaw drip loss rate (%) = (weight before freezing \u2212 weight after thawing) \u00F7 weight before freezing \u00D7 100%",
        "Calculate the thaw drip loss rate and assess how repeated freeze-thaw cycles accumulate in water-holding capacity",
        "Weight before freezing (g)",
        "Weight after thawing (g)",
        "Number of freeze-thaw cycles",
        "First-cycle drip loss baseline (%)",
        "Typical drip loss per cycle under the same process (used to extrapolate multi-cycle accumulation)",
        "Drip loss increment per cycle",
        "Each cycle damages the cell structure further, so the drip loss grows by this factor (typically 0.1-0.2)",
        "Thaw drip loss rate = (weight before freezing \u2212 weight after thawing) \u00F7 weight before freezing \u00D7 100%. Freeze-thaw cycles break down cell structure, so water-holding capacity falls and the drip loss accumulates with each cycle. Slow freezing forms large ice crystals and does more damage, while quick freezing reduces the loss.",
        "\U0001F4DA In-depth analysis: Freeze-Thaw Drip Loss",
        "Controlling drip loss in quick-frozen foods",
        "Assessing water-holding capacity over repeated cycles",
        "Loss accounting for the thawing process",
        "Actual drip loss = (weight before freezing \u2212 weight after thawing) \u00F7 weight before freezing \u00D7 100%; across cycles this accumulates as each round's base rate \u00D7(1 + increment rate)^(i\u22121).",
        "500 g before freezing and 475 g after thawing: actual drip loss =(500\u2212475)/500\u00D7100%=5.0%, so 25 g of juice is lost; with a base of 5% and a 15% increment, the second-cycle drip loss is about 5.75%.",
        "How do I reduce thaw drip loss?",
        "Use quick freezing to keep ice crystals small, reduce frozen storage temperature swings, temper in the packaging before thawing, and avoid repeated freezing and thawing.",
        "Is a higher drip loss always worse?",
        "Drip loss carries away soluble solids and flavour, so excessive loss hurts texture and yield; set the threshold according to the product.",
        "About \"Freeze-Thaw Drip Loss Calculator\"",
        "The Freeze-Thaw Drip Loss Calculator is an online tool in the field of food and cooking. A food and cooking tool that helps you master ingredient ratios and nutrition precisely.",
    ]))

    write('emulsion-stability', build('emulsion-stability', [
        "\U0001F4DD Emulsion Stability (Centrifugal Separation) Tester",
        "Compute the emulsion stability index ESI and the degree of creaming or breaking from the layer heights after centrifugation",
        "Emulsion Stability Tester",
        " / Emulsion Stability Test",
        "\U0001F4D6 See the \"Emulsion Stability (Centrifugal Separation) Assessment User Guide\"",
        "ESI = emulsion layer height \u00F7 total height \u00D7 100%",
        "Total sample column height (mm)",
        "Emulsion layer height after centrifugation (mm)",
        "Height of the emulsion layer that is still uniformly milky after centrifugation",
        "Height of the clear liquid layer (mm)",
        "Height of the clear liquid (water layer) separated at the bottom or top",
        "Emulsion stability index ESI = emulsion layer height \u00F7 total height \u00D7 100%. Creaming index (CI) = clear layer \u00F7 total height \u00D7 100%. The higher the ESI the more stable. Accelerated separation by centrifugation is a common quick assessment (for example 3000r/min for 15 min). Note: emulsion layer plus clear layer should be close to the total height, otherwise recheck the measurement.",
        "\U0001F4DA In-depth analysis: Emulsion Stability (Centrifugal Separation) Assessment",
        "Formula screening for salad dressings and dairy drinks",
        "Verifying homogenisation stability",
        "Optimising emulsifier dosage",
        "Emulsion stability index ESI = emulsion layer height \u00F7 total height \u00D7 100%; the more clear liquid separates after centrifugation the less stable the emulsion is.",
        "With a total tube height of 50 mm, an emulsion layer of 42 mm and 8 mm of separated liquid: ESI=42/50\u00D7100%=84.0%, a fairly stable emulsion; below ESI<50% you need more emulsifier or a higher homogenisation pressure.",
        "How should the centrifugation conditions be set?",
        "Commonly 3000-10000 rpm for 5-30 min; conditions must be fixed so batches can be compared, and the higher the speed the harsher the test.",
        "How high does the ESI need to be?",
        "There is no single line, so set it per product; dairy drinks often require ESI above 80%, while sauces may be a little lower, and shelf-life testing is the final word.",
        "About \"Emulsion Stability Tester\"",
        "The Emulsion Stability (centrifugal separation) tester. A food and cooking tool that helps you master ingredient ratios and nutrition precisely.",
    ]))

    write('oil-absorption-rate', build('oil-absorption-rate', [
        "\U0001F373 Frying Oil Absorption Rate Predictor",
        "Predict the oil uptake of fried food from the initial moisture and the amount of water evaporated (water displacement model)",
        " / Frying Oil Absorption Prediction",
        "\U0001F4D6 See the \"Frying Oil Absorption Prediction User Guide\"",
        "Oil uptake rate = oil absorbed \u00F7 weight before frying \u00D7 100%",
        "Weight before frying (g)",
        "Initial moisture content (%)",
        "Weight after frying (g)",
        "Moisture content after frying (%)",
        "Water displacement coefficient k",
        "Evaporated water is partly replaced by oil, so a larger k means more uptake (typically 0.5-0.8, higher for deep frying)",
        "Water displacement model: during frying water evaporates and opens pores, which oil then fills. Oil absorbed \u2248 k \u00D7 water evaporated. Oil uptake rate = oil absorbed \u00F7 weight before frying \u00D7 100%. Lowering the initial moisture, shortening the frying time and lowering the oil temperature all reduce uptake.",
        "\U0001F4DA In-depth analysis: Frying Oil Absorption Prediction",
        "Controlling oil uptake in fries and chicken pieces",
        "Applying water displacement patterns in the frying process",
        "Low-oil recipe development",
        "Water evaporated = water before frying \u2212 water after frying (converted via the moisture content); predicted oil uptake = k \u00D7 water evaporated (k being the displacement coefficient); uptake rate = oil absorbed \u00F7 weight before frying \u00D7 100%.",
        "100 g before frying (70% moisture) and 55 g after (40% moisture): 48 g of water evaporated, and taking k=0.65 the predicted oil uptake is 31.2 g, an uptake rate of 31.2% and about 56.7% oil in the finished product, which is high, so lower the starting moisture or shorten the fry.",
        "Why does oil replace water?",
        "During frying heated water escapes and creates capillary negative pressure that draws oil into the pores, so oil uptake is about k\u00D7water loss; lowering the initial moisture or shortening the time reduces the oil.",
        "How is the k coefficient chosen?",
        "It varies with product and process (0.3-0.8) and should be calibrated against measurement; batter coating or pre-drying lowers the effective k.",
        "About \"Frying Oil Absorption Rate Predictor\"",
        "The Frying Oil Absorption Rate Predictor is an online tool in the field of food and cooking. A food and cooking tool that helps you master ingredient ratios and nutrition precisely.",
    ]))


if __name__ == '__main__':
    main()

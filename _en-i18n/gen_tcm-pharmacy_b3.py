#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'tcm-pharmacy')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'tcm-pharmacy')
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
    out = {'slug': slug, 'industry': 'tcm-pharmacy', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
DISCL_M = " A professional medical tool based on authoritative medical standards, for reference only."

def main():
    write('herb-processing', build('herb-processing', [
        "\U0001F33F Chinese Herb Piece (Processing Specification) Identifier",
        "Looks up the identification features, processing purpose and efficacy differences of Chinese herb pieces in different processed forms",
        "/ Chinese herb piece processing identifier",
        "Search herbs (name / processing method)",
        "Stir-frying",
        "Roasting with adjuvant",
        "Calcination",
        "Steaming",
        "Wine processing",
        "Vinegar processing",
        "Honey roasting",
        "Total",
        "records",
        "\U0001F4D6 Classification of processing methods",
        "Tiaozhi (preparation)",
        "Cleaning and cutting. Includes picking, washing, soaking, moistening and slicing; these are the basic steps of processing.",
        "Water processing / fire processing",
        "Water processing:",
        "Floating, soaking, soaking in water and levigation by water.",
        "Fire processing:",
        "Stir-frying, roasting, calcining, simmering and baking.",
        "Combined water and fire processing",
        "Steaming, boiling, blanching and stewing. Such as Rehmannia preparata (steamed), scutellaria (boiled) and bitter apricot kernel (blanched).",
        "Carbonizing",
        "Stir-charred or calcined charcoal, such as diyutan charcoal, cattail pollen charcoal and hair charcoal, mainly used to stop bleeding.",
        "Other methods",
        "Fermentation (medicinal leaven), sprouting (malt sprout), frost preparation (croton frost) and purification (mirabilite).",
        "\U0001F4DA In-depth analysis: Chinese herb piece (processing specification) identification",
        "Pharmacy acceptance",
        "Dispensing review",
        "Herb piece specifications",
        "Raw / prepared / roasted / stir-fried",
        "The same herb has different actions in different processed forms: rehmannia - sheng dihuang (clears heat and cools blood) and shu dihuang (nourishes yin and tonifies blood); rhubarb - raw rhubarb (strong purgative), wine-processed rhubarb (moves blood) and prepared rhubarb (gentle purgative); fresh ginger, dried ginger and charred ginger increase in warmth.",
        "Categories of roasting with adjuvant",
        "Honey roasting (licorice, ephedra, aster) strengthens moistening of the lungs; vinegar roasting (corydalis, cyperus) enters the liver and relieves pain; salt roasting (eucommia, fennel) enters the kidneys; ginger roasting (magnolia, bamboo shavings) warms the middle; wine roasting (angelica, white peony) moves blood and ascends.",
        "Can raw and prepared rhubarb substitute for each other?",
        "No. Raw rhubarb contains anthraquinone glycosides with strong purgative action, while in prepared rhubarb about 70% of bound anthraquinones are hydrolyzed so the purgative action is gentler and heat-clearing anti-inflammatory action is stronger; mixing them easily leads to constipation or diarrhea deviation.",
        "What are the regular patterns in how processing changes herb property?",
        "Common patterns: wine processing lifts and guides the herb upward and enhances blood moving (wine-processed rhubarb, wine-processed scutellaria); vinegar processing enters the liver, enhances analgesia and reduces toxicity (vinegar-processed corydalis, vinegar-processed genkwa); ginger processing harmonizes the stomach and stops vomiting (ginger-processed pinellia, ginger-processed magnolia); salt processing enters the kidneys and enhances yin-nourishing heat-clearing (salt-processed phellodendron, salt-processed anemarrhena); honey processing moistens the lungs, stops cough and moderates the property (honey-processed ephedra, honey-processed licorice); charring stops bleeding (diyutan charcoal, schizonepeta charcoal). Identification mainly looks at changes in color, odor and texture.",
        "About the Chinese Herb Piece (Processing Specification) Identifier",
        "Chinese Herb Piece (Processing Specification) Identifier." + DISCL_M,
        "e.g. rhubarb, wine processing, honey roasting...",
    ]))
    write('herb-properties', build('herb-properties', [
        "\U0001F4C4 Single Herb (Property, Flavor, Channel Tropism) Query",
        "Looks up the property, flavor, channel tropism, actions, indications and dosage of common Chinese herbs, with built-in data on more than 120 common herbs",
        "/ Single herb property, flavor and channel tropism query",
        "Search herbs (supports pinyin / name)",
        "Cold",
        "Hot",
        "Warm",
        "Cool",
        "Neutral",
        "Total",
        "herbs",
        "Four qi (cold, hot, warm, cool)",
        "Cold and cool herbs belong to yin, clearing heat and draining fire and cooling blood and detoxifying; warm and hot herbs belong to yang, warming the interior and dispelling cold and tonifying fire and assisting yang; neutral herbs show little cold or hot bias.",
        "Five flavors (sour, bitter, sweet, pungent, salty)",
        "Sour astringes, bitter drains, sweet tonifies, pungent disperses and salty softens. Different flavors correspond to different directions of action.",
        "Channel tropism",
        "Refers to the selective action of a drug on a certain part of the body, that is the zang organs and channels its action reaches. Channel tropism helps select herbs precisely.",
        "Warning: the data in this tool is for study reference only; follow medical advice in clinical use. Doses are routine amounts and need adjustment for special constitutions.",
        "\U0001F4DA In-depth analysis: single herb (property, flavor, channel tropism) quick lookup",
        "Clinical prescribing",
        "Teaching lookup",
        "Materia medica revision",
        "Astragalus",
        "Warm in nature, sweet in flavor, enters the spleen and lung channels; actions: tonifies qi and raises yang, strengthens the defensive qi and secures the exterior, drains water and reduces swelling, and expels toxin and promotes tissue growth; indications: spleen qi deficiency, sinking of middle qi, exterior deficiency spontaneous sweating, qi deficiency edema and sores that are hard to break; contains astragaloside IV at 0.04% or above (Chinese Pharmacopoeia 2020).",
        "Coptis",
        "Cold in nature, bitter in flavor, enters the heart, spleen, stomach, liver, gallbladder and large intestine channels; actions: clears heat and dries dampness, drains fire and detoxifies; indications: damp-heat focal distension, vomiting and acid regurgitation, high fever with clouded mind, red eyes and toothache; contains berberine hydrochloride at 5.5% or above (pharmacopoeia); it is drying and easily damages body fluids, so use it cautiously in yin deficiency.",
        "How is channel tropism related to actions?",
        "Channel tropism refers to the site of action and corresponds to the actions; a herb of the same flavor may enter several channels (such as coptis entering the heart, spleen, stomach, liver and gallbladder), so herb selection in practice also considers how many channels it covers.",
        "Does channel tropism always show up in the actions?",
        "They are mostly related but not absolute: channel tropism is a positional summary of the actions, such as apricot kernel entering the lung and large intestine channels, corresponding to relieving cough and wheezing and moistening the intestines. But some herbs have broad channel tropism (such as licorice entering all twelve channels), and later records of channel tropism differ. Practically, select herbs \"with actions first and channel tropism second\": first define the actions and indications needed, then use channel tropism to judge the targeted site, rather than choosing by channel tropism first.",
        "About the Single Herb (Property, Flavor, Channel Tropism) Query",
        "Single Herb (Property, Flavor, Channel Tropism) Query." + DISCL_M,
        "e.g. astragalus, ginseng, angelica...",
    ]))
    write('herb-quality', build('herb-quality', [
        "\u2696\ufe0f Chinese Herb Quality (Appearance Character) Evaluator",
        "Evaluates the quality grade of Chinese herb pieces through appearance indicators, with built-in standards for common herbs",
        "/ Chinese herb quality evaluator",
        "Quality standard",
        "Scored evaluation",
        "Determine the quality grade",
        "\U0001F4D6 Identification essentials",
        "Look (shape, color)",
        "Observe the shape, size, surface features and color of the herb. For example coptis has golden yellow fracture surfaces, codonopsis shows a chrysanthemum-core pattern, and gastrodia has vertical wrinkles and nodes on the surface.",
        "Touch (texture)",
        "Feel the texture of the herb. For example firm (minerals), soft (cistanche), brittle (dried ginger), powdery (chinese yam) and horny (gastrodia).",
        "Smell (odor)",
        "Smell the odor of the herb. For example musk has a characteristic aroma, angelica is strongly fragrant, asafoetida smells of garlic, and animal materials smell fishy.",
        "Taste (flavor)",
        "Taste the herb. For example coptis is extremely bitter, licorice is sweet, smoked plum is sour and dried ginger is pungent. Note that toxic herbs must not be tasted.",
        "Water test / fire test",
        "Water test:",
        "Safflower turns water golden yellow and bear bile rotates in water like a thread.",
        "Fire test:",
        "Lygodium spores crackle when heated and musk swells and bubbles when burned.",
        "\U0001F4DA In-depth analysis: Chinese herb quality (appearance character) evaluation",
        "Herb piece acceptance",
        "Warehouse inspection",
        "Grading and pricing",
        "Astragalus overall score",
        "Appearance 40x0.3 + color 30x0.25 + fracture 25x0.25 + odor 15x0.2 = 12 + 7.5 + 6.25 + 3 = 28.75 (80 or above excellent, 60-80 good, 40-60 fair, below 40 poor); when the total 31 giving below 40 as poor disagrees with the weighted 287/1000, use the total 28.75; recheck is recommended.",
        "5-item weighted scoring",
        "c.weight weights total 100%; typical appearance 25-35, color 20-30, fracture 15-25, odor 10-20, texture 10-20; total = sum(s_i x w_i / 100) comes from qualityDB itself.",
        "Why use weights instead of a simple total?",
        "The dimensions differ in importance (appearance and color matter more than odor), and weighting avoids the bias where one poor item masks overall excellence or one good item hides several poor ones, which is closer to how experienced pharmacists score.",
        "Can moldy herbs still be used?",
        "No. Mold not only lowers active components, it is more likely to produce harmful substances such as aflatoxin, and when mold spots are visible to the naked eye the mycelium has usually already penetrated deep inside; washing, drying or soaking in wine cannot remove the toxins. Likewise, severely insect-damaged herbs (powdery fracture, insect droppings), oil-spotted herbs (oily or sugary herbs turning soft and sticky with a rancid smell) and discolored herbs with a sour rancid odor should all be judged non-conforming and no longer used medicinally.",
        "About the Chinese Herb Quality (Appearance Character) Evaluator",
        "Chinese Herb Quality (Appearance Character) Evaluator." + DISCL_M,
    ]))


if __name__ == '__main__':
    main()
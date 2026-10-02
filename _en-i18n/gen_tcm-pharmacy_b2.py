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
    write('formula-song', build('formula-song', [
        "\U0001F33F Formula Song (Seven-Syllable Quatrain) Generator",
        "Includes classic formula songs and can generate a simple seven-syllable formula song from entered herbs",
        "/ Formula song generator",
        "Classic formula songs",
        "Auto-generate",
        "Search classic formula songs",
        "Enter the formula name, herbs and actions to automatically generate a seven-syllable formula song",
        "Formula name",
        "Herbs (comma separated, 4-8 is recommended)",
        "Actions (brief description)",
        "Generate the formula song",
        "Copy the formula song",
        "Change example",
        "\U0001F4D6 The value of formula songs",
        "Aids memorization",
        "A formula song condenses the name, composition, actions and indications into four lines in seven-syllable rhyming verse, easy to recite and memorize.",
        "Formula song structure",
        "The first two lines usually carry the herb and formula names, the third states the actions or indications, and the fourth adds usage or compatibility points.",
        "Classic formula song examples",
        "Si Jun Zi Tang:",
        "With ginseng, atractylodes, poria and licorice it is the Four Gentlemen decoction, the one that tonifies qi and strengthens the spleen; with poor appetite, loose stools and fatigue take it and the spleen qi deficiency resolves.",
        "Ma Huang Tang:",
        "In Ma Huang Tang the cinnamon twig is used, with apricot kernel and licorice as the other three; it induces sweating, releases the exterior and opens the lungs, the classic choice for wind-cold exterior excess without sweating.",
        "\U0001F4DA In-depth analysis: formula song (seven-syllable quatrain) template generator",
        "Formula teaching",
        "Clinical recitation",
        "Exam revision",
        "Si Jun Zi Tang",
        "Ren / Zhu / Ling / Cao in equal parts, with the name carrying ginseng and the group of atractylodes and poria; the sweet and warm licorice harmonizes the middle, boosts qi and strengthens the spleen, the base formula for spleen and stomach qi deficiency.",
        "Ma Huang Tang",
        "Ma / Gui / Xing / Gan in three liang, with the name carrying Ma Huang and the cassia twig; apricot kernel and licorice release the exterior, open the lungs and relieve wheezing, the main formula for wind-cold exterior excess.",
        "Is the character count fixed?",
        "Seven-syllable lines of four lines are used: the first line carries the formula name, the second lists the three main herbs, the third states the actions and the fourth gives clinical modifications; if it does not fit you can manually shorten or extend it.",
        "Can the auto-generated song be recited directly?",
        "It can serve as a memorization skeleton, but check three elements before memorizing: whether the herb composition is complete, whether the chief herb is named, and whether the indications match the textbook. The value of a formula song lies in its rhythm and compression, and an auto-generated version may swap herb order or use aliases just to make it rhyme, which can create memory errors. The safer approach is to treat the generated result as a draft and collate it against the original song (such as Tang Tou Ge Jue) before finalizing.",
        "About the Formula Song (Seven-Syllable Quatrain) Generator",
        "Formula Song (Seven-Syllable Quatrain) Generator." + DISCL_M,
        "How to use the Formula Song (Seven-Syllable Quatrain) Generator",
        "What does the Formula Song (Seven-Syllable Quatrain) Generator do?",
        "Includes classic formula songs of common formulas for reference, and generating a simple seven-syllable quatrain formula song from the entered formula name, herbs and actions helps you memorize formula composition and action, serving as a recitation aid for Chinese materia medica and formula study.",
        "How do I use the Formula Song (Seven-Syllable Quatrain) Generator?",
        "Which scenarios suit the Formula Song (Seven-Syllable Quatrain) Generator?",
        "e.g. Ma Huang Tang, Si Wu Tang...",
        "e.g. Qi Bu Yang Xue Tang",
        "e.g. astragalus, angelica, atractylodes, poria, licorice",
        "e.g. tonify qi and nourish blood",
    ]))
    write('four-qi-nature', build('four-qi-nature', [
        "\U0001F4DA Medicinal Property (Cold Hot Warm Cool) Four Qi Classifier",
        "Determines the four qi attribute (cold, hot, warm, cool or neutral) from the actions and indications of a herb, assisting formula composition and herb selection",
        "/ Four qi classifier",
        "Look up by herb",
        "Judge by symptom",
        "Enter the herb name",
        "Select the patient's symptom features and the system recommends the herb property according to the principle of treating cold with heat and heat with cold",
        "Fever / high fever",
        "Fear of cold / cold intolerance",
        "Thirst with a preference for cold drinks",
        "No thirst / preference for hot drinks",
        "Flushed face and red eyes",
        "Pale complexion",
        "Constipation / dry stool",
        "Loose stool / diarrhea",
        "Scanty dark urine",
        "Clear copious urine",
        "Red tongue with yellow coating",
        "Pale tongue with white coating",
        "Rapid forceful pulse",
        "Slow weak pulse",
        "Determine the property",
        "\U0001F321\ufe0f Four qi property overview",
        "Cold nature (yin)",
        "Clears heat and drains fire, cools blood and detoxifies, nourishes yin and clears deficiency heat. Suitable for heat and yang patterns.",
        "Representative herbs:",
        "Coptis, scutellaria, phellodendron, gypsum, anemarrhena, gardenia, honeysuckle, forsythia, isatis root and indigowoad leaf",
        "Cool nature (yin, weaker than cold)",
        "Clears heat less strongly than cold herbs, suitable for mild heat patterns or patients weak enough that they cannot tolerate cold herbs.",
        "Mint, pueraria, bezoar, chrysanthemum, cassia seed, rehmannia, moutan bark and lycium bark",
        "Hot nature (yang)",
        "Warms the interior and dispels cold, restores yang and rescues collapse, tonifies fire and assists yang. Suitable for cold and yin patterns.",
        "Aconite, dried ginger, cinnamon, evodia, galangal, prickly ash and black pepper",
        "Warm nature (yang, weaker than hot)",
        "Its warming dispersing action is milder than hot herbs, suitable for mild cold patterns or general deficiency-cold patterns.",
        "Ephedra, cassia twig, schizonepeta, saposhnikovia, ginger, angelica, astragalus, ginseng, atractylodes and jujube",
        "Neutral nature",
        "Little cold or hot bias, mild in action and broadly applicable, often used as an adjunct or harmonizing ingredient.",
        "Ginseng (slightly warm), codonopsis, chinese yam, poria, licorice, goji, gastrodia and dragon bone",
        "\U0001F4DA In-depth analysis: four qi herb property (cold, hot, warm, cool) classification",
        "Syndrome-based prescribing",
        "Cold and heat differentiation",
        "Materia medica teaching",
        "Cold pattern chooses warm and hot",
        "Chief complaint of cold limbs, pale tongue with white coating and a deep slow pulse indicates a cold pattern; the property score gives weight 0 to cold/cool and 100 to warm/hot, recommending warm herbs (aconite, dried ginger, cinnamon, cassia twig, ephedra).",
        "Heat pattern, 5 points cold",
        "Chief complaint of fever and thirst, red tongue with yellow coating and a rapid pulse indicates a heat pattern; symptom analysis gives cold 30 + cool 25 + warm 5 + hot 0 = 55, so recommendQi = cold, recommending cold herbs such as coptis, scutellaria, gardenia, gentian and gypsum.",
        "When are neutral herbs used?",
        "Neutral herbs are neither cold nor hot, suitable for patterns with no clear cold or heat or for long-term conditioning (such as licorice, chinese yam, goji); in a formula they often serve as adjuvant or harmonizing herbs.",
        "How do you choose with mixed cold and heat?",
        "Use the compatibility of combining cold and heat, pungent opening and bitter descending: Ban Xia Xie Xin Tang pairs the cold of coptis and scutellaria with the warmth of dried ginger and pinellia to treat focal distension from cold and heat binding. The principle is to clarify the primary and secondary of cold and heat and the location (upper heat with lower cold, stomach heat with intestinal cold), then combine in proportion, rather than simply picking a single herb of intermediate temperature. Single neutral herbs (such as licorice or poria) can moderate, but they cannot replace a cold-and-heat combined structure.",
        "About the Medicinal Property (Cold Hot Warm Cool) Four Qi Classifier",
        "Medicinal Property (Cold Hot Warm Cool) Four Qi Classifier." + DISCL_M,
        "e.g. coptis, dried ginger, ginseng",
    ]))
    write('granule-equivalent', build('granule-equivalent', [
        "\U0001F33F Formula Granule (Equivalence) Converter",
        "Converts a Chinese herb piece prescription into formula granule doses, supporting single-herb and whole-formula conversion",
        "/ Formula granule converter",
        "Single-herb conversion",
        "Whole-formula conversion",
        "Herb piece dose (g)",
        "Convert",
        "Enter a herb piece prescription to batch-convert into formula granule doses",
        "Enter the prescription (herb name:grams, one herb per line or comma separated)",
        "Batch convert",
        "Download the prescription",
        "\U0001F4D6 Formula granule conversion notes",
        "Conversion principle",
        "Formula granules are made into granules by extracting, concentrating and drying herb pieces. Conversion must use the",
        "equivalence ratio",
        "of each herb (how many grams of herb piece 1 g of formula granule equals).",
        "Conversion formula",
        "Formula granule dose = herb piece dose / equivalence ratio",
        "Example: astragalus piece 30 g with an equivalence ratio of 5 (1 g of granule equals 5 g of herb piece) gives a granule dose of 30 / 5 = 6 g",
        "Factors affecting the equivalence ratio",
        "The equivalence ratio differs by herb and mainly depends on herb nature (low for flowers and leaves, high for roots and rhizomes), extraction process and extract yield. The usual range is 1:1 to 1:10.",
        "Precautions",
        "Formula granules and traditional decoctions may differ in efficacy, so acute and severe cases should use decoctions. Formula granules are convenient and quick, suitable for chronic disease conditioning and travel.",
        "Warning: the equivalence ratio may differ between manufacturers; follow the manufacturer's instructions in practice. The data in this tool are general reference values.",
        "\U0001F4DA In-depth analysis: formula granule (equivalent dose) conversion",
        "Herb piece to granule conversion",
        "Clinical dispensing",
        "Hospital pharmacy department",
        "Astragalus piece 10 g to granule",
        "Astragalus piece 10 g with an equivalence ratio of 1:5 (granuleDB[\"astragalus\"].ratio = 5) gives granuleDose = 10/5 = 2 g; at 1 g per sachet that is 2 sachets.",
        "Compound granules",
        "Astragalus 10 g, codonopsis 10 g, atractylodes 10 g, licorice 3 g with equivalence ratios 1:5, 1:4, 1:5, 1:4 give a total granule amount of 2 + 2.5 + 2 + 0.75 = 7.25 g; at 1 g per sachet that is about 8 sachets, and the total prepared dose equals the original herb pieces.",
        "Is the equivalence reliable?",
        "Ratios differ between manufacturers (1:4 to 1:8 is common); use granules from a single manufacturer and lock the equivalence ratio by batch number; granules converted from decocted and filtered multi-herb liquid are closer to the bioavailability of a decoction than those from a single-herb extract.",
        "How do you convert back to herb pieces?",
        "It is commonly labelled \"each sachet equals X g of herb piece\", so divide the prescribed herb piece amount by that value to get the number of sachets. The equivalence ratio for the same herb may differ between manufacturers (affected by extraction process and extract yield), so recheck when switching manufacturers. Note that special decoction methods such as pre-boiling, adding late, dissolving and taking dissolved are simplified in granules, so for formulas containing volatile components (such as mint or amomum) or herbs needing pre-boiling to reduce toxicity (such as aconite), the equivalence between granules and the original decoction is still disputed.",
        "About the Formula Granule (Equivalence) Converter",
        "Formula Granule (Equivalence) Converter." + DISCL_M,
        "e.g. astragalus:30, angelica:10, atractylodes:15, saposhnikovia:6",
    ]))


if __name__ == '__main__':
    main()
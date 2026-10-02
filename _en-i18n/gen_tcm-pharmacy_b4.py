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
    write('herb-storage', build('herb-storage', [
        "\U0001F33F Chinese Herb Storage (Temperature/Humidity) Condition Lookup",
        "Looks up storage conditions, temperature and humidity requirements, shelf life and maintenance methods for Chinese herb pieces",
        "/ Chinese herb storage condition lookup",
        "Roots and rhizomes",
        "Fruits",
        "Flowers and leaves",
        "Animal materials",
        "Minerals",
        "Total",
        "records",
        "\U0001F321\ufe0f General standards for the storage environment",
        "Cool store",
        "Ambient store",
        "Cold store",
        "\U0001F4D6 Chinese herb storage maintenance methods",
        "Drying maintenance",
        "Reduce the moisture content of herbs by sun drying, air drying or oven drying. Moisture content is generally controlled at: roots and rhizomes 11-13%, fruits 8-10%, flowers and leaves 7-9%.",
        "Cold storage maintenance",
        "Store valuable or insect-prone herbs in a cold store (2-8 C) to prevent insects and mold; suitable for ginseng, American ginseng, deer antler and bird's nest.",
        "Sealed storage maintenance",
        "Place dried herbs in sealed containers, isolating them from moisture and microorganisms in the air. Can be used together with desiccants (silica gel).",
        "Mutual protection storage",
        "Use the special odors of two herbs to protect each other from insects. For example moutan bark with alisma to prevent insects; prickly ash with animal materials to prevent insects; camphor with Chinese herbs to repel insects.",
        "Common deterioration phenomena",
        "Insect damage:",
        "Likely at 25-35 C and humidity above 70%, common in herbs rich in starch and protein",
        "Mold:",
        "Likely at humidity above 75% and 25-35 C, common in herbs rich in sugar and mucilage",
        "Oil spotting:",
        "Herbs containing volatile oils or fatty oils oxidize at high temperature, such as apricot kernel, peach kernel and angelica",
        "Discoloration:",
        "Flowers and leaves fade under light and high temperature, such as safflower and chrysanthemum",
        "Loss of odor:",
        "Aromatic herbs lose volatile oils at high temperature, such as mint and patchouli",
        "\U0001F4DA In-depth analysis: Chinese herb storage (temperature / humidity / light protection) conditions",
        "Pharmacy management",
        "Herb piece maintenance",
        "Pharmacy GSP",
        "Insect-prone herb pieces",
        "Codonopsis, angelica, astragalus and chinese yam are high in sugar and easily insect-damaged, so store in a cool store (20 C or below, RH 45-75%); sealing plus lime desiccant plus regular fumigation is recommended (use aluminum phosphide with care).",
        "Herbs containing volatile oils",
        "Mint, patchouli, cinnamon and clove are highly volatile, so store protected from light and cold (2-10 C) in small packages to avoid repeated opening; for every 1 C above the temperature limit the volatile loss increases by 0.5-1%.",
        "What if RH is too high?",
        "Add a lime or calcium chloride desiccant cabinet, sealing and air conditioning dehumidification; herbs containing fat-soluble components mold or turn rancid when RH exceeds 80%; inspect every 3-7 days.",
        "How should they be stored at home?",
        "The key is sealing, keeping cool and dry, and protecting from light: pack into glass or food-grade plastic containers with a sealing gasket, put in food-grade desiccants and keep in a cool place (below 20 C); valuable insect-prone herbs (such as cordyceps or ginseng) can be sealed and refrigerated (4 C), and after taking them out let them return to room temperature before opening to avoid condensation. Herbs containing volatile oils (mint, patchouli, amomum) should be sealed separately and not stored together with odor-absorbing herbs; check once a year around the plum rain season for mold or insects.",
        "About the Chinese Herb Storage (Temperature/Humidity) Condition Lookup",
        "Chinese Herb Storage (Temperature/Humidity) Condition Lookup." + DISCL_M,
        "Enter the herb name, such as ginseng or goji...",
    ]))
    write('incompatibility-check', build('incompatibility-check', [
        "\U0001F48A Nineteen Fears and Eighteen Antagonisms (Compatibility Taboo) Checker",
        "Enter the herbs in a prescription and it automatically checks for the nineteen fears, eighteen antagonisms and pregnancy contraindications",
        "/ Nineteen Fears and Eighteen Antagonisms checker",
        "Enter herb names (separated by comma, space or Chinese comma)",
        "Check compatibility taboos",
        "\U0001F4DC Nineteen fears",
        "The nineteen fears refer to nine groups of mutually feared herb combinations that should not be used together",
        "\U0001F4DC Eighteen antagonisms",
        "The eighteen antagonisms refer to three groups of mutually antagonistic herb combinations that should not be used together",
        "\U0001F930 Pregnancy contraindicated herbs",
        "Herbs prohibited or to be used with caution in pregnancy",
        "Prohibited herbs (absolutely banned)",
        "Croton, blistering beetle, strychnine, aconite, fuzi, tianxiong, realgar, qingfen, arsenolite, mercury, musk, achyranthes, chuanxiong, sanleng, ezhu, leech, gadfly, centipede, scorpion, pangolin, senna, genkwa, kansui, Beijing daiji, shanglu, morning glory seed, musk, safflower, peach kernel, sappan, frankincense and myrrh",
        "Use with caution herbs (use with care depending on the case)",
        "Rhubarb, mirabilite, senna, aloe, Chinese dwarf cherry seed, immature bitter orange, mature bitter orange, areca, magnolia, fuzi, dried ginger, cinnamon, pinellia, arisaema, baifuzi, cogongrass root, coix, mallow seed, achyranthes, chuanxiong, moutan, red peony, safflower, peach kernel, sappan, vaccaria and artemisia",
        "\U0001F4DA In-depth analysis: nineteen fears / eighteen antagonisms (compatibility taboo) check",
        "Prescription review",
        "Clinical pharmacy",
        "Dispensing safety",
        "Eighteen antagonisms detection",
        "If the prescription contains \"licorice + zexie\" or \"ginseng + wulingzhi\" it is flagged red, since the eighteen antagonisms mnemonic reads \"bencao mingyan shiba fan, ban lou bei lian ji gong wu, zao ji sui yuan ju zhan cao, zhu shen xin shao pan lilu\"; these are compatibility taboos that should not be used together.",
        "Nineteen fears",
        "Sulfur fears mirabilite, mercury fears arsenic, wolf poison fears litharge, croton fears morning glory, clove fears turmeric, chuanwu/caowu fears rhino horn, yaoxiao fears sanleng, official cinnamon fears fluorite, ginseng fears wulingzhi; they must not be combined in one formula.",
        "What are the consequences of violating a taboo?",
        "Toxicity or side effects may be increased (for example combining pinellia with fuzi increases cardiac toxicity); clinically it should be avoided, decocted separately when necessary with 2 to 4 hours of spacing.",
        "Are antagonistic pairs also used in old formulas?",
        "They are, for example in the Jin Gui Yao Lue Gansui Banxia Tang where kansui is used together with licorice, a special use of \"opposing yet complementing\" intended to stimulate the drug action and expel retained fluid. This shows the eighteen antagonisms are not absolutely forbidden, but they are a high-risk \"no harm with cause\" usage: it must be done with clear syndrome differentiation, dose control and physician supervision, and modern toxicology research still disputes its safety. Routine prescriptions and self-compounding should strictly avoid it, and old formulas must not be cited as a basis for self-administration.",
        "About the Nineteen Fears and Eighteen Antagonisms (Compatibility Taboo) Checker",
        "Nineteen Fears and Eighteen Antagonisms (Compatibility Taboo) Checker." + DISCL_M,
        "e.g. ginseng, wulingzhi, licorice, lilu",
    ]))
    write('index', build('index', [
        "\U0001F33F Chinese Materia Medica Tools",
        "Chinese materia medica",
        "Chinese materia medica tools",
        "Based on the herb type and amount, computes the optimal alcohol strength, steeping time and daily dose for medicinal wine, suitable for tonic wine preparation.",
        "Enter the formula type and the taker's situation (such as age and constitution), computes the recommended amount and use of common drug guides such as ginger, jujube and salt, for standardized addition and dosage control of drug guides in TCM prescriptions.",
        "Enter the herbs in the prescription and, based on special decoction requirements such as pre-boiling, adding late and wrapping, automatically generates a schedule of decoction order, duration and water volume for each herb, used for standardized guidance in decoction workflow and pharmacy dispensing.",
        "Medicinal wine steeping concentration/time calculation",
        "Medicinal Wine Steeping Concentration / Time Calculator",
        "Includes classic formula songs of common formulas for reference, and generating a simple seven-syllable quatrain formula song from the entered formula name, herbs and actions helps you memorize formula composition and action, serving as a recitation aid for Chinese materia medica and formula study.",
        "Chinese Herb Dose (Adult / Child) Converter",
        "Enter the adult dose and the child's age or weight and convert to the pediatric dose by age-based conversion formulas (such as 1/8 to 1/6 of the adult dose for children under one year), used for safe pediatric TCM dosing and individualized administration.",
        "Enter the herb piece prescription dose and convert each herb piece to a formula granule dose by the equivalence conversion coefficient, supporting single-herb and whole-formula batch conversion, used for converting outpatient traditional herb piece prescriptions into formula granule prescriptions.",
        "Based on the required action and the number of diners, computes the best ratio of ingredients to herbs in medicinal meals, with built-in classic recipes, convenient for home conditioning.",
        "Compares the daily treatment cost (DDC) and total course cost of different Chinese patent medicines and Western medicines, supporting rational drug choice",
        "Medication Timing (Before/After Meal) Recommender",
        "\u23F0 Medication Timing (Before/After Meal) Recommender",
        "Analyzes the jun-chen-zuo-shi structure and dose ratio of a formula, supporting classic formula lookup and custom formula analysis",
        "Adverse Reaction (ADR) Causality Assessor",
        "Based on the Naranjo scale and the ministry ADR criteria, assesses the causal relationship between a drug and an adverse reaction",
        "Through the actions and indications of a herb, determines its four qi attribute (cold, hot, warm, cool or neutral), assisting formula composition and herb selection",
        "Chinese Herb Quality (Appearance Character) Evaluator",
        "Evaluates herb piece quality grade against built-in standards for common herbs using appearance indicators such as shape, size, surface features and color, such as fracture features and color quality, for herb piece acceptance and quality grading.",
        "Chinese Herb Storage (Temperature/Humidity) Condition Lookup",
        "Looks up the suitable storage temperature, relative humidity, shelf life and maintenance methods (such as sun drying and oven drying to control moisture) for each type of Chinese herb piece, giving references such as 11-13% moisture content for roots and rhizomes, for scientific storage and maintenance of herb pieces in pharmacy and warehouse.",
        "Five Flavors (Sour Bitter Sweet Pungent Salty) Zang-Fu Lookup",
        "Looks up which zang organ each of the five flavors sour, bitter, sweet, pungent and salty belongs to (such as sour entering the liver and bitter entering the heart) and its direction of action (rising, floating, sinking and descending), and lists representative herbs, for syndrome differentiation and formula compatibility referencing the five flavor theory.",
        "Chinese Patent Medicine (Functions and Indications) Quick Lookup",
        "Looks up common Chinese patent medicines, listing their functions and indications, composition, usage and dosage and precautions, supporting quick search by name or action, for clinical drug selection, pharmacist review and public understanding of patent medicine use.",
        "Chinese Herb Piece (Processing Specification) Identifier",
        "Looks up the identification features, processing purpose and efficacy differences of different processed forms of the same herb (such as raw, honey roasted and wine processed), for herb piece identification, understanding the role of processing and specification selection when prescribing.",
        "Queries the graded pregnancy contraindications of Chinese medicine (prohibited, to avoid and use with caution), listing contraindicated herbs and risks such as musk, leech and croton, used for pregnancy prescription review and pregnancy contraindication safety checks.",
        "Enter the herbs in the prescription and it automatically checks for the nineteen fears, eighteen antagonisms and pregnancy contraindications",
        "Looks up the property, flavor, channel tropism, actions, indications and usage of common Chinese herbs, with built-in data on more than 120 common herbs",
        "About the Chinese Materia Medica Tools",
        "This Chinese materia medica tool collection includes 21 free online tools covering the common calculation, conversion and lookup needs in Chinese materia medica. Whether you are a practitioner in the field, a student or an ordinary user, you can find ready-to-use practical tools here. All tools run entirely in the front end and no data is uploaded to the server, so privacy and security are protected.",
        "The Chinese materia medica tools included on this page are (some representative tools):",
        "These tools help you quickly finish common Chinese materia medica tasks without memorizing complex formulas or doing manual conversions, so you just enter the values and get the result.",
        "Do the Chinese materia medica tools need a download or registration?",
        "No. All Chinese materia medica tools on this page are pure front-end online tools; open the page and use them directly, with no software to install, no account to register and no data uploaded.",
        "Are the Chinese materia medica tool results accurate, and is the data secure?",
        "The tools compute locally in your browser using public mathematical formulas and common industry standards, so results are immediate. All computation happens locally on your device and no data is uploaded to the server, so privacy and security are assured.",
    ]))


if __name__ == '__main__':
    main()
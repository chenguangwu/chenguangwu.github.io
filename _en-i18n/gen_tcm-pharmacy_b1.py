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
    write('calc-time-concentration', build('calc-time-concentration', [
        "\U0001F9EE Medicinal Wine Steeping Concentration / Time Calculator",
        "Enter the herb category, herb weight, liquor volume and alcohol strength to estimate the crude drug concentration, extract concentration, suggested steeping time and dosing, and back-calculate the amount for a target concentration.",
        "Core formulas (from the input variables): dose*2",
        "Medicinal wine steeping concentration/time calculation",
        "/ Medicinal wine steeping concentration/time calculation",
        "Herb category",
        "Roots and rhizomes (such as ginseng, astragalus)",
        "Fruits and seeds (such as goji, schisandra)",
        "Whole herbs, flowers and leaves",
        "Animal materials (such as deer antler, gecko)",
        "Herb weight (g)",
        "White liquor volume (mL)",
        "White liquor alcohol strength (%)",
        "Target crude drug concentration (g/mL, may be blank)",
        "\U0001F4A1 Crude drug concentration = herb weight / liquor volume (g/mL); extract concentration = herb weight x extraction rate / volume; the suggested steeping time depends on the herb category; the usual dose is 15 to 30 mL each time, 1 to 2 times per day.",
        "\U0001F4CA Common medicinal wine steeping reference",
        "Medicinal wine contains ethanol, so take it as directed by a physician; it is contraindicated for pregnant women, children and liver disease patients",
        "The extraction rate is an empirical value (about 15% to 30%) and actually varies with the herb, the degree of comminution and the alcohol strength",
        "This tool is for formula design reference only and is not a medical basis; it runs entirely in the front end and uploads no data",
        "\U0001F4DA In-depth analysis: medicinal wine concentration / extract amount / single dose calculation",
        "Crude drug to wine ratio design",
        "Extract prediction",
        "Single-dose compliance",
        "Concentrated formula 0.1 g/mL",
        "herb 100 g + vol 1000 mL gives conc = 100/1000 = 0.1 g/mL and ratio 1:10; for a flower/leaf category with p.rate about 0.105 the extract = 10.5 g and extConc = 10.5 mg/mL; a concentration of 0.1 triggers dose = 15 mL per time.",
        "Reaching target 0.1",
        "The generated concentration 0.05 is below the target 0.1, so it fails; either increase the herb to 200 g or reduce the liquor to 500 mL, and a concentration of 0.2 triggers dose = 10 mL per time, which works out to 1.5 g of crude drug per dose.",
        "How does dose relate to concentration?",
        "dose = 20 mL (conc below 0.1), 15 mL (0.1 <= conc < 0.2), 10 mL (conc 0.2 or above); this keeps the crude drug in one dose under 1.5 to 2 g so a single intake never takes in too much active component.",
        "How is the daily amount set?",
        "A routine medicinal wine is 10-15 mL each time, 1-2 times per day, and you should start from the smallest amount and adjust after observing tolerance; therapeutic medicinal wines (containing toxic herbs) must have the dose set by a physician and must not be self-dosed at the usual tonic wine amount. Note that concentration here means the grams of crude drug per mL of liquor, which is different from the alcohol strength; it is contraindicated in abnormal liver function, pregnancy, children, and people taking cephalosporins or hypoglycemic drugs.",
        "About Medicinal Wine Steeping Concentration/Time Calculation",
        "Used for medicinal wine formula design and steeping process reference. Enter the herb category, weight, liquor volume and alcohol strength to estimate the crude drug concentration, extract concentration and final alcohol strength, and get a suggested steeping time and dose, and back-calculate the required amount for a target concentration.",
        "Steeping time by herb category",
        "Back-calculate the amount for a target concentration",
        "Includes a common medicinal wine reference table",
        "Medicinal wine formula concentration design",
        "Home steeping amount estimation",
        "TCM preparation process reference",
        "Dose conversion",
        "Herb weight",
        "White liquor volume",
        "White liquor alcohol strength",
        "Target crude drug concentration",
    ]))
    write('decoction-time', build('decoction-time', [
        "\u2728 Decoction (Pre-boil / Add Late) Schedule Generator",
        "Enter the prescription herbs to automatically generate a schedule of decoction order, times and water volume",
        "Enter the prescription herbs to automatically generate a schedule of decoction order, times and water volume.",
        "/ Decoction schedule generator",
        "Enter herb names (separated by comma, space or Chinese comma)",
        "Number of herbs in the prescription",
        "Average dose per herb (g)",
        "Number of decoctions",
        "Two decoctions (first plus second)",
        "Three decoctions",
        "One decoction",
        "Generate the decoction schedule",
        "Download the schedule",
        "\U0001F4D6 Special decoction method reference",
        "Pre-boil herbs (need 20-60 minutes of pre-boiling)",
        "Mineral and shell type:",
        "Gypsum, dragon bone, oyster shell, hematite, magnetite, abalone shell, mother-of-pearl, turtle shell, softshell turtle shell, pangolin scale",
        "Toxic type:",
        "Aconite (fuzi), chuanwu, caowu, pinellia and arisaema must be pre-boiled 30-60 minutes to reduce toxicity",
        "Heavy and slow-to-extract type:",
        "Water buffalo horn, antelope horn and polygonum cuspidatum",
        "Add-late herbs (added in the last 5-10 minutes of the first decoction)",
        "Aromatic type:",
        "Mint, patchouli, Eupatorium fortunei, amomum, cardamom, tsaoko, cinnamon and cassia twig",
        "Long-decoction loses activity type:",
        "Rhubarb (for purgation), uncaria, senna, artemisia and mosla",
        "Wrapped decoction herbs (decocted wrapped in gauze)",
        "Plantago seed, lepidium seed, cattail pollen, lygodium seed, inula, wulingzhi, red halloysite, talc powder and puffball",
        "Dissolved herbs (dissolved then mixed into the decoction)",
        "Ejiao, deer antler glue, turtle shell glue, softshell turtle shell glue, honey and maltose",
        "Taken dissolved (ground and taken with the decoction)",
        "Notoginseng powder, amber powder, pearl powder, dragon's blood powder, bezoar, musk, cinnabar and antelope horn powder",
        "\U0001F4DA In-depth analysis: decoction (pre-boil / add late / wrap) schedule generation",
        "Oral decoctions",
        "Special decoction methods",
        "Routine formulas",
        "5 herbs totaling 50 g",
        "count = 5, avgDose = 10, totalWeight = 50; the first decoction adds ceil(50x10) = 500 mL, the second ceil(50x8) = 400 mL and the third ceil(50x6) = 300 mL; the combined liquid is about ceil(500x0.3) = 150 mL, taken warm in 2 divided doses.",
        "Containing aconite",
        "5 herbs totaling 50 g, with 10 g of aconite listed for pre-boiling; pre-boil 30-60 minutes then add the rest (mint 6 g added in the last 5 minutes), giving about 90 minutes total, roughly double the routine 30-50 minutes, to reduce toxicity.",
        "Why are some herbs added late?",
        "Mint, patchouli and amomum contain volatile components that long decoction destroys, so their active constituents are lost; rhubarb added late keeps its purgative action and uncaria added late keeps its antihypertensive potency.",
        "How long should pre-boiling be?",
        "Minerals, shells, horns and shells (gypsum, oyster shell, turtle shell) are generally pre-boiled 20-30 minutes; toxic herbs (aconite, aconite root) need 30-60 minutes or even longer to reduce toxicity, following medical advice and using the absence of a numb spicy sensation on tasting as the endpoint. After pre-boiling the other herbs (except the add-late ones) go in for co-decoction rather than changing the water. Never shorten the pre-boiling time for aconite-type herbs on your own.",
        "About the Decoction (Pre-boil / Add Late) Schedule Generator",
        "Decoction (Pre-boil / Add Late) Schedule Generator." + DISCL_M,
        "e.g. gypsum, pre-boil, zhimu, mint, add late, licorice, japonica rice",
    ]))
    write('five-flavors', build('five-flavors', [
        "\U0001F4DA Five Flavors (Sour Bitter Sweet Pungent Salty) Zang-Fu Lookup",
        "Looks up the correspondence between the five flavors and the zang-fu organs, the direction of action and representative herbs, assisting with syndrome differentiation and herb selection",
        "/ Five flavor zang-fu lookup",
        "Sour flavor",
        "Bitter flavor",
        "Sweet flavor",
        "Pungent flavor",
        "Salty flavor",
        "Bland flavor",
        "Astringent flavor",
        "\U0001F4D6 Five flavor theory",
        "Where each flavor enters",
        "Sour enters the liver, bitter enters the heart, sweet enters the spleen, pungent enters the lung and salty enters the kidney. The flavor of a herb has a specific affinity with the organs.",
        "Where each flavor travels",
        "Sour travels to the tendons (excess causes difficulty urinating), bitter to the bones (excess causes vomiting), sweet to the flesh (excess causes bloating), pungent to the qi (excess causes a hollow feeling) and salty to the blood (excess causes thirst).",
        "Direction of action of the five flavors",
        "Pungent disperses:",
        "Disperses exterior conditions, moves qi and moves blood",
        "Sour astringes:",
        "Constrains and secures",
        "Sweet tonifies:",
        "Tonifies, harmonizes the middle and relieves urgency",
        "Bitter drains:",
        "Clears heat, dries dampness and directs rebellious qi downward",
        "Salty softens:",
        "Softens hardness and dissipates nodules, and causes purgation",
        "What each flavor injures",
        "Sour injures the tendons (too sour makes liver qi rise excessively), bitter injures qi (too bitter drains heart qi internally), sweet injures the flesh (too sweet makes spleen qi stagnate), pungent injures the skin and hair (too pungent disperses lung qi) and salty injures the blood (too salty makes kidney water overflow).",
        "What each flavor is contraindicated in",
        "Liver disease avoids pungent (pungent dispersion damages liver yin), heart disease avoids salty (salty softening damages heart blood), spleen disease avoids sour (sour constraining hinders spleen transport), lung disease avoids bitter (bitter draining damages lung qi) and kidney disease avoids sweet (sweet slowing hinders kidney qi).",
        "\U0001F4DA In-depth analysis: five flavors (sour bitter sweet pungent salty) and the zang organs",
        "Medicinal nature teaching",
        "Clinical formula composition",
        "Materia medica lookup",
        "Five flavors entering the organs",
        "Sour-liver-astringent (such as smoked plum or schisandra); bitter-heart-drying and draining (such as coptis or rhubarb); sweet-spleen-tonifying and harmonizing (such as licorice or codonopsis); pungent-lung-dispersing (such as ephedra or chuanxiong); salty-kidney-softening hardness (such as mirabilite or oyster shell).",
        "Combined flavors",
        "Sour and sweet transform into yin (smoked plum plus licorice gives fluid production and thirst relief); pungent and bitter open and descend (pinellia plus coptis, pungent opening and bitter draining, treats focal distension); sweet and warm clear great heat (astragalus plus codonopsis plus licorice tonifies the middle and boosts qi).",
        "Is channel tropism related to property and flavor?",
        "Property and flavor determine where the action takes effect; the five flavors entering the five organs is a basic rule, but the specific channel tropism still follows measured efficacy (for example platycodon is pungent and enters the lung while also carrying other herbs upward).",
        "How do the five flavors correspond to efficacy?",
        "Pungent disperses (it can move and disperse, like ephedra and mint releasing the exterior, moving qi and blood); sour astringes (it can constrict and secure, like schisandra and smoked plum constraining the lung and astringing the intestines); sweet moderates (it can tonify, harmonize and moderate, like licorice and jujube tonifying the middle and relieving urgency); bitter drains (it can drain, dry and harden, like rhubarb purging and coptis drying dampness and clearing heat); salty softens (it can descend and soften, like mirabilite purgating and oyster shell softening hardness and dissipating nodules); bland seeps (it can seep and drain, like poria and coix draining water and seeping dampness). Note that real herbs often carry several flavors, so the main flavor should define the dominant action.",
        "About the Five Flavors (Sour Bitter Sweet Pungent Salty) Zang-Fu Lookup",
        "Five Flavors (Sour Bitter Sweet Pungent Salty) Zang-Fu Lookup." + DISCL_M,
    ]))


if __name__ == '__main__':
    main()
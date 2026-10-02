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
    write('jun-chen-zuo-shi', build('jun-chen-zuo-shi', [
        "\U0001F48A Formula Jun-Chen-Zuo-Shi (Dose Ratio) Analyzer",
        "Analyzes the jun-chen-zuo-shi structure and dose ratio of a formula, supporting classic formula lookup and custom formula analysis",
        "/ Formula jun-chen-zuo-shi analyzer",
        "Classic formulas",
        "Custom formula",
        "Select a classic formula",
        "Analyze the formula structure",
        "Add herbs and assign jun-chen-zuo-shi roles to analyze the dose ratio",
        "+ Add herb",
        "\U0001F4DA Jun-chen-zuo-shi composition principles",
        "Jun herb (chief drug)",
        "The drug that plays the main therapeutic role for the primary disease or syndrome and is the core of the formula. Its dose is usually the largest or relatively large.",
        "Chen herb (deputy drug)",
        "Assists the jun herb to strengthen treatment of the primary disease or syndrome, or treats a secondary disease or syndrome. The dose is next to the jun herb.",
        "Zuo herbs",
        "Include zhuo assistants (assisting jun and chen), zuo correctives (removing or reducing toxic side effects) and counter-assistants (preventing the property from becoming too extreme). The doses are smaller.",
        "Shi herb (guide herb)",
        "Guides the drugs directly to the affected site, or harmonizes all the herbs in the formula. The dose is usually the smallest.",
        "Classic ratio reference",
        "The jun : chen : zuo : shi dose ratio is usually about",
        "or",
        ", and varies with the specific disease and syndrome.",
        "\U0001F4DA In-depth analysis: formula jun-chen-zuo-shi (dose ratio) analysis",
        "Classic formula interpretation",
        "Clinical prescribing",
        "Teaching deconstruction",
        "Xiao Jian Zhong Tang",
        "Jun maltose 30 g (41%), chen cassia twig 9 g + white peony 18 g (37% combined), zuo honey-fried licorice 6 g (8%), shi fresh ginger 9 g + 4 jujubes (13%); total dose 73 g, jun share 41% above 30% (a characteristic of classical tonifying formulas), chen-to-zuo ratio about 4.5:1, and zuo and shi clearly less than jun and chen to show that supporting the healthy qi is the dominant aim.",
        "Jun-chen-zuo-shi visualization",
        "presentRoles has 4 categories so unitDose = min(30, 9, 6, 9) = 6 (the zuo herb), and the actual ratio is jun : chen : zuo : shi = 30:18:6:9 = 5:3:1:1.5; the larger the gap between jun and chen versus zuo and shi, the clearer the formula's main attack direction.",
        "Is a higher jun share always better?",
        "Jun herb share is commonly 30-50%; above 60% it is mostly an emergency formula (such as Du Shen Tang); too few supporting herbs easily damage the healthy qi and too many weaken the main attack, so clinical judgment is needed.",
        "Can the chen herb exceed the jun herb?",
        "Yes, and many famous formulas do exactly that (in some formulas the chen herb is increased because it targets a secondary syndrome or an acute condition). The distinction between jun and chen is based on \"which one plays the leading therapeutic role in the formula\" and is not completely identical to having the largest dose. For example in Xiao Chai Hu Tang bupleurum is the jun herb, but scutellaria and pinellia may be used in amounts comparable to bupleurum. When analyzing, first clarify the direction of the main indication and then check whether the dose ratio serves that direction, rather than mechanically identifying the jun herb by dose ranking.",
        "About the Formula Jun-Chen-Zuo-Shi (Dose Ratio) Analyzer",
        "Formula Jun-Chen-Zuo-Shi (Dose Ratio) Analyzer." + DISCL_M,
    ]))
    write('medicated-diet', build('medicated-diet', [
        "\U0001F33F Medicated Meal (Ingredient + Herb) Ratio Calculator",
        "Computes the best ratio of ingredients to herbs in a medicated meal from the required action and the number of diners",
        "/ Medicated meal ratio calculator",
        "Warning: medicated meals are for wellness reference only; consult a professional TCM practitioner for constitution assessment. Medicated meals should not be eaten in large amounts or long term.",
        "Select a medicated meal recipe",
        "Constitution type",
        "Compute the recipe",
        "\U0001F4D6 Medicated meal recipe overview",
        "Built-in classic medicated meal recipes",
        "\U0001F4D0 Ratio principles",
        "Drug to food ratio",
        "The ratio of herbs to ingredients in a medicated meal is generally 1:5 to 1:10, with food as the main part and herbs as the adjunct. The number of herbs should not be excessive; 2 to 5 is ideal.",
        "Constitution adjustment",
        "Qi deficiency: increase the qi-tonifying herbs; yang deficiency: increase the yang-warming herbs; yin deficiency: increase the yin-nourishing herbs and reduce the warm and hot herbs; phlegm-dampness: increase the spleen-strengthening and dampness-draining herbs.",
        "Dose adjustment",
        "Standard recipes are based on 2 servings; add proportionally for each extra person. For children the amount is 1/3 to 1/2 of the adult amount.",
        "\U0001F4DA In-depth analysis: medicated meal (ingredient + herb) ratio",
        "Constitution conditioning",
        "Seasonal wellness",
        "Post-illness dietary therapy",
        "Danggui Shengjiang Yangrou Tang, 4 servings",
        "Base 2 servings; angelica 30 g, fresh ginger 45 g, mutton 500 g; adjusted to 4 servings gives servingFactor = 2; for yang deficiency constitution herbFactor = 1.1 and foodFactor = 0.9, so angelica 30 x 1.1 x 2 = 66 g, ginger 45 x 1.1 x 2 = 99 g, mutton 500 x 0.9 x 2 = 900 g.",
        "Ingredient to herb ratio",
        "Angelica 99 g / mutton 900 g gives 0.11; the drug to food ratio is kept within 1:9 to 1:19 (Chinese Medicinal Dietetics standard), and yang deficiency dietary therapy takes ingredients as the main part with herbs as the adjunct.",
        "What is herbFactor for a constitution?",
        "Balanced 1.0/1.0, qi deficiency 1.1/0.9, yang deficiency 1.1/0.9, yin deficiency 0.9/1.1, phlegm-dampness 0.9/1.1, damp-heat 0.8/1.2, blood stasis 1.2/0.8, qi stagnation 1.1/1.0, special constitution 0.8/1.0.",
        "Will long-term use cause an overdose?",
        "A medicated meal is positioned as dietary support, and the herb amount is usually below the therapeutic dose (about one third to one half of a decoction), with emphasis on intermittent use. If it is taken continuously for more than 2 weeks, reassess whether the constitution has changed, since constitution shifts with season, age and disease course, and sticking to one formula long term easily creates bias (such as long-term warm tonification turning heat-producing). Pause medicated meals during acute illness, fever, pregnancy and acute flares of chronic disease, and treat the illness first.",
        "About the Medicated Meal (Ingredient + Herb) Ratio Calculator",
        "Medicated Meal (Ingredient + Herb) Ratio Calculator." + DISCL_M,
    ]))
    write('medication-timing', build('medication-timing', [
        "\u2764\ufe0f Medication Timing (Before/After Meal) Recommender",
        "Recommends the best medication timing from the drug type and actions to optimize efficacy and reduce adverse reactions",
        "/ Medication timing recommender",
        "Select the drug type",
        "Purpose of taking the medicine",
        "Treating a disease",
        "Daily conditioning",
        "Gastrointestinal condition",
        "Gastrointestinal sensitivity",
        "Spleen and stomach deficiency",
        "Generate the recommendation",
        "\U0001F4CC Medication timing quick reference table",
        "Best timing for each drug type at a glance",
        "\U0001F4D6 Medication timing terminology",
        "Taken on an empty stomach",
        "Taken on an empty stomach before eating after getting up in the morning, giving fast and complete absorption. Suitable for anthelmintics and strong purgatives that expel water.",
        "Taken before meals",
        "Taken 30-60 minutes before meals. With an empty stomach the drug acts fully on the gastrointestinal tract and absorbs well. Suitable for tonics, stomachic drugs and antacids.",
        "Taken after meals",
        "Taken 15-30 minutes after meals. Food reduces the drug's irritation to the gastrointestinal tract. Suitable for strongly irritant drugs and digestives.",
        "Taken with meals",
        "Taken with the meal. Suitable for digestants that disperse food stagnation and for oily drugs, using food to help the drug action.",
        "Taken at bedtime",
        "Taken 30-60 minutes before bed. Suitable for tranquilizers, mild laxatives and yin-nourishing herbs, so the effect is fully exerted at night.",
        "Taken at fixed times",
        "Taken at fixed intervals (such as every 4, 6 or 8 hours) to keep the blood concentration stable. Suitable for antibiotics and antimalarials.",
        "\U0001F4DA In-depth analysis: medication timing (before / after meals / bedtime)",
        "Outpatient dispensing counseling",
        "Chinese herbal decoctions",
        "Chinese patent medicine care",
        "Switch to after meals for sensitive stomachs",
        "A tonifying formula taken on an empty stomach or before meals (such as Bu Zhong Yi Qi Tang) should be adjusted in timing for people with sensitive stomachs: taken warm at 30 C, 30-60 minutes after meals, in small frequent amounts; the aim is to reduce gastrointestinal irritation rather than change the efficacy.",
        "Switch tranquilizers to bedtime",
        "Tranquilizers (such as Tian Wang Bu Xin Dan or Zhu Sha An Shen Wan) are recommended 30 minutes before bed to aid sleep; if a tonifying formula is also included, take the tonic before meals and the tranquilizer at bedtime separately.",
        "What interval between Chinese and Western medicines?",
        "Chinese and Western medicines are advised to be spaced 30-60 minutes apart; Chinese herbs containing minerals or tannins (such as oyster shell or pomegranate peel) need a 2-hour gap from iron supplements and antibiotics to avoid chelation reactions that reduce absorption.",
        "Must tonic herbs always be taken on an empty stomach?",
        "Most tonics (tonifying qi and blood, nourishing yin and warming yang) are best taken on an empty stomach 30-60 minutes before meals for absorption; but those that irritate the gastrointestinal tract (such as those containing rhubarb, coptis, aconite or minerals) are better taken 30 minutes after meals. Tranquilizers are best taken 1 hour before bed; anthelmintics and purgatives are best taken on an empty stomach in the morning; diaphoretic formulas are taken warm and then kept out of the wind to produce a mild sweat. If epigastric discomfort or loose stools appear after taking medicine, switch to after meals and tell the physician for adjustment rather than stopping on your own.",
        "About the Medication Timing (Before/After Meal) Recommender",
        "\u23F0 Medication Timing (Before/After Meal) Recommender." + DISCL_M,
        "How to use the Medication Timing (Before/After Meal) Recommender",
        "What does the Medication Timing (Before/After Meal) Recommender do?",
        "Enter the drug category or action (such as tonic, stomachic or tranquilizing) and it recommends the best timing such as before meals, after meals or bedtime, explains the reason to reduce gastrointestinal irritation and improve absorption, for rational use guidance and patient medication education.",
        "How do I use the Medication Timing (Before/After Meal) Recommender?",
        "Which scenarios suit the Medication Timing (Before/After Meal) Recommender?",
    ]))
    write('medicinal-guide', build('medicinal-guide', [
        "\U0001F4D0 Drug Guide (Ginger / Jujube / Salt) Dose Calculator",
        "Computes the amount and use of common drug guides from the formula type and the taker's situation",
        "/ Drug guide dose calculator",
        "Select the drug guide",
        "Number of herbs in the prescription",
        "Elderly",
        "Weak constitution",
        "Formula action category",
        "Ordinary formula",
        "Interior-warming and cold-dispelling formula",
        "Heat-clearing formula",
        "Tonic formula",
        "Exterior-releasing and sweating formula",
        "Harmonizing formula",
        "Compute the drug guide amount",
        "\U0001F4D6 Common drug guides overview",
        "\U0001F4DA In-depth analysis: drug guide (ginger / jujube / wine / scallion white) dose calculation",
        "Decoction drug guides",
        "Pediatric reduction",
        "Elderly and weak",
        "Yellow wine drug guide",
        "For adults the yellow wine baseDose = 15 mL; with 8 herbs in the formula, a weak constitution factor = 0.7 and an exterior-releasing formula typeFactor = 1.0 gives totalFactor = 0.7; unitDose = ceil(15x0.7) = 11 mL and gramDose is about 10.5 g.",
        "Jujube for tonification",
        "In a tonic formula the jujube base is 4 dates; with a formula of 8 herbs (factor 1.0) plus an elderly patient (1.0) plus the tonic type (1.2 for jujube), totalFactor = 1.2 gives 4 x 1.2, about 5 dates (6 g x 1.2 is about 7.2 g).",
        "Why do the drug guide amounts differ by formula?",
        "Warm and tonifying formulas pair with ginger or yellow wine to assist warming and transportation, while cold and cool formulas reduce ginger and wine so as not to burden the stomach; exterior-releasing formulas use more ginger and harmonizing formulas use more jujube, adjusting by dosage form and channel tropism so the action reaches the intended channel.",
        "Can the drug guide be omitted?",
        "In most cases it should not be arbitrarily omitted, but it is not absolute: ginger (3 slices, about 10 g) harmonizes the stomach, stops vomiting and disperses cold; jujube (3-5 dates) tonifies the middle and moderates the property; scallion white (2-3 segments) unblocks yang and releases the exterior; yellow wine as a guide enters blood-moving formulas. If a guide is missing, a similar nature and flavor can substitute (use dried ginger at a reduced amount when fresh ginger is unavailable), but guides with a different indication direction should not be swapped (for example swapping wine for jujube in a blood-moving formula loses its meaning).",
        "About the Drug Guide (Ginger / Jujube / Salt) Dose Calculator",
        "Drug Guide (Ginger / Jujube / Salt) Dose Calculator." + DISCL_M,
    ]))


if __name__ == '__main__':
    main()
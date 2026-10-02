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
    write('tcm-adr-assessment', build('tcm-adr-assessment', [
        "\U0001F48A Adverse Reaction (ADR) Causality Assessor",
        "Assesses the causal relationship between a drug and an adverse reaction based on the Naranjo scale and the ministry ADR criteria",
        "/ ADR causality assessor",
        "Warning: this tool is for pharmaceutical professionals only and does not replace clinical judgment. ADR reports should follow the standard process of the medical institution.",
        "Suspect drug name",
        "Adverse reaction presentation",
        "\U0001F4CC Naranjo scale assessment",
        "Answer the following 10 questions item by item; the system scores automatically and determines the causality grade",
        "\U0001F4D0 Scoring criteria notes",
        "Naranjo scale grading",
        "Total 9 or above:",
        "Certain",
        "Total 5-8:",
        "Probable",
        "Total 1-4:",
        "Possible",
        "Total 0 or below:",
        "Doubtful",
        "Ministry of Health five-criteria method",
        "1. Is there a reasonable temporal sequence between the start of the drug and the onset of the ADR",
        "2. Does the ADR match the known ADR type of this drug",
        "3. Does the ADR disappear or lessen after stopping or reducing the dose",
        "4. Does the ADR recur when the same drug is used again",
        "5. Can the ADR be explained by concomitant medication or disease progression",
        "Result of the five-criteria judgment",
        "Certain:",
        "The first 4 are \"yes\" and the 5th is \"no\"",
        "Probable:",
        "The first 3 are \"yes\", the 4th is untried or unknown, and the 5th is \"no\"",
        "Possible:",
        "The first 2 are \"yes\", the 3rd is unknown or untried, the 4th is untried, and the 5th is possible",
        "Doubtful:",
        "The first 2 are \"yes\" and the 3rd to 5th are unknown or \"no\"",
        "\U0001F4DA In-depth analysis: ADR causality (10-item weighted) assessment",
        "Chinese patent medicine monitoring",
        "Hospital pharmacy affairs",
        "Post-marketing reevaluation",
        "Complete 10-item answers",
        "Tick the 10 questions step by step, score range -1 to 13; total 9 or above gives \"certain\", 5-8 gives \"probable\", 1-4 gives \"possible\", 0 gives \"doubtful\" and -1 or below gives \"impossible\"; generate the ADR report text containing drug name, clinical presentation, causality grade and handling recommendations.",
        "Unanswered item prompt",
        "If any question has no checked value then unanswered++ and the report flags \"incomplete data\" and downgrades the grade by one level; it is recommended to check past medication, rechallenge and blood concentration before finalizing the grade.",
        "How does it differ from assessor-3?",
        "tcm-adr-assessment outputs a complete PDF report (including the unanswered item prompt and handling recommendations); assessor-3 only shows the 4-level grade and is used for quick screening by clinical pharmacists.",
        "How do I read the weighted score?",
        "The weighted version gives higher weight to temporal plausibility, dechallenge/rechallenge and prior literature reports, so at the same total score a high score from key items means the causality is more reliable. When reading the score, look back at which items earned the points rather than only the total; if the points mainly come from weak evidence items such as \"reported in the literature\", then even a high total should be conservatively graded as \"possible\".",
        "About the Adverse Reaction (ADR) Causality Assessor",
        "Adverse Reaction (ADR) Causality Assessor." + DISCL_M,
        "e.g. Tripterygium wilfordii polyglycoside tablets",
        "e.g. abnormal liver function",
    ]))
    write('tcm-dosage', build('tcm-dosage', [
        "\U0001F476 Chinese Herb Dose (Adult / Child) Converter",
        "Converts the adult dose to a pediatric Chinese herb dose from the child's age or weight using multiple formulas",
        "Core formulas (from the input variables): (30 x 0.035 + 0.1) + (weight - 30) / 5 x 0.1; Math.min.apply(null, allDoses); Math.max.apply(null, allDoses)",
        "/ Chinese herb dose converter",
        "Warning: this tool is for dose reference only and does not replace the TCM practitioner's prescription. Pediatric use must be under professional physician guidance.",
        "Adult dose (g)",
        "Child age (years)",
        "Child weight (kg)",
        "Drug category",
        "Ordinary Chinese herb",
        "Toxic Chinese herb (reduced dose)",
        "Tonic",
        "1. Convert by age (most commonly used)",
        "Under 1 year: adult dose x 1/8 to 1/6",
        "1-2 years: adult dose x 1/6 to 1/5",
        "2-4 years: adult dose x 1/4",
        "4-6 years: adult dose x 1/3",
        "6-8 years: adult dose x 1/2",
        "8-12 years: adult dose x 1/2 to 2/3",
        "12-15 years: adult dose x 2/3 to the adult amount",
        "2. Young formula (by age)",
        "Child dose = adult dose x age / (age + 12)",
        "Suitable for children aged 2 to 12",
        "3. Clark formula (by weight)",
        "Child dose = adult dose x weight(kg) / 60",
        "(The adult standard weight is taken as 60 kg, which suits Chinese herbs better than the 70 kg used for Western medicine)",
        "4. Convert by body surface area (more precise)",
        "Child dose = adult dose x child body surface area / 1.73",
        "Body surface area = weight(kg) x 0.035 + 0.1 (under 30 kg)",
        "Over 30 kg: for every extra 5 kg the body surface area increases by 0.1",
        "\U0001F4CC Pediatric medication notes",
        "Toxic Chinese herbs",
        "For toxic drugs such as aconite, aconite root, strychnine, pinellia and arisaema, the pediatric dose must be reduced by an extra 30% to 50% and the decoction time extended.",
        "Children should not abuse tonics. When truly needed, keep the dose small and the course short to avoid precocious development or stagnation.",
        "Newborns and infants",
        "In infants under 1 year liver and kidney function is immature so medication requires extra caution. External medicines also carry a skin absorption risk.",
        "\U0001F4DA In-depth analysis: Chinese herb dose (adult / child) conversion",
        "Pediatric Chinese herbs",
        "Elderly and weak",
        "Toxic drug reduction",
        "Ma Huang Tang for a 6-year-old at 20 kg",
        "Adult Ma Huang 9 g; for age 6 youngDose = 9x6/(6+12) = 3 g; the Clark method gives clarkDose = 9x20/60 = 3 g; the BSA method gives bsa = 20x0.035+0.1 = 0.8 and bsaDose = 9x0.8/1.73 = 4.16 g; the mean of the four methods is about 3.5 g and for a toxic herb adjustFactor = 0.7 gives a recommended 2.45 g, take 2 to 3 g.",
        "Toxic aconite",
        "Adult aconite 10 g; the adjustment factor 0.7 gives a recommended 7 g; pre-boil 60-90 minutes to reduce the diester diterpenoid aconitine; for a 6-year-old follow the pediatric step of 1.5 g or less.",
        "Which of the four methods is most accurate?",
        "The BSA method is most sensitive to differences in child weight; the Young method suits ages 1 to 12; the Clark method suits children whose weight deviates from normal; averaging several methods and then adjusting for toxicity or tonic nature is more robust.",
        "Are newborns and infants the same?",
        "No, the younger the child the less simple proportional conversion works. Common references: within 1 year one fifth to one quarter of the adult amount, 1 to 3 years one quarter to one third, 3 to 7 years one third to one half, 7 to 12 years one half to two thirds and above 12 years close to the adult amount. But the",
        "body surface area",
        "method is more accurate for infants and toddlers; more importantly, toxic herbs (such as aconite, asarum and cinnabar) and strong purgatives that expel water require great caution in children and should be decided by a physician, and age and weight must be strictly distinguished as two separate parameters.",
        "About the Chinese Herb Dose (Adult / Child) Converter",
        "Chinese Herb Dose (Adult / Child) Converter." + DISCL_M,
    ]))
    write('tcm-pharmacoeconomics', build('tcm-pharmacoeconomics', [
        "\U0001F4B0 Pharmacoeconomics (Daily Treatment Cost) Comparator",
        "Compares the daily treatment cost (DDC) and course cost of different Chinese patent medicines and Western medicines, supporting rational drug choice",
        "Compares the daily treatment cost (DDC) and course cost of different Chinese patent medicines and Western medicines, supporting rational drug choice.",
        "/ Pharmacoeconomics comparator",
        "Warning: cost data is for reference only, and actual prices depend on local pharmacies and hospitals. This tool does not replace clinical drug choice.",
        "Package unit price (yuan)",
        "Package quantity (tablets / capsules / sachets)",
        "Single dose (tablets / capsules / sachets)",
        "Course length in days",
        "\U0001F4CA Drug cost comparison",
        "\U0001F4CC Common drug reference",
        "Click to quickly import reference data",
        "Daily treatment cost (DDC)",
        "DDC = package unit price / package quantity x single dose x daily frequency",
        "Reflects the daily drug cost the patient spends; a lower value is more economical.",
        "Total course cost",
        "Course cost = DDC x course length in days",
        "Reflects the total drug expenditure for one treatment cycle.",
        "Cost performance index",
        "Using the lowest daily cost as the base (100), a lower value for another drug means it is relatively more expensive.",
        "\U0001F4DA In-depth analysis: TCM economics (daily treatment cost / DDC) comparison",
        "Chinese patent medicine selection",
        "Insurance payment",
        "Hospital pharmacy affairs",
        "Xuesaitong vs ginkgo leaf tablets",
        "Xuesaitong 36 yuan per box of 24 capsules, 3 capsules twice daily gives unitPrice = 1.5 yuan and ddc = 1.5x3x2 = 9.0 yuan/day, 7 days = 63 yuan; ginkgo leaf tablets 28 yuan per box of 24 tablets, 2 tablets three times daily gives unitPrice = 1.17 yuan and ddc = 1.17x2x3 = 7.0 yuan/day, so the latter DDC ratio is 78%.",
        "Three-drug horizontal comparison",
        "A 4 yuan/day, B 9 yuan/day, C 15 yuan/day gives ratio A 27%, B 60%, C 100% (min 4); above 300% is a warning for C, 200%-300% is flagged, 100%-200% is economical and 100% (A) is best; a 14-day total course comes to 4x14 + 9x14 + 15x14 = 392 yuan.",
        "What does DDC mean?",
        "Defined Daily Dose Cost, the daily treatment drug cost; essential and insurance-covered drug selection often prioritizes DDC of 5 yuan/day or less; exceeding the 300% warning line requires review by the pharmacy committee.",
        "Is looking at daily cost enough?",
        "No. DDC (defined daily cost) only reflects the unit price level and cannot reflect efficacy and course length: a regimen that works slowly but has a short course may be more economical. A rational comparison should look at total course cost and cost per unit of efficacy (such as the cost needed to improve symptoms by one point), and also account for the cost of handling adverse reactions. Note also that the daily cost of same-named Chinese patent medicines from different manufacturers, or the same formula in different dosage forms, can differ several-fold, so comparisons should lock the specific manufacturer and dosage form.",
        "About the Pharmacoeconomics (Daily Treatment Cost) Comparator",
        "Pharmacoeconomics (Daily Treatment Cost) Comparator." + DISCL_M,
        "e.g. Liuwei Dihuang Wan",
    ]))


if __name__ == '__main__':
    main()
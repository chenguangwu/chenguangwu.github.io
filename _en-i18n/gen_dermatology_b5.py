#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'dermatology')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'dermatology')
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
    out = {'slug': slug, 'industry': 'dermatology', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
DISCL_M = " A professional medical tool based on authoritative medical standards, for reference only."
DISCL_D = " Results are for dermatology health education and preliminary screening reference only; they cannot replace a dermatologist's in-person examination, dermoscopy, biopsy, or other diagnostic tests and professional diagnosis. Seek timely medical care if a lesion rapidly enlarges, bleeds, ulcerates, or is accompanied by systemic symptoms such as fever."

def main():
    write('miliaria-classification', build('miliaria-classification', [
        "\U0001F4DA Miliaria (Crystal/Rubra/Pustular) Classifier",
        "Identify the four types of miliaria by sweat-duct obstruction depth and clinical presentation to guide differentiated treatment and prevention.",
        "Miliaria is classified by sweat-duct obstruction depth: miliaria crystallina (intraepidermal, clear thin-walled vesicles), miliaria rubra (intraepidermal, red papules/papulovesicles), miliaria pustulosa (rubra with secondary pustules), and miliaria profunda (upper dermis, skin-colored papules); differentiated cooling and anti-infection measures are given accordingly.",
        "Select miliaria type",
        "Miliaria crystallina",
        "Miliaria rubra",
        "Miliaria pustulosa",
        "Miliaria profunda",
        "Generate classification report",
        "Comparison table of four miliaria types",
        "Obstruction depth",
        "Mid-epidermis",
        "Epidermis (secondary to rubra)",
        "Epidermal-dermal junction",
        "Lesion morphology",
        "1-2 mm clear thin-walled vesicles",
        "2-4 mm red papules/papulovesicles",
        "Pustules on an erythematous base",
        "1-3 mm skin-colored firm papules",
        "Subjective symptoms",
        "Pruritus and burning",
        "Pruritus and pain",
        "Mild itch / anhidrosis",
        "Trunk / neck",
        "Neck / chest-back / folds",
        "Folds / scalp",
        "Trunk / limbs",
        "Predisposed population",
        "Newborns / febrile patients",
        "Infants / adults",
        "Recurrent rubra",
        "Adults in tropical regions",
        "Common triggers",
        "High temperature and fever",
        "Hot humid environment",
        "Secondary infection of rubra",
        "After recurrent rubra",
        "Prevention tips:",
        "Keep the environment well-ventilated and cool (room temperature 24-26\u00b0C), wear loose breathable cotton clothing, bathe frequently to keep skin clean and dry. Avoid over-wrapping infants. Wipe off sweat promptly and change clothes after heavy sweating.",
        "\U0001F4DA Deep Dive: Miliaria (Crystal/Rubra/Pustular) Classifier",
        "Classification reading: enter the lesion morphology (clear vesicles / red itchy papules / pustules / skin-colored induration), and the tool distinguishes crystallina, rubra, pustulosa, and profunda.",
        "Trigger analysis: highlights common triggers such as high temperature and humidity, non-breathable clothing, and poor sweating, and gives advice on environmental cooling and breathable dressing.",
        "Layered management: mild cases focus on cooling and ventilation; for pustulosa keep clean to prevent infection; for profunda or high-fever discomfort, prompt medical care is advised.",
        "Example: dense pinpoint clear vesicles on the neck without redness or itch \u2192 classified as crystallina; advise cooling, ventilation, and loose clothing; it usually resolves in days; if it turns red and itchy, it becomes rubra.",
        "Does pustulosa need antibiotics?",
        "Most pustulosa are aseptic small pustules that only need to be kept clean and dry; if there is redness, swelling, heat, pain, suppuration, or fever, seek medical care to rule out infection." + DISCL_D,
        "Why do heat and sweat cause miliaria?",
        "Sweat-duct walls rupture due to high temperature, humidity, and sweat retention, and sweat leaking into the skin causes the rash; cooling and ventilation are the most direct prevention." + DISCL_D,
        "Is miliaria profunda dangerous?",
        "Miliaria profunda (deep type) affects thermoregulation and may cause discomfort; recurrent cases should seek medical care and avoid continued high-heat environments." + DISCL_D,
        "About the Miliaria (Crystal/Rubra/Pustular) Classifier",
        "The Miliaria (Crystal/Rubra/Pustular) Classifier is an online tool in the professional medical domain." + DISCL_M,
    ]))
    write('onychomycosis-grading', build('onychomycosis-grading', [
        "\U0001F4CB Onychomycosis (Hyphae/Spore) Microscopy Grader",
        "Grade the fungal burden of onychomycosis by the detection density of hyphae and spores in KOH direct microscopy of nail scrapings, combined with the extent of nail involvement, to assist treatment decisions.",
        "Onychomycosis score = microscopy (hyphae + spores + yeast, \u00d71.2) + clinical (nail plate / number / thickening); microscopy 0 is negative; total \u22644 is 1+ mild, \u22649 is 2+ moderate, >9 is 3+ severe; moderate-to-severe suggests oral antifungal therapy.",
        "Hyphae detection density",
        "0 - Not seen",
        "1+ few (occasional on careful search)",
        "2+ moderate (visible in most fields)",
        "3+ numerous (seen in every field)",
        "Spore detection density",
        "1+ few",
        "2+ moderate",
        "3+ numerous",
        "Blastospores / pseudohyphae",
        "Extent of nail involvement",
        "0 - Not involved",
        "<25% (distal-lateral type)",
        ">50% (proximal / total dystrophic type)",
        "Number of involved nails",
        "2-3 nails",
        "\u22654 nails",
        "Nail plate thickness",
        "Thickened",
        "Fungal burden grade",
        "Microscopy findings",
        "Treatment guidance",
        "No fungal elements detected",
        "Consider culture/PCR to rule out non-fungal nail disease",
        "Few hyphae / spores",
        "Topical only (amorolfine / ciclopirox)",
        "Topical \u00b1 oral, based on extent",
        "Numerous / extensive involvement",
        "Oral antifungal (terbinafine / itraconazole)",
        "KOH microscopy cannot identify the species; concurrent fungal culture is recommended. Onychomycosis diagnosis requires clinical + microscopy/culture. Oral antifungals need liver-function tests; course: 6 weeks for fingernails, 12 weeks for toenails.",
        "\U0001F4DA Deep Dive: Onychomycosis (Hyphae/Spore) Microscopy Grader",
        "Microscopy reading: enter the KOH findings (hyphae positive / spores positive / negative) and the number of involved nails, and the tool marks the strength of evidence for fungal infection.",
        "Clinical typing: distinguish distal-lateral, white superficial, and total dystrophic types by lesion morphology, indicating differences in suitability of oral vs. topical therapy.",
        "Severity assessment: gives mild/moderate/severe by the proportion and thickness of involved nails; total dystrophy or marked subungual thickening suggests combined oral antifungal therapy.",
        "Example: right thumbnail distal yellow thickening, KOH shows hyphae positive, ~50% involved \u2192 graded moderate distal-lateral type; after confirmation at a clinic, topical/oral combination is advised.",
        "Does a negative microscopy rule out onychomycosis?",
        "Not necessarily; shallow sampling or prior medication can cause false negatives; clinically typical cases can still be combined with culture/repeat microscopy, and the final judgment is made by the physician." + DISCL_D,
        "What to watch with oral antifungals?",
        "Oral antifungals require liver-function and interaction assessment, monitoring before and during treatment, a full course as prescribed, and no self-discontinuation." + DISCL_D,
        "Is topical treatment enough?",
        "Superficial and limited involvement can be topical; total dystrophy or thick nails often need oral combination, with the specific plan decided by the physician." + DISCL_D,
        "About the Onychomycosis (Hyphae/Spore) Microscopy Grader",
        "The Onychomycosis (Hyphae/Spore) Microscopy Grader." + DISCL_M,
    ]))

if __name__ == '__main__':
    main()

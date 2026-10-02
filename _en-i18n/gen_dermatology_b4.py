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
    write('insect-bite-reaction', build('insect-bite-reaction', [
        "\U0001F9F4 Insect Bite (Dermatitis) Reaction Scorer",
        "Based on the insect-bite dermatitis reaction severity scoring system, assess local inflammatory intensity to help judge whether systemic treatment is needed.",
        "Clinical presentation score (0-3 each item)",
        "Erythema extent",
        "Edema degree",
        "2 - obvious",
        "3 - severe / tense",
        "Pruritus degree",
        "1 - occasional",
        "2 - persistent tolerable",
        "3 - severe unbearable",
        "Pain / tenderness",
        "1 - mild tenderness",
        "2 - spontaneous pain",
        "3 - severe pain",
        "Lesion count",
        "1 - 1-5",
        "2 - 6-15",
        "3 - >15",
        "Vesicle / erosion",
        "1 - small vesicles",
        "2 - bullae",
        "3 - erosion / ulceration",
        "Systemic symptoms (each adds 2 points)",
        "Fever",
        "Lymphadenopathy",
        "Generalized rash",
        "Insect type (affects management)",
        "Mosquito bite",
        "Bee / wasp sting",
        "Tick bite",
        "Spider bite",
        "Bedbug bite",
        "Flea bite",
        "Other / unknown",
        "Reference scoring criteria",
        "Local cold compress + topical antipruritic",
        "Topical corticosteroids + oral antihistamines",
        "Systemic corticosteroids + antihistamines",
        "Emergency care, watch for anaphylactic shock",
        "Bee/wasp stings and tick bites need special attention to allergic reaction and infectious disease risk. If dyspnea, laryngeal edema, or blood pressure drop of anaphylactic shock appears, call emergency services immediately.",
        "\U0001F4DA Deep Dive: Insect Bite (Dermatitis) Reaction Scorer",
        "Reaction scoring: enter the erythema diameter at the bite, whether edema/vesicles are present, and itch degree; the tool gives mild/moderate/severe grading and management points.",
        "Differentiation cue: flag large bullae, annular erythema, or linear distribution (e.g., Paederus) as special morphology to avoid misjudging as a common mosquito bite.",
        "Systemic warning: if accompanied by fever, lymphadenopathy, or widespread wheals, it suggests possible allergy/systemic reaction; advise consultation rather than local care only.",
        "Example: one 3 cm erythema on the lower leg, mild edema, itch 2/10, no vesicles \u2192 rated mild insect-bite dermatitis; advises cold compress, topical calamine / low-potency steroid, and observation.",
        "Is large swelling normal?",
        "Local redness and swelling after a bite are common, but if it rapidly expands, develops bullae, or is accompanied by fever or dyspnea, it may be allergy or infection and needs timely care." + DISCL_D,
        "How is a Paederus bite different?",
        "Paederus body fluid causes linear, streak-like erythematous vesicles with obvious burning; never slap the insect\u2014blow it away, then wash and treat as dermatitis." + DISCL_D,
        "Can you scratch the itch?",
        "Avoid scratching if possible, as breaking the skin easily leads to secondary bacterial infection; cold compress and topical antipruritics are safer, and seek care for signs of infection (purulence, heat, pain)." + DISCL_D,
        "About the Insect Bite (Dermatitis) Reaction Scorer",
        "Insect Bite (Dermatitis) Reaction Scorer. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))
    write('leprosy-grading', build('leprosy-grading', [
        "\U0001F4DA Leprosy (WHO) Grading Tool",
        "Based on the WHO leprosy disability grading system, assess peripheral nerve damage and disability in leprosy patients to guide rehabilitation.",
        "WHO leprosy disability grading (grades 0-2)",
        "Hands and feet (take the highest grade)",
        "Grade 0 - no sensory loss, no visible deformity",
        "Normal hand/foot sensation, no muscle atrophy or motor impairment",
        "Grade 1 - sensory loss but no visible deformity",
        "Protective sensation loss (cannot feel pinprick / cotton), but appearance normal",
        "Grade 2 - sensory loss with visible deformity",
        "Claw hand / foot drop / plantar ulcer / muscle atrophy / complex deformity / amputation",
        "Eyes (take the highest grade)",
        "Grade 0 - no leprosy-related eye disease",
        "Normal vision, no corneal sensation loss, no eyelid deformity",
        "Grade 1 - corneal sensation loss or mild eye disease",
        "Corneal sensation loss but no visual impairment or eyelid deformity",
        "Grade 2 - severe visual impairment or blindness",
        "Vision <6/60, lagophthalmos (incomplete eyelid closure), iridocyclitis, corneal ulcer",
        "Clinical classification (Ridley-Jopling)",
        "TT - Tuberculoid",
        "BT - Borderline tuberculoid",
        "BB - Mid-borderline",
        "BL - Borderline lepromatous",
        "LL - Lepromatous",
        "PN - Indeterminate",
        "Associated nerve damage (multiple choice)",
        "Ulnar nerve enlargement",
        "Median nerve enlargement",
        "Common peroneal nerve enlargement",
        "Great auricular nerve enlargement",
        "Nerve tenderness",
        "Nerve abscess",
        "Generate grading report",
        "WHO leprosy disability grading criteria",
        "Hands and feet",
        "Eyes",
        "No sensory loss, no visible deformity",
        "No leprosy-related eye disease",
        "Standard MDT treatment",
        "Sensory loss, no visible deformity",
        "Corneal sensation loss, no visual impairment",
        "Protection education + sensory training",
        "Sensory loss + visible deformity (claw hand / ulcer / amputation)",
        "Vision <6/60 / lagophthalmos / corneal ulcer",
        "Surgical rehabilitation + protection + assistive devices",
        "Ridley-Jopling classification reference",
        "Type",
        "Lesion count",
        "Bacterial load",
        "Contagiousness",
        "Strong",
        "1-2",
        "Stronger",
        "Several to a dozen-plus",
        "Multiple",
        "Weak",
        "Very weak",
        "Diffuse infiltration / nodules",
        "WHO MDT treatment regimen:",
        "1. Multibacillary (MB: BB/BL/LL): rifampicin + dapsone + clofazimine, 12-month course. 2. Paucibacillary (PB: TT/BT): rifampicin + dapsone, 6-month course. After completing MDT, even if lesions remain, the patient is cured and no longer contagious.",
        "Important note:",
        "Leprosy is preventable, treatable, and not to be feared. Early diagnosis and timely MDT are key to preventing disability. Grade 2 disability (G2D) is an important indicator of leprosy control; WHO targets G2D in <1% of new cases. Refer if the following 'suspected leprosy signs' appear: 1. skin shows pale/red patches with sensory loss; 2. hands/feet numbness with muscle weakness; 3. face shows infiltrative nodules or plaques; 4. peripheral nerve enlargement with tenderness.",
        "\U0001F4DA Deep Dive: Leprosy (WHO) Grading Tool",
        "Lesion counting: enter the number of visible skin lesions (anesthetic plaques); the tool distinguishes PB from MB by \u22645 / >5.",
        "Nerve assessment: mark whether accompanied by peripheral nerve enlargement, numbness, or weakness, suggesting nerve function monitoring and adequate multidrug therapy.",
        "Regimen cue: by classification, give directional reference for WHO-MDT (paucibacillary 6 months / multibacillary 12 months), emphasizing standardized medication and follow-up.",
        "Example: 3 anesthetic erythematous patches over the body with right ulnar nerve enlargement \u2192 rated PB (paucibacillary), indicating nerve involvement needing MDT and regular nerve function checks.",
        "Which is more severe, PB or MB?",
        "MB (multibacillary) has higher bacillary load, relatively stronger contagiousness, and a longer course; typing rests on lesion count and smear, set by the specialist per standards." + DISCL_D,
        "Can leprosy infect family members?",
        "After standardized MDT it quickly becomes inactive and non-contagious; daily contact risk is low; the key is early diagnosis, treatment, and completing the course." + DISCL_D,
        "Why does numbness matter?",
        "Nerve involvement can cause permanent numbness and deformity; early protection of the affected limb and nerve-function monitoring are vital for preventing disability." + DISCL_D,
        "About the Leprosy (WHO) Grading Tool",
        "Leprosy (WHO) Grading Tool is a professional medical online tool. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))

if __name__ == '__main__':
    main()

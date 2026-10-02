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
    write('seborrheic-dermatitis', build('seborrheic-dermatitis', [
        "\U0001F9F4 Seborrheic Dermatitis (Dandruff) Assessor",
        "Assess seborrheic dermatitis severity from multiple dimensions - dandruff, erythema, pruritus, scaling, and involved area - to assist shampoo and topical choice.",
        "Seborrheic dermatitis score = sum of 6 site/feature items (each 0 to 3); total \u22644 is mild, \u226410 is moderate, >10 is severe.",
        "Dandruff / scaling amount",
        "1 small and fine",
        "2 moderate, flaky",
        "3 large amount, oily thick scales",
        "1 mild pale red",
        "2 moderate obvious erythema",
        "3 severe deep red / infiltration",
        "Pruritus",
        "1 occasional mild",
        "2 frequent but tolerable",
        "3 intractable, affecting life/sleep",
        "Scale adherence",
        "0 no scales",
        "1 easily detachable",
        "2 fairly adherent",
        "3 thick crust tightly adherent",
        "Involved area",
        "1 localized scalp",
        "2 widespread scalp \u00b1 hairline",
        "3 scalp + face/chest-back, etc.",
        "Hair loss / hair involvement",
        "1 mild temporary hair loss",
        "Severity grading and treatment",
        "Antifungal shampoos containing ketoconazole / selenium sulfide / zinc pyrithione",
        "Antifungal shampoo + topical low-potency corticosteroids",
        "Combined topicals; refractory cases take oral antifungals / short-term systemic steroids",
        "Mechanism note:",
        "Seborrheic dermatitis relates to Malassezia overgrowth, sebum secretion, and skin-barrier imbalance. Treatment is mainly antifungal (ketoconazole) + anti-inflammatory; shampoo 2-3 times weekly, leave on 3-5 minutes then rinse. Facial lesions may use short-course low-potency corticosteroids plus calcineurin inhibitors for maintenance.",
        "\U0001F4DA Deep Dive: Seborrheic Dermatitis (Dandruff) Assessor",
        "Site assessment: enter scaling amount, oiliness, and erythema extent per region; the tool summarizes mild/moderate/severe grading and care priorities.",
        "Scalp quantification: grade diffuse or localized scalp desquamation separately to guide the frequency of medicated shampoos (ketoconazole / selenium sulfide / tar).",
        "Efficacy follow-up: record grading changes after intervention, observe scaling and itch relief, and assist maintenance planning.",
        "Example: oily yellow crusts on the nasolabial folds and between the eyebrows with mild erythema, moderate scalp desquamation \u2192 graded moderate seborrheic dermatitis; antifungal shampoo + short-term local low-potency steroid is advised.",
        "How to distinguish from psoriasis?",
        "Seborrheic dermatitis favors oily areas with greasy scales; psoriasis usually has thick silvery scales with the Auspitz sign; atypical cases need physician differentiation." + DISCL_D,
        "Why does it recur?",
        "It relates to Malassezia, sebum, stress, and season; hard to cure but controllable; regular care and as-needed medication reduce recurrence." + DISCL_D,
        "What about infant seborrheic dermatitis?",
        "Infant 'cradle cap' is mostly benign; gently clean after softening with warm water; obvious redness, swelling, or oozing needs medical attention." + DISCL_D,
        "About the Seborrheic Dermatitis (Dandruff) Assessor",
        "The Seborrheic Dermatitis (Dandruff) Assessor." + DISCL_M,
    ]))
    write('vss-scar', build('vss-scar', [
        "\U0001F9F4 Scar (VSS) Vancouver Scoring Tool",
        "Based on the VSS (Vancouver Scar Scale) standard, assess the severity of hypertrophic scars and keloids from four dimensions: pigmentation, vascularity, pliability, and height.",
        "Vancouver Scar Scale VSS = pigmentation P + vascularity V + pliability Pl + height H (each 0 to 3), max 12; total \u22643 is mild, \u22647 is moderate, >7 is severe.",
        "Pigmentation",
        "0 - Normal skin color",
        "1 - Hypopigmentation",
        "2 - Hyperpigmentation",
        "Vascularity",
        "0 - Normal (consistent with surroundings)",
        "1 - Pink",
        "2 - Red",
        "3 - Purple",
        "Pliability",
        "1 - Supple (easily wrinkled)",
        "2 - Yielding (bendable)",
        "3 - Firm (hard to move)",
        "4 - Band-like (cord-like)",
        "5 - Contracture (limited mobility)",
        "Height",
        "0 - Flat",
        "Calculate VSS",
        "VSS severity reference grading",
        "VSS total score",
        "Suggested intervention",
        "Observation or topical silicone gel",
        "Silicone dressing + pressure therapy",
        "Combined therapy (drug injection / laser / surgery)",
        "Scoring range:",
        "Pigmentation 0-2, vascularity 0-3, pliability 0-5, height 0-3, total 0-13. Higher score means more severe scar. Commonly used for burn and postoperative scar efficacy assessment.",
        "\U0001F4DA Deep Dive: Scar (VSS) Vancouver Scoring Tool",
        "Multidimensional assessment: enter the scar's color (vascular/pigmented), pliability (supple\u2192firm), thickness (0-3), and pain and itch (each 0-3); the tool weights and sums the VSS.",
        "Efficacy comparison: re-score after laser, injection, or surgery; a falling score reflects softening, fading, and symptom relief, assisting follow-up decisions.",
        "Key identification: locate the most severe dimension (thickness or pain) to guide the focus of local treatments such as fractional laser and intralesional injection.",
        "Example: scar dark red (high vascularity), firm, thickened 3 mm, itch 2 \u2192 high summed VSS, suggesting comprehensive treatment focused on softening, fading, and symptom control.",
        "Is lower better on every VSS dimension?",
        "Yes, lower scores on each dimension mean closer to normal skin with milder symptoms, commonly used in research and efficacy follow-up." + DISCL_D,
        "Is this also used for burn scars?",
        "The same VSS can assess hypertrophic or atrophic scars; dynamic assessment better reflects maturation and outcome." + DISCL_D,
        "When is intervention best?",
        "Intervention works best during the proliferative phase (red, firm, itchy); early laser/injection/pressure therapy is arranged by the physician based on the situation." + DISCL_D,
        "About the Scar (VSS) Vancouver Scoring Tool",
        "The Scar (VSS) Vancouver Scoring Tool." + DISCL_M,
    ]))
    write('wood-lamp', build('wood-lamp', [
        "\U0001F4DA Leukoderma (Wood's Lamp) Fluorescence Lookup",
        "Different skin diseases show characteristic fluorescence under a Wood's lamp (365 nm UV). Click a fluorescence color below to look up the corresponding skin disease and its differential significance.",
        "Wood's lamp (365 nm long-wave UV) reading: different skin diseases show characteristic fluorescence - vitiligo bright blue-white, tinea versicolor yellow-green or copper-orange, erythrasma coral red, tinea capitis blue-green, Pseudomonas infection yellow-green, porphyria pink or red; it has high auxiliary diagnostic value for superficial fungal infections.",
        "Select the observed fluorescence feature",
        "Wood's lamp examination essentials",
        "Principle:",
        "A Wood's lamp emits 320-400 nm (peak 365 nm) long-wave UV, causing certain skin substances to produce characteristic fluorescence. It must be used in a dark room; clean the affected area before examination and avoid interference from topical drugs/cosmetics.",
        "Fluorescence manifestations",
        "Vitiligo",
        "Bright porcelain-white / blue-white",
        "Confirmation and border determination; more sensitive for early lesions",
        "Tinea versicolor (pityriasis versicolor)",
        "Pale yellow / golden yellow",
        "Characteristic of Malassezia infection",
        "Erythrasma",
        "Coral red / pink",
        "Infection by Corynebacterium minutissimum",
        "Tinea capitis (Microsporum)",
        "Bright green",
        "Screening for broken hairs / kerion",
        "Melasma (epidermal type)",
        "Deepened color / enhanced contrast",
        "Differentiating epidermal from dermal type",
        "Porphyria",
        "Urine / feces pink-red",
        "Porphyria cutanea tarda",
        "The Wood's lamp is an auxiliary test that requires combination with clinical and lab tests (fungal microscopy/culture, pathology, etc.) for diagnosis. Some drugs and topical agents can produce false fluorescence.",
        "\U0001F4DA Deep Dive: Leukoderma (Wood's Lamp) Fluorescence Lookup",
        "Fluorescence reading: enter the lesion's fluorescence color under the Wood's lamp (bright blue-white / coral red / yellow-green / dark, etc.); the tool matches the characteristic manifestations of common diseases.",
        "Leukoderma differentiation: vitiligo shows bright blue-white fluorescence with clear borders, distinguished from nevus anemicus / nevus depigmentosus (no fluorescence), and helps assess the depigmentation extent.",
        "Infection clues: erythrasma coral red, tinea versicolor yellow-green, some tinea capitis green fluorescence; the tool summarizes possible pathogens and directions for care.",
        "Example: a leukoderma shows clear-bordered bright blue-white fluorescence under the Wood's lamp \u2192 the tool judges it as 'typical vitiligo fluorescence' and suggests further evaluation combining clinical and dermoscopic findings.",
        "Can a Wood's lamp confirm vitiligo?",
        "It cannot confirm alone; bright blue-white fluorescence is an important clue and must be combined with clinical, dermoscopic, and history findings." + DISCL_D,
        "Why do some tinea infections not fluoresce?",
        "Fluorescence is affected by the fungus species, medication use, and lamp intensity; absence of fluorescence does not rule out infection; microscopy or culture is needed if necessary." + DISCL_D,
        "What to prepare before the examination?",
        "Avoid applying ointments or cleansers to the area before examination; a dark room gives more accurate observation; follow the specific operational protocol." + DISCL_D,
        "About the Leukoderma (Wood's Lamp) Fluorescence Lookup",
        "The Leukoderma (Wood's Lamp) Fluorescence Lookup." + DISCL_M,
    ]))
    write('zoster-phn', build('zoster-phn', [
        "\U0001F52E Herpes Zoster (PHN) Pain Predictor",
        "Based on known acute-phase risk factors for herpes zoster, assess the risk of developing postherpetic neuralgia (PHN) to support early antiviral and analgesic intervention decisions.",
        "PHN risk score = age + acute pain severity + prodromal pain + rash severity + immune status + ocular involvement + diabetes + sex, summed; total \u22643 is low risk, \u22647 is moderate risk, >7 is high risk.",
        "< 50 years",
        "\u2265 70 years",
        "Acute-phase pain severity (NRS 0-10)",
        "0-3 mild",
        "Prodromal pain before rash",
        "Rash severity",
        "Localized (<1 dermatome)",
        "Severe (bullae / hemorrhage / \u226550 lesions)",
        "Immunocompromised (tumor / HIV / long-term immunosuppression)",
        "Trigeminal / ophthalmic branch involvement",
        "Assess PHN risk",
        "PHN risk stratification",
        "Risk score",
        "Stratification",
        "Standard antiviral therapy, symptomatic analgesia",
        "Active antiviral + early neuropathic pain management",
        "Combined analgesia, close follow-up, consider preventive intervention",
        "Key interventions:",
        "Starting antiviral therapy within 72 hours of rash onset (valacyclovir / famciclovir / acyclovir) shortens the course and lowers PHN risk. High-risk PHN populations should start neuropathic-pain drugs early (gabapentin / pregabalin), and shingles vaccination is encouraged to prevent recurrence.",
        "This tool is a risk-assessment model based on literature risk factors, not a diagnostic standard. PHN is defined as pain persisting \u22653 months after rash healing.",
        "\U0001F4DA Deep Dive: Herpes Zoster (PHN) Pain Predictor",
        "Enter onset age (\u226550/\u226560 raises risk), acute-phase pain VAS, lesion count and location; the tool indicates the PHN risk level by weighting.",
        "High-risk identification: mark advanced age, severe acute pain, ocular/auricular zoster, or immunocompromise as high risk, prompting early standardized antiviral therapy.",
        "Intervention tips: prompt that antiviral, analgesia, and nerve protection within 72h of onset lower PHN probability; those with persistent pain should see a pain clinic early.",
        "Example: 68 years old, acute-phase pain VAS 8, multiple trunk bullae \u2192 tool grades PHN high risk; advise early sufficient antiviral + analgesia and follow up whether pain exceeds 3 months.",
        "What is PHN?",
        "Pain persisting \u22653 months after rash healing is postherpetic neuralgia, related to age and severe acute pain, a common neuropathic pain in middle-aged and elderly people." + DISCL_D,
        "How to lower the risk?",
        "Start standardized antiviral and adequate analgesia as early as possible (within 72h); assess vaccination for high-risk people; involve a pain clinic promptly for chronic pain." + DISCL_D,
        "Who should get the vaccine?",
        "Those aged 50 and above, especially with a history of shingles or chronic disease, are advised to vaccinate; consult a physician for specific contraindications and regimens." + DISCL_D,
        "About the Herpes Zoster (PHN) Pain Predictor",
        "The Herpes Zoster (PHN) Pain Predictor." + DISCL_M,
    ]))

if __name__ == '__main__':
    main()

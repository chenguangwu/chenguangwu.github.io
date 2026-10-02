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
    write('calc-1', build('calc-1', [
        "\U0001F4D0 Burn Area Rule of Nines",
        "Estimate adult total body surface area (TBSA) burned by the Chinese Rule of Nines, and estimate 24-hour fluid resuscitation by body weight.",
        "Burn area = sum of each region's TBSA percentage; \u226410 mild, 10-30 moderate, 30-50 severe, \u226550 extreme; fluid volume (Parkland formula) = 4 mL \u00d7 body weight \u00d7 burn area percentage.",
        "Burn area by body region (%)",
        "Right upper limb",
        "Left upper limb",
        "Anterior trunk",
        "Posterior trunk",
        "Right lower limb",
        "Left lower limb",
        "Perineum",
        "Calculate area",
        "\U0001F4DA Deep Dive: Burn Area Rule of Nines",
        "Adult area estimation: enter the affected proportion of each region by the new Rule of Nines - head/neck 9%, both upper limbs 18%, trunk 27%, both lower limbs 46%, perineum 1% - and sum to TBSA.",
        "Small-area supplement: scattered wounds smaller than one palm (~1% TBSA) are added separately by the 'palm method' to avoid rounding errors of the Rule of Nines.",
        "Pediatric correction: for children, use age-adjusted proportions (head/neck = 9 + (12 - age)%, both lower limbs = 46 - (12 - age)%) because the head is larger and lower limbs smaller, to guide initial fluid estimation.",
        "Example: anterior right upper limb (~half of the 9% upper limb \u2248 4.5%) + anterior trunk 13.5% = ~18% TBSA; the tool gives the area and prompts that moderate burns need timely medical assessment for fluid resuscitation.",
        "How to choose between the Rule of Nines and the palm method?",
        "Use the Rule of Nines for large areas and the palm method (1 palm \u2248 1%) for scattered small wounds; the two can be combined for better precision." + DISCL_D,
        "How do area and fluid volume correspond?",
        "Clinically, formulas such as Parkland estimate 24h fluid by TBSA and weight; this tool only gives area reference, and fluid resuscitation is decided by the physician based on injury and vital signs." + DISCL_D,
        "Why are the proportions different for children?",
        "Children have a larger head and relatively smaller lower limbs, so the head/neck proportion rises with age while the lower limbs decrease, requiring the age-adjusted Rule of Nines." + DISCL_D,
        "e.g. 60",
    ]))
    write('contact-dermatitis-patch', build('contact-dermatitis-patch', [
        "\U0001F3CB\uFE0F Contact Dermatitis (Allergen) Patch Test",
        "Select positive patch-test allergens to look up common sources of allergic contact dermatitis and avoidance strategies. Patch testing is read at 48/72 hours.",
        "Patch-test reading: remove the chambers 48 hours (72 if needed) after application, wait 30 minutes, then read by ICDRG criteria - negative, doubtful (?), weak positive (+), strong positive (++), extreme positive (+++); positivity indicates allergic contact dermatitis and requires avoidance based on the allergen source.",
        "Common patch allergens (click reaction intensity)",
        "Generate avoidance advice",
        "Reading criteria:",
        "?+ doubtful (mild erythema) | + positive (erythema + infiltration + papules) | ++ strong positive (erythema + papules + small vesicles) | +++ extreme positive (confluent bullae). Note irritant reactions and false positives; reading must combine the clinical exposure history.",
        "This tool only provides avoidance guidance for common allergens and cannot replace specialist patch-test interpretation. Multiple positives warrant systematic dermatologic evaluation and an individualized avoidance plan.",
        "\U0001F4DA Deep Dive: Contact Dermatitis (Allergen) Patch Test",
        "Allergen entry: select the tested standard series allergens and enter each point's reaction intensity (+ erythema / ++ papulovesicular / +++ confluent vesicles / IR irritation); the tool organizes them by ICDRG grading.",
        "Reading-time check: prompt initial reading at 48h and re-readings at 72h and 96h; delayed reactions (e.g., fragrances, glucocorticoids) are easily missed, so avoid premature conclusions.",
        "Avoidance advice: summarize an avoidance list for positive allergens (e.g., nickel items, skincare with specific preservatives) to assist daily contact management.",
        "Example: nickel ++ at 48h worsening to +++ at 72h, fragrance mix +, rest negative \u2192 the tool judges 'nickel and fragrance mix positive (delayed)' and advises avoiding nickel jewelry and discontinuing products with that fragrance.",
        "Does a positive patch test mean it is the cause?",
        "Positivity indicates sensitization, but whether it is the cause of this episode requires synthesis with site and exposure history; past sensitization can also be positive." + DISCL_D,
        "Why check again at 96h?",
        "Fragrances and glucocorticoids often react late; those negative at 48h may turn positive at 72/96h, and missing them overlooks key allergens." + DISCL_D,
        "What to note before testing?",
        "During testing avoid sun exposure and heavy sweating from exercise, pause topical steroids, and follow the protocol and physician's instructions." + DISCL_D,
        "About the Contact Dermatitis (Allergen) Patch Test",
        "Contact Dermatitis (Allergen) Patch Test. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))
    write('hdss-hyperhidrosis', build('hdss-hyperhidrosis', [
        "\U0001F4CB Hyperhidrosis (HDSS) Severity Assessor",
        "Based on the HDSS (Hyperhidrosis Disease Severity Scale), assess how much hyperhidrosis interferes with daily life to support graded treatment decisions.",
        "HDSS severity scale 1 to 4: 1 mild, 2 moderate, 3 severe, 4 extreme; grades 3-4 suggest local botulinum toxin type A injection or systemic anticholinergics, and refractory cases are evaluated for sympathectomy.",
        "HDSS core question: to what extent does sweating interfere with your daily activities?",
        "Sweating is never noticeable and never interferes with daily activities",
        "Sweating is tolerable and occasionally interferes with daily activities",
        "Sweating is barely tolerable and frequently interferes with daily activities",
        "Sweating is completely intolerable and always interferes with daily activities",
        "Affected sites (multiple choice)",
        "Axillae",
        "Palms",
        "Soles",
        "Head and face",
        "Generalized",
        "Symptoms persist \u22656 months, at least once weekly",
        "Onset before age 25",
        "Family history of hyperhidrosis",
        "Sweating stops during sleep (suggests primary focal hyperhidrosis)",
        "HDSS grading and treatment",
        "No treatment needed or topical antiperspirant only",
        "Topical aluminum chloride + tap-water iontophoresis",
        "Botulinum toxin type A injection",
        "Botulinum toxin / systemic medication; refractory cases evaluated for sympathectomy",
        "HDSS grades 3-4 indicate severe hyperhidrosis. Rule out secondary hyperhidrosis (hyperthyroidism, diabetes, pheochromocytoma, infection, tumor, etc.), especially if generalized, nocturnal, or new-onset in adulthood.",
        "\U0001F4DA Deep Dive: Hyperhidrosis (HDSS) Severity Assessment",
        "Self-rating: choose grade 1-4 by 'no effect / occasional effect / obvious effect / always affected', and the tool gives severity and a recommended direction.",
        "Impact-domain identification: indicates whether hyperhidrosis interferes with handshakes, writing, footwear, or socializing, helping judge whether the intervention threshold (usually \u2265 grade 3) is reached.",
        "Care routing: for grades that persistently affect life, suggests consulting for topical, iontophoresis, botulinum toxin, or oral regimens.",
        "Example: palms often require frequent wiping and affect signing and socializing \u2192 rated grade 3 (obvious effect); the tool suggests consultation for botulinum toxin or iontophoresis.",
        "Does HDSS grade 3 require treatment?",
        "Grade 3 means a clear impact on life and is usually worth intervening; the specific plan (topical / botulinum toxin / oral) is set by the physician by site and severity." + DISCL_D,
        "How does primary hyperhidrosis differ from normal sweating?",
        "Primary hyperhidrosis often causes excess local sweating (palms/axillae/head-face) at normal temperature and without exercise, related to emotion and reduced during sleep; rule out secondary causes such as hyperthyroidism." + DISCL_D,
        "Can it be cured?",
        "Most cases focus on symptom control; botulinum toxin is effective but needs repetition; severe cases may be evaluated for surgery, with risks fully explained by the physician." + DISCL_D,
        "About the Hyperhidrosis (HDSS) Severity Assessor",
        "Hyperhidrosis (HDSS) Severity Assessor. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))
    write('pityriasis-rosea', build('pityriasis-rosea', [
        "\U0001F4DA Pityriasis Rosea (Herald Plaque and Daughter Lesions) Differentiator",
        "Check clinical features to help differentiate pityriasis rosea (herald plaque + daughter lesions in a Christmas-tree distribution) from tinea corporis, secondary syphilis, guttate psoriasis, and similar diseases.",
        "Pityriasis rosea diagnosis: count the number of satisfied features among 10 clinical features (herald plaque, Christmas-tree distribution, collarette scale, etc.) and core features; \u22658 with \u22653 core = highly consistent, \u22655 with \u22652 core = fairly consistent, otherwise differentiate from tinea corporis / secondary syphilis / guttate psoriasis.",
        "Clinical features (check those that apply)",
        "A single larger 'herald plaque' appears first (2-10 cm oval orange-pink patch)",
        "Days later, numerous smaller 'daughter lesions' appear on the trunk/proximal limbs",
        "Lesion long axes follow skin lines / Langer lines (a 'Christmas tree' pattern on the back)",
        "Collarette fine scaling at the edges (collarette scale)",
        "Mild to moderate itching",
        "Mainly on trunk and proximal limbs; face and distal sites rare",
        "Self-limiting course (usually resolves in 6-8 weeks)",
        "No palmoplantar involvement, no mucosal lesions",
        "No recent new drug use (rule out drug eruption)",
        "Negative fungal microscopy (rule out tinea corporis)",
        "Analysis and differentiation",
        "Key points for common differential diagnoses",
        "Tinea corporis",
        "Annular erythema with active scaling at the border and central clearing; positive fungal microscopy; no Christmas-tree distribution. KOH microscopy confirms.",
        "Secondary syphilis",
        "Coppery-red papules on palms/soles, generalized lymphadenopathy, possible mucosal patches; history of sexual contact / chancre; positive syphilis serology (RPR/TPPA).",
        "Guttate psoriasis",
        "Drop-like red papules/plaques with silvery scales; pinpoint bleeding on scraping (Auspitz sign); often triggered by streptococcal infection.",
        "Nummular eczema",
        "Coin-shaped erythema, oozing and crusting, intense itching; common on extensor limbs; no collarette scaling or Christmas-tree distribution.",
        "Drug eruption",
        "History of drug use, polymorphic rash, possible mucosal involvement; gradually resolves after stopping the drug. A detailed drug history is needed.",
        "Pityriasis rosea is mostly self-limiting, managed with symptomatic antipruritic care. If palms/soles are involved, systemic symptoms are marked, or high-risk sexual behavior exists, syphilis must be ruled out. Atypical or persistent cases should see a dermatologist.",
        "\U0001F4DA Deep Dive: Pityriasis Rosea (Herald Plaque and Daughter Lesions) Differentiation",
        "Herald-plaque recognition: enter the first single oval erythematous plaque (herald plaque) and the subsequent daughter lesions along a 'Christmas-tree' orientation on the trunk/limb flexures; the tool flags the typical pityriasis rosea pattern.",
        "Differentiation cue: for atypical distributions (face-only, inverse, annular) mark the need to rule out syphilis, tinea, psoriasis, or drug eruption, and advise consultation.",
        "Course education: note the disease is mostly self-limiting (6-8 weeks) and give antipruritic and avoid-overly-hot-baths care points to reduce misuse of potent drugs.",
        "Example: a herald plaque first appears on chest/back, then 1-2 weeks later oval daughter lesions align along skin lines on the trunk \u2192 the tool judges 'typical pityriasis rosea pattern' and advises observing self-limitation with symptomatic antipruritic care.",
        "Does pityriasis rosea need medication?",
        "Mostly self-limiting, managed with antipruritics, moisturizing, and avoiding hot baths; widespread or intensely itchy cases may use antihistamines or phototherapy per physician advice, without overmedication." + DISCL_D,
        "How to distinguish from syphilis?",
        "Atypical or generalized cases need to rule out secondary syphilis; physicians often combine history and serology, consulting when needed for a clear diagnosis." + DISCL_D,
        "Is it contagious?",
        "Generally considered non-contagious, possibly related to a post-viral reaction; just avoid scratching to prevent secondary infection." + DISCL_D,
        "About the Pityriasis Rosea (Herald Plaque and Daughter Lesions) Differentiator",
        "Pityriasis Rosea (Herald Plaque and Daughter Lesions) Differentiator. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))
    write('salt-alopecia', build('salt-alopecia', [
        "\U0001F4CB Alopecia Areata (SALT) Severity Assessor",
        "Based on the SALT (Severity of Alopecia Areata Tool) standard, divide the scalp into four regions and weight each region's hair-loss percentage to compute the severity of alopecia areata involvement.",
        "SALT = 0.40\u00d7top% + 0.24\u00d7posterior% + 0.18\u00d7right% + 0.18\u00d7left%",
        "Top (parieto-occipital)",
        "Weight 40%",
        "Posterior (occipital)",
        "Weight 24%",
        "Right (temporo-parietal)",
        "Weight 18%",
        "Left (temporo-parietal)",
        "Body hair involved (eyebrows / beard / body hair)",
        "With nail changes (pitting, leukonychia, etc.)",
        "Calculate SALT",
        "Alopecia areata severity grading (S grading)",
        "SALT (hair loss %)",
        "Mild, mainly local treatment",
        "Moderate, local + contact immunotherapy",
        "Moderate-severe, needs systemic evaluation",
        "Severe, systemic treatment",
        "Alopecia totalis; S5b with body-hair loss is alopecia universalis",
        "SALT = 0.40\u00d7top% + 0.24\u00d7posterior% + 0.18\u00d7right% + 0.18\u00d7left%. Range 0-100, representing the scalp hair-loss percentage. Treatment response is commonly assessed by the SALT improvement rate.",
        "\U0001F4DA Deep Dive: Alopecia Areata (SALT) Severity Assessment",
        "Regional estimation: enter the hair-loss area proportion of each scalp region (top / temporal / occipital, etc.); the tool weights and sums SALT (0-100, representing overall hair loss",
        "Severity stratification: by SALT, mild (<25%), moderate (25-50%), severe (>50%); alopecia totalis/universalis are marked separately.",
        "Efficacy follow-up: re-evaluate before and after treatment; a falling hair-loss % indicates regrowth progress and helps judge response to topical, intralesional, or systemic therapy.",
        "Example: ~40% top loss and ~10% each temporal side \u2192 the tool sums SALT\u224860%, indicating severe alopecia areata and suggesting active intralesional/topical therapy and systemic evaluation.",
        "What is SALT 100?",
        "It represents nearly complete scalp hair loss (alopecia totalis); if eyebrows and eyelashes also fall out it is alopecia universalis, needing more active evaluation and follow-up." + DISCL_D,
        "Can alopecia areata grow back on its own?",
        "Some mild cases spontaneously regrow, but large or long-standing areas recover slowly; standardized treatment (intralesional / topical / systemic) aids recovery." + DISCL_D,
        "Is self-estimation accurate?",
        "Regional area estimation is a trend reference; trichoscopy and physician assessment are more accurate; rapidly expanding or nail-changing cases should seek care promptly." + DISCL_D,
        "About the Alopecia Areata (SALT) Severity Assessor",
        "Alopecia Areata (SALT) Severity Assessor. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))
    write('vasi-vitiligo', build('vasi-vitiligo', [
        "\U0001F4D0 Vitiligo (VASI) Pigmented Area Assessor",
        "Based on the VASI (Vitiligo Area Scoring Index) standard, quantify each region's depigmented area and degree using the patient's 'palm units' (palm + fingers \u2248 1% body surface area) to assess the extent of vitiligo involvement.",
        "VASI = \u03a3(each region's palm units \u00d7 depigmentation%)",
        "For each region enter: \u2460 the depigmented area in patient 'palm units' (1 palm \u2248 1% body surface); \u2461 the depigmentation percentage within that region (0-100, fully depigmented = 100)",
        "Palm units",
        "Depigmentation (%)",
        "Upper limbs (including hands)",
        "Lower limbs (including feet)",
        "Palms/soles / genitals / folds",
        "Calculate VASI",
        "VASI severity reference grading",
        "VASI (body-surface depigmentation %)",
        "Localized, mainly topical drugs",
        "Topical treatment + narrowband UVB",
        "Mainly phototherapy, consider systemic intervention",
        "Systemic treatment, some may consider depigmentation",
        "VASI = \u03a3(each region's palm units \u00d7 depigmentation%). The result approximates the percentage of involved body-surface area. Treatment response is commonly assessed by the VASI improvement rate (percentage drop from baseline).",
        "\U0001F4DA Deep Dive: Vitiligo (VASI) Pigmented Area Assessment",
        "Regional assessment: enter each body region's vitiligo area proportion and its depigmentation degree (0-100% depigmented); the tool weights and sums VASI.",
        "Severity stratification: by VASI, distinguish mild/moderate/severe depigmentation burden; generalized (>50%) is flagged for higher attention.",
        "Efficacy follow-up: re-evaluate before and after treatment; a falling depigmentation % or appearance of repigmentation islands indicates recovery progress and helps adjust phototherapy/topical plans.",
        "Example: both hands 5% area and nearly complete depigmentation (95%), trunk 20% area and 60% depigmentation \u2192 the tool weights to VASI\u224816+12=28, indicating phototherapy + topical agents to promote repigmentation as the focus.",
        "Is a lower VASI better?",
        "Yes, a lower VASI means a smaller overall depigmentation burden and more repigmentation, commonly used in efficacy follow-up and drug trials." + DISCL_D,
        "Can vitiligo repigment?",
        "In stable disease, phototherapy with topical steroids / calcineurin inhibitors promotes repigmentation; large areas or mucosal sites are harder and need patient treatment." + DISCL_D,
        "Will it turn all white?",
        "Progression speed and extent vary by person; standardized treatment controls it; rapidly expanding or white-hair-associated cases should see a dermatologist promptly." + DISCL_D,
        "About the Vitiligo (VASI) Pigmented Area Assessor",
        "Vitiligo (VASI) Pigmented Area Assessor. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))

if __name__ == '__main__':
    main()

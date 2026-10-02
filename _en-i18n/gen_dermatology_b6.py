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
    write('index', build('index', [
        "\U0001F9F4 Dermatology & STD Tools",
        "Dermatology & STD",
        "Dermatology & STD Tools",
        "Based on the HDSS (Hyperhidrosis Disease Severity Scale), assess how much hyperhidrosis interferes with daily life to assist treatment grading decisions.",
        "Based on known acute-phase risk factors for herpes zoster, assess the risk of developing postherpetic neuralgia (PHN) to support early antiviral and analgesic intervention decisions.",
        "Grade the fungal burden of onychomycosis by the detection density of hyphae and spores in KOH direct microscopy of nail scrapings, combined with the extent of nail involvement, to assist treatment decisions.",
        "Enter the GAGS score by acne lesion type and location, with automatic grading (mild/moderate/severe) and severity prompts, for acne assessment and follow-up.",
        "Calculate the SALT alopecia severity score by the proportion of hair loss area in each scalp region, quantifying the extent of hair loss for alopecia areata record-keeping and treatment comparison.",
        "Assess the severity of actinic keratosis (AK) based on the Olsen grade and lesion features, evaluating malignancy risk and treatment indications.",
        "Grade pernio (chilblains) by its cutaneous manifestations and provide warming and treatment guidance based on involvement.",
        "Estimate adult total body surface area (TBSA) burned by the Chinese Rule of Nines, and estimate 24-hour fluid resuscitation by body weight.",
        "Assess scar severity by four items - color, thickness, pliability, and relief (Vancouver scale, total 0-14); higher scores mean more severe, used in burn and plastic surgery follow-up.",
        "Assess seborrheic dermatitis severity by four items - erythema, scaling, pruritus, and involved area (each 0-3) - and provide grading, for efficacy follow-up and disease records.",
        "Calculate the SCORAD index by combining lesion area, subjective symptoms, and sign intensity to assess atopic dermatitis severity, for dermatology diagnosis and efficacy follow-up reference.",
        "Calculate the total EASI score by the area of eczema involvement and the intensity of four items - erythema, induration, excoriation, and lichenification - to quantify severity for dermatology efficacy assessment.",
        "Calculate the VASI vitiligo severity score by the weighted percentage of depigmentation in each body region, quantifying pigment loss for disease records and repigmentation efficacy assessment.",
        "Calculate the total PASI score by the area of head, upper limbs, trunk, and lower limbs and the intensity of erythema, induration, and desquamation, quantifying psoriasis severity for efficacy assessment reference.",
        "Select positive patch-test allergens to look up common sources of allergic contact dermatitis and avoidance strategies. Patch testing is read at 48/72 hours.",
        "Based on an insect-bite dermatitis reaction severity scoring system, assess local inflammatory response intensity to help judge whether systemic treatment is needed.",
        "Based on the VSS (Vancouver Scar Scale) standard, assess the severity of hypertrophic scars and keloids from four dimensions: pigmentation, vasculature, pliability, and height.",
        "Check clinical features to help differentiate pityriasis rosea (herald patch + Christmas-tree distribution of daughter patches) from tinea corporis, secondary syphilis, guttate psoriasis, and other similar diseases.",
        "Based on sweat-duct obstruction depth and clinical manifestations such as red rashes and pustules, quickly differentiate the four miliaria types - crystallina, rubra, pustulosa, and profunda - and give differentiated treatment and prevention advice.",
        "Different skin diseases show characteristic fluorescence under a Wood's lamp (365 nm UV). Click a fluorescence color below to look up the corresponding skin disease and its differential significance.",
        "Based on the dermoscopy ABCD rule, calculate the total TDS to screen melanoma risk. TDS>5.45 suggests possible melanoma and biopsy is needed for confirmation.",
        "Assess seborrheic dermatitis severity from multiple dimensions - dandruff, erythema, pruritus, scaling, and involved area - to assist shampoo and topical choice.",
        "Based on the WHO leprosy disability grading system, assess peripheral nerve damage and disability in leprosy patients to guide rehabilitation.",
        "About Dermatology & STD Tools",
        "The Dermatology & STD Tools collection includes 23 free online tools covering common calculation, conversion, and lookup needs in dermatology and STD scenarios. Whether you are a practitioner, student, or general user in the field, you can find ready-to-use practical tools here. All tools run purely in the frontend, with no data uploaded to servers, protecting your privacy and security.",
        "The dermatology and STD tools on this page include (representative tools):",
        "These tools help you quickly complete common dermatology- and STD-related tasks without memorizing complex formulas or manual conversions; just input and get results.",
        "Do the dermatology and STD tools need to be downloaded or registered?",
        "No. All dermatology and STD tools on this page are pure-frontend online tools; open the page and use them directly, with no software installation, no account registration, and no data upload.",
        "Are the calculation results of the dermatology and STD tools accurate? Is the data secure?",
        "The tools compute locally in your browser based on public mathematical formulas and general industry standards, with instant results. All calculations are completed locally on your device, and data is never uploaded to servers, ensuring privacy and security.",
    ]))
    write('pasi-score', build('pasi-score', [
        "\U0001F4D0 Psoriasis (PASI) Area & Severity Score",
        "Based on the PASI (Psoriasis Area and Severity Index) standard, comprehensively score the area and lesion severity (erythema, induration, desquamation) of four body regions for psoriasis assessment and efficacy monitoring.",
        "PASI = 0.1\u00d7(E+I+D)\u00d7A head-neck + 0.2\u00d7(E+I+D)\u00d7A upper limbs + 0.3\u00d7(E+I+D)\u00d7A trunk + 0.4\u00d7(E+I+D)\u00d7A lower limbs",
        "Head / neck",
        "Weight 0.1 (10% of body surface)",
        "Induration",
        "Desquamation",
        "Upper limbs",
        "Weight 0.2 (20% of body surface)",
        "Trunk",
        "Weight 0.3 (30% of body surface)",
        "Lower limbs",
        "Weight 0.4 (40% of body surface)",
        "Calculate PASI",
        "PASI severity grading",
        "PASI score",
        "Lesions are relatively localized; topical agents are the mainstay",
        "Systemic therapy or phototherapy is needed",
        "Systemic therapy (biologics, etc.) is recommended",
        "Head-neck",
        ". PASI 75/90/100 are commonly used as efficacy endpoints (percentage improvement from baseline).",
        "\U0001F4DA Deep Dive: Psoriasis (PASI) Area & Severity Score",
        "Four-region assessment: enter the area grade (0-6) and three severity items (each 0-4) per region; the tool computes each region's score by head 0.1, upper limbs 0.2, trunk 0.3, lower limbs 0.4 weights and sums to PASI.",
        "Efficacy reading: the PASI difference and improvement rate before and after treatment (e.g., achieving PASI 75) are key clinical efficacy indicators; the tool assists before-after comparison.",
        "Key-region identification: outputs each region's score, locates the most severe region, and guides the intensity of local treatment and discussion of systemic therapy such as biologics.",
        "Example: lower-limb area grade 5, all three severity items 3 \u2192 that region \u2248 0.4\u00d75\u00d7(3+3+3)=18; adding the other regions gives PASI\u224826, moderate-to-severe, suggesting systemic therapy evaluation.",
        "What does PASI 75 mean?",
        "It means PASI decreases by \u226575% from baseline after treatment, a common efficacy threshold; PASI 90/100 represent even better control." + DISCL_D,
        "Does a higher score mean more severe?",
        "Yes, PASI ranges 0-72; higher means greater area and inflammation, commonly used for follow-up and drug efficacy assessment." + DISCL_D,
        "Is self-scoring accurate?",
        "Area and severity need training; self-assessment is fine for trends; treatment decisions are based on physician assessment plus PASI and quality of life." + DISCL_D,
        "About the Psoriasis (PASI) Area & Severity Score",
        "The Psoriasis (PASI) Area & Severity Score." + DISCL_M,
    ]))
    write('rater-28', build('rater-28', [
        "\U0001F9F4 Scar (VSS) Vancouver Score",
        "Scar assessment = thickness + vascularity + pliability + color (each 0 to 3); total \u22643 is mild, \u22647 is moderate, >7 is severe (Vancouver Scar Scale, VSS).",
        "Vancouver Scar Scale (VSS) (4 dimensions, total 0-14; higher score means more severe scar)",
        "1. Thickness",
        "0-1 mm (1 point)",
        "1-2 mm (2 points)",
        ">2 mm (3 points)",
        "2. Vascularity",
        "Similar to normal skin (0 points)",
        "Pink (1 point)",
        "Red (2 points)",
        "Purple (3 points)",
        "3. Pliability",
        "Supple (slight resistance) (1 point)",
        "Yielding (2 points)",
        "Bendable but with some force (3 points)",
        "Firm (4 points)",
        "Contracture causing deformity (5 points)",
        "Mild pigmentation (1 point)",
        "Moderate pigmentation (2 points)",
        "Severe pigmentation / depigmentation (3 points)",
        "\U0001F4DA Deep Dive: Scar (VSS) Vancouver Score",
        "Multidimensional assessment: enter the scar's color (vascular/pigmented), pliability (supple\u2192firm), thickness (0-3), and pain and itch (each 0-3); the tool weights and sums the VSS.",
        "Efficacy comparison: re-score before and after laser, injection, or surgery; a falling score reflects scar softening, fading, and symptom relief, assisting follow-up.",
        "Key-item identification: locate the most severe dimension (e.g., thickness or pain) to guide the focus of local treatments (e.g., fractional laser, intralesional injection).",
        "Example: scar red (vascularity 2), firm (pliability 3), thickened 2 mm (thickness 2), occasional itch (1) \u2192 high summed VSS, suggesting comprehensive treatment focused on softening and fading.",
        "Is a lower VSS score better?",
        "Yes, lower VSS dimension scores mean the scar is closer to normal skin with milder symptoms, commonly used in research and efficacy follow-up." + DISCL_D,
        "Is the scoring the same for new and old scars?",
        "Early scars are red, firm, and itchy with high scores; mature scars trend flat, soft, and faded; dynamic assessment better reflects the course." + DISCL_D,
        "Can a scar disappear or flatten?",
        "Most can improve (soften, fade, flatten), but complete removal is difficult; the specific laser/injection/surgery plan is decided by the physician." + DISCL_D,
        "About the Scar (VSS) Vancouver Score",
        "The Scar (VSS) Vancouver Score.",
        "Multi-dimensional scoring by vascularity / pigmentation / pliability / thickness / pain-itch",
        "Objective quantification of scar severity",
        "Follow-up before and after laser, injection, etc.",
        "Burn or postoperative scar assessment",
        "Preliminary grading before seeing a doctor",
    ]))
    write('scorad-index', build('scorad-index', [
        "\U0001F9F4 Atopic Dermatitis (SCORAD) Index Assessor",
        "Based on the SCORAD (Severity Scoring of Atopic Dermatitis) standard, assess the severity of atopic dermatitis/eczema from three dimensions: lesion area (A), lesion intensity (B), and subjective symptoms (C).",
        "A. Lesion area (percentage of body surface, 0-100)",
        "Estimate by the 'Rule of Nines': head-neck 9%, each upper limb 9%, anterior trunk 18%, posterior trunk 18%, each lower limb 18%, perineum 1%.",
        "B. Lesion intensity (6 items, each 0-3, max 18)",
        "Edema / papules",
        "Oozing / crusting",
        "Dryness",
        "C. Subjective symptoms (each 0-10, max 20; patient's average score over the last 3 days)",
        "Pruritus intensity",
        "Sleep loss",
        "Calculate SCORAD",
        "SCORAD severity grading",
        "SCORAD score",
        "Mainly topical corticosteroids and emollients",
        "Standardized topical therapy is needed, with systemic intervention if necessary",
        "Systemic therapy is recommended; consider biologics",
        "SCORAD = A/5 + 7\u00d7B/2 + C = A/5 + 3.5\u00d7B + C (A is area %, B is intensity score, C is subjective score). Children may use objective SCORAD (only A/5 + 7B/2).",
        "\U0001F4DA Deep Dive: Atopic Dermatitis (SCORAD) Index Assessor",
        "Three-dimensional entry: enter the lesion area proportion, six sign-intensity items, and itch/sleep disturbance; the tool computes the composite SCORAD by the standard weighted formula.",
        "Severity stratification: by SCORAD, mild (<25), moderate (25-50), severe (>50), assisting treatment-intensity selection.",
        "Efficacy comparison: SCORAD changes before and after treatment directly reflect improvement in inflammation, itch, and sleep, guiding topical/systemic treatment adjustment.",
        "Example: area 30%, all six intensity items 2, itch 7/sleep 5 \u2192 the tool computes SCORAD about 40+ by weighting, moderate-to-severe, suggesting stronger emollient and anti-inflammatory care.",
        "Does a higher SCORAD mean more severe?",
        "Yes, SCORAD integrates area, signs, and itch/sleep; higher means more severe, commonly used for follow-up and efficacy assessment." + DISCL_D,
        "Does dryness count as an intensity item?",
        "In common versions dryness is counted in the intensity score; practices vary slightly by center, and the tool gives the standard six items for trend reference." + DISCL_D,
        "How to score children?",
        "Same standard, but children have greater itch/sleep impact; assessment should combine age and care, with specifics per pediatric/dermatology advice." + DISCL_D,
        "About the Atopic Dermatitis (SCORAD) Index Assessor",
        "The Atopic Dermatitis (SCORAD) Index Assessor." + DISCL_M,
        "Is this tool free?",
        "Completely free, no registration needed, used directly in the browser.",
    ]))

if __name__ == '__main__':
    main()

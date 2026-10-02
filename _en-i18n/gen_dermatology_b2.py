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
    write('actinic-keratosis', build('actinic-keratosis', [
        "\U0001F4CB Actinic Keratosis (Erythema) Border Assessor",
        "Assess the severity of actinic keratosis (AK) and its malignant transformation risk and treatment indications based on the Olsen grading and lesion features",
        "Lesion feature assessment",
        "1. Erythema / inflammation",
        "1 - faint pink",
        "2 - obvious red",
        "3 - deep / dark red",
        "2. Scale / keratosis",
        "1 - thin scale",
        "2 - moderate scale",
        "3 - thick keratosis",
        "3. Border definition",
        "0 - ill-defined border",
        "1 - partially clear",
        "2 - clear border",
        "3 - sharply raised edge",
        "4. Lesion size",
        "5. Palpation texture",
        "0 - smooth",
        "2 - sandpaper-like rough",
        "3 - firm nodular feel",
        "6. Lesion count",
        "0 - solitary (1)",
        "1 - few (2-5)",
        "2 - multiple (6-15)",
        "3 - widespread (>15)",
        "High-risk features (each selected +2 points)",
        "Rapid enlargement",
        "Bleeding / ulceration",
        "Tenderness / pain",
        "Immunosuppressed state",
        "Scalp (balding area)",
        "Ear",
        "Lower lip",
        "Other sites",
        "Olsen AK severity grading criteria",
        "Malignant transformation risk",
        "Grade 1 (mild)",
        "Faint erythema, thin scale, palpable",
        "Low (<1%/year)",
        "Observation / topical agents",
        "Grade 2 (moderate)",
        "Obvious erythema + keratosis, clear border",
        "Moderate (1-5%/year)",
        "Topical agents / cryotherapy",
        "Grade 3 (severe)",
        "Marked keratotic thickening, may be verrucous",
        "Higher (5-10%/year)",
        "Cryotherapy / surgery / photodynamic therapy",
        "Rapid enlargement / bleeding / ulceration / pain",
        "High (>10%/year)",
        "Biopsy + surgical excision",
        "Clinical points:",
        "Actinic keratosis (AK) is a precancerous lesion that can progress to squamous cell carcinoma (SCC). High-risk features (rapid enlargement, bleeding, ulceration, pain, immunosuppression) are strong indications for biopsy and active treatment. Face, scalp, ear, and lower lip are high-risk sites. Widespread AK suggests a 'field cancerization' effect requiring comprehensive management.",
        "\U0001F4DA Deep Dive: Actinic Keratosis (Erythema) Border Assessment",
        "Sun-exposed-site screening: enter the count and largest diameter of AK lesions on sun-exposed areas such as face, scalp, and dorsum of hands, and preliminarily read risk by Olsen clinical grading (I erythema, II scale, III marked keratosis).",
        "Follow-up monitoring: compare lesion count and grading between two assessments, flag new or progressive lesions, and help decide whether cryotherapy or photodynamic therapy is needed.",
        "Risk education: flag multiple or thickened (grade III) lesions for higher attention, and with risk factors such as immunosuppression and fair skin, advise regular dermatology review.",
        "Example: 6 AK lesions on the face, the largest 8 mm with marked keratotic thickening (Olsen III), the rest erythematous and scaly (I-II). The tool summarizes as 'multiple, with high-grade lesions' and advises prioritizing the thickened ones and shortening the review interval.",
        "Can this grading diagnose skin cancer?",
        "No. AK is a precancerous lesion, and this tool only provides preliminary clinical morphological grading; whether it is malignant requires the physician to combine dermoscopy, biopsy, etc., and consult promptly if needed." + DISCL_D,
        "Must Olsen grade III always be treated?",
        "Lesions with marked thickening and keratosis have a higher progression risk and are usually advised active treatment (cryotherapy / photodynamic / topical, etc.); the specific plan is set by the dermatologist." + DISCL_D,
        "How often should review be done?",
        "Generally follow up every 6-12 months; multiple lesions, immunosuppression, or prior progression shorten to 3-6 months, subject to the physician's arrangement." + DISCL_D,
        "About the Actinic Keratosis (Erythema) Border Assessor",
        "Actinic Keratosis (Erythema) Border Assessor. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))
    write('assessor-14', build('assessor-14', [
        "\U0001F4CB Seborrheic Dermatitis (Dandruff) Assessment",
        "Dandruff",
        "Seborrheic dermatitis score = erythema + scaling/dandruff + itching + affected area (each 0 to 3); \u22643 mild, \u22647 moderate, >7 severe.",
        "Seborrheic dermatitis severity score (erythema / scaling / itching / affected area, 0-3 each)",
        "1. Erythema degree",
        "No erythema (0)",
        "Mild redness (1)",
        "Obvious erythema (2)",
        "Severe deep red (3)",
        "2. Scaling / dandruff",
        "No scaling (0)",
        "Sparse fine scale (1)",
        "Abundant greasy scale (2)",
        "Thick crusting (3)",
        "3. Itching degree",
        "No itching (0)",
        "Occasional mild itch (1)",
        "Obvious itch affecting life (2)",
        "Severe unbearable itch (3)",
        "Localized (<10% scalp/face) (1)",
        "Multiple regions (10%-30%) (2)",
        "Widespread (>30%) (3)",
        "\U0001F4DA Deep Dive: Seborrheic Dermatitis (Dandruff) Assessment",
        "Dandruff assessment: enter the coverage and greasiness of scalp scale and whether erythema is present; the tool gives mild/moderate/severe grading and care priorities.",
        "Facial involvement assessment: enter erythema and scaling in seborrheic zones such as eyebrows, nasolabial folds, and behind the ears to judge whether antifungal or low-potency topical steroids are needed.",
        "Efficacy follow-up: record grading changes before and after medication/shampoo intervention, observe whether scale and itch improve, and help decide a maintenance plan.",
        "Example: diffuse fine scalp scale with mild erythema and occasional itch is rated 'mild seborrheic dermatitis'; the tool suggests a ketoconazole / selenium sulfide shampoo twice weekly and observation for 2-4 weeks.",
        "Can the result replace a doctor's diagnosis?",
        "No. This tool is for self-monitoring reference; if erythema is marked, there is oozing, hair loss, or it does not heal, consult to rule out psoriasis, fungal infection, etc." + DISCL_D,
        "Why is it worse in winter?",
        "Seborrheic dermatitis often worsens with dryness, staying up late, and stress; Malassezia colonization and sebum production act together, and moisturizing and regular routines help relieve it." + DISCL_D,
        "How to set shampoo frequency?",
        "Aim for oil control and desquamation without irritation; medicated shampoos per instructions 2-3 times weekly, then reduce frequency for maintenance after symptoms ease, avoiding over-cleansing that damages the barrier." + DISCL_D,
        "About the Seborrheic Dermatitis (Dandruff) Assessment",
        "Seborrheic Dermatitis (Dandruff) Assessment.",
        "Graded by scalp and facial scale, greasiness, erythema, and itching",
        "Self-monitoring of dandruff and seborrheic dermatitis",
        "Reference for medicated shampoo frequency",
        "Efficacy follow-up and care adjustment",
        "Preliminary assessment before consultation",
    ]))
    write('chilblain-grading', build('chilblain-grading', [
        "\U0001F4CB Chilblain (Grading) and Warming Guide",
        "Grade chilblain (cold-induced erythema) by lesion presentation and provide warming and treatment guidance based on involvement.",
        "Chilblain grades I/II/III: grade I erythema and edema, grade II vesicles and erosion, grade III ulceration and necrosis; secondary infection needs topical anti-infection and severe cases need oral antibiotics.",
        "Chilblain severity grading",
        "Erythema, swelling, itch/burning, no vesicles",
        "Erythema + vesicles/erosion, marked pain",
        "Ulceration/necrosis, involving deep tissue",
        "Involvement (multiple choice)",
        "Fingers / dorsum of hands involved",
        "Toes / heels involved",
        "Auricle / nasal tip involved",
        "Recurs every year (chronic chilblain)",
        "Secondary infection (purulence, lymphadenopathy)",
        "Generate guidance",
        "Warming and prevention points",
        "Warming principles:",
        "1 Keep hands and feet dry and warm, wear gloves / thick socks and warm shoes; 2 avoid prolonged exposure to cold-wet environments; 3 do not directly roast the frozen area with hot water / a stove (easily causes necrosis); 4 rewarm gradually (soak in 37-40\u00b0C warm water for 15-30 min); 5 improve nutrition and exercise to enhance peripheral circulation; 6 quit smoking (nicotine constricts vessels).",
        "Treatment:",
        "Grade I is mainly warming + topical vasodilators (e.g., nifedipine cream / sodium heparin); grade II needs vesicle care to prevent infection; grade III needs debridement and dressing changes, with anti-infection if needed. Recurrent cases may take oral nifedipine / nicotinamide to improve circulation.",
        "Warning:",
        "If chilblain-like lesions are accompanied by systemic symptoms, persist in summer, or have atypical distribution, systemic diseases such as chilblain lupus and cryoglobulinemia must be ruled out.",
        "\U0001F4DA Deep Dive: Chilblain (Grading) and Warming Guidance",
        "Degree reading: enter the lesion morphology by site (finger/toe/ear/nose) - erythema and swelling (I), vesicles (II), or ulceration/necrosis (III) - and the tool outputs the degree and cautions.",
        "Warming guidance: by degree, give rewarming method (avoid roasting), warming level, and activity advice; grade I mainly warming and observation, grades II/III prompt consultation.",
        "Recurrence management: for those who recur each winter, advise pre-winter warming protection and local circulation improvement to reduce recurrence.",
        "Example: toes show purplish-red edematous plaques with itch but no ulceration \u2192 rated grade I chilblain; advise warm-water rewarming, thick-sock warming, and avoid scratching; consult if not improved or worsened in 1-2 weeks.",
        "Can chilblain be warmed by a fire?",
        "Direct roasting or sudden heat is not advised; rewarm slowly with warm water (~37-40\u00b0C), as sudden heat worsens tissue damage and itching." + DISCL_D,
        "What to do for grade III chilblain?",
        "Blisters, ulceration, or necrosis are more severe and need medical wound care and infection prevention; do not puncture on your own." + DISCL_D,
        "Why do some people get it every year?",
        "Poor peripheral circulation, insufficient warming, and high humidity predispose to recurrence; strengthening acral warming and dryness and moderate activity to improve circulation reduce recurrence." + DISCL_D,
        "About the Chilblain (Grading) and Warming Guide",
        "Chilblain (Grading) and Warming Guide. A professional medical tool based on authoritative medical standards, for reference only.",
        "How to Use the Chilblain (Grading) and Warming Guide",
        "Used for degree judgment and warming-care guidance of acral chilblains on fingers, toes, and auricles after cold exposure, helping identify ulceration/necrosis that needs consultation.",
        "What does the Chilblain (Grading) and Warming Guide do?",
        "How to use the Chilblain (Grading) and Warming Guide?",
        "Which scenarios suit the Chilblain (Grading) and Warming Guide?",
    ]))

if __name__ == '__main__':
    main()

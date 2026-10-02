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
    write('dermatoscopy-abcd', build('dermatoscopy-abcd', [
        "\u26A1 Dermoscopy (ABCD Rule) Melanoma Screener",
        "Calculate the total dermoscopy score (TDS) by the dermoscopy ABCD rule to screen melanoma risk. TDS > 5.45 suggests possible melanoma and biopsy is needed for confirmation.",
        "Asymmetry",
        "Asymmetry - 0/1/2 points × 1.3",
        "0 points",
        "Completely symmetric",
        "1 point",
        "Asymmetric on one axis",
        "2 points",
        "Asymmetric on two axes",
        "Border",
        "Border - 0-8 points × 0.1",
        "Count the quadrants (0-8) where the border abruptly stops",
        "Number of border-interrupted quadrants",
        "Color",
        "Color - number of colors × 0.5",
        "Check the colors present in the lesion (up to 6)",
        "Light brown",
        "Dark brown",
        "Black",
        "Red",
        "White",
        "Blue-gray",
        "Dermoscopic structures",
        "Differential structures - number of structures × 0.5",
        "Check the dermoscopic structures present (up to 5)",
        "Reticular structure",
        "Homogeneous structure",
        "Dots / globules",
        "Streaks / radial streaming",
        "Blue-white veil",
        "Calculate TDS score",
        "TDS score criteria",
        "TDS score",
        "Likely benign, regular follow-up",
        "Suggest excisional biopsy or close follow-up",
        "Strongly suggests melanoma, excisional biopsy mandatory",
        "TDS = (A\u00d71.3) + (B\u00d70.1) + (C\u00d70.5) + (D\u00d70.5). A is the asymmetry score (0/1/2), B is the number of border-interrupted quadrants (0-8), C is the number of colors (1-6), D is the number of dermoscopic structures (1-5).",
        "Important reminder:",
        "The ABCD rule applies to assessing melanoma risk of pigmented lesions but not to: 1. facial lentiginous nevus (HLA type); 2. acral melanoma (use the 3-step rule); 3. nodular melanoma (often false-negative); 4. amelanotic melanoma. Blue-white veil, atypical vascular pattern, and regression structures are independent high-risk signs of melanoma, warranting vigilance regardless of TDS.",
        "\U0001F4DA Deep Dive: Dermoscopy (ABCD Rule) Melanoma Screener",
        "Four-dimension entry: enter the lesion's asymmetry, border definition, number of colors (blue/gray/black/brown/red/white), and maximum diameter / structural disarray; the tool scores by ABCD weighting.",
        "Risk stratification: by total score, distinguish low-risk (suggest follow-up) from high-risk (prompt biopsy), helping identify lesions needing further dermatologic management.",
        "Follow-up comparison: regularly score new or changing nevi, flag a rising total score, and prompt early consultation rather than watchful waiting.",
        "Example: a lesion that is clearly asymmetric, has irregular borders, contains 4 colors, and is 8 mm in maximum diameter \u2192 high ABCD score; the tool flags 'high risk, suggest prompt dermoscopy review and biopsy'.",
        "Does a high score necessarily mean melanoma?",
        "No. ABCD is a screening tool; a high score only indicates higher risk and needs professional dermoscopy and biopsy; the final diagnosis rests on pathology." + DISCL_D,
        "Which nevi need special attention?",
        "Pigmented nevi that rapidly enlarge, change color, have blurred borders, exceed 6 mm, or itch/bleed should be seen early." + DISCL_D,
        "Should ordinary nevi also be measured?",
        "Stable ordinary nevi of many years usually only need observation; watching the 'ABCDEF' changes (asymmetry/border/color/diameter/evolution/elevation) is more meaningful." + DISCL_D,
        "About the Dermoscopy (ABCD Rule) Melanoma Screener",
        "Dermoscopy (ABCD Rule) Melanoma Screener. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))
    write('easi-eczema', build('easi-eczema', [
        "\U0001F4D0 Eczema (EASI) Area and Severity Assessor",
        "Based on the EASI (Eczema Area and Severity Index) standard, score the four severity items and area of four body regions to assess atopic dermatitis / eczema severity.",
        "EASI = 0.1\u00d7(E+I+Ex+L)\u00d7A head/neck + 0.2\u00d7...\u00d7A upper limbs + 0.3\u00d7...\u00d7A trunk + 0.4\u00d7...\u00d7A lower limbs",
        "Patient age group (affects head/neck weight)",
        "Adult / adolescent (\u22658 yr)",
        "Child (<8 yr)",
        "Adult weights: head/neck 0.1 / upper limbs 0.2 / trunk 0.3 / lower limbs 0.4; child weights: head/neck 0.2 / upper limbs 0.2 / trunk 0.3 / lower limbs 0.3",
        "Head and neck",
        "Weight 0.1",
        "Papules / induration",
        "Upper limbs",
        "Weight 0.2",
        "Trunk",
        "Weight 0.3",
        "Lower limbs",
        "Weight 0.4",
        "Calculate EASI",
        "EASI severity grading",
        "EASI score",
        "No lesions",
        "Mainly topical treatment",
        "Needs systemic intervention or phototherapy",
        "Systemic treatment, consider biologics",
        ". Severity each item 0-3, area 0-6, full score 72.",
        "\U0001F4DA Deep Dive: Eczema (EASI) Area and Severity Assessment",
        "Four-region assessment: enter each region's affected area (grade 0-6) and four severity items (each 0-4); the tool weights and sums EASI with head/neck 0.1, upper limbs 0.2, trunk 0.3, lower limbs 0.4.",
        "Efficacy comparison: do an EASI before and after treatment; the difference and drop directly reflect improvement in inflammation and scratching, aiding follow-up.",
        "Key-region identification: output each region's score to locate the worst area (e.g., lichenified shins), guiding topical potency and moisturizing focus.",
        "Example: upper limbs area grade 3 with all severities 2, lower limbs area grade 4 with all severities 3 \u2192 the tool weights to EASI ~20+, moderate-severe, suggesting intensified topical therapy and moisturizing.",
        "Does a higher EASI mean more severe?",
        "Yes, a higher EASI means greater affected area and inflammation (~0-72), commonly used in research and follow-up comparison; daily care still rests on itch and quality of life." + DISCL_D,
        "Why is the head/neck weight lowest?",
        "EASI weights by body region",
        "body surface area",
        "proportion (head/neck smallest, lower limbs largest), so the score better reflects actual involvement." + DISCL_D,
        "Can children use it?",
        "The same standard can be used, but children have thin skin and are prone to relapse, so assessment must combine age and care, following pediatric / dermatology advice." + DISCL_D,
        "About the Eczema (EASI) Area and Severity Assessor",
        "Eczema (EASI) Area and Severity Assessor. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))
    write('gags-acne', build('gags-acne', [
        "\U0001F9F4 Acne (GAGS) Grading Tool",
        "Based on the GAGS (Global Acne Grading System) standard, score the most severe lesion in 6 regions and combine regional factors to compute global acne severity.",
        "GAGS = \u03a3(most severe lesion score per region \u00d7 regional factor)",
        "Most severe lesion type per region",
        "Forehead",
        "Factor 2",
        "0 - no lesion",
        "1 - comedones",
        "2 - papules",
        "3 - pustules",
        "4 - nodules",
        "Right cheek",
        "Left cheek",
        "Nose",
        "Factor 1",
        "Jaw",
        "Chest",
        "Upper back",
        "Calculate GAGS",
        "GAGS grading criteria",
        "GAGS score",
        "Topical retinoids, benzoyl peroxide",
        "Topical combination + oral antibiotics",
        "Oral isotretinoin, consider combination therapy",
        "Oral isotretinoin, dermatology specialist",
        "GAGS = \u03a3(most severe lesion score per region \u00d7 regional factor). Regional factors: forehead / both cheeks / chest / upper back = 2, nose / jaw = 1. Lesion scores: 0 none, 1 comedone, 2 papule, 3 pustule, 4 nodule. Maximum 48.",
        "\U0001F4DA Deep Dive: Acne (GAGS) Grading Tool",
        "Regional counting: enter the counts of comedones, papules, pustules, and nodulocysts per body region and weight by the most severe lesion type there (comedone 1, papule 2, pustule 3, nodule 4); the tool weights and sums.",
        "Severity stratification: by total score, mild (1-18), moderate (19-30), severe (31-38), very severe (>38), helping choose topical or oral medication paths.",
        "Efficacy follow-up: re-score before and after treatment and watch whether the nodule/cyst weighted items fall, to judge if systemic therapy works.",
        "Example: lower-face 8 papules (weight 2) + 2 nodules (weight 4), anterior chest 5 pustules (weight 3) \u2192 the tool computes the total GAGS and judges it moderate-severe, suggesting topical plus oral when needed.",
        "How does GAGS differ from ordinary grading?",
        "GAGS counts by region and weights the most severe lesion, more quantitative than a simple 'mild/moderate/severe', and easier for before-after comparison and typing." + DISCL_D,
        "Why do nodules/cysts have high weight?",
        "Nodules/cysts easily scar and indicate moderate-severe disease; their high weight makes them influence the total more, prompting active intervention." + DISCL_D,
        "Is self-assessment error large?",
        "Counting and typing need some experience; self-test is only a trend reference; obvious acne or high scarring risk should see a dermatologist in person." + DISCL_D,
        "About the Acne (GAGS) Grading Tool",
        "Acne (GAGS) Grading Tool. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))

if __name__ == '__main__':
    main()

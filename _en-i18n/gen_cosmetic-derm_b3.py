#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cosmetic-derm 第3批：fitzpatrick-wrinkle / formula-1 / glogau-photoaging / injection"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'cosmetic-derm')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'cosmetic-derm')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        for i, it in enumerate(items):
            print('   ', i, repr((it.get('zh') or it.get('zh_src', ''))[:50]))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    return mp


def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'cosmetic-derm', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))


# ---------------- fitzpatrick-wrinkle (54) ----------------
write('fitzpatrick-wrinkle', build('fitzpatrick-wrinkle', [
    "\U0001F4CB Facial Wrinkle (Fitzpatrick) Elasticity Assessor",
    "Based on the Fitzpatrick wrinkle grading and skin-elasticity assessment, comprehensively judge facial aging degree and give treatment advice.",
    "Facial Wrinkle Elasticity Assessor",
    "/ Facial Wrinkle Elasticity Assessor",
    '\U0001F4D6 View the "Facial Wrinkle (Fitzpatrick) Elasticity Assessor User Guide"',
    "1. Skin Phototype (Fitzpatrick Phototype)",
    "Type I \u2014 always burns, never tans (pale / very fair skin)",
    "Type II \u2014 usually burns, rarely tans (fair skin)",
    "Type III \u2014 sometimes burns, gradually tans (medium skin)",
    "Type IV \u2014 rarely burns, tans easily (light brown skin)",
    "Type V \u2014 very rarely burns, dark brown skin",
    "Type VI \u2014 never burns, deeply pigmented black skin",
    "2. Wrinkle Grading (Fitzpatrick Wrinkle Class)",
    "Static wrinkle grade",
    "Grade I \u2014 fine lines, superficial, visible only when smiling",
    "Grade II \u2014 moderate wrinkles, faint lines visible at rest",
    "Grade III \u2014 deep wrinkles, clearly visible at rest",
    "Grade IV \u2014 very deep wrinkles with redundant skin laxity",
    "Elastosis degree",
    "1 \u2014 mild (fine texture)",
    "2 \u2014 moderate (coarser texture, slight yellowing)",
    "3 \u2014 marked (coarse deep texture, yellow papules)",
    "4 \u2014 severe (thick leathery, nodular)",
    "Facial laxity (0\u201310)",
    "Pigmented area (%)",
    "\U0001F4CB Fitzpatrick Wrinkle Grading Reference",
    "Wrinkle feature",
    "Elastosis",
    "Common age range",
    "Fine lines, appear with expression",
    "None or slight",
    "20\u201335 years",
    "Faint lines visible at rest",
    "Mild\u2013moderate",
    "35\u201350 years",
    "Deep lines clearly visible at rest",
    "50\u201365 years",
    "Very deep wrinkles with laxity",
    "65 years and above",
    "\u26A0\uFE0F This tool is based on the Fitzpatrick wrinkle grading standard and is for aesthetic assessment reference only; it does not constitute medical advice. For a specific plan, consult a licensed physician.",
    "\U0001F4DA Deep Dive: Facial Wrinkle (Fitzpatrick) Elasticity Assessor",
    "Anti-aging stratification: good rebound and mainly dynamic wrinkles \u2192 prioritize botulinum toxin; poor rebound and many static wrinkles \u2192 prioritize RF / collagen stimulation.",
    "Pre-procedure assessment: judge whether skin laxity reaches the threshold for thread lift / surgery.",
    "Education: help clients understand that 'dynamic and static wrinkles need different treatments'.",
    "Forehead pinch-pull test",
    "Input: Pinched skin springs back within 2 seconds of release, faint lines at rest \u2192 judged as fair elasticity, mainly dynamic wrinkles; suggest botulinum toxin + retinol.",
    "Does slow pinch-rebound mean aging?",
    "It is one factor, but also affected by dehydration and sun exposure; a single test is not diagnostic.",
    "What is the difference between dynamic and static wrinkles?",
    "Appearing only with expression is dynamic; present at rest is static; the latter often needs more active intervention.",
    "Can the result determine the treatment?",
    "No. It is only an initial stratification; energy parameters are set by a physician with imaging.",
    'About "Facial Wrinkle Elasticity Assessor"',
    "Facial wrinkle (Fitzpatrick) elasticity assessor: assess facial wrinkle grade and skin elasticity online, providing Fitzpatrick wrinkle grading and photo-aging advice. A medical professional tool based on authoritative medical standards; for reference only.",
]))

# ---------------- formula-1 (36) ----------------
write('formula-1', build('formula-1', [
    "\U0001F3CB\uFE0F Mesotherapy Formula Calculator",
    "Enter the target total volume and each component's ratio to calculate the volume of each component in the mesotherapy injection formula.",
    "Mesotherapy Formula",
    "/ Mesotherapy Formula",
    '\U0001F4D6 View the "Mesotherapy Formula Calculator User Guide"',
    "Adjusted ratio = each component ratio / total ratio; volume = total \u00d7 adjusted ratio; content = volume \u00d7 concentration",
    "When the total ratio deviates from 100% (\u00b10.5% tolerance), it is proportionally adjusted to 100% with a warning. Component content: hyaluronic acid = volume \u00d7 input concentration (mg/ml), vitamin C = volume \u00d7 input concentration (mg/ml), peptides / coenzymes estimated at 2 mg/ml. Outputs each component's volume, adjusted ratio, concentration and content plus the total, for ratio conversion and dosing calculation of meso / mesodermal formulas (e.g. HA+VC+peptide).",
    "Hyaluronic acid (mg/ml)",
    "Vitamin C (mg/ml)",
    "Coenzyme / peptide ratio (%)",
    "\U0001F4A1 Each component volume = total \u00d7 ratio%; the total ratio is recommended to sum to 100%, otherwise it is proportionally adjusted.",
    "Mesotherapy is a medical procedure; the formula must be designed and performed by a licensed physician.",
    "\U0001F4DA Deep Dive: Mesotherapy Formula Calculator",
    "Formula check: convert 'XX mg/mL \u00d7 Y mL' into the actual amount added to avoid manual errors.",
    "Dilution calculation: for a high-concentration stock, back-calculate how much base solution to add from the target concentration.",
    "Cost estimate: roughly calculate the single-formula cost from each component's amount and unit price.",
    "Hydration-formula back-calculation",
    "Input: Target hyaluronic acid 1.5% in 5 mL, stock 2% \u2192 take 3.75 mL stock plus 1.25 mL base, with a note to prepare fresh and use immediately.",
    "Can I prepare it myself once calculated?",
    "Not advised. Mesotherapy is a medical procedure; the formula and sterility are handled by qualified personnel in a clinic.",
    "Is higher concentration better?",
    "No. Too high easily irritates or clumps; prepare per the product instructions and safety window.",
    "Does this tool give medical orders?",
    "No. It is only an arithmetic reference for ratios; defer specific components and contraindications to a physician.",
    'About "Mesotherapy Formula"',
    "Mesotherapy formula calculator: based on the target total volume and each component's concentration/ratio (hyaluronic acid, vitamin C, peptides), it calculates each component's volume and actual content.",
    "Multi-component ratio calculation",
    "Mesotherapy formula design",
    "Hydration injection ratio reference",
    "Skin-nutrition formula research",
    "Total formula volume",
    "Hyaluronic acid concentration",
    "Vitamin C concentration",
    "Hyaluronic acid ratio",
    "Vitamin C ratio",
    "Peptide ratio",
]))

# ---------------- glogau-photoaging (54) ----------------
write('glogau-photoaging', build('glogau-photoaging', [
    "\u2728 Photo-aging (Glogau) Classifier",
    "Based on the Glogau photo-aging classification, judge the photo-aging grade through indicators such as wrinkles, pigmentation and keratosis.",
    "Photo-aging Glogau Classifier",
    "/ Photo-aging Glogau Classifier",
    '\U0001F4D6 View the "Photo-aging (Glogau) Classifier User Guide"',
    "Glogau photo-aging grading: composite score = (wrinkles\u00d73 + pigment\u00d72 + keratosis\u00d71.5 + makeup\u00d72 + age\u00d71.5) \u00f7 10; <1.5 Type I, 1.5\u20132.5 Type II, 2.5\u20133.5 Type III, >3.5 Type IV.",
    "Please select according to the actual situation",
    "Wrinkles at rest (no expression)",
    "No wrinkles",
    "Few fine lines (appear with movement)",
    "Early-to-moderate wrinkles at rest",
    "Many deep wrinkles at rest",
    "Pigmentation / freckles",
    "Mild (few light spots)",
    "Obvious (most light spots + some deep spots)",
    "Severe (many deep dark spots)",
    "Keratosis (actinic)",
    "None visible but palpable",
    "Few visible",
    "Many clearly visible",
    "Need makeup coverage?",
    "Little coverage suffices",
    "Needs more coverage",
    "Hard to fully cover",
    "60s or above",
    "Type I\u2013II (fair, burns easily)",
    "Type V\u2013VI (dark skin)",
    "\U0001F4CB Glogau Photo-aging Classification Standard",
    "Typical age",
    "Type I: no wrinkles",
    "Early photo-aging",
    "Slight pigmentation, no keratosis, no wrinkles",
    "Type II: wrinkles with movement",
    "Early\u2013moderate",
    "Early freckles, palpable keratosis, fine lines when smiling",
    "Type III: wrinkles at rest",
    "Obvious pigmentation, visible keratosis, wrinkles at rest",
    "Type IV: wrinkles only",
    "Yellow-gray skin, much keratosis, dense wrinkles",
    "\u26A0\uFE0F The Glogau classification is used to assess photo-aging degree and guide treatment-intensity choice. Results are for reference only; for a specific plan consult a dermatologist.",
    "\U0001F4DA Deep Dive: Photo-aging (Glogau) Classifier",
    "Standardized clinic records: chains use a unified scale to record client baselines, easing cross-branch follow-up comparison.",
    "Treatment communication: translate the abstract 'skin has aged' into a concrete grade so clients understand why combination therapy is needed.",
    "Education: tell the public that photo-aging is a gradable, intervenable process, not a sudden 'overnight aging'.",
    "Mixed photo-aging self-assessment",
    "Input: Cheek patchy spots, nasal ala telangiectasia, forehead static fine lines, dorsum-hand skin thinning \u2192 comprehensively graded Glogau Type III; suggest sun protection + light-based therapy + retinol combined.",
    "What is the difference between Glogau and the Fitzpatrick skin type?",
    "Fitzpatrick looks at tanning / burning response (skin-color risk); Glogau looks at existing photo-aging degree; the two are complementary, not substitutes.",
    "Is the result suitable for setting the plan directly?",
    "Not suitable. Grading only reflects degree; specific energy parameters and products must be adjusted by a physician per individual.",
    "Will grading be affected by makeup?",
    "Yes. Assess bare-faced under natural light against standard photos; wearing makeup or strong light causes misjudgment.",
    'About "Photo-aging Glogau Classifier"',
    "Photo-aging (Glogau) classifier: assess skin photo-aging degree online, providing Glogau photo-aging classification and treatment advice. A medical professional tool based on authoritative medical standards; for reference only.",
]))

# ---------------- injection (32) ----------------
write('injection', build('injection', [
    "\U0001F504 Aesthetic Injection Unit Calculator",
    "Select injection type, area and target effect to calculate the recommended dosage of botulinum toxin / hyaluronic acid.",
    "Aesthetic Injection Unit",
    "/ Aesthetic Injection Unit",
    '\U0001F4D6 View the "Aesthetic Injection Unit Calculator User Guide"',
    "Injection type",
    "Botulinum toxin (botulinum toxin type A)",
    "Hyaluronic acid (hyaluronic acid filler)",
    "Mild improvement",
    "Moderate improvement",
    "Strong improvement",
    "\U0001F4A1 Botulinum toxin is measured in units (U), hyaluronic acid in volume (ml). Dosage varies with individual differences, muscle strength and product brand.",
    "Injection is a medical procedure; the dosage is for reference only and must be performed after assessment by a licensed physician.",
    "\U0001F4DA Deep Dive: Aesthetic Injection Unit Calculator",
    "Consultant education: use a range, not a fixed value, to explain to clients 'why others get 20 U but you get 30 U'.",
    "Repurchase records: log the actual dosage each time and track your stable range long-term to ease follow-up communication.",
    "Pitfall education: warn that a 'flat per-area package price' may hide over-dosing or dilution risk.",
    "Masseter HA / botulinum distinction",
    "Input: Masseter hypertrophy wanting a slimmer face \u2192 usually choose botulinum toxin dosed per side, not hyaluronic acid; this tool reminds you not to confuse the materials.",
    "Why do some people need more and some less at the same site?",
    "Muscle volume, expression intensity and prior dosage all differ; a physician must individualize.",
    "What are the consequences of calculating too many units?",
    "Excess botulinum toxin can cause frozen expression and drooping; excess HA can cause displacement and swelling \u2014 seek medical care promptly in both cases.",
    "Can this result serve as medical basis?",
    "No. It is only a reference range; the final word is the licensed physician's diagnosis and prescription.",
    'About "Aesthetic Injection Unit"',
    "Aesthetic injection unit calculator: based on injection type (botulinum toxin / HA), area and target effect, it recommends reference dosage and injection-point suggestions.",
    "Botulinum toxin / HA dual mode",
    "Multi-site dosage reference",
    "Three-tier effect grading",
    "Injection-point suggestions",
    "Injection dosage estimate",
]))

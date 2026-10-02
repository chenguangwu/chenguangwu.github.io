#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'endocrinology')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'endocrinology')
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
    out = {'slug': slug, 'industry': 'endocrinology', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
#!/usr/bin/env python3

def main():
    write('aldosterone-renin', build('aldosterone-renin', [
        "\U0001F918 Aldosterone/Renin (ARR) Ratio Calculator",
        "Compute the aldosterone/renin ratio (ARR) to screen for primary aldosteronism and guide the confirmatory test",
        "Core formulas (by input): min(100, (arr \u00F7 barMax) \u00D7 100); aldo \u00F7 (renin \u00D7 1)",
        "\U0001F4D6 See the \"Aldosterone/Renin (ARR) Ratio Calculator User Guide\"",
        "Aldosterone (ng/dL)",
        "Renin unit",
        "Plasma renin activity PRA (ng/mL/h)",
        "Direct renin concentration DRC (mU/L)",
        "Renin value",
        "Blood draw position",
        "Upright",
        "Supine",
        "Serum potassium (mmol/L)",
        "Calculate ARR",
        "Primary aldosteronism example",
        "ARR screening thresholds and interpretation",
        "Does not support primary aldosteronism",
        "Grey zone",
        "Combine with the absolute aldosterone value and repeat if needed",
        "A confirmatory test is advised (such as saline infusion)",
        "Over 50 with aldosterone \u226515",
        "Strongly suspect primary aldosteronism, confirmatory testing and subtyping needed",
        "Note: when direct renin concentration (DRC) is used, the threshold = aldosterone (ng/dL) \u00F7 DRC (mU/L), with a positive threshold around 3.7-5.7.",
        "Indications for screening",
        "\u2022 Spontaneous or diuretic-induced hypokalaemia",
        "\u2022 Resistant hypertension (uncontrolled on 3 or more drugs)",
        "\u2022 Hypertension with an adrenal incidentaloma",
        "\u2022 Early-onset hypertension or a family history of stroke (under 40)",
        "\u2022 Hypertension with sleep apnoea",
        "Preparation before testing:",
        "Stop drugs that affect ARR for at least 2-4 weeks. Spironolactone, amiloride and diuretics need 6 weeks; beta-blockers falsely raise ARR (they suppress renin) while ACEI/ARB falsely lower it (they raise renin). Verapamil sustained-release plus an alpha-blocker can be used as a bridge. Correct hypokalaemia first.",
        "\U0001F4DA In-depth analysis: Aldosterone/Renin (ARR) Ratio Calculator",
        "Screening for primary aldosteronism in resistant hypertension with hypokalaemia.",
        "Functional assessment of an adrenal incidentaloma with hypertension.",
        "Cause screening in young hypertension or with a family history of early cerebrovascular events.",
        "ARR calculation example",
        "Plasma aldosterone 200 pg/mL and renin 1.0 ng/mL/h give ARR=200 (common cut-offs are over 30-50, depending on units and reagent). A raised ratio suggests primary aldosteronism; stop interfering drugs and confirm with a saline loading or captopril test.",
        "Which drugs interfere with ARR?",
        "ACEI/ARB, diuretics, beta-blockers, NSAIDs and licorice preparations can markedly change aldosterone/renin, and screening usually requires stopping them for 2-4 weeks as advised by your doctor.",
        "Does a positive ARR mean it is definitely primary aldosteronism?",
        "ARR is a screening test, not a diagnosis. It needs a confirmatory test (saline, captopril or oral sodium loading) plus imaging; older people and renovascular hypertension can also give false positives.",
        "About \"Aldosterone/Renin (ARR) Ratio Calculator\"",
        "ARR (aldosterone to renin ratio) is the first-line screening index for primary aldosteronism; this tool computes the ratio and gives screening threshold interpretation and confirmation advice.",
        "Supports both PRA and DRC units",
        "Upright and supine modes",
        "Assessed together with potassium",
        "Confirmatory test decision advice",
        "Primary aldosteronism screening",
        "Resistant hypertension assessment",
        "Differential diagnosis of hypokalaemia",
        "Adrenal disease workup",
    ]))

    write('cortisol-rhythm', build('cortisol-rhythm', [
        "\U0001F4CB Cortisol Diurnal Rhythm Reference Assessor",
        "Enter serum cortisol at different time points to assess whether the circadian rhythm is normal, supporting Cushing syndrome screening",
        "Core formulas (by input): (m16 \u00F7 m8) \u00D7 100; (m0 \u00F7 m8) \u00D7 100",
        "\U0001F4D6 See the \"Cortisol Diurnal Rhythm Reference Assessor User Guide\"",
        "Cortisol at 8:00 (nmol/L)",
        "Cortisol at 16:00 (nmol/L)",
        "Midnight cortisol at 0:00 (nmol/L)",
        "Sampling condition",
        "Blood draw while awake",
        "Indwelling cannula during sleep",
        "Assess the rhythm",
        "Cushing example",
        "Reference values for serum cortisol diurnal rhythm",
        "Normal range (nmol/L)",
        "Rhythm characteristic",
        "8:00 (morning)",
        "16:00 (afternoon)",
        "About 50% of the morning value",
        "0:00 (midnight)",
        "Below 140 (awake)",
        "Midnight (sleep, cannula in place)",
        "True nadir",
        "Clinical meaning of an abnormal rhythm",
        "Rhythm pattern",
        "Rhythm lost (midnight \u226550% of morning)",
        "Characteristic of Cushing syndrome",
        "Proceed to DST or midnight salivary cortisol",
        "Low all day with the rhythm present",
        "Check ACTH and the insulin tolerance test",
        "High morning with midnight suppression",
        "Pseudo-Cushing from stress or depression",
        "Distinguish with the 1mg DST",
        "No midnight suppression (awake draw)",
        "Repeat with a sleep indwelling cannula",
        "Sampling during sleep is more accurate",
        "Key points for reading the rhythm:",
        "Normal cortisol follows a circadian rhythm, peaking at 6-8 in the morning and reaching its lowest at midnight. Loss of the rhythm is the earliest and most sensitive abnormality in Cushing syndrome. An awake midnight draw is easily distorted by stress, so an indwelling cannula during sleep is advised. A single abnormal rhythm cannot confirm the diagnosis and must be read together with 24-hour urinary free cortisol, midnight salivary cortisol and the dexamethasone suppression test.",
        "\U0001F4DA In-depth analysis: Cortisol Diurnal Rhythm Reference Assessor",
        "Hypercortisol screening in central obesity with purple striae and hypertension.",
        "Differentiating pseudo-Cushing from depression, alcohol or obesity.",
        "Reading the result of a low-dose dexamethasone suppression test.",
        "Cortisol rhythm example",
        "Morning cortisol at 8:00 is raised while midnight (or salivary) cortisol fails to fall or even rises, and low-dose dexamethasone does not suppress it: this supports Cushing syndrome and needs further localisation (ACTH-dependent versus independent).",
        "Why does the sampling time matter?",
        "Normal cortisol is high in the morning and low at night, and loss of that rhythm is an important clue for Cushing; midnight salivary or serum cortisol is a sensitive first-line screen.",
        "How do I read the dexamethasone suppression test?",
        "Failure to suppress cortisol after a low dose (1mg overnight or 2mg over 48h) suggests Cushing; depression, obesity and drugs can cause false positives, so repeat and combine results.",
        "About \"Cortisol Diurnal Rhythm Reference Assessor\"",
        "Loss of the cortisol diurnal rhythm is the earliest and most sensitive marker of Cushing syndrome. This tool assesses the serum cortisol rhythm and supports screening for adrenal disease.",
        "Three-point rhythm assessment",
        "Awake and sleep sampling modes",
        "Automatic detection of a lost rhythm",
        "Rhythm curve visualisation",
        "Cushing syndrome screening",
        "Adrenal cortex function assessment",
        "Pituitary-adrenal axis testing",
    ]))

    write('ti-rads', build('ti-rads', [
        "\U0001F4CB Thyroid Nodule (TI-RADS) Stratifier",
        "Using the ACR TI-RADS (2017) criteria, score the ultrasound features to stratify thyroid nodule risk and give management advice",
        "\U0001F4D6 See the \"Thyroid Nodule (TI-RADS) Stratifier User Guide\"",
        "ACR TI-RADS (2017) scores five features and adds them up: composition (cystic 0, mixed 1, solid 2) + echogenicity (anechoic 0, hyperechoic or isoechoic 1, hypoechoic 2, very hypoechoic 3) + shape (wider than tall 0, taller than wide 3) + margins (smooth 0, ill-defined 1, lobulated or irregular 2, extrathyroidal extension 3) + echogenic foci (none or large comet-tail 0, coarse calcification 1, peripheral rim calcification 2, punctate echogenic foci 3); a total of 0 is TR1, 2 is TR2, 3 is TR3, 4 to 6 is TR4, and 7 or more is TR5; fine-needle aspiration is advised for TR4 at 1.5cm or larger or TR5 at 1cm or larger, and TR3 and above should be followed up.",
        "1. Nodule composition",
        "Cystic (predominantly cystic)",
        "Spongiform",
        "Mixed (solid + cystic)",
        "Entirely solid",
        "2. Echogenicity",
        "Anechoic (cystic)",
        "Hyperechoic / isoechoic",
        "Hypoechoic",
        "Very hypoechoic",
        "3. Shape",
        "Wider than tall (transverse)",
        "Taller than wide (taller than wide)",
        "4. Margins",
        "Smooth",
        "Ill-defined",
        "Lobulated / irregular",
        "Extrathyroidal extension",
        "5. Echogenic foci",
        "Large comet-tail artefact",
        "Coarse calcification",
        "Rim calcification",
        "Punctate echogenic foci (microcalcification)",
        "ACR TI-RADS scoring and management standard",
        "TR level",
        "No FNA, no follow-up needed",
        "Benign",
        "\u22652.5cm FNA; 1.5-2.5cm follow-up",
        "\u22651.5cm FNA; 1-1.5cm follow-up",
        "\u22651.0cm FNA; \u22650.5cm consider follow-up",
        "Cautions:",
        "TI-RADS is a risk assessment system and does not replace pathological diagnosis. FNA (fine-needle aspiration biopsy) is the confirmatory gold standard. The follow-up interval is usually 6-12 months, shortened to 3-6 months for high-risk nodules.",
        "\U0001F4DA In-depth analysis: Thyroid Nodule (TI-RADS) Stratifier",
        "Structured scoring of a thyroid nodule ultrasound report.",
        "Judging FNA indications against nodule size thresholds.",
        "Setting follow-up intervals and imaging review plans.",
        "ACR TI-RADS scoring example",
        "Composition 2 + echogenicity 2 + shape 3 (taller than wide) + margins 2 + echogenic foci 2 gives 11 points \u2192 TR 5 (highly suspicious). FNA is advised for a nodule of 1.5 cm or more.",
        "How does ACR TI-RADS compare with other versions?",
        "ACR uses a five-feature additive score while ATA and MACIS each have their own emphasis; this tool scores by ACR, and clinically you should follow whichever standard your hospital uses.",
        "What does each score mean for management?",
        "TR 3 mostly needs follow-up, TR 4 is aspirated depending on size (\u22651.5 cm) and TR 5 is aspirated even when small (\u22651 cm); very low-risk nodules (purely cystic or spongiform) can be followed up alone.",
        "About \"Thyroid Nodule (TI-RADS) Stratifier\"",
        "Based on the ACR TI-RADS (2017) Thyroid Imaging Reporting and Data System, ultrasound features are scored to stratify nodule risk and support management decisions.",
        "All five ultrasound features scored",
        "TI-RADS level computed automatically",
        "FNA and follow-up indications given",
        "Matches the ACR standard",
        "Reading thyroid ultrasound reports",
        "Nodule management planning",
        "Endocrinology clinic reference",
        "Ultrasound teaching",
    ]))


if __name__ == '__main__':
    main()

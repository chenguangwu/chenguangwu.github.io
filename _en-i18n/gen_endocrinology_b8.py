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
    write('cycle-hormone', build('cycle-hormone', [
        "\u2697\uFE0F Sex Hormones (LH/FSH/E2/T) Cycle Interpretation",
        "Enter the six sex hormone results and the day of the menstrual cycle to match reference ranges automatically and interpret them",
        "\"Enter the six sex hormone results and the day of the menstrual cycle to match reference ranges automatically and interpret them\" is computed from the input parameters and the result is reported.",
        "\U0001F4D6 See the \"Sex Hormones (LH/FSH/E2/T) Cycle Interpretation User Guide\"",
        "Test date",
        "Reproductive age (18-40 years)",
        "Perimenopause (40-55 years)",
        "Hormone results",
        "FSH follicle stimulating hormone (mIU/mL)",
        "T testosterone (ng/mL)",
        "PRL prolactin (ng/mL)",
        "\U0001F50D Start interpreting",
        "Past test records",
        "\U0001F4CB Reference notes for the six sex hormones",
        "Basal values (cycle day 2-5)",
        "is the key moment for assessing ovarian function:",
        ": basal 3.5-12.5 mIU/mL, over 10 suggests reduced ovarian reserve, over 25 suggests perimenopause, over 40 suggests menopause",
        ": basal 2.4-12.6 mIU/mL, an LH/FSH ratio over 2-3 suggests possible polycystic ovary syndrome (PCOS)",
        ": basal 20-50 pg/mL, a high basal value (over 80) suggests reduced ovarian reserve",
        ": 0.29-1.67 ng/mL, a raised level indicates hyperandrogenism, common in PCOS",
        ": 3.5-23.3 ng/mL, over 25 indicates hyperprolactinaemia and a pituitary tumour should be excluded",
        ": follicular phase under 1.5 ng/mL, luteal phase 3.3-25.6 ng/mL, mid-luteal over 3 indicates ovulation",
        "This tool is for reference only and does not replace professional medical diagnosis; follow your doctor's interpretation.",
        "Assay methods and units vary between laboratories, so use the reference range printed on your report.",
        "Basal endocrine testing is best done on cycle day 2-5 with a fasting morning blood draw.",
        "Hormone levels must be judged together with the clinical picture and ultrasound.",
        "\U0001F4DA In-depth analysis: Sex Hormones (LH/FSH/E2/T) Cycle Interpretation",
        "Locating the follicular or luteal phase from the cycle day and matching the reference range.",
        "Monitoring the ovulatory window (the LH peak and E2 change) to guide conception attempts.",
        "Recognising hormonal cycle patterns in people with irregular periods.",
        "Cycle matching example",
        "Cycle day 12: LH peaks, E2 rises and progesterone stays low \u2192 judged as",
        "ovulation",
        "; on cycle day 22 progesterone over 5 ng/mL with LH falling back \u2192 ovulation has occurred (luteal phase). The system matches the reference range for that stage and flags values as high or low.",
        "Why match the reference range by cycle day?",
        "Sex hormones change sharply as the follicle develops, so the same number means different things in the follicular and luteal phases; only stage-matched ranges are accurate.",
        "What if the cycle is irregular?",
        "With an irregular cycle a single hormone value cannot locate the stage reliably, so vaginal ultrasound tracking of follicles and endometrium, or assessment over several cycles, is better.",
        "About \"Sex Hormones (LH/FSH/E2/T) Cycle Interpretation\"",
        "Enter the six sex hormone results (FSH, LH, E2, T, PRL and P) with the cycle day to match the reference range for that stage automatically, compute the LH/FSH ratio and recognise common patterns such as polycystic ovary syndrome (PCOS), diminished ovarian reserve (DOR) and premature ovarian insufficiency (POI).",
        "All six hormones interpreted one by one",
        "Automatic cycle phase matching",
        "LH/FSH ratio calculation",
        "Common pattern recognition",
        "Past results saved",
        "First-line infertility screening",
        "Supporting PCOS judgement",
        "Ovarian reserve assessment",
        "Hormonal analysis of abnormal periods",
        "e.g. 6.5",
        "e.g. 4.2",
        "e.g. 35",
        "e.g. 0.5",
        "e.g. 15",
    ]))

    write('sex-hormone-cycle', build('sex-hormone-cycle', [
        "\U0001F3CB\uFE0F Sex Hormones (LH/FSH/E2/T) Cycle Interpreter",
        "Enter the six sex hormone results with the cycle phase to interpret hypothalamic-pituitary-gonadal axis function",
        "\"Enter the six sex hormone results with the cycle phase to interpret hypothalamic-pituitary-gonadal axis function\" is computed from the input parameters and the result is reported.",
        "\U0001F4D6 See the \"Sex Hormones (LH/FSH/E2/T) Cycle Interpreter User Guide\"",
        "Menstrual cycle phase",
        "Follicular phase (day 2-5, basal)",
        "Ovulatory phase (day 13-15)",
        "Luteal phase (day 21-23)",
        "FSH follicle stimulating hormone (mIU/mL)",
        "T testosterone (ng/dL)",
        "PRL prolactin (ng/mL)",
        "Premature ovarian failure example",
        "PCOS example",
        "Female sex hormone reference ranges (by cycle phase)",
        "Hormone",
        "Follicular phase",
        "Ovulatory phase",
        "Luteal phase",
        "8-60 (total testosterone in women)",
        "3.4-24.1 (non-pregnant)",
        "Male sex hormone reference ranges",
        "280-1100 (total testosterone, falling with age)",
        "Key reading points:",
        "Basal values should be measured on cycle day 2-5. FSH over 25 suggests diminished ovarian reserve (DOR); FSH over 40 with low E2 indicates premature ovarian failure (POF). An LH/FSH ratio of 2-3 or more with raised T suggests PCOS. A raised prolactin needs repeating after excluding stress and drug effects, and a persistent level over 100 calls for a pituitary MRI. Low T with raised LH/FSH in men indicates primary hypogonadism.",
        "\U0001F4DA In-depth analysis: Sex Hormones (LH/FSH/E2/T) Cycle Interpreter",
        "Assessing ovulatory function and ovarian reserve at a first infertility visit.",
        "Cycle comparison of follicular versus luteal hormone levels.",
        "Reading hormones in polycystic ovary and ovulation monitoring.",
        "Cycle hormone reading example",
        "Cycle day 22: progesterone P over 5 ng/mL, moderate E2 and LH already falling \u2192 suggests ovulation has occurred (luteal phase); if P stays under 3 with no rise, this suggests anovulation. FSH and E2 together give a first idea of ovarian reserve.",
        "When should the six sex hormones be tested?",
        "Basal ovarian function is usually assessed on cycle day 2-4 (early follicular); progesterone for ovulation assessment is measured in the mid-luteal phase (day 21-23). Follow your doctor's instructions.",
        "Is the FSH/LH ratio meaningful?",
        "An LH/FSH above 2-3 in the early follicular phase supports a PCOS tendency; raised FSH with low E2 suggests reduced ovarian reserve and needs to be read alongside AMH and age.",
        "About \"Sex Hormones (LH/FSH/E2/T) Cycle Interpretation\"",
        "The six sex hormones are the core indices for assessing hypothalamic-pituitary-gonadal (HPG) axis function, and reading them with the cycle phase is essential for diagnosing reproductive endocrine disorders.",
        "Reference ranges for both sexes",
        "Read by cycle phase",
        "LH/FSH ratio computed automatically",
        "Cause hints such as PCOS and POF",
        "Reading infertility investigations",
        "Menopause assessment",
        "Hypogonadism diagnosis",
    ]))

    write('mage-index', build('mage-index', [
        "\u2697\uFE0F Blood Glucose Variability (MAGE) Index Calculator",
        "Enter continuous glucose monitoring (CGM) data to compute the mean amplitude of glycaemic excursions (MAGE) and assess glycaemic variability quality",
        "\U0001F4D6 See the \"Blood Glucose Variability (MAGE) Index Calculator User Guide\"",
        "Valid excursion threshold (mmol/L)",
        "Glucose unit",
        "CGM glucose data points (in time order)",
        "Calculate MAGE",
        "Enter glucose data and click calculate",
        "Clinical meaning of MAGE:",
        "MAGE is the gold standard index for assessing glycaemic variability. It counts only excursions larger than 1 SD, taking the mean absolute value from every valid peak-to-trough or trough-to-peak, and is not affected by the baseline glucose level.",
        "MAGE assessment bands",
        "Variability level",
        "Small variability, well controlled",
        "Moderate variability, needs attention",
        "Large variability, regimen needs adjusting",
        "1. Compute the mean of all glucose values (MBG) and the standard deviation (SD)",
        "2. Identify the peaks and troughs on the continuous glucose curve",
        "3. Compute the amplitude difference between adjacent peak and trough",
        "4. Keep the valid excursions whose amplitude is above the SD threshold (normally 1 SD)",
        "5. MAGE = arithmetic mean of the absolute amplitudes of all valid excursions",
        "Note: this tool uses a simplified algorithm, taking the highest point of each rising segment as a peak and the lowest point of each falling segment as a trough.",
        "\U0001F4DA In-depth analysis: Blood Glucose Variability (MAGE) Index Calculator",
        "Objective assessment of glycaemic variability (within-day variation) in type 1 diabetes.",
        "Reference for variability management and drug adjustment in patients with fear of hypoglycaemia.",
        "A variability metric in CGM report reading that complements HbA1c and",
        "(SD).",
        "MAGE calculation example",
        "After importing a day of CGM data, first compute the glucose SD, then remove all small excursions whose peak-to-trough difference is under 1 SD and average the rest. This example series gives MAGE\u22483.8 mmol/L, meaning within-day variability is high and basal rates plus extra snacks need optimising.",
        "How do MAGE, HbA1c and SD differ?",
        "HbA1c looks at the long-term mean, SD at overall dispersion, while MAGE specifically characterises meaningful large swings, which relates more closely to the risk of hypo- and hyperglycaemic events.",
        "What data quality is needed?",
        "You need sufficiently dense continuous CGM readings (usually 24-72 hours or more); sparse or discontinuous data underestimates MAGE.",
        "About \"Blood Glucose Variability (MAGE) Index Calculator\"",
        "Mean amplitude of glycaemic excursions (MAGE) is the classic gold standard for assessing glycaemic variability in diabetes, describing the amplitude of swings rather than the average level.",
        "Custom data point input",
        "Automatic peak and trough detection",
        "Computes MBG/SD/CV/LAGE together",
        "Glucose trend visualisation",
        "CGM dynamic glucose data analysis",
        "Diabetes regimen evaluation",
        "Glycaemic variability research",
        "Endocrinology research and teaching",
        "How to use the Blood Glucose Variability (MAGE) Index Calculator",
        "To interpret continuous glucose monitoring (CGM) data and quantify within-day glycaemic variability for type 1 diabetes management and for optimising variability in patients with fear of hypoglycaemia.",
        "What does the Blood Glucose Variability (MAGE) Index Calculator do?",
        "How do I use the Blood Glucose Variability (MAGE) Index Calculator?",
        "Which scenarios suit the Blood Glucose Variability (MAGE) Index Calculator?",
    ]))


if __name__ == '__main__':
    main()

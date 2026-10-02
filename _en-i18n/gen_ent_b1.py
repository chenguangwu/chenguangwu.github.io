#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'ent')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'ent')
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
    out = {'slug': slug, 'industry': 'ent', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

DISCL_M = " A professional medical tool based on authoritative medical standards, for reference only."


def main():
    write('adenoid-grading', build('adenoid-grading', [
        "\U0001F4DA Adenoid Hypertrophy (Nasopharyngoscopy) Grader",
        "Grades adenoid hypertrophy by the proportion of choanal obstruction seen on nasopharyngoscopy, and assesses surgical indications together with clinical symptoms.",
        "Adenoid hypertrophy grading (obstruction ratio on nasopharyngoscopy or a lateral film): grade I up to 25%, grade II 26\u201350%, grade III 51\u201375%, grade IV over 75%; grades III\u2013IV with mouth breathing, snoring or OSAHS call for surgical removal.",
        "Degree of adenoid obstruction (proportion of choanal obstruction under nasopharyngoscopy)",
        "Obstruction \u226425%",
        "Obstruction 26-50%",
        "Obstruction 51-75%",
        "Obstruction >75%",
        "Mouth breathing",
        "Snoring during sleep",
        "Sleep apnoea",
        "Recurrent nasal obstruction / purulent discharge",
        "Otitis media with effusion / hearing loss",
        "Adenoid facies",
        "Adenoid hypertrophy grading and management",
        "Obstruction ratio",
        "Medication with regular review",
        "Consider surgery if medication fails",
        "Surgical removal recommended",
        "Surgical indications:",
        "Adenoidectomy is recommended for grade III\u2013IV hypertrophy with sleep apnoea, recurrent otitis media with effusion, adenoid facies, or failure of medical treatment. Endoscopic power-assisted adenoidectomy under direct vision is currently the preferred technique.",
        "\U0001F4DA In-depth Analysis: Adenoid Hypertrophy (Nasopharyngoscopy) Grader",
        "Children who snore or breathe through the mouth in their sleep can be graded by nasopharyngoscopy for adenoid obstruction.",
        "Assess the cause of adenoid facies (high-arched hard palate).",
        "Judge the degree of obstruction and the extent of surgery before an operation.",
        "Grade III obstruction",
        "Nasopharyngoscopy shows adenoids blocking about 70% of the choanae (grade III, A/N\u22480.75) with night-time snoring and hypoxia, so adenoidectomy is recommended.",
        "How is the A/N ratio calculated?",
        "On a lateral X-ray it is the ratio of adenoid thickness to nasopharyngeal height; a value above 0.7 suggests hypertrophy, and combining it with endoscopy is more accurate.",
        "Which grade needs surgery?",
        "Grades III\u2013IV with sleep apnoea, growth retardation or recurrent otitis media usually call for surgery; grades I\u2013II can be observed.",
        "About \"Adenoid Hypertrophy (Nasopharyngoscopy) Grader\"",
        "Adenoid Hypertrophy (Nasopharyngoscopy) Grader." + DISCL_M,
        "How to use the Adenoid Hypertrophy (Nasopharyngoscopy) Grader",
        "What does the Adenoid Hypertrophy (Nasopharyngoscopy) Grader do?",
        "How do I use the Adenoid Hypertrophy (Nasopharyngoscopy) Grader?",
        "What scenarios is the Adenoid Hypertrophy (Nasopharyngoscopy) Grader suitable for?",
    ]))

    write('ahi-severity', build('ahi-severity', [
        "\U0001FAC1 Sleep Apnoea (AHI) Severity Assessor",
        "Computes the AHI and RDI from polysomnography (PSG) data to assess the severity of obstructive sleep apnoea (OSA).",
        "Core formulas (by input variable): Math.round(totalEvents \u00f7 hours \u00d7 10) \u00f7 10; Math.round(hypopneas \u00f7 hours \u00d7 10) \u00f7 10; Math.round(odCount \u00f7 hours \u00d7 10) \u00f7 10",
        "Number of apnoeas",
        "Number of hypopnoeas",
        "Total sleep time (hours)",
        "Lowest oxygen saturation (%)",
        "Oxygen desaturation events (OD)",
        "Number of micro-arousals",
        "AHI severity grading criteria (AASM)",
        "AHI (events/hour)",
        "No sleep apnoea",
        "Mild snoring, daytime sleepiness not obvious",
        "Obvious snoring, daytime sleepiness, treatment needed",
        "Severe snoring, marked daytime sleepiness, high cardiovascular risk",
        "Hypoxaemia grading",
        "Lowest SpO\u2082",
        "No obvious hypoxaemia",
        "Mild hypoxaemia",
        "Moderate hypoxaemia",
        "Severe hypoxaemia, urgent intervention needed",
        "Treatment recommendations:",
        "For mild to moderate OSA, CPAP or an oral appliance can be the first choice; for severe OSA, CPAP is the first choice; patients with obvious anatomical narrowing may consider surgery (UPPP, nasal expansion and similar). Those with AHI>30 and severe hypoxaemia need active treatment to lower cardiovascular event risk.",
        "\U0001F4DA In-depth Analysis: Sleep Apnoea (AHI) Severity Assessor",
        "Night-time snoring and daytime sleepiness are graded by AHI after a PSG study.",
        "Baseline assessment before CPAP pressure titration.",
        "Follow-up after weight loss or surgery.",
        "Moderate OSA",
        "PSG shows AHI=22 events/hour and LSaO2=88%, which is moderate OSA; CPAP treatment plus lifestyle intervention is recommended.",
        "What is the difference between AHI and RDI?",
        "AHI counts only apnoeas plus hypopnoeas, while RDI adds respiratory-effort-related arousals, so in some people RDI is greater than AHI, although AHI remains the main clinical measure.",
        "How low should the lowest oxygen saturation be before concern?",
        "LSaO2 below 80% is severe hypoxaemia and below 70% is high risk, requiring active intervention such as CPAP or surgery.",
        "About \"Sleep Apnoea (AHI) Severity Assessor\"",
        "Sleep Apnoea (AHI) Severity Assessor." + DISCL_M,
    ]))

    write('allergy-skin-test', build('allergy-skin-test', [
        "\U0001F442 Allergen (Skin Test) Result Interpreter",
        "Semi-quantitative grading of skin prick test (SPT) wheal diameters against the histamine positive control.",
        "Skin prick test: a wheal diameter below 3 mm is negative; an allergen-to-histamine wheal ratio below 0.5 is 1+, 0.5\u20131.0 is 2+, 1.0\u20131.5 is 3+, and 1.5 or above is 4+; positivity strengthens as the ratio rises, and antihistamines must be stopped 3\u20135 days before testing.",
        "Positive control (histamine 10 mg/mL)",
        "Histamine wheal diameter (mm)",
        "Histamine flare diameter (mm)",
        "Allergen reaction",
        "Allergen wheal diameter (mm)",
        "Allergen flare diameter (mm)",
        "Skin prick test grading criteria",
        "Wheal diameter",
        "Compared with the positive control",
        "Negative (-)",
        "<1/3 of control",
        "No allergic reaction",
        "\u22651/3 of control",
        "\u22651/2 of control",
        "Mildly positive",
        "= control",
        "Moderately positive",
        "2\u00d7 control",
        ">2\u00d7 control with pseudopods",
        "Strongly positive",
        "Interpretation notes:",
        "Read the skin prick test result after 15-20 minutes, measuring the longest wheal diameter and the perpendicular diameter and taking the average. Histamine (10 mg/mL) serves as the positive control and saline as the negative control. Grading is semi-quantitative, based on the ratio of the allergen wheal to the histamine wheal. Antihistamines must be stopped for at least 3-5 days before testing.",
        "\U0001F4DA In-depth Analysis: Allergen (Skin Test) Result Interpreter",
        "Screening for inhaled or ingested allergens in patients with allergic rhinitis or asthma.",
        "Identifying the sensitising allergen before immunotherapy (desensitisation).",
        "Investigating the cause of urticaria or eczema.",
        "Dust mite positive",
        "SPT shows a dust mite wheal of 6 mm (negative control 1 mm, so a net 5 mm) against a histamine control of 8 mm, which is read as positive (++), indicating dust mite allergy; allergen avoidance plus desensitisation is recommended.",
        "How large must a wheal be to count as positive?",
        "A wheal diameter of 3 mm or more that exceeds the negative control is positive; grading: 3\u20134 mm (+), 5\u20137 mm (++), 8\u201310 mm (+++), above 10 mm (++++).",
        "Which drugs must be stopped before skin testing?",
        "Antihistamines and glucocorticoids can suppress the reaction and are usually stopped 3\u20137 days beforehand; follow medical advice to avoid false negatives.",
        "About \"Allergen (Skin Test) Result Interpreter\"",
        "Allergen (Skin Test) Result Interpreter." + DISCL_M,
    ]))

    write('calc-1', build('calc-1', [
        "\U0001F4CB Rhinitis Symptom Score (TNSS)",
        "The Total Nasal Symptom Score (TNSS) quantifies the severity of allergic or chronic rhinitis symptoms.",
        "Rhinitis symptom score",
        "/ Rhinitis symptom score",
        "\U0001F4D6 View the \"Rhinitis Symptom Score (TNSS) Guide\"",
        "The TNSS nasal symptom total is the sum of nasal obstruction, nasal itching, sneezing and rhinorrhoea across 4 items (0 to 3 each), for a maximum of 12; a score of 7 or above indicates marked symptoms and a visit to an ENT department is recommended.",
        "Rhinorrhoea",
        "0 no symptoms",
        "1 mild",
        "Sneezing",
        "Nasal itching",
        "Nasal obstruction",
        "\U0001F4DA In-depth Analysis: Rhinitis Symptom Score (TNSS)",
        "Patients with allergic rhinitis self-score the TNSS daily to monitor symptom fluctuation and the response to medication.",
        "Compare scores before and after environmental allergen exposure to assess triggers.",
        "Used in clinical trials as an endpoint for nasal symptom efficacy.",
        "Self-assessment for moderate to severe rhinitis",
        "Rhinorrhoea 2 + sneezing 2 + nasal itching 1 + nasal obstruction 2 = 7 points (0\u201312), which counts as severe; an ENT consultation to assess the medication plan is recommended.",
        "What is the difference between TNSS and RQLQ?",
        "TNSS is a pure symptom severity scale (0\u201312), while RQLQ is a quality-of-life questionnaire; the former is simple and the latter comprehensive, and they can be used together.",
        "Is the score heavily influenced by subjectivity?",
        "TNSS is a self-rated scale affected by the patient's own judgement, so record it at a fixed time and on consecutive days to improve comparability.",
    ]))


if __name__ == '__main__':
    main()

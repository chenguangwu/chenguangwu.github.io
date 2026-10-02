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
    write('laryngeal-nerve', build('laryngeal-nerve', [
        "\U0001F50A Recurrent Laryngeal Nerve (Palsy) Acoustic Analyser",
        "Enter voice acoustic analysis parameters to assess vocal fold vibration stability, supporting the objective diagnosis and follow-up of recurrent laryngeal nerve paralysis.",
        "\"Enter voice acoustic analysis parameters to assess vocal fold vibration stability, supporting the objective diagnosis and follow-up of recurrent laryngeal nerve paralysis.\" It performs a professional calculation from the input parameters and outputs the result.",
        "Male",
        "Female",
        "Fundamental frequency F0 (Hz)",
        "Jitter (%)",
        "Shimmer (%)",
        "Noise-to-harmonics ratio NHR",
        "Harmonics-to-noise ratio HNR (dB)",
        "Maximum phonation time MPT (seconds)",
        "Normal reference values for acoustic parameters",
        "F0 fundamental frequency",
        "A lower value suggests altered vocal fold mass or paralysis",
        "Jitter perturbation",
        "A higher value suggests unstable vocal fold vibration",
        "Shimmer amplitude perturbation",
        "A higher value suggests incomplete glottic closure",
        "NHR noise-to-harmonics ratio",
        "A higher value suggests an increased breathy component",
        "HNR harmonics-to-noise ratio",
        "A lower value suggests poorer voice quality",
        "MPT maximum phonation time",
        ">15 seconds",
        ">10 seconds",
        "A shorter time suggests incomplete glottic closure or reduced vital capacity",
        "Clinical use:",
        "Acoustic analysis is an important objective tool for assessing voice disorders. In recurrent laryngeal nerve paralysis, incomplete glottic closure increases breathiness (shimmer up, NHR up, HNR down), makes vocal fold vibration unstable (jitter up) and shortens the MPT. Combining laryngoscopy and electromyography gives a full assessment of recurrent laryngeal nerve function.",
        "\U0001F4DA In-depth Analysis: Recurrent Laryngeal Nerve (Palsy) Acoustic Analyser",
        "Assessing the recurrent laryngeal nerve in hoarseness after thyroid surgery.",
        "Follow-up of recovery from vocal fold paralysis.",
        "Objective recording of voice disorders.",
        "Abnormal acoustic parameters",
        "MPT=7 s, jitter=1.8% and shimmer=9% indicate incomplete vocal fold closure and incomplete recurrent laryngeal nerve paralysis, so laryngoscopy is recommended to confirm the side.",
        "What does a rise in jitter or shimmer mean?",
        "Raised frequency or amplitude perturbation reflects irregular vocal fold vibration, which is common with vocal fold masses, paralysis and abnormal tension.",
        "Can normal acoustics rule out paralysis?",
        "No. Mild paralysis can look nearly normal acoustically, so laryngoscopy is needed to view vocal fold movement directly.",
        "About \"Recurrent Laryngeal Nerve (Palsy) Acoustic Analyser\"",
        "\uFE0F Recurrent Laryngeal Nerve (Palsy) Acoustic Analyser." + DISCL_M,
        "How to use the Recurrent Laryngeal Nerve (Palsy) Acoustic Analyser",
        "What does the Recurrent Laryngeal Nerve (Palsy) Acoustic Analyser do?",
        "How do I use the Recurrent Laryngeal Nerve (Palsy) Acoustic Analyser?",
        "What scenarios is the Recurrent Laryngeal Nerve (Palsy) Acoustic Analyser suitable for?",
    ]))

    write('lund-kennedy-score', build('lund-kennedy-score', [
        "\U0001F4DA Nasal Endoscopy (Lund-Kennedy) Scorer",
        "Based on nasal endoscopy findings, it scores nasal polyps, oedema, discharge, scarring and crusting bilaterally in chronic rhinosinusitis, for a total of 0-20 points.",
        "The Lund-Kennedy endoscopy score is the sum of 5 items on each side (polyps, oedema, discharge, scarring and crusting); up to 5 is mild, up to 13 moderate and above 13 severe mucosal inflammation.",
        "\U0001F539 Left nasal cavity",
        "Nasal polyps",
        "0 none",
        "1 middle meatus",
        "2 beyond the middle meatus",
        "1 mild to moderate",
        "2 severe",
        "Discharge",
        "1 clear or thin",
        "2 thick or purulent",
        "Scarring (adhesions)",
        "1 mild",
        "\U0001F539 Right nasal cavity",
        "Lund-Kennedy score interpretation",
        "Mild mucosal inflammation",
        "Marked mucosal inflammation, medication or surgery needed",
        "Severe mucosal inflammation, surgery recommended",
        "The Lund-Kennedy score is an endoscopic quantitative assessment of mucosal inflammation in rhinosinusitis, scoring 0-10 per side for a bilateral total of 0-20. It is often used together with the Lund-Mackay CT score to assess the severity and treatment response of chronic rhinosinusitis.",
        "\U0001F4DA In-depth Analysis: Nasal Endoscopy (Lund-Kennedy) Scorer",
        "Endoscopic quantitative assessment of chronic rhinosinusitis.",
        "Comparison before and after FESS.",
        "Monitoring the response to drug treatment.",
        "Bilateral mild",
        "Right: polyps 0 + oedema 1 + discharge 1 + scarring 0 + crusting 0 = 2; the left is the same at 2; the total of 4 out of 20 is mild, so drug treatment takes priority.",
        "How is the total graded?",
        "0-5 is mild, 6-10 moderate and 11-20 severe; the higher the score, the more severe the endoscopic inflammation.",
        "What is the point of combining it with Lund-Mackay?",
        "The former grades mucosal inflammation (function and endoscopy) and the latter CT anatomy (structure); together they make the assessment more complete.",
        "About \"Nasal Endoscopy (Lund-Kennedy) Scorer\"",
        "Nasal Endoscopy (Lund-Kennedy) Scorer." + DISCL_M,
    ]))

    write('lund-mackay-score', build('lund-mackay-score', [
        "\U0001F4CB Sinus CT (Lund-Mackay) Scorer",
        "Based on the Lund-Mackay scoring system, it grades the severity of chronic rhinosinusitis on CT, scoring each sinus's opacification from 0 to 2 and the ostiomeatal complex 0 or 2.",
        "The Lund-Mackay sinus CT score is the sum of 6 sinuses or ostiomeatal complexes on each side (0 to 2 each: none, partial or complete), out of 24; up to 4 is mild, up to 12 moderate, up to 20 severe and above 20 extremely severe.",
        "Right side",
        "Maxillary sinus",
        "0 normal",
        "1 partial opacification",
        "2 complete opacification",
        "Anterior ethmoid sinus",
        "Posterior ethmoid sinus",
        "Sphenoid sinus",
        "Frontal sinus",
        "Ostiomeatal complex (OMC)",
        "0 not obstructed",
        "2 completely obstructed",
        "Left side",
        "Lund-Mackay scoring criteria",
        "Score range",
        "Mild mucosal disease, conservative treatment can be considered",
        "Several sinuses involved; assess surgical indications after drug treatment",
        "Extensive disease, surgical intervention recommended",
        "All sinus groups involved, surgery strongly recommended",
        "Scoring notes:",
        "Each sinus (maxillary, anterior ethmoid, posterior ethmoid, sphenoid and frontal) is scored 0-2 by its degree of opacification, where 0 is normal, 1 partial and 2 complete; the ostiomeatal complex (OMC) scores 0 or 2, where 0 is not obstructed and 2 completely obstructed. Each side is worth up to 12 points and the total is up to 24.",
        "\U0001F4DA In-depth Analysis: Sinus CT (Lund-Mackay) Scorer",
        "Reviewing CT before chronic rhinosinusitis surgery and quantifying the extent of bilateral sinus disease with Lund-Mackay.",
        "Reviewing CT after sinus surgery and comparing the total score to assess the outcome.",
        "Judging surgical indications when several sinus groups are involved, with a total of 13 or above usually calling for surgery.",
        "Bilateral opacification across several sinuses",
        "Right: maxillary 2 + anterior ethmoid 2 + posterior ethmoid 1 + sphenoid 1 + frontal 0 + OMC 2 = 8; the left is the same at 8; the total of 16 out of 24 is severe, so endoscopic sinus surgery is recommended.",
        "Why does the OMC only score 0 or 2?",
        "The ostiomeatal complex is the key drainage pathway, so only obstruction is judged (0 not obstructed, 2 completely obstructed) without distinguishing partial obstruction.",
        "How does it combine with the Lund-Kennedy endoscopy score?",
        "Lund-Mackay reflects CT anatomical disease and Lund-Kennedy reflects endoscopic mucosal inflammation; together they assess chronic rhinosinusitis more comprehensively.",
        "About \"Sinus CT (Lund-Mackay) Scorer\"",
        "Based on the Lund-Mackay scoring system, it quantifies sinus CT findings in chronic rhinosinusitis and is a standardised tool for preoperative assessment and postoperative follow-up.",
        "Independent scoring of 6 sites on each side",
        "Automatic calculation of the total and of each side",
        "Provides clinical management recommendations",
        "Preoperative assessment for chronic rhinosinusitis",
        "Quantitative analysis of sinus CT images",
        "Comparative follow-up of surgical outcome",
        "ENT clinical research",
    ]))

    write('nasal-resistance', build('nasal-resistance', [
        "\U0001F3CB\uFE0F Nasal Resistance (NRM) Meter",
        "Computes unilateral and total nasal resistance from rhinomanometry data to assess nasal ventilation.",
        "Core formulas (by input variable): Math.round(totalRes \u00d7 1000) \u00f7 1000; Math.round(lRes \u00d7 1000) \u00f7 1000; Math.round(rRes \u00d7 1000) \u00f7 1000",
        "Reference pressure point",
        "Nasal pressure difference \u0394P (Pa)",
        "Airflow V (cm\u00b3/s)",
        "Normal nasal resistance values and grading",
        "Unilateral resistance Pa/(cm\u00b3/s)",
        "Total nasal resistance",
        "Normal nasal ventilation",
        "Mild nasal obstruction",
        "Moderate nasal obstruction affecting daily life",
        "Severely elevated",
        "Severe nasal obstruction with mouth breathing",
        "Calculation notes:",
        "Nasal resistance R = \u0394P / V (Pa/(cm\u00b3/s)). Total nasal resistance is calculated as R total = (R left \u00d7 R right) / (R left + R right). Common reference pressure points are 75 Pa, 150 Pa and 300 Pa, with 150 Pa the most frequently used. Measuring nasal resistance is an objective way to assess nasal ventilation and can be used to quantify obstruction, evaluate drug response and compare findings before and after surgery.",
        "\U0001F4DA In-depth Analysis: Nasal Resistance (NRM) Meter",
        "Objectively quantifying left and right nasal resistance in patients with nasal obstruction.",
        "Outcome after septoplasty or turbinate surgery.",
        "Comparison before and after rhinitis drug trials.",
        "Right-sided resistance high",
        "Anterior rhinomanometry gives a right nasal resistance of 0.45 Pa\u00b7s/cm\u00b3 (normal under 0.3) against 0.18 on the left, indicating right nasal obstruction such as septal deviation or turbinate hypertrophy, so nasal endoscopy is recommended.",
        "What is the normal nasal resistance?",
        "Total nasal resistance in adults is about 0.1-0.3 Pa\u00b7s/cm\u00b3 at a 150 Pa pressure difference; it is affected by flow and nasal condition, and the two sides can be asymmetric.",
        "How does it relate to acoustic rhinometry?",
        "Nasal resistance reflects overall patency while acoustic rhinometry reflects local cross-sectional area, so the two assess nasal structure in a complementary way.",
        "About \"Nasal Resistance (NRM) Meter\"",
        "Nasal Resistance (NRM) Meter." + DISCL_M,
    ]))


if __name__ == '__main__':
    main()

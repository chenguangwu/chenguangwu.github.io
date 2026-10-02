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
    write('tdi-score', build('tdi-score', [
        "\U0001F4CB Olfactory Function (TDI Score) Tester",
        "Based on the three sub-tests of the Sniffin' Sticks olfactory test (threshold T, discrimination D and identification I), it computes the total TDI score and classifies olfactory function.",
        "The TDI composite olfactory index = threshold T + discrimination D + identification I, from 0 to 16 each, out of 48; above 30.5 is normal olfaction, 16\u201330.5 is hyposmia and below 16 is functional anosmia.",
        "Threshold test (T)",
        "Range 1-16",
        "Discrimination test (D)",
        "Range 0-16",
        "Identification test (I)",
        "TDI score classification criteria",
        "TDI total",
        "Normal olfactory function",
        "Hyposmia",
        "Reduced olfactory function, further testing needed",
        "Functional anosmia",
        "Severe loss of smell",
        "Notes on the three sub-tests",
        "T - threshold test",
        "n-Butanol is diluted step by step to find the lowest concentration the subject can reliably detect. A staircase method is used and the result runs from 1 to 16, where a higher score means a lower threshold, that is greater olfactory sensitivity.",
        "D - discrimination test",
        "Three pens are presented at a time, two alike and one different, and the subject must pick out the one that smells different. There are 16 sets and each correct answer scores 1 point, for a total of 0-16.",
        "I - identification test",
        "Sixteen everyday odours are presented and the subject picks the correct name from four options. Each correct answer scores 1 point, for a total of 0-16.",
        "Clinical use:",
        "The TDI score is an internationally recognised way to quantify olfactory function and is widely used to diagnose olfactory disorders and to evaluate and follow up treatment. Age and sex influence the normal range, and the lower limit can be relaxed for older adults.",
        "\U0001F4DA In-depth Analysis: Olfactory Function (TDI Score) Tester",
        "Assessing and following up smell loss after COVID-19.",
        "Screening for the cause of olfactory disorders, such as rhinitis or neurodegeneration.",
        "Occupational olfactory testing.",
        "T=8 + D=10 + I=9 gives TDI=27, below 30.5, which is hyposmia, so olfactory training and follow-up are recommended.",
        "What do the three TDI components mean?",
        "T is the threshold, the most dilute concentration that can be smelled; D is discrimination, whether two odours are the same; and I is identification, naming the odour. Together they reflect both the threshold and the cognitive side of the olfactory pathway.",
        "How does TDI relate to the Sniffin' Sticks test?",
        "Sniffin' Sticks is the standard tool for TDI, and local versions such as smell cards also exist; the scoring criteria should be calibrated against local norms.",
        "About \"Olfactory Function (TDI Score) Tester\"",
        "Olfactory Function (TDI Score) Tester." + DISCL_M,
    ]))

    write('tinnitus-matching', build('tinnitus-matching', [
        "\U0001F4E1 Tinnitus (Frequency and Loudness) Matcher",
        "Records the tinnitus pitch-match frequency and loudness-match value, classifying the acoustic characteristics of the tinnitus and supporting clinical assessment.",
        "Tinnitus matching: by frequency it is divided into low, up to 500 Hz, usually Meniere's disease or middle ear disease; mid, up to 2000 Hz; and high, above 2000 Hz, usually noise-induced or age-related hearing loss. The loudness grading guides masking therapy.",
        "Tinnitus type",
        "Pure tone tinnitus",
        "Noise-like tinnitus",
        "Mixed type",
        "Pitch-match frequency",
        "Loudness-match value (dB SL)",
        "Tinnitus masking level (dB HL)",
        "Classification of tinnitus acoustic characteristics",
        "Frequency classification",
        "Low-frequency tinnitus",
        "Common in Meniere's disease and middle ear disease",
        "Mid-frequency tinnitus",
        "Middle ear or cochlear disease",
        "High-frequency tinnitus",
        "Common in noise-induced and age-related hearing loss",
        "Loudness classification",
        "Just perceptible, usually the compensated stage",
        "Affects daily life, intervention needed",
        "Clearly troublesome, often with anxiety",
        "Severely troublesome, active treatment needed",
        "Test notes:",
        "Pitch matching presents pure tones or narrowband noise one by one from low to high frequency, and the patient indicates the pitch that sounds most similar. Loudness matching starts at a high level at the matched frequency and lowers it gradually until the patient judges it equally loud to the tinnitus, and the value is recorded in dB SL, the sensation level. The Feldmann masking curve can further characterise how the tinnitus is masked.",
        "\U0001F4DA In-depth Analysis: Tinnitus (Frequency and Loudness) Matcher",
        "Matching the dominant pitch and loudness for patients with tinnitus.",
        "Customising masking sound or sound therapy.",
        "Following up treatment response through matching stability.",
        "Pure tone matching gives a dominant tinnitus pitch of 4 kHz and an equivalent loudness of 12 dB SL, indicating high-frequency tinnitus, which is common after noise exposure or with age, so a masking sound can be chosen on that basis.",
        "Why is tinnitus loudness given in dB SL?",
        "SL, the sensation level, is the number of decibels above the hearing threshold at that frequency and reflects the relative loudness of the tinnitus; in some patients it sits above the threshold, while in others it is subliminal.",
        "Does matching help treatment?",
        "Yes. Customising masking or habituation sounds from the matched frequency and loudness is the basis of tinnitus sound therapy.",
        "About \"Tinnitus (Frequency and Loudness) Matcher\"",
        "Tinnitus (Frequency and Loudness) Matcher." + DISCL_M,
    ]))

    write('tonsil-grading', build('tonsil-grading', [
        "\U0001F4DA Tonsil (Grade I-IV) Grader",
        "Based on the Brodsky criteria, it grades the tonsils by the proportion of the oropharyngeal width they occupy and assesses surgical indications together with clinical symptoms.",
        "Tonsillar hypertrophy is graded 0 to IV: grade 0 within the fossa, grade I up to 25%, grade II 26\u201350%, grade III 51\u201375% and grade IV over 75%, when the tonsils meet in the midline; grades III\u2013IV with OSAHS call for surgical removal.",
        "Tonsil size (Brodsky grading)",
        "Grade 0",
        "Tonsils within the fossa",
        "\u226425% of oropharyngeal width",
        "26-50% of oropharyngeal width",
        "51-75% of oropharyngeal width",
        ">75% of oropharyngeal width, kissing tonsils",
        "Recurrent tonsillitis, 3 or more episodes a year",
        "Snoring during sleep or apnoea",
        "Difficulty swallowing",
        "History of peritonsillar abscess",
        "Suspected focal tonsillitis, as in nephritis or rheumatism",
        "Brodsky tonsil grading criteria",
        "Grade",
        "Share of oropharyngeal width",
        "Within the tonsillar fossa",
        "Tonsils atrophied or removed",
        "Mild hypertrophy",
        "Moderate hypertrophy",
        "Severe hypertrophy",
        ">75%, bilateral kissing tonsils",
        "Extremely severe hypertrophy",
        "Surgical indications for tonsillectomy:",
        "1. Chronic tonsillitis recurring 3 or more times a year, or 5 or more times in 2 years; 2. grade III-IV tonsillar hypertrophy with OSAHS; 3. peritonsillar abscess, with tonsillectomy as a second-stage or first-stage procedure; 4. focal tonsillitis with nephritis, rheumatic fever or psoriasis; 5. tonsillar tumour, which needs biopsy to confirm.",
        "\U0001F4DA In-depth Analysis: Tonsil (Grade I-IV) Grader",
        "Assessing tonsil size in children who snore or have OSA.",
        "Surgical indications in recurrent tonsillitis.",
        "Judging the impact on swallowing and speech.",
        "Grade III hypertrophy",
        "Both tonsils reach the palatopharyngeal arch, grade III, blocking about 70% of the pharyngeal space with night-time snoring and hypoxia, so tonsillectomy is recommended.",
        "How does grading relate to surgery?",
        "Grades III\u2013IV with OSA, swallowing difficulty, or 7 or more suppurative episodes a year usually call for surgery, while grades I\u2013II can be observed.",
        "Does tonsil enlargement matter in adults?",
        "Rapid unilateral enlargement in an adult raises suspicion of a tumour rather than simple physiological hypertrophy, so a biopsy is needed to exclude it.",
        "About \"Tonsil (Grade I-IV) Grader\"",
        "Tonsil (Grade I-IV) Grader." + DISCL_M,
    ]))


if __name__ == '__main__':
    main()

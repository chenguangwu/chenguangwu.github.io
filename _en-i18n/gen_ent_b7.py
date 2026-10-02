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
    write('tympanic-perforation', build('tympanic-perforation', [
        "\U0001F4D0 Tympanic Membrane Perforation (Area) and Hearing Loss Estimator",
        "Estimates the percentage of perforated area and the expected degree of hearing loss from the size and site of a tympanic membrane perforation.",
        "Core formulas (by input variable): Math.round(baseHL \u00d7 locFactor); Math.round(pct \u00d7 0.6); \u03c0 \u00d7 (pd\u00f72) \u00d7 (pw\u00f72)",
        "Perforation site",
        "Central",
        "Marginal",
        "Attic",
        "Perforation maximum diameter (mm)",
        "Perforation minimum diameter (mm)",
        "Tympanic membrane maximum diameter (mm)",
        "Tympanic membrane minimum diameter (mm)",
        "Perforation grading and management",
        "Expected hearing loss",
        "Small perforation",
        "Can heal spontaneously, observe",
        "Medium perforation",
        "Patch or observe",
        "Large perforation",
        "Tympanoplasty recommended",
        "Total perforation",
        "Tympanoplasty required",
        "Clinical notes:",
        "The tympanic membrane area is about 85 mm\u00b2. Perforation area correlates positively with hearing loss, but the site also matters. Marginal and attic perforations damage the annulus or involve the ossicular chain, so the hearing loss often exceeds the estimate from area alone and the risk of malignant change is higher.",
        "\U0001F4DA In-depth Analysis: Tympanic Membrane Perforation (Area) and Hearing Loss Estimator",
        "Hearing assessment for a perforation remaining after otitis media.",
        "Prognosis of a traumatic perforation.",
        "Indications for tympanoplasty.",
        "Medium central perforation",
        "A central perforation of the pars tensa covering about 40%, with air conduction down 30 dB on audiometry and bone conduction normal, is a conductive loss; either observe for 3 months or proceed to tympanoplasty.",
        "Does a perforation always cause hearing loss?",
        "Small perforations cause only slight loss, under 30 dB, while large ones or those with ossicular damage cause a greater drop; most recover once the perforation heals.",
        "When is surgery needed?",
        "If it has not healed after 3 months, discharge recurs, the hearing loss is marked, or the perforation is marginal and prone to cholesteatoma, tympanoplasty or mastoid surgery is recommended.",
        "About \"Tympanic Membrane Perforation (Area) and Hearing Loss Estimator\"",
        "Tympanic Membrane Perforation (Area) and Hearing Loss Estimator." + DISCL_M,
    ]))

    write('tympanometry', build('tympanometry', [
        "\U0001F4DA Acoustic Immittance (Tympanogram) Classifier",
        "Enter the tympanogram peak pressure (dPa) and compliance (mL) to classify it automatically using the Jerger types A, As, Ad, B and C, and to plot the tympanogram curve.",
        "\"Enter the tympanogram peak pressure (dPa) and compliance (mL) to classify it automatically using the Jerger types A, As, Ad, B and C, and to plot the tympanogram curve.\" It performs a professional calculation from the input parameters and outputs the result.",
        "Peak pressure TPP (daPa)",
        "Static compliance SC (mL)",
        "External canal volume ECV (mL)",
        "Gradient (%)",
        "Type analysis",
        "Jerger tympanogram classification criteria",
        "Peak pressure (dPa)",
        "Compliance (mL)",
        "Normal tympanogram",
        "Type As",
        "Low compliance: otosclerosis, ossicular fixation",
        "Type Ad",
        "High compliance: ossicular discontinuity, flaccid tympanic membrane",
        "No peak",
        "Flat pattern: middle ear effusion, tympanic membrane perforation",
        "Negative pressure: eustachian tube dysfunction",
        "Clinical points:",
        "A type B tympanogram with an abnormally large ECV suggests a tympanic membrane perforation; in a type C tympanogram a peak pressure from -100 to -200 daPa is type C1, mild negative pressure, and below -200 daPa is type C2, severe negative pressure. Acoustic immittance is an important tool for screening middle ear function and, together with pure tone audiometry, distinguishes conductive from sensorineural hearing loss.",
        "\U0001F4DA In-depth Analysis: Acoustic Immittance (Tympanogram) Classifier",
        "Screening children for otitis media with effusion.",
        "Assessing eustachian tube dysfunction.",
        "Identifying the nature of hearing loss, such as conductive loss.",
        "Type B tympanogram",
        "A flat tympanogram with no peak, type B, and low compliance suggests middle ear effusion, that is otitis media with effusion; confirm it with pure tone audiometry.",
        "Is type A always normal?",
        "A type A tracing with a normal peak is usually normal, but As with a low peak indicates stiffness and Ad with a high peak indicates laxity, so judge it together with the acoustic reflexes.",
        "What does type C mean?",
        "A negatively shifted peak indicates negative middle ear pressure, an early sign of eustachian tube obstruction that can progress to effusion; treat the nose and the eustachian tube.",
        "About \"Acoustic Immittance (Tympanogram) Classifier\"",
        "Acoustic Immittance (Tympanogram) Classifier." + DISCL_M,
    ]))

    write('vocal-cord-assessment', build('vocal-cord-assessment', [
        "\U0001F4CB Laryngoscopy (Vocal Fold Movement) Assessor",
        "Assesses vocal fold movement by laryngoscopy, judging mobility, the fixed position and glottic closure, to help diagnose vocal fold paralysis.",
        "Vocal fold paralysis grading: movement normal; reduced movement is incomplete paralysis, grade I; fixation in the intermediate position is complete paralysis, grade III, with both the superior laryngeal and recurrent laryngeal nerves injured; fixation in another position is paralysis grade II.",
        "Vocal fold mobility",
        "Mobility on the affected side",
        "Normal",
        "Reduced movement",
        "Fixed",
        "Affected side",
        "Left",
        "Right",
        "Both sides",
        "Vocal fold position when fixed",
        "Fixed position",
        "Midline position",
        "Paramedian position",
        "Intermediate position",
        "Glottic closure",
        "Complete",
        "Incomplete",
        "Cannot close",
        "Arytenoid cartilage",
        "Movement normal",
        "Fixed",
        "Reference for grading vocal fold paralysis",
        "Normal vocal fold movement",
        "Incomplete vocal fold paralysis, mild recurrent laryngeal nerve injury",
        "Grade II",
        "Vocal fold paralysis, recurrent laryngeal nerve injury",
        "Complete vocal fold paralysis, superior plus recurrent laryngeal nerve injury",
        "Clinical points:",
        "Fixation in the paramedian position indicates recurrent laryngeal nerve injury, while fixation in the intermediate position indicates combined superior and recurrent laryngeal nerve injury, that is vagal injury. Bilateral vocal fold paralysis can cause laryngeal obstruction and needs emergency management. Look for causes such as neck surgery, tumours and viral infection.",
        "\U0001F4DA In-depth Analysis: Laryngoscopy (Vocal Fold Movement) Assessor",
        "Laryngoscopy for hoarseness to assess vocal fold mobility.",
        "Follow-up of recurrent laryngeal nerve monitoring after thyroid surgery.",
        "Recording which side is paralysed.",
        "Right vocal fold fixed",
        "Laryngoscopy shows the right vocal fold fixed in the paramedian position with incomplete glottic closure, indicating right recurrent laryngeal nerve paralysis; a mediastinal CT is recommended to exclude a mass.",
        "What are the common causes of vocal fold fixation?",
        "Trauma or surgery such as thyroid or oesophageal, tumour compression, viral infection of the Bell type, and central lesions; because the left nerve runs a longer course, beware of a chest mass.",
        "Is laryngoscopy essential for the assessment?",
        "Yes. Acoustic analysis can suggest the problem but cannot visualise it, so diagnosis and localisation need video or fibreoptic laryngoscopy.",
        "About \"Laryngoscopy (Vocal Fold Movement) Assessor\"",
        "\uFE0F Laryngoscopy (Vocal Fold Movement) Assessor." + DISCL_M,
    ]))


if __name__ == '__main__':
    main()

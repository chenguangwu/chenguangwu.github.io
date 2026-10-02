#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'pediatrics')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'pediatrics')
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
    out = {'slug': slug, 'industry': 'pediatrics', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
#!/usr/bin/env python3
# body for pediatrics b2: developmental-milestones / diarrhea-dehydration / enuresis-age / growth-curve-zscore / hearing-screening

def main():
    # developmental-milestones (55)
    write('developmental-milestones', build('developmental-milestones', [
"Developmental Milestones (Gross/Fine/Speech/Social) Assessor",
"Compare developmental milestones by child's age in months; assess gross-motor, fine-motor, language and social domains",
" / Developmental Milestones Assessor",
"Assessment basis",
"By current age in months",
"View delayed items",
"Developmental Milestones Quick Reference (Key Ages)",
"Gross motor",
"Fine motor",
"Head up 90°",
"Relaxed hand fisting",
"Vocal laugh",
"Fixate on face",
"Sit briefly alone",
"Reach and grasp",
"Babble",
"Stranger anxiety",
"Crawl",
"Pincer grasp",
"Imitate ba-ma (unconscious)",
"Wave bye-bye",
"Stand alone",
"Put object in container",
"Say ba-ma consciously",
"Point to object",
"18 months",
"Walk steadily alone",
"Stack 2 blocks",
"Say 10-20 words",
"Imitate household tasks",
"24 months",
"Jump with both feet",
"Stack 6 blocks",
"Say 2-3 word phrases",
"Parallel play",
"36 months",
"Stand on one foot",
"Draw a circle",
"Say complete sentences",
"Cooperative play",
"Note: milestone timing varies individually. If a domain lags >2 months (infancy) or >3 months (toddler), refer for developmental assessment. Red flags: no smile at 4 mo, no reaching at 6 mo, no sitting at 9 mo, no crawling/pointing at 12 mo, no walking/ba-ma at 18 mo, no 2-word phrase at 24 mo, no sentences at 36 mo. This tool is for screening reference only.",
"In-Depth: Developmental Milestones Assessment",
"Gross/fine motor, speech, social",
"Month-age reference",
"Attainment rate",
"18-month attainment rate",
"At 18 mo should walk, say words, point; attainment ≥80% normal, <50% clearly delayed.",
"Clearly delayed",
"Single-domain attainment <50% -> clearly delayed, early intervention ASAP.",
"Milestone range?",
"Listed by month for speech/motor/social; lag >2 months warrants vigilance.",
"Preterm correction?",
"Use corrected age (subtract preterm weeks) until age 2.",
"About the Developmental Milestones (Gross/Fine/Speech/Social) Assessor",
"The pediatric developmental-milestones assessor evaluates gross-motor, fine-motor, language and social domains by age in months. A medical professional tool based on authoritative standards, for reference only.",
    ]))

    # diarrhea-dehydration (47)
    write('diarrhea-dehydration', build('diarrhea-dehydration', [
"Diarrhea (Dehydration Severity) Grader",
"Grade dehydration by stool frequency, stool character and dehydration signs, and give a rehydration plan",
"Core formula (by input): weight×deficit×1000; freq×10×weight÷10",
" / Diarrhea Dehydration Grader",
"Stool frequency (times/day)",
"Duration (days)",
"Stool character",
"Watery stool",
"Mucoid stool",
"Bloody stool",
"Rice-water stool",
"Dehydration signs (check present)",
"Diarrhea Dehydration Grading (WHO)",
"Signs",
"None/mild dehydration",
"Moderate dehydration",
"Severe dehydration",
"General condition",
"Irritable/agitated",
"Lethargic/coma",
"Eye sockets",
"Thirst",
"Drinks normally",
"Excessively thirsty",
"Drinks poorly",
"Skin turgor",
"Slow recoil",
"Recoil >2 sec",
"Note: acute diarrhea is mostly viral (rotavirus/norovirus) and self-limiting. Bloody stool needs workup for bacterial enteritis (Shigella/Salmonella/EHEC). Rice-water stool needs cholera workup. Zinc shortens illness (10-20 mg/day ×10-14 days). Low-osmolarity ORS III is the first-choice oral rehydration salt. Antibiotics are not routine; used only for bloody stool/severe bacterial infection. This tool is for clinical reference only.",
"In-Depth: Diarrhea Dehydration Grading",
"Sign-based grading",
"Maintenance volume calculation",
"Bloody-stool warning",
"10 kg watery stool",
"Maintenance = 1000 mL/day (first 10 kg × 100); moderate-severe add cumulative deficit.",
"Bloody stool suggests bacterial enteritis, needs culture; avoid antibiotics in EHEC to prevent HUS.",
"Maintenance formula?",
"First 10 kg ×100, 10-20 kg portion ×50, >20 kg portion ×20 mL/day.",
"Cholera?",
"Rice-water stool is managed as class-A; massive rapid oral/IV rehydration.",
"About the Diarrhea (Dehydration Severity) Grader",
"The pediatric diarrhea (dehydration severity) grader assesses dehydration degree and rehydration plan from stool frequency, character and signs. A medical professional tool based on authoritative standards, for reference only.",
"How to use the Diarrhea (Dehydration Severity) Grader",
"What does the Diarrhea (Dehydration Severity) Grader do?",
"Enter the child's stool frequency, stool character and dehydration signs (sunken eyes, thirst, skin turgor) to assess mild/moderate/severe dehydration and suggest oral or IV rehydration. For home and clinic pediatric diarrhea assessment.",
"How to use the Diarrhea (Dehydration Severity) Grader?",
"Which scenarios is the Diarrhea (Dehydration Severity) Grader suitable for?",
    ]))

    # enuresis-age (34)
    write('enuresis-age', build('enuresis-age', [
"Enuresis (Nighttime) and Age Assessor",
"By age, enuresis frequency and associated symptoms, distinguish primary/secondary enuresis and give treatment advice",
"Core formula (by input): max(0,15-(age-5)×1)",
" / Enuresis and Age Assessor",
"Nighttime wetting frequency (times/week)",
"Ever dry continuously for >6 months?",
"No (never)",
"Yes (relapsed after >6 months dry)",
"Daytime incontinence/urgency",
"Constipation",
"Polydipsia/polyuria",
"History of UTI",
"Snoring/sleep apnea",
"Assess enuresis type",
"Enuresis Classification and Age Relation",
"Normal nighttime continence",
"Enuresis diagnostic criteria",
"≥2 times/week, for 3 months",
"≥2 times/month, for 3 months",
"Note: enuresis is defined as involuntary night urine in a ≥5-year-old, ≥2 times/week for ≥3 months, with no neurologic/urologic organic lesion. Primary (NE): never dry ≥6 months (80%); secondary: relapsed after ≥6 months dry (often psychosocial stress/illness). Monosymptomatic (night only) vs non-monosymptomatic (with daytime symptoms). First-line: desmopressin (DDAVP) and enuresis alarm. Constipation can worsen enuresis. This tool is for clinical reference only.",
"In-Depth: Enuresis Age Assessment",
"Diagnosis at ≥5 years",
"Mono/non-monosymptomatic",
"Spontaneous remission rate",
"Frequent at 7 years",
"At 7 years, ≥2 times/week -> meets enuresis diagnosis; primary (since infancy) monosymptomatic, spontaneous remission ~90%.",
"Secondary",
"Relapsed after being dry + daytime symptoms -> secondary; check UTI/constipation/diabetes etc.",
"At what age is it diagnosed?",
"Only ≥5 years and ≥2 times/week can be diagnosed; before that it is mostly immaturity.",
"Treatment?",
"Basics: enuresis alarm + limit evening fluids; medication (desmopressin) as backup; daytime symptoms need combined therapy.",
"About the Enuresis (Nighttime) and Age Assessor",
"The pediatric enuresis (nighttime) and age assessor distinguishes primary/secondary enuresis and evaluates night-wetting frequency and behavioral/pharmacologic treatment indications. A medical professional tool based on authoritative standards, for reference only.",
    ]))

    # growth-curve-zscore (30)
    write('growth-curve-zscore', build('growth-curve-zscore', [
"Growth Curve (Height/Weight/Head) Z-Score Calculator",
"Based on WHO growth standards, compute Z-scores to assess growth (Z = (measured - median)/SD)",
"The growth-curve Z-score calculator, based on WHO standards, computes Z-scores of height, weight and head circumference to assess growth, and outputs results from the input parameters.",
" / Growth Curve Z-Score Calculator",
"Height/length (cm)",
"Head circumference (cm) (<2 years)",
"Calculate Z-scores",
"Z-Score Interpretation (WHO)",
"Z-score range",
"Nutrition assessment",
"Severe underweight/wasting/stunting",
"Moderately low, needs attention",
"Growth within normal range",
"Above average, possible overweight",
"Severely high",
"Possible obesity, needs evaluation",
"Note: Z-score is the WHO-recommended growth assessment. Under 2 years measure recumbent length; ≥2 years standing height. Weight/age (ZWA) shows underweight, height/age (ZHA) stunting, weight/height (ZWH) wasting. This tool uses a simplified WHO reference model, for screening reference only.",
"In-Depth: Growth Curve Z-Score",
"WHO median/SD",
"Height, weight, head",
"Z<-2 suggests",
"Boy 18 mo, height 76",
"WHO median 82.3, SD≈3.2: Z=(76−82.3)/3.2≈−2.0 -> stunting borderline, investigate nutrition.",
"Height 80, weight 11: Z≈−0.7/−0.3, both within ±2, good growth.",
"Z meaning?",
"Z=(measured−median)/SD; |Z|>2 is abnormally low/high.",
"Head circumference?",
"Head Z reflects brain growth; too small check microcephaly, too large check hydrocephalus.",
"About the Growth Curve (Height/Weight/Head) Z-Score Calculator",
"The pediatric growth-curve Z-score calculator, based on WHO standards, computes Z-scores of height, weight and head circumference to assess whether growth is normal. A medical professional tool based on authoritative standards, for reference only.",
    ]))

    # hearing-screening (41)
    write('hearing-screening', build('hearing-screening', [
"Hearing (OAE/AABR) Screening Result Tool",
"Interpret newborn/infant hearing-screening results; give follow-up and diagnostic-evaluation advice",
" / Hearing Screening Result Tool",
"Screening method",
"OAE (otoacoustic emissions)",
"AABR (automated auditory brainstem response)",
"OAE + AABR combined",
"Day/month age",
"Left-ear screening result",
"Fail (refer)",
"Not tested/missed",
"Right-ear screening result",
"Has hearing high-risk factors",
"Generate interpretation report",
"Hearing Screening Method Comparison",
"AABR automated auditory brainstem",
"Cochlea (outer hair cells)",
"Auditory nerve-brainstem pathway",
"Test time",
"~1-2 min/ear",
"~5-10 minutes",
"Applicable to newborns",
"Yes (during natural sleep)",
"Auditory neuropathy detection",
"No (OAE may be normal)",
"Yes (can detect ANSD)",
"False-positive rate",
"Higher (external ear factors)",
"Note: newborn hearing screening follows the '1-3-6' principle: screen by 1 month, diagnose by 3 months, intervene by 6 months. High-risk factors: NICU >5 days, family deafness history, craniofacial anomaly, intrauterine infection (CMV/rubella), hyperbilirubinemia needing exchange transfusion, bacterial meningitis, mechanical ventilation. Both OAE and AABR fail -> workup for auditory neuropathy spectrum disorder (ANSD). This tool is for clinical reference only.",
"In-Depth: Hearing Screening OAE/AABR",
"OAE vs AABR",
"Both ears pass/refer",
"High-risk factors",
"OAE both ears pass",
"Both OAE ears pass -> pass, routine follow-up; with risk factors AABR is advised.",
"Any ear refer -> re-screen; still refer -> refer for diagnostic ABR and ENT.",
"OAE checks cochlea, AABR checks auditory nerve-brainstem; AABR preferred for high-risk infants.",
"Panic if fail?",
"Newborn vernix can falsely refer; re-screen within 42 days is enough.",
"About the Hearing (OAE/AABR) Screening Result Tool",
"The newborn hearing (OAE/AABR) screening result tool interprets otoacoustic-emission and automated auditory-brainstem-response results and follow-up advice. A medical professional tool based on authoritative standards, for reference only.",
    ]))

if __name__ == '__main__':
    main()

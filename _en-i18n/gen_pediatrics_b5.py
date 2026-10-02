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
# body for pediatrics b5: seizure-classification / vaccine-schedule / vanderbilt-adhd / xinshengerhuangdan-xiaoshidanhongsu-quxian

def main():
    # seizure-classification (41)
    write('seizure-classification', build('seizure-classification', [
"Seizure (Febrile/Afebrile) Classifier",
"By seizure features and associated symptoms, distinguish seizure types and assess recurrence risk and management",
" / Seizure Classifier",
"1. With fever?",
"With fever",
"Without fever",
"2. Duration of episode",
"<15 minutes",
"≥15 minutes",
"3. Seizure type",
"Generalized",
"Focal",
"4. Number of episodes (in 24h)",
"Once",
"≥2 times",
"Prior history of febrile seizures",
"Family history of febrile seizures/epilepsy",
"Generate classification report",
"Febrile Seizure Classification (ILAE)",
"Simple FS",
"Generalized, <15 min, once in 24h, no neuro abnormality",
"Complex FS",
"Focal / ≥15 min / multiple in 24h / post-ictal neuro signs",
"FS status",
"≥30 minutes",
"Emergency management",
"Note: febrile seizures (FS) occur at 6 mo-5 yr, peak 12-18 mo. Differentiate from CNS infection, epilepsy, electrolyte disorder. Red flags: afebrile seizure, developmental delay, focal onset, prolonged episode (>15 min), recurrent, positive neuro signs. These need further workup (EEG/imaging). This tool is for clinical reference only.",
"In-Depth: Seizure Classification (Febrile/Afebrile)",
"With/without fever",
"Duration/single",
"Focal/generalized",
"Simple febrile seizure",
"Fever + brief (<15 min) + generalized + single -> simple FS, low risk, parent education.",
"Complex/afebrile",
">15 min or focal or recurrent, or afebrile -> suspect epilepsy/encephalitis, neuro evaluation.",
"Febrile-seizure baseline?",
"6 mo-5 yr fever with seizure; short-term recurrence ~30%, mostly benign.",
"When to investigate?",
"Afebrile, complex, <6 mo or >5 yr, abnormal neuro signs need thorough evaluation.",
"About the Seizure (Febrile/Afebrile) Classifier",
"The pediatric seizure (febrile/afebrile) classifier distinguishes febrile from afebrile seizures and assesses type, recurrence risk and management. A medical professional tool based on authoritative standards, for reference only.",
    ]))

    # vaccine-schedule (45)
    write('vaccine-schedule', build('vaccine-schedule', [
"Vaccination (National EPI) Schedule Tool",
"China's childhood immunization program: by birth date query due vaccines and status",
" / Vaccination Schedule Tool",
"National EPI schedule: by birth date + months infer due time - HepB at 0,1,6 mo; BCG at 0 mo; polio at 2,3,4 mo; DPT at 3,4,5 mo; MMR at 8,18 mo; months reached and not yet vaccinated marked 'due', not yet 'pending'.",
"Currently vaccinated up to (months, optional)",
"Copy schedule",
"National EPI Vaccine List",
"Vaccine name",
"Disease prevented",
"Hepatitis B vaccine",
"Hepatitis B",
"BCG vaccine",
"Tuberculosis",
"Polio vaccine",
"Poliomyelitis",
"DPT vaccine",
"Pertussis/diphtheria/tetanus",
"DT vaccine",
"Diphtheria/tetanus",
"MMR vaccine",
"Measles/mumps/rubella",
"JE vaccine",
"Japanese encephalitis",
"MenA vaccine",
"Meningococcal disease (group A)",
"MenAC vaccine",
"Meningococcal disease (A/C)",
"HepA vaccine",
"Hepatitis A",
"Note: before vaccination ensure the child is well - no fever, acute illness, or acute flare of chronic disease. Observe 30 min after. Contraindications: severe allergy to vaccine components, immunodeficiency, neurologic disease etc. Self-paid category-2 vaccines (pneumonia, rotavirus, Hib, flu etc.) can be chosen as needed. This tool is for reference; follow the local clinic schedule.",
"In-Depth: Vaccination Schedule",
"National immunization program",
"By birth date",
"Overdue reminder",
"Reaches 2 months",
"Current month-age inference: HepB (0/1/6), polio (2/3/4), DPT (3/4/5) etc.; at 2 months due polio + DPT first dose.",
"Overdue",
"Red = overdue-not-vaccinated; catch up per catch-up principles ASAP, does not affect later intervals.",
"Schedule basis?",
"Per national EPI; month-age from birth date matches doses.",
"Preterm/low birth weight?",
"Count by actual birth date; HepB first dose delayed if weight <2 kg (when mother antigen-negative).",
"About the Vaccination (National EPI) Schedule Tool",
"China's national EPI vaccination schedule tool: by child age query vaccine types, doses and cautions. A medical professional tool based on authoritative standards, for reference only.",
"e.g. 12",
    ]))

    # vanderbilt-adhd (40)
    write('vanderbilt-adhd', build('vanderbilt-adhd', [
"ADHD (Vanderbilt) Scale Assessor",
"NICHQ Vanderbilt ADHD Diagnostic Rating Scale: assess ADHD symptoms and behavioral comorbidity in 6-18 yr children",
" / Vanderbilt ADHD Scale Assessor",
"Rater",
"Parent version",
"Teacher version",
"Compute assessment result",
"Vanderbilt Scale Scoring",
"Symptom dimensions",
"Positive criterion",
"Corresponding DSM",
"Inattention",
"9 items",
"≥6 items scored ≥2 (often)",
"ADHD-inattentive type",
"Hyperactivity/impulsivity",
"ADHD-hyperactive/impulsive type",
"Behavior problems",
"8 items",
"≥3 items scored ≥3 (very often)",
"Oppositional defiant/conduct disorder",
"Anxiety/depression",
"7 items",
"≥3 items scored ≥3",
"Mood comorbidity",
"Note: scores 0=never,1=occasionally,2=often,3=very often,4=very frequently. ADHD diagnosis needs: inattention OR hyperactivity/impulsivity ≥6 items scored ≥2, onset before age 12, persistent ≥6 months, across settings (home+school), impairing function. Both parent and teacher scales positive. Exclude hyperthyroidism, sleep disorder, vision/hearing impairment etc. Treatment: behavioral therapy + medication (methylphenidate/atomoxetine). This is a screening tool; diagnosis needs specialist.",
"In-Depth: Vanderbilt ADHD",
"Attention/hyperactivity",
"Behavior/anxiety",
"Across settings",
"Attention 9 items ≥2 total 7",
"Inattention dimension ≥6 positive (0-4 scale ≥2) -> inattentive type positive, cross-check teacher version.",
"Comorbidity",
"Behavior ≥3 or anxiety ≥3 -> ODD/anxiety comorbidity, combined intervention.",
"Diagnostic threshold?",
"Inattention or hyperactivity dimension ≥6 positive, across settings (parent+teacher), ≥6 yr -> suspect ADHD.",
"Why across settings?",
"ADHD needs multi-setting presentation; single-setting positive may be situational.",
"About the ADHD (Vanderbilt) Scale Assessor",
"The ADHD (Vanderbilt) scale assessor uses the NICHQ Vanderbilt scale to assess child ADHD symptoms and comorbid behavior problems. A medical professional tool based on authoritative standards, for reference only.",
    ]))

    # xinshengerhuangdan-xiaoshidanhongsu-quxian (32)
    write('xinshengerhuangdan-xiaoshidanhongsu-quxian', build('xinshengerhuangdan-xiaoshidanhongsu-quxian', [
"Newborn Jaundice (Hour-Specific Bilirubin) Curve",
"Enter age in hours and total serum bilirubin; Bhutani nomogram assigns risk zone and shows phototherapy/exchange thresholds. Supports mg/dL and μmol/L toggle.",
"The newborn jaundice hour-bilirubin curve, by entering age in hours and TSB, assigns risk zone via the Bhutani nomogram and shows phototherapy/exchange thresholds, supporting mg/dL and μmol/L toggle, outputs results from the input parameters.",
"⚠️ This tool is a newborn-jaundice risk-stratification aid for medical staff quick estimation only; it does not replace clinical exam or physician decisions. Critical/high-risk infants should be managed per neonatal protocols immediately.",
"Postnatal age (hours)",
"Total serum bilirubin",
"Bilirubin unit",
"35 weeks",
"36 weeks",
"37 weeks",
"≥38 weeks (term)",
"High-risk factors",
"None (low risk)",
"Yes (hemolysis/G6PD/infection etc.)",
"Assess risk",
"Bhutani Nomogram Risk Zones (by hour-age percentile)",
"≥95 percentile -> high-risk zone (red): close monitoring/intervention",
"75-95 percentile -> high-intermediate zone (orange): follow up in 24h",
"40-75 percentile -> low-intermediate zone (yellow): can follow up",
"<40 percentile -> low-risk zone (green): low risk",
"Phototherapy/exchange thresholds drop with gestational age and high-risk factors. This tool uses simplified AAP 2022 thresholds.",
"In-Depth: Newborn Hour-Specific Bilirubin Curve",
"Bhutani percentile",
"AAP 2022 thresholds",
"Unit toggle",
"Bhutani ~40-75 percentile; low-risk phototherapy threshold ≈12 mg/dL -> exceeds needs phototherapy.",
"High-risk stricter",
"Gestation <38 weeks or high-risk, phototherapy threshold drops to ≈10 mg/dL, nomogram shifts left overall.",
"Relation to neonatal-jaundice?",
"Both are hour-bilirubin curves; this is the old slug, same algorithm.",
"Percentile meaning?",
"TSB position in the population distribution at the same hour-age; higher is closer to the phototherapy line.",
    ]))

if __name__ == '__main__':
    main()

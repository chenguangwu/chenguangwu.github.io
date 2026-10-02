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
    write('short-stature-prediction', build('short-stature-prediction', [
        "\U0001F52E Short Stature (GHD) Height Predictor",
        "Genetic target height calculation plus height SDS assessment, bone-age height prediction and GHD risk stratification",
        "\U0001F4D6 See the \"Short Stature (GHD) Height Predictor User Guide\"",
        "Actual age (years)",
        "Current height (cm)",
        "II. Genetic target height (parents)",
        "III. Bone age and growth data",
        "Bone age (years)",
        "Height 1 year ago (cm)",
        "IV. GHD-related clinical factors",
        "Peak GH on stimulation (ng/mL)",
        "Birth length (cm)",
        "Birth weight (kg)",
        "Craniofacial features (frontal bossing, saddle nose, small mandible)",
        "History of neonatal hypoglycaemia",
        "Bone age delayed by over 2 years",
        "Pituitary MRI abnormality",
        "Typical GHD",
        "Normal short stature",
        "Target height",
        "SDS reference",
        "Bone age prediction",
        "GHD diagnosis",
        "Genetic target height (MPH) formula",
        "Target height for boys = (father's height + mother's height + 13) / 2 \u00B1 5cm\nTarget height for girls = (father's height + mother's height - 13) / 2 \u00B1 5cm\n\n\u00B15cm is the range of genetic variation (3rd-97th percentile)",
        "Target height reflects genetic potential. If actual height falls below the lower bound of the target height range, a pathological factor is suggested (GHD, Turner syndrome, chronic disease and so on). A deviation within \u00B15cm of the target height range is normal genetic variation.",
        "Clinical meaning:",
        "A short target height is not automatically abnormal, but it must be read together with the SDS. If both parents are short (so the target height is itself low), short stature in the child may be familial or constitutional rather than pathological GHD.",
        "Chinese child height standards (simplified)",
        "Male P3",
        "Male P50",
        "Female P3",
        "Female P50",
        "3 years",
        "9 years",
        "Source: standardised growth curves for height and weight of Chinese children and adolescents aged 0-18 (2009), simplified",
        "SDS classification",
        "Short (needs assessment)",
        "Markedly short (high pathology alert)",
        "SDS = (actual height - mean for the same age and sex) / standard deviation\n\nSDS \u2264 -2 defines short stature (height below the 3rd percentile for the same age and sex)",
        "Bayley-Pinneau bone age height prediction",
        "The Bayley-Pinneau method uses the relationship between bone age and actual age to predict final adult height. It falls into three cases:",
        "Case 1: bone age \u2248 actual age (difference \u2264 1 year)\n  predicted height = current height \u00D7 B/P coefficient\n  (B is the median bone-age height percentile for that bone age, P is the final height coefficient)\n\nCase 2: bone age > actual age (early type)\n  predicted height comes out short (less growth remaining)\n\nCase 3: bone age < actual age (delayed type, common in GHD)\n  predicted height comes out tall (more growth remaining)",
        "This tool uses a simplified coefficient method: a higher final height coefficient is applied when bone age is delayed and a lower one when it is early.",
        "Growth velocity standards",
        "Normal growth velocity",
        "Abnormal alert",
        "25cm/year",
        "Under 18cm/year",
        "1-2 years",
        "12cm/year",
        "Under 8cm/year",
        "2 years to pre-puberty",
        "5-7cm/year",
        "Under 4cm/year",
        "Boys 6-12cm/year",
        "Girls 6-11cm/year",
        "Under 5cm/year",
        "After age 2 up to pre-puberty, a yearly growth velocity under 4cm calls for a high alert for a growth disorder; an endocrinology visit is advised.",
        "Key points for diagnosing growth hormone deficiency (GHD)",
        "\U0001F4CF Diagnostic conditions (all must be met):",
        "1. Height more than 2SD below the same age and sex (SDS \u2264 -2)",
        "2. Yearly growth velocity below the normal value for the age (under 4cm/year after age 2)",
        "3. Delayed bone age (usually more than 2 years)",
        "4. Peak GH below 10 ng/mL on two stimulation tests",
        "5. Other causes of short stature have been excluded",
        "\U0001F52C GH stimulation test thresholds:",
        "\u2022 Peak GH \u2265 10 ng/mL \u2192 normal (GHD excluded)",
        "\u2022 Peak GH 5-10 ng/mL \u2192 partial GHD",
        "\u2022 Peak GH < 5 ng/mL \u2192 complete GHD",
        "\u26A0\uFE0F GHD high-risk features:",
        "\u2022 Neonatal hypoglycaemia, prolonged jaundice or micropenis",
        "\u2022 Midline craniofacial malformation (cleft lip/palate, cyclopia and so on)",
        "\u2022 Visual impairment or nystagmus (septo-optic dysplasia)",
        "\u2022 Pituitary MRI abnormality (hypoplastic pituitary or ectopic posterior lobe)",
        "\u2022 Combined deficiency of several pituitary hormones",
        "\U0001F489 rhGH treatment:",
        "\u2022 Dose: 0.1-0.15 IU/kg/day (0.025-0.035 mg/kg/day)",
        "\u2022 Subcutaneous injection, at bedtime each day",
        "\u2022 Height catch-up is fastest in the first year (\"catch-up growth\")",
        "\u2022 Treatment continues until an acceptable height is reached or the epiphyses close",
        "\u2022 Regular monitoring needed: thyroid function, IGF-1, blood glucose, bone age",
        "\u26A0\uFE0F This tool is for reference only and does not replace medical diagnosis. Short stature diagnosis and GHD assessment need a paediatric endocrinologist weighing the full history, physical examination and laboratory results together. rhGH prescriptions must be issued by a specialist.",
        "\U0001F4DA In-depth analysis: Short Stature (GHD) Height Predictor",
        "Genetic target height assessment when a child's height falls below the 3rd percentile for the same age and sex.",
        "First-line screening for precocious puberty or growth hormone deficiency, compared against growth velocity.",
        "Judging during follow-up whether growth deviates beyond the genetic range.",
        "Target height calculation example",
        "Father 175 cm, mother 162 cm, boy: target height=(175+162+13)/2=175 cm, giving a genetic range of about 170-180 cm. If actual height is clearly below that range and growth velocity has slowed, bone age and endocrine causes need assessment.",
        "What are the limits of the target height formula?",
        "It reflects genetic potential (about \u00B12 SD, within 5 cm) and is affected by ethnicity, nutrition and illness; an early or delayed bone age changes the final height, so a bone age film is needed too.",
        "When is a stimulation test needed?",
        "When height is below the target height range and yearly growth velocity is abnormal (such as under 4-5 cm/year), or when growth hormone deficiency or chronic disease is suspected, a paediatric endocrinologist assesses the need.",
        "About \"Short Stature (GHD) Height Predictor\"",
        "This tool brings together genetic target height, height SDS, growth velocity, bone-age height prediction and GHD risk stratification to support paediatric endocrine assessment and management decisions.",
        "Genetic target height (MPH) calculation",
        "Standardised height SDS assessment",
        "Bayley-Pinneau bone age height prediction",
        "Multi-factor GHD risk stratification",
        "First-line screening for child short stature",
        "Supporting GHD diagnosis",
        "Reference for predicting rhGH response",
        "Follow-up monitoring of child growth",
        "What does the Short Stature (GHD) Height Predictor do?",
        "How do I use the Short Stature (GHD) Height Predictor?",
        "Which scenarios suit the Short Stature (GHD) Height Predictor?",
        "Assesses the genetic target height and growth potential behind a child's height deviation, and combines bone age to support short stature screening and the indications for growth stimulation testing.",
    ]))

    write('detector-metabolism', build('detector-metabolism', [
        "\u2697\uFE0F Catecholamine (Metabolite) Assay",
        "Enter 24-hour urine VMA and HVA plus blood catecholamine results and judge their clinical meaning against the reference ranges",
        "\"Enter 24-hour urine VMA and HVA plus blood catecholamine results and judge their clinical meaning against the reference ranges\" is computed from the input parameters and the result is reported.",
        "\U0001F4D6 See the \"Catecholamine (Metabolite) Assay User Guide\"",
        "24h urine VMA (mg/24h)",
        "24h urine HVA (mg/24h)",
        "Blood noradrenaline (pg/mL)",
        "Blood adrenaline (pg/mL)",
        "Blood dopamine (pg/mL)",
        "Analyse and interpret",
        "\U0001F4DA In-depth analysis: Catecholamine (Metabolite) Assay",
        "Screening for neuroblastoma in children with abdominal pain and hypertension.",
        "Metabolite assessment in adults with paroxysmal hypertension (phaeochromocytoma).",
        "Metabolite follow-up monitoring after surgery or in hereditary syndromes.",
        "Metabolite reading example",
        "Markedly raised 24-hour urinary VMA and HVA together with raised fractionated plasma noradrenaline and adrenaline suggests a catecholamine-secreting tumour (phaeochromocytoma or neuroblastoma), and localisation imaging plus genetic testing should follow.",
        "How do VMA/HVA relate to fractionated blood?",
        "VMA/HVA are the final urinary metabolites and reflect overall secretion, while fractionated blood reflects the immediate level; the two complement each other, and urinary metabolites are the more specific when collection is done properly.",
        "What does proper urine collection involve?",
        "Protect from light, add preservative (such as hydrochloric acid), measure the 24 hours accurately, stop interfering drugs before testing and avoid bananas, chocolate and vanilla.",
        "VMA (vanillylmandelic acid) normal reference range 1.0-7.0mg/24h, the main end metabolite of catecholamines",
        "HVA (homovanillic acid) normal 1.0-4.0mg/24h, a dopamine metabolite and a marker of neuroblastoma in children",
        "Collecting 24-hour urine needs hydrochloric acid preservative, protection from light, and avoiding bananas, chocolate and coffee during collection",
        "Blood catecholamines are strongly affected by sampling site and stress, so draw the sample while the patient is quietly supine",
        "Results from this tool are for reference only and do not replace a clinician's diagnostic judgement",
        "About \"Catecholamine (Metabolite) Assay\"",
        "This tool analyses catecholamines and their metabolites; enter 24-hour urinary VMA and HVA plus blood catecholamine values to read them clinically against the reference ranges and assess risk.",
        "Five indicators analysed together",
        "Automatic comparison with reference ranges",
        "Phaeochromocytoma and neuroblastoma risk alerts",
        "Age factors taken into account",
        "Endocrine tumour screening",
        "Supporting phaeochromocytoma diagnosis",
        "Paediatric neuroblastoma screening",
        "Differential diagnosis of hypertension",
        "How to use the Catecholamine (Metabolite) Assay",
        "To screen for catecholamine-secreting tumours such as paroxysmal hypertension (phaeochromocytoma) and hypertension with abdominal pain in children (neuroblastoma).",
        "What does the Catecholamine (Metabolite) Assay do?",
        "How do I use the Catecholamine (Metabolite) Assay?",
        "Which scenarios suit the Catecholamine (Metabolite) Assay?",
    ]))


if __name__ == '__main__':
    main()

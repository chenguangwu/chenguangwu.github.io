#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'gastroenterology')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'gastroenterology')
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
    out = {'slug': slug, 'industry': 'gastroenterology', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
DISCL_M = " A professional medical tool based on authoritative medical standards, for reference only."

def main():
    write('hepatic-encephalopathy', build('hepatic-encephalopathy', [
        "\U0001F9E0 Hepatic Encephalopathy (West Haven Grading) Tool",
        "Assess hepatic encephalopathy severity (grade I-IV) based on the West Haven criteria, aiding clinical grading and treatment decisions.",
        "Hepatic Encephalopathy West Haven Grading Tool",
        "/ Hepatic Encephalopathy Grading",
        "\U0001F4D6 View the Hepatic Encephalopathy West Haven Grading Usage Guide",
        "Hepatic encephalopathy grading 0 to IV: take the highest level among consciousness, behavior, cognition, and asterixis; in order grade 0 (MHE), grade I, grade II, grade III, grade IV (coma).",
        "Consciousness and behavior assessment",
        "Awake, normal orientation",
        "Mild cognitive impairment, somnolence or insomnia",
        "Somnolent, abnormal behavior but arousable",
        "Stuporous (arousable by strong stimulus)",
        "Coma (unarousable)",
        "Behavior change",
        "Euphoria/depression, decreased attention",
        "Personality change, inappropriate behavior",
        "Marked behavioral disturbance",
        "No autonomous behavior",
        "Intellect and neurological signs",
        "Cognition/intellect",
        "Decreased calculation ability, reduced attention",
        "Disorientation, impaired memory",
        "Severe disorientation",
        "No response",
        "Asterixis",
        "Can be elicited",
        "Often present",
        "Absent (deep coma)",
        "Precipitating factor present",
        "\U0001F4CB West Haven grading criteria",
        "Consciousness",
        "Behavior/intellect",
        "Neurological signs",
        "Grade 0 (minimal HE)",
        "Abnormal psychological or neurophysiological tests",
        "Sleep disturbance, mild cognitive impairment",
        "Euphoria/depression, decreased calculation ability",
        "Asterixis can be elicited",
        "Somnolent, abnormal behavior",
        "Disorientation, personality change",
        "Marked asterixis",
        "Stuporous (arousable by strong stimulus)",
        "Asterixis often present, hyperreflexia",
        "Asterixis absent",
        "Grade 0 (minimal/occult hepatic encephalopathy, MHE) requires psychological tests (number connection test NCT-A/B, symbol digit pattern test) or neurophysiological examination for confirmation.",
        "\U0001F4CA Common precipitating factors",
        "Gastrointestinal bleeding",
        ": sudden ammonia load increase (most common)",
        "Infection",
        ": spontaneous bacterial peritonitis, pneumonia, etc.",
        "Electrolyte disturbance",
        ": hypokalemia, hyponatremia",
        "Constipation",
        ": increased ammonia absorption",
        "Sedative-hypnotic drugs",
        ": benzodiazepines, barbiturates",
        "High-protein diet",
        ": excessive protein load",
        "Excessive diuresis",
        ": dehydration, renal impairment",
        "Note: The West Haven grading is the most commonly used clinical standard. Grade 0 requires special testing to detect. Ammonia levels do not perfectly parallel the grade, but dynamic monitoring helps assess efficacy. Treatment centers on removing precipitants, with lactulose and rifaximin as first-line drugs. For clinical reference only.",
        "\U0001F4DA Deep Dive: Hepatic Encephalopathy West Haven Grading",
        "Grading assessment: take the highest level among consciousness, behavior, cognition, and asterixis to determine the HE grade",
        "Treatment stratification: grade I-II outpatient/day care, grade III-IV hospitalization with ICU",
        "Precipitant management: identify and remove infection, bleeding, constipation, hypokalemia, and other precipitants",
        "Algorithm: consciousness state, behavior change, cognition/intellect, and asterixis each take grade 0~IV (0 normal, I mild, II somnolent/abnormal behavior, III stuporous, IV coma); the highest of the four determines the HE grade. Grade 0 is minimal (MHE), grade I starts lactulose, grade II requires hospitalization, grade III needs ICU monitoring, grade IV needs intubation for airway protection.",
        "Example: consciousness grade 2 (somnolent), behavior grade 2 (markedly abnormal), cognition grade 2 (disoriented), asterixis grade 2 (marked) \u2192 highest grade 2, grade II hepatic encephalopathy; hospitalization, lactulose enema + rifaximin, and correction of precipitants are advised. If consciousness grade 4 (coma) and the rest grade 1 \u2192 highest grade 4, grade IV (coma), critical, requiring ICU, intubation, and urgent liver transplant evaluation.",
        "Does MHE (grade 0) need treatment?",
        "Minimal hepatic encephalopathy has normal labs and imaging, but psychological and neurophysiological tests are abnormal, affecting quality of life and driving safety. Oral lactulose is advised (target 2~3 soft stools/day) with periodic assessment; most cases can be managed as outpatients.",
        "Why is lactulose effective?",
        "Lactulose is fermented by colonic bacteria to produce acid, lowering luminal pH so ammonia is trapped as NH\u2084\u207A and excreted in stool, while also promoting defecation to reduce ammonia absorption; it is foundational therapy for HE at all stages.",
        "About the Hepatic Encephalopathy West Haven Grading Tool",
        "The Hepatic Encephalopathy West Haven grading tool assesses the severity grade of hepatic encephalopathy from consciousness state, behavior, intellect, and neurological signs." + DISCL_M,
    ]))
    write('hp-dob', build('hp-dob', [
        "\U0001FA7B Hp Breath Test DOB Value Interpreter",
        "Enter the DOB value from a \u00B9\u00B3C/\u00B9\u00B4C urea breath test to determine H. pylori infection status.",
        "Hp Breath Test DOB Value Interpreter",
        "/ Hp Breath Test DOB Interpretation",
        "\U0001F4D6 View the Hp Breath Test DOB Value Interpretation Usage Guide",
        "DOB = (post-dose \u00B2\u00B3CO\u2082/\u00B2\u00B3CO\u2082 ratio \u2212 pre-dose) \u00d7 1000",
        "Breath test type",
        "\u00B9\u00B3C-urea breath test",
        "\u00B9\u00B4C-urea breath test",
        "DOB value (\u2030)",
        "PPI used in the last 2 weeks",
        "Antibiotics used in the last 4 weeks",
        "Bismuth used in the last 4 weeks",
        "\U0001F4CB DOB interpretation criteria",
        "\u22654.0 (most standards)",
        "\u00B9\u00B3C-UBT: DOB = (post-dose \u00B2\u00B3CO\u2082/\u00B2\u00B3CO\u2082 ratio \u2212 pre-dose) \u00d7 1000, unit \u2030. The positive threshold may differ slightly by manufacturer reagent (2.0-6.0\u2030).",
        "\U0001F4CA Common causes of false negatives",
        "PPI use",
        ": acid suppression lowers H. pylori load; test after discontinuation \u22652 weeks",
        "Antibiotic use",
        ": inhibits H. pylori growth; test after discontinuation \u22654 weeks",
        "Bismuth use",
        ": affects H. pylori activity; test after discontinuation \u22654 weeks",
        "H2 receptor blockers",
        ": recommend discontinuation \u226524-48 hours",
        "Upper gastrointestinal bleeding",
        ": sensitivity is reduced in the acute phase",
        "Gastric mucosal atrophy",
        ": reduced gastric acid may cause false negatives",
        "Note: The breath test is the preferred non-invasive method for H. pylori detection. Recheck after eradication therapy should be done \u22654 weeks after treatment ends, and PPI should be stopped \u22652 weeks before the recheck. For clinical reference only.",
        "\U0001F4DA Deep Dive: Hp Breath Test DOB Value Interpretation",
        "Infection interpretation: judge negative/positive by threshold from the \u00B9\u00B3C/\u00B9\u00B4C urea breath test DOB value",
        "False negative screening: PPI in the last 2 weeks and antibiotics/bismuth in the last 4 weeks can cause false negatives",
        "Recheck timing: recheck \u22654 weeks after eradication to confirm success",
        "Algorithm: positive threshold DOB \u2265 4.0 (\u00B9\u00B3C unit \u2030, \u00B9\u00B4C unit DPM). <2.0 negative; 2.0~4.0 gray zone/borderline (combine other methods or recheck); \u22654.0 positive. If PPI (\u22652 weeks), antibiotics, or bismuth (\u22654 weeks) were used before testing and DOB<4.0 \u2192 the result is unreliable (possibly a false negative) and retesting after discontinuation is needed; if it is still \u22654.0 during medication \u2192 suggests relatively heavy infection.",
        "Example: DOB 8.5 (\u2030) \u2192 \u22654.0, positive; bismuth quadruple therapy or high-dose dual therapy for eradication is recommended, with recheck \u22654 weeks after completion. If DOB 3.0 \u2192 gray zone (2.0~4.0); combining with stool antigen or rechecking in 2~4 weeks is advised. If DOB 1.5 and PPI was taken within the past week \u2192 the result is unreliable (possibly a false negative); stop PPI for \u22652 weeks then retest.",
        "Are the \u00B9\u00B3C and \u00B9\u00B4C thresholds the same?",
        "Clinical interpretation commonly uses DOB \u2265 4.0 for both, but the units differ (\u00B9\u00B3C in \u2030, \u00B9\u00B4C in DPM), and thresholds vary slightly by manufacturer reagent (some \u00B9\u00B4C use \u2265100 DPM). Follow your own laboratory's reagent instructions.",
        "Why does PPI cause false negatives?",
        "PPI suppresses gastric acid secretion and alters the gastric microenvironment, which can temporarily reduce H. pylori urease activity and bacterial load, lowering the DOB value and causing false negatives. Hence PPI should be stopped \u22652 weeks and antibiotics/bismuth \u22654 weeks before testing.",
        "About the Hp Breath Test DOB Value Interpreter",
        "The H. pylori Hp breath test DOB value interpreter takes the DOB value from a 13C or 14C urea breath test to judge H. pylori infection status and interpret the result." + DISCL_M,
    ]))

if __name__ == '__main__':
    main()

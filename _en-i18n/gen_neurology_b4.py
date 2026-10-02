#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'neurology')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'neurology')
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
    out = {'slug': slug, 'industry': 'neurology', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
#!/usr/bin/env python3

def main():
    # qmg (70)
    write('qmg', build('qmg', [
        "📋 Myasthenia Gravis QMG Quantitative Assessor",
        "Quantitative Myasthenia Gravis (QMG) score, assesses myasthenia gravis (MG) weakness severity; total 0-39, higher = worse",
        "Myasthenia Gravis (QMG) Quantitative Assessor",
        "/ QMG Myasthenia Gravis Quantitative Assessor",
        '📖 View "Myasthenia Gravis QMG Quantitative Assessor Guide"',
        "QMG = sum of items (incl. vital capacity), higher = worse weakness; <=4 minimal, <=9 mild, <=14 moderate, <=19 mod-severe, >19 severe; VC item <2 suggests respiratory involvement, watch for myasthenic crisis.",
        "1. Diplopia (sustained gaze at 30 deg abduction)",
        "0 - No diplopia, sustains 60 sec",
        "1 - Sustains 11-60 sec",
        "2 - Sustains 1-10 sec",
        "3 - Sustains <1 sec or immediate diplopia",
        "2. Ptosis (sustained eye opening looking up)",
        "0 - Sustains >=61 sec",
        "3 - Sustains <1 sec",
        "3. Facial weakness (eyelid closure strength)",
        "0 - Normal closure, lashes fully buried",
        "1 - Can close but lashes exposed",
        "2 - Incomplete closure, sclera visible",
        "3 - Cannot close eyes",
        "4. Dysphagia (200mL water timed)",
        "0 - Normal (no choking)",
        "1 - Mild difficulty (occasional choking)",
        "2 - Moderate difficulty (marked choking/nasal reflux)",
        "3 - Severe difficulty (cannot swallow / needs tube feeding)",
        '5. Dysarthria (timed "1001" counting)',
        "0 - Clear, no nasal",
        "1 - Mild nasal / slurred",
        "2 - Moderate nasal",
        "3 - Severe nasal / hard to understand",
        "6. Right arm abduction (sustained hold)",
        "0 - >=240 sec",
        "1 - 120-239 sec",
        "2 - 30-119 sec",
        "3 - <30 sec",
        "7. Left arm abduction (sustained hold)",
        "8. Grip - right hand (sex-specific thresholds)",
        "0 - >=15 lb (F)/>=25 lb (M)",
        "1 - 10-14 lb (F)/15-24 lb (M)",
        "2 - 5-9 lb (F)/5-14 lb (M)",
        "3 - <5 lb",
        "9. Grip - left hand",
        "10. Vital capacity (VC, sitting)",
        "0 - >=3000 mL (M)/>=2000 mL (F)",
        "1 - 2500-2999 mL (M)/1500-1999 mL (F)",
        "2 - 2000-2499 mL (M)/1000-1499 mL (F)",
        "3 - <2000 mL (M)/<1000 mL (F)",
        "11. Right hip flexion (sustained hold)",
        "12. Left hip flexion (sustained hold)",
        "📋 QMG Grading Standard",
        "MGFA classification reference",
        "Minimal",
        "Type I (ocular) / IIa",
        "IIa-IIb",
        "IIb-IIIa",
        "IIIa-IIIb",
        "IV-V",
        "Clinical application:",
        "QMG is the primary efficacy endpoint in MG trials; a drop >=3.5 (MCID) is clinically meaningful. Used to assess immunotherapy (corticosteroids, IVIG, plasmapheresis, immunosuppressants, biologics like eculizumab/rozanolixizumab). VC <1500 mL suggests respiratory muscle involvement, watch for myasthenic crisis.",
        "📚 In-depth: QMG Myasthenia Gravis Quantitative Scale",
        "MG ocular-facial, bulbar, limb and respiratory muscle scoring.",
        "Treatment response assessment.",
        "Respiratory function (VC item) warning.",
        "12 items total 18 (max 39), with VC (q10) reduced: suggests bulbar/respiratory involvement, watch for crisis.",
        "Total 6: mainly extraocular muscles, mild generalized.",
        "Total score?",
        "12 items each 0-3, max 39; higher = worse.",
        "Vital capacity item?",
        "Reflects respiratory muscles; drop suggests myasthenic crisis risk, needs urgent care.",
        "About the Myasthenia Gravis (QMG) Quantitative Assessor",
        "QMG myasthenia gravis quantitative assessor, based on the Quantitative Myasthenia Gravis Score, assesses weakness severity in myasthenia gravis (MG) patients. A medical professional tool based on authoritative medical standards, for reference only.",
    ]))

    # rater-18 (26)
    write('rater-18', build('rater-18', [
        "✅ Stroke (NIHSS) Score",
        "The NIHSS (National Institutes of Health Stroke Scale) is the gold standard for assessing acute stroke neurological deficit severity, with 15 items, total 0-42, higher = worse deficit.",
        '📖 View "Stroke (NIHSS) Score Guide"',
        "NIHSS total = sum of 15 neurological items, max 42; 0 no stroke symptoms, <=1 minimal, <=4 mild, <=15 moderate, <=20 mod-severe, >20 severe; higher = worse deficit.",
        "NIHSS should be performed by trained raters, as early as possible",
        "Score by first response, no repeated instruction",
        "0-1 minimal 2-4 mild 5-15 moderate 16-20 mod-severe 21-42 severe",
        "NIHSS is an important reference for thrombolysis decisions",
        "📚 In-depth: NIHSS Neurological Score (42-point scale)",
        "Comprehensive stroke neurological deficit score.",
        "Reperfusion treatment indication reference.",
        "Tracked alongside other rater-series scores.",
        "13 items total 9 /42: moderate deficit (5-15), assess thrombolysis/thrombectomy.",
        "Total 25 /42: severe, poorer prognosis, intensify monitoring.",
        "Upper limit?",
        "Max 42, higher = worse deficit.",
        "Relation to NIHSS?",
        "Implementation of the same NIHSS scale, identical scoring criteria.",
        "About the Stroke (NIHSS) Score",
        "NIHSS is an internationally used stroke neurological deficit scale, with 15 items (consciousness, gaze, vision, facial palsy, motor, ataxia, sensation, language, dysarthria, neglect), total 0-42, widely used for acute stroke severity, thrombolysis decisions and prognosis.",
        "15-item standardized NIHSS assessment",
        "Dynamically generated score options",
        "Acute stroke severity assessment",
        "Thrombolysis/thrombectomy treatment decisions",
        "Stroke treatment efficacy monitoring",
        "Stroke prognosis judgment",
    ]))

    # rater-19 (25)
    write('rater-19', build('rater-19', [
        "✅ Parkinson's (UPDRS) Motor Score",
        "The UPDRS Motor Examination (Part III) is the core scale for Parkinson's motor symptoms, 14 items each 0-4, total 0-56. Should be assessed separately in 'on' and 'off' medication states.",
        '📖 View "Parkinson\'s (UPDRS) Motor Score Guide"',
        "UPDRS Part III total = sum of 14 items (each 0-4), max 56; <=10 mild, <=20 moderate, <=30 mod-severe, >30 severe motor impairment; assess in on/off states.",
        "0=normal 1=slight 2=mild 3=moderate 4=severe",
        'UPDRS motor assessment should be done in "on" or "off" medication states separately',
        "Recommended to be performed by trained neurologists",
        "0-10 mild 11-20 moderate 21-30 mod-severe >30 severe",
        "Important basis for medication adjustment and DBS surgery indication",
        "📚 In-depth: Composite Motor Score (56-point scale)",
        "Multi-dimensional motor function score (0-56).",
        "Parkinson's and other movement disorder assessment.",
        "Before-after treatment comparison.",
        "Marked impairment",
        "14 items total 30 /56: marked motor impairment, suggests mod-severe involvement.",
        "Total 8 /56: mild, follow-up observation.",
        "Max score?",
        "56-point scale, higher = worse motor impairment.",
        "Use?",
        "Same concept as UPDRS Part III motor scale, suitable for longitudinal follow-up.",
        "About the Parkinson's (UPDRS) Motor Score",
        "UPDRS Motor Examination covers 14 items (speech, rigidity, tremor, bradykinesia, postural stability), each 0-4, total 0-56. It is an important basis for PD medication adjustment and DBS surgery evaluation.",
        "14-item standardized motor assessment",
        "Parkinson's motor symptom assessment",
        "Medication efficacy judgment",
    ]))

    # rater-21 (60)
    write('rater-21', build('rater-21', [
        "✅ Dystonia (TWSTRS) Score",
        "TWSTRS is a standardized scale for cervical dystonia (spasmodic torticollis), with severity, disability and pain subscales, total 0-75.",
        '📖 View "Dystonia (TWSTRS) Score Guide"',
        "TWSTRS cervical dystonia total = severity (6 items) + disability (4 items) + pain score; pain score = min(20, pain severity + duration x2 + pain disability), max 75; <=20 mild, <=40 moderate, <=60 mod-severe, >60 severe.",
        "I. Severity scale",
        "Head rotation deviation",
        "1 - 1-15 degrees",
        "2 - 16-30 degrees",
        "3 - >30 degrees",
        "Head lateral tilt deviation",
        "Head anteroposterior deviation",
        "Deviation duration (1 minute)",
        "1 - occasional (1-25%)",
        "2 - frequent (26-50%)",
        "3 - constant (>50%)",
        "Shoulder elevation/protraction",
        "1 - slight",
        "2 - marked",
        "3 - severe",
        "Head tremor amplitude",
        "1 - slight (1-25%)",
        "2 - moderate (26-50%)",
        "3 - severe (>50%)",
        "II. Disability scale",
        "Work/housework ability",
        "0 - no effect",
        "1 - mild",
        "2 - moderate",
        "Driving/travel",
        "Reading/writing",
        "Social/dining out",
        "III. Pain scale",
        "Neck pain severity (0-10)",
        "Pain duration (days/week)",
        "0 - no pain",
        "1 - occasional (1-2 days)",
        "2 - frequent (3-5 days)",
        "3 - constant (6-7 days)",
        "Pain-caused activity limitation (0-10)",
        "TWSTRS is mainly used for cervical dystonia (spasmodic torticollis) assessment",
        "Severity scale needs 1-minute observation with patient seated and relaxed",
        "0-20 mild 21-40 moderate 41-75 severe",
        "Important tool for botulinum toxin efficacy assessment and DBS surgery indication",
        "📚 In-depth: Composite Tic Score (75-point scale)",
        "Composite score of motor/vocal tic number, frequency, intensity, interference.",
        "Tic disorder severity assessment.",
        "Medication/behavioral therapy follow-up.",
        "Number+frequency+intensity/interference total 45 /75: moderate-severe tic burden.",
        "Total 18 /75: mild, mainly simple tics.",
        "Max score?",
        "75-point scale (with number, frequency, intensity and interference sub-caps), higher = worse.",
        "Intensity item cap?",
        "Intensity/interference capped per rules to avoid single-dimension amplification.",
        "About the Dystonia (TWSTRS) Score",
        "TWSTRS includes severity, disability and pain subscales, total 0-75, used to assess cervical dystonia motor abnormality, functional impact and pain.",
        "3-subscale composite assessment",
        "Multi-dimensional motor abnormality score",
        "Pain and disability quantification",
        "Spasmodic torticollis severity assessment",
        "Botulinum toxin efficacy judgment",
    ]))

    # rater-22 (27)
    write('rater-22', build('rater-22', [
        "✅ Ataxia (SARA) Score",
        "SARA is an international standard scale for cerebellar ataxia severity, with 8 items, total 0-40. Gait assessment requires walking 10 m on flat ground (incl. turn).",
        '📖 View "Ataxia (SARA) Score Guide"',
        "SARA cerebellar ataxia total = sum of 8 items (gait/stance/sit/speech/finger-nose/heel-knee-shin/alternating/heel-shin slide), max 40; <=3 mild, <=8 mild-moderate, <=15 moderate, <=30 severe, >30 extremely severe.",
        "SARA applies to all types of cerebellar ataxia assessment",
        "Gait assessment needs 10 m walk on flat ground (incl. turn)",
        "0-3 mild 4-8 mild-moderate 9-15 moderate 16-30 severe >30 extremely severe",
        "Often used for disease progression monitoring and clinical trial efficacy",
        "📚 In-depth: Ataxia Score (40-point scale)",
        "Cerebellar ataxia multi-movement score (0-40).",
        "Spinocerebellar degeneration assessment.",
        "Rehabilitation and medication follow-up.",
        "Marked ataxia",
        "8 movements total 22 /40: marked ataxia, gait and finger-nose heavily involved.",
        "Total 8 /40: mild, mainly fine-movement instability.",
        "Max score?",
        "40-point scale (gait 8, stance 6, sit 4, speech 6, others 4 each), higher = worse.",
        "Relation to SARA?",
        "Same spinocerebellar ataxia assessment approach, consistent item weights.",
        "About the Ataxia (SARA) Score",
        "SARA includes 8 items (gait, stance, sit, speech, pursuit, nose-finger test, alternating movements), total 0-40, widely used for hereditary ataxia staging, efficacy and progression monitoring.",
        "8-item standardized SARA assessment",
        "5-level severity grading",
        "Cerebellar ataxia severity assessment",
        "Hereditary ataxia progression monitoring",
        "Rehabilitation efficacy assessment",
        "Clinical trial data collection",
    ]))

    # rls-severity (26)
    write('rls-severity', build('rls-severity', [
        "🧠 Restless Legs RLS Severity Assessor",
        "International Restless Legs Syndrome Rating Scale (IRLS), assesses RLS symptom severity; total 0-40",
        "Restless Legs (RLS) Severity Assessor",
        "/ RLS Restless Legs Severity Assessor",
        '📖 View "Restless Legs RLS Severity Assessor Guide"',
        "Each item 0-4: none (0), mild (1), moderate (2), severe (3), very severe (4)",
        "📋 IRLS Grading Standard",
        "No treatment needed",
        "Non-drug treatment, iron supplement",
        "Dopamine agonists / gabapentinoids",
        "Medication, monitor ferritin regularly",
        "Comprehensive drug management, screen worsening factors",
        "Clinical application:",
        "IRLS is the gold standard for RLS severity. Check serum ferritin before treatment (<75 ug/L needs iron). First-line: dopamine agonists (pramipexole/ropinirole) or alpha2delta ligands (gabapentin/pregabalin). Note: long-term dopamine use may worsen symptoms (augmentation), reassess regularly. Avoid antihistamines, SSRIs/SNRIs that may aggravate RLS.",
        "📚 In-depth: IRLS Restless Legs Severity",
        "RLS symptoms, sleep and daytime function scoring.",
        "Iron deficiency / drug-induced secondary screening.",
        "Dopaminergic treatment follow-up.",
        "10 items total 24 (max 40): severe, nocturnal symptoms significantly disturb sleep.",
        "Total 9: mild, occasional.",
        "Grading?",
        "0 none; mild 1-10, moderate 11-20, severe 21-30, very severe 31-40.",
        "Notes?",
        "Rule out cramps/postural discomfort, watch ferritin and renal function.",
        "About the Restless Legs (RLS) Severity Assessor",
        "RLS restless legs severity assessor, based on the International Restless Legs Syndrome Rating Scale (IRLS), assesses RLS symptom severity, with 10 items. A medical professional tool based on authoritative medical standards, for reference only.",
    ]))

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'psychiatry')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'psychiatry')
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
    out = {'slug': slug, 'industry': 'psychiatry', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('panss-schizophrenia', build('panss-schizophrenia', [
        "💭 Positive and Negative Syndrome Scale (PANSS)",  # 0
        "Positive and Negative Syndrome Scale (PANSS) scoring calculator for clinicians to rate 30 symptom items (1-7). Subscales: Positive P (7), Negative N (7), General G (16); total 30-210. PANSS is a clinician-rated scale requiring training.",  # 1
        "PANSS total = positive (7) + negative (7) + general psychopathology (7); composite = positive - negative; <=57 none/minimal, 58-74 mild, 75-95 moderate, >=96 marked/severe.",  # 2
        "Rating: 1=none 2=minimal 3=mild 4=moderate 5=mod-severe 6=severe 7=extreme",  # 3
        "PANSS Total Severity Reference",  # 4
        "Marked/severe",  # 5
        "This is a calculation aid for a clinician-rated scale and does not replace psychiatric diagnosis. PANSS must be rated by trained clinicians based on interview and observation.",  # 6
        "📚 Deep Dive: PANSS Schizophrenia Symptoms",  # 7
        "Positive symptoms",  # 8
        "Negative symptoms",  # 9
        "General psychopathology",  # 10
        "Total 77",  # 11
        "30 items each 1-7: positive 7 sum 21 (P1-P7), negative 7 sum 18 (N1-N7), general 16 sum 38 -> total 77, positive-negative diff = 3, slightly higher positive.",  # 12
        "Negative-dominant 64",  # 13
        "Positive 16, negative 24, general 24 -> 64, negative factor prominent, implying prognosis and cognitive rehab need focus.",  # 14
        "How are subscales computed?",  # 15
        "Positive = P1-P7, negative = N1-N7, general = G1-G16; higher total means worse symptoms; often paired with CGI for efficacy.",  # 16
        "Notes before rating?",  # 17
        "A certified rater must score 1-7 by anchored descriptions based on the past week, avoiding influence from patient cooperation.",  # 18
        "About the Positive and Negative Syndrome Scale (PANSS)",  # 19
        "Positive and Negative Syndrome Scale (PANSS). A medical professional tool based on authoritative medical standards, for reference only.",  # 20
    ]))
    write('pcl5-ptsd', build('pcl5-ptsd', [
        "🔍 PTSD Checklist (PCL-5)",  # 0
        "PTSD Checklist for DSM-5 (PCL-5) is a self-report on reactions to the worst traumatic event in the past month. 20 items, 0-4 each, total 0-80. Cutoff 31-33 suggests possible PTSD.",  # 1
        "PCL-5 total = sum of 20 items (0-4, max 80); clustered as B re-experiencing, C avoidance, D negative cognition, E hyperarousal; higher total means worse PTSD symptoms.",  # 2
        "PCL-5 DSM-5 Symptom Clusters",  # 3
        "Symptom cluster",  # 4
        "B Intrusive symptoms",  # 5
        "At least 1 item",  # 6
        "C Avoidance",  # 7
        "D Negative alterations in cognition/mood",  # 8
        "At least 2 items",  # 9
        "E Alterations in arousal/reactivity",  # 10
        "This is a self-help screening tool and does not replace psychiatric diagnosis. PCL-5 >=31 suggests further professional trauma assessment.",  # 11
        "📚 Deep Dive: PCL-5 Post-Traumatic Stress",  # 12
        "PTSD screening",  # 13
        "DSM-5 clusters",  # 14
        "Symptom follow-up",  # 15
        "Total 38 and DSM-met",  # 16
        "20 items 0-4: B intrusion 5 sum 9 (>=1 >0), C avoidance 2 sum 4 (>=1), D negative 7 sum 14 (>=2), E arousal 6 sum 11 (>=2) -> total 38, meets DSM clusters and >=31, likely PTSD.",  # 17
        "Below criteria 22",  # 18
        "Total 22 but some cluster short on items -> does not meet DSM criteria; follow-up and psychoeducation advised.",  # 19
        "Criteria?",  # 20
        "Commonly total >=31 and B/C/D/E each meet minimum items (B>=1, C>=1, D>=2, E>=2) indicates DSM-5 positive screen.",  # 21
        "Aligned with DSM-5?",  # 22
        "PCL-5 maps to the four DSM-5 clusters; useful for screening but not standalone diagnosis; clinical interview must confirm trauma exposure.",  # 23
        "About the PTSD Checklist (PCL-5)",  # 24
        "PTSD Checklist (PCL-5). A medical professional tool based on authoritative medical standards, for reference only.",  # 25
    ]))
    write('pdss-panic', build('pdss-panic', [
        "💭 Panic Disorder Severity Scale (PDSS)",  # 0
        "Panic Disorder Severity Scale (PDSS) self-report rates frequency, distress and functional impact of panic attacks over the past week. 7 items, 0-4 each, total 0-28. Total >=8 suggests clinically significant panic disorder.",  # 1
        "PDSS severity = sum of 7 items (0-4, max 28); mean = total / 7; <=3 subclinical, 4-7 mild, 8-13 moderate, >=14 severe.",  # 2
        "PDSS Severity Levels",  # 3
        "Mild symptoms",  # 4
        "Monitor; follow up if needed",  # 5
        "Professional assessment and treatment advised",  # 6
        "Active medication + psychotherapy (CBT) needed",  # 7
        "This is a self-help screening tool and does not replace psychiatric diagnosis. First-line treatment for panic disorder is CBT and SSRIs.",  # 8
        "📚 Deep Dive: PDSS Panic Disorder Severity",  # 9
        "Panic attack frequency",  # 10
        "Anticipatory anxiety",  # 11
        "Avoidance behavior",  # 12
        "Total 8 (subthreshold)",  # 13
        "7 dimensions each 0-4: attack frequency 1, distress 1, anticipatory anxiety 1, agoraphobia 1, situational avoidance 1, within-attack fear 2, impairment 1 -> total 8, near clinical cutoff; monitoring advised.",  # 14
        "Severe 18",  # 15
        "Dimensions 3-4 sum 18, severe; needs systematic medication + psychotherapy and comorbidity workup.",  # 16
        "Positive cutoff?",  # 17
        "Commonly total >=8 warrants attention, >=14 mostly moderate-severe; but combine with clinical interview, not score alone.",  # 18
        "Difference from panic scales?",  # 19
        "PDSS is severity-oriented; it can pair with panic-related cognition self-rating (e.g. ACQ) to assess cognitive features.",  # 20
        "About the Panic Disorder Severity Scale (PDSS)",  # 21
        "Panic Disorder Severity Scale (PDSS). A medical professional tool based on authoritative medical standards, for reference only.",  # 22
    ]))
    write('phq15-somatization', build('phq15-somatization', [
        "🧠 Somatic Symptom Scale (PHQ-15)",  # 0
        "Patient Health Questionnaire somatic module (PHQ-15) rates bother from 15 somatic symptoms over the past month. Each 0-2, total 0-30; >=10 suggests moderate-severe somatic symptoms, further assessment advised.",  # 1
        "PHQ-15 total = sum of 15 somatic items (0-2, max 30); <=4 minimal, 5-9 low, 10-14 medium, >=15 high somatic distress.",  # 2
        "PHQ-15 Severity Levels",  # 3
        "No notable somatization",  # 4
        "Mild somatic symptoms, monitor",  # 5
        "Further medical and psychological assessment advised",  # 6
        "Clear somatization, integrated intervention needed",  # 7
        "This is a self-help screening tool and does not replace medical exams or psychiatric diagnosis. Rule out organic disease first, then consider psychosomatic factors.",  # 8
        "📚 Deep Dive: PHQ-15 Somatization",  # 9
        "Somatic symptom burden",  # 10
        "Psychosomatic comorbidity",  # 11
        "Follow-up change",  # 12
        "Total 12 (medium)",  # 13
        "15 items 0-2 (none/some/a lot): GI 2, fatigue 2, pain 2, dizziness 1, palpitations 1, dyspnea 1, back pain 1, chest pain 1, other 1 = 12, moderate somatic burden.",  # 14
        "Mild 5",  # 15
        "Total 5, mild; note triggers and emotional links.",  # 16
        "Severity levels?",  # 17
        "0-4 mild, 5-9 medium, 10-15 severe; high scores suggest ruling out organic causes and checking depression/anxiety comorbidity.",  # 18
        "What is it for?",  # 19
        "Used in primary care to identify somatization and psychosomatic disorders; not a substitute for specialist exam.",  # 20
        "About the Somatic Symptom Scale (PHQ-15)",  # 21
        "Somatic Symptom Scale (PHQ-15). A medical professional tool based on authoritative medical standards, for reference only.",  # 22
    ]))
    write('phq9-depression', build('phq9-depression', [
        "📋 Depression Scale (PHQ-9)",  # 0
        "Self-rate 9 depressive symptom items based on feelings over the past two weeks to screen depression severity. 9 items, 0-3 each.",  # 1
        "PHQ-9 total = sum of 9 items (0-3, max 27); <=4 none, 5-9 mild, 10-14 moderate, 15-19 mod-severe, 20-27 severe.",  # 2
        "PHQ-9 Severity Levels",  # 3
        "Consider psychotherapy/medication",  # 4
        "Immediate medication and suicide-risk assessment",  # 5
        "This is a self-help screening tool and does not replace psychiatric diagnosis. If item 9 (self-harm thoughts) has any score, or you feel distressed, seek professional psychological/psychiatric help immediately.",  # 6
        "📚 Deep Dive: PHQ-9 Depression Scale",  # 7
        "Depression severity",  # 8
        "Core symptoms",  # 9
        "Suicide risk",  # 10
        "Total 17 (mod-severe)",  # 11
        "9 items 0-3: 2,2,2,2,2,2,2,1,2 = 17, mod-severe; core items (interest/mood) >=2 and >=5 items >=2 meet DSM threshold; item 9 >0 needs suicide assessment.",  # 12
        "Mild 6",  # 13
        "Mostly 1 each: total 6, mild; psychoeducation and follow-up advised.",  # 14
        "Relation to calc-1?",  # 15
        "Both are PHQ-9 implementations; this page is the scale version, calc-1 is its calculator; scoring rules are identical.",  # 16
        "How is DSM met?",  # 17
        ">=5 items at >=2 days/week and interest or mood core >=2 meets depressive-episode symptom threshold (duration and function still needed).",  # 18
        "About the Depression Scale (PHQ-9)",  # 19
        "Depression Scale (PHQ-9). A medical professional tool based on authoritative medical standards, for reference only.",  # 20
        "How to use the Depression Scale (PHQ-9)",  # 21
        "What does the Depression Scale (PHQ-9) do?",  # 22
        "How do I use the Depression Scale (PHQ-9)?",  # 23
        "When is the Depression Scale (PHQ-9) useful?",  # 24
        "Total and severity",  # 25
        "PHQ-9 total 0-27, sum of 9 symptom frequencies (0 not at all to 3 nearly every day):",  # 26
        "None/minimal depression;",  # 27
        "Mild;",  # 28
        "Moderate;",  # 29
        "Moderately severe;",  # 30
        "Severe.",  # 31
        "Key attention to item 9",  # 32
        "Item 9 ('self-harm/thoughts of death') if >=1, regardless of total, needs priority attention and prompt medical assessment; symptoms persisting >=2 weeks warrant a visit.",  # 33
        "Scope and limits",  # 34
        "This is a self-report screening tool and does not replace psychiatric diagnosis; severity thresholds are clinical references; individual differences and somatic illness need comprehensive judgment.",  # 35
    ]))


if __name__ == '__main__':
    main()

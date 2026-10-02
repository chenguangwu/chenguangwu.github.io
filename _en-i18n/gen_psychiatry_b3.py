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
    write('isi-insomnia', build('isi-insomnia', [
        "😴 Insomnia Severity Index (ISI)",  # 0
        "Insomnia Severity Index (ISI) assesses the nature and severity of insomnia symptoms over the past two weeks. 7 items, 0-4 each, total 0-28.",  # 1
        "ISI = sum of 7 items (0-4 each, max 28); <=7 no insomnia, 8-14 subthreshold, 15-21 moderate, 22-28 severe.",  # 2
        "ISI Severity Levels",  # 3
        "No insomnia",  # 4
        "Sleep is good",  # 5
        "Subthreshold insomnia",  # 6
        "Attend to sleep hygiene, intervene if needed",  # 7
        "Moderate insomnia",  # 8
        "Seek medical evaluation; CBT-I advised",  # 9
        "Severe insomnia",  # 10
        "Needs active treatment",  # 11
        "This is a self-help screening tool and does not replace sleep-medicine diagnosis. For chronic insomnia, see a sleep clinic.",  # 12
        "📚 Deep Dive: ISI Insomnia Severity",  # 13
        "Sleep-onset difficulty",  # 14
        "Satisfaction",  # 15
        "Daytime impairment",  # 16
        "Total 14 (moderate)",  # 17
        "7 items 0-4: onset 2, maintenance 2, early-wake 2, satisfaction 2, interference 2, noticeability 2, impairment 2 = 14, moderate insomnia; sleep hygiene + CBT-I advised.",  # 18
        "Severe 21",  # 19
        "Several 3-4 items total 21, severe, with marked daytime impairment; needs a specialist insomnia clinic.",  # 20
        "Severity levels?",  # 21
        "0-7 none, 8-14 mild, 15-21 moderate, 22-28 extreme; combine total with daytime impairment to set intervention intensity.",  # 22
        "What is CBT-I?",  # 23
        "Cognitive Behavioral Therapy for Insomnia, first-line non-drug therapy, including stimulus control, sleep restriction and cognitive restructuring.",  # 24
        "About the Insomnia Severity Index (ISI)",  # 25
        "Insomnia Severity Index (ISI). A medical professional tool based on authoritative medical standards, for reference only.",  # 26
        "How to use the Insomnia Severity Index (ISI)",  # 27
        "What does the Insomnia Severity Index (ISI) do?",  # 28
        "How do I use the Insomnia Severity Index (ISI)?",  # 29
        "When is the Insomnia Severity Index (ISI) useful?",  # 30
        "Total score and levels",  # 31
        "Insomnia Severity Index (ISI) total 0-28, sum of 7 items:",  # 32
        "No clinically significant insomnia;",  # 33
        "Subthreshold insomnia;",  # 34
        "Moderate clinical insomnia;",  # 35
        "Severe clinical insomnia.",  # 36
        "Used to screen insomnia severity and track treatment response; rising scores signal worse sleep onset/maintenance difficulty and daytime impairment.",  # 37
        "Scope and limits",  # 38
        "ISI is a self-report screen; its thresholds are common references. Confirmation and treatment need a sleep specialist with polysomnography etc.",  # 39
    ]))
    write('les-stress', build('les-stress', [
        "📚 Life Events Scale (LES) Stress Assessment",  # 0
        "Life Events Stress Scale (based on the Holmes-Rahe Social Readjustment Rating Scale, SRRS): check life events experienced in the past 12 months; it accumulates Life Change Units (LCU) and assesses stress-related health risk.",  # 1
        "Life-event stress total = sum of event weights; <150 low risk (serious-illness risk ~30%), 150-299 medium (~50%), >=300 high (~80%).",  # 2
        "Accumulated stress value",  # 3
        "Stress Health-Risk Levels",  # 4
        "LCU total",  # 5
        "Recent serious-illness risk",  # 6
        "About 30%",  # 7
        "About 50%",  # 8
        "About 80%",  # 9
        "This is a self-help stress reference; 'health risk' reflects group statistics, not individual prediction. Under high stress, strengthen self-care, social support and professional help when needed.",  # 10
        "📚 Deep Dive: LES Life-Event Stress",  # 11
        "Negative events",  # 12
        "Positive events",  # 13
        "Accumulated stress value",  # 14
        "Accumulated 220",  # 15
        "Check past-year events and sum weights: spouse loss 100, job loss 47, family conflict 35, health decline 38 -> about 220, high life-event load; mind psychosomatic health.",  # 16
        "Low load 60",  # 17
        "Only marriage/love 50 + minor change 10 -> 60, lower stress load.",  # 18
        "How is it scored?",  # 19
        "Each event has a fixed stress weight (positive/negative); checked items sum to the total; higher means more recent life change.",  # 20
        "What is it for?",  # 21
        "Used in psychosomatic medicine and stress research to flag links between recent life change and onset/relapse risk; not a diagnosis.",  # 22
        "About the Life Events Scale (LES) Stress Assessment",  # 23
        "Life Events Scale (LES) Stress Assessment. A medical professional tool based on authoritative medical standards, for reference only.",  # 24
    ]))
    write('lsas-social', build('lsas-social', [
        "📋 Liebowitz Social Anxiety Scale (LSAS)",  # 0
        "Liebowitz Social Anxiety Scale (LSAS) rates fear and avoidance across 24 social/performance situations. Each item has fear (0-3) and avoidance (0-3); total 0-144. Total >60 suggests possible social anxiety disorder.",  # 1
        "LSAS total = sum of fear + sum of avoidance (each item 0-3); fear 11 items, avoidance 11 items; higher total means worse social anxiety.",  # 2
        "LSAS Severity Levels (total 0-144)",  # 3
        "None/mild",  # 4
        "Marked",  # 5
        "This is a self-help screening tool and does not replace psychiatric diagnosis. First-line treatment for social anxiety disorder is CBT and SSRIs.",  # 6
        "📚 Deep Dive: LSAS Social Anxiety",  # 7
        "Fear dimension",  # 8
        "Avoidance dimension",  # 9
        "Performance vs social type",  # 10
        "Total 64",  # 11
        "24 situations each rated fear (0-3) and avoidance (0-3): fear 36, avoidance 28 -> total 64, severe social anxiety; performance 13 items, social 11 items can be viewed separately.",  # 12
        "Mild 30",  # 13
        "Fear 18 + avoidance 12 = 30, mild; self-help exposure practice can start first.",  # 14
        "Subscales?",  # 15
        "Fear and avoidance subscales each 0-72, total 0-144; splitting performance vs social helps locate anxiety situation types.",  # 16
        "Interpretation cutoff?",  # 17
        "Commonly >=30 mild, >=60 moderate-severe, >=80 severe, but must be combined with clinical judgment.",  # 18
        "About the Liebowitz Social Anxiety Scale (LSAS)",  # 19
        "Liebowitz Social Anxiety Scale (LSAS). A medical professional tool based on authoritative medical standards, for reference only.",  # 20
    ]))
    write('mdq-bipolar', build('mdq-bipolar', [
        "🔍 Mood Disorder Questionnaire (MDQ)",  # 0
        "Mood Disorder Questionnaire (MDQ) screens for bipolar disorder. Part 1 has 13 yes/no questions, Part 2 checks if they occurred in the same period, Part 3 rates how much they bothered functioning. All three criteria met suggests a positive screen.",  # 1
        "MDQ bipolar screen: (1) >=7 of 13 affirmative, (2) no past mixed episodes, (3) impact on >=2 areas; all three together indicate a positive screen.",  # 2
        "MDQ Positive Criteria (all required)",  # 3
        "Part 1",  # 4
        ">=7 'yes' (of 13 items)",  # 5
        "Part 2",  # 6
        "Select 'yes' (symptoms co-occurred)",  # 7
        "Part 3",  # 8
        "Select 'moderate' or 'severe' problem",  # 9
        "This is a self-help screening tool and does not replace psychiatric diagnosis. MDQ positive suggests further professional mood-disorder assessment.",  # 10
        "📚 Deep Dive: MDQ Bipolar Screening",  # 11
        "Recognizing elevated mood",  # 12
        "Comorbidity differentiation",  # 13
        "Pre-medication assessment",  # 14
        "Part 1: 8 of 13 'yes' (>=7); Part 2: 'problems caused by mood = yes'; Part 3 severity >=2 -> all three met, positive screen, possible bipolar.",  # 15
        "Part 1 only 5 'yes' or latter two not met -> negative, but persistent low mood still needs unipolar-depression workup.",  # 16
        "The three criteria?",  # 17
        "Part 1 >=7 'yes', symptoms co-sourced from mood, and functional impact >= moderate; all three required for positive.",  # 18
        "Are false positives common?",  # 19
        "MDQ specificity is modest; ADHD/borderline personality etc. can yield false positives; a positive must be confirmed by psychiatry for the bipolar spectrum.",  # 20
        "About the Mood Disorder Questionnaire (MDQ)",  # 21
        "Mood Disorder Questionnaire (MDQ). A medical professional tool based on authoritative medical standards, for reference only.",  # 22
    ]))
    write('mmpi2-personality', build('mmpi2-personality', [
        "🧠 Minnesota Multiphasic Personality Inventory-2 (MMPI-2)",  # 0
        "Minnesota Multiphasic Personality Inventory-2 (MMPI-2) clinical-scale T-score interpretation reference. Enter each clinical scale's T-score (standardized); it auto-reads elevation level and gives reference interpretation. T-score has mean 50, SD 10.",  # 1
        "MMPI-2: each clinical scale T-score (default 50, >=65 elevated); more elevated scales and higher peak T suggest a more notable profile.",  # 2
        "Interpretation",  # 3
        "T-score elevation level",  # 4
        "T-score",  # 5
        "No notable elevation",  # 6
        "Subclinical, needs context",  # 7
        "Suggests related traits/symptoms",  # 8
        "Clear pathological significance",  # 9
        "MMPI-2 must be administered and interpreted by professionals; this tool only gives reference reading of T-score elevation and does not replace clinical personality assessment or diagnosis.",  # 10
        "📚 Deep Dive: MMPI-2 Clinical Scales",  # 11
        "Scale profile",  # 12
        "Elevated items",  # 13
        "Validity scales",  # 14
        "Hypochondriasis scale T70",  # 15
        "Clinical scale (e.g. Hypochondriasis Hs) raw-to-T conversion = 70 (>65 elevated), suggesting prominent somatic concern; first check validity scales (e.g. F, L) to rule out response bias.",  # 16
        "Multiple scales elevated",  # 17
        "Depression D, Hysteria Hy, Paranoia Pa all T>65 -> a 'neurotic' profile; interpret with interview.",  # 18
        "How to read T-scores?",  # 19
        "Clinical-scale normative T-scores, >65 taken as elevated; must combine validity scales (F authenticity, L defensiveness, K denial) to judge credibility.",  # 20
        "Can I self-diagnose?",  # 21
        "No; MMPI-2 needs trained interpreters for the profile combination; avoid concluding from a single scale.",  # 22
        "About the Minnesota Multiphasic Personality Inventory-2 (MMPI-2)",  # 23
        "Minnesota Multiphasic Personality Inventory-2 (MMPI-2). A medical professional tool based on authoritative medical standards, for reference only.",  # 24
    ]))


if __name__ == '__main__':
    main()

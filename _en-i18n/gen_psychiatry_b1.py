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
    write('aq-autism', build('aq-autism', [
        "📋 Autism Spectrum Quotient (AQ) Self-Assessment",  # 0
        "Autism Spectrum Quotient (AQ, Baron-Cohen 2001) screens autistic traits in individuals aged 16+ with average intelligence. 50 items, 4-point scale, total 0-50. Score >=32 suggests clinically significant autistic traits; 26-31 indicates broad autism phenotype.",  # 1
        "AQ = sum of 50 item scores, broken into factors: social skill, communication, imagination, attention switching and attention to detail; higher scores indicate more pronounced autistic traits.",  # 2
        "AQ Severity Levels and Subscales",  # 3
        "Low autistic traits",  # 4
        "Broad phenotype",  # 5
        "Broad autism phenotype, monitoring suggested",  # 6
        "Suggests clinically significant autistic traits, professional evaluation advised",  # 7
        "This scale is a self-help screening tool and does not replace developmental-behavioral or psychiatric diagnosis. AQ screens only; confirmation requires developmental history and clinical assessment.",  # 8
        "📚 Deep Dive: AQ and the Autism Spectrum",  # 9
        "Social communication",  # 10
        "Attention switching",  # 11
        "Imagination and detail",  # 12
        "Total 32 (positive)",  # 13
        "50 items scored forward/reverse per FWD: total 32 >= cutoff 32, indicating marked autistic-spectrum features; ASD specialist assessment advised.",  # 14
        "Negative 18",  # 15
        "Total 18, below positive cutoff, but specific social difficulties still merit attention.",  # 16
        "What is the cutoff?",  # 17
        "Adult version commonly uses >=32 as the positive threshold; child/self-report thresholds differ; results are screening only.",  # 18
        "Relation to diagnosis?",  # 19
        "AQ is a self-report screen; a positive result only indicates need for further standardized assessment such as ADOS/ADI-R.",  # 20
        "About the Autism Spectrum Quotient (AQ) Self-Assessment",  # 21
        "Autism Spectrum Quotient (AQ) Self-Assessment. A medical professional tool based on authoritative medical standards, for reference only.",  # 22
    ]))
    write('asrs-adhd', build('asrs-adhd', [
        "🧠 Adult ADHD Self-Report Scale (ASRS)",  # 0
        "WHO Adult ADHD Self-Report Scale (ASRS-v1.1), Part A 6-item screening version, assessing attention-deficit/hyperactive symptoms over the past 6 months. Dashed-border options are 'positive' items; >=4 positive among 6 suggests possible adult ADHD.",  # 1
        "ASRS-v1.1: among the 6 core items, >=4 positive (score in the critical range) indicates a positive screen, suggesting possible adult ADHD.",  # 2
        "ASRS Positive-Criteria Rules",  # 3
        "Positive options (dashed border)",  # 4
        "Items 1-4",  # 5
        "Often / Very often",  # 6
        "Items 5-6",  # 7
        "Sometimes / Often / Very often",  # 8
        "This scale is a self-help screening tool and does not replace psychiatric diagnosis. Confirming adult ADHD requires childhood history, functional impairment and clinical interview.",  # 9
        "📚 Deep Dive: ASRS and Adult ADHD",  # 10
        "Inattention",  # 11
        "Hyperactivity-impulsivity",  # 12
        "Positive screen",  # 13
        "6 items (never 0 ... very often 4); shaded positive options (items 1-4 >=3, items 5-6 >=2) hit 4 -> positive, suggesting possible adult ADHD; refer for specialist assessment.",  # 14
        "Fewer than 4 positive options -> below screening positive, but persistent symptoms still warrant monitoring.",  # 15
        "What is the positive criterion?",  # 16
        "ASRS-v1.1 positive threshold combines the first 6 items (4 attention, 2 hyperactivity-impulsivity); hitting >=4 is positive.",  # 17
        "Confirmation?",  # 18
        "Positive result is screening only; adult ADHD needs childhood history, collateral rating and clinical interview showing persistent functional impairment.",  # 19
        "About the Adult ADHD Self-Report Scale (ASRS)",  # 20
        "Adult ADHD Self-Report Scale (ASRS). A medical professional tool based on authoritative medical standards, for reference only.",  # 21
    ]))
    write('assessor-risk-5', build('assessor-risk-5', [
        "🔍 Crisis Risk Screen (C-SSRS)",  # 0
        "Columbia Suicide Severity Rating Scale (C-SSRS) assesses severity of suicidal ideation and behavior",  # 1
        "Crisis Risk Screen (C-SSRS)",  # 2
        "/ Crisis Risk Screen (C-SSRS)",  # 3
        "C-SSRS suicide risk: take the highest level among ideation items (0 none to 5 specific plan + intent) and grade behavior items; higher level means higher risk requiring urgent intervention.",  # 4
        "Warning: this tool is for professional screening reference only",  # 5
        "If you or someone else is in crisis, call a 24-hour psychological crisis hotline immediately:",  # 6
        "or",  # 7
        "Life line:",  # 8
        "This is the professional interview version (semi-structured); general users please use",  # 9
        "Crisis Risk Screen (C-SSRS) self-report version",  # 10
        "Part 1: Suicidal Ideation (past month)",  # 11
        "Please answer yes or no based on your true feelings over the past month",  # 12
        "Part 2: Suicidal Behavior (past 3 months)",  # 13
        "Please honestly answer whether the following behaviors occurred",  # 14
        "High-risk alert:",  # 15
        "Call a 24-hour psychological crisis hotline immediately",  # 16
        "Life line",  # 17
        "In an emergency, go to the nearest hospital ER or call 120.",  # 18
        "Contact a mental-health professional promptly; hotline:",  # 19
        "Your current assessment result is high risk",  # 20
        "Call a 24-hour psychological crisis hotline immediately:",  # 21
        "Life line:",  # 22
        "In an emergency, go to the nearest hospital ER or call 120.",  # 23
        "I understand",  # 24
        "This tool runs on the brief C-SSRS screen entirely in your browser; data is never uploaded to any server",  # 25
        "C-SSRS is a widely used clinical and research crisis-risk assessment tool developed by Columbia University",  # 26
        "The ideation section rises from level 1 to 5; the highest 'yes' option determines ideation severity",  # 27
        "For behavior, any 'yes' within the past 3 months indicates high risk requiring immediate intervention",  # 28
        "This tool is for professional reference only and does not replace psychiatric diagnosis or clinical judgment",  # 29
        "📚 Deep Dive: C-SSRS Interview Version",  # 30
        "Ideation grading",  # 31
        "Behavior identification",  # 32
        "Ideation positive through level 3 of 5, with all 4 behavior items (recent attempt / preparation / non-suicidal self-injury / actual attempt) negative -> moderate risk; prompt professional involvement advised.",  # 33
        "Behavior item 4 'actual attempt = yes' within the past 3 months -> high risk; immediate crisis intervention.",  # 34
        "Difference from self-report version?",  # 35
        "This page is the professional-rated version (assessor, semi-structured); cssrs-suicide is self-rated. Both share the same risk-stratification logic; general users should prefer the self-report version.",  # 36
        "Who administers it?",  # 37
        "It should be completed by a trained rater via semi-structured questioning; results inform triage and monitoring decisions.",  # 38
        "About the Crisis Risk Screen (C-SSRS)",  # 39
        "This tool is based on Columbia University's C-SSRS for screening psychological crisis and suicidal-ideation risk. It assesses suicidal ideation (5-level progression) and suicidal behavior (actual attempt / preparation / self-injury), auto-grades risk level and gives clinical advice.",  # 40
        "C-SSRS: an international standardized crisis-risk assessment scale",  # 41
        "Five-level progressive ideation assessment (passive wish to specific plan)",  # 42
        "Distinguishes suicidal behavior from non-suicidal self-injury",  # 43
        "Automatic risk grading with clinical intervention advice",  # 44
        "Initial crisis-risk screening in psychiatric outpatient clinics",  # 45
        "Crisis assessment in psychological counseling",  # 46
        "Emergency psychiatric triage assessment",  # 47
        "Reference for crisis hotline intervention",  # 48
    ]))
    write('bis11-impulse', build('bis11-impulse', [
        "📋 Barratt Impulsiveness Scale (BIS-11)",  # 0
        "Barratt Impulsiveness Scale, 11th edition (BIS-11, Patton 1995) assesses impulsive traits. 30 items, 4-point scale (1-4), with 11 reverse-scored items; total 30-120, divided into attention, motor and non-planning subscales. Higher total means stronger impulsivity.",  # 1
        "BIS-11 total impulsiveness = sum of 30 items; three factors: attention, motor, non-planning; <=52 low, 53-71 medium, >=72 high impulsiveness.",  # 2
        "BIS-11 Severity Reference",  # 3
        "Low impulsiveness",  # 4
        "Low impulsiveness, good self-control",  # 5
        "Common range in the general population",  # 6
        "High impulsiveness",  # 7
        "High impulsiveness, attention suggested",  # 8
        "Very high impulsiveness, may impair functioning",  # 9
        "This scale is a self-help screening tool and does not replace psychiatric diagnosis. For reverse items (marked 'reverse'), stronger agreement means lower impulsiveness; scoring is auto-converted.",  # 10
        "📚 Deep Dive: BIS-11 Impulsiveness",  # 11
        "Attentional impulsiveness",  # 12
        "Motor impulsiveness",  # 13
        "Non-planning impulsiveness",  # 14
        "Total 65",  # 15
        "30 items 1-4 (reverse: 5-v): attentional 22, motor 24, non-planning 19 -> total 65, above norm suggesting elevated impulsiveness, seen in ADHD/substance use etc.",  # 16
        "Low impulsiveness 45",  # 17
        "Factors 15/16/14 -> 45, near norm; impulsiveness not prominent.",  # 18
        "Meaning of the three factors?",  # 19
        "Attentional (cognitive instability), motor (acting without thinking) and non-planning (lack of forethought) impulsiveness; subscale scores locate intervention targets.",  # 20
        "How are reverse items handled?",  # 21
        "REV-list items are scored as 5 minus raw before summing; the script auto-flips them via the REV dictionary.",  # 22
        "About the Barratt Impulsiveness Scale (BIS-11)",  # 23
        "Barratt Impulsiveness Scale (BIS-11). A medical professional tool based on authoritative medical standards, for reference only.",  # 24
    ]))
    write('cage-substance', build('cage-substance', [
        "💭 CAGE Substance Use Questionnaire",  # 0
        "The CAGE questionnaire screens for alcohol use disorder. Four yes/no questions; each 'yes' scores 1. Total >=2 suggests alcohol-related problems requiring further assessment.",  # 1
        "Each 'yes' on the four CAGE items scores 1; total = number of affirmative answers; >=2 is a positive screen, indicating alcohol-related risk.",  # 2
        "CAGE Result Interpretation",  # 3
        "No obvious alcohol problem for now",  # 4
        "Suggests alcohol-related problems; further AUDIT assessment advised",  # 5
        "This scale is a self-help screening tool and does not replace psychiatric/addiction-medicine diagnosis. CAGE targets alcohol; CAGE-AID extends to drug use. For addiction, consult addiction medicine.",  # 6
        "📚 Deep Dive: CAGE Substance-Use Screening",  # 7
        "Initial alcohol-problem screen",  # 8
        "Quick pre-visit inquiry",  # 9
        "Follow-up re-screen",  # 10
        "Positive (>=2)",  # 11
        "4 items (yes=1/no=0): Cut down yes, Annoyed no, Guilty yes, Eye-opener no -> 2 points, positive screen; AUDIT further assessment advised.",  # 12
        "Negative 0",  # 13
        "All 4 items no -> 0 points, not yet positive; health education still advised.",  # 14
        "Why only 4 items?",  # 15
        "CAGE is brief and sensitive, ideal for quick bedside screening; a positive result warrants deeper assessment of amount and duration of drinking.",  # 16
        "Used for drugs?",  # 17
        "Originally designed for alcohol; it can screen other substances but is less precise than dedicated scales (e.g. DAST).",  # 18
        "About the CAGE Substance Use Questionnaire",  # 19
        "CAGE Substance Use Questionnaire. A medical professional tool based on authoritative medical standards, for reference only.",  # 20
    ]))


if __name__ == '__main__':
    main()

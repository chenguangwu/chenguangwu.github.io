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
    write('rater-23', build('rater-23', [
        "🧠 Liebowitz Social Anxiety Scale (LSAS) Rating",  # 0
        "Liebowitz Social Anxiety Scale rates fear/anxiety and avoidance across 24 social situations to quantify social anxiety disorder severity",  # 1
        "Total = sum of fear + sum of avoidance (each item 0-3); split by performance/social type; max = items x 3 x 2.",  # 2
        "Fear/anxiety:",  # 3
        "0=none, 1=mild, 2=moderate, 3=severe",  # 4
        "Avoidance:",  # 5
        "0=never, 1=occasionally, 2=often, 3=always",  # 6
        "This tool runs on the Liebowitz Social Anxiety Scale (LSAS) entirely in your browser; data is never uploaded to any server",  # 7
        "LSAS has 24 situations (13 performance + 11 social-interaction); each rates fear and avoidance separately",  # 8
        "Total range 0-144; >30 suggests possible social anxiety disorder, >60 highly likely, >90 severe",  # 9
        "This tool is screening reference only and does not replace psychiatric diagnosis",  # 10
        "📚 Deep Dive: LSAS Social Anxiety Rating (rater)",  # 11
        "Performance situations",  # 12
        "Social situations",  # 13
        "Fear/avoidance subscales",  # 14
        "Total 64",  # 15
        "24 situations each recorded fear f and avoidance a (0-3): performance 13 items fear 20+avoid 16=36, social 11 items fear 16+avoid 12=28 -> total 64, performance dominant.",  # 16
        "Low 25",  # 17
        "Fear 15 + avoidance 10 = 25, mild, avoidance-dominant.",  # 18
        "Difference from lsas-social?",  # 19
        "This page is the rater version; lsas-social is the scale display; both score 24 situations by fear+avoidance.",  # 20
        "Maximum score?",  # 21
        "Each situation fear+avoidance 0-3, 24 situations -> max total 144, fear/avoidance each max 72.",  # 22
        "About the Liebowitz Social Anxiety Scale (LSAS) Rating",  # 23
        "Liebowitz Social Anxiety Scale (LSAS) rates fear/anxiety and avoidance across 24 social situations, distinguishing performance and social-interaction types, to quantify social anxiety disorder severity.",  # 24
        "Comprehensive 24-situation assessment",  # 25
        "Dual-dimension fear/anxiety and avoidance scoring",  # 26
        "Performance/social-interaction classification analysis",  # 27
        "Automatic severity grading with clinical interpretation",  # 28
        "Screening and severity assessment of social anxiety disorder",  # 29
        "Baseline assessment before psychotherapy",  # 30
        "Treatment response tracking and follow-up",  # 31
        "Epidemiological survey of social anxiety",  # 32
    ]))
    write('rater-24', build('rater-24', [
        "🧠 Connor-Davidson Resilience Scale (CD-RISC) Rating",  # 0
        "Connor-Davidson Resilience Scale (CD-RISC-25) has 25 items assessing resilience to adversity; total 0-100",  # 1
        "Resilience total = sum of items (0-4); max = items x 4; score rate = total / max x 100%; >=80 high, 65-79 mod-high, 50-64 medium, <50 to improve.",  # 2
        "Please choose the most fitting description based on the past month",  # 3
        "This tool runs on the Connor-Davidson Resilience Scale (CD-RISC-25) entirely in your browser; data is never uploaded to any server",  # 4
        "CD-RISC has 25 items, 0-4 each, total 0-100; higher score means stronger resilience",  # 5
        "General population averages about 80, clinical anxiety/depression about 50-65, PTSD about 47",  # 6
        "This tool is a mental-health self-assessment reference and does not replace professional psychological evaluation",  # 7
        "📚 Deep Dive: CD-RISC Resilience Rating (rater)",  # 8
        "Item-by-item scoring",  # 9
        "Locate low-score items",  # 10
        "Before/after comparison",  # 11
        "Total 60",  # 12
        "25 items 0-4 entered individually total 60, 60% of max 100; 'adapts to change' only 1, 'planning' 2 are improvement targets.",  # 13
        "High score 85",  # 14
        "Several 3-4 items total 85, good resilience, little intervention room.",  # 15
        "Difference from cdrisc-resilience?",  # 16
        "This page is the item-by-item rater version; cdrisc-resilience is self-rated; both score 0-100 identically.",  # 17
        "How to use low scores?",  # 18
        "Locate items <=1 as resilience-training entry points and retest to see improvement.",  # 19
        "About the Connor-Davidson Resilience Scale (CD-RISC) Rating",  # 20
        "Connor-Davidson Resilience Scale (CD-RISC-25) has 25 items assessing resilience to adversity, stress and trauma, compared with general and clinical population norms.",  # 21
        "Standardized 25-item resilience assessment",  # 22
        "0-100 total quantifies resilience level",  # 23
        "Compared with general/anxiety/PTSD reference lines",  # 24
        "Weak-item identification and improvement advice",  # 25
        "Mental-health self-assessment and resilience baseline",  # 26
        "Resilience-change tracking before/after counseling/therapy",  # 27
        "Post-trauma recovery assessment",  # 28
        "Mental-health education and screening",  # 29
    ]))
    write('self-assess-4', build('self-assess-4', [
        "🧠 Adult ADHD Self-Report (ASRS) Rating",  # 0
        "Adult ADHD Self-Report Scale (ASRS-v1.1) Part A screening version, 6 items assessing adult ADHD symptoms; a WHO-recommended screening tool",  # 1
        "ASRS adult ADHD screen: positive items = items at/above threshold; >=4 suggests positive screen, >=5 highly suspected; professional diagnosis advised.",  # 2
        "Please choose the most fitting description based on the past 6 months. Options marked with a star are positive items.",  # 3
        "Assessment / screening result",  # 4
        "This tool runs on ASRS-v1.1 Part A (6-item screening) entirely in your browser; data is never uploaded to any server",  # 5
        "ASRS was jointly developed by WHO and Harvard; a standardized adult-ADHD screening tool",  # 6
        "Items 1-3: 'sometimes/often/very often' is positive; items 4-6: 'often/very often' is positive",  # 7
        "4 or more positive items suggests possible adult ADHD; further professional assessment advised",  # 8
        "This tool is for screening only and does not replace psychiatric diagnosis",  # 9
        "📚 Deep Dive: ASRS Adult ADHD Self-Rating (rater)",  # 10
        "Attention subscale",  # 11
        "Hyperactivity subscale",  # 12
        "Positive determination",  # 13
        "Positive screen",  # 14
        "6 items by positiveFrom threshold: 3 of 4 attention items and both 2 hyperactivity items positive -> positive count 5 >=4, suggests ADHD.",  # 15
        "Positive count 2 <4 -> negative, atypical symptoms.",  # 16
        "Difference from asrs-adhd?",  # 17
        "This page is the item-by-item self-assess version; asrs-adhd is the scale display; thresholds are identical.",  # 18
        "Value of subscales?",  # 19
        "Splitting attention (first 4) and hyperactivity-impulsivity (last 2) shows strength/deficit sides, aiding subtyping.",  # 20
        "About the Adult ADHD Self-Report (ASRS) Rating",  # 21
        "Adult ADHD Self-Report Scale (ASRS-v1.1) Part A screening version, 6 items assess adult ADHD symptoms, distinguishing inattentive from hyperactive/impulsive types; a WHO-recommended screening tool.",  # 22
        "ASRS-v1.1 WHO-standardized screening scale",  # 23
        "6-item quick screen (4 positives = positive screen)",  # 24
        "Inattentive/hyperactive-impulsive subtyping",  # 25
        "Automatic determination with clinical advice",  # 26
        "Initial adult-ADHD screening",  # 27
        "Psychiatric outpatient adjunct assessment",  # 28
        "Self-rating reference for attention distress",  # 29
        "Mental-health survey",  # 30
    ]))
    write('ybocs-ocd', build('ybocs-ocd', [
        "💭 Yale-Brown Obsessive Compulsive Scale (Y-BOCS)",  # 0
        "Yale-Brown Obsessive Compulsive Scale (Y-BOCS) self-report rates severity of obsessions and compulsions over the past week. 10 items (first 5 obsessions, last 5 compulsions), 0-4 each, total 0-40.",  # 1
        "Y-BOCS total = sum of 10 items (0-4); obsessions = first 5, compulsions = last 5; <=7 subclinical, 8-15 mild, 16-23 moderate, >=24 severe.",  # 2
        "Y-BOCS Severity Levels",  # 3
        "No notable OCD symptoms",  # 4
        "Mild symptoms, observation and follow-up",  # 5
        "Medication / psychotherapy (CBT-ERP) advised",  # 6
        "Active medication + psychotherapy needed",  # 7
        "Severe functional impairment, intensive treatment",  # 8
        "This is a self-help screening tool and does not replace psychiatric diagnosis. First-line OCD treatment is exposure and response prevention (CBT-ERP) and SSRIs.",  # 9
        "📚 Deep Dive: Y-BOCS Obsessive-Compulsive Severity",  # 10
        "Obsession assessment",  # 11
        "Compulsion assessment",  # 12
        "Before/after treatment comparison",  # 13
        "Total 20 (moderate-severe)",  # 14
        "10 items each 0-4: obsessions 5 sum 12 (e.g. intrusive 3, resistance 2, distress 3, control 2, time 2), compulsions 5 sum 8 (e.g. time 2, resistance 1, distress 2, control 1, time 2) -> total 20, moderate-severe; medication plus ERP advised.",  # 15
        "Mild 8",  # 16
        "Thought 5 (about 1 each) + behavior 3 (about 0.6 each) -> total 8, mild; start CBT and follow up.",  # 17
        "How is severity graded?",  # 18
        "Total <=7 minimal/subclinical, 8-15 mild, 16-23 mod-severe, 24-32 extreme; view obsession and compulsion scores separately.",  # 19
        "Notes for assessment?",  # 20
        "Scored by trained clinicians via semi-structured interview; avoid replacing with patient self-report; suicide risk needs separate assessment.",  # 21
        "About the Yale-Brown Obsessive Compulsive Scale (Y-BOCS)",  # 22
        "Yale-Brown Obsessive Compulsive Scale (Y-BOCS). A medical professional tool based on authoritative medical standards, for reference only.",  # 23
    ]))


if __name__ == '__main__':
    main()

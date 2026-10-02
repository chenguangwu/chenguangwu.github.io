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
    write('calc-1', build('calc-1', [
        "🔍 PHQ-9 Depression Screening Scale",  # 0
        "Over the past 2 weeks, how often have the following problems bothered you? 0=not at all, 1=several days, 2=more than half the days, 3=nearly every day.",  # 1
        "PHQ-9 total = sum of 9 items (0-3, max 27); item 9 (self-harm thoughts) >0 triggers a high-risk alert; seek professional help promptly.",  # 2
        "10. If you have had any of these problems, how difficult have they made work, social or family life? (not scored)",  # 3
        "Somewhat difficult",  # 4
        "Extremely difficult",  # 5
        "📚 Deep Dive: PHQ-9 Depression Screening",  # 6
        "Depression severity",  # 7
        "Attention to the suicidal item",  # 8
        "Follow-up scoring",  # 9
        "Total 15 (moderate)",  # 10
        "9 items 0-3: 2,2,2,1,2,2,2,1,1 = 15, moderate depression; item 9 (suicide) >0 requires immediate",  # 11
        "referral.",  # 12
        "Severe 24",  # 13
        "First 8 items 3, item 9 = 0 -> 24 but no suicidal item; severe still needs prompt treatment; if item 9 >0, handle as emergency.",  # 14
        "Severity levels?",  # 15
        "0-4 none, 5-9 mild, 10-14 moderate, 15-19 mod-severe, 20-27 severe; item 9 viewed separately, >0 means assess suicide risk.",  # 16
        "Difference from PHQ-9 self-report?",  # 17
        "This tool is the PHQ-9 self-report implementation; results aid screening and follow-up; diagnosis needs clinical correlation.",  # 18
    ]))
    write('cdrisc-resilience', build('cdrisc-resilience', [
        "📋 Connor-Davidson Resilience Scale (CD-RISC)",  # 0
        "Connor-Davidson Resilience Scale brief version (CD-RISC-10) assesses ability to cope with stress and adversity over the past month. 10 items, 0-4 each, total 0-40; higher score means stronger resilience.",  # 1
        "CD-RISC total resilience = sum of 25 items (0-5 each, max 125); <=19 lower, 20-29 medium, >=30 higher.",  # 2
        "CD-RISC-10 Resilience Reference",  # 3
        "Lower resilience, strengthen coping skills advised",  # 4
        "Shows some resilience",  # 5
        "Good resilience, strong recovery",  # 6
        "Resilience can be built through training. This self-assessment tool's score is for reference only and can track personal growth.",  # 7
        "📚 Deep Dive: CD-RISC Resilience",  # 8
        "Resilience level",  # 9
        "Stress coping",  # 10
        "Before/after intervention",  # 11
        "Total 60/100",  # 12
        "25 items 0-4: balanced answers total 60, medium resilience; low items (e.g. 'adapts to change' only 1) are improvement targets.",  # 13
        "High resilience 82",  # 14
        "Several 3-4 items total 82, stronger resilience, recovers faster from adversity.",  # 15
        "Score range?",  # 16
        "0-100, higher is better; below about 50 suggests more vulnerability under stress, with targeted training possible.",  # 17
        "Can it be trained?",  # 18
        "Resilience improves via cognitive restructuring, social support and mindfulness; CD-RISC fits before/after comparison.",  # 19
        "About the Connor-Davidson Resilience Scale (CD-RISC)",  # 20
        "Connor-Davidson Resilience Scale (CD-RISC). A medical professional tool based on authoritative medical standards, for reference only.",  # 21
    ]))
    write('cssrs-suicide', build('cssrs-suicide', [
        "💭 Crisis Risk Screen (C-SSRS Self-Report)",  # 0
        "Columbia Suicide Severity Rating Scale (C-SSRS) screening version assesses severity of suicidal ideation and history of suicidal behavior. For risk-screening reference; answer honestly.",  # 1
        "Crisis Risk Screen (C-SSRS Self-Report)",  # 2
        "/ Crisis Risk Screen (C-SSRS Self-Report)",  # 3
        "High-risk alert:",  # 4
        "Call a 24-hour psychological crisis hotline immediately",  # 5
        "or",  # 6
        "Life line",  # 7
        "In an emergency, go to the nearest hospital ER or call 120.",  # 8
        "Contact a mental-health professional promptly; hotline:",  # 9
        "Your current assessment result is high risk",  # 10
        "Call a 24-hour psychological crisis hotline immediately:",  # 11
        "Life line:",  # 12
        "In an emergency, go to the nearest hospital ER or call 120.",  # 13
        "I understand",  # 14
        "Suicide-risk assessment must be done by professionals; this tool is screening reference only. If you or someone is in crisis, call a 24-hour psychological crisis hotline immediately:",  # 15
        "(Beijing Crisis Care and Intervention Center",  # 16
        ") or go to the nearest hospital ER.",  # 17
        "📚 Deep Dive: C-SSRS Self-Report Version",  # 18
        "Suicidal ideation grading",  # 19
        "Suicidal behavior identification",  # 20
        "Emergency risk stratification",  # 21
        "Ideation level 3, no behavior",  # 22
        "Ideation 5-level 'yes' through level 3 (ideation with method) but levels 4-5 no; all 4 behavior items no -> moderate risk; prompt professional involvement and risk removal.",  # 23
        "High risk (actual attempt)",  # 24
        "Ideation all no or up to level 5, behavior item 4 'actual attempt = yes' within 3 months -> high risk; immediate crisis intervention and monitoring.",  # 25
        "How is risk stratified?",  # 26
        "By highest ideation level and presence of behavior (preparation / non-suicidal self-injury / attempt): no behavior and low ideation is low risk; method or behavior raises to moderate/high.",  # 27
        "Who should assess?",  # 28
        "Complete under professional guidance; self-report is screening reference only. If moderate/high risk is indicated, contact a professional immediately or call the 24-hour crisis hotline 400-161-9995.",  # 29
        "About the Crisis Risk Screen (C-SSRS Self-Report)",  # 30
        "Crisis Risk Screen (C-SSRS Self-Report). A medical professional tool based on authoritative medical standards, for reference only.",  # 31
    ]))
    write('eat26-eating', build('eat26-eating', [
        "📋 Eating Attitudes Test (EAT-26)",  # 0
        "Eating Attitudes Test (EAT-26) screens for possible eating-disorder tendencies. 26 items, 6-point scale; total >=20 suggests eating-disorder concern needing further assessment.",  # 1
        "EAT-26 total = sum of 26 items (reverse-scored items weighted REVERSE/NORMAL); <20 low risk, >=20 suggests eating-disorder risk needing professional assessment.",  # 2
        "EAT-26 Scoring Notes",  # 3
        "Forward item score",  # 4
        "Reverse items (8/13/25) score",  # 5
        "Usually",  # 6
        "This is a self-help screening tool and does not replace psychiatric/nutrition diagnosis. If binge eating, vomiting or extreme diet restriction occurs, seek medical care promptly.",  # 7
        "📚 Deep Dive: EAT-26 Eating Attitudes",  # 8
        "Eating-disorder screening",  # 9
        "Dieting-behavior assessment",  # 10
        "High-risk group identification",  # 11
        "Positive (>=20)",  # 12
        "26 items scored NORM/REV: assume total 24, and item 4 (binge) or item 9 (vomiting) reported 'often/always' -> reaches positive cutoff 20; refer to eating-disorder specialist.",  # 13
        "Negative 8",  # 14
        "Total 8 and high-risk items not triggered -> not positive, but keep monitoring body-image cognition.",  # 15
        "What does positive mean?",  # 16
        "Total >=20 or any high-risk item reported frequently suggests possible eating disorder; combine with weight and eating-behavior interview.",  # 17
        "Who is it for?",  # 18
        "Commonly used for adolescents and young adults; males can also be positive; do not limit to females.",  # 19
        "About the Eating Attitudes Test (EAT-26)",  # 20
        "Eating Attitudes Test (EAT-26). A medical professional tool based on authoritative medical standards, for reference only.",  # 21
    ]))
    write('gad7-anxiety', build('gad7-anxiety', [
        "💭 Generalized Anxiety (GAD-7) Screener",  # 0
        "Self-rate 7 anxiety-symptom items based on feelings over the past two weeks to screen generalized anxiety severity. 7 items, 0-3 each.",  # 1
        "GAD-7 total = sum of 7 items (0-3 each, max 21); <=4 none, 5-9 mild, 10-14 moderate, >=15 severe.",  # 2
        "GAD-7 Severity Levels",  # 3
        "No anxiety",  # 4
        "Needs further assessment and intervention",  # 5
        "This is a self-help screening tool and does not replace psychiatric diagnosis. At GAD-7 total >=10 sensitivity is high; seek professional assessment.",  # 6
        "📚 Deep Dive: GAD-7 Generalized Anxiety",  # 7
        "Screening anxiety",  # 8
        "Severity grading",  # 9
        "Treatment follow-up",  # 10
        "Total 12 (moderate)",  # 11
        "7 items (not at all 0 / several days 1 / more than half 2 / nearly every day 3): 2,2,2,1,2,2,1 = 12, moderate anxiety; psychotherapy advised, >=14 consider medication.",  # 12
        "Severe 21",  # 13
        "All 7 items 3 -> 21, severe; urgent psychiatric assessment and screen for depressive comorbidity.",  # 14
        "Severity criteria?",  # 15
        "0-4 none/minimal, 5-9 mild, 10-14 moderate, 15-21 severe; high item-2 score suggests marked functional impairment.",  # 16
        "Can it replace diagnosis?",  # 17
        "No; it only screens and monitors severity; confirmation needs structured clinical interview.",  # 18
        "About the Generalized Anxiety (GAD-7) Screener",  # 19
        "Generalized Anxiety (GAD-7) Screener. A medical professional tool based on authoritative medical standards, for reference only.",  # 20
    ]))


if __name__ == '__main__':
    main()

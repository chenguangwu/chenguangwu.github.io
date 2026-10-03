#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'dance')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'dance')
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
    out = {'slug': slug, 'industry': 'dance', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
# -*- coding: utf-8 -*-
def main():
    write('index', build('index', [
        '💃 Dance Art Tools',
        'Dance Art',
        'Dance Art Tools',
        'Partner spacing calculator that finds the optimal partner distance and movement path radius from arm span and dance style, assisting partner work and blocking.',
        'Estimates stability margin from rotation body mass distribution and rotation speed to judge whether a spin is unstable, for mechanical analysis and safety notes in dance spins, apparatus and stage moves.',
        'Choreography timeline planner that generates an 8-beat phrase timeline from BPM and time signature with customizable phrases, assisting choreography and teaching.',
        'Flexibility tester that computes percentile rank and flexibility level from a seated forward reach result against age and gender standards, assisting fitness assessment.',
        'Quality (student satisfaction / progress) assessment',
        'Scores students across dimensions such as teaching effect, progress and satisfaction on a 5-point scale, and outputs a composite score and grade for dance training quality tracking and teaching improvement.',
        'The seated forward reach is a classic test of body flexibility. Enter gender, age and result (cm) to compute the percentile rank and grade automatically, referencing data from the National Physical Fitness Standards.',
        'Enter a music BPM to compute beat interval, bar duration and movement density, mapping musical rhythm to dance movements for beat planning and groove training.',
        'About "Dance Art Tools"',
        'This Dance Art Tools collection gathers 7 free online tools covering the common calculation, conversion and lookup needs of dance art. Whether you are a practitioner, a student or an ordinary user, you will find ready-to-use utilities here. Every tool runs purely in the browser; no data is uploaded to the server, so your privacy and security are protected.',
        'Dance art tools included on this page (representative tools only):',
        'These tools help you finish common dance art tasks fast, with no need to memorize complex formulas or convert by hand - input and you get the result.',
        'Do the Dance Art Tools require downloads or registration?',
        'No. All Dance Art Tools on this page are pure front-end online tools: open the page and use them right away, with no software to install, no account to register, and no data uploaded.',
        'Are the Dance Art Tools results accurate, and is the data safe?',
        'The tools compute in your browser using public math formulas and common industry standards, so results are available instantly. All computation happens locally on your device; no data is uploaded to the server, so privacy and security are guaranteed.',
    ]))

    write('tester-4', build('tester-4', [
        '💭 Flexibility Test (Seated Forward Reach) Percentile Rank',
        'The seated forward reach is a classic test of body flexibility. Enter gender, age and result (cm) to compute the percentile rank and grade automatically, referencing data from the National Physical Fitness Standards.',
        '📖 Read the "Flexibility Test (Seated Forward Reach) Percentile Rank User Guide"',
        'Result (cm)',
        'Compute percentile rank',
        'Seated forward reach test method: the subject sits on a flat surface with legs straight and heels against the board, leans forward and pushes the cursor with fingertips, and the maximum reach distance is recorded (cm; a negative value means the fingertips did not reach the toes).',
        'Warm up fully before the test to avoid strain; the knees must not bend; push forward at a steady speed with no sudden force.',
        'Percentile rank is the percentage of people in the same age and gender group that you exceed, e.g. P75 means better than 75% of people.',
        'Data in this tool is a reference standard; actual grading follows the standards of your local sports authority.',
        '📚 Deep dive: flexibility test (seated forward reach) percentile rank',
        'Percentile rank:',
        'enter gender, age and result to get the percentile rank and grade.',
        'Age comparison: the same result is graded differently across age ranges, enabling longitudinal comparison.',
        'Progress tracking: compare the percentile rank of two tests to quantify training effectiveness.',
        'Percentile rank example',
        'Female, age 25, seated forward reach 22 cm → percentile rank about 80, graded "excellent"; six months later at 26 cm it rises to about 90.',
        'What is the source of the standards?',
        'It follows national physical fitness monitoring standards, grouped by gender and age.',
        'Do results need to be uploaded?',
        'No. Everything is computed in the local browser and never uploaded.',
        'What does the grade mean?',
        'It is a flexibility fitness reference only and does not replace professional medical or rehabilitation assessment.',
        'About "Flexibility Test (Seated Forward Reach) Percentile Rank"',
        'The seated forward reach is a classic flexibility test in national physical fitness monitoring, reflecting the flexibility of the lower back and hamstring muscle groups. This tool computes percentile rank by gender and age range from data in the National Physical Fitness Standards, helping assess flexibility levels.',
        'Matches reference standards by gender and age range',
        'Auto-computes percentile rank P5-P95',
        'Shows reference results for P10/P25/P50/P75/P90',
        'Gives graded training suggestions',
        'Flexibility assessment for school PE classes',
        'Flexibility level tracking in dance training',
        'National physical fitness monitoring aid',
        'Stretching plans by fitness coaches',
        'How to use the Flexibility Test (Seated Forward Reach) Percentile Rank',
        'Used for seated forward reach fitness grading, tracking flexibility progress before and after training, and group fitness screening.',
        'What does the Flexibility Test (Seated Forward Reach) Percentile Rank do?',
        'How do I use the Flexibility Test (Seated Forward Reach) Percentile Rank?',
        'What scenarios suit the Flexibility Test (Seated Forward Reach) Percentile Rank?',
    ]))


if __name__ == '__main__':
    main()

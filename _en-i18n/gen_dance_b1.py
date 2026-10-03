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
    write('assessor-csat-1', build('assessor-csat-1', [
        '⚖️ Student Satisfaction and Progress Assessment',
        'Evaluate dance training quality across five dimensions - teaching quality, course design, student progress, venue environment and service attitude - each scored 1-5, then compute a weighted composite score and generate improvement suggestions.',
        'Quality (student satisfaction / progress) assessment',
        '/ Quality (student satisfaction / progress) assessment',
        '📖 Read the "Student Satisfaction and Progress Assessment User Guide"',
        'Composite score = Σ (dimension score × dimension weight), each dimension scored on a 5-point scale and weights sum to 100%; a composite score of 4.5 or above is excellent, 3.5 to 4.4 is good, 2.5 to 3.4 is average, and below 2.5 is fail; dimensions scoring 1 to 2 are flagged as weak areas that need teaching improvement measures. Track teaching quality by scoring teaching effect, progress and satisfaction separately.',
        'Assess teaching quality',
        'Score each item 1-5: 1=very dissatisfied / 2=dissatisfied / 3=neutral / 4=satisfied / 5=very satisfied',
        'Composite score = weighted sum of item scores × weights (teaching quality and student progress carry higher weights)',
        'Items scoring 2 or below are listed as key improvement targets',
        'Collect student ratings in bulk and enter the average for a more objective assessment',
        '📚 Deep dive: student satisfaction and progress assessment',
        'End-of-term teaching review: score the five dimensions separately, compute the weighted composite and grade, and locate the weakest dimension for targeted improvement.',
        'Student progress tracking: plot a progress curve from enrollment, midterm and final assessments to quantify teaching effectiveness.',
        'Cross-institution comparison: compare dimension averages across classes to guide scheduling, staffing and venue resource decisions.',
        'Institution quality review example',
        'Teaching 4.5 / Course 4.0 / Progress 4.8 / Environment 4.2 / Service 4.0 (equal weights) gives a weighted composite of 4.3 → grade A; the shortcoming is course design, so schedule an extra choreography breakdown class next week.',
        'How do I set the weights?',
        'Set dimension weights according to institutional priorities; equal weights are the default. The weight file stays in the local browser only.',
        'Do ratings need to be uploaded to a server?',
        'No. All ratings are processed locally and never uploaded, protecting the privacy of student and institution data.',
        'Can the results be used directly for formal assessment?',
        'Treat them as internal quality tracking references only; they do not replace the institution formal assessment or HR system.',
        'About "Student Satisfaction and Progress Assessment"',
        'A comprehensive quality assessment tool for dance training institutions, scoring five dimensions - teaching quality, course design, student progress, venue environment and service attitude - with weights, helping institutions quantify teaching quality, locate weak links and keep improving.',
        'Five-dimension weighted scoring (teaching quality and student progress 25% each)',
        'Visual bar chart of each dimension score',
        'Automatic weak-area detection with improvement suggestions',
        'Supports bulk scoring with averages entered once',
        'Quarterly quality assessment for dance training institutions',
        'Student satisfaction questionnaire summary',
        'Reference for teacher performance review',
        'Basis for course improvement plans',
        'How to use the Student Satisfaction and Progress Assessment',
        "'+d.name+' (weight '+Math.round(d.weight*100)+'%)'",
        'Used for teaching quality review, student progress tracking and cross-class comparison at dance training institutions.',
        'What does the Student Satisfaction and Progress Assessment do?',
        'Scores students across dimensions such as teaching effect, progress and satisfaction on a 5-point scale, and outputs a composite score and grade for dance training quality tracking and teaching improvement.',
        'How do I use the Student Satisfaction and Progress Assessment?',
        'What scenarios suit the Student Satisfaction and Progress Assessment?',
    ]))


if __name__ == '__main__':
    main()

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
    write('choreography-timeline', build('choreography-timeline', [
        '💃 Choreography Timeline',
        '8-beat phrase planner that generates a dance timeline from BPM and bar count',
        '"8-beat phrase planner that generates a dance timeline from BPM and bar count" is computed from the input parameters and returns the result.',
        '📖 Read the "Choreography Timeline User Guide"',
        'Number of phrases',
        'Bars per phrase',
        '4/4',
        '3/4',
        '6/8',
        'Start time (seconds)',
        '💃 Generate timeline',
        '➕ Add phrase',
        '📋 Export text',
        '🎯 Apply template',
        '📋 Common choreography structure templates',
        'Intro-climax-outro',
        'Solo / showcase',
        'Rondo form',
        'Competition piece',
        'Progressive development',
        'Narrative choreography',
        'Intro-A-B-outro',
        'Four-part form',
        'Ensemble choreography',
        'Duration per bar = time signature × 60 ÷ BPM; phrase duration = bars × duration per bar. You can customize each phrase name and movement description.',
        '📚 Deep dive: choreography timeline',
        'Phrase planning: generate a timeline of 8-beat phrases, label each with movement names, and form an executable choreography skeleton.',
        'Teaching breakdown: split a whole dance into several 8-beat phrases for teaching and rehearsal, reducing the learning load.',
        'Duration estimate: sum phrase durations for the total, used for pacing control and program scheduling.',
        'Choreography duration estimate example',
        'BPM 128 in 4/4, one 8-beat phrase takes 3.75 s; choreographing 16 phrases gives about 60 s, plus 10 s for staging, so the total program length is about 70 s.',
        'How do I choose the time signature?',
        'Fill in the time signature of the music you use; it affects the seconds per phrase.',
        'Can I export the choreography structure?',
        'Yes, you can export phrase names and movement descriptions for teaching records.',
        'Can I customize the phrases?',
        'Yes. Phrases can be renamed and given movement descriptions, and the timeline recalculates automatically.',
        'About "Choreography Timeline"',
        'The Choreography Timeline planner generates an 8-beat phrase timeline from BPM and time signature, supports custom phrase names and movement descriptions, and exports the choreography structure in one click.',
        'Automatic phrase timing',
        'Custom multi-phrase naming',
        'Common choreography structure templates',
        'One-click text export',
        'Dance choreography planning',
        'Competition piece structure design',
        'Teaching phrase scheduling',
        'Rehearsal time management',
    ]))

    write('flexibility-test', build('flexibility-test', [
        '💭 Flexibility Test',
        'Seated forward reach percentile grading by age and gender against standards',
        'Core formula (from input variables): max(1,min(99,pct))',
        '📖 Read the "Flexibility Test User Guide"',
        'Seated forward reach result (cm)',
        '📋 Grading standards reference (adults)',
        'Male (cm)',
        'Female (cm)',
        'The seated forward reach reflects lower back and hamstring flexibility. Dance practitioners usually need at least a good level. Data references national physical fitness monitoring standards.',
        '📚 Deep dive: flexibility test',
        'Fitness grading: enter a result to compute',
        'the percentile rank',
        'and the flexibility level for a quick answer.',
        'Before/after training comparison: compare percentile rank across two tests to quantify flexibility gains.',
        'Group screening: enter results in bulk to see the distribution and identify individuals needing more training.',
        'Flexibility level example',
        'Male, age 20, seated forward reach 18 cm → percentile rank about 75 and flexibility level "good" per the national fitness standard; after 8 weeks of training at 22 cm, percentile rank rises to about 85.',
        'What is the source of the standards?',
        'It follows national physical fitness monitoring standards, grouped and referenced by age and gender.',
        'Is the data uploaded?',
        'No. Results are processed locally only and never uploaded.',
        'Can the level be used for medical judgment?',
        'It is a physical fitness reference only and does not replace professional medical or rehabilitation assessment.',
        'About "Flexibility Test"',
        'The Flexibility Test tool computes percentile rank and flexibility level from a seated forward reach result, referencing national physical fitness monitoring standards by age and gender.',
        'Auto-matches standards by age and gender',
        'Percentile rank visualization',
        'Five-level evaluation system',
        'Personalized training suggestions',
        'Flexibility assessment for dance students',
        'Physical fitness monitoring test',
        'Flexibility progress tracking',
    ]))


if __name__ == '__main__':
    main()

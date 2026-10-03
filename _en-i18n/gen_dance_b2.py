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
    write('bpm-rhythm', build('bpm-rhythm', [
        '🎵 BPM Beat Mapping',
        'Convert music BPM to dance movement rhythm, computing beat intervals, bar duration and movement density',
        'Core formula (from input variables): Math.round(dur×beatsPerSec); Math.floor(movesPerSec×dur); Math.floor(totalBeats÷bpb)',
        '📖 Read the "BPM Beat Mapping User Guide"',
        'BPM (beats per minute)',
        'Dance style',
        'Waltz (3/4)',
        'Tango (4/4)',
        'Salsa (4/4)',
        'Street dance (4/4)',
        'Ballet (3/4 or 4/4)',
        'Time signature (beats per bar)',
        'Beats per movement',
        'Dance duration (seconds)',
        '▶ Start metronome',
        '📋 BPM reference for common dance styles',
        'BPM range',
        'Graceful and flowing',
        'Sharp and powerful',
        'Passionate and lively',
        'Street dance',
        'Free groove',
        'Ballet adagio',
        'Gentle stretch',
        'Jazz dance',
        'Energetic and dynamic',
        'Beat interval(ms) = 60000 ÷ BPM; bar duration(s) = time signature × beat interval ÷ 1000; movement density = total movements within the duration.',
        '📚 Deep dive: BPM beat mapping',
        'Choreography beat planning: convert BPM to seconds per beat and place movement accents every 8 beats to avoid rushing or dragging the beat.',
        'Groove training: design breathing and accent points along the bar duration to build a stable body rhythm.',
        'Cross-tempo transitions: when two tracks differ greatly in BPM, compute transition beats to switch movements smoothly.',
        'BPM conversion example',
        'BPM 120 in 4/4 → 0.5 s per beat, 2 s per bar, 4 s for an 8-beat phrase; if each movement takes 2 beats, an 8-beat phrase fits 4 movements.',
        'How do I get the BPM?',
        'Read the tempo with a metronome or music software and enter it manually.',
        'Does the time signature matter?',
        'Yes. Bar duration depends on the time signature, so you must fill in the time signature for an accurate result.',
        'Are the results exact?',
        'They are theoretical beat conversions; in practice the audio and the live playing are the reference.',
        'About "BPM Beat Mapping"',
        'The BPM Beat Mapping calculator converts beat interval, bar duration and movement density from a music BPM, helping dancers match musical rhythm precisely.',
        'Presets for multiple dance styles',
        'Beat visualization and metronome',
        'Real-time movement density',
        'Choreography beat planning',
        'Dance class rhythm training',
        'Music and movement matching',
        'Rehearsal beat calibration',
    ]))


if __name__ == '__main__':
    main()

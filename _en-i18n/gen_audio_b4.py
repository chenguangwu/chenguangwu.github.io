#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'audio')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'audio')
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
    out = {'slug': slug, 'industry': 'audio', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
# -*- coding: utf-8 -*-
def main():
    write('index', build('index', [
        '🎧 Audio Tools',
        'Audio Tools',
        'Audio Tools',
        'Spectrum Parameters and Frequency Locator',
        'Enter a time-domain signal or audio sample data to draw a spectrum in real time, showing the energy distribution of each frequency component for audio debugging, vibration and acoustic analysis.',
        'Online audio waveform viewer built on the Web Audio API, drawing the time-domain waveform and frequency-domain spectrum (FFT) in real time with local file analysis support - suited to audio debugging, runs purely in the browser.',
        'Audio Echo Effect Tool',
        'Online audio echo and reverb tool that adjusts the dry/wet mix and delay parameters to add a sense of space; upload audio to preview in real time and export. Suited to voice-over and music production, runs purely in the browser.',
        'Audio Playback Speed Adjuster',
        'Online audio speed changer: upload audio, adjust playback speed, optionally preserve the original pitch (speed change without pitch shift), and export WAV. Suited to podcasts and language learning, processed entirely in the browser.',
        'Upload audio, drag a selection on the waveform, preview it and export as WAV. Processed locally; the file is never uploaded.',
        'Audio Volume Adjuster',
        '🔊 Audio Volume Adjuster',
        '🎤 Online Recording Tool',
        'About "Audio Tools"',
        'This Audio Tools collection gathers 7 free online tools covering the common calculation, conversion and lookup needs of audio work. Whether you are a practitioner, a student or an ordinary user, you will find ready-to-use utilities here. Every tool runs purely in the browser; no data is uploaded to the server, so your privacy and security are protected.',
        'Audio tools included on this page (representative tools only):',
        'These tools help you finish common audio tasks fast, with no need to memorize complex formulas or convert by hand - input and you get the result.',
        'Do the Audio Tools require downloads or registration?',
        'No. All Audio Tools on this page are pure front-end online tools: open the page and use them right away, with no software to install, no account to register, and no data uploaded.',
        'Are the Audio Tools results accurate, and is the data safe?',
        'The tools compute in your browser using public math formulas and common industry standards, so results are available instantly. All computation happens locally on your device; no data is uploaded to the server, so privacy and security are guaranteed.',
    ]))


if __name__ == '__main__':
    main()

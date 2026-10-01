#!/usr/bin/env python3
# gen_acoustics_b6.py — acoustics b6 (3 slugs): string-fundamental/wavelength-frequency/wavelength-from-freq
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'acoustics')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'acoustics')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

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
    out = {'slug': slug, 'industry': 'acoustics', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

SFQ = [
 "String Fundamental (f1 = (1/2L)·sqrt(T/u))",
 "The fundamental of a string fixed at both ends depends on tension, linear density and length.",
 "String Fundamental Calculator",
 "/ String Fundamental",
 "String Fundamental",
 "📖 View Guide: \"String Fundamental (f1 = (1/2L)·sqrt(T/u))\"",
 "L=0.65m, T=80N, u=0.01 gives about 68.8 Hz.",
 "String Length (m)",
 "Tension (N)",
 "Linear Density (kg/m)",
 "f1 = (1/2L)·sqrt(T/u); u is the linear density (kg/m).",
 "📚 Deep Dive: Fundamental frequency of a string",
 "The fundamental f1=(1/2L)·sqrt(T/u), with length L, tension T and linear density u.",
 "Understand the tension-pitch relation when tuning guitar or violin.",
 "String instrument design or tuning calculations.",
 "String fundamental",
 "String length L=0.65 m, tension T=80 N, linear density u=0.001 kg/m gives f1=(1/2·0.65)·sqrt(80/0.001)=0.769·sqrt(80000)=0.769·282.8=217.5 Hz.",
 "Why does tightening a string raise its pitch?",
 "Increasing tension T raises sqrt(T/u) and thus the fundamental, so tuning changes tension via the peg.",
 "How does linear density affect it?",
 "Larger u lowers the fundamental, so thicker or denser strings sound lower, usually set together with tension.",
]

WFR = [
 "Wavelength-Frequency (lambda = v / f)",
 "Given wave speed and frequency, find the sound wavelength.",
 "Wavelength and Frequency Converter",
 "/ Wavelength-Frequency Conversion",
 "Wavelength-Frequency Conversion",
 "📖 View Guide: \"Wavelength-Frequency (lambda = v / f)\"",
 "Wave Speed (m/s)",
 "343 m/s and 440 Hz correspond to a wavelength of about 0.78 m (note A4).",
 "📚 Deep Dive: The relation between wavelength and frequency",
 "In air lambda=c/f, giving the spatial period from the frequency.",
 "Loudspeaker crossover and absorber thickness design depend on wavelength.",
 "Understand that low frequencies have long wavelengths and high frequencies short ones.",
 "Wavelength at 1 kHz",
 "With c=343 m/s and f=1000 Hz, lambda=343/1000=0.343 m, about 34 cm.",
 "Why are low frequencies hard to absorb?",
 "Low frequencies have very long wavelengths (e.g. 50 Hz is about 6.9 m) and conventional absorbers are far thinner than the wavelength, so absorption is inefficient.",
 "Is wavelength inversely proportional to frequency?",
 "Yes in a fixed medium: lambda=c/f, so doubling the frequency halves the wavelength.",
]

WFF = [
 "Wavelength from frequency",
 "Enter the frequency (and sound speed) to get the wavelength.",
 "Wavelength Calculator (from Frequency)",
 "/ Wavelength Calculator (from Frequency)",
 "📖 View Guide: \"Wavelength from frequency\"",
 "lambda = c/f. 1 kHz in air gives lambda=0.343 m.",
 "1 kHz in air gives lambda=0.343 m.",
 "📚 Deep Dive: Wavelength from frequency (multiple media)",
 "Sound speed differs across media (air, water, steel), so lambda=c/f changes accordingly.",
 "The wavelength of ultrasound in a medium determines resolution and penetration.",
 "In acoustic design choose the medium's speed to compute the wavelength.",
 "Wavelength in water",
 "In water c=1480 m/s, f=100 kHz gives lambda=1480/1e5=0.0148 m=14.8 mm, far shorter than in air at the same frequency.",
 "Is the wavelength the same across media at a fixed frequency?",
 "No: wavelength depends on the medium's speed; water conducts sound about 4.3x faster than air, so the same frequency gives about 4.3x the wavelength.",
 "Why does ultrasound imaging resolution come down to wavelength?",
 "Resolution is roughly one wavelength, so the shorter the wavelength (higher the frequency) the finer the detail resolved.",
]

write('string-fundamental', build('string-fundamental', SFQ))
write('wavelength-frequency', build('wavelength-frequency', WFR))
write('wavelength-from-freq', build('wavelength-from-freq', WFF))

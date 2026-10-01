#!/usr/bin/env python3
# gen_acoustics_b5.py — acoustics b5 (5 slugs): sound-power-level/sound-pressure-level/sound-speed-air/spl-add/spring-natural-freq
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

SPW = [
 "Sound power level from sound power (W0=10^-12 W)",
 "Enter the sound power to get the sound power level.",
 "Sound Power Level Calculator",
 "/ Sound Power Level Calculator",
 "📖 View Guide: \"Sound power level from sound power (W0=10^-12 W)\"",
 "Sound Power W (W)",
 "📚 Deep Dive: Sound power level conversion",
 "Convert equipment sound power W to level Lw=10·log10(W/W0), W0=10^-12 W.",
 "Add the levels of different devices directly to get the total sound power level.",
 "Unify product noise ratings onto the Lw scale.",
 "Sound power level",
 "Equipment sound power W=0.001 W with W0=10^-12 W gives Lw=10·log10(1e9)=90 dB.",
 "Does sound power level depend on distance?",
 "No: the sound power level describes the source itself and does not vary with measurement distance;",
 "sound pressure level",
 " varies with distance.",
 "How do multiple devices combine?",
 "Convert back to power, sum, then take the log: Lw_total=10·log10(sum(10^(Lwi/10))).",
]

SPL = [
 "Sound pressure level from sound pressure (p0=20 uPa)",
 "Enter the sound pressure (rms) to get the SPL.",
 "Sound Pressure Level Calculator",
 "/ Sound Pressure Level Calculator",
 "📖 View Guide: \"Sound pressure level from sound pressure (p0=20 uPa)\"",
 "Sound Pressure p (rms) (Pa)",
 "p=0.632 Pa -> about 90 dB (near the pain threshold).",
 "📚 Deep Dive: Sound pressure level conversion",
 "Convert the rms pressure p to level Lp=20·log10(p/p0), p0=20 uPa.",
 "Understand how everyday noise levels in dB(A) map to pressure.",
 "Convert a calibrated microphone voltage to SPL.",
 "Sound pressure level",
 "With rms pressure p=0.02 Pa and reference p0=20 uPa=2x10^-5 Pa, Lp=20·log10(0.02/2e-5)=20·log10(1000)=60 dB, about normal conversation level.",
 "Why is 20 uPa the reference?",
 "It is the hearing-threshold pressure for young ears near 1 kHz, adopted as the 0 dB SPL reference.",
 "Are dB and dB(A) the same?",
 "No: dB(A) additionally applies A-weighting to mimic the ear's reduced sensitivity to low frequencies, tracking perceived loudness more closely.",
]

SSA = [
 "Speed of Sound in Air (v = 331.4 + 0.6·T)",
 "In dry air the speed of sound rises nearly linearly with temperature.",
 "Speed of Sound in Air Calculator",
 "/ Speed of Sound in Air",
 "Speed of Sound in Air",
 "📖 View Guide: \"Speed of Sound in Air (v = 331.4 + 0.6·T)\"",
 "v = 331.4 + 0.6·T (C), a dry-air approximation.",
 "At 20 C the speed is about 343 m/s.",
 "📚 Deep Dive: Speed of sound in air versus temperature",
 "The speed c=331.3+0.606·T (T in Celsius) is used for temperature correction.",
 "Convert outdoor acoustic measurements using the air temperature.",
 "Estimate how temperature affects wind-instrument tuning.",
 "Speed at 20 C",
 "At T=20 C, c=331.3+0.606·20=343.4 m/s, consistent with the common value of 343 m/s.",
 "Does humidity affect the speed much?",
 "At room temperature the effect is small (<1%), so engineering work mostly uses the temperature approximation; precise work can add a humidity correction.",
 "Why does sound speed up when it gets warmer?",
 "Higher temperature makes gas molecules move more vigorously and restores elasticity faster, so the speed grows with the",
 "square root",
 " of absolute temperature.",
]

SPD = [
 "Combining two sound pressure levels (L = 10·log10(10^(L1/10)+10^(L2/10)))",
 "Two sound pressure levels cannot be added directly; they must be summed energetically.",
 "Sound Pressure Level Addition Calculator",
 "/ Sound Pressure Level Addition",
 "Sound Pressure Level Addition",
 "📖 View Guide: \"Combining two sound pressure levels (L = 10·log10(10^(L1/10)+10^(L2/10)))\"",
 "Sound Pressure Level 1 (dB)",
 "Sound Pressure Level 2 (dB)",
 "Energy sum: L = 10·log10(10^(L1/10)+10^(L2/10)).",
 "Two identical 80 dB sources give 83 dB (not 160).",
 "📚 Deep Dive: Adding multiple sound pressure levels",
 "For simultaneous sources, the total SPL is L=10·log10(sum(10^(Li/10))).",
 "Aggregate the contributions of each source in noise prediction.",
 "Verify that 'N equal sources raise the level by 10·log10(N) dB'.",
 "Multiple sources combined",
 "Four devices of 80 dB each: L=10·log10(4·10^8)=10·log10(4x10^8)=86.0 dB, which is 10·log10(4)=6 dB above a single unit.",
 "What is the rule for equal sources?",
 "N equal levels add 10·log10(N) dB: 2 sources give +3, 4 give +6 and 10 give +10 dB.",
 "Do I need to add every term when the levels differ a lot?",
 "Yes, you must sum each 10^(Li/10) term and then take the log; you cannot simply take the largest.",
]

SNF = [
 "Natural frequency (f = (1/2·pi)·sqrt(k/m))",
 "The natural frequency of an undamped spring-mass system depends on stiffness and mass.",
 "Spring-Mass Natural Frequency Calculator",
 "/ Spring Natural Frequency",
 "Spring Natural Frequency",
 "📖 View Guide: \"Natural frequency (f = (1/2·pi)·sqrt(k/m))\"",
 "k=100 N/m and m=1 kg give about 1.59 Hz.",
 "📚 Deep Dive: Natural frequency of a spring-mass system",
 "With spring stiffness k and mass m, the natural frequency is f_n=(1/2·pi)·sqrt(k/m).",
 "In vibration isolation design choose a natural frequency below the disturbance frequency.",
 "Estimate resonance risk in mechanical structures.",
 "Natural frequency",
 "With stiffness k=1000 N/m and mass m=0.25 kg, f_n=(1/2·pi)·sqrt(1000/0.25)=(1/2·pi)·sqrt(4000)=10.1 Hz.",
 "What does a low natural frequency mean?",
 "Larger mass or lower stiffness lowers the natural frequency, making it easier to isolate high-frequency disturbance (higher isolation ratio).",
 "How does this relate to audio acoustics?",
 "Structural vibration radiates sound, and the natural frequency sets the main band of structural noise, making it a coupling point in acoustic design.",
]

write('sound-power-level', build('sound-power-level', SPW))
write('sound-pressure-level', build('sound-pressure-level', SPL))
write('sound-speed-air', build('sound-speed-air', SSA))
write('spl-add', build('spl-add', SPD))
write('spring-natural-freq', build('spring-natural-freq', SNF))

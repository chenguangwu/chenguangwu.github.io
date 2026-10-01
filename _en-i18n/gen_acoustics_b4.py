#!/usr/bin/env python3
# gen_acoustics_b4.py — acoustics b4 (5 slugs): pipe-open/reverberation-time/room-axial-mode/sound-intensity-level/sound-intensity-spherical
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

POP = [
 "Open-pipe fundamental (f1 = v / 2L)",
 "A pipe open at both ends has a fundamental wavelength twice the pipe length.",
 "Open Pipe Fundamental Calculator",
 "/ Open Pipe Fundamental",
 "Open Pipe Fundamental",
 "📖 View Guide: \"Open-pipe fundamental (f1 = v / 2L)\"",
 "A pipe open at both ends has f1 = v/2L and contains all harmonics.",
 "343 m/s and a 0.5 m pipe give about 343 Hz.",
 "📚 Deep Dive: Standing-wave frequencies in an open pipe",
 "A pipe open at both ends (e.g. flute, open pipe) has standing-wave frequencies f_n=n·c/(2L), n=1,2,3...",
 "Compute the open-pipe fundamental and all integer harmonics.",
 "Back-solve frequency from length when tuning wind instruments.",
 "With pipe length L=0.66 m and sound speed c=343 m/s, the fundamental f1=c/(2L)=343/1.32=260 Hz; harmonics are 2f1, 3f1... (integer multiples).",
 "Why do open and closed pipes sound different?",
 "An open pipe contains all integer harmonics while a closed pipe has only odd ones, so the differing harmonic structure changes the timbre.",
 "Does a real pipe mouth need correction?",
 "A real open end extends slightly beyond the pipe (end correction), so the effective length is a bit longer than the geometric one and precision work must add that correction.",
]

RVT = [
 "Reverberation Time (T60 = 0.161·V / A)",
 "Estimate room reverberation time with the Sabine formula, where A is the total absorption in sabins.",
 "Reverberation Time (Sabine) Calculator",
 "/ Reverberation Time",
 "Reverberation Time",
 "📖 View Guide: \"Reverberation Time (T60 = 0.161·V / A)\"",
 "Total Absorption (sabin)",
 "T60 = 0.161·V/A (A in sabins).",
 "100 m3 with 10 sabins gives about 1.61 s.",
 "📚 Deep Dive: Sabine reverberation time",
 "For halls, studios and classrooms, T=0.161V/A with A=sum(Si·ai).",
 "Back-solve the absorption needed for the intended use (speech / music).",
 "Account for the change in reverberation time before and after a retrofit.",
 "Room reverberation time",
 "Room volume V=500 m3, total surface absorption A=100 sabins, T=0.161·500/100=0.805 s, a relatively dry speech-oriented space.",
 "Where does 0.161 in the Sabine formula come from?",
 "It derives from the sound speed c=343 m/s: 0.161=0.163·(V in m3 / c), an empirical metric coefficient.",
 "Is a longer reverberation time better?",
 "Concert halls often favour a rich 1.5-2.5 s, while meeting rooms and classrooms want short values (<1 s) for speech clarity.",
]

RAM = [
 "Axial resonance frequencies of a rectangular room",
 "Enter the room dimension and mode order n to get the axial resonance frequency.",
 "Room Axial Normal Mode Calculator",
 "/ Room Axial Normal Mode Calculator",
 "📖 View Guide: \"Axial resonance frequencies of a rectangular room\"",
 "f_n = n·c/(2L). The first mode of a 5 m room is about 34.3 Hz.",
 "Room Dimension L (m)",
 "Mode Order n",
 "The first mode of a 5 m room is about 34.3 Hz.",
 "📚 Deep Dive: Axial mode frequencies of a room",
 "A rectangular room has axial normal frequencies f=n·c/(2L) along length, width and height.",
 "Predict where low-frequency boom or dips occur in small rooms.",
 "Place speakers and the listening seat away from strong modal regions.",
 "Axial mode",
 "With room length L=5 m and sound speed c=343 m/s, the first axial mode f1=c/(2L)=34.3 Hz and the second 68.6 Hz, from which the low-frequency standing-wave distribution follows.",
 "How do axial modes differ from oblique / tangential modes?",
 "Axial modes run along one dimension (n in one axis), tangential along two and oblique along three; axial modes usually carry the most energy and deserve the most attention.",
 "Why is bass hard to control in small rooms?",
 "Modes are sparse and concentrated in the audible low frequencies, and between neighbouring modes colouration appears (some frequencies too strong, others too weak).",
]

SIL = [
 "Sound Intensity Level (L_I = 10·log10(I / I0))",
 "Intensity level is referenced to I0 = 1x10^-12 W/m2.",
 "/ Sound Intensity Level",
 "Sound Intensity Level",
 "📖 View Guide: \"Sound Intensity Level (L_I = 10·log10(I / I0))\"",
 "Sound Intensity (W/m2)",
 "1x10^-6 W/m2 corresponds to 60 dB.",
 "📚 Deep Dive: Intensity level from sound pressure",
 "In a free field I=p_rms2/(rho·c), then compute the",
 "intensity level",
 "In intensity measurement, derive it from sound pressure and particle velocity.",
 "sound pressure level",
 " consistency with the intensity level.",
 "Pressure to intensity",
 "With rms pressure p_rms=0.1 Pa and air rho·c=412, I=p2/(rho·c)=0.01/412=2.43x10^-5 W/m2, L_I=10·log10(2.43x10^-5/1e-12)=73.9 dB.",
 "What is the relation between intensity and pressure?",
 "In a plane-wave free field I=p_rms2/(rho·c); intensity is the sound power flow per unit area.",
 "When do intensity level and pressure level differ?",
 "They differ with reflections, in the near field or in a diffuse field; they are equal for plane waves in a free field.",
 "How to use Sound Intensity Level (L_I = 10·log10(I / I0))",
 "In a free field I=p_rms2/(rho·c), then compute the intensity level L_I=10·log10(I/I0).",
 "Sound Intensity Level expresses the intensity relative to the reference I0=10^-12 W/m2 in decibels on a logarithmic scale, describing how strong a sound is.",
 "Units and magnitude reference",
 "Unit dB. 0 dB is about the hearing threshold, 60 dB normal conversation, 90 dB a lawn mower and 120 dB the pain threshold; every +10 dB roughly doubles perceived loudness.",
 "Applicability limits and notes",
 "Using L",
 "=10·log10(I/I0). Real sound fields are affected by reflection, absorption and microphone frequency response; this result is a standard-model estimate, and precise acoustic measurement needs calibrated equipment and an anechoic environment.",
]

SIS = [
 "Sound intensity at distance r from a point source",
 "Enter sound power and distance to get the intensity after spherical spreading.",
 "Free-Field Intensity I = P / (4·pi·r2)",
 "/ Spherical Sound Intensity Calculator",
 "Spherical Sound Intensity Calculator",
 "📖 View Guide: \"Sound intensity at distance r from a point source\"",
 "I = P/(4·pi·r2) (spherical free field). 1 W at 2 m -> I=0.0199 W/m2.",
 "Sound Power P (W)",
 "I = P/(4·pi·r2) (spherical free field).",
 "1 W at 2 m -> I=0.0199 W/m2.",
 "📚 Deep Dive: Spherically spreading sound intensity",
 "A point source radiates I=P/(4·pi·r2), decaying spherically with distance.",
 "Estimate intensity at distance for noise prediction.",
 "Cross-check with the inverse-square law for",
 "sound pressure level",
 " decay.",
 "Point source intensity",
 "For a point source of power P=1 W, at r=10 m, I=1/(4·pi·100)=7.96x10^-4 W/m2, corresponding to an",
 "intensity level",
 " of about 89 dB.",
 "Is spherical spreading the same as free-space decay?",
 "Yes: point source energy",
 " spreads evenly",
 " over a sphere of radius r, so intensity decays with r2, which is the inverse-square law.",
 "Does it apply to line sources?",
 "No; a line source (e.g. a road) spreads cylindrically and decays by 3 dB per doubling of distance rather than 6 dB.",
]

write('pipe-open', build('pipe-open', POP))
write('reverberation-time', build('reverberation-time', RVT))
write('room-axial-mode', build('room-axial-mode', RAM))
write('sound-intensity-level', build('sound-intensity-level', SIL))
write('sound-intensity-spherical', build('sound-intensity-spherical', SIS))

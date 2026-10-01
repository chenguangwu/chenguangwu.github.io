#!/usr/bin/env python3
# gen_acoustics_b3.py — acoustics b3 (5 slugs): freq-to-note/intensity-inverse-square/intensity-level/mass-law-tl/pipe-closed
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

FTN = [
 "Map a frequency to the nearest 12-tone equal-tempered note name",
 "Enter a frequency to get the nearest standard note name (A4=440 Hz) and the cent deviation.",
 "Frequency to Note Calculator",
 "/ Frequency to Note Calculator",
 "📖 View Guide: \"Map a frequency to the nearest 12-tone equal-tempered note name\"",
 "Reference A4=440 Hz, 12-tone equal temperament.",
 "442 Hz -> A4, about +8 cents.",
 "📚 Deep Dive: Converting frequency to note name",
 "Tuner software maps the detected frequency to the nearest piano note name.",
 "Confirm which pitch a frequency corresponds to in a synth or arrangement.",
 "Understand 12-tone equal temperament and the 440 Hz reference in music teaching.",
 "The note for 440 Hz",
 "With A4=440 Hz as reference, MIDI pitch n=69+12·log2(f/440). f=440 gives n=69, i.e. A4; f=523.25 gives n=72, i.e. C5.",
 "How does equal temperament define notes?",
 "Adjacent semitones always differ by 2^(1/12)=1.0595, doubling each octave, with A4 set at 440 Hz.",
 "Why does the same note name have different frequencies?",
 "It depends on the reference pitch (e.g. A4=432 Hz vs 440 Hz systems); this tool defaults to the 440 Hz international standard.",
]

IIS = [
 "Sound Intensity Inverse-Square Law Calculator",
 "For a point source, sound intensity decays with the square of distance.",
 "/ Sound Intensity Inverse-Square",
 "Sound Intensity Inverse-Square",
 "📖 View the Sound Intensity Inverse-Square Law Calculator Guide",
 "Intensity Decay (I2 = I1·(r1/r2)2)",
 "Initial Intensity (W/m2)",
 "Initial Distance (m)",
 "I2 = I1·(r1/r2)2; spherical spreading from a point source.",
 "Doubling distance cuts intensity to 1/4.",
 "📚 Deep Dive: The inverse-square law for sound intensity",
 "In a reflection-free field a point source's intensity decays with the square of distance.",
 "Estimate how far the intensity drops when moving away from a machine.",
 "Explain why doubling distance drops the",
 "sound pressure level",
 " by about 6 dB.",
 "Doubling the distance, intensity",
 "For point source power P, at distance r1, I1=P/(4·pi·r12); at r2=2r1, I2=P/(4·pi·r22)=I1/4, i.e. intensity drops to 1/4, corresponding to a 6 dB drop in sound pressure level.",
 "Why does doubling distance drop 6 dB?",
 "Intensity varies inversely with distance squared; energy spreads over 4x the area, and 10·log10(1/4)=-6 dB.",
 "When does the inverse-square law fail?",
 "It holds only for a free field with a point source and no reflection or absorption; in a reverberant room the decay is slower.",
]

ITL = [
 "Intensity level from sound intensity (I0=10^-12 W/m2)",
 "Enter the sound intensity to get the intensity level.",
 "/ Sound Intensity Level Calculator",
 "📖 View Guide: \"Intensity level from sound intensity (I0=10^-12 W/m2)\"",
 "Sound Intensity I (W/m2)",
 "📚 Deep Dive: Computing the sound intensity level",
 "From intensity I the level L_I=10·log10(I/I0) with I0=10^-12 W/m2.",
 "Convert measured intensity to a logarithmic scale for noise assessment.",
 "sound pressure level",
 " serves as a cross-check (the two are equal in a free field).",
 "Intensity level",
 "At intensity I=10^-6 W/m2 with I0=10^-12 W/m2, L_I=10·log10(10^6)=60 dB.",
 "What is the difference between intensity level and sound pressure level?",
 "Intensity level is defined from intensity, sound pressure level from pressure; in a free field with plane waves the two are numerically equal.",
 "Where does I0=10^-12 come from?",
 "It approximates the human hearing threshold near 1 kHz and is adopted as the reference intensity.",
 "How to use Intensity level from sound intensity (I0=10^-12 W/m2)",
 "Intensity Level L",
 " expresses a sound's intensity relative to the reference I0=10^-12 W/m2 on a logarithmic decibel (dB) scale; the larger the value, the stronger the sound.",
 "Units and magnitude reference",
 "Unit dB (decibel, a dimensionless logarithmic ratio). Everyday reference: 0 dB hearing threshold, 40 dB normal conversation, 70 dB vacuum cleaner, above 85 dB prolonged exposure risks hearing damage, 120 dB pain threshold.",
 "Applicability limits and notes",
 "The formula L",
 "=10·log10(I/I0) applies under the point-source free-field approximation; actual sound pressure level is also affected by the inverse-square law, environmental reflection and frequency weighting (A-weighting). This tool uses an ideal model, for quick estimates only.",
]

MLT = [
 "Field sound transmission loss of a single-leaf homogeneous wall",
 "Enter frequency and surface density to estimate transmission loss TL by the mass law.",
 "Mass Law Transmission Loss Calculator",
 "/ Mass Law Transmission Loss Calculator",
 "📖 View Guide: \"Field sound transmission loss of a single-leaf homogeneous wall\"",
 "Surface Density m (kg/m2)",
 "📚 Deep Dive: Estimating transmission loss by the mass law",
 "Quick estimate for single-leaf walls and floors: TL=20·log10(m·f)-48.",
 "Compare insulation performance across surface densities and frequencies.",
 "Predict the 'doubling mass adds only 6 dB' effect before an insulation retrofit.",
 "Single-leaf wall insulation",
 "With surface density m=20 kg/m2 and frequency f=500 Hz, TL=20·log10(20·500)-48=20·log10(10000)-48=80-48=32 dB.",
 "Why does doubling mass add only about 6 dB?",
 "TL follows 20·log10 of mass, so doubling mass adds +6 dB; merely thickening a wall has limited benefit.",
 "What are the limits of the mass law?",
 "It ignores the coincidence effect, stiffness and damping; near the critical frequency the real insulation is markedly below the estimate.",
]

PCL = [
 "Closed-pipe fundamental (f1 = v / 4L)",
 "A pipe closed at one end and open at the other has a fundamental wavelength four times the pipe length.",
 "Closed Pipe Fundamental Calculator",
 "/ Closed Pipe Fundamental",
 "Closed Pipe Fundamental",
 "📖 View Guide: \"Closed-pipe fundamental (f1 = v / 4L)\"",
 "A pipe closed at one end has f1 = v/4L and contains only odd harmonics.",
 "343 m/s and a 0.5 m pipe give about 171.5 Hz.",
 "📚 Deep Dive: Standing-wave frequencies in a closed pipe",
 "A pipe closed at one end and open at the other (e.g. closed-pipe instruments, bottle mouths) has standing-wave frequencies f_n=n·c/(4L), n=1,3,5...",
 "Compute the closed-pipe fundamental and odd harmonics.",
 "Predict the sounding frequency for pipe organs or teaching demos.",
 "With pipe length L=0.34 m and sound speed c=343 m/s, the fundamental f1=c/(4L)=343/1.36=252 Hz; only odd harmonics (3f1, 5f1...) are allowed.",
 "Why does a closed pipe have only odd harmonics?",
 "The closed end must be a pressure antinode and the open end a node, so the boundary condition allows only odd n and even harmonics are missing.",
 "How does it differ from an open pipe?",
 "An open pipe has nodes at both ends, f_n=n·c/(2L) with all integer harmonics, and its fundamental is twice that of a closed pipe of the same length.",
]

write('freq-to-note', build('freq-to-note', FTN))
write('intensity-inverse-square', build('intensity-inverse-square', IIS))
write('intensity-level', build('intensity-level', ITL))
write('mass-law-tl', build('mass-law-tl', MLT))
write('pipe-closed', build('pipe-closed', PCL))

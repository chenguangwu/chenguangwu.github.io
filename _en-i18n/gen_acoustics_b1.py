#!/usr/bin/env python3
# gen_acoustics_b1.py — acoustics b1 (5 slugs): absorption-coeff-sabine/acoustic-impedance/beat-frequency/combine-two-spl/critical-distance
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

ACS = [
 "Back-solve average absorption coefficient from the Sabine formula",
 "Enter room volume, surface area and reverberation time to back-solve the average absorption coefficient.",
 "Average Absorption Coefficient Calculator",
 "/ Average Absorption Coefficient Calculator",
 "📖 View Guide: \"Back-solve average absorption coefficient from the Sabine formula\"",
 "Surface Area S (m2)",
 "\u1fb1 = 0.161·V/(S·RT60) (metric).",
 "📚 Deep Dive: Measuring material absorption coefficient by the Sabine method",
 "Measure reverberation time before and after laying the specimen in a reverberation chamber, then back-solve the material absorption coefficient.",
 "Compare the lab absorption of different finishes (perforated panels, soft cladding, wood-wool board) for selection.",
 "Check whether the single-value coefficient in a report is consistent with the measured reverberation time.",
 "Compute the absorption coefficient",
 "Reverberation room V=200 m3, empty-room RT T0=6.0 s; after laying specimen S=10 m2, T1=4.5 s. From A=0.161V/T the empty-room absorption A0=53.7 sabins, after laying A1=71.6 sabins, specimen contribution dA=17.9, absorption coefficient a=dA/S=1.79 (>1 is a normal upper bound due to edge and mounting conditions).",
 "Can the absorption coefficient exceed 1?",
 "a>1 is common in lab measurements due to mounting, edge effects and test uncertainty; engineering practice uses the single value under standard conditions, not extremes.",
 "What is the relation between Sabine and ISO 354?",
 "ISO 354 determines building-product absorption in a reverberation room; its computation rests on the Sabine formula and absorption conversion, and is the source standard for reported coefficients.",
]

AIMP = [
 "Product of medium density and sound speed",
 "Enter medium density and sound speed to get the characteristic acoustic impedance.",
 "Characteristic Impedance Z = p·c",
 "/ Acoustic Impedance Calculator",
 "Acoustic Impedance Calculator",
 "📖 View Guide: \"Product of medium density and sound speed\"",
 "Z = p·c. Air about 415 Rayl, water about 1.48e6 Rayl. 1.2x343 = 412 Rayl.",
 "Z = p·c. Air about 415 Rayl, water about 1.48e6 Rayl.",
 "📚 Deep Dive: Computing the characteristic acoustic impedance of a medium",
 "Given medium density and sound speed, compute the characteristic impedance to judge transmission and reflection strength.",
 "Compare air, water and",
 " impedance to explain differences in insulation and coupling.",
 "Estimate interface reflection when designing matching layers for ultrasound transducers.",
 "Air characteristic impedance",
 "At 20 C, air density p=1.20 kg/m3 and sound speed c=343 m/s give Z=pc=412 Pa·s/m. Water: density about 1000, sound speed about 1480, Z=1.48x10^6, far above air, so the water-air interface reflects strongly.",
 "How is acoustic impedance like electrical resistance?",
 "Acoustic impedance Z=p/u (sound pressure / particle velocity), analogous to electrical impedance, sets the reflection and transmission ratio at an interface.",
 "Why chase impedance mismatch for sound insulation?",
 "Interface reflection coefficient r=(Z2-Z1)/(Z2+Z1): a larger mismatch gives stronger reflection and weaker transmission, the physical basis of mass-law insulation.",
]

BFR = [
 "Beat Frequency (f_beat = |f1 - f2|)",
 "Two close frequencies superpose into beats; the beat frequency is their difference.",
 "Beat Frequency Calculator",
 "/ Beat Frequency",
 "Beat Frequency",
 "📖 View Guide: \"Beat Frequency (f_beat = |f1 - f2|)\"",
 "440 and 444 Hz superpose into a 4 Hz beat.",
 "📚 Deep Dive: Computing the beat frequency of two tones",
 "When tuning guitar or violin, listen to the beat between two strings to align their frequencies.",
 "Judge interference of two close frequencies on a scope or in audio.",
 "Observe the beat-disappearance point when calibrating tuning forks or generators.",
 "Find the beat frequency",
 "Two tuning forks at f1=440 Hz and f2=444 Hz give f_beat=|f1-f2|=4 Hz, i.e. 4 loudness swells per second; as the frequencies converge the beat frequency approaches 0.",
 "How are beats produced?",
 "Two close-frequency waves superpose so the resultant amplitude fluctuates at the difference frequency; the ear hears periodic loudness swells, which are the beats.",
 "Can the beat frequency exceed the two frequencies?",
 "No; the beat frequency equals the absolute difference of the two frequencies, necessarily below the higher of them.",
]

CSP = [
 "Total level of two incoherent sources",
 "Enter two sound pressure levels and get the energy-summed total level.",
 "Two-Level SPL Combination Calculator",
 "/ Two-Level SPL Combination Calculator",
 "📖 View Guide: \"Total level of two incoherent sources\"",
 "Sound Pressure Level L1 (dB)",
 "Sound Pressure Level L2 (dB)",
 "Energy sum: L=10log10(10^(L1/10)+10^(L2/10)).",
 "📚 Deep Dive: Energy summation of two sound pressure levels",
 "Two devices running together, find the combined total",
 "sound pressure level",
 " rather than adding the levels directly.",
 "Verify the rule of thumb that adding an identical source raises the level only 3 dB.",
 "Account total-level change before and after noise control.",
 "Two equal levels combined",
 "Two identical machines at 80 dB each give L=10·log10(10^8+10^8)=10·log10(2·10^8)=83.0 dB, i.e. equal levels add only 3 dB, not 160 dB.",
 "Why can't dB be added directly?",
 "The decibel is logarithmic and represents an energy ratio; summing requires converting back to energy (10^(L/10)), adding, then taking the log.",
 "What if two levels differ greatly?",
 "If the difference is =10 dB, the quieter source barely affects the total, which is about the louder one (error <0.5 dB).",
]

CDS = [
 "Critical distance where direct and reverberant sound are equal",
 "Enter room volume, reverberation time and directivity factor to estimate the critical distance.",
 "Critical Distance (Reverberant Field) Calculator",
 "/ Critical Distance (Reverberant Field) Calculator",
 "📖 View Guide: \"Critical distance where direct and reverberant sound are equal\"",
 "r_c = 0.141·sqrt(Q·V/RT60) (metric approximation). V=200, RT60=1, Q=1 -> r_c=2 m.",
 "Directivity Factor Q",
 "r_c = 0.141·sqrt(Q·V/RT60) (metric approximation).",
 "📚 Deep Dive: Computing the critical distance",
 "When placing a conference speaker or loudspeaker, judge when direct sound is masked by reverberation.",
 "Determine the optimal miking/listening distance in hall acoustics design.",
 "Estimate the knee where speech intelligibility decays with distance in open offices.",
 "Find the critical distance",
 "With room constant R=50 m2 and source directivity Q=1, critical distance Dc=0.141·sqrt(Q·R)=0.141·sqrt(50)=1.0 m. Beyond about 1 m the reverberant field dominates and clarity drops.",
 "Is a larger critical distance better?",
 "Usually good for speech intelligibility: a larger critical distance means more absorption and less reverberation, so speech stays clear at distance.",
 "How does directivity Q affect it?",
 "Larger Q (more focused source) gives larger critical distance, since more energy radiates toward the listener.",
 "How to use Critical distance where direct and reverberant sound are equal",
]

write('absorption-coeff-sabine', build('absorption-coeff-sabine', ACS))
write('acoustic-impedance', build('acoustic-impedance', AIMP))
write('beat-frequency', build('beat-frequency', BFR))
write('combine-two-spl', build('combine-two-spl', CSP))
write('critical-distance', build('critical-distance', CDS))

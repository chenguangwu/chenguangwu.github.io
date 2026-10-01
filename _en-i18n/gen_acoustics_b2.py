#!/usr/bin/env python3
# gen_acoustics_b2.py — acoustics b2 (5 slugs): decibel-power-ratio/decibel-power/decibel-voltage-ratio/decibel-voltage/doppler-acoustic
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

DPR = [
 "Convert a power ratio to decibels",
 "Enter two power values and get their ratio in decibels.",
 "Power Ratio to Decibel Converter",
 "/ Power Ratio to Decibel Converter",
 "📖 View Guide: \"Convert a power ratio to decibels\"",
 "Reference Power P1 (W)",
 "Compared Power P2 (W)",
 "Power quantity: dB = 10log10(P2/P1).",
 "📚 Deep Dive: Converting a power ratio to decibels",
 "When amplifier gain is given as a power ratio, converting to dB eases cascaded calculations.",
 "Compare two sound powers or",
 "electric power",
 " in relative terms.",
 "Convert a multiplier (e.g. 100x power) to a logarithmic scale.",
 "Power ratio to dB",
 "Power rises from 1 W to 100 W, ratio 100, L=10·log10(100)=20 dB. Every 10x power step is +10 dB.",
 "Why does power use 10 times the log?",
 "The decibel is essentially the log of a power ratio (10 times the bel); energy quantities such as sound and electric power use 10·log10.",
 "How does it differ from voltage dB?",
 "Voltage / sound pressure relate to the",
 "square root",
 " of power, hence 20·log10; for the same ratio voltage dB is twice power dB.",
]

DPW = [
 "Power Decibel (L = 10·log10(P / P0))",
 "A power ratio expressed as ten times the logarithm, in decibels.",
 "Power Decibel Converter",
 "/ Power Decibel Conversion",
 "Power Decibel Conversion",
 "📖 View Guide: \"Power Decibel (L = 10·log10(P / P0))\"",
 "Reference Power (W)",
 "L = 10·log10(P / P0) (power quantity).",
 "Power 10x = 10 dB.",
 "📚 Deep Dive: Power and absolute decibel conversion",
 "Sound Power Level",
 "Lw=10·log10(W/W0), W0=10^-12 W, used to label equipment sound power.",
 "Electric power",
 " is expressed in dBW (reference 1 W) or dBm (reference 1 mW).",
 "Convert a measured",
 "power reading",
 " to a unified dB scale for comparison.",
 "Equipment radiates sound power W=0.01 W with W0=10^-12 W, Lw=10·log10(0.01/1e-12)=10·log10(1e10)=100 dB.",
 "How do dBW and dBm convert?",
 "dBm uses a 1 mW reference and dBW a 1 W reference, 30 dB apart: X dBW = (X+30) dBm.",
 "Is sound power level the same as",
 "sound pressure level",
 "?",
 "No: sound power level describes the source's total radiating capacity, while sound pressure level also depends on distance and room; the two are linked through the room constant.",
]

DVR = [
 "Convert a field quantity (voltage / sound pressure) ratio to decibels",
 "Enter two voltages (or sound pressures) and get their ratio in decibels.",
 "Voltage Ratio to Decibel Converter",
 "/ Voltage Ratio to Decibel Converter",
 "📖 View Guide: \"Convert a field quantity (voltage / sound pressure) ratio to decibels\"",
 "Reference Voltage V1 (V)",
 "Compared Voltage V2 (V)",
 "Field quantity: dB = 20log10(V2/V1).",
 "📚 Deep Dive: Converting a voltage ratio to decibels",
 "Convert an amplifier's voltage gain from a multiplier to dB.",
 "Compare the relative magnitude of two signal voltages.",
 "Express filter and attenuator insertion loss in voltage dB.",
 "Voltage ratio to dB",
 "Output is 10x the input, L=20·log10(10)=20 dB; if it is 1/10, then -20 dB.",
 "Why 20 instead of 10 for voltage?",
 "Power is proportional to voltage squared, and power dB uses 10·log10; expanding gives 20·log10(voltage ratio), so voltage / sound pressure quantities use the 20x factor.",
 "What does a negative dB mean?",
 "A negative value means the ratio is below 1, i.e. attenuation or a level below the reference.",
]

DVL = [
 "Voltage Decibel (L = 20·log10(V / V0))",
 "Voltage, sound pressure and other field quantities expressed as twenty times the logarithm, in decibels.",
 "Voltage Decibel Converter",
 "/ Voltage Decibel Conversion",
 "Voltage Decibel Conversion",
 "📖 View Guide: \"Voltage Decibel (L = 20·log10(V / V0))\"",
 "Reference Voltage (V)",
 "L = 20·log10(V / V0) (field quantity).",
 "Voltage 10x = 20 dB.",
 "📚 Deep Dive: Absolute voltage and decibel conversion",
 "Electrical signals are expressed as dBV (reference 1 V) or dBu/dBm (reference 0.775 V).",
 "Bring audio line level and microphone level onto a common dB scale.",
 "Convert a measured voltage to a standard level unit for comparison.",
 "dBV conversion",
 "Signal voltage V=0.775 V against a 1 V reference gives 20·log10(0.775)=-2.2 dBV; against a 0.775 V reference it is 0 dBu.",
 "How do dBu and dBV convert?",
 "dBu uses a 0.775 V reference and dBV a 1 V reference, about 2.21 dB apart: X dBV = (X+2.21) dBu.",
 "Which is commonly used for microphone level?",
 "Professional audio uses dBu; consumer gear often dBV. Note the references differ and the values cannot be added directly.",
]

DOP = [
 "Acoustic Doppler Effect Calculator",
 "When a source moves at speed vs toward a stationary observer, the observed frequency rises.",
 "/ Acoustic Doppler",
 "Acoustic Doppler",
 "📖 View the Acoustic Doppler Effect Calculator Guide",
 "Source approaching (f' = f·v / (v - vs))",
 "Original Frequency (Hz)",
 "Source Speed (m/s)",
 "f' = f·v / (v - vs) for a source approaching the observer; when receding the denominator becomes v + vs.",
 "At a source speed of 34.3 m/s the shift is about +49 Hz.",
 "📚 Deep Dive: Computing the acoustic Doppler shift",
 "Estimate the siren pitch change as an ambulance approaches and recedes.",
 "Recover velocity from the frequency shift in ultrasonic speed measurement (blood flow, vehicle speed).",
 "Compensate the shift in acoustic ranging or moving-target detection.",
 "An approaching source",
 "Source frequency f=1000 Hz, sound speed c=343 m/s, source moving toward a stationary listener at vs=34.3 m/s gives f'=f·c/(c-vs)=1000·343/308.7=1111 Hz, a rise of about 111 Hz.",
 "Why does pitch rise when it approaches?",
 "As the source moves toward the listener the wavefronts are compressed and the arrival frequency rises; when receding they stretch and the frequency drops.",
 "Are listener motion and source motion symmetric?",
 "The formula is asymmetric: listener motion changes the denominator (reception rate), source motion changes the numerator (wave spacing), though the limiting results are close.",
]

write('decibel-power-ratio', build('decibel-power-ratio', DPR))
write('decibel-power', build('decibel-power', DPW))
write('decibel-voltage-ratio', build('decibel-voltage-ratio', DVR))
write('decibel-voltage', build('decibel-voltage', DVL))
write('doppler-acoustic', build('doppler-acoustic', DOP))

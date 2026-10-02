#!/usr/bin/env python3
# gen_signal_head.py — shared head for signal batches b1..b6
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'signal')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'signal')
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
    out = {'slug': slug, 'industry': 'signal', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
# body_s_b2.py
def main():
    write('db-power-ratio', build('db-power-ratio', [
        'Decibel value from two powers',
        'Convert the power ratio P1/P2 into the decibel dB scale: 10·log10(P1/P2).',
        'Power Ratio to Decibel Calculator',
        '/ Power Ratio to Decibel Calculator',
        'View "Decibel value from two powers" guide',
        'Enter powers P1, P2 to find the decibel ratio.',
        'Power ratio dB = 10·log10(P1/P2).',
        'Deep dive: Power ratio to decibel (10log10)',
        'Taking 10 times log10 of the two powers p1/p2 yields dB.',
        'Express link power gain/loss.',
        'Power reference when SNR is expressed in dB.',
        'L = 10xlog10(100/1) = 10x2 = 20 dB, meaning a power ratio of 100x.',
        'Attenuation case',
        'If p1=1, p2=10, then L = 10xlog10(0.1) = -10 dB, meaning attenuation by 10x.',
        'Why multiply by 10 for power dB?',
        'The decibel is based on the logarithm of the power ratio; since power corresponds to amplitude squared, the coefficient is 10 (20 for amplitude).',
        'How to interpret negative values?',
        'Negative dB means p1 is smaller than p2, i.e. attenuation or loss.',
    ]))
    write('db-voltage-ratio', build('db-voltage-ratio', [
        'Decibel value from two voltages',
        'Convert the voltage ratio V1/V2 into the decibel dB scale: 20·log10(V1/V2).',
        'Voltage Ratio to Decibel Calculator',
        '/ Voltage Ratio to Decibel Calculator',
        'View "Decibel value from two voltages" guide',
        'Enter voltages V1, V2 to find the decibel ratio.',
        'Voltage V1 (V)',
        'Voltage V2 (V)',
        'Voltage ratio dB = 20·log10(V1/V2).',
        'Deep dive: Voltage ratio to decibel (20log10)',
        'Taking 20 times log10 of the two voltages v1/v2 yields dB.',
        'Express amplifier voltage gain.',
        'The coefficient difference from power dB.',
        'L = 20xlog10(10/1) = 20x1 = 20 dB, meaning a voltage ratio of 10x.',
        'Half voltage',
        'If v1=1, v2=2 (half), then L = 20xlog10(0.5) ~ -6.02 dB, i.e. -6dB is about half voltage.',
        'Why 20 for voltage but 10 for power?',
        'Voltage squared is proportional to power, so after taking the logarithm the coefficient doubles: 20log10(v) = 10log10(v^2).',
        'How many times voltage corresponds to 3dB?',
        '20log10(x)=3 -> x~1.412x (the half-power point corresponds to amplitude 1/sqrt(2)~0.707).',
    ]))
    write('duty-cycle', build('duty-cycle', [
        'Duty cycle from on-time and period',
        'From period T and high-level on-time ton, compute the duty cycle D = ton/T of a pulse signal.',
        'Duty Cycle Calculator',
        '/ Duty Cycle Calculator',
        'View "Duty cycle from on-time and period" guide',
        'Enter on-time ton and period T to find the duty cycle.',
        'On-time ton (ms)',
        'Deep dive: Duty cycle',
        'The ratio of pulse on-time ton to period T gives the duty cycle.',
        'Duty cycle settings for PWM dimming and motor speed control.',
        'Compare average effects under different on-times.',
        'Duty cycle D = 2/10 x 100% = 20%; if ton increases to 5 then D=50% (half-period on).',
        'Full on',
        'If ton=T, then D=100%, equal to a continuously on DC.',
        'What is the relation between duty cycle and average voltage?',
        'Under an ideal switch, average voltage ~ duty cycle x supply voltage; see the pwm-average tool.',
        'Can the duty cycle exceed 100%?',
        'No, ton cannot exceed the period; the maximum is 100%.',
    ]))
    write('energy-discrete', build('energy-discrete', [
        'Signal energy from a sampled sequence',
        'For a discrete-time signal x[n], compute total energy E = Sum|x[n]|^2 or average power P = E/N.',
        'Discrete Signal Energy Calculator',
        '/ Discrete Signal Energy Calculator',
        'View "Signal energy from a sampled sequence" guide',
        'Enter a discrete sampled sequence (space- or comma-separated) to find the total signal energy.',
        'Sampled sequence x[n]',
        'Deep dive: Discrete signal energy',
        'The sum of squares of each discrete-sample value gives the total signal energy.',
        'Energy computation for finite-length sequences.',
        'Compare energy differences among sequences of different amplitudes.',
        'Sequence 1 2 3',
        'Energy E = 1^2 + 2^2 + 3^2 = 1 + 4 + 9 = 14; a single point 1 gives E=1.',
        'Amplitude doubled',
        'If the sequence is 2 4 6, then E = 4+16+36 = 56, four times the original 14 (amplitude-squared relation).',
        'What is the difference between discrete energy and power?',
        'Finite-length sequences yield total energy; infinite-length ones usually yield average power (energy/length).',
        'What is the unit?',
        'Depends on',
        'the dimension; if samples are voltages then their squares are in voltage-squared dimension.',
    ]))
    write('fft-resolution', build('fft-resolution', [
        'Frequency resolution (Deltaf = fs / N)',
        'Given sampling rate fs and FFT length N, output the adjacent frequency-bin spacing Deltaf and the upper analyzable frequency limit.',
        'FFT Frequency Resolution Calculator',
        '/ FFT Frequency Resolution',
        'FFT Frequency Resolution',
        'View "Frequency resolution (Deltaf = fs / N)" guide',
        'The frequency resolution of an N-point FFT is the sampling rate divided by the number of points.',
        'Sampling rate (Hz)',
        'FFT length',
        'Deltaf = fs / N; the larger N, the higher the resolution.',
        '1 kHz sampling, 1024 points -> about 0.977 Hz.',
        'Deep dive: FFT frequency resolution',
        'Sampling rate fs and length N determine the frequency resolution df = fs/N.',
        'Estimate the number of points needed to separate closely spaced frequency components.',
        'Evaluate spectral leakage and resolution before windowing.',
        'Resolution df = 1000 / 1024 ~ 0.977 Hz, i.e. the spacing between adjacent spectral lines is about 1Hz.',
        'Improve resolution',
        'If N increases to 8192, then df ~ 0.122 Hz, able to resolve closer frequencies.',
        'How to improve frequency resolution?',
        'Increase N (longer acquisition time) or lower fs, df = fs/N.',
        'Are resolution and leakage the same thing?',
        'No, resolution is the line spacing while leakage is caused by the truncation window; they must be handled separately.',
    ]))
if __name__ == '__main__':
    main()

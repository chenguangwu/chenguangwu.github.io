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
# body_s_b4.py
def main():
    write('mod-index-fm', build('mod-index-fm', [
        'FM modulation index from frequency deviation and modulation frequency',
        'FM Modulation Index Calculator',
        '/ FM Modulation Index Calculator',
        'View "FM modulation index from frequency deviation and modulation frequency" guide',
        'Enter maximum frequency deviation Delta f and modulation frequency fm to find the FM modulation index.',
        'Maximum deviation Delta f (kHz)',
        'Modulation frequency f_m (kHz)',
        'Deep dive: FM modulation index beta',
        'FM modulation index beta = maximum deviation / modulation frequency.',
        'Determine narrowband/wideband FM and the number of sidebands.',
        'Input for the Carson bandwidth formula.',
        'Modulation index beta = 75 / 15 = 5, wideband FM with many sidebands.',
        'Narrowband case',
        'If Delta f=5kHz, fm=15kHz, then beta~0.33, close to narrowband FM (beta << 1).',
        'What is the relation between beta and bandwidth?',
        'Carson bandwidth ~ 2(Delta f + fm) = 2fm(beta+1); a larger beta occupies a wider band.',
        'How are wideband and narrowband defined?',
        'Usually beta << 1 is narrowband FM and a larger beta is wideband FM; there is no absolute hard boundary.',
    ]))
    write('natural-frequency-2nd', build('natural-frequency-2nd', [
        'Natural frequency (omega_n = sqrt(k/m))',
        'For the denominator s^2+2 zeta omega_n s+omega_n^2 of a second-order system transfer function, find the natural frequency omega_n and damping ratio zeta from pole positions or coefficients.',
        'Second-Order System Natural Frequency Calculator',
        '/ Second-Order Natural Frequency',
        'Second-Order Natural Frequency',
        'View "Natural frequency (omega_n = sqrt(k/m))" guide',
        'The undamped natural angular frequency of a second-order system.',
        'At k=100, m=1, omega_n=10 rad/s, fn~1.59 Hz.',
        'Deep dive: Second-order system natural frequency',
        'From stiffness k and inertia m, find the natural angular frequency omega_n and frequency fn.',
        'Estimate mechanical/circuit resonance points.',
        'Avoid operating frequencies near resonance.',
        'Double the stiffness',
        'If k=200, then omega_n=sqrt(200)~14.14 rad/s, fn~2.25 Hz, and the resonance point moves up.',
        'How to convert between omega_n and fn?',
        'fn = omega_n/(2pi), where omega_n is angular frequency (rad/s) and fn is ordinary frequency (Hz).',
        'Does damping affect the natural frequency?',
        'With damping the actual',
        'oscillation frequency',
        'omega_d=omega_n sqrt(1-zeta^2), slightly lower than omega_n.',
    ]))
    write('nyquist-rate', build('nyquist-rate', [
        'Nyquist sampling (fs >= 2 f_max)',
        'Given the highest signal frequency f_max, find the minimum sampling rate fs >= 2 f_max required to avoid aliasing.',
        'Nyquist Sampling Rate Calculator',
        '/ Nyquist Sampling Rate',
        'Nyquist Sampling Rate',
        'View "Nyquist sampling (fs >= 2 f_max)" guide',
        'The minimum sampling rate to reconstruct a continuous signal without distortion is twice the highest signal frequency.',
        'Highest frequency (Hz)',
        'fs_min = 2 f_max (Nyquist rate).',
        '20 kHz audio requires >=40 kHz sampling (CD uses 44.1 kHz).',
        'Deep dive: Nyquist sampling rate',
        'Twice the highest frequency fmax is the minimum alias-free sampling rate.',
        'ADC selection and anti-aliasing design.',
        'Compare sampling requirements for different fmax.',
        'fmax=20000Hz (audio upper limit)',
        'Nyquist rate fs = 2 x 20000 = 40000 Hz = 40 kHz; CD samples at 44.1kHz for margin.',
        'Higher frequency',
        'If fmax=1MHz, at least 2MHz sampling is needed, otherwise high frequencies alias into low frequencies.',
        'Should the actual sampling rate be exactly 2fmax?',
        'It should be above 2fmax with an anti-aliasing filter, leaving transition-band margin to prevent aliasing.',
        'What is aliasing?',
        'When sampling is insufficient, high-frequency components fold into false low-frequency components, destroying signal fidelity.',
    ]))
    write('peak-time-2nd', build('peak-time-2nd', [
        'Second-Order System Peak Time Calculator',
        'For an underdamped second-order system (0<zeta<1) step response, the time to first reach the peak is tp = pi/(omega_n sqrt(1-zeta^2)).',
        '/ Second-Order Peak Time',
        'Second-Order Peak Time',
        'View "Second-Order System Peak Time Calculator" guide',
        'Peak time (tp = pi / (omega_n sqrt(1-zeta^2)))',
        'Natural angular frequency (rad/s)',
        'Damping ratio',
        'tp = pi/(omega_n sqrt(1-zeta^2)); overshoot = exp(-zeta pi/sqrt(1-zeta^2)).',
        'At omega_n=10, zeta=0.1, tp~0.316 s and overshoot ~73%.',
        'Deep dive: Second-order system peak time',
        'The time tp for an underdamped second-order system to first reach its peak.',
        'Response speed and damping evaluation.',
        'Compare peak times for different zeta and omega_n.',
        'Increased damping',
        'If zeta=0.5, then tp = pi/(10 x sqrt(0.75)) ~ 0.363 s, slightly later with reduced overshoot.',
        'How does peak time vary with damping?',
        'As zeta increases, the denominator sqrt(1-zeta^2) decreases and tp increases; the peak arrives later but overshoot is lower.',
        'Is peak time the same as rise time?',
        'No, peak time is when the maximum overshoot is first reached, while rise time is when the final value reaches a',
        'certain point.',
    ]))
    write('pll-lock-range', build('pll-lock-range', [
        'Lock range (Delta f = K_v V_max)',
        'The capture bandwidth and lock range of a PLL depend on the loop gain K and natural frequency omega_n design.',
        'PLL Lock Range Calculator',
        '/ PLL Lock Range',
        'PLL Lock Range',
        'View "Lock range (Delta f = K_v V_max)" guide',
        'In a PLL, the frequency pull range of the VCO is determined by its gain and the control voltage.',
        'VCO gain (Hz/V)',
        'Maximum control voltage (V)',
        'Delta f = K_v V_max; VCO gain K_v is in Hz/V.',
        'For K_v=1 MHz/V and V_max=5V the range is ±5 MHz.',
        'Deep dive: PLL lock range',
        'VCO gain Kv times maximum control voltage Vmax gives the capture/lock frequency-offset range.',
        'Estimate the frequency span a PLL can track.',
        'Compare lock capability for different Kv.',
        'Lock offset Delta f = 1e6 x 5 = 5x10^6 Hz = 5 MHz, i.e. lockable within ±5MHz of the center frequency.',
        'Limited control voltage',
        'If Vmax=2V, then Delta f=2MHz, the control range narrows and a higher Kv is needed to compensate.',
        'Is lock range the same as capture range?',
        'Usually the capture range is smaller than the lock (hold) range; initial acquisition is more demanding.',
        'Is a larger Kv always better?',
        'A larger Kv gives a wider lock range but is more susceptible to noise and drift, requiring loop filtering.',
    ]))
if __name__ == '__main__':
    main()

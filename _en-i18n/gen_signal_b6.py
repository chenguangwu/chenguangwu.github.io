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
# body_s_b6.py
def main():
    write('snr-db', build('snr-db', [
        'SNR from signal power and noise power',
        'Convert the ratio of signal power S to noise power N into decibels: SNR_dB = 10·log10(S/N), or use the voltage ratio 20·log10(V_s/V_n).',
        'Signal-to-Noise Ratio (SNR) Calculator',
        '/ Signal-to-Noise Ratio (SNR) Calculator',
        'View "SNR from signal power and noise power" guide',
        'Enter signal power Ps and noise power Pn to find the SNR (dB).',
        'Signal power Ps (W)',
        'Noise power Pn (W)',
        'Deep dive: Signal-to-noise ratio (dB)',
        'Signal power',
        'Taking 10log10 of ps and noise power pn gives the SNR.',
        'Communication quality and ADC effective-bit evaluation.',
        'Compare different noise levels.',
        'SNR = 10xlog10(10/0.1) = 10xlog10(100) = 20 dB; raising noise to 1 drops the SNR to 10dB.',
        'Speech intelligibility',
        'Generally SNR>20dB is clear, while <10dB has obvious noise and is hard to distinguish.',
        'Must the SNR unit be dB?',
        'A ratio (linear) can also be used; dB is more convenient across orders of magnitude.',
        'Is a higher SNR always better?',
        'Usually higher is clearer, but too high may mean the signal is too strong or the system dynamic range is wasted.',
    ]))
    write('steady-state-error', build('steady-state-error', [
        'Step steady-state error (e_ss = 1 / (1 + K_p))',
        'The steady-state error e_ss of a feedback control system under step/ramp/parabolic inputs, determined by system type and open-loop gain.',
        'Unity-Feedback Steady-State Error Calculator',
        '/ Steady-State Error',
        'Steady-State Error',
        'View "Step steady-state error (e_ss = 1 / (1 + K_p))" guide',
        'The steady-state error of a type-0 unity-feedback system under a unit step input.',
        'Proportional gain K_p',
        'e_ss = 1/(1+K_p) (type-0 system, unit step).',
        'At K_p=9, e_ss=0.1 (10%).',
        'Deep dive: Unity-feedback steady-state error',
        'For proportional control Kp, the unit-step steady-state error ess = 1/(1+Kp).',
        'Trade-off between system accuracy and gain.',
        'Compare the static error for different Kp.',
        'Steady-state error ess = 1/(1+9) = 0.10, i.e. a 10% final-value deviation; raising Kp to 99 gives ess~1%.',
        'Integral action removes static error',
        'Pure proportional control always has a static error; adding integral drives the step ess toward 0, but may affect stability.',
        'Why does pure proportional control have a static error?',
        'To maintain the output the controller needs a certain error to drive it; with zero error there is no drive, so a steady-state deviation remains.',
        'Does a larger Kp give a smaller static error?',
        'Yes, ess=1/(1+Kp) decreases as Kp increases, but too large a value can cause oscillation.',
    ]))
if __name__ == '__main__':
    main()

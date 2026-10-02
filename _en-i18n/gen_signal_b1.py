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
# body_s_b1.py
def main():
    write('bandwidth-q', build('bandwidth-q', [
        'Bandwidth from center frequency and Q factor',
        'From the center frequency f0 and quality factor Q, compute the -3dB bandwidth Deltaf of a bandpass filter.',
        'Resonant Bandwidth Calculator',
        '/ Resonant Bandwidth Calculator',
        'View "Bandwidth from center frequency and Q factor" guide',
        'Enter center frequency f0 and quality factor Q to find the -3dB bandwidth.',
        'Quality factor Q',
        'Deep dive: Bandwidth and quality factor (BW = f0/Q)',
        'Compute the relationship between the -3dB bandwidth of resonant circuits or filters and the center frequency and Q value.',
        'Given the center frequency and Q, find the passband width.',
        'An intuitive comparison of high-Q narrowband versus low-Q wideband.',
        'Bandwidth BW = 1000 / 10 = 100 Hz; if Q rises to 100, BW narrows to 10 Hz.',
        'Find Q from a given bandwidth',
        'If f0=1kHz requires BW=50Hz, then Q = 1000/50 = 20; a higher Q gives stronger selectivity.',
        'Is a larger Q always better?',
        'High Q gives good selectivity but a narrow passband and slow settling; trade off per application (frequency-selective vs wideband).',
        'Which bandwidth is meant?',
        'Usually the -3dB bandwidth (between half-power points), where power drops to half and amplitude drops to 1/sqrt(2).',
    ]))
    write('bit-rate-nyquist', build('bit-rate-nyquist', [
        'Maximum bit rate from bandwidth and levels',
        'Based on the Nyquist sampling theorem, given bandwidth B and modulation order M, compute the maximum bit rate free of intersymbol interference.',
        'Nyquist Maximum Bit Rate Calculator',
        '/ Nyquist Maximum Bit Rate Calculator',
        'View "Maximum bit rate from bandwidth and levels" guide',
        'Enter bandwidth B and the number of levels M per symbol to find the maximum intersymbol-interference-free bit rate.',
        'Bandwidth B (Hz)',
        'Levels M',
        'Deep dive: Nyquist interference-free rate',
        'Compute the maximum symbol/bit rate of an ideal low-pass channel free of intersymbol interference.',
        'How bandwidth B and levels M per symbol affect capacity.',
        'Compare bit rates under different modulation orders.',
        'R = 2 x 3000 x log2(4) = 6000 x 2 = 12000 bps = 12 kbps; raising M to 16 doubles R to 24 kbps.',
        'Binary case',
        'If M=2, then R = 2B x 1 = 6000 bps; doubling the number of levels doubles the rate (within the Nyquist limit).',
        'Is this Shannon capacity?',
        'No, this is the Nyquist interference-free rate limit (ideal channel), ignoring SNR; Shannon capacity additionally includes the SNR term.',
        'Why 2B?',
        'An ideal low-pass channel carries at most 2B independent symbols per second; multiplying by log2(M) bits per symbol yields the bit rate.',
    ]))
    write('carrier-freq', build('carrier-freq', [
        'Carrier frequency from upper and lower sidebands',
        'From the upper and lower sideband frequencies of a double-sideband signal, compute the carrier center frequency fc and bandwidth.',
        'Carrier Frequency Calculator',
        '/ Carrier Frequency Calculator',
        'View "Carrier frequency from upper and lower sidebands" guide',
        'Enter the upper and lower sideband frequencies to find the carrier frequency.',
        'Upper sideband f_upper (kHz)',
        'Lower sideband f_lower (kHz)',
        'Deep dive: Carrier frequency (midpoint of sidebands)',
        'Given upper sideband fu and lower sideband fl, find the carrier fc.',
        'Compute spectrum parameters of an AM modulated wave.',
        'Verify whether the modulated sidebands are symmetric.',
        'Carrier fc = (1010 + 990) / 2 = 1000 Hz; frequency offset = 1010 - 1000 = 10 Hz.',
        'Wide frequency-offset case',
        'If fu=1200 and fl=800, then fc=1000 and offset 200Hz; deeper modulation yields wider sidebands.',
        'Is carrier frequency the same as center frequency?',
        'For symmetric modulation they coincide, fc = (fu+fl)/2; for asymmetric modulation it follows the given definition.',
        'What does the sideband difference reflect?',
        'Half the difference between the upper and lower sidebands is the highest modulation frequency or the maximum frequency deviation.',
    ]))
    write('cascade-gain-db', build('cascade-gain-db', [
        'Total gain from per-stage gains (dB)',
        'When multiple amplifier stages are cascaded, summing each stage gain (dB) gives the total cascade gain.',
        'Cascade Gain Calculator',
        '/ Cascade Gain Calculator',
        'View "Total gain from per-stage gains (dB)" guide',
        '20 = 27 dB -> linear ~ 501.',
        'Enter three stage gains (dB) to find the total gain and the linear total gain.',
        'Stage 1 gain G1 (dB)',
        'Stage 2 gain G2 (dB)',
        'Stage 3 gain G3 (dB)',
        'The cascade total gain is the sum of the dB values.',
        '10 - 3 + 20 = 27 dB -> linear ~ 501.',
        'Deep dive: Cascade gain (adding dB)',
        'Total gain of multi-stage amplifiers/attenuators is simply the sum of the dB values.',
        'Given each stage g1/g2/g3, find the total dB and the linear multiplier.',
        'Compute links that include negative gain (attenuation).',
        'Total gain = 10 - 3 + 20 = 27 dB; linear multiplier = 10^(27/10) ~ 10^2.7 ~ 501x.',
        'Net attenuation',
        'If all three stages are -3dB, the total is -9dB, linear ~ 0.126x (about attenuated to 1/8).',
        'Why add dB directly?',
        'dB is a logarithmic unit; cascaded multiplication maps to logarithmic addition, so total gain is the sum of the stage dB values.',
        'What does negative dB mean?',
        'Negative dB indicates attenuation; for example -3dB attenuates to about 0.707x (half power).',
    ]))
    write('damping-ratio', build('damping-ratio', [
        'Damping ratio (zeta = c / (2sqrt(k m)))',
        'In the step response of a second-order system, find the damping ratio zeta from overshoot Mp, or conversely compute overshoot and settling time from zeta.',
        'Second-Order System Damping Ratio Calculator',
        '/ Damping ratio calculation',
        'Damping ratio calculation',
        'View "Damping ratio (zeta = c / (2sqrt(k m)))" guide',
        'zeta = c/(2sqrt(km)); zeta>1 overdamped. Example zeta=0.1 (underdamped oscillation).',
        'Damping ratio describes how fast a second-order system oscillation decays.',
        'Damping coefficient (N s/m)',
        'zeta = c/(2sqrt(km)); zeta<1 oscillatory, zeta=1 critical, zeta>1 overdamped.',
        'Example zeta=0.1 (underdamped oscillation).',
        'Deep dive: Damping ratio zeta',
        'From c, k, m of a second-order system, find the damping ratio and classify under/critical/overdamped.',
        'Control-system stability and overshoot evaluation.',
        'Compare response shapes under different damping.',
        'zeta = 2 / (2 x sqrt(100 x 1)) = 2/20 = 0.10, underdamped, will oscillate with overshoot.',
        'Critical damping',
        'If c=20 (others unchanged), then zeta=20/20=1.0, exactly critical damping, fastest with no oscillation and no overshoot.',
        'What does the size of zeta mean?',
        'zeta<1 underdamped (oscillatory), zeta=1 critical, zeta>1 overdamped (slow, no overshoot).',
        'How large is the underdamped overshoot?',
        'Maximum overshoot ~ exp(-pi zeta/sqrt(1-zeta^2)), about 73% at zeta=0.1.',
    ]))
if __name__ == '__main__':
    main()

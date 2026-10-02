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
# body_s_b3.py
def main():
    write('first-order-rise', build('first-order-rise', [
        'Rise time (tr ~ 2.2 tau)',
        'For the step response of a first-order low-pass filter, find the time constant tau and the rise time for the output to go from 10% to 90%.',
        'First-Order System Rise Time Calculator',
        '/ First-Order Rise Time',
        'First-Order Rise Time',
        'View "Rise time (tr ~ 2.2 tau)" guide',
        'A first-order system takes about 2.2 time constants to rise from 10% to 90%.',
        'At tau=1 ms the rise is about 2.2 ms.',
        'Deep dive: First-order system rise time',
        'For an RC or similar first-order system, the 10% to 90% rise time tr ~ 2.2 tau.',
        'Evaluate the trade-off between bandwidth and rise time.',
        'Estimate the response speed of oscilloscopes/probes.',
        'Rise time tr = 2.2 x 0.001 = 0.0022 s = 2.2 ms; halving tau gives tr=1.1ms.',
        'Bandwidth conversion',
        'First-order -3dB bandwidth fc~1/(2pi tau)~159Hz, corresponding to the rise time of 2.2 tau.',
        'What does the 10%~90% in tr=2.2 tau mean?',
        'It is the time for the output to rise from 10% to 90% of its final value, about 2.2 time constants for a first-order step response.',
        'What is the relation with bandwidth?',
        'Approximately tr x BW ~ 0.35, useful for estimating system speed.',
        'How to use rise time (tr ~ 2.2 tau)',
        'What does rise time (tr ~ 2.2 tau) do?',
        'Enter the first-order system time constant tau and estimate the 10% to 90% rise time as tr ~ 2.2 tau; used for speed evaluation of RC circuits and control-system step responses.',
        'How to use rise time (tr ~ 2.2 tau)?',
        'Which scenarios suit rise time (tr ~ 2.2 tau)?',
        'First-order step response V(t)=V_final·(1-e^(-t/tau)): the output approaches the final value V_final exponentially with time constant tau.',
        'At t=tau it reaches 63.2%, at t=2 tau 86.5%, at t=5 tau 99.3%. tau=R·C (RC circuit) or L/R (RL circuit).',
    ]))
    write('fourier-base', build('fourier-base', [
        'Fundamental frequency (f0 = 1 / T)',
        'For a periodic signal f(t), compute Fourier coefficients an/bn, DC component a0, and the trigonometric/exponential Fourier series expansion.',
        'Fourier Series Fundamental Frequency Calculator',
        '/ Fourier Fundamental Frequency',
        'Fourier Fundamental Frequency',
        'View "Fundamental frequency (f0 = 1 / T)" guide',
        'The fundamental frequency of a periodic signal is the reciprocal of its period.',
        'A period of 20 ms corresponds to a 50 Hz fundamental.',
        'Deep dive: Fundamental frequency (f0 = 1/T)',
        'Find the fundamental f0 from period T of a periodic signal.',
        'The frequency reference for Fourier series expansion.',
        'Harmonic frequencies are integer multiples of the fundamental.',
        'T=0.02s (50Hz period)',
        'Fundamental f0 = 1 / 0.02 = 50 Hz; second harmonic 100Hz, third 150Hz.',
        'Longer period',
        'If T=0.04s, then f0=25Hz, the fundamental drops by half and the harmonics shift down accordingly.',
        'What is the relation between fundamental and angular frequency?',
        'Angular frequency omega0 = 2pi f0 = 2pi/T.',
        'Does a non-periodic signal have a fundamental?',
        'A strictly non-periodic (single segment) signal uses the Fourier transform to get a continuous spectrum, with no discrete fundamental.',
    ]))
    write('gain-db', build('gain-db', [
        'Gain (G = 20·log10(Vout / Vin))',
        'Bidirectional conversion between linear amplification factor and decibel scale: dB = 20·log10(A) for voltage or 10·log10(A) for power.',
        'Voltage Gain Decibel Calculator',
        '/ Gain in Decibels',
        'Gain in Decibels',
        'View "Gain (G = 20·log10(Vout / Vin))" guide',
        'Express the voltage gain of an amplifier or network in decibels.',
        'Output amplitude (V)',
        'Input amplitude (V)',
        'A 10x voltage gain = 20 dB.',
        'Deep dive: Voltage gain dB',
        'Taking 20log10 of the output/input voltage ratio gives the gain.',
        'Amplifier gain expression and cascading.',
        'Compare positive and negative gain (amplification/attenuation).',
        'Gain G = 20xlog10(10/1) = 20 dB, i.e. a 10x voltage amplification.',
        'Attenuation',
        'If vout=0.5, vin=1, then G = 20xlog10(0.5) ~ -6.02 dB (about half voltage).',
        'Does gain dB agree with power dB?',
        'They agree under equal impedance (voltage squared = power); otherwise use 20log and 10log separately.',
        'What does 0dB represent?',
        '0dB means vout=vin, i.e. unity gain, no amplification and no attenuation.',
    ]))
    write('group-delay', build('group-delay', [
        'Group delay from phase difference and angular frequency difference',
        'From the derivative of the phase response phi(omega), compute the delay time tau_g = -dphi/domega for a narrowband signal envelope passing through the system.',
        'Group Delay Calculator',
        '/ Group Delay Calculator',
        'View "Group delay from phase difference and angular frequency difference" guide',
        'Enter phase difference Delta phi (degrees) and angular frequency difference Delta omega (rad/s) to find the group delay.',
        'Phase difference Delta phi (deg)',
        'Angular frequency difference Delta omega (rad/s)',
        'tau_g = -dphi/domega, with phase in radians.',
        'Deep dive: Group delay',
        'The phase-frequency slope -dphi/domega gives the group delay, measuring delay consistency across frequency components.',
        'Evaluate filter linear phase.',
        'Estimate wideband signal distortion (waveform broadening).',
        'Group delay tg = -(90xpi/180) / 1000 = -(pi/2)/1000 ~ -1.571x10^-3 s ~ -1.57 ms.',
        'Constant delay',
        'If phase varies linearly with frequency (constant slope), the group delay is constant and the signal is undistorted.',
        'Is a negative group delay a problem?',
        'A physically realizable system has non-negative group delay; the sign in the example depends on the phase definition direction, so the absolute value is what matters.',
        'What is the difference between group delay and phase delay?',
        'Phase delay is the single-frequency phase shift divided by frequency; group delay is the phase-frequency slope and determines the envelope delay.',
    ]))
    write('mod-index-am', build('mod-index-am', [
        'AM modulation index from modulating and carrier amplitudes',
        'AM Modulation Index Calculator',
        '/ AM Modulation Index Calculator',
        'View "AM modulation index from modulating and carrier amplitudes" guide',
        'Enter modulating-wave amplitude Am and carrier amplitude Ac to find the AM modulation index.',
        'Modulating amplitude A_m (V)',
        'Carrier amplitude A_c (V)',
        'm = A_m/A_c, m<=1 means no overmodulation.',
        'Deep dive: AM modulation index',
        'For an AM wave, modulation index m = modulating component / carrier amplitude.',
        'Determine whether overmodulation occurs (m>1 causes distortion).',
        'Compare different modulation depths.',
        'Modulating 2, carrier 5',
        'Modulation index m = 2 / 5 = 0.40, normal AM (m<1, no distortion).',
        'Overmodulation',
        'If m=1.2 (>1), the envelope crosses zero and reverses, causing severe distortion; it should be avoided.',
        'What happens if m exceeds 1?',
        'Overmodulation makes the envelope no longer proportional to the modulating signal, producing clipping distortion after demodulation.',
        'Modulation index and power efficiency?',
        'The sideband power ratio grows with m^2; a larger m raises the information-power share but also the risk of overmodulation.',
    ]))
if __name__ == '__main__':
    main()

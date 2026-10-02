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
# body_s_b5.py
def main():
    write('pwm-average', build('pwm-average', [
        'Average voltage (V_avg = D V_cc)',
        'Within one period of a PWM signal, the high-level duty cycle D determines the output average voltage V_avg = D V_high.',
        'PWM Average Voltage Calculator',
        '/ PWM Average Voltage',
        'PWM Average Voltage',
        'View "Average voltage (V_avg = D V_cc)" guide',
        'The average voltage of a PWM output after low-pass filtering equals the duty cycle times the supply voltage.',
        'Duty cycle (%)',
        'V_avg = D V_cc, where D is the 0-100% duty cycle.',
        '50% duty cycle, 5 V supply -> 2.5 V.',
        'Deep dive: PWM average voltage',
        'Duty cycle',
        'D and supply Vcc give the ideal average voltage.',
        'Estimate average drive for motors/LEDs.',
        'Compare average effects of different duty cycles.',
        'Average voltage Vavg = (50/100) x 5 = 2.5 V; raising D to 80% gives 4.0V.',
        'Full duty cycle',
        'At D=100% Vavg=5V equals the DC supply, and at D=0% it is 0V.',
        'Does the actual average voltage equal the theory?',
        'The ideal switch holds; in practice switching loss, filtering and load cause ripple and deviation.',
        'Is duty cycle linear with brightness/speed?',
        'The average is linear, but perceived brightness and motor speed are also affected by nonlinearity and inertia.',
        'How to use average voltage (V_avg = D V_cc)',
        'What does average voltage (V_avg = D V_cc) do?',
        'Enter duty cycle D and supply voltage V_cc, then compute the average output voltage of a PWM after low-pass filtering as V_avg = D V_cc; used for DAC, dimming and motor-drive equivalent voltage.',
        'How to use average voltage (V_avg = D V_cc)?',
        'Which scenarios suit average voltage (V_avg = D V_cc)?',
        'PWM average voltage V_avg=D V_sup: the product of duty cycle D (0-1) and supply voltage, i.e. the time average of the output voltage over one period.',
        'D = high-level time / period. Used for LED dimming and motor speed control: the average voltage determines brightness/speed. After low-pass filtering an approximate DC V_avg is obtained.',
    ]))
    write('q-factor', build('q-factor', [
        'Quality factor from center frequency and bandwidth',
        'Quality factor of a resonant circuit: series Q = omega0 L/R = 1/(omega0 C R), parallel Q = R/(omega0 L) = omega0 C R; also equals f0/Delta f_3dB.',
        'Quality Factor Q Calculator',
        '/ Quality Factor Q Calculator',
        'View "Quality factor from center frequency and bandwidth" guide',
        'Enter center frequency f0 and -3dB bandwidth Delta f to find the quality factor Q.',
        'Bandwidth Delta f (Hz)',
        'Q = f0/Delta f, the larger the better the selectivity.',
        'Deep dive: Quality factor Q',
        'Resonator Q = f0 / bandwidth, measuring the ratio of stored energy to loss.',
        'Evaluate filter selectivity and cavity Q.',
        'Compare narrowband high-Q with wideband low-Q.',
        'Q = 1000 / 100 = 10; if BW narrows to 10Hz, then Q=100 (better selectivity).',
        'Low Q',
        'If BW=500Hz, then Q=2, wideband with low selectivity and relatively large loss.',
        'What does a higher Q mean?',
        'A high Q means low loss, sharp resonance and strong frequency selectivity, but a narrow bandwidth.',
        'What is the relation between Q and bandwidth?',
        'Q = f0/BW, inversely proportional; a high Q necessarily means a narrow band.',
    ]))
    write('rc-cutoff', build('rc-cutoff', [
        '-3dB cutoff (fc = 1 / (2pi R C))',
        'The -3dB cutoff frequency fc = 1/(2pi R C) and time constant tau = R C of a first-order RC low-pass/high-pass filter.',
        'RC Cutoff Frequency Calculator',
        '/ RC Cutoff Frequency',
        'RC Cutoff Frequency',
        'View "Cutoff (fc = 1 / (2pi R C))" guide',
        'The -3dB corner frequency of a first-order RC low-pass/high-pass filter.',
        '1 kOhm and 1 uF correspond to about 159 Hz.',
        'Deep dive: RC cutoff frequency',
        'From resistor R and capacitor C, find the -3dB cutoff fc = 1/(2pi R C).',
        'Corner-frequency design for low-pass/high-pass filters.',
        'Compare corner frequencies for different R and C.',
        'Reduce the capacitance',
        'If C=0.1uF, then fc~1591.5Hz; a smaller capacitor shifts the cutoff up by ten times.',
        'Is the cutoff frequency where gain is zero?',
        'No, it is the -3dB point (amplitude drops to 1/sqrt(2), power drops by half), i.e. the half-power point.',
        'Which affects fc more, R or C?',
        'fc is inversely proportional to both R and C; halving either doubles fc.',
    ]))
    write('signal-power', build('signal-power', [
        'Power from RMS value and load',
        'Average power of a periodic signal P = (1/T) integral |x(t)|^2 dt, or discrete P = (1/N) Sum |x[n]|^2.',
        'Signal Power Calculator',
        '/ Signal Power Calculator',
        'View "Power from RMS value and load" guide',
        'Enter RMS voltage V and resistance R to find the signal power.',
        'RMS voltage V (V)',
        'Deep dive: Signal power (P = V^2/R)',
        'Given voltage v and load R, find the power.',
        'Power estimation for 50Ohm systems and matched loads.',
        'Compare power for different voltages/impedances.',
        'Power P = 5^2 / 50 = 25 / 50 = 0.5 W; if R=75Ohm then P~0.333W.',
        'Voltage doubled',
        'If v=10V, R=50Ohm, then P=100/50=2W, and power rises fourfold with the square of voltage.',
        'When does the formula apply?',
        'It applies when the RMS voltage and a purely resistive load are known; AC uses RMS, instantaneous values use instantaneous power.',
        'What is the relation with dBm?',
        'P=0.5W=500mW, relative to 1mW this is 10log10(500)~27dBm.',
    ]))
    write('sine-rms', build('sine-rms', [
        'RMS value (V_rms = V_pk / sqrt(2))',
        'For a sine wave of amplitude A, RMS = A/sqrt(2), average power = A^2/2.',
        'Sine Wave RMS Calculator',
        '/ Sine RMS Value',
        'Sine RMS Value',
        'View "RMS value (V_rms = V_pk / sqrt(2))" guide',
        'The RMS (effective) value of a sine wave is 1/sqrt(2) of its peak.',
        'Peak voltage (V)',
        'V_rms = V_pk / sqrt(2); mains 220 V is the RMS value, with peak about 311 V.',
        'Deep dive: Sine RMS value (RMS)',
        'Convert sine peak Vpk to RMS Vrms = Vpk/sqrt(2).',
        'AC voltage/current measurement conversion.',
        'Power calculation',
        'Must use the RMS value.',
        'RMS Vrms = 10 / sqrt(2) ~ 7.071 V; applied to a 50Ohm load, power = 7.071^2/50 ~ 1.0 W.',
        'Mains peak value',
        'If the RMS value is 220V, then peak ~ 220 x sqrt(2) ~ 311V.',
        'Why use RMS to compute power?',
        'The RMS value makes AC and DC produce the same power in a resistor; it is the DC equivalent of power.',
        'Do non-sinusoidal waves also divide by sqrt(2)?',
        'No, sqrt(2) applies only to sinusoids; other waveforms have their own form factors.',
    ]))
if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'telecom')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'telecom')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
DISCL = "Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected."
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
    out = {'slug': slug, 'industry': 'telecom', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
# -*- coding: utf-8 -*-
def main():
    write('convert-24', build('convert-24', [
        '🔄 BER and SNR Conversion',
        '📖 Read the "BER and SNR Conversion User Guide"',
        'Bit error rate',
        'Milli bit error rate',
        'Kilo bit error rate',
        'SNR conversion',
        'Milli SNR conversion',
        'Kilo SNR conversion',
        '📚 Deep dive: proportional conversion between BER and SNR',
        'Given a value in one unit, convert it to another with a fixed coefficient for quick reconciliation.',
        'Align units in verbal communication or reports (for example, expressing a decimal defect rate as',
        'For precise physical-layer BER↔SNR conversion, use this tool for a magnitude estimate first, then verify with a professional tool.',
        'How to use the conversion',
        'After you enter a value, a conversion coefficient and the from/to units, the tool converts directly with result = value × coefficient. For example value 0.0015, coefficient 10⁶, from "decimal defect rate" to "',
        '" → 1 500 PPM. Note: this is only proportional conversion and does not derive BER↔SNR under a channel model; to derive by modulation scheme use the "',
        '" tool instead.',
        'How is this tool different from the "BER to SNR Conversion" tool?',
        'This tool only applies the fixed coefficient you enter and does not distinguish modulation scheme or channel model; the latter derives between BER and Eb/N0 using the theoretical formulas for BPSK/QPSK/16-QAM/64-QAM.',
        'What conversion coefficient should I fill in?',
        'The factor between the two units. For example decimal→percentage is 100, decimal→PPM is 1,000,000, and dB→linear must be converted by 10^(dB/10) first.',
        'About "BER and SNR Conversion"',
        'BER and SNR Conversion. A free online tool processed entirely in the browser, no data uploaded, your privacy and security protected.',
    ]))

    write('estimate-9', build('estimate-9', [
        '🔮 Free Space Path Loss Estimator',
        'Compute free space path loss (FSPL) from the Friis transmission equation and estimate the received signal strength',
        'Core formula (from input variables): 20×Math.log10(dKM) + 20×Math.log10(fMHz) + 32.44; 20×Math.log10(d) + 20×Math.log10(fMHz) + 32.44; fMHz×1e6',
        '📖 Read the "Free Space Path Loss Estimator User Guide"',
        '📡 Optional: link budget (received signal strength)',
        'Transmit power Pt (dBm, optional)',
        'Transmit antenna gain Gt (dBi, optional)',
        'Receive antenna gain Gr (dBi, optional)',
        '💡 Formula: FSPL(dB) = 20·log10(d[km]) + 20·log10(f[MHz]) + 32.44; received power Pr = Pt + Gt + Gr − FSPL',
        'FSPL only applies to ideal free-space (line of sight, unobstructed) scenarios; real losses are larger',
        'MHz and km is the standard unit pairing; if you use GHz or m the tool converts automatically',
        '📚 Deep dive: free space path loss FSPL',
        'In the first pass for a microwave or satellite link, compute free space loss from frequency and distance as the first term of the link budget.',
        'Entering transmit power and antenna gain gives the received power directly, so you can check whether receiver sensitivity is met.',
        'Observe the effect of doubling frequency (loss +6 dB) or doubling distance (loss +6 dB) to understand the coverage versus band trade-off.',
        'Free space loss at 2.4 GHz over 1 km',
        'FSPL = 20log10(d[km]) + 20log10(f[MHz]) + 32.44 = 20log10(1) + 20log10(2400) + 32.44 = 0 + 67.60 + 32.44 = 100.04 dB; wavelength λ = 2.998×10⁸ ÷ 2.4×10⁹ ≈ 12.49 cm. With Pt = 20 dBm, Gt = 3 dBi, Gr = 2 dBi → Pr = 20 + 3 + 2 − 100.04 = −75.04 dBm. Shortening distance to 100 m drops FSPL to 80.04 dB (20 dB less), raising Pr to −55.04 dBm.',
        'Why does doubling distance only add 6 dB of loss?',
        'In free space power falls off with the square of distance, and 20log10(2) ≈ 6.02 dB. Frequency behaves the same way: 20log10(2) ≈ 6.02 dB, so doubling frequency also adds about 6 dB of loss.',
        'Why is a real link worse than this value?',
        'FSPL only considers free-space spreading and excludes atmospheric absorption, rain fade, multipath fading, obstruction blockage and antenna mismatch. Real design must stack these margins on top.',
        'About "Free Space Path Loss Estimator"',
        'Enter frequency and distance to estimate free space path loss with the standard FSPL formula, optionally fill in transmit power and antenna gain to get the received signal strength, and compare losses across distances.',
        'Supports automatic conversion between MHz/GHz and km/m',
        'Link budget and received signal strength grading',
        'Loss comparison table at different distances',
        'Wireless link budget and coverage planning',
        'Wi-Fi / walkie-talkie / microwave communication estimation',
        'IoT device transmission range assessment',
        'RF engineering teaching and lab work',
    ]))


if __name__ == '__main__':
    main()

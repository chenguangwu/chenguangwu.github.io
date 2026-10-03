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
    write('ap-coverage', build('ap-coverage', [
        '📏 AP Coverage Radius',
        'Estimate wireless AP coverage radius from link budget and free-space path loss.',
        '📖 Read the "AP Coverage Radius User Guide"',
        'MAPL = Pt + Gt + Gr − Pr_min − fade margin − additional losses',
        'Receiver sensitivity Pr_min (dBm)',
        'Environmental additional loss (dB)',
        'Fade margin (dB)',
        'Environment type',
        'Free space (outdoor line of sight)',
        'Indoor office (many walls)',
        'Indoor dense (many partitions)',
        'Compute coverage radius',
        '📋 Computation principle',
        'Link budget:',
        'Maximum allowable path loss MAPL = Pt + Gt + Gr − Pr_min − fade margin − additional losses',
        'Back out distance from FSPL:',
        'Set FSPL = MAPL and solve inversely: d = 10^((MAPL − 20·log10(f) − 32.44)/20) (km)',
        'Environment adjustment:',
        'For indoor scenarios, wall penetration loss is stacked on top of the additional loss (office about +8dB, dense about +15dB, already folded into the options as reference).',
        '📚 Deep dive: wireless AP coverage radius estimation',
        'Before deploying office or factory Wi-Fi, estimate a single AP coverage radius from AP transmit power, antenna gain and terminal receiver sensitivity.',
        'Compare coverage between indoor office and dense partition environments to decide AP deployment density.',
        'Back out usable coverage diameter after allowing for the fade margin, avoiding weak signal at the edges from planning on ideal values.',
        'Coverage radius for 2.4 GHz indoor office',
        'Pt = 20 dBm, Gt = 3 dBi, Gr = 2 dBi, receiver sensitivity −75 dBm, frequency 2400 MHz, additional loss 0 dB, fade margin 10 dB, environment "indoor office (many walls)" extra 8 dB → total loss 18 dB. MAPL = 20 + 3 + 2 − (−75) − 18 = 82.00 dB; d = 10^((82.00 − 20log10(2400) − 32.44) ÷ 20) = 10^((82.00 − 67.60 − 32.44) ÷ 20) ≈ 0.1252 km ≈ 125 m. Coverage diameter about 250 m, graded "good coverage"; if the environment changes to "indoor dense (many partitions)" (+15 dB), the radius drops to about 76 m.',
        'What is the environmental additional loss?',
        'Free space (outdoor line of sight) 0 dB, indoor office (many walls) 8 dB, indoor dense (many partitions) 15 dB, on top of the base additional loss and fade margin you enter (usually 8-12 dB).',
        'Why is the computed radius larger than measured?',
        'The model assumes free-space propagation plus fixed environment corrections and excludes metal reflections, furniture blockage, co-channel interference and terminal variation. For real deployment, keep 30% headroom on top of this and do a site survey.',
        'About "AP Coverage Radius"',
        'AP Coverage Radius is an online tool in the IT development domain. It is an online tool built for developers, runs purely in the browser, and no code leaves your browser.',
    ]))

    write('ber-snr', build('ber-snr', [
        '🔄 Bit Error Rate to SNR Conversion',
        'Theoretical conversion between bit error rate (BER) and energy per bit to noise density ratio (Eb/N0) for digital modulation, supporting BPSK/QPSK/16QAM/64QAM.',
        '📖 Read the "BER to SNR Conversion User Guide"',
        'Modulation scheme',
        'Eb/N0 from BER',
        'BER from Eb/N0',
        'Bit error rate BER',
        'Channel',
        'AWGN additive Gaussian white noise',
        '📋 Theory formulas and references',
        'M-QAM rectangular (k=log2M bits/symbol)',
        '16-QAM: BER ≈ (3/4)·Q(√(4/5·γb)), γb = Eb/N0 (linear)',
        'Q(x) = 0.5·erfc(x/√2), γb converted from dB to linear: γb = 10^(Eb/N0_dB/10)',
        'Eb/N0 typically required at BER=1e-5',
        'Note: this tool gives theoretical values for an AWGN channel and does not include coding gain or implementation losses.',
        '📚 Deep dive: BER and Eb/N0 conversion',
        'During link budgeting, back out the required Eb/N0 from a target bit error rate, then convert it into transmit power or antenna gain requirements.',
        'Given a received Eb/N0, estimate the BER to decide whether forward error correction or a lower-order modulation is needed.',
        'Compare the BER of BPSK, 16-QAM and 64-QAM at the same Eb/N0 to understand the cost of higher-order modulation.',
        'BER of BPSK at 10 dB',
        'Eb/N0 = 10 dB → γb = 10^(10/10) = 10. The BER of BPSK/QPSK = Q(√(2γb)) = Q(√20) = Q(4.472) ≈ 3.87×10⁻⁶. In reverse: to reach a target BER = 1×10⁻⁶ you need Q(x) = 10⁻⁶ → x ≈ 4.753 → γb = x²÷2 ≈ 11.3 → Eb/N0 ≈ 10.5 dB, meaning about 0.5 dB more link headroom for the same modulation.',
        'Why do 16-QAM / 64-QAM results differ so much?',
        'Higher-order modulation packs more bits per symbol, so constellation points are closer together and the BER degrades markedly at the same Eb/N0. That is why higher-order modulation is only used when channel conditions are good (Eb/N0 high).',
        'Is the computed BER the theoretical value without error correction?',
        'Yes. This is the theoretical bit error rate at the modem output and excludes forward error correction (FEC), interleaving and retransmission. The final frame error rate of a real system will be far lower than this BER thanks to error correction.',
        'About "BER to SNR Conversion"',
        'BER to SNR Conversion is an online tool in the IT development domain. It is an online tool built for developers, runs purely in the browser, and no code leaves your browser.',
    ]))

    write('bandwidth-calculator', build('bandwidth-calculator', [
        '🌐 Bandwidth and Download Time Calculator',
        'Convert between Mbps and download time to compute how long a file takes at a given bandwidth and the resulting actual download speed.',
        '📖 Read the "Bandwidth and Download Time Calculator User Guide"',
        'Download time = file size × 8 ÷ (bandwidth × effective utilization); 1 Byte = 8 bit, so Mbps and MB/s differ by a factor of 8; at 100 Mbps a 1 GB file takes theoretically about 82 seconds, or about 102 seconds at 80% effective bandwidth; used for network transfer and experience evaluation.',
        'Bandwidth rate',
        'Bandwidth unit',
        'Mbps (megabit/second)',
        'Gbps (gigabit/second)',
        'MB/s (megabyte/second)',
        'File unit',
        'Line efficiency/utilization (%)',
        'Common bandwidth quick pick',
        'Mbps 100 M broadband',
        'Mbps gigabit (300M)',
        'Mbps gigabit broadband',
        'Gbps 10 G (1G)',
        '📋 Conversion notes',
        'Core conversion:',
        '1 Byte = 8 bit, so 1 MB/s = 8 Mbps',
        'Actual download speed (MB/s) = bandwidth(Mbps) × efficiency / 8',
        'Bandwidth unit is bps (bit/second) while download speed is often expressed as B/s (byte/second).',
        'Line efficiency is affected by protocol overhead, packet loss and server throttling, typically 80%-95%.',
        '📚 Deep dive: bandwidth and download time conversion',
        'Given bandwidth and',
        'download duration, decide whether to upgrade the plan or switch to offline distribution.',
        'Compute the actual speed after accounting for line efficiency (protocol overhead, concurrent occupancy) to avoid promising delivery times based on theoretical values.',
        'Convert between Mbps / MB·s⁻¹ and KB / MB / GB / TB so the whole team shares one unit convention.',
        'Downloading a 2 GB file at 100 Mbps',
        'Bandwidth 100 Mbps, file 2 GB = 2,048 MB, line efficiency 90%: actual download speed = 100 × 0.90 ÷ 8 = 11.25 MB/s; time = 2,048 ÷ 11.25 ≈ 182 seconds, about 3 min 2 sec. Estimating at the theoretical value (100% efficiency) gives 164 seconds, underestimating by about 18 seconds - use real efficiency for cross-city sync or bulk distribution.',
        'Why divide by 8?',
        'Bandwidth unit Mbps is megabit per second, while file size is usually given in bytes (MB). 1 byte = 8 bits, so byte speed = bit bandwidth ÷ 8.',
        'What line efficiency should I fill in?',
        'Ethernet and TCP overhead typically takes 5-10%, and concurrent occupancy adds more, so real efficiency is often 80-95%. Use a lower value for shared bandwidth or evening peaks, and a higher value for dedicated lines.',
        'About "Bandwidth and Download Time Calculator"',
        'Bandwidth and Download Time Calculator is an online tool in the IT development domain. It is an online tool built for developers, runs purely in the browser, and no code leaves your browser.',
    ]))


if __name__ == '__main__':
    main()

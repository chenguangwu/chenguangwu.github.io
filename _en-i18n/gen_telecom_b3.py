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
    write('path-loss', build('path-loss', [
        '🔮 Path Loss Estimator',
        'd and f are taken in km and MHz; FSPL is the free space path loss and Pr is the received power.',
        '📖 Read the "Path Loss Estimator User Guide"',
        'Compute free space path loss (FSPL) to estimate wireless transmission loss and received power.',
        '📋 Formulas and notes',
        'Free space path loss (FSPL):',
        '(d in km, f in MHz)',
        'Received power:',
        'Typical scenarios:',
        '2.4GHz WiFi, 5GHz WiFi, 4G/5G mobile communications, satellite links, etc.',
        'Note: free space is an ideal model; real deployments must also account for atmospheric absorption, obstructions, multipath and other additional losses.',
        '📚 Deep dive: path loss and received power estimation',
        'In the initial design of a base station or in-building system, estimate loss and received power from frequency, distance and antenna parameters.',
        'Compare the coverage capability of different bands such as 700 MHz / 2.6 GHz / 3.5 GHz to inform band selection.',
        'Compare the estimate against receiver sensitivity to decide whether a repeater or higher antenna gain is needed.',
        'Coverage comparison of 700 MHz and 3.5 GHz',
        'Both at 2 km: 700 MHz → FSPL = 20log10(2) + 20log10(700) + 32.44 = 6.02 + 56.90 + 32.44 = 95.36 dB; 3.5 GHz (3500 MHz) → 6.02 + 70.88 + 32.44 = 109.34 dB, about 14 dB apart. With Pt = 40 dBm, Gt = 15 dBi, Gr = 3 dBi, received power at 700 MHz = 58 − 95.36 = −37.36 dBm and at 3.5 GHz = 58 − 109.34 = −51.36 dBm - 5 times the frequency gives 14 dB less received power, which is exactly why low bands cover better.',
        'Is a low band always better?',
        'Low bands lose less and diffract strongly, but offer narrow bandwidth and low capacity. 5G typically uses 3.5 GHz as the capacity layer and 700 MHz as the coverage layer; the two complement rather than replace each other.',
        'Can this model be used indoors?',
        'The free space model severely underestimates loss indoors. Stack wall penetration loss indoors (',
        'walls commonly 10-20 dB), or use a dedicated indoor propagation model.',
        'About "Path Loss Estimator"',
        'Path Loss Estimator is an online tool in the IT development domain. It is an online tool built for developers, runs purely in the browser, and no code leaves your browser.',
    ]))

    write('quick-calc-time-bandwidth', build('quick-calc-time-bandwidth', [
        '📡 Bandwidth (Mbps) and Download Time Quick Lookup',
        '📖 Read the "Bandwidth (Mbps) and Download Time Quick Lookup User Guide"',
        'Bandwidth and time conversion: time = (file size × 8) ÷ bandwidth; bandwidth = (file size × 8) ÷ time; 1 MB = 8 Mbit, so at 100 Mbps a 1 GB file takes about 80 seconds; common files (photo about 5 MB, song about 10 MB, movie about 4 GB) can be checked against the table for a quick estimate.',
        '📚 Deep dive: quick reference for bandwidth and download time',
        'Quickly look up "how long does a common file take on a given bandwidth" during live discussions, with no on-the-spot math.',
        'Explain to non-technical colleagues why 100 Mbps and 1000 Mbps feel so different in practice.',
        'Estimate the transfer window for backups, mirrors or video assets and schedule them in off-peak hours.',
        'How to use this quick table',
        'Type a keyword such as "100M", "1GB" or "4K" to filter the matching bandwidth and time entries. For example a 100 Mbps line at 90% efficiency gives an actual speed of about 11.25 MB/s, so 1 GB takes about 91 seconds and 10 GB about 15 minutes; at 1000 Mbps those become about 9 seconds and 1.5 minutes. When you need precision for a specific file size, use the "',
        '" tool.',
        'Are the table values accurate?',
        'They are estimates for common combinations, converted with a fixed efficiency and ignoring real network congestion and protocol overhead. Fine for quick communication, but use precise calculation for proposals or contracts.',
        'What if I cannot find my combination?',
        'The quick table only covers common bandwidth and file type combinations. For any other combination use "Bandwidth and Download Time Calculator" with your actual parameters, or start from the nearest entry for a magnitude estimate.',
        'About "Bandwidth (Mbps) and Download Time Quick Lookup"',
        'Bandwidth (Mbps) and Download Time Quick Lookup. A free online tool processed entirely in the browser, no data uploaded, your privacy and security protected.',
        'Type what you want to look up...',
    ]))


if __name__ == '__main__':
    main()

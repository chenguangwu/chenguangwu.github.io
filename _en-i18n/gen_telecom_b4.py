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
    write('index', build('index', [
        '📡 Telecom Engineering Tools',
        'Telecom Engineering',
        'Telecom Engineering Tools',
        'Bandwidth and Download Time Calculator: enter file size and network bandwidth (Mbps) to estimate download time, for network transfer and experience evaluation.',
        'Theoretical conversion between bit error rate (BER) and energy per bit to noise density ratio (Eb/N0) for digital modulation, supporting BPSK/QPSK/16QAM/64QAM.',
        'Bandwidth (Mbps) and Download Time Quick Lookup',
        'Quick bandwidth and download time lookup: compute download duration from bandwidth (Mbps) and file size, with common file type references for network planning.',
        'BER and SNR Conversion',
        'BER and SNR converter: converts between BER and SNR under a channel model, for link quality assessment and budgeting.',
        'Estimate wireless path loss from frequency, distance and antenna parameters, compare coverage across bands, and support preliminary base station and in-distribution design. Runs purely in the browser.',
        'Split one network into multiple equal-size subnets, auto-generating each subnet address, usable range and broadcast address for address planning and allocation.',
        'Free Space Path Loss Estimator',
        'Compute free space path loss (FSPL) from the Friis transmission equation, with optional received signal strength estimation',
        'Online wireless AP coverage radius calculator: enter transmit power, antenna gain and receiver sensitivity to estimate coverage distance, for Wi-Fi deployment planning. Runs purely in the browser.',
        'About "Telecom Engineering Tools"',
        'This Telecom Engineering Tools collection gathers 8 free online tools covering the common calculation, conversion and lookup needs of telecom engineering. Whether you are a practitioner, a student or an ordinary user, you will find ready-to-use utilities here. Every tool runs purely in the browser; no data is uploaded to the server, so your privacy and security are protected.',
        'Telecom engineering tools included on this page (representative tools only):',
        'These tools help you finish common telecom engineering tasks fast, with no need to memorize complex formulas or convert by hand - input and you get the result.',
        'Do the Telecom Engineering Tools require downloads or registration?',
        'No. All Telecom Engineering Tools on this page are pure front-end online tools: open the page and use them right away, with no software to install, no account to register, and no data uploaded.',
        'Are the Telecom Engineering Tools results accurate, and is the data safe?',
        'The tools compute in your browser using public math formulas and common industry standards, so results are available instantly. All computation happens locally on your device; no data is uploaded to the server, so privacy and security are guaranteed.',
    ]))

    write('subnet-planner', build('subnet-planner', [
        '🌐 Subnet Planner',
        'Split one network into multiple equal-size subnets, auto-generating each subnet address, usable range and broadcast address for address planning and allocation.',
        'Core formula (from input variables): (netAddr+subnetSize-1)>>>0; min(subCount,1024); (2)^newMask-oldMask',
        '📖 Read the "Subnet Planner User Guide"',
        'Original network address',
        'Original prefix (/)',
        'Split method',
        'By new prefix',
        'By subnet count',
        'New prefix (/)',
        'Subnet count',
        '📋 Splitting rules',
        'Equal-size subnet split:',
        'Borrowing n host bits splits the original network into 2ⁿ subnets.',
        'New prefix = original prefix + n',
        ', and each subnet holds 2^(32−new prefix) addresses.',
        'Usable hosts:',
        'When the new prefix is ≥31 it is point-to-point / single host; otherwise 2^(32−new prefix) − 2 (network and broadcast addresses removed).',
        'The network address of subnet index i = base address + i × subnet size.',
        '📚 Deep dive: subnetting and address planning',
        'Split a large block evenly by the new prefix to get each subnet address, usable range and broadcast address.',
        'Work backward from the required subnet count to see how many bits to borrow, avoiding too few hosts after splitting.',
        'Pre-generate the list when assigning subnets to departments or floors and paste it straight into the configuration document.',
        'Splitting 192.168.1.0/24 into /26',
        'New prefix /26 → subnet count = 2^(26−24) = 4; addresses per subnet = 2^(32−26) = 64, usable hosts = 64 − 2 = 62. New mask 255.255.255.192, the four subnets are 192.168.1.0/26, 192.168.1.64/26, 192.168.1.128/26 and 192.168.1.192/26, with usable ranges .1-.62, .65-.126, .129-.190 and .193-.254 respectively. If you ask for "6 subnets", the tool rounds up to 3 borrowed bits → /27, giving 8 subnets with 30 usable hosts each.',
        'Why subtract 2 from the hosts per subnet?',
        'The subnet network address (all 0s) and broadcast address (all 1s) cannot be assigned to hosts, so usable count = address count − 2. /31 and /32 are the exceptions, treated as point-to-point links and host routes.',
        'Why does the count increase when splitting by subnet count?',
        'The subnet count must be an integer power of two. If you ask for 6, the tool rounds up to 8 (borrowing 3 bits), and the 2 extra subnets can be kept in reserve or merged later.',
        'About "Subnet Planner"',
        'Subnet Planner is an online tool in the IT development domain. It is an online tool built for developers, runs purely in the browser, and no code leaves your browser.',
    ]))


if __name__ == '__main__':
    main()

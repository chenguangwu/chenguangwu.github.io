#!/usr/bin/env python3
# gen_encode_b3.py — encode b3 (5 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'encode')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'encode')

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
    out = {'slug': slug, 'industry': 'encode', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

CRE = [
 "#️⃣ CRC Error-Detection Capability",
 "Estimate undetected-error probability and overhead from CRC width (e.g. 16 or 32) and channel bit error rate, comparing CRC-16 with CRC-32.",
 "📖 View Guide: CRC Error-Detection Capability",
 "Generator polynomial degree",
 "Transfer frames",
 "Data bit width",
 "Undetected random-error probability for CRC ≈ 2⁻ʳ",
 "Larger r means stronger detection; common CRC-16 (r=16), CRC-32 (r=32).",
 "📚 In Depth: CRC Error-Detection Capability",
 "Protocol selection: compare",
 "-16/CRC-32 miss rates and bandwidth cost at the target error rate.",
 "Storage checksum planning: choose a detection-strength vs overhead balance for firmware/images.",
 "Teaching contrast: show the exponential drop in miss rate when bit width doubles.",
 "Example: CRC-32, BER 1e-6",
 "Random-error miss rate is around 1/2^32, far below CRC-16's 1/2^16, fitting high-reliability transfer.",
 "Can CRC correct errors?",
 "No, detection only; correction needs Hamming or Reed-Solomon codes.",
 "Why is CRC-32 stronger?",
 "Higher polynomial degree raises burst and random error detection exponentially with bit width.",
 "Does CRC prevent tampering?",
 "No; the known polynomial can be deliberately collided, use a cryptographic hash for tamper resistance.",
]

CRC = [
 "#️⃣ CRC Checksum Width",
 "Look up the checksum width and hex length for common CRC standards (CRC-8, CRC-16, CRC-32) for protocol design.",
 "📖 View Guide: CRC Checksum Width",
 "Generator polynomial degree",
 "Input bytes",
 "CRC-n produces an n-bit checksum",
 "Hex length = ceil(n/4)",
 "Common CRC-8/CRC-16/CRC-32.",
 "📚 In Depth: CRC Checksum Width",
 "Protocol field planning: pick the standard and",
 "width and appended byte count.",
 "Cross-system alignment: confirm the peer uses the same CRC bit width and representation length.",
 "Teaching quick reference: directly list the bit-width comparison of common CRC standards.",
 "Example: CRC-32",
 "Bit width 32 bits, shown as 8 hex chars; CRC-16 is 16 bits, 4 chars.",
 "How do bit width and standard name relate?",
 "CRC-N is usually an N-bit checksum; the specific polynomial is defined by the standard (e.g. CRC-32's 0x04C11DB7).",
 "Why is a polynomial needed?",
 "The polynomial determines detection characteristics; bit width alone is not enough, and cross-system use needs the same polynomial.",
 "How is the representation length computed?",
 "Every 4 bits is one hex char, so 8/16/32 bits map to 2/4/8 chars.",
]

E2 = [
 "📏 Hamming Distance Estimator",
 "Estimate the differing-bit count of two equal-length binary strings for error-correction and link-reliability analysis.",
 "📖 View Guide: Hamming Distance Estimator",
 "Binary string length",
 "Differing-bit ratio %",
 "Samples",
 "Hamming distance = count of positions where two equal-length strings differ",
 "The difference rate can be approximated by sampling statistics.",
 "📚 In Depth: Hamming Distance Estimator",
 "Error-correcting code design: Hamming distance sets detectable/correctable errors (distance d corrects floor((d-1)/2) bits).",
 "DNA / sequence alignment: use edit distance to approximate sequence differences.",
 "Dedup and similarity: compare bit differences of hashes or fingerprints to find near-duplicates.",
 "Example: 10110 vs 10011",
 "Bit-by-bit, positions 3 and 5 differ, Hamming distance = 2; it detects 1-bit error but cannot correct it (needs distance >= 3).",
 "What if lengths differ?",
 "Strict Hamming distance requires equal length; for unequal lengths use aligned edit distance or sampling approximation.",
 "How does Hamming distance relate to error correction?",
 "Codeword minimum distance d detects d-1 errors and corrects floor((d-1)/2) errors.",
 "Can it measure",
 "text similarity",
 "?",
 "For fixed-length encodings (e.g. hashes) yes; free text needs encoding first then comparison.",
]

E3 = [
 "#️⃣ Hash Output Length",
 "Look up the output length (bytes and bits) of common hash algorithms (MD5, SHA family) for hash value storage planning.",
 "📖 View Guide: Hash Output Length",
 "Algorithm code 1=MD5 2=SHA1 3=SHA256 4=SHA512",
 "Output base 16=hex 64=Base64",
 "Hex length = bytes x 2",
 "Used to estimate hash value storage space.",
 "📚 In Depth: Hash Output Length",
 "Field design: choose hash length for databases/indexes to balance collision and storage.",
 "Signature integration: confirm the peer's digest bit count (e.g. SHA-256 is 32 bytes).",
 "Teaching quick reference: compare",
 "/SHA-1/SHA-256 output scale.",
 "Example: SHA-256",
 "Output 256 bits = 32 bytes = 64 hex chars.",
 "Is MD5 still usable?",
 "Only for non-security checks (e.g. dedup); broken, so not for integrity/tamper resistance.",
 "How do bits relate to security?",
 "Collision resistance scales roughly with half the bits (birthday attack); SHA-256 far exceeds MD5/SHA-1.",
 "Why give both bytes and bits?",
 "Storage uses bytes, display uses hex (2 chars/byte); both are common.",
]

E4 = [
 "📻 Morse Code Transmission Time",
 "Convert an English word or character sequence into Morse dot/dash and gap timings to estimate total transmission time.",
 "📖 View Guide: Morse Code Duration",
 "Letter count",
 "Average dots/dashes per letter",
 "Unit duration ms",
 "Each symbol includes dot/dash and gaps; actual duration is about dot-dash count x 1.5 units",
 "Used to understand Morse code transmission speed.",
 "📚 In Depth: Morse Code Transmission Time",
 "Hand/electronic key planning: estimate a message's send time at a target WPM (words/min).",
 "Teaching demo: visually show the timing relation of dot (1 unit), dash (3 units) and gaps.",
 "rhythm training",
 "to set a timing baseline for single characters/words in practice.",
 "Example: SOS @20WPM",
 "SOS (...---...) at 20 WPM (about 60 ms/unit) finishes in about 1.3 seconds (including character/word gaps).",
 "WPM vs unit duration?",
 "Under the PARIS standard, 1 WPM ≈ 1200 ms/unit, 20 WPM ≈ 60 ms/unit.",
 "Why is a dash 3 units?",
 "Convention: dot = 1, dash = 3 units; intra-character gap = 1, inter-character = 3, inter-word = 7.",
 "Does it support Chinese?",
 "Standard Morse covers only Latin letters, digits and a few punctuation; Chinese needs pinyin/digits first.",
]

write('crc-error-rate', build('crc-error-rate', CRE))
write('crc', build('crc', CRC))
write('encode-2', build('encode-2', E2))
write('encode-3', build('encode-3', E3))
write('encode-4', build('encode-4', E4))

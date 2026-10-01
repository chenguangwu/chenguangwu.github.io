#!/usr/bin/env python3
# gen_encode_b4.py — encode b4 (5 slugs): encode-5/encode-6/encode-7/encode/encoding-redundancy
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

E5 = [
 "🔳 QR Code Version Capacity",
 "Estimate the minimum QR version and capacity level from character count and encoding mode (numeric, alphanumeric, byte).",
 "📖 View the QR Code Version Capacity Guide",
 "Mode 1=Numeric 2=Alphanumeric 3=Byte",
 "Error correction 1=L 2=M 3=Q 4=H",
 "QR versions 1-40; capacity varies with version and error-correction level",
 "Result is a rough estimate; the actual capacity depends on the encoding specification.",
 "📚 Deep Dive: QR Code Version Capacity",
 "Design: Pick the smallest version for the content to reduce module density and improve scannability.",
 "Error-tolerance trade-off: With a fixed version, choose the L/M/Q/H correction level.",
 "Capacity warning: If the estimate exceeds version 40, prompt to split or shorten the content.",
 "Example: 100 digits",
 "Numeric mode fits up to about version 3 (~80+ chars); version 4 is safer, depending on the correction level.",
 "Version vs capacity?",
 "QR versions 1-40 set the module count; higher versions hold more, and within a version numeric > alphanumeric > byte capacity decreases.",
 "Does the correction level affect capacity?",
 "Yes. L (7%) has the largest capacity and H (30%) the smallest; higher tolerance trades capacity for damage resistance.",
 "Why choose the smallest version?",
 "Fewer modules mean a sparser pattern that scans more reliably on print or screen; too large can fail to scan.",
 "How to use QR Code Version Capacity",
 "When planning printed QR content, determine the required version and capacity-for example on product packaging, business cards, posters, and tickets; when capacity is limited, trade off encoding mode (numeric/alphanumeric/byte/kanji) and correction level to avoid exceeding the version limit and failing generation.",
 "What does QR Code Version Capacity do?",
 "Enter the number of characters to encode and the mode (numeric, alphanumeric, or byte); the tool estimates the minimum QR version and capacity level, helping you generate a properly sized code.",
 "How do I use QR Code Version Capacity?",
 "Which scenarios suit QR Code Version Capacity?",
]

E6 = [
 "🔄 Radix Conversion Digits",
 "Compute the number of digits an integer needs in a target radix (2-36), comparing binary vs hex compactness.",
 "📖 View the Radix Conversion Digits Guide",
 "Target radix 2-36",
 "Supports radix 2-36.",
 "📚 Deep Dive: Radix Conversion Digits",
 "Bit-width planning: Pick the smallest width that covers the maximum value for registers/indexes",
 "radix digits",
 "Representation comparison: Visually show how the same number differs in length across binary, decimal, and hexadecimal.",
 "Encoding design: Determine the digits needed for a state count N in a given base (ceil(log_base(N))).",
 "Example: 255 to hexadecimal",
 "255 needs 2 hex digits (FF), 8 binary bits, or 3 decimal digits.",
 "Digit formula?",
 "For a positive integer N and base b, digits = floor(log_b(N))+1 (N=0 counts as 1 digit).",
 "Does it support decimals?",
 "This tool computes integer digits; decimals need separate floating-point representation rules.",
 "Why is the radix capped at 36?",
 "Digits 0-9 and letters A-Z give 36 symbols; beyond that you need a custom symbol set.",
]

E7 = [
 "#️⃣ Hash Collision Probability",
 "Estimate birthday-paradox collision probability from hash-space bits and stored item count; risk rises sharply as n approaches the square root of 2^bits.",
 "📖 View the Hash Collision Probability Guide",
 "Hash output bits",
 "Collision probability rises sharply as n approaches sqrt(2^bits).",
 "📚 Deep Dive: Hash Collision Probability",
 "Dedup/bucketing design: Assess the risk when hash-bucket size approaches",
 "the square root",
 "and collisions surge.",
 "Unique ID planning: Choose enough width for short IDs to keep in-system collision rate low.",
 "Safety boundary: Note that short hashes identify but do not prevent collisions.",
 "Example: 32-bit hash, 77k entries",
 "At ~50k entries the collision chance is already near 1%; after approaching sqrt(2^32) is about 65k it climbs fast, so move to 64 bits.",
 "Why the square root?",
 "birthday paradox",
 "Collision probability becomes significant when entries reach about sqrt(2*2^bits), not 2^bits.",
 "What if a collision happens?",
 "For dedup, cascade a second check (e.g., compare the original value); don't rely solely on hash equality.",
 "How large a space is safe?",
 "64 bits usually suffices against accidental collisions; resisting deliberate collisions needs 128-bit+ cryptographic hashes.",
]

ENC = [
 "🕵️ Caesar Cipher Shift",
 "Shift English letters by 0-25 to demonstrate the Caesar cipher, for teaching classical substitution ciphers.",
 "📖 View the Caesar Cipher Shift Guide",
 "Letter position A=0",
 "Shift amount",
 "Demonstrates letter-position math only; no full encrypt/decrypt.",
 "📚 Deep Dive: Caesar Cipher Shift",
 "Cryptography teaching: Visually show single-table substitution and cyclic shifting.",
 "Puzzles/games: Quickly generate or crack simple shift ciphertext.",
 "Concept demo: Show the weakness that the key space is only 25 and easily brute-forced.",
 "Example: HELLO shift 3",
 "H to K, E to H, L to O, L to O, O to R -> \"KHOOR\"; shift 0 or 26 gives plaintext.",
 "Is it secure?",
 "No. The key space is only 25, so brute force cracks it; for teaching only.",
 "How are non-letter characters handled?",
 "Spaces, punctuation, and digits are usually kept unchanged; only A-Z/a-z shift cyclically.",
 "What if the shift exceeds 25?",
 "Modulo 26; shift 26 equals shift 0 (plaintext).",
]

ER = [
 "🔐 Encoding Redundancy",
 "Compare average code length with source entropy to compute redundancy (avgLen - H) / H; lower redundancy means a better code.",
 "📖 View the Encoding Redundancy Guide",
 "Average code length",
 "Information entropy",
 "Symbol count",
 "Redundancy = (avg length - entropy) / avg length",
 "Lower redundancy means a better code; ideally it approaches 0.",
 "📚 Deep Dive: Encoding Redundancy",
 "Source-coding optimization: Assess Huffman/arithmetic coding redundancy vs entropy to guide compression.",
 "Channel-efficiency analysis: Compare average lengths of different variable-length codes against the theoretical lower bound.",
 "Teaching demo: Show the wasted redundancy of fixed-length codes when symbol probabilities are uneven.",
 "Example: two symbols p=0.9/0.1",
 "Entropy is about 0.469 bit; a fixed 1 bit/symbol gives redundancy about 113%, while Huffman approaches entropy with near-zero redundancy.",
 "Why isn't lower redundancy always better?",
 "For error correction we often add redundancy deliberately (e.g., channel coding); efficiency and reliability must be balanced.",
 "Relation to compression ratio?",
 "Lower source-coding redundancy means stronger compression; this metric measures the gap from the Shannon limit.",
 "How is entropy computed?",
 "H = -Sum p_i*log2(p_i), see",
 "the tool.",
]

write('encode-5', build('encode-5', E5))
write('encode-6', build('encode-6', E6))
write('encode-7', build('encode-7', E7))
write('encode', build('encode', ENC))
write('encoding-redundancy', build('encoding-redundancy', ER))

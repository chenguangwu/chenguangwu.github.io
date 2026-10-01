#!/usr/bin/env python3
# gen_encode_b6.py — encode b6 (5 slugs): radix-digits/shannon-entropy/url-encoded-length/url/utf-8
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

RD = [
 "🧮 Radix Digit Count",
 "Compute the minimum digits needed to represent N states in a chosen radix (e.g. 256 states need 2 hex digits).",
 "📖 View the Radix Digit Count Guide",
 "States to represent",
 "Byte capacity",
 "For example, 256 states need 2 digits in hexadecimal.",
 "📚 Deep Dive: Radix Digit Count",
 "State encoding: Pick the fewest radix digits for a finite-state machine's state count.",
 "Address/index planning: Digits needed for N cells in base b is ceil(log_b(N)).",
 "Representation comparison: Compare binary vs hex compactness for the same state space.",
 "Example: N=256, hexadecimal",
 "ceil(log_16(256))=2 digits (00-FF); binary needs 8 bits.",
 "Formula?",
 "Minimum digits = ceil(log_b(N)), with N the total states and b the radix.",
 "Difference?",
 "The former counts digits to cover a number of states; the latter counts the length of a specific value.",
 "What if N=0 or 1?",
 "For N<=1, record 1 digit (a single state needs no distinction).",
]

SE = [
 "🌡️ Shannon Entropy",
 "Compute Shannon entropy H (bits/symbol) from discrete source symbol probabilities (probabilities should sum to 1; zero-probability terms count as 0).",
 "📖 View the Shannon Entropy Guide",
 "Event1 probability",
 "Event2 probability",
 "Event3 probability",
 "Event4 probability",
 "Probabilities should sum to 1; a zero-probability event contributes 0.",
 "📚 Deep Dive: Shannon Entropy",
 "Compression limit: Entropy is the theoretical lower bound on average code length for lossless compression.",
 "Randomness check: High entropy suggests the data is close to",
 "a uniform distribution",
 ", and more \"random\".",
 "Cryptographic strength: The entropy of keys/nonces measures resistance to guessing.",
 "Example: fair coin",
 "p=0.5/0.5 -> H = -2x0.5*log2(0.5) = 1 bit/symbol; less bias means lower entropy.",
 "Must probabilities sum to 1?",
 "Yes; discrete-source probabilities are normalized, and input frequencies are auto-normalized.",
 "How are zero-probability terms handled?",
 "By the limit 0*log(0)=0, they add nothing to entropy.",
 "Is higher entropy always good?",
 "In compression, high entropy means hard to compress; in security, high entropy (keys) is good.",
]

UEL = [
 "🔤 URL Encoded Length Estimator",
 "Estimate the RFC 3986 encoded length of a URL containing CJK, spaces or symbols (only alphanumerics and -_.~ are safe).",
 "📖 View the URL Encoded Length Estimator Guide",
 "Special characters",
 "Already-encoded characters",
 "URL encoding turns each unsafe char into %XX (3 chars)",
 "Encoded length = safe chars + 3 x chars to encode",
 "Only A-Z a-z 0-9 and -_.~ are safe; all others must be encoded.",
 "📚 Deep Dive: URL Encoded Length Estimator",
 "Request-line budget: Long params with CJK grow a lot after percent-encoding; estimate whether they exceed server limits.",
 "Link generation: Length planning for Chinese params embedded in short/share links.",
 "Gateway limit check: Avoid encoded URLs exceeding proxy/browser length caps.",
 "Example: \"q=hello world\"",
 "Each of the 2 CJK chars is 3 UTF-8 bytes -> 9 %XX chars total; the encoded string is much longer than the original.",
 "Which characters are not encoded?",
 "In RFC 3986, A-Z a-z 0-9 and -_.~ are safe; everything else (incl. CJK/space) becomes %XX.",
 "Why do CJK chars get so long?",
 "Each CJK char is 3 UTF-8 bytes, and each byte becomes %XX (3 chars), so 1 CJK char is about 9 chars.",
 "Difference?",
 "This tool estimates absolute length; the other estimates the relative expansion ratio.",
]

URL = [
 "🔤 URL Encoding Space Overhead",
 "Estimate the percent-encoding size growth of a URL or query string to anticipate parameter bloat in links.",
 "📖 View the URL Encoding Space Overhead Guide",
 "Chars to encode",
 "Each non-ASCII/special char encodes to %XX (3 chars)",
 "Space encodes to %20 or +",
 "Used to estimate URL parameter length.",
 "📚 Deep Dive: URL Encoding Space Overhead",
 "Link size planning: Assess the expansion rate of CJK/symbol-heavy params after encoding.",
 "Storage budget: Estimate encoded field width before saving URLs to the database.",
 "Comparison: Compare the encoding overhead of different param sets side by side.",
 "Example: a param with 10 CJK chars",
 "About 30 bytes become about 90 chars after encoding, ~200% growth (each CJK char is about 9 chars).",
 "How do ratio and length relate?",
 "The ratio measures relative growth; the length tool gives absolute chars; the two are complementary.",
 "Why do CJK chars expand so much?",
 "Each CJK char is 3 UTF-8 bytes, each encoded as %XX (3 chars), so about 3x.",
 "Can the expansion be reduced?",
 "You can Base64Url the whole string or use a shorter encoding, but that sacrifices readability.",
]

U8 = [
 "💾 UTF-8 Byte Count",
 "Estimate the UTF-8 byte size from counts of ASCII and multibyte characters (CJK, emoji) for storage estimation.",
 "📖 View the UTF-8 Byte Count Guide",
 "CJK (3-byte) characters",
 "Emoji (4-byte) characters",
 "ASCII = 1 byte",
 "Latin/Greek etc. = 2 bytes",
 "Common CJK = 3 bytes",
 "Emoji = 4 bytes",
 "Used to estimate multilingual text storage size.",
 "📚 Deep Dive: UTF-8 Byte Count",
 "Storage planning: Estimate byte size of mixed Chinese/English text by character type.",
 "Transfer budget: The true byte length of API payloads after UTF-8 encoding.",
 "DB fields: Set VARCHAR width by bytes, not chars (e.g. MySQL utf8mb4).",
 "Example: 10 ASCII + 5 CJK",
 "10x1 + 5x3 = 25 bytes; with emoji it is 4 bytes each.",
 "Why is UTF-8 variable length?",
 "ASCII is 1 byte, common CJK 3 bytes, some symbols/emoji 4 bytes, balancing compatibility and compactness.",
 "How many bytes does an emoji take?",
 "Most are 4 bytes (utf8mb4); some combined emoji are longer.",
 "How does it differ from character count?",
 "Chars != bytes; under UTF-8 you must count bytes for storage/transfer to avoid truncation and mojibake.",
]

write('radix-digits', build('radix-digits', RD))
write('shannon-entropy', build('shannon-entropy', SE))
write('url-encoded-length', build('url-encoded-length', UEL))
write('url', build('url', URL))
write('utf-8', build('utf-8', U8))

#!/usr/bin/env python3
# gen_encode_b1.py — encode b1 (5 slugs)
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

ASCII = [
 "🔍 ASCII Readability Check",
 "Estimate the share of ASCII and printable characters in text.",
 "📖 View Guide: ASCII Readability Check",
 "Non-ASCII count",
 "Control character count",
 "ASCII ratio = (total - non-ASCII) / total",
 "Control characters (e.g. newlines) may be counted within a safe range as needed.",
 "📚 In Depth: ASCII Readability Check",
 "Initial readability check for logs/packet captures: high printable ASCII suggests plaintext, low ratio often means binary or wrong encoding.",
 "Garble localization: compare raw vs decoded ASCII ratio on a garbled Chinese page to locate the faulty encoding step.",
 "Pre-ingest cleaning: filter non-text fields by a readability threshold to avoid binary contamination.",
 "Example: mixed log snippet",
 "A log with Chinese and binary fragments has about 62% printable ASCII, indicating embedded non-text content; first run",
 "encoding detection",
 "then ingest.",
 "What ASCII ratio counts as readable text?",
 "No absolute threshold; printable ASCII above 80% with very few control characters is usually treated as plain text, depending on the use case.",
 "Does Chinese affect the judgment?",
 "Yes. Each Chinese UTF-8 character is 3 bytes and all non-ASCII; this metric focuses on whether large binary or unprintable bytes are present, and alone cannot prove Chinese mojibake.",
 "Can it distinguish Base64 from plaintext?",
 "Base64 uses only 64 printable characters with high ASCII ratio but high entropy; judge further by character distribution (only A-Z a-z 0-9 + / =).",
]

B32 = [
 "🔤 Base32 Encoded Length Estimator",
 "Estimate the encoded string length from input bytes per Base32 rules.",
 "📖 View Guide: Base32 Encoded Length Estimator",
 "Include padding 1=yes 0=no",
 "Base32 encodes every 5 bytes into 8 characters",
 "With padding, length is always a multiple of 8",
 "Used to estimate the encoded data size.",
 "📚 In Depth: Base32 Encoded Length Estimator",
 "Key/token length planning: TOTP secrets and random tokens expand about 1.6x via Base32; size storage fields accordingly.",
 "Short-link capacity: Base32 avoids lowercase and ambiguous chars, fitting length budgets for manual copying.",
 "Versus Base64: Base32 expands more but has a safer alphabet, used for ambiguity-free display.",
 "Example: 20 bytes",
 "random bytes",
 "20 bytes encode to 32 Base32 chars (ceil(20/5)*8 = 32), used for one-time-password secret display for verbal verification.",
 "Why is Base32 longer than Base64?",
 "Each Base32 char carries only 5 bits (Base64 carries 6), so the same data needs more characters, expanding about 60%.",
 "How is padding computed?",
 "Base32 pads with = to a multiple of 8 characters; the length estimate already includes padding.",
 "What scenarios is it good for?",
 "Manual copying and verbal checks where confusing 0/O and 1/l must be avoided.",
]

B58 = [
 "🔤 Base58 Checked Length",
 "Estimate the Base58-encoded length including the 4-byte checksum.",
 "📖 View Guide: Base58 Checked Length",
 "Payload bytes",
 "Checksum bytes",
 "Version bytes",
 "Each Base58 char carries about log2(58) ≈ 5.86 bits",
 "Often used for cryptocurrency address length estimation.",
 "📚 In Depth: Base58 Checked Length",
 "Bitcoin address budget: 33 bytes (version + pubkey hash + 4 checksum) encode to about 34 Base58 chars.",
 "Private key / WIF length check: compare how the checksum affects the final length.",
 "Typo-proof planning: Base58 removes ambiguous chars, fitting length budgets for manual address checks.",
 "Example: Bitcoin P2PKH address",
 "Version 1 byte + pubkey hash 20 bytes + checksum 4 bytes = 25 bytes, Base58 encodes to about 34 chars.",
 "Why Base58 instead of Base64?",
 "Base58 removes ambiguous chars like 0/O/1/l/I, lowering manual-copy error rates.",
 "What does the checksum do?",
 "The first 4 bytes of double SHA256, used to detect address input errors.",
 "Why is the length not an integer multiple?",
 "Base58 does not group by powers of two; length is approximately ceil(n*log(256)/log(58)).",
]

B64LEN = [
 "🔤 Base64 Encoded Length",
 "Compute the Base64 character count from input bytes.",
 "📖 View Guide: Base64 Encoded Length",
 "Include padding 1/0",
 "Line-break chars (0 = none)",
 "Base64 encodes every 3 bytes into 4 characters",
 "Chars = ceil(n/3) x 4; pad 2 for remainder 1, 1 for remainder 2 =",
 "Base64 cannot be shortened; this is only a length estimate.",
 "📚 In Depth: Base64 Encoded Length",
 "API payload budget:",
 "Small inlined images expand about 33% via Base64; estimate request-body limits accordingly.",
 "Email /",
 "Attachment planning: estimate size and line count of MIME Base64 attachments.",
 "Database field design: estimate the width needed for Base64 columns.",
 "Example: 100 KB file",
 "100x1024 bytes -> ceil(100x1024/3)x4 ≈ 136,708 chars, about 133 KB (expands by 1/3).",
 "Why is it always about 1/3 larger?",
 "6-bit groups map to 8-bit chars at a 4/3 ratio; round up and optionally wrap at 76 chars.",
 "Do line breaks add length?",
 "MIME adds CRLF every 76 chars; pure length excludes breaks, but real transfer must count them.",
 "Can it be used in URLs?",
 "No; + / must be replaced with - _, use Base64Url (see",
 "Base64 encode/decode",
 "tool).",
]

B64SIZE = [
 "🔤 Base64 Encoded Size",
 "Estimate the Base64 output size from the original data size.",
 "📖 View Guide: Base64 Encoded Size",
 "Original size KB",
 "Header metadata KB",
 "Per-line break overhead %",
 "Base64 encodes every 3 bytes into 4 chars, growing about 33%",
 "With line-break overhead the size grows further.",
 "📚 Base64 Quick Reference",
 "Encoding rule",
 "Every 3 bytes of raw data become 4 chars, size grows by about",
 "Standard alphabet",
 "A-Z a-z 0-9 + / , padding char",
 "URL-safe variant",
 "Replace",
 "with",
 ", commonly used in URLs / file names",
 "Email attachments (MIME), Data URI, token transfer, binary-to-text",
 "Note: Base64 is encoding, not encryption; it provides no confidentiality.",
 "📚 In Depth: Base64 Output Size and Line-Break Overhead",
 "Estimate Base64 char and byte volume from the original KB count.",
 "Assess the extra overhead from MIME line breaks (every 76 chars).",
 "Capacity planning for email attachments and inlined resources.",
 "10 KB inlined image",
 "10 KB raw data becomes about 13.3 KB after Base64 (about 33% growth); with a 76-char wrap, add about 2.6% line-break overhead.",
 "With data URI header",
 "Adding the data:image/png;base64, header slightly increases total length; ideal for writing directly into HTML /",
 "background-image.",
 "Why does Base64 grow by 33%?",
 "Every 3 bytes become 4 chars, a 4/3 ≈ 1.33x increase in char count, so size grows about 33%.",
 "How much do line breaks add?",
 "MIME inserts CRLF every 76 chars; the overhead is about 2/76 ≈ 2.6% of the char count.",
]

write('ascii-readability', build('ascii-readability', ASCII))
write('base32', build('base32', B32))
write('base58', build('base58', B58))
write('base64-length', build('base64-length', B64LEN))
write('base64-size', build('base64-size', B64SIZE))

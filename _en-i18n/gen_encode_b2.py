#!/usr/bin/env python3
# gen_encode_b2.py — encode b2 (5 slugs)
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

BIN = [
 "🔐 Binary / Hex to ASCII",
 "Each ASCII character is 8 bits (1 byte), representable as 8 binary bits or 2 hex digits. Paste a continuous encoded string, choose the radix, and decode it into readable text.",
 "Binary / Hex to ASCII",
 "/ Binary / Hex to ASCII",
 "📖 View Guide: Binary to ASCII",
 "Parse 8 bits per byte: ASCII ranges 0 to 127, e.g. 01000001 = 65 = letter A, 00110000 = 48 = digit 0; each hex digit maps to 4 bits (0x41 = 01000001); printable chars are 32 to 126, others are control chars (0x0A newline, 0x0D carriage return); group by 8 bits when unseparated, or split by the delimiter when space-separated, then convert each group to decimal and map to a character.",
 "Encoded string (binary or hex)",
 "Encoding radix",
 "Binary (8 bits/group)",
 "Hex (2 digits/group)",
 "Each binary group of 8 bits is one byte; each hex pair is one byte; spaces and newlines are ignored automatically.",
 "Covers ASCII only (0-127). Non-ASCII (e.g. Chinese UTF-8) is multi-byte; it needs UTF-8 byte splitting then per-byte conversion, which this tool does not support directly.",
 "If the result is garbled, the bit count is likely wrong or other characters were mixed in; clean the input first.",
 "📋 Example",
 "📚 In Depth: Binary / Hex to ASCII",
 "Protocol packet analysis: restore captured 8-bit binary/hex strings into readable ASCII.",
 "Teaching demo: visually show the one-to-one mapping between characters and binary/hex.",
 "Debug embedded data: eyeball readable strings from a binary stream.",
 "Example: hex 48656C6C6F",
 "Map by every 2 digits: 48=H, 65=e, 6C=l, 6C=l, 6F=o -> \"Hello\".",
 "What if the bit count is wrong?",
 "Binary needs 8-bit groups, hex needs 2-digit groups; uneven length causes misalignment or zero-padding, so align first.",
 "Can non-printable characters be shown?",
 "Control characters (e.g. 0x00/0x0A) have no readable glyph and are usually shown as escapes or placeholders.",
 "Does it support Chinese?",
 "Convert to a UTF-8 byte sequence first, then decode per byte; a single character may span multiple bytes.",
 "How to use Binary / Hex to ASCII",
 "Parse the ASCII payload in network or serial communication packets; troubleshoot character data printed in binary or hex form by embedded devices or logs; demonstrate the mapping between binary, hex and ASCII characters.",
 "What does Binary / Hex to ASCII do?",
 "How to use Binary / Hex to ASCII?",
 "What scenarios is Binary / Hex to ASCII good for?",
 "Map binary (8 bits per group) to characters by the ASCII table; the result is the corresponding text.",
 "For encoding debugging, teaching and data observation. Note: group by 8 bits and use a consistent charset (e.g. UTF-8/ASCII); non-printable characters may not display.",
]

C1 = [
 "🔤 Base64 Encode / Decode",
 "Supports standard Base64 and Base64URL, correctly handling Unicode text.",
 "Base64 Encode / Decode",
 "/ Base64 Encode / Decode",
 "📖 View Guide: Base64 Encode / Decode",
 "Base64 regroups every 3 bytes (24 bits) into 4 groups of 6 bits, each mapped to a 64-char table (A-Z, a-z, 0-9, plus, slash); short groups are zero-padded and filled with equals (1 missing byte -> 2 equals, 2 missing -> 1 equals); encoded length = ceil(original / 3) * 4; Base64URL uses hyphen for plus, underscore for slash and drops padding; Unicode text must be UTF-8 byte-encoded first.",
 "Use Base64URL (URL safe)",
 "Encoding: convert any text into a Base64 string.",
 "Decoding: restore a Base64 string to the original text; failure shows an error.",
 "Base64URL replaces + with -, / with _, and removes the trailing =.",
 "📚 In Depth: Base64 Encode / Decode",
 "Front-back data exchange: put binary/",
 "safely into",
 "text fields.",
 "Token/signature transfer: encode/decode Base64URL fragments like JWT and signatures.",
 "Debug check: decode a captured Base64 string to view the original.",
 "Example: encode \"ToolBox\"",
 "ToolBox -> VG9vbEJveA==; decode back to the original text, mind the padding =.",
 "Base64 vs Base64URL?",
 "The latter replaces +/ with -_ and drops padding, so it sits in URLs/file names without escaping.",
 "Why treat Chinese specially?",
 "UTF-8 byte-encode first, then Base64; otherwise the platform default encoding causes errors.",
 "Common decode failures?",
 "Length not a multiple of 4, missing padding, or mixing standard/URL variants.",
]

C2 = [
 "🔤 URL Encode / Decode",
 "Encode URL components with encodeURIComponent or decode a full URL.",
 "URL Encode / Decode",
 "/ URL Encode / Decode",
 "📖 View Guide: URL Encode / Decode",
 "URL encoding turns unsafe chars into percent plus two hex digits (space -> %20, Chinese byte-by-byte UTF-8); encodeURIComponent encodes everything except A-Z a-z 0-9 and - _ . ! ~ * ' ( ); encodeURI keeps colon, slash, question, hash, brackets, @ etc. as structural chars to preserve full URL semantics; decoding is the reverse, and illegal percent sequences should be kept as-is.",
 "Parse URL",
 "Encoding: run encodeURIComponent on the string.",
 "Decoding: run decodeURIComponent on the string.",
 "Parse URL: extract protocol, host, path, query parameters and other parts.",
 "📚 In Depth: URL Encode / Decode",
 "Parameter construction: escape user input before putting it into query params to avoid &/= truncation.",
 "Log restore: decode server-recorded encoded URLs back to readable addresses for troubleshooting.",
 "API debugging: verify the request line the frontend actually sends matches expectations.",
 "Example: encode \"a b&c=1\"",
 "encodeURIComponent -> \"a%20b%26c%3D1\"; decode back to the original, space becomes %20, & = become %26 %3D.",
 "encodeURI vs encodeURIComponent?",
 "The latter escapes more thoroughly (including ?#/ etc.), good for a single param value; the former keeps URL structural chars.",
 "Which characters need no encoding?",
 "RFC 3986 treats A-Z a-z 0-9 and - _ . ~ as safe and leaves them as-is.",
 "Still garbled after decoding?",
 "Usually the server did not decode as UTF-8; that is a server-side issue, the tool's decoding is correct.",
 "Enter text or URL here...",
]

CHK = [
 "#️⃣ Checksum Collision Probability",
 "Estimate the random undetected-error probability from checksum bit width and data volume; suitable for random errors only, not adversarial tampering.",
 "📖 View Guide: Checksum Collision Probability",
 "Checksum bit width (bits)",
 "Attempts",
 "Data to check (bits)",
 "Undetected random-error probability for an n-bit checksum ≈ 2⁻ⁿ",
 "Cumulative ≈ 1 - (1 - 2⁻ⁿ)^N",
 "Applies to random errors only; cannot prevent deliberate tampering.",
 "📚 In Depth: Checksum Collision Probability",
 "Link-layer selection: compare 8/16/32-bit checksum miss rates at a given error rate.",
 "Storage integrity: plan archive checksum width to balance cost and miss risk.",
 "Security boundary note: state that checksums cannot stop forgery; use a MAC/signature instead.",
 "Example: 16-bit checksum, 10^6 packets",
 "Random-error miss rate is around 1/65536, but an attacker can still construct collisions on purpose, so use only in non-security scenarios.",
 "Can a checksum prevent tampering?",
 "No. Checksums are linear and easily collide on purpose; preventing tampering requires a cryptographic hash or MAC.",
 "Are more bits always better?",
 "More bits lower the random miss rate but add overhead; trade off by channel error rate.",
 "Relationship?",
 "CRC is a checksum with a polynomial, stronger at detecting burst errors; see",
]

CMP = [
 "🗜️ Data Compression Ratio",
 "Compute the compression ratio and rate from original and compressed sizes to quantify compression effectiveness.",
 "📖 View Guide: Data Compression Ratio",
 "Compressed bytes",
 "File count",
 "Compression rate = (1 - compressed/original) x 100%",
 "The closer the rate is to 100%, the stronger the compression.",
 "📚 In Depth: Data Compression Ratio",
 "Storage optimization: compare compression rates of different algorithms on logs/backups.",
 "Transfer cost: estimate bandwidth saved by compressed messages.",
 "Format selection: compare gzip/zstd/zip effects on similar data.",
 "Example: 100 MB -> 30 MB",
 "Compression rate = (1-30/100)x100% = 70%, ratio = 100/30 ≈ 3.33x.",
 "Compression rate vs ratio?",
 "Rate = (1 - compressed/original) x 100% is the saved fraction; ratio = original/compressed is the volume multiple.",
 "Why does it sometimes grow?",
 "Compressed or",
 "random data",
 "has no redundancy, and the compression header adds a bit; that is normal.",
 "Is close to 100% always good?",
 "Higher rate saves more space but trades CPU and time; real-time scenarios may not be worth it.",
]

write('binary-to-ascii', build('binary-to-ascii', BIN))
write('calc-1', build('calc-1', C1))
write('calc-2', build('calc-2', C2))
write('checksum-collision', build('checksum-collision', CHK))
write('compression-ratio', build('compression-ratio', CMP))

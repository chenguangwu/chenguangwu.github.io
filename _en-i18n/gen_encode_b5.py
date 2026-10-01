#!/usr/bin/env python3
# gen_encode_b5.py — encode b5 (5 slugs): hamming-bits/html/huffman-avg-length/image-to-base64/jwt-size
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

HB = [
 "✅ Hamming Code Parity Bits",
 "Compute the Hamming parity bits r from data bits m using 2^r >= m + r + 1 for single-bit error correction.",
 "📖 View the Hamming Code Parity Bits Guide",
 "Data bits",
 "Total message data bits",
 "Transmission rate bit/s",
 "Smallest r satisfying 2^r >= m + r + 1",
 "Code length = m + r, efficiency = m/(m+r)",
 "Hamming code can detect and correct single-bit errors.",
 "📚 Deep Dive: Hamming Code Parity Bits",
 "Memory ECC design: Plan the fewest parity bits for m data bits to correct single-bit errors.",
 "Teaching demo: Show parity bits grow logarithmically as data bits increase.",
 "Protocol check planning: Estimate the cost of adding Hamming protection to critical fields.",
 "Example: 8-bit data",
 "Needs r=4 (2^4=16 >= 8+4+1=13), a 12-bit codeword, correcting 1 and detecting 2 errors.",
 "What does the formula mean?",
 "2^r >= m+r+1 ensures r parity bits can locate any of the m+r positions (including all-correct).",
 "How many bits can Hamming correct?",
 "Standard Hamming corrects 1 and detects 2 bit errors; SEC-DED adds one overall parity bit.",
 "Where are parity bits placed?",
 "At powers of two (1,2,4,8,...); data bits fill the rest, and parity covers locate the error bit.",
]

HTML = [
 "📏 HTML Entity Length",
 "Estimate the escaped length when special characters (&, <, >, quotes, etc.) are converted to HTML entities.",
 "📖 View the HTML Entity Length Guide",
 "Plain characters",
 "Characters to escape",
 "Unicode entities",
 "& < > \" etc. take 4-5 characters",
 "Unicode entity &#xHHHH; is about 7-8 characters",
 "Used to estimate the escaped text length after HTML escaping.",
 "📚 Deep Dive: HTML Entity Length",
 "Template size check: When user content has many special chars, escaping grows storage/transfer.",
 "XSS defense check: Confirm escaped entity length does not break layout truncation.",
 "Rich-text storage: Estimate escaped field width before saving to the database.",
 "Example: \"a<b&c\"",
 "Escaped to \"a&amp;lt;b&amp;amp;c\"; the original 6 chars become 19 (each special char expands to a 4-5 char entity).",
 "Which characters must be escaped?",
 "& < > \" ' must be escaped in the relevant context to prevent parsing errors and XSS.",
 "Why does length grow noticeably?",
 "Each entity like &amp; is 5 chars vs 1 original char, so volume multiplies when many special chars are present.",
 "URL encoding",
 "Difference?",
 "HTML entities display text safely on the page; URL encoding is for transmission. The two scenarios differ.",
]

HAL = [
 "🔐 Huffman Average Code Length",
 "Estimate the average code length and compression efficiency from symbol frequencies per Huffman coding.",
 "📖 View the Huffman Average Code Length Guide",
 "Symbol1 frequency",
 "Symbol1 code length",
 "Symbol2 frequency",
 "Symbol2 code length",
 "Symbol3 frequency",
 "Symbol3 code length",
 "Average length = Σ(fᵢ / Σf) · lᵢ",
 "The theoretical lower bound is entropy H",
 "Input frequencies (or probabilities; results match after normalization).",
 "📚 Deep Dive: Huffman Average Code Length",
 "Compression scheme evaluation: Compare Huffman average length vs fixed-length/arithmetic coding.",
 "Teaching demo: Show the optimal prefix tree where frequent symbols get short codes and rare ones long codes.",
 "Format optimization: Choose a symbol probability model for logs/protocols to shorten average length.",
 "Example: A:0.5 B:0.25 C:0.25",
 "Huffman code A=0,B=10,C=11; average length = 0.5x1+0.25x2+0.25x2 = 1.5 bit/symbol (entropy=1.5, already optimal).",
 "Why is Huffman optimal?",
 "It minimizes average length under the prefix-code condition, equal to entropy (when probabilities are powers of 2).",
 "Difference from arithmetic coding?",
 "Arithmetic coding crosses symbol boundaries and approaches entropy more closely; Huffman is simpler but slightly redundant.",
 "What if frequencies are unknown?",
 "First gather statistics or use a general model; for dynamic cases use adaptive Huffman.",
]

IMG = [
 "🖼️ Image to Base64",
 "Pick or drag an image to convert locally to a Base64 string; preview, check size, and copy in one click, ideal for embedding images in HTML/CSS/mini-programs.",
 "/ Image to Base64",
 "📖 View the Image to Base64 Guide",
 "Encode an image file into Base64 text (usually output as a Data URL).",
 "Flow",
 ": Read image byte stream -> Base64 encode -> assemble",
 ": Inline small icons to cut requests, embed in HTML/CSS, preview locally before upload.",
 "Cost",
 ": Encoded size grows about 33%; large images should not be inlined (empirical threshold within ~10KB).",
 ": Base64 is encoding, not compression, and does not shrink real transfer size.",
 "Click to choose an image, or drag it here",
 "Supports PNG / JPG / WebP / GIF; keep it under 5MB",
 "Copy data:URL",
 "Download image",
 "Output data:URL prefix",
 "Keep original format",
 "Force PNG",
 "Force JPEG",
 "Force WebP",
 "Base64 -> Image (paste to decode and preview)",
 "Decode preview",
 "📚 Deep Dive: Local Image to Base64 Inlining",
 "Convert small PNG/JPG/SVG images into Base64 strings inlined into the page.",
 "Preview and check the encoded size to decide if inlining fits.",
 "One-click copy of the data URI for direct use in",
 "Small-icon inlining",
 "A few-KB icon converted to Base64 can be written straight into CSS, saving one HTTP request but growing the stylesheet.",
 "Large photos should not be inlined",
 "A several-hundred-KB photo grows about 33% after Base64 and slows first paint; keep it as an external link.",
 "Does conversion upload to a server?",
 "No. Conversion runs locally in the browser; the image never leaves your device.",
 "What are the pros and cons of Base64 images?",
 "Pros: fewer requests and easy single-file distribution. Cons: larger size and uncacheable; only good for small images.",
 "Verify the result yourself before using it in production",
 "Paste a string starting with data:image/ or a raw base64 string",
]

JWT = [
 "📏 JWT Length Estimator",
 "Estimate the encoded JWT length from header, payload and signature sizes (Base64 inflates by about 33%).",
 "📖 View the JWT Length Estimator Guide",
 "Header bytes",
 "Payload bytes",
 "Signature length bytes",
 "Base64 encoding inflates by about 33%.",
 "📚 Deep Dive: JWT Token Length Estimate and Overhead",
 "Estimate total encoded JWT length from header/payload/signature sizes.",
 "Assess how the session token affects request-header size.",
 "Decide whether compact claims are needed to reduce length.",
 "Compact claims",
 "Header+payload 120 bytes each, signature 32 bytes; after ~33% Base64 inflation the token is about 250 bytes, fitting in a Cookie.",
 "Too many claims make it too long",
 "At 1 KB payload the token can exceed 1.4 KB and hit the gateway header limit; trim unnecessary claims.",
 "Why does a JWT get longer?",
 "All three parts use Base64",
 "URL encoding",
 ", and the original",
 "volume inflates about 33%; the signature adds a fixed length on top.",
 "How long is safe?",
 "Safety is not directly tied to length, but overlong tokens consume header quota; keep only necessary claims.",
]

write('hamming-bits', build('hamming-bits', HB))
write('html', build('html', HTML))
write('huffman-avg-length', build('huffman-avg-length', HAL))
write('image-to-base64', build('image-to-base64', IMG))
write('jwt-size', build('jwt-size', JWT))

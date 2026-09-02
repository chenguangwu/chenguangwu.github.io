#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 it/ 开发者工具集群的【英文版使用指南】guides/<slug>-guide.en.html（首批 15 个）。

背景：站点指南有两大模板体系——
1) V2 模板（cognition/senses 等 19 篇，gen_v2_brain_senses_guides_en.py 产出）：静态独立英文页 .en.html；
2) 原生 i18n 模板（it/ 及旧指南 164 篇）：body 用 data-i18n，靠 ?lang=en + guide-en-pack.js 渲染英文，
   sitemap 已声明 en-US -> ?lang=en，但英文翻译包未填，故 ?lang=en 仅换标题/描述、正文仍中文。

本生成器沿用 A 策略（独立 .en.html 静态英文页），与 19 篇 V2 英文指南一致、对 SEO 收录最稳、且
_build.py 已能自动识别 .en.html 兄弟页并把 sitemap hreflang 切到文件级。

it/ 模板无 .related/.faq 块，inject_en_link 通用降级：优先 V2 锚点，否则在 </nav> 后插入语言条。
内容据各工具实际功能撰写，非机翻套话。
"""
import json, io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDES_DIR = os.path.join(ROOT, 'guides')

EN = [
 {'slug':'base64','tool':'tools/it/base64.html','name':'Base64 Encode / Decode',
  'desc':'Base64 guide: convert text and binary files to and from Base64, including file to data URI, with URL-safe mode.',
  'intro':'Base64 encodes binary or text data into printable ASCII characters. It is widely used to embed data inside text protocols such as JSON, CSS and email. This ToolBox Base64 tool runs entirely in your browser for encoding and decoding, supporting both strings and files.',
  'features':['Text to Base64 and Base64 to text, both directions','File to Base64: turn images or files into data URIs','URL-safe mode: replace + / = with - _ and drop padding','One-click copy of the result','Large-file chunking to avoid UI freezing','Client-side only, nothing uploaded'],
  'scenarios':['Inline a small icon as Base64 in CSS to reduce requests','Transport binary data through text-only APIs','Embed attachments inside email bodies','Debug API payloads that contain Base64 fields'],
  'steps':['Pick Encode or Decode mode','For encode: paste text or choose a file; for decode: paste a Base64 string','If you need URL compatibility, enable URL-safe','Click convert and see the result instantly','Copy or download the output'],
  'tips':['Base64 adds about 33 percent size overhead, so avoid it for long-term large-file storage','Inline Base64 suits small icons; use a separate cached file for big images','Before decoding, confirm standard Base64; URL-safe strings must be converted back first'],
  'faqs':[('Is Base64 encryption?','No. Base64 is only encoding and anyone can decode it. Never use it to protect sensitive data.'),('What if the data URI is too long?','The source file is likely large; reference it as a separate file instead of inlining.')]},

 {'slug':'json-formatter','tool':'tools/it/json-formatter.html','name':'JSON Formatter',
  'desc':'JSON Formatter guide: pretty-print, validate and inspect JSON with instant syntax checking and path highlighting.',
  'intro':'The JSON Formatter pretty-prints compact JSON into a readable, indented structure and validates it as you type. It is the fastest way to make an API response or config file human-readable and to catch syntax errors before they break your code.',
  'features':['Pretty-print with configurable indentation','Live validation and clear error positions','Collapsible tree view for large documents','Spot invalid characters and trailing commas','Copy or download the formatted result','Runs locally, no upload'],
  'scenarios':['Read a minified API response from a logs panel','Check why a config file fails to parse','Share a readable version of a payload with a teammate','Inspect nested structures quickly'],
  'steps':['Paste or upload your JSON','Watch it format and validate in real time','Expand or collapse nodes to explore','Fix any highlighted errors','Copy or download the clean output'],
  'tips':['Use 2-space indent for web code, 4-space for configs','A trailing comma is invalid in strict JSON but valid in JSON5','Format before diffing two payloads to reduce noise'],
  'faqs':[('Does it change my data?','No, formatting only changes whitespace; the values stay identical.'),('Can it handle huge files?','Yes, but very large files are easier to explore with the collapse feature.')]},

 {'slug':'json-minify','tool':'tools/it/json-minify.html','name':'JSON Minifier',
  'desc':'JSON Minifier guide: strip whitespace and comments from JSON to shrink payloads for APIs and storage.',
  'intro':'The JSON Minifier removes all unnecessary whitespace, line breaks and (where supported) comments, producing the smallest valid JSON. Smaller payloads mean faster network transfers and less storage.',
  'features':['Remove whitespace and newlines','Optional comment stripping for JSONC','Preserve exact data values','One-click copy or download','Safe local processing'],
  'scenarios':['Shrink a config before saving to a database','Reduce the size of a response cached at the edge','Pack embedded JSON inside a script tag','Compare behavior before and after minify'],
  'steps':['Paste your JSON','Enable comment stripping if your source uses JSONC','Click minify','Copy or download the compact result'],
  'tips':['Minify only at the boundary; keep authored files readable','Minified JSON is hard to debug, so keep the source','Confirm the consumer accepts the exact same schema'],
  'faqs':[('Is minified JSON still valid?','Yes, it is standard JSON with only whitespace removed.'),('What about comments?','Standard JSON has no comments; comment stripping targets JSONC-style inputs.')]},

 {'slug':'json-diff','tool':'tools/it/json-diff.html','name':'JSON Diff',
  'desc':'JSON Diff guide: compare two JSON documents and see structural differences side by side.',
  'intro':'JSON Diff compares two JSON documents and shows exactly what changed: added, removed and modified keys and values. It is essential when reviewing API responses, config changes or data migrations.',
  'features':['Structural comparison, not just text','Added, removed and changed paths highlighted','Recursive object and array diffing','Side-by-side or unified view','Copy or export the difference report','Local and private'],
  'scenarios':['Spot what changed between two API responses','Review a teammate config pull request','Verify a migration did not alter data','Debug why two environments behave differently'],
  'steps':['Paste the original JSON on the left','Paste the modified JSON on the right','Click compare','Read the highlighted differences by path','Export or copy the report if needed'],
  'tips':['Format both sides first for cleaner diffs','Array order matters; sort before comparing if order is unstable','Focus on changed paths rather than raw text'],
  'faqs':[('Does order in arrays affect the result?','Yes, positional arrays are compared by index; sort them first if order is not significant.'),('Can it diff very large files?','It can, though extremely large documents may be slower to render.')]},

 {'slug':'json-to-csv','tool':'tools/it/json-to-csv.html','name':'JSON to CSV',
  'desc':'JSON to CSV guide: flatten an array of objects into a CSV table for spreadsheets and data tools.',
  'intro':'JSON to CSV converts a JSON array of objects into a CSV spreadsheet. It auto-detects columns from keys and is the bridge between APIs (JSON) and spreadsheets (CSV).',
  'features':['Array of objects to rows and columns','Header row from object keys','Nested values flattened or joined','Handles missing fields gracefully','Download as .csv','Browser-only'],
  'scenarios':['Export an API list into Excel','Turn a query result into a shareable table','Feed JSON into a tool that only reads CSV','Quick reporting from raw data'],
  'steps':['Paste a JSON array of objects','Review the detected columns','Adjust flattening if needed','Convert and download the CSV'],
  'tips':['All objects should share the same key set for a clean table','Deeply nested fields are flattened with dot paths','Open the CSV in a spreadsheet to verify encoding'],
  'faqs':[('What if objects have different keys?','Columns are the union of all keys; missing values become empty cells.'),('How are nested objects handled?','They are flattened using dot notation unless you choose to join them.')]},

 {'slug':'json-to-yaml','tool':'tools/it/json-to-yaml.html','name':'JSON to YAML',
  'desc':'JSON to YAML guide: convert JSON into readable YAML for Kubernetes, CI and config files.',
  'intro':'JSON to YAML turns JSON into YAML, the human-friendly markup used by Kubernetes, CI pipelines and many configuration systems. It preserves the exact data structure while improving readability.',
  'features':['Lossless JSON to YAML conversion','Configurable indentation','Preserves types (numbers, booleans, null)','Copy or download the YAML','Local conversion'],
  'scenarios':['Author a Kubernetes manifest from API data','Write a CI config from a JSON spec','Make a config file easier to review','Migrate between formats safely'],
  'steps':['Paste your JSON','Set the desired indentation','Convert to YAML','Copy or download the result'],
  'tips':['YAML is indentation-sensitive; keep it consistent','Quote strings that look like numbers if needed','Validate the YAML in its target system after conversion'],
  'faqs':[('Is the conversion lossless?','Yes, the data structure is preserved exactly.'),('Why does my number become a string?','Only if the source quoted it; ensure numeric types are unquoted in JSON.')]},

 {'slug':'jwt-debugger','tool':'tools/it/jwt-debugger.html','name':'JWT Debugger',
  'desc':'JWT Debugger guide: decode, inspect and verify JSON Web Tokens (header, payload, signature) entirely in the browser.',
  'intro':'The JWT Debugger decodes a JSON Web Token into its header, payload and signature parts so you can inspect claims, expiry and algorithm. It helps you debug auth flows without sending tokens to a server.',
  'features':['Split a JWT into header, payload, signature','Read standard claims like sub, exp, iat','Show human-readable expiry time','Verify signature with your secret or public key','Highlight expired tokens','Client-side, tokens never leave the browser'],
  'scenarios':['Inspect a token returned by your login API','Check why a request is rejected as unauthorized','Debug expiry and clock-skew issues','Teach how JWT structure works'],
  'steps':['Paste the JWT string','Read the decoded header and payload','Check exp and other claims','Optionally paste a secret or key to verify the signature','Note whether the token is expired'],
  'tips':[('Never paste production secrets into untrusted tools; this one runs locally'),('exp is in seconds since epoch; compare with current time'),('alg none and weak HS256 are common pitfalls to watch')],
  'faqs':[('Is it safe to paste a token here?','The tool runs in your browser and does not upload the token, but avoid pasting secrets you do not control.'),('Does it verify the signature?','Yes, if you provide the correct secret or public key; otherwise it only decodes.')]},

 {'slug':'qrcode','tool':'tools/it/qrcode.html','name':'QR Code Generator',
  'desc':'QR Code Generator guide: create scannable QR codes from text, URLs or contact data with adjustable size and error correction.',
  'intro':'The QR Code Generator turns any text, link or structured data into a downloadable QR code. It is useful for sharing URLs, Wi-Fi credentials and contact cards without typing.',
  'features':['Encode URL, text, email, phone or Wi-Fi','Adjustable size and margin','Error-correction levels (L/M/Q/H)','Download as PNG or SVG','Bulk or batch encoding','Fully local'],
  'scenarios':['Print a QR for a product page','Share Wi-Fi without revealing the password','Add a code to a poster or badge','Encode a vCard for quick contact save'],
  'steps':['Choose the content type','Enter the text or URL','Pick size and error correction','Generate the code','Download or copy it'],
  'tips':['Higher error correction survives dirty or small prints','Keep URLs short for faster scans','Test the code with a real phone before publishing'],
  'faqs':[('Which error-correction level should I use?','H for print, M for screens; higher levels tolerate damage but store less.'),('What can a QR encode?','Text, URLs, email, phone, Wi-Fi and contact cards, among others.')]},

 {'slug':'regex-tester','tool':'tools/it/regex-tester.html','name':'Regex Tester',
  'desc':'Regex Tester guide: build and debug regular expressions with live match highlighting, groups and flags.',
  'intro':'The Regex Tester lets you write a regular expression and see matches against your sample text in real time. It highlights captures, named groups and explains why a pattern matches or fails.',
  'features':['Live match highlighting','Capture and named groups','Common flags (g, i, m, s)','Explain mode for pattern breakdown','Replace preview','No server involved'],
  'scenarios':['Extract emails or IDs from a log','Validate an input format','Build a find-and-replace pattern','Learn how a tricky pattern behaves'],
  'steps':['Paste your sample text','Write the regular expression','Toggle flags as needed','Read the highlighted matches and groups','Use the replace view to preview changes'],
  'tips':['Start simple and add constraints gradually','Use non-capturing groups (?:...) to reduce noise','Test edge cases like empty strings and unicode'],
  'faqs':[('What does the g flag do?','It returns all matches instead of stopping at the first.'),('Why does my pattern match too much?','A greedy quantifier may over-match; try a lazy one or a tighter character class.')]},

 {'slug':'url-encode','tool':'tools/it/url-encode.html','name':'URL Encode / Decode',
  'desc':'URL Encode guide: percent-encode and decode URL components safely for queries and paths.',
  'intro':'URL Encode converts unsafe characters into percent-encoded form so they travel correctly in links and queries. Decode reverses it. Both run locally and follow standard encoding rules.',
  'features':['Encode and decode directions','Component versus full-URL modes','Preserve or encode reserved characters as needed','One-click copy','Browser-only'],
  'scenarios':['Put a space or symbol inside a query parameter','Fix a link that breaks on special characters','Prepare a value for a form submission','Debug a malformed URL'],
  'steps':['Paste the text or URL','Choose encode or decode','Pick the scope (component or full)','Convert and copy the result'],
  'tips':['Encode parameter values, not the whole well-formed URL blindly','Plus signs and spaces need care in query strings','Decode before logging to read the real value'],
  'faqs':[('Encode or decode?','Encode to send safely; decode to read what was sent.'),('Why does a space become plus or percent?','Both are valid in queries; the context decides which to use.')]},

 {'slug':'hash-multi','tool':'tools/it/hash-multi.html','name':'Multi Hash',
  'desc':'Multi Hash guide: compute MD5, SHA-1, SHA-256, SHA-512 and more for text or files at once.',
  'intro':'Multi Hash calculates several cryptographic digests (MD5, SHA-1, SHA-256, SHA-512 and others) for the same input simultaneously. It is handy for integrity checks, fingerprinting and learning how hashes differ.',
  'features':['Many algorithms in one run','Text and file input','Drag-and-drop file hashing','Show hex and base64 digests','Local computation, no upload'],
  'scenarios':['Verify a downloaded file against a published checksum','Fingerprint a string for deduplication','Compare algorithm outputs for teaching','Detect accidental changes'],
  'steps':['Enter text or drop a file','Select the algorithms you need','Compute and read the digests','Copy the one you need'],
  'tips':['Use SHA-256 or stronger for security; MD5 and SHA-1 are broken for collisions','Recompute after any change to confirm integrity','Hashes are one-way; you cannot recover the input'],
  'faqs':[('Which hash is secure?','SHA-256 or SHA-512 for security; avoid MD5 and SHA-1 for protection.'),('Can I recover the input from a hash?','No, cryptographic hashes are one-way by design.')]},

 {'slug':'password-generator','tool':'tools/it/password-generator.html','name':'Password Generator',
  'desc':'Password Generator guide: create strong random passwords and passphrases with custom length and character sets.',
  'intro':'The Password Generator creates high-entropy credentials from a secure random source. You control length, character classes and exclusion rules so the output fits any policy.',
  'features':['Adjustable length','Toggle upper, lower, digits, symbols','Exclude ambiguous characters','Passphrase mode with word lists','Copy without storing','Local randomness'],
  'scenarios':['Create a new account password','Generate a one-time credential','Produce a memorable passphrase','Meet a strict company policy'],
  'steps':['Set the length','Choose which character sets to include','Exclude ambiguous characters if needed','Generate and copy the password'],
  'tips':['Longer is better than complex symbols alone','Use a password manager instead of memorizing','Prefer passphrases for things you type often'],
  'faqs':[('How long should it be?','At least 12 to 16 characters for important accounts.'),('Is it saved anywhere?','No, generation happens in your browser and nothing is stored.')]},

 {'slug':'uuid-generator','tool':'tools/it/uuid-generator.html','name':'UUID Generator',
  'desc':'UUID Generator guide: generate RFC 4122 v4 UUIDs in bulk for identifiers, keys and test data.',
  'intro':'The UUID Generator produces random (v4) UUIDs that are extremely unlikely to collide. They are ideal as database primary keys, request IDs and placeholders in tests.',
  'features':['Generate many UUIDs at once','RFC 4122 version 4','Uppercase or lowercase','Copy as list or comma-separated','No network needed'],
  'scenarios':['Create primary keys for new records','Tag requests and events with unique IDs','Seed test fixtures with stable-looking identifiers','Avoid predictable sequential IDs'],
  'steps':['Choose how many UUIDs you need','Pick the format options','Generate','Copy the list'],
  'tips':['Use v4 for randomness; v1 leaks a timestamp and MAC','Bulk generate then paste into your schema','UUIDs are large; use them where uniqueness matters more than size'],
  'faqs':[('v4 versus v1?','v4 is random and privacy-friendly; v1 embeds time and hardware info.'),('Can two UUIDs collide?','The chance is astronomically low for v4.')]},

 {'slug':'timestamp-converter','tool':'tools/it/timestamp-converter.html','name':'Timestamp Converter',
  'desc':'Timestamp Converter guide: convert Unix epoch to human date and back, across time zones.',
  'intro':'The Timestamp Converter switches between Unix epoch seconds and readable dates, and shows the value in multiple time zones. It is the quickest way to debug log times and API timestamps.',
  'features':['Epoch to date and date to epoch','Seconds and milliseconds','Multiple time zones at once','Current time helper','Local only'],
  'scenarios':['Read a timestamp from a server log','Convert a date into epoch for an API','Compare times across regions','Debug off-by-1000 (seconds vs ms) bugs'],
  'steps':['Enter an epoch or a date','Choose seconds or milliseconds','See the converted value and time zones','Copy what you need'],
  'tips':['Check whether the source uses seconds or milliseconds','Time zones change the wall-clock but not the instant','Use UTC to avoid daylight-saving confusion'],
  'faqs':[('Seconds or milliseconds?','Many systems use seconds; JavaScript uses milliseconds. Verify the source.'),('Why does the date look wrong?','Usually a time-zone or unit (s vs ms) mismatch.')]},

 {'slug':'number-base-converter','tool':'tools/it/number-base-converter.html','name':'Number Base Converter',
  'desc':'Number Base Converter guide: convert between binary, octal, decimal and hexadecimal with bit views.',
  'intro':'The Number Base Converter translates integers between binary, octal, decimal and hexadecimal. It is useful for programming, networking and understanding how computers represent values.',
  'features':['Binary, octal, decimal, hex','Instant conversion as you type','Show two-complement for negatives','Bit-length view','No upload'],
  'scenarios':['Read a color value in hex','Convert a subnet mask to binary','Translate a permission bitmask','Learn base arithmetic'],
  'steps':['Enter a number in any base','See all other bases at once','Adjust bit length if needed','Copy the target value'],
  'tips':['Hex pairs map cleanly to bytes (00 to FF)','Watch sign handling for negative numbers','Leading zeros do not change the value'],
  'faqs':[('Why does hex matter?','It compacts binary and matches how bytes and memory are shown.'),('How are negatives handled?','Using two-complement with the chosen bit length.')]},
]

TPL = """<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - ToolBox</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="ToolBox">
<meta property="og:url" content="{canonical}">
<meta property="og:description" content="{desc}">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://chenguangwu.github.io/og-image.png">
<meta name="twitter:image:alt" content="ToolBox - Free Online Tools & Guides">
<meta property="og:image" content="https://chenguangwu.github.io/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="ToolBox - Free Online Tools & Guides">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="zh-CN" href="{zh_url}">
<link rel="alternate" hreflang="en-US" href="{canonical}">
<link rel="alternate" hreflang="x-default" href="{zh_url}">
<script type="application/ld+json">{article_json}</script>
<script type="application/ld+json">{breadcrumb_json}</script>
<script type="application/ld+json">{faq_json}</script>
<style>
:root{--primary:#FF6B35;--text:#1F2937;--muted:#6B7280;--border:#E5E7EB;--bg:#FFFAF7;}
*{box-sizing:border-box;}
body{margin:0;font-family:"Plus Jakarta Sans","Noto Sans SC",system-ui,sans-serif;color:var(--text);background:var(--bg);line-height:1.75;}
.breadcrumb a{color:var(--primary);text-decoration:none;margin-right:6px;}
.breadcrumb a:hover{text-decoration:underline;}
main{max-width:820px;margin:0 auto;padding:28px 20px 60px;}
h1{font-size:28px;margin:0 0 8px;}
.lead{font-size:16px;color:var(--muted);margin:0 0 22px;}
h2{font-size:20px;margin:28px 0 10px;color:var(--primary);}
.toc{background:#fff;border:1px solid var(--border);border-radius:14px;padding:14px 18px;margin:18px 0;}
.toc ul{margin:0;padding-left:20px;}
.toc a{color:var(--text);text-decoration:none;}
.toc a:hover{color:var(--primary);}
ul,ol{padding-left:22px;}
li{margin:8px 0;}
.related{margin-top:26px;padding:16px;background:#fff;border:1px solid var(--border);border-radius:14px;}
.related h3{margin:0 0 10px;font-size:16px;color:var(--text);}
.tool-chip{display:inline-block;margin:4px 6px 4px 0;padding:6px 12px;border:1px solid var(--border);border-radius:999px;color:var(--primary);text-decoration:none;font-size:14px;}
.tool-chip:hover{background:var(--primary);color:#fff;}
.faq{margin-top:26px;}
.faq dt{font-weight:700;margin-top:14px;}
.faq dd{margin:4px 0 0;color:var(--muted);}
.back{margin-top:30px;padding:16px;background:#fff;border:1px solid var(--border);border-radius:14px;}
.back a{color:var(--primary);font-weight:700;text-decoration:none;}
</style>
<script src="/js/analytics.js" defer></script>
<link rel="stylesheet" href="../css/common.css">
<script src="../js/common.js" defer></script>
</head>
<body>
<nav class="breadcrumb"><a href="https://chenguangwu.github.io/">ToolBox</a> / <a href="https://chenguangwu.github.io/guides/index.html">Guides</a> / <span>{title}</span></nav>
<main>
<h1>{title}</h1>
<p class="lead">{intro}</p>
<div class="toc"><strong>Contents</strong><ul><li><a href="#s0">Key Features</a></li><li><a href="#s1">Use Cases</a></li><li><a href="#s2">How to Use</a></li><li><a href="#s3">Practical Tips</a></li><li><a href="#s4">FAQ</a></li></ul></div>
<h2 id="s0">Key Features</h2>
<ul>{features}</ul>
<h2 id="s1">Use Cases</h2>
<ul>{scenarios}</ul>
<h2 id="s2">How to Use</h2>
<ol>{steps}</ol>
<h2 id="s3">Practical Tips</h2>
<ul>{tips}</ul>
<div class="related"><h3>Related Tool</h3>{related_chips}</div>
<div class="faq"><h2 id="s4">FAQ</h2><dl>{faqs}</dl></div>
<div class="back"><a href="https://chenguangwu.github.io/guides/index.html">&larr; Back to Guides</a></div>
</main>
</body>
</html>"""


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            .replace('"', '&quot;'))


def li(items):
    return '\n'.join('<li>%s</li>' % esc(x) for x in items)


def faq_dl(items):
    out = []
    for q, a in items:
        out.append('<dt>%s</dt>' % esc(q))
        out.append('<dd>%s</dd>' % esc(a))
    return '\n'.join(out)


def inject_en_link():
    """给中文指南注入「🌐 English」芯片（幂等）。it/ 模板无 .related/.faq，降级到 </nav> 后插入。"""
    for g in EN:
        slug = g['slug']
        zh = os.path.join(GUIDES_DIR, '%s-guide.html' % slug)
        if not os.path.exists(zh):
            print('  ! 中文指南缺失，跳过:', slug)
            continue
        html = io.open(zh, encoding='utf-8').read()
        if 'data-en-guide-link' in html:
            continue
        en_href = '%s-guide.en.html' % slug
        chip = '<p class="back"><a href="%s" data-en-guide-link>&#127760; English</a></p>' % en_href
        m = re.search(r'(<div class="related">.*?</div>)\s*(<div class="faq">)', html, re.S)
        if m:
            new = m.group(1)[:-6] + chip + '</div>'
            html = html[:m.start()] + new + m.group(2) + html[m.end():]
        elif '</nav>' in html:
            html = html.replace('</nav>', '</nav>\n' + chip, 1)
        else:
            print('  ! 无注入锚点:', slug)
            continue
        io.open(zh, 'w', encoding='utf-8').write(html)
        print('  OK 注入英文芯片:', slug)


def main():
    n = 0
    for g in EN:
        slug = g['slug']
        tool = g['tool']
        title = g['name']
        canonical = 'https://chenguangwu.github.io/guides/%s-guide.en.html' % slug
        zh_url = 'https://chenguangwu.github.io/guides/%s-guide.html' % slug
        article_json = json.dumps({
            '@context': 'https://schema.org', '@type': 'Article',
            'inLanguage': 'en-US', 'headline': title,
            'description': g['desc'],
            'author': {'@type': 'Organization', 'name': 'ToolBox'},
            'datePublished': '2026-09-02', 'dateModified': '2026-09-02',
            'mainEntityOfPage': {'@type': 'WebPage', '@id': canonical}
        }, ensure_ascii=False)
        breadcrumb_json = json.dumps({
            '@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'ToolBox',
                 'item': 'https://chenguangwu.github.io/'},
                {'@type': 'ListItem', 'position': 2, 'name': 'Guides',
                 'item': 'https://chenguangwu.github.io/guides/index.html'},
                {'@type': 'ListItem', 'position': 3, 'name': title,
                 'item': canonical}]}, ensure_ascii=False)
        faq_json = json.dumps({
            '@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': q,
                            'acceptedAnswer': {'@type': 'Answer', 'text': a}}
                           for q, a in g['faqs']]}, ensure_ascii=False)
        related_chips = ('<a class="tool-chip" href="https://chenguangwu.github.io/%s?lang=en">%s &rarr;</a>'
                         '<a class="tool-chip" href="%s">&#127760; &#20013;&#25991;</a>' % (tool, esc(title), zh_url))
        html = (TPL
                .replace('{title}', esc(title))
                .replace('{desc}', esc(g['desc']))
                .replace('{canonical}', canonical)
                .replace('{zh_url}', zh_url)
                .replace('{intro}', esc(g['intro']))
                .replace('{features}', li(g['features']))
                .replace('{scenarios}', li(g['scenarios']))
                .replace('{steps}', li(g['steps']))
                .replace('{tips}', li(g['tips']))
                .replace('{faqs}', faq_dl(g['faqs']))
                .replace('{related_chips}', related_chips)
                .replace('{article_json}', article_json)
                .replace('{breadcrumb_json}', breadcrumb_json)
                .replace('{faq_json}', faq_json))
        out = os.path.join(GUIDES_DIR, '%s-guide.en.html' % slug)
        io.open(out, 'w', encoding='utf-8').write(html)
        n += 1
        print('  OK: guides/%s-guide.en.html' % slug)
    print('英文指南生成完成：%d 篇' % n)
    print('--- 反向注入：中文指南 -> 英文芯片 ---')
    inject_en_link()


if __name__ == '__main__':
    main()

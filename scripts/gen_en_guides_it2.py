#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 it/ 开发者工具集群【第二批 69 篇】英文使用指南 guides/<slug>-guide.en.html。

沿用 A 策略（独立 .en.html 静态页），与第一批 15 篇 + 19 篇 V2 英文指南一致、对 SEO 收录最稳。
_build.py 已能自动识别 .en.html 兄弟页并把 sitemap hreflang 切到文件级（非 ?lang=en）。
内容据各工具实际功能撰写，非机翻套话。
"""
import json, io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDES_DIR = os.path.join(ROOT, 'guides')

EN = [
 {'slug':'aes-encryptor','tool':'tools/it/aes-encryptor.html','name':'AES Encrypt / Decrypt',
  'desc':'AES guide: encrypt and decrypt text and files with AES-256 in CBC/GCM modes, all in your browser.',
  'intro':'The AES Encrypt / Decrypt tool protects data with the Advanced Encryption Standard. It runs locally, so your plaintext and key never leave the browser. Use it to secure notes, config snippets or small files before sharing.',
  'features':['AES-256 with CBC and GCM modes','Password-based key derivation','Encrypt text or files','Base64 or hex output','No upload, fully local'],
  'scenarios':['Secure a private note before sending','Encrypt a config file for storage','Demo AES to students','Verify a cipher you produced elsewhere'],
  'steps':['Pick encrypt or decrypt','Choose the mode and enter a passphrase','Paste the text or pick a file','Read the ciphertext output'],
  'tips':['GCM also provides integrity, not just confidentiality','Use a long random passphrase, not a word','Lost keys are unrecoverable by design'],
  'faqs':[('Is my data uploaded?','No, all cryptography happens in your browser.'),('Which mode should I use?','GCM for new work; CBC only for compatibility.')]},

 {'slug':'api-sign-generator','tool':'tools/it/api-sign-generator.html','name':'API Signature Generator',
  'desc':'API Signature guide: build HMAC-SHA signed requests for AWS, Alibaba Cloud and custom APIs.',
  'intro':'The API Signature Generator builds the signature your backend expects. It supports common schemes such as HMAC-SHA256 over a canonical string, helping you debug auth errors without reading vendor SDKs.',
  'features':['HMAC-SHA1/256/512 signatures','Configurable secret and nonce','Shows the signed string','Multiple preset schemes','Local only'],
  'scenarios':['Debug a 401 from a signed API','Reproduce a server-side signature','Teach API signing','Test webhook authenticity'],
  'steps':['Select the signing scheme','Enter the secret and the payload','Adjust the canonical format','Copy the resulting signature'],
  'tips':['Whitespace and ordering in the canonical string matter','Keep secrets out of logs and commits','Verify the server uses the same hash'],
  'faqs':[('HMAC vs raw hash?','HMAC keys the hash so it cannot be forged without the secret.'),('Why do signatures mismatch?','Usually a trailing newline or different param order.')]},

 {'slug':'base32-encode','tool':'tools/it/base32-encode.html','name':'Base32 Encode / Decode',
  'desc':'Base32 guide: encode and decode Base32 (RFC 4648) for case-insensitive, human-friendly transport.',
  'intro':'Base32 uses an A-Z and 2-7 alphabet so output is safe in case-insensitive systems and easy to read aloud. This tool converts text or hex to and from Base32 without uploading anything.',
  'features':['RFC 4648 Base32 and Base32Hex','Text and hex input','Strict or lenient decoding','Show the padding','Fully local'],
  'scenarios':['Share a key that survives case changes','Encode a secret for DNS or labels','Decode a token from a system','Teach encoding basics'],
  'steps':['Paste the text or hex','Choose the variant','Convert','Copy the result'],
  'tips':['Base32 is larger than Base64 but safer in email','Watch the padding equals signs','Base32Hex uses 0-9 and A-V'],
  'faqs':[('Base32 vs Base64?','Base32 avoids ambiguous characters; Base64 is more compact.'),('Why the padding?','It aligns the last group to a multiple of 8 bits.')]},

 {'slug':'base58-encode','tool':'tools/it/base58-encode.html','name':'Base58 Encode / Decode',
  'desc':'Base58 guide: encode and decode Base58 used by Bitcoin and IPFS addresses.',
  'intro':'Base58 drops easily-confused characters (0, O, I, l) so addresses are less error-prone. This tool converts between bytes and Base58, the encoding behind Bitcoin and IPFS identifiers.',
  'features':['Bitcoin Base58 alphabet','Text and hex input','Checksum-aware display','Decode back to bytes','Local only'],
  'scenarios':['Convert a hash to a wallet-style string','Decode an IPFS-style id','Verify address encoding','Teach cryptocurrency addressing'],
  'steps':['Paste the data or hex','Encode or decode','Copy the Base58 string'],
  'tips':['Base58 is not the same as Base58Check','No padding characters are used','Double-check copied addresses'],
  'faqs':[('Why no 0 and O?','To prevent visual confusion in handwritten or printed addresses.'),('Base58Check?','Adds a checksum prefix; this tool handles raw Base58.')]},

 {'slug':'base85-encode','tool':'tools/it/base85-encode.html','name':'Base85 Encode / Decode',
  'desc':'Base85 guide: encode and decode Base85 (Ascii85 / RFC 1924) for compact binary transport.',
  'intro':'Base85 packs four bytes into five characters, making it more compact than Base64. This tool supports common variants such as Ascii85 and the IPv6 RFC 1924 form.',
  'features':['Ascii85 and RFC 1924 variants','Binary, text or hex input','Configurable delimiter','Decode back','Fully local'],
  'scenarios':['Embed binary in PostScript or PDF','Encode an IPv6 address compactly','Shrink data for transport','Compare encoding efficiency'],
  'steps':['Choose the variant','Paste the input','Convert','Copy the output'],
  'tips':['Ascii85 often wraps output in <~ ~>','It is denser than Base64 but less universal','Watch for variant-specific delimiters'],
  'faqs':[('When use Base85?','When you need denser encoding than Base64 in a compatible system.'),('Is it safe?','It is encoding, not encryption; data is not secret.')]},

 {'slug':'basic-auth-generator','tool':'tools/it/basic-auth-generator.html','name':'Basic Auth Header Generator',
  'desc':'Basic Auth guide: build the Authorization header for HTTP Basic authentication.',
  'intro':'The Basic Auth Generator turns a username and password into the Base64 value used in the HTTP Authorization header. It is handy when testing APIs or configuring reverse proxies.',
  'features':['Builds the Authorization header','Base64 with proper encoding','Copy-ready curl snippet','No upload','Local only'],
  'scenarios':['Test an endpoint that needs Basic auth','Build a header for a proxy','Teach HTTP auth','Debug a 401 response'],
  'steps':['Enter the username and password','Copy the generated header','Use it in curl or your client'],
  'tips':['Basic auth sends credentials on every request; use HTTPS','Prefer tokens for new systems','Never log the full header'],
  'faqs':[('Is Basic auth secure?','Only over TLS; otherwise credentials are trivially decoded.'),('Why Base64?','It makes arbitrary bytes safe to place in a header.')]},

 {'slug':'bcrypt','tool':'tools/it/bcrypt.html','name':'Bcrypt Hash Generator',
  'desc':'Bcrypt guide: hash and verify passwords with bcrypt, the adaptive password hashing function.',
  'intro':'Bcrypt is designed to be slow, which slows down brute-force attacks. This tool hashes a password with a configurable cost factor and can verify a hash, all in your browser.',
  'features':['Adjustable cost factor','Generates a salt automatically','Verify a hash against a password','Shows the full hash format','Local only'],
  'scenarios':['Hash a password before storing it','Verify a stored bcrypt hash','Pick a sensible cost','Teach password hashing'],
  'steps':['Enter the password','Set the cost factor','Generate the hash','Copy or verify it'],
  'tips':['Higher cost means slower logins and harder cracking','Never roll your own crypto primitives','Store the whole hash, salt included'],
  'faqs':[('What cost should I use?','As high as your servers can afford, often 10 to 12.'),('Bcrypt vs Argon2?','Argon2 is newer; bcrypt is still widely supported.')]},

 {'slug':'bip39-generator','tool':'tools/it/bip39-generator.html','name':'BIP39 Mnemonic Generator',
  'desc':'BIP39 guide: generate and validate BIP39 seed phrases for cryptocurrency wallets.',
  'intro':'BIP39 turns entropy into a list of words that backs up a wallet. This tool generates mnemonics, derives a seed, and validates phrases, all locally for offline safety.',
  'features':['12, 18 or 24 word phrases','Multiple languages','Seed derivation preview','Validates checksum','Offline capable'],
  'scenarios':['Create a wallet backup phrase','Recover a wallet from words','Validate a phrase before import','Teach seed mechanics'],
  'steps':['Choose the word count and language','Generate or enter the phrase','Check the checksum','Derive the seed if needed'],
  'tips':['Never share a live mnemonic online','Write it on paper, not in cloud notes','The checksum prevents typos'],
  'faqs':[('Is this a wallet?','No, it only produces and checks the phrase; store funds separately.'),('Why 24 words?','More entropy means a stronger backup.')]},

 {'slug':'bitwise-calculator','tool':'tools/it/bitwise-calculator.html','name':'Bitwise Calculator',
  'desc':'Bitwise guide: compute AND, OR, XOR, NOT and shifts for integers in decimal, hex or binary.',
  'intro':'The Bitwise Calculator applies logic operations and shifts to integers, showing results in binary, decimal and hex. It is useful for masks, flags and low-level debugging.',
  'features':['AND, OR, XOR, NOT, shifts','Binary, decimal, hex input','Live bit view','Multi-operand support','Local only'],
  'scenarios':['Build a permission bitmask','Flip specific bits','Debug a flags field','Teach binary logic'],
  'steps':['Enter the values in any base','Pick the operation','See the result in every base'],
  'tips':['XOR with all ones is a bitwise NOT for fixed width','Shifts multiply or divide by two','Use hex for byte-aligned work'],
  'faqs':[('Why bitwise?','It is the fastest way to manipulate individual bits.'),('Signed shifts?','This tool treats values as unsigned integers.')]},

 {'slug':'box-shadow-generator','tool':'tools/it/box-shadow-generator.html','name':'Box Shadow Generator',
  'desc':'Box Shadow guide: build CSS box-shadow values visually with inset, blur and spread.',
  'intro':'The Box Shadow Generator produces the CSS box-shadow property from sliders for offset, blur, spread, color and inset. Copy the snippet straight into your stylesheet.',
  'features':['Offset, blur, spread sliders','Inset toggle','Color with alpha','Multi-layer shadows','Copy CSS'],
  'scenarios':['Design a card lift effect','Add depth to a button','Create a soft glow','Teach CSS shadows'],
  'steps':['Adjust the sliders','Toggle inset if needed','Copy the generated CSS'],
  'tips':['Large blur with zero spread looks soft','Inset flips the shadow inward','Subtle shadows read as more premium'],
  'faqs':[('box-shadow vs filter drop-shadow?','box-shadow follows the border box; drop-shadow follows the alpha.'),('Why no shadow on print?','Shadows are visual only and often omitted by printers.')]},

 {'slug':'case-converter','tool':'tools/it/case-converter.html','name':'Case Converter',
  'desc':'Case Converter guide: switch text between camelCase, snake_case, kebab-case, PascalCase and more.',
  'intro':'The Case Converter normalizes identifiers and headings across programming conventions. Paste a string and get every common casing variant at once.',
  'features':['camelCase, PascalCase, snake_case, kebab-case','UPPER, lower, Title Case','Handles spaces and punctuation','Bulk lines','Local only'],
  'scenarios':['Rename a variable across conventions','Normalize CSV column names','Title a document','Teach naming styles'],
  'steps':['Paste the text','See all variants','Copy the one you need'],
  'tips':['Acronyms break simple rules; review output','snake_case is common in Python','kebab-case is safest in URLs'],
  'faqs':[('Which case for JSON?','camelCase is the common convention.'),('Does it translate?','No, it only changes casing, not language.')]},

 {'slug':'chmod-calculator','tool':'tools/it/chmod-calculator.html','name':'Chmod Calculator',
  'desc':'Chmod guide: compute Linux file permissions in symbolic and numeric (octal) form.',
  'intro':'The Chmod Calculator translates between symbolic notation like rwxr-xr-- and the numeric 754 form. Toggle bits for owner, group and others to build a safe permission set.',
  'features':['Symbolic and octal views','Per-role read, write, execute','Special bits (setuid, setgid, sticky)','Common presets','Local only'],
  'scenarios':['Set a web file to 644','Make a script executable','Lock down a private key','Teach Unix permissions'],
  'steps':['Toggle the bits for each role','Read the octal value','Apply with chmod'],
  'tips':['755 for executables, 644 for files','700 keeps a directory private','Avoid 777 unless you mean it'],
  'faqs':[('What is 644?','Owner read/write, everyone else read only.'),('Sticky bit?','Keeps users from deleting others files in a shared dir.')]},

 {'slug':'color-converter','tool':'tools/it/color-converter.html','name':'Color Converter',
  'desc':'Color Converter guide: convert between HEX, RGB, HSL, HSV and CMYK with a live preview.',
  'intro':'The Color Converter translates color values across formats designers and developers use, showing a swatch so you can confirm the result visually.',
  'features':['HEX, RGB, HSL, HSV, CMYK','Live swatch preview','Copy any format','Alpha support','Local only'],
  'scenarios':['Match a brand color in CSS','Convert a design token','Pick a readable contrast','Teach color models'],
  'steps':['Enter a color in any format','See all equivalents','Copy what you need'],
  'tips':['HSL is easier for lightness tweaks','CMYK is for print, not screens','Check contrast for text'],
  'faqs':[('RGB vs HSL?','HSL separates hue from lightness, easier to adjust.'),('Why does CMYK look dull?','Print ink has a smaller gamut than screens.')]},

 {'slug':'crontab-generator','tool':'tools/it/crontab-generator.html','name':'Crontab Generator',
  'desc':'Crontab guide: build and explain cron schedule expressions for cron jobs.',
  'intro':'The Crontab Generator turns a human description into a five-field cron expression and explains what each field means, reducing the chance of a job firing at the wrong time.',
  'features':['Five-field cron builder','Plain-English explanation','Common presets','Validate the expression','Local only'],
  'scenarios':['Schedule a nightly backup','Run a report every weekday','Trigger a cleanup monthly','Teach cron syntax'],
  'steps':['Set minute, hour, day, month and weekday','Read the explanation','Copy the line'],
  'tips':['Use a leading zero for single digits','*/15 means every 15 units','Test with a dry run first'],
  'faqs':[('What does * mean?','Any value for that field.'),('Why did it run at midnight?','Unset fields default to zero, not star.')]},

 {'slug':'css-minify','tool':'tools/it/css-minify.html','name':'CSS Minifier',
  'desc':'CSS Minifier guide: compress CSS by removing whitespace and comments for faster loads.',
  'intro':'The CSS Minifier shrinks stylesheets so they download and parse faster. It strips comments and redundant spaces while keeping the rules intact.',
  'features':['Removes comments and whitespace','Keeps selectors valid','Handles media queries','Large input supported','Local only'],
  'scenarios':['Shrink a production stylesheet','Compare before and after size','Teach build optimization','Prepare assets for CDN'],
  'steps':['Paste the CSS','Minify','Copy the smaller output'],
  'tips':['Keep the original for edits','Minify at build time, not by hand','Verify layout after minifying'],
  'faqs':[('Does minifying change behavior?','Only by removing safe whitespace and comments.'),('When to minify?','As the last step before deploying.')]},

 {'slug':'csv-to-json','tool':'tools/it/csv-to-json.html','name':'CSV to JSON Converter',
  'desc':'CSV to JSON guide: convert tabular CSV into JSON arrays or objects.',
  'intro':'The CSV to JSON tool turns spreadsheet rows into JSON you can feed to an API or script. It maps the header row to keys and handles quoting correctly.',
  'features':['Array of objects or array of arrays','Custom delimiter','Header row toggle','Handles quoted fields','Local only'],
  'scenarios':['Feed a CSV into an API','Import rows into a script','Preview structured data','Teach data formats'],
  'steps':['Paste the CSV','Choose the output shape','Convert and copy'],
  'tips':['Quote fields that contain commas','Pick the delimiter that matches your file','Check the header row is clean'],
  'faqs':[('Nested JSON?','Flat CSV maps to flat objects; nest afterward if needed.'),('Encoding?','UTF-8 is assumed; check accents render.')]},

 {'slug':'csv-validator','tool':'tools/it/csv-validator.html','name':'CSV Validator',
  'desc':'CSV Validator guide: check CSV files for well-formed rows, consistent columns and encoding.',
  'intro':'The CSV Validator parses a file and reports structural problems such as ragged rows, bad quoting or a missing header, before the data reaches your pipeline.',
  'features':['Detects ragged rows','Validates quoting','Reports line numbers','Encoding check','Local only'],
  'scenarios':['Sanity-check an export','Find the broken row in a big file','Teach CSV rules','Prepare data for import'],
  'steps':['Paste or upload the CSV','Read the diagnostics','Fix the flagged lines'],
  'tips':['Consistent column counts matter most','Quote fields with newlines','A header row eases mapping'],
  'faqs':[('Ragged rows?','Rows with a different column count than the header.'),('Why validate?','Bad CSV silently corrupts downstream imports.')]},

 {'slug':'curl-parser','tool':'tools/it/curl-parser.html','name':'curl Command Parser',
  'desc':'curl Parser guide: paste a curl command and inspect its method, headers, body and URL.',
  'intro':'The curl Parser breaks a copied curl snippet into its parts so you can reproduce a request in code or a different client. It is ideal when reading API docs or bug reports.',
  'features':['Extracts URL, method, headers, body','Shows query params','Detects auth headers','Pretty view','Local only'],
  'scenarios':['Reproduce a failing request','Port curl to a language','Inspect a captured call','Teach HTTP clients'],
  'steps':['Paste the curl command','Review the parsed fields','Copy what you need'],
  'tips':['Watch for -d vs --data-binary','Headers may carry auth tokens','Strip secrets before sharing'],
  'faqs':[('Does it run the request?','No, it only parses the command text.'),('Where is the body?','In -d or --data arguments.')]},

 {'slug':'date-duration','tool':'tools/it/date-duration.html','name':'Date Duration Calculator',
  'desc':'Date Duration guide: compute the span between two dates in days, weeks, months or years.',
  'intro':'The Date Duration Calculator finds how much time lies between two calendar dates, useful for project plans, ages and deadlines.',
  'features':['Day, week, month, year output','Inclusive or exclusive count','Add or subtract intervals','Time-of-day aware','Local only'],
  'scenarios':['Measure a project length','Calculate an age','Count days to a deadline','Teach date math'],
  'steps':['Enter the start and end dates','Choose the unit','Read the span'],
  'tips':['Decide whether to include both endpoints','Time zones change day boundaries','Leap years affect month math'],
  'faqs':[('Inclusive count?','Including both the start and end day adds one.'),('Why off by one?','Usually an inclusive versus exclusive choice.')]},

 {'slug':'docker-run-converter','tool':'tools/it/docker-run-converter.html','name':'docker run to Compose',
  'desc':'docker run Converter guide: turn a docker run command into a docker-compose.yml.',
  'intro':'The docker run Converter translates a long docker run invocation into a compose file, making multi-container setups easier to version and share.',
  'features':['Maps flags to compose keys','Ports, volumes, env preserved','Readable YAML output','Local only'],
  'scenarios':['Convert a one-liner to compose','Document a stack','Share a reproducible setup','Teach Docker'],
  'steps':['Paste the docker run command','Review the YAML','Copy it into compose'],
  'tips':['Named volumes beat host paths for portability','Map only the ports you need','Keep secrets out of the file'],
  'faqs':[('Does it run Docker?','No, it only converts the command text.'),('Why compose?','It is easier to manage and version than run flags.')]},

 {'slug':'dockerfile-generator','tool':'tools/it/dockerfile-generator.html','name':'Dockerfile Generator',
  'desc':'Dockerfile guide: scaffold a Dockerfile for common languages and web servers.',
  'intro':'The Dockerfile Generator builds a starting Dockerfile for Node, Python, Go and more, with sensible base images and layering so you can iterate quickly.',
  'features':['Language presets','Multi-stage templates','Expose and cmd set','Copy-optimized layers','Local only'],
  'scenarios':['Bootstrap a new service','Standardize a team template','Teach container basics','Reproduce a build'],
  'steps':['Pick the language and version','Choose single or multi-stage','Copy the Dockerfile'],
  'tips':['Multi-stage keeps images small','Order layers by change frequency','Pin base image tags'],
  'faqs':[('Multi-stage?','Builds in one image, ships a smaller runtime image.'),('Why small images?','Faster pulls and a smaller attack surface.')]},

 {'slug':'emoji-meaning','tool':'tools/it/emoji-meaning.html','name':'Emoji Meaning Lookup',
  'desc':'Emoji guide: look up the name, codepoint and meaning of any emoji.',
  'intro':'The Emoji Meaning tool resolves an emoji to its Unicode name and codepoint, helpful when you need the canonical label for accessibility or search.',
  'features':['Shows name and codepoint','Unicode version','Copy the escape sequence','Search by keyword','Local only'],
  'scenarios':['Find an emoji name for a label','Get the codepoint for CSS','Teach Unicode','Clarify a glyph'],
  'steps':['Paste or search the emoji','Read its metadata','Copy what you need'],
  'tips':['Some emoji are sequences of codepoints','Skin tones add variation selectors','Names help screen readers'],
  'faqs':[('Codepoint?','The hexadecimal Unicode value of the character.'),('Why two codepoints?','Some emoji combine a base and a modifier.')]},

 {'slug':'gitignore-generator','tool':'tools/it/gitignore-generator.html','name':'.gitignore Generator',
  'desc':'.gitignore guide: build a .gitignore file for languages, frameworks and editors.',
  'intro':'The .gitignore Generator composes ignore rules for your stack so build output and secrets stay out of version control.',
  'features':['Language and framework presets','Editor and OS rules','Merge multiple sets','Preview the file','Local only'],
  'scenarios':['Scaffold a new repo','Add Node or Python ignores','Exclude IDE folders','Teach VCS hygiene'],
  'steps':['Pick your stacks','Merge the rules','Copy the .gitignore'],
  'tips':['Ignore secrets, never commit them','Add build dirs, not source','Review before first commit'],
  'faqs':[('Already tracked?','gitignore does not untrack files; use git rm --cached.'),('Why ignore?','Keeps the repo lean and avoids leaking artifacts.')]},

 {'slug':'hash-identifier','tool':'tools/it/hash-identifier.html','name':'Hash Identifier',
  'desc':'Hash Identifier guide: guess the algorithm behind an unknown hash string.',
  'intro':'The Hash Identifier inspects a hash\'s length and character set to suggest which algorithm produced it, speeding up forensic and debugging work.',
  'features':['Detects MD5, SHA families, bcrypt, etc.','Length and charset analysis','Confidence hints','Local only'],
  'scenarios':['Identify a stored password hash','Classify unknown data','Teach hash formats','Triage a breach dump'],
  'steps':['Paste the hash','Read the candidates','Confirm by context'],
  'tips':['Length is a strong clue but not proof','bcrypt starts with $2','Never trust identification alone'],
  'faqs':[('Certain?','It suggests; context confirms.'),('Why identify?','To pick the right verification method.')]},

 {'slug':'hmac-generator','tool':'tools/it/hmac-generator.html','name':'HMAC Generator',
  'desc':'HMAC guide: create keyed hashes with HMAC-SHA for message authentication.',
  'intro':'The HMAC Generator produces a keyed MAC so a receiver can verify both integrity and authenticity of a message using a shared secret.',
  'features':['HMAC-SHA1/256/512','Text or hex secret','Base64 or hex output','Verify a tag','Local only'],
  'scenarios':['Sign a webhook payload','Verify an API request','Teach MACs','Detect tampering'],
  'steps':['Enter the key and message','Pick the hash','Generate or verify the tag'],
  'tips':['Share the secret securely out of band','Rotate keys periodically','Use SHA-256 or stronger'],
  'faqs':[('HMAC vs signature?','HMAC uses symmetric secrets; signatures use keypairs.'),('Why not plain hash?','A plain hash cannot prove who sent it.')]},

 {'slug':'html-entity-encoder','tool':'tools/it/html-entity-encoder.html','name':'HTML Entity Encoder',
  'desc':'HTML Entity guide: encode and decode HTML entities and numeric character references.',
  'intro':'The HTML Entity Encoder converts special characters to entities so they render safely in markup, and decodes entities back to text.',
  'features':['Named and numeric entities','Encode or decode','Handle attributes and text','Local only'],
  'scenarios':['Escape user input for display','Decode a copied snippet','Teach HTML escaping','Fix broken characters'],
  'steps':['Paste the text or entities','Choose a direction','Convert and copy'],
  'tips':['Escape <, > and & in attributes','Use UTF-8 to avoid most entities','Decode before re-escaping'],
  'faqs':[('Why encode?','So characters are not parsed as markup.'),('Named vs numeric?','Both work; numeric is universal.')]},

 {'slug':'http-methods-reference','tool':'tools/it/http-methods-reference.html','name':'HTTP Methods Reference',
  'desc':'HTTP Methods guide: a quick reference for GET, POST, PUT, PATCH, DELETE and their semantics.',
  'intro':'The HTTP Methods Reference summarizes what each verb means, its idempotence and when to use it, so your API stays predictable.',
  'features':['Method definitions','Idempotence flags','Safe-method notes','Example use cases','Local only'],
  'scenarios':['Design a REST API','Choose the right verb','Teach HTTP','Review a spec'],
  'steps':['Pick a method','Read its semantics','Apply it to your route'],
  'tips':['GET must not change state','PUT replaces, PATCH modifies','DELETE is usually idempotent'],
  'faqs':[('PUT vs POST?','PUT targets a known URI; POST creates.'),('Idempotent?','Safe to retry without extra effect.')]},

 {'slug':'http-response-headers','tool':'tools/it/http-response-headers.html','name':'HTTP Response Headers',
  'desc':'HTTP Headers guide: a reference for common response headers like Cache-Control and Content-Type.',
  'intro':'The HTTP Response Headers reference explains the headers servers send back, from caching and content type to security policies.',
  'features':['Common header catalog','Security header notes','Caching directives','Local reference','Searchable'],
  'scenarios':['Tune browser caching','Set security headers','Debug a download','Teach HTTP'],
  'steps':['Pick a header','Read its meaning','Apply it to your server'],
  'tips':['Cache-Control beats Expires','CSP reduces XSS risk','Content-Type prevents sniffing'],
  'faqs':[('Cache-Control?','Controls how and how long responses are cached.'),('Which security headers?','CSP, HSTS, X-Content-Type-Options first.')]},

 {'slug':'http-status','tool':'tools/it/http-status.html','name':'HTTP Status Code Lookup',
  'desc':'HTTP Status guide: look up what 2xx, 3xx, 4xx and 5xx codes mean.',
  'intro':'The HTTP Status Code tool explains what a response code indicates, helping you debug APIs and web servers faster.',
  'features':['Full 1xx to 5xx catalog','Class explanations','Common causes','Local reference','Searchable'],
  'scenarios':['Debug a 404 or 500','Pick the right redirect code','Teach HTTP','Review an API spec'],
  'steps':['Enter a code','Read the meaning','See typical fixes'],
  'tips':['4xx is client side, 5xx is server side','301 vs 302 changes caching','418 is a joke'],
  'faqs':[('301 vs 302?','301 is permanent, 302 temporary.'),('429?','Too many requests; respect Retry-After.')]},

 {'slug':'id-card-generator','tool':'tools/it/id-card-generator.html','name':'ID Card Generator',
  'desc':'ID Card guide: generate placeholder identifiers and test card numbers for development.',
  'intro':'The ID Card Generator produces fake identifiers and formatted test numbers for prototyping and testing forms, with no real personal data.',
  'features':['Random ID strings','Formatted test numbers','Bulk generation','Checksum option','Local only'],
  'scenarios':['Populate a demo database','Test a form validator','Mock an API response','Teach validation'],
  'steps':['Choose a format','Set the count','Generate and copy'],
  'tips':['Use only for testing, never real data','Add checksums to exercise validators','Discard after use'],
  'faqs':[('Real data?','No, entirely synthetic.'),('Why checksums?','To mimic real validation rules.')]},

 {'slug':'integer-base-converter','tool':'tools/it/integer-base-converter.html','name':'Integer Base Converter',
  'desc':'Integer Base guide: convert integers between binary, octal, decimal and hexadecimal.',
  'intro':'The Integer Base Converter translates whole numbers across bases with instant feedback, useful for programming, networking and bit work.',
  'features':['Binary, octal, decimal, hex','Live conversion','Two-complement for negatives','Bit-length view','Local only'],
  'scenarios':['Read a hex color or port','Convert a subnet mask','Translate a permission bitmask','Teach bases'],
  'steps':['Enter a number in any base','See all other bases','Copy the target'],
  'tips':['Hex pairs map to bytes','Two-complement handles negatives','Leading zeros do not change value'],
  'faqs':[('Why hex?','It compacts binary and matches memory views.'),('Negatives?','Shown via two-complement with a bit length.')]},

 {'slug':'ip-calculator','tool':'tools/it/ip-calculator.html','name':'IP Subnet Calculator',
  'desc':'IP Calculator guide: compute subnet ranges, network and broadcast addresses for IPv4.',
  'intro':'The IP Calculator breaks down a CIDR into its network, first and last host, and broadcast address, essential for network planning.',
  'features':['IPv4 CIDR analysis','Network and broadcast','Host range and count','Wildcard mask','Local only'],
  'scenarios':['Plan a VLAN','Size a subnet','Teach networking','Verify a config'],
  'steps':['Enter an IP with prefix','Read the breakdown','Use the range'],
  'tips':['/24 gives 254 usable hosts','Smaller prefixes mean bigger ranges','Reserve network and broadcast'],
  'faqs':[('Usable hosts?','Total minus network and broadcast addresses.'),('CIDR?','Classless notation like 192.168.0.0/24.')]},

 {'slug':'ipv4-range-expander','tool':'tools/it/ipv4-range-expander.html','name':'IPv4 Range Expander',
  'desc':'IPv4 Range guide: expand CIDR blocks or start-end ranges into individual addresses.',
  'intro':'The IPv4 Range Expander lists every address in a CIDR or a start-end span, handy for audits, firewalls and tests.',
  'features':['CIDR to list','Start-end to list','Large range capped','Local only'],
  'scenarios':['Audit a firewall rule','Generate test addresses','Teach subnetting','Build a host scan list'],
  'steps':['Enter the range or CIDR','Expand','Copy the addresses'],
  'tips':['Very large ranges are capped for safety','Use CIDR when possible','Mind the broadcast ends'],
  'faqs':[('Why capped?','To avoid million-line outputs.'),('Start-end vs CIDR?','CIDR aligns to boundaries; ranges do not.')]},

 {'slug':'ipv6-converter','tool':'tools/it/ipv6-converter.html','name':'IPv6 Converter',
  'desc':'IPv6 guide: expand and compress IPv6 addresses and convert between formats.',
  'intro':'The IPv6 Converter normalizes addresses to full and compressed forms and converts between IPv4-mapped and other representations.',
  'features':['Expand and compress','IPv4-mapped form','Validation','Local only'],
  'scenarios':['Normalize a config','Compare two addresses','Teach IPv6','Debug a binding'],
  'steps':['Enter the address','Choose the form','Copy the result'],
  'tips':['Leading zeros are dropped in compression',':: stands for the longest zero run','Double-check the scope'],
  'faqs':[('Compressed?','Collapses the longest run of zeros to ::.'),('IPv4-mapped?','Embeds an IPv4 address inside IPv6.')]},

 {'slug':'js-minify','tool':'tools/it/js-minify.html','name':'JavaScript Minifier',
  'desc':'JS Minifier guide: compress JavaScript by removing whitespace and comments.',
  'intro':'The JavaScript Minifier shrinks scripts for faster delivery. It strips safe whitespace and comments while keeping behavior intact.',
  'features':['Removes comments and whitespace','Keeps logic valid','Large input supported','Local only'],
  'scenarios':['Shrink a production bundle','Compare sizes','Teach build steps','Prepare for CDN'],
  'steps':['Paste the JS','Minify','Copy the output'],
  'tips':['Keep source maps for debugging','Minify at build time','Verify behavior after'],
  'faqs':[('Safe?','Only whitespace and comments are removed.'),('Source maps?','Keep them separate from the minified file.')]},

 {'slug':'json-path','tool':'tools/it/json-path.html','name':'JSONPath Evaluator',
  'desc':'JSONPath guide: query and extract fields from JSON using JSONPath expressions.',
  'intro':'The JSONPath Evaluator runs path queries against JSON so you can pull exactly the data you need without writing code.',
  'features':['JSONPath support','Live result preview','Handles arrays','Error messages','Local only'],
  'scenarios':['Extract a nested field','Test a query for code','Teach JSON querying','Trim an API response'],
  'steps':['Paste the JSON','Write a path','See the matches'],
  'tips':['$.store.book[*] selects all books','Use filters like ?(@.price<10)','Watch for null results'],
  'faqs':[('JSONPath vs XPath?','JSONPath targets JSON instead of XML.'),('Why no result?','The path did not match any node.')]},

 {'slug':'json-repair','tool':'tools/it/json-repair.html','name':'JSON Repair',
  'desc':'JSON Repair guide: fix broken or truncated JSON into valid, parseable data.',
  'intro':'The JSON Repair tool heals common mistakes such as trailing commas, single quotes and unquoted keys so you can parse otherwise invalid JSON.',
  'features':['Fixes trailing commas','Quotes keys and strings','Balances braces','Preview result','Local only'],
  'scenarios':['Recover a truncated log','Clean a hand-edited file','Teach JSON rules','Prep data for parse'],
  'steps':['Paste the broken JSON','Repair','Copy the valid output'],
  'tips':['Back up the original first','Not all damage is fixable','Validate after repair'],
  'faqs':[('Always works?','Most structural issues yes; semantic ones no.'),('Why break?','Editors and logs often emit near-JSON.')]},

 {'slug':'json-schema-validator','tool':'tools/it/json-schema-validator.html','name':'JSON Schema Validator',
  'desc':'JSON Schema guide: validate JSON against a draft-07 schema.',
  'intro':'The JSON Schema Validator checks your data against a schema so contracts stay consistent between services and validators.',
  'features':['Draft-07 support','Clear error paths','Sample schema','Local only'],
  'scenarios':['Validate an API payload','Lock a config format','Teach schemas','Catch bad input early'],
  'steps':['Paste the JSON and schema','Validate','Read the errors'],
  'tips':['required enforces presence','type catches shape mistakes','Use $ref for reuse'],
  'faqs':[('Which draft?','Draft-07 is the common baseline.'),('Why validate?','Fails fast on malformed input.')]},

 {'slug':'json-to-toml','tool':'tools/it/json-to-toml.html','name':'JSON to TOML Converter',
  'desc':'JSON to TOML guide: convert JSON into TOML for config files.',
  'intro':'The JSON to TOML tool translates JSON into the readable TOML format used by many modern config systems.',
  'features':['JSON to TOML','Nested tables','Keeps types','Local only'],
  'scenarios':['Author a config file','Migrate settings','Teach TOML','Feed a tool that needs TOML'],
  'steps':['Paste the JSON','Convert','Copy the TOML'],
  'tips':['Arrays of tables need care','TOML is order-sensitive','Keep keys simple'],
  'faqs':[('TOML vs YAML?','TOML is simpler and less ambiguous.'),('Nested?','Maps become tables.')]},

 {'slug':'json-to-xml','tool':'tools/it/json-to-xml.html','name':'JSON to XML Converter',
  'desc':'JSON to XML guide: convert JSON into XML with configurable root and array handling.',
  'intro':'The JSON to XML tool maps JSON to XML elements, useful when talking to legacy systems that expect XML.',
  'features':['JSON to XML','Root element option','Array handling','Local only'],
  'scenarios':['Feed a legacy API','Interop with XML tools','Teach data formats','Bridge two systems'],
  'steps':['Paste the JSON','Set options','Convert and copy'],
  'tips':['Decide how arrays serialize','XML has no native types','Watch attribute vs element choice'],
  'faqs':[('Types lost?','XML is text; indicate types yourself.'),('Root?','Give the document a single root element.')]},

 {'slug':'kubernetes-yaml-generator','tool':'tools/it/kubernetes-yaml-generator.html','name':'Kubernetes YAML Generator',
  'desc':'Kubernetes guide: scaffold Deployments, Services and ConfigMaps as YAML.',
  'intro':'The Kubernetes YAML Generator builds common resource manifests so you can stand up a workload without memorizing field names.',
  'features':['Deployment, Service, ConfigMap','Replicas and ports','Image and probes','Local only'],
  'scenarios':['Bootstrap a workload','Standardize a template','Teach k8s','Reproduce a manifest'],
  'steps':['Pick the resource','Set the fields','Copy the YAML'],
  'tips':['Set resource requests','Add a readiness probe','Keep secrets in Secrets'],
  'faqs':[('Apply?','Use kubectl apply -f with the output.'),('Why YAML?','It is the native k8s manifest format.')]},

 {'slug':'markdown-lint','tool':'tools/it/markdown-lint.html','name':'Markdown Linter',
  'desc':'Markdown Lint guide: check Markdown for style and structure issues.',
  'intro':'The Markdown Linter flags inconsistent headings, broken links and formatting smells so your docs stay clean and consistent.',
  'features':['Heading order checks','Link and image checks','Style rules','Line notes','Local only'],
  'scenarios':['Clean up docs','Enforce a style guide','Teach Markdown','Prep a README'],
  'steps':['Paste the Markdown','Read the warnings','Fix the lines'],
  'tips':['One H1 per document','Consistent list markers help','Link-check before publish'],
  'faqs':[('Enforced?','Rules are suggestions you can adopt.'),('Why lint?','Consistent docs are easier to maintain.')]},

 {'slug':'markdown-to-html','tool':'tools/it/markdown-to-html.html','name':'Markdown to HTML',
  'desc':'Markdown guide: convert Markdown into clean HTML.',
  'intro':'The Markdown to HTML tool renders Markdown to semantic HTML you can paste into a page or email.',
  'features':['GitHub-style rendering','Headings, lists, code','Tables and links','Local only'],
  'scenarios':['Write docs faster','Preview a post','Generate email HTML','Teach Markdown'],
  'steps':['Paste the Markdown','Convert','Copy the HTML'],
  'tips':['Escape raw HTML if needed','Use fenced code blocks','Sanitize before untrusted input'],
  'faqs':[('XSS?','Sanitize output if the source is untrusted.'),('Tables?','Supported via pipe syntax.')]},

 {'slug':'math-evaluator','tool':'tools/it/math-evaluator.html','name':'Math Expression Evaluator',
  'desc':'Math Evaluator guide: compute expressions with functions, variables and units.',
  'intro':'The Math Evaluator parses and computes arithmetic expressions, including parentheses, functions and constants, without installing anything.',
  'features':['Arithmetic and functions','Variables','Constants like pi and e','Step preview','Local only'],
  'scenarios':['Check a formula quickly','Evaluate a derived expression','Teach order of operations','Script-free math'],
  'steps':['Type the expression','Evaluate','Read the result'],
  'tips':['Use parentheses to be explicit','Functions need their arguments','Watch operator precedence'],
  'faqs':[('Safe?','It evaluates math only, not code.'),('Variables?','Assign like x=3 then use x.')]},

 {'slug':'md5','tool':'tools/it/md5.html','name':'MD5 Hash',
  'desc':'MD5 guide: compute the MD5 checksum of text or files for quick integrity checks.',
  'intro':'The MD5 tool produces a 128-bit digest commonly used to verify downloads. Note it is broken for security, so use it only for non-adversarial checksums.',
  'features':['Text and file input','Hex output','Fast local hashing','Local only'],
  'scenarios':['Verify a downloaded file','Tag cached data','Teach hashing','Detect accidental change'],
  'steps':['Paste text or pick a file','Hash','Compare the digest'],
  'tips':['MD5 is not for passwords or signatures','Use SHA-256 for security','Compare digests exactly'],
  'faqs':[('Still safe?','For integrity only; collisions are easy to craft.'),('When SHA?','Whenever an adversary is possible.')]},

 {'slug':'meta-tags-generator','tool':'tools/it/meta-tags-generator.html','name':'Meta Tags Generator',
  'desc':'Meta Tags guide: build SEO and social meta tags for a page.',
  'intro':'The Meta Tags Generator produces title, description, Open Graph and Twitter Card tags so your pages look right when shared.',
  'features':['Title and description','Open Graph tags','Twitter Card tags','Copy-ready HTML','Local only'],
  'scenarios':['Prepare a new page','Fix share previews','Teach SEO basics','Standardize tags'],
  'steps':['Enter the title and description','Add an image URL','Copy the tags'],
  'tips':['Keep titles under ~60 characters','og:image should be 1200x630','Unique descriptions help SEO'],
  'faqs':[('OG vs Twitter?','Twitter falls back to OG when absent.'),('Required?','Title and description are the minimum.')]},

 {'slug':'mime-type-lookup','tool':'tools/it/mime-type-lookup.html','name':'MIME Type Lookup',
  'desc':'MIME Type guide: look up the content type for a file extension and vice versa.',
  'intro':'The MIME Type Lookup maps extensions to media types so your server sends the right Content-Type header.',
  'features':['Extension to type','Type to extension','Common aliases','Local only'],
  'scenarios':['Set a server header','Debug a download','Teach web basics','Pick a type for an upload'],
  'steps':['Enter an extension or type','Read the mapping','Copy it'],
  'tips':['Wrong types break downloads','application/json not text/json','Charset belongs on text types'],
  'faqs':[('Why it matters?','Browsers decide handling from Content-Type.'),('text vs application?','Application implies download, not display.')]},

 {'slug':'morse','tool':'tools/it/morse.html','name':'Morse Code Translator',
  'desc':'Morse guide: encode and decode Morse code for text and signals.',
  'intro':'The Morse Code tool converts text to dots and dashes and back, handy for radio, puzzles and learning.',
  'features':['Text to Morse','Morse to text','Adjustable speed preview','Local only'],
  'scenarios':['Encode a call sign','Decode a signal','Teach Morse','Make a puzzle'],
  'steps':['Type text or Morse','Convert','Copy the result'],
  'tips':['Use a slash between words','Spaces separate letters','Mind prosigns'],
  'faqs':[('Same both ways?','Yes, it encodes and decodes.'),('Standard?','ITU Morse is the common set.')]},

 {'slug':'nanoid-generator','tool':'tools/it/nanoid-generator.html','name':'NanoID Generator',
  'desc':'NanoID guide: generate short, URL-safe unique identifiers.',
  'intro':'The NanoID Generator creates compact random IDs with a customizable alphabet and length, great for database keys and codes.',
  'features':['Configurable length and alphabet','URL-safe default','Bulk generation','Local only'],
  'scenarios':['Create record IDs','Generate invite codes','Tag assets','Teach ID design'],
  'steps':['Set length and alphabet','Generate','Copy the IDs'],
  'tips':['Shorter IDs collide sooner','Avoid ambiguous chars for humans','Use crypto randomness'],
  'faqs':[('NanoID vs UUID?','NanoID is shorter and customizable.'),('Collision?','Longer and larger alphabets reduce it.')]},

 {'slug':'nginx-config-generator','tool':'tools/it/nginx-config-generator.html','name':'Nginx Config Generator',
  'desc':'Nginx guide: scaffold server blocks, reverse proxies and redirects.',
  'intro':'The Nginx Config Generator builds common directives so you can stand up a site, proxy or redirect without memorizing syntax.',
  'features':['Server block template','Reverse proxy','SSL redirect','Static root','Local only'],
  'scenarios':['Host a static site','Proxy to a backend','Force HTTPS','Teach Nginx'],
  'steps':['Pick the scenario','Fill the fields','Copy the config'],
  'tips':['Test with nginx -t before reload','Proxy headers matter','Keep includes organized'],
  'faqs':[('Reload?','Use nginx -s reload after editing.'),('Why a template?','Reduces syntax mistakes.')]},

 {'slug':'password-strength','tool':'tools/it/password-strength.html','name':'Password Strength Checker',
  'desc':'Password Strength guide: estimate and improve the strength of a password.',
  'intro':'The Password Strength Checker scores a password on length, variety and patterns, helping users pick stronger credentials. It never stores or sends input.',
  'features':['Entropy estimate','Checks length and classes','Flags common patterns','Local only'],
  'scenarios':['Coach a user on strength','Audit a policy','Teach password hygiene','Validate a field'],
  'steps':['Type the password','Read the score','Apply the suggestions'],
  'tips':['Length beats complexity alone','Avoid dictionary words','Use a manager'],
  'faqs':[('Stored?','No, everything stays in your browser.'),('Entropy?','A measure of unpredictability in bits.')]},

 {'slug':'prime-checker','tool':'tools/it/prime-checker.html','name':'Prime Number Checker',
  'desc':'Prime guide: test whether a number is prime and factor it.',
  'intro':'The Prime Checker determines primality and can factor integers, useful for math, crypto and teaching.',
  'features':['Primality test','Factorization','Large integer support','Local only'],
  'scenarios':['Verify a prime for crypto','Factor a number','Teach number theory','Check a modulus'],
  'steps':['Enter the integer','Test or factor','Read the result'],
  'tips':['Trial division is fine for modest sizes','Big integers need care','1 is not prime'],
  'faqs':[('Any size?','Within practical limits of the browser.'),('Why factor?','Useful in crypto and math.')]},

 {'slug':'qr-beautify','tool':'tools/it/qr-beautify.html','name':'QR Code Beautifier',
  'desc':'QR Beautify guide: style QR codes with colors, logos and rounded modules.',
  'intro':'The QR Beautify tool customizes a QR code\'s appearance while keeping it scannable, ideal for branding.',
  'features':['Color and gradient','Logo overlay','Rounded modules','Quiet-zone control','Local only'],
  'scenarios':['Brand a QR code','Make a poster code','Teach QR design','Style a menu code'],
  'steps':['Enter the content','Style it','Download the code'],
  'tips':['Keep contrast high for scans','Do not cover the finder squares','Test with a real phone'],
  'faqs':[('Still scannable?','If contrast and quiet zone are preserved.'),('Logo safe?','Keep it small and central.')]},

 {'slug':'sitemap-generator','tool':'tools/it/sitemap-generator.html','name':'Sitemap Generator',
  'desc':'Sitemap guide: build an XML sitemap from a list of URLs.',
  'intro':'The Sitemap Generator turns a URL list into a standards-compliant XML sitemap you can submit to search engines.',
  'features':['XML sitemap output','Priority and changefreq','Lastmod option','Local only'],
  'scenarios':['Submit a site to search engines','Rebuild after changes','Teach SEO','Audit coverage'],
  'steps':['Paste the URLs','Set options','Copy the XML'],
  'tips':['One URL per line','Keep under the size limit','Submit via Search Console'],
  'faqs':[('Required?','Strongly recommended for indexing.'),('Limit?','50k URLs or 50MB per file.')]},

 {'slug':'slugify','tool':'tools/it/slugify.html','name':'Slugify Text',
  'desc':'Slugify guide: turn titles into URL-friendly slugs.',
  'intro':'The Slugify tool converts headings and names into lowercase, hyphenated slugs safe for URLs and filenames.',
  'features':['Lowercase and hyphenate','Strip punctuation','Transliterate option','Bulk lines','Local only'],
  'scenarios':['Build a blog URL','Name a file','Generate an anchor','Teach URL hygiene'],
  'steps':['Paste the text','Slugify','Copy the result'],
  'tips':['Keep slugs short and readable','Avoid stop words when useful','Be consistent across the site'],
  'faqs':[('Accents?','Optional transliteration removes them.'),('Why hyphens?','They are the most URL-safe separator.')]},

 {'slug':'sql-formatter','tool':'tools/it/sql-formatter.html','name':'SQL Formatter',
  'desc':'SQL Formatter guide: pretty-print and standardize SQL queries.',
  'intro':'The SQL Formatter indents and wraps SQL so queries are readable and reviewable, supporting common dialects.',
  'features':['Multi-dialect support','Keyword uppercasing','Indent control','Local only'],
  'scenarios':['Review a teammate query','Debug a long statement','Teach SQL style','Prep a migration'],
  'steps':['Paste the SQL','Choose dialect and style','Format and copy'],
  'tips':['Consistent style eases review','Uppercase keywords read clearly','Watch string literals'],
  'faqs':[('Dialects?','MySQL, PostgreSQL, SQLite and more.'),('Safe?','It reformats only, no execution.')]},

 {'slug':'svg-placeholder-generator','tool':'tools/it/svg-placeholder-generator.html','name':'SVG Placeholder Generator',
  'desc':'SVG Placeholder guide: create placeholder images for layouts and mockups.',
  'intro':'The SVG Placeholder Generator emits scalable placeholder graphics with custom size, text and color for prototyping.',
  'features':['Any dimensions','Custom label and color','Scalable SVG output','Local only'],
  'scenarios':['Mock a page layout','Reserve an ad slot','Teach responsive design','Prototype quickly'],
  'steps':['Set width and height','Add a label and color','Copy the SVG'],
  'tips':['SVG scales without blur','Use neutral colors','Replace before launch'],
  'faqs':[('SVG vs PNG?','SVG is resolution independent.'),('Where used?','As a stand-in during design.')]},

 {'slug':'token-generator','tool':'tools/it/token-generator.html','name':'Token Generator',
  'desc':'Token guide: generate secure random tokens for APIs and sessions.',
  'intro':'The Token Generator creates cryptographically random tokens for CSRF, password reset and API keys, using the browser crypto API.',
  'features':['Configurable length','Hex or base64url','Bulk generation','Local randomness'],
  'scenarios':['Issue an API key','Create a CSRF token','Generate a reset code','Teach token design'],
  'steps':['Set length and format','Generate','Copy the token'],
  'tips':['Use crypto randomness, not Math.random','Store hashes of long-lived tokens','Rotate periodically'],
  'faqs':[('Safe?','Uses the Web Crypto API.'),('Store?','Keep only a hash of durable tokens.')]},

 {'slug':'toml-to-json','tool':'tools/it/toml-to-json.html','name':'TOML to JSON Converter',
  'desc':'TOML to JSON guide: convert TOML config into JSON.',
  'intro':'The TOML to JSON tool maps TOML into JSON so you can feed config into systems that expect JSON.',
  'features':['TOML to JSON','Nested tables','Type preservation','Local only'],
  'scenarios':['Migrate config','Interop with JSON tools','Teach TOML','Bridge formats'],
  'steps':['Paste the TOML','Convert','Copy the JSON'],
  'tips':['Tables become objects','Arrays of tables become arrays','Keep keys valid in JSON'],
  'faqs':[('Why JSON?','Many tools consume it natively.'),('Nested?','Tables map to nested objects.')]},

 {'slug':'triangle-calculator','tool':'tools/it/triangle-calculator.html','name':'Triangle Calculator',
  'desc':'Triangle guide: solve side lengths and angles of a triangle.',
  'intro':'The Triangle Calculator computes missing sides or angles from what you know, using trigonometry and the laws of sines and cosines.',
  'features':['Solve by sides or angles','Area and perimeter','Right-triangle mode','Local only'],
  'scenarios':['Check a geometry problem','Lay out a structure','Teach trigonometry','Verify a measurement'],
  'steps':['Enter the known values','Solve','Read sides and angles'],
  'tips':['Right triangles are simplest','Degrees versus radians matters','Three angles sum to 180'],
  'faqs':[('Which law?','Sine law for opposite pairs, cosine for included angle.'),('Units?','Consistent length units throughout.')]},

 {'slug':'unicode-lookup','tool':'tools/it/unicode-lookup.html','name':'Unicode Lookup',
  'desc':'Unicode guide: look up characters by codepoint, name or glyph.',
  'intro':'The Unicode Lookup resolves characters to their metadata and finds code points by name or glyph, helpful for fonts, i18n and debugging mojibake.',
  'features':['Search by name or glyph','Codepoint and block','Copy escapes','Local only'],
  'scenarios':['Find a special character','Diagnose mojibake','Teach Unicode','Pick a symbol'],
  'steps':['Search or paste a char','Read the metadata','Copy the escape'],
  'tips':['Codepoints are hexadecimal','Blocks group related chars','Watch combining marks'],
  'faqs':[('Block?','A range of code points for a script or symbol set.'),('Mojibake?','Wrong encoding when decoding text.')]},

 {'slug':'unit-converter-advanced','tool':'tools/it/unit-converter-advanced.html','name':'Advanced Unit Converter',
  'desc':'Unit Converter guide: convert across length, mass, temperature, data and more.',
  'intro':'The Advanced Unit Converter handles many categories with precise factors, useful for engineering, cooking and data sizes.',
  'features':['Many categories','Binary and SI data units','Temperature with offsets','Local only'],
  'scenarios':['Convert engineering units','Translate data sizes','Switch temperature scales','Teach units'],
  'steps':['Pick a category','Enter the value and units','Read the result'],
  'tips':['Data has binary and decimal units','Temperature needs offsets, not ratios','Check the category first'],
  'faqs':[('KiB vs KB?','KiB is 1024, KB is 1000.'),('Why offsets for temp?','Celsius and Fahrenheit have zero points.')]},

 {'slug':'user-agent-parser','tool':'tools/it/user-agent-parser.html','name':'User-Agent Parser',
  'desc':'User-Agent guide: parse a UA string into browser, OS and device fields.',
  'intro':'The User-Agent Parser breaks a UA string into its parts so you can detect browser, OS and device type for analytics or debugging.',
  'features':['Browser, OS, device','Engine and version','Readable output','Local only'],
  'scenarios':['Debug a layout bug','Classify traffic','Teach UA structure','Inspect a request'],
  'steps':['Paste the UA string','Read the fields','Use what you need'],
  'tips':['UA can be spoofed; do not trust blindly','Prefer feature detection in code','Bots have telling strings'],
  'faqs':[('Reliable?','Best-effort; clients can lie.'),('Why parse?','To reproduce or segment by environment.')]},

 {'slug':'wifi-qr-generator','tool':'tools/it/wifi-qr-generator.html','name':'Wi-Fi QR Generator',
  'desc':'Wi-Fi QR guide: encode network credentials into a scannable QR code.',
  'intro':'The Wi-Fi QR Generator creates a QR code that lets phones join a network by scanning, without typing the password.',
  'features':['WPA, WEP, open','Hidden network option','Encodes SSID and key','Local only'],
  'scenarios':['Share a guest network','Set up a venue','Teach QR uses','Avoid typing a long key'],
  'steps':['Enter SSID and password','Pick the auth type','Generate and scan'],
  'tips':['Use WPA2 or better','Keep the code private','Test with a real phone'],
  'faqs':[('Safe?','Anyone who scans gets the password.'),('Format?','Uses the standard WIFI: QR scheme.')]},

 {'slug':'xml-formatter','tool':'tools/it/xml-formatter.html','name':'XML Formatter',
  'desc':'XML Formatter guide: pretty-print and validate XML.',
  'intro':'The XML Formatter indents XML for readability and reports well-formedness errors so you can fix broken documents.',
  'features':['Pretty-print','Well-formedness check','Attribute handling','Local only'],
  'scenarios':['Tidy a config file','Debug a parse error','Teach XML','Prep a feed'],
  'steps':['Paste the XML','Format or validate','Read the output'],
  'tips':['XML is case-sensitive','Close every tag','Watch CDATA sections'],
  'faqs':[('Validate?','It checks well-formedness, not a schema.'),('Why indent?','Easier to read and review.')]},

 {'slug':'xml-to-json','tool':'tools/it/xml-to-json.html','name':'XML to JSON Converter',
  'desc':'XML to JSON guide: convert XML into JSON for modern pipelines.',
  'intro':'The XML to JSON tool maps XML elements and attributes into JSON, bridging legacy and modern systems.',
  'features':['XML to JSON','Attribute handling','Array detection','Local only'],
  'scenarios':['Consume a legacy feed','Bridge two systems','Teach data formats','Prep for code'],
  'steps':['Paste the XML','Convert','Copy the JSON'],
  'tips':['Attributes need a convention','Repeated tags become arrays','Text vs child nodes differ'],
  'faqs':[('Attributes?','Usually prefixed like @attr.'),('Lossy?','Some structure choices are opinionated.')]},

 {'slug':'xml-validator','tool':'tools/it/xml-validator.html','name':'XML Validator',
  'desc':'XML Validator guide: check XML for well-formedness and common errors.',
  'intro':'The XML Validator parses a document and reports exactly where it breaks, so you can fix feeds, configs and SOAP messages.',
  'features':['Well-formedness check','Line and column errors','Attribute checks','Local only'],
  'scenarios':['Debug a broken feed','Validate a config','Teach XML rules','Prep a publish'],
  'steps':['Paste the XML','Validate','Fix the flagged lines'],
  'tips':['One root element required','Quote all attributes','Escape special chars in text'],
  'faqs':[('Well-formed vs valid?','Well-formed parses; valid also matches a schema.'),('Why fail?','Usually an unclosed tag or bad char.')]},

 {'slug':'yaml-to-json','tool':'tools/it/yaml-to-json.html','name':'YAML to JSON Converter',
  'desc':'YAML to JSON guide: convert YAML into JSON.',
  'intro':'The YAML to JSON tool maps YAML into JSON, handy when a tool expects JSON but your config is YAML.',
  'features':['YAML to JSON','Nested structures','Type preservation','Local only'],
  'scenarios':['Feed a JSON tool','Migrate config','Teach YAML','Bridge formats'],
  'steps':['Paste the YAML','Convert','Copy the JSON'],
  'tips':['Indentation is significant','Tabs are not allowed','Watch multiline strings'],
  'faqs':[('Indent?','Spaces only, consistent per level.'),('Types?','Scalars map to JSON types.')]},

 {'slug':'yaml-validator','tool':'tools/it/yaml-validator.html','name':'YAML Validator',
  'desc':'YAML Validator guide: check YAML for syntax errors and structure.',
  'intro':'The YAML Validator parses YAML and reports indentation or mapping mistakes before they break a deploy or pipeline.',
  'features':['Syntax check','Clear error location','Handles anchors','Local only'],
  'scenarios':['Validate a CI config','Check a compose file','Teach YAML','Prep a deploy'],
  'steps':['Paste the YAML','Validate','Fix the flagged lines'],
  'tips':['Use spaces, never tabs','Align keys in a map','Quote strings with colons'],
  'faqs':[('Common error?','Inconsistent indentation.'),('Anchors?','Reuse values with & and *.')]},
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

#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'text')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'text')
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
    out = {'slug': slug, 'industry': 'text', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('reading-time-estimator', build('reading-time-estimator', [
        "Reading Time Estimator",
        "/ Reading Time Estimator",
        "📖 View the \"Reading Time Estimator User Guide\"",
        "🔮 Reading Time Estimator",
        "Estimating reading time helps with scheduling and writing summaries. This tool counts Chinese characters and English words separately and converts them into minutes by common reading speed, giving an approximate time needed.",
        "Reading time (minutes) = Chinese character count ÷ Chinese reading speed + English word count ÷ English reading speed; common speeds are 300 to 500 Chinese chars/min and 200 to 250 English words/min (default 400 chars/min and 200 words/min may be taken); aloud time is about 1.5 to 2 times silent reading (Chinese aloud about 200 chars/min); the result is rounded up to the minute.",
        "Paste the text to estimate",
        "In a purely front-end tool site, reading time estimation is a very practical little feature, helping users judge how much time a long article will take.",
        "Chinese speed (characters/minute)",
        "English speed (words/minute)",
        "Chinese reading speed varies from person to person; an ordinary adult reads about 250–400 chars/min, and an English native about 200–250 words/min. Adjustable parameters adapt to different readers.",
        "This tool counts unified CJK segment characters (Chinese, Japanese, Korean) as Chinese characters and English digits as words, without interfering with each other.",
        "The estimate is for reference only: technical articles, content with code or charts is actually slower, and entertainment content may be faster.",
        "📋 Reference Reading Speed",
        "Chinese normal",
        "300 chars/min",
        "Chinese fast",
        "500 chars/min",
        "English native",
        "200 words/min",
        "📚 In-Depth Analysis: Reading Time Estimator",
        "Before publishing a WeChat official account / blog post, estimate the approximate reading time of a Chinese-English mixed article, helping label \"about X minutes to read\" in the title or at the end.",
        "When laying out course or training materials, compute separately by the different",
        "reading speeds",
        "of Chinese and English to give a total time closer to reality.",
        "When a content platform does recommendation / ranking, use reading time as a weight factor to avoid long articles being misjudged as low completion.",
        "Example: a Chinese-English mixed article",
        "An article with 1200 Chinese characters and 80 English words, taking Chinese 300 chars/min and English 200 words/min: Chinese takes 1200÷300=4.0 min, English 80÷200=0.4 min, total 4.4 min, rounded up to about 4–5 min (the tool shows integer minutes by Math.round).",
        "Why are Chinese and English calculated separately?",
        "Their reading speeds differ: counting Chinese by character count and English by word count is more accurate. The tool uses regex to count Chinese characters and English words separately, then divides by their respective speeds and adds them.",
        "How are punctuation, spaces and digits counted?",
        "Chinese statistics only look at CJK ideographs (\\u4e00–\\u9fff); English words are split by [A-Za-z0-9]+; punctuation and pure spaces are not counted separately, and the result is an integer minute not less than 1.",
    ]))

    write('sensitive-word-filter', build('sensitive-word-filter', [
        "🔍 Sensitive Word Detector",
        "Supports a custom word list, highlights hits and one-click replaces them.",
        "/ Sensitive Word Detector",
        "Sensitive-word detection matches against a word library: hit count = Σ occurrences of each sensitive word in the text (an Aho-Corasick automaton can scan all patterns in one pass); hit rate = number of hit words ÷ total words in the text × 100%; it highlights by the offset of the hit position and returns context snippets, supporting fuzzy matching of homophones, variants and inserted separators to improve recall.",
        "Sensitive words (separate with commas or newlines)",
        "illegal,spam,fraud,cheat",
        "Replacement character",
        "Detect and replace",
        "Copy cleaned text",
        "📚 In-Depth Analysis: Sensitive Word Detector / Filter",
        "Before publishing user comments, bullet comments or UGC, batch-screen whether they contain violating words; after a hit, replace with a mask or highlight as a warning.",
        "Filter a custom sensitive-word list (such as competitor names, internal terms) uniformly to avoid words that should not appear in outgoing content.",
        "In a content-moderation pipeline, first run a round of keyword scanning to flag risky segments for human review, reducing the chance of missed checks.",
        "Example: replace and highlight",
        "The text \"Claim your grand prize\" contains the sensitive word \"prize\"; in replace mode \"*\" masks it as \"Claim your ***\"; in highlight mode the page highlights \"prize\" in yellow. Multiple words are separated by newlines or commas and matched exactly by regex.",
        "How is the mask length determined?",
        "The replacement character repeats by the original word length, but is limited to 1–6 characters (Math.max(1, Math.min(6, length))), masking the original word without being too long and affecting layout.",
        "Can it match partial words or",
        "?",
        "List entries are first regex-escaped (special characters taken literally) and matched by substring inclusion, so an entry \"prize\" would hit \"won the prize\". For whole-word boundaries, add boundary markers around the entry.",
    ]))

    write('stats-1', build('stats-1', [
        "📖 Word Count (with character and word counts)",
        "With character count and word count",
        "/ Word Count (with character and word counts)",
        "📐 Counting Scope Notes",
        "Chinese characters are counted character by character within the Unicode CJK range; English words by continuous letter strings; digits by continuous digit strings; total characters are given in two scopes, with and without whitespace; line count is split by newlines, and non-empty lines exclude pure-whitespace lines.",
        "Input the text to count",
        "This is a sample text used to demonstrate word counting. Hello ToolBox 2026!",
        "Start counting",
        "📚 In-Depth Analysis: Word Count (characters / words / lines)",
        "Before publishing writing, a paper or social-media copy, count the total characters and Chinese-English word counts to confirm whether word limits are met (such as abstract length, platform caps).",
        "Compare character count (with whitespace) and (without whitespace) to find extra spaces and invisible characters, ensuring accurate layout and billing.",
        "Quickly estimate the item scale of code, lists or rosters by line count and non-empty line count.",
        "Example: a Chinese-English mixed paragraph",
        "Text \"This is a sample, Hello World 2026!\": total characters (with whitespace) 22, without whitespace 19, Chinese characters 8, English words 2 (Hello / World), digit groups 1 (2026), lines 1, non-empty lines 1.",
        "How are English words counted?",
        "Identified by continuous letter strings (e.g. Hello, World each count as 1); hyphens and letters inside abbreviations are merged into the same word; Chinese is counted",
        "character by character, and punctuation and whitespace are not counted as Chinese characters.",
        "Are digits counted as characters?",
        "Digits are counted in \"total characters\" and \"digit groups\" but not in Chinese character count or English word count; continuous digits (such as 2026) count as one digit group, not 4 English words.",
        "About Word Count (with character and word counts)",
    ]))

    write('text-to-1337', build('text-to-1337', [
        "Text to Leet Speak",
        "/ Text to Leet Speak",
        "📖 View the \"Text to 1337 User Guide\"",
        "📝 Text to Leet Speak (1337)",
        "Leet (1337) speak replaces letters with similar-looking digits and symbols, used in geek circles and game nicknames in earlier years. Choose the strength to turn ordinary text into a leet style.",
        "Leet conversion replaces by a letter-to-digit-or-symbol mapping table: a → 4 or @, e → 3, i → 1 or !, o → 0, s → 5 or $, t → 7, g → 9, b → 8; light mode replaces only some characters, heavy mode replaces all and mixes case; the character count is unchanged before and after conversion, and readability drops as the replacement ratio rises.",
        "Replacement strength",
        "Low (common letters only)",
        "Medium (more replacements)",
        "High (all replaceable)",
        "Low strength replaces only the most common letters such as e/a/o/t/l/s and has the highest readability; high strength replaces almost every letter and looks more like traditional 1337.",
        "The same letter is written differently in different leet dialects (e.g. a can also be written as /\\, @); this tool uses one common mapping set.",
        "Used for nicknames, easter eggs and teaching demos; please do not use it in official copy as it hurts accessibility.",
        "📋 Common Leet Mappings",
        "📚 In-Depth Analysis: Text to Leet Speak",
        "Do character replacement for game IDs, community nicknames and password inspiration, turning ordinary English into a \"hacker-style\" writing with digits.",
        "When making fun copy or campaign slogans, use 1337 replacement to create recognisability (e.g. LEET→1337).",
        "In security teaching, demonstrate what a \"confusable weak password\" looks like, reminding users not to use only letter→digit replacement as a password.",
        "Example: leet speak is fun",
        "Mapping rules e→3, a→4, o→0, t→7, l→1, s→5, other characters unchanged. \"leet speak is fun\" → \"1337 5p34k 15 fun\" (leet=1337, speak=5p34k, is=15). Only lowercase letters take effect; uppercase stays as-is.",
        "Which letters are replaced?",
        "Only the 6 common mappings are replaced: e→3, a→4, o→0, t→7, l→1, s→5; b, g, i etc. not in the table are kept as-is. For a more complete 1337 table, extend on this rule yourself.",
        "Are uppercase letters converted?",
        "No. The mapping keys are lowercase; an input uppercase letter (such as L) is not replaced and the output stays uppercase, convenient for scenarios where you need to preserve",
        "meaning.",
    ]))

    write('text-to-ascii-art', build('text-to-ascii-art', [
        "/ Text to ASCII Art",
        "📖 View the \"Text to ASCII Art User Guide\"",
        "📝 Text to ASCII Art",
        "Use monospaced characters to spell 5-line-high pixel large letters, suitable for command-line banners and the opening decoration of a project README. Only supports uppercase A–Z and digits 0–9; other characters are left blank.",
        "ASCII art maps by a dot-matrix font: each character is represented by a 5-row × 5-to-7-column bitmap of 0 and 1, replacing 1 with a placeholder character (such as # or @) row by row and 0 with a space; output width = character count × single-character column width + spacing × (character count − 1); only supports uppercase A to Z and digits 0 to 9, and other characters are padded with blank blocks.",
        "Input text (auto upper-case, A-Z 0-9 only)",
        "Each character is a 5-row × 5-column pixel grid, using a fill character (default #) for lit pixels and a space for off pixels, with custom fill character support.",
        "Only built-in glyphs for A–Z and 0–9; lowercase is auto-converted to uppercase, and other characters (including Chinese, spaces, symbols) are left blank as padding.",
        "Rendering depends on a monospaced font; after copying please view in a monospaced environment, and reduce the font size if the width looks broken.",
        "To use the result in a README, put it entirely into a",
        "code block; for a terminal banner the fill character is recommended to be",
        "or",
        "If you need fancier fonts (italic, shadow, small/large), switch to a mature tool such as figlet; this tool focuses on lightweight, dependency-free output.",
        "📚 In-Depth Analysis: Text to ASCII Art",
        "Convert a short title or logo text into a terminal-",
        "usable ASCII character drawing, for READMEs and welcome messages.",
        "When making retro-style posters or chat separators, use pure-text dot-matrix fonts to add design sense.",
        "Teaching demo of the font-rendering principle \"representing glyphs with 0/1 pixel dot matrices\", intuitively showing how characters are encoded.",
        "Example: letter A",
        "Built-in 5×5 dot-matrix font (A–Z, 0–9). The dot matrix of letter A is: row 1 .###., row 2 #...#, row 3 #####, row 4 #...#, row 5 #...# (1 means solid, 0 means blank). Inputting \"HI\" outputs H and I dot matrices side by side as a character drawing.",
        "Which characters are supported?",
        "Built-in dot matrices for A–Z and 0–9; lowercase is auto-rendered as the corresponding uppercase; Chinese and symbols are not yet supported, and other input characters are ignored or left blank.",
        "What do 0 and 1 in the dot matrix represent?",
        "1 means the pixel is solid (rendered as # or ●), 0 means blank. The whole glyph is described by 5 rows × 5 columns = 25 pixels in total, separated by semicolons within a row and by newlines between rows.",
    ]))

    write('text-to-braille', build('text-to-braille', [
        "Text to Braille",
        "/ Text to Braille",
        "📖 View the \"Text to Braille User Guide\"",
        "📝 Text to Braille",
        "Braille represents characters with a 6-dot cell (2 columns × 3 rows); Unicode assigns a code point to each dot pattern starting at U+2800. Enter text to convert it character by character into Braille, convenient for tactile reading and accessible layout preview.",
        "Braille is encoded by a 6-dot cell (2 columns × 3 rows), dot positions numbered 1 to 6; Unicode code point = U+2800 + dot bitmask (each dot weight 1, 2, 4, 8, 16, 32, summed and added to U+2800); e.g. a is dot 1, i.e. U+2801, b is dots 1 and 2, i.e. U+2803; Chinese characters are first converted to pinyin and then spelled by Braille rules, and digits have the prefix U+283C.",
        "Input text (English / digits / punctuation)",
        "Basic Braille Latin letters a–j correspond to dots 1–5; k–t add the 6th dot (dots 3-6) on top of a–j; the rest of the letters have dedicated dot combinations.",
        "Digits 1–0 reuse the dot patterns of a–j, distinguished by a leading # (number sign); this tool outputs digit dot patterns directly.",
        "Complete English Braille also includes the capital prefix (⠠), the number prefix (⠼) and contractions; formal layout needs dedicated rules.",
        "📋 Braille Letter Dots (a–j)",
        "Dot pattern",
        "Dot positions",
        "📚 In-Depth Analysis: Text to Braille",
        "Convert English words, digits or short sentences into Braille",
        "(⠿), for Braille teaching, accessibility demos or fun display.",
        "When doing accessibility (a11y) popular science, intuitively present the \"text → Braille dot pattern\" mapping to help understand the dot system.",
        "In creative design, turn a",
        "brand name",
        "into Braille dot patterns as a visual element (note: display only, not real Braille layout).",
        "Example: Hello 123!",
        "Map a–z, 0–9 and common punctuation: H→⠓, e→⠑, l→⠇, l→⠇, o→⠕, space kept, 1→⠂, 2→⠆, 3→⠒, !→⠖. Thus \"Hello 123!\" → \"⠓⠑⠇⠇⠕ ⠂⠆⠒⠖\".",
        "Not distinguished (all treated as lowercase dot patterns).",
        "Does it support Chinese and punctuation?",
        "Built-in Braille mappings for a–z, 0–9 and some English punctuation (. , ? ! : ; - ' ( )) are provided; Chinese is out of scope and is kept or ignored as-is, depending on the implementation.",
        "Is Braille syllable-based or character-by-character?",
        "This tool maps each single character directly (grade 1 Braille idea), without abbreviations or contractions; real Braille layout (grade 2) uses many abbreviations — sufficient for display purposes, but do not treat it as formal Braille.",
    ]))


if __name__ == '__main__':
    main()
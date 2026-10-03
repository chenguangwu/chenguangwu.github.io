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
    write('analysis-density', build('analysis-density', [
        "📊 Keyword Density Analysis",
        "Count text word frequency and keyword density for SEO and content optimisation",
        "/ Keyword Density Analysis",
        "This tool counts total words by the rule \"Chinese by character, English by word\": each Chinese character is counted as one word, and consecutive English letters are split into words. For each keyword it counts occurrences; density = keyword occurrences ÷ total words × 100%. The recommended density range is 1%–5%.",
        "Text to analyse",
        "In search engine optimisation, keyword density is an important factor affecting ranking. Keyword density helps SEO ranking overall.",
        "Keywords (separate multiple with commas or spaces)",
        "Start analysis",
        "📚 In-Depth Analysis: Keyword Density Analysis (Chinese by character, English by word)",
        "SEO copy pre-screening: paste the web page title, body or promotional copy to count the occurrences and density of the target keyword, and judge whether it falls in the healthy 1%–5% range, avoiding being down-weighted for keyword stuffing.",
        "Multi-keyword comparison: enter several candidate keywords at once (e.g. brand word, industry word, long-tail word) to compare their densities horizontally and find words that are under-covered or over-repeated.",
        "Take a bilingual copy as an example",
        "Body \"apple apple banana apple fruit apple apple\" with keywords being a Chinese word and the English word \"apple\": Chinese counts 10 characters, English counts 2 words, total words 12; the Chinese keyword appears 3 times at 25.00% density, the English keyword \"apple\" appears 2 times at 16.67% density.",
        "What density is appropriate?",
        "Generally recommended between 1%–5%: too low means weak keyword-to-topic relevance; too high (>5%) is easily judged as stuffing by search engines and instead down-weighted. Long articles may relax slightly, short ones need more restraint.",
        "How are Chinese and English counted?",
        "This tool uses the rule \"Chinese by character, English by word\": each Chinese character counts as 1 word, and consecutive English letters (e.g. SEO, apple) are split into words by spaces or punctuation; density = keyword occurrences ÷ total words × 100%.",
        "About Keyword Density Analysis",
    ]))

    write('calc-1', build('calc-1', [
        "⚖️ Text Diff (Characters)",
        "Compare two texts line by line and highlight added, deleted and modified content",
        "Text diff compares line by line: it matches by longest common subsequence per line; unmatched lines are added or deleted; within a line a character-level diff marks the modified segments; similarity = 2 × matched lines ÷ (original line count + new line count) × 100%; additions are highlighted green, deletions red, modifications yellow, for quickly locating changes between two versions.",
        "Added: lines present in text B but not in A.",
        "Deleted: lines present in text A but not in B.",
        "Modified: line content has changed.",
        "📚 In-Depth Analysis: Text Diff (Characters)",
        "After revising copy or code, paste the old version into A and the new version into B to immediately see which lines were added, deleted or kept unchanged.",
        "Compare the differences between two contracts / clauses / configurations, locate the change points, and avoid missing key revisions.",
        "In code review or translation proofreading, confirm whether the translated paragraphs correspond one to one with the source, and find omitted or extra paragraphs.",
        "Example: comparing two short sentences",
        "A=\"I love Beijing\", B=\"I love Shanghai\": the tool compares by longest common subsequence (LCS), marks \"I\" \"love\" as the same, the old \"Beijing\" as deleted and the new \"Shanghai\" as added — the difference position is clear at a glance.",
        "Is the diff based on lines or characters?",
        "This tool splits by line and then does LCS comparison, so paragraph / line-level changes are the clearest; character-level differences within a single line are not marked character by character.",
        "Why are some identical contents marked as added?",
        "Leading/trailing spaces and invisible characters (such as full-width / half-width spaces) being different will cause a line to be judged inconsistent; it is recommended to unify line breaks and indentation before comparing.",
    ]))

    write('convert-6', build('convert-6', [
        "👤 Case Conversion (lowercase / UPPERCASE / Title Case)",
        "lowercase / UPPERCASE / Title Case text conversion",
        "/ Case Conversion (lowercase / UPPERCASE / Title Case)",
        "Case conversion: ALL UPPER = all Latin letters to uppercase; all lower = all Latin letters to lowercase; Title Case = first character of each word to uppercase. Processed character by character; Chinese characters, digits and symbols are unchanged, only English letters are affected.",
        "Conversion target",
        "ALL UPPER (UPPER)",
        "all lower (lower)",
        "📚 In-Depth Analysis: Case Conversion (lowercase / UPPERCASE / Title Case)",
        "Convert a passage of English to all uppercase for titles or emphasis, or all lowercase for variable names and email normalisation.",
        "Capitalise the first letter of each word (Title Case) for the normalised display of personal names, proper nouns and article titles.",
        "Process mixed-case text pasted by users",
        "and normalise it before entering subsequent retrieval or comparison flows, reducing matching failures caused by case differences.",
        "Example: three modes",
        "Input \"hello world\", uppercase → \"HELLO WORLD\", lowercase → \"hello world\", Title Case → \"Hello World\" (only the first letter of each word is capitalised, the rest unchanged). Note that Title Case only replaces the initial letter; upper case already inside a word stays as-is.",
        "Will Title Case change letters inside a word?",
        "No. The rule only capitalises the first letter after a word boundary (\\b); the remaining letters of the word are kept as-is, so \"iPhone\" becomes \"IPhone\" rather than all uppercase.",
        "Will Chinese be affected?",
        "It will not. The regex \\b\\w mainly matches ASCII word characters; Chinese characters are output as-is, and case conversion only acts on English letters.",
        "About Case Conversion (lowercase / UPPERCASE / Title Case)",
    ]))

    write('convert-7', build('convert-7', [
        "🔄 Camel / Snake / Kebab Case Converter",
        "Camel / snake / kebab case online converter",
        "Camel / snake / kebab case conversion",
        "/ Camel / Snake / Kebab Case Converter",
        "📚 In-Depth Analysis: Unit Conversion (Coefficient Method)",
        "Given the value of a quantity and the coefficient \"source unit → base unit\", quickly convert to another unit, e.g. convert kilometres to metres by a factor of 1000.",
        "Handle dimensions with conversion coefficients in recipes, engineering and finance, avoiding mistakes from manual multiplication and division.",
        "Batch-verify whether values of different calibres are equivalent, e.g. whether the same length expressed in different units yields the same result.",
        "Example: convert kilometres to metres",
        "Formula: result = value × coefficient × (source factor ÷ target factor). Set value=2, coefficient=1, source factor=1000 (the factor of km relative to m), target factor=1, then result=2×1×1000/1=2000, i.e. 2 km = 2000 m.",
        "What do the coefficient and the source/target factors do respectively?",
        "The coefficient is for overall scaling (e.g. exchange rate, multiplier), and the source/target factor is for",
        ": result = value × coefficient × (source factor ÷ target factor). Convert both units to the same base and then divide.",
        "How to read a result with many digits?",
        "The tool displays up to 6 decimal places; in practice keep only the",
        "significant figures",
        "matching the dimension; if the source/target factor is set reversed, the result will differ by a conversion ratio, so confirm the factor direction when checking.",
        "About Camel / Snake / Kebab Case Converter",
        "Camel / snake / kebab case converter. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
    ]))

    write('index', build('index', [
        "📝 Text Processing Tools",
        "Text Processing",
        "Text Processing Tools",
        "Lorem Ipsum Generator",
        "The Lorem Ipsum Generator is a free online text-processing tool; Lorem Ipsum is the meaningless Latin placeholder text commonly used in typesetting, letting readers focus on the layout rather than the content. Choose the number of paragraphs to generate standard paragraphs, convenient for filling prototypes and samples. Runs purely on the front end, data…",
        "Case Conversion (lowercase / UPPERCASE / Title Case)",
        "Case conversion tool: convert text between all lowercase, all uppercase and Title Case, for layout and naming-convention processing.",
        "Paste or input two texts and compare them line by line, highlighting additions, deletions and modifications with colours, for quickly locating the change position and specific content between two versions during code and manuscript revision.",
        "Word Count (with character and word counts)",
        "Word count tool: count the number of characters, words and lines in text, supporting mixed Chinese-English counting, for writing and layout word accounting.",
        "Camel / Snake / Kebab Case Converter",
        "Naming-format conversion tool: convert between camelCase, snake_case and kebab-case, for unifying code variable and file name formats.",
        "Text to ASCII Art",
        "Text to ASCII Art is a free online text-processing tool that uses monospaced characters to spell out 5-line-high pixel large letters, suitable for command-line banners and the opening decoration of a project README. It only supports uppercase A–Z and digits 0–9, and leaves other characters blank. Runs purely on the front end, data…",
        "Reading Time Estimator",
        "Reading Time Estimator is a free online text-processing tool; estimating reading time helps with scheduling and writing summaries. This tool counts Chinese characters and English words separately and converts them into minutes by common reading speed, giving an approximate time needed. Runs purely on the front end, data not uploaded, no registration, open the browser…",
        "Sensitive Word Detector",
        "Online sensitive-word detection tool that scans the input text against a sensitive-word library, highlighting hit positions and counts, suitable for content moderation and pre-publishing self-check, runs purely on the front end.",
        "Text to Leet Speak",
        "Text to Leet Speak is a free online text-processing tool; Leet (1337) speak replaces letters with similar-looking digits and symbols, used in geek circles and game nicknames in earlier years. Choose the strength to turn ordinary text into a leet style. Runs purely on the front end, data not uploaded, no…",
        "Text to Braille",
        "Braille represents characters with a 6-dot cell (2 columns × 3 rows); Unicode assigns a code point to each dot pattern starting at U+2800. Enter text to convert it character by character into Braille, convenient for tactile reading and accessible layout preview.",
        "Financial text auto line-wrap tool that wraps paragraphs by a specified width, suitable for report remarks and document layout alignment, processed instantly on the front end.",
        "Mirror-reverse text left and right to generate copyable characters or a preview image, for fun signatures, artistic text and watermarks; supports one-click copy of results with instant front-end conversion.",
        "Keyword Density Analysis",
        "Keyword density analysis tool: enter text and keywords, count word frequency and density share, for SEO and content-optimisation pre-screening.",
        "About Text Processing Tools",
        "The Text Processing Tools collection gathers 13 free online tools covering the common calculation, conversion and lookup needs of text-processing scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you can find ready-to-use practical tools here. All tools run purely on the front end, data is not uploaded to a server, and your privacy and security are protected.",
        "The text processing tools collected on this page include (representative tools):",
        "These tools help you quickly finish common text-processing tasks without memorising complex formulas or doing manual conversions — just enter the values and get the result.",
        "Do the Text Processing Tools require a download or registration?",
        "No. All text processing tools on this page are purely front-end online tools: open the page and use them directly, with no software to install, no account to register, and no data uploaded.",
        "Are the calculation results of the Text Processing Tools accurate? Is the data secure?",
        "The tools compute locally in your browser based on public mathematical formulas and general industry standards, so results are available immediately. All operations run locally on your device, data is never uploaded to a server, and your privacy and security are guaranteed.",
    ]))

    write('lorem-ipsum-generator', build('lorem-ipsum-generator', [
        "/ Lorem Ipsum Generator",
        "📖 View the \"Lorem Placeholder Text Generator User Guide\"",
        "✨ Lorem Ipsum Generator",
        "Lorem Ipsum is the meaningless Latin placeholder text commonly used in typesetting, letting readers focus on the layout rather than the content. Choose the number of paragraphs to generate standard paragraphs, convenient for filling prototypes and samples.",
        "The placeholder text is generated by paragraph: each paragraph consists of 4 to 7 sentences of 10 to 18 words each, drawn from a standard Lorem Ipsum Latin word list of about 70 words; the first sentence of a paragraph starts with a capital letter and ends with a period, words are separated by a single space; the generated amount = paragraph count × average sentence count × average sentence length (words), used for prototype filling and layout samples.",
        "Number of paragraphs (1–10)",
        "Paragraph length",
        "Short (about 30 words)",
        "Medium (about 60 words)",
        "Long (about 100 words)",
        "Lorem Ipsum derives from a scrambled Latin passage of Cicero's \"De Finibus Bonorum et Malorum\"; since the 16th century the printing industry has used it as placeholder copy, and to this day it is a design convention.",
        "This tool randomly concatenates words from a word list; it is not the fixed classic text, but the style is consistent and sufficient for filling the layout and previewing fonts.",
        "Placeholder text should be replaced before the official copy goes live, to avoid mistakenly publishing Lorem Ipsum to a production page.",
        "📋 Classic Opening",
        "📚 In-Depth Analysis: Lorem Ipsum Generator",
        "When making a web page / poster / UI prototype, you need a meaningless placeholder text to support the layout and quickly generate several typesetting samples.",
        "Fill design drafts or presentation documents with sample text, avoiding the use of real content that makes reviewers mistake it for the final draft.",
        "When testing text overflow, line wrapping and font adaptation, use randomly lengthed Latin paragraphs to verify layout robustness.",
        "Example: generate 3 paragraphs",
        "Choose 3 paragraphs; the tool randomly draws words from a fixed word bank (lorem, ipsum, dolor…), each paragraph starts with a capitalised first word and ends with a period, e.g. the first paragraph might be \"",
        "ipsum dolor sit amet consectetur adipiscing elit.\", giving 3 placeholder texts with consistent structure and random content.",
        "Is the content the same every time?",
        "No. Words are concatenated in random order but all come from the same standard Lorem Ipsum word bank, ensuring it is \"Latin-like\" placeholder text rather than real semantics.",
        "Can I specify the number of paragraphs and sentences?",
        "This tool generates by paragraph count (1–10), each paragraph being a random word string; for finer length control, generate multiple times and then crop manually.",
    ]))


if __name__ == '__main__':
    main()
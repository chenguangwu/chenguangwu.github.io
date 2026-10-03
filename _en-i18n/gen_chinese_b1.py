#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'chinese')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'chinese')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    return mp


def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'chinese', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

#!/usr/bin/env python3


def main():
    # ===== chinese-character (32) =====
    write('chinese-character', build('chinese-character', [
        'Chinese Character Query',
        'Look up a character’s pinyin, radical, stroke count, and meaning',
        'View the Chinese Character Query User Guide',
        'Chinese Character Query: enter a single character to instantly get its pinyin, radical, total stroke count, glyph structure, and Unicode / input-method encoding. Fully offline, client-side parsing — ideal for literacy, dictionary lookup, and verifying standard handwriting.',
        'Han',
        'Detailed Definition',
        'Related Characters',
        'Deep Dive: Chinese Character Query',
        'When you meet an unfamiliar character while reading, just copy or type it in to see its pinyin, radical, and strokes — you grasp the pronunciation and shape instantly, with no paper dictionary needed.',
        'When helping a child with homework, confirm a character’s',
        'radical and phonetic component',
        'and stroke count, so you can look it up by the Xinhua Dictionary radical-index method, or check whether the handwriting is standard.',
        'Before data entry or typesetting, verify a rare character’s',
        'code point and input-method encoding, to avoid garbled text, missing glyphs, or picking a wrong homograph (e.g. the triplet qí / zhī / zhǐ).',
        'Look up the pronunciation and structure of a character',
        'Enter xī: pinyin xī (1st tone), radical sun (rì), 20 total strokes, left-right structure, Unicode U+66E6; this places it under the sun radical with 16 remaining strokes, and helps confirm it is the common form meaning “morning light”.',
        'Does it list all readings of a polyphone?',
        'It lists the common readings of polyphones with notes on meaning differences — for example the character read as háng (bank) or xíng (to walk) — so you can choose the right sound by context.',
        'Which standard defines the radical and stroke count?',
        'By default it takes the radical and standard stroke count from the General Standard Chinese Character List and the Standard Stroke Order of Commonly Used Characters in Modern Chinese, consistent with mainstream dictionaries and input methods.',
        'Can the results be used for calligraphy or literacy teaching?',
        'It can support teaching with glyph structure and stroke counts, but for the standard stroke order we recommend checking against',
        'the animation tool for comparison.',
        'About Chinese Character Query',
        'Chinese Character Query is a fully offline, client-side tool: enter a single character to get its pinyin, radical, stroke count, glyph structure, and input-method encoding, helping with literacy, dictionary lookup, and standard-handwriting verification.',
        'Pinyin & polyphones: shows pronunciation and marks polyphones with contextual meanings',
        'Radical & strokes: gives the radical and total strokes for radical-index lookup',
        'Encoding lookup: provides Unicode and Wubi / Zhengma input-method codes to avoid garbled or missing glyphs',
        'Unfamiliar characters while reading: instantly see pinyin, radical, and strokes to grasp sound and shape',
        'Homework help: verify radical and stroke count, check handwriting standard',
        'Data entry proofreading: confirm rare-character code points and encodings, avoid wrong homographs',
        'Type or paste a single Chinese character',
    ]))

    # ===== chinese-culture (61) =====
    write('chinese-culture', build('chinese-culture', [
        'Chinese Culture Toolkit',
        'Classical poetry / Idiom chain / Stroke count / Cognitive biases / Famous quotes / Moral dilemmas',
        'View the Chinese Culture Toolkit User Guide',
        'Classical Poetry',
        'Idiom Chain',
        'Stroke Count',
        'Cognitive Biases',
        'Famous Quotes',
        'Moral Dilemmas',
        'By dynasty',
        'By type',
        'By author',
        'Random poem',
        'Mode: Player vs AI',
        'Player-vs-AI mode: you enter an idiom and the AI continues the chain. Machine-quiz mode: the AI gives an idiom and you respond.',
        'Combo',
        'Time (s)',
        'Start chain',
        'Enter an idiom to start the chain',
        'Includes stroke-count data for 1000+ common characters. Enter a character or word to look up each character’s stroke count and the total.',
        'Decision biases',
        'Memory biases',
        'Social biases',
        'Probability biases',
        'Draw a random card',
        'Life',
        'Study',
        'Motivation',
        'Philosophy',
        'Wisdom',
        'Emotion',
        'Random dilemma',
        'Previous',
        'Next',
        'Click “Random dilemma” to start exploring',
        'Deep Dive: Chinese Culture Toolkit',
        'When writing or speaking and you want a fitting idiom, search by keyword to get its definition, source, and near / opposite terms, avoiding misreading it from its form or using it in the wrong context.',
        'Near traditional festivals like Spring Festival, Dragon Boat, or Mid-Autumn, check the festival’s origin, customs, and corresponding lunar date, for copywriting, event planning, or telling traditions to children.',
        'When appreciating classical poetry, search by author, dynasty, famous lines, and creative background, or verify the dates and phenology of the 24 solar terms, to support cultural study.',
        'Look up the source of the idiom “shou zhu dai tu”',
        'Enter “shou zhu dai tu” (waiting by a stump for a hare): meaning — a metaphor for sticking to past experience and refusing to adapt; source — Hanfeizi (Wudu); near term “ke zhou qiu jian” (marking the boat to find the sword); opposite “sui ji ying bian” (act according to circumstances); useful as a reminder to adapt to the situation.',
        'Which cultural modules does the toolkit include?',
        'Typically an idiom dictionary, classical-poetry search, traditional festivals and solar terms, and name culture; see the page’s available modules for specifics. Fully offline, client-side lookup — data is not uploaded.',
        'Does poetry search support filtering by author or dynasty?',
        'Yes — by author, dynasty, and famous-line keywords, convenient for thematic appreciation or teaching examples; results are compiled from public classics.',
        'Why do festival dates sometimes differ from the Gregorian calendar?',
        'Spring Festival, Dragon Boat, and Mid-Autumn follow the lunar calendar, so their Gregorian dates shift year to year; use the',
        'tool to convert precisely to the corresponding day of a specific year.',
        'About the Chinese Culture Toolkit',
        'The Chinese Culture Toolkit gathers small tools for Chinese culture — idiom definitions and sources, classical-poetry search, traditional festivals and solar terms, and name culture — a fully offline, client-side lookup that lets you understand the language, culture, and allusions behind Chinese characters in one place.',
        'Idiom allusions: look up definition, source, and near / opposite terms to avoid misreading',
        'Poetry search: filter by author, dynasty, and famous-line keywords, and view creative background',
        'Festival facts: check traditional-festival origins, customs, and the 24 solar terms’ phenology',
        'Writing & speeches: pick a fitting idiom and verify its source and context',
        'Festival planning: check festival origins, customs, and lunar dates to arrange activities',
        'Cultural study: search poetry background and solar-term meanings to aid appreciation',
        'Search poem title, author, or content...',
        'Enter a four-character idiom...',
        'Enter a character or word to look up stroke count...',
        'Search cognitive biases...',
        'Search quotes...',
    ]))

    # ===== chinese-radical-lookup (19) =====
    write('chinese-radical-lookup', build('chinese-radical-lookup', [
        'Radical Lookup',
        'Enter a character to show common radicals and structure references (static, offline).',
        '/ Radical Lookup',
        'View the Radical Lookup User Guide',
        'Radical Lookup: search characters by radical, view the radical’s pronunciation, stroke count, and common characters containing it, based on the Xinhua Dictionary radical-index method. Fully offline, client-side lookup.',
        'Character (single character supported)',
        'Deep Dive: Radical Lookup',
        'When you only know a character’s rough radical (e.g. the water radical, wood radical, or heart radical), use radical search to list same-radical characters, then narrow down by remaining strokes to find the target — completing a dictionary lookup.',
        'In literacy teaching, explain the pattern of phonetic compounds: judge a character’s meaning category by its radical (semantic component) — e.g. the speech radical relates to words, the metal radical relates to metals — aiding understanding and memory.',
        'When practicing calligraphy or proofreading, confirm which radical a character belongs to and how many strokes it has, avoiding wrong radical splits (e.g. the character jing belongs to the grass radical, not the knife radical).',
        'Look up characters under the wood radical',
        'Enter the wood radical (4 strokes): it lists same-radical characters like yang, liu, song, bai, tao, li, and marks the radical’s pronunciation mù and meaning “tree”; you can narrow further by remaining strokes.',
        'How do I use the radical-index method?',
        'First determine the character’s radical and count its strokes, find the page in the radical index, then count the remaining strokes after removing the radical, and locate the character in the matching stroke table.',
        'Is a phonetic compound’s radical always its semantic component?',
        'Mostly the semantic component (the meaning radical), e.g. the water radical in “river”; but some characters are indexed by convention (e.g. the character zai is indexed under the earth radical) — follow the dictionary’s radical rules.',
        'What if a rare radical cannot be found?',
        'Switch to the hard-to-index table or search by total strokes; this tool covers common radicals of general-standard characters, so very rare radicals may be absent.',
        'For example: you',
    ]))

    # ===== lunar-calendar (36) =====
    write('lunar-calendar', build('lunar-calendar', [
        'Lunar ↔ Gregorian Converter',
        'Supports lunar queries for 1900–2100 · Sexagenary year · Zodiac · Solar terms · Suitable/Avoid',
        'Lunar conversion',
        '/ Lunar conversion',
        'View the Lunar ↔ Gregorian Converter User Guide',
        'Gregorian → Lunar',
        'Lunar → Gregorian',
        'Convert to lunar',
        'Leap month',
        'Convert to Gregorian',
        'Zodiac animal',
        'Constellation',
        'Weekday',
        'Day of year',
        'Suitable',
        'Avoid',
        'Deep Dive: Lunar ↔ Gregorian Converter',
        'Elders only remember the lunar birthday; enter the lunar date to convert to that year’s Gregorian date, planning the cake and gathering ahead to avoid miscalculating the shifting date each year.',
        'Check which Gregorian day a year’s Spring Festival, Dragon Boat, or Mid-Autumn falls on, or reverse from a Gregorian holiday to the lunar date, for holiday planning and custom preparation.',
        'Learn a day’s corresponding 24 solar terms (e.g. Beginning of Spring, Qingming) and sexagenary year (e.g. Year of Bingwu), for wellness, farming, or traditional date selection.',
        'The Gregorian date of Spring Festival 2026',
        'Enter lunar New Year’s Day (2026): converts to Gregorian 2026-02-17 (Tuesday), also showing the sexagenary year as Bingwu, convenient for arranging the holiday and reunion dinner.',
        'Why do lunar and Gregorian dates never line up each year?',
        'The lunar calendar sets months by moon phases and adds leap months to reconcile with the tropical year, while the Gregorian calendar sets the year by Earth’s orbit; their cycles differ, so the corresponding Gregorian date shifts yearly.',
        'Does a leap month affect date conversion?',
        'Yes. A leap-month year has 13 lunar months; conversion must follow that year’s leap-month rules, and this tool has built-in leap-month data for common years.',
        'Are the 24 solar terms based on the lunar or Gregorian calendar?',
        'Solar terms are set by the sun’s ecliptic longitude, so their Gregorian dates are relatively fixed (e.g. Qingming usually falls on April 4–6); this tool can mark them for reference.',
        'About Lunar Conversion',
        'The Lunar ↔ Gregorian Converter is a fully offline, client-side tool that converts dates both ways between lunar and Gregorian, and can look up traditional festivals, the 24 solar terms, and the sexagenary year — handy for arranging festivals, birthdays, and farming references.',
        'Two-way conversion: lunar ↔ Gregorian date conversion with built-in leap-month handling',
        'Festivals & solar terms: marks festivals like Spring Festival, Dragon Boat, Mid-Autumn, and the 24 solar terms',
        'Sexagenary year: shows the corresponding sexagenary year to aid traditional date selection',
        'Lunar birthday: convert to that year’s Gregorian date and plan the gathering ahead',
        'Holiday planning: check Spring Festival, Dragon Boat, Mid-Autumn Gregorian dates and prepare customs',
        'Solar-term reference: learn solar-term dates and phenology for wellness and farming',
    ]))

    # ===== stroke-order-viewer (19) =====
    write('stroke-order-viewer', build('stroke-order-viewer', [
        'Stroke Order Demo',
        'Local static demo: stroke order and structure hints for common, frequently used characters.',
        '/ Stroke Order Demo',
        'View the Stroke Order Demo User Guide',
        'Stroke Order Demo: enter a character to dynamically show the standard writing stroke order with per-stroke animation, marking the total stroke count and stroke names, based on the Standard Stroke Order of Commonly Used Characters in Modern Chinese. Fully offline, client-side rendering.',
        'Enter a single character',
        'View stroke order',
        'Deep Dive: Stroke Order Demo',
        'Children learning to write can trace characters like huo (fire), shui (water), and yong stroke by stroke along the animation, building correct starting, moving, and ending order, avoiding reversed strokes.',
        'Adults practicing calligraphy or penmanship can verify error-prone stroke orders (e.g. the character wan writes horizontal-turning-hook before left-falling; the character ji writes left-falling before horizontal-turning-left-falling), correcting long-standing mistakes.',
        'In teaching Chinese as a foreign language, demonstrate stroke order to international students with stroke-name explanations, lowering memorization difficulty and meeting standard-writing requirements.',
        'Demonstrate the stroke order of yong (the Eight Principles of Yong)',
        'Input yong (5 strokes): the animation shows, in order, dot → horizontal-turning-hook → horizontal-left-falling → left-falling → right-falling, the basic strokes of the Eight Principles of Yong; you can pause stroke by stroke to observe each direction.',
        'Which standard defines the stroke order?',
        'Based on the Standard Stroke Order of Commonly Used Characters in Modern Chinese and common writing habits, covering common standard characters; rare or variant characters may be absent.',
        'Can I slow down or pause stroke by stroke?',
        'Per-stroke demo with pause / replay is supported for tracing and teaching; see the page controls for specifics, fully offline, client-side rendering.',
        'What if the stroke order or count disagrees with the dictionary?',
        'First confirm you entered the standard simplified character; if a traditional or variant form is involved, the stroke order may differ — switch to the corresponding glyph and look it up again.',
    ]))


if __name__ == '__main__':
    main()

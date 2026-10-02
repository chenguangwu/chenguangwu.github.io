#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'language')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'language')
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
    out = {'slug': slug, 'industry': 'language', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('stats-2', build('stats-2', [
        "📊 Character Count (Chinese, English and Punctuation)",
        "With Chinese characters, English letters and punctuation",
        "Chinese characters + English words + numeric characters + punctuation marks + whitespace = total characters",
        "Counts Chinese characters, English words, numbers, punctuation and whitespace in the text separately, for word-count accounting, layout estimation and character-encoding verification. Text is processed only in the local browser and never uploaded.",
        "Text to count",
        "Ni hao, Hello world! 2026",
        "Count Characters",
        "📚 Deep Dive: Character Count (Chinese, English and Punctuation)",
        "Check submissions against journal word limits and tell total characters apart from visible characters",
        "Count Chinese characters, letters, digits and punctuation separately in mixed Chinese-English text",
        "Keep writing length under control and check platform character limits",
        "Category Breakdown",
        "Counting example: a sample text of 2 Chinese characters, 5 English letters, 4 digits and 1 punctuation mark gives 12 characters in total; counting visible characters only, without the newline and space, also gives 12.",
        "Chinese vs English",
        "The same passage of 500 Chinese characters is about 500 characters; translated into English it may be 350 words but roughly 2100 letters plus spaces. Conclusions differ depending on whether you count characters or words, so agree on the metric in advance.",
        "What Is the Difference Between Total and Visible Characters?",
        "Total characters include invisible control characters such as spaces and newlines; visible characters count only printed letters and punctuation, and submissions are often measured by visible word count.",
        "How Many Characters Is a Chinese Character?",
        "One Chinese character (including punctuation) usually counts as one character at the UTF-16 or code point level. One English letter counts as one character, and mixed text adds up separately.",
        "About Character Count (Chinese, English and Punctuation)",
        "Character Count (Chinese, English and Punctuation). A language and translation tool, processed entirely in the browser, works offline.",
        "Paste or enter the text to count here",
    ]))
    write('korean-hangul-decomposer', build('korean-hangul-decomposer', [
        "📊 Korean Hangul Decomposer",
        "Enter Korean text to see how each syllable is composed of its initial consonant, medial vowel and final consonant",
        "Decompose and analyze",
        "📖 Consonant Table",
        "📖 Vowel Table",
        "📚 Deep Dive: Korean Hangul Decomposer (Initial, Medial, Final)",
        "Enter Korean text and split it syllable by syllable into initial consonant, medial vowel and final consonant",
        "Understand the block structure of Hangul to aid literacy and typing",
        "Study the syllable encoding for teaching or input-method research",
        "Syllable Breakdown",
        "한 = initial ㅎ + medial ㅏ + final ㄴ; 사 = ㅅ + ㅏ (no final); 랑 = ㄹ + ㅏ + ㅇ. Each block combines these three elements.",
        "A Hangul syllable = 0xAC00 + initial index × 588 + medial index × 28 + final index. For example 한 (0xD55C) lets you reverse-derive the three elements, which helps with programmatic decomposition.",
        "Why Split Into Initial, Medial and Final?",
        "Hangul is a featural script, and each block is assembled from a consonant (initial), a vowel (medial) and an optional consonant (final). Being able to decompose a block lets you understand how any unfamiliar syllable is read.",
        "Is the Final Always a Consonant?",
        "The final (batchim) can only be one of the 27 valid final sounds (including forms such as ㅇ), and it may be empty. Vowels cannot serve as finals, and double finals are normalized to their representative sound.",
        "About Korean Hangul Decomposer",
        "Korean Hangul Decomposer is an online tool in the education and learning field. An education tool that supports study and improves efficiency.",
        "Enter Korean text...",
    ]))
    write('generator-19', build('generator-19', [
        "👤 Acronym Generator (Automatic Initials)",
        "Automatic initials",
        "The acronym concatenates the initial letter of each word in the phrase: acronym = first letter of word 1 + first letter of word 2 + … + first letter of word n. Letter case (all upper, initial capital, all lower) and the separator (none, hyphen, dot) are adjustable. When a phrase contains Chinese, the pinyin initial of each word is used. The acronym length equals the number of words, so for long phrases keep only 3 to 5 letters and add a digit or a suffix to avoid collisions.",
        "📚 Deep Dive: Acronym Generator",
        "Build an acronym from the initial of each word in a phrase (such as API)",
        "Adjust the",
        "and the separator, for naming and distilling terminology",
        "Produce candidate acronyms quickly when naming teams and projects",
        "Taking Initials",
        "\"Application Programming Interface\" takes the initials A, P, I, giving API in uppercase with no separator; \"natural language processing\" gives NLP.",
        "Separator Options",
        "The same phrase with a kebab separator gives A-P-I, and with lowercase gives api. Function words (of, and) can be skipped for a shorter acronym, e.g. \"Federal Bureau of Investigation\" gives FBI (skipping of).",
        "How Should Acronym Rules Be Defined?",
        "The common approach is to take the initial of each content word and skip function words such as a, the and of. Letter case and separation follow the style guide, for example camelCase for variables and all caps for brands.",
        "Can Ambiguity Arise?",
        "Yes, different phrases may share the same acronym (API and others). Formal naming should check for collisions to avoid clashing with existing acronyms.",
        "About Acronym Generator (Automatic Initials)",
        "Acronym Generator (Automatic Initials). A language and translation tool, processed entirely in the browser, works offline.",
    ]))
    write('phrase-translator', build('phrase-translator', [
        "🗣️ Common Phrase Translator",
        "Displays common Chinese and English expressions by category, with phonetic notation",
        "📚 Deep Dive: Common Phrase and Sentence Translation",
        "Look up idiomatic phrases and fixed collocations for travel and communication",
        "Take ready-made sentences by scenario (greetings, ordering, asking directions)",
        "Compare literal translation with the idiomatic phrasing",
        "Scenario Phrases",
        "\"How much is it?\" in English and ¿Cuánto cuesta? in Spanish; \"I don't understand\" in English and Je ne comprends pas in French.",
        "Avoid Literal Translation",
        "The literal rendering of the Chinese interjection meaning \"come on\" as cheer up is wrong; on the field of play it should be Go! or Come on!. Idiomatic phrases cannot be translated word for word, so memorize the fixed collocations.",
        "How Do Phrases Differ from Single Words in Translation?",
        "Phrases contain idioms and collocations, so literal translation is often wrong. Ready-made sentences stay idiomatic and can be applied directly in high-frequency situations.",
        "How Do I Learn Pronunciation?",
        "Combine phonetic notation or audio playback and shadow the speaker. Plain text translation carries no pronunciation, so use a separate pronunciation or phonetic tool.",
        "About Common Phrase Translator",
        "Common Phrase Translator is an online tool in the language and translation field. A language and translation tool, processed entirely in the browser, works offline.",
        "Search for a phrase...",
    ]))

if __name__ == '__main__':
    main()
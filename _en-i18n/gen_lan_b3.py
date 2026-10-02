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
    write('german-gender-quiz', build('german-gender-quiz', [
        "🏋️ German Noun Gender Quiz",
        "Practise the gender of German nouns (der/die/das) or look up the gender of a noun",
        "Practice mode",
        "Lookup mode",
        "der (masculine)",
        "die (feminine)",
        "das (neuter)",
        "Reset score",
        "Enter a noun to look up its gender",
        "📖 Gender Rule Cheat Sheet",
        "Ending",
        "Gender",
        "Months / seasons / directions",
        "-e (multisyllabic)",
        "Infinitive of a verb",
        "Most nouns ending in -en",
        "📚 Deep Dive: Quiz on German Noun Genders (der/die/das)",
        "Get random nouns and practise the definite articles der (masculine), die (feminine) and das (neuter)",
        "Learn common gender patterns (for example -ung/-heit are feminine, -chen is neuter)",
        "Consolidate noun and article pairings after a mistake",
        "Gender Patterns",
        "Nouns ending in -ung, -heit, -keit or -schaft are mostly feminine (die); nouns ending in -chen or -lein are neuter (das); nouns ending in -er are often masculine (der), but there are many exceptions worth memorizing.",
        "How to Use the Quiz",
        "For the noun Haus you should pick das (neuter); for Frau pick die (feminine); for Mann pick der (masculine). Wrong words go into the review queue.",
        "Is There a Pattern in German Noun Genders?",
        "Partly (suffixes and meaning, such as seasons being mostly masculine and most metals neuter), but roughly one third has to be memorized outright. Nouns always start with a capital letter.",
        "Does Getting the Gender Wrong Matter Much?",
        "It affects the article, the adjective ending and pronoun agreement. German nouns always take an article, so a wrong gender throws off the case endings of the whole sentence.",
        "About German Noun Gender Quiz",
        "German Noun Gender Quiz is an online tool in the education and learning field. An education tool that supports study and improves efficiency.",
        "Enter a German noun, e.g. Haus, Blume, Kind...",
    ]))
    write('ipa-practice', build('ipa-practice', [
        "🎮 IPA Pronunciation Practice",
        "Learn the International Phonetic Alphabet (IPA). Tap a symbol to see how it is pronounced with examples, and play audio",
        "Browse and learn",
        "Practice quiz",
        "Tap a symbol below to read its detailed pronunciation notes",
        "Vowels",
        "Monophthongs",
        "Diphthongs",
        "Consonants",
        "Plosives",
        "Fricatives",
        "Affricates",
        "Nasals",
        "Laterals and approximants",
        "What is the pronunciation description of this symbol?",
        "📚 Deep Dive: IPA Phonetic Alphabet Practice",
        "Practise the pronunciation and discrimination of English and general IPA vowels and consonants",
        "Listen to minimal pairs on the symbol cards and tell them apart (/i/ vs /ɪ/)",
        "Correct pronunciation deviations caused by dialect or negative transfer from the native language",
        "Minimal Pairs",
        "ship /ʃɪp/ vs sheep /ʃiːp/: the difference lies in /ɪ/ (short) and /iː/ (long); bit /bɪt/ vs beat /biːt/ works the same way. Practise long vowels against lax vowels.",
        "Voicing of Consonants",
        "/s/ (voiceless) vs /z/ (voiced), /p/ vs /b/. Put a hand on your throat to feel the vocal fold vibration of voiced sounds; this is a common confusion for Mandarin speakers.",
        "What Is the IPA Used For?",
        "It is a single set of symbols that transcribes the pronunciation of any language precisely. The /.../ in a dictionary entry is phonetic transcription, and it reflects actual pronunciation far better than spelling does.",
        "Do British and American IPA Differ a Lot?",
        "The phonetic systems differ (for example the American rhotic r and letter pronunciation differences), but both share the IPA. When checking a dictionary, look at whether it is transcribed in British English (RP) or American English (GA).",
        "About IPA Pronunciation Practice",
        "IPA Pronunciation Practice is an online tool in the education and learning field. An education tool that supports study and improves efficiency.",
    ]))
    write('text-polisher', build('text-polisher', [
        "🌍 Text Polishing Tool",
        "Local processing: full-width and half-width forms, extra spaces, punctuation normalization, character count, synonym replacement",
        "Text Polishing",
        "/ Text Polishing",
        "Polishing rewrites along four dimensions: fluency (split long sentences, keeping each single sentence between 20 and 40 characters), word choice (replace colloquial words and repetitions), tone consistency (uniformly formal or friendly), and logical cohesion (add connectives and clear references). For readability, an average sentence length of 25 to 40 characters and a rare-word share below 5% count as easy to read. The rewrite depth is divided into three levels: light (synonym swap), medium (sentence restructuring) and deep (paragraph reorganization).",
        "This is a  test text, and it contains  extra spaces . When Chinese and English are  mixed , punctuation is easy to get wrong .",
        "Remove extra spaces",
        "Normalize Chinese punctuation",
        "Convert full-width to half-width (letters and digits)",
        "Remove blank lines",
        "Trim leading and trailing spaces",
        "Insert a space between Chinese and English",
        "✨ One-Click Polish",
        "Polished result",
        "💡 Synonym replacement: select Chinese words in the output text and the system recommends replacements from the local thesaurus.",
        "📚 Deep Dive: Text Polishing Tool",
        "Official documents and emails: turn a colloquial, wordy draft into formal, concise written English while preserving the original meaning and avoiding ambiguity.",
        "Papers and reports: reduce similarity and improve fluency, avoiding a stiff machine-translation tone and raising professional readability.",
        "Social media copy: improve flow and appeal while keeping the intended tone, so the expression reads more naturally.",
        "Email Polishing Example",
        "Original: \"please deal with that thing as soon as possible\" becomes polished: \"We would appreciate your prompt follow-up on this matter\". Notes: removes colloquial wording, supplies the subject, makes the action explicit, and reads more formal without losing politeness.",
        "Does Polishing Change the Original Meaning?",
        "By default only the expression is adjusted and the meaning is preserved. When a sentence is ambiguous, the original is kept and a note is given so you can confirm the final wording.",
        "Which Styles Are Supported?",
        "Common options include formal, concise, fluent and de-colloquialized. You can pick by scenario, and the output lists the main edits so you can review them one by one.",
        "About Text Polishing",
        "Text polishing is an online tool for writing and creation. A writing tool that helps improve both the efficiency and the quality of your text.",
        "Paste the text you want to polish here...",
    ]))
    write('french-verb-conjugator', build('french-verb-conjugator', [
        "📚 French Verb Conjugator",
        "Enter the infinitive form of a French verb to see its conjugation across tenses and persons",
        "Look up conjugation",
        "Tap a common verb below for a quick lookup",
        "⚡ Common Verbs",
        "Verb Grouping Rules",
        "Group 1 (-er)",
        ": the largest group, with uniform conjugation rules, such as parler, aimer, commencer",
        "Group 2 (-ir)",
        ": verbs ending in -ir take -issons in the plural of the present tense, such as finir, choisir, grandir",
        "Group 3 (irregular)",
        ": includes endings such as -re and -oir and conjugates irregularly, such as avoir, etre, aller, faire",
        "📚 Deep Dive: French Verb Conjugator",
        "Enter an infinitive to look up conjugation in the indicative, conditional and subjunctive",
        "Memorize the personal endings of the three regular groups -er, -ir and -re",
        "Look up common irregular verbs such as avoir, être and aller",
        "Group 1 -er in the present tense",
        "parler in the present indicative: je parle / tu parles / il parle / nous parlons / vous parlez / ils parlent. Uniformly drop -er and add -e, -es, -e, -ons, -ez, -ent.",
        "Irregular verbs",
        "avoir in the present tense: j'ai / tu as / il a / nous avons / vous avez / ils ont. A high-frequency irregular verb that needs separate memorization.",
        "How Many Groups Do French Verbs Have?",
        "Mainly three: -er (the largest, uniformly regular), -ir (such as finir to finis) and -re (such as rendre to rends), plus high-frequency irregular verbs like être, avoir and aller.",
        "When Is the Subjunctive Used?",
        "It expresses doubt, wish and emotion in main and subordinate clauses (such as il faut que + subjonctif). It does not share the tense system of the indicative and is triggered by the sentence pattern.",
        "About French Verb Conjugator",
        "French Verb Conjugator is an online tool in the education and learning field. An education tool that supports study and improves efficiency.",
        "Enter a verb infinitive, e.g. parler, finir, avoir...",
    ]))

if __name__ == '__main__':
    main()
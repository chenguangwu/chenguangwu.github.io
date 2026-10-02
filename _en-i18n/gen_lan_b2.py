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
    write('spanish-accent-rules', build('spanish-accent-rules', [
        "🦷 Spanish Accent Position Checker",
        "Enter a Spanish word to automatically determine the stress position, syllable division, and whether an accent mark is required",
        "Analyze Stress",
        "Enter a word, then click Analyze",
        "📖 Accent Rules Explained",
        "Rule 1: Ends in a vowel, n, or s",
        "Words ending in a vowel (a, e, i, o, u) or in the consonants n and s place the stress on the",
        "penultimate syllable",
        "Rule 2: Ends in any other consonant",
        "Words ending in a consonant other than n or s place the stress on the",
        "last syllable (final syllable)",
        "Rule 3: The accent mark (´)",
        "When the stress does not fall on the default position above, an accent mark is mandatory. In a word carrying an accent mark, the stressed syllable is exactly the one holding the mark.",
        "Rule 4: Diphthongs and triphthongs",
        "In a diphthong (ai, au, ei, eu, ia, ie, io, iu, ou, ua, ue, uo, ui), a strong vowel (a, e, o) combined with a weak vowel (i, u) counts as one syllable, and two weak vowels also count as one syllable. Two strong vowels next to each other belong to separate syllables.",
        "📚 Deep Dive: Spanish Accent Rules (Quick Reference)",
        "Check whether a word needs an accent mark (á/é/í/ó/ú/ñ)",
        "Tell apart the spelling of heteronyms such as el/él and si/sí",
        "Confirm the stress class before running a spelling check",
        "Heteronyms",
        "el (definite article, no accent) vs él (he, accented); si (if) vs sí (yes, stressed on the final syllable). Meaning depends on the accent.",
        "Deciding the Spelling",
        "café ends in a consonant with final stress, so mark é; libro ends in a vowel with penultimate stress, so no mark. Repeated practice internalizes the rule.",
        "Does the accent mark only go on vowels?",
        "Yes. In Spanish the accent mark is added only to a, e, i, o, u (ñ is an independent letter, not an accented vowel); á indicates that the syllable is stressed.",
        "Do question words always take an accent?",
        "Yes. Interrogative and exclamative words (qué, cuándo, dónde) always carry an accent to distinguish them from relative words (que, cuando); this is fixed usage.",
        "About Spanish Accent Position Checker",
        "Spanish Accent Position Checker is an online tool in the education and learning field. An education tool that supports study and improves efficiency.",
        "How to Use Spanish Accent Position Checker",
        "Enter a word, e.g. casa, lápiz, español...",
        "What Does Spanish Accent Position Checker Do?",
        "Spanish Accent Position Checker automatically analyzes the stress position and syllable division of a Spanish word and decides whether an accent mark (tilde) is required, applying the spelling stress rules to support orthography and pronunciation study.",
        "How Do I Use Spanish Accent Position Checker?",
        "What Scenarios Suit Spanish Accent Position Checker?",
        "Spanish accent rules classify words by how many syllables come after the ending: a vowel or n/s ending puts the stress on the penultimate syllable (llana, normally unmarked), other endings stress the final syllable (aguda, which needs an accent mark); stress on the antepenultimate syllable (esdrújula) always takes a mark.",
        "The result marks the stress position of the word and whether an accent mark is needed; interrogative and exclamative words (qué, quién) take extra marks. The rules are general, proper nouns excepted.",
        "Enter a word, e.g. casa, lápiz, español...",
    ]))
    write('riyuwushiyintulianxi-dianjifayin', build('riyuwushiyintulianxi-dianjifayin', [
        "🎮 Japanese Kana Chart Practice (Click to Hear)",
        "Click a kana card to hear its pronunciation and see the romanization; hiragana/katakana switching and listen-and-pick practice are supported",
        "📐 Notes",
        "Gojuon = あ(a) か(ka) さ(sa) た(ta) な(na) は(ha) ま(ma) や(ya) ら(ra) わ(wa) ん(n)",
        "The kana chart is the foundation of Japanese pronunciation: 45 plain sounds plus the syllabic nasal ん, extended by voiced sounds, semi-voiced sounds and digraphs. Clicking a card calls SpeechSynthesis to read it aloud (the browser needs a Japanese voice; when unsupported, the romanization is shown instead).",
        "Hiragana",
        "Katakana",
        "Listen and choose: romanization",
        "(Click the speaker below to replay)",
        "Correct: ",
        "/ ",
        "Accuracy: ",
        "💡 Tip: pronunciation relies on the browser speech synthesizer; if you hear nothing, check whether the system has a Japanese voice pack installed. Practice mode draws 4 random candidates each round.",
        "Click a card to read out the corresponding kana",
        "Pronunciation quality depends on the browser and the system voice pack",
        "📚 Deep Dive: Japanese Kana Chart Practice (Click to Hear)",
        "Click kana to hear them and drill hiragana/katakana recognition",
        "Memorize row by row (a-row, ka-row and so on)",
        "Compare where plain, voiced and digraph sounds sit",
        "Structure of the Kana Chart",
        "a-row a/i/u/e/o, ka-row ka/ki/ku/ke/ko... 46 base sounds in total (including ん); hiragana derives from cursive Chinese characters and katakana from their radicals, e.g. ア comes from the left-ear component of a Chinese character.",
        "Voiced and Digraph Sounds",
        "adding voicing dots to the ka-row gives が ga/gi/gu/げ ge/ご go; digraphs such as きゃ kya, きゅ kyu and きょ kyo are formed from a consonant plus a small ya-row.",
        "When Do You Use Hiragana and When Katakana?",
        "Hiragana covers native words and grammar, katakana covers loanwords and onomatopoeia. The two sound the same but look different, so recognize both.",
        "Why Is It Called Fifty Sounds Rather Than Fifty?",
        "45 plain sounds plus ん makes 46. The traditional name gojuon refers to the historical full chart, while the actual base pronunciation is 46 sounds, extended by voiced, semi-voiced and digraph sounds.",
        "About Japanese Kana Chart Practice (Click to Hear)",
        "Japanese Kana Chart Practice (Click to Hear). A language and translation tool, processed entirely in the browser, works offline.",
        "How to Use Japanese Kana Chart Practice (Click to Hear)",
        "What Does Japanese Kana Chart Practice (Click to Hear) Do?",
        "The Japanese kana chart practice tool drills hiragana and katakana through click-to-hear, covering plain and voiced sounds and supporting listen-and-repeat, which suits beginners studying Japanese on their own.",
        "How Do I Use Japanese Kana Chart Practice (Click to Hear)?",
        "What Scenarios Suit Japanese Kana Chart Practice (Click to Hear)?",
    ]))
    write('idiom-solitaire', build('idiom-solitaire', [
        "🎮 Idiom Chain Game",
        "The system sets the prompt and you keep the chain going. Enter an idiom starting with the given character and see how long your chain runs",
        "/ Idiom Chain",
        "Chain Mode",
        "Exact-character chain",
        "Homophone chain",
        "Time limit per prompt (seconds)",
        "15s",
        "20s",
        "30s",
        "Idioms chained",
        "Click to start the game",
        "Skip (no score)",
        "End the game",
        "Your chain",
        ": the first character of the next idiom must be exactly the same as the last character of the previous idiom.",
        ": the first character of the next idiom only needs to sound the same as the last character of the previous idiom.",
        "Answer within the time limit; the game ends when the time runs out or the input is not an idiom. Skipping costs no points but earns none.",
        "📚 Deep Dive: Idiom Chain (Word Game)",
        "Chain the next idiom from the final character to build vocabulary and reaction speed",
        "Switch between the homophone and exact-character rules",
        "Interactive idiom practice for families and classrooms",
        "Chaining Rule",
        "yi fan feng shun goes to shun li zhang chang, then to zhang ju zhi tu. The final character shun can take shun... or the homophones shun and shun. The rule can require the same character or the same sound.",
        "Pitfall",
        "A final character with multiple readings or a rare one (such as wei, read two ways) easily blocks the chain. Allow homophones to relax it, or restrict the idiom pool to common idioms for smoother play.",
        "Does the Chain Use the Final Character or the Sound?",
        "Two common variants: strictly the same final Chinese character, or only the same sound (tone included). Teaching usually prefers the same character to also drill writing.",
        "What If You Get Stuck?",
        "Allow homophones, look up an idiom dictionary, or change the rule (for example limit idioms to a theme). For pure fun there is no need to insist on a unique solution.",
        "About Idiom Chain Game",
        "Idiom Chain Game is an online tool in the education and learning field. An education tool that supports study and improves efficiency.",
        "Enter an idiom starting with the given character...",
    ]))
    write('index', build('index', [
        "🌍 Language and Translation Tools",
        "Language and Translation",
        "Language and Translation Tools",
        "Generate an acronym from the initial letters of a phrase (such as API), with adjustable letter case and separator, useful for naming and distilling terminology. Generated entirely in the browser and ready to copy.",
        "A common-phrase translation tool that displays everyday Chinese and English expressions with phonetic notation across greetings, travel, dining and more, supports one-click copy, and suits travel abroad and quick language reference.",
        "Uses a built-in dictionary to translate word by word or phrase by phrase among Chinese, English, Japanese, Korean, French, German and Russian. Data is processed locally with no network needed, suitable for offline lookup and for comparing simple sentences.",
        "A grammar checker that detects common grammar, punctuation and collocation problems in Chinese and English text and suggests revisions, suitable for polishing writing, proofreading papers and improving everyday copy.",
        "A vocabulary learning tool that applies spaced repetition to help you memorize English words efficiently, supporting card-based study and review schedules. Suitable for exam preparation, vocabulary building and daily English study.",
        "The Japanese kana chart practice tool drills hiragana and katakana through click-to-hear, covering plain and voiced sounds and supporting listen-and-repeat, which suits beginners studying Japanese on their own.",
        "Reading Speed Test",
        "Enter the number of words read within a period and the time spent, and the tool computes words per minute (WPM), then compares the result with standard models to give a reading level reference that helps assess reading efficiency and training direction.",
        "Uses a sample test or a known ratio of recognized words to estimate your English vocabulary range (such as 3000-5000) by statistical method. Useful as a reference when self-assessing and planning a memorization plan.",
        "A character count tool that precisely counts Chinese characters, Latin letters, digits and punctuation in the text and distinguishes total characters from visible characters. Suitable for controlling writing length, paper formatting and word count checks.",
        "Text Polishing",
        "Text polishing is a free online language and translation tool, and also an online tool for writing and creation. A writing tool that helps improve both the efficiency and the quality of your text. Runs entirely in the browser, uploads no data and needs no registration, ready to use as soon as the page opens.",
        "Look up the grammatical gender of German nouns (der/die/das), and use practice mode to decide the article from the ending or the meaning, which helps remember noun-article pairings. A standard drill for beginners in German.",
        "Enter a French verb in its infinitive form and the tool lists its conjugation table across the indicative, conditional and subjunctive moods and tenses, with shortcuts for common verbs. Suitable for French learners.",
        "Spanish Accent Position Checker automatically analyzes the stress position and syllable division of a Spanish word and decides whether an accent mark (tilde) is required, applying the spelling stress rules to support orthography and pronunciation study.",
        "Korean Hangul Decomposer",
        "Enter Korean text and split it syllable by syllable into initial consonant, medial vowel and final consonant, showing the Hangul composition structure visually for Korean study and input research.",
        "Tap an IPA phoneme to see the place of articulation, the manner and example words, with speech playback for shadowing, helping English and linguistics learners master standard phoneme pronunciation.",
        "The system gives an idiom and you must enter a new idiom starting with the final character of that idiom. The tool verifies whether the first and last characters match and counts the chain length, for idiom accumulation and enjoyable language practice.",
        "English Irregular Verbs · Root and Affix Memory Cards · Japanese Kana · Acronym Builder · Hello in Many Languages · Character Count",
        "About Language and Translation Tools",
        "This collection gathers 17 free online tools covering the common calculation, conversion and lookup needs of language and translation scenarios. Whether you are a practitioner, a student or an ordinary user, you will find a ready-to-use utility here. Every tool runs entirely in the browser and uploads no data to the server, so your privacy is protected.",
        "The language and translation tools included on this page are (representative tools):",
        "These tools help you finish common language and translation tasks quickly, with no formulas to memorize and no manual conversion needed. Enter and you get the result.",
        "Do the language and translation tools require a download or registration?",
        "No. Every tool on this page runs entirely in the browser. Open the page and use it right away, with nothing to install, no account to create, and no data uploaded.",
        "Are the results of the language and translation tools accurate? Is my data safe?",
        "Each tool computes locally in your browser from public mathematical formulas and general industry standards, so results are available instantly. All computation happens on your own device, nothing is uploaded to the server, and your privacy is fully protected.",
    ]))

if __name__ == '__main__':
    main()
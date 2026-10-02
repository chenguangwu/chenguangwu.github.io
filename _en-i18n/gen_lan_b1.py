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
    write('language-toolkit', build('language-toolkit', [
        "📖 Language Learning Toolkit",
        "English irregular verbs · root and prefix cards · Japanese kana · initial acronyms · greetings in many languages · character count",
        "📖 Irregular Verbs",
        "🧠 Roots and Affixes",
        "🌸 Kana Chart",
        "🔤 Initial Acronyms",
        "🌍 Greetings in Many Languages",
        "🔢 Character Count",
        "Base form",
        "Past tense",
        "Past participle",
        "Chinese meaning",
        "Click any row to copy the three forms of that verb; 120+ common irregular verbs are included.",
        "🔄 Flip the card",
        "🔀 Draw a random card",
        "Root",
        "See",
        "Click a card to flip it · view the meaning and example words",
        "Voiceless",
        "Voiced",
        "Semi-voiced",
        "Yōon",
        "Click any kana to see its romanization; you can enter practice mode below.",
        "✏️ Practice mode",
        "Type the romanization of the kana below:",
        "Enter text (Chinese or English)",
        "ALL CAPS",
        "Generate acronyms",
        "All language families",
        "Includes \"hello\" in 100 languages; click a card to copy the greeting.",
        "Hanzi count",
        "Digit count",
        "English word count",
        "Sentence count",
        "📚 Deep dive: Language Learning Toolkit (collection)",
        "Call translation, vocabulary, phonetics and conjugation sub-tools from one place",
        "Pick the right tool for the task (memorize words / fix pronunciation / check grammar)",
        "Build your own language learning workflow",
        "Task mapping",
        "Vocabulary→vocabulary-builder; pronunciation→ipa-practice; conjugation→french-verb-conjugator; stress→spanish-accent-rules; combine as needed.",
        "Workflow",
        "Reading foreign articles: first rough-translate with translator → check sentence patterns with grammar-checker → collect new words with vocabulary-builder → drill pronunciation with ipa-practice, closing the learning loop.",
        "How is the toolkit different from an ordinary translator?",
        "It goes beyond translation to cover memorization, pronunciation, grammar and culture, which suits systematic learning rather than a one-off lookup.",
        "Is any data uploaded?",
        "Most tools in this kit are pure front end and process text locally; the translation features call external interfaces, so mind the sensitivity of the content.",
        "About \"Language Learning Toolkit\"",
        "The Language Learning Toolkit is a language translation tool that runs entirely in the front end and supports offline use.",
        "Search verbs (English or Chinese)...",
        "Enter romanization (for example a)",
        "For example: World Health Organization\nor: People's Republic of China",
        "Search for a language name or greeting...",
        "Paste or type the text you want to count...",
    ]))

    write('calc-1', build('calc-1', [
        "📖 English Vocabulary Size Estimate",
        "Estimate the range of your English vocabulary through a sampling test or a known recognition rate.",
        "Vocabulary estimate = f(test accuracy, word list)",
        "Sampling test",
        "By recognition rate",
        "Below are 20 English words of varying difficulty. Tick the ones you recognize and the tool will estimate your vocabulary size from the sampling result.",
        "Select all known",
        "Select all unknown",
        "Estimate vocabulary size",
        "Recognition rate (%)",
        "Baseline total words",
        "General English 20000 words",
        "Common 10000 words",
        "Basic 5000 words",
        "Core 3000 words",
        "📋 Vocabulary level reference",
        "Vocabulary range",
        "Approximate level",
        "Beginner",
        "Basic everyday communication",
        "Junior/high school level",
        "College English CET-4/CET-6",
        "IELTS/TOEFL preparation",
        "Advanced/academic English",
        "Close to native speaker",
        "The sampling test is an entertainment estimate, not a professional assessment tool.",
        "Ticking the words you truly know improves the accuracy of the estimate.",
        "📚 Deep dive: English Vocabulary Size Estimate (sampling statistics)",
        "Tick the recognized share of 20 stratified sample words to estimate the total vocabulary range",
        "Set a memorization plan after self-testing (for example a target of 5000/8000)",
        "Compare different word lists (general/IELTS/TOEFL) to see the coverage gap",
        "Ratio to total",
        "Knowing 14 of 20 sampled words (70%) against a 20000-word reference list gives an estimated vocabulary of about 14000; a common concise dictionary covers 80% of text with about 3000 core words, so knowing 70% of the sample already exceeds the basic threshold.",
        "Understanding the range",
        "Sampling has random error, so the result is a range rather than a fixed value; knowing 16/20 (80%) and 14/20 (70%) differ by 10 percentage points but the totals may differ by 2000 words, which is normal fluctuation.",
        "Why does the sampling use 20 words?",
        "Too few gives large error and too many wastes time; 20 words balance reliability and efficiency, and sampling stratified by difficulty (high frequency to low frequency) is more accurate.",
        "Can the estimate serve as my real vocabulary size?",
        "It only estimates passive vocabulary (recognizing a word's meaning); active reuse (speaking and writing) is usually smaller. Since how strictly you judge \"known\" also affects the result, treat it as a reference rather than an exact number.",
        "About \"English Vocabulary Size Estimate\"",
        "Vocabulary size is one important indicator of English ability. This tool gives a rough vocabulary range and a matching level reference through a sampling test or a recognition rate.",
        "Two estimation modes available",
        "Built-in graded sampling word list",
        "Automatic level range output",
        "Simple to operate with instant feedback",
        "English learning self-assessment",
        "Baseline test before exam preparation",
        "Making a vocabulary study plan",
    ]))

    write('calc-2', build('calc-2', [
        "🏎️ Reading Speed Test",
        "Enter the number of characters read and the time taken to compute your reading speed, with a level reference.",
        "Reading speed = characters / time",
        "Characters read",
        "Self-rated comprehension (%)",
        "Time taken (minutes)",
        "Extra seconds",
        "Calculate speed",
        "Reading speed = total characters / total time in minutes. The higher the self-rated comprehension, the more meaningful the effective reading speed.",
        "📋 Reading speed level reference",
        "Speed range (characters/minute)",
        "Level description",
        "Basic reading speed",
        "Normal reading speed",
        "Good reading speed",
        "Fairly fast reading speed",
        "Fast reading speed",
        "Very fast / skimming reading",
        "Test with a full article rather than a single paragraph to get a more accurate result.",
        "Reading speed should be judged together with comprehension.",
        "📚 Deep dive: Reading Speed Test (WPM)",
        "Enter characters and time to compute words per minute (WPM)",
        "See the effective rate together with the comprehension self-rating",
        "Reading speed",
        "Track speed changes before and after training to measure progress",
        "WPM calculation",
        "Reading 3000 characters in 10 minutes gives WPM = 3000/10 = 300 characters/minute; Chinese native readers commonly reach 200-500 characters/minute, and mid-to-high comprehension is the healthiest combination.",
        "Comprehension correction",
        "At the same 300 characters/minute, a low comprehension self-rating (<60%) means skimming rather than effective reading. Improvement should balance comprehension, not chase speed alone.",
        "How is WPM computed?",
        "WPM = total characters / total time in minutes; English usually counts words while Chinese counts characters, so cross-language comparison must state the unit.",
        "What speed counts as good?",
        "There is no absolute standard; comprehension is what matters. Blindly raising speed is useless if comprehension collapses, so aim for your personal best speed while keeping comprehension above 80%.",
        "About \"Reading Speed Test\"",
        "Reading speed is an important indicator of reading efficiency. This tool quantifies how many characters you read per minute and, together with your comprehension self-rating, gives an effective reading speed reference.",
        "Supports precise input in minutes and seconds",
        "Built-in timer to assist the test",
        "Assesses effective speed together with comprehension",
        "Provides graded reading level reference",
        "English/Chinese reading training assessment",
        "Timed reading practice before exams",
        "Self-check of learning efficiency",
        "Before and after comparison for speed reading courses",
    ]))

if __name__ == '__main__':
    main()

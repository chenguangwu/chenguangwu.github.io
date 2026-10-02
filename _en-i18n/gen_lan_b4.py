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
    write('grammar-checker', build('grammar-checker', [
        "📝 Grammar Check",
        "Detect common grammar problems in Chinese and English text",
        "Uses a dual detection approach combining rules and statistical models. Common issues include mixed Chinese and English punctuation, missing sentence components, subject-verb disagreement, inappropriate collocations and the same word recurring within 20 characters. Each issue reports its position offset along with a revision suggestion. Issue density = number of issues ÷ total sentences, and rewrite suggestions are chosen by minimum edit distance. A density below 0.5 is good, 0.5 to 1.5 suggests local revision, and above 1.5 calls for overall polishing.",
        "🔍 Check",
        "📚 Deep Dive: Grammar Check (Rules and Comparison)",
        "Paste text to check subject-verb agreement, tense, articles and other common errors",
        "Verify target-language grammar points after translating between Chinese and English",
        "Run a basic grammar self-check before writing",
        "Common Types",
        "English: a missing -s in the third person singular (he go to goes), misuse of a/an, mixed tenses; Chinese: mixing up the structural particles de, di and de as in the roles of possessive, adverbial and complement marker, plus word order errors. \"He eat apples\" should become \"eats\".",
        "Limits",
        "Rule-based checking catches obvious hard errors, but context, meaning and collocation errors (such as the wrong word choice) are often missed. Important text still needs human polishing.",
        "Can Grammar Check Replace a Human Reviewer?",
        "No. It only works as the first net to catch low-level mistakes; style, logic and idiomatic phrasing need human review or a native-speaker check.",
        "Why Does It Sometimes Report False Positives?",
        "Rules and statistical models tend to misjudge unusual but correct sentence patterns such as inversion and literary phrasing, so context matters.",
        "About Grammar Check",
        "Grammar Check is an online tool in the language and translation field. A language and translation tool, processed entirely in the browser, works offline.",
        "How to Use Grammar Check",
        "What Does Grammar Check Do?",
        "The grammar check tool detects common grammar, punctuation and collocation problems in Chinese and English text and suggests revisions, suitable for polishing writing, proofreading papers and improving everyday copy.",
        "How Do I Use Grammar Check?",
        "What Scenarios Suit Grammar Check?",
        "Grammar check results list suspected error types (spelling, tense, collocation, punctuation) together with revision suggestions.",
        "Machine checking is based on rules and models, so it may miss or misreport issues. Please review key text manually. Results are a writing aid and do not replace professional proofreading.",
        "Enter Chinese or English text to check its grammar...",
    ]))
    write('translator', build('translator', [
        "🌐 Multilingual Translation",
        "Multilingual translation among Chinese, English, Japanese, Korean, French, German and Russian based on a built-in dictionary",
        "Japanese",
        "Supports translation of 100+ common words",
        "🔄 Translate",
        "📋 Copy",
        "🗑️ Clear",
        "⚡ Quick Select",
        "📚 Built-in Dictionary Samples",
        "📚 Deep Dive: Text Translation (Multilingual)",
        "Quick reference for translating text among Chinese, English, Japanese, Korean, Spanish and more",
        "Splitting long sentences into segments improves accuracy",
        "Check technical terms against the source text after translating",
        "Segmented Translation",
        "\"The weather is nice today, let's go to the park.\" For long and difficult sentences, breaking the subject, verb and object apart before translating gives a more accurate result.",
        "Terminology Check",
        "In technical text, the Chinese term for cache is rendered as cache rather than buffer. Look the term up again after translating to avoid common machine-translation mismatches.",
        "Can Machine Translation Be Used Directly for Formal Documents?",
        "Direct finalization is not recommended. Long sentences, cultural references and technical terms are error-prone and need human proofreading, and sensitive or legal text must be reviewed by a native speaker.",
        "Why Does the Same Sentence Translate Differently Each Time?",
        "Neural translation generates text dynamically from context, so a tiny change can shift the result. For final text, prioritize consistency and lock terminology manually.",
        "About Multilingual Translation",
        "Multilingual Translation is an online tool in the language and translation field. A language and translation tool, processed entirely in the browser, works offline.",
        "Enter the text you want to translate...",
        "Translation result...",
    ]))
    write('vocabulary-builder', build('vocabulary-builder', [
        "📚 Vocabulary Learning",
        "Learn English words efficiently with spaced repetition",
        "Total words",
        "Streak days",
        "IELTS",
        "TOEFL",
        "Click a card to see the definition",
        "Unknown",
        "Vague",
        "Known",
        "📚 Deep Dive: Vocabulary Learning (Spaced Repetition)",
        "Build a vocabulary notebook and schedule reviews along the forgetting curve",
        "Learn words through multiple channels with example sentences and pronunciation",
        "Grow your vocabulary in bulk by grouping words by topic and root",
        "Spaced Review",
        "Reviewing new words on days 1, 2, 4, 7 and 15 matches the Ebbinghaus curve and resists forgetting far better than massed cramming. The tool dynamically pushes the next review date based on your accuracy.",
        "Root-based Memory",
        "Root spect (to look): inspect (look inward = to inspect), respect (look again = to respect), prospect (look forward = prospect). Learning a set of related roots together is far more efficient.",
        "Why Does Spaced Repetition Work?",
        "Reviewing at the critical point of fast forgetting cements the memory with the fewest repetitions. This pure front-end tool schedules reviews from local records, and no data is uploaded.",
        "Is Memorizing Words Enough?",
        "No. You also need example sentences, collocations and active use (speaking and writing). Learning words in isolation often leads to recognizing a word without being able to use it.",
        "About Vocabulary Learning",
        "Vocabulary Learning is an online tool in the language and translation field. A language and translation tool, processed entirely in the browser, works offline.",
    ]))

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'psychology')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'psychology')
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
    out = {'slug': slug, 'industry': 'psychology', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('scl90-assessment', build('scl90-assessment', [
        "💭 SCL-90 Mental Health Self-Rating Scale: 90 items · 9 factors · radar chart",
        "The Symptom Checklist-90 (SCL-90) is one of the most widely used mental health screening tools. It consists of 90 items covering nine symptom dimensions — somatization, obsessive-compulsive, interpersonal sensitivity, depression, anxiety, hostility, phobic anxiety, paranoid ideation and psychoticism — plus 7 extra items covering sleep and appetite. Please answer based on your actual feelings over the past week, rating each item on a 5-level scale from \"none\" to \"severe\". This tool automatically computes the total score, mean score, number of positive items, number of negative items, positive symptom mean and the nine factor scores, and presents a radar chart with a per-dimension interpretation. All answering and computation happen locally in your browser and are never uploaded to any server.",
        "📖 Read the \"Symptom Checklist (SCL-90) usage guide\"",
        "Each item uses a 1-5 five-level scale (1 none, 2 very mild, 3 moderate, 4 fairly severe, 5 severe). Total score = the sum of the 90 items, ranging from 90 to 450; mean score = total ÷ 90; positive item count = the number of items scoring ≥ 2; negative item count = 90 - positive count; positive symptom mean = (total - positive count × 1 - negative count × 1) ÷ positive count, that is the mean over only the items \"with symptoms\", used to characterize the average severity. Factor score = the sum of the items in that factor ÷ the number of items in that factor, also landing in the 1-5 range. Common screening thresholds for a positive result:",
        "total score > 160",
        ", or",
        "positive item count > 43",
        "or any single factor score > 2",
        "meeting any one of them suggests further professional assessment is needed. A factor score of 2-3 is mild distress, 3-4 is moderate, and above 4 is fairly severe.",
        "Print / export PDF",
        "Disclaimer:",
        "The result of this assessment is a self-test reference and does not replace professional psychological or medical diagnosis. SCL-90 is a symptom screening scale rather than a diagnostic tool; a higher score only means more subjective distress over the past week and can be affected by sleep, physical illness, life events and your answering attitude, while a normal score does not rule out distress. If you are struggling with obvious pain, your social functioning is impaired, or you have thoughts of harming yourself, please contact a psychiatrist or psychotherapist as soon as possible, and call your local psychological assistance or emergency hotline right away if needed.",
        "📚 Deep dive: SCL-90 Symptom Self-Rating Scale",
        "Mental health self-check: answer based on your real feelings over the past week to quickly see which factors score high, as a signal of what deserves attention.",
        "Preparation before counseling: bring the result to your counselor to help them locate the direction to discuss faster (reference only, not a diagnosis).",
        "State tracking: measure once before and after a stress cycle to see whether the total and certain factors fluctuate noticeably, which signals a need to adjust.",
        "How to read the total score, mean score and factor scores",
        "SCL-90 has 90 items, each 0-4 (from none to severe). The total is the sum of all items (0-360), the mean = total ÷ 90, the positive item count is the number of items scoring ≥ 1, and the positive symptom mean = the total score of positive items ÷ positive item count. More important are the 10 factor scores (such as depression, anxiety, obsessive-compulsive and somatization), each being the mean of its own items. Reading factor scores instead of only the total is what tells you where the \"discomfort\" actually sits.",
        "What factors does SCL-90 have?",
        "The standard version has 10 factors: somatization, obsessive-compulsive symptoms, interpersonal sensitivity, depression, anxiety, hostility, phobic anxiety, paranoid ideation and psychoticism, plus the additional \"other\" factor (sleep, appetite and so on). Each factor is made of several items, and the factor score reflects the severity in that area.",
        "Does a high score mean I have a mental illness?",
        "No. SCL-90 is a symptom self-rating screen; a high score only flags more distress in certain areas recently and calls for attention. It cannot replace a psychiatric diagnosis. If several factors are clearly high or it seriously affects your life, seek professional assessment instead of diagnosing yourself.",
        "Can the result be used for diagnosis or to label other people?",
        "No. It is a self-rating screening tool whose result fluctuates with your state over the past week; it is for self-awareness and as a reference when seeking help, and it does not constitute any medical conclusion.",
        "Radar chart of the nine symptom factors",
    ]))

    write('random-12', build('random-12', [
        "🎲 Cognitive Bias Cards (Random Display)",
        "Random display",
        "Random sampling: draws items at random without replacement from the cognitive bias library using a Fisher-Yates shuffle, showing the bias name, definition and a typical case (such as anchoring, confirmation bias, survivorship bias and the availability heuristic); you can keep drawing, which makes it useful for psychology study and for checking your own thinking biases.",
        "📚 Deep dive: Cognitive Bias Cards (Random Display)",
        "Thinking training: flip one bias card a day, get to know things like \"confirmation bias\" and \"loss aversion\", and sharpen how clear-headed your decisions are.",
        "Teaching design: teachers and trainers use it to show learners the common traps of irrational thinking concretely.",
        "Self-reminder: when you catch yourself catastrophizing or thinking in black-and-white terms, go back to the matching card and adjust.",
        "What is a cognitive bias",
        "A cognitive bias is a \"mental shortcut\" the human brain takes to save energy. It is harmless most of the time, but it easily causes systematic errors when you are investing, arguing or judging other people. Getting to know them is the first step toward rational decisions.",
        "Are the definitions in the cards reliable?",
        "The definitions follow the standard wording found in common behavioral economics and cognitive psychology literature, meant for education and self-awareness. For rigorous research, defer to the academic sources.",
        "How do I apply the biases in daily life?",
        "\"Recognize\" first, then \"name\": when an emotional judgement appears, try to call out the name of the matching bias, and that alone often calms you enough to redo the judgement.",
        "About \"Cognitive Bias Cards (Random Display)\"",
        "Cognitive Bias Cards (Random Display). A free online tool that runs entirely in the front end, uploads no data and protects your privacy and security.",
        "Self-awareness of heuristic biases in everyday decisions (anchoring, confirmation bias, availability bias and more)",
        "Identifying and avoiding common cognitive traps in product and operations design",
        "Analyzing where and how information gets distorted when reading news and arguments",
        "Illustrating typical cognitive biases in teaching or sharing, to strengthen critical thinking",
    ]))

    write('generator-20', build('generator-20', [
        "✨ Philosophical School Word Cloud Generator (Built-in Works)",
        "Built-in works",
        "Word cloud generation: extracts high-frequency words from each school's representative works and keywords; font size = base size × term frequency weight (frequency ÷ maximum frequency); colors are assigned by school group; the layout radiates outward from the center in descending frequency order. It suits teaching guided tours and reading notes, and you can adjust the font size and colors before exporting.",
        "📚 Deep dive: Philosophical School Word Cloud Generator (Built-in Works)",
        "Teaching demo: in a philosophy class or book-sharing session, use a word cloud to present the core concept set of a school in an intuitive way.",
        "Reading notes: after finishing a philosopher's representative work, turn the keywords into a word cloud to help memory and review.",
        "Content posters: quickly generate a polished concept graphic of a school for an article or community post.",
        "Where do the words in the cloud come from",
        "Each school has a curated word list of its representative works and core terms built in (for example existentialism maps to \"absurdity, freedom, authenticity\"), and at generation time the font size is decided by term frequency, so the more core the word the larger it appears.",
        "Can I use the generated word cloud commercially?",
        "The word cloud is generated from the public concept word lists built into this tool and contains no third-party copyrighted material, so personal and educational use is usually fine; for a formal commercial release, verify it yourself.",
        "Can I customize the words?",
        "The current version generates from the built-in school word lists; custom input can be added later. All rendering happens locally in your browser and no data is uploaded.",
        "About \"Philosophical School Word Cloud Generator (Built-in Works)\"",
        "Philosophical School Word Cloud Generator (Built-in Works). A free online tool that runs entirely in the front end, uploads no data and protects your privacy and security.",
        "Sorting out the core claims and representative figures of schools such as existentialism, utilitarianism and Kantian ethics",
        "Quickly generating keyword word clouds for each school when preparing an intro to philosophy or course handouts",
        "Comparing worldviews, value orderings and methodologies across schools in writing or debate",
        "Using a visual word cloud to help remember school traits and their classic works",
    ]))

    write('bigfive-personality-test', build('bigfive-personality-test', [
        "📝 Big Five Personality Test: 60 items · 5 dimensions 15 facets · 28-type matching",
        "The Big Five model (Big Five / OCEAN) is the best-evidenced descriptive framework in contemporary personality psychology, using five orthogonal dimensions — openness, conscientiousness, extraversion, agreeableness and neuroticism — to characterize stable behavioural tendencies. This assessment has 60 items, 12 per main dimension and 4 for each of 15 facets, with reverse scoring handled automatically and converted to T scores with mean 50 and standard deviation 10; it then uses weighted Euclidean distance to match your dominant and secondary types among the centroids of 28 personality prototypes, and gives strengths, blind spots, suitable career directions and interpersonal advice. Please answer with your first reaction instead of picking the answer that \"looks better\" — the Big Five has no better or worse, only a position on a distribution. All computation happens locally in your browser.",
        "📖 Read the \"Big Five Personality Test (OCEAN) usage guide\"",
        "Disclaimer:",
        "The result of this assessment is a self-test reference and does not replace professional psychological or medical diagnosis. The 60-item short scale is weaker in reliability than full professional instruments such as NEO-PI-R, and the T scores use a general reference norm rather than a local stratified norm, so judgments about high versus low near the boundary (T between 45 and 55) are not stable. Personality traits describe probabilistic tendencies rather than a fixed ceiling of ability, so please do not use them to label yourself or others, nor as the sole basis for important decisions such as hiring or admission. If you are persistently affected by emotional distress or interpersonal pain, please seek help from a psychiatrist or psychotherapist.",
        "📚 Deep dive: Big Five Personality Test (OCEAN)",
        "Self-awareness: look at how your scores are distributed across the five dimensions to understand why you react the way you do in certain situations.",
        "Teamwork: have each member take the test and compare who is more extraverted, more conscientious and more open, so task assignment goes more smoothly.",
        "Hiring reference (limited scope): some roles do consider conscientiousness or extraversion, but only as one signal among many, never as a sole basis for a hiring decision.",
        "How to read the five Big Five dimensions",
        "The Big Five describes personality with five independent dimensions: O openness, C conscientiousness, E extraversion, A agreeableness and N neuroticism. Each dimension is a continuous spectrum, and a high or low score is only a tendency, not a judgement of good or bad. For example, high E prefers social recharging, high N is more easily disturbed by stress, and high C is more disciplined and reliable. Looking at the combination of all five is much closer to the real you than looking at any single one.",
        "What are the five dimensions of the Big Five?",
        "O openness (curiosity, seeking novelty), C conscientiousness (self-discipline, reliability), E extraversion (sociability, energy), A agreeableness (cooperation, trust), N neuroticism (emotional sensitivity, stress response). Their English initials spell OCEAN.",
        "Do high or low scores mean good or bad?",
        "Neither — they are tendency descriptions. A high neuroticism score is not a weakness; it makes you more perceptive. A low extraversion score does not mean being antisocial, just that you need solitude to recharge. Dimensions have no better or worse; only the combination forms a complete personality portrait.",
        "Can the Big Five be used for hiring screening?",
        "It can serve as one reference signal but must never be the sole basis for a hiring decision. Personality is only one of many factors affecting performance, and using interest or personality tests for screening is both inaccurate and a compliance risk.",
        "Bar chart of T scores for the five personality dimensions",
        "Personality result card",
    ]))

if __name__ == '__main__':
    main()

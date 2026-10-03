#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'cognition')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'cognition')
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
    out = {'slug': slug, 'industry': 'cognition', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('cognitive-assessment', build('cognitive-assessment', [
        "\u26A1 SCOPE Comprehensive Cognitive Assessment: 8 subtests \u00b7 age norms \u00b7 four-dimension radar chart",
        "A comprehensive cognitive-ability assessment tool using 8 classic subtests covering four dimensions - attention, working memory, processing speed and executive function: simple reaction time, choice reaction time, digit span forward, digit span backward, symbol-digit modality test, Stroop interference, 2-back working memory and Trail Making Test TMT-A/B. Each item gives instructions and practice trials before the formal test; raw scores are converted via four-tier age norms into standard scores (mean 100, SD 15) and percentiles, outputting a four-dimension radar chart, item-by-item detail table and strength/weakness interpretation. History is saved locally in the browser; you can export CSV and a result-card PNG.",
        "Ready? Tap \"Start Assessment\"",
        "Takes about 12 minutes total; recommended in a quiet environment on a non-touchscreen device for more accurate reaction-time readings.\n        Each test shows instructions and a practice trial first; practice scores are not counted.",
        "\u26A0\uFE0F Use boundary: this page is an entertainment and self-test reference tool for observing your cognitive-performance fluctuation across different states (sleep, caffeine, fatigue),",
        "and does not constitute a clinical diagnosis",
        ", nor can it be used to screen for cognitive impairment, assess capacity, or serve as a basis for any medical, occupational or legal purpose. If you or a family member is concerned about real changes in memory or attention, please seek a standard assessment at a neurology or memory clinic.",
        "\U0001F4DA In-depth: Comprehensive Cognitive Assessment",
        "Multi-domain screening: complete attention, memory, speed, executive and other subtasks in turn, aggregating each domain's score into a personal cognitive profile.",
        "Pre/post-training comparison: use the first assessment as a baseline, retest after an interval to observe each domain's change and guide training focus.",
        "Self-understanding: use relative strengths/weaknesses to identify patterns like 'memory weaker than speed' and arrange targeted practice.",
        "Example Domain Profile",
        "Attention 82, working memory 74, processing speed 88, executive function 79 (relative 100-point); working memory is relatively low and can be a follow-up training focus; scores are in-site self-ratings, not standard norms.",
        "What level do the scores represent?",
        "Each domain's score is an in-site relative self-rating (illustrative 100-point), not a standardised-norm conversion; it is only for personal lateral comparison and training tracking.",
        "Can it detect cognitive decline?",
        "No. This is a self-rating and training-aid tool; if concerned about memory or cognitive changes, consult a professional institution for a standard assessment.",
        "How often is retesting appropriate?",
        "Suggest an interval of several weeks or more to reduce the practice effect, and retest at roughly the same time and similar state for more comparable results.",
        "About SCOPE Comprehensive Cognitive Assessment",
        "Multi-domain items generate an attention/memory/speed/executive-function self-rating profile for training baselines and personal tracking.",
        "Multi-cognitive-domain scoring",
        "Relative strength/weakness profile",
        "Retest tracking",
        "Pre/post-training comparison",
        "Self-understanding of cognitive strengths",
        "Arranging targeted practice",
    ]))
    write('corsi-block-test', build('corsi-block-test', [
        "\U0001F58B Corsi Block-Tapping Test",
        "The Corsi Block-Tapping Test is used to measure visual-spatial short-term memory span. The system highlights several blocks in sequence; tap them back in the same (forward) or reverse (backward) order. A staircase method auto-adjusts difficulty; everything runs on your device.",
        "Corsi Block-Tapping Test",
        "/ Corsi Block-Tapping Test",
        "\U0001F4D6 View the User Guide for Corsi Block-Tapping Test",
        "\U0001F4D0 Scoring Principle",
        "Each sequence length L is randomly generated and non-repeating. Each length has 2 trials: if at least 1 of 2 is correct, advance to L+1; if 2 consecutive are wrong, stop. Corsi span = the last passed length, plus 0.5 if that length was correct only 1/2 times. Product Score = the sum of lengths of all correctly reproduced sequences, more sensitive to memory capacity and interference resistance. Approximate norms: child ~4.8, adult ~5.5, elderly ~4.9.",
        "Recall Mode",
        "Forward (tap in order)",
        "Backward (tap in reverse)",
        "Demo Pace",
        "Slow (0.9 s/block)",
        "Medium (0.65 s/block)",
        "Fast (0.45 s/block)",
        "Current Length",
        "Trials",
        "Passed Length",
        "Correct Trials",
        "After tapping \"Start Test\", watch the blocks light up in sequence, then tap them back per the rule.",
        "Replay This Sequence",
        "End and Record",
        "Hint: during the demo phase, block highlights are system-controlled; in the input phase, tap forward in the lit order, or backward in the reverse order. Faster pace and longer length approach real memory load.",
        "\U0001F4DA In-depth: Corsi Block-Tapping Test",
        "Forward tapping: tap squares in the lit order, recording the maximum spatial sequence length accurately reproduced (visual-spatial span).",
        "Backward tapping: tap in reverse, adding central-executive load; capacity is usually shorter.",
        "Spatial-memory training/research: track pre/post changes by max span, or compare verbal vs working-memory pathways.",
        "Spatial Span Calculation",
        "Forward correct through length 6, wrong at 7 -> forward span 6; backward correct at 5, wrong at 6 -> backward span 5; backward shorter fits the dual load of 'retain + reverse'.",
        "How does Corsi differ from digit span?",
        "Digit span is the verbal/auditory channel, Corsi is the visual-spatial channel; they test different memory subsystems and are often paired to distinguish memory types.",
        "Is backward much harder than forward normal?",
        "Normal. Backward requires remembering positions then reversing order, extra central-executive load; most people's backward span is about 1 lower than forward.",
        "Can it assess spatial cognitive impairment?",
        "No. This tool is for training and self-rating; clinical spatial-cognition assessment needs a professional institution.",
        "About Corsi Block-Tapping Test",
        "Tap spatial positions in presented order to measure visual-spatial working-memory span, complementing digit span to test different memory channels.",
        "Forward / backward tapping",
        "Spatial sequence span",
        "Visual-spatial channel",
        "Spatial memory training",
        "Verbal x spatial memory comparison",
        "Cognitive research demonstration",
    ]))
    write('digit-span-test', build('digit-span-test', [
        "\U0001F4D6 Digit Span Memory Test",
        "Digit Span is a classic WAIS subtest measuring verbal working-memory span. Digits are presented one by one at a steady pace; repeat them per the rule. Supports forward, backward and sequencing conditions, with a staircase method auto-adjusting difficulty, and optional spoken/auditory presentation.",
        "Digit Span Memory Test",
        "/ Digit Span Memory Test",
        "\U0001F4D6 View the User Guide for Digit Span Memory Test",
        "\U0001F4D0 Scoring Principle",
        "Each length has 2 trials: if at least 1 of 2 is correct, advance to a longer sequence; if 2 consecutive all-wrong at the same length, stop. Span = the last passed length, plus 0.5 if that length was correct only 1/2 times. Total span = mean of forward, backward and sequencing spans; sequence score = sequencing-condition span. Approximate WAIS adult norms: forward ~6.5, backward ~5.5, sequencing ~5.0 (rough reference only, not clinical).",
        "Presentation Speed",
        "Slow (1.5 s/digit)",
        "Standard (1.0 s/digit)",
        "Fast (0.5 s/digit)",
        "Test Condition",
        "Forward (repeat in order)",
        "Backward (repeat in reverse)",
        "Sequencing (repeat ascending)",
        "Auditory Presentation",
        "Enable Voice Reading",
        "Start This Condition",
        "Run All Three",
        "End and Record",
        "Current Length",
        "Trials",
        "In Progress",
        "Correct Trials",
        "After setting speed and condition, tap \"Start This Condition\". Running all three auto-proceeds forward, backward, sequencing in order.",
        "Confirm",
        "Hint: the sequence is presented only once, please concentrate. Backward requires saying the heard digits in reverse; sequencing requires saying them ascending. Faster pace approaches real working-memory load. All data is saved only in your local browser.",
        "\U0001F4DA In-depth: Digit Span Test",
        "Forward: measures the phonological loop's storage capacity; presented group by group from short to long, recording the max length correctly repeated.",
        "Backward: adds central-executive control on top of storage, requiring reverse output; capacity is usually 1-2 digits shorter than forward.",
        "Education/training baseline: use max span as the working-memory capacity baseline to observe lateral comparison across training or age stages.",
        "Max Span Calculation",
        "Forward correct through length 8, failed at 9 -> forward span 8; backward correct at 6, failed at 7 -> backward span 6; backward usually shorter than forward, matching the working-memory hierarchy model.",
        "What is the difference between forward and backward?",
        "Forward only tests 'retaining' the sequence; backward also requires 'operating' (reversing order), involving more central-executive control, so backward capacity is generally lower and harder.",
        "What span is normal?",
        "Adults' forward is commonly about 7\u00b12 digits, backward about 5-6, but strongly affected by age, language and state; a single result is only for self-reference.",
        "Can this test diagnose attention deficit?",
        "No. It is a screening practice for working-memory capacity; any diagnosis must be made by a professional institution with a battery of tests.",
        "About Digit Span Memory Test",
        "Forward/backward digit strings assess auditory short-term and working-memory capacity, a classic component of comprehensive intelligence tests.",
        "Forward and backward modes",
        "Max span record",
        "Gradually increasing length",
        "Working-memory capacity baseline",
        "Education training pre/post comparison",
        "Attention self-rating practice",
        "Enter your answer here",
    ]))

if __name__ == '__main__':
    main()

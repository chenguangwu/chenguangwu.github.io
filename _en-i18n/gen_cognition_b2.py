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
    write('human-benchmark', build('human-benchmark', [
        "\U0001F9E0 Human Benchmark Cognitive Baseline Test",
        "8 classic cognitive subtests, each converted to a norm percentile, aggregated into a memory-attention-processing speed-executive four-dimension ability radar chart and a 0-100 composite brain index. Everything runs locally in the browser, no internet needed, no data uploaded.",
        "Human Benchmark Cognitive Baseline Test",
        "/ Human Benchmark Cognitive Baseline Test",
        "\U0001F4D6 View the User Guide for Human Benchmark Cognitive Baseline Test",
        "\U0001F4D0 Scoring and Composite-Index Principle",
        "After each subtest yields a raw score, convert to a percentile by the population normal norm (mean \u03bc, SD \u03c3): for lower-is-better, percentile = 1 - \u03a6((x-\u03bc)/\u03c3); for higher-is-better, percentile = \u03a6((x-\u03bc)/\u03c3), where \u03a6 is the standard normal CDF. The four abilities = weighted aggregation of subtest percentiles (memory 30% / attention 25% / processing speed 25% / executive 20%); the composite brain index = the four-dimension weighted mean (0-100), equivalent to 'you beat x% of people'. Norms are published-literature empirical values, for self-reference only, not equivalent to medical or clinical diagnosis. Random delays and target positions use crypto.getRandomValues; feedback sound uses AudioContext.",
        "\U0001F3AF Test",
        "\U0001F4CA Report",
        "\U0001F558 History",
        "Tap any subtest to start; clear the current test to redo anytime; after all 8 are done a report is auto-generated.",
        "\u25B6 Complete all 8 in sequence",
        "\u21BA Reset Progress",
        "Select a subtest above, or tap 'Complete all 8 in sequence' to start the assessment.",
        "Not enough subtests completed. Please finish at least 1 on the Test page; after all 8 you can generate the full four-dimension radar chart and composite index.",
        "Composite Brain Index (you beat \u2014% of people)",
        "\U0001F5BC\uFE0F Export Scorecard PNG",
        "\U0001F4CB Copy JSON",
        "Local History (localStorage)",
        "\U0001F4CC Cognitive performance is heavily affected by sleep, mood, device and age; a single result is for entertainment and self-reference only; repeating practice itself raises scores (practice effect), so a rising history curve does not equal real ability growth. This tool stores no data on any server.",
        "\U0001F4DA In-depth: Human Benchmark Test",
        "Reaction-time test: measures the delay to click on a visual stimulus, taking the median of multiple trials as a reaction-speed reference.",
        "Memory tests: digit/auditory/visual memory each measure retention capacity and accuracy of a different channel.",
        "Friend lateral comparison: use the same-rule scores for a fun ranking, observing each person's strength/weakness differences.",
        "Reaction-Time Median",
        "5 reaction times 268/251/243/259/247 ms, median about 251 ms after dropping extremes; reaction time is affected by device, input latency and state, for relative reference only.",
        "What does each subtest measure?",
        "Reaction time measures perception-action latency; digit/auditory/visual memory measure short-term retention of different channels; multi-dimensional self-rating, not pointing to a single ability.",
        "Can scores be compared with others?",
        "Yes for fun comparison, but cross-device and cross-state latency differences are large; ranking is for entertainment reference only.",
        "Can it assess comprehensive intelligence?",
        "No. These are entertainment collections of single-dimension mini-tests, not an intelligence or ability assessment; formal assessment needs a professional institution.",
        "About Human Benchmark Cognitive Baseline Test",
        "A collection of multi-dimension solo mini-tests - reaction time, memory, prediction - comparing personal cognitive performance laterally, an entertainment self-rating.",
        "Reaction-time / memory multi-dimension",
        "Fun score ranking",
        "Instantly testable",
        "Reaction speed and memory self-rating",
        "Friend lateral comparison",
        "Multi-dimension strength/weakness identification",
    ]))
    write('index', build('index', [
        "\U0001F9E0 Cognition and Brain-Training Tools",
        "Cognition and Brain Training",
        "Cognition and Brain-Training Tools",
        "Digit Span Memory Test",
        "Digit Span is a classic WAIS subtest measuring verbal working-memory span. Digits are presented one by one at a steady pace; repeat them per the rule. Supports forward, backward and sequencing conditions, with a staircase method auto-adjusting difficulty, optional spoken/auditory...",
        "Stroop Test",
        "The Stroop effect reveals the conflict between two automatic processes - 'reading the word' and 'naming the color': when the word-meaning color differs from the ink color, naming the ink color slows down and is more error-prone. This test uses a three-phase design to quantify your personal interference and compare against norms.",
        "SCOPE Comprehensive Cognitive Assessment",
        "SCOPE Comprehensive Cognitive Assessment: simple reaction time, choice reaction time, digit span forward and backward, symbol-digit modality, Stroop interference, 2-back working memory, Trail Making Test TMT-A/B, 8 subtests, by 18-29/30-49...",
        "Time Perception and Rhythm-Precision Test",
        "Test your 'time sense' and 'rhythm sense': one-second challenge, double-click speed, beat sync - three modules; error distribution shown via a canvas bar chart, with local best and history curves. All computed locally in the browser, no internet, no upload.",
        "Corsi Block-Tapping Test",
        "The Corsi Block-Tapping Test measures visual-spatial short-term memory span. The system highlights several blocks in sequence; tap them back in the same (forward) or reverse (backward) order. A staircase method auto-adjusts difficulty...",
        "Human Benchmark Cognitive Baseline Test",
        "8 classic cognitive subtests, each converted to a norm percentile, aggregated into a memory-attention-processing speed-executive four-dimension ability radar chart and a 0-100 composite brain index. Everything runs locally in the browser, no internet needed, no data uploaded.",
        "Schulte Table Attention Training",
        "The Schulte Table is a classic attention and visual-search training tool. Tap squares quickly in a specified order; the system counts time, click rate and errors in real time, saving each set's performance and drawing a history curve. All computed in your browser...",
        "N-Back Working-Memory Training",
        "N-Back is a classic working-memory paradigm: when each stimulus appears, judge whether it matches the 'N-th previous' stimulus on the corresponding channel. Supports single channel (position) and dual channel (position+letter/digit/color); N can be fixed or adaptive; gives real-time position hit...",
        "About Cognition and Brain-Training Tools",
        "The Cognition and Brain-Training Tools collection contains 8 free online tools covering common calculation, conversion and lookup needs in cognition and brain-training scenarios. Whether you are a practitioner, student or ordinary user in the field, you can find ready-to-use small tools here. All tools run entirely in the browser, upload no data to the server, and protect your privacy and security.",
        "The cognition and brain-training tools on this page include (representative selection):",
        "These tools help you quickly complete common tasks related to cognition and brain training without memorising complex formulas or doing manual conversions; just enter to get results.",
        "Do the cognition and brain-training tools need to be downloaded or registered?",
        "No. All cognition and brain-training tools on this page are pure front-end online tools; open the web page to use them directly, with no software installation, no account registration, and no data upload.",
        "Are the cognition and brain-training tools' results accurate? Is the data safe?",
        "The tools calculate locally in your browser based on public mathematical formulas and general industry standards, with results available instantly. All computation is done locally on your device, data is never uploaded to the server, and your privacy and security are protected.",
    ]))
    write('nback-training', build('nback-training', [
        "\U0001F9E0 N-Back Working-Memory Training",
        "N-Back is a classic working-memory paradigm: when each stimulus appears, judge whether it matches the 'N-th previous' stimulus on the corresponding channel. Supports single channel (position) and dual channel (position+letter/digit/color); N can be fixed or adaptive; gives real-time position hit rate, voice hit rate and the signal-detection metric d', and draws a training curve by day.",
        "N-Back Working-Memory Training",
        "/ N-Back Working-Memory Training",
        "\U0001F4D6 View the User Guide for N-Back Working-Memory Training",
        "\U0001F4D0 Calculation Principle",
        "Hit rate HR = hits / signal trials, false-alarm rate FA = false alarms / noise trials. Log-linear correction (HR'=(H+0.5)/(S+1), FA'=(F+0.5)/(N+1)) avoids 0/1 extremes; z-scores come from Acklam's inverse-normal CDF approximation, d' = z(HR') - z(FA'). Under dual channel, position and letter compute d' independently. Adaptive rule: 4 consecutive all-correct raises N+1 (cap 9), 3 consecutive errors lowers N-1 (floor 1).",
        "Channel Mode",
        "Single channel (position)",
        "Dual channel (+letter)",
        "Stimulus Material",
        "Digits (0-9)",
        "Letters (A-H)",
        "Color squares",
        "N-Value Mode",
        "Fixed",
        "Adaptive",
        "Start N (fixed mode)",
        "Presentation Duration",
        "Interval",
        "Keys: single channel press",
        "Space",
        "= match /",
        "= mismatch; dual channel position press",
        "= match",
        "= mismatch, letter press",
        "= mismatch. You can also tap on-screen buttons. With voice on, letters are read aloud (letter material only).",
        "\u25B6 Start Training",
        "\U0001F50A Voice: On",
        "Clear Training Records",
        "Adaptive Mode",
        "Trials",
        "Position Hit Rate",
        "Voice Hit Rate",
        "Position d'",
        "Letter d'",
        "End",
        "Position Match (Q)",
        "Position Mismatch (A)",
        "Letter Match (P)",
        "Letter Mismatch (L)",
        "This Round's Result",
        "Signal-Detection Detail",
        "Training Curve (by-day aggregation)",
        "Export JSON",
        "Run Another Round",
        "Use boundary: this tool is for cognitive training and self-monitoring; all metrics come from signal-detection-theory math,",
        "and is not equivalent to medical or clinical diagnosis",
        ". If you have concerns about attention/memory, consult a professional institution. Voice reading relies on the browser's SpeechSynthesis; some environments do not support it or require user interaction before it can sound.",
        "\U0001F4DA In-depth: N-back Working-Memory Training",
        "Working-memory training: start from 2-back, raise to 3-back once hit rate is stable, gradually increasing memory load.",
        "Sensitivity (d') estimation: combine hit rate and false-alarm rate to compute the signal-detection metric, assessing discriminability rather than mere accuracy.",
        "Research/self-tracking: record hit rate, false-alarm rate and reaction time at different N, observing working-memory capacity change before/after training.",
        "2-back Hit Rate and Sensitivity",
        "Of 30 targets, 27 hits, 4/60 false alarms; hit rate 0.90, false-alarm rate 0.067; by signal-detection approximation d' \u2248 z(0.90) - z(0.067) \u2248 1.28 - (-1.50) = 2.78, good discriminability.",
        "What does N represent?",
        "N means 'count back how many': 2-back judges whether the current stimulus matches the one 2 before it; larger N means higher memory load.",
        "Does hit-rate level alone show memory quality?",
        "Not fully. High hits often accompany high false alarms; you need d' (sensitivity) with the false-alarm rate to distinguish 'truly remembered' from 'guessed right'.",
        "Can it replace clinical memory diagnosis?",
        "No. This is a training and self-rating tool; results are affected by state, fatigue and practice effect; leave cognitive assessment to professional institutions.",
        "About N-Back Working-Memory Training",
        "Judge whether the current stimulus matches the N-th previous one; progressively raise N to train working memory, with sensitivity d' estimation.",
        "Adjustable N load",
        "Hit / false-alarm statistics",
        "Sensitivity d' output",
        "Progressive working-memory training",
        "Self-tracking before/after comparison",
        "Cognitive research data collection",
    ]))

if __name__ == '__main__':
    main()

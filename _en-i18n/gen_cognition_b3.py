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
    write('schulte-table', build('schulte-table', [
        '🎮 Schulte Table Attention Trainer',
        'The Schulte Table is a classic training tool for attention and visual search. Tap the cells in the specified order as fast as you can; the system tracks time, tap rate and error count in real time, saves each session and plots a history curve. All computation runs locally in your browser; no internet connection required.',
        'Schulte Table Attention Trainer',
        '/ Schulte Table Attention Trainer',
        '📖 View the User Guide for Schulte Table Attention Trainer',
        '📐 Scoring Principle',
        'Numbers 1 to N are randomly distributed in the grid; tap them all in ascending (1->N) or descending (N->1) order as quickly as possible. Core metrics: completion time T (seconds), error taps E, and tap rate R = N / T (cells per second, higher is better). Attention level is usually measured by the average time per cell; a lower value means more efficient visual search. In color-name mode, cells show color words but must be tapped by their hidden order, additionally testing interference resistance and Stroop-style inhibition.',
        'Grid Order',
        '3 × 3 (Beginner)',
        '5 × 5 (Standard)',
        '7 × 7 (Hard)',
        'Content Mode',
        'Common Chinese Characters',
        'Color Names',
        'Order',
        'Ascending (small -> large)',
        'Descending (large -> small)',
        'Start Training',
        'Tapped / Total',
        'Rate (cells/s)',
        'Error Taps',
        'Note: each wrong tap triggers a vibration and counts as an error, but the progress does not advance - you must tap the next correct cell to continue. In color-name mode, ignore the text color and tap by the hidden order.',
        'History Score Curve',
        'Clear This Spec',
        'No practice records for this spec yet; complete a session first.',
        '📚 Deep Dive: Schulte Table',
        'Attention training: tap 1-25 in order within a 5×5 (25-cell) grid and record total time; a shorter time means more efficient visual search and focus.',
        'Cross comparison: repeat tests with a fixed grid spec and compare time fluctuations across states as attention feedback.',
        'Teaching / team activities: use as a focus game or classroom icebreaker - low barrier, instantly measurable.',
        'Time and Efficiency Reference',
        'Tapping through a 5×5 grid in order took 38 s; skilled adults are usually in the 25-40 s range. Time is affected by grid spec, proficiency and current focus; a single result is only a relative reference.',
        'Is a larger grid harder?',
        'Yes. More cells spread the search targets and increase interference; time typically grows roughly linearly with cell count, so compare at the same spec.',
        'Does a shorter time mean smarter?',
        'Not necessarily. It mainly reflects visual search speed and current focus, and is clearly affected by practice effects; it should not be taken as a measure of ability.',
        'Is it suitable for children\'s attention training?',
        'It can serve as a fun focus exercise, but if there is a persistent attention problem, a professional assessment is needed. This tool has no diagnostic function.',
        'About Schulte Table Attention Trainer',
        'Tap numbers in order within the grid and use completion time to assess visual search speed and attention focus.',
        'Adjustable grid spec',
        'Completion time tracking',
        'Attention feedback',
        'Attention training',
        'Cross-state comparison',
        'Classroom focus activities',
    ]))
    write('stroop-test', build('stroop-test', [
        '📝 Stroop Effect Test',
        'The Stroop effect reveals a conflict between two automatic processes - reading the word and naming the color: when the word meaning and ink color mismatch, naming the ink color becomes slower and more error-prone. This test uses a three-stage design to quantify your personal interference and compare it with norms.',
        'Stroop Effect Test',
        '/ Stroop Effect Test',
        '📖 View the User Guide for Stroop Effect Test',
        '📐 Calculation Principle',
        'Stroop interference = mean RT of incongruent trials (meaning != ink color) - mean RT of congruent trials (meaning = ink color), in milliseconds; interference rate = interference / congruent mean RT × 100%. Error bars show the standard error of the mean SEM = SD / √n. Norm reference: healthy adults show interference of about 30-100 ms and an interference rate of about 8-20%; error rate usually rises slightly in the incongruent condition. RT averages only correctly responded trials; timeouts are recorded as errors.',
        'Number of Colors',
        '4 Colors',
        '3 Colors',
        'Per-Trial Time Limit',
        'Practice Stage',
        'On',
        'Skip',
        'Keys: ',
        'Red /',
        'Green /',
        'Blue /',
        'Yellow. You can also tap the color buttons on screen. Always name',
        'the ink color',
        ', not the word meaning.',
        '▶ Start Test',
        'Ready',
        'Red',
        'Green',
        'Blue',
        'Yellow',
        'End Early',
        'Test Result',
        'Condition Details',
        'Interference Effect Visualization (mean ± SEM)',
        'Congruent',
        'Incongruent',
        'Neutral',
        'Per-Trial RT Scatter',
        'Export JSON',
        'Scope of use: this test is for fun self-assessment in cognitive psychology and teaching demos,',
        'and does not constitute any medical or neuropsychological diagnosis',
        '. Interference is affected by fatigue, language proficiency and attention state; for research use, fix the device and environment and take repeated measurements for the mean. The neutral condition uses non-color words to eliminate the direct word-meaning vs. color conflict.',
        '📚 Deep Dive: Stroop Color-Word Test',
        'Psychology teaching and experiment demos: reproduce the classic Stroop effect in class, intuitively showing the conflict between automatic processing (word reading) and controlled processing (color naming).',
        'Attention self-assessment and training: use the interference score to track RT changes under congruent/incongruent conditions as instant feedback for focus practice.',
        'Cognitive research data collection: record RT under fixed trials and randomized balanced order, providing reproducible baseline data for attention-control studies.',
        'Interference Accounting',
        'Incongruent mean RT 982 ms, congruent 621 ms, interference = 982 - 621 = 361 ms; a larger interference usually means stronger conflict from automatic word reading interfering with color naming.',
        'How is the interference score calculated?',
        'Subtract the mean RT of the congruent (meaning = color) or neutral condition from the mean RT of the incongruent (meaning conflicts with color) condition; the difference is the Stroop interference, in milliseconds.',
        'Can the result be used for clinical diagnosis?',
        'No. This tool is only for teaching demos, attention self-assessment and training feedback, for entertainment / self-understanding. For any cognitive or neurological judgment, consult a professional institution.',
        'Why is my incongruent RT noticeably slower?',
        'Word reading is a highly automatic habit; when a color conflict occurs, you must actively suppress "reading the meaning" and instead "name the ink color". This suppression cost raises RT and is exactly the source of the Stroop effect.',
        'About Stroop Effect Test',
        'Quantify cognitive interference via the RT difference between reading the word meaning and naming the ink color, for attention self-assessment and classroom Stroop demos.',
        'Stroop interference calculation',
        'Congruent / incongruent conditions',
        'Real-time RT feedback',
        'Psychology classroom effect demo',
        'Attention self-assessment and training',
        'Attention-control experiment data collection',
    ]))
    write('time-perception', build('time-perception', [
        '🎵 Time Perception & Rhythm Accuracy Test',
        'Measure your sense of time and rhythm: one-second challenge, double-click speed and beat sync, three modules; error distribution is shown with a canvas bar chart, with local best and history curves. All computation runs locally in the browser; no internet, no upload.',
        'Time Perception & Rhythm Accuracy Test',
        '/ Time Perception & Rhythm Accuracy Test',
        '📖 View the User Guide for Time Perception & Rhythm Accuracy Test',
        '📐 Timing & Accuracy Principle',
        'The one-second challenge uses performance.now() to precisely record press duration; signed error = estimated duration - 1000 ms (positive = overestimate); mean absolute error MAE and standard deviation σ describe stability, and the percentile is converted by a population normal norm (lower is better). Double-click speed records the interval between two clicks, takes the fastest valid interval over 10 rounds, and shows the jitter distribution with a histogram. Beat sync uses AudioContext.currentTime to pre-schedule 20 precise beats (not setInterval to drive sound); the user click deviation from the nearest beat = early (-) / late (+); consistency = standard deviation of deviations, smaller is steadier. Norms are empirical values, for self-reference only.',
        'One-Second Challenge',
        'Hold to estimate 1 second, 5 times',
        'Double-Click Speed',
        '10 rounds of double-click to test hand speed',
        'Beat Sync',
        'BPM 60/90/120 · 20 beats',
        'Select a module above to start the test.',
        'Summary & Local Best',
        '📌 Time perception is affected by attention, age, fatigue and context. Professionally music-trained people usually have better rhythm consistency; caffeine or fatigue can shift your estimation bias. This tool results are for entertainment and self-reference only, not any medical or professional ability assessment.',
        '📚 Deep Dive: Time Perception Test',
        'Production method: silently count in mind and actively stop to "produce" the target duration, comparing the stop moment with the real duration.',
        'Estimation method: after presenting an interval, let the subject judge its length, measuring the bias direction of time estimation.',
        'Attention correlation: retest under relaxed / tense states and observe how emotion and attention stretch or compress time perception.',
        'Production Bias Accounting',
        'Target 10 s, actually stopped at 11.4 s, relative bias = (11.4 - 10) / 10 = +14%, meaning a tendency to "overestimate / prolong" time; the bias direction may reverse under different emotions, and a single result is only a reference.',
        'What is the difference between estimation and production?',
        'The estimation method is "given a duration, judge how long" (passive perception), and the production method is "stop out a duration yourself" (active generation); the two measure different aspects of time perception.',
        'Why does time feel slower when tense?',
        'Emotional arousal raises the subjective "tick rate" of the internal clock, making a unit of time perceived as longer; this is a common time-perception distortion.',
        'Can it measure time-perception disorders?',
        'No. This tool is for self-assessment and research demos; clinical assessment related to time perception must be done by a professional institution.',
        'About Time Perception & Rhythm Accuracy Test',
        'Estimate or produce a specified duration and use the deviation to assess time-perception accuracy, for attention and interoception research and self-assessment.',
        'Estimation / production method',
        'Relative bias accounting',
        'State correlation comparison',
        'Time-perception self-assessment',
        'Emotion × attention correlated retest',
        'Research demo',
    ]))

if __name__ == '__main__':
    main()

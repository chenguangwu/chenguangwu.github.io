#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'ent')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'ent')
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
    out = {'slug': slug, 'industry': 'ent', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

def main():
    write('pure-tone-audiometry', build('pure-tone-audiometry', [
        "\U0001F442 Pure Tone Hearing Screening \u00b7 Audiogram \u00b7 Pure-Tone Audiogram",
        "A pure front-end Web Audio tool: it uses AudioContext to generate pure tones at 125 / 250 / 500 / 1000 / 2000 / 4000 / 8000 Hz, eight frequencies in all, as sine waves with adjustable duration and volume. It estimates the hearing threshold ear by ear with an ascending method, from low to high, and automatically plots a standard audiogram with a logarithmic frequency axis against dB, marking the normal, mild, moderate, severe and profound bands according to the WHO grading. Please wear headphones and test in a quiet environment.",
        "Pure Tone Hearing Screening \u00b7 Audiogram",
        "/ ENT \u00b7 Pure Tone Hearing Screening",
        "Home",
        "\U0001F4D6 View the \"Pure Tone Hearing Screening \u00b7 Audiogram Guide\"",
        "Limits of use:",
        "This test is an",
        "entertainment self-test",
        ", and a web page cannot calibrate volume physically in dB HL, so the result is",
        "not a medical diagnosis",
        "and cannot replace professional pure tone audiometry or an ear examination. If you feel your hearing has dropped, please see a medical facility.",
        "\u2460 Test each ear in turn",
        "\u2461 Audiogram and grading",
        "Testing needs audio output. After you grant permission, the browser creates an AudioContext to generate the pure tones.",
        "\U0001F50A Click to start (authorise audio)",
        "Ear currently tested",
        "Right ear R",
        "Left ear L",
        "Tone duration",
        "Overall volume compensation",
        "Select a frequency (click to switch; the blue box marks the current one)",
        "Right ear \u00b7 1000 Hz",
        "Presentation level 40 dB",
        "\u25B6 Play the current tone",
        "\U0001F50A Heard it",
        "\U0001F507 Did not hear it",
        "Ascending method: the tone is first played at a low level; if you",
        "do not hear it",
        "the level automatically rises by 5 dB and tries again; if you",
        "hear it",
        "it probes downwards until it finds the lowest level that is just audible, which is recorded as the approximate threshold for that frequency in dB HL. You can replay the current tone or switch frequency or ear at any time.",
        "Testing progress (click a cell to jump to that ear or frequency)",
        "Right ear O\u3000Left ear X",
        "Once several frequencies have been tested, the audiogram is plotted here automatically.",
        "Copy the result JSON",
        "Save the result file",
        "\U0001F5A8 Print / export PDF",
        "Principle:",
        "Pure tone audiometry is the gold standard screening method in audiology; it records the lowest sound pressure level that is just audible at each frequency, which is the hearing threshold in dB HL. Clinically the average of 500, 1000, 2000 and 4000 Hz, the PTA, is used for the WHO grading: normal \u226425, mild 26\u201340, moderate 41\u201360, severe 61\u201380 and profound above 80 dB HL. This page generates approximate pure tones with Web Audio and estimates thresholds with an ascending method,",
        "without hardware calibration",
        ", so it is for entertainment and general education only.",
        "\U0001F4DA In-depth Analysis: Pure Tone Hearing Screening \u00b7 Audiogram",
        "Self-test the thresholds of both ears at each frequency for a first idea of whether hearing has dropped.",
        "Compare the audiograms of the left and right ears to detect unilateral hearing loss.",
        "Use the WHO grading to understand the degree of loss (normal, mild, moderate, severe or profound).",
        "Right ear 4 kHz threshold 35 dB",
        "A right ear threshold of 20 dB at 1000 Hz and 35 dB at 4000 Hz gives a PTA of about 28 dB, graded mild, suggesting a slight high-frequency drop; professional pure tone audiometry at a medical facility is recommended to confirm it.",
        "Can a web page replace professional pure tone audiometry?",
        "No. The page has no dB HL hardware calibration and the volume varies greatly between devices and headphones, so it is for entertainment and general education only and cannot be used for diagnosis or to replace an ear examination.",
        "How is the WHO grading calculated?",
        "Take the average threshold, the PTA, at 500, 1000, 2000 and 4000 Hz: normal \u226425, mild 26\u201340, moderate 41\u201360, severe 61\u201380 and profound above 80 dB HL.",
    ]))

    write('temporal-resolution-hearing', build('temporal-resolution-hearing', [
        "\U0001F442 Auditory Temporal Resolution Test \u00b7 Auditory Temporal Resolution",
        "An experimental Web Audio hearing test. It includes two paradigms: gap detection, where an adjustable gap is inserted between two bursts of white noise and you judge whether you can hear the break, and modulation detection, where amplitude modulation is added to a carrier and you judge whether you can hear the fluctuation. A 2-IFC adaptive staircase estimates millisecond-level thresholds, which are then compared with reference ranges for children, young adults and older adults. Please test in a quiet environment wearing headphones.",
        "Auditory temporal resolution test",
        "/ ENT \u00b7 Auditory Temporal Resolution Test",
        "Home",
        "\U0001F4D6 View the \"Auditory Temporal Resolution Test Guide\"",
        "Limits of use:",
        "This test is an entertainment self-test and its results are strongly affected by the device, headphones, ambient noise and individual differences;",
        "it cannot replace professional hearing and ear examinations",
        ". If you feel your hearing has dropped or you have tinnitus, please see a medical facility.",
        "\u2460 Gap detection",
        "\u2461 Modulation detection",
        "\u2462 Results and norms",
        "Testing needs access to audio output. After you grant permission, the browser creates an AudioContext to generate pure tones and noise.",
        "\U0001F50A Click to start (authorise audio)",
        "Test mode",
        "Adaptive staircase (recommended, estimates the threshold automatically)",
        "Manual listening (adjust the gap yourself)",
        "Duration of each noise burst",
        "Gap size",
        "Adaptive test progress",
        "\u25B6 Play this round (two stimuli)",
        "\u21BA Replay this round",
        "It will play in turn",
        "the first segment",
        "the second segment",
        "of white noise, with a pause between them. One segment has a silent gap in the middle and the other is continuous. After listening, judge",
        "which segment has the break",
        "The first segment has the break",
        "The second segment has the break",
        "Waiting to start\u2026",
        "\u25B6 Preview the current gap",
        "\u25B6 Preview the \"continuous, no gap\" reference",
        "In manual mode, drag the slider above to change the gap from 1 to 50 ms and compare \"with gap\" against \"continuous\", building an intuitive sense of temporal resolution. This mode does not count towards the threshold estimate.",
        "Modulation detection also needs audio authorisation; if you have already authorised it above, you can ignore this.",
        "Adaptive staircase (recommended)",
        "Manual listening",
        "Carrier frequency",
        "Modulation frequency",
        "Modulation depth",
        "It will play in turn",
        "pure tones. One segment fluctuates periodically in loudness through amplitude modulation while the other stays constant. After listening, judge",
        "which segment fluctuates",
        "The first segment fluctuates",
        "The second segment fluctuates",
        "\u25B6 Preview the current modulation",
        "\u25B6 Preview the \"constant, no modulation\" reference",
        "Drag \"modulation depth\" and \"modulation frequency\" to hear the fluctuation under different conditions. This mode does not count towards the threshold estimate.",
        "Gap threshold (ms)",
        "Modulation depth threshold (%)",
        "Gap test rounds",
        "Modulation test rounds",
        "Gap detection \u00b7 age reference ranges",
        "The values in the table are",
        "reference ranges",
        ", a rough summary based on published literature for comparison only, and not strict diagnostic cut-offs.",
        "Modulation detection \u00b7 age reference ranges",
        "After at least one adaptive test is completed, the interpretation appears here.",
        "Copy the result text",
        "Reset all tests",
        "Principle:",
        "Auditory temporal resolution is the ability of the auditory system to resolve rapid changes in temporal structure. The gap detection threshold (GDT) reflects the ability to notice brief silence, while amplitude modulation detection (AMD) reflects the ability to track loudness fluctuation. Both decline with age and relate to central auditory processing. This page uses a 2-IFC adaptive staircase, shrinking the stimulus after each correct answer and enlarging it after each wrong one, and takes the mean of the reversals in the final segment as an approximate estimate.",
        "\U0001F4DA In-depth Analysis: Auditory Temporal Resolution Test",
        "Self-test the ability to notice brief silence, that is gaps, and assess central auditory processing.",
        "Assess the ability to track loudness fluctuation, that is amplitude modulation.",
        "Compare against the age reference ranges to see whether temporal resolution has declined with age.",
        "Young adult gap threshold about 4 ms",
        "A 25-year-old subject with a gap detection threshold of 4.2 ms and a modulation depth threshold of 10% falls within the young adult reference range, so temporal resolution is essentially normal.",
        "What is the difference between gap detection and modulation detection?",
        "Gap detection judges whether a silent break can be heard between two noise bursts, while modulation detection judges whether a pure tone fluctuates periodically in loudness; together they reflect temporal resolution ability.",
        "Can the result be used as a diagnosis?",
        "No. The results are strongly affected by the device, headphones, ambient noise and individual differences, so they are for entertainment and comparison only and cannot replace professional hearing and ear examinations.",
    ]))


if __name__ == '__main__':
    main()

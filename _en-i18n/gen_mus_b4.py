#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'music')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'music')
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
    out = {'slug': slug, 'industry': 'music', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('rhythm-trainer', build('rhythm-trainer', [
        "🎮 Rhythm Trainer",
        "Tap along with the beat to train your sense of rhythm. Supports the spacebar or clicking.",
        "📖 Read the \"Rhythm Trainer User Guide\"",
        "Easy",
        "Quarter notes",
        "Medium",
        "Eighth notes",
        "Hard",
        "Sixteenth notes",
        "BPM tempo",
        "2 bars",
        "▶ Start Training",
        "Get ready...",
        "📋 Rhythm Pattern",
        "🥁 Tap",
        "or press the spacebar",
        "📊 Score Result",
        "🔍 Deviation of Each Tap",
        "1. Choose a difficulty and BPM tempo, then click \"Start Training\"\n    2. After four count-in beats, the rhythm starts playing\n    3. Press",
        "the spacebar",
        "or click",
        "the tap button",
        "4. After playback finishes, check the score and deviation analysis",
        "About the Rhythm Trainer",
        "The Rhythm Trainer is a pure front-end rhythm practice tool built on the Web Audio API. It helps music students and enthusiasts improve their sense of rhythm by randomly generating rhythm patterns of varying difficulty and evaluating tap accuracy in real time, making rhythm training simple and fun.",
        "Free BPM adjustment",
        "Real-time Web Audio sound",
        "Precise deviation analysis",
        "Pure front-end with no uploads",
        "Warm up before instrument practice",
        "Basic sense-of-rhythm training",
        "An aid for sight-singing and ear training",
        "Demonstrations in music class",
        "📚 Deep Dive: Rhythm Trainer (Deviation Feedback)",
        "Tap along with the metronome and see in real time how far you are from the beat in milliseconds, improving your timing",
        "Practice the stability of complex rhythm patterns such as syncopation and triplets",
        "Record your accuracy rate and",
        "then track your progress over time",
        "Deviation and Standard Deviation",
        "At 100 BPM (a beat of 600 ms), eight taps with deviations [+12, −8, +5, −15, +9, −3, +7, −10] ms give a mean of +0.375 and a standard deviation of about 9.4 ms. The smaller the standard deviation, the steadier you are.",
        "Syncopation Practice",
        "In two beats at 120 BPM, play a long-short-short pattern (occupying 500/250/250 ms) and the taps should land at 0, 500 and 750 ms; the feedback corrects tapping early or late.",
        "Why Does the Metronome Matter?",
        "It provides a steady reference beat so you can expose and correct dragging or rushing. Long-term practice internalizes a stable pulse and makes your playing tighter.",
        "How Much Deviation Is Acceptable?",
        "±20 to 30 ms is acceptable for amateur playing and within ±10 ms for professionals. What really matters is that the standard deviation keeps falling, not that one attempt happens to be accurate.",
    ]))
    write('guitar-fretboard', build('guitar-fretboard', [
        "📚 Guitar Fretboard Note Map",
        "An interactive guitar fretboard showing the note position of every fret, with mode highlighting and pitch playback",
        "📖 Read the \"Guitar Fretboard Note Map User Guide\"",
        "Tuning",
        "Standard (EADGBE)",
        "C major",
        "A minor",
        "G major",
        "E minor",
        "D major",
        "B minor",
        "F major",
        "D minor",
        "Display mode",
        "All notes",
        "Natural notes only",
        "In-key notes only",
        "Hidden",
        "Click a note on the fretboard to see the details",
        "Full fretboard note map for all 6 strings across frets 0 to 15",
        "Supports major and minor mode highlighting",
        "4 tunings to switch between",
        "Click a note to hear its pitch",
        "4 display modes",
        "Fret marker dots (3/5/7/9/12)",
        "Learn the note layout of the guitar fretboard",
        "Practice scale fingerings in different modes",
        "Understand how the notes change with different tunings",
        "Look up where a given note sits on the fretboard",
        "📚 Deep Dive: Guitar Fretboard Note Map",
        "Check the actual note name and frequency of a given string and fret, for memorizing the fretboard or reading transcriptions",
        "Given a root note, see where the scale or chord tones fall on the fretboard",
        "Compare open string frequencies when tuning, such as with standard tuning EADGBE",
        "Fret Spacing to Frequency",
        "In twelve-tone equal temperament each fret raises by a semitone: f = open string frequency × 2^(fret/12). The high E string open E4 = 329.63 Hz, and the 12th fret = 329.63×2 = 659.26 Hz (E5, exactly one octave up).",
        "Root Notes in Standard Tuning",
        "From low to high: E2 (82.41), A2 (110), D3 (146.83), G3 (196), B3 (246.94), E4 (329.63). The 5th fret of the low E string is A2 (110 Hz), the same note as the adjacent string's open string, which lets you cross-check.",
        "Why Is the 12th Fret One Octave Up?",
        "12 semitones make one octave, and frequency ×2^(12/12) = ×2, so the 12th fret is exactly double the open string, on every string.",
        "How Do You Memorize Open String Frequencies?",
        "Standard tuning from low to high is E A D G B E. Adjacent strings are mostly a perfect fourth apart (5 semitones), except G to B which is a perfect fourth plus a minor third. Remembering E2/A2/D3/G3/B3/E4 lets you derive every fret.",
        "How to Use the Guitar Fretboard Note Map",
        "What Does the Guitar Fretboard Note Map Do?",
        "An interactive guitar fretboard showing the note name of every string from fret 1 to 24, with mode and scale highlighting plus click-to-play auditioning. Used to memorize fretboard positions, find chord shapes and practice scales.",
        "How Do I Use the Guitar Fretboard Note Map?",
        "What Scenarios Suit the Guitar Fretboard Note Map?",
    ]))

if __name__ == '__main__':
    main()
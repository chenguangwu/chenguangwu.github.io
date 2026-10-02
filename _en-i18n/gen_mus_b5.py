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
    write('music-analysis', build('music-analysis', [
        "🎵 Audio Frequency Analyzer",
        "Detect pitch, frequency and note names in real time using the microphone",
        "\"Detect pitch, frequency and note names in real time using the microphone\" performs a professional calculation from the input parameters and outputs the result.",
        "Music Analysis",
        "/ Music Analysis",
        "📖 Read the \"Audio Frequency Analyzer User Guide\"",
        "🎤 Start Analysis",
        "Click Start Analysis",
        "Cents deviation",
        "💡 Tip: results are best with the microphone close to a single sound source such as a piano, a voice or a whistle. Browser microphone permission is required.",
        "Common frequency reference",
        "Frequency (Hz)",
        "Concert pitch (tuning reference)",
        "Middle C, the starting point of the piano's mid register",
        "High C",
        "A4 one octave down",
        "Low register",
        "Lowest note on the cello",
        "Lowest note on the guitar",
        "Audio parameter calculation",
        "Compute file size",
        "📚 Deep Dive: Audio Frequency Analyzer (Live Spectrum)",
        "Measure pitch and frequency in real time with the microphone to support ear training and tuning",
        "Visualize a voice or instrument as a spectrum to see the fundamental and harmonic distribution",
        "Capture transient peak frequencies for records in acoustics experiments",
        "Real-time Pitch Detection",
        "An FFT of the signal gives the frequency f of the largest amplitude peak, then with C0 = 16.3516 Hz the MIDI number n = 12·log2(f/C0) is computed. Rounding gives the nearest note name and the fraction ×100 gives the cent deviation, so 440 Hz yields A4 with a deviation of 0.",
        "Spectrum Observation",
        "When singing A4 the fundamental is about 440 Hz, and integer multiples such as 880 and 1320 Hz above it are the harmonics. In the spectrum chart the horizontal axis is frequency and the vertical axis is amplitude, so the row of peaks is the harmonic structure.",
        "How Does the Analyzer Find the Pitch?",
        "Autocorrelation or the FFT peak method is common: the FFT finds the highest-energy frequency as an approximation of the fundamental, while autocorrelation resists harmonic interference better. The result is then converted to a note name and cents.",
        "Why Does It Sometimes Measure Inaccurately?",
        "High noise, several notes sounding at once or a weak fundamental such as a drum will skew the result. A quiet room, a single note and a close microphone give the most stable readings.",
        "About Music Analysis",
        "Music Analysis is an online tool in the music and arts field. A music and arts tool implemented entirely in the browser, with live playback support.",
        "How to Use the Audio Frequency Analyzer",
        "Duration (seconds)",
        "What Does the Audio Frequency Analyzer Do?",
        "The audio frequency analyzer uses the microphone to detect pitch, frequency and note names in real time and visualizes sound as a spectrum, which suits ear training, tuning and acoustics experiments.",
        "How Do I Use the Audio Frequency Analyzer?",
        "What Scenarios Suit the Audio Frequency Analyzer?",
        "Sample rate",
        "Bit depth",
        "Channels",
        "Duration (seconds)",
    ]))
    write('chord-progression', build('chord-progression', [
        "🎶 Chord Progression Generator",
        "Randomly generate pop chord progressions with playback auditioning, suited to arrangement for guitar, piano and more.",
        "📖 Read the \"Chord Progression Generator User Guide\"",
        "A major",
        "B major",
        "F# major",
        "B-flat major",
        "E-flat major",
        "F#m minor",
        "C#m minor",
        "G#m minor",
        "G minor",
        "C minor",
        "16 bars",
        "Click \"Randomize\" to get a chord progression",
        "📚 Classic Progression Library",
        "Click any progression to apply it quickly to the current key and bar count",
        "About the Chord Progression Generator",
        "A chord progression is a set of chords arranged in a specific order that forms the basic harmonic framework of a piece of music. Progressions in different styles create very different emotions and atmospheres, making them a core element of songwriting and arrangement.",
        "Supports 10 major keys and 9 minor keys",
        "8 classic progressions built in",
        "Flexible 4, 8 or 16 bar configuration",
        "Adjustable BPM tempo",
        "One click copies the chord text",
        "Arrangement for guitar sing-alongs",
        "Piano accompaniment composition",
        "Songwriting inspiration",
        "Music theory study",
        "📚 Deep Dive: Chord Progression Generator (Scale Degree Movement)",
        "Generate common progressions such as I–V–vi–IV from the scale degrees of a key while writing or arranging, building a accompaniment framework fast",
        "After transcribing a track, look for alternative progressions and compare how ii–V–I and I–vi–IV–V feel differently",
        "Pair each chord of the progression with its component notes for easier piano or guitar playing",
        "C Major I–V–vi–IV",
        "The seventh-degree chords in C major are I=C, ii=Dm, iii=Em, IV=F, V=G, vi=Am and vii°=Bdim. The classic pop progression I–V–vi–IV = C → G → Am → F, where each chord takes three notes (root plus major or minor third plus perfect fifth).",
        "From Scale Degrees to Actual Chords",
        "G major I–V–vi–IV: I=G, V=D, vi=Em, IV=C, so G → D → Em → C. The V chord D consists of D, F# and A (a major triad at 0/4/7 semitones).",
        "Why Does the vi Degree Sound Sad?",
        "The vi degree is the relative minor chord. In I–V–vi–IV the vi degree pulls the major color toward the minor, creating the emotional turn common in pop songs.",
        "How Do Scale Degrees Map to Actual Chords?",
        "Fix the key first (the C major scale is C D E F G A B), take degrees 1 to 7 in turn as roots, then stack thirds to add the third and fifth. Minor keys work the same way using the natural minor scale.",
        "How to Use the Chord Progression Generator",
        "What Does the Chord Progression Generator Do?",
        "It generates common pop chord progressions in one click, supports MIDI playback auditioning and shows chord fingerings, which suits arrangement for guitar and piano and helps you build a song framework quickly.",
        "How Do I Use the Chord Progression Generator?",
        "What Scenarios Suit the Chord Progression Generator?",
    ]))

if __name__ == '__main__':
    main()
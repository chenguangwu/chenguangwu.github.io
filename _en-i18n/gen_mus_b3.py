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
    write('web-tuner', build('web-tuner', [
        "📚 Web Audio Tuner",
        "Real-time pitch detection based on the browser microphone, helping you tune guitars, basses, ukuleles and other instruments",
        "📖 Read the \"Web Audio Tuner User Guide\"",
        "Reference pitch A4:",
        "440 Hz (standard)",
        "Start Tuning",
        "Click the \"Start Tuning\" button and grant microphone access to begin pitch detection",
        "In tune",
        "Click the \"Start Tuning\" button and the browser will request microphone permission",
        "Play a single string into the microphone and wait for the pitch to stabilize",
        "The needle centered (green) means in tune, left of center is flat (orange) and right of center is sharp (red)",
        "You can tap the guitar string buttons at the bottom to set the target note reference",
        "Supports switching the A4 reference frequency (432/440/442 Hz)",
        "Tool introduction and frequently asked questions",
        "Real-time pitch detection",
        "Autocorrelation algorithm for fundamental frequency analysis",
        "Needle-style tuner visualization",
        "Deviation accurate to the cent",
        "Supports A4 = 432/440/442 Hz",
        "Quick reference for the six guitar strings",
        "Pure front-end, nothing to install",
        "No data uploaded, privacy protected",
        "Applicable instruments",
        "Guitar",
        "Bass",
        "Ukulele",
        "Violin",
        "Cello",
        "Other string instruments",
        "📚 Deep Dive: Online Tuner (Microphone Pitch Detection)",
        "Tune a guitar or ukulele against the microphone and watch the needle and cent deviation",
        "Measure the deviation direction (sharp or flat) when an instrument goes out of tune, then fine-tune the pegs",
        "Demonstrate the concept of cents in class; within ±5 cents counts as in tune",
        "From Frequency to Note Name and Cents",
        "C0 = 16.3516 Hz and n = 12·log2(f/C0); 440 Hz gives n=69, so A4, and cents = (69−69)×100 = 0 (in tune). 446 Hz gives n≈69.246, or +24.6 cents (sharp).",
        "Deciding Whether It Is In Tune",
        "When the needle is centered and |cents| ≤ 5 it shows \"In tune\"; +24.6 cents shows \"Sharp\", so loosen the string to bring the frequency down toward 440 Hz.",
        "How Does a Tuner Work?",
        "The microphone captures sound, FFT or autocorrelation yields the fundamental frequency, twelve-tone equal temperament gives the nearest note name and cent deviation, and the needle indicates sharp or flat so you can turn the peg accordingly.",
        "Is ±5 Cents a Reasonable Definition of In Tune?",
        "Human pitch resolution is about 5 to 6 cents, and ensemble playing demands more (often under 3). Within ±5 cents is enough for solo playing and practice.",
        "About Web Audio Tuner",
        "The online tuner detects pitch through the Web Audio API and supports tuning guitars, basses, ukuleles and other instruments, showing the frequency, note and deviation. A music and arts tool implemented entirely in the browser, with live playback support.",
        "How to Use the Web Audio Tuner",
        "What Does the Web Audio Tuner Do?",
        "It uses the browser microphone to capture sound in real time and analyzes the pitch with Web Audio, showing the current note name and deviation to help guitars, basses, ukuleles and other string instruments tune quickly. Pure front-end, no network needed.",
        "How Do I Use the Web Audio Tuner?",
        "What Scenarios Suit the Web Audio Tuner?",
    ]))
    write('detector', build('detector', [
        "🔍 BPM Detection (Tap the Beat)",
        "Tap the button along with the beat of the music to automatically compute beats per minute (BPM)",
        "📖 Read the \"BPM Detection (Tap the Beat) User Guide\"",
        "BPM = 60 ÷ average tap interval (seconds); the average interval = Σ of the time differences between adjacent taps ÷ (tap count − 1). Tempo terms are banded by BPM: below 60 is Largo, 60 to 76 is Adagio, 76 to 108 is Andante, 108 to 120 is Moderato, 120 to 168 is Allegro, and above 168 is Presto. Tapping 8 to 16 times in a row improves stability; discard the first tap if needed to remove the start-up error.",
        "Average interval (ms)",
        "Tempo terms",
        "Tap the beat",
        "🎼 Tempo Term Reference",
        "BPM range",
        "Italian term",
        "Grave / Larghissimo",
        "Lento",
        "Largo",
        "Andante",
        "Allegro",
        "Vivace",
        "Presto",
        "Prestissimo",
        "📚 Deep Dive: BPM Detection (Tap the Beat)",
        "Listen to a track and tap the button or spacebar to estimate its BPM automatically",
        "Record each tap interval while practicing along with the beat to check your steadiness",
        "Roughly measure the tempo of untagged audio, which helps with sorting and mixing",
        "Computing BPM from the Average Interval",
        "Successive tap intervals of 500, 505, 495 and 500 ms give an average of 500 ms, so BPM = 60000/500 = 120 (around the Moderato and Allegro boundary).",
        "BPM below 60 is Largo, 66 to 76 is Adagio, 76 to 108 is Andante, 108 to 120 is Moderato, 120 to 168 is Allegro, and above 168 is Presto.",
        "How Many Taps Are Needed for Accuracy?",
        "Averaging at least 4 to 8 taps is more reliable. The first one or two taps are often inaccurate because of the start, so discard them and average the stable middle section.",
        "Why Does the Result Sometimes Double or Halve?",
        "If you happen to tap every off-beat or every two beats, the average interval becomes twice or half the value. Compare against the tempo terms to judge whether it matches what you hear.",
        "At least 3 taps are needed for a reasonably accurate BPM",
        "Taps more than 2 seconds apart reset the timer automatically",
        "Tap evenly along with the beat, avoiding sudden fast and slow changes",
        "The BPM calculation uses the average interval of the most recent 8 taps",
        "Supports tapping quickly with the spacebar",
        "About BPM Detection (Tap the Beat)",
        "The BPM detector measures beats per minute of the music by tapping the beat, which suits music production, DJ mixing and beat training.",
        "Large buttons for tapping the beat, with intuitive operation",
        "Automatically identifies the tempo term from Largo to Prestissimo",
        "Dynamically averaged from the most recent taps for stable results",
        "Let a DJ pin down the BPM of a track for beat-matched mixing",
        "Setting the beat when producing music",
        "Tempo perception training while studying music",
        "An aid for metronome calibration",
        "How to Use BPM Detection (Tap the Beat)",
        "What Does BPM Detection (Tap the Beat) Do?",
        "Tap along with the beat of the music using the button or the spacebar; the tool automatically records each tap interval, averages them, and computes both beats per minute (BPM) and the tempo term such as Andante or Allegro. Used to measure song tempo and practice keeping the beat.",
        "How Do I Use BPM Detection (Tap the Beat)?",
        "What Scenarios Suit BPM Detection (Tap the Beat)?",
    ]))
    write('bpm-converter', build('bpm-converter', [
        "🏎️ BPM Tempo Converter",
        "Convert between BPM and note duration, delay times, LFO frequency and sample length, essential for music production and DJing",
        "\"Convert between BPM and note duration, delay times, LFO frequency and sample length, essential for music production and DJing\" performs a professional calculation from the input parameters and outputs the result.",
        "BPM Tempo Converter",
        "/ BPM Tempo Converter",
        "📖 Read the \"BPM Tempo Converter User Guide\"",
        "BPM value (40-300)",
        "🎶 Note Duration",
        "Click any card to copy the value",
        "⏲ Delay Time",
        "Synchronized time values suited to delay effects",
        "🌈 LFO Frequency",
        "Convert BPM to LFO sync frequency (Hz), click to copy",
        "🎧 Sample Length",
        "🔀 Reverse Calculation: Duration to BPM",
        "Enter a duration (ms) to compute the matching BPM automatically",
        "Duration (ms)",
        "Note type",
        "Dotted quarter",
        "One bar (4/4)",
        "About the BPM Tempo Converter",
        "BPM (beats per minute) is the most fundamental tempo metric in music production. This tool helps you convert quickly between BPM and various time values, and suits music production, DJ mixing, arrangement and audio engineering.",
        "Convert between BPM and note duration",
        "Compute synchronized delay times",
        "Convert LFO frequency",
        "Compute sample length precisely",
        "Derive BPM backwards from a duration",
        "Quick presets for common tempos",
        "One click copies every result",
        "Supports multiple sample rates",
        "Compute precise note durations while arranging",
        "Match the BPM of two tracks in DJ mixing",
        "Set synchronized times on a delay effect",
        "Sync LFO parameters to the BPM",
        "Align audio sample loops with the beat",
        "Convert between MIDI note values and milliseconds",
        "📚 Deep Dive: BPM Tempo Converter (Duration, LFO, Samples)",
        "Convert BPM to quarter-note milliseconds while arranging, aligning the note grid and delay times",
        "Set an LFO or vibrato frequency synced to the BPM, such as one filter sweep per beat",
        "Compute how many sample points a note occupies at a given sample rate for precise slicing",
        "BPM to Note Duration",
        "At 120 BPM a quarter note = 60000/120 = 500 ms; an eighth = 250 ms, a sixteenth = 125 ms and a dotted quarter = 500×1.5 = 750 ms.",
        "LFO and Sample Count",
        "At 120 BPM each beat lasts 500 ms. For an LFO with one cycle per beat, frequency = 1000/500 = 2 Hz. At a sample rate of 44100 Hz a quarter note equals round(500/1000×44100) = 22050 samples.",
        "How Do You Convert Between BPM and Milliseconds?",
        "Quarter-note milliseconds = 60000 / BPM; given the milliseconds ms of a note, the matching BPM = 60000 × beats of that note / ms (for example an eighth note is 0.5 beats).",
        "How Do You Compute LFO Sync Frequency?",
        "Period milliseconds = quarter-note milliseconds × multiplier (1 for every beat, 2 for every two beats), and frequency (Hz) = 1000 / period milliseconds. For example once per bar (4 beats) gives 1000/(500×4) = 0.5 Hz.",
    ]))

if __name__ == '__main__':
    main()
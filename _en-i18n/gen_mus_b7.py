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
    write('index', build('index', [
        "🎵 Music and Arts Tools",
        "Music and Arts",
        "Music and Arts Tools",
        "Choose a note value (quarter, eighth, triplet, dotted and more) and a tempo (BPM) to compute the exact duration of each subdivided note and visualize the bar structure, with click-to-play practice. Useful for music theory study and rhythm training.",
        "Chord Progression Generator",
        "🎶 Chord Progression Generator",
        "The scale generator produces note name sequences for modes such as major, minor and pentatonic scales and supports auditioning, which suits music theory study, improvisation and instrument practice as a reference.",
        "Audio Conversion",
        "It compares the characteristics of common audio formats such as WAV, MP3 and FLAC, computes the raw PCM file size from the sample rate, bit depth and channel count, and explains the key points of bitrate conversion and sample rate conversion. Used for estimating size and choosing formats before audio processing.",
        "Two-way conversion between Hz frequency and note names · Twelve-tone equal temperament · Web Audio auditioning",
        "BPM Tempo Converter",
        "⏱️ BPM Tempo Converter",
        "Enter the original and target BPM to compute the tempo ratio and apply time stretching to the audio, with real-time auditioning and fine adjustment. Used for cover transpositions, practicing an instrument against a track and other music creation and practice scenarios.",
        "Enter a chord name such as Cmaj7 or Am to parse its component notes and the frequency of each note, then highlight them on the piano keyboard. Used to study chord composition, arrange accompaniment and train sight-singing and ear training.",
        "Randomly plays rhythm patterns that you must tap along with, training your beat sense and steadiness while reporting accuracy and tempo. Suitable as a first step for instruments and runs entirely in the browser.",
        "Music Player",
        "Upload a local audio file such as MP3 or WAV and get play and pause, seek dragging, volume control and multi-track playlist management. Used to play local music directly in the browser with no extra software to install.",
        "Music Analysis",
        "The audio frequency analyzer uses the microphone to detect pitch, frequency and note names in real time and visualizes sound as a spectrum, which suits ear training, tuning and acoustics experiments.",
        "Tap along with the beat of the music using the button or the spacebar; the tool automatically records each tap interval, averages them, and computes both beats per minute (BPM) and the tempo term such as Andante or Allegro. Used to measure song tempo and practice keeping the beat.",
        "The ear trainer plays intervals and chords through the Web Audio API and trains your listening recognition. Repeated practice builds the listening foundation for sight-singing, improvisation and composition, which suits music learners.",
        "An interactive guitar fretboard showing the note name of every string from fret 1 to 24, with mode and scale highlighting plus click-to-play auditioning. Used to memorize fretboard positions, find chord shapes and practice scales.",
        "Tap along with the metronome using the spacebar or by clicking, with real-time feedback on how far each tap is from the beat, training rhythmic stability and pulse feel. Used for rhythm training by drummers and instrumentalists.",
        "Web Audio Tuner",
        "🎤 Web Audio Tuner",
        "Jianpu Lookup",
        "Choose a key signature such as C major, G major or F major and see the correspondence table of jianpu numbers (1 to 7), staff positions and solfege or note names for that key. Used for translating between jianpu and staff notation, sight-singing and quick theory reference.",
        "Virtual Piano Keyboard",
        "⌨️ Virtual Piano Keyboard",
        "Music Theory",
        "The music theory learner provides scale and chord lookups plus a piano keyboard for auditioning, covering the common modes and chord compositions. Suitable for starting music theory and for quick harmony reference.",
        "About Music and Arts Tools",
        "This collection gathers 19 free online tools covering the common calculation, conversion and lookup needs of music and arts scenarios. Whether you are a practitioner, a student or an ordinary user, you will find a ready-to-use utility here. Every tool runs entirely in the browser and uploads no data to the server, so your privacy is protected.",
        "The music and arts tools included on this page are (representative tools):",
        "These tools help you finish common music and arts tasks quickly, with no formulas to memorize and no manual conversion needed. Enter and you get the result.",
        "Do the music and arts tools require a download or registration?",
        "No. Every tool on this page runs entirely in the browser. Open the page and use it right away, with nothing to install, no account to create, and no data uploaded.",
        "Are the results of the music and arts tools accurate? Is my data safe?",
        "Each tool computes locally in your browser from public mathematical formulas and general industry standards, so results are available instantly. All computation happens on your own device, nothing is uploaded to the server, and your privacy is fully protected.",
    ]))
    write('ear-trainer', build('ear-trainer', [
        "🎮 Ear Trainer",
        "Listen and identify intervals and chords to improve your musical ear",
        "📖 Read the \"Ear Trainer User Guide\"",
        "🎵 Interval Recognition",
        "🎶 Chord Recognition",
        "Played together",
        "Played one after another (arpeggio)",
        "Click play, listen and then choose an answer",
        "📊 Training Statistics",
        "Correct count",
        "Streak",
        "📖 Interval Reference",
        "About the Ear Trainer",
        "The Ear Trainer is an online listening training tool built on the Web Audio API that helps you improve your musical ear. By practicing interval and chord recognition repeatedly you can hear pitch relationships faster, laying a solid foundation for sight-singing and ear training, improvisation and composition.",
        "Interval recognition (12 intervals)",
        "Chord recognition (major, minor, augmented, diminished)",
        "Two playback modes: together or arpeggiated",
        "Real-time statistics and streak counting",
        "Pure front-end processing, no network needed",
        "Daily ear training for music students",
        "An aid for music theory classes",
        "Choir and band listening training",
        "Self-study for music enthusiasts",
        "📚 Deep Dive: Ear Trainer (Interval and Chord Recognition)",
        "Listen to two notes and judge the interval (from a minor second to a major seventh) to train relative pitch",
        "Listen to a chord and judge its type (major, minor, dominant seventh and so on) to improve harmonic recognition",
        "Repeated random questions with instant feedback build the mapping between intervals and what you hear",
        "Intervals in Semitones",
        "The semitone difference between adjacent note names: minor second 1, major second 2, minor third 3, major third 4, perfect fourth 5, tritone 6, perfect fifth 7, minor sixth 8, major sixth 9, minor seventh 10, major seventh 11, octave 12.",
        "Chord Recognition",
        "C-E-G sounding together is major (bright), C-E♭-G is minor (soft) and C-E-G-B♭ is a dominant seventh (tense). Distinguish them by color and completeness.",
        "How Do You Train Relative Pitch?",
        "Start with intervals that have a distinctive color such as the perfect fifth and the major third, memorize a reference song (the perfect fifth at the opening of Star Wars, for example), then extend to every semitone level.",
        "Where Should Chord Recognition Start?",
        "First separate major and minor chords (bright and dark), then add the dominant seventh (a sense of resolution) and the major seventh (the soft glow of jazz). After each listen, check the answer to build auditory memory.",
    ]))

if __name__ == '__main__':
    main()
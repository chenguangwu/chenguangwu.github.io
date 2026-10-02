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
    write('audio-converter', build('audio-converter', [
        "🔄 Audio Format Conversion Parameters",
        "Audio format comparison, bitrate calculation and sample rate conversion explained",
        "\"Audio format comparison, bitrate calculation and sample rate conversion explained\" performs a professional calculation from the input parameters and outputs the result.",
        "Audio Conversion",
        "/ Audio Format",
        "📖 Read the \"Audio Format Conversion Parameters User Guide\"",
        "Common audio format comparison",
        "PCM file size calculation",
        "Sample rate conversion notes",
        "Audio quality",
        "Size per minute (16bit/stereo)",
        "Telephone grade",
        "Telephone, voice walkie-talkie",
        "AM broadcast",
        "Voice, short audio",
        "CD quality",
        "Music CD, streaming",
        "DVD quality",
        "Video, professional audio",
        "High resolution",
        "Professional recording, Blu-ray",
        "Ultra high resolution",
        "Mastering, Hi-Res",
        "Bit depth notes",
        "Dynamic range",
        "Old games, telephone",
        "CD standard",
        "Professional recording, mastering",
        "DAW, professional production",
        "📚 Deep Dive: Audio Format and Bitrate Conversion",
        "Estimate file size from sample rate, bit depth and channels before exporting, then pick the right format",
        "Compare the size difference between lossless WAV and lossy MP3 to make storage and upload decisions",
        "Unify sample rates across different material to avoid resampling loss inside the DAW",
        "PCM Bitrate and Size",
        "44100 Hz / 16 bit / stereo gives byte rate = 44100 × 16/8 × 2 = 176400 B/s = 1411.2 kbps; each minute is about 10.09 MB, and 10 minutes of WAV is about 100.9 MB.",
        "Size After MP3 Conversion",
        "For the same 3 minutes of audio: MP3 320 kbps is about 320×180/8/1024 ≈ 7.03 MB; 192 kbps ≈ 4.22 MB; 128 kbps ≈ 2.81 MB (WAV would be about 30.3 MB).",
        "How Much Do 44100 and 48000 Differ?",
        "44100 is the CD standard while 48000 is the video and professional standard. The size difference is about 9% since byte rate is proportional to sample rate, and mixes are often unified to 48000 before delivery.",
        "Is a Higher MP3 Bitrate Always Better?",
        "A higher bitrate means a larger file that is closer to lossless; 192 kbps is already close to CD listening quality and 320 is the highest bitrate. Web distribution commonly uses 128 to 192 to balance size and quality.",
        "About Audio Conversion",
        "Audio Conversion is an online tool in the music and arts field. A music and arts tool implemented entirely in the browser, with live playback support.",
        "How to Use Audio Format Conversion Parameters",
        "Sample rate (Hz)",
        "Duration (seconds)",
        "What Does Audio Format Conversion Parameters Do?",
        "It compares the characteristics of common audio formats such as WAV, MP3 and FLAC, computes the raw PCM file size from the sample rate, bit depth and channel count, and explains the key points of bitrate conversion and sample rate conversion. Useful for estimating size and choosing formats before audio processing.",
        "How Do I Use Audio Format Conversion Parameters?",
        "What Scenarios Suit Audio Format Conversion Parameters?",
        "Sample rate (Hz)",
        "Bit depth",
        "Channels",
        "Duration (seconds)",
    ]))
    write('beat-subdivision', build('beat-subdivision', [
        "🎵 Beat Subdivision Calculator",
        "Compute the exact duration of note values, dotted notes and triplets, with a visual bar structure",
        "\"Compute the exact duration of note values, dotted notes and triplets, with a visual bar structure\" performs a professional calculation from the input parameters and outputs the result.",
        "📖 Read the \"Beat Subdivision Calculator User Guide\"",
        "BPM (tempo)",
        "Note value table",
        "Bar visualization",
        "Metronome",
        "BPM comparison",
        "Note duration reference",
        "A dotted note equals the original value × 1.5; a triplet equals the original value × 2/3, dividing the original note evenly into three parts. Eighth-note triplets are common in solo fills, and sixteenth-note triplets appear often in jazz.",
        "Bar subdivision structure",
        "Subdivision precision",
        "Whole note",
        "Half note",
        "Quarter-note triplet",
        "Eighth-note triplet",
        "Sixteenth-note triplet",
        "Click a square to play the sound of that subdivision. Each beat is separated by a space and the number gives the beat position. A darker color means a later subdivision.",
        "Choose a subdivision type and click the play button to start practicing",
        "Metronome BPM",
        "Accent volume",
        "Off-beat volume",
        "Make sure the device is not muted; headphones work better. The metronome uses the Web Audio API and needs no network connection.",
        "BPM Duration Difference",
        "Enter two BPM values to see the duration difference of each note value",
        "Tool Introduction and User Guide",
        "The Beat Subdivision Calculator helps musicians, composers and students compute note values precisely. Whether standard notes, dotted notes or triplets, it gives exact durations down to the millisecond, and with the visual bar chart and the built-in metronome it makes rhythm practice more efficient.",
        "Supports 9 time signatures (2/4, 3/4, 4/4, 5/4, 6/8, 7/8, 3/8, 9/8, 12/8)",
        "Computes 18 note values (6 each for plain, dotted and triplet)",
        "Visual bar structure grid",
        "Web Audio API metronome supporting subdivision practice",
        "BPM comparison to see differences at a glance",
        "Exports the results as a text file",
        "Set note values precisely during MIDI production",
        "Compute durations before practicing a complex rhythm",
        "Compare playing difficulty at different tempos",
        "Confirm beat subdivision while arranging",
        "Explain note value relationships in teaching",
        "A shared tempo reference for band rehearsal",
        "📚 Deep Dive: Beat Subdivision Calculator (Note Milliseconds)",
        "Convert BPM and note values to milliseconds while reading music, aligned with the project grid",
        "Look up the duration of each note instantly when legato or dotted notes are confusing",
        "Set subdivision steps for a drum machine or sequencer (for example a sixteenth note at 125 ms)",
        "Regular Subdivision",
        "At 120 BPM a quarter note lasts 500 ms; an eighth note = 250 ms, a sixteenth note = 125 ms, a dotted quarter = 750 ms and a dotted eighth = 375 ms.",
        "Splitting one beat (500 ms) into three at 120 BPM gives an eighth-note triplet of about 166.7 ms each (3 fill one beat); a quarter-note triplet places 3 notes in 2 beats, about 333.3 ms each.",
        "Why Is a Dotted Note ×1.5?",
        "A dot extends the note by half its value, so a dotted quarter = quarter + eighth = 500 + 250 = 750 ms, that is the original duration × 1.5.",
        "How Do You Tell a Triplet from Regular Eighth Notes?",
        "Two regular eighth notes fill one beat (250 ms each), while an eighth-note triplet places 3 notes in one beat (about 166.7 ms each), which is denser and evenly split into three.",
        "About Beat Subdivision Calculator",
        "Beat Subdivision Calculator: computes the exact duration of note values, dotted notes and triplets, with time signature selection, bar visualization, a Web Audio metronome and BPM comparison. A music and arts tool implemented entirely in the browser, with live playback support.",
    ]))
    write('music-theory', build('music-theory', [
        "📚 Music Theory Learner",
        "Scales, chord lookups and piano playback",
        "Music Theory",
        "/ Music Theory",
        "📖 Read the \"Music Theory Learner User Guide\"",
        "Choose a root note",
        "Major scale (natural major)",
        "Minor scale (natural minor)",
        "Harmonic minor",
        "Melodic minor",
        "Major pentatonic",
        "Minor pentatonic",
        "Dorian mode",
        "Phrygian mode",
        "Lydian mode",
        "Mixolydian mode",
        "Locrian mode",
        "Common chord lookup",
        "Major triad (Major)",
        "Minor triad (Minor)",
        "Diminished triad (Dim)",
        "Augmented triad (Aug)",
        "Major seventh chord (Maj7)",
        "Dominant seventh chord (7)",
        "Minor seventh chord (m7)",
        "Diminished seventh chord (dim7)",
        "Half-diminished chord (m7b5)",
        "Suspended fourth chord (sus4)",
        "Suspended second chord (sus2)",
        "Add nine chord (add9)",
        "🎹 Virtual Piano",
        "Click a key to hear a single note",
        "📚 Deep Dive: Music Theory Quick Reference (Scales, Chords, Keyboard)",
        "Look up the interval structure and note names of major, minor and pentatonic scales",
        "See the component note templates of each chord type (major, minor, augmented, diminished, seventh)",
        "Click notes on the keyboard to hear the pitch and build the mapping between note names and positions",
        "Scale Intervals",
        "The natural major semitone intervals are [0,2,4,5,7,9,11], the natural minor [0,2,3,5,7,8,10], the major pentatonic [0,2,4,7,9] and the minor pentatonic [0,3,5,7,10].",
        "Chord Templates",
        "Major [0,4,7], minor [0,3,7], augmented [0,4,8], diminished [0,3,6], dominant seventh [0,4,7,10], major seventh [0,4,7,11]; the root plus the intervals gives the component notes.",
        "What Is the Relationship Between Scales and Chords?",
        "Chords are usually built by stacking scale degrees in thirds. For example a major tonic chord uses degrees 1, 3 and 5 while vii° uses degrees 7, 2 and 4, so knowing scales explains where most chords come from.",
        "How Do You Memorize the Black-Key Pattern?",
        "Within a group of 12 keys the black keys group in pairs or threes, matching the semitone changes. C major uses white keys only (no sharps), and each added sharp in the key signature brings one more black key, landing on notes such as #F and #C.",
        "About Music Theory",
        "Music Theory is an online tool in the music and arts field. A music and arts tool implemented entirely in the browser, with live playback support.",
        "How to Use the Music Theory Learner",
        "What Does the Music Theory Learner Do?",
        "The music theory learner provides scale and chord lookups plus a piano keyboard for auditioning, covering the common modes and chord compositions. Suitable for starting music theory and for quick harmony reference.",
        "How Do I Use the Music Theory Learner?",
        "What Scenarios Suit the Music Theory Learner?",
    ]))

if __name__ == '__main__':
    main()
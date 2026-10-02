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
    write('music-player', build('music-player', [
        "🎵 Local Music Player",
        "Upload a local audio file with playback control and a playlist",
        "Music Player",
        "/ Music Player",
        "📖 Read the \"Local Music Player User Guide\"",
        "Playback progress = current time ÷ total duration × 100%; seeking = target percentage × total duration; volume maps linearly or logarithmically from 0 to 1 to decibels (dB = 20 × log₁₀(volume)). The playlist is indexed sequentially or randomly, using a Fisher-Yates shuffle when playing randomly without repeats. When the playback rate changes, total duration = original duration ÷ rate.",
        "No track selected",
        "Please upload an audio file",
        "📁 Choose an audio file",
        "🔁 Repeat one",
        "🔀 Shuffle",
        "📚 Deep Dive: Local Music Player (Playlist)",
        "Play local MP3 or WAV files directly in the browser with no player software to install",
        "Build a multi-track playlist for continuous listening and drag the progress bar to reach a passage",
        "Adjust the volume or pause for background music or practice accompaniment",
        "Playlist Management",
        "Select 5 audio files at once and the list order is the playback order. Click a track to jump to it, and drag to seek.",
        "Progress Bar",
        "Resume at 1:23 without reloading.",
        "Volume Control",
        "The volume slider maps to the Web Audio GainNode (linear from 0 to 1), where 0.5 is about half the loudness. Pausing keeps the current position and resumes from there.",
        "Are the Files Uploaded to a Server?",
        "No. The player reads local files through the browser File API, and audio only plays in local memory with no network upload, so your privacy is protected.",
        "Which Formats Are Supported?",
        "It depends on the browser decoder. Common formats such as MP3, WAV, OGG and AAC usually play, while FLAC needs transcoding or is unsupported in some browsers.",
        "About Music Player",
        "Music Player is an online tool in the music and arts field. A music and arts tool implemented entirely in the browser, with live playback support.",
        "Previous track",
        "Play / Pause",
        "Next track",
    ]))
    write('convert-speed', build('convert-speed', [
        "🏎️ Song Speed Conversion (Fine BPM Adjustment)",
        "Song speed change: new duration = original duration × (original BPM / new BPM)",
        "📖 Read the \"Song Speed Conversion (Fine BPM Adjustment) User Guide\"",
        "Original duration (seconds)",
        "Original BPM",
        "New BPM",
        "Speed Conversion Principle",
        "After a speed change the duration is original duration × (original BPM / new BPM), based on the linear relationship between playback speed and time. The faster the beat, the shorter the duration.",
        "📚 Deep Dive: Song Speed Conversion (Fine BPM Adjustment)",
        "Raise or lower the speed of a cover while keeping the pitch, by computing the new duration and the speed-up factor first",
        "Estimate the duration change when a DJ mixes two tracks with different BPM",
        "Slow down a track for easier practice and derive the target BPM backwards",
        "Computing the New Duration When Speeding Up",
        "An original track of 4 minutes (240 s) at 120 BPM raised to 140 gives new duration = 240 × (120/140) ≈ 205.7 s; the speed-up is (140/120 − 1)×100% ≈ 16.7%.",
        "Deriving the Target BPM Backwards",
        "From 180 s at 120 BPM, to practice a slow version at 220 s, the target BPM = 120 × (180/220) ≈ 98.2 BPM (about 18% slower).",
        "Does Changing Speed Change the Pitch?",
        "Changing only the playback rate also changes the pitch (faster means higher). To preserve pitch you need a time-stretching algorithm such as elastique in a DAW, while the duration still changes in proportion to the BPM.",
        "Why Does the Duration Formula Use Original BPM / New BPM?",
        "Duration is inversely proportional to BPM: a larger BPM plays faster and shortens the duration, so the ratio factor is original BPM / new BPM, and multiplying the original duration gives the new duration.",
        "About Song Speed Conversion (Fine BPM Adjustment)",
        "Song Speed Conversion (Fine BPM Adjustment). A music and arts tool implemented entirely in the browser, with live playback support.",
    ]))
    write('random-training-rhythm', build('random-training-rhythm', [
        "🎲 Rhythm Training (Random Rhythm Tapping)",
        "Random rhythm tapping",
        "📖 Read the \"Rhythm Training (Random Rhythm Tapping) User Guide\"",
        "Rhythm accuracy = hit beats ÷ total beats × 100%. The deviation of a single tap = actual tap time − standard beat time (positive means late, negative means early), and the mean deviation = Σ deviation ÷ count. Steadiness can be measured by the standard deviation of the deviations, with a standard deviation below 30 ms considered stable. The beat interval = 60000 ÷ BPM milliseconds, so 120 BPM gives 500 ms.",
        "📚 Deep Dive: Random Rhythm Training (Tap Along)",
        "Drummers and instrumentalists tap along to random rhythm patterns with the spacebar or by clicking to build a steady pulse",
        "Set the BPM to align with the metronome and watch the tap deviation in real time to improve timing accuracy",
        "Switch between subdivisions such as eighth notes, sixteenth notes and triplets to read complex rhythms",
        "Deviation Feedback",
        "With the metronome at 100 BPM (a beat of 600 ms), you should tap within ±30 ms of the beat. A continuous deviation of +120 ms means you are dragging overall and need to start earlier.",
        "Subdivision Practice",
        "At 120 BPM the eighth-note interval is 250 ms, the sixteenth note 125 ms, and an eighth-note triplet places 3 notes within 500 ms (about 166.7 ms each). Random questions train you to switch between intervals.",
        "What Is the Scoring Based On?",
        "Using the metronome beats as the reference, it records",
        "for each tap, computing the deviation in milliseconds from the nearest beat along with",
        "and the steadier you are the closer it is to 0.",
        "Why Are Triplets Hard to Follow?",
        "A triplet splits one beat evenly into 3 parts (not 2 or 4), while the brain is used to binary rhythm. Internalize the even spacing of 166.7 ms per note at a slow tempo first, then speed up.",
        "About Rhythm Training (Random Rhythm Tapping)",
        "Rhythm Training (Random Rhythm Tapping). A music and arts tool implemented entirely in the browser, with live playback support.",
    ]))
    write('generator-1', build('generator-1', [
        "🎵 Scale Generator (Major, Minor, Pentatonic)",
        "Major / Minor / Pentatonic",
        "📖 Read the \"Scale Generator (Major, Minor, Pentatonic) User Guide\"",
        "Scales are generated from their interval structure: major is whole whole half whole whole whole half (five major seconds plus two minor seconds), the natural minor is whole half whole whole half whole whole, the harmonic minor raises the seventh degree, and the pentatonic scale drops the fourth and seventh degrees. Frequencies follow twelve-tone equal temperament, f = f₀ × 2 raised to the power of (n ÷ 12), where f₀ takes A4 = 440 Hz and n is the relative semitone count. For example C4 = 261.63 Hz and G4 = 392.00 Hz.",
        "📚 Deep Dive: Scale Generator (Major, Minor, Pentatonic)",
        "Generate the note name sequence of a scale in a given key before practicing an instrument, and follow it to run scales or sight-sing",
        "Load the scale of the relevant mode before improvising so you avoid notes outside the key",
        "Compare the interval structure of the natural major, natural minor and pentatonic scales in class",
        "C Natural Major",
        "Starting from the root with the semitone intervals [0,2,4,5,7,9,11] you get C D E F G A B; moving the same pattern to the root G gives G A B C D E F#.",
        "A Minor Pentatonic",
        "The minor pentatonic intervals [0,3,5,7,10] starting from A give A C D E G (no degrees 4 and 7), which is common in blues and rock improvisation and hard to get wrong.",
        "Where Do Major and Minor Scales Differ?",
        "They differ in degrees 3, 6 and 7: the natural minor lowers each of the major scale's 3, 6 and 7 by a semitone (the intervals become [0,2,3,5,7,8,10]), turning the sound from bright to soft.",
        "Why Does the Pentatonic Scale Sound Good and Rarely Clash?",
        "The pentatonic scale removes the minor seconds that easily create dissonance (such as 4 against 3 or 7 against 1), so any combination of its notes tends to be consonant, which suits improvisation and teaching children.",
        "About Scale Generator (Major, Minor, Pentatonic)",
        "Scale Generator (Major, Minor, Pentatonic). A music and arts tool implemented entirely in the browser, with live playback support.",
    ]))

if __name__ == '__main__':
    main()
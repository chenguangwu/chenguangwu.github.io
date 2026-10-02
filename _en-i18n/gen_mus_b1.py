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
    write('chord-notes', build('chord-notes', [
        "🔄 Chord Note Converter",
        "Enter a chord name to see its component notes and frequencies, visualized on the piano keyboard",
        "📖 Read the \"Chord Note Converter User Guide\"",
        "Press Enter to analyze",
        "🔍 Analyze Chord",
        "🔊 Play Chord",
        "🎹 Piano Keyboard",
        "⚡ Common Chord Quick Reference",
        "Click to fill in a chord name and analyze it",
        "Triads",
        "Seventh chords",
        "Suspensions and additions",
        "📖 Chord Interval Rules Reference",
        "Chord type",
        "Notation example",
        "Intervals (semitones)",
        "Major triad",
        "Root, major third, perfect fifth",
        "Minor triad",
        "Root, minor third, perfect fifth",
        "Augmented triad",
        "Root, major third, augmented fifth",
        "Diminished triad",
        "Root, minor third, diminished fifth",
        "Major seventh chord",
        "Major triad plus major seventh",
        "Minor seventh chord",
        "Minor triad plus minor seventh",
        "Dominant seventh chord",
        "Major triad plus minor seventh",
        "Diminished seventh chord",
        "Diminished triad plus diminished seventh",
        "Half-diminished seventh chord",
        "Diminished triad plus minor seventh",
        "Suspended second chord",
        "Root, major second, perfect fifth",
        "Suspended fourth chord",
        "Root, perfect fourth, perfect fifth",
        "Add nine chord",
        "Major triad plus the ninth",
        "Sixth chord",
        "Major triad plus the sixth",
        "Minor sixth chord",
        "Minor triad plus the sixth",
        "Chord Note Converter is a pure front-end music theory tool that parses 15 common chord types, shows the component notes with their frequencies, and highlights them on a virtual piano keyboard. All computation runs locally in the browser with no network requests, so your data stays safe.",
        "Supports 15 chord types including major, minor, augmented, diminished, seventh and suspended chords",
        "Shows each note name with its frequency (based on A4 = 440 Hz)",
        "Visualizes the chord on the piano keyboard with the component notes highlighted",
        "Audible playback through the Web Audio API, for a single note or the whole chord",
        "Quick reference table of common chords, one click to fill in and analyze",
        "Pure front-end processing with no backend service, protecting your privacy",
        "Study music theory and look up chord composition quickly",
        "Confirm chord tones while arranging",
        "Reference chord fingerings during instrument practice",
        "An aid for music teaching",
        "📚 Deep Dive: Chord Composition Lookup",
        "Enter chord names such as C, Am, G7 or F#m7 to see the actual component notes and frequencies",
        "Confirm chord spelling while arranging so you neither omit nor add tones",
        "Work with piano or guitar fingerings to see where each note sits on the keyboard or fretboard",
        "Triad Construction",
        "Stack thirds from the root: a major triad uses [0,4,7] so C = C E G; a minor triad uses [0,3,7] so Am = A C E; diminished uses [0,3,6] and augmented uses [0,4,8].",
        "A dominant seventh dom7 is [0,4,7,10] so G7 = G B D F; a minor seventh m7 is [0,3,7,10] so Am7 = A C E G; a major seventh maj7 is [0,4,7,11] so Cmaj7 = C E G B.",
        "What Do the Numbers in a Chord Name Mean?",
        "The numbers give the stacked intervals counted with the root as 1: 7 is a dominant seventh (a minor seventh), maj7 is a major seventh, and 9, 11 and 13 are extensions; m marks a minor triad, dim diminished and aug augmented.",
        "How Do I Write Any Chord from a Root Note Quickly?",
        "Memorize the interval templates and count up from the root note by semitones. For root A, a major third [0,4,7] gives A, A+4 semitones = C, A+7 = E, so A C E.",
        "Enter a chord name, e.g. C, Am, F#m7, G7, Dm7b5...",
    ]))
    write('sheet-music', build('sheet-music', [
        "📚 Jianpu and Staff Notation Lookup",
        "Choose a key signature to see the jianpu numbers, staff positions and note-name correspondence",
        "Jianpu Lookup",
        "/ Jianpu Lookup",
        "📖 Read the \"Jianpu and Staff Notation Lookup User Guide\"",
        "Key signature and scale-degree conversion: jianpu numbers 1 to 7 correspond to the seven degrees of the major scale, sung as do re mi fa sol la ti. Converting a jianpu number to a note name requires transposing by the key signature (when 1 equals C, 5 is G; when 1 equals G, 5 is D, and note name = tonic plus the semitone difference of the degree). Staff positions follow the clef and the line-space relationship: on the treble clef the space below the bottom line is middle C (C4), and octaves are written with octave marks or with jianpu octave dots.",
        "Choose a key signature",
        "Scale degree table",
        "Jianpu symbol quick reference",
        "Basic degree",
        "Higher octave",
        "Dot above the number",
        "Lower octave",
        "Dot or comma below the number",
        "Sharp",
        "Raise by a semitone",
        "Flat",
        "Lower by a semitone",
        "Double sharp",
        "Raise by a whole tone",
        "Double flat",
        "Lower by a whole tone",
        "Tie",
        "Extend by one beat (a quarter note becomes a half note)",
        "Dotted note",
        "Extend the original value by half",
        "Rest",
        "Indicates a pause",
        "Dotted note",
        "Original value plus half of the original value",
        "Trill mark",
        "trill, played in fast alternation",
        "Time signature",
        "2 beats per measure, with the quarter note as one beat",
        "3 beats per measure, common in waltzes",
        "4 beats per measure, the most common",
        "6 eighth notes per measure, a compound meter",
        "Accent mark",
        "Play this note with extra emphasis",
        "Staccato mark",
        "Short and detached notes",
        "Slur",
        "Several notes played legato",
        "Three notes played within the time of two",
        "📚 Deep Dive: Jianpu and Staff Notation Lookup",
        "Choose a key signature (C, G, F and so on) to see which note names and solfege syllables the jianpu numbers 1 to 7 map to in that key",
        "Convert jianpu to staff notation or back, as a quick reference for sight-singing and theory study",
        "Compare solfege syllables do-re-mi with note names C-D-E in class",
        "C major correspondence",
        "C major: jianpu 1 = C (do), 2 = D, 3 = E, 4 = F, 5 = G, 6 = A, 7 = B. With twelve-tone equal temperament, 1 = C4 = 261.63 Hz and 5 = G4 = 392 Hz.",
        "Transposed correspondence",
        "G major (one sharp, #F): 1 = G, 2 = A, 3 = B, 4 = C, 5 = D, 6 = E, 7 = #F. The same jianpu number maps to a different note name and pitch in each key.",
        "How Do Jianpu Numbers Map to Solfege?",
        "Jianpu numbers 1 to 7 always map to do through si. The key signature decides which note name 1 (do) falls on, and transposing means shifting the whole column of numbers to a new tonic.",
        "How Do You Derive Staff Positions from Jianpu?",
        "Fix the key signature and the clef first (on the treble clef the space below the bottom line is C4), then place each jianpu number on its line or space by scale degree, using accidentals to handle chromatic alterations within the key.",
        "About Jianpu Lookup",
        "Jianpu Lookup is an online tool in the music and arts field. A music and arts tool implemented entirely in the browser, with live playback support.",
        "How to Use Jianpu and Staff Notation Lookup",
        "What Does Jianpu and Staff Notation Lookup Do?",
        "Choose a key signature such as C major, G major or F major and see the correspondence table of jianpu numbers (1 to 7), staff positions and solfege or note names for that key. Useful for translating between jianpu and staff notation, sight-singing and quick theory reference.",
        "How Do I Use Jianpu and Staff Notation Lookup?",
        "What Scenarios Suit Jianpu and Staff Notation Lookup?",
    ]))

if __name__ == '__main__':
    main()
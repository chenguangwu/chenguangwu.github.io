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
    write('piano-keyboard', build('piano-keyboard', [
        "⌨️ Virtual Piano Keyboard",
        "\n      Play notes with the mouse or the computer keyboard, with three timbre options, octave shifting and recording with playback.\n     ",
        "📖 Read the \"Virtual Piano Keyboard User Guide\"",
        "Waiting for you to play...",
        "Timbre selection",
        "🎹 Piano",
        "🞛 Electric piano",
        "🎼 Organ",
        "Show note names",
        "Show keyboard shortcuts",
        "← Swipe left and right to see the full keyboard →",
        "📝 Recording and Playback",
        "● Start recording",
        "▶ Play back",
        "🗑 Clear recording",
        "⌨ Keyboard mapping",
        "Use the computer keyboard to play the white and black keys of the current octave:",
        "About the Virtual Piano Keyboard",
        "This is a virtual piano that runs entirely in the browser, synthesizing a realistic piano timbre with the Web Audio API. No software or plugin needs installing, so it works the moment you open the page.",
        "Timbres synthesized with the Web Audio API",
        "Three timbres: piano, electric piano and organ",
        "Play with keyboard shortcuts",
        "Record your playing sequence",
        "Play back recorded content",
        "Switch the octave range",
        "ADSR envelope simulation",
        "Responsive design",
        "Music study and practice",
        "Melody composition and inspiration capture",
        "Pitch and chord recognition training",
        "Teaching demonstrations and explanation",
        "📚 Deep Dive: Online Piano Keyboard (Equal Temperament Frequencies)",
        "Play the piano in the browser with the mouse or computer keyboard, with no real instrument needed",
        "Look up the note name and frequency of a given key for teaching demonstrations",
        "Play scales and chords to hear how they sound, which supports understanding of music theory",
        "Key Frequencies",
        "A0 = 27.5 Hz and each key to the right raises a semitone (×2^(1/12)); middle C (C4) = 261.63 Hz, A4 = 440 Hz and C5 = 523.25 Hz (C4×2).",
        "Playing the C Major Scale",
        "From C4, click C D E F G A B C5 in turn for the frequencies 261.63 → 293.66 → 329.63 → 349.23 → 392 → 440 → 493.88 → 523.25 Hz, and hear the bright direction of the major scale.",
        "Why Does a Piano Have 88 Keys?",
        "The standard range covers 88 keys from A0 (27.5 Hz) to C8 (4186 Hz), with 52 white keys and 36 black keys, which covers the range of most repertoire. Each key is one semitone.",
        "How Is the Computer Keyboard Mapped?",
        "Typically one row of keys maps to the white keys of an octave (A=S=C and so on), and the row above maps to the black keys. Each pressed key uses a Web Audio oscillator to sound the matching semitone frequency.",
    ]))
    write('freq-note-converter', build('freq-note-converter', [
        "📡 Frequency Note Converter",
        "Two-way conversion between Hz frequency and note names · Twelve-tone equal temperament · Web Audio auditioning",
        "\"Two-way conversion between Hz frequency and note names · Twelve-tone equal temperament · Web Audio auditioning\" performs a professional calculation from the input parameters and outputs the result.",
        "📖 Read the \"Frequency Note Converter User Guide\"",
        "A4 reference frequency",
        "440 Hz (standard)",
        "415 Hz (Baroque)",
        "Custom:",
        "Frequency → Note",
        "Note → Frequency",
        "Enter frequency",
        "Audition",
        "Note",
        "Twelve-tone equal temperament reference table",
        "Click any note to audition it (A4 =",
        "Natural notes",
        "Sharp and flat notes",
        "Tool introduction and frequently asked questions",
        "The frequency note converter is based on twelve-tone equal temperament and converts in both directions between Hz frequency and note names, which suits tuning, audio engineering and instrument calibration.",
        "Frequency to note conversion, with cent deviation display",
        "Note to frequency conversion (C0 to B8)",
        "Adjustable A4 reference frequency (432/440/442/443/415/custom)",
        "Full twelve-tone equal temperament table (C0 to B8)",
        "Front-end computation only, no data uploaded",
        "Confirm the standard frequency when tuning instruments",
        "Pitch reference in audio engineering",
        "Learn music theory and equal temperament",
        "Frequency lookups in electronic music production",
        "📚 Deep Dive: Two-Way Conversion Between Hz Frequency and Note (Equal Temperament)",
        "Look up a measured frequency as a note name with its cent deviation during tuning or audio engineering",
        "Enter a target note name in a synthesizer to get its frequency, or work in reverse",
        "Compare the cent difference of the 432 Hz and 440 Hz standards for A",
        "Frequency to Note",
        "In equal temperament f = 440 × 2^((n−69)/12), where n is the MIDI number and A4 = 69. 261.63 Hz gives n = 69 + 12·log2(261.63/440) = 60, so C4; 440 Hz gives A4.",
        "Cent Deviation",
        "For a measured 446 Hz against A4 (440): cents = 1200·log2(446/440) ≈ +24.6 cents, about a quarter of a semitone sharp; 432 Hz against A4 ≈ −31.8 cents.",
        "What Is a Cent?",
        "1 semitone = 100 cents, and it is a logarithmic unit of relative pitch: cents = 1200·log2(measured frequency / reference frequency). Within ±5 cents the human ear basically cannot hear a difference.",
        "Which Is More Accurate, 432 Hz or 440 Hz?",
        "440 Hz is the modern international concert pitch for A4; 432 Hz is an alternative tuning. The absolute audio values differ but the interval relationships are identical, so neither is right or wrong. Choose according to the needs of the work.",
    ]))

if __name__ == '__main__':
    main()
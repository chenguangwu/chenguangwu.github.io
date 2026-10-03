#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'audio')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'audio')
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
    out = {'slug': slug, 'industry': 'audio', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
# -*- coding: utf-8 -*-
def main():
    write('audio-speed', build('audio-speed', [
        '🏎️ Audio Playback Speed Adjuster',
        'Upload an audio file and freely adjust playback speed (0.25x ~ 4x), with pitch preservation, progress seeking, and variable-speed WAV export. Processed entirely in the browser; the file is never uploaded.',
        '/ Audio Playback Speed Adjuster',
        '📖 Read the "Audio Playback Speed Adjuster User Guide"',
        'Keep original pitch (play without shifting pitch)',
        '📚 Deep dive: audio playback speed adjustment',
        'In language learning, speed up a slow podcast or open course to 1.25x~1.5x to save time while keeping the original intonation for shadowing and imitation.',
        'Speed up a long lecture or meeting recording to review it faster and quickly locate the key passages that need close listening.',
        'Generate a 0.75x slow version or a 1.2x quick preview for short-video voice-over to match speaking rhythm and pauses.',
        'Variable-speed without pitch shift example',
        'For 44100Hz speech of 120 seconds, speeding up to 1.5x gives a playback duration of about 120÷1.5=80 seconds, the playback rate becomes 1.5x and the pitch stays the same; with plain resampling (no pitch preservation) the pitch would be raised by about 7 semitones and sound cartoonish, so front-end time stretching needs WSOLA or a phase vocoder to rearrange the time domain and correct phase.',
        'How is speed changed without shifting pitch?',
        'The core is rearranging the audio time structure without changing the fundamental frequency: first frame the signal with overlap-add (OLA), then use WSOLA to search neighboring frames for the most similar waveform alignment position, or use a phase vocoder to unwrap phase in the frequency domain. Playback rate changes while pitch is preserved.',
        'Does speeding up or slowing down damage audio quality?',
        'Within a moderate range (about 0.5x~2x) algorithm distortion is minimal; extreme rates introduce metallic artifacts or jitter, and speeding up compresses silence while slowing down stretches reverb tails. Preview boundary speeds before exporting to confirm naturalness.',
        'About "Audio Playback Speed Adjuster"',
        'Playback speed',
    ]))

    write('audio-volume', build('audio-volume', [
        '🔄 Audio Volume Adjuster',
        'Adjust audio volume in real time (0% ~ 200%) with the Web Audio API GainNode, supporting fades, VU meter visualization and WAV export. Processed entirely in the browser; the file is never uploaded.',
        '/ Audio Volume Adjuster',
        '📖 Read the "Audio Volume Adjuster User Guide"',
        '🔇 Mute',
        '🔄 Fade-in time',
        '🔄 Fade-out time',
        'Fade in / fade out take effect',
        'Export WAV',
        'on export; during real-time playback only the base volume gain applies. Adjustable range 0 ~ 10 seconds.',
        'About "Audio Volume Adjuster"',
        '📚 Deep dive: audio volume adjustment',
        'Unify the loudness of a batch of recordings so the edit does not swing between loud and quiet.',
        'Raise quiet vocals overall while monitoring peaks to prevent clipping distortion after export.',
        'Normalize material so the loudest point reaches a target level (e.g. −1dBFS), which simplifies distribution.',
        'Gain and normalization example',
        'Volume adjustment is essentially multiplying sample values by a gain coefficient g. Expressed in dB, g=10^(dB/20); for example +6dB corresponds to g≈1.995 (about double the amplitude). To normalize to a −1dBFS peak: first find the current maximum absolute sample A_max, the target peak is 10^(−1/20)≈0.891, so gain g=0.891/A_max. If g is so large that some sample exceeds ±1.0 it is clipped and distorts, so check the peak after boosting.',
        'Are volume and loudness the same thing?',
        'No. Volume is simple amplitude gain while loudness is the perceived loudness (commonly measured in LUFS). Simply doubling amplitude does not necessarily sound twice as loud. Before distribution, loudness normalization (e.g. −14LUFS) is recommended rather than looking at peaks alone.',
        'Why does the sound break when I raise the volume?',
        'Because sample values are amplified past ±1.0 and hard-clipped since they exceed the representable range, producing harsh distortion. Leave headroom, use soft clipping or reduce first then raise, and check that the peak stays under 0dBFS after boosting.',
        'Remove file',
        'Play / Pause',
    ]))

    write('audio-waveform', build('audio-waveform', [
        '🏋️ Audio Waveform Viewer',
        'Upload an audio file to visualize waveforms, spectrum and overview in real time. Built on the Web Audio API, processed entirely in the browser; the file is never uploaded.',
        '/ Audio Waveform Viewer',
        '📖 Read the "Audio Waveform Viewer User Guide"',
        '📈 Time-domain waveform',
        '🌈 Frequency-domain spectrum',
        '🗺️ Waveform overview',
        'Smoothing',
        '💡 Tip: while playing audio you can watch the real-time waveform and spectrum; switch to "Waveform overview" to see a static waveform of the entire clip, and click the progress bar to jump to a playback position.',
        '📚 Deep dive: audio waveform viewer',
        'When debugging recordings or mixes, observe the time-domain waveform to judge whether levels are overloaded and whether there are silent sections or clicks.',
        'Analyze the frequency-domain energy distribution of a clip to locate hum at a given frequency or formants.',
        'Visualize sound for teaching or demos, showing intuitively how amplitude and spectrum relate.',
        'FFT spectrum parameter example',
        'In Web Audio you read data with an AnalyserNode: with fftSize=2048 the frequency-domain bin count is 1024, and frequency resolution = sample rate÷fftSize = 44100÷2048 ≈ 21.5Hz/bin. Applying a Hann window reduces spectral leakage. The time-domain waveform directly reflects the amplitude of each sample (−1~+1), with the vertical axis often shown in dB or linear amplitude.',
        'Why does the spectrum look like a blurry smear?',
        'Insufficient resolution or a missing window causes leakage. Increasing fftSize raises frequency resolution (but lowers time resolution), and applying a Hann/Hamming window suppresses edge discontinuity so the spectrum becomes sharper.',
        'Why can I hear the sound but see nothing on the waveform?',
        'It may be an extremely low-amplitude ultrasonic segment, or phase cancellation averaged out in mono display, or the vertical axis is scaled to full scale while the signal is tiny. Zoom the vertical axis or switch to the spectrum view to cross-check.',
        'About "Audio Waveform Viewer"',
        'Play / Pause',
    ]))


if __name__ == '__main__':
    main()

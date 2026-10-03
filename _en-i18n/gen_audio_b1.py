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
    write('analysis-1', build('analysis-1', [
        '📡 Spectrum Parameters and Frequency Locator',
        'Visualization',
        'Spectrum Parameters and Frequency Locator',
        '/ Spectrum Parameters and Frequency Locator',
        '📖 Read the "Spectrum Parameters and Frequency Locator User Guide"',
        'Spectrum analysis applies a fast Fourier transform (FFT) to the input time-domain signal, mapping each sample to complex coefficients for different frequency components; its magnitude represents the energy at that frequency (often converted to dB via 20·log10), while phase represents time offset. Frequency resolution equals the sample rate divided by the FFT length, and a Hann window suppresses spectral leakage from frame-boundary discontinuity. Everything is computed locally in the browser; no data is uploaded to the server.',
        'Sample rate fs (Hz)',
        'FFT length N (points, a power of 2)',
        'Target frequency bin index (0 ～ N/2)',
        '📚 Deep dive: spectrum parameters and frequency location',
        'Audio/vibration spectrum analysis: enter sample rate, FFT length and target bin to compute frequency resolution, Nyquist frequency and the frequency of the bin, locating which frequency a peak belongs to.',
        'Window selection: understand that the Hann window widens the main lobe (about 2 bins), so adjacent frequencies are not masked by the main lobe and misread.',
        'Worked example (fs=8000Hz, N=1024, bin=10)',
        'Frequency resolution Δf=fs/N=8000/1024=7.8125 Hz; Nyquist frequency=fs/2=4000 Hz; the target bin 10 corresponds to 10×7.8125=78.125 Hz; Hann main lobe width=2×Δf=15.625 Hz. The tool computes directly from the formula to help read spectrum values and locate peaks.',
        'What if the frequency resolution is too coarse?',
        'Increasing the FFT length N or lowering the sample rate (while still meeting Nyquist) refines Δf; but a very large N raises computation cost, and note that the window main lobe widens accordingly.',
        'How do I avoid spectral aliasing?',
        'The sample rate must be more than twice the highest frequency of interest (Nyquist), otherwise high-frequency content folds back into low frequencies and causes aliasing; apply an anti-aliasing filter before sampling when necessary.',
        'About "Spectrum Parameters and Frequency Locator"',
        'Spectrum Parameters and Frequency Locator. A free online tool processed entirely in the browser, no data uploaded, your privacy and security protected.',
    ]))

    write('audio-cut', build('audio-cut', [
        '🎧 Audio Cutter',
        'Upload audio, drag a selection on the waveform, preview it and export as WAV. Processed entirely locally; the file is never uploaded.',
        '"Upload audio, drag a selection on the waveform, preview it and export as WAV. Processed entirely locally; the file is never uploaded." is computed from the input parameters and returns the result.',
        '/ Audio Cutter',
        '📖 Read the "Audio Cutter User Guide"',
        'Supports MP3 / WAV / OGG / M4A / FLAC / WebM and other browser-decodable formats',
        'Duration:',
        'Sample rate:',
        'Channels:',
        'Size:',
        'Start:',
        'End:',
        'Clip duration:',
        'Start time',
        'End time',
        'Preview clip',
        'Export WAV',
        'Select all',
        'Reset selection',
        '📚 Deep dive: audio cutting tool',
        'Cut a highlight out of a long recording or trim leading and trailing silence to produce a short audio clip ready to use.',
        'Extract a particular line of dialogue or a sound effect for video editing or courseware, locating start and end precisely on the waveform.',
        'Cut a song down to a ringtone or ringtone asset, avoiding manual re-encoding.',
        'Precise trimming and fades example',
        'For a 44100Hz stereo track, to take 30.000 s to 35.250 s the sample index range is 44100×30=1,323,000 to 44100×35.25=1,554,225 (per channel). Add a 5~10ms linear fade in and fade out at the cut boundaries to avoid clicks from waveform discontinuity. WAV export is a non-destructive cut and keeps the original sample fidelity.',
        'Why is there a click at the start after cutting?',
        'When the cut point lands on a non-zero waveform position, hard-cutting the signal creates a discontinuity that produces a click. Adding a very short fade in and fade out (a few milliseconds) at the boundaries removes it, and this tool applies that processing when you export after dragging on the waveform.',
        'Does cutting lose audio quality?',
        'Cutting purely by sample index is lossless (no re-encoding) as long as the export format matches the original fidelity (e.g. both WAV); lossy export formats would introduce compression loss.',
        'About "Audio Cutter"',
    ]))


if __name__ == '__main__':
    main()

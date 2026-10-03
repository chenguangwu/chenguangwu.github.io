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
    write('audio-echo', build('audio-echo', [
        '🎧 Audio Echo and Reverb Effect',
        'Adds echo / reverb effects to audio using the Web Audio API ConvolverNode and DelayNode, with real-time preview and WAV export. Processed entirely in the browser; the file is never uploaded.',
        '/ Audio Echo and Reverb Effect',
        '📖 Read the "Audio Echo and Reverb Effect User Guide"',
        '🎧 Echo',
        '🏛️ Reverb',
        '📚 Deep dive: audio echo and reverb effect',
        'Add a sense of space to voice-over or vocals, simulating the reflective ambience of a room, hall or corridor.',
        'When producing music, fine-tune the dry/wet ratio so the dry signal stays clear while the wet signal provides envelopment without muddiness.',
        'Quickly preview how different delay parameters affect the listening experience to pick a suitable echo length.',
        'Delay and feedback example',
        'An echo is essentially a delay line: the signal is delayed by d milliseconds and mixed with the original. With delay d=250ms and feedback coefficient g=0.4, the first echo appears at 250ms, the second at 500ms at 0.4 times the previous amplitude, decaying in turn. Reverb instead uses multiple random delays or a convolution impulse response to emulate early reflections and the tail. A dry/wet ratio of 0.3 means the wet signal accounts for 30% of the final output.',
        'What is the difference between echo and reverb?',
        'An echo is a discernible, discrete repeat of the delayed sound (you can count the first hit, the second hit); reverb is a continuous tail formed by many dense, indistinguishable reflections that simulate the room sound field. The former gives rhythm, the latter gives space.',
        'Why does the result sound muffled or dirty after adding the effect?',
        'Usually the wet ratio is too high, or the delay setting clashes with the rhythm. Lowering the dry/wet ratio, shortening the delay and avoiding conflict with the tempo usually helps; if noise floor is amplified, denoise first and then apply the effect.',
        'About "Audio Echo and Reverb Effect"',
        'Click the waveform to jump to a playback position',
        'Playback progress, click to jump',
        'Play / Pause',
        'Stop',
    ]))

    write('audio-recorder', build('audio-recorder', [
        '🎨 Audio Recorder and Processor',
        'Record audio, adjust volume and speed, and visualize waveforms - all done locally in the browser',
        '/ Audio Recorder and Processor',
        '📖 Read the "Online Recording Tool User Guide"',
        'Uses MediaRecorder to capture microphone audio and saves it locally as a file, supports volume and playbackRate adjustment plus real-time waveform drawing; everything runs in the browser and no data is uploaded.',
        'Start recording',
        'Stop recording',
        '📊 Waveform display',
        'Click or drag an audio file here to load it',
        'Supports MP3 / WAV / OGG / WebM / M4A and other formats',
        '🎛️ Audio processing',
        'Export audio',
        'Reset parameters',
        '📁 Recording list',
        'No recordings yet; click the "Start recording" button above to record',
        'In-browser recording',
        'Volume adjustment (0-200%)',
        'Playback speed adjustment (0.5-2.0x)',
        'Real-time waveform visualization',
        'Multi-segment recording management',
        'Export the processed audio',
        'Supports drag-and-drop loading of audio files',
        'Record voice memos',
        'Adjust audio volume and speaking rate',
        'Visualize audio waveforms',
        'Quickly record and download audio clips',
        '📚 Deep dive: online recording tool',
        'Record meetings, interviews or lectures straight from the browser microphone with live waveform and level, then export the material as soon as you stop.',
        'Record voice-over or podcast dry vocals, first testing a few seconds to confirm gain is right and there is no clipping or noise, then record properly.',
        'Capture ambience or instrument material, exporting WAV to keep original fidelity for later editing.',
        'Sample rate and format example',
        'Recording in the browser with MediaRecorder, the common constraints are 44100Hz or 48000Hz sample rate, mono or stereo. With a WebM/Opus container a bitrate around 128kbps is enough for speech; for lossless material export WAV (16bit/44.1kHz mono is about 5MB per minute). Before recording, use the live level meter to confirm the peak stays below 0dBFS to avoid clipping.',
        'Why does the recording sometimes have noise or clicks?',
        'Usually input gain is too high and causes clipping, or the environment feeds back and produces howling. Lower the microphone gain, stay 15~30cm from the sound source and record in a quiet room; local browser processing never uploads audio, so privacy stays under your control.',
        'WebM/Opus or WAV?',
        'WebM/Opus is compact and suits network transfer and quick sharing; WAV is lossless and uncompressed, suited to editing and further processing. If the audio will go into a DAW for detailed work, export WAV.',
        'About "Audio Recorder and Processor"',
        'Audio Recorder and Processor is an online tool in the design and creative domain. Design and creative tools, visual operation, one-click CSS code generation.',
        'How to use the Audio Recorder and Processor',
        'What does the Audio Recorder and Processor do?',
        'The Audio Recorder and Processor records audio locally in the browser, adjusts volume and speed, and visualizes waveforms. It runs purely in the browser with no data uploaded, fitting voice and material processing.',
        'How do I use the Audio Recorder and Processor?',
        'What scenarios suit the Audio Recorder and Processor?',
    ]))


if __name__ == '__main__':
    main()

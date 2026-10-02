#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'niche')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'niche')
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
    out = {'slug': slug, 'industry': 'niche', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('convert-fps', build('convert-fps', [
        "🔄 Video Frame Rate Conversion (fps)",
        "Video frame count ↔ duration (seconds), requires a frame rate in fps",
        "📖 Read the Video Frame Rate Conversion (fps) user guide",
        "Frame rate conversion: frame count = duration (seconds) × frame rate; duration (seconds) = frame count ÷ frame rate; duration per frame = 1 ÷ frame rate seconds, that is 1000 ÷ frame rate milliseconds; frames per minute = frame rate × 60.",
        "Frames → seconds",
        "Seconds → frames",
        "📚 Deep Dive: Video Frame Rate Conversion (fps)",
        "Convert between frame count and seconds: given the frame count find the duration, or given the duration find the total frame count.",
        "Check the shot length of animation or time-lapse footage and confirm the finished seconds after rendering at the target frame rate.",
        "Verify that the editing timeline matches the frame count of the material so the exported duration does not fall apart.",
        "Conversion formulas",
        "Frames → seconds: seconds = frame count ÷ frame rate; seconds → frames: frame count = seconds × frame rate. The frame rate must be greater than 0, otherwise the conversion is impossible; the frame rate is the shared bridge quantity in both directions.",
        "150 frames at 30fps = 150/30 = 5 seconds; 3 seconds at 24fps = 3×24 = 72 frames. Time-lapse footage of 240 frames played at 24fps gives a 10-second finished piece, while playing it at 12fps gives 20 seconds.",
        "The conversion result does not match what the player shows?",
        "It is usually because the frame rate value differs (such as mixing 29.97 with 30); confirm the true frame rate of the source, since a 0.1% difference accumulates into a noticeable duration offset over long footage.",
        "Does the frame count need to be an integer?",
        "Physical frame counts can only be integers, so the tool rounds; but duration calculations are more precise with the unrounded value, which matters especially when syncing audio.",
        "About Video Frame Rate Conversion (fps)",
        "Video frame rate conversion (fps). Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
    ]))
    write('convert-sample', build('convert-sample', [
        "📡 Audio Sample Rate Conversion (kHz)",
        "Audio sample count ↔ duration (seconds), requires a sample rate",
        "📖 Read the Audio Sample Rate Conversion (kHz) user guide",
        "Sample rate conversion: sample count = duration (seconds) × sample rate × 1000; duration (seconds) = sample count ÷ (sample rate × 1000), where the sample rate is in kHz; interval per sample = 1 ÷ (sample rate × 1000) seconds, that is 1000000 ÷ (sample rate × 1000) microseconds.",
        "Sample rate (kHz)",
        "Samples → seconds",
        "Seconds → samples",
        "📚 Deep Dive: Audio Sample Rate Conversion (kHz)",
        "Convert between sample count and seconds, used in audio programming, ring buffers and latency calculations.",
        "Derive the number of buffer points for a given duration from the sample rate, to configure capture or playback buffer sizes.",
        "Check whether the sample position and the time ruler in a digital audio workstation correspond.",
        "Count and seconds",
        "Samples → seconds: seconds = sample count ÷ (sample rate kHz × 1000); seconds → samples: sample count = seconds × sample rate kHz × 1000. The sample rate must be greater than 0, and the result keeps two decimal places.",
        "At 44.1 kHz, 1 second = 1 × 44.1 × 1000 = 44,100 samples; 88,200 samples = 88200/44100 = 2 seconds. At 48 kHz, 0.5 seconds = 24,000 samples; with a buffer of 1024 samples, that is a latency of 1024/48000 ≈ 0.0213 seconds.",
        "What is the difference between samples and frames?",
        "In audio these are usually called samples, where one sample is one captured value; in stereo each sample frame holds two points, left and right, so buffer sizing must multiply by the channel count.",
        "How do I choose the buffer size?",
        "A larger buffer means higher latency but fewer dropouts; latency (seconds) = buffer samples ÷ sample rate, and monitoring is generally kept within about 10 ms.",
        "About Audio Sample Rate Conversion (kHz)",
        "Audio sample rate conversion (kHz). Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
    ]))
    write('recommender-temp-pottery', build('recommender-temp-pottery', [
        "🌡️ Pottery Firing Temperature Curve Recommendation",
        "An online tool for recommending pottery firing temperature curves",
        "📖 Read the Pottery Firing Temperature Curve Recommendation user guide",
        "Temperature curves are recommended by clay body and vessel form: in the ramp-up stage, below 600 °C rise slowly at 80 to 120 °C per hour (driving off crystal water and organic matter to prevent cracking), 600 to 1000 °C at 120 to 150 °C per hour, and 60 to 80 °C per hour to wrap up near the firing temperature; in the soak stage hold at the firing temperature for 15 to 30 minutes to level the glaze surface; in the cooling stage cool evenly at 60 to 100 °C per hour, and below 600 °C the kiln may cool naturally.",
        "📚 Deep Dive: Pottery Firing Temperature Curve Recommendation",
        "Look up the recommended temperature range and soak time for bisque and glaze firing by clay body, as a parameter reference for kiln loading and firing.",
        "Compare the firing windows of different clay bodies to judge whether a glaze matches the firing temperature of the clay body.",
        "Use the soak time to plan constant-temperature control in the high temperature range, ensuring the body or glaze reacts fully.",
        "Recommended parameter table",
        "Bisque / glaze temperatures and soaking: earthenware (low fire) 800-950°C / 980-1050°C / 20-30 min; stoneware clay (mid fire) 900-1000°C / 1180-1240°C / 30-45 min; kaolin clay (high fire porcelain) 900-980°C / 1260-1320°C / 40-60 min; zisha clay 1000-1100°C / 1120-1180°C / 20-30 min; bone china 900-1000°C / 1220-1280°C / 30-40 min. The glaze firing temperature should be slightly below the limit of the body, and soaking lets the glaze melt fully.",
        "Firing kaolin porcelain: bisque at 950°C (the midpoint of the 900-980 range) soaking 20-30 min, which sets the body and gives it enough strength for glazing; glaze firing ramped to 1300°C (within 1260-1320) soaking 50 min so the glaze fully vitrifies. If the glaze matures at 1200 °C it does not suit this body and stoneware clay should be used instead.",
        "Why is the bisque temperature lower than the glaze firing?",
        "The purpose of bisque firing is to set the shape, remove water and create some porosity so it absorbs glaze; too high a temperature makes the body too dense to hold glaze well, while glaze firing needs high heat to melt and vitrify the glaze.",
        "How does soak time affect the finished piece?",
        "Too short and the glaze does not fully level, leaving pinholes and orange peel; too long and the glaze may run and stick to the kiln shelf or the body may over-fire and deform. Generally high fire porcelain needs 40-60 min and low fire clay 20-30 min is enough.",
        "About Pottery Firing Temperature Curve Recommendation",
        "Pottery firing temperature curve recommendation. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
    ]))


if __name__ == '__main__':
    main()

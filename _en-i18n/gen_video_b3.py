#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'video')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'video')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    return mp


def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'video', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # ---------------- video-speed (67) ----------------
    write('video-speed', build('video-speed', [
        "⏱️ Video Speed Duration Calculator",
        "Compute the duration after speeded-up playback, timecode conversion, editing duration estimation",
        "Video Duration Calculator",
        "/ Video Duration Calculation",
        "📖 Read the \"Video Speed Duration Calculator User Guide\"",
        "Duration at playback speed",
        "= original duration ÷ speed",
        "(e.g. 60 minutes at 1.5x ≈ 40 minutes). Timecode HH:MM:SS:FF (FF is frames) converts to and from seconds; the duration of an edited clip = out point − in point.",
        "Common frame rates are 24/25/30 fps, which affect the timecode and frame precision.",
        "📋 Reference",
        "Milliseconds",
        "Timecode (HH:MM:SS:FF)",
        "Target duration (seconds)",
        "⏱️ Common Speed Duration Table (30-minute video)",
        "Speed",
        "Percent saved",
        "Frame-by-frame study",
        "Slow-motion detail",
        "Listening practice",
        "Normal playback",
        "Slightly faster viewing",
        "First choice for lectures",
        "Familiar content",
        "Quick skim",
        "Review recap",
        "Finding key points",
        "Super-speed scanning",
        "Preview positioning",
        "Fast seeking",
        "🎬 Video Frame Rate Standards",
        "Duration per frame",
        "Film standard",
        "Movies, TV series",
        "PAL format",
        "Europe / China TV",
        "NTSC drop-frame",
        "US / Japan TV",
        "Non-drop-frame",
        "Web video, live streaming",
        "PAL interlaced",
        "High frame rate",
        "Games, slow motion",
        "Ultra high frame rate",
        "Slow-motion photography",
        "Super slow motion",
        "Motion analysis",
        "💡 Speed-watching tips",
        ": suitable for knowledge videos, basically loses no information",
        ": suitable for tutorials and lectures, requires focused attention",
        ": suitable for entertainment content, quickly skimming the plot",
        ": only suitable for quickly locating segments, not for normal viewing",
        ": suitable for language learning and observing action details",
        "📜 Calculation record",
        "📚 Deep dive: Video Speed Duration Calculator",
        "Study plans",
        ": use 1.5x or 2x speed for long videos and online courses, and back-derive from the original duration how long it takes to finish, arranging daily progress.",
        "Recording and editing conversion: given the total duration and frame rate, find the total frame count; or given the frame count, find the duration, for checking export parameters.",
        "Finish within a fixed time: to watch a 45-minute video within 30 minutes, solve backwards for the required speed (45÷30=1.5x).",
        "Worked example (original duration 00:45:00, i.e. 2700 seconds)",
        "New duration = original duration ÷ speed. (1) 1.5x: 2700÷1.5=1800 seconds=00:30:00, saving (2700−1800)÷2700×100%≈33%. (2) 2x: 2700÷2=1350 seconds=00:22:30, saving 50%. (3) Reverse: to finish 45 minutes of content in a target of 30 minutes (1800 seconds), the required speed=2700÷1800=1.5x. Total frames (@30fps) = 2700×30=81000 frames; SMPTE timecode FF = seconds × fps taken modulo, and 00:45:00 corresponds to 00:45:00:00.",
        "Does pitch and speech rate change at higher speed?",
        "This tool only computes duration and does not change actual playback. Whether playback alters pitch depends on the player: pure rate playback changes pitch and speeds up, while enabling \"playback without pitch change\" (such as YouTube speed) keeps the pitch and changes only the speed. The calculation logic is always new duration = original duration ÷ speed.",
        "What is FF in SMPTE timecode?",
        "FF is the frame count (Frame), = seconds × frame rate (fps) taken modulo 60 (for 30 fps, 30 frames advance 1 second). It is used to align material in editing software; this tool also gives total frames = duration × fps, which makes it easy to cross-check against Premiere / DaVinci projects.",
        "About \"Video Duration Calculation\"",
        "Video duration calculation. A video processing tool that runs entirely in the browser, protecting your privacy.",
        "Reverse-compute the speed",
    ]))

    # ---------------- video-trimmer (28) ----------------
    write('video-trimmer', build('video-trimmer', [
        "🎬 Video Trim Time Planner",
        "Mark trim segments after uploading a video, export the trim schedule for editing",
        "\"Mark trim segments after uploading a video, export the trim schedule for editing\" is professionally computed from the input parameters and outputs the result.",
        "Video Trimmer",
        "/ Video Trimmer",
        "📁 Choose video file",
        "⏱ Set as current",
        "➕ Add segment",
        "📤 Export schedule",
        "💡 Note: this tool is for planning the time segments of a video trim; the exported schedule can be used with editing software such as ffmpeg and Premiere. The browser cannot directly cut video files.",
        "ffmpeg trim command reference",
        "# Trim the segment from 00:01:30 to 00:02:45",
        "# Trim 60 seconds starting at 00:00:30",
        "# Precise trim (re-encode, avoiding keyframe issues)",
        "📚 Deep dive: Video Trim Time Planning",
        "Trimming screen recordings: cut the 30-second opening buffer and the 1-minute ending, plan to keep the middle section, and avoid leftover redundancy after export.",
        "Splitting into multiple posts: cut a 1-hour livestream into 3 highlight segments, compute the duration of each, and keep each post under the platform limit (e.g. Douyin 60 minutes, WeChat 5 minutes).",
        "Keeping the best segments: concatenate multiple non-contiguous segments, compute the cumulative kept duration and the cut ratio, and evaluate information density.",
        "Worked example (60-minute video, cut into 3 segments)",
        "Segment A 00:05:00–00:10:00 = 5 minutes; segment B 00:20:00–00:28:00 = 8 minutes; segment C 00:40:00–00:46:00 = 6 minutes. Cumulative kept = 5+8+6 = 19 minutes; cut = total 60 − kept 19 = 41 minutes; cut ratio = 41÷60×100% ≈ 68.3%. The tool computes each segment as \"end − start\" and aggregates, giving three outputs: kept / cut / ratio.",
        "What precision should trim times use?",
        "Use the timeline timecode; accuracy to the second is enough for most trim planning, and fine editing can be adjusted later in Premiere / CapCut. This tool plans in seconds, helping you fix each segment's start and end first and avoid discovering the wrong duration only after export.",
        "How is the cut ratio computed and what is it for?",
        "Cut ratio = (original total duration − kept duration) ÷ original total duration × 100%. It directly reflects \"how much was cut\" and is used to evaluate the information density of the result or whether it meets platform size / duration limits (e.g. a WeChat post ≤5 minutes, requiring you to work backwards from this to decide which segments to keep).",
        "About \"Video Trimmer\"",
        "The video trimmer is an online tool in the video processing domain. A video processing tool that runs entirely in the browser, protecting your privacy.",
        "Hour",
        "Minute",
    ]))


if __name__ == '__main__':
    main()

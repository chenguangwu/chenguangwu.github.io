#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'film')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'film')
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
    out = {'slug': slug, 'industry': 'film', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # ---------- aspect-ratio (42) ----------
    slug = 'aspect-ratio'
    en = [
        '🎞️ Film Aspect Ratio Converter',
        'Size conversion, cropping and letterbox calculation across different frame formats',
        'Key formula (by input variable): Math.round(w ÷ r)',
        'Ratio Conversion',
        'Crop / Letterbox',
        '16:9 (1.78:1) — Video / TV',
        '2.35:1 — Cinemascope',
        '2.39:1 — Modern Cinemascope',
        '1.85:1 — US Film',
        '4:3 (1.33:1) — Traditional TV',
        '3:2 (1.5:1) — Photography',
        '9:16 (0.56:1) — Vertical Short Video',
        '1:1 — Square',
        'Width (pixels)',
        'Height (pixels)',
        'Original Width (pixels)',
        'Original Height (pixels)',
        'Target Aspect Ratio',
        '2.35:1 (Cinemascope)',
        '2.39:1 (Modern Cinemascope)',
        '1.85:1 (US Film)',
        'Aspect Ratio Note:',
        '16:9 is the video standard; 2.35:1 / 2.39:1 are used for cinema widescreen; 9:16 is used for vertical short videos. Aspect ratio = width / height.',
        'Common Film & Video Resolutions',
        '📚 In-Depth Analysis: Film Frame Aspect Ratio Conversion',
        'Given the width, compute the height for the target format, to confirm output size after cropping or letterboxing.',
        'When converting 16:9 footage to 2.39:1 cinema widescreen, calculate how much height needs to be cropped.',
        'Unify output specs before multi-platform release: short video 9:16, landscape 16:9, film 2.39:1 cross-referenced.',
        '1920×1080 to 2.39:1',
        'At 16:9 (1.778), width 1920 → height = 1920 ÷ 1.778 = 1080. After switching to 2.39:1, height = 1920 ÷ 2.39 ≈ 803 px, meaning 277 px must be cropped top and bottom (or add letterbox to keep the full frame). Conversely, if height is locked at 1080, width = 1080 × 2.39 ≈ 2581 px, requiring side padding.',
        'What are the ratios of common frame formats?',
        '16:9 ≈ 1.778, 4:3 ≈ 1.333, 3:2 = 1.5, 1:1 = 1.0, 9:16 ≈ 0.5625, 1.85:1 Academy widescreen, 2.35:1 and 2.39:1 cinema widescreen. The tool auto-recognizes these standard ratios and names them.',
        'How to choose between cropping and letterboxing?',
        'Cropping loses frame content but fills the screen; letterboxing keeps the full content but adds black bars top and bottom. For interviews and subtitle content, letterboxing is recommended; for mood shots, cropping is acceptable. The conversion result only gives dimensions; the specific method is decided in editing software.',
        'About "Film Aspect Ratio Converter"',
        'One of the most common delivery issues for film, TV and short-video footage is inconsistent frame format. This tool provides aspect-ratio conversion, proportional scaling, cropping and letterboxing results, so adaptation strategies can be reviewed under one consistent standard.',
        'Supports quick conversion of common formats such as 16:9, 2.39:1, 9:16 and 1:1.',
        'Provides two adaptation plans "Plan A/B": letterbox-first keeps the full frame, center-crop-first keeps the main subject.',
        'Crop parameters can be copied directly for sync with editing / post-production teams.',
        'Film set: align horizontal and vertical footage under one standard.',
        'Content operations: generate specs and crop parameters uniformly before publishing to different platforms.',
        'Project management: provide a traceable adaptation-parameter list before delivering to clients.',
    ]
    write(slug, build(slug, en))

    # ---------- color-grading (27) ----------
    slug = 'color-grading'
    en = [
        '⚖️ Color Grading LUT Reference',
        'A quick reference table of LUT types, color spaces and grading parameters for film and short-video workflows, with type filtering and keyword search.',
        'Color Grading LUT Reference',
        '/ Color Grading LUT Reference',
        'This table summarizes the typical division of 1D/3D LUTs: a 1D LUT handles grayscale mapping (e.g., monitor calibration, basic color transformation), a 3D LUT handles 3D color mapping (e.g., Log to Rec.709 or creative stylization). Filtering and searching help quickly find reference items matching the shot source and delivery spec, aiding color decisions.',
        'Filter by Type',
        'Technical LUT',
        'Creative LUT',
        'Monitor Calibration',
        'LUT Note:',
        'A LUT (Look-Up Table) is used for color-space conversion and creative grading. A 1D LUT handles the grayscale curve (1024 levels); a 3D LUT handles color mapping (33³ or 65³ cube). Technical LUTs are for color-space conversion; creative LUTs are for stylized grading.',
        'Common LUT Type Reference',
        'Color Space Reference',
        'Grading Parameter Reference',
        '📚 In-Depth Analysis: Color Grading LUT Type Quick Reference',
        'Before editing, filter common LUTs by type (e.g., cinematic, Japanese style, film emulation) to quickly narrow the selection.',
        'Filter by applicable color space (Rec.709 / Log / HDR) to confirm which class your footage needs.',
        'When explaining the style direction to a client, use the typical parameters on the quick-reference table as a communication reference.',
        'How to use this quick-reference table',
        'First filter by type (e.g., "film emulation"), then enter keywords in the search box (e.g., "Kodak" "Fujifilm" "teal-orange") to narrow the range; the table lists the LUT name, applicable color space and typical grading parameters (contrast, saturation, color-temperature shift, etc.). For example, Log footage usually needs a conversion LUT back to Rec.709 first, then a style LUT on top—reversing the order causes color shift.',
        'Can the parameters in the table be copied directly?',
        'Only as a starting point. Different cameras have different Log curves, color temperatures and exposure baselines; actual grading should rely on the waveform monitor and preview, treating the parameters as reference ranges rather than fixed values.',
        'Why does the picture look gray after applying a LUT?',
        'Mostly because a style LUT was applied directly on Log footage. Log footage needs a color-space conversion (conversion LUT or CST) back to the display space first, then the style LUT on top.',
        'About "Color Grading LUT Reference"',
        'Film color-grading LUT reference table, providing common LUT types, color-space conversions and grading parameter references. A design/creative tool with visual operation and one-click CSS code generation.',
        'Search LUT name…',
    ]
    write(slug, build(slug, en))

    # ---------- convert-time-1 (25) ----------
    slug = 'convert-time-1'
    en = [
        '🔄 Editing Timecode (Hours/Minutes/Seconds/Frames) Converter',
        'Supports mutual conversion between HH:MM:SS:FF timecode, total frames and total seconds, for editing alignment and subtitle timing checks.',
        'Hours (0-23)',
        'Frame',
        'SMPTE Timecode Principle',
        'Standard film-editing timecode: total frames = ((hours×3600 + minutes×60 + seconds) × fps) + frames. The same moment yields different total-frame counts at different frame rates.',
        '📚 In-Depth Analysis: Timecode vs Frame/Second Conversion',
        'When marking edit points, convert hours:minutes:seconds:frames into total frames, to align across different frame-rate projects.',
        'Convert the subtitle timeline from seconds to timecode, or conversely extract seconds from timecode.',
        'When collaborating with audio or VFX, communicate with a unified timecode to avoid ambiguity from "which second".',
        'Total frames = (hours×3600 + minutes×60 + seconds) × frame rate + frames = (0 + 60 + 30) × 25 + 12 = 2262 frames; corresponding seconds = 2262 ÷ 25 = 90.48 s. If the same timecode is interpreted at 24 fps, frame 12 becomes 12/24 = 0.50 s, shifting the whole clip by 90.50 − 90.48 = 0.02 s—cross-frame-rate projects must align by total frames or seconds, not by moving the timecode directly.',
        'What frame rate should I enter?',
        'Enter the actual project frame rate: film 24 fps, domestic TV 25 fps (PAL), North America 29.97/30 fps (NTSC), high frame rate 50/60 fps. A wrong entry shifts the converted seconds.',
        'Can the frame number exceed the frame rate?',
        'No. The frame number ranges from 0 to (frame rate − 1), e.g., 0–24 at 25 fps. Exceeding it means a wrong input; carry over to seconds and then write the frame number.',
        'About "Editing Timecode (Hours/Minutes/Seconds/Frames) Converter"',
        'Used for quick conversion between HH:MM:SS:FF timecode, total frames and seconds. Suits multi-frame-rate project alignment, subtitle labor checks and footage re-inspection workflows.',
        'Supports three-way conversion among HH:MM:SS:FF, total frames and total seconds',
        'Supports common fps and fractional fps input',
        'Results can be used directly for reconciliation and review records',
        'All page calculations run locally in the browser, protecting footage parameter privacy',
        'Timecode verification for multi-camera edit clips',
        'Subtitle timeline aligned with audio track points',
        'Duration review in invoice reconciliation or delivery checklists',
        'Project recalculation and cross-department handoff acceptance',
    ]
    write(slug, build(slug, en))

    # ---------- editing-timecode (30) ----------
    slug = 'editing-timecode'
    en = [
        '🔄 SMPTE Timecode Converter',
        'Film-editing SMPTE timecode conversion and total-frame/second mutual conversion, supporting subtitle alignment and footage delivery review.',
        'Editing Timecode Converter',
        '/ Editing Timecode Converter',
        'Timecode to Frames',
        'Frames to Timecode',
        '24 fps (Film)',
        'Timecode (HH:MM:SS:FF)',
        'SMPTE Timecode:',
        'Format is HH:MM:SS:FF (hours:minutes:seconds:frames). 24 fps for film, 25 fps for PAL TV, 29.97/30 fps for NTSC. Drop-frame timecode is used for precise sync.',
        'Common Frame Rate Reference',
        '📚 In-Depth Analysis: SMPTE Timecode Conversion',
        'Convert HH:MM:SS:FF timecode into total frames, for passing precise in/out points across software.',
        'When locating footage, derive the timecode from total frames and jump directly to that position in the editor.',
        'Check the same time point at different frame rates to confirm whether position drifts after transcoding or speed change.',
        'Timecode 01:00:00:00 at 24 fps = (1×3600 + 0 + 0) × 24 + 0 = 86400 frames; the same timecode at 25 fps = 90000 frames, a difference of 3600 frames (i.e., 150 s). Therefore, cross-frame-rate projects should always hand off by total frames or seconds; timecode is only equivalent at the same frame rate.',
        'How to handle 29.97 fps drop-frame timecode?',
        'Drop-frame (DF) timecode skips several frame numbers every minute to align with real time. This tool calculates by non-drop-frame (NDF); for 29.97 DF projects, use a professional tool to convert first, then verify the total frames.',
        'Which is more accurate, timecode or seconds?',
        'Timecode is unambiguous only at the same frame rate; seconds are absolute time and safer across frame rates. When handing off footage, it is recommended to give both values.',
        'About "Editing Timecode Converter"',
        'Suitable for film-editing scenarios of mutual conversion among SMPTE timecode, total frames and seconds, supporting marking alignment and delivery review at multiple fps.',
        'Supports two-way conversion between timecode, total frames and total seconds',
        'Supports common integer and fractional frame rates (24/25/29.97/23.976)',
        'Can output duration and millisecond results needed for alignment records',
        'All in-page calculations run locally, protecting footage reconciliation data security',
        'Multi-camera footage sync and footage reconciliation',
        'Subtitle timeline aligned with audio/video points',
        'Caliber review before cross-department handoff',
        'Problem-clip review and duration-deviation analysis',
    ]
    write(slug, build(slug, en))


if __name__ == '__main__':
    main()

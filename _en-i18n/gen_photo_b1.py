#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""photo 第1批：bracketing-plan / calc-exposure-aperture / card-capacity / convert-focal / depth-of-field"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'photo')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'photo')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        for i, it in enumerate(items):
            print('   ', i, repr((it.get('zh') or it.get('zh_src', ''))[:50]))
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
    out = {'slug': slug, 'industry': 'photo', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))


# ---------------- bracketing-plan (19) ----------------
write('bracketing-plan', build('bracketing-plan', [
    "\U0001F4E3 Bracket Exposure Plan",
    "Plan the number of bracketed shots and EV range.",
    '\U0001F4D6 View the "Bracket Exposure Plan User Guide"',
    "Range (stops)",
    "Step (stops)",
    "Count = range/step + 1; covers [base-range/2, base+range/2]",
    "For HDR blending or safety exposure.",
    "\U0001F4DA Deep Dive: Bracketed Shot Count Planning",
    "HDR/panorama bracketing computes shot count by EV range and step.",
    "Set lowest/highest EV to cover the dynamic range.",
    "Balance shot count with post-blending burden.",
    "+/-3EV step 1",
    "Range +/-3EV, step 1EV: count = ceil(6/1)x2+1 = 13 shots, lowest EV = mid-3, highest = mid+3, covering 6 stops of light.",
    "Step 2 saves shots",
    "Range +/-2EV, step 2EV: count = ceil(4/2)x2+1 = 5 shots, half the count but coarser light transition, good for even lighting.",
    "Why is bracketed count 2N+1?",
    "Centered on the median, N steps each end totals 2N shots, plus the median 1 gives 2N+1; smaller step means more shots and smoother blending.",
    "How to choose the step?",
    "High contrast uses 1EV fine transition, low contrast uses 2-3EV to save shots; HDR usually +/-2~3EV with 1EV step is enough.",
]))

# ---------------- calc-exposure-aperture (48) ----------------
write('calc-exposure-aperture', build('calc-exposure-aperture', [
    "\U0001F4D0 Exposure Triangle Calculator",
    "Compute exposure value (EV) from aperture, shutter and ISO, and perform equivalent-exposure reciprocity conversion.",
    "Exposure Triangle Calculator",
    "/ Exposure Triangle Calculator",
    '\U0001F4D6 View the "calc-exposure-aperture User Guide"',
    "EV100 = log2(N^2/t) - log2(S/100); absolute exposure EV = log2(N^2/t); equivalent shutter t = 100*N^2/(S*2^EV100)",
    "N is the aperture f-number, t is shutter time (s), S is ISO. EV100 normalized to ISO 100 eases cross-sensitivity comparison; each 1 EV difference means double light. Scene brightness graded by EV100 (snowy noon >=16, Sunny 16 rule ~14, cloudy ~12, night <=2).",
    "Aperture f/N",
    "Shutter speed (s)",
    "\U0001F9EE Calculate EV",
    "\U0001F4A1 EV100 = log2(N^2/t) - log2(ISO/100); keeping EV unchanged, opening aperture 1 stop needs shutter 1 stop faster",
    "\u2696\uFE0F Reciprocity: solve target EV",
    "Enter target EV and any two items (leave the third blank to auto-solve)",
    "Target EV100",
    "Aperture (leave blank to solve)",
    "Shutter (leave blank to solve)",
    "ISO (leave blank to solve)",
    "Solve missing parameter",
    "Shutter accepts fraction (1/125), decimal (0.008) or integer (2) seconds",
    "EV100 is the exposure value at ISO 100 baseline, reflecting scene brightness (e.g. daylight ~EV15)",
    "Reciprocity may fail at very long/short exposures; real shooting relies on measurement",
    "\U0001F4DA Deep Dive: Exposure Triangle Calculator",
    "Balance exposure by adjusting aperture, shutter and ISO three factors.",
    "Compute EV and give equivalent exposure combos.",
    "Judge scene brightness level by EV.",
    "Overexposed by 1 stop",
    "Stop aperture from f/8 to f/11, or speed shutter 1 stop, reduces exposure by 1 EV; compensate by raising ISO or slowing shutter.",
    "Sunny 16 rule",
    "Sunny day ~EV100 15, use f/16 + 1/100s + ISO100 for roughly correct exposure.",
    "What is",
    "Aperture, shutter and ISO together decide exposure; any change alters brightness and image style (depth of field, motion, noise).",
    "Does larger EV mean brighter image?",
    "EV describes scene brightness and exposure combo; smaller value means darker light, more exposure needed.",
    "Focal Length and Angle of View Conversion",
    'About "Exposure Triangle Calculator"',
    "Enter aperture, shutter, ISO to compute EV100, auto-generate the equivalent-exposure reciprocity table, and solve missing parameter given a target EV.",
    "Supports fraction shutter input (1/125) and decimal seconds",
    "Auto-generate shutter table for different apertures at same EV",
    "Solve any of aperture/shutter/ISO for target EV",
    "Manual exposure parameter conversion",
    "Depth-of-field vs shutter trade-off decision",
    "Photography teaching and exposure practice",
    "Studio lighting parameter estimation",
    "e.g. 2.8, 4, 8",
    "e.g. 1/125, 0.008, 2",
    "Blank = solve aperture",
    "Blank = solve shutter",
    "Blank = solve ISO",
]))

# ---------------- card-capacity (20) ----------------
write('card-capacity', build('card-capacity', [
    "\U0001F4F7 Memory Card Usable Shot Count",
    "Estimate usable shot count from capacity and per-shot size.",
    '\U0001F4D6 View the "Memory Card Usable Shot Count User Guide"',
    "Card capacity GB",
    "Per-shot MB",
    "JPEG per-shot MB",
    "Count = capacity(GB)x1000 / per-shot size(MB)",
    "RAW usually 20-50 MB, JPEG smaller.",
    "\U0001F4DA Deep Dive: Memory Card Capacity and Shot Count Estimate",
    "Compute RAW/JPEG shot count by card capacity and per-shot size.",
    "Estimate timelapse/video recording duration.",
    "Travel spare-card planning.",
    "64GB card",
    "64GB card, RAW ~25MB/shot: count = 64x1000/25 ~ 2560 shots; JPEG ~8MB -> 8000; at 10fps recording ~64x1000/(25x10x60) ~ 4.3 min.",
    "Capacity conversion",
    "30MB/shot, 1000 shots need 30GB; 14-bit RAW is several times larger than compressed JPEG; estimate peak usage before burst to avoid filling.",
    "How much do RAW and JPEG differ?",
    "Uncompressed RAW ~12-30MB, JPEG high quality 3-10MB; RAW holds all data good for editing but takes space.",
    "Why does video eat more capacity?",
    "Video is a continuous stream; 4K 100Mbps ~750MB per minute, far faster than a single shot; timelapse by frame rate.",
]))

# ---------------- convert-focal (30, src_diff idx23) ----------------
write('convert-focal', build('convert-focal', [
    "\U0001F504 Lens Focal Length and Angle of View Conversion",
    "Lens focal length and angle of view conversion online tool",
    "Lens Focal Length and Angle of View Conversion",
    "/ Lens Focal Length and Angle of View Conversion",
    '\U0001F4D6 View the "convert-focal User Guide"',
    "Lens focal length",
    "mm focal length",
    "km focal length",
    "Angle of view conversion",
    "mm AoV conversion",
    "km AoV conversion",
    "\U0001F4DA Deep Dive: Lens Focal Length and Angle of View Conversion",
    "Convert focal length to angle of view by sensor size.",
    "Compare equivalent angle of view across formats.",
    "Estimate framing range before choosing a lens.",
    "APS-C equivalent",
    "APS-C crop factor ~1.5, 50mm lens ~75mm full-frame equivalent, narrower angle, better for portraits.",
    "Wide angle of view",
    "Full-frame 24mm horizontal AoV ~74\u00b0, good for landscape and indoor; telephoto narrows AoV markedly.",
    "What determines the angle of view?",
    "Determined by focal length and sensor size together: shorter focal length, larger sensor, wider AoV.",
    "Is it the real focal length?",
    "No. Equivalent focal length only reflects angle of view; the physical focal length is unchanged, and depth of field and bokeh differ accordingly.",
    "Exposure Triangle Calculator",
    'About "Lens Focal Length and Angle of View Conversion"',
    "Lens focal length and angle of view conversion. Free online tool, pure front-end processing, data not uploaded, privacy-safe.",
    "Unit conversion of focal length and angle of view",
    "Cross-format comparison for multiple lenses",
    "Focal-range planning and framing estimate",
    "Unified lens-library parameter organizing",
]))

# ---------------- depth-of-field (23) ----------------
write('depth-of-field', build('depth-of-field', [
    "\U0001F9EE Depth of Field (DOF) Calculator",
    "Estimate near and far depth of field at the focus distance.",
    '\U0001F4D6 View the "Depth of Field (DOF) Calculator User Guide"',
    "H = f^2/(N*c) + f; near/far = H*S/(H\u00b1(S-f))",
    "Smaller aperture, shorter focal length, farther distance give greater depth of field.",
    "\U0001F4DA Deep Dive: Depth of Field (Near/Far) Calculation",
    "Compute near and far DOF from focal length, aperture and object distance.",
    "Control bokeh to emphasize the subject.",
    "Large DOF focus for landscape.",
    "Portrait bokeh",
    "50mm, f/1.8, focus 2m: DOF ~0.04m (near 1.98m, far 2.02m), shallow DOF blurs background; stop to f/8 extends DOF to ~0.5m.",
    "Landscape deep focus",
    "24mm, f/11, focus 3m: DOF reaches several meters to far limit near infinity, front and back sharp, good for landscape.",
    "What does depth of field depend on?",
    "Smaller aperture, shorter focal length, farther object distance give greater DOF; aperture controls bokeh most directly, each f-stop adds ~doubles DOF.",
    "Is near/far DOF symmetric?",
    "No, at close focus far DOF far exceeds near DOF; at hyperfocal focus far DOF extends to infinity.",
    "How to use the DOF Calculator",
    "Quick reference for photo parameters, exposure and quality.",
    "What does the DOF Calculator do?",
    "The DOF calculator computes near and far DOF range from aperture, focal length and focus distance, suited to control bokeh and focus zone, aiding portrait and landscape photography.",
    "How do I use the DOF Calculator?",
    "Which scenarios suit the DOF Calculator?",
]))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""photo 第4批：mired / nd-filter / photo-10 / photo-11 / photo-2"""
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


# ---------------- mired (17) ----------------
write('mired', build('mired', [
    "\U0001F504 Mired (Color Temperature) Converter",
    "Convert between color temperature in Kelvin and Mired micro-reciprocal units.",
    '\U0001F4D6 View the "Mired (Color Temperature) Converter User Guide"',
    "Color temperature K",
    "Photographic filters commonly use Mired to describe color-temperature shift.",
    "\U0001F4DA Deep Dive: Mired (Micro-reciprocal) Conversion",
    "Compute Mired from Kelvin color temperature.",
    "Correct color temperature with filter Mired offset.",
    "White balance under mixed light sources.",
    "Mired calculation",
    "3200K tungsten: Mired = 1e6/3200 = 312.5; plus +100 warm filter gives Mired 212.5 -> color temp = 1e6/212.5 ~ 4706K, clearly warmer.",
    "Shift direction",
    "Lower Mired = higher color temp (cool/blue); higher Mired = lower temp (warm/orange); correct daylight with minus-Mired blue filter, tungsten with plus-Mired orange filter.",
    "Why use Mired instead of K?",
    "Filter color-temperature effect is subtractive and nonlinear; Mired (1e6/K) approximates linearity, making filter offsets easy to stack.",
    "How to set the offset?",
    "The offset to add equals the difference between target and current Mired; e.g. correcting 5500K (182) to 3200K (312) needs a +130 Mired orange filter.",
]))

# ---------------- nd-filter (20) ----------------
write('nd-filter', build('nd-filter', [
    "\U0001F504 ND Filter Shutter Conversion",
    "Compute the extended shutter speed after adding an ND filter.",
    '\U0001F4D6 View the "ND Filter Shutter Conversion User Guide"',
    "Base shutter s",
    "ND stops",
    "Target shutter s",
    "New shutter = base x 2^stops",
    "ND1000 is about 10 stops and can render flowing water like silk.",
    "\U0001F4DA Deep Dive: ND Filter Extends Shutter",
    "Compute new shutter and extension factor from ND stops.",
    "Long exposure for silky water / cloud blur.",
    "Pick the right ND stop.",
    "ND1000 long exposure",
    "Original shutter 1/100s, ND1000 (10 stops): new shutter = 1/100 x 2^10 = 10.24s, extended 1024x, water turns to mist.",
    "Stop selection",
    "For a 2s exposure from 1/500s you need ~1000x ~ 2^10 (ND1000); to merely blur crowds, ND8 (3 stops) suffices.",
    "How do ND stops compute extension?",
    "Each stop cuts one exposure step and doubles shutter; NDx stops n=log2(x), extension 2^n, ND1000 = 10 stops x 1024.",
    "Does ND affect aperture?",
    "It only reduces light, not aperture, depth of field or focal length; to keep DOF, stop down aperture together with ND for long exposure.",
]))

# ---------------- photo-10 (25) ----------------
write('photo-10', build('photo-10', [
    "\U0001F4E3 Bracketed Exposure Count",
    "Compute the number of frames and step for HDR bracketing.",
    '\U0001F4D6 View the "Bracketed Exposure Count User Guide"',
    "Total EV range",
    "Step EV",
    "Count = 2 x ceil(total range / step) + 1",
    "Ensure adjacent frames overlap by at least 1 EV.",
    "\U0001F4DA Deep Dive: Actual Bracketing EV Coverage",
    "Compute required frames from total EV range and step.",
    "Check whether actual coverage is enough for HDR merge.",
    "Control the sequence length.",
    "Frame count",
    "Total range 6EV, step 1EV: count = ceil(6/1)*2+1 = 13 frames; actual coverage = 13 frames x 1EV span, ends cover +/-6EV around the median.",
    "Coverage check",
    "Shooting only 5 frames at 2EV step gives 8EV coverage, still short of a 10EV scene; add frames or reduce step.",
    "Why ceil?",
    "Steps round up so the range is fully covered, then add the median frame for the total, avoiding edge clipping.",
    "Is coverage EV the same as the range?",
    "Slightly more, since ends include boundaries; check actual coverage against the scene brightest and darkest.",
    "How to Use the Bracketed Exposure Count",
    "Quick reference for photo parameters, exposure and quality.",
    "What does the Bracketed Exposure Count do?",
    "Enter the desired total dynamic range and per-step exposure (e.g. 1 EV, 2 EV); the tool computes the minimum bracketed frames needed for HDR merge and reminds to keep at least 1 EV overlap between adjacent frames, so highlights and shadow detail are fully captured.",
    "How do I use the Bracketed Exposure Count?",
    "Which scenarios suit the Bracketed Exposure Count?",
]))

# ---------------- photo-11 (21) ----------------
write('photo-11', build('photo-11', [
    "\U0001F3CE\uFE0F Panning Shutter Speed",
    "Estimate the recommended shutter speed for panning shots.",
    '\U0001F4D6 View the "Panning Shutter Speed User Guide"',
    "Object speed km/h",
    "Suggested shutter ~ 1 / (focal length x angular speed / 10)",
    "Angular speed ~ lateral speed / distance",
    "Adjust up or down per the desired blur effect.",
    "\U0001F4DA Deep Dive: Recommended Shutter for Moving Subjects",
    "Derive angular view speed from object speed, distance and focal length.",
    "Compute the shutter denominator to freeze motion.",
    "Panning parameters.",
    "Freeze a race car",
    "Car 100km/h = 27.8m/s, distance 20m, 200mm: ang",
    "= 27.8/20 x 180/pi ~ 79.5 deg/s, suggested shutter ~ 1/(79.5 x 10) ~ 1/795s (1/800s freezes near subjects).",
    "Angular speed",
    "Slow-shutter trails",
    "For motion blur in the same scene, use 1/100s: movement ~0.8 deg/frame, car body streaks; weigh whether the subject stays recognizable.",
    "Why angular speed rather than linear speed?",
    "The sensor records image angle; longer focal length gives larger angular speed and needs faster shutter; same for nearby subjects.",
    "Can panning lower the shutter?",
    "Yes, reverse-panning offsets relative angular speed, letting you use slower shutter to freeze the subject and blur the background for more dynamism.",
]))

# ---------------- photo-2 (19) ----------------
write('photo-2', build('photo-2', [
    "\U0001F4F7 Equivalent Focal Length",
    "Compute equivalent focal length across formats.",
    '\U0001F4D6 View the "Equivalent Focal Length User Guide"',
    "Lens focal length mm",
    "Crop factor 1=full-frame 1.5=APS-C 2=M43",
    "Target format factor",
    "Full-frame baseline factor is 1.",
    "\U0001F4DA Deep Dive: Equivalent Focal Length Angle-of-View Ratio",
    "Compare framing differences of two lenses by equivalent focal length.",
    "Estimate composition change before swapping lenses.",
    "Crop-factor effect.",
    "Framing difference",
    "35mm vs 50mm: angle ratio = 50/35 ~ 1.43, 50mm frames ~1.4x tighter than 35mm, subject appears larger; conversely wide angle fits more.",
    "Crop effect",
    "Full-frame 50mm on APS-C is equivalent 75mm: angle narrows like telephoto, you must step back to fit the same frame.",
    "How to compute the angle ratio?",
    "Approximate as the focal-length ratio (angle is not strictly linear but close); long/short focal ratio is the framing zoom factor.",
    "Does equivalent affect perspective?",
    "No, perspective is set by subject distance; equivalent only changes the angle range, compression depends on where you stand.",
]))

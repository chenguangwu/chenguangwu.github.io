#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""photo 第2批：dpi / dynamic-range / equivalent-focal / ev / exposure-value"""
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


# ---------------- dpi (22) ----------------
write('dpi', build('dpi', [
    "\U0001F4F7 Print Resolution DPI",
    "Compute the pixels and DPI needed for photo printing.",
    '\U0001F4D6 View the "Print Resolution DPI User Guide"',
    "Width pixels",
    "Height pixels",
    "Print width cm",
    "Target DPI",
    "DPI = pixels / inch length",
    "Inch = cm / 2.54",
    "300 DPI is common for high-quality printing.",
    "\U0001F4DA Deep Dive: DPI and Print Size Conversion",
    "Get physical print size from pixels and DPI.",
    "Back-calc pixels needed for a given print size.",
    "Judge if an enlargement is sharp enough.",
    "Print size",
    "6000px wide @300dpi: print width = 6000/300 = 20in ~ 50.8cm; at only 150dpi it is 40in, with visible grain up close.",
    "Required pixels",
    "To print A4 width 21cm @300dpi: required pixels = 21/2.54x300 ~ 2480px; below this prints look soft.",
    "Is 300dpi necessary?",
    "Up close 300dpi is fine; posters viewed far need only 150dpi; greater viewing distance accepts lower DPI.",
    "Can interpolation make up for missing pixels?",
    "Interpolation only softens enlargement, adds no real detail; insufficient original pixels will blur large prints, so shoot high resolution upfront.",
]))

# ---------------- dynamic-range (20) ----------------
write('dynamic-range', build('dynamic-range', [
    "\U0001F4F7 Dynamic Range Stop Rating",
    "Convert brightness ratio to dynamic-range stop rating.",
    '\U0001F4D6 View the "Dynamic Range Stop Rating User Guide"',
    "Brightest",
    "Darkest",
    "Sensor stops",
    "DR = log2(brightest/darkest)",
    "Unit is exposure stops.",
    "\U0001F4DA Deep Dive: Dynamic Range and Clipping Steps",
    "Assess by sensor stops whether it holds the light/dark ratio.",
    "Judge whether on-site highlights/shadows clip.",
    "Decide if GND filter/bracketing is needed.",
    "Light/dark ratio assessment",
    "Scene brightness ratio 1000:1 ~ log2(1000) ~ 10 stops; if sensor DR is 14 stops it fits, highlights/shadows don't clip; only 8 stops needs filter or bracketing.",
    "Clipping judgment",
    "DR 12 stops, scene contrast 14 stops: exceeds by 2 stops, brightest or darkest must clip, need to compress light ratio or HDR.",
    "How to understand DR stops?",
    "Each stop = double light/dark; 12 stops is a 4096:1 recordable range; beyond it one end is blown white or black.",
    "How to widen the effective range?",
    "Use a graduated filter to compress sky, lift shadows in post, or bracket-expose HDR, stitching several narrow ranges into a wide one.",
]))

# ---------------- equivalent-focal (18) ----------------
write('equivalent-focal', build('equivalent-focal', [
    "\U0001F504 Equivalent Focal Length Conversion",
    "Convert actual focal length to full-frame equivalent.",
    '\U0001F4D6 View the "Equivalent Focal Length Conversion User Guide"',
    "Actual focal length mm",
    "Equivalent focal length = actual focal length x crop factor",
    "APS-C factor ~1.5, M4/3 ~2.0.",
    "\U0001F4DA Deep Dive: Equivalent Focal Length Conversion",
    "Convert APS-C/M43 lens focal length to full-frame angle of view.",
    "Compare framing range across formats.",
    "Choose lens to match composition.",
    "APS-C equivalent",
    "Crop factor 1.5, lens 35mm: full-frame equivalent = 35x1.5 = 52.5mm, angle of view about full-frame 50mm standard lens.",
    "M4/3 equivalent",
    "Factor 2.0, 25mm lens: equivalent = 50mm; for full-frame 85mm portrait need 42.5mm lens (x2=85).",
    "Does actual focal length change?",
    "No, only the angle of view is converted; depth of field is still set by real aperture and physical focal length, equivalent is for comparing framing range.",
    "Where does the factor come from?",
    "Full-frame diagonal 43.3mm over each format's diagonal: APS-C ~1.5, M4/3 ~2.0.",
]))

# ---------------- ev (28) ----------------
write('ev', build('ev', [
    "\U0001F4E3 Exposure Value (EV)",
    "Compute exposure value from aperture, shutter, ISO.",
    '\U0001F4D6 View the "Exposure Value (EV) User Guide"',
    "Shutter time s",
    "N is aperture value, t is shutter time",
    "Lower EV means brighter image.",
    "\U0001F4DA Deep Dive: Exposure Value (EV) Calculation",
    "From aperture, shutter, ISO compute EV to judge exposure.",
    "Compare equivalent exposure of different parameter combos.",
    "Meter reading verification.",
    "EV calculation",
    "f/8, 1/125s, ISO100: EV100 = log2(N^2/t) = log2(64x125) = log2(8000) ~ 12.97; by EV100 scene tier it falls in 'cloudy/bright shadow', sunny noon ~ EV 14-15.",
    "Equivalent interchange",
    "Same EV means equal exposure: f/8\u00b71/125 equals f/11\u00b71/60 (one stop each), swap params to keep brightness while changing bokeh.",
    "What is EV?",
    "Exposure value, each +1 EV doubles exposure; EV100 uses ISO100 baseline, formula EV = log2(N^2/t x 100/ISO).",
    "What do high/low EV mean?",
    "High EV = bright scene (e.g. sunny day EV14+), low = dark (indoor EV4-7); camera auto-exposure tracks the target EV.",
    "How do EV tiers map to scenes?",
    "EV100 (ISO 100) common tiers: >=16 snow/beach noon, >=14 bright daylight (Sunny 16 rule), >=12 cloudy/bright shadow, >=10 bright indoor, >=8 normal indoor/dusk, >=6 sunset, <=2 night. This page and the",
    "Exposure Triangle Calculator",
    " page share the same tier set.",
    "How to use Exposure Value (EV)",
    "Quick reference for photo parameters, exposure and quality.",
    "What does Exposure Value (EV) do?",
    "The EV calculator computes exposure value from aperture, shutter and ISO; lower EV means brighter image, suited to quantitative control of manual exposure, flash and exposure compensation.",
    "How do I use Exposure Value (EV)?",
    "Which scenarios suit Exposure Value (EV)?",
]))

# ---------------- exposure-value (17) ----------------
write('exposure-value', build('exposure-value', [
    "\U0001F4E3 Exposure Value (EV) Calculation",
    "Compute exposure value from aperture, shutter, ISO.",
    '\U0001F4D6 View the "Exposure Value (EV) Calculation User Guide"',
    "Shutter seconds",
    "Same scene EV constant; adjusting the three needs balance.",
    "\U0001F4DA Deep Dive: Exposure Value EV@ISO100 Conversion",
    "Unify ISO100 baseline to compare exposure at different sensitivities.",
    "Reciprocity parameter conversion.",
    "Understand exposure compensation.",
    "Baseline conversion",
    "f/5.6, 1/250, ISO200: EV@ISO100 = log2(N^2/t x 100/ISO) = log2(31.36x250x0.5) = log2(3920) ~ 11.94; equivalent at ISO100 f/5.6\u00b71/500.",
    "Compensation understanding",
    "EV11.9 plus +1 compensation: equivalent to one stop faster shutter or one stop wider aperture, brightening the image by double.",
    "EV vs EV@ISO100 difference?",
    "EV includes current ISO, EV@ISO100 normalizes to ISO100 for cross-comparison; difference = log2(ISO/100).",
    "Is reciprocity reliable?",
    "Holds for normal exposure, but extreme long/short exposures have reciprocity failure (needs compensation); flash and continuous light also differ.",
]))

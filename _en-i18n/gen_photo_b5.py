#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""photo 第5批：photo-3 / photo-4 / photo-5 / photo-6 / photo-7"""
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


# ---------------- photo-3 (17) ----------------
write('photo-3', build('photo-3', [
    "\U0001F4CB Guide Number Calculator",
    "Compute flash distance from guide number and aperture.",
    '\U0001F4D6 View the "Guide Number Calculator User Guide"',
    "Guide number m",
    "Double ISO, distance x sqrt(2)",
    "GN is usually rated at ISO100.",
    "\U0001F4DA Deep Dive: ISO and Effective Flash Distance",
    "Find effective lighting distance from GN and ISO.",
    "Back-calc the required aperture.",
    "Fill-light planning in low light.",
    "GN=40, ISO100, f/4: ISO100 distance = GN/f = 40/4 = 10m; ISO400 factor 2 -> actual 20m, lights farther subjects.",
    "Required aperture",
    "At 8m, GN40, ISO100: required f = 40/8 = f/5; opening to f/4 overexposes, stopping to f/8 underexposes.",
    "How do distance and ISO relate?",
    "Effective distance grows with sqrt(ISO/100); high ISO throws flash farther or allows smaller aperture.",
    "Why adjust aperture too?",
    "With fixed GN, distance and aperture are locked together; change one and you must change the other, ISO is the third variable in the triad.",
]))

# ---------------- photo-4 (20) ----------------
write('photo-4', build('photo-4', [
    "\u23F1\uFE0F Star Trail Duration",
    "Estimate the longest exposure before visible star trailing.",
    '\U0001F4D6 View the "Star Trail Duration User Guide"',
    "Sensor long-edge pixels",
    "Acceptable movement pixels",
    "500 Rule: exposure seconds <= 500 / (focal length x crop factor)",
    "NPF is more accurate, accounting for pixel size",
    "Used in astrophotography to avoid star trailing.",
    "\U0001F4DA Deep Dive: Star-trail Safe Shutter (500/NPF Rule)",
    "Compute longest trailing-free shutter from focal length.",
    "Compare the 500 Rule and NPF approximation.",
    "Wide-angle long-exposure star trails.",
    "500 Rule",
    "24mm full-frame: 500/24 ~ 20.8s, beyond that stars trail; for star trails, deliberately use multi-minute exposure.",
    "NPF is stricter",
    "NPF ~ (35 x pixel size um)/focal length; 24mm, 4um pixel: ~ 35x4/24 ~ 5.8s, stricter than the 500 Rule with rounder stars.",
    "Which is more accurate, 500 or NPF?",
    "The 500 Rule is loose, fine for web; NPF accounts for pixel size and is stricter, NPF prevents pixel-level trailing on high-MP bodies.",
    "Can wide angle go longer?",
    "Yes, shorter focal length allows longer; but Earth rotation is fixed, very long still trails, star trails need minutes.",
]))

# ---------------- photo-5 (17) ----------------
write('photo-5', build('photo-5', [
    "\U0001F4F7 Hyperfocal Focus",
    "Compute and apply the sharp range when focusing at the hyperfocal distance.",
    '\U0001F4D6 View the "Hyperfocal Focus User Guide"',
    "Focused at H, DOF runs from H/2 to infinity",
    "A common technique in landscape photography.",
    "\U0001F4DA Deep Dive: Hyperfocal Near/Far Limits",
    "Find near and far limits when focusing at hyperfocal.",
    "Confirm what is sharp from near to infinity.",
    "Maximize the sharp band in landscapes.",
    "Sharp band",
    "24mm, f/11, c=0.03: H ~ 1.76m, focus at H gives near limit H/2 ~ 0.88m, far limit infinity, whole frame sharp from foreground to sky.",
    "f/16 goes farther",
    "Same 24mm at f/16: H ~ 1.22m, near limit ~ 0.61m, far still infinity, near sharper but diffraction slightly up.",
    "Why is the near limit H/2?",
    "When focused at hyperfocal, the nearest sharp point is exactly H/2 and the farthest is infinity; this is the geometric result of the hyperfocal definition.",
    "Any downside to stopping down too far?",
    "f/16+ diffraction softens overall; landscapes commonly use f/8-f/11 to balance DOF and sharpness.",
]))

# ---------------- photo-6 (18) ----------------
write('photo-6', build('photo-6', [
    "\U0001F9EE Angle of View Calculator",
    "Compute the horizontal and vertical angle of view of a lens.",
    '\U0001F4D6 View the "Angle of View Calculator User Guide"',
    "Sensor height mm",
    "Angle = 2 x arctan(sensor edge length / (2 x focal length))",
    "Full-frame defaults to 36x24 mm.",
    "\U0001F4DA Deep Dive: Angle of View (Horizontal/Vertical/Diagonal)",
    "Compute the three angles from focal length and the sensor three sizes.",
    "Composition and panorama stitching planning.",
    "Compare across formats.",
    "Three angles",
    "Full-frame 36x24, diagonal 43.3mm, 50mm: horizontal ~ 39.6 deg, vertical ~ 27 deg, diagonal ~ 46.8 deg; for stitching use the horizontal angle for overlap.",
    "Format difference",
    "APS-C 24x16 at same 50mm: horizontal ~ 27 deg, narrower than full-frame, frames like 75mm equivalent, step back to fit.",
    "What is the diagonal angle good for?",
    "Judge whether the frame max angle fits the subject diagonal; reference for stitching and wide-angle edge distortion.",
    "Can the three angles be derived from each other?",
    "They cannot be simply derived; each needs its own sensor dimension via FOV = 2 atan(size / 2f).",
]))

# ---------------- photo-7 (18) ----------------
write('photo-7', build('photo-7', [
    "\U0001F4F7 Magnification Ratio",
    "Compute magnification in macro photography.",
    '\U0001F4D6 View the "Magnification Ratio User Guide"',
    "Subject actual width mm",
    "Image width mm",
    "Magnification = image size / actual size",
    "1:1 means image and subject are the same size.",
    "\U0001F4DA Deep Dive: Macro Sensor Coverage",
    "Find the subject coverage on the sensor from magnification.",
    "Decide if a small subject fits fully.",
    "Estimate the largest shootable subject.",
    "M=0.5x, sensor height 24mm: image height = 12mm, 50% of sensor; largest subject = 24/0.5 = 48mm fills the frame.",
    "Full-frame condition",
    "To fill-frame a 30mm insect you need M = 24/30 = 0.8x; if the lens only does 0.5x, move closer or add close-up.",
    "How do coverage and magnification relate?",
    "Image height = subject height x M, coverage = image height / sensor size; larger M means more coverage and smaller shootable subject.",
    "Does sensor size matter?",
    "At same M, a larger sensor fits a bigger subject full-frame, so medium format macros see wider.",
]))

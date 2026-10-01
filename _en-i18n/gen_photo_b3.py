#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""photo 第3批：field-of-view / flash-gn / golden-hour / hyperfocal / macro-magnification"""
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


# ---------------- field-of-view (17) ----------------
write('field-of-view', build('field-of-view', [
    "\U0001F9EE Field of View (FOV) Calculator",
    "Compute horizontal/vertical angle of view from focal length and sensor size.",
    '\U0001F4D6 View the "Field of View (FOV) Calculator User Guide"',
    "Sensor height mm",
    "Wider sensor, shorter focal length, larger angle of view.",
    "\U0001F4DA Deep Dive: Angle of View (Horizontal/Vertical) Calculation",
    "Get horizontal/vertical angle of view from focal length and sensor size.",
    "Judge by composition if the subject fits.",
    "Compare angles of view across lenses.",
    "50mm full-frame",
    "Full-frame 36x24mm, 50mm: horizontal FOV = 2xatan(36/(2x50)) ~ 39.6\u00b0, vertical = 2xatan(24/100) ~ 27\u00b0, diagonal ~ 46.8\u00b0.",
    "Wide-angle comparison",
    "24mm horizontal FOV ~ 73.7\u00b0, nearly twice wider than 50mm, good for landscape/architecture; 200mm only ~10\u00b0 telephoto compression.",
    "What is the relation between angle of view and focal length?",
    "Shorter focal length wider angle; FOV = 2xatan(sensor size/(2f)); larger format gives wider angle at same focal length.",
    "Why differ horizontal vs vertical?",
    "Sensor width exceeds height, so horizontal angle exceeds vertical; non-square formats must be computed separately.",
]))

# ---------------- flash-gn (18) ----------------
write('flash-gn', build('flash-gn', [
    "\U0001F4CB Flash Guide Number (GN)",
    "Find usable aperture from guide number and distance.",
    '\U0001F4D6 View the "Flash Guide Number (GN) User Guide"',
    "Guide number",
    "Aperture = GN / distance (ISO100)",
    "Doubling ISO increases effective distance ~1.4x.",
    "\U0001F4DA Deep Dive: Flash Guide Number (GN) and Usable Aperture",
    "Find usable aperture from GN and distance (ISO100).",
    "Back-calc aperture from distance change.",
    "Correct GN for high ISO.",
    "Aperture calculation",
    "GN=40, distance 10m (ISO100): usable aperture f = GN/d = 40/10 = f/4; at 5m then f/8, closer needs smaller aperture to avoid overexposure.",
    "ISO correction",
    "ISO from 100 to 400: correction factor = sqrt(400/100) = 2, equivalent GN = 80, same distance usable f/8.",
    "What is GN?",
    ", GN = aperture f x distance m (ISO100); larger means stronger flash, core to choosing lights and computing exposure.",
    "Does ISO affect GN?",
    "Yes, GN grows with sqrt(ISO/100); high ISO raises equivalent GN, same distance allows smaller aperture.",
]))

# ---------------- golden-hour (26) ----------------
write('golden-hour', build('golden-hour', [
    "\U0001F52E Daylight Duration Estimator",
    "Estimate sunrise/sunset daylight duration from latitude and declination.",
    '\U0001F4D6 View the "Daylight Duration Estimator User Guide"',
    "Latitude \u00b0",
    "Declination \u00b0",
    "Golden hour minutes",
    "Day length = 2 x acos(-tan\u03c6 x tan\u03b4)/15 hours",
    "Declination summer solstice ~23.44, winter solstice ~-23.44, equinoxes ~0. Golden hour is about 1 hour after sunrise / before sunset.",
    "\U0001F4DA Deep Dive: Daylight Duration and Golden Hour",
    "Compute the day's daylight duration from latitude and declination.",
    "Estimate the golden-hour window (low-angle light after sunrise / before sunset).",
    "Outdoor shoot time planning.",
    "Summer-solstice daylight",
    "Latitude 30\u00b0, summer declination +23.45\u00b0: cos(h) = -tan30 x tan23.45 ~ -0.250, daylight = 2xacos(-0.25)/15 ~ 13.9h, golden hour ~ 1 hour after sunrise / before sunset of soft light.",
    "Winter comparison",
    "Same latitude winter declination -23.45\u00b0: daylight ~ 10.1h, golden window shorter, arrive earlier.",
    "Why is golden-hour light good?",
    "Sun at low angle, soft warm light, long shadows, strong dimension; appears only ~1 hour after sunrise / before sunset.",
    "How to get declination?",
    "Varies with season: summer +23.45\u00b0, winter -23.45\u00b0, equinoxes 0\u00b0; higher latitude gives bigger summer-winter daylight gap.",
    "How to use the Daylight Duration Estimator",
    "Quick reference for photo parameters, exposure and quality.",
    "What does the Daylight Duration Estimator do?",
    "The daylight-duration estimator computes sunrise/sunset daylight from latitude and declination and flags the golden hour (~1 hour after sunrise / before sunset), suited to outdoor photography and itinerary planning.",
    "How do I use the Daylight Duration Estimator?",
    "Which scenarios suit the Daylight Duration Estimator?",
]))

# ---------------- hyperfocal (15) ----------------
write('hyperfocal', build('hyperfocal', [
    "\U0001F9EE Hyperfocal Distance (H) Calculator",
    "Compute the depth-of-field range when focused at the hyperfocal distance.",
    '\U0001F4D6 View the "Hyperfocal Distance (H) Calculator User Guide"',
    "Focused at hyperfocal, DOF extends from H/2 to infinity.",
    "\U0001F4DA Deep Dive: Hyperfocal Distance Calculation",
    "Compute hyperfocal from focal length, aperture and circle of confusion.",
    "Landscape focus to reach infinity at far limit.",
    "Maximize the sharp range.",
    "50mm, f/8, full-frame CoC c=0.03mm: H = f^2/(N*c)+f = 2500/(8x0.03)+50 ~ 10433mm ~ 10.4m; focus at 10.4m, near limit 5.2m far limit infinity.",
    "Stop down aperture to widen sharpness",
    "Same 50mm stop to f/16: H ~ 50^2/(16x0.03)+50 ~ 5262mm ~ 5.3m, near limit ~2.6m fully sharp, good for deep landscape.",
    "How to use hyperfocal?",
    "Focus at the hyperfocal distance, near limit H/2 and far limit infinity, everything from H/2 to infinity is sharp; the max-DOF method for landscape.",
    "How big should the circle of confusion be?",
    "Full-frame commonly 0.03mm, APS-C 0.02mm; smaller means larger hyperfocal and stricter sharpness, set by output size.",
]))

# ---------------- macro-magnification (19) ----------------
write('macro-magnification', build('macro-magnification', [
    "\U0001F4F7 Macro Magnification Ratio",
    "Compute macro magnification from focal length and object distance.",
    '\U0001F4D6 View the "Macro Magnification Ratio User Guide"',
    "Object distance mm",
    "Format height mm",
    "Magnification m = f/(S-f)",
    "m=1 is 1:1 macro, specimen and image same size.",
    "\U0001F4DA Deep Dive: Macro Magnification Calculation",
    "Compute magnification from image height and object height.",
    "Judge if it reaches 1:1 macro.",
    "Estimate the smallest object size shootable.",
    "Magnification",
    "Object height 24mm imaged 24mm on sensor (APS-C height): magnification M = 1.0x (true 1:1 macro); if image height 12mm then M=0.5x.",
    "Smallest object",
    "M=1.0, sensor height 24mm: largest object = 24mm fills the frame; for smaller, need higher magnification or crop in post.",
    "What does 1:1 mean?",
    "Image and object same size, magnification 1.0x; macro-labeled lenses often reach 1:1 or higher, normal lenses mostly 0.2-0.5x.",
    "What limits magnification?",
    "Limited by the lens's minimum focus distance and optical design; adding extension rings/bellows breaks through but hurts quality and infinity focus.",
]))

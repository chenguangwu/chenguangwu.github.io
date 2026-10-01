#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""photo 第6批：photo-8 / photo-9 / photo / print-size / raw-size"""
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


# ---------------- photo-8 (19) ----------------
write('photo-8', build('photo-8', [
    "\U0001F9E0 File Size Estimate",
    "Estimate RAW/JPEG image file size.",
    '\U0001F4D6 View the "File Size Estimate User Guide"',
    "Megapixels",
    "Compression ratio 1=lossless 3=RAW 10=JPEG",
    "Uncompressed size = pixels x bit depth / 8",
    "Compressed ~ uncompressed / compression ratio",
    "Actual size varies with image content.",
    "\U0001F4DA Deep Dive: Compressed/Uncompressed Image Size",
    "Compute single-frame uncompressed size from pixels and bit depth.",
    "Estimate actual file by compression ratio.",
    "Storage and transfer planning.",
    "24MP, 14bit: uncompressed = 24e6 x 14 / 8 / 1e6 ~ 42MB; ratio 4 -> ~10.5MB/frame, 100 bursts ~ 1GB.",
    "Bit-depth effect",
    "Same 24MP at 12bit: uncompressed = 24 x 12 / 8 = 36MB, down 6MB; higher bit depth keeps more editing headroom but uses more card.",
    "How to compute uncompressed size?",
    "Pixels x bit depth / 8 = bytes, then to MB; RAW also carries metadata and overhead, slightly larger.",
    "Is the compression ratio reliable?",
    "Lossless ~ 1.2-1.5x, lossy JPEG up to 5-10x; estimate storage with typical ratios and leave margin.",
]))

# ---------------- photo-9 (21) ----------------
write('photo-9', build('photo-9', [
    "\U0001F4F7 Diffraction Limit Aperture",
    "Estimate the diffraction-limit aperture for a sensor pixel density.",
    '\U0001F4D6 View the "Diffraction Limit Aperture User Guide"',
    "Pixel pitch um",
    "Wavelength nm",
    "Allowed circle-of-confusion multiple",
    "Diffraction blur ~ 2.44 x lambda x N",
    "When blur exceeds pixel pitch, the small-aperture effect becomes visible",
    "Small-pixel sensors hit the diffraction limit earlier.",
    "\U0001F4DA Deep Dive: Airy Disk and Diffraction-limit Aperture",
    "Find Airy disk diameter from wavelength and aperture.",
    "Judge if pixel-level hits the diffraction limit.",
    "Pick the best aperture for sharpness.",
    "Airy disk",
    "lambda=550nm, f/8: Airy diameter = 2.44 x 0.00055 x 8 ~ 0.0107mm = 10.7um; if pixel pitch > 10.7um the diffraction limit is not yet pixel-level.",
    "Limit aperture",
    "4um pixel, 400mm: pixel-level limit aperture ~ derived from pixel x 2.44 x lambda ~ f/29; too-small aperture softens via diffraction, landscapes commonly best at f/8-f/11.",
    "What is the Airy disk?",
    "Diffraction images a point as a disk whose diameter ~ lambda x f; smaller aperture, larger disk; beyond pixel size the whole image softens.",
    "How to pick the best aperture?",
    "Avoid the widest-aperture aberration and smallest-aperture diffraction; most lenses peak at f/5.6-f/11.",
]))

# ---------------- photo (23) ----------------
write('photo', build('photo', [
    "\U0001F9EE Depth of Field Calculator",
    "Compute photographic depth of field, near and far limits.",
    '\U0001F4D6 View the "Depth of Field Calculator User Guide"',
    "DOF = H d^2 / (H^2 - d^2) (simplified approximation)",
    "Focus distance must exceed focal length.",
    "\U0001F4DA Deep Dive: Total DOF (Near/Far/Total)",
    "Find the total DOF band from focal length, aperture and distance.",
    "Control front/back sharp range.",
    "Portrait vs landscape trade-offs.",
    "Total DOF",
    "50mm, f/4, focus 3m: H=f^2/(N c)+f ~ 20.88m, near limit 2.63m, far limit 3.49m => front DOF 0.37m, back DOF 0.49m, total 0.87m (shallow, good for bokeh); stop to f/11 extends total to ~2.75m.",
    "Distance effect",
    "Same 50mm f/4 focus 1m: near limit 0.96m, far limit 1.05m => total DOF only ~0.09m, extremely shallow; closer focus, narrower DOF.",
    "How is total DOF obtained?",
    "Far limit minus near limit equals front DOF (focus to nearest sharp) plus back DOF (focus to farthest sharp); closer focus and wider aperture shrink total DOF, the core of bokeh control.",
    "Why small aperture for landscapes?",
    "Small aperture gives large total DOF, sharp front to back; but too small invites diffraction, f/8-f/11 balances. Focused at hyperfocal, back DOF reaches infinity.",
    "How to Use the Depth of Field Calculator",
    "Quick reference for photo parameters, exposure and quality.",
    "What does the Depth of Field Calculator do?",
    "The DOF calculator derives depth of field, near/far limits and hyperfocal from aperture, focal length and focus distance; it helps control bokeh and focus region, aiding portrait and landscape shooting.",
    "How do I use the Depth of Field Calculator?",
    "Which scenarios suit the Depth of Field Calculator?",
]))

# ---------------- print-size (41) ----------------
write('print-size', build('print-size', [
    "\u2696\uFE0F Print Size Reference",
    "Convert image resolution to print size, DPI/PPI calculator",
    "/ Print Size Reference",
    '\U0001F4D6 View the "Pixels and Print Size User Guide"',
    "Size calculator",
    "Standard reference table",
    "Print size = pixels / DPI x unit factor (in=1, cm=2.54, mm=25.4); megapixels MP = W x H / 1e6; aspect ratio = W/H; 300 DPI pixels needed = print size(in) x 300",
    "W x H are pixel counts, DPI is print resolution. Same image, higher DPI -> smaller printable physical size; 300 DPI is the high-quality print baseline, 150 DPI suits large posters. Aspect ratio sets the photo ratio (3:2, 4:3, 1:1, etc).",
    "Image width (pixels)",
    "Image height (pixels)",
    "72 (screen display)",
    "150 (general print)",
    "200 (magazine quality)",
    "300 (high quality)",
    "600 (professional print)",
    "Paper unit",
    "\u2696\uFE0F Calculate size",
    "Common photo print sizes (300 DPI)",
    "DPI vs PPI:",
    "DPI (dots per inch) sets print sharpness. 300 DPI suits high-quality photos, 150 DPI general prints. Print size = pixels / DPI.",
    "\U0001F4DA Deep Dive: Print Size and Pixel Need",
    "Find print width/height from pixels and DPI.",
    "Back-calc the megapixels needed for a sharp print.",
    "Evaluate enlargement output.",
    "Print size",
    "6000 x 4000 (24MP) @300dpi: width = 6000/300 = 20in ~ 50.8cm, height = 4000/300 ~ 13.3in, about A3 full resolution.",
    "MP needed",
    "Print 30 x 20cm @300dpi: needs 3543 x 2362 ~ 8.4MP; below that it gets soft, so 24MP is plenty.",
    "Is print size bound by DPI?",
    "Yes, size = pixels / DPI; same pixels lower DPI prints larger but softer; set DPI by viewing distance.",
    "How many MP are enough?",
    "Common 24MP prints A3; large posters need 50MP+ or lower DPI viewed from afar.",
    'About "Print Size Reference"',
    "Print Size Reference is a photo-output helper that converts pixels and print DPI into physical size and lists pixel needs for common photo specs, judging whether a photo meets sharp print requirements.",
    "Two-way pixel and physical size conversion",
    "Multiple DPI tiers (72-600) with quality rating",
    "Standard photo-spec pixel table (6-inch / A4 etc)",
    "Sharpness check before 6-inch printing",
    "Confirm A4 album source-pixel threshold",
    "E-commerce hero image DPI vs load balance",
    "ID photo size and pixel match",
]))

# ---------------- raw-size (18) ----------------
write('raw-size', build('raw-size', [
    "\U0001F9E0 RAW File Size Estimate",
    "Estimate RAW file size from pixels and bit depth.",
    '\U0001F4D6 View the "RAW File Size Estimate User Guide"',
    "Pixels million",
    "Bit depth bit",
    "Size = pixels x bit depth / 8",
    "Compression and metadata overhead not counted.",
    "\U0001F4DA Deep Dive: RAW File Size and Recording",
    "Compute single-frame RAW MB from pixels and bit depth.",
    "Estimate video/burst buffer usage.",
    "Storage card selection.",
    "24MP, 14bit: RAW = 24e6 x 14 / 8 / 1e6 ~ 42MB/frame; 10fps burst buffers ~420MB/s, needs a fast card.",
    "Recording usage",
    "Same params @10fps for 60s: 42 x 10 x 60 / 1000 ~ 25.2GB, RAW video is very storage-hungry, usually a compressed proxy is used.",
    "How much bigger is RAW than JPEG?",
    "About 3-8x, as it holds all Bayer data and metadata; 14bit adds 17% over 12bit.",
    "Why does burst care about card speed?",
    "Hundreds of MB per second; slow cards fill the buffer and stop shooting quickly, need V90 / UHS-II class.",
]))

#!/usr/bin/env python3
# optical batch7 (5 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'optical')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'optical')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'critical-angle': [
"Critical Angle θc",
"From the refractive indices of the denser-to-rarer media, compute the total internal reflection critical angle using θc = arcsin(n₂/n₁).",
"/ Total Internal Reflection Critical Angle Calculator",
'📖 View the "Critical Angle θc User Guide"',
"Refractive index of the denser medium n₁",
"Refractive index of the rarer medium n₂",
"Total internal reflection exists only when light travels from the denser medium (n₁) to the rarer medium (n₂) with n₁>n₂.",
"Example: glass (n=1.5) → air (n=1.0), θc≈41.8°.",
"📚 In-Depth Analysis: Critical Angle Calculation",
"From the two media",
"refractive index",
"compute the total internal reflection critical angle.",
"Fiber optics / prism / total internal reflection condition assessment.",
"Determine whether total internal reflection occurs.",
"Glass to air",
"n₁=1.5 (glass), n₂=1.0 (air) →",
"=arcsin(1.0/1.5)=arcsin(0.667)≈41.8°; an incident angle > 41.8° means total internal reflection.",
"Water to air",
"n₁=1.33 → θc=arcsin(1/1.33)≈48.8°; the fiber cladding must have a lower refractive index to achieve total internal reflection guiding within the core.",
"What are the conditions for the critical angle to exist?",
"Light must travel from the denser medium (larger n) to the rarer medium (smaller n) with an incident angle ≥ θc; the reverse direction has no total internal reflection.",
"Is there refracted light in total internal reflection?",
"There is no refracted light; the energy is totally reflected back into the original medium, but an evanescent wave exists (used in interference/sensing).",
],
'optical-path-length': [
"Optical Path Length OP",
"From the refractive index and geometric distance, compute the equivalent vacuum path of light in the medium using optical path = n·L.",
"Optical Path Length Calculator",
"/ Optical Path Calculator",
"Optical Path Calculator",
'📖 View the "Optical Path Length OP User Guide"',
"Geometric distance L (mm)",
"Optical path length converts the medium path into an equivalent vacuum length; it is the basis of Fermat's principle and interference analysis.",
"📚 In-Depth Analysis: Optical Path Length Calculation",
"From the medium",
"refractive index",
"and the geometric distance, compute the optical path.",
"Used for interference / equal-optical-path conditions.",
"Fermat's principle equivalent air path.",
"Single medium",
"Glass of n=1.5 with 10cm thickness → OPL=1.5×10=15cm, equivalent to the phase delay of traveling 15cm in air.",
"Multiple segments",
"Air 5cm (n=1) + water 3cm (n=1.33) → OPL=5+3.99=8.99cm; interference depends on whether the OPL difference between paths is an integer multiple of λ.",
"What is optical path length?",
"The geometric distance weighted by the refractive index, reflecting phase accumulation; equal optical path means equal phase, which is the criterion for bright/dark interference.",
"What is the difference between optical path and geometric distance?",
"They are equal in vacuum; in a medium the optical path = refractive index × distance, which is longer than the geometric distance (light slows down).",
],
'microscope-magnification': [
"Compound Microscope Total Magnification",
"From the objective/eyepiece focal lengths, the optical tube length and the near point distance, compute the total magnification using M = (L/f₀)(D/fₑ).",
"Microscope Magnification Calculator",
"/ Microscope Magnification Calculator",
'📖 View the "Compound Microscope Total Magnification User Guide"',
"Optical tube length L (mm)",
"Near point distance D (mm)",
"The tube length L is the distance from the objective's back focal plane to the eyepiece's front focal plane (standard 160mm).",
"The near point distance D is usually taken as 250mm.",
"📚 In-Depth Analysis: Microscope Magnification",
"From the objective/eyepiece focal lengths and the tube length, compute the total magnification.",
"Choose the objective magnification to match the eyepiece.",
"Effective magnification is limited by resolution.",
"Total magnification",
"Tube length L=16cm, objective f_o=1cm, eyepiece f_e=2.5cm → M=(16/1)×(25/2.5)=16×10=160× (25cm is the near point distance).",
"Effective upper limit",
"An oil objective with NA=1.4 has an effective magnification of ≈1000×NA=1400×; blindly pushing to 2000× only shows blur without adding detail (empty magnification).",
"Is higher magnification better?",
"No. Beyond the effective magnification corresponding to the resolution (≈1000×NA) it becomes empty magnification, and detail gets noisier rather than clearer.",
"How to choose the objective magnification?",
"Start at low power to find the field then switch to high power; a 100× oil objective needs oil immersion to raise NA, and using it dry drops the resolution sharply.",
],
'thin-lens-imaging': [
"Thin Lens Imaging (Gaussian Formula)",
"Enter the object distance and focal length to compute the image distance and magnification using 1/f = 1/u + 1/v, and determine real/virtual image.",
"Thin Lens Imaging Calculator",
"/ Thin Lens Imaging Calculator",
'📖 View the "Thin Lens Imaging (Gaussian Formula) User Guide"',
"f = 1/u + 1/v (real object distance u>0, convex lens f>0). Image distance v>0 is a real image (can be caught on a screen), v",
"Gaussian formula: 1/f = 1/u + 1/v (real object distance u>0, convex lens f>0).",
"Image distance v>0 is a real image (can be caught on a screen), v<0 is a virtual image; magnification m<0 means inverted.",
"📚 In-Depth Analysis: Thin Lens Imaging",
"From the object distance and focal length, compute the image distance and magnification.",
"Determine real/virtual, upright/inverted, magnified/shrunk.",
"Camera / projector / magnifier design.",
"Real image",
"Convex lens f=10cm, object distance u=−15cm (real object) → 1/v=1/10−1/15=0.0333 → v=30cm (real image), magnification m=−v/u=2× inverted and magnified.",
"Virtual image",
"Object distance u=−5cm<f → 1/v=1/10−1/5=−0.1 → v=−10cm (virtual image), m=2× upright and magnified, the principle of a magnifier.",
"Sign convention?",
"Real object distance u is negative, real image v is positive, virtual image v is negative; m=−v/u, negative means inverted. A consistent sign convention avoids errors.",
"How many times does a magnifier magnify?",
"M≈25/f(cm); f=10cm→2.5×. The closer the object (f), the greater the magnification, but the farther and blurrier the image.",
],
'f-number': [
"F-Number N",
"From the focal length and effective aperture, compute the photographic lens f-number using N = f/D.",
"F-Number Calculator",
"/ F-Number Calculator",
"F-Number Calculator",
'📖 View the "F-Number N User Guide"',
"Effective aperture D (mm)",
"Each √2 increase in N halves the light intake; depth of field increases as N grows.",
"📚 In-Depth Analysis: F-Number",
"From the focal length and aperture, compute the F-number (F=f/D).",
"The F-number determines light intake and depth of field.",
"Light-passing area ∝ 1/F².",
"Basic conversion",
"Focal length 50mm, aperture 25mm → F=50/25=2.0 (F2 fast aperture); aperture 12.5mm → F=4.0.",
"Light intake",
"F2→F4 halves the aperture and reduces the light to 1/4 (a 2-stop difference); each √2 increase in F-number halves the light, and depth of field deepens accordingly.",
"Does a small F-number mean a large aperture?",
"Yes. F=f/D, so a large D gives a small F, more light intake, shallow depth of field and strong background blur.",
"Depth of field and F-number?",
"A large F-number (small aperture) gives deep depth of field with both foreground and background sharp; a small F-number gives shallow depth of field and strong blur.",
],
}

def build(slug, en_list):
    path = os.path.join(WORK, slug + '.json')
    wj = json.load(open(path, encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('!! %s length mismatch %d vs %d' % (slug, len(en_list), len(items)))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src'):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if not en or not isinstance(en, str):
            print('!! %s empty translation' % slug)
            sys.exit(1)
        if CJK.search(en) or CNP.search(en):
            print('!! %s CJK/CNP violation: %s' % (slug, en[:60]))
            sys.exit(1)
        mp[z] = en
    return mp

def write(slug, mp):
    os.makedirs(OUT, exist_ok=True)
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('name', slug)
    out = {'slug': slug, 'industry': 'optical', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

for slug, en_list in EN.items():
    write(slug, build(slug, en_list))

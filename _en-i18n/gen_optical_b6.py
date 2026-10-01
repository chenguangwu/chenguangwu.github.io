#!/usr/bin/env python3
# optical batch6 (5 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'optical')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'optical')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'snell-refraction': [
"Snell's Law of Refraction",
"From the incident angle and the refractive indices on both sides, compute the refraction angle using n₁·sinθ₁ = n₂·sinθ₂, and automatically detect total internal reflection.",
"Snell's Law of Refraction Calculator",
"/ Refraction Law Calculator",
"Refraction Law Calculator",
'📖 View the "Snell\'s Law of Refraction User Guide"',
"sinθ₁ = n₂·sinθ₂ to compute the refraction angle",
"Refractive index of the incident medium n₁",
"Refractive index of the refracting medium n₂",
"Snell's law: n₁·sinθ₁ = n₂·sinθ₂.",
"When n₁·sinθ₁ > n₂ (light going from denser to rarer medium at too large an angle), total internal reflection occurs.",
"📚 In-Depth Analysis: Snell's Law of Refraction",
"From the incident angle and the two media",
"refractive index",
"compute the refraction angle.",
"Determine refraction vs. total internal reflection.",
"Trial calculations for lenses, prisms and water surfaces.",
"Air to glass",
"n₁=1.0, n₂=1.5, incident 30° → sinθ₂=(1.0×sin30°)/1.5=0.333 → θ₂≈19.5°, the light bends toward the normal.",
"Total internal reflection boundary",
"Glass to air at 50° incident (> critical 41.8°) → no refraction, total internal reflection, the light is confined within the glass.",
"What is the refraction law formula?",
"n₁sinθ₁=n₂sinθ₂, where θ is the angle to the normal; the angle is smaller (closer to the normal) in the denser medium.",
"Why does a pool look shallower?",
"Refraction from water to air shifts the virtual image of the pool bottom upward; the apparent depth = real depth / refractive index, about 3/4 of the actual.",
],
'numerical-aperture': [
"Numerical Aperture NA",
"From the medium's refractive index and the maximum acceptance half-angle, compute the numerical aperture using NA = n·sinθ.",
"Numerical Aperture (NA) Calculator",
"/ Numerical Aperture Calculator",
"Numerical Aperture Calculator",
'📖 View the "Numerical Aperture NA User Guide"',
"Medium refractive index n",
"Maximum acceptance half-angle θ (°)",
"NA determines the light-gathering power and the diffraction resolution limit of a lens (resolution ∝ λ/NA).",
"Oil immersion objectives use oil with n≈1.515, significantly improving NA and resolution.",
"📚 In-Depth Analysis: Numerical Aperture NA",
"From the medium",
"refractive index",
"and the half-aperture angle, compute NA=n·sinθ.",
"NA determines light gathering and resolution.",
"Oil immersion raises NA and boosts resolution.",
"Dry vs. oil immersion objectives",
"Air n=1.0, θ=60° → NA=0.866; oil immersion n=1.515, θ=60° → NA=1.31, with light gathering and resolution improving together.",
"The larger the NA, the smaller the Rayleigh limit d=0.61λ/NA; with λ=550nm and NA=1.31, d≈256nm, finer than a dry objective.",
"Can NA be greater than 1?",
"Yes. Oil immersion (n>1) makes NA>1; the upper limit for a dry objective is ≈1 (since sinθ≤1 in air).",
"NA and depth of field?",
"A large NA gives high resolution but shallow depth of field; a high-magnification oil objective has an extremely thin focal depth and requires fine focusing.",
],
'lens-maker': [
"Lens Maker's Formula",
"From the refractive index and the radii of curvature of the two surfaces, compute the lens focal length using 1/f = (n-1)(1/R₁ - 1/R₂).",
"Lens Maker's Formula Calculator",
"/ Lens Maker's Formula Calculator",
'📖 View the "Lens Maker\'s Formula User Guide"',
"Front surface radius of curvature R₁ (mm)",
"Rear surface radius of curvature R₂ (mm)",
"Sign convention: convex surface R>0, concave surface R<0 (light entering from the left).",
"For a plano-convex lens, take R₂=∞ (enter a very large value as an approximation).",
"📚 In-Depth Analysis: Lens Maker's Formula",
"From the",
"refractive index",
"and the two radii of curvature, compute the focal length.",
"Design the refractive power of convex/concave lenses.",
"Infer curvature from the focal length of a trial lens.",
"Biconvex",
"n=1.5, R₁=+10cm, R₂=−10cm (biconvex) → 1/f=(1.5−1)(1/10−(−1/10))=0.5×0.2=0.1 → f=10cm (converging).",
"Plano-concave",
"n=1.5, R₁=∞, R₂=+10cm (plano-concave) → 1/f=0.5×(0−0.1)=−0.05 → f=−20cm (diverging).",
"How is the sign of the radius of curvature determined?",
"With light traveling left to right, a surface convex toward the incident light is positive, concave is negative; a sign error flips the sign of the focal length.",
"Is it only accurate for thin lenses?",
"This is a thin-lens approximation; thick lenses use matrix/thick-lens formulas, and the error becomes noticeable when the center thickness cannot be ignored.",
],
'gaussian-beam-waist': [
"Focused Gaussian Beam Waist",
"From the wavelength, the focal length of the focusing lens and the incident beam diameter, compute the beam waist radius using w₀ = 4λf/(πD).",
"Gaussian Beam Waist Radius Calculator",
"/ Gaussian Beam Waist Calculator",
"Gaussian Beam Waist Calculator",
'📖 View the "Focused Gaussian Beam Waist User Guide"',
"w₀ = 4λf/(πD) to compute the beam waist radius",
"Lens focal length f (mm)",
"Incident beam diameter D (mm)",
"Applicable to the approximation of a collimated incident Gaussian beam with a lens aperture much larger than the beam.",
"The smaller the beam waist radius, the higher the focused power density.",
"📚 In-Depth Analysis: Gaussian Beam Waist",
"From the wavelength and beam waist, compute the far-field divergence and waist.",
"Laser focusing/collimation design.",
"Use the M² factor to correct for real beams.",
"Waist and divergence",
"A 1064nm laser with beam waist w0=1mm → far-field half-angle θ=λ/(πw0)=1.064e-3/(π×1)≈0.339mrad; at 1m the spot radius is ≈0.34mm.",
"Focusing",
"Focusing the same beam through an f=50mm lens gives a focal waist w0'≈λf/(πw)=1.064e-3×50/(π×1)≈16.9μm, used for precision micromachining.",
"How small can the Gaussian waist be?",
"Limited by the diffraction limit: a shorter wavelength and a larger incident waist give a smaller focus; a real beam with M²>1 is M² times larger than ideal.",
"What affects the divergence angle?",
"θ=λ/(πw0); a smaller waist gives larger divergence, so collimation needs a large waist or a long-focal-length beam expander.",
],
'diffraction-grating': [
"Diffraction Grating Equation",
"From the grating constant, diffraction order and wavelength, compute the diffraction angle using d·sinθ = mλ.",
"Diffraction Grating Equation Calculator",
"/ Diffraction Grating Equation Calculator",
'📖 View the "Diffraction Grating Equation User Guide"',
"Grating constant d (nm)",
"Diffraction order m",
"Grating constant d = 1 / (lines per mm).",
"The maximum visible order satisfies m ≤ d/λ.",
"📚 In-Depth Analysis: Grating Diffraction Calculation",
"From the grating constant and wavelength, compute the angle of each diffraction order.",
"Used in spectrometer/spectroscopy design.",
"Determine whether a given order exists (sinθ≤1).",
"First-order diffraction",
"A grating of 500 lines/mm → constant d=1/500mm=2μm; λ=550nm, m=1 → sinθ=550e-9/2e-6=0.275 → θ≈16.0°.",
"Order limit",
"For the same grating at λ=550nm, sinθ=m·0.275≤1 → m is at most 3; higher orders with sinθ>1 do not exist.",
"What is the grating equation?",
"d·sinθ=m·λ (m=0,±1,±2…); the smaller d is, the larger the angular dispersion and the wider the separation.",
"Why are there missing orders?",
"When the",
"single-slit diffraction minimum",
"coincides exactly with a principal maximum of a given order, a missing order appears, determined by the ratio of the slit width to the grating constant.",
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

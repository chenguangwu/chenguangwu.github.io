#!/usr/bin/env python3
# optical batch8 (6 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'optical')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'optical')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'recommender-1': [
"🚗 Driving Glasses (Polarized + UV) Recommendation",
"Polarized + UV",
'📖 View the "Driving Glasses (Polarized + UV) Recommendation User Guide"',
"Driving glasses recommendation: match the polarization and UV400 protection level, visible light transmission (VLT) and tint to the driving scenario (daytime/night/rain-fog/strong light), while considering face-shape fit; for night driving choose high-transmission lenses.",
"📚 In-Depth Analysis: Lens Recommendation (by Scenario)",
"Recommend the lens type by prescription/purpose/budget.",
"Match for myopia/presbyopia/digital use across scenarios.",
"refractive index",
"and functional combination.",
"Moderate myopia + screen user",
"−3.00D, long screen time → recommend 1.60 aspheric + blue-light filter + anti-fatigue near addition, balancing thinness and eye protection, mid-range budget.",
"High prescription + appearance",
"−8.00D → 1.74 high-index aspheric to reduce thickness; choose impact-resistant PC for sports, or 1.67 for better value if ultimate thinness is not required.",
"Is blue-light filtering a must?",
"Recommended for heavy screen users; those mostly outdoors/driving do not need it all the time—choose by primary scenario to avoid color-shift issues.",
"What should the recommendation be based on?",
"Comprehensively based on prescription, visual scenario, frame type and budget—not a single parameter. This tool provides a preliminary screening that must still be confirmed by an optometrist.",
'About the "Driving Glasses (Polarized + UV) Recommendation"',
"Driving Glasses (Polarized + UV) Recommendation. A free online tool processed purely on the front end; data is not uploaded, protecting your privacy and security.",
],
'mirror-imaging': [
"Spherical Mirror Imaging",
"From the object distance and radius of curvature, compute the image distance and magnification using f=R/2 and 1/f = 1/u + 1/v.",
"Spherical Mirror Imaging Calculator",
"/ Spherical Mirror Imaging Calculator",
'📖 View the "Spherical Mirror Imaging User Guide"',
"Concave mirror f>0, convex mirror f<0 (here determined by the sign of the radius of curvature).",
"The formula is isomorphic to the thin lens: 1/f = 1/u + 1/v.",
"📚 In-Depth Analysis: Plane Mirror Imaging",
"From the object distance, compute the image distance and symmetry.",
"Number of images for multiple mirrors at an angle (360/θ−1).",
"Periscope / reflective system layout.",
"Single mirror",
"Object 30cm from the mirror → virtual image 30cm behind the mirror, same size and upright; the image and object are symmetric about the mirror plane.",
"Two mirrors at an angle",
"Two mirrors at 60° → number of images = 360/60−1 = 5; the smaller the angle the more images, approaching nearly infinite as they become parallel.",
"Is the image in a mirror left-right reversed?",
'It is front-back reversed (depth mirroring), not left-right; the habitual phrase "left-right reversed" is really front-back reversal relative to yourself.',
"What is the angle imaging formula?",
"For an integer angle θ, number of images = 360/θ−1 (when θ divides 360 exactly), otherwise take the floor.",
],
'rayleigh-resolution': [
"Rayleigh Criterion",
"From the wavelength and aperture diameter, compute the minimum resolvable angle of an optical system using θ = 1.22λ/D.",
"/ Rayleigh Resolution Limit Calculator",
'📖 View the "Rayleigh Criterion User Guide"',
"Aperture diameter D (mm)",
"Rayleigh criterion: two point sources are just resolvable when the maximum of one wavefront coincides with the first minimum of the other.",
"The human pupil is about 2-5mm; the resolution limit in visible light is about 1′ (arcminute).",
"📚 In-Depth Analysis: Rayleigh Resolution Limit",
"From the wavelength and NA, compute the minimum resolvable distance.",
"Upper limit of microscope/lens resolution.",
"Choose high NA or a shorter wavelength to improve resolution.",
"Visible light",
"λ=550nm, NA=1.4 (oil objective) → d=0.61×550/1.4≈240nm, the theoretical limit of an optical microscope (~0.2μm).",
"Improving resolution",
"Switching to UV λ=365nm or NA 1.5 → d≈149nm; to go smaller you need electron/scanning-probe methods to break the diffraction limit.",
"Two object points are just resolvable when the separation of their Airy disk centers is ≥ the first dark ring (1.22λ/2NA); take 0.61λ/NA as the spacing.",
"Can resolution be infinitely small?",
"Limited by the diffraction limit, optics reaches ~200nm; super-resolution bypasses the Rayleigh limit via STED/PALM and similar methods.",
],
'lens-power-diopter': [
"Diopter P",
"From the focal length (in meters), compute the lens diopter (D) using P = 1/f.",
"Diopter (Focal Length Conversion) Calculator",
"/ Diopter Calculator",
"Diopter Calculator",
'📖 View the "Diopter P User Guide"',
"Diopter unit D = m⁻¹; convex lens P>0 (hyperopia/presbyopia), concave lens P<0 (myopia).",
"📚 In-Depth Analysis: Lens Diopter",
"From the focal length (meters), compute the diopter D=1/f.",
"Convex is positive, concave is negative.",
"Reading and writing eyeglass prescriptions.",
"Focal length to diopter",
"Focal length f=0.1m (10cm convex lens) → D=1/0.1=+10.00D; f=−0.25m concave lens → −4.00D.",
"Two thin lenses in close contact and coaxial: total D=D₁+D₂; +2.00 combined with −1.00 → +1.00D, equivalent to a single lens.",
"What is the diopter unit?",
"D (diopter) = 1/meter; + is converging (hyperopia/presbyopia), − is diverging (myopia).",
"Do overlapping lenses simply add?",
"Thin lenses in close contact and coaxial have their diopters added; when separated, the separation effect must be included.",
],
'telescope-magnification': [
"Refracting Telescope Angular Magnification",
"From the objective and eyepiece focal lengths, compute the telescope angular magnification using M = f₀/fₑ.",
'📖 View the "Refracting Telescope Angular Magnification User Guide"',
"A Keplerian telescope uses two convex lenses; a positive magnification indicates an inverted image.",
"The larger the magnification the smaller the field of view, limited by the diffraction limit.",
"📚 In-Depth Analysis: Telescope Magnification",
"From the objective/eyepiece focal length ratio, compute the angular magnification.",
"Choose the magnification to match the aperture and stability.",
"Trade-off between hand shake and brightness.",
"Basic conversion",
"Objective focal length 1000mm, eyepiece 25mm → magnification M=1000/25=40×; switch to a 10mm eyepiece → 100×.",
"Brightness trade-off",
"Doubling the magnification halves the exit pupil diameter and reduces brightness to 1/4; handheld >10× is prone to shake and needs a tripod; for astronomy, pair high magnification with a large aperture to keep it bright.",
"Is higher magnification better?",
'No. Beyond the rule of thumb "aperture (mm)/magnification ≈ 7", handheld views shake, dim and lose quality, needing a tripod and sufficient aperture.',
"What limits the magnification?",
"Limited by aperture (brightness/resolution), atmospheric seeing and handheld stability; for ground observation the practical upper limit is about 2× aperture (mm).",
],
'recommender-11': [
"👓 Frame (Material/Style/Fit) Recommendation",
"Material/Style/Fit",
'📖 View the "Frame (Material/Style/Fit) Recommendation User Guide"',
"Frame recommendation: match by face shape (round/square/long/heart), prescription (small frames suit high powers), material (titanium/acetate/TR90) and budget, while balancing wearing comfort and optical center alignment.",
"📚 In-Depth Analysis: Lens Recommendation (by Function)",
"Recommend by functional priority (impact resistance/photochromic/polarized).",
"Split by scenario: sports/outdoor/driving.",
"Coating combination suggestions.",
"Sports and outdoor",
"Running/cycling → impact-resistant PC + photochromic + anti-reflective, light and shatter-resistant; add polarization for driving to cut road glare.",
"Active/breakage-prone → full-rim impact-resistant PC takes priority over thinness; for low prescriptions 1.50/1.56 is safe and sufficient.",
"What is the difference between PC and resin?",
"PC is extremely impact-resistant and light but scratches easily and needs a hard coat; resin (CR-39) is comfortable with good transmission but less impact-resistant—choose by scenario.",
"Can coatings be stacked?",
"Yes. Anti-reflective + hard + blue-light filter + photochromic can be combined, but more layers raise cost and risk—add on demand, don't pile them up.",
'About the "Frame (Material/Style/Fit) Recommendation"',
"Frame (Material/Style/Fit) Recommendation. A free online tool processed purely on the front end; data is not uploaded, protecting your privacy and security.",
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

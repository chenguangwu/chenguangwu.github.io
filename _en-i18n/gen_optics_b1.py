#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'optics')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'optics')
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
    out = {'slug': slug, 'industry': 'optics', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('fresnel-reflectance', build('fresnel-reflectance', [
        "Fraction of energy reflected at an interface at normal incidence.",
        "Fresnel Reflectance Calculator",
        "/ Fresnel Normal-Incidence Reflectance",
        "Fresnel Normal-Incidence Reflectance",
        "📖 Read the \"Fresnel Reflectance Calculator\" guide",
        "Air to glass reflects about 4%.",
        "📚 Deep dive: Fresnel reflectance at normal incidence",
        "Designing anti-reflection coating reduction for lens elements.",
        "Estimating reflected light loss at a glass surface.",
        "Computing the reflected power fraction at an interface.",
        "Air to glass n=1.5",
        "R=((n1−n2)/(n1+n2))²=((1−1.5)/(1+1.5))²=(−0.2)²=0.04=4%. A single surface loses 4% of the light.",
        "Air to water n=1.33",
        "R=((1−1.33)/2.33)²=(−0.142)²=2.0%. Water surfaces reflect less than glass.",
        "Total transmission through two surfaces of glass?",
        "Each surface reflects about 4%, so uncoated glass transmits approximately (0.96)²≈92%.",
        "How does coating reduce reflection?",
        "A quarter-wave coating makes the reflections from the two interfaces cancel, bringing single-surface reflection below 0.5%.",
    ]))

    write('prism-deviation', build('prism-deviation', [
        "Deviation angle of a small-angle prism from refractive index and apex angle",
        "Enter the refractive index n and prism apex angle A (degrees) to get the deviation angle.",
        "Prism Minimum Deviation Angle Calculator",
        "/ Prism Minimum Deviation Angle Calculator",
        "📖 Read the \"Deviation angle of a small-angle prism from refractive index and apex angle\" guide",
        "Apex angle A (degrees)",
        "The approximation applies to prisms with a small apex angle.",
        "📚 Deep dive: small-angle prism deviation",
        "Estimating dispersion deviation with a prism.",
        "Designing the angles of a beam splitter.",
        "Small-apex-angle prism approximation.",
        "n=1.5 and prism angle 10°",
        "Small-angle approximation δ=(n−1)A=(1.5−1)×10=5°. The emerging ray is deviated by 5°.",
        "δ=0.52×30=15.6° (small-angle approximation; large angles need the exact refraction formula).",
        "How large is the error in the small-angle approximation?",
        "The smaller A is, the more accurate it is; for A>20° use the exact minimum deviation formula δ=2arcsin(n sin(A/2))−A.",
        "Why can a prism disperse light?",
        "n varies with wavelength (dispersion), so different colours have different deviation angles and white light spreads into a spectrum.",
    ]))

    write('rayleigh-criterion', build('rayleigh-criterion', [
        "Minimum resolvable angle for diffraction by a circular aperture.",
        "/ Rayleigh Criterion",
        "📖 Read the \"Rayleigh Resolution Limit Calculator\" guide",
        "Aperture D (m)",
        "The human pupil of about 2mm resolves roughly 1′.",
        "📚 Deep dive: the Rayleigh resolution criterion (angular)",
        "Angular resolution limits of telescopes and the eye.",
        "Relationship between aperture and resolving power.",
        "Image quality evaluation of optical systems.",
        "Aperture 100mm, λ=550nm",
        "θ=1.22λ/D=1.22×550e-9/0.1=6.71e-6rad≈1.39″. Two stars closer than this cannot be separated.",
        "Aperture 200mm",
        "θ=1.22×550e-9/0.2=3.36e-6rad≈0.69″, doubling the resolving power.",
        "Does a larger aperture always look sharper?",
        "Yes: θ∝1/D, so doubling the aperture halves the angular resolution (with diminishing returns when atmospheric seeing limits you).",
        "Rayleigh versus Dawes limit?",
        "Dawes uses 116/D(mm) arcseconds, slightly looser than the Rayleigh 138/D(mm), and is often used for visual observation.",
    ]))

    write('snells-law', build('snells-law', [
        "Snell's Law Refraction Calculator",
        "Find the refraction angle from the incidence angle and refractive indices.",
        "/ Snell's Law",
        "Snell's Law",
        "📖 Read the \"Snell's Law Refraction Calculator\" guide",
        "Light going from air into glass bends toward the normal.",
        "📚 Deep dive: the law of refraction (Snell)",
        "Refraction angle of a ray crossing an interface.",
        "Calculating underwater apparent depth illusions.",
        "Ray tracing through prisms and lenses.",
        "Air to glass, 30° incidence",
        "sinθ2=n1 sinθ1/n2=1×sin30°/1.5=0.333, θ2=19.5°. The refracted ray sits closer to the normal.",
        "Glass to air, 30° incidence",
        "sinθ2=1.5×0.5/1=0.75, θ2=48.6°; beyond the critical angle there is total internal reflection.",
        "What is the incidence angle measured from?",
        "From the normal to the interface, not from the interface itself.",
        "When does total internal reflection occur?",
        "When going from optically denser to less dense medium with an incidence angle above the critical angle (about 41.8° for glass to air).",
    ]))


if __name__ == '__main__':
    main()
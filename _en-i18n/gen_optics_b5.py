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
    write('thin-film-max', build('thin-film-max', [
        "Constructive-interference wavelength from film thickness, refractive index and order",
        "Enter film refractive index n, thickness t (nanometres) and order m to get the constructive-interference wavelength.",
        "2nt = mλ (normal incidence)",
        "/ Thin-Film Constructive Interference Wavelength Calculator",
        "Thin-Film Constructive Interference Wavelength Calculator",
        "📖 Read the \"Constructive-interference wavelength from film thickness, refractive index and order\" guide",
        "Normal incidence, with both constructive conditions approximated.",
        "📚 Deep dive: thin-film constructive interference wavelength",
        "Wavelength design for anti-reflection and high-reflection coatings.",
        "The cause of the colours in soap films and oil films.",
        "Centre wavelength of interference filters.",
        "Water film n=1.33, thickness 500nm, m=1",
        "λ=2nt/m=2×1.33×500/1=1330nm (constructive in the infrared). Taking m=2 gives λ=665nm (visible red).",
        "Air film 250nm, m=1",
        "λ=2×1.0×250=500nm, so the film shows enhanced green.",
        "Constructive or destructive depends on the phase jump",
        "When one interface introduces a half-wave loss the conditions swap; this formula treats 2nt=mλ as constructive.",
        "Why is film thickness often taken as λ/4?",
        "A single-layer anti-reflection coating uses an optical thickness n t=λ/4 so the two reflections cancel.",
    ]))

    write('thin-film-min', build('thin-film-min', [
        "Destructive-interference wavelength from film thickness, refractive index and order",
        "Enter film refractive index n, thickness t (nanometres) and order m to get the destructive-interference wavelength.",
        "2nt = (m+½)λ (normal incidence)",
        "/ Thin-Film Destructive Interference Wavelength Calculator",
        "Thin-Film Destructive Interference Wavelength Calculator",
        "📖 Read the \"Destructive-interference wavelength from film thickness, refractive index and order\" guide",
        "The colours of a soap film come from thin-film interference.",
        "📚 Deep dive: thin-film destructive interference wavelength",
        "The minimum-reflection wavelength of an anti-reflection coating.",
        "Designing interference destructive conditions.",
        "Mapping film thickness to the extinction wavelength.",
        "Water film n=1.33, thickness 500nm, m=1",
        "λ=2nt/(m+0.5)=2×1.33×500/1.5=887nm (destructive near the infrared).",
        "For m=0",
        "λ=2×1.33×500/0.5=2660nm; smaller m corresponds to destructive interference at longer wavelengths.",
        "How does it differ from the constructive formula?",
        "Only the denominator changes from m to m+0.5 (the phase relation once the half-wave loss is accounted for).",
        "What is the best thickness for an anti-reflection coating?",
        "Usually take n t=λ/4 so the target wavelength is destructively interfered, rather than the general order m of this formula.",
    ]))

    write('index', build('index', [
        "🔭 Optics Tools",
        "Optics",
        "Optics Tools",
        "Refractive Index Calculator",
        "The Refractive Index Calculator is a free online optics tool that derives the refractive index from the speed of light in a medium. Runs entirely in the front end, uploads no data and needs no registration - open the page and use it. Suitable for engineering estimates, everyday conversions and quick cross-checks, with results one click away to copy.",
        "Combined Lens Focal Length Calculator",
        "The Combined Lens Focal Length Calculator finds the equivalent focal length of two lenses in contact, 1/f=1/f₁+1/f₂, for combining and converting focal lengths of multiple lenses in optical system design.",
        "Single-Slit Diffraction Dark Fringe Calculator",
        "The Single-Slit Diffraction Dark Fringe Calculator gives the first dark fringe angle of Fraunhofer single-slit diffraction, a·sinθ=λ, for quantitative analysis in physics experiments, optical measurement and diffraction phenomena.",
        "Spherical Mirror Focal Length Calculator",
        "The Spherical Mirror Focal Length Calculator uses f=R/2 to obtain the focal length of a concave or convex mirror from its radius of curvature, for parameter conversion in geometrical optics, telescopes and mirror design.",
        "Thin Lens Imaging Formula Calculator",
        "Thin lens imaging formula 1/f = 1/d_o + 1/d_i",
        "The Snell's Law Refraction Calculator finds the refraction angle from the incidence angle and the refractive indices on both sides, n₁sinθ₁=n₂sinθ₂, and determines whether total internal reflection occurs, for geometrical optics and fibre transmission analysis.",
        "Separated Two-Lens Combination Focal Length Calculator",
        "Combined focal length from two lens focal lengths and their separation",
        "Brewster Angle Calculator",
        "The Brewster Angle Calculator gives the incidence angle at which reflected light is fully polarised, θ=arctan(n₂/n₁), for parameter determination in optical coating, polariser and reflection elimination scenarios.",
        "Lens Optical Power (Dioptres) Calculator",
        "Optical power (dioptres) of a lens from its focal length",
        "The Rayleigh Resolution Limit Calculator gives the minimum resolvable angle for circular aperture diffraction, θ=1.22λ/D, for evaluating the resolution limits of telescopes, microscopes and camera lenses.",
        "Fresnel Reflectance Calculator",
        "The Fresnel Reflectance Calculator gives the fraction of energy reflected at an interface at normal incidence, determined by the refractive indices of the two media, for estimating reflection loss in anti-reflection coatings, windows and fibre end faces.",
        "Spherical Mirror Imaging Formula Calculator",
        "Spherical mirror imaging formula 1/f = 1/d_o + 1/d_i",
        "Optical Doppler Shift Calculator",
        "Observed frequency from the source frequency, relative velocity and speed of light",
        "Magnifier Angular Magnification Calculator",
        "Angular magnification of a simple magnifier from near point and focal length",
        "Prism Minimum Deviation Angle Calculator",
        "Deviation angle of a small-angle prism from refractive index and apex angle",
        "Malus's Law Calculator",
        "Transmitted intensity from the initial polarised intensity and the angle between polarisers",
        "Optical Magnification Calculator",
        "The Optical Magnification Calculator gives the lateral magnification m=−dᵢ/dₒ (the negative sign indicates inversion), for image magnification analysis in geometrical optics imaging, microscopes and projection systems.",
        "Resolving Power Calculator",
        "Resolving power of a circular aperture from aperture and wavelength",
        "Young's Double-Slit Fringe Spacing Calculator",
        "Fringe spacing from wavelength, screen distance and slit separation",
        "2nt = (m+½)λ (normal incidence)",
        "Enter film refractive index n, thickness t (nanometres) and interference order m to compute the wavelength producing destructive interference at normal incidence using 2nt=(m+½)λ, for coating and anti-reflection design.",
        "2nt = mλ (normal incidence)",
        "Constructive-interference wavelength from film thickness, refractive index and order",
        "About \"Optics Tools\"",
        "The Optics Tools collection contains 21 free online tools covering the common calculation, conversion and lookup needs of optics scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you will find practical tools here that are ready to use the moment you open them. All tools run entirely in the front end and upload no data to the server, protecting privacy and security.",
        "The optics tools collected on this page include (representative tools):",
        "These tools help you complete common optics tasks quickly without memorising complex formulas or manual conversions - just enter the values and get the result.",
        "Do the optics tools need downloading or registration?",
        "No. All optics tools on this page are pure front-end online tools. Open the page and use them directly, with no software to install, no account to register and no data uploaded.",
        "Are the optics tool results accurate, and is the data secure?",
        "The tools are based on public mathematical formulas and general industry standards, computing locally in your browser for instant results. All computation happens on your own device and data is never uploaded to the server, so privacy and security are assured.",
    ]))


if __name__ == '__main__':
    main()
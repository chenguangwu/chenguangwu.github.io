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
    write('doppler-optical', build('doppler-optical', [
        "Observed frequency from the source frequency, relative velocity and speed of light",
        "Enter source frequency f, relative velocity v and the speed of light c to get the observed frequency (non-relativistic approximation).",
        "Optical Doppler Shift Calculator",
        "/ Optical Doppler Shift Calculator",
        "📖 Read the \"Observed frequency from the source frequency, relative velocity and speed of light\" guide",
        "The optical Doppler effect: observed frequency f prime = f*(1 + v/c), where v is the relative velocity between source and observer (positive when receding, negative when approaching) and c is the speed of light; the shift is Δf = f prime − f = f*v/c; the fractional shift Δf/f = v/c is used in laser velocimetry and astronomical redshift measurement.",
        "Relative velocity v (m/s)",
        "Speed of light c (m/s)",
        "Take v positive for approaching (blueshift).",
        "📚 Deep dive: optical Doppler shift",
        "Estimating the radial velocity of celestial objects (redshift/blueshift).",
        "Laser velocimetry and coherent radar frequency shift calculations.",
        "Effect of source motion on the observed frequency.",
        "Source receding at 300km/s",
        "f′=f(1+v/c)=5e14×(1+3e5/3e8)=5e14×1.001=5.005e14 Hz, Δf=5e11 Hz (redshift).",
        "Approaching at 0.01c",
        "v/c=0.01: f′=5e14×1.01=5.05e14 Hz, blueshift.",
        "Why use this approximation when speeds approach light?",
        "When v≪c the classical approximation f′=f(1+v/c) applies; at high speed the relativistic longitudinal Doppler formula is required.",
        "How do you tell redshift from blueshift?",
        "Receding (v>0, moving apart) lowers the frequency and gives redshift; approaching raises it and gives blueshift.",
    ]))

    write('refractive-index-speed', build('refractive-index-speed', [
        "Refractive index from the speed of light in a medium.",
        "Refractive Index Calculator",
        "/ Refractive Index",
        "Refractive Index",
        "📖 Read the \"refractive-index-speed\" guide",
        "Speed of light in the medium v (m/s)",
        "Speed of light in vacuum c (m/s)",
        "Water has n≈1.33, glass n≈1.5.",
        "📚 Deep dive: deriving the refractive index from the speed of light",
        "Knowing the propagation speed of light in a medium, back out that medium's",
        "compare how strongly different optical materials slow light, for material selection.",
        "Check whether experimentally measured light speeds fall in a plausible refractive index range.",
        "Speed in water v=2.25e8 m/s",
        "n=c/v=3e8/2.25e8=1.3333, consistent with water's refractive index of about 1.33 in the visible range.",
        "Speed in glass v=1.5e8 m/s",
        "n=c/v=3e8/1.5e8=2.0000. This value corresponds to high-index optical glass (ordinary crown glass is about 1.5, corresponding to v≈2.0e8 m/s).",
        "Can the refractive index be less than 1?",
        "Since n=c/v, a computed n<1 means light travels faster than in vacuum, which violates special relativity and usually indicates a bad input (wrong units, or mixing group velocity with phase velocity). Ordinary transparent media have n≥1.",
        "Does the refractive index depend on wavelength?",
        "Yes, that is dispersion. A material typically has a higher index at short wavelengths (blue-violet), which is why a prism splits white light into a spectrum. Always state the wavelength used; the common reference is n_D for the sodium D line at 589 nm.",
    ]))

    write('resolving-power', build('resolving-power', [
        "Resolving power of a circular aperture from aperture and wavelength",
        "Enter the aperture diameter D and the wavelength λ (nanometres) to get the resolving power.",
        "Resolving Power Calculator",
        "/ Resolving Power Calculator",
        "📖 Read the \"Resolving power of a circular aperture from aperture and wavelength\" guide",
        "Aperture D (metres)",
        "A larger R means finer resolution.",
        "0.1 m, 550 nm → about 1.49×10⁵.",
        "📚 Deep dive: resolving power",
        "Evaluating the resolving power of gratings and telescopes.",
        "Calculating the minimum resolvable wavelength difference.",
        "Spectral resolution design for spectrometers.",
        "Aperture 0.1m, λ=550nm",
        "R=D/(1.22λ)=0.1/(1.22×550e-9)=1.49e5. Resolvable Δλ≈λ/R≈3.7e-3nm.",
        "Aperture 1m",
        "R=0.1/(1.22×550e-9)... correcting D=1: R=1/(6.71e-7)=1.49e6.",
        "Is a larger R always better?",
        "A large R resolves smaller wavelength differences, giving a spectrometer far better ability to separate neighbouring spectral lines.",
        "How does it relate to the Rayleigh angular criterion?",
        "They share the same origin: Rayleigh gives the minimum resolvable angle, while resolving power R=λ/Δλ=D/(1.22λ).",
        "How to use Resolving Power of a Circular Aperture from Aperture and Wavelength",
        "What does Resolving Power of a Circular Aperture from Aperture and Wavelength do?",
        "Enter the circular aperture diameter D and the light wavelength λ (nanometres) to compute the resolving power and the limiting resolution angle using R = D / (1.22·λ). Used to evaluate the resolution of telescopes, microscopes and cameras.",
        "How do I use Resolving Power of a Circular Aperture from Aperture and Wavelength?",
        "Which scenarios suit Resolving Power of a Circular Aperture from Aperture and Wavelength?",
        "Resolving power: the smallest angular separation at which an optical system can distinguish two points. The Rayleigh criterion gives θ_min≈1.22·λ/D (λ wavelength, D aperture).",
        "The smaller θ_min is, the higher the resolution; increasing the aperture D or using a shorter wavelength λ improves the resolution limit, a core constraint in microscope and telescope design.",
    ]))

    write('single-slit-diffraction', build('single-slit-diffraction', [
        "Angle of the first dark fringe in Fraunhofer single-slit diffraction.",
        "Single-Slit Diffraction Dark Fringe Calculator",
        "/ Single-Slit Diffraction",
        "Single-Slit Diffraction",
        "📖 Read the \"Single-Slit Diffraction Dark Fringe Calculator\" guide",
        "sinθ = mλ. The first dark fringe has m=1.",
        "Slit width a (m)",
        "Dark fringe order m",
        "The first dark fringe has m=1.",
        "📚 Deep dive: single-slit diffraction dark fringes",
        "Angular distribution of diffraction from a narrow slit.",
        "Estimating the limit of small apertures and gaps.",
        "Diffraction broadening in optical instruments.",
        "Slit width 0.1mm, λ=500nm, first order",
        "Slit width halved to 0.05mm",
        "sinθ=0.01, θ=0.573°; the narrower the slit, the more pronounced the diffraction.",
        "How wide is the central bright fringe?",
        "The spacing between the two first-order dark fringes is 2θ; a narrower slit gives a wider central fringe with more spread-out energy.",
        "How does it differ from the grating formula?",
        "A single slit shows broadening set by the slit width a, while a grating shows interference set by the period d, which is sharper.",
    ]))

    write('young-fringe', build('young-fringe', [
        "Fringe spacing from wavelength, screen distance and slit separation",
        "Enter the wavelength λ (nanometres), screen distance L (metres) and slit separation d (millimetres) to get the fringe spacing.",
        "Young's Double-Slit Fringe Spacing Calculator",
        "/ Young's Double-Slit Fringe Spacing Calculator",
        "📖 Read the \"Fringe spacing from wavelength, screen distance and slit separation\" guide",
        "Screen distance L (metres)",
        "Slit separation d (millimetres)",
        "Fringe spacing is proportional to wavelength and inversely proportional to slit separation.",
        "📚 Deep dive: Young's double-slit fringe spacing",
        "Fringe density in the two-slit interference experiment.",
        "Effect of wavelength and screen distance on fringe spacing.",
        "Estimating the sensitivity of interferometric measurement.",
        "λ=550nm, slit separation 0.5mm, screen distance 1m",
        "Δy=λL/d=550e-9×1/0.5e-3=1.1e-3m=1.1mm. Adjacent bright fringes are 1.1mm apart.",
        "Slit separation halved to 0.25mm",
        "Δy=2.2mm; the closer the slits, the wider the fringes.",
        "Are the fringes evenly spaced?",
        "They are evenly spaced under the small-angle approximation; at large angles the spherical wave phase makes the spacing vary slightly.",
        "What do double-slit fringes look like in white light?",
        "A white central fringe with coloured spectra spreading to either side, violet close in and red farther out.",
    ]))


if __name__ == '__main__':
    main()
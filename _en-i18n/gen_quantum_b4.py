#!/usr/bin/env python3
# gen_quantum_head.py — shared head for quantum batches b1..b6
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'quantum')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'quantum')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
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
    out = {'slug': slug, 'industry': 'quantum', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('photoelectric-effect', build('photoelectric-effect', [
        "Maximum initial kinetic energy of a photoelectron equals photon energy minus work function.",
        "Photoelectric Effect Calculator",
        "/ Photoelectric Effect",
        "Photoelectric effect",
        "📖 View \"Photoelectric Effect Calculator - User Guide\"",
        "K_max = hf - phi. f must be > phi/h to escape.",
        "Work function phi (eV)",
        "f must be > phi/h to escape.",
        "📚 In-depth: Photoelectric Effect Maximum Kinetic Energy",
        "Photoelectron maximum",
        "Kinetic energy calculation",
        "Determine cut-off frequency and work function.",
        "Principle of phototubes / solar cells.",
        "f=1e15 Hz, work function 2 eV",
        "Frequency below cut-off",
        "When hf < Phi, K_max < 0, no photoelectron emission (independent of light intensity).",
        "Does light intensity affect kinetic energy?",
        "No; it only affects the number of photoelectrons; kinetic energy is set by frequency (Einstein's equation).",
        "Reflection of wave-particle duality?",
        "Photon energy",
        "E=hf is delivered to the electron in one step, reflecting the particle nature of light.",
    ]))
    write('photoelectric-threshold', build('photoelectric-threshold', [
        "Find cut-off frequency from work function",
        "Enter work function phi (eV) to obtain the cut-off frequency.",
        "Photoelectric Threshold Frequency Calculator",
        "/ Photoelectric Threshold Frequency Calculator",
        "📖 View \"Find Cut-off Frequency from Work Function - User Guide\"",
        "Work function phi (eV)",
        "phi = 4.5 eV -> about 1.09 x 10^15 Hz.",
        "📚 In-depth: Photoelectric Cut-off Frequency",
        "Material cut-off frequency / wavelength.",
        "Determine whether photoelectrons can be produced.",
        "Correspondence between work function and wavelength.",
        "Work function 4.5 eV",
        "f_0 = Phi/h = 4.5 x 1.602e-19/6.626e-34 = 1.09e15 Hz, corresponding to lambda_0 = 276 nm (ultraviolet).",
        "Sodium 2.3 eV",
        "f_0 = 5.57e14 Hz, lambda_0 = 538 nm, visible light can already eject electrons.",
        "Cut-off wavelength and work function",
        "lambda_0 = hc/Phi = 1240/Phi(eV) nm; the larger the work function, the shorter the cut-off wavelength.",
        "Why do most metals need ultraviolet?",
        "Most metals have Phi > 3 eV, so lambda_0 is in the ultraviolet region.",
    ]))
    write('photon-energy', build('photon-energy', [
        "Find photon energy from frequency or wavelength.",
        "Photon Energy Calculator",
        "/ Photon Energy",
        "Photon energy",
        "📖 View \"Photon Energy Calculator - User Guide\"",
        "Visible light approx 2.48 eV.",
        "500 nm visible light approx 2.48 eV.",
        "📚 In-depth: Photon Energy",
        "Estimate single-photon energy.",
        "Wavelength-energy correspondence.",
        "Photochemical / biological excitation threshold.",
        "500 nm visible light",
        "1064 nm infrared laser",
        "E = 1.24e-19 J = 0.775 eV, often used for frequency doubling to obtain green light.",
        "Shorter wavelength, energy?",
        "Higher; E = hc/lambda, ultraviolet photons have far more energy than infrared photons.",
        "Common conversions",
        "E(eV) = 1240/lambda(nm), convenient for quick estimation.",
    ]))
    write('photon-flux', build('photon-flux', [
        "Find photons per second from power and wavelength",
        "Enter optical power P and wavelength lambda to obtain the photon flux.",
        "Photon Flux Calculator",
        "/ Photon Flux Calculator",
        "📖 View \"Find Photons per Second from Power and Wavelength - User Guide\"",
        "📚 In-depth: Photon Flux",
        "Photon rate for a given power.",
        "Optical communication / photovoltaic photon counting.",
        "Radiance to photon-flow conversion.",
        "1 W, 500 nm source",
        "N = P lambda/(hc) = 1 x 5e-7/1.986e-25 = 2.52e18 photons/s.",
        "Same power 1000 nm",
        "Wavelength doubled -> N doubled = 5.04e18/s (per",
        "Photon energy",
        "halved).",
        "With fixed power, why does longer wavelength give higher flux?",
        "Energy per photon decreases with increasing wavelength, so more photons for the same power.",
        "Relation with light intensity?",
        "Light intensity = power per unit area; multiply by area to get total photon rate.",
    ]))
    write('photon-momentum', build('photon-momentum', [
        "Relativistic momentum of a photon.",
        "Photon Momentum Calculator",
        "/ Photon Momentum",
        "Photon momentum",
        "📖 View \"Photon Momentum Calculator - User Guide\"",
        "Photon momentum and energy: momentum p = h / lambda, where h is Planck's constant and lambda is the wavelength; photon energy E = hc / lambda; wavenumber = 1 / lambda; shorter wavelength gives larger momentum and energy, used in Compton scattering and radiation-pressure calculations.",
        "A photon has zero rest mass but carries momentum.",
        "📚 In-depth: Photon Momentum",
        "Estimate radiation pressure.",
        "Force on optical tweezers / solar sails.",
        "Momentum conservation in Compton scattering.",
        "500 nm photon",
        "Solar sail under radiation pressure",
        "At total reflection the momentum change is 2p, accumulating into a measurable thrust.",
        "Does a photon have mass?",
        "Rest mass is zero, but it has momentum p = E/c = h/lambda, given by the energy-momentum relation.",
        "How large is the radiation pressure?",
        "P_rad = I/c (absorption) / 2I/c (reflection), ground sunlight about 4.7 mu Pa.",
    ]))

if __name__ == '__main__':
    main()

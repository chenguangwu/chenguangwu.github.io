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
    write('angular-momentum-quant', build('angular-momentum-quant', [
        "Find angular momentum from principal quantum number",
        "Enter principal quantum number n to obtain orbital angular momentum.",
        "Angular Momentum Quantization Calculator",
        "/ Angular Momentum Quantization Calculator",
        "📖 View \"Find Angular Momentum from Principal Quantum Number - User Guide\"",
        "📚 In-depth: Angular Momentum Quantization",
        "Hydrogen atom orbitals",
        "Angular momentum",
        "Values.",
        "Determine the allowed quantized angular momentum.",
        "Convert angular momentum quantum numbers to physical quantities.",
        "n=3 angular momentum",
        "L=sqrt[l(l+1)] hbar approaches n hbar at the maximum l=n-1; for n=3, L approx 3 hbar = 3 x 1.0546e-34 = 3.16e-34 J s.",
        "Comparison with classical",
        "Angular momentum takes only integer multiples of hbar and cannot be described by continuous values for microscopic orbits.",
        "Why sqrt[l(l+1)] hbar instead of l hbar?",
        "In quantum mechanics the magnitude is L=sqrt[l(l+1)] hbar, while the z-component m_l hbar is an integer multiple of l hbar.",
        "What is hbar?",
        "Reduced Planck constant hbar = h/2pi = 1.0546e-34 J s.",
        "How to use Find Angular Momentum from Principal Quantum Number",
        "What does finding angular momentum from the principal quantum number do?",
        "The tool uses L=sqrt(l(l+1)) hbar or the simplified L=n hbar to compute orbital angular momentum from n, suitable for atomic physics and quantum mechanics exercises.",
        "How do I use Find Angular Momentum from Principal Quantum Number?",
        "In what scenarios is finding angular momentum from the principal quantum number useful?",
        "Formula and meaning",
        "Magnitude of orbital angular momentum L=sqrt(l(l+1)) hbar, where l is the azimuthal quantum number (0,1,2,...); its z-component takes m_l hbar (m_l = -l...l). Quantization means angular momentum is not continuous.",
        "Used for atomic shells, spectral terms and magnetic quantum number analysis; l determines subshell shape (s/p/d/f).",
        "Results follow the standard quantum mechanical model; specific systems also require spin and coupling schemes.",
    ]))
    write('band-gap-photon', build('band-gap-photon', [
        "Find absorption/emission wavelength from band-gap energy",
        "Enter band-gap energy Eg (eV) to obtain the corresponding photon wavelength.",
        "Band-Gap Photon Wavelength Calculator",
        "/ Band-Gap Photon Wavelength Calculator",
        "📖 View \"Find Absorption/Emission Wavelength from Band-Gap Energy - User Guide\"",
        "Band gap Eg (eV)",
        "Si band gap 1.12 eV -> about 1107 nm (infrared).",
        "📚 In-depth: Band-Gap Photon Wavelength",
        "Estimate the longest wavelength a semiconductor can absorb.",
        "Design cut-off wavelength for photovoltaic materials.",
        "Determine the optical response range of a material.",
        "Silicon band gap 1.12 eV",
        "lambda = hc/Eg = 1240 eV nm / 1.12 eV = 1107 nm. Silicon absorbs only light with wavelength < 1107 nm.",
        "Gallium arsenide 1.42 eV",
        "lambda = 1240/1.42 = 873 nm, near infrared, suitable for red-light alloy solar cells.",
        "Where does the constant 1240 come from?",
        "hc approx 1240 eV nm, so lambda(nm) = 1240/E(eV), convenient for band-wavelength conversion.",
        "Does a smaller band gap give a wider absorption range?",
        "Yes; the smaller the band gap, the longer the cut-off wavelength, so more sunlight can be absorbed (but the voltage is lower).",
    ]))
    write('bohr-orbit-radius', build('bohr-orbit-radius', [
        "Bohr Orbit Radius Calculator",
        "Radius of the nth orbit of hydrogen.",
        "/ Bohr Orbit Radius",
        "Bohr orbit radius",
        "📖 View \"Bohr Orbit Radius Calculator - User Guide\"",
        "Bohr orbit radius r_n = a0 x n^2, where a0 = 0.529 x 10^-10 m (0.529 A, ground-state radius of hydrogen) and n is the principal quantum number (positive integer); at n = 1, r = 0.529 A, at n = 2, 2.12 A, at n = 3, 4.76 A; the corresponding energy level E_n = -13.6 / n^2 eV (ground state -13.6 eV, n = 2 is -3.4 eV), the larger n the closer to the ionization limit 0.",
        "Ground state n=1 radius 0.529 A.",
        "📚 In-depth: Bohr Orbit Radius",
        "Orbit radii of hydrogen at each energy level.",
        "Estimate atomic scale.",
        "Cross-check with Rydberg constant.",
        "Ground state n=1",
        "r = a0 n^2 = 5.29e-11 x 1 = 5.29e-11 m = 0.529 A (Bohr radius).",
        "r = 5.29e-11 x 4 = 2.12e-10 m; radius grows rapidly as n^2.",
        "Is a0 an empirical value?",
        "No, a0 = 4 pi eps0 hbar^2 / (m_e e^2) = 5.29e-11 m, derived from fundamental constants.",
        "Scope of the Bohr model?",
        "Good only for hydrogen-like single-electron approximation; multi-electron cases need Schrodinger / Hartree-Fock.",
    ]))
    write('boltzmann-population', build('boltzmann-population', [
        "Find the particle number ratio from level spacing and temperature",
        "Enter energy-level difference Delta E (eV) and temperature T to obtain the population ratio of two levels.",
        "Boltzmann Population Ratio Calculator",
        "/ Boltzmann Population Ratio Calculator",
        "📖 View \"Find the Particle Number Ratio from Level Spacing and Temperature - User Guide\"",
        "Energy-level difference Delta E (eV)",
        "📚 In-depth: Boltzmann Population Ratio",
        "Ratio of particle numbers between two energy levels.",
        "Judge inversion between upper/lower levels at laser/thermal equilibrium.",
        "Effect of temperature on excited-state fraction.",
        "Energy gap 0.1 eV, 300 K",
        "N_high/N_low = e^(-Delta E/kT) = e^(-0.1/(8.617e-5 x 300)) = e^(-3.86) = 0.021, the upper state is only about 2%.",
        "1 eV energy gap",
        "kT approx 0.0259 eV, ratio = e^(-38.6) approx 1.6e-17, almost entirely in the ground state at room temperature.",
        "What is kT at room temperature?",
        "About 0.0259 eV; when Delta E >> kT the upper level is essentially unoccupied.",
        "Does degeneracy matter?",
        "Strictly g_high/g_low x e^(-Delta E/kT); this tool assumes degeneracy 1.",
    ]))
    write('compton-shift', build('compton-shift', [
        "Change in wavelength after X-ray scattering.",
        "Compton Shift Calculator",
        "/ Compton Shift",
        "Compton shift",
        "📖 View \"Compton Shift Calculator - User Guide\"",
        "lambda_C = h/(m_e c) approx 2.43 pm. 90 deg scattering Delta lambda approx 2.43 pm.",
        "Scattering angle theta (deg)",
        "90 deg scattering Delta lambda approx 2.43 pm.",
        "📚 In-depth: Compton Shift",
        "Wavelength increment of X/gamma photon after scattering.",
        "Effect of scattering angle on wavelength shift.",
        "Energy loss in photon-electron collision.",
        "90 deg scattering",
        "180 deg backscattering",
        "Delta lambda = 2.426 pm x 2 = 4.85 pm, maximum shift.",
        "What is h/m_e c?",
        "Electron",
        "Compton wavelength",
        "2.426 pm; shift is 0 at theta=0 (no collision).",
        "Does it depend on the incident wavelength?",
        "The shift depends only on the scattering angle, not on the incident wavelength (the relative effect is more significant at short wavelengths).",
    ]))

if __name__ == '__main__':
    main()

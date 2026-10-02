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
    write('compton-wavelength', build('compton-wavelength', [
        "Find Compton wavelength from particle mass",
        "Enter particle mass m to obtain the Compton wavelength.",
        "Compton Wavelength Calculator",
        "/ Compton Wavelength Calculator",
        "📖 View \"Find Compton Wavelength from Particle Mass - User Guide\"",
        "Electron m=9.109e-31 -> 2.426 pm.",
        "📚 In-depth: Compton Wavelength",
        "Definition of a particle's Compton wavelength.",
        "Estimate the characteristic scale of scattering.",
        "Inverse relationship between mass and wavelength.",
        "Electron",
        "Proton",
        "m_p approx 1836 m_e -> lambda_c approx 1.32 fm, three orders of magnitude smaller than the electron.",
        "Physical meaning?",
        "The Compton wavelength is the characteristic length of a particle's wave nature, and also the upper-scale limit of the Compton shift.",
        "Relation with mass?",
        "lambda_c = h/(mc); the larger the mass, the shorter the wavelength.",
    ]))
    write('cyclotron-frequency', build('cyclotron-frequency', [
        "Cyclotron angular frequency of a charged particle in a magnetic field.",
        "Cyclotron Frequency Calculator",
        "/ Cyclotron Frequency",
        "Cyclotron frequency",
        "📖 View \"Cyclotron Frequency Calculator - User Guide\"",
        "omega = qB/m (independent of velocity). Used for cyclotron design.",
        "Magnetic flux density B (T)",
        "omega = qB/m (independent of velocity).",
        "Used for cyclotron design.",
        "📚 In-depth: Cyclotron Frequency",
        "Cyclotron motion of charged particles in a magnetic field.",
        "Cyclotron resonance, mass-spectrometer design.",
        "Estimate plasma confinement frequency.",
        "Electron in 1 T field",
        "Proton (m 1836 times larger)",
        "f_c = 28 GHz/1836 = 15.2 MHz, frequency drops inversely with mass.",
        "Does it depend on radius?",
        "No; cyclotron frequency depends only on q/m and B; radius only affects orbit size.",
        "Relativistic correction?",
        "At high speed mass increases, frequency drops with gamma, requiring the relativistic formula.",
    ]))
    write('de-broglie-wavelength', build('de-broglie-wavelength', [
        "Relation between the wavelength of matter waves and momentum.",
        "De Broglie Wavelength Calculator",
        "/ De Broglie Wavelength",
        "De Broglie wavelength",
        "📖 View \"De Broglie Wavelength Calculator - User Guide\"",
        "Electron 1e6 m/s -> lambda approx 0.73 nm.",
        "📚 In-depth: De Broglie Wavelength",
        "Estimate matter-wave wavelength.",
        "Basis for electron-microscope resolution.",
        "Neutron/atom diffraction scale.",
        "Electron 1e6 m/s",
        "Electron 1e7 m/s",
        "lambda shortens 10x = 0.0727 nm, close to atomic spacing, lattice diffraction becomes observable.",
        "Larger velocity, wavelength?",
        "Shorter; lambda = h/(mv), so high-speed electrons have short wavelengths,",
        "Resolving power",
        "High.",
        "Do macroscopic objects have a wavelength?",
        "Yes but extremely short (huge mass), wave nature is unobservable.",
    ]))
    write('energy-time-uncertainty', build('energy-time-uncertainty', [
        "Find energy broadening from time uncertainty",
        "Enter time uncertainty Delta t to obtain the minimum energy broadening.",
        "Energy-Time Uncertainty Calculator",
        "/ Energy-Time Uncertainty Calculator",
        "📖 View \"Find Energy Broadening from Time Uncertainty - User Guide\"",
        "Time uncertainty Delta t (s)",
        "📚 In-depth: Energy-Time Uncertainty",
        "Estimate natural linewidth of an energy level.",
        "Relation between excited-state lifetime and width.",
        "Energy uncertainty in ultrafast processes.",
        "Lifetime 1 ns",
        "Lifetime 1 fs",
        "tau = 1e-15 -> Delta E approx 3.29e-4 eV, linewidth of ultrafast states grows significantly.",
        "Is it a measurement error?",
        "It is intrinsic fluctuation: short-lived states necessarily have energy broadening (natural linewidth).",
        "Symmetric with position-momentum uncertainty?",
        "Formally similar but time is not an operator, so the meaning differs slightly.",
    ]))
    write('fermi-energy-3d', build('fermi-energy-3d', [
        "Find Fermi energy from free-electron density",
        "Enter free-electron number density n and effective mass m to obtain the Fermi energy.",
        "3D Fermi Energy Calculator",
        "/ 3D Fermi Energy Calculator",
        "📖 View \"Find Fermi Energy from Free-Electron Density - User Guide\"",
        "Electron density n (m^-3)",
        "Effective mass m (kg)",
        "Copper about 7.0 eV.",
        "📚 In-depth: 3D Fermi Energy",
        "Estimate the Fermi level of a metal.",
        "Relation between electron concentration and Fermi energy.",
        "Reference energy for transport properties.",
        "Copper n=8.5e28/m^3",
        "E_F = hbar^2/(2m)(3 pi^2 n)^(2/3) = 7.05 eV, consistent with the measured value of about 7.0 eV for copper.",
        "Halve n",
        "E_F prop to n^(2/3); halving the concentration lowers the Fermi energy to 7.05 x 2^(-2/3) = 4.44 eV.",
        "Only valid at zero temperature?",
        "The formula is the T=0 limit; at room temperature kT << E_F the approximation is still good.",
        "Is the Fermi energy the highest occupied energy?",
        "Yes; at 0 K electrons fill up to E_F, above which everything is empty.",
        "How to use Find Fermi Energy from Free-Electron Density",
        "What does finding Fermi energy from free-electron density do?",
        "Enter free-electron number density n and effective mass m; the tool computes the Fermi energy by the 3D free-electron gas formula E_F = (hbar^2/2m)(3 pi^2 n)^{2/3}, used to estimate the highest occupied electron level in metals and semiconductors.",
        "How do I use Find Fermi Energy from Free-Electron Density?",
        "In what scenarios is finding Fermi energy from free-electron density useful?",
        "3D free-electron gas Fermi energy E_F = (hbar^2/2m) (3 pi^2 n)^(2/3) (n electron number density): the highest energy level occupied by electrons at absolute zero.",
        "E_F marks the highest kinetic-energy scale of electrons in a metal; when temperature is far below T_F = E_F/k_B the electron gas is highly degenerate and Fermi-Dirac statistics must be used.",
        "Results follow the ideal free-electron model; real band structure and effective mass will modify them; for physics estimation reference only.",
    ]))

if __name__ == '__main__':
    main()

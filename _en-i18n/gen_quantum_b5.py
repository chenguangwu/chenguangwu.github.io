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
    write('quantum-oscillator-energy', build('quantum-oscillator-energy', [
        "Find energy from level and frequency",
        "Enter level n and frequency f to obtain the harmonic oscillator energy.",
        "Quantum Harmonic Oscillator Energy Calculator",
        "/ Quantum Harmonic Oscillator Energy Calculator",
        "📖 View \"Find Energy from Level and Frequency - User Guide\"",
        "Energy level n",
        "n=2, f=1e14 Hz -> about 1.035 eV.",
        "📚 In-depth: Quantum Harmonic Oscillator Energy",
        "Molecular vibrational energy levels.",
        "Estimate zero-point energy.",
        "Quantum-optical cavity mode energy.",
        "Zero-point energy n=0",
        "E_0 = hbar omega/2 = 3.31e-20 J = 0.207 eV, the ground state still has non-zero energy.",
        "Level spacing?",
        "Equal spacing Delta E = hbar omega, unlike the classical harmonic oscillator.",
        "Why is zero-point energy not zero?",
        "The uncertainty relation forbids a particle from resting at the potential minimum, so the ground state retains hbar omega/2.",
    ]))
    write('rydberg-wavelength', build('rydberg-wavelength', [
        "Wavelength of hydrogen spectral lines.",
        "Rydberg Wavelength Calculator",
        "/ Rydberg Formula",
        "Rydberg formula",
        "📖 View \"Rydberg Wavelength Calculator - User Guide\"",
        "R approx 1.097e7 m^-1. n:3->2 is the Balmer alpha line approx 656 nm.",
        "Lower level n1",
        "Upper level n2",
        "Rydberg constant R approx 1.097e7 m^-1.",
        "n:3->2 is the Balmer alpha line approx 656 nm.",
        "📚 In-depth: Rydberg Wavelength (Spectral Lines)",
        "Transition wavelength of hydrogen.",
        "Balmer / Lyman series calculation.",
        "Spectral-line identification and assignment.",
        "1/lambda = R_inf(1/2^2 - 1/3^2) = 1.097e7 x 0.1389, lambda = 656.3 nm (red light).",
        "n=2->1 (Lyman alpha)",
        "1/lambda = R_inf(1 - 1/4) = 0.823e7, lambda = 121.6 nm (ultraviolet).",
        "What is R_inf?",
        "Rydberg constant 1.097373e7 m^-1 (infinite nuclear-mass approximation).",
        "Which n correspond to the different series?",
        "Lyman n->1, Balmer n->2, Paschen n->3, in ultraviolet / visible / infrared respectively.",
    ]))
    write('spin-magnetic-moment', build('spin-magnetic-moment', [
        "Find magnetic moment from magnetic quantum number",
        "Enter magnetic quantum number m_l to obtain the orbital magnetic moment (in units of mu_B).",
        "Electron Spin Magnetic Moment Calculator",
        "/ Electron Spin Magnetic Moment Calculator",
        "📖 View \"Find Magnetic Moment from Magnetic Quantum Number - User Guide\"",
        "Magnetic quantum number m_l",
        "📚 In-depth: Spin Magnetic Moment",
        "Values of the electron spin magnetic moment.",
        "Magnitude of magnetic resonance / Zeeman splitting.",
        "Convert magnetic moment to Bohr magneton.",
        "m_l=1 (or spin +/- 1 unit)",
        "Electron spin intrinsic",
        "|mu_s| = g_s mu_B/2 approx 9.27e-24 J/T (g_s approx 2), exactly 1 Bohr magneton.",
        "What is mu_B?",
        "Bohr magneton 9.274e-24 J/T, the natural unit of atomic magnetic moment.",
        "Relation with orbital magnetic moment?",
        "Same form mu = mu_B m_l; the spin g-factor is 2.",
    ]))
    write('stefan-boltzmann-power', build('stefan-boltzmann-power', [
        "Find radiation power from area and temperature",
        "Enter area A and absolute temperature T to obtain the blackbody radiation power.",
        "Blackbody Radiation Power Calculator",
        "/ Blackbody Radiation Power Calculator",
        "📖 View \"Find Radiation Power from Area and Temperature - User Guide\"",
        "A=0.01, T=300 K -> about 4.59 W.",
        "📚 In-depth: Stefan-Boltzmann Radiation Power",
        "Total blackbody radiation power.",
        "Estimate radiation from stars / hot bodies.",
        "Radiative cooling design.",
        "0.01 m^2 blackbody at 300 K",
        "Solar surface 5778 K (per unit area)",
        "Blackbody condition?",
        "The formula holds for an ideal blackbody (emissivity 1); multiply by emissivity epsilon for a gray body.",
        "Sensitive to temperature?",
        "P prop T^4; a slight temperature rise sharply increases radiation power.",
    ]))
    write('thermal-de-broglie', build('thermal-de-broglie', [
        "Find thermal de Broglie wavelength from temperature and mass",
        "Enter mass m and temperature T to obtain the thermal de Broglie wavelength.",
        "Thermal de Broglie Wavelength Calculator",
        "/ Thermal de Broglie Wavelength Calculator",
        "📖 View \"Find Thermal de Broglie Wavelength from Temperature and Mass - User Guide\"",
        "Electron at 300 K -> about 4.3 nm.",
        "📚 In-depth: Thermal de Broglie Wavelength",
        "Determine the quantum degeneracy condition.",
        "Bose-Einstein condensation criterion.",
        "Statistical regime of quantum gases.",
        "Electron at 300 K",
        "Cool down to 3 K",
        "lambda_th prop 1/sqrt(T) increases 10x = 43 nm, easier to enter the degenerate state.",
        "De Broglie wavelength",
        "Difference?",
        "The thermal de Broglie wavelength uses the thermal momentum sqrt(mkT), characterizing the ensemble-averaged wave nature.",
        "When does condensation occur?",
        "BEC occurs when lambda_th is comparable to the interparticle spacing, e.g. alkali atoms cooled to nK.",
        "How to use Find Thermal de Broglie Wavelength from Temperature and Mass",
        "What does finding the thermal de Broglie wavelength from temperature and mass do?",
        "Enter particle mass m and temperature T; the tool computes the thermal de Broglie wavelength by lambda = h/sqrt(2 pi m k T), used to judge under what conditions a gas shows quantum degeneracy (wavelength comparable to spacing), applicable to Bose-Einstein condensation analysis.",
        "How do I use Find Thermal de Broglie Wavelength from Temperature and Mass?",
        "In what scenarios is finding the thermal de Broglie wavelength from temperature and mass useful?",
        "Thermal de Broglie wavelength lambda_db = h/sqrt(2 pi m k_B T): the characteristic wavelength of a particle's wave nature at temperature T.",
        "Quantum degeneracy appears when interparticle spacing approaches lambda_db (e.g. Bose-Einstein condensation, Fermi gas); at room temperature heavy particles have tiny lambda_db and the classical approximation holds.",
    ]))

if __name__ == '__main__':
    main()

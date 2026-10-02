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
    write('heisenberg-uncertainty', build('heisenberg-uncertainty', [
        "Lower bound on the product of position and momentum uncertainties.",
        "Heisenberg Uncertainty Calculator",
        "/ Heisenberg Uncertainty",
        "Heisenberg uncertainty",
        "📖 View \">= hbar / 2 - User Guide\"",
        "Heisenberg uncertainty principle: Delta x x Delta p is no lower than hbar / 2, where the reduced Planck constant hbar = h / 2pi = 1.0546 x 10^-34 J s; the equivalent form is Delta E x Delta t no lower than hbar / 2 (energy and time); for an electron, if the position uncertainty is 1 x 10^-10 m, the momentum uncertainty is no lower than 5.27 x 10^-25 kg m/s and the velocity uncertainty about 5.8 x 10^5 m/s; the smaller the uncertainty of one quantity, the larger the lower bound of the other, forming a measurement limit.",
        "Position uncertainty Delta x (m)",
        "📚 In-depth: Heisenberg Uncertainty Relation",
        "Position-momentum uncertainty lower bound.",
        "Estimate quantum-limit resolution.",
        "Momentum broadening of a trapped particle.",
        "Position uncertainty 0.1 nm",
        "Constrain to 1 pm",
        "Delta p increases 100x = 5.27e-23; the more precisely position is known, the more uncertain momentum is.",
        "Can both be measured precisely at the same time?",
        "No; Delta x Delta p >= hbar/2 is an intrinsic limit, not an instrument-precision issue.",
        "Relation with energy-time",
        "Both are uncertainty relations but with different variables (position-momentum vs energy-time).",
    ]))
    write('hydrogen-energy-level', build('hydrogen-energy-level', [
        "Energy of the nth level of hydrogen.",
        "Hydrogen Energy Level Calculator",
        "/ Hydrogen Energy Level",
        "Hydrogen energy level",
        "📖 View \"Hydrogen Energy Level Calculator - User Guide\"",
        "Ground state n=1 -> -13.6 eV.",
        "📚 In-depth: Hydrogen Energy Level",
        "Energy of each hydrogen shell.",
        "Compute spectral-line energy differences.",
        "Determine ionization energy.",
        "E_n = -13.6/n^2 = -13.6/4 = -3.4 eV; n=1 is -13.6 eV (ionization needs 13.6 eV).",
        "n=3->2 transition",
        "Delta E = -3.4 - (-1.51) = -1.89 eV, emitting a 1.89 eV photon (corresponding to 656 nm red light).",
        "Why are energy levels negative?",
        "Taking infinity as 0, bound-state energy is negative; n->infinity approaches 0 (free electron).",
        "How to modify for hydrogen-like ions?",
        "E_n = -13.6 Z^2/n^2; larger nuclear charge Z makes the energy more negative.",
    ]))
    write('infinite-well-energy', build('infinite-well-energy', [
        "Energy levels of a particle in a 1D potential well.",
        "Infinite Square Well Energy Calculator",
        "/ 1D Infinite Square Well",
        "1D infinite square well",
        "📖 View \"Infinite Square Well Energy Calculator - User Guide\"",
        "E_n = n^2 h^2/(8mL^2). Electron in 1 nm well ground state approx 0.376 eV.",
        "Particle mass m (kg)",
        "Well width L (m)",
        "Electron 1 nm well ground state approx 0.376 eV.",
        "📚 In-depth: 1D Infinite Square Well Energy",
        "Quantum-dot / nano-confinement energy levels.",
        "Estimate particle confinement energy.",
        "Effect of well size on ground-state energy.",
        "Electron confined to 1 nm",
        "E_1 = h^2/(8mL^2) = 6.626e-34^2/(8 x 9.11e-31 x 1e-18) = 0.376 eV; n=2 is 4x = 1.50 eV.",
        "Confinement 0.5 nm",
        "E_1 prop 1/L^2 increases 4x = 1.50 eV; narrower well gives higher levels.",
        "Is E_n proportional to n^2?",
        "Yes; E_n = n^2 E_1, level spacing grows with n.",
        "Relation with well width?",
        "E_1 prop 1/L^2; confinement effects are significant at the nanometer scale.",
    ]))
    write('mass-energy-equivalence', build('mass-energy-equivalence', [
        "Mass-Energy Equivalence Calculator",
        "Energy corresponding to mass.",
        "/ Mass-Energy Equivalence",
        "Mass-energy equivalence",
        "📖 View \"Mass-Energy Equivalence Calculator - User Guide\"",
        "Mass-energy relation E = m x c^2, where c = 2.99792458 x 10^8 m/s, c^2 approx 8.9875 x 10^16 m^2/s^2; 1 g mass corresponds to about 8.99 x 10^13 J (about 2.15 x 10^13 cal, equivalent to about 25000 tons of TNT); 1 u mass defect corresponds to 931.494 MeV; inversely mass from energy m = E / c^2, unit conversion 1 eV = 1.602 x 10^-19 J.",
        "1 kg corresponds to 9e16 J.",
        "📚 In-depth: Mass-Energy Equivalence",
        "Total energy corresponding to mass.",
        "Estimate energy release in nuclear reactions.",
        "Energy scale of annihilation / fission.",
        "1 kg of matter",
        "E = mc^2 = 1 x (2.998e8)^2 = 8.99e16 J (about 2.5 x 10^10 kWh).",
        "1 g mass",
        "E = 0.001 x 8.99e16 = 8.99e13 J, equivalent to about 215000 tons of TNT.",
        "Why is c^2 so huge?",
        "The square of the speed of light is about 9e16, so even tiny mass contains enormous energy.",
        "Why does nuclear fission release energy?",
        "After fission the total rest mass of the products is slightly reduced, and the difference is converted to kinetic energy by Delta E = Delta m c^2.",
        "How to use the Mass-Energy Equivalence Calculator",
        "What does the Mass-Energy Equivalence Calculator do?",
        "An online calculator for mass-energy equivalence (E=mc^2); enter mass to get the corresponding energy, or inversely enter energy to get mass; used for nuclear physics and relativity teaching; pure front-end.",
        "How do I use the Mass-Energy Equivalence Calculator?",
        "In what scenarios is the Mass-Energy Equivalence Calculator useful?",
        "Mass-energy equivalence E = m c^2: energy corresponding to mass m, c approx 2.998 x 10^8 m/s is the speed of light. Mass is a form of energy.",
        "Order of magnitude",
        "1 kg mass corresponds to about 9 x 10^16 J (90 petajoules). In nuclear reactions and matter-antimatter annihilation, the mass difference is converted to energy.",
    ]))
    write('pair-production-threshold', build('pair-production-threshold', [
        "Minimum photon energy required to produce an electron-positron pair.",
        "Pair Production Threshold Calculator",
        "/ Pair Production Threshold",
        "Pair production threshold",
        "📖 View \"Pair Production Threshold Calculator - User Guide\"",
        "Requires >= the sum of the rest energies of the two electrons.",
        "📚 In-depth: Pair Production Threshold",
        "Minimum energy for a gamma photon to produce e+ e-.",
        "Threshold determination in high-energy physics.",
        "Lower energy limit of a detector.",
        "Threshold energy",
        "Where the excess energy goes",
        "The part above 1.022 MeV is converted to kinetic energy of the positron/electron and the recoil nucleus.",
        "Why twice the rest energy?",
        "An electron and a positron must be created simultaneously, each with rest energy 0.511 MeV.",
        "Must it be near a nuclear field?",
        "Yes; in vacuum a third body (nucleus) is needed to conserve momentum, otherwise it cannot occur.",
    ]))

if __name__ == '__main__':
    main()

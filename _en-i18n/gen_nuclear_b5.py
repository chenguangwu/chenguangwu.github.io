#!/usr/bin/env python3
# gen_nuclear_b5.py — nuclear b5 (5 slugs): nuclear-radius/pair-annihilation/q-value/radioactive-decay/reaction-rate
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'nuclear')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'nuclear')

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
    out = {'slug': slug, 'industry': 'nuclear', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

NRD = [
 "Find the nuclear radius from the mass number",
 "Enter the mass number A to get the nuclear radius (r₀ = 1.2 fm).",
 "Nuclear Radius Calculator",
 "/ Nuclear Radius Calculator",
 "📖 View Guide: \"Find the nuclear radius from the mass number\"",
 "Mass number A",
 "Fe-56 gives about 4.59 fm.",
 "📚 Deep Dive: Nuclear radius (R = r₀·A^(1/3))",
 "R = r₀·A^(1/3) with r₀ ≈ 1.2 fm gives the nuclear radius from the mass number A.",
 "Estimating nuclear density and reaction cross-sections.",
 "Compare nuclear sizes for different A.",
 "Heavy nuclei",
 "For A = 208 (Pb), R ≈ 1.2e-15 x 5.92 ≈ 7.1 fm; the nuclear size grows slowly with the cube root of A.",
 "Is the nuclear volume proportional to A?",
 "Yes. Since R ∝ A^(1/3) the volume is proportional to A and the nuclear density is nearly constant, which underlies the liquid drop model.",
 "Is r₀ a fixed value?",
 "About 1.2 fm, with slight differences between fits such as charge radius and matter radius.",
]

PAN = [
 "Electron pair annihilation produces two 511 keV photons.",
 "Electron Annihilation Photon Energy Calculator",
 "/ Electron-Positron Annihilation",
 "Electron-Positron Annihilation",
 "📖 View Guide: \"Electron Annihilation Photon Energy Calculator\"",
 "Each photon carries 511 keV.",
 "Both photons carry 511 keV each.",
 "📚 Deep Dive: Electron pair annihilation energy",
 "e⁺e⁻ annihilation releases photons of E = mₑc² ≈ 511 keV each.",
 "The principle of positron emission tomography (PET).",
 "Compare the annihilation energy of different particles.",
 "Electron rest energy",
 "E = mₑc² / e / 1000 = 511 keV; electron-positron annihilation produces two back-to-back 511 keV gamma photons.",
 "Energy conservation",
 "The total rest energy of 2 x 511 = 1022 keV turns into two photons of 511 keV each, emitted back to back so momentum is conserved.",
 "Why two photons?",
 "A single photon cannot conserve energy and momentum at the same time, while two photons emitted back to back satisfy both.",
 "Where does 511 keV come from?",
 "The electron rest mass of 9.11e-31 kg multiplied by c² gives about 8.19e-14 J, which converts to 511 keV.",
]

QVL = [
 "The energy released corresponding to the mass difference before and after a reaction.",
 "Nuclear Reaction Q-Value Calculator",
 "/ Nuclear Reaction Q-Value",
 "Nuclear Reaction Q-Value",
 "📖 View Guide: \"Nuclear Reaction Q-Value Calculator\"",
 "Initial total mass m_i (u)",
 "Final total mass m_f (u)",
 "Q > 0 releases energy and Q < 0 absorbs it.",
 "Unit conversion: 1 u ≈ 931.5 MeV.",
 "📚 Deep Dive: Nuclear reaction Q-value",
 "Q = (mᵢ - m_f)·c² gives the energy released from the initial to final mass difference.",
 "Judge whether a nuclear reaction absorbs or releases energy.",
 "Compare the mass differences of different reactions.",
 "Q = (4.0026 - 4.0015) x 931.5 ≈ 0.0011 x 931.5 ≈ 1.02 MeV, so the reaction releases energy.",
 "Endothermic reaction",
 "If m_f > m_i then Q is negative and outside energy, the threshold energy, is needed for the reaction to occur.",
 "Does Q > 0 guarantee the reaction happens?",
 "Not necessarily; the reaction must also satisfy",
 "angular momentum",
 ", parity and the Coulomb barrier, since Q only judges the energy balance.",
 "What about the 931.5 factor?",
 "1 u·c² ≈ 931.5 MeV converts a mass difference in atomic mass units into MeV.",
]

RDC = [
 "The number of nuclei as it falls with time.",
 "Radioactive Decay Calculator",
 "/ Radioactive Decay",
 "Radioactive Decay",
 "📖 View Guide: \"Radioactive Decay Calculator\"",
 "N = N₀e^(-λt). About 50% remains after one half-life.",
 "About 50% remains after one half-life.",
 "📚 Deep Dive: Radioactive decay (N = N₀e^(-λt))",
 "The surviving number N = N₀e^(-λt) decays exponentially with time.",
 "Decay counting and inventory estimation.",
 "Compare the remaining nuclei for different λ and t.",
 "N = 1000 x e^(-1) ≈ 367.9 nuclei, i.e. after about one",
 "mean life",
 "36.8% remains.",
 "One",
 "if t = ln2/λ = 693, then N = 500, exactly half.",
 "Relation between N and the activity A?",
 "A = λN, so fewer nuclei means lower activity; both decay as the same exponential.",
 "Why exponential?",
 "Each nucleus has a constant and independent decay probability, so the decays per unit time are proportional to the number present, which solves to an exponential.",
]

RRT = [
 "Find the reaction rate from neutron flux, cross-section and target nuclei",
 "Enter the neutron flux Φ, the microscopic cross-section σ and the number of target nuclei N to get the reaction rate.",
 "Nuclear Reaction Rate Calculator",
 "/ Nuclear Reaction Rate Calculator",
 "📖 View Guide: \"Find the reaction rate from neutron flux, cross-section and target nuclei\"",
 "R = ΦσN. The example gives 1×10⁵ /s.",
 "Flux Φ (1/(m²·s))",
 "Cross-section σ (m²)",
 "Number of target nuclei N",
 "The example gives 1×10⁵ /s.",
 "📚 Deep Dive: Nuclear reaction rate (R = ΦσN)",
 "R = flux Φ x cross-section σ x number of target nuclei N gives the reaction rate.",
 "Reactor and activation analysis calculations.",
 "Compare rates for different fluxes and cross-sections.",
 "R = 1e13 x 1e-28 x 1e20 = 1×10⁵ s⁻¹; a tenfold flux gives a tenfold rate.",
 "Large cross-section nuclei",
 "If σ = 1e-24, the barn scale, then R = 1e9 s⁻¹ and the reaction is greatly enhanced.",
 "What is the unit of σ?",
 "Usually the barn, where 1 barn = 1e-28 m², which expresses the effective area for a reaction between the nucleus and an incoming particle.",
 "What is the flux Φ?",
 "The number of incident particles per unit time per unit area, in particles·m⁻²·s⁻¹, which sets the collision frequency.",
]

write('nuclear-radius', build('nuclear-radius', NRD))
write('pair-annihilation', build('pair-annihilation', PAN))
write('q-value', build('q-value', QVL))
write('radioactive-decay', build('radioactive-decay', RDC))
write('reaction-rate', build('reaction-rate', RRT))

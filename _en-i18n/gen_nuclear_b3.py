#!/usr/bin/env python3
# gen_nuclear_b3.py — nuclear b3 (5 slugs): decay-fraction/dose-equivalent/effective-halflife/fission-energy-yield/gamma-attenuation
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

DFR = [
 "Find the decayed fraction from the decay constant and time",
 "Enter the decay constant λ and the time t to get the decayed fraction.",
 "Decayed Fraction Calculator",
 "/ Decayed Fraction Calculator",
 "📖 View Guide: \"Find the decayed fraction from the decay constant and time\"",
 "Decayed fraction = 1 - e^(-λt)",
 "📚 Deep Dive: Decayed fraction (1 - e^(-λt))",
 "f = 1 - e^(-λt) gives the proportion already decayed after time t.",
 "Design of irradiation and storage times.",
 "Compare the extent of decay for different λt.",
 "f = 1 - e^(-1) = 1 - 0.3679 = 0.6321, i.e. about 63.2% has decayed.",
 "One",
 "mean life",
 "when t = 1/λ, f = 1 - e⁻¹ ≈ 63.2%, so about two thirds decay within one mean life.",
 "Relation between decayed fraction and survival probability?",
 "Survival probability P = e^(-λt) and decayed fraction f = 1 - P are complementary; see survival-probability.",
 "What does λt = 1 mean?",
 "About 63.2% has then decayed, a common reference point when discussing decay rates.",
]

DQE = [
 "Find the dose equivalent from absorbed dose and quality factor",
 "Enter the absorbed dose D and the radiation weighting factor Q to get the dose equivalent.",
 "Dose Equivalent Calculator",
 "/ Dose Equivalent Calculator",
 "📖 View Guide: \"Find the dose equivalent from absorbed dose and quality factor\"",
 "Absorbed dose D (Gy)",
 "Weighting factor Q",
 "H = D·Q; for alpha particles Q = 20.",
 "📚 Deep Dive: Equivalent dose (H = D·Q)",
 "The absorbed dose",
 "D times the radiation weighting factor Q gives the equivalent dose (Sv).",
 "Compare the harm of different radiation types (alpha has a high Q).",
 "Radiation protection dose assessment.",
 "D = 2 Gy, Q = 20 (alpha particles)",
 "Equivalent dose H = 2 x 20 = 40 Sv; the same D with gamma (Q=1) gives only 2 Sv.",
 "Weighting difference",
 "Q reaches 20 for alpha but is mostly 1 for beta and gamma, so at equal absorbed dose alpha is about 20 times more harmful.",
 "Relation between Sv and Gy?",
 "Sv = Gy x Q; the values are equal for gamma and beta (Q=1), while alpha is far more harmful because of its high Q.",
 "How is Q chosen?",
 "It depends on the radiation type and energy: about 20 for alpha and about 1 for beta and gamma, with exact values taken from protection standards.",
]

EFL = [
 "Find the effective half-life from the physical and biological half-lives",
 "Enter the physical half-life t_phys and the biological half-life t_bio to get the effective half-life.",
 "Effective Half-Life Calculator",
 "/ Effective Half-Life Calculator",
 "📖 View Guide: \"Find the effective half-life from the physical and biological half-lives\"",
 "Physical half-life t_phys (days)",
 "Biological half-life t_bio (days)",
 "8 days and 30 days give about 6.32 days.",
 "📚 Deep Dive: Effective half-life",
 "te = 1/(1/tp + 1/tb) combines physical decay with biological elimination.",
 "Estimate how long radionuclides stay in the body.",
 "Compare the effect of different biological half-times.",
 "Physical tp = 8 years, biological tb = 30 years",
 "te = 1/(1/8 + 1/30) = 1/(0.125 + 0.0333) = 1/0.1583 ≈ 6.32 years.",
 "Fast biological elimination",
 "If tb = 2 years, then te = 1/(0.125 + 0.5) = 1.6 years; fast biological elimination accelerates overall clearance.",
 "Is the effective",
 "half-life always shorter?",
 "Yes. The physical and biological clearance routes add together, so te is smaller than the lesser of tp and tb.",
 "What is the biological half-time?",
 "The time for metabolism and excretion to halve the amount of nuclide, acting at the same time as",
 "radioactive decay",
 "in the body.",
 "How to use Find the Effective Half-Life from Physical and Biological Half-Lives",
 "What is Find the Effective Half-Life from Physical and Biological Half-Lives for?",
 "How do I use Find the Effective Half-Life from Physical and Biological Half-Lives?",
 "Which scenarios suit Find the Effective Half-Life from Physical and Biological Half-Lives?",
 "Effective half-life T_e: a radionuclide in the body is cleared by physical decay and biological excretion at the same time, so 1/T_e = 1/T_p + 1/T_b, where T_p is the physical half-life and T_b the biological half-life.",
 "In nuclear medicine it estimates how long radioactivity remains in the body, for dose and protection planning; T_e is always smaller than the lesser of T_p and T_b.",
]

FEY = [
 "Nuclear Fission Total Energy Yield Calculator",
 "Find the total energy from the number of fissioned atoms and the energy released per fission.",
 "/ Fission Energy Yield",
 "Fission Energy Yield",
 "📖 View Guide: \"Nuclear Fission Total Energy Yield Calculator\"",
 "Total energy E = N x E_f; a single uranium-235 fission releases about 200 MeV (about 3.2 × 10⁻¹¹ J); 1 kg of uranium-235 contains about 2.56 × 10²⁴ nuclei, so complete fission yields about 8.2 × 10¹³ J, equivalent to roughly 2000 tonnes of standard coal. Each fission also releases 2 to 3 neutrons, with the energy split into about 168 MeV of fragment kinetic energy, about 5 MeV carried by neutrons and about 7 to 15 MeV of gamma rays; nuclear fuel has an energy density about 10⁶ times that of fossil fuels.",
 "Number of fissioned atoms N",
 "Energy per fission E_f (MeV)",
 "Each U-235 fission releases about 200 MeV.",
 "1 g of uranium-235 releases an enormous amount of energy.",
 "📚 Deep Dive: Fission energy yield",
 "Total energy E = number of fissions x energy released each time (about 200 MeV) x 1e6 x e.",
 "Estimate the energy scale of reactors and nuclear devices.",
 "Compare the total release for different numbers of fissions.",
 "n = 1e20 fissions at 200 MeV each",
 "1 mole of uranium",
 "About 6.02e23 fissions x 200 MeV ≈ 1.93×10¹³ J, roughly several hundred tonnes of TNT.",
 "How much energy per fission?",
 "Typically about 200 MeV, including kinetic energy, gamma rays and neutrons; this tool uses that empirical value.",
 "How does it relate to the",
 "mass defect?",
 "Each fission loses about 0.2 u of mass, corresponding to roughly 200 MeV, consistent with the binding energy curve.",
]

GAT = [
 "Find the transmitted intensity from the linear attenuation coefficient and thickness",
 "Enter the initial intensity I₀, the attenuation coefficient μ and the thickness x to get the transmitted intensity.",
 "Gamma Ray Attenuation Calculator",
 "/ Gamma Ray Attenuation Calculator",
 "📖 View Guide: \"Find the transmitted intensity from the linear attenuation coefficient and thickness\"",
 "Initial intensity I₀",
 "Attenuation coefficient μ (1/cm)",
 "Thickness x (cm)",
 "📚 Deep Dive: Exponential attenuation of gamma rays",
 "I = I₀·e^(-μx) is the intensity remaining after a shield of thickness x.",
 "Lead and",
 "concrete shielding design.",
 "Compare the effect of different linear attenuation coefficients μ.",
 "Doubling the thickness",
 "If x = 10 cm, then I = 100 x e⁻¹ ≈ 36.79; doubling the thickness drops the intensity to about 37%.",
 "What is μ?",
 "The linear attenuation coefficient in cm⁻¹, which depends on the material and the ray energy; a larger value means stronger shielding.",
 "How is the half-value layer computed?",
 "The half-value layer is x₁/₂ = ln2/μ, about 6.93 cm when μ = 0.1 as in this example.",
]

write('decay-fraction', build('decay-fraction', DFR))
write('dose-equivalent', build('dose-equivalent', DQE))
write('effective-halflife', build('effective-halflife', EFL))
write('fission-energy-yield', build('fission-energy-yield', FEY))
write('gamma-attenuation', build('gamma-attenuation', GAT))

#!/usr/bin/env python3
# gen_nuclear_b4.py — nuclear b4 (5 slugs): half-life-from-activity-nuclei/half-life-from-lambda/mass-defect/mean-life-from-halflife/mean-life
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

HAN = [
 "Back out the half-life from the number of nuclei and the activity",
 "Enter the number of nuclei N and the activity A to get the half-life.",
 "Half-Life from Activity and Number of Nuclei",
 "/ Half-Life from Activity and Number of Nuclei",
 "📖 View Guide: \"Back out the half-life from the number of nuclei and the activity\"",
 "Activity A (Bq)",
 "The example gives about 5730 years.",
 "📚 Deep Dive: Half-life from activity and number of nuclei",
 "Experimental determination of an isotope half-life",
 "Compare th across different activities.",
 "th = 1e20 x 0.693147 / 3.833e8 ≈ 1.808×10¹¹ s ≈ 5730 years, that is C-14.",
 "Higher activity",
 "If A = 7.666e8, th halves to 9.04e10 s, meaning faster decay.",
 "Where does the formula come from?",
 "Eliminating λ between A = λN and λ = ln2/th gives th = N·ln2/A.",
 "Is a closed system required?",
 "The measurement assumes the number of nuclei falls only through decay, with no other source or sink; otherwise a correction is needed.",
]

HLB = [
 "Find the half-life from the decay constant.",
 "Half-Life Calculator",
 "/ Half-Life (from Decay Constant)",
 "Half-Life (from Decay Constant)",
 "📖 View Guide: \"Half-Life Calculator\"",
 "It is the reciprocal style relation with the decay constant.",
 "📚 Deep Dive: Half-life from the decay constant",
 "th = ln2/λ uses the",
 "decay constant",
 "to back out the half-life.",
 "Find the characteristic time from a known λ.",
 "Compare th for different λ.",
 "th = 0.693147 / 1.21e-4 ≈ 5.73×10³ years ≈ 5730 years for C-14.",
 "Increasing λ",
 "If λ = 1.21e-3, then th ≈ 573 years, ten times shorter.",
 "Are th and λ reciprocals?",
 "Not directly: th = ln2/λ, so they differ by the factor ln2.",
 "Must the units match?",
 "A λ in yr⁻¹ gives th in years and a λ in s⁻¹ gives th in seconds, so the units must agree.",
]

MDF = [
 "The difference between the sum of the nucleon masses and the nuclear mass.",
 "Mass Defect Calculator",
 "/ Mass Defect",
 "Mass Defect",
 "📖 View Guide: \"Mass Defect Calculator\"",
 "Δm = Zm_p + Nm_n - M. For iron-56: Z=26, N=30.",
 "Proton number Z",
 "Neutron number N",
 "Nuclear mass M (u)",
 "For iron-56: Z=26, N=30.",
 "📚 Deep Dive: Mass defect (Δm = Z·mp + N·mn - M)",
 "The total mass of the constituent nucleons minus the measured nuclear mass gives the mass defect.",
 "A prerequisite for binding energy calculations.",
 "Compare Δm across different nuclei.",
 "Δm = (26 x 1.6726e-27 + 30 x 1.6749e-27 - 55.9349 x 1.6605e-27) / 1.6605e-27 ≈ 0.52 u, corresponding to a binding energy of about 491 MeV.",
 "More nucleons",
 "Δm grows with the nucleon number, but the",
 "specific binding energy",
 "(Δm/A) peaks near iron.",
 "Should M be the atomic or the nuclear mass?",
 "Use the nuclear mass; if you use the atomic mass you must subtract the electron masses, and this tool works on the nuclear mass basis.",
 "Where does the mass defect go?",
 "It is released as binding energy (ΔE = Δm·c²), leaving the nucleus lighter than the free nucleons.",
 "How to use the Mass Defect Calculator",
 "What is the Mass Defect Calculator for?",
 "The Mass Defect Calculator finds the difference between the sum of the nucleon masses in a nucleus and the actual nuclear mass; that difference corresponds to the binding energy, which suits the study of mass-energy relations in nuclear physics.",
 "How do I use the Mass Defect Calculator?",
 "Which scenarios suit the Mass Defect Calculator?",
]

MLF = [
 "Find the mean life from the half-life",
 "Enter the half-life t½ in years to get the mean life.",
 "📖 View Guide: \"Find the mean life from the half-life\"",
 "Half-life t½ (years)",
 "C-14 gives about 8267 years.",
 "📚 Deep Dive: Mean life (τ = th/ln2)",
 "mean life:",
 "divide by ln2.",
 "A characteristic parameter of decay statistics.",
 "Compare the mean life for different th.",
 "th = 5730 years",
 "τ = 5730 / 0.693147 ≈ 8267 years, about 44% longer than the half-life.",
 "Short-lived",
 "If th = 1 day, then τ ≈ 1.44 days.",
 "Relation between mean life and half-life?",
 "τ = th/ln2 ≈ 1.4427·th; the mean life is the average survival time of a nucleus before it decays.",
 "Why is τ larger than th?",
 "Because the",
 "exponential distribution",
 "has a long tail, so the average survival time exceeds the time needed for half to decay.",
]

MNL = [
 "The average survival time of a radionuclide.",
 "Mean Life Calculator",
 "/ Mean Life",
 "Mean Life",
 "📖 View Guide: \"Mean Life Calculator\"",
 "📚 Deep Dive: Mean life (τ = th/ln2)",
 "From the",
 "half-life th, find the mean life τ.",
 "Decay follows an",
 "exponential distribution",
 ", whose characteristic time this is.",
 "Used for the survival probability e^(-t/τ).",
 "th = 5730 years",
 "τ = 5730 / 0.693147 ≈ 8267 years, at which point the survival probability is e^(-1) ≈ 36.8% (see survival-probability).",
 "Physical meaning of τ",
 "At any moment a surviving nucleus lasts on average another τ, which is the reciprocal of the",
 "decay constant",
 "(τ = 1/λ).",
 "Relation between τ and λ?",
 "τ = 1/λ = th/ln2, three equivalent ways to describe how fast the decay is.",
 "Can the mean life be measured directly?",
 "It is derived from th or λ, being a statistical average rather than the exact lifetime of any single nucleus.",
]

write('half-life-from-activity-nuclei', build('half-life-from-activity-nuclei', HAN))
write('half-life-from-lambda', build('half-life-from-lambda', HLB))
write('mass-defect', build('mass-defect', MDF))
write('mean-life-from-halflife', build('mean-life-from-halflife', MLF))
write('mean-life', build('mean-life', MNL))

#!/usr/bin/env python3
# gen_nuclear_b2.py — nuclear b2 (5 slugs): binding-energy-per-nucleon/binding-energy/carbon-dating-age/decay-constant-from-halflife/decay-constant
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

BEP = [
 "Specific Binding Energy Calculator",
 "The average binding energy per nucleon, which reflects nuclear stability.",
 "/ Specific Binding Energy",
 "Specific Binding Energy",
 "📖 View Guide: \"Specific Binding Energy Calculator\"",
 "Specific binding energy = binding energy / mass number A; binding energy BE = Δm x c², where the mass defect Δm = Z x proton mass + N x neutron mass - nuclear mass, with c² taken as 931.5 MeV/u (1 u equals 931.494 MeV), i.e. BE(MeV) = Δm(u) x 931.5. The specific binding energy curve peaks near A about 56 (the iron peak) at roughly 8.8 MeV/nucleon, the most stable region; fusion of light nuclei and fission of heavy nuclei both move toward the iron peak and release energy.",
 "Nucleon number A",
 "The iron peak is about 8.8 MeV/nucleon.",
 "A larger specific binding energy means greater stability.",
 "📚 Deep Dive: Specific binding energy",
 "Total binding energy divided by the number of nucleons gives the binding energy per nucleon (MeV/nucleon).",
 "How nuclear stability relates to nucleon number (the iron peak).",
 "Compare the specific binding energy of light and heavy nuclei.",
 "Mass defect",
 "Total binding energy = 0.528 x 931.5 ≈ 491.8 MeV; specific binding energy = 491.8 / 56 ≈ 8.78 MeV/nucleon, close to the peak and hence most stable.",
 "Light nucleus comparison",
 "For A=4 (He-4) the specific binding energy is about 7.07 MeV/nucleon, below iron, so fusion releases energy.",
 "Where is the maximum of the specific binding energy?",
 "Near iron-56, at about 8.8 MeV/nucleon, is the peak and the most stable region for nuclei.",
 "What is 931.5?",
 "The energy in MeV corresponding to 1 u (1 u·c² ≈ 931.5 MeV), used to turn a mass defect into binding energy.",
]

BIN = [
 "Nuclear Binding Energy Calculator",
 "The energy released when nucleons are bound into a nucleus.",
 "/ Binding Energy",
 "Binding Energy",
 "📖 View Guide: \"Nuclear Binding Energy Calculator\"",
 "Binding energy BE = Δm x c²; the mass defect Δm = (Z x m_proton + N x m_neutron) - m_nucleus, where Z is the proton number, N the neutron number and A = Z + N. Since tables usually give atomic masses, the hydrogen atom mass replaces the proton mass in practice, i.e. Δm = Z x m_H + N x m_neutron - m_atom. With 1 u = 931.494 MeV/c², BE(MeV) = Δm(u) x 931.494; a larger binding energy means the nucleons are bound more tightly.",
 "The total binding energy of iron-56 is about 492 MeV.",
 "📚 Deep Dive: Nuclear binding energy",
 "The mass defect",
 "Δm converts into the total binding energy BE = Δm·c².",
 "Assess nuclear stability and released energy.",
 "Compare the total binding energy of different nuclei.",
 "Mass defect 0.528 u",
 "Total binding energy BE = 0.528 x 1.492×10⁻¹⁰ J ≈ 7.88×10⁻¹¹ J, or 0.528 x 931.5 ≈ 491.8 MeV.",
 "1 MeV = 1.602×10⁻¹³ J, so 491.8 MeV ≈ 7.88×10⁻¹¹ J.",
 "Does a larger binding energy mean more stability?",
 "Total binding energy grows with the nucleon number, so stability must be judged by the",
 "specific binding energy",
 "(per nucleon), see binding-energy-per-nucleon.",
 "Where does the mass defect come from?",
 "The total rest mass of the nucleons in a nucleus exceeds the actual mass of the nucleus, and that difference is the mass equivalent of the binding energy.",
]

CDA = [
 "Infer the age of a sample from the remaining carbon-14 fraction.",
 "Carbon-14 Dating Calculator",
 "/ Carbon-14 Dating",
 "Carbon-14 Dating",
 "📖 View Guide: \"Carbon-14 Dating Calculator\"",
 "t = T½/ln2 · ln(N₀/N). A remaining 50% means one half-life.",
 "A remaining 50% means one half-life.",
 "📚 Deep Dive: Carbon-14 dating",
 "t = (th/ln2)·ln(1/frac) gives the sample age from the remaining fraction.",
 "Dating in archaeology and paleontology.",
 "Compare ages for different remaining fractions.",
 "th=5730 years, remaining frac=0.5",
 "t = (5730/0.693) x ln(1/0.5) ≈ 8267 x 0.693 ≈ 5730 years, i.e. after one",
 "25% remaining",
 "If frac=0.25, then t ≈ 8267 x ln(4) = 8267 x 1.386 ≈ 11460 years, two half-lives.",
 "What is the upper limit?",
 "With a C-14 half-life of 5730 years, effective dating usually reaches about 50 000 years; beyond that the signal is too weak.",
 "How is frac measured?",
 "Measure the ratio of the sample's current C-14 activity to the initial atmospheric activity to get the remaining fraction.",
]

DCF = [
 "Find the decay constant from the half-life",
 "Enter the half-life t½ (in seconds) to get the decay constant.",
 "📖 View Guide: \"Find the decay constant from the half-life\"",
 "📚 Deep Dive: Finding the decay constant from the half-life",
 "λ = ln2/th takes the",
 " and returns the",
 "decay constant",
 "Compute constants such as C-14 (th = 5730 years).",
 "Compare λ across different lifetimes.",
 "th = 1.808e11 s (about 5730 years)",
 "Short-lived",
 "If th = 1 day ≈ 8.64e4 s, then λ ≈ 8.02×10⁻⁶ s⁻¹; the shorter the life, the larger λ.",
 "Is λ inversely proportional to th?",
 "Yes. λ = ln2/th, so a longer half-life means slower decay and a smaller λ.",
 "Units?",
 "λ is in s⁻¹ (or yr⁻¹ depending on the unit of th) and expresses the decay probability per unit time.",
]

DCN = [
 "Find the decay constant from the half-life.",
 "Decay Constant Calculator",
 "/ Decay Constant",
 "Decay Constant",
 "📖 View Guide: \"Decay Constant Calculator\"",
 "Carbon-14 has a half-life of 5730 years.",
 "📚 Deep Dive: Decay constant (λ = ln2/th)",
 "From the",
 "half-life th, find the decay constant λ.",
 "Radioactive decay",
 "rate parameter calculation.",
 "Used for downstream calculations of activity and age.",
 "th = 5730 years",
 "λ = 0.693147 / 5730 ≈ 1.210×10⁻⁴ yr⁻¹; in seconds λ ≈ 3.834×10⁻¹² s⁻¹.",
 "Doubling the half-life",
 "If th = 11460 years, λ halves to 6.05×10⁻⁵ yr⁻¹.",
 "How do yearly and per-second λ convert?",
 "They differ by a factor of 365.25 x 24 x 3600; only the time unit changes, the physical quantity is the same.",
 "Can λ exceed 1?",
 "Yes. For extremely short lives such as the microsecond scale λ is large, meaning very fast decay.",
]

write('binding-energy-per-nucleon', build('binding-energy-per-nucleon', BEP))
write('binding-energy', build('binding-energy', BIN))
write('carbon-dating-age', build('carbon-dating-age', CDA))
write('decay-constant-from-halflife', build('decay-constant-from-halflife', DCF))
write('decay-constant', build('decay-constant', DCN))

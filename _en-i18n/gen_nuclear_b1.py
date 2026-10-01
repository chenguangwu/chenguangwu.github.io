#!/usr/bin/env python3
# gen_nuclear_b1.py — nuclear b1 (5 slugs): absorbed-dose/activity-decay/activity-from-halflife/activity/age-from-activity
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

ABD = [
 "Find the absorbed dose from deposited energy and mass",
 "Enter the deposited energy E and the mass m to get the absorbed dose.",
 "Absorbed Dose Calculator",
 "/ Absorbed Dose Calculator",
 "📖 View Guide: \"Find the absorbed dose from deposited energy and mass\"",
 "📚 Deep Dive: Absorbed dose (D = E/m)",
 "Divide the deposited radiation energy E by the mass m of the material to get the absorbed dose.",
 "Dose calculation in Gy (J/kg).",
 "Compare dose intensity across different masses.",
 "Absorbed dose D = 0.05 / 1 = 0.05 Gy; if the mass drops to 0.5 kg then D = 0.1 Gy, since the same energy is more concentrated.",
 "Conversion with rad",
 "1 Gy = 100 rad, so 0.05 Gy = 5 rad.",
 "Absorbed dose versus equivalent dose?",
 "Absorbed dose is energy per mass (Gy); the equivalent dose further multiplies by the radiation weighting factor Q (Sv), see dose-equivalent.",
 "Can Gy and Sv be used interchangeably?",
 "No. Gy describes deposited energy and Sv the biological harm equivalent; the values coincide only for γ/β (Q=1).",
]

ACD = [
 "The initial activity decays with time.",
 "Activity Decay Calculator",
 "/ Activity Decay over Time",
 "Activity Decay over Time",
 "📖 View Guide: \"Activity Decay Calculator\"",
 "A = A₀e^(-λt). Activity decays in step with the number of nuclei.",
 "Initial activity A₀ (Bq)",
 "Activity decays in step with the number of nuclei.",
 "📚 Deep Dive: Radioactive activity decay (A = A₀e^(-λt))",
 "Given the initial activity A₀, the",
 "decay constant",
 "λ and the time t, find the current activity.",
 "Compute isotope decay curves.",
 "Compare the remaining activity for different λ and t.",
 "After one",
 "if t = ln2/λ = 693, then A = 100 x e^(-0.693) = 50 Bq, exactly half.",
 "What is the unit of activity?",
 "The becquerel Bq is one decay per second; the older unit is the curie Ci, with 1 Ci = 3.7×10¹⁰ Bq.",
 "How is λ obtained?",
 "From the half-life th, λ = ln2/th; see decay-constant / decay-constant-from-halflife.",
 "How to use the Activity Decay Calculator",
 "What is the Activity Decay Calculator for?",
 "The Activity Decay Calculator applies the radioactive decay law to an initial activity over time; enter the half-life and the elapsed time to get the remaining activity. It suits nuclear physics study and radiation protection estimates.",
 "How do I use the Activity Decay Calculator?",
 "Which scenarios suit the Activity Decay Calculator?",
]

AFH = [
 "Find the activity from the half-life and the number of nuclei",
 "Enter the half-life t½ and the number of nuclei N to get the activity.",
 "Activity from Half-Life and Number of Nuclei",
 "/ Activity from Half-Life and Number of Nuclei",
 "📖 View Guide: \"Find the activity from the half-life and the number of nuclei\"",
 "The example gives 3.83×10⁸ Bq.",
 "📚 Deep Dive: Activity from half-life and number of nuclei",
 "A = (ln2/th) x N gives the activity from the number of nuclei and the",
 "half-life directly.",
 "Estimate the activity of long-lived isotopes such as C-14.",
 "Compare the total activity for different numbers of nuclei.",
 "th=1.808e11 s (about 5730 years), N=1e20",
 "A = (0.693/1.808e11) x 1e20 ≈ 3.83×10⁸ Bq; multiplying the number of nuclei by 10 multiplies the activity by 10.",
 "Short-lived case",
 "If th = 1 day ≈ 8.64e4 s and N = 1e20, then A ≈ 8.02×10¹⁵ Bq, far higher than for a long-lived isotope.",
 "Is this A the total activity of the sample?",
 "Yes, it is the total decay rate for the given number of nuclei N; the",
 "specific activity",
 "needs the mass divisor, see specific-activity.",
 "Why is the activity higher for a short half-life at the same N?",
 "λ is proportional to 1/th: the shorter the life, the faster the decay and the higher the instantaneous activity.",
 "How to use Activity from Half-Life and Number of Nuclei",
 "What is Activity from Half-Life and Number of Nuclei for?",
 "Enter the radionuclide half-life t½ and the number of nuclei N, then compute the decay activity as A = (ln2 / t½)·N in becquerels (Bq). It is used in nuclear physics, source activity estimates and decay calculations.",
 "How do I use Activity from Half-Life and Number of Nuclei?",
 "Which scenarios suit Activity from Half-Life and Number of Nuclei?",
 "Radioactive activity A = λ·N = (ln2/T½)·N is the number of decays per unit time, where λ is the decay constant, N the number of nuclei and T½ the half-life.",
 "A is in becquerels (Bq, one decay per second); medicine commonly uses kilobecquerels (kBq) and megabecquerels (MBq). Activity decays exponentially with time as A(t) = A₀·e^(-λt).",
 "Activity reflects the decay rate rather than the total hazard; radiation safety also depends on the radiation type and energy, so the result is for reference only.",
]

ACT = [
 "Decays per unit time (becquerel).",
 "Radioactivity Calculator",
 "/ Radioactivity",
 "Radioactivity",
 "📖 View Guide: \"Radioactivity Calculator\"",
 "Decay constant λ (s⁻¹)",
 "📚 Deep Dive: Activity (A = λN)",
 "The decay constant",
 "λ times the number of nuclei N gives the activity.",
 "Find the decay rate from λ and the number of nuclei.",
 "Verify A = λN and its",
 "half-life relation.",
 "A = 1e-9 x 1e20 = 1×10¹¹ Bq; raising the number of nuclei to 1e21 gives A = 1e12 Bq.",
 "Conversion with half-life",
 "If th = ln2/λ = 6.93e8 s, then A = (ln2/th) x N is equivalent and gives the same result.",
 "Relation between A = λN and A₀e^(-λt)?",
 "The first is the definition of instantaneous activity and the second its decay over time; they agree at t = 0.",
 "What is the unit of λ?",
 "λ is in s⁻¹ (decay probability per second) and N is the number of nuclei, so A comes out in s⁻¹, i.e. Bq.",
]

AFA = [
 "Find the age from the initial and current activity",
 "Enter the decay constant λ, the initial number of nuclei N₀ and the current number N to get the age.",
 "Radiometric Dating Calculator",
 "/ Radiometric Dating Calculator",
 "📖 View Guide: \"Find the age from the initial and current activity\"",
 "t = (1/λ)·ln(N₀/N). A halving of C-14 gives about 5730 years.",
 "Current number of nuclei N",
 "A halving of C-14 gives about 5730 years.",
 "📚 Deep Dive: Dating from the activity ratio",
 "t = (1/λ)·ln(N₀/N) infers the age from the initial to current ratio of nuclei.",
 "Radiometric dating such as C-14.",
 "Compare ages for different remaining fractions.",
 "t = (1/3.833e-12) x ln(1e20/5e19) ≈ 2.609e11 x 0.693 ≈ 1.808e11 s ≈ 5730 years, exactly one C-14",
 "25% remaining",
 "If N = 2.5e19 (25% left), then t ≈ 2 x 5730 = 11460 years, two half-lives.",
 "Which dating methods does this suit?",
 "Closed systems with known λ and initial amount, such as C-14 whose λ corresponds to a 5730 year half-life.",
 "Why does half remaining equal th?",
 "N/N₀ = e^(-λt) = 0.5 gives t = ln2/λ = th, so the half-life is the time for the activity to halve.",
]

write('absorbed-dose', build('absorbed-dose', ABD))
write('activity-decay', build('activity-decay', ACD))
write('activity-from-halflife', build('activity-from-halflife', AFH))
write('activity', build('activity', ACT))
write('age-from-activity', build('age-from-activity', AFA))

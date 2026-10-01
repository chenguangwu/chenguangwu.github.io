#!/usr/bin/env python3
# gen_nuclear_b6.py — nuclear b6 (3 slugs): specific-activity-from-halflife/specific-activity/survival-probability
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

SAF = [
 "Find the specific activity from the half-life and molar mass",
 "Enter the half-life t½ in seconds and the molar mass M to get the specific activity.",
 "/ Specific Activity Calculator",
 "📖 View Guide: \"Find the specific activity from the half-life and molar mass\"",
 "C-14 gives about 1.65×10¹¹ Bq/g.",
 "📚 Deep Dive: Specific activity from the half-life",
 "Measuring the purity and activity concentration of radioisotopes.",
 "Compare the specific activity of different nuclides.",
 "a = (0.693/1.808e11) x 6.022e23 / 14 ≈ 1.65×10¹¹ Bq at the per gram level;",
 "a shorter half-life gives a higher specific activity.",
 "Shorter half-life is higher",
 "If th drops to 1 day, the specific activity grows by about a factor of 2e7, a huge jump in activity concentration.",
 "What is the unit of specific activity?",
 "Usually Bq/g or Bq/mol; this tool reports the value in the unit matching the supplied M.",
 "How does it differ from activity-from-halflife?",
 "That tool gives the total activity for a given number of nuclei, while this one gives the activity per unit mass, i.e. the specific activity.",
]

SAC = [
 "Radioactivity per unit mass.",
 "/ Specific Activity",
 "Specific Activity",
 "📖 View Guide: \"Specific Activity Calculator\"",
 "a = λN_A/M. Carbon-14 has a relatively low specific activity.",
 "Carbon-14 has a relatively low specific activity.",
 "📚 Deep Dive: Specific activity (standard formula)",
 "a = λ·N_A/(M/1000) from the",
 "half-life gives the activity per kg.",
 "Measuring the activity concentration of a radioactive source in Bq/kg.",
 "Compare nuclides with different half-lives.",
 "th = 5730 years, M = 14 (C-14)",
 "Consistent with the per gram value",
 "1.65×10¹⁴ Bq/kg = 1.65×10¹¹ Bq/g, matching the order of magnitude of the previous tool.",
 "Why divide by M/1000?",
 "M is in g/mol, so M/1000 is in kg/mol; N_A divided by kg/mol gives the number of nuclei per kg, and multiplying by λ gives Bq/kg.",
 "Is higher always better?",
 "When preparing a source, a high specific activity means less mass is needed to reach the target activity, but radiation safety then demands more care.",
]

SVP = [
 "Find the survival probability from the decay constant and time",
 "Enter the decay constant λ and the time t to get the survival probability of the nuclide.",
 "Nuclide Survival Probability Calculator",
 "/ Nuclide Survival Probability Calculator",
 "📖 View Guide: \"Find the survival probability from the decay constant and time\"",
 "📚 Deep Dive: Survival probability (P = e^(-λt))",
 "P = e^(-λt) gives the probability of still being undecayed after time t.",
 "Reliability and storage",
 "comparisons of the survival rate for different λt.",
 "P = e^(-1) ≈ 0.3679, i.e. about 36.8% survive while 63.2% have decayed.",
 "One",
 "if t = ln2/λ, then P = 0.5, so exactly half survive.",
 "How does the survival probability relate to the",
 "decayed fraction",
 "?",
 "Complementary: the decayed fraction = 1 - P, see decay-fraction.",
 "Does it mean anything for a single nucleus?",
 "The exponential law is statistical: it gives a proportion across many nuclei and a decay probability for any single one.",
]

write('specific-activity-from-halflife', build('specific-activity-from-halflife', SAF))
write('specific-activity', build('specific-activity', SAC))
write('survival-probability', build('survival-probability', SVP))

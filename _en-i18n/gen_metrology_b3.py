#!/usr/bin/env python3
# gen_metrology_b3.py — metrology b3 (5 slugs): gauge-reproducibility/grr-percent/grr-study/guard-band-95/least-count-error
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'metrology')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'metrology')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EXTRA = {
 'least-count-error': {
  '分辨率？': 'Resolution?',
 },
}

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
    out = {'slug': slug, 'industry': 'metrology', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

GRB = [
 "Differences between operators",
 "Reproducibility = range of operator averages / d2*.",
 "/ Gage Reproducibility",
 "Gage Reproducibility",
 "📖 View Guide: \"Differences between operators\"",
 "Reproducibility = R̄/d2*",
 "Range of operator averages R0",
 "Number of operators",
 "It reflects systematic differences between people.",
 "It is only meaningful when it exceeds repeatability.",
 "📚 Deep Dive: Gage reproducibility",
 "Compute cross-operator variation",
 "GRR component",
 "AV = sqrt((XbarDiff*K2)^2 - EV^2/(n*r)). Example: operator average difference 0.005, K2=0.5231 gives AV about 0.0021.",
 "Range of operator averages 0.06, 2 operators",
 "Looking up d2* = 1.128 gives σ_o = 0.06/1.128 = 0.0532. Reproducibility reflects person-to-person differences and is usually reduced with a unified work instruction.",
 "Is it about people?",
 "Yes, it reflects differences in training and technique.",
 "How to improve it?",
 "Standardize the operation, introduce fixtures, and strengthen training.",
]

GRP = [
 "Find %GRR from measurement system error and tolerance",
 "Enter the measurement system error GRR and the tolerance zone to get %GRR.",
 "%GRR = GRR / tolerance x 100%",
 "/ Gage Repeatability and Reproducibility Percentage Calculator",
 "Gage Repeatability and Reproducibility Percentage Calculator",
 "📖 View Guide: \"Find %GRR from measurement system error and tolerance\"",
 "Tolerance zone",
 "A measurement system with %GRR below 10% is acceptable.",
 "📚 Deep Dive: GRR percentage",
 "Judge gage acceptability",
 "Gage selection",
 "%GRR = GRR / total variation x 100%. Example: GRR=0.004, total variation 0.02 gives %GRR=20%.",
 "GRR=1.8, tolerance zone 12",
 "%GRR = 1.8/12 x 100% = 15.0%, which lands in the 10%-30% borderline region and is usually taken as acceptable but needing attention; improve the gage or method whenever conditions allow.",
 "What is the criterion?",
 "Below 10% is good, 10-30% depends on the situation, above 30% is unacceptable.",
 "Versus P/T?",
 "%GRR is based on total variation and P/T on tolerance; the two are assessed side by side.",
]

GRS = [
 "Gage repeatability and reproducibility analysis",
 "%GRR = 6 x sqrt(σ_r^2 + σ_o^2) / tolerance x 100%.",
 "/ GRR Study (%GRR)",
 "GRR Study (%GRR)",
 "📖 View Guide: \"Gage repeatability and reproducibility analysis\"",
 "Tolerance T",
 "%GRR below 10% is good.",
 "10%-30% depends on the situation.",
 "📚 Deep Dive: GRR study (gage R&R)",
 "Design a crossed experiment",
 "Analyze gage capability",
 "Selection",
 "GRR = sqrt(EV^2 + AV^2) (range method). Example: EV=0.0018, AV=0.0021 gives GRR=0.0028.",
 "σ_r=0.035, σ_o=0.02, tolerance 0.5",
 "GRR spread = 6 x sqrt(0.035^2 + 0.02^2) = 0.2419, %GRR = 0.2419/0.5 x 100% = 48.4%, judged \"unacceptable\". The main contribution comes from",
 ", so improving the gage's own variation should come first.",
 "Samples?",
 "Typically 10 parts x 3 operators x 2-3 repeats.",
 "What is the purpose?",
 "To quantify how much of the process variation comes from the gage.",
]

GB9 = [
 "Find the one-sided 95% guard band from expanded uncertainty",
 "Enter the expanded uncertainty U to get the one-sided 95% guard band.",
 "Guard Band (95%) Calculator",
 "/ Guard Band (95%) Calculator",
 "📖 View Guide: \"Find the one-sided 95% guard band from expanded uncertainty\"",
 "Expanded uncertainty U",
 "A guard band narrows the conformance limits and lowers the risk of wrong decisions.",
 "📚 Deep Dive: 95% guard band",
 "Set acceptance limits",
 "Reduce false acceptance",
 "Metrological confirmation",
 "Acceptance limit = specification limit ± U (or k*U depending on risk). Example: upper limit 10.00, U=0.02, accept at 9.98 to reduce false acceptance.",
 "Expanded uncertainty",
 "GB = 1.65 x 0.12 = 0.1980. Pulling the specification limit inward by 0.198 when judging conformance cuts false-acceptance risk to about 5%, at the cost of slightly more false rejects.",
 "Why?",
 "It leaves an uncertainty margin and reduces the chance of passing an out-of-tolerance item (false acceptance).",
 "What is the risk?",
 "Too tight a band raises the false-reject rate, so trade the two risks off against each other.",
]

LCE = [
 "± half a scale division",
 "Reading error is about ± scale division / 2.",
 "Scale Division Error",
 "/ Error from Scale Division",
 "Error from Scale Division",
 "📖 View Guide: \"± half a scale division\"",
 "Limiting error = ± (scale division / 2)",
 "Scale division (mm)",
 "Visual interpolation is usually ±0.5 division.",
 "Digital gages do not have this error.",
 "📚 Deep Dive: Scale division error",
 "Interpolation error",
 "Digital resolution",
 "Conformance records",
 "Interpolation error is about ±(0.5 to 1) x scale division. Example: a caliper with 0.02 mm division has a reading error of about ±0.01 to 0.02 mm.",
 "Scale division 0.005 mm",
 "Reading limiting error = ±0.005/2 = ±0.0025 mm, lower limit -0.0025. This is the maximum error estimated from reading rules; the actual reading error is usually smaller.",
 "Digital resolution is the smallest displayed digit; record one interpolated digit.",
 "Versus uncertainty?",
 "It contributes as a",
 "Type B uncertainty",
 "component.",
]

write('gauge-reproducibility', build('gauge-reproducibility', GRB))
write('grr-percent', build('grr-percent', GRP))
write('grr-study', build('grr-study', GRS))
write('guard-band-95', build('guard-band-95', GB9))
write('least-count-error', build('least-count-error', LCE))

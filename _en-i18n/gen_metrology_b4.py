#!/usr/bin/env python3
# gen_metrology_b4.py — metrology b4 (5 slugs): measurement-cg/measurement-cgk/ndc-number/precision-tolerance-ratio/relative-uncertainty
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'metrology')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'metrology')

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
    out = {'slug': slug, 'industry': 'metrology', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

MCG = [
 "Find the measurement capability index from the tolerance zone and measurement standard deviation",
 "Enter the upper and lower specification limits and the measurement standard deviation s to get Cg.",
 "Measurement Capability Index Cg Calculator",
 "/ Measurement Capability Index Cg Calculator",
 "📖 View Guide: \"Find the measurement capability index from the tolerance zone and measurement standard deviation\"",
 "Cg ≥ 1.33 usually means the measurement system is qualified.",
 "📚 Deep Dive: Measurement system capability Cg",
 "Use the gage capability index",
 "Gage selection",
 "Cg = (USL-LSL)/(6*sigma_measure) (or the constrained form 0.2*(USL-LSL)). Example: tolerance 0.1, sigma_m=0.008 gives Cg = 0.1/(6*0.008) = 2.08.",
 "Cg = (8-2)/(6 x 0.25) = 4.000, far above the 1.33 threshold, so the gage resolution is more than enough for this tolerance zone.",
 "What is the criterion?",
 "Cg ≥ 1.33 is usually acceptable.",
 "Versus Cpk?",
 "Cg looks at the measurement system itself, Cpk at the process.",
]

MCK = [
 "Find the bias-corrected capability index from bias and standard deviation",
 "Enter the upper and lower specification limits, the measurement mean and the standard deviation to get Cgk.",
 "Bias-Corrected Capability Index Cgk Calculator",
 "/ Bias-Corrected Capability Index Cgk Calculator",
 "📖 View Guide: \"Find the bias-corrected capability index from bias and standard deviation\"",
 "Measurement mean x̄",
 "Cgk accounts for both bias and variation.",
 "📚 Deep Dive: Measurement system capability Cgk",
 "Capability with bias",
 "Acceptance",
 "Cgk = min(USL-mean, mean-LSL)/(3*sigma_measure). Example: with the mean off center by 0.002, Cgk is slightly lower than Cg.",
 "Cgk = min(8-5.5, 5.5-2)/(3 x 0.25) = 2.5/0.75 = 3.333. The mean 5.5 sits exactly in the center; once it shifts, Cgk falls noticeably below Cg.",
 "Versus Cg?",
 "Cgk also accounts for bias and is therefore stricter.",
 "What is the criterion?",
]

NDC = [
 "Find the number of distinct categories from part variation and measurement error",
 "Enter the part-to-part variation PV and the measurement system error GRR to get NDC.",
 "Number of Distinct Categories (NDC) Calculator",
 "/ Number of Distinct Categories (NDC) Calculator",
 "📖 View Guide: \"Find the number of distinct categories from part variation and measurement error\"",
 "Part variation PV",
 "With NDC ≥ 5 the measurement system can distinguish between parts.",
 "📚 Deep Dive: Number of distinct categories (NDC)",
 "Judge gage resolution",
 "Paired with GRR",
 "NDC = 1.41*(PV/GRR). Example: process variation PV=0.02, GRR=0.0028 gives NDC = 1.41*7.14 ≈ 10.",
 "Part-to-part variation PV=6.5, GRR=0.8",
 "NDC = 1.41 x 6.5/0.8 = 11.46, well above 5, so this measurement system resolves the true differences between parts.",
 "What is the criterion?",
 "NDC ≥ 5 means the gage resolves process variation well enough.",
 "What if it falls short?",
 "Improve the resolution or change the gage.",
]

PTR = [
 "Find the precision-to-tolerance ratio from measurement standard deviation and tolerance zone",
 "Enter the measurement standard deviation s and the tolerance zone Tol to get PTR.",
 "Precision to Tolerance Ratio (PTR) Calculator",
 "/ Precision to Tolerance Ratio (PTR) Calculator",
 "📖 View Guide: \"Find the precision-to-tolerance ratio from measurement standard deviation and tolerance zone\"",
 "Tolerance zone Tol",
 "PTR below 0.1 usually means the resolution is sufficient.",
 "📚 Deep Dive: Precision to tolerance ratio (P/T)",
 "Gage capability against tolerance",
 "Gage selection",
 "P/T = 6*sigma_measure / tolerance (or GRR/tolerance). Example: GRR=0.004, tolerance 0.1 gives P/T=24%.",
 "s=0.15, tolerance 6",
 "PTR = 6 x 0.15/6 = 0.150, slightly above the recommended upper limit of 0.1; the gage precision is tight for this tolerance, so move to higher-precision equipment.",
 "What is the criterion?",
 "P/T below 10% is good, 10-30% depends on the situation, above 30% is unacceptable.",
 "Versus %GRR?",
 "One uses tolerance as the denominator, the other total variation.",
]

RLU = [
 "Find the relative uncertainty from standard uncertainty and measured value",
 "Enter the standard uncertainty u and the measured value x to get the relative uncertainty.",
 "Relative Uncertainty Calculator",
 "/ Relative Uncertainty Calculator",
 "📖 View Guide: \"Find the relative uncertainty from standard uncertainty and measured value\"",
 "Standard uncertainty u",
 "Relative uncertainty makes comparisons across dimensions easy.",
 "📚 Deep Dive: Relative uncertainty",
 "Compute relative U",
 "Compare across ranges",
 "Reporting",
 "U_rel = U / |y| * 100%. Example: y=100.0, U=0.5 gives U_rel = 0.5%.",
 "u=0.2, measured value 25",
 "u_rel = 0.2/|25| x 100% = 0.800%. Relative uncertainty makes it easy to compare precision between measurements of different magnitudes.",
 "Where is it used?",
 "It suits cross-range comparison and judging orders of magnitude.",
 "Versus absolute?",
 "Where the absolute value is small the relative one is larger, so state which one you mean.",
]

write('measurement-cg', build('measurement-cg', MCG))
write('measurement-cgk', build('measurement-cgk', MCK))
write('ndc-number', build('ndc-number', NDC))
write('precision-tolerance-ratio', build('precision-tolerance-ratio', PTR))
write('relative-uncertainty', build('relative-uncertainty', RLU))

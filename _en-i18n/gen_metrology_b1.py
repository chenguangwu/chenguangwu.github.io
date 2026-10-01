#!/usr/bin/env python3
# gen_metrology_b1.py — metrology b1 (5 slugs): bias-absolute/bias-percent/calibration-uncertainty/combined-uncertainty/dimensional-tolerance
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

BIA = [
 "Find absolute bias from a measured value and a reference value",
 "Enter a measured value and a reference standard value to get the absolute bias.",
 "Absolute Bias Calculator",
 "/ Absolute Bias Calculator",
 "📖 View Guide: \"Find absolute bias from a measured value and a reference value\"",
 "Bias = x - x_ref",
 "Bias reflects the direction of systematic error.",
 "📚 Deep Dive: Absolute bias",
 "Compute gage systematic bias",
 "Bias decision",
 "Calibration correction",
 "bias = mean(measured values) - reference value (true value). Example: reference 10.000 mm, mean of 10 readings 10.015, bias = +0.015 mm.",
 "Measured 20.35, reference 20",
 "Bias = x - x_ref = 20.35 - 20 = 0.350. A positive value means the readings run systematically high, so when correcting you subtract this amount from later readings.",
 "Bias versus error?",
 "Bias is the averaged systematic error over repeated measurements and reflects the overall offset of the gage.",
 "How do I correct it?",
 "Subtract the bias at calibration time, or build a correction curve and apply it.",
]

BIP = [
 "Find relative bias from a measured value and a reference value",
 "Enter a measured value and a reference standard value to get the relative bias.",
 "Relative Bias Calculator",
 "/ Relative Bias Calculator",
 "📖 View Guide: \"Find relative bias from a measured value and a reference value\"",
 "Bias% = (x - x_ref)/x_ref x 100%",
 "Relative bias makes comparisons across measuring ranges easy.",
 "📚 Deep Dive: Percentage bias",
 "Compute relative bias",
 "Assess against process tolerance",
 "Pre-check before GRR",
 "%bias = bias / process variation (or tolerance) x 100%. Example: bias=0.015, process variation 0.1, %bias=15%.",
 "Measured 20.6, reference 20",
 "Bias% = (20.6 - 20)/20 x 100% = 3.00%. Relative bias makes cross-range comparison easy; the same absolute bias looks far more severe on a small range.",
 "What is the criterion?",
 "Generally %bias below 10% is acceptable; the exact threshold depends on the industry and the risk involved.",
 "Which denominator?",
 "Whether to use process variation or tolerance must be agreed up front, because the two can lead to different conclusions.",
]

CLU = [
 "Standard + repeatability",
 "Calibration Uncertainty",
 "/ Calibration Uncertainty Combination",
 "Calibration Uncertainty Combination",
 "📖 View Guide: \"Standard + repeatability\"",
 "Standard uncertainty",
 "Repeatability uncertainty",
 "Calibration certificates usually state expanded uncertainty, so divide it by k first.",
 "Components are combined assuming independence.",
 "📚 Deep Dive: Calibration uncertainty",
 "Compute the uncertainty of a calibration result",
 "Issue certificates",
 "Propagate to the next level",
 "Usually U = k*u_c with k=2 for about 95% confidence. Example: standard u=0.5 μm, transfer u=0.3 μm, combined then expanded gives 1.2 μm (k=2).",
 "Standard 0.04, repeatability 0.025",
 "u_c = sqrt(0.04^2 + 0.025^2) = 0.04717; taking k=2 gives the",
 "expanded uncertainty",
 "U = 0.09434. The two components combine as the root sum square rather than by direct addition.",
 "Versus GRR?",
 "Calibration uncertainty describes the gage's own precision, while GRR also covers operator and method variation.",
 "How is k chosen?",
 "k=2 is usual for 95% and k about 2.58 for 99%.",
]

CMU = [
 "Root sum square of independent components.",
 "Combined Uncertainty",
 "/ Combined Standard Uncertainty",
 "Combined Standard Uncertainty",
 "📖 View Guide: \"Combined Uncertainty\"",
 "Components u_i (comma separated)",
 "Components are assumed independent.",
 "With correlation coefficients, weighting is required.",
 "📚 Deep Dive: Combined uncertainty",
 "Combine multi-component uncertainty",
 "Reporting",
 "Modeling",
 "u_c = sqrt(sum(u_i^2) + covariance terms). Example: two independent components 1 and 2 give u_c = sqrt(1+4) = 2.24.",
 "Component sequence 0.05,0.12,0.09",
 "u_c = sqrt(0.05^2 + 0.12^2 + 0.09^2) = 0.15811; the tool also reports the combination of the first two components, 0.13000, so you can judge how much the third one contributes.",
 "Independence assumption?",
 "Variances of independent components add directly; when they are correlated you must add covariance terms.",
 "Versus expanded?",
 "u_c multiplied by the coverage factor k gives the",
 "expanded uncertainty",
]

DMT = [
 "Upper deviation - lower deviation",
 "Tolerance = upper deviation - lower deviation, and limit dimensions = basic size plus/minus deviation.",
 "Dimensional Tolerance Zone",
 "/ Dimensional Tolerance Zone",
 "📖 View Guide: \"Upper deviation - lower deviation\"",
 "Dimensional tolerance: tolerance T = upper deviation es - lower deviation ei; maximum limit size = basic size + es, minimum limit size = basic size + ei; tolerance-zone center = basic size + (es + ei) / 2. A smaller tolerance demands higher machining precision and higher cost, so pick it according to the required fit.",
 "Upper deviation ES (mm)",
 "Lower deviation EI (mm)",
 "Deviations can be positive or negative.",
 "The type of fit is set by the tolerance zone.",
 "📚 Deep Dive: Dimensional tolerance",
 "Compute the tolerance zone",
 "Upper and lower limits",
 "Conformance decision",
 "Tolerance = USL - LSL. Example: a shaft at 20±0.05 has USL=20.05, LSL=19.95 and a tolerance of 0.10 mm.",
 "Nominal 30, upper deviation +0.021, lower deviation -0.007",
 "Tolerance = 0.021 - (-0.007) = 0.028 mm; maximum limit size 30.021 mm, minimum limit size 29.993 mm. A negative lower deviation must be substituted with its sign.",
 "One-sided tolerance?",
 "Only USL or LSL is given and the other side follows from the functional requirement.",
 "Tolerance and fit?",
 "The relative position of the hole and shaft tolerance zones determines a clearance or interference fit.",
]

write('bias-absolute', build('bias-absolute', BIA))
write('bias-percent', build('bias-percent', BIP))
write('calibration-uncertainty', build('calibration-uncertainty', CLU))
write('combined-uncertainty', build('combined-uncertainty', CMU))
write('dimensional-tolerance', build('dimensional-tolerance', DMT))

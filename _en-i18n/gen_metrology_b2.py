#!/usr/bin/env python3
# gen_metrology_b2.py — metrology b2 (5 slugs): drift-rate/effective-dof-welch/expanded-uncertainty/flatness-deviation/gauge-repeatability
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

DRT = [
 "Find the drift rate from two readings and the elapsed time",
 "Enter two readings taken before and after, plus the time interval, to get the drift rate.",
 "Drift Rate Calculator",
 "/ Drift Rate Calculator",
 "📖 View Guide: \"Find the drift rate from two readings and the elapsed time\"",
 "Initial value x1",
 "Final value x2",
 "Time interval Δt (days)",
 "Positive drift means the measured value grows with time.",
 "📚 Deep Dive: Drift rate",
 "Compute sensor drift",
 "Stability assessment",
 "Service life",
 "Drift rate = Δreading / time. Example: a change of 0.02 mV over 24 h gives a drift of 0.00083 mV/h.",
 "Previous 100, current 103.6, interval 12 days",
 "Drift rate = (103.6 - 100)/12 = 0.3000 units/day. Extrapolated at this rate over one month the accumulated drift is about 9 units, so arrange an interim check or recalibration.",
 "Thermal drift?",
 "It is usually quoted as %FS/°C; control the temperature or build in temperature compensation.",
 "What is the impact?",
 "Long-term drift accumulates into error, so periodic calibration is required.",
]

EDW = [
 "Find the effective degrees of freedom from component uncertainties and their degrees of freedom",
 "Enter the uncertainties u, v of two components and their degrees of freedom ν to get the effective degrees of freedom.",
 "Effective Degrees of Freedom (Welch) Calculator",
 "/ Effective Degrees of Freedom (Welch) Calculator",
 "📖 View Guide: \"Find the effective degrees of freedom from component uncertainties and their degrees of freedom\"",
 "It is used with a t table to set the coverage factor.",
 "📚 Deep Dive: Welch effective degrees of freedom",
 "Combine uncertainty degrees of freedom",
 "Choose k from the t distribution",
 "Small samples",
 "nu_eff = u_c^4 / sum(u_i^4/nu_i). Example: u1=1, nu1=10; u2=2, nu2=5 gives nu_eff about 9.1.",
 "ν_eff = (2.5^2 + 1.5^2)^2 / (2.5^4/6 + 1.5^4/12) = (8.5)^2/(6.5104 + 0.4219) = 10.42. The combined degrees of freedom fall between those of the two components, leaning toward the one with the larger uncertainty.",
 "What is it for?",
 "Use nu_eff to look up the coverage factor k in the t table rather than always fixing k=2.",
 "Versus combination?",
 "First combine to get u_c, then compute nu_eff.",
]

EXU = [
 "U = coverage factor k x combined uncertainty.",
 "Expanded Uncertainty",
 "/ Expanded Uncertainty",
 "📖 View Guide: \"Expanded Uncertainty\"",
 "k=2 gives about 95% confidence. Report form: measured value ± U.",
 "Combined uncertainty u_c",
 "Measured value",
 "k=2 gives about 95% confidence.",
 "Report form: measured value ± U.",
 "📚 Deep Dive: Expanded uncertainty",
 "Report the interval of a measurement result",
 "Certificates",
 "Compliance",
 "U = k * u_c. Example: u_c=0.5, k=2 gives U=1.0 (the 95% interval is about ±1.0).",
 "u_c=0.075, k=3, measured value 25.00",
 "U = 3 x 0.075 = 0.2250; the interval is 24.7750 to 25.2250. A larger k gives a wider interval and a higher confidence level, so the report must also state the k value.",
 "What does it mean?",
 "One may reasonably believe the true value lies in [y-U, y+U] at the stated confidence level.",
 "How is k chosen?",
 "Use 2 for 95% and 2.58 for higher confidence.",
 "How to use expanded uncertainty",
 "What is expanded uncertainty for?",
 "Enter the combined standard uncertainty and the coverage factor k, then compute the expanded uncertainty as U = k x u_c to give the credible interval of a measurement result.",
 "How do I use expanded uncertainty?",
 "Which scenarios suit expanded uncertainty?",
]

FLD = [
 "Highest point - lowest point",
 "Flatness = highest measured point - lowest measured point (minimum zone approximation).",
 "Flatness Error",
 "/ Flatness Error",
 "📖 View Guide: \"Highest point - lowest point\"",
 "Flatness = highest point - lowest point",
 "Highest point (mm)",
 "Lowest point (mm)",
 "Actual measurement needs multi-point sampling.",
 "📚 Deep Dive: Flatness deviation",
 "Compute flatness",
 "Quality inspection",
 "Lapping",
 "Flatness = highest point - lowest point (minimum containing plane). Example: 9 measured points with a range of 0.008 mm give flatness 0.008 mm.",
 "Highest point 0.018 mm, lowest point -0.012 mm",
 "Flatness = 0.018 - (-0.012) = 0.030 mm, i.e. 30.0 μm. This is the minimum-zone approximation; the more points measured, the closer it gets to the true flatness.",
 "Versus parallelism?",
 "Flatness is the form error of a single surface, while parallelism constrains the relation between two planes.",
 "How to measure?",
 "Three points define the datum plane, then take the largest deviation among the remaining points.",
]

GRP = [
 "Range method R̄/d2",
 "Repeatability standard deviation = average range / d2.",
 "/ Gage Repeatability",
 "Gage Repeatability",
 "📖 View Guide: \"Range method R̄/d2\"",
 "Repeatability = R̄/d2",
 "Number of measurements",
 "The range method gives a quick estimate.",
 "d2 varies with the number of measurements.",
 "📚 Deep Dive: Gage repeatability",
 "Compute the variation of repeated measurements by one operator",
 "GRR component",
 "Repeatability EV = Rbar * K1 (range method). Example: Rbar=0.003, K1=0.5908 (2 trials) gives EV=0.0018.",
 "Average range 0.07, 4 repeated trials",
 "Looking up d2 = 2.059 gives σ_r = 0.07/2.059 = 0.0340; the 99% process spread is 5.15σ_r = 0.1751. Since d2 changes with the number of trials, choosing the wrong one visibly skews the result.",
 "Versus reproducibility?",
 "Repeatability is the same operator with the same gage; reproducibility spans operators and equipment.",
 "What is the criterion?",
 "EV% should be far smaller than the tolerance or process variation.",
]

write('drift-rate', build('drift-rate', DRT))
write('effective-dof-welch', build('effective-dof-welch', EDW))
write('expanded-uncertainty', build('expanded-uncertainty', EXU))
write('flatness-deviation', build('flatness-deviation', FLD))
write('gauge-repeatability', build('gauge-repeatability', GRP))

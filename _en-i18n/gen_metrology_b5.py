#!/usr/bin/env python3
# gen_metrology_b5.py — metrology b5 (5 slugs): resolution-uncertainty/roundness-deviation/std-dev-type-a/tolerance-stackup-worst/type-a-uncertainty
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'metrology')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'metrology')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EXTRA = {
 'type-a-uncertainty': {
  '平均值 20.0167，': 'Mean 20.0167,',
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

RSU = [
 "Uncertainty contributed by the resolution of the last displayed digit.",
 "Resolution Uncertainty",
 "/ Resolution Uncertainty",
 "📖 View Guide: \"Resolution Uncertainty\"",
 "Typical treatment for digital instruments.",
 "Resolution of the last digit a.",
 "📚 Deep Dive: Resolution uncertainty",
 "Estimate Type B from resolution",
 "Digital / analog",
 "Uncertainty budget",
 "u_res = scale division / sqrt(12) (",
 "rectangular distribution",
 "). Example: division 0.01 gives u_res = 0.01/3.464 = 0.0029.",
 "Resolution of the last digit 0.002",
 "Under a rectangular distribution u = 0.002/(2√3) = 0.000577; the tool also gives half-width/√3 = 0.000333 for comparison, and the gap between the two treatments is worth noting.",
 "Which distribution?",
 "Readings are uniform within one division, so take",
 "division/√12.",
 "Digital displays?",
 "The last digit is ±0.5 count and is handled the same way.",
]

RND = [
 "Roundness = maximum radius - minimum radius (minimum zone approximation).",
 "Roundness Error",
 "/ Roundness Error",
 "📖 View Guide: \"Roundness Error\"",
 "Roundness = R_max - R_min",
 "Maximum radius (mm)",
 "Minimum radius (mm)",
 "This is the max-min approximation.",
 "📚 Deep Dive: Roundness deviation",
 "Compute roundness",
 "Quality inspection",
 "Bearings",
 "Roundness = maximum radius - minimum radius (least squares or minimum zone circle). Example: a range of 0.005 mm gives roundness 0.005 mm.",
 "Maximum radius 15.012, minimum radius 14.986",
 "Roundness = 15.012 - 14.986 = 0.026 mm, i.e. 26.0 μm. This is the minimum-zone approximation; precision rotating parts usually still need roundness evaluated against the relevant standard.",
 "Versus cylindricity?",
 "Roundness applies to a single cross-section, while cylindricity also covers the axial profile.",
 "Which datum?",
 "Evaluate against the least-squares circle center or the minimum zone circle.",
]

SDA = [
 "Find the Type A standard uncertainty from the sample standard deviation and the number of measurements",
 "Enter the sample standard deviation s and the number of measurements n to get the Type A standard uncertainty.",
 "Type A Standard Uncertainty Calculator",
 "/ Type A Standard Uncertainty Calculator",
 "📖 View Guide: \"Find the Type A standard uncertainty from the sample standard deviation and the number of measurements\"",
 "Number of measurements n",
 "u_A = s/√n (for repeated measurements).",
 "📚 Deep Dive: Type A standard deviation",
 "Estimate s from repeated measurements",
 "uncertainty",
 "s = sqrt(sum((xi-xbar)^2)/(n-1)). Example: 5 readings of 10.001, 10.003, 9.999, 10.002, 10.000 give s about 0.0016.",
 "Sample",
 "standard deviation 1.5, 16 measurements",
 "u_A = s/√n = 1.5/4 = 0.3750. Doubling the number of measurements only cuts u_A to about 70%, so increasing n gives diminishing returns.",
 "Type A definition?",
 "An uncertainty component evaluated by statistical methods (repeated observations).",
 "Versus Type B?",
 "Type B uses non-statistical information such as certificates, experience or handbooks.",
]

TSW = [
 "Worst-case accumulation of a linear dimension chain = the sum of the absolute tolerances of all links.",
 "Worst-Case Accumulation",
 "/ Dimension Chain Worst Case",
 "Dimension Chain Worst Case",
 "📖 View Guide: \"Worst-Case Accumulation\"",
 "Tolerance of each link (comma separated)",
 "The worst case is conservative.",
 "A statistical approach can use RSS instead.",
 "📚 Deep Dive: Worst-case tolerance stack-up",
 "Compute worst-case assembly clearance",
 "Dimension chain",
 "Design margin",
 "Total tolerance = sum(|t_i|) (linear addition). Example: three parts at ±0.05, ±0.03 and ±0.02 give ±0.10 mm overall.",
 "Dimension chain tolerances 0.12,-0.05,0.08,0.03",
 "Worst-case accumulation = 0.12+0.05+0.08+0.03 = 0.280 mm, an average of 0.070 mm per link. Negative tolerances enter as absolute values, so the result is the most conservative estimate.",
 "Versus RSS?",
 "Worst-case stacking is conservative, while RSS (root sum square) is statistically tighter; choose by risk.",
 "Where is it used?",
 "Critical fits and safety parts take the worst case.",
]

TAU = [
 "Type A Uncertainty",
 "Derived statistically from repeated observations, u_A = sample standard deviation / √n.",
 "/ Type A Standard Uncertainty",
 "Type A Standard Uncertainty",
 "📖 View Guide: \"Type A Uncertainty\"",
 "Bessel formula: the experimental standard deviation s = sqrt(Σ(xᵢ - x̄)² / (n - 1)); the standard uncertainty of the mean u_A = s / √n; degrees of freedom ν = n - 1; relative standard uncertainty = u_A / x̄ x 100%. A larger n gives a smaller u_A.",
 "Measured values (comma separated)",
 "Based on the Bessel formula.",
 "A larger n gives a smaller uncertainty.",
 "📚 Deep Dive: Type A uncertainty",
 "Evaluate uA from an observation series",
 "Repeated measurement",
 "Uncertainty budget",
 "u_A = s/√n (standard uncertainty of the mean). Example: s=0.0016, n=5 gives u_A=0.00072.",
 "Repeated observations 20.02,20.05,19.98,20.01,20.04,20.00",
 "s = 0.0258 (Bessel formula, dividing by n-1) and u_A = s/√6 = 0.0105.",
 "Versus s?",
 "A single s is the observed",
 "spread, while the uncertainty of the mean is s/√n.",
 "Degrees of freedom?",
 "nu = n-1, which feeds into the effective degrees of freedom.",
]

write('resolution-uncertainty', build('resolution-uncertainty', RSU))
write('roundness-deviation', build('roundness-deviation', RND))
write('std-dev-type-a', build('std-dev-type-a', SDA))
write('tolerance-stackup-worst', build('tolerance-stackup-worst', TSW))
write('type-a-uncertainty', build('type-a-uncertainty', TAU))

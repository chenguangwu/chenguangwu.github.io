#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'process')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'process')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
DISCL = "Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected."
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
    out = {'slug': slug, 'industry': 'process', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('defect-probability', build('defect-probability', [
        "Out-of-Spec Probability Calculator",
        "Probability of exceeding the upper specification limit under the normal assumption.",
        "/ Out-of-Spec Probability",
        "Out-of-Spec Probability",
        "📖 View the \"Out-of-Spec Probability Calculator User Guide\"",
        "z=5 -> probability about 2.87e-7. When symmetric, total defects are the sum of both sides.",
        "z=5 -> probability about 2.87e-7.",
        "When symmetric, total defects are the sum of both sides.",
        "📚 In-Depth Analysis: Out-of-Spec Probability Calculator",
        "Assuming the quality characteristic follows",
        ", estimate the probability of one-sided (upper-spec-only or lower-spec-only) exceedance and the corresponding",
        ", translating the capability index into an intuitive 'defect rate'.",
        "When the customer requires communication in 'defects per million opportunities', convert the probability into DPMO for easy cross-comparison.",
        "Given the specification and process parameters, back-calculate the tail probability at the current σ level to judge whether tighter control is needed.",
        "One-sided (upper spec) exceedance probability P = 1 - Φ(z), where z = (USL - μ)/σ, Φ is the standard normal cumulative distribution function; corresponding DPMO = P × 10^6. The same method gives the lower-spec P = Φ((μ - LSL)/σ). This tool uses the upper spec as an example.",
        "Shaft diameter USL=10.05, μ=10.0, σ=0.02: z = (10.05-10.0)/0.02 = 2.50; P = 1 - Φ(2.5) = 1 - 0.99379 = 0.6210%; corresponding DPMO ≈ 6209.7. If σ is reduced from 0.02 to 0.01, then z=5, P≈0.00003%, DPMO≈0.3, almost zero defects - showing that compressing dispersion yields exponential benefit in reducing tail probability.",
        "Why one-sided?",
        "This tool computes the upper-tail probability of exceeding the upper limit by the upper spec (USL); if you care about falling below the lower limit, use the lower-spec formula Φ((μ-LSL)/σ). When both sides exceed simultaneously and the specs are far from the mean, the two tail probabilities can be approximated by addition, but more rigorously the total probability outside the spec interval should be computed directly.",
        "What if the normal-distribution assumption does not hold?",
        "Actual characteristics are often not strictly normal (skewness, heavy tails). In that case the normal approximation underestimates the tail probability (heavy tails are more dangerous); a normality test (e.g. Anderson-Darling) should be done, or a non-parametric method / Box-Cox transformation used before re-evaluation.",
    ]))

    write('dpmo-calc', build('dpmo-calc', [
        "DPMO = defects / (units × opportunities) × 10^6",
        "Defects per million opportunities, a universal measure of process quality.",
        "DPMO Calculator",
        "/ DPMO Calculation",
        "DPMO Calculation",
        "📖 View the \"DPMO Calculator User Guide\"",
        "20000×1e6 = 6200 DPMO. Opportunities refers to the number of features that can be defective.",
        "Number of units",
        "Opportunities refers to the number of features that can be defective.",
        "📚 In-Depth Analysis: DPMO Calculator",
        "Convert 'number of defects' into 'defects per million opportunities', enabling processes of different products and complexities to be compared on the same scale.",
        "When initiating a Six Sigma project, quantify the baseline defect level as a unified KPI for before-and-after improvement comparison.",
        "When summarizing multiple processes / multiple defect types, first compute the overall DPMO then map to",
        "sigma level",
        "DPMO = defects ÷ (number of products × per-unit defect opportunities) × 10^6. 'Opportunities' refers to the number of independent positions/features on a single unit that can go wrong (e.g. 200 solder joints on a PCB means 200 opportunities); the more consistent the opportunity definition, the fairer the cross-process comparison.",
        "A batch sampled 2000 products, each with 10 key characteristics (opportunities=10), and 124 defects were found: DPMO = 124 ÷ (2000 × 10) × 10^6 = 124 ÷ 20000 × 10^6 = 6200.0. This DPMO corresponds to about a 4.0 sigma level (with 1.5σ shift) and can serve as the baseline improvement target.",
        "How should the number of opportunities be set reasonably?",
        "Opportunities should be 'potentially independent defect occurrence points', and the probability of a defect at each opportunity should be roughly similar; do not arbitrarily inflate the number of opportunities to push down DPMO (that would artificially inflate the sigma level). The industry usually counts by critical-to-quality (CTQ) characteristics and keeps a consistent basis.",
        "Is lower DPMO always better?",
        "The goal is to reduce defects, but DPMO is greatly affected by the opportunity definition; the same defect rate with different opportunity definitions yields different DPMO. Therefore comparisons must use the same opportunity basis, or use auxiliary metrics such as defect rate / rolled throughput yield for cross-validation.",
    ]))

    write('first-pass-yield', build('first-pass-yield', [
        "FPY = good units / input units × 100%",
        "The proportion that passes first time without rework.",
        "First Pass Yield Calculator",
        "/ First Pass Yield (FPY)",
        "First Pass Yield (FPY)",
        "📖 View the \"First Pass Yield Calculator User Guide\"",
        "FPY = good units / input units",
        "Good units",
        "Input units",
        "Units passing after rework are not counted in FPY.",
        "📚 In-Depth Analysis: First Pass Yield Calculator",
        "Measures the proportion of products that are 'no rework, no repair, pass first time', reflecting the process's ability to do it right the first time (stricter than the final yield).",
        "In lean / Six Sigma it is a core metric for process quality and waste, directly tied to rework cost.",
        "For multi-station processes, multiply each station's FPY to get RTY (see",
        "rolled throughput yield",
        "tool).",
        "FPY = first-time-good units ÷ total produced units × 100%. First-time-good means units that pass without any rework/repair; if a unit passes after repair, it is not counted as 'first-time-good'.",
        "A process started 1000 units that day, of which 950 passed first time and 50 passed after rework: FPY = 950 ÷ 1000 × 100% = 95.00%. Although the final yield is 100%, FPY is only 95%, indicating 5% rework waste; the root cause of those 50 units should be traced rather than only looking at final shipment.",
        "What is the difference between FPY and final yield?",
        "Final yield includes units passing after rework, masking rework cost; FPY only counts first-time-good units, more truthfully exposing process variation and waste, and is the metric Six Sigma values more.",
        "Should FPY be low but yield 100% be addressed?",
        "Yes. Low FPY means persistent rework, bringing labor, hours, equipment occupation and potential quality risk; in the long run it erodes delivery and cost, and should be an improvement focus rather than ignored because of 'final pass'.",
    ]))

    write('measurement-uncertainty', build('measurement-uncertainty', [
        "Combined Uncertainty Calculator",
        "Synthesis (RSS) of multiple independent uncertainty components.",
        "/ Combined Measurement Uncertainty",
        "Combined Measurement Uncertainty",
        "📖 View the \"Combined Uncertainty Calculator User Guide\"",
        "√0.38≈0.616. Components should be mutually independent.",
        "Component 1 u1",
        "Component 2 u2",
        "Component 3 u3",
        "Components should be mutually independent.",
        "📚 In-Depth Analysis: Combined Uncertainty Calculator",
        "Per the GUM method, root-sum-square multiple independent uncertainty components (e.g. gauge, environment, method) to obtain the total standard uncertainty u_c of the measurement result.",
        "Calibration / test report gives",
        "expanded uncertainty",
        "before; first assess each component's contribution and identify the dominant error source.",
        "Judge whether the existing measurement system satisfies the 'one-tenth' engineering rule (measurement uncertainty ≤ 1/10 of the tolerance).",
        "Combined standard uncertainty u_c = √(u1² + u2² + u3² + …), assuming the components are mutually independent; if components are correlated a covariance term must be added. Components can come from gauge resolution, repeatability, temperature/environment, standard transfer, etc. Expanded uncertainty U = k·u_c (k usually 2, corresponding to about 95% confidence).",
        "A dimensional measurement has three standard uncertainty components: gauge repeatability u1=0.5, environmental temperature drift u2=0.3, standard block transfer u3=0.2 (unit μm): u_c = √(0.5² + 0.3² + 0.2²) = √(0.25+0.09+0.04) = √0.38 ≈ 0.6164 μm. The repeatability (0.5) is the dominant component, so improving the gauge yields more benefit than suppressing temperature drift.",
        "Why use root-sum-square instead of direct addition?",
        "The components are random/systematic errors from different sources; worst-case addition (linear superposition) would severely overestimate; root-sum-square (RSS) gives a statistically reasonable combined value under the independence assumption and is the internationally accepted GUM practice.",
        "How to handle non-independent components?",
        "If correlation exists (e.g. the same temperature affects both gauge and workpiece), add a covariance term 2·ρ·ui·uj inside the sum of squares; for simplicity, de-correlate first or adopt a more conservative correlation assumption, to avoid underestimating the total uncertainty.",
    ]))


if __name__ == '__main__':
    main()

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
    write('cp-index', build('cp-index', [
        "Cp Process Capability Calculator",
        "Measures the ratio of specification width to process dispersion (ignoring shift).",
        "/ Process Capability Index Cp",
        "Process Capability Index Cp",
        "📖 View the \"Cp Process Capability Calculator User Guide\"",
        "σ=0.01 -> Cp=1.667. Cp≥1.33 is generally considered acceptable.",
        "Specification 9.95-10.05, σ=0.01 -> Cp=1.667.",
        "Cp≥1.33 is generally considered acceptable.",
        "📚 In-Depth Analysis: Cp Process Capability Calculator",
        "Assess the potential capability of a process to meet specification requirements while in statistical control, looking only at specification width and process dispersion, ignoring whether the mean is centered.",
        "When trial-producing a new product or accepting equipment, use short-term data (usually 25-50 subgroups) to estimate process σ and judge whether the process has the basic capability to meet tolerances.",
        "Compare the 'inherent' machining precision of different suppliers or production lines (independent of mean position).",
        "Formula and judgement",
        "Cp = (USL - LSL) / (6σ), where σ is the process",
        "(for capability study the within-subgroup standard deviation is used, not the overall standard deviation); 6σ represents the process natural tolerance (±3σ). Judgement: Cp ≥ 1.67 is over-capable (tolerances may be relaxed or cost reduced); 1.33 ≤ Cp < 1.67 adequate; 1.00 ≤ Cp < 1.33 marginal; Cp < 1.00 inadequate and needs improvement. Note Cp does not reflect mean shift; when the mean is off-center, use Cpk.",
        "Shaft diameter spec 10±0.05 mm, i.e. USL=10.05, LSL=9.95, process σ=0.01: Cp = (10.05-9.95)/(6×0.01) = 0.10/0.06 ≈ 1.667, above 1.33 and close to 1.67, capability adequate. If process variation expands to σ=0.02, then Cp = 0.10/0.12 ≈ 0.833 < 1.00, capability clearly insufficient; prioritize reducing dispersion (rather than adjusting the mean).",
        "What is the difference between Cp and Cpk?",
        "Cp only looks at specification width and process dispersion, assuming the process mean is exactly centered; Cpk additionally accounts for the mean's shift relative to the specification center, representing the actually achievable capability. When the mean is centered, Cpk=Cp; the larger the shift, the smaller the Cpk, so Cpk is the more conservative and more commonly used criterion.",
        "Which σ is used in the formula?",
        "Process capability study uses the 'within-subgroup standard deviation' (e.g. subgroup range method, moving range method), representing short-term, inherent variation; do not use the overall standard deviation that includes special causes, otherwise variation is overestimated and capability underestimated. For long-term performance Pp/Ppk, the overall standard deviation is used.",
    ]))

    write('cpk-index', build('cpk-index', [
        "Cpk Process Capability Calculator",
        "A capability index that simultaneously accounts for process centering shift.",
        "/ Process Capability Index Cpk",
        "Process Capability Index Cpk",
        "📖 View the \"Cpk Process Capability Calculator User Guide\"",
        "Cpk=Cp. Cpk≥1.33 means process capability is adequate.",
        "When the center is unshifted, Cpk=Cp.",
        "Cpk≥1.33 means process capability is adequate.",
        "📚 In-Depth Analysis: Cpk Process Capability Calculator",
        "Beyond Cp, it further incorporates mean shift to give the process's actual ability to stably produce conforming product, and is the single most commonly used criterion for supplier qualification and customer acceptance.",
        "When the process mean deviates from the specification center due to equipment wear, temperature drift, etc., use Cpk to quantify the conforming-rate loss caused by the shift.",
        "Monitor capability changes before and after improvement measures (e.g. re-tooling, leveling fixtures) to verify that correction is effective.",
        "Formula and judgement",
        "Cpk = min[(USL - μ)/(3σ), (μ - LSL)/(3σ)], taking the smaller of the upper and lower one-sided capability indices, representing the side suppressed by the shift. σ is the within-subgroup",
        ", μ is the process mean. Judgement: Cpk ≥ 1.33 adequate capability (most automotive industry requires ≥1.33 or higher); 1.00 ≤ Cpk < 1.33 marginal; Cpk < 1.00 inadequate and needs improvement; Cpk ≥ 2.0 is Six Sigma level (with 1.5σ shift corresponding to about 3.4",
        "Shaft diameter spec 10±0.05 (USL=10.05, LSL=9.95), μ=10.0, σ=0.01: Cpk = min[(10.05-10.0)/(3×0.01), (10.0-9.95)/(3×0.01)] = min[0.05/0.03, 0.05/0.03] = min[1.667, 1.667] = 1.667, the mean is centered so it equals Cp. If tool wear shifts μ to 10.02: Cpk = min[(10.05-10.02)/0.03, (10.02-9.95)/0.03] = min[1.000, 2.333] = 1.000; even though dispersion is unchanged, the shift has dropped capability below 1.33.",
        "Why does Cpk take the minimum of the two?",
        "The process can only be judged by the 'more constrained side': if the mean is high, the risk of exceeding the upper limit is greater; if low, the risk of falling below the lower limit is greater. Taking min conservatively treats the worst side as the overall capability, avoiding being masked by the good-looking number on the other side.",
        "How high must Cpk be to be considered acceptable?",
        "There is no universal hard rule; it depends on the industry and customer: general manufacturing ≥1.33, automotive/medical/aerospace often require ≥1.67, critical safety parts higher. Below 1.0 is usually considered a non-conforming process that must be corrected before batch delivery.",
    ]))

    write('cpk-with-shift', build('cpk-with-shift', [
        "Cpk with Shift Calculator",
        "Capability after the process mean shifts by δ relative to the center.",
        "/ Cpk with Shift",
        "Cpk with Shift",
        "📖 View the \"Cpk with Shift Calculator User Guide\"",
        "When δ=0 it returns to the original Cpk.",
        "Nominal center",
        "Shift amount δ",
        "Shift reduces Cpk.",
        "📚 In-Depth Analysis: Cpk with Shift Calculator",
        "Given the known 'nominal value' and measured 'shift amount' (e.g. fixture tooling error, positioning deviation), derive the actual mean directly from nominal + shift, then compute the shifted Cpk.",
        "At the design stage, do robustness assessment: given the allowed shift upper limit, back-calculate the required process σ to meet the target Cpk.",
        "Compare the gap between 'centered capability' and 'actual shifted capability' as a basis for correction priority.",
        "Actual mean μ = nominal value + shift amount (shift amount can be positive or negative, representing the systematic deviation relative to nominal); Cpk = min[(USL - μ)/(3σ), (μ - LSL)/(3σ)]. This tool substitutes 'nominal + shift' as μ, saving the step of measuring the mean first.",
        "Nominal 10.0, shift 0.02 -> μ=10.02; spec USL=10.05, LSL=9.95, σ=0.01: Cpk = min[(10.05-10.02)/(3×0.01), (10.02-9.95)/(3×0.01)] = min[0.03/0.03, 0.07/0.03] = min[1.000, 2.333] = 1.000, actual mean μ=10.0200. Just a 0.02 mm shift pulls capability from 1.667 down to 1.0, showing this dimension is very sensitive to eccentricity; priority should be controlling the shift rather than further compressing σ.",
        "How is the shift amount obtained?",
        "The shift amount comes from tooling error, fixture positioning deviation or the long-term mean's deviation relative to nominal; it can be back-calculated from process data μ - nominal, or given by gauge/instrument calibration; it is a systematic deviation, not random variation.",
        "What is the difference between Cpk with shift and directly computing Cpk?",
        "Mathematically equivalent, only the input method differs: the ordinary Cpk tool takes 'measured mean μ', this tool takes 'nominal + shift amount', better suited to design review and shift-sensitivity analysis, avoiding running a round of mean measurement first.",
    ]))


if __name__ == '__main__':
    main()

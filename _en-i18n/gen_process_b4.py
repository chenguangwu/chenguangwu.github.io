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
    write('sigma-level', build('sigma-level', [
        "Sigma Level Calculator",
        "Convert defects per million opportunities into the long-term sigma level.",
        "/ Sigma Level",
        "Sigma Level",
        "📖 View the \"Sigma Level Calculator User Guide\"",
        "6σ corresponds to DPMO≈3.4.",
        "📚 In-Depth Analysis: Sigma Level Calculator",
        "Convert",
        " into the process sigma level (including 1.5σ long-term shift), for goal setting in Six Sigma projects and cross-process benchmarking.",
        "Before and after improvement, use the same DPMO→sigma mapping to intuitively show the capability leap 'from 3σ to 4σ'.",
        "Align capability level with customer / industry benchmarks (e.g. 3.4 DPMO = Six Sigma).",
        "First compute the good rate y = 1 - DPMO/10^6; from the standard-normal inverse function get the baseline Z_bench = Φ⁻¹(y); industry practice adds the 1.5σ long-term drift to get sigma level = Z_bench + 1.5. The 1.5σ is an empirical drift amount used to connect short-term capability and long-term performance.",
        "DPMO=6210 -> y = 1 - 6210/10^6 = 0.99379; Z_bench = Φ⁻¹(0.99379) ≈ 2.500; sigma level = 2.500 + 1.5 = 4.00. That is, this process is about a 4 sigma level. To reach Six Sigma (3.4 DPMO), DPMO must be reduced from 6210 to 3.4, a gap of about three orders of magnitude.",
        "Why add the 1.5σ shift?",
        "The long-term process mean drifts (about 1.5σ); adding the shift back maps 'long-term DPMO' to 'short-term sigma level', facilitating the use of the classic Six Sigma reference table (e.g. 3.4 DPMO = 6σ). If only communicating short-term capability, the shift may be omitted and Z_bench reported directly.",
        "Can the sigma level exceed 6?",
        "Yes. DPMO below 3.4 (e.g. 0.001 DPMO) corresponds to >6σ; but the Six Sigma system often takes 3.4 DPMO as the 'long-term' target of Six Sigma, with higher levels mostly used in ultra-precision fields such as semiconductors.",
    ]))

    write('tolerance-rss', build('tolerance-rss', [
        "Tolerance Stack-up Calculator (RSS)",
        "Use the root-sum-square method to estimate the statistical total tolerance of a linear dimension chain.",
        "/ Tolerance Stack-up (Statistical RSS)",
        "Tolerance Stack-up (Statistical RSS)",
        "📖 View the \"Tolerance Stack-up Calculator (RSS) User Guide\"",
        "√0.0725≈0.269. RSS is looser than worst case.",
        "RSS is looser than worst case.",
        "📚 In-Depth Analysis: Tolerance Stack-up Calculator (RSS)",
        "In dimension-chain / assembly-clearance analysis, use root-sum-square (Root Sum Square) to estimate the total variation after stacking multiple part tolerances, closer to statistical reality than worst case.",
        "Under mass production each part's error is approximately an independent random distribution; RSS gives the 'typical' total tolerance rather than an extreme value.",
        "On the premise of guaranteeing assembly function, use RSS to relax tolerances and reduce cost, rather than uniformly tightening per worst case.",
        "Total tolerance T = √(t1² + t2² + … + tn²), each ti being each component-ring tolerance (take absolute value when stacking in the same direction). RSS assumes the errors are mutually independent and approximately normal, giving the typical total variation at about 99.73% (±3σ) confidence.",
        "An assembly dimension chain consists of three segments with tolerances 0.1, 0.15, 0.2 mm respectively: T = √(0.1² + 0.15² + 0.2²) = √(0.01 + 0.0225 + 0.04) = √0.0725 ≈ 0.269 mm (RSS). Compared with the worst-case stacked 0.45 mm, RSS is significantly smaller, indicating that under mass production single-part tolerances can be appropriately relaxed without exceeding specs.",
        "How to choose between RSS and worst case (WC)?",
        "WC assumes all errors simultaneously take extreme values stacked in the same direction, giving an absolutely safe but over-tight total tolerance; RSS assumes independent randomness and gives a typical value. Use WC for single-piece / small-batch / safety-critical parts, and RSS is more economical under mass-production statistical process control.",
        "What is the premise of RSS?",
        "It requires each component error to be mutually independent and approximately normally distributed (or at least symmetric); if a systematic deviation exists (e.g. tools uniformly oversized), it should first be treated as a shift rather than random tolerance, otherwise RSS underestimates the true total error.",
    ]))

    write('tolerance-worst-case', build('tolerance-worst-case', [
        "Tolerance Stack-up Calculator (Worst Case)",
        "Total tolerance of a linear dimension chain under the worst case.",
        "/ Tolerance Stack-up (Worst Case)",
        "Tolerance Stack-up (Worst Case)",
        "📖 View the \"Tolerance Stack-up Calculator (Worst Case) User Guide\"",
        "0.2 = 0.45. Worst case is conservative.",
        "Worst case is conservative.",
        "📚 In-Depth Analysis: Tolerance Stack-up Calculator (Worst Case)",
        "In safety-critical, single-piece or small-batch assembly, use worst case (Worst Case) stacking to estimate the upper bound of total tolerance, guaranteeing 100% no out-of-spec.",
        "Compared with the RSS tool, evaluate the cost of 'tightening tolerances for absolute safety', assisting tolerance-allocation decisions.",
        "For limit-dimension checks required by contract / regulation, the guaranteed value must be given by the extreme-value method.",
        "Total tolerance T = t1 + t2 + … + tn, directly add each component-ring tolerance linearly (assuming all take extremes in the same direction). This method does not depend on distribution assumptions and gives a conservative upper bound.",
        "The same segment dimension-chain tolerances 0.1, 0.15, 0.2 mm stacked by worst case: T = 0.1 + 0.15 + 0.2 = 0.450 mm. This is much larger than RSS's 0.269 mm - meaning if WC is used to guarantee 100% conformance, each part must be controlled more tightly (or leave larger design clearance), at higher cost; mass-production scenarios usually switch to RSS for typical values.",
        "Does the worst-case method over-design?",
        "Yes. It assumes all errors simultaneously take same-direction extremes, an actual probability that is extremely low; controlling tolerances this way often leads to unnecessary high machining cost; it is only worthwhile when any out-of-spec is unacceptable (e.g. aviation, medical implants).",
        "Can it be mixed with RSS?",
        "You can divide labor: use addition/subtraction for systematic deviations (shifts), use RSS for random tolerances; you can also use WC for critical rings and RSS for non-critical rings in a hybrid tolerance allocation, balancing safety and cost.",
    ]))

    write('xbar-control-limits', build('xbar-control-limits', [
        "X-bar Control Limit Calculator",
        "The 3σ control limits of the subgroup-mean control chart.",
        "/ Mean Control Chart Limits",
        "Mean Control Chart Limits",
        "📖 View the \"X-bar Control Limit Calculator User Guide\"",
        "σ=2, n=5 -> limits ±2.683. σ/√n is the standard error of the mean.",
        "Grand mean (x-double-bar)",
        "50, σ=2, n=5 -> limits ±2.683.",
        "σ/√n is the standard error of the mean.",
        "📚 In-Depth Analysis: X-bar Control Limit Calculator",
        "Compute the center line CL and control limits UCL/LCL for the mean control chart (X-bar chart), monitoring whether the process mean is in control and whether there is special-cause variation.",
        "Before process-capability study, first confirm the process is stable (in control); otherwise the capability index is meaningless.",
        "When the subgroup size changes (different n), update the standard error and limits by √n.",
        "Standard error SE = σ/√n (σ is the process",
        ", n is the subgroup size); center line CL = μ (process target / mean); control limits UCL = μ + 3·SE, LCL = μ - 3·SE (3σ principle, corresponding to about 0.27% false-alarm rate). When σ is unknown, the subgroup range mean R̄/d₂ is often used for estimation.",
        "Process target μ=50, σ=2, subgroup size n=5: SE = 2/√5 ≈ 0.8944; UCL = 50 + 3×0.8944 ≈ 52.683, LCL = 50 - 3×0.8944 ≈ 47.317, CL = 50.000. If a subgroup mean falls outside [47.317, 52.683], it triggers an out-of-control signal; investigate the special cause rather than immediately adjusting the machine.",
        "Which σ is used in the formula?",
        "Control-chart limits are estimated with the 'inherent process standard deviation' (e.g. R̄/d₂ or S̄/c₄), reflecting common-cause variation under control; do not use the full-sample overall standard deviation (including special causes would exaggerate σ, widen the control limits and miss anomalies).",
        "Do larger subgroup size n make the control limits narrower?",
        "Yes. SE = σ/√n, larger n makes SE smaller and the control limits narrower, more sensitive to mean shift; but too large n increases detection lag and cost, conventionally 4-5, and critical processes may use larger subgroups.",
    ]))


if __name__ == '__main__':
    main()

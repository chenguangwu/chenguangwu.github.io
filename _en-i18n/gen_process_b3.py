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
    write('index', build('index', [
        "🏭 Process Control Tools",
        "Process Control",
        "Process Control Tools",
        "X-bar Control Limit Calculator",
        "The X-bar Control Limit Calculator computes the 3σ upper and lower control limits of the subgroup-mean control chart, suitable for monitoring mean stability and detecting out-of-control in statistical process control (SPC).",
        "Cpk with Shift Calculator",
        "The Cpk with Shift Calculator computes the actual capability index after the process mean shifts by δ relative to the center, suitable for accurate process-capability assessment when systematic deviation exists.",
        "Tolerance Stack-up Calculator (Worst Case)",
        "The Tolerance Stack-up Calculator (Worst Case) computes the total tolerance accumulation of a linear dimension chain under the worst case, suitable for tolerance design and clearance-risk estimation in mechanical assembly.",
        "Rolled Throughput Yield Calculator",
        "The Rolled Throughput Yield Calculator computes the overall first-pass yield of serially connected processes (each station's yield multiplied), suitable for comprehensive process-capability assessment of complex production lines.",
        "Cp Process Capability Calculator",
        "Enter the upper spec limit USL, lower spec limit LSL and process standard deviation σ; the tool computes the Cp process capability index, measuring the ratio of specification width to process dispersion (ignoring shift), to judge whether the process can stably meet tolerance requirements.",
        "Combined Uncertainty Calculator",
        "Enter each independent uncertainty component in turn (e.g. instrument, environment, method); the tool synthesizes them by the root-sum-square method (RSS) to obtain the combined standard uncertainty, and can multiply by a coverage factor to give the expanded uncertainty, used for error expression in test reports.",
        "Tolerance Stack-up Calculator (RSS)",
        "Enter the tolerance of each link in a linear dimension chain; the tool uses the root-sum-square (RSS) method to estimate the statistical total tolerance after assembly, closer to actual variation in mass production than the extreme-value method, assisting tolerance allocation and assemblability assessment.",
        "First Pass Yield Calculator",
        "FPY = good units / input units × 100%",
        "Cpk Process Capability Calculator",
        "The Cpk Process Capability Calculator accounts for process centering shift to find the capability index, entering mean, standard deviation and spec limits to output Cpk, suitable for Six Sigma and quality control.",
        "Pp Process Performance Calculator",
        "The Pp Process Performance Calculator finds the performance index under total process variation (versus specification width), suitable for long-term process-capability assessment and companion analysis with Ppk.",
        "Ppk Process Performance Calculator",
        "The Ppk Process Performance Calculator finds the long-term process-performance index accounting for centering shift, suitable for capability assessment of actual production data and supply-quality commitment.",
        "Sigma Level Calculator",
        "The Sigma Level Calculator converts defects per million opportunities (DPMO) into the long-term sigma level, suitable for process-capability benchmarking and improvement-target setting in Six Sigma projects.",
        "Out-of-Spec Probability Calculator",
        "The Out-of-Spec Probability Calculator finds the probability of exceeding the upper spec limit under the normal assumption, entering mean, standard deviation and USL to output the defect rate, suitable for process risk control.",
        "DPMO Calculator",
        "DPMO = defects / (units × opportunities) × 10^6",
        "About \"Process Control Tools\"",
        "The Process Control Tools collection includes 14 free online tools covering common calculation, conversion and query needs in process-control scenarios. Whether you are a practitioner, student or general user in the field, you can find ready-to-use handy tools here. All tools run purely on the front end, with no data uploaded to the server, protecting privacy and security.",
        "The process control tools included on this page (some representative tools):",
        "These tools help you quickly complete common process-control-related tasks without memorizing complex formulas or manual conversion; just enter to get results.",
        "Do the process control tools need download or registration?",
        "No. All process control tools on this page are pure front-end online tools; just open the web page to use them directly, no software installation, no account registration, and no data upload.",
        "Are the calculation results of the process control tools accurate? Is the data safe?",
        "The tools compute locally in your browser based on public mathematical formulas and general industry standards, with results available instantly. All calculations are completed locally on your device, and data is not uploaded to the server, ensuring privacy and security.",
    ]))

    write('pp-index', build('pp-index', [
        "Pp Process Performance Calculator",
        "A performance index measured by the long-term (overall) standard deviation.",
        "/ Process Performance Index Pp",
        "Process Performance Index Pp",
        "📖 View the \"Pp Process Performance Calculator User Guide\"",
        "Pp uses the overall standard deviation, including special causes.",
        "Pp is often lower than Cp.",
        "📚 In-Depth Analysis: Process Performance Calculator",
        "Using the overall",
        " (long-term) to assess the actual process performance Pp, reflecting whether the total variation including special causes can meet the specification.",
        "Compared with Cp (Pp uses overall σ, Cp uses within-subgroup σ); a large gap indicates the process has special causes and is not yet stable.",
        "Used as the performance metric for customer acceptance in long-term supply quality audits.",
        "Formula and judgement",
        "Pp = (USL - LSL) / (6σ_long), where σ_long is the overall standard deviation based on all historical data (including special-cause variation). Judgement threshold is the same as Cp: ≥1.33 adequate, <1.00 inadequate. Pp is usually ≤ Cp, because overall variation is not less than within-subgroup variation.",
        "Spec USL=10.05, LSL=9.95, long-term overall σ_long=0.015: Pp = (10.05-9.95)/(6×0.015) = 0.10/0.09 ≈ 1.111. If short-term within-subgroup σ=0.01 (corresponding Cp=1.667), then Pp(1.111) < Cp(1.667), the gap indicates the process is disturbed by special causes and stability needs improvement.",
        "How to choose between Pp and Cp?",
        "Cp/Cpk use within-subgroup standard deviation, representing 'short-term/inherent' capability, on the premise that the process is in control; Pp/Ppk use overall standard deviation, representing 'long-term/actual' performance. Supply audits often require both: only a process that is in control and also meets the long-term target is truly good.",
        "What does Pp smaller than Cp indicate?",
        "It means overall variation is greater than within-subgroup variation, with identifiable special causes present (e.g. shift differences, equipment drift, incoming-material variation); process stabilization (SPC control) should be done first, then capability improvement; otherwise the capability index is artificially inflated.",
    ]))

    write('ppk-index', build('ppk-index', [
        "Ppk Process Performance Calculator",
        "A long-term process-performance index accounting for shift.",
        "/ Process Performance Index Ppk",
        "Process Performance Index Ppk",
        "📖 View the \"Ppk Process Performance Calculator User Guide\"",
        "Ppk includes long-term variation and shift.",
        "Ppk≥1.33 is considered adequate performance.",
        "📚 In-Depth Analysis: Process Performance Calculator",
        "Using the overall",
        " (long-term) to assess the actual process performance Ppk, while incorporating mean shift, giving the long-term achievable conforming-product capability.",
        "Compared with Cpk: Ppk uses overall σ, Cpk uses within-subgroup σ; a large difference indicates long-term shift or special causes.",
        "Customer annual audits, PPAP, etc. use Ppk as a long-term quality-commitment metric.",
        "Formula and judgement",
        "Ppk = min[(USL - μ)/(3σ_long), (μ - LSL)/(3σ_long)], where σ_long is the overall standard deviation. Judgement: ≥1.33 long-term adequate, <1.00 inadequate. Ppk is usually ≤ Cpk.",
        "Spec USL=10.05, LSL=9.95, long-term mean μ=10.0, overall σ_long=0.015: Ppk = min[(10.05-10.0)/(3×0.015), (10.0-9.95)/(3×0.015)] = min[0.05/0.045, 0.05/0.045] = min[1.111, 1.111] = 1.111. If short-term Cpk=1.667, then Ppk<Cpk, indicating the long term needs further stabilization.",
        "What is the core difference between Ppk and Cpk?",
        "The only difference is the source of σ: Cpk uses within-subgroup (short-term) standard deviation, Ppk uses overall (long-term) standard deviation; both account for mean shift. Hence Ppk is closer to the customer's actual long-term received performance.",
        "Do customers want Ppk or Cpk?",
        "PPAP/annual audits mostly require Ppk (long-term commitment), while the process-development stage internally uses Cpk (short-term capability) to drive improvement; the safe approach is for both to meet the target with a small gap, indicating a process that is both capable and stable.",
    ]))

    write('rolled-throughput-yield', build('rolled-throughput-yield', [
        "Rolled Throughput Yield Calculator",
        "Overall first-pass yield when multiple processes are in series.",
        "/ Rolled Throughput Yield (RTY)",
        "Rolled Throughput Yield (RTY)",
        "📖 View the \"Rolled Throughput Yield Calculator User Guide\"",
        "98%×97%×99% ≈ 94.11%. More processes means lower RTY.",
        "Station 1 yield (%)",
        "Station 2 yield (%)",
        "Station 3 yield (%)",
        "More processes means lower RTY.",
        "📚 In-Depth Analysis: Rolled Throughput Yield Calculator",
        "Compute the 'first-pass straight-through rate' of a serially connected multi-process, exposing the intermediate rework hidden behind '100% final yield'.",
        "In Six Sigma, use RTY to back-infer the process",
        "sigma level",
        "and hidden cost, more sensitive than looking at final yield alone.",
        "Identify which process has the lowest FPY as the priority improvement step.",
        "RTY = FPY1 × FPY2 × … × FPYn, each FPY being each process's",
        "first pass yield",
        " (decimal). RTY must be ≤ any single-process FPY; more processes means more obvious decay.",
        "Three processes have first-pass yields of 98%, 97%, 99% respectively: RTY = 0.98 × 0.97 × 0.99 = 0.941094 ≈ 94.11% (decimal 0.9411). Even though each is close to 99%, after three in series the straight-through rate has fallen below 95%, indicating at least about 6% of units have undergone rework; the 97% process should be investigated.",
        "Where does RTY differ from final yield?",
        "Final yield usually counts 'final good / input', counting units good after rework as good; RTY only counts those good all the way from the first pass, so RTY ≤ final yield, and the difference is the volume of rework waste.",
        "Is RTY necessarily lower with more processes?",
        "As long as a single-process FPY<100% there is inevitable decay, positively correlated with the number of processes; to raise RTY either improve the single-process FPY (root cause) or reduce unnecessary processes (slim down), not hide front-end defects by end screening.",
    ]))


if __name__ == '__main__':
    main()

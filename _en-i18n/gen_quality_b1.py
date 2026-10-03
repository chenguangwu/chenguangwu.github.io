#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'quality')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'quality')
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
    out = {'slug': slug, 'industry': 'quality', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('calc-cpk', build('calc-cpk', [
        '📋 Process Capability Index (Cp/Cpk) Calculator',
        'Compute process capability indices Cp, Cpk and performance indices Pp, Ppk to assess whether the process meets specification requirements',
        'Core calculation formula (by input variables): min(Cpu, Cpl); min(Ppu, Ppl)',
        '📖 View the User Guide for Process Capability Index (Cp/Cpk) Calculator',
        'Manual input of mean / standard deviation',
        'Automatic calculation from raw data',
        'Standard deviation σ (overall)',
        'In manual mode Pp/Ppk and Cp/Cpk use the same σ; to distinguish within-group / overall variation, use the "Raw data" mode.',
        'Raw data (one value per line, or separated by comma / space)',
        'In raw-data mode: Cp/Cpk use within-group variation estimate (moving range MR/d2, d2=1.128); Pp/Ppk use overall standard deviation (sample n-1).',
        '📖 Formula: Cp = (USL−LSL)/(6σ); Cpk = min((USL−μ), (μ−LSL))/(3σ); Pp/Ppk same formula but use overall standard deviation. Rating reference: Cpk≥2.0 excellent; 1.67-2.0 superior; 1.33-1.67 qualified; 1.0-1.33 insufficient; <1.0 severely insufficient.',
        '📚 Deep Dive: Cp / Cpk and Pp / Ppk Process Capability Indices',
        'After trial production of a new product, evaluate whether the process can stably meet tolerance: manually fill the upper/lower spec limits, process mean and',
        'σ, or calculate automatically from raw data.',
        'To judge whether insufficient capability is from "too-wide tolerance / too-large variation" or "center shift" — compare the gap between Cp and Cpk to locate it.',
        'When customers audit the plant or submit PPAP, provide Cp/Cpk values and the corresponding',
        'to evidence that the process is in control.',
        'Effect of mean shift on Cpk',
        'Spec 9.90–10.10 mm, σ=0.02. Mean centered μ=10.00: Cp = 0.20/(6×0.02) = 1.667, Cpu=Cpl=0.10/(3×0.02)=1.667, Cpk=1.667, two-sided nonconforming about 0.00006% (about 0.6 DPMO). If the mean drifts to μ=10.04: Cpu=0.06/0.06=1.000, Cpl=0.14/0.06=2.333, Cpk drops to 1.000, nonconforming rises to about 2,700 DPMO — Cp unchanged, the problem is center shift, so center the equipment rather than reduce variation.',
        'What is the difference between Cp and Cpk?',
        'Cp=(USL−LSL)/6σ only measures variation relative to the tolerance band, ignoring position; Cpk takes the smaller of Cpu and Cpl, reflecting shift as well. High Cp but low Cpk means the process center is off.',
        'What Cpk is considered acceptable?',
        'Generally Cpk≥1.33 is sufficient capability (corresponding to about 63 DPMO), 1.00–1.33 is marginal and needs tighter control, <1.00 is insufficient and should be improved. Automotive and medical industries often require 1.67 or above.',
    ]))
    write('control-chart', build('control-chart', [
        '🧪 X-bar Control Chart Simulation and Rule Violation Detection',
        'Enter subgroup means and auto-draw the control chart, identifying abnormal patterns',
        'The X-bar Control Chart Simulation performs professional calculation and outputs results based on input parameters.',
        'Control chart simulation',
        '/ Control Chart Simulation',
        '📖 View the User Guide for X-bar Control Chart Simulation and Rule Violation Detection',
        'Subgroup means (comma or space separated)',
        'Simulate a data set',
        'Simulate process shift',
        'Copy violation results',
        '📖 Rule Violation Rules (based on control limits)',
        'Rule violation rules detected by this tool',
        'Rule 1: 1 point falls outside the 3σ control limits',
        'Rule 2: 9 consecutive points on the same side of the center line',
        'Rule 3: 6 consecutive points increasing or decreasing',
        'Rule 4: 14 consecutive points alternating up and down',
        'Rule 5: 2 of 3 consecutive points fall outside the same-side 2σ zone',
        'Control limits: UCL/LCL = x-bar ± 3σ/√n; σ_xbar = σ/√n. Any rule violation indicates an out-of-control process, and special causes should be investigated.',
        '📚 Deep Dive: X-bar Control Chart and Rule Violation',
        'Each day, sample by fixed subgroups and enter means, observe whether any point exceeds the ±3σ control limits to judge if the process is in control.',
        'After equipment adjustment or material change, re-enter a batch of data and verify the adjustment effect by whether the center line drifts.',
        'On-site training demo: use built-in simulation to generate normal and shifted data, explaining the violation rules.',
        'Control limits for 8 subgroup means',
        'Subgroup size n=4, process',
        'σ=2. Means 10.0,10.5,9.5,10.0,10.5,9.5,10.0,10.0: center line CL = 80.0÷8 = 10.000, standard error σ/√n = 2÷2 = 1.000, UCL = 10.000+3×1.000 = 13.000, LCL = 7.000, all 8 points fall within limits, judged stable. If the last 4 groups become 11.5,11.8,12.0,12.2, though still under 13.0, multiple consecutive points are on the same side of the center line, the tool will flag process shift per the violation rules.',
        'Are control limits and specification limits the same?',
        'No. Control limits UCL/LCL = mean ±3σ/√n are determined by the process own variation, used to judge whether in control; specification limits are given by customer or design requirements. In control is not the same as conforming.',
        'Why flag a violation when all points are within limits?',
        'Random distribution can also produce patterns like 7 consecutive points on the same side or consecutive rise/fall; these "non-random" patterns often appear before exceeding limits, so control chart violation detection looks beyond just limit breaches.',
        'About Control Chart Simulation',
        'Enter subgroup means and process standard deviation to auto-draw the X-bar control chart and identify process abnormal patterns by common violation rules.',
        'Auto-calculate UCL/CL/LCL',
        'Auto-detect 5 violation rules',
        'SVG chart highlights abnormal points',
        'Built-in controlled / shifted data simulation',
        'SPC process monitoring',
        'Statistical process training',
        'Control chart teaching demo',
    ]))
    write('convert-qualified-defect', build('convert-qualified-defect', [
        '🔄 Nonconforming Rate and PPM Converter',
        'Online tool for nonconforming rate and PPM conversion',
        '📖 View the User Guide for Nonconforming Rate and PPM Converter',
        'Nonconforming rate',
        'Milli-nonconforming rate',
        'Kilo-nonconforming rate',
        'Milli-PPM conversion',
        'Kilo-PPM conversion',
        '📚 Deep Dive: Nonconforming Rate and PPM Inter-conversion',
        'Convert the',
        'to a unified',
        'caliber, easing horizontal comparison of defect levels at different magnitudes.',
        'When writing quality reports, convert PPM back to percentage for non-quality departments to understand.',
        'Convert among different multiplier calibrations such as milli, kilo and hundred, avoiding mixed units in reports.',
        '0.35% nonconforming rate conversion',
        'Nonconforming rate 0.35% → decimal defect rate 0.0035 → PPM = 0.0035 × 10⁶ = 3,500 PPM. Reverse check: 3,500 PPM ÷ 10⁶ = 0.0035 = 0.35%. If converted to "per-mille" calibration it is 3.5‰, equivalent to 0.35%, and when merging reports always unify to the same multiplier before adding.',
        'How to convert PPM and percentage?',
        'PPM = nonconforming rate (%) × 10,000, i.e. 1% = 10,000 PPM; conversely PPM ÷ 10,000 = percentage.',
        'PPM and',
        'the same?',
        'No. PPM is by nonconforming units ÷ total inspected; DPMO is by defect count ÷ (units × opportunities per unit). When a product has multiple defect opportunities, DPMO better reflects true quality level.',
        'About the Nonconforming Rate and PPM Converter',
        'Nonconforming rate and PPM conversion. A free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.',
    ]))

if __name__ == '__main__':
    main()

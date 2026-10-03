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
    write('process-capability', build('process-capability', [
        '📋 Process Capability Index (Cp / Cpk) Calculator',
        'Calculate process capability indices, yield rate and nonconforming rate (DPMO)',
        'Core formula (by input variables): √(variance)',
        'Process Capability Index',
        '/ Process Capability Index',
        '📖 View the User Guide for Process Capability Index (Cp / Cpk) Calculator',
        'Enter parameters directly',
        'Calculate from data',
        'Standard deviation σ (short-term)',
        'Sample data (comma, space or newline separated)',
        '📖 Formulas and Interpretation',
        'Cp = (USL − LSL) / (6σ) — Potential process capability',
        'Cpu = (USL − μ) / (3σ) — Upper-side capability',
        'Cpl = (μ − LSL) / (3σ) — Lower-side capability',
        'Cpk = min(Cpu, Cpl) — Actual process capability',
        'Zbench = 3 × Cpk — Yield = Φ(Zbench)',
        'DPMO = (1 − Yield) × 1,000,000',
        'Cpk Interpretation Reference',
        'Cpk ≥ 1.67: Adequate capability (excellent)',
        '1.33 ≤ Cpk < 1.67: Capability acceptable',
        '1.00 ≤ Cpk < 1.33: Marginal capability, improvement needed',
        'Cpk < 1.00: Insufficient capability, immediate improvement required',
        '📚 Deep Dive: Process Capability Index Cp / Cpk',
        'Given the upper/lower spec limits, automatically compute the mean and',
        ', and output Cp, Cpk and the yield rate.',
        'When you only have summary statistics (mean,',
        ') fill them in directly to quickly assess process capability.',
        'Convert Cpk into',
        'and short-term σ level, for your monthly quality report or customer report.',
        'Capability assessment of shaft diameter 10.00±0.05',
        'Sample (mm) 10.01, 9.99, 10.02, 10.00, 9.98, 10.03, 9.99, 10.01: mean 10.0038, sample standard deviation 0.0164 (divided by n−1). Spec 9.95–10.05: Cp = 0.10÷(6×0.0164) = 1.016; Cpu=(10.05−10.0038)÷(3×0.0164)=0.939, Cpl=(10.0038−9.95)÷(3×0.0164)=1.093, Cpk = 0.939 — marginal capability, and the lower Cpu indicates a shift toward the upper limit; the mean should be lowered by about 0.004 mm or the variation compressed directly.',
        'Use n or n−1 for sample standard deviation?',
        'The tool uses n−1 for sample data (unbiased estimate). This is consistent with the short-term σ estimate commonly used in process capability analysis; if you have a known process σ, please enter it in the manual input mode.',
        'Cpk is high but customer complaints persist, why?',
        'Cpk assumes the data are normal and the process is stable. If there are bimodal distributions, measurement system error or spec misinterpretation, the index becomes distorted. In such cases, judge together with control charts and gauge R&R.',
        'About the Process Capability Index',
        'Calculate process capability indices Cp, Cpk, Cpu, Cpl, estimate two-sided yield rate and DPMO, support direct parameter input or compute mean and standard deviation from sample data.',
        'One-click Cp/Cpk/Cpu/Cpl calculation',
        'Automatic statistics from sample data',
        'Yield rate and DPMO estimation',
        'Cpk rating and improvement suggestions',
        'Process capability assessment',
        'SPC process improvement',
        'Quality review reporting',
        'How to use the Process Capability Index (Cp / Cpk) Calculator',
        'What does the Process Capability Index (Cp / Cpk) Calculator do?',
        'Enter the upper/lower spec limits, process mean and standard deviation; the tool computes Cp and the shift-adjusted Cpk, and converts to the yield rate and defects per million opportunities (DPMO), helping quality engineers assess how well the process meets the tolerance.',
        'How to use the Process Capability Index (Cp / Cpk) Calculator?',
        'Which scenarios is the Process Capability Index (Cp / Cpk) Calculator suitable for?',
        'E.g.: 10.1, 9.9, 10.0, 10.2, 9.8, 10.0',
    ]))
    write('six-sigma', build('six-sigma', [
        '🔮 Six Sigma Level Estimator',
        'Convert between DPMO and sigma level (with 1.5σ long-term shift)',
        'The DPMO ↔ sigma level (with 1.5σ long-term shift) converter performs professional calculation and outputs results based on input parameters.',
        'Six Sigma Estimator',
        '/ Six Sigma Estimator',
        '📖 View the User Guide for Six Sigma Level Estimator',
        'Yield rate (%)',
        'Short-term sigma level σ (with 1.5 shift baseline)',
        '📖 Sigma Level Reference Table (with 1.5σ shift)',
        'Note: the long-term shift is assumed to be 1.5σ. Short-term level = long-term level + 1.5. Six Sigma (short-term 6σ) corresponds to a long-term 3.4 DPMO.',
        '📚 Deep Dive: Six Sigma Level and DPMO Inter-conversion',
        'Given',
        'find the corresponding',
        'sigma level',
        'and yield rate, for benchmarking quality maturity.',
        'Given a target σ level, back-calculate the allowable DPMO and nonconforming count as improvement goals.',
        'Use the reference table to quickly locate how far the current level is from 6σ (3.4 DPMO).',
        'What sigma level corresponds to DPMO 6,210',
        'DPMO = 6,210 → yield rate = 1 − 6,210/10⁶ = 99.379%, from the standard normal the long-term Z ≈ 2.50σ, after adding the 1.5σ shift the short-term level ≈ 4.00σ. For comparison: short-term 6σ corresponds to 3.4 DPMO (yield 99.99966%), short-term 4σ corresponds to 6,210 DPMO — the two differ by two levels, meaning the defect rate must drop by about 1,800×.',
        'Why is 6σ equal to 3.4 DPMO rather than 0.002?',
        'Below ±6σ the two-sided tail is only about 0.002 DPMO; but after accounting for the long-term 1.5σ shift, the one-sided tail becomes 3.4 DPMO, and the industry convention "6σ = 3.4 DPMO" refers to the long-term performance.',
        'How to convert between short-term and long-term levels?',
        'Short-term = long-term + 1.5. The DPMO input to the tool is treated as long-term performance, and the output sigma level is the short-term level; if your DPMO itself is short-term data, you need to subtract 1.5 before benchmarking.',
        'About the Six Sigma Estimator',
        'Convert among DPMO, yield rate and sigma level, using the 1.5σ long-term shift assumption, with a reference table and level assessment.',
        'DPMO / yield / σ three-way conversion',
        'Short/long-term level conversion',
        'Quality level and gap hints',
        'Sigma level reference table',
        'Six Sigma project assessment',
        'Quality goal setting',
        'Process capability benchmarking',
        'Quality training and teaching',
    ]))
    write('table-sampling', build('table-sampling', [
        '🎲 AQL Sampling Plan Lookup and Decision',
        'Online tool for AQL sampling plan lookup and decision',
        '📖 View the User Guide for AQL Sampling Plan Lookup and Decision',
        'AQL sampling plan (GB/T 2828.1 equivalent to ISO 2859-1): look up the sample-size code letter from the lot size and inspection level, then look up the sample size and Ac (acceptance number) and Re (rejection number) by the AQL value; if the number of defects does not exceed Ac it is accepted, and if it reaches or exceeds Re it is rejected; General Inspection Level II is the default, with tightened and reduced inspection switched per the switching rules.',
        '📚 Deep Dive: AQL Sampling Plan Lookup and Decision',
        'Before incoming inspection, look up the standard sampling plan by lot size and AQL value, to determine',
        'the code letter and acceptance/rejection numbers.',
        'For outgoing inspection, issue the sampling report at the customer-specified AQL (e.g. 0.65 or 1.0).',
        'After sampling finds a number of nonconforming items, look up the table to decide whether the lot is accepted or rejected, and give disposal suggestions.',
        'Plan for lot size 3,200 and AQL 1.0',
        'General Inspection Level II: lot size 1,201–3,200 falls in code letter K, corresponding to a sample size of 125 pieces. Look up the AQL 1.0 column: acceptance number Ac=3, rejection number Re=4, i.e. among 125 sampled, ≤3 nonconforming is accepted and ≥4 is rejected. If AQL 0.65 is used instead, under the same sample size Ac=2, Re=3, stricter; if the lot size rises to 10,001–35,000 the code letter becomes M and the sample size 315 pieces.',
        'How to choose the AQL value?',
        'AQL is the worst acceptable process average, determined by product risk and customer agreement: general consumer goods commonly use 1.0–2.5, critical safety parts use 0.065–0.25. The smaller the AQL, the stricter the sample size or acceptance number.',
        'What determines the sample-size code letter?',
        'It is jointly determined by the lot-size range and inspection level (GB/T 2828.1 / ISO 2859-1). Level II is the default; Level I has a smaller sample size (higher risk) and Level III larger.',
        'About the AQL Sampling Plan Lookup and Decision',
        'AQL sampling plan lookup and decision. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.',
        'Enter the content to query...',
    ]))

if __name__ == '__main__':
    main()

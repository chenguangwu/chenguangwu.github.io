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
    write('estimate-six-sigma', build('estimate-six-sigma', [
        '🔮 Sigma Level (σ) Estimator',
        'Estimate the process sigma level (with 1.5σ shift) and yield from DPMO or defect data',
        'Core calculation formula (by input variables): (defects × 1000000) ÷ (units × opps); (1 - dpmo÷1000000) × 100; 1 - dpmo÷1000000',
        '📖 View the User Guide for Sigma Level (σ) Estimator',
        'Enter DPMO directly',
        'Calculate from defect data',
        'DPMO (defects per million opportunities)',
        'Number of product units',
        'DPMO — Sigma Level Reference Table (with 1.5σ shift)',
        '📖 Sigma level = Z + 1.5 (short-term), where Z = normsinv(yield), yield = 1 − DPMO/1,000,000. Six Sigma (6σ) corresponds to 3.4 DPMO. The 1.5σ shift is the standard Six Sigma assumption.',
        '📚 Deep Dive: DPMO and Sigma Level Estimation',
        'From defect count, unit count and opportunities per unit compute',
        ', then convert to process',
        'sigma level',
        ', measuring quality maturity.',
        'Set improvement goals: back-calculate the DPMO and defect-count ceiling needed to reach 4σ or 6σ.',
        'Rank production lines / shifts horizontally by a unified σ level to identify the weakest link.',
        'Back-calculate sigma level from defect count',
        'Defects 24, products 5,000, opportunities per unit 8: DPMO = 24×10⁶ ÷ (5,000×8) = 600. Yield = 1 − 600/10⁶ = 99.94%, corresponding long-term Z ≈ 3.24σ; by the 1.5σ long-term shift, short-term sigma level ≈ 4.74σ. To reach short-term 6σ, DPMO must drop to about 3.4, i.e. defects from 24 to within 1.',
        'Why add the 1.5σ shift?',
        'Motorola practice found that long-running process means drift about 1.5σ relative to short-term, so short-term level = long-term level + 1.5. The industry saying "6σ = 3.4 DPMO" is derived from this.',
        'How to determine "opportunities per unit"?',
        'It is the total number of positions or inspection items on a product where defects may occur, e.g. a PCBA with 200 solder joints has 200 opportunities. The same production line should fix the calibration, otherwise DPMO is not comparable.',
        'How to use the Sigma Level (σ) Estimator',
        'What does the Sigma Level (σ) Estimator do?',
        'Input defect count, opportunity count and unit count to get DPMO, compute the process sigma level (with 1.5σ shift) and corresponding yield, for Six Sigma management and manufacturing process capability improvement evaluation.',
        'How to use the Sigma Level (σ) Estimator?',
        'What scenarios is the Sigma Level (σ) Estimator suitable for?',
    ]))
    write('index', build('index', [
        '✅ Quality Management Tools',
        'Quality Management',
        'Quality Management Tools',
        'PPM Conversion (nonconforming rate ↔ defects per million)',
        'Process Capability Index (Cp/Cpk) Calculator',
        'Compute process capability indices Cp, Cpk and performance indices Pp, Ppk to assess whether the process meets specification requirements',
        'Nonconforming Rate and PPM Converter',
        'The Nonconforming Rate and PPM Converter inter-converts nonconforming rate, defect rate and parts-per-million (PPM), suitable for unified expression in quality reports, supplier incoming material and process defects.',
        'Sigma Level (σ) Estimator',
        'Input defect count, opportunity count and unit count to get DPMO, compute the process sigma level (with 1.5σ shift) and corresponding yield, for Six Sigma management and manufacturing process capability improvement evaluation.',
        'Six Sigma Estimator',
        'Enter DPMO or sigma level; the tool converts between them including the 1.5σ long-term shift, giving the corresponding grade (e.g. world-class 6σ), for measuring process quality maturity and setting improvement goals.',
        'Process Capability Index',
        'Process Capability Index Cp / Cpk Calculator',
        'AQL Sampling Plan Lookup and Decision',
        'The AQL Sampling Plan Lookup and Decision tool looks up the standard sampling plan by acceptance quality limit and gives accept/reject decision, suitable for determining sampling plans in incoming and outgoing inspection.',
        'Control Chart Simulation',
        'X-bar Control Chart Simulation and Rule Violation Detection',
        'About Quality Management Tools',
        'The Quality Management Tools collection includes 8 free online tools covering common calculation, conversion and lookup needs in quality management scenarios. Whether you are a practitioner, student or ordinary user in the field, you can find ready-to-use small tools here. All tools run purely front-end, no data uploaded to the server, protecting your privacy and security.',
        'The quality management tools on this page include (representative selection):',
        'These tools help you quickly complete common quality-management tasks without memorizing complex formulas or manual conversion; just enter to get results.',
        'Do the quality management tools need to be downloaded or registered?',
        'No. All quality management tools on this page are pure front-end online tools; open the page to use directly, no software install, no account registration, no data upload.',
        'Are the quality management tool results accurate? Is the data safe?',
        'The tools compute locally in your browser based on public math formulas and general industry standards, with results instantly available. All computation is done locally on your device; data is never uploaded to the server, and your privacy and security are protected.',
    ]))
    write('ppm-calculator', build('ppm-calculator', [
        '🔄 PPM Conversion (nonconforming rate ↔ defects per million)',
        'Enter a value in any input box and the rest convert automatically',
        'The PPM Conversion performs professional calculation and outputs results based on input parameters.',
        '/ PPM Conversion',
        '📖 View the User Guide for PPM Conversion (nonconforming rate ↔ defects per million)',
        'Convert by count',
        'Convert by ratio',
        'Nonconforming count d',
        'Total inspected N',
        'Nonconforming rate (%)',
        'Defect rate (decimal, e.g. 0.0015)',
        'PPM (parts per million)',
        '📖 Conversion relations',
        'Percentage % = (d / N) × 100',
        'Defect rate (decimal) = d / N = PPM / 1,000,000 = % / 100',
        'DPMO = defect count / opportunities × 1,000,000 (defined separately when opportunities ≠ product count)',
        'Common reference',
        '3.4 PPM ≈ Six Sigma (with 1.5σ shift) long-term quality level',
        '📚 Deep Dive: PPM Conversion (nonconforming rate ↔ defects per million)',
        'After incoming inspection, fill nonconforming count d and total inspected N to get at once',
        ', decimal defect rate, PPM and',
        'When customers require quality goals in PPM, convert the internal percentage calibration over.',
        'Given a target PPM, back-calculate the allowed nonconforming count, for setting sampling release criteria.',
        '12 nonconforming among 8,000',
        'd=12, N=8,000: nonconforming rate = 12÷8,000×100 = 0.15%, decimal defect rate 0.0015, PPM = 0.0015×10⁶ = 1,500. If each unit has 5 defect opportunities, DPMO = 12÷(8,000×5)×10⁶ = 300. Reverse: when target PPM ≤ 1,000, 8,000 units allow at most 8 nonconforming.',
        'Do all six fields need to be filled?',
        'No. Fill any one item (nonconforming count + total, percentage, decimal defect rate, PPM or DPMO), and the rest auto-link and compute, suitable for back-deriving other calibrations from a known one.',
        'What is the difference between PPM and DPMO?',
        'PPM is the nonconforming units as parts per million of total inspected; DPMO is defects as parts per million of "units × opportunities". Scenarios with multiple defect opportunities use DPMO for better accuracy.',
        'About PPM Conversion',
        'Two-way conversion among nonconforming rate, PPM (parts per million), percentage and DPMO, and estimation of the corresponding sigma level.',
        'Dual mode: count conversion and ratio conversion',
        'Any input auto-links',
        'Sigma level estimation',
        'Quality metric conversion',
        'Supplier quality assessment',
        'Quality report compilation',
    ]))

if __name__ == '__main__':
    main()

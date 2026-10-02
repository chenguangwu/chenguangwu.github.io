#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'tcm-chemistry')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'tcm-chemistry')
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
    out = {'slug': slug, 'industry': 'tcm-chemistry', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
DISCL_M = " A professional medical tool based on authoritative medical standards, for reference only."

def main():
    write('granule-quality', build('granule-quality', [
        "\u2696\ufe0f Granule (Particle Size / Moisture) Quality Controller",
        "Particle size distribution analysis, moisture determination and overall quality evaluation of granules (referencing Chinese Pharmacopoeia standards)",
        "Particle size distribution analysis, moisture determination and overall quality evaluation of granules (referencing Chinese Pharmacopoeia standards).",
        "/ Granule quality control",
        "Particle size distribution",
        "Overall quality control",
        "Pharmacopoeia standard",
        "Sieve analysis of particle size distribution",
        "Enter the amount retained on each sieve to compute the particle size distribution and uniformity",
        "Total sample mass (g)",
        "Granule type",
        "General granules",
        "Soluble / suspension granules",
        "Effervescent granules",
        "Amount retained on each sieve (g)",
        "Above sieve 1 (2000 um)",
        "Sieve 2 (850 um) to sieve 1",
        "Sieve 3 (355 um) to sieve 2",
        "Sieve 4 (250 um) to sieve 3",
        "Sieve 5 (180 um) to sieve 4",
        "Below sieve 5 (180 um) (fine powder)",
        "\U0001F9EA Analyze the particle size",
        "Overall quality evaluation",
        "Moisture (%)",
        "Solubility (soluble granules)",
        "Fully dissolved, no turbidity",
        "Slight turbidity",
        "Turbid / insoluble",
        "Fill weight RSD (%)",
        "Labelled content (%)",
        "Microbial limits",
        "Complies with the specification",
        "Does not comply with the specification",
        "Particle size (coarse grains + fine powder total %)",
        "\U0001F9EA Overall evaluation",
        "Chinese Pharmacopoeia granule quality standard",
        "Granules should be dry and uniform in color, with no moisture absorption, softening or caking.",
        "Particle size",
        "The total of material not passing sieve 1 (2000 um) and passing sieve 5 (180 um) must not exceed 15% of the test portion.",
        "Moisture",
        "General granules: not more than 6.0%",
        "Effervescent granules: not more than 0.5%",
        "(measured by the prescribed method)",
        "Solubility",
        "Soluble granules: should dissolve completely or show only slight turbidity, with no foreign matter",
        "Suspension granules: should be uniformly suspended",
        "Effervescent granules: should rapidly produce carbon dioxide and appear effervescent",
        "Fill weight difference",
        "Single-dose packages: no more than 2 packages may exceed the fill weight limit, and none may exceed the limit by one fold",
        "Labeled fill weight",
        "Fill weight limit",
        "1.0 g and below",
        "Above 1.0 g to 1.5 g",
        "Above 1.5 g to 6.0 g",
        "Above 6.0 g",
        "Total aerobic count: <=1000 cfu/g",
        "Total mold and yeast count: <=100 cfu/g",
        "Escherichia coli: not detected (1 g)",
        "Salmonella: not detected (10 g)",
        "\U0001F4DA In-depth analysis: granule particle size / moisture quality control",
        "Particle size distribution d50/d90",
        "Overall pass judgment",
        "Sieve fractions p1+p6 (coarse + fine) <=15% passes the sieve requirement; d50 about 600 um, d10 about 300 um, d90 about 1100 um give a uniformity d90/d10 of about 3.67.",
        "Overall judgment",
        "Moisture <=6%, solubility pass, RSD <=5%, content 95-105%, microbe pass, particle size <=15% means all six items pass and the batch is judged conforming.",
        "What is the particle size limit?",
        "Pharmacopoeia granules: the total of material not passing sieve 1 (10 mesh) and passing sieve 5 (80 mesh) must not exceed 15%.",
        "How is uniformity computed?",
        "Uniformity = d90/d10; the smaller it is the narrower the distribution; granules generally require a moderate value.",
        "About the Granule (Particle Size / Moisture) Quality Controller",
        "Granule particle size and moisture quality controller - particle size distribution analysis, moisture determination and overall quality evaluation of granules." + DISCL_M,
    ]))
    write('hplc-optimization', build('hplc-optimization', [
        "\u2764\ufe0f HPLC Condition Optimizer",
        "Computes key HPLC parameters such as retention time, theoretical plate count and resolution",
        "Computes key HPLC parameters such as retention time, theoretical plate count and resolution.",
        "/ HPLC condition optimization",
        "Retention time prediction",
        "Column efficiency calculation",
        "Resolution evaluation",
        "Column length (mm)",
        "Internal diameter (mm)",
        "Flow rate (mL/min)",
        "Dead time t0 (min)",
        "Capacity factor k' (retention factor)",
        "Gradient slope factor (gradient mode)",
        "\u2764\ufe0f Compute the retention time",
        "Retention time tR (min)",
        "Peak width W (min)",
        "Column length L (mm)",
        "\u2764\ufe0f Compute the column efficiency",
        "Retention time of peak 1 tR1 (min)",
        "Retention time of peak 2 tR2 (min)",
        "Base width of peak 1 W1 (min)",
        "Base width of peak 2 W2 (min)",
        "\u2764\ufe0f Compute the resolution",
        "\U0001F4DA In-depth analysis: HPLC condition optimization (retention / efficiency / resolution)",
        "Retention time tR",
        "Theoretical plate count N",
        "Resolution Rs",
        "Column efficiency",
        "t0 = 1 min and k = 5 gives tR = 6 min; peak width W = 0.3 min gives N = 16 x (6/0.3)^2 = 6400, and H = L/N = 250/6400 = 0.039 mm.",
        "Resolution",
        "tR1 = 6.0, tR2 = 6.8, W1 = W2 = 0.3: Rs = 2 x (6.8-6.0)/(0.3+0.3) = 2.67 above 1.5, baseline separation.",
        "What N counts as good?",
        "Analytical columns generally need N >= 10000 to pass and >= 20000 to be excellent; it relates to column length, particle size and flow rate.",
        "What is the Rs pass line?",
        "Rs >= 1.5 gives baseline separation and more accurate quantification.",
        "About the HPLC Condition Optimizer",
        "HPLC condition optimizer - high-performance liquid chromatography condition parameter optimization, including retention time prediction, column efficiency calculation and resolution evaluation." + DISCL_M,
        "0 = isocratic elution",
    ]))
    write('impurity-limit', build('impurity-limit', [
        "\U0001F33F Impurity Limit (TLC) Semi-Quantitative Estimator",
        "Computes the TLC impurity limit and evaluates whether the impurity level meets the standard",
        "Computes the TLC impurity limit and evaluates whether the impurity level meets the standard.",
        "/ Impurity limit semi-quantification",
        "Impurity limit calculation",
        "Semi-quantitative evaluation",
        "Standard reference",
        "Test sample mass (mg)",
        "Test sample solution volume (mL)",
        "Reference standard mass (mg)",
        "Reference standard solution volume (mL)",
        "Spotting volume - test sample (uL)",
        "Spotting volume - reference standard (uL)",
        "\U0001F33F Compute the limit",
        "TLC spot semi-quantitative evaluation",
        "Test sample spot color intensity (0-10)",
        "Reference spot color intensity (0-10)",
        "Reference spot concentration (ug/uL)",
        "Test sample spotting amount (ug)",
        "\U0001F33F Semi-quantitative evaluation",
        "TCM impurity limit standard reference",
        "\U0001F4DA In-depth analysis: impurity limit (TLC) semi-quantification",
        "Spotting volume ratio method",
        "Spot intensity ratio method",
        "Limit percentage",
        "Spotting volume ratio",
        "Sample 1.0 g made up to 10 mL and spotted 2 uL (0.2 mg of sample), reference 0.1 mg/mL spotted 2 uL (0.2 ug of reference): limit = (0.2 ug / 0.2 mg) x 100 = 0.1%.",
        "Intensity ratio method",
        "Sample spot intensity si = 120, reference spot intensity sti = 240, reference concentration stdC = 1 ug/uL, spotting 10 uL, sample mass 0.5 g; impurity amount = 1 x (120/240) = 0.5 ug/uL x 10 uL = 5 ug; limit = (5 ug / 500 mg) x 100 = 0.001%.",
        "Can TLC quantify?",
        "It is semi-quantitative and used for limit tests; precise quantification needs HPLC or GC.",
        "What are the assumptions of the spot intensity method?",
        "It assumes response is linear with amount and that spotting volumes on the same plate are consistent; otherwise a co-spotted reference correction is needed.",
        "About the Impurity Limit (TLC) Semi-Quantitative Estimator",
        "Impurity limit semi-quantitative estimator - a tool for TLC impurity limit calculation and semi-quantitative evaluation." + DISCL_M,
    ]))


if __name__ == '__main__':
    main()
#!/usr/bin/env python3
# gen_reproductive-medicine_head.py — shared head for reproductive-medicine batches b1..bN
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'reproductive-medicine')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'reproductive-medicine')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
DISCL = "Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected."
EXTRA = {
    'sperm-concentration': {"稀释倍数 D（1:X）": "Dilution factor D (1:X)"},
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
    out = {'slug': slug, 'industry': 'reproductive-medicine', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('retrograde-ejaculation', build('retrograde-ejaculation', [
        "\U0001F50D Retrograde Ejaculation Detector",
        "Assesses retrograde ejaculation severity based on post-ejaculation urinary sperm count and semen volume",
        "Retrograde Ejaculation (Urinary Sperm) Detector",
        'View "Retrograde Ejaculation Detector User Guide"',
        "Retrograde ejaculation assessment: semen total sperm = semen volume x concentration; urine total sperm = urine volume x concentration; retrograde ratio = urine sperm / (semen + urine sperm) x 100%; >=70% suggests retrograde ejaculation.",
        "Determination: sperm found in post-ejaculation urine centrifuge sediment suggests retrograde ejaculation; a higher urine sperm proportion means more severe.",
        "Antegrade semen volume (mL)",
        "Antegrade semen concentration (x10^6/mL)",
        "Post-ejaculation urine volume (mL)",
        "Urine sperm concentration (x10^6/mL)",
        "\U0001F4CB Retrograde Ejaculation Criteria",
        "Urinary sperm",
        "No retrograde ejaculation",
        "Small amount of sperm",
        "Partial retrograde",
        "Mild retrograde ejaculation",
        "Complete retrograde",
        "Complete retrograde ejaculation",
        "\U0001F52C Testing and Management Points",
        "Testing",
        ": urinate immediately after ejaculation, centrifuge sediment and examine under microscope for sperm",
        "Etiology",
        ": diabetic neuropathy, prostate / bladder neck surgery, alpha-blockers, spinal cord injury",
        "Management",
        ": alkalinize urine, stop related drugs, sympathomimetic drugs to induce antegrade ejaculation",
        "Sperm retrieval",
        ": recover sperm from urine for ART, ensuring urine pH and osmolarity",
        "Tip: the low pH and high osmolarity of urine damage sperm; it is recommended to empty the bladder before testing and take sodium bicarbonate to alkalinize the urine. For learning reference only.",
        "\U0001F4DA In-Depth: Retrograde Ejaculation Severity",
        "Post-ejaculation urine sperm proportion.",
        "Complete / partial retrograde determination.",
        "Sperm retrieval strategy selection.",
        "Semen 0.5mL x10, urine 40mL x3",
        "semenTotal=5, urineTotal=120, total 125x10^6; urine proportion=120/125x100%=96%: nearly complete retrograde.",
        "Urine proportion 20%",
        "Urine 20%: partial retrograde; antegrade semen can still achieve natural conception; recover urinary sperm if needed.",
        "Relation to detector-9?",
        "Both use the same algorithm (urine sperm proportion); this tool focuses on severity grading and management suggestions.",
        "Can one still have children?",
        "Even complete retrograde can recover sperm from urine for IUI / ICSI assisted pregnancy.",
        'About "Retrograde Ejaculation (Urinary Sperm) Detector"',
        "The Retrograde Ejaculation (Urinary Sperm) Detector evaluates retrograde ejaculation severity based on post-ejaculation urine centrifuged sperm count and semen volume, calculating antegrade / retrograde sperm distribution. A professional medical tool based on authoritative medical standards, for reference only.",
        "How to use the Retrograde Ejaculation Detector",
        "What does the Retrograde Ejaculation Detector do?",
        "Enter the sperm count in centrifuged post-ejaculation urine and semen volume; the tool assesses the severity of retrograde ejaculation (mild / moderate / severe) and compares with normal semen volume to determine whether a large number of sperm flow back into the bladder, for andrological efficacy follow-up and diagnosis.",
        "How do I use the Retrograde Ejaculation Detector?",
        "Which scenarios suit the Retrograde Ejaculation Detector?",
    ]))
    write('semen-volume', build('semen-volume', [
        "\U0001F4CB Semen Volume Assessor",
        "Compares with WHO 5th edition lower reference limit 1.5 mL and indicates etiologies of abnormal volume",
        'View "Semen Volume Assessor User Guide"',
        "Semen volume grading: 1.5-6 mL normal, >6 mL excessive (may dilute sperm), 1.0-1.5 mL low, 0.5-1.0 mL hypospermia, <0.5 mL severe hypospermia; abstinence <2 days may underestimate semen volume.",
        "Abstinence days",
        "\U0001F4CB WHO 5th Edition Semen Volume Lower Reference Limit (1.5 mL)",
        "Etiology hint",
        "Confirm complete sampling and appropriate abstinence duration",
        "Hypospermia",
        "Investigate retrograde ejaculation, ejaculatory duct obstruction",
        "Severe hypospermia",
        "Investigate ejaculatory duct obstruction, seminal vesicle hypoplasia",
        "Excessive",
        "Seminal vesiculitis, accessory gland hypersecretion",
        "\U0001F52C Measurement and Sampling Points",
        "WHO recommends 2-7 days of abstinence; abstinence duration significantly affects semen volume",
        "The first fraction has the highest sperm density; loss affects both volume and concentration",
        "For low volume, check post-ejaculation urine centrifuge for sperm (rule out retrograde ejaculation)",
        "Excessive volume may dilute sperm concentration; assess by total sperm count if needed",
        "Tip: semen volume is affected by accessory gland (seminal vesicle, prostate) function. For abnormal results, combine semen pH, fructose, neutral alpha-glucosidase, etc. for comprehensive judgment.",
        "\U0001F4DA In-Depth: Semen Volume Assessment",
        "Relationship between abstinence days and volume.",
        "Hypospermia determination.",
        "Sampling standardization check.",
        "Volume 2.5 mL, abstinence 4 days",
        "Collection qualified with 2-7 days abstinence, volume 2.5 mL >= 1.4 mL normal.",
        "0.8 mL < 1.4 mL: hypospermia; rule out retrograde ejaculation and insufficient accessory gland secretion.",
        "WHO volume lower limit?",
        ">=1.4 mL; below this suggests incomplete collection or reduced secretion.",
        "How long abstinence is accurate?",
        "Recommend 2-7 days abstinence; too short lowers volume, too long lowers motility.",
        'About "Semen Volume Assessor"',
        "The Semen Volume Assessor interprets semen volume against the WHO 5th edition lower reference limit 1.5 mL, and indicates etiologies such as retrograde ejaculation, incomplete collection or ejaculatory duct obstruction for abnormal volume. A professional medical tool based on authoritative medical standards, for reference only.",
        "How to use the Semen Volume Assessor",
        "What does the Semen Volume Assessor do?",
        "Enter semen volume, interpret against the WHO 5th edition lower reference limit 1.5 mL, and indicate etiologies of abnormal volume.",
        "How do I use the Semen Volume Assessor?",
        "Which scenarios suit the Semen Volume Assessor?",
        "According to WHO 5th edition, the normal semen volume lower reference limit is",
        "; below this (hypospermia) may relate to incomplete collection, high ejaculation frequency or insufficient accessory gland secretion.",
        "A single result is affected by abstinence days and collection completeness; recheck after standard 2-7 days abstinence; very low volume combined with low concentration may indicate insufficient total sperm count.",
        "Applicability limits",
        "Semen volume is only one fertility indicator; combine with concentration, motility and morphology; results serve as andrological screening reference.",
    ]))
    write('sperm-concentration', build('sperm-concentration', [
        "\U0001F3CB\uFE0F Sperm Concentration Reference (WHO 5th Edition)",
        "Modified Neubauer counting chamber formula (each large square volume 0.1 mm3 = 10^-4 mL).",
        "Sperm Concentration (WHO 5th Edition) Reference",
        "/ Sperm Concentration Reference",
        'View "Sperm Concentration Reference (WHO 5th Edition) User Guide"',
        "Concentration (x10^6/mL) = (counted sperm / number of large squares) x dilution factor x 0.01",
        "Convert sperm concentration by modified Neubauer chamber method and interpret against the WHO 5th edition lower reference limit (15x10^6/mL)",
        "Formula: concentration (x10^6/mL) = (counted sperm / number of large squares) x dilution factor x 0.01",
        "Total counted sperm C (count)",
        "Number of counted large squares n (count)",
        "\U0001F4CB WHO 5th Edition Sperm Concentration Lower Reference Limit (5th percentile)",
        "Concentration above the lower reference limit",
        "Concentration below the lower reference limit",
        "Severe oligozoospermia",
        "Recommend recheck and further examination",
        "Cryptozoospermia",
        "Recheck after centrifuge sediment; biopsy if needed",
        "\U0001F52C Counting Principle",
        "Modified Neubauer chamber: each large square 1mm x 1mm, depth 0.1mm, volume 0.1uL",
        "For undiluted samples each large square represents 0.1uL, conversion factor x10^4/mL",
        "Count two independent diluted samples separately; acceptance limits follow the WHO duplicate-count table",
        "WHO recommends counting at least 200 sperm for accuracy",
        "Tip: this tool is for learning reference; concentration results are affected by counting error, dilution uniformity and sampling representativeness; clinical interpretation requires comprehensive assessment with semen volume, motility, morphology and other indicators.",
        "\U0001F4DA In-Depth: Sperm Concentration (Counting Chamber Method)",
        "Hemocytometer concentration calculation.",
        "Dilution factor correction.",
        "Oligo / azoospermia quantification.",
        "2 squares counted 200, dilution 10x",
        "Concentration=(C/n)xDx0.01=(200/2)x10x0.01=10x10^6/mL, near the lower reference limit.",
        "2 squares counted 600, dilution 10x",
        "Concentration=(600/2)x10x0.01=30x10^6/mL, above the >=16 reference.",
        "Formula meaning?",
        "C is the sperm count in the counted squares, n is the number of squares, D is the dilution factor; x0.01 is the chamber constant conversion.",
        "No sperm?",
        "Count 0 requires centrifuge sediment recheck; if still none, report azoospermia and further differentiate.",
        'About "Sperm Concentration (WHO 5th Edition) Reference"',
        "The Sperm Concentration (WHO 5th Edition) Reference converts sperm concentration (x10^6/mL) from the modified Neubauer chamber counted sperm, number of large squares and dilution factor, and interprets against the WHO 5th edition lower reference limit. A professional medical tool based on authoritative medical standards, for reference only.",
        "How to use the Sperm Concentration Reference (WHO 5th Edition)",
        "What does the Sperm Concentration Reference (WHO 5th Edition) do?",
        "Sperm Concentration Reference (WHO 5th Edition): enter the modified Neubauer chamber count result, number of counted large squares and dilution factor; it automatically converts sperm concentration (x10^6/mL) and interprets against the WHO 5th edition 15x10^6/mL lower reference limit for normality.",
        "How do I use the Sperm Concentration Reference (WHO 5th Edition)?",
        "Which scenarios suit the Sperm Concentration Reference (WHO 5th Edition)?",
    ]))

if __name__ == "__main__":
    main()

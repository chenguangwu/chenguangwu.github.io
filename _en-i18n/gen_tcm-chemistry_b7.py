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
    write('solubility-guide', build('solubility-guide', [
        "\U0001F4DA Active Component Solubility Lookup",
        "Look up the solubility of TCM active components in different solvents to guide extraction process design",
        "/ Active component solubility lookup",
        "Search component name",
        "\U0001F4CC Export the results",
        "Solubility grade explanation:",
        "Freely soluble (>=1 g/1 mL) > soluble (>=0.1 g/1 mL) > slightly soluble (>=0.01 g/1 mL) > sparingly soluble (<0.01 g/1 mL)",
        "\U0001F4DA In-depth analysis: active component solubility lookup",
        "Category search",
        "Solvent polarity table",
        "Solubility grade determination",
        "Alkaloids",
        "Free alkaloids are sparingly soluble in water and readily soluble in chloroform or diethyl ether; as salts (such as berberine hydrochloride) they are readily soluble in water and poorly soluble in organic solvents.",
        "Flavonoids / saponins",
        "Flavonoids are slightly soluble in cold water and readily soluble in hot alcohol; saponins are readily soluble in water or alcohol and poorly soluble in diethyl ether, and foam when shaken.",
        "What solubility grades exist?",
        "Five grades: freely soluble, soluble, slightly soluble, sparingly soluble and insoluble, classified by the amount of solvent needed for 1 g of solute.",
        "Why look up solubility?",
        "It guides solvent selection for extraction, purification, formulation dissolution and quality control.",
        "About the Active Component Solubility Lookup",
        "Active component solubility lookup - solubility data for Chinese medicine chemistry constituents, covering alkaloids, flavonoids, saponins and terpenes." + DISCL_M,
        "e.g. berberine, baicalin, ginsenoside...",
    ]))
    write('stability-test', build('stability-test', [
        "\U0001F9EE Stability (Light / Heat) Accelerated Test Calculator",
        "Predicts the shelf life of TCM preparations from the Arrhenius equation and designs accelerated test schemes",
        "Predicts the shelf life of TCM preparations from the Arrhenius equation and designs accelerated test schemes.",
        "/ Stability accelerated test",
        "Shelf life prediction",
        "Accelerated test design",
        "Q1E extrapolation",
        "Arrhenius equation shelf life prediction",
        "Accelerated temperature (C)",
        "Accelerated test time (months)",
        "Long-term storage temperature (C)",
        "\U0001F9EE Compute the shelf life",
        "Accelerated test condition design",
        "Long-term test",
        "Accelerated test",
        "Intermediate condition test",
        "Light stability test",
        "Packaging type",
        "Non-permeable packaging",
        "Semi-permeable packaging",
        "Light-protective packaging",
        "\U0001F9EA Generate the test scheme",
        "ICH Q1E extrapolation",
        "Degradation rate under accelerated conditions (%)",
        "Accelerated time (months)",
        "Degradation rate under intermediate conditions (%)",
        "Intermediate test time (months)",
        "Specification limit (%)",
        "\U0001F9EA Compute the extrapolated shelf life",
        "\U0001F4DA In-depth analysis: stability accelerated test (Arrhenius)",
        "Arrhenius shelf life",
        "ICH Q1A conditions",
        "Q1E extrapolation",
        "With Ea = 84 kJ/mol, R = 8.314, accelerated at 50 C (323.15 K) and storage at 25 C (298.15 K): ratio = exp(84000/8.314 x (1/298.15 - 1/323.15)) = exp(2.617) = 13.7; 6 months accelerated equals about 82 months at 25 C.",
        "ICH conditions",
        "Accelerated 40 C/75% RH for 6 months, long-term 25 C/60% RH for 12 to 36 months; light stability uses a total illuminance of at least 1.2x10^6 lux.h plus UV of at least 200 W.h/m2.",
        "What are the Arrhenius assumptions?",
        "A single degradation pathway with constant activation energy is assumed, and extrapolation only holds near the temperature range.",
        "What is Q1E extrapolation?",
        "When accelerated and intermediate condition data agree, the long-term shelf life can be extrapolated, and it requires",
        "statistical testing",
        "About the Stability (Light / Heat) Accelerated Test Calculator",
        "Stability accelerated test calculator - predicts drug shelf life from the Arrhenius equation, including accelerated test condition design." + DISCL_M,
    ]))
    write('structure-identification', build('structure-identification', [
        "\U0001F4CA Structure Identification (IR / UV / NMR) Data Interpreter",
        "Enter spectral data to automatically assign characteristic peaks and assist structure identification",
        "/ Structure identification interpretation",
        "Infrared IR",
        "Ultraviolet UV",
        "Nuclear magnetic resonance NMR",
        "Mass spectrometry MS",
        "Enter IR absorption peaks (cm-1), comma separated",
        "\U0001F4CA Interpret the IR data",
        "Enter UV absorption peaks (nm), comma separated",
        "Solvent",
        "Chloroform",
        "\U0001F4CA Interpret the UV data",
        "Enter 1H NMR chemical shifts (ppm), comma separated",
        "\U0001F4CA Interpret the NMR data",
        "Molecular ion peak m/z",
        "Main fragment peaks (comma separated)",
        "\U0001F4CA Interpret the MS data",
        "\U0001F4DA In-depth analysis: structure identification (IR / UV / NMR / MS) interpretation",
        "IR groups",
        "UV conjugation",
        "1H NMR chemical shift",
        "IR 1710 cm-1 corresponds to C=O and 3300 cm-1 to O-H; UV with lambda max around 270 nm indicates an aromatic ring conjugation; 1H NMR delta 2.3 corresponds to C=O-CH3.",
        "MS nitrogen rule",
        "A molecular ion peak M = 298 (even) means it contains zero or an even number of nitrogens; common losses of 15 (CH3), 18 (H2O) and 28 (CO) indicate the corresponding groups.",
        "What is the nitrogen rule?",
        "Organic molecules with no nitrogen or an even number of nitrogens have an even M; an odd nitrogen count gives an odd M.",
        "How is the structure determined by NMR?",
        "Chemical shift, splitting and integration are used together; delta 2 to 3 is mostly hydrogens next to a carbonyl or a benzylic hydrogen.",
        "About the Structure Identification (IR / UV / NMR) Data Interpreter",
        "Structure identification data interpreter - IR, UV, NMR and MS spectral data interpretation, an aid for identifying Chinese medicine chemical constituents." + DISCL_M,
    ]))
    write('toxicity-dose', build('toxicity-dose', [
        "\U0001F48A Toxic Dose (LD50) Converter",
        "Converts LD50 and equivalent doses between animal species, with toxicity grade evaluation",
        "Converts LD50 and equivalent doses between animal species, with toxicity grade evaluation.",
        "/ Toxic dose conversion",
        "Dose conversion",
        "Toxicity grading",
        "Source animal species",
        "Mouse",
        "Rat",
        "Guinea pig",
        "Rabbit",
        "Target species",
        "LD50 dose (mg/kg)",
        "Conversion method",
        "Body surface area method (recommended)",
        "Body weight method (simple)",
        "Average human weight (kg)",
        "10 (general toxicity)",
        "100 (routine new drug)",
        "1000 (high toxicity / unknown)",
        "\U0001F48A Compute the equivalent dose",
        "LD50 value (mg/kg)",
        "Intraperitoneal injection",
        "Subcutaneous injection",
        "\U0001F9EA Toxicity grading",
        "\U0001F4DA In-depth analysis: toxic dose (LD50) conversion",
        "Species equivalent dose",
        "Human MRD starting dose",
        "Oral / intravenous differences",
        "Mouse to human BSA",
        "Mouse LD50 = 200 mg/kg, KM mouse = 3 and human = 37; HED = 200 x (3/37) = 16.2 mg/kg; with SF = 10 the MRD = 1.62 mg/kg.",
        "A drug with an oral LD50 of 120 mg/kg (rat) falls in the low toxicity range (50 < LD50 <= 500); human use must be far below this and a safety factor applied.",
        "What are the LD50 grades?",
        "Oral rat: <=5 extremely toxic, 5 to 50 highly toxic, 50 to 500 low toxic, 500 to 5000 practically non-toxic.",
        "What safety factor is used?",
        "First-in-human studies commonly use 1/10 of the HED; with repeated-dose data, take NOAEL/10 and multiply by the species factor.",
        "About the Toxic Dose (LD50) Converter",
        "Toxic dose LD50 converter - dose conversion between animals and humans, including equivalent dose conversion across species." + DISCL_M,
    ]))


if __name__ == '__main__':
    main()
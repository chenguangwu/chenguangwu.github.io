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
    write('concentration-calc', build('concentration-calc', [
        "\U0001F321\ufe0f Concentration Temperature and Vacuum Calculator",
        "Boiling point calculation for a solution under reduced-pressure evaporation, protecting heat-sensitive active components",
        "Core formulas (from the input variables): vacuumNeeded / 750.062",
        "Concentration (reduced-pressure evaporation) temperature and vacuum calculator",
        "/ Concentration temperature calculation",
        "Boiling point calculation",
        "Reference data table",
        "Solvent type",
        "Water (boiling point 100 C)",
        "Ethanol (boiling point 78.4 C)",
        "Methanol (boiling point 64.7 C)",
        "Acetone (boiling point 56.5 C)",
        "Ethanol-water mixture (70%)",
        "Target evaporation temperature (C)",
        "Vacuum (mmHg, optional)",
        "Ambient atmospheric pressure (mmHg)",
        "Boiling point of water at different vacua",
        "Absolute pressure (mmHg)",
        "Vacuum (mmHg)",
        "Vacuum (MPa)",
        "Common process parameters:",
        "Concentration at 50-60 C: suitable for heat-sensitive components such as baicalin and volatile oils, vacuum about 0.08-0.09 MPa",
        "Concentration at 60-70 C: routine TCM concentration, vacuum about 0.07-0.08 MPa",
        "Concentration at 70-80 C: heat-resistant components with higher efficiency, vacuum about 0.05-0.06 MPa",
        "\U0001F4DA In-depth analysis: reduced-pressure concentration temperature and vacuum",
        "Antoine back-calculation of boiling point",
        "Vacuum to boiling point",
        "Protecting heat-sensitive components",
        "Water boiling point under vacuum",
        "At normal pressure 760 mmHg and vacuum 660 mmHg the absolute pressure is 100 mmHg; Antoine for water: T = 1730.63/(8.071-log10(100))-233.426 = 1730.63/(8.071-2)-233.426 is about 51.6 C.",
        "Lower vacuum",
        "Absolute pressure 50 mmHg gives T = 1730.63/(8.071-1.699)-233.426 = 1730.63/6.372-233.426, about 38.2 C, suitable for volatile oils and enzymes.",
        "What are the vacuum units?",
        "mmHg gauge pressure is common, and absolute pressure = atmospheric pressure - gauge pressure; 1 mmHg is about 0.1333 kPa, and 750 mmHg is about 0.1 MPa.",
        "Why concentrate under reduced pressure?",
        "Lowering the boiling point reduces damage to heat-sensitive components and shortens the heating time.",
        "About the Concentration (Reduced-Pressure Evaporation) Temperature and Vacuum Calculator",
        "Concentration temperature and vacuum calculator - reduced-pressure evaporation process parameter calculation, including boiling point to vacuum conversion for water and ethanol solutions." + DISCL_M,
        "Leave blank to compute automatically",
    ]))
    write('content-assay', build('content-assay', [
        "\u2696\ufe0f Content Assay (Reference Standard) Internal Standard Calculator",
        "Computes the active component content in Chinese medicine by the internal standard method, including the correction factor",
        "Computes the active component content in Chinese medicine by the internal standard method, including the correction factor.",
        "/ Internal standard method content calculation",
        "Correction factor calculation",
        "Content assay calculation",
        "Internal standard correction factor (f) calculation",
        "Reference standard mass (mg)",
        "Reference standard concentration (mg/mL)",
        "Internal standard mass (mg)",
        "Internal standard concentration (mg/mL)",
        "Reference standard peak area",
        "Internal standard peak area",
        "\u2696\ufe0f Compute the correction factor",
        "Sample assay",
        "Correction factor f",
        "Sample mass (mg)",
        "Internal standard amount in the sample (mg)",
        "Sample final volume (mL)",
        "Target peak area in the sample",
        "Internal standard peak area in the sample",
        "Loss on drying (%)",
        "\u2696\ufe0f Compute the content",
        "\U0001F4DA In-depth analysis: content assay (internal standard method) correction factor",
        "Internal standard method correction factor f",
        "Extract / loss on dry basis conversion",
        "Sample content percentage",
        "Internal standard peak area isArea = 500000, internal standard concentration isConc = 1 mg/mL, reference peak area stdArea = 520000, reference concentration stdConc = 1; f = (500000x1)/(520000x1) = 0.9615.",
        "Sample content",
        "Sample peak area 480000, internal standard peak area 500000, internal standard in the sample solution 1 mg/mL, sampled 1 mL, sample mass 0.5 g; target concentration = 0.9615 x (480000/500000) x 1 = 0.923 mg/mL, content = 0.923/0.5 x 100 = 184.6% (which drops after loss on drying conversion).",
        "Why use the internal standard method?",
        "Injection volume fluctuations are cancelled by the internal standard peak area ratio, so it tolerates injection-to-injection error better than the external standard method.",
        "How is loss on drying handled?",
        "Reported content is often on a dry basis: content(dry) = content(wet)/(1-LOD/100).",
        "About the Content Assay (Reference Standard) Internal Standard Calculator",
        "Content assay internal standard calculator - reference standard internal standard method assay computation, including the correction factor and content calculation." + DISCL_M,
        "0 = not dried",
    ]))
    write('crystallization-yield', build('crystallization-yield', [
        "\U0001F321\ufe0f Crystallization (Solvent/Temperature) Yield Predictor",
        "Predicts cooling crystallization yield from how solubility varies with temperature to optimize the crystallization process",
        "Core formulas (from the input variables): max(0, actualDissolved - remainLow); theoreticalCrystal x (1 - lossRate/100); (actualCrystal / feed) x 100",
        "/ Crystallization yield prediction",
        "Crystallization method",
        "Cooling crystallization",
        "Antisolvent crystallization",
        "Solvent evaporation crystallization",
        "Charge (g)",
        "Dissolution temperature (C)",
        "Crystallization temperature (C)",
        "Solubility at high temperature (g/100 mL solvent)",
        "Solubility at low temperature (g/100 mL solvent)",
        "Solvent volume (mL)",
        "Crystallization loss rate (%)",
        "\U0001F321\ufe0f Compute the yield",
        "Common crystallization solvent system reference:",
        "Baicalin: water-ethanol system, dissolves at 70 C and crystallizes at 5 C",
        "Berberine: methanol-water system, dissolve hot and crystallize on cooling",
        "Rutin: dissolved in boiling water, crystallizes on cooling",
        "Artemisinin: petroleum ether-ethyl acetate system, crystallizes at low temperature",
        "\U0001F4DA In-depth analysis: crystallization (cooling) yield prediction",
        "Solubility difference method",
        "Mother liquor remainder",
        "Yield and purity",
        "Charge 100 g, high-temperature solubility 20%, low-temperature 2%, solvent 1000 mL, loss 5%: solubility limit = 20x1000/100 = 200 g, actual dissolved 100 g, low-temperature remainder = 2x1000/100 = 20 g, theoretical crystal = 80 g, actual crystal = 80x0.95 = 76 g, yield 76%.",
        "Improving the yield",
        "Lowering the low-temperature solubility to 1% leaves 10 g, theoretical crystal 90 g, and the yield rises to about 85.5%.",
        "What about antisolvent crystallization?",
        "It lowers solubility by adding an antisolvent, following the same logic of solubility difference multiplied by total solvent volume.",
        "Why is the yield below theory?",
        "Mother liquor entrainment, adsorption on the vessel wall and filtration losses, converted as lossRate.",
        "About the Crystallization (Solvent/Temperature) Yield Predictor",
        "Crystallization yield predictor - predicts crystallization yield from solvent-temperature solubility data, including cooling crystallization and solvent evaporation crystallization computation." + DISCL_M,
    ]))


if __name__ == '__main__':
    main()
#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'paper')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'paper')
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
    out = {'slug': slug, 'industry': 'paper', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('naipo-dingpo-zhishu', build('naipo-dingpo-zhishu', [
        "📋 Burst (Puncture) Index",
        "Compute the burst (puncture) index from the burst strength and the grammage, for cross-comparison of the strength of paper and board.",
        "📖 View the usage guide for 'Burst (Puncture) Index'",
        "Burst index = burst strength ÷ grammage (kPa·m²/g); 1 kPa ≈ 0.0102 kgf/cm²",
        "The burst index is the burst strength divided by the grammage, allowing the puncture strength of paper and board to be compared across grammages; kgf/cm² is also converted and the deviation against the 3.0 kPa·m²/g reference is given.",
        "Burst strength (kPa)",
        "Sample grammage (g/m²)",
        "💡 Burst index = burst strength ÷ grammage (kPa·m²/g); 1 kPa ≈ 0.0102 kgf/cm²; the common reference is about 3.0 kPa·m²/g.",
        "📚 Deep Dive: Burst (Puncture) Index",
        "For linerboard and corrugated quality control: divide the burst strength by the grammage to get the burst index, compare the puncture strength across grammages, and judge whether the raw material strength meets the standard.",
        "For incoming supplier comparison: convert the burst strength of different suppliers to the same index basis, remove the grammage difference and then compare together with price.",
        "For lightweight scheme evaluation: reduce the grammage while keeping the burst index, to assess the strength risk after down-grammaging.",
        "Worked example: burst strength 350 kPa, grammage 80 g/m²",
        "Burst index = 350 ÷ 80 = 4.375 kPa·m²/g; converted 350 × 0.0102 = 3.57 kgf/cm²; deviation against the common reference 3.0 kPa·m²/g = (4.375 − 3.0) ÷ 3.0 × 100% = 45.83%.",
        "Should I look at burst strength or burst index?",
        "Burst strength is the measured absolute value (kPa) and is strongly affected by grammage; the burst index is the burst strength divided by the grammage, used to compare the strength of the material itself across grammages and batches, so procurement and quality control rely mainly on the index.",
        "How many kgf/cm² is 1 kPa?",
        "1 kPa ≈ 0.0102 kgf/cm² (that is, 1 kgf/cm² ≈ 98.07 kPa). Chinese paper mills conventionally use kgf/cm² while export orders often use kPa; this tool gives both conventions.",
        "About 'Burst (Puncture) Index'",
        "Burst (Puncture) Index. A free online tool processed entirely in the browser, no data uploaded, privacy and security protected.",
        "Score A",
        "Score B",
    ]))

    write('strength-9', build('strength-9', [
        "📄 Tear (Internal/Edge Tear) Strength",
        "Compute the tear index from the tear force and the sample grammage, to compare the tear resistance of paper and board across different grammages.",
        "📖 View the usage guide for 'Tear (Internal/Edge Tear) Strength'",
        "Tear index = tear force ÷ grammage (mN·m²/g); normalised tear force = tear force ÷ grammage × 100",
        "The tear index removes the effect of the grammage difference and is the comparable cross-section indicator of tear resistance; the normalised tear force per 100 g/m² and the deviation against the 8.0 reference are also given.",
        "Tear force (mN)",
        "Sample grammage (g/m²)",
        "💡 Tear index = tear force ÷ grammage (mN·m²/g); a higher index means better tear resistance; the common reference is about 8.0 mN·m²/g.",
        "📚 Deep Dive: Tear (Internal/Edge Tear) Strength",
        "For paper and board quality control: substitute the tear force and grammage to get the tear index, eliminating the grammage difference to compare the tear resistance of different grammage grades horizontally.",
        "For process suitability prediction: bagging, slitting and die-cutting steps pay attention to the tear index; a low index easily causes tears and linting during processing.",
        "For furnish and beating degree adjustment: re-measure the tear force after changing the furnish mix or beating degree, and use the change in the tear index to judge how much fibre length is retained.",
        "Worked example: tear force 750 mN, grammage 80 g/m²",
        "Tear index = 750 ÷ 80 = 9.375 mN·m²/g; normalised tear force per 100 g/m² = 750 ÷ 80 × 100 = 937.5 mN; deviation against the common reference 8.0 mN·m²/g = (9.375 − 8.0) ÷ 8.0 × 100% = 17.19%.",
        "What is the difference between internal tear and edge tear?",
        "Internal tear reflects the overall fibre bonding strength of the sheet, while edge tear is affected by the quality of the slitting cut edge; the two should be sampled and measured separately. The 1.5x internal tear reference force given by this tool is only for quick comparison, and the verdict still rests on the measured values of each specimen.",
        "Why divide by the grammage?",
        "Tear force grows with grammage, so comparing grades of different grammage directly leads to the wrong conclusion that 'thicker is tougher'; only after dividing by the grammage to get the tear index is it a comparable material indicator.",
        "About 'Tear (Internal/Edge Tear) Strength'",
        "Tear (Internal/Edge Tear) Strength. A free online tool processed entirely in the browser, no data uploaded, privacy and security protected.",
        "Internal tear",
        "Edge tear",
    ]))

    write('strength-10', build('strength-10', [
        "📄 Interlayer (Peel) Adhesion Strength",
        "Enter the peel force and the specimen width to compute the interlayer (peel) adhesion strength and assess the gap to common requirements.",
        "📖 View the usage guide for 'Interlayer (Peel) Adhesion Strength'",
        "Peel strength = peel force ÷ (specimen width ÷ 1000) = peel force × 1000 ÷ specimen width (N/m); 1 kN/m = 1000 N/m",
        "Converted per the GB/T peel test convention: first derive the peel strength per unit width from the peel force and specimen width, then convert to kN/m and N/cm and give the margin against the common requirement of 1.0 kN/m.",
        "Peel force (N)",
        "Specimen width (mm)",
        "💡 Peel strength = peel force × 1000 ÷ specimen width; 1 kN/m = 1000 N/m; the common requirement for packaging board is ≥ 1.0 kN/m.",
        "📚 Deep Dive: Interlayer (Peel) Adhesion Strength",
        "For coated paper, coated board and multi-ply board quality control: substitute the peel force and specimen width measured by the peel test, convert to peel strength per unit width (N/m, kN/m), and judge whether the interlayer bonding meets the internal control target.",
        "For incoming and finished product comparison: peel test specimen widths often differ between materials, so only after converting to strength per unit width can they be compared horizontally, removing the false differences caused by width.",
        "For verifying process adjustments: re-measure the peel force after changing the glue amount, press pressure or drying curve, and quantify the improvement by the margin against the 1.0 kN/m requirement.",
        "Worked example: peel force 180 N, specimen width 75 mm",
        "Peel strength = 180 × 1000 ÷ 75 = 2400.0 N/m = 2.4000 kN/m; force per centimetre = 180 × 10 ÷ 75 = 24.00 N/cm; margin against the common requirement 1.0 kN/m = (2.4000 − 1.0) ÷ 1.0 × 100% = 140.00%.",
        "Why convert the peel force into a strength per unit width?",
        "The peel force only reflects the loading of the whole specimen; with different specimen widths the same peel force corresponds to completely different degrees of interlayer bonding. Only after converting to N/m (force per metre of width) can specimens and batches be compared.",
        "Where does the 1.0 kN/m reference come from?",
        "It is only a common internal control reference for the interlayer of packaging board; requirements differ significantly across products such as liquid packaging and food board, so the actual verdict should follow the customer standard or the internal control document.",
        "About 'Interlayer (Peel) Adhesion Strength'",
        "Interlayer (Peel) Adhesion Strength. A free online tool processed entirely in the browser, no data uploaded, privacy and security protected.",
        "Load (kN)",
        "Area (m²)",
    ]))

    write('index', build('index', [
        "📄 Papermaking and Printing Tools",
        "Papermaking and Printing",
        "Papermaking and Printing Tools",
        "Enter the roll outer diameter, core diameter and paper thickness, and estimate the total roll length (metres) with the spiral unwinding formula. Used for printing, slitting and length-based pricing in stocktaking.",
        "Enter the weight of pulping raw material (wood chips, waste paper, etc.) and the resulting pulp weight to compute the pulp yield (%) and assess pulping efficiency. Used for mill cost accounting and process optimisation.",
        "Paper Moisture Calculator",
        "Enter the wet and oven-dry weights of the paper to compute the moisture content, with support for switching between dry basis (dry weight as the base) and wet basis (wet weight as the base). Used for moisture control in papermaking and printing workshops.",
        "Convert between GSM (g/m²), ream weight and pound weight (lb); enter any one parameter to obtain the others. Used to unify the grammage description in printing and paper procurement.",
        "Enter the wet pulp mass, dryness, pulp volume and target consistency to compute the dry fibre amount, mass consistency, volumetric consistency (g/L) and the water needed for dilution/thickening.",
        "The filler (calcium carbonate/talc) addition tool estimates the filler addition ratio and the ash content of the finished sheet from the input parameters, suitable for papermaking formulation and cost/strength trade-offs.",
        "Enter paper defect types such as holes and scratches together with size and count parameters, and grade the paper quality and conformity against standards such as GB/T 451.2, helping papermaking and printing quality inspection quickly screen out rejects.",
        "The burst/puncture index calculator derives the burst index from burst strength and grammage to assess the paper's resistance to internal bursting, suitable for quality testing and grading of board and packaging paper.",
        "The interlayer peel adhesion strength tool derives the interlayer bonding strength from peel force and width to assess the interface bonding of paper-plastic or multi-layer materials, suitable for composite packaging and board quality inspection.",
        "Estimate the board edge crush strength ECT from the ring crush strength of the liner, inner liner and medium together with the flute type, then use the McKee formula to compute the empty box compression strength BCT, and derive the safe stacking layers and stacking height.",
        "The tear strength calculator computes internal and edge tear strength to assess the tear resistance of paper, suitable for quality testing and suitability judgement of packaging and printing papers.",
        "The paper grade reference table summarises the classification, quality indicators and uses of common paper grades and supports quick lookup, suitable as a reference for paper selection, procurement and process matching in printing.",
        "About 'Papermaking and Printing Tools'",
        "This Papermaking and Printing Tools collection includes 12 free online tools covering the common calculation, conversion and lookup needs of papermaking and printing scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you can find ready-to-use practical tools here. All tools run purely in the front end, data is not uploaded to the server, and privacy and security are protected.",
        "The papermaking and printing tools collected on this page include (some representative tools):",
        "These tools help you quickly complete common papermaking and printing tasks without memorising complex formulas or converting manually; just input and you get the result.",
        "Do the Papermaking and Printing Tools need a download or registration?",
        "No. All Papermaking and Printing Tools on this page are pure front-end online tools. Open the page and use them directly, with no software to install, no account to register, and no data uploaded.",
        "Are the calculation results of the Papermaking and Printing Tools accurate? Is the data secure?",
        "The tools compute locally in your browser from public mathematical formulas and common industry standards, so results are available instantly. All computation happens locally on your device, data is never uploaded to the server, and privacy is well protected.",
    ]))


if __name__ == '__main__':
    main()

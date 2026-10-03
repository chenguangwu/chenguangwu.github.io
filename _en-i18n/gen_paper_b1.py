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
    write('strength-1', build('strength-1', [
        "🎚️ Box Compression Strength (McKee Formula)",
        "Estimate the board edge crush strength ECT from the ring crush strength of the liner, inner liner and medium together with the flute type, then use the McKee formula to compute the empty box compression strength BCT, and derive the safe stacking layers and stacking height.",
        "📖 View the usage guide for 'Box Compression Strength (McKee Formula)'",
        "Corrugated box compression (BCT) is estimated with the McKee empirical formula:",
        ", where ECT is the board edge crush strength (N/150mm), T is the board thickness (mm), and Z is the box perimeter (mm). ECT is obtained by summing the ring crush strength Rct of each paper layer (including the flute take-up factor and the medium contribution).",
        "Flute type matters: A flute gives a high ECT while E flute is flat; BCT also drops as stacking height, temperature and humidity increase.",
        "The safety factor is usually taken as 3-5 (the worse the storage/transport/humidity conditions, the larger it is).",
        "Results are for reference only; formal packaging design should follow GB/T 6543 and measured compression strength.",
        "Flute type",
        "A flute",
        "C flute",
        "B flute",
        "E flute",
        "Liner ring crush RCT (N/m)",
        "Inner liner ring crush RCT (N/m)",
        "Medium ring crush RCT (N/m)",
        "Board thickness d (mm)",
        "Ring-crush to edge-crush conversion factor",
        "Direct ECT input (N/m, optional)",
        "Box length L (mm)",
        "Box width W (mm)",
        "Box height H (mm)",
        "Safety factor SF",
        "Single box weight incl. contents (kg)",
        "💡 ECT ≈ (liner RCT + inner liner RCT + medium RCT × flute take-up) × conversion factor; BCT = 5.87 × ECT × √(perimeter × thickness); safe load = BCT ÷ SF; max stacking layers = floor(safe load ÷ load per layer) + 1.",
        "📈 Safe stacking layers vs safety factor",
        "ECT estimated from ring crush strength is an empirical formula; if a measured ECT is available, enter it directly to override",
        "The McKee formula applies to conventional transport corrugated boxes and is affected by temperature, humidity, printing and slotting",
        "The safety factor SF is usually taken as 3 (storage) and 3-4 for long-distance transport",
        "📚 Deep Dive: Box Compression Strength (McKee Formula)",
        "In transport packaging design, the box body compression (BCT) is estimated from the corrugated board edge crush (ECT) to set the number of stacking layers.",
        "When selecting a box, back-calculate the required ECT and flute type from the goods weight and the safety factor.",
        "In warehouse planning, use BCT and the safety factor to account for the load per layer and the maximum stacking height.",
        "Worked example: A flute box compression (ECT estimated, 400×300×300mm, box weight 15kg)",
        "ECT≈(4000+4000+2500×1.53)×0.5≈5913 N/m; BCT=5.87×ECT×√(perimeter×thickness)=5.87×5913×√(1.4×0.0036)≈2464 N (≈251 kgf); with a safety factor of 3 the safe load is ≈821 N, about 6 layers can be stacked and the stacking height is about 1.8 m. Formula: BCT=5.87·ECT·√(Pm·d). [SRC]",
        "Worked example: stacking layer calculation",
        "Load per layer=15×9.81≈147 N; max layers=floor(safe load/load per layer)+1=floor(821/147)+1=6 layers. Stacking height=6×0.3=1.8 m. The smaller the safety factor, the fewer layers can be stacked.",
        "What are the applicable conditions of the BCT formula BCT=5.87·ECT·√(Pm·d)?",
        "This is a common form of the McKee empirical formula, applicable to regular slotted containers (RSC) with the ECT entered for the correct flute orientation. ECT can be estimated from the liner/medium ring crush strengths and the flute take-up factor (ECT≈(liner+liner+medium×takeup)×efficiency), or it can be measured and entered directly.",
        "What safety factor is appropriate?",
        "For general transport and storage take 3-5, and take a higher value for damp, long-cycle or automatic stacking conditions. It combines temperature and humidity, stacking time, vibration and handling factors; too small a safety factor risks collapse, too large wastes material and raises cost.",
        "About 'Box Compression Strength (McKee Formula)'",
        "Used to estimate corrugated box compression strength. ECT is estimated from the ring crush strength of the liner, inner liner and medium together with the flute type, then BCT is computed with the McKee formula, and the maximum safe stacking layers and stacking height are given by combining the safety factor.",
        "Dual mode: ECT estimation plus direct input",
        "Computes BCT with the McKee formula",
        "Stacking layers vs safety factor curve",
        "Corrugated box structural design",
        "Stacking and warehouse safety assessment",
        "Paper grade selection and cost optimisation",
        "Packaging and transport scheme verification",
        "Liner ring crush",
        "Inner liner ring crush",
        "Medium ring crush",
        "Board thickness",
        "Conversion factor",
        "Direct ECT input",
        "Box length",
        "Box width",
        "Box height",
        "Single box weight",
    ]))

    write('detector-17', build('detector-17', [
        "🔍 Paper Defect (Holes/Scratches) Detection",
        "Enter the paper defect type and parameters, and grade the paper quality against standards such as GB/T 451.2",
        "📖 View the usage guide for 'Paper Defect (Holes/Scratches) Detection'",
        "Paper defect grading (GB/T 451.2 etc.): graded by hole diameter and count - for printing paper, a hole diameter greater than 2.0 mm or a defect count per square metre over the limit is reject; defect area ratio = Σ defect area ÷ inspected area × 100%; the grade (qualified, downgraded or reject) is decided by paper type and defect type.",
        "Paper type",
        "Printing paper",
        "Packaging paper",
        "Tissue paper",
        "Industrial paper",
        "Defect type",
        "Holes",
        "Scratches/tears",
        "Specks/dust",
        "Creases",
        "Blisters/bubbles",
        "Maximum defect size (mm)",
        "Defects per square metre",
        "Inspected area (m²)",
        "📚 Deep Dive: Paper Defect (Holes/Scratches) Detection",
        "In appearance inspection, the grade is decided by comparing the acceptance limits (size, density) against the paper type and defect type.",
        "Printing paper is sensitive to holes/specks, while packaging paper has a different tolerance for scratches/blisters, so the limits differ.",
        "Before releasing a batch, count the defects per unit area and combine them with the single-defect size for an overall grade.",
        "Worked example: hole grading for printing paper (size 2.5mm, density 8 per m², area 10m²)",
        "Acceptance limits for printing paper holes: size≤2mm, density≤5 per m². Measured size 2.5mm>2 (oversize) and density 8>5 (over density) → reject; this 10 m² area has about 8×10=80 defects in total. Formula: total defects = density × area. [SRC]",
        "Worked example: grading rules",
        "Both size and density within limits and both within half the limit → superior grade; both within limits → first grade; only one within limits → qualified; both over limits → reject. Look up the limit table for the paper type.",
        "Are the defect limits the same for different paper types?",
        "No. This tool has built-in limits for four categories: printing/packaging/tissue/industrial paper. For holes, printing paper is size≤2mm and density≤5, while industrial paper is relaxed to size≤10mm and density≤10. Choosing the wrong paper type gives a wrong verdict.",
        "Which matters more, size or density?",
        "Both matter, but large-size defects (holes, blisters) are more damaging to print break-through and appearance, so size is usually checked first; density reflects overall cleanliness. Exceeding either limit at the same time means reject.",
        "Paper defect detection is based on GB/T 451.2 'Determination of grammage of paper and board' and related GB/T 15442 standards",
        "Printing paper has the strictest requirements: holes≤2mm and ≤5 per m²; packaging paper may be moderately relaxed",
        "Holes and tears affect printing and packaging performance, and in severe cases cause break-through or missing print",
        "Detection should be carried out under standard light sources, over an area of at least 5m² to ensure statistical reliability",
        "Common causes: poor formation on the wire, uneven press pressure, contamination of the dryer drum surface, etc.",
        "About 'Paper Defect (Holes/Scratches) Detection'",
        "A paper defect detection and grading tool. Enter the defect type, size and count to grade the paper quality (superior/first/qualified/reject) against GB/T standards.",
        "Supports five common paper defect types",
        "Automatically matches limits for different paper types",
        "Dual judgement by size and count",
        "Gives process improvement suggestions",
        "Paper mill quality control",
        "Printing paper acceptance",
        "Packaging material testing",
        "Paper quality grading",
    ]))

    write('calc-concentration-1', build('calc-concentration-1', [
        "🧮 Pulp Consistency Calculation",
        "Enter the wet pulp mass, dryness, pulp volume and target consistency to compute the dry fibre amount, mass consistency, volumetric consistency (g/L) and the water needed for dilution or thickening.",
        "Core formulas (by input variable): wet×max(dryPct,0)÷100; dryFiber÷(target÷100)",
        "📖 View the usage guide for 'Pulp Consistency Calculation'",
        "Wet pulp mass (kg)",
        "Dryness (%)",
        "Pulp volume (L)",
        "💡 Dry fibre amount = wet pulp mass × dryness; mass consistency = dry amount ÷ pulp mass; volumetric consistency = dry amount ÷ volume (g/L); dilution/thickening water = dry amount ÷ target consistency - wet pulp mass.",
        "📊 Common pulp consistency ranges",
        "Mass consistency (dryness) is expressed as a mass fraction; volumetric consistency requires the pulp volume",
        "A target consistency below the current one means dilution (add water), above means thickening (dewater)",
        "📚 Deep Dive: Pulp Consistency Calculation",
        "In the beating and blending section, the volumetric consistency (g/L) must be computed from the dryness (%) and volume (L) to control the consistency at the machine head.",
        "When diluting or thickening in the storage tank, back-calculate the water to add or the amount to evaporate from the target dryness.",
        "When mass consistency and volumetric consistency are mixed up, use the dry fibre amount (kg) as the bridge to avoid errors.",
        "Worked example: mass and volumetric consistency (dryness 20%, pulp 500kg, volume 480L)",
        "Dry fibre amount=500×20%=100.00 kg; volumetric consistency=100×1000/480≈208.3 g/L; a dryness of 20% counts as 'high consistency' (>10%). Formula: volumetric consistency = dry fibre (kg)×1000÷volume (L). [SRC]",
        "Worked example: dilution to target consistency (target 3%)",
        "Total mass after dilution = dry fibre ÷ target %=100÷3%=3333.33 kg; water to add=3333.33−500=2833.33 kg. Formula: final mass = dry amount ÷ (target%/100), water to add = final mass - original mass. [SRC]",
        "What is the difference between mass consistency (%) and volumetric consistency (g/L)?",
        "Mass consistency = dry fibre ÷ total pulp mass (%), volumetric consistency = dry fibre ÷ pulp volume (g/L). For the same dry amount, volume changes caused by beating degree or temperature make the two values diverge, so blending should follow whichever one the process standard specifies.",
        "How are low, medium and high consistency divided?",
        "Common convention: <3% low, 3%-10% medium, >10% high (some literature uses 8% or 10% as the boundary). This tool uses 3% / 10%; follow your own internal control standard.",
        "About 'Pulp Consistency Calculation'",
        "Used for pulp consistency conversion in papermaking. Enter the wet pulp mass, dryness, pulp volume and target consistency to compute the dry fibre amount, mass consistency, volumetric consistency (g/L) and the water needed for dilution or thickening, with reference ranges for common pulp consistency.",
        "Mass consistency and volumetric consistency conversion",
        "Dilution/thickening water calculation",
        "Automatic consistency category judgement",
        "Pulp blending consistency adjustment",
        "Dry fibre amount accounting",
        "Headbox consistency dilution calculation",
        "Pulp transport process design",
        "Wet pulp mass",
        "Dryness",
        "Pulp volume",
    ]))

    write('basis-weight', build('basis-weight', [
        "⚖️ Paper Grammage Conversion",
        "Conversion between GSM (g/m²), ream weight and pound weight",
        "'Conversion between GSM (g/m²), ream weight and pound weight' performs a professional calculation from the input parameters and outputs the result.",
        "📖 View the usage guide for 'Paper Grammage Conversion'",
        "GSM conversion",
        "Ream weight conversion",
        "Grammage GSM (g/m²)",
        "Sheet size",
        "787×1092mm (full size)",
        "889×1194mm (A-size double)",
        "Sheets per ream",
        "500 sheets",
        "480 sheets",
        "1000 sheets",
        "Conversion notes:",
        "1 pound (lb) ≈ 453.592g; ream weight = grammage × single sheet area × sheets per ream. Paper is measured differently across countries: the US uses pounds (lb), China uses grammage (gsm).",
        "Common paper grammage reference",
        "📚 Deep Dive: Paper Grammage Conversion",
        "In printing and papermaking, grammage (g/m²) is the most basic indicator and must be converted between g/m², pounds (lb) and ounces per square yard for paper selection and quotation.",
        "In procurement and warehousing, the ream (usually 500 sheets) is used to compute the ream weight (kg/lb), which simplifies transport measurement and inventory management.",
        "For plate making and cost estimation, the single sheet weight is grammage × sheet area, then multiplied by the print run to estimate the total paper consumption.",
        "Worked example: grammage and imperial units (80 g/m²)",
        "1) Ream weight (500 sheets A-size double)≈80×0.895=71.6 lb; 2) ounces per square yard=80×0.02949≈2.36 oz/yd²; 3) a single A4 sheet (0.21×0.297m) weighs 80×0.21×0.297≈5.00 g. Formula: pounds≈gsm×0.895 (approximation for 500 sheets A-size double). [SRC]",
        "Worked example: ream weight calculation (70 g/m², 787×1092mm, 500 sheets)",
        "Single sheet area=0.787×1.092=0.8594 m²; single sheet weight=70×0.8594=60.16 g; ream weight=60.16×500=30079 g≈30.08 kg (≈66.3 lb). Formula: ream weight = grammage × single sheet area × sheets per ream. [SRC]",
        "How do you convert grammage g/m² and pounds (lb)?",
        "Pound (lb) usually refers to the 'ream weight of 500 A-size double sheets', approximately 1 lb≈1.128 g/m² (that is, gsm×0.895≈lb/ream). More rigorously, use the ream weight formula with the actual sheet size to avoid mixing up sheet sizes.",
        "How much do full size and A-size double sheets differ in area?",
        "Full size 787×1092mm≈0.8594 m², A-size double 889×1194mm≈1.061 m², so at the same grammage the A-size double ream is about 23% heavier. Always state the sheet size in quotations and layouts.",
        "About 'Paper Grammage Conversion'",
        "A paper grammage conversion tool supporting conversion between gsm and pounds, and between ream weight and grammage in square metres, with a common paper grammage reference table. A business and office tool that improves work efficiency, with data processed locally to protect privacy.",
    ]))


if __name__ == '__main__':
    main()

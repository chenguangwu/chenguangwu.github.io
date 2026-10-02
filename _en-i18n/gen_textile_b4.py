#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'textile')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'textile')
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
    out = {'slug': slug, 'industry': 'textile', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # length-gsm (37)
    write('length-gsm', build('length-gsm', [
        "⚖️ Knitted Loop Weight (GSM)",
        "Enter loop length, yarn linear density, course and wale density to calculate knitted fabric GSM (g/m²)",
        "Core formulas (by input variables): loopLen×tex×wpc×cpc÷100; yarnLen×tex÷1000",
        "📖 View 'Knitted Loop Weight (GSM) User Guide'",
        "Loop length (mm)",
        "Yarn linear density (tex)",
        "Wale density (wales/cm)",
        "Course density (courses/cm)",
        "💡 GSM = loop length (mm) × linear density (tex) × wale density × course density ÷ 100",
        "tex = grams per 1000 m; 1 tex ≈ 590.5 / English count (Ne)",
        "Longer loop length and lower density give lower GSM and softer hand feel",
        "📚 In-depth: Loop Length and GSM Estimation",
        "Estimate GSM of knitted fabric from loop length, yarn count and density",
        "Predict GSM change by adjusting density/yarn count during machine setup",
        "Quickly estimate weight for same structure across specs",
        "GSM Estimation",
        "Wale 10/cm, course 14/cm → stitches 140/cm²; loop 4 mm, tex 18 → single loop weight ≈ 4×18/1e6 = 7.2e-5 g; GSM ≈ 140×7.2e-5×10000 ≈ 100.8 g/m² (with structure factor).",
        "Density vs GSM",
        "Course density 14 → 16/cm → stitches 160/cm² → GSM rises to about 115 g/m², fabric denser.",
        "Why is it an estimate, not exact?",
        "Structure factor and moisture regain are not included; the formula gives an approximation; exact GSM is by weighing.",
        "What does loop length affect?",
        "Longer loops use more yarn and make looser/softer fabric; shorter loops are denser but may feel stiff.",
        "About 'Knitted Loop Weight (GSM)'",
        "Knitted loop weight is a core metric for knitted fabric thickness and quality. Based on loop length, yarn linear density, course and wale density, this tool calculates knitted GSM (g/m²) and judges fabric hand feel, supporting knitting process design and quality control.",
        "Standard GSM formula calculation",
        "Output loop density and yarn length together",
        "Automatic tex and English count Ne conversion",
        "Hand-feel grading (light/medium/mid-heavy/heavy)",
        "Knitted fabric process design",
        "Yarn selection and density adjustment",
        "Fabric GSM quality inspection",
        "Cost accounting and material estimation",
        "Loop length",
        "Yarn linear density",
        "Wale density",
        "Course density",
    ]))

    # liquor-ratio (54)
    write('liquor-ratio', build('liquor-ratio', [
        "🧵 Dyeing Liquor Ratio Calculator",
        "Calculate dyeing liquor ratio, total dye-liquor volume and dye/chemical concentration conversion",
        "Performs professional calculation and outputs results based on input parameters for 'calculate dyeing liquor ratio, total dye-liquor volume and dye/chemical concentration conversion'.",
        " / Liquor Ratio Calculation",
        "📖 View 'liquor-ratio User Guide'",
        "🧵 Dyeing Liquor Ratio Calculator",
        "🧵 Liquor Ratio Calculation",
        "🔄 Concentration Conversion",
        "Fabric weight (kg)",
        "Liquor ratio (1:X)",
        "Total dye/chemical (g)",
        "Dye/chemical density (g/mL, optional)",
        "Dye owf% (%)",
        "or concentration (g/L)",
        "🔢 Liquor Ratio Formula",
        "Liquor ratio",
        "= dye-liquor volume (L) : fabric weight (kg), usually expressed as 1:X",
        "Total dye-liquor volume",
        "= fabric weight (kg) × liquor ratio X",
        "Water added volume",
        "= total dye-liquor volume − dye/chemical solution volume",
        "🔢 Concentration Conversion Formula",
        ": concentration = (fabric weight × owf% × 10) ÷ (fabric weight × liquor ratio)",
        "Simplified: concentration (g/L) = owf% × 10 ÷ liquor ratio",
        ": owf% = concentration (g/L) × liquor ratio ÷ 10",
        "📊 Common Liquor Ratio Reference",
        "Typical liquor ratio",
        "Jig dyeing machine",
        "Low liquor ratio, saves dye/chemicals",
        "Overflow dyeing machine",
        "Common, good leveling",
        "Winch dyeing machine",
        "High liquor ratio, for relaxed style",
        "Air-flow dyeing machine",
        "Ultra-low liquor ratio, energy saving",
        "Package yarn dyeing",
        "Yarn dyeing",
        "Smaller liquor ratio saves more dye/chemicals and water, but requires better leveling; at the same owf%, smaller ratio means higher concentration.",
        "📚 In-depth: Dyeing Liquor Ratio Calculator",
        "Dye-liquor preparation: from fabric weight and liquor ratio (1:10 etc.) compute total volume, water added and dye/chemical concentration (g/L).",
        "owf conversion: convert owf% (on fabric weight",
        ") into actual g/L dosing to avoid prescription concentration deviation.",
        "Lab-to-bulk scale-up: when scaling lab sample to bulk, lock actual g/L rather than simply keeping the ratio, ensuring consistent shade.",
        "Liquor preparation example",
        "Fabric 10kg, ratio 1:10, dye 20g, density 1.0 → total liquor=10×10=100L; dye solution vol=20/1/1000=0.02L, water≈99.98L; concentration=20/100=0.20g/L; equals owf%=20/1000/10×100=0.20%. For owf 2%, dye=10×2/100×1000=200g, corresponding 2.00g/L. Bulk 50kg×1:15 → total liquor 750L.",
        "How does liquor ratio affect dyeing?",
        "Small ratio (less liquor) dyes faster, poorer leveling, prone to shade bars; large ratio costs more, slower heating. Cotton often 1:8–1:15, wool 1:15–1:30, by fiber and machine.",
        "How to choose owf% and g/L?",
        "Lab and prescription use owf% (on cloth weight); bulk control uses actual g/L (on liquor) for stability; they convert via ratio. On scale-up lock g/L to avoid shade deviation from ratio change.",
        "About 'Dyeing Liquor Ratio Calculator'",
        "Dyeing liquor ratio calculator — dyeing liquor ratio and dye-liquor volume calculation, an online textile dyeing process tool, free to use. A business/office tool to boost efficiency, with local data processing for privacy.",
        "Before dye lot, compute total and added liquor from fabric weight and ratio.",
        "Convert prescription owf% to actual g/L for unified bulk dosing.",
        "On scale-up lock g/L rather than simply keeping the ratio, ensuring consistent shade.",
    ]))

    # pattern-calculator (55)
    write('pattern-calculator', build('pattern-calculator', [
        "🧮 Marker Utilization Calculator",
        "Fabric marker, utilization calculation, material estimation, piece layout preview",
        "Core formulas (by input variables): Math.ceil(totalPieceArea÷(fw×0.8)); (totalPieceArea÷fabricArea×100); min(1,400÷fw,300÷fl)",
        "Marker Calculator",
        " / Marker Calculator",
        "📖 View 'Marker Utilization Calculator User Guide'",
        "Seam allowance/waste (%)",
        "Layout direction",
        "Any direction",
        "On-grain (same direction)",
        "Piece list",
        "+ Add piece",
        "🧮 Calculate marker",
        "📊 Marker result",
        "📖 Marker tips",
        "📋 Reference data",
        "💡 Basic marker principles",
        "Large before small",
        ": place large pieces first, then fill gaps with small pieces",
        "Tight nesting",
        ": nest concave/convex shapes to reduce gaps",
        "Correct grain",
        ": mind warp/weft direction; bias grain for stretch-needed parts",
        "Match stripes/checks",
        ": patterned fabric needs matching, adding waste",
        "Pile direction",
        ": pile fabric needs uniform nap direction in layout",
        "Reasonable edge margin",
        ": leave 2–3 cm seam allowance at edge to avoid edge defects",
        "📊 Fabric Utilization Reference by Product",
        "Plain T-shirt",
        "Regular shape, high utilization",
        "More components",
        "Trouser legs relatively regular",
        "Suit",
        "Complex pattern, match stripes/checks",
        "Pieces vary in size",
        "Coat",
        "Width-limited, more bias cutting",
        "Lingerie/bra",
        "Many small pieces, complex shapes",
        "📚 In-depth: Pattern Marker Calculation",
        "Estimate placeable piece count within given width and length",
        "Recalculate footprint after seam allowance, verify actual unit consumption",
        "Mixed layout of multiple specs optimizes total utilization",
        "Placeable count",
        "Cloth 150 cm wide, 200 cm long, 1 cm seam; front 50×70 → per row (150/(50+2))≈2 cols, per col (200/(70+2))≈2 rows = 4 pcs; back same.",
        "Seam allowance impact",
        "Seam 1 cm → 1.5 cm, single piece footprint grows 1 cm edge → 200 cm direction drops from 2 rows to 1, utilization ~halves, needs re-layout.",
        "How much seam allowance is typical?",
        "Regular wear 1 cm, thick fabric 1.5 cm, overlock separate; affects unit consumption, must count.",
        "Can marker layout be auto-optimal?",
        "This tool gives rectangular estimation; irregular pieces need CAD marker for true utilization.",
        "About 'Marker Calculator'",
        "Marker Calculator is an online tool for the textile and apparel field. A textile tool that helps calculate fabric parameters and usage.",
    ]))

    # ratio-20 (38)
    write('ratio-20', build('ratio-20', [
        "🧵 Grading Size Increment",
        "Enter base size (M) dimensions and per-part increments to auto-derive S–XXL sizes",
        "Core formulas (by input variables): Math.round(size×10)÷10",
        "📖 View 'Grading Size Increment User Guide'",
        "Part name",
        "Base size M (cm)",
        "Increment (cm/size)",
        "💡 Size = base M ± increment × size step; S is −1, L is +1, XL is +2, XXL is +3",
        "Increment is the size difference between adjacent sizes, e.g. bust 4 cm per size",
        "Different parts have different increments, compute each separately",
        "📚 In-depth: Grading (Increment) Calculation",
        "Generate full size table from base size and per-part increments",
        "Check grading evenness and fit regularity",
        "Change base or increment to quickly recompute the series",
        "Bust increment",
        "Base M bust 100 cm, increment 4 cm → S=96, L=104, XL=108, 2XL=112; even top-down.",
        "Multi-part linkage",
        "Garment length increment 2 cm, sleeve 1.5 cm; from M, S length −2, sleeve −1.5, L adds, keeping proportion.",
        "How to set increments?",
        "By body rules and national size standard, bust often 4 cm, collar 1 cm, length 2 cm, even steps.",
        "Is even grading enough?",
        "Not necessarily; must match human growth ratios, or large sizes look short, small sizes tight.",
        "About 'Grading Size Increment'",
        "Grading size increment is the core of garment grading. Centered on base size M, this tool auto-derives XS–XXL sizes from per-part increments and generates a grading table, helping graders quickly build size series.",
        "Supports custom part names and base sizes",
        "One-click generate XS–XXL six-size grading table",
        "Auto-stat size step and full span",
        "Garment grading size calculation",
        "Size series spec table creation",
        "Increment rule verification",
        "Production size sheet preparation",
        "How to Use Grading Size Increment",
        "What does Grading Size Increment do?",
        "How to use Grading Size Increment?",
        "What scenarios is Grading Size Increment suitable for?",
        "Part name",
        "Base size",
        "Increment",
    ]))

    # shrinkage (46)
    write('shrinkage', build('shrinkage', [
        "🔢 Shrinkage Correction",
        "Correct garment size by fabric shrinkage; supports cut-size back-calculation and finished-size prediction",
        "📖 View 'Shrinkage Correction User Guide'",
        "Shrinkage = (original size − washed size) / original size × 100%",
        "Predict finished size",
        "Back-calculate cut size",
        "Given cut size and shrinkage, predict post-wash finished size",
        "Cut size (cm)",
        "Shrinkage (%, positive=shrink, negative=stretch)",
        "Given target finished size and shrinkage, back-calculate cut size",
        "Target finished size (cm)",
        "📐 Formulas and Common Shrinkage",
        "Shrinkage",
        "= (original size − washed size) / original size × 100%",
        "Predict finished",
        "= cut size × (1 − shrinkage%)",
        "Back-calculate cut",
        "= target size / (1 − shrinkage%)",
        "Fabric",
        "Pure cotton",
        "Linen",
        "📚 In-depth: Shrinkage and Pre-shrinking",
        "Measure cut piece before/after wash to compute shrinkage",
        "Back-derive cut size from target finished size (add shrinkage)",
        "Compare shrinkage under wash conditions to choose pre-shrinking process",
        "Cut 100 cm, washed 95 cm → shrinkage = (100 − 95) / 100 × 100% = 5%; i.e. 5 cm per meter.",
        "Pre-shrink back-derive",
        "Want finished 100 cm, shrinkage 5% → cut size = 100 / (1 − 5%) ≈ 105.3 cm; cutting short gives insufficient finished.",
        "Are warp and weft shrinkage the same?",
        "Usually warp (length) shrinkage exceeds weft (width); cut fabric with separate allowances.",
        "Can pre-shrinking eliminate shrinkage?",
        "Pre-shrinking greatly reduces re-shrinkage, but regain and finishing residue leave residual shrinkage, keep margin.",
        "About 'Shrinkage Correction'",
        "Shrinkage Correction tool corrects garment size by fabric shrinkage, supports two-way calculation of predicted finished size and back-calculated cut size, with common fabric shrinkage reference.",
        "Two-way calculation mode",
        "Supports shrink and stretch",
        "Common fabric shrinkage reference",
        "Garment cut size calculation",
        "Fabric shrinkage prediction",
        "Pattern allowance design",
        "Wash process control",
        "How to Use Shrinkage Correction",
        "What does Shrinkage Correction do?",
        "Enter fabric shrinkage and garment target size to forward-predict post-wash finished size, or back-calculate cut allowance to offset shrinkage; used in pattern making to correct patterns by shrinkage and ensure garment specs.",
        "How to use Shrinkage Correction?",
        "What scenarios is Shrinkage Correction suitable for?",
    ]))

if __name__ == "__main__":
    main()

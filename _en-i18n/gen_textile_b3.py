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
    # estimate-dosage-fabric-qty (35)
    write('estimate-dosage-fabric-qty', build('estimate-dosage-fabric-qty', [
        "📐 Fabric & Trim Usage Estimator",
        "Enter per-piece fabric length, fabric width, production quantity and loss rate to estimate total fabric and trim usage",
        "Core formulas (by input variables): totalLen×width÷100; perLen×width÷100; netLen×waste÷100",
        "📖 View 'Fabric & Trim Usage Estimator Guide'",
        "Per-piece fabric length (m)",
        "Production quantity (pcs)",
        "Fabric unit price (¥/m)",
        "💡 Total usage = per-piece length × quantity × (1 + loss rate); fabric area = total length × width ÷ 100",
        "Per-piece length includes seam allowance and marker margin; width is in cm",
        "Loss rate is generally 2%–5%, covering cutting waste and defective-piece replenishment",
        "📚 In-depth: Fabric Usage and Cost Estimation",
        "Estimate total material and cost from per-piece length and quantity before ordering",
        "Include loss rate to calculate safe stock and avoid shortages",
        "When mixing multiple styles, sum each style's usage for purchasing planning",
        "Total Material and Cost",
        "Per piece 1.5 m, 100 pcs, 5% loss → total = 1.5 × 100 × 1.05 = 157.5 m; unit price ¥25/m → cost ¥3937.5.",
        "Safe Stock Quantity",
        "Net usage 150 m, plus 5% loss and 2% cutting waste → stock = 150 × 1.07 ≈ 160.5 m, leaving margin against defect cloth.",
        "What is the difference between loss rate and cutting waste?",
        "Loss rate covers process rework and defective cloth; cutting waste is marker offcuts; their sum is the total stock coefficient.",
        "How to estimate with multiple widths?",
        "First compute per-piece net area, then divide by width for per-piece length, multiply by quantity and loss; narrower width gives longer per-piece length.",
        "About 'Fabric & Trim Usage Estimator'",
        "Fabric and trim usage estimation is central to garment marker planning and procurement. Based on per-piece length, fabric width, production quantity and loss rate, this tool quickly calculates net usage, loss-inclusive total usage, fabric area and cost to support precise purchasing and cost control.",
        "Net usage and loss-inclusive usage calculated simultaneously",
        "Fabric area, total cost and per-piece cost output together",
        "Supports custom loss rate and fabric unit price",
        "Garment order fabric procurement accounting",
        "Production cost estimation and quotation",
        "Marker plan usage comparison",
        "Quick trim usage estimation",
        "Per-piece fabric length",
        "Fabric width",
        "Production quantity",
        "Fabric unit price",
    ]))

    # fabric-converter (32)
    write('fabric-converter', build('fabric-converter', [
        "🧵 Fabric Unit Converter",
        "GSM/width/length/price conversion",
        "Core formulas (by input variables): price ÷ (mWeight ÷ 1000); rmb ÷ (mWeight ÷ 1000); mWeight × 0.9144",
        "Fabric Conversion",
        " / Fabric Conversion",
        "📖 View 'Fabric Unit Converter Guide'",
        "📚 In-depth: Fabric (GSM/Meter Weight/Yard Price) Conversion",
        "Convert meter weight and yard weight from GSM and width",
        "Switch between meter price and yard price for domestic and export quotations",
        "Unify different fabric units for easy price comparison",
        "Meter Weight and Yard Weight",
        "GSM 200, width 1.5 m → meter weight = 200 × 1.5 / 1000 = 0.3 kg/m; 100 m cloth weighs 30 kg; yard weight = 0.3 × 0.9144 ≈ 0.274 kg/yd.",
        "Yard Price Conversion",
        "Meter price ¥30/m → yard price = 30 / 0.9144 ≈ ¥32.8/yd (1 yd = 0.9144 m).",
        "What is the relationship between meter weight and GSM?",
        "Meter weight (kg/m) = GSM × width (m) / 1000; knowing any two yields the third.",
        "How to convert yards and meters?",
        "1 yard = 0.9144 m; yard price = meter price / 0.9144; meter price = yard price × 0.9144.",
        "About 'Fabric Conversion'",
        "Fabric conversion is an online tool for the textile and apparel field. A textile tool that helps calculate fabric parameters and usage.",
        "How to Use the Fabric Unit Converter",
        "GSM (g/m²)",
        "Width (cm)",
        "Price (¥/meter)",
        "Meter price (¥/meter)",
        "Length value",
        "Original unit",
        "Width value",
        "What does the Fabric Unit Converter do?",
        "Fabric Unit Converter: inter-converts fabric usage and cost by GSM, width, length and price, for garment pattern making and procurement estimation.",
        "How to use the Fabric Unit Converter?",
        "What scenarios is the Fabric Unit Converter suitable for?",
    ]))

    # fuliao-lalian-niukou-guige (25)
    write('fuliao-lalian-niukou-guige', build('fuliao-lalian-niukou-guige', [
        "🔢 Trim (Zipper/Button) Specification",
        "Enter two parameters to auto-calculate common results",
        "📖 View 'Trim (Zipper/Button) Specification Guide'",
        "Zipper length = opening + 2× margin; button count = ceil(opening/spacing)+1",
        "Opening length (cm)",
        "Button spacing (cm)",
        "Seam allowance margin (cm)",
        "💡 Trim (zipper/button) specs and quantities are derived from the opening size and spacing of garment parts.",
        "📚 In-depth: Trim (Zipper/Button) Specification",
        "Calculate button count and spacing from placket/opening length",
        "Select zipper length matching the opening with margin",
        "Verify trim specs against the production order",
        "Button Count",
        "Placket 60 cm, button spacing 10 cm → buttons = 60 / 10 + 1 = 7 pcs (including both ends); spacing 12 cm gives 6 pcs.",
        "Zipper Length",
        "Opening 55 cm, zipper should be ≥ opening + 2 cm margin → choose 58–60 cm closed-end zipper; add 3 cm more if a bottom facing is needed.",
        "How to set button spacing?",
        "Typically 8–12 cm by placket stress and appearance; thick wool may use denser spacing to prevent gaping.",
        "Why leave margin on a zipper?",
        "The top/bottom stops need engagement space; a too-short zipper cannot fully close or may burst, so it is generally 2–5 cm longer than the opening.",
        "About 'Trim (Zipper/Button) Specification'",
        "Trim (zipper/button) specification. A textile tool that helps calculate fabric parameters and usage.",
        "Opening length (cm)",
        "Button spacing (cm)",
        "Seam allowance margin (cm)",
    ]))

    # fukuanpailiaoliyonglv (37)
    write('fukuanpailiaoliyonglv', build('fukuanpailiaoliyonglv', [
        "🧵 Fabric Width Utilization Rate",
        "Enter fabric width, per-piece marker length, number of pieces and effective usable width to calculate the fabric width utilization rate",
        "Core formulas (by input variables): totalLen×effWidth÷100; totalLen×width÷100",
        "📖 View 'Fabric Width Utilization Rate Guide'",
        "Effective usable width (cm)",
        "Per-piece marker length (m)",
        "Marker piece count (pcs)",
        "💡 Width utilization = effective usable width ÷ fabric width × 100%; total usage = per-piece length × quantity",
        "Effective usable width is the actual marker-available width after removing selvage",
        "Higher width utilization saves more fabric; generally above 90% is excellent",
        "📚 In-depth: Fabric Width Utilization Rate",
        "Estimate marker ceiling by the ratio of effective width to total width",
        "When edge structure is poor, compress effective width and recalculate utilization",
        "Optimize total width utilization by mixed layout of multiple specs",
        "Width Utilization Rate",
        "Cloth width 150 cm, effective cuttable 144 cm → width utilization = 144 / 150 = 96%; 6 cm left as seam/trim edge.",
        "Effective Width Optimization",
        "Original effective 138 cm (92%) → adjust pattern to effective 144 cm (96%), unit consumption drops about 4%.",
        "What is the difference between width utilization and cutting-table utilization?",
        "Width utilization looks at horizontal effective ratio; cutting-table utilization looks at net piece ratio over the whole roll area, the latter being more comprehensive.",
        "How to determine effective width?",
        "Selvage, needle holes and defect zones are not cuttable; effective width = total width minus unusable edges; set by fabric inspection results.",
        "About 'Fabric Width Utilization Rate'",
        "Fabric width utilization reflects how effectively the width direction is used. Based on fabric width, effective usable width, per-piece marker length and piece count, this tool calculates width utilization, selvage loss and total usage to help optimize marker plans and reduce fabric waste.",
        "Width utilization and selvage loss calculated simultaneously",
        "Total usage length and area output together",
        "Marker plan width utilization evaluation",
        "Fabric width selection comparison",
        "Selvage loss control analysis",
        "How to Use the Fabric Width Utilization Rate",
        "What does the Fabric Width Utilization Rate do?",
        "How to use the Fabric Width Utilization Rate?",
        "What scenarios is the Fabric Width Utilization Rate suitable for?",
        "Fabric width",
        "Effective usable width",
        "Per-piece marker length",
        "Marker piece count",
    ]))

    # kangjingdianbanshuaiqi (35)
    write('kangjingdianbanshuaiqi', build('kangjingdianbanshuaiqi', [
        "☢️ Antistatic Half-Life",
        "Enter initial voltage, attenuated voltage and decay time to calculate the electrostatic half-life and judge antistatic performance",
        "Core formulas (by input variables): t×Math.LN2÷Math.log(ratio); (v0-vt)÷v0×100",
        "📖 View 'Antistatic Half-Life Guide'",
        "Initial voltage V₀ (V)",
        "Attenuated voltage Vt (V)",
        "Decay time t (s)",
        "💡 Half-life τ = t × ln2 ÷ ln(V₀/Vt); shorter half-life means better antistatic performance",
        "Half-life < 2s is excellent antistatic, < 10s is qualified",
        "Requires Vt < V₀, and both greater than 0",
        "📚 In-depth: Antistatic Half-Life",
        "Measure the time for fabric static voltage to decay to half and grade antistatic level",
        "Compare when selecting antistatic garment fabrics",
        "Verify finishing effect via half-life change before and after treatment",
        "Half-Life Calculation",
        "Initial voltage 5000 V, decay to 500 V in 5 s → half-life t₁/₂ = 5 × ln2 / ln(5000/500) = 5 × 0.693 / 1 ≈ 3.46 s; <2 s is excellent.",
        "Grade Reference",
        "Half-life < 2 s excellent antistatic (for clean/explosion-proof garments); 2–10 s good; >10 s tends to accumulate static and needs conductive yarn.",
        "How to measure half-life?",
        "Apply high voltage to the sample to reach initial voltage, disconnect and record time to decay to half, per GB/T 12703.",
        "What does a long half-life indicate?",
        "Charge is hard to dissipate, prone to dust attraction and discharge; add conductive fiber or antistatic finishing to reduce it.",
        "About 'Antistatic Half-Life'",
        "Antistatic half-life is a core metric for textile static dissipation. Based on initial voltage, attenuated voltage and decay time, this tool calculates electrostatic half-life by an exponential decay model and grades antistatic performance, supporting antistatic fabric evaluation and finishing verification.",
        "Standard exponential decay half-life formula",
        "Decay rate and voltage ratio output together",
        "Antistatic performance grading (excellent/good/qualified/poor)",
        "Automatic antistatic finishing suggestions",
        "Antistatic fabric performance testing",
        "Antistatic workwear evaluation",
        "Antistatic finishing agent effect verification",
        "Electronic cleanroom fabric selection",
        "Initial voltage",
        "Attenuated voltage",
        "Decay time",
    ]))

if __name__ == "__main__":
    main()

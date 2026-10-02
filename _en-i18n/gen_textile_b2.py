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
    # cost-calculator (65)
    write('cost-calculator', build('cost-calculator', [
        "💰 Fabric Cost Calculator",
        "Fabric/garment cost accounting, material usage and processing fee estimation",
        "Core formulas (by input): fu×fabricWeightM2×gsm÷1000; totalCostPer÷(1-pm÷100); fp×fu×(1+w÷100)",
        "📖 View 'Fabric Cost Calculator User Guide'",
        "Fabric price (yuan/m)",
        "Material per piece (m)",
        "GSM (g/m²)",
        "Trimming cost (yuan/piece)",
        "Processing fee (yuan/piece)",
        "Order quantity (pieces)",
        "Profit margin (%)",
        "Other costs (yuan/piece)",
        "💰 Calculate cost",
        "📊 Costing result",
        "📖 Reference data",
        "👔 Garment material usage",
        "📏 Common fabric widths",
        "Fabric type",
        "Common width",
        "Common GSM",
        "Cotton/shirting",
        "Denim",
        "Knit/T-shirt",
        "Wool/coat",
        "Silk/chiffon",
        "💵 Processing fee reference (China)",
        "Category",
        "Simple process",
        "Complex process",
        "T-shirt/tank",
        "5-10 yuan",
        "10-20 yuan",
        "15-25 yuan",
        "25-40 yuan",
        "20-35 yuan",
        "35-60 yuan",
        "30-50 yuan",
        "Suit/coat",
        "👔 Common garment material per piece (150cm width)",
        "Size S",
        "Size M",
        "Size L",
        "Size XL",
        "Short-sleeve T-shirt",
        "Long-sleeve shirt",
        "Trousers/dress pants",
        "Jeans",
        "Short dress",
        "Long coat",
        "📚 In-depth: Garment Cost and Quoting",
        "At sampling, estimate per-piece total cost and back-calculate the suggested retail price",
        "When pricing, split fabric, trimming, processing and other cost shares",
        "Adjust",
        "profit margin",
        "or loss rate for pricing sensitivity analysis",
        "Per-piece cost composition",
        "Fabric 30 yuan/m × 1.5 m/piece × (1 + 8% loss) = 48.6 yuan; trims 12 + labor 15 + other 3 = 78.6 yuan/piece.",
        "Back-calculate selling price",
        "Cost 78.6 yuan, target margin 30% → suggested retail = 78.6 / (1 - 30%) ≈ 112.3 yuan; at 20% margin, 98.3 yuan.",
        "What is a typical loss rate?",
        "Cutting table 3%-8%, checks or stripe matching up to 10%-15%, by pattern complexity.",
        "Should the quote include tax and freight?",
        "Usually the quote covers labor and material, tax/freight separate; bulk pricing should state trade terms (FOB/EXW etc.).",
        "About the Fabric Cost Calculator",
        "Fabric cost calculator. A textile/apparel tool to help compute fabric parameters and usage.",
    ]))

    # dye-temp (52)
    write('dye-temp', build('dye-temp', [
        "🌡️ Dyeing Temperature Reference",
        "Query dyeing temperature processes and heating programs for various dyes",
        "/ Dyeing Temperature Reference",
        "📖 View 'dye-temp User Guide'",
        "🌡️ Dyeing Temperature Reference",
        "Dyeing process temperature by dye type: reactive 40-80 ℃ (cotton usually 60 ℃ with alkali fixation), direct 80-100 ℃, acid 80-100 ℃ (wool and nylon), disperse 120-130 ℃ (PET high-temp high-pressure), cationic 95-100 ℃ (acrylic), vat leuco method 50-60 ℃; heating rate 1-2 ℃/min, hold 30-60 min, bath ratio 1:10-1:20.",
        "Azoic (insoluble azo) dyes",
        "Fiber type",
        "Silk",
        "Acrylic",
        "📊 Dye Temperature Range Overview",
        "Suitable fiber",
        "Dyeing temperature",
        "Heating method",
        "📚 Dyeing Temperature Principles",
        "🌡️ Effect of Temperature on Dyeing",
        "Exhaustion rate",
        ": higher temperature increases dye molecular kinetic energy, faster diffusion, higher exhaustion",
        "Levelness",
        ": too high temperature causes too-fast uptake, easily uneven dyeing",
        "Fixation",
        ": reactive dyes need a specific fixation temperature, disperse dyes need high temperature to promote dyeing",
        ": low temperature needs longer holding time",
        "🔥 Heating Program Key Points",
        "Initial dyeing temperature",
        ": usually start at 40-50°C to avoid too-fast initial uptake",
        "Heating rate",
        ": 1-2°C/min, ensure level dyeing",
        "Holding temperature",
        ": after reaching dyeing temperature, hold 30-60 min",
        "Cooling",
        ": cool slowly below 60°C before unloading",
        "Different dye manufacturers' processes may vary slightly; actual production follows the parameters provided by the dye maker.",
        "📚 In-depth: Dyeing Temperature Reference",
        "Dye selection: choose dye by fiber and check its temperature range (reactive 60-80°C, disperse 130°C HTHP, acid/direct 95-100°C).",
        "Heating program: check initial temp, heating rate and holding time to set the process curve.",
        "Troubleshooting: if temperature is off, check fiber/dye mismatch to avoid under- or over-dyeing.",
        "Reactive dye process example",
        "Choose reactive (cotton/linen/viscose) → 60-80°C, start 40°C, heat 1.5°C/min to 60°C, add alkali fix hold 30-45min. Disperse (PET) needs 130°C HTHP (low-temp type can use atmospheric 100°C carrier method). Acid (wool/silk) boils at 95-100°C.",
        "Why does PET need 130°C?",
        "PET has a tight structure and high glass transition; water cannot enter the fiber at atmospheric pressure, needing 130°C HTHP (or carrier method 100°C); cellulosic fibers like cotton/linen dye at 60-100°C.",
        "Why start dyeing at 40°C?",
        "Low-temperature start slows initial uptake and avoids fast adsorption causing uneven dyeing; then raise 1-2°C/min to target and hold. Cationic on acrylic (Tg ~80°C) often starts at 70°C and needs tighter rate control.",
        "About the Dyeing Temperature Reference",
        "Dyeing temperature reference — query dyeing temperature process parameters for various dyes, free to use. A business/office tool to boost efficiency, with local data processing for privacy.",
        "Check dyeing temperature range by fiber and dye to set initial and holding processes.",
        "Verify heating rate and holding time to avoid fast initial uptake causing uneven dyeing.",
        "For high-temp types like PET, confirm whether HTHP or carrier equipment is needed.",
        "Temperature reference",
        "Dyeing temperature depends on fiber and dye: cotton/linen reactive usually 60-80℃, wool/silk acid 40-60℃ (anti-felting), PET disperse usually 100-130℃ (HTHP).",
        "Choose temperature by fabric for uptake and fastness; too high harms fiber, too low under-dyes.",
        "Follow the dye instruction for exact process; home dyeing should control temperature and rinse well for fixation.",
    ]))

    # dye-mixer (51)
    write('dye-mixer', build('dye-mixer', [
        "🧮 Dye Ratio Calculator",
        "CMYK/RGB color mixing, dye amount calculation, recipe saving",
        "Core formulas (by input): Math.round(waterVolume×0.02); (dyeTotal×pct÷100); fw×conc÷100",
        "📖 View 'Dye Ratio Calculator User Guide'",
        "Fabric weight (g)",
        "Bath ratio (water:fabric)",
        "Dyeing type",
        "Select base dyes (multi-select mixing)",
        "💾 Save recipe",
        "🧪 Recipe result",
        "📖 Dyeing guide",
        "📊 Concentration reference",
        "📋 History recipes",
        "💡 Dyeing basics",
        "Bath ratio",
        ": ratio of dye liquor weight to fabric weight, commonly 1:10~1:30",
        "Dye concentration (owf)",
        ": percentage of dye weight to fabric weight",
        "Sodium sulfate / salt",
        ": exhausting agent, usually 10-30g/L",
        "Soda ash",
        ": fixing agent, used in reactive dyeing, 5-20g/L",
        "Bath temperature",
        ": direct/acid dyes 90-100°C, reactive 60°C, disperse 130°C",
        "Dyeing time",
        ": usually 30-60 minutes",
        "📊 Common Dye Concentration Reference (owf%)",
        "Shade depth",
        "Extra light",
        "Light pink, light blue, off-white",
        "Pink, sky blue, light gray",
        "Scarlet, deep blue, grass green",
        "Navy, dark green, black",
        "Extra deep",
        "Above 6%",
        "Jet black, deep navy",
        "📚 In-depth: Dye Formulation (Recipe Calculation)",
        "Compute dye liquor recipe from bath ratio and dye concentration (o.w.f)",
        "For combination shades, compute actual amount by each dye's share",
        "Scale the recipe by fabric weight when enlarging/shrinking batches",
        "Dye and bath volume",
        "Fabric 1000 g, dye concentration 2% (o.w.f) → dye = 1000 × 2% = 20 g; bath ratio 1:10 → bath = 1000 × 10 = 10000 mL = 10 L.",
        "Combination shade recipe",
        "Red 60% + yellow 30% + blue 10% total 20 g → red 12 g, yellow 6 g, blue 2 g; scale to 5 kg fabric by ×5.",
        "What does o.w.f mean?",
        "On fiber weight",
        ", dye amount = fabric weight × o.w.f%; the standard measure in dyeing recipes.",
        "Does bath ratio affect dyeing?",
        "Too large a bath ratio lowers dye use efficiency and raises energy cost; too small hurts levelness; choose 1:8-1:15 by equipment and dye.",
        "About the Dye Ratio Calculator",
        "Dye ratio calculator. A textile/apparel tool to help compute fabric parameters and usage.",
    ]))

    # cutting-1 (30)
    write('cutting-1', build('cutting-1', [
        "🖼️ Cutting Layout Utilization",
        "Input fabric width, marker length and total piece area to compute cutting layout utilization",
        "Core formulas (by input): width÷100×length; max(0,100-rate)",
        "📖 View 'Cutting Layout Utilization User Guide'",
        "Marker length (m)",
        "Total piece area (m²)",
        "💡 Utilization = total piece area ÷ (width × marker length) × 100%",
        "Width in cm, marker length in m, piece area in m²",
        "Higher utilization saves material; excellent layouts exceed 85%",
        "📚 In-depth: Cutting Table Layout Utilization",
        "After layout, check fabric utilization and optimize unit consumption to reduce cost",
        "Compare different width/piece-count plans, pick the highest utilization",
        "When utilization falls below threshold, adjust layout or switch to narrower fabric",
        "Utilization check",
        "Fabric 1.5 m × 2 m = 3 m², net piece area 2.55 m² → utilization = 2.55 / 3 = 85% (good).",
        "Width comparison",
        "Same pattern at 150 cm width 85% vs 120 cm width 72% → narrower is cheaper but raises unit use, price comprehensively.",
        "What utilization is acceptable?",
        "Generally cutting utilization 80%-90%, checks/matching lower; below 80% re-layout or review pattern.",
        "How does utilization relate to unit consumption?",
        "Unit use = fabric area / (pieces × utilization); higher utilization lowers unit use and cost.",
        "About the Cutting Layout Utilization",
        "Cutting layout utilization reflects fabric economy, a key metric for apparel cost control. This tool quickly computes utilization and loss rate from fabric width, marker length and total piece area, helping optimize layout plans and reduce fabric cost.",
        "Utilization and loss rate computed together",
        "Apparel layout plan optimization",
        "Marker maker skill assessment",
        "Cost control and quoting",
        "Fabric width",
        "Marker length",
        "Total piece area",
    ]))

    # density-8 (34)
    write('density-8', build('density-8', [
        "⚙️ Embroidery Stitch Density",
        "Input embroidery area, stitch pitch and thread density to compute stitch count and thread usage",
        "Core formulas (by input): threadMm÷1000; threadM×1.08",
        "📖 View 'Embroidery Stitch Density User Guide'",
        "Embroidery area (cm²)",
        "Stitch pitch (mm)",
        "Thread density (stitches/cm²)",
        "💡 Stitch count = area × thread density; thread usage = stitch count × pitch",
        "Smaller pitch and higher thread density make embroidery denser but use more thread",
        "Actual thread needs 5%-10% allowance (knots, color changes)",
        "📚 In-depth: Fabric Density (stitch / yarn density)",
        "Count warp/weft density on inspection to verify spec compliance",
        "When density anomaly causes GSM/feel deviation, locate yarn or loom issues",
        "Compare densities of different weaves to estimate feel and breathability",
        "Warp/weft density measurement",
        "In a 5×5 cm swatch, 150 horizontal and 140 vertical stitches → warp 150/5 = 30 /cm, weft 140/5 = 28 /cm (i.e. 300×280 /10cm).",
        "Total density",
        "Warp 30 /cm + weft 28 /cm = 58 /cm; total cover factor varies with yarn and weave.",
        "How to count density most accurately?",
        "Use a pick glass to count within 5 cm then convert to 10 cm; avoid edges, take representative middle area.",
        "Is higher density always better?",
        "Not necessarily; high density is thicker but may be stiff and less breathable; balance by use (e.g. summer cloth sparse, workwear dense).",
        "About the Embroidery Stitch Density",
        "Embroidery stitch count and thread usage determine density and cost. This tool computes total stitches, theoretical and loss-inclusive thread usage from area, pitch and thread density, aiding embroidery parameter setting and thread purchasing.",
        "Total stitches and thread usage computed together",
        "Auto-includes 8% loss allowance",
        "Supports custom pitch and thread density",
        "Embroidery parameter setting",
        "Thread usage and purchasing plan",
        "Embroidery cost accounting",
        "Embroidery teaching and design",
        "Embroidery area",
        "Stitch pitch",
        "Thread density",
    ]))

if __name__ == "__main__":
    main()

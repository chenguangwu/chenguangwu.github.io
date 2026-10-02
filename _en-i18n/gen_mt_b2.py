#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'metallurgy')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'metallurgy')
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
    out = {'slug': slug, 'industry': 'metallurgy', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('analysis-price-1', build('analysis-price-1', [
        "\U0001F4CA Price Quote Volatility and Hedging Benchmark Analysis",
        "Enter a price series to compute the mean, range and amplitude, volatility and a hedging benchmark band",
        "Price (Quote / Volatility / Hedging) Analysis",
        "/ Price (Quote / Volatility / Hedging) Analysis",
        "\U0001F4CA Price Quote Volatility and Hedging Benchmark Analysis",
        "Enter a series of same-specification quotes over a period (weekly or monthly) to compute the mean, range and amplitude, standard deviation and coefficient of variation (CV), and to give a \u00b11\u03c3 volatility band around the mean or a custom benchmark price, supporting volatility assessment and hedging decisions.",
        "Price Series (comma or newline separated, unit: CNY/t)",
        "Hedging Benchmark Price (leave blank to use the mean)",
        "Start Analysis",
        "\U0001F4DA In-Depth Analysis: Price Quote Volatility and Hedging Benchmark Analysis",
        "Metals market tracking: enter a series of same-specification quotes over a period (weekly or monthly), compute the mean, range and amplitude, and judge whether the current price is high or low relative to the historical range.",
        "Volatility and hedging decisions: use",
        "to quantify how violently prices move. High volatility raises the need for price locking or hedging, and the mean line can serve as a hedging benchmark price.",
        "Example: 8 periods of copper price (CNY/t)",
        "11, 22, 33, 44, 55, 66, 77, 88. Mean = 49.50, maximum 88, minimum 11, amplitude 77.00, overall standard deviation \u2248 25.20, coefficient of variation \u2248 50.92%. A hedging benchmark price of the mean 49.50 is suggested, with a \u00b11\u03c3 band of about [24.30, 74.70].",
        "How should the coefficient of variation (CV) be read?",
        "CV = standard deviation \u00f7 mean \u00d7 100% removes the effect of units and price level, making it easy to compare how volatile different products are side by side. A larger CV means a less stable price.",
        "How should the hedging benchmark price be set?",
        "Common practice is to use the mean or moving mean of the statistical window as the price-locking reference. When the current price is below the mean and an increase is expected, raise the hedging ratio; otherwise lower it. This tool gives the mean and the \u00b11\u03c3 band for decision making and does not constitute investment advice.",
        "About \"Price (Quote / Volatility / Hedging) Analysis\"",
        "Price (Quote / Volatility / Hedging) Analysis. A free online tool processed entirely in the browser with no data upload, protecting your privacy.",
        "Enter weekly rebar or hot-rolled coil quotes to compute the mean and median and judge the price level",
        "Compare quotes from multiple suppliers of the same specification and use the standard deviation to identify abnormally high batches",
        "Track price series volatility to support price-locking and hedging timing decisions",
        "Cost volatility analysis to assess the impact of material prices on budget",
        "e.g.: 45000,45200,44800,45500",
        "Leave blank = use the mean",
    ]))
    write('steel-calc-1', build('steel-calc-1', [
        "\U0001F9EE Steel Structure Weld Calculation",
        "Check fillet weld strength following the GB 50017 approach to see whether the weld satisfies tension, shear or combined stress requirements.",
        "\"Check fillet weld strength following the GB 50017 approach to see whether the weld satisfies tension, shear or combined stress requirements.\" is computed from the input parameters with professional calculations and outputs a result.",
        "Steel Structure Weld Calculation",
        "/ Steel Structure Weld Calculation",
        "Fillet Weld Leg hf (mm)",
        "Calculated Weld Length lw (mm)",
        "Axial Force N (kN)",
        "Shear Force V (kN)",
        "Bending Moment M (kN\u00b7m)",
        "Weld Strength Design Value ffw (N/mm\u00b2)",
        "Fillet Weld Strength Increase Coefficient \u03b2f",
        "Butt Weld Plate Thickness t (mm)",
        "Fillet weld effective thickness he = 0.7 hf",
        "Fillet weld combined stress: \u221a[(\u03c3f/\u03b2f)\u00b2 + \u03c4f\u00b2] \u2264 ffw",
        "Butt weld normal stress \u03c3 = N/(t\u00b7lw) + M/W, shear stress \u03c4 = V/(t\u00b7lw)",
        "The calculation length has already deducted the arc start and end effect, so please enter the actual effective length",
        "\U0001F4DA In-Depth Analysis: Steel Structure Weld Calculation",
        "Fillet weld check for steel beam connections in factory buildings: for corbel or splice joints carrying combined axial tension, shear and bending, check per GB 50017 whether the fillet weld combined stress is satisfied.",
        "Butt weld check for embedded parts in equipment foundations: for butt joints under tension, compression and bending, verify that normal stress, shear stress and equivalent stress stay within the weld strength design value.",
        "Weld review for retrofits and strengthening: when reinforcing existing welds or adding load-carrying welds, back-calculate the required leg size or length to avoid insufficient or excessive design.",
        "Fillet weld check (hf8 / lw200 / N120kN / V50kN / M8kN\u00b7m / ffw160 / \u03b2f1.22)",
        "Effective thickness he=0.7hf=5.6 mm; effective area A=he\u00d7lw=1120 mm\u00b2; axial normal stress \u03c3f=N/A=120000/1120=107.14 N/mm\u00b2; shear stress \u03c4f=V/A=50000/1120=44.64 N/mm\u00b2; section modulus for bending W=he\u00d7lw\u00b2/6=5.6\u00d7200\u00b2/6=37333 mm\u00b3, bending normal stress \u03c3fM=M/W=8e6/37333=214.29 N/mm\u00b2; combined stress \u221a[(\u03c3f+\u03c3fM)/\u03b2f)\u00b2 + \u03c4f\u00b2] = \u221a[(321.43/1.22)\u00b2 + 44.64\u00b2] = 267.22 N/mm\u00b2; stress ratio 267.22/160=167.0%, so it does not satisfy the requirement and hf must be increased or lw lengthened. Converting to an equivalent butt weld under the same load (t10): \u03c3=180, \u03c4=25, equivalent stress \u221a(180\u00b2+3\u00d725\u00b2)=185.14, stress ratio 115.7%, still not satisfied, indicating the joint load is on the high side.",
        "Why is the fillet weld effective thickness taken as 0.7hf?",
        "The load-bearing section of a fillet weld is the minimum section along the 45\u00b0 direction, whose thickness is about 0.7 times the leg size hf (he=0.7hf). This is a simplified assumption in GB 50017; actual penetration is slightly greater, but designing at 0.7hf is on the safe side.",
        "What if the check fails?",
        "Increase the leg size hf, lengthen the calculated length lw, or switch to a butt weld (with a larger effective section). You can also reduce the load or add stiffeners. Note that the calculation length has already deducted the defective arc start and end segments, so the input should be the effective length; results serve as preliminary design only, and official drawings follow the design calculation sheet.",
        "Butt welds use",
    ]))
    write('analysis-grade', build('analysis-grade', [
        "\U0001F4CA Tailings (Grade / Loss / Utilisation) Analysis",
        "Grade / Loss / Utilisation",
        "Back-calculate from the two-product mass balance: from raw ore grade \u03b1, concentrate grade \u03b2 and tailings grade \u03b8, the concentrate yield \u03b3 = (\u03b1 \u2212 \u03b8) \u00f7 (\u03b2 \u2212 \u03b8), then the recovery \u03b5 = \u03b3 \u00d7 \u03b2 \u00f7 \u03b1, and give the metal lost with the tailings and the loss rate. Metal grades must be reconciled with on-site metering and assay values; this result is for process estimation and teaching demonstration only.",
        "Tailings (Grade / Loss / Utilisation) Analysis",
        "/ Tailings (Grade / Loss / Utilisation) Analysis",
        "Beneficiation metrics: concentrate yield \u03b3 = (raw ore grade \u2212 tailings grade) \u00f7 (concentrate grade \u2212 tailings grade) \u00d7 100%; concentrate recovery = \u03b3 \u00d7 concentrate grade \u00f7 raw ore grade; tailings metal loss rate = tailings grade \u00d7 tailings yield \u00f7 raw ore grade; enrichment ratio = concentrate grade \u00f7 raw ore grade.",
        "Raw Ore Treated Q (t)",
        "Raw Ore Grade \u03b1 (%)",
        "Concentrate Grade \u03b2 (%)",
        "Tailings Grade \u03b8 (%)",
        "Metal Balance Analysis",
        "\U0001F4DA In-Depth Analysis: Tailings (Grade / Loss / Utilisation) Analysis",
        "Metal balance in a concentrator: given the raw ore tonnage and raw ore grade, the concentrate output and concentrate grade, back-calculate the tailings grade and check whether it exceeds the design tailings specification.",
        "Assessing resource loss: use the useful component grade in the tailings and the tailings yield to compute the metal carried away and the loss rate, and judge whether recovery meets target.",
        "Tailings re-treatment and comprehensive utilisation: judge re-treatment value or suitability for brick making, backfill and other uses from the remaining useful mineral and associated element grades in the tailings.",
        "Example: copper metal balance and tailings grade",
        "Raw ore treated 10000 t at 1.0% grade gives 100 t of contained copper; concentrate output 200 t at 20% grade gives 40 t of contained copper. Copper in tailings = 100 \u2212 40 = 60 t; tailings yield = 1 \u2212 200/10000 = 98%. Tailings grade = 60 \u00f7 (10000 \u2212 200) \u00d7 100% = 0.612%. Recovery = (100 \u2212 60) \u00f7 100 \u00d7 100% = 40% (in this example the concentrate output is low, the recovery is uneconomic and the separation operation needs review).",
        "What is the relationship between tailings grade and recovery?",
        "Recovery = (raw ore metal \u2212 tailings metal) \u00f7 raw ore metal \u00d7 100%. At fixed raw ore grade and tonnage, a lower tailings grade means less metal carried away and higher recovery. Concentrators usually take improving recovery and lowering tailings grade as their core performance metrics.",
        "Do tailings have utilisation value?",
        "It depends on the remaining useful minerals and associated element grades. If the tailings still carry decent grades of metal or valuable elements they can be re-treated; tailings containing iron, silicon and calcium are often used as cement blend material, brick raw material or underground backfill aggregate, reducing volume while adding value.",
        "About \"Tailings (Grade / Loss / Utilisation) Analysis\"",
        "Tailings (Grade / Loss / Utilisation) Analysis. A free online tool processed entirely in the browser with no data upload, protecting your privacy.",
    ]))
    write('convert-hardness', build('convert-hardness', [
        "\U0001F504 Brinell / Rockwell / Vickers Hardness Conversion Table",
        "An online Brinell / Rockwell / Vickers hardness conversion table",
        "Brinell",
        "Milli-Brinell",
        "Kilo-Brinell",
        "Rockwell",
        "Milli-Rockwell",
        "Kilo-Rockwell",
        "\U0001F4DA In-Depth Analysis: Brinell / Rockwell / Vickers Hardness Conversion Table",
        "When only one hardness scale reading is available on site, scale units linearly within the same scale (such as milli/kilo prefix conversion).",
        "Distinguishing \"the same scale",
        "\" from \"cross-scale hardness equivalence\": cross-scale (HRC\u2194HBW\u2194HV) must use interpolation from a reference table and cannot use a linear factor.",
        "When organising test data in bulk, first normalise readings with different prefixes to the same magnitude before comparing.",
        "Linear Scaling Within the Same Scale",
        "This tool converts readings linearly within the same scale: output = original value \u00d7 rate \u00d7 f \u00b7 t, where the unit factor f takes milli = 1, kilo = 0.001, other = 1000 (switched according to the chosen magnitude). This changes only the magnitude of the number, not the hardness itself.",
        "Difference from Cross-scale Conversion",
        "To convert HRC 30 to HBW you cannot use a linear factor; you must interpolate from the ASTM E140 reference table (about HBW 285). The linear scaling here is only for converting magnitudes of the same scale such as \"285 HBW\" to \"0.285 kHBW\", so that unit conversion is not mistaken for hardness equivalence.",
        "Why can't HRC be multiplied by a factor to give HBW?",
        "The three scales differ in indenter, load and geometric definition, and the calibration curves are non-linear, so a reference table is mandatory. Linear factors apply only to prefix magnitude conversion within one scale.",
        "How do I use the milli/kilo factor?",
        "When the reading unit is milli (\u00d71), kilo (\u00d70.001) or other (\u00d71000), the tool normalises the magnitude by the factor; essentially shifting the integer positions, with no change in physical meaning.",
        "About \"Brinell / Rockwell / Vickers Hardness Conversion Table\"",
        "Brinell / Rockwell / Vickers Hardness Conversion Table. A free online tool processed entirely in the browser with no data upload, protecting your privacy.",
    ]))


if __name__ == '__main__':
    main()
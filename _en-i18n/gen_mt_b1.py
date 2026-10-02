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
    write('power-6', build('power-6', [
        "\u26a1 Electric Furnace (Arc / Power / Electrode) Smelting",
        "Compute the specific power consumption per tonne, the electricity cost per tonne and the cost per heat from power consumption and steel output.",
        "Specific power = power consumption per heat \u00f7 steel output (kWh/t); cost per tonne = specific power \u00d7 electricity price (using CNY 0.6/kWh)",
        "Specific power consumption is the core energy metric of electric arc furnace smelting (industry advanced level about 350 kWh/t). This tool also gives the cost per tonne of steel and the cost per heat based on CNY 0.6/kWh.",
        "Power Consumption per Heat (kWh)",
        "Steel Output (t)",
        "\U0001F4A1 Specific power = consumption \u00f7 output (kWh/t); the advanced industry level is about 350 kWh/t; electricity price is estimated at CNY 0.6/kWh.",
        "\U0001F4DA In-Depth Analysis: Electric Furnace (Arc / Power / Electrode) Smelting",
        "Benchmarking Specific Power: divide the power consumption per heat by the steel output to get kWh/t and compare against the industry advanced level (about 350 kWh/t) to judge how well the furnace is running.",
        "Smelting cost accounting: convert the power consumption into cost per tonne and cost per heat at the electricity price, for quotation and cost control.",
        "Power supply check: estimate the average active power from the power consumption per heat and the smelting time to judge whether transformer capacity and the power supply scheme match.",
        "Example: 20000 kWh per heat, 50 t output",
        "Specific power = 20000 \u00f7 50 = 400.00 kWh/t. At CNY 0.6/kWh the cost per tonne is 400.00 \u00d7 0.6 = CNY 240.00/t and the cost per heat is 20000 \u00d7 0.6 = CNY 12000.00. Steel output per kWh = 50 \u00f7 20000 \u00d7 1000 = 2.5000 kg/kWh.",
        "What specific power is normal for an electric arc furnace?",
        "A conventional electric arc furnace smelting carbon steel runs about 380 to 450 kWh/t. With scrap preheating or an ultra-high-power furnace this can fall to 320 to 360 kWh/t. Full-scrap short process and long process have different measurement conventions, so process conditions must be stated when comparing.",
        "Why look at cost per tonne as well?",
        "Electricity price differences strongly affect the cost conclusion: two plants with identical power consumption can differ by tens of CNY per tonne because of different tariffs, so quotation and cost-reduction decisions must be made on a monetary basis.",
        "About \"Electric Furnace (Arc / Power / Electrode) Smelting\"",
        "Electric Furnace (Arc / Power / Electrode) Smelting. A free online tool processed entirely in the browser with no data upload, protecting your privacy.",
        "How to Use Electric Furnace (Arc / Power / Electrode) Smelting",
        "Arc",
        "What Does Electric Furnace (Arc / Power / Electrode) Smelting Do?",
        "This electric furnace smelting calculator estimates steelmaking power consumption and smelting rhythm from parameters such as arc power and electrodes, suited to electric arc furnace process optimisation and energy management.",
        "How Do I Use Electric Furnace (Arc / Power / Electrode) Smelting?",
        "What Scenarios Suit Electric Furnace (Arc / Power / Electrode) Smelting?",
        "Arc",
    ]))
    write('stats-10', build('stats-10', [
        "\U0001F4CA Metal (Yield and Product Rate) Statistics",
        "Yield Rate / Product Rate",
        "From the weights of metallic charge fed, qualified cast billet (ingot) and qualified finished product, compute metal yield and product rate at two levels, plus the combined product rate and metal loss, to measure metal loss across the process and processing efficiency. Data is processed only locally in the browser and never uploaded.",
        "Yield rate = qualified billet (ingot) \u00f7 metallic charge \u00d7 100%",
        "Product rate = qualified finished product \u00f7 qualified billet (ingot) \u00d7 100%",
        "From the weights of metallic charge fed, qualified cast billet (ingot) and qualified finished product, compute metal yield and product rate at two levels, plus the combined product rate and metal loss, to measure metal loss across the process and processing efficiency. All data is processed only locally in the browser and never uploaded.",
        "Metallic Charge Fed (t)",
        "Qualified Billet (Ingot) (t)",
        "Qualified Finished Product (t)",
        "\U0001F4DA In-Depth Analysis: Metal Yield and Product Rate Statistics",
        "Compute metal yield and product rate for steelmaking and rolling to measure metal loss across the process and processing efficiency.",
        "Enter by heat or by batch to compare yield and product rate differences across crews and steel grades.",
        "Use the product rate trend to monitor equipment condition and process stability.",
        "Yield Rate and Product Rate",
        "Metal yield = metal output \u00f7 metal input \u00d7 100%; product rate = qualified product \u00f7 raw material \u00d7 100%.",
        "Descriptive statistics",
        ": mean = \u03a3x/n;",
        "(median after sorting); variance = \u03a3(x \u2212 mean)\u00b2/n;",
        "= \u221avariance; range = maximum \u2212 minimum.",
        "Feeding 100 t of raw material yields 92 t of qualified product, so the product rate = 92%. Yield rates (%) for 10 heats: 91, 93, 92, 90, 94, 92, 93, 91, 92, 95; mean 92.3%, range 95 \u2212 90 = 5%, standard deviation about 1.4%. A heat dropping to 85% is a clear deviation and oxidation or metal-loss issues should be investigated.",
        "How do yield rate and product rate differ?",
        "Yield rate looks at metal recovery in the smelting step (output / input), while product rate looks at the qualified proportion in the processing step (qualified product / raw material). The former includes melt loss, the latter includes processing scrap.",
        "What does a large range mean?",
        "A large range or standard deviation means large variation between heats, so the process or raw material is unstable. Continuous monitoring reveals equipment degradation or operational drift early.",
        "About \"Metal (Yield and Product Rate) Statistics\"",
        "Metal (Yield and Product Rate) Statistics. A free online tool processed entirely in the browser with no data upload, protecting your privacy.",
    ]))
    write('calc-1', build('calc-1', [
        "\U0001F504 Alloy Composition Conversion",
        "Compute the required charge quantities from the target alloy mass, target element contents and raw material composition.",
        "Additive required = target element mass \u00f7 (additive purity \u00d7 element content)",
        "Target Total Alloy Mass (kg)",
        "Target Main Element Content (%)",
        "Target Added Element Content (%)",
        "Main Raw Material Purity (%)",
        "Additive Purity (%)",
        "Target Element Content in Additive (%)",
        "Compute Charge",
        "Target element mass = total alloy mass \u00d7 target content",
        "Main raw material required = total alloy mass \u2212 additive required",
        "Burn loss and impurities are not included, so allow margin in the actual charge",
        "\U0001F4DA In-Depth Analysis: Alloy Composition Conversion",
        "Back-calculate the mass of intermediate alloy to add from the target content of the added element when charging, to avoid relying on experience and getting it wrong.",
        "Given the additive purity and the proportion of the target element it contains, back-calculate the actual intermediate alloy mass to charge and deduct it from the main metal mass.",
        "When adding several elements at once, back-calculate each one and sum the total addition and the final charge weight.",
        "Back-calculation Formula",
        "Element mass to add mAddElement = M \u00d7 targetAdd / 100 (M is the main metal mass and targetAdd the target percentage). Intermediate alloy charge mAdditive = mAddElement \u00f7 (addPurity/100) \u00f7 (addContent/100) (addPurity is additive purity and addContent is the element content in the additive). Main metal charge mMain = M \u2212 mAdditive.",
        "For 100 kg of main metal needing 2% of an element, with additive purity 99% and 60% of that element: mAddElement = 100\u00d72/100 = 2 kg; mAdditive = 2 \u00f7 0.99 \u00f7 0.60 = 2 \u00f7 0.594 \u2248 3.367 kg; mMain = 100 \u2212 3.367 = 96.633 kg. That is, charge 96.633 kg of main metal plus 3.367 kg of intermediate alloy.",
        "What is the difference between purity and content?",
        "Purity is how clean the intermediate alloy itself is (such as 99%), while content is the mass fraction of the target element within that alloy (such as 60% of the element). Both must be divided out to get the charge that actually contributes the target element.",
        "How is burn loss accounted for?",
        "This formula does not include burn loss. Easily oxidised elements (such as Al, Mg and Si) need extra charge based on the process burn loss rate, or a recovery coefficient correction in the final composition step.",
    ]))
    write('analysis-34', build('analysis-34', [
        "\U0001F4CA Metallurgical (QC / Spectrometry / Chemical) Analysis",
        "QC / Spectrometry / Chemical",
        "The standard deviation and relative standard deviation of parallel measurements evaluate method precision, the difference from the certified value of a reference material evaluates accuracy, and the spike recovery reflects matrix interference and procedural loss. Only all three together show whether a batch of spectrometry or chemical results can be reported: precision passing with low recovery usually points to a matrix effect, while accuracy and precision both out of tolerance usually means an instrument or preparation problem. Calculations run locally in your browser and entered data is never uploaded.",
        "RSD = SD \u00f7 mean \u00d7 100%; relative error RE = (mean \u2212 certified value) \u00f7 certified value \u00d7 100%; spike recovery = (spiked result \u2212 background) \u00f7 spike amount \u00d7 100%",
        "Parallel Measurements (comma, space or newline separated, %)",
        "Certified Value of Reference Material (%)",
        "Background Measured (%)",
        "Spike Amount (%)",
        "Result After Spiking (%)",
        "Method RSD Upper Limit (%)",
        "Relative Error Upper Limit (%, take absolute value)",
        "\U0001F4DA In-Depth Analysis: Metallurgical (QC / Spectrometry / Chemical) Analysis",
        "Compute recovery, relative standard deviation (RSD) and composition deviation for spectrometry and chemical test results to assess method reliability.",
        "Quantify unknown samples against a calibration curve and check the linear range and",
        "correlation coefficient",
        "Monitor composition deviation across batches to identify systematic offsets and random error.",
        "Analytical Statistics",
        "Recovery = (result after spike \u2212 background) \u00f7 spike amount \u00d7 100%, evaluating method accuracy; relative standard deviation RSD =",
        "SD \u00f7 mean \u00d7 100%, evaluating precision; relative error RE = (mean \u2212 certified value) \u00f7 certified value \u00d7 100%; composition deviation is the difference between the mean and the certified value. SD is computed on the n\u22121 sample basis, and this must be stated when reporting, otherwise it cannot be compared directly with the population basis using n.",
        "For an element with a certified value of 0.50% and 5 parallel measurements of 0.48, 0.51, 0.49, 0.50 and 0.52%: mean 0.5000%, sample",
        "SD = 0.01581%, RSD = 3.16% (on the population basis dividing by n it would be SD 0.01414% and RSD 2.83%; the two must not be mixed). In the spike experiment the background is 0.50%, 0.20% is added and 0.69% is measured after spiking, so recovery = (0.69 \u2212 0.50) \u00f7 0.20 \u00d7 100% = 95.00%, which falls in the good 95% to 105% band.",
        "What RSD counts as passing?",
        "It depends on the standard and the level: for major components RSD under 2 to 5% is typical, and trace analysis may be relaxed. Follow the method standard or internal control criteria; here 2.8% is good.",
        "What does a low recovery indicate?",
        "Possible matrix interference, loss or non-linear calibration. Matrix matching or spike correction is needed, and measured values must not simply be reported as true values.",
        "About \"Metallurgical (QC / Spectrometry / Chemical) Analysis\"",
        "Metallurgical (QC / Spectrometry / Chemical) Analysis. A free online tool processed entirely in the browser with no data upload, protecting your privacy.",
        "e.g.: 0.48,0.51,0.49,0.50,0.52",
    ]))


if __name__ == '__main__':
    main()
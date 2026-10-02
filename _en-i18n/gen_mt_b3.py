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
    write('hardness-conversion', build('hardness-conversion', [
        "\U0001F504 Hardness Conversion Table",
        "Brinell (HB), Rockwell (HRC/HRB) and Vickers (HV) hardness conversion using approximate values per ASTM E140 / GB/T 33362.",
        "Hardness conversion (ASTM E140 / GB/T 33362 approximation): convert Brinell HB, Rockwell HRC/HRB and Vickers HV by linear interpolation on the standard reference table; hardness on different scales for the same material corresponds to the same tensile strength band, so HRC 20 corresponds to about HB 238 and HV 247, and HRC 40 to about HB 371 and HV 392.",
        "Input Hardness Type",
        "Rockwell HRC",
        "Brinell HBW",
        "Vickers HV",
        "Rockwell HRB",
        "\U0001F4CB Common Hardness Conversion Reference Table",
        "HRC suits hardened high-hardness steel (20 to 70); HBW suits annealed or normalised steel and castings; HV has the widest applicability and converts directly to strength.",
        "The conversion relationship is a non-linear empirical approximation that varies by material and standard, so this table applies to carbon steel and low-alloy steel.",
        "\U0001F4DA In-Depth Analysis: Hardness Conversion Table",
        "When drawings specify one hardness scale but incoming material only has a reading on another, interpolate between them using the ASTM E140 reference table.",
        "Use",
        "to estimate approximate tensile strength from material hardness for quick material selection judgements.",
        "Normalise test data across scales in batches to make SPC statistics and cross-comparison easier.",
        "Reference Table Interpolation",
        "Common approximate correspondence points: HRC 20\u2248HBW 225\u2248HV 240; HRC 40\u2248HBW 380\u2248HV 400; HRC 60\u2248HBW 700\u2248HV 700 (carbon steel approximation; high-alloy steels deviate). Interpolation is estimated linearly between adjacent points, and error grows beyond the calibrated range.",
        "Empirical Tensile Strength Estimation",
        "For annealed or normalised carbon steel, approximate tensile strength \u03c3b \u2248 HV \u00d7 3.0 (MPa). For example HV 240 gives \u03c3b\u2248720 MPa and HV 400 gives \u03c3b\u22481200 MPa. This is an empirical relation; heat treatment state and alloying change the ratio significantly, so for formal material selection follow tensile testing.",
        "Can the hardness conversion table replace real testing?",
        "No. The table is a statistical empirical relation affected by material, heat treatment and scale range. Strength of critical parts must still be determined by tensile testing; conversion is only a quick reference.",
        "Why do high-alloy steels deviate more?",
        "Alloying elements change work hardening and matrix strength, shifting the hardness-to-strength ratio, and different scales respond differently to different matrices, so cross-scale error is more pronounced in high-alloy materials.",
        "About \"Hardness Conversion Table\"",
        "Hardness Conversion Table is an online tool in the business and office domain. A business and office tool that improves work efficiency with local data processing that protects privacy.",
    ]))
    write('energy-1', build('energy-1', [
        "\u26a1 Energy Consumption (per Tonne of Steel / Aluminium, Energy Saving and Emission Reduction)",
        "Convert electricity and gas savings into standard coal equivalent and estimate the corresponding carbon dioxide reduction and equivalent energy.",
        "Standard coal equivalent = (electricity saved \u00d7 0.1229 + gas saved \u00d7 1.33) \u00f7 1000 (tce); CO\u2082 reduction \u2248 standard coal \u00d7 2.66 (t); equivalent energy = standard coal \u00d7 29.307 (GJ)",
        "Aggregate energy savings using the equivalent-value conversion factors (1 kWh = 0.1229 kgce, 1 m\u00b3 of natural gas = 1.33 kgce), then convert into the three conventions of tce, tCO\u2082 and GJ, for energy efficiency assessment and carbon accounting.",
        "Electricity Saved (kWh)",
        "Gas Saved (m\u00b3)",
        "\U0001F4A1 Standard coal = (electricity \u00d7 0.1229 + gas \u00d7 1.33) \u00f7 1000 tce; 1 tce \u2248 2.66 tCO\u2082 \u2248 29.307 GJ.",
        "\U0001F4DA In-Depth Analysis: Energy Consumption (per Tonne of Steel / Aluminium, Energy Saving and Emission Reduction)",
        "Energy efficiency assessment and reporting: convert electricity and gas savings into standard coal equivalent by equivalent value, aggregate into the tce convention for reporting, and meet energy audit and efficiency benchmarking requirements.",
        "Carbon accounting: convert standard coal into CO\u2082 reduction to track progress against dual-carbon goals and prepare for carbon asset verification.",
        "Verifying technical retrofit benefits: count energy savings before and after the retrofit and convert to emission reduction to quantify the benefit of a single piece of equipment or production line.",
        "Example: 100000 kWh and 5000 m\u00b3 of gas saved",
        "Standard coal = (100000 \u00d7 0.1229 + 5000 \u00d7 1.33) \u00f7 1000 = 18.940 tce; CO\u2082 reduction = 18.94 \u00d7 2.66 = 50.38 t; equivalent energy = 18.94 \u00d7 29.307 = 555.1 GJ; equivalent to 18940.0 kgce.",
        "How are the conversion factors 0.1229 and 1.33 set?",
        "They follow the equivalent-value convention of the Chinese general",
        "energy consumption calculation",
        "rules: 1 kWh of electricity converts to 0.1229 kgce and 1 m\u00b3 of natural gas to 1.33 kgce. Under the equivalent-value approach (accounting for generation efficiency) the electricity factor is about 0.3 kgce/kWh, and the different conventions give very different results.",
        "Why is CO\u2082 reduction taken as 2.66 t/tce?",
        "The carbon emission factor of standard coal is about 2.66 tCO\u2082/tce (sources give 2.66 to 2.77). It corresponds to a coal-dominated energy structure; if the savings come from green power, use the emission factor of the relevant grid instead.",
        "About \"Energy Consumption (per Tonne of Steel / Aluminium, Energy Saving and Emission Reduction)\"",
        "Energy Consumption (per Tonne of Steel / Aluminium, Energy Saving and Emission Reduction). A free online tool processed entirely in the browser with no data upload, protecting your privacy.",
        "Tonne of Steel",
        "Tonne of Aluminium",
    ]))
    write('alloy-ratio', build('alloy-ratio', [
        "\U0001F9EE Alloy Ratio Calculator",
        "Compute the amount of each ferroalloy raw material to add from the target element content (Cr/Ni/Mo and so on), with recovery correction.",
        "Core formula (over the input variables): delta \u00f7 (e.rawPct\u00f7100 \u00d7 e.recovery\u00f7100); W \u00d7 (e.target \u2212 initPct) \u00f7 100",
        "Molten Steel Weight W (t)",
        "Initial Element Content in the Steel (%)",
        "Target Element to Raw Material Ratio",
        "Target Content (%)",
        "Raw Material Alloy Content (%)",
        "Recovery (%)",
        "+ Add Element",
        "Compute Addition",
        "\U0001F4CB Calculation Notes",
        "The increment for an element \u0394M = W \u00d7 (target content \u2212 initial content) / 100 (t)",
        "Raw material addition = \u0394M \u00f7 (raw material alloy content \u00d7 recovery)",
        "Example:",
        "For 5t of steel needing Cr raised to 18%, with high-carbon ferrochrome as the raw material (60% Cr, 95% recovery), addition = 5\u00d718% \u00f7 (60%\u00d795%) \u2248 1.58 t.",
        "Note: this tool is a theoretical estimate and does not consider side effects such as carbon or phosphorus introduced by the raw material, or temperature effects.",
        "\U0001F4DA In-Depth Analysis: Alloy Ratio Calculator",
        "Back",
        "alloy composition",
        "from the target to get the raw material mass to add, for the melting charge sheet.",
        "Account for raw material alloy content and smelting recovery to avoid under-charging leading to a low composition.",
        "With multi-element targets, back-calculate each element separately and take the largest of the raw material additions for coordinated charging.",
        "Back-calculation Formula",
        "Element mass to add \u0394M = W \u00d7 (target content \u2212 initial content) / 100 (W is the molten steel mass). Raw material addition = \u0394M \u00f7 (raw material alloy content \u00d7 recovery). Recovery reflects the actual yield of that element in smelting and is below 1 for easily oxidised elements.",
        "For 5 t of steel targeting Cr 18% (initial negligible) with high-carbon ferrochrome (60% Cr, 95% recovery): \u0394M = 5000\u00d7(18\u22120)/100 = 900 kg; addition = 900 \u00f7 (0.60\u00d70.95) = 900 \u00f7 0.57 \u2248 1579 kg \u2248 1.58 t. So about 1.58 t of high-carbon ferrochrome is needed to make up the Cr.",
        "How is recovery chosen?",
        "Take empirical values based on furnace type and oxidation tendency (of the order Cr 95%, Si 85%, Mn 80%) and adjust from the furnace-side assay. Choosing too low leads to under-charging and a low composition.",
        "What if the initial content cannot be ignored?",
        "Use (target \u2212 initial) in the formula. If the steel already contains some Cr, only the difference needs topping up and the addition drops accordingly, avoiding over-alloying.",
        "About \"Alloy Ratio Calculator\"",
        "Alloy Ratio Calculator is an online tool in the business and office domain. A business and office tool that improves work efficiency with local data processing that protects privacy.",
    ]))
    write('heat-treatment', build('heat-treatment', [
        "\U0001F529 Heat Treatment Time Curve",
        "Estimate workpiece heating time, holding time and total process time, and generate a heat treatment time-temperature curve.",
        "Core formula (over the input variables): (temp \u2212 roomT) \u00f7 heatRate \u00d7 60; heatMin \u00d7 (1 + d\u00f7200)",
        "Effective Workpiece Thickness d (mm)",
        "Workpiece Material",
        "Tool Steel",
        "Heating Temperature (\u00b0C)",
        "Heating Rate (\u00b0C/h)",
        "Holding Coefficient (min/mm)",
        "\U0001F4CB Process Reference",
        "Heating time experience:",
        "\u03c4_heat = d \u00f7 v \u00d7 60 + loading correction (this tool estimates from ramp to temperature)",
        "Holding time:",
        "\u03c4_hold = holding coefficient \u00d7 d, carbon steel 1.0 to 1.5, alloy steel 1.5 to 2.0, tool steel 2.0 to 2.5 min/mm.",
        "Holding coefficient reference:",
        "carbon steel 1.2, alloy steel 1.8, tool steel 2.2, stainless steel 2.0 min/mm (use the lower bound for salt bath furnaces and the upper bound for air furnaces).",
        "Annealing requires furnace cooling (very slow), normalising is air cooled, quenching uses quenching medium, and tempering is generally air cooled.",
        "\U0001F4DA In-Depth Analysis: Heat Treatment Time Curve",
        "When writing process cards for annealing, quenching and normalising, estimate the duration of heating, holding and cooling stages for scheduling and energy forecasting.",
        "Give baseline holding and cooling times from the effective workpiece thickness and material coefficient, distinguishing carbon steel, alloy steel, tool steel and stainless steel.",
        "Extend heating time for large sections with a thickness correction factor so the core is not left un-heated.",
        "Stage Duration Formula",
        "Heating baseline heatMin = (temp\u221220)/heatRate \u00d7 60; thickness correction heatMinAdj = heatMin \u00d7 (1 + d/200) (d is effective thickness in mm). Holding holdMin = holdCoef \u00d7 d (holdCoef is the material coefficient in min/mm). Cooling coolMin: annealing d\u00d74, quenching d\u00d70.2, normalising and others d\u00d71.5. Material coefficients MAT_COEF: carbon steel 1.2, alloy steel 1.8, tool steel 2.2, stainless steel 2.0 min/mm.",
        "Worked example (built-in tool model)",
        "Annealing at 820\u00b0C, heating rate 100, effective thickness 30 mm, holdCoef 1.2: heatMin=(800)/100\u00d760=480; heatMinAdj=480\u00d7(1+30/200)=480\u00d71.15=552; holdMin=1.2\u00d730=36; coolMin (annealing)=30\u00d74=120; total \u2248 552+36+120=708 (units follow the tool's built-in calibration and are best used as relative scheduling reference).",
        "Why is holding time proportional to thickness?",
        "Heat must reach the core and homogenise the structure, and conduction plus phase transformation take time, so holding increases linearly with effective thickness. The material coefficient reflects how easy conduction and phase transformation are.",
        "Why is quenching cooling time so short?",
        "Quenching must pass quickly through the pearlite or bainite nose, so the cooling stage coefficient is small (d\u00d70.2). In practice the medium's cooling capability and workpiece size govern; the tool gives a process scheduling baseline.",
        "About \"Heat Treatment Time Curve\"",
        "Heat Treatment Time Curve is an online tool in the business and office domain. A business and office tool that improves work efficiency with local data processing that protects privacy.",
    ]))


if __name__ == '__main__':
    main()
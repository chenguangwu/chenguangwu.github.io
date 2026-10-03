#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'mining')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'mining')
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
    out = {'slug': slug, 'industry': 'mining', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('excavation-volume', build('excavation-volume', [
        "📐 Excavation Volume Calculator",
        "Volume and earthwork calculation for pits, road cuts and mine pits",
        "Core formulas (by input variable): (π × H ÷ 3) × (R1×R1 + R1×R2 + R2×R2); (W1Actual + W2) ÷ 2 × D × L; Math.ceil(looseVolume ÷ 20)",
        "Excavation Volume Calculator",
        "/ Excavation Volume",
        "Excavation shape",
        "Swell factor (1.2-1.5)",
        "Unit earthwork price (CNY/m³)",
        "📐 Calculate excavation volume",
        "👆 Select a shape to start calculating",
        "📚 Deep Dive: Excavation Volume Calculator",
        "Infrastructure stripping or stope widening: compute the in-situ volume for cuboid, trapezoidal section, cylinder/frustum, pit and other shapes, then multiply by the swell factor to get the loose volume.",
        "Earthwork cost calculation: volume × unit price gives the total cost, supporting tendering and settlement.",
        "Slope/pit estimation: apply a slope coefficient or a simplified slope enlargement to get an approximate volume including the slope.",
        "Formula scope",
        "Cuboid V=L·W·D; trapezoidal section V=(top width+bottom width)/2×depth×length (with a slope, top width = bottom width + 2·depth·slope); cylinder V=πR²H, frustum V=πH/3·(R₁²+R₁R₂+R₂²); loose volume = in-situ volume × swell factor; cost = in-situ volume × unit price.",
        "Worked example (cuboid)",
        "Pit length 20 m, width 10 m, depth 3 m, swell factor 1.3, unit price 20 CNY/m³. In-situ volume 600 m³, loose volume 780 m³, total cost 12,000 CNY.",
        "Boundary: switching shapes",
        "Switch to a frustum (D1=20, D2=10, H=5): V=π·5/3·(100+50+25)=π·5/3·175≈916.3 m³. For a cylinder (D2=0), V=πR₁²H. Pit mode applies a simplified slope enlargement of 0.6·depth, so its volume is slightly larger than a pure cuboid.",
        "Why do the in-situ and loose volumes differ by a factor of 1.3?",
        "After excavation the pore space increases and the material bulks up; the swell/loosenability factor swell describes this bulking (generally 1.2–1.3 for soil, larger for rock). In-situ volume = original volume, loose volume = volume of the loose pile after excavation. Transport and waste dump capacity are counted by the loose volume, while quantity settlement often uses the in-situ volume; the two must not be mixed.",
        "Why does the trapezoidal section add 2·depth·slope to the top width?",
        "In sloped excavation the pit top is wider than the pit bottom, and the widening per side = depth × slope coefficient (e.g. a 1:1 slope has coefficient 1), so both sides add 2·depth·slope. Otherwise, using only the bottom width misses the triangular slope volume and underestimates the earthwork.",
        "About 'Excavation Volume'",
        "Excavation Volume is an online tool in the mining and metallurgy field. A mining and metallurgy tool that helps compute mineral parameters and indicators.",
    ]))

    write('convert-grade-ore', build('convert-grade-ore', [
        "🔄 Ore Grade (g/t) and Value Conversion",
        "g/t",
        "Ore grade",
        "Milli ore grade",
        "Kilo ore grade",
        "Value conversion",
        "Milli value conversion",
        "Kilo value conversion",
        "📚 Deep Dive: Ore Grade (g/t) and Value Conversion",
        "Convert the grade figures (g/t or %) from an assay report by a",
        "coefficient, then combine with the unit price to quickly estimate the metal value per tonne of ore.",
        "Aligning different unit conventions: unify milli/kilo-prefixed grade or value units to the standard unit, avoiding quotation errors.",
        "Scheme comparison: compare the value per tonne of ore of the same ore body at different cut-off grades, supporting decisions on the mining cut-off grade.",
        "Formula scope",
        "Output r = grade value val × coefficient rate × from/to. from/to are the unit conversion multipliers (1 =",
        "/ value, 0.001 = milli, 1000 = kilo); rate is the unit price multiplier (e.g. CNY per gram). In essence it is the generic multiplier of grade × unit price × unit conversion.",
        "For a gold ore with grade 5 g/t, unit price 500 CNY/g, from=ore grade (1), to=value (1): r=5×500×1/1=2500 (CNY per tonne of ore). Meaning: each tonne of run-of-mine ore contains 5 g of gold, which at 500 CNY/g is worth 2500 CNY. [SRC]",
        "Boundary: unit mismatch",
        "If from/to is chosen wrongly (e.g. entering g/t as %), the result differs by a factor of 10000 (1% = 10000 g/t). The tool does not validate unit semantics, it is pure mathematical multiplication, so you must confirm that from/to and val have matching dimensions before use; rate should also match the unit of val (g/t with CNY/g, % with CNY/t).",
        "Why does the result change so much with from/to?",
        "from/to are multipliers of the 10³ order (1 / 0.001 / 1000), so a wrong choice differs by a factor of a thousand to a million. They are meant to handle milli/kilo prefixes, but the tool performs no semantic validation. The safest approach is to convert only within the same unit (from=to=1); cross-unit conversion should be dimension-checked manually.",
        "Is this value the sales revenue?",
        "No. r is only a linear estimate of grade × unit price, without deducting beneficiation recovery, smelting processing fees, transport and taxes, and without accounting for metal price fluctuations. It is a rough theoretical metal value per tonne of ore; a real economic evaluation must combine metallurgical recovery with the full cost.",
        "About 'Ore Grade (g/t) and Value Conversion'",
        "Ore Grade (g/t) and Value Conversion. A mining and metallurgy tool that helps compute mineral parameters and indicators.",
    ]))

    write('mineral-density', build('mineral-density', [
        "⛏️ Ore Density / Porosity",
        "True density, bulk density, loose density, porosity",
        "Core formulas (by input variable): |(bulkDensity - ref.bd)| ÷ ref.bd × 100; (1 - Vs ÷ V) × 100; bulkDensity × 0.6",
        "/ Ore Density",
        "Ore type",
        "Ore mass (kg or t)",
        "Container volume (L or m³)",
        "True solid volume (L or m³)",
        "⛏️ Calculate density",
        "👆 Enter the measurement data",
        "📚 Deep Dive: Ore Density / Porosity",
        "Laboratory measurement: enter the mass, total volume and solid volume to obtain the bulk density (approximating the loose density), the true density and the porosity, and compare with reference minerals to judge the lithology.",
        "Beneficiation judgement: excessive porosity indicates a loose, slaking or water-bearing material, which affects crushing, grinding and separation.",
        "Anomaly detection: a large deviation between the measured density and the reference value suggests the sample may be mixed or contain voids/secondary minerals.",
        "Formula scope",
        "Bulk density (approximating loose density) = mass/total volume; true density = mass/solid volume; porosity = (1−solid volume/total volume)×100%; void ratio = (total volume−solid volume)/solid volume; loose density ≈ bulk density×0.6 (loose empirical value); deviation = difference between measured and reference value / reference value.",
        "Worked example (iron ore reference)",
        "Mass 1000 kg, total volume 500 L, solid volume 350 L (iron ore reference: true density 5.1, bulk density 3.2, loose density 2.4 t/m³). Bulk density 2.00 t/m³, true density 2.857 t/m³, porosity 30.0%, void ratio 0.429, loose density 1.20 t/m³; deviation from reference: true density 44.0%, bulk density 37.5%, judged 'high porosity'. [SRC]",
        "Boundary: missing solid volume",
        "When the solid volume is not filled in, only the bulk density is computed, not the true density/porosity. A porosity of 30.0% sits exactly on the '>30 high porosity' boundary (the code uses a strict >30), so this 30.0 case does not trigger high porosity and counts as normal; a measured 30.1% would be judged high porosity, so leave some margin when entering data.",
        "Is a large gap between bulk density and true density normal?",
        "Yes. Bulk density includes pores (using the total volume), while true density counts only the solid skeleton (using the solid volume); the difference is exactly the pore contribution. Porous rocks (e.g. sandstone with 5–25% porosity) show a clear gap; dense metallic ores (e.g. magnetite) can reach a true density around 5, while the bulk density is slightly lower because of fissures. Only an excessive deviation suggests a sample problem.",
        "Why do loose density 1.20 and bulk density 2.00 differ?",
        "Loose density is for grains naturally piled up (including inter-grain voids), whereas bulk density is for the intact block (including closed pores). The tool uses bulk density×0.6 as a loose empirical estimate, for reference only; the real loose density should be measured (e.g. by the container method), especially since it affects bin and stockpile capacity design.",
        "About 'Ore Density / Porosity'",
        "Ore Density / Porosity. A mining and metallurgy tool that helps compute mineral parameters and indicators.",
    ]))

    write('index', build('index', [
        "⛏️ Mining and Metallurgy Tools",
        "Mining and Metallurgy",
        "Mining and Metallurgy Tools",
        "Excavation Volume",
        "The Excavation Volume Calculator estimates earthwork volume and transport/stockpile volume by pit, road cut or mine pit shape, supports multiple section types, and suits earthwork engineering and mining stripping volume estimation.",
        "Estimate per-hole charge, unit consumption and hole pattern parameters from the volume formula or the Langefors formula.",
        "Ore grade (g/t ↔ %) with metal content and ore value conversion, supporting precious and base metals",
        "Computes the required airflow by four separate methods from the number of simultaneous underground workers, diesel equipment power, the explosive charge per round and the gas outburst rate, then takes the maximum value multiplied by the leakage factor as the design ventilation quantity.",
        "The ore grade and value conversion tool converts a g/t grade into ore value at the metal price and performs unit conversion, suitable for beneficiation, trading and resource valuation.",
        "Mine Safety Inspection Assessment",
        "Select an assessment mode, quantify the risk level with a risk matrix (likelihood L × severity S), and check hazards item by item against the safety inspection checklist to classify hazard levels. Used for pre-work underground safety risk assessment and rectification closure.",
        "Estimates resources and reserves from ore body area, thickness and grade, supporting the block method and the volume method, used for preliminary mine assessment and reporting, with pure front-end calculation for preliminary reference.",
        "Enters truck capacity, operating parameters and shift schedule to compute the load, cycle time, per-shift output and the number of trucks required, optimising mine haulage organisation and dispatch efficiency.",
        "Compliance assessment of the mine safety regulation/inspection/training system, scoring from five dimensions against the Coal Mine Safety Regulations and determining the safety grade",
        "The mining cost, indicator and efficiency analysis tool computes the cost per tonne of ore and operating efficiency from financial and engineering models, suitable for mine operation analysis, investment estimation and cost reduction.",
        "Enter the area, average thickness, ore density and grade of each block, compute ore amount and metal content by the block method, and automatically total all blocks.",
        "The ore density and porosity tool derives porosity from true density, bulk density and loose density, supporting physical property characterisation of ore and determination of beneficiation process parameters.",
        "About 'Mining and Metallurgy Tools'",
        "This Mining and Metallurgy Tools collection includes 12 free online tools covering the common calculation, conversion and lookup needs of mining and metallurgy scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you can find ready-to-use practical tools here. All tools run purely in the front end, data is not uploaded to the server, and privacy and security are protected.",
        "The mining and metallurgy tools collected on this page include (some representative tools):",
        "These tools help you quickly complete common mining and metallurgy tasks without memorising complex formulas or converting manually; just input and you get the result.",
        "Do the Mining and Metallurgy Tools need a download or registration?",
        "No. All Mining and Metallurgy Tools on this page are pure front-end online tools. Open the page and use them directly, with no software to install, no account to register, and no data uploaded.",
        "Are the calculation results of the Mining and Metallurgy Tools accurate? Is the data secure?",
        "The tools compute locally in your browser from public mathematical formulas and common industry standards, so results are available instantly. All computation happens locally on your device, data is never uploaded to the server, and privacy is well protected.",
    ]))

    write('analysis-cost-3', build('analysis-cost-3', [
        "⚡ Mining Cost, Indicator and Efficiency Analysis",
        "Enter output/cost/grade/waste/metal price to compute the cost and efficiency per tonne of ore",
        "Enter the ore output, total mining cost, ore grade, waste volume and metal price to automatically compute the cost per tonne of ore, the strip ratio, metal output, unit metal cost, total output value, gross profit and gross margin, for monthly mine operation analysis and cost reduction.",
        "Ore output (tonnes)",
        "Total mining cost (CNY)",
        "Ore grade (%)",
        "Waste volume (tonnes)",
        "Metal price (CNY per tonne of metal)",
        "Start analysis",
        "📚 Deep Dive: Mining Cost, Indicator and Efficiency Analysis",
        "Mine operation accounting: enter the ore output, total mining cost,",
        "ore grade",
        ", waste volume and metal price to compute the cost per tonne of ore, the strip ratio, the unit metal cost, the gross profit and the",
        ", used for monthly operation analysis.",
        "Cost reduction and ore blending optimisation: compare the cost per tonne of ore and the strip ratio across different mining areas or crews to locate high-cost links; evaluate the economics of blending schemes together with grade and metal price.",
        "Example monthly data of a mine",
        "Output 10000 t, total cost 5000000 CNY, grade 2.5%, waste 30000 t, metal price 60000 CNY per tonne of metal. Cost per tonne of ore = 500.00 CNY/t, strip ratio = 3.00, metal output = 250 t, unit metal cost = 20000.00 CNY/t, total output value = 15000000 CNY, gross profit = 10000000 CNY, gross margin = 66.67%.",
        "What is the strip ratio?",
        "Strip ratio = waste volume ÷ ore volume, indicating how many tonnes of waste must be stripped to mine 1 tonne of ore; it is the core economic indicator of an open pit, and a higher strip ratio means greater mining cost and energy consumption.",
        "Why is the unit metal cost higher than the cost per tonne of ore?",
        "The cost per tonne of ore only spreads the mining expense, while the unit metal cost = total cost ÷ (output × grade) is the full cost each tonne of metal should carry, which is closer to the economic evaluation convention on the smelting side.",
        "About 'Mining (Cost/Indicator/Efficiency) Analysis'",
        "Mining (Cost/Indicator/Efficiency) Analysis. A mining and metallurgy tool that helps compute mineral parameters and indicators.",
    ]))


if __name__ == '__main__':
    main()

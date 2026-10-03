#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'chemical')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'chemical')
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
    out = {'slug': slug, 'industry': 'chemical', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('miaomu-guige-zhiliang-yanshou-biaozhun', build('miaomu-guige-zhiliang-yanshou-biaozhun', [
        "Nursery Stock (Specification/Quality/Acceptance) Standards",
        "Enter two parameters to automatically compute the common results",
        "View the Nursery Stock (Specification/Quality/Acceptance) Standards User Guide",
        "Pass rate = passing plants / total; overall score = (pass rate + specification compliance rate) / 2",
        "Total plants sampled (plants)",
        "Passing plants (plants)",
        "Plants meeting the specification (plants)",
        "Nursery stock acceptance is graded comprehensively by the pass rate and the specification compliance rate.",
        "In-Depth Analysis: Nursery Stock (Specification/Quality/Acceptance) Standards",
        "Specification check: grade the stock by root collar diameter/DBH and seedling height, and match the design requirements.",
        "Out-of-nursery quality judgement: check root system integrity, absence of pests and disease, and mechanical damage, then give a release conclusion.",
        "Landscaping project acceptance: check the specification plant by plant against the design list, locate the non-compliant plants and tally the rework quantity.",
        "Tree acceptance grading walkthrough",
        "Entering DBH 8cm, height 350cm and crown spread 200cm, the tool grades it as a class II tree against the street tree standard, and notes that the DBH passes but the crown spread is slightly small and needs a remark.",
        "How are DBH and root collar diameter measured?",
        "DBH is the trunk diameter at 1.3m above the ground; root collar diameter is measured at the junction of root and stem. Bare-root seedlings are usually measured at the root collar, large balled-and-bagged trees at the DBH; the design governs.",
        "What is the grading based on?",
        "Based on the local nursery stock quality grading standard or the design specification; this tool demonstrates the common ranges, and formal acceptance is governed by the contract and the standard text.",
        "What if the acceptance check fails?",
        "Record the numbers and reasons of the non-compliant plants, require replanting or replacement, and re-check the batch inspection report of the incoming stock.",
        "About Nursery Stock (Specification/Quality/Acceptance) Standards",
        "Nursery Stock (Specification/Quality/Acceptance) Standards tool: checks the specification grade by root collar diameter, DBH, height and crown spread, supporting out-of-nursery inspection and landscaping project acceptance. Pure front-end processing, data is computed locally to protect privacy.",
        "One-click spec/parameter conversion: get the result in real time from the formula",
        "Local computation: data never leaves the browser, protecting business data",
        "Results can be copied and exported for easy record keeping and review",
        "Supports switching between common units: reduces manual conversion errors",
        "Specification grade check: match the design requirements",
        "Out-of-nursery quality judgement: root system and pests/disease",
        "Landscaping project acceptance: check the specification plant by plant",
        "Tallying the rework for non-compliant plants",
        "Total plants sampled (plants)",
        "Passing plants (plants)",
        "Plants meeting the specification (plants)",
    ]))

    write('solution-concentration', build('solution-concentration', [
        "Solution Concentration Conversion",
        "Molar concentration / mass fraction / ppm / dilution",
        "Core formula (by input variable): mg / (kg x 1000) x 1e6; (s / t) x 100; (s / t) x 1e6",
        "Solution Concentration Calculation",
        "/ Solution Concentration",
        "View the Solution Concentration Conversion User Guide",
        "In-Depth Analysis: Solution Concentration Conversion",
        "Mass fraction",
        "↔ amount concentration: given the density and",
        "molecular weight",
        ", convert between w% and mol/L.",
        "ppm and mg/L conversion: for dilute aqueous solutions approximately 1ppm≈1mg/L, supporting environmental and water quality limit judgements.",
        "Dilution preparation calculation: derive the water to add and the final volume from the stock concentration and the target concentration.",
        "10% NaCl amount concentration walkthrough",
        "Entering w%=10, density 1.07 g/mL and M=58.44, the tool outputs about 1.83 mol/L and gives a reference for the water to add when diluting to 0.1 mol/L.",
        "Is ppm the same as mg/L?",
        "Approximately true for dilute aqueous solutions; not true for gases or concentrated non-aqueous systems, the medium",
        " must be taken into account to avoid misuse.",
        "How to choose between mass fraction and amount concentration?",
        "Preparation and reaction stoichiometry mostly use mol/L; formulations and dosing commonly use w%; bridging across systems requires the density and molecular weight.",
        "What to watch out for when diluting?",
        "Make up to the target volume rather than simply adding water to that volume; when diluting concentrated acid always add acid into water and cool it, to prevent splashing.",
        "About Solution Concentration Calculation",
        "Solution concentration conversion tool: inter-converts mass fraction, amount concentration and ppm/mg·L, and supports dilution preparation, assisting laboratory analysis and dosing. Pure front-end processing, data is computed locally to protect privacy.",
        "One-click spec/parameter conversion: get the result in real time from the formula",
        "Local computation: data never leaves the browser, protecting business data",
        "Results can be copied and exported for easy record keeping and review",
        "Supports switching between common units: reduces manual conversion errors",
        "Mass fraction and amount concentration",
        "ppm and mg/L conversion",
        "Calculating the water to add for dilution preparation",
        "Safety notes for diluting concentrated acid",
    ]))

    write('convert-density-crude', build('convert-density-crude', [
        "Crude Oil API Gravity and Density Conversion",
        "Online crude oil API gravity and density conversion tool",
        "View the Crude Oil API Gravity and Density Conversion User Guide",
        "Crude oil API gravity",
        "Milli crude oil API gravity",
        "Kilo crude oil API gravity",
        "Milli density conversion",
        "Kilo density conversion",
        "In-Depth Analysis: Crude Oil API Gravity and Density Conversion",
        "API gravity and density cross-calculation: back-calculate the API gravity from the laboratory density, or look up the matching density from the API gravity, unifying the measurement basis.",
        "Light/heavy oil classification: by API gravity, light (>31.1), medium and heavy (<22.3), which affects pricing and the processing route.",
        "Trade measurement density correction: correct densities measured at different temperatures to the standard temperature, reducing delivery quantity disputes.",
        "Density corresponding to API 32 walkthrough",
        "Entering an API gravity of 32, the tool outputs a 15℃ density of about 0.865 g/cm³, classifies it as light crude oil, and notes that the light-end yield in refining is relatively high.",
        "Does a higher API gravity mean a lighter oil?",
        "Yes.",
        "API gravity and density",
        "are inversely proportional: the larger the value the smaller the density and the lighter the oil; light crude is usually easier to produce and gives a higher light-end yield.",
        "Why is the 15℃ standard density used?",
        "To remove the effect of temperature on volume, trade and inventory settle on the density/volume at the standard temperature, avoiding temperature disputes.",
        "Is density related to pricing?",
        "Yes. Light, low-sulfur crude usually commands a premium; density is one of the key parameters for classification and pricing and must be used together with sulfur content and others.",
        "About Crude Oil API Gravity and Density Conversion",
        "Crude oil API gravity and density conversion tool: cross-converts with the standard formula and classifies light/heavy oil, assisting trade measurement and refining feed blending. Pure front-end processing, data is computed locally to protect privacy.",
        "One-click spec/parameter conversion: get the result in real time from the formula",
        "Local computation: data never leaves the browser, protecting business data",
        "Results can be copied and exported for easy record keeping and review",
        "Supports switching between common units: reduces manual conversion errors",
        "API gravity and density cross-calculation",
        "Light/heavy oil classification",
        "Trade measurement density temperature correction",
        "Pricing and processing route reference",
    ]))

    write('convert-capacity-tank', build('convert-capacity-tank', [
        "Tank Capacity and Level Height Conversion",
        "Online tank capacity and level height conversion tool",
        "View the Tank Capacity and Level Height Conversion User Guide",
        "Tank capacity",
        "Milli tank capacity",
        "Kilo tank capacity",
        "Level height conversion",
        "Milli level height conversion",
        "Kilo level height conversion",
        "In-Depth Analysis: Tank Capacity and Level Height Conversion",
        "Level to volume stocktaking: measure the current level height and compute the existing inventory volume from the tank type and diameter, for stock reconciliation.",
        "Receipt and issue operation verification: convert the planned receipt or issue volume into a target level, guiding truck loading and tank transfer.",
        "Safe level red line calculation: set the maximum level from the filling factor and tank height to prevent overfilling and overflow.",
        "Vertical tank level and volume walkthrough",
        "Entering tank diameter 10m, level 4m and a vertical cylindrical tank, the tool outputs a current inventory of about 314m³, and gives a filling rate of about 31% for a full tank of 1000m³.",
        "How is a horizontal tank calculated?",
        "A horizontal tank requires segmented integration of the heads and shell or a volume table lookup, converted non-linearly by level height; this tool supports the corresponding geometric formula or table-style input.",
        "Why limit the filling factor?",
        "To prevent expansion from temperature change, breathing valve failure or overflow, 5%–10% vapour space is normally left; the exact value follows the medium characteristics and the applicable code.",
        "Where does the level conversion error come from?",
        "It mainly comes from tank out-of-roundness, foundation settlement and measurement datum deviation; large tanks are best corrected with a calibrated volume table.",
        "About Tank Capacity and Level Height Conversion",
        "Tank capacity and level conversion tool: back-computes the volume from the level height for the given tank type or vice versa, assisting stocktaking and safe level management. Pure front-end processing, data is computed locally to protect privacy.",
        "One-click spec/parameter conversion: get the result in real time from the formula",
        "Local computation: data never leaves the browser, protecting business data",
        "Results can be copied and exported for easy record keeping and review",
        "Supports switching between common units: reduces manual conversion errors",
        "Level to volume stocktaking: stock reconciliation",
        "Target level calculation for receipt and issue operations",
        "Setting the safe level red line",
        "Fits horizontal and vertical tank types",
    ]))


if __name__ == '__main__':
    main()

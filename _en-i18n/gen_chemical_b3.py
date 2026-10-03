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
    write('analysis-cost-7', build('analysis-cost-7', [
        "Budget Item Summary Analysis",
        "Budget item summary",
        "Budget Item Summary Analysis",
        "/ Budget Item Summary Analysis",
        "View the Budget Item Summary Analysis User Guide",
        "Total = sum of each item amount; item share = amount / total x 100%; cumulative share of the top N items = sum of the top N amounts / total x 100%; deviation = (total - reference budget) / reference budget x 100%.",
        "In budget preparation and cost control, first sum the items to get the total investment or annual operating cost, then use the share structure to identify the main cost drivers (the top N items), and compare against the reference budget to judge overspend or saving. Results change with the accounting basis and price assumptions; the official budget follows the internal accounting system.",
        "Amount of each budget item (yuan, separated by commas or line breaks)",
        "Total reference budget (yuan)",
        "Focus on the top N items",
        "Compute the summary",
        "In-Depth Analysis: Budget Item Summary Analysis",
        "Project budget preparation: sum items such as equipment, installation, raw materials and energy to obtain the total investment and annual operating cost, supporting project approval and vendor selection.",
        "Cost structure analysis: use the item shares and the cumulative share of the top N items to identify the main cost drivers and focus cost reduction efforts.",
        "Deviation monitoring: quantify overspend or saving and the deviation rate against the reference budget, supporting budget execution tracking.",
        "Worked example (6 items, reference budget 2500)",
        "Item amounts (yuan): 800, 200, 1200, 300, 500, 150. Total 3150.00; largest item 1200.00, smallest 150.00; highest item share 38.10% (1200); cumulative share of the top 3 items (1200, 800, 500) 79.37%; against the reference budget of 2500 the overspend is 650.00 (deviation 26.00%).",
        "What is the cumulative share of the top N items for?",
        "It quickly points out the few items that contribute the most. For example, when the cumulative share of the top 3 items approaches 80%, cost reduction should focus on these core items rather than spreading effort evenly.",
        "How should the sign of the deviation rate be read?",
        "When the total exceeds the reference budget it shows overspend and a positive deviation rate; when it is lower it shows saving and a negative deviation rate; the larger the absolute deviation rate, the further budget execution has drifted, and the accounting basis and price assumptions must be checked.",
        "About Budget Item Summary Analysis",
        "Budget item summary analysis tool for chemical enterprises: performs cost estimation and deviation analysis by plant investment, production cost and process scheme, supporting budget preparation and cost reduction decisions. Pure front-end processing, data is computed locally to protect privacy.",
        "One-click spec/parameter conversion: get the result in real time from the formula",
        "Local computation: data never leaves the browser, protecting business data",
        "Results can be copied and exported for easy record keeping and review",
        "Supports switching between common units: reduces manual conversion errors",
        "Plant investment budget preparation: sum the item estimates into a total investment",
        "Production cost control and deviation analysis: locate the overspending stage",
        "Process optimisation scheme cost comparison: screen out the better route",
        "Budget and project approval report supporting evidence: quick estimates support vendor selection",
        "For example: 800,200,1200,300",
    ]))

    write('checker-15', build('checker-15', [
        "Chemical Industry Quality Management System Self-Check",
        "Self-check item by item across the three modules of standard management, process inspection and rectification closure, automatically computing the attainment rate of each module and the system compliance degree, locating weak links and outputting a rectification list.",
        "Quality (Standard/Inspection/Rectification) System",
        "/ Quality (Standard/Inspection/Rectification) System",
        "View the Chemical Industry Quality Management System Self-Check User Guide",
        "System compliance degree = actual score of each item / full score x 100%. 90% and above is excellent, 75-89% is good, 60-74% is pass,",
        "Assess the system compliance degree",
        "System compliance degree = actual score of each item / full score x 100%",
        "90% and above is excellent, 75-89% is good, 60-74% is pass, below 60% is fail",
        "This tool is designed with reference to ISO 9001 and the quality management system requirements of the chemical industry; it does not replace external audit",
        "In-Depth Analysis: Chemical Industry Quality Management System Self-Check",
        "ISO 9001 internal audit preparation: self-check item by item against the standard clauses, generate a list of nonconformities and rectification suggestions, and shorten the external audit preparation cycle.",
        "Production licence review inspection: check process control records against the production licence and industry specifications, and locate evidence gaps.",
        "Annual system compliance self-assessment: quantify the attainment rate of each module and the overall compliance degree, and track the results of annual improvement.",
        "Walkthrough of a 16-point checklist self-check",
        "Entering the self-check results of each module, the tool outputs the attainment rates for standard management, process inspection and rectification closure plus the overall compliance degree, and lists the items that failed as a rectification list.",
        "Can the self-check results be used directly for the external audit?",
        "They can serve as the basis for internal audit and inspection preparation; formal certification is still carried out by a qualified certification body, and objective evidence and records must be retained.",
        "How to improve when the attainment rate is low?",
        "First locate the module that failed (standard/inspection/rectification), supplement documents, training and process records for the weak items, then verify closure.",
        "How does this map to the ISO 9001 clauses?",
        "The 16 points can be mapped to standard clauses (such as document control, process confirmation and nonconforming product control), making the self-check results traceable to the system requirements.",
        "About Chemical Industry Quality Management System Self-Check",
        "Quality management system self-check tool for chemical enterprises, covering 16 points across the three modules of standard management, process inspection and rectification closure, quantitatively assessing system compliance and locating weak links.",
        "Checklist self-check across the three modules of standard, inspection and rectification",
        "ISO 9001 internal audit preparation for chemical enterprises",
        "Annual self-check of the quality management system",
        "Preparation for the production licence review inspection",
        "Formulating the quality management improvement plan",
    ]))

    write('mixture-ratio', build('mixture-ratio', [
        "Mixing Ratio Calculation",
        "Dilution / mixing / percentage / alcohol by volume",
        "Core formula (by input variable): dec x 1000; dec x 100",
        "Mixing Ratio",
        "/ Mixing Ratio",
        "View the Mixing Ratio Calculation User Guide",
        "In-Depth Analysis: Mixing Ratio Calculation",
        "Multi-component mass ratio conversion: given the total charge and the ratio (e.g. A:B:C=3:1:1), compute the gram weight of each component.",
        "Solution preparation volume ratio: dilute or blend by volume ratio, estimating the amount of liquid to add and the final volume.",
        "Reaction charge ratio check: convert the actual charge by the stoichiometric ratio to control excess and side reactions.",
        "Walkthrough of a charge at A:B:C=3:1:1",
        "Entering a total charge of 500g and a ratio of 3:1:1, the tool outputs A 300g, B 100g, C 100g, and notes that charging by the stoichiometric ratio can avoid excess of a component.",
        "How to choose between mass ratio and molar ratio?",
        "Formulas commonly use the mass ratio for easy weighing; chemical reactions are more rigorous with the molar ratio. Cross-system conversion goes through",
        "molecular weight",
        ", to avoid applying one directly.",
        "How is preparation error controlled?",
        "For lab trials, weigh or measure with 0.1g/0.1mL precision, mix uniformly before sampling; for error-sensitive formulas, replicate samples are recommended for verification.",
        "Does the volume change when mixing by volume ratio?",
        "Some liquids show volume contraction or expansion on mixing (non-ideal mixing); take the final volume from measurement, and use the mass method for important formulas.",
        "About Mixing Ratio",
        "Mixing ratio calculation tool: converts the charge of each component by ratio, supports multi-component ingredients and solution preparation, and assists formula reproduction and lab trials. Pure front-end processing, data is computed locally to protect privacy.",
        "One-click spec/parameter conversion: get the result in real time from the formula",
        "Local computation: data never leaves the browser, protecting business data",
        "Results can be copied and exported for easy record keeping and review",
        "Supports switching between common units: reduces manual conversion errors",
        "Multi-component mass ratio conversion",
        "Solution preparation volume ratio",
        "Reaction charge ratio check",
        "Lab trial formula scaling",
    ]))

    write('reaction-yield', build('reaction-yield', [
        "Reaction Yield Calculation",
        "Theoretical yield / actual yield / limiting reactant / yield",
        "Core formula (by input variable): (act / theo) x 100; scale x (y1 - y2) / 100; scale x y2 / 100",
        "Reaction Yield",
        "/ Reaction Yield",
        "View the Reaction Yield Calculation User Guide",
        "In-Depth Analysis: Reaction Yield Calculation",
        "Theoretical yield calculation: derive the theoretical yield from the moles of the limiting reactant and the stoichiometric ratio.",
        "Actual yield check: actual yield / theoretical yield x 100%, quantifying the yield level.",
        "Low yield troubleshooting: compare the yield of each step to locate the loss (side reaction, separation, work-up).",
        "Walkthrough of a synthesis reaction yield",
        "Entering a limiting reactant of 1.0 mol, a stoichiometric product of 1.0 mol and an actual product of 0.72 mol, the tool outputs the mass corresponding to the theoretical yield and an actual yield of 72%, and notes that the loss may be in the separation step.",
        "How is the theoretical yield determined?",
        "It is set by the limiting reactant in the balanced equation; first find the reactant with the smallest mole ratio, then compute the product upper limit by the coefficient ratio.",
        "Is a low yield always a reaction problem?",
        "Not necessarily. Separation, extraction, drying and transfer losses also lower it; locate the loss step by step rather than looking only at the total yield.",
        "How is the total yield of a multi-step reaction computed?",
        "Multiply the yield of each step (e.g. three steps 90% x 85% x 80% is about 61%); improving any one step has a strong effect on the total yield.",
        "About Reaction Yield",
        "Reaction yield calculation tool: checks the yield from the theoretical and actual yields and supports multi-step total yield analysis, assisting process optimisation. Pure front-end processing, data is computed locally to protect privacy.",
        "One-click spec/parameter conversion: get the result in real time from the formula",
        "Local computation: data never leaves the browser, protecting business data",
        "Results can be copied and exported for easy record keeping and review",
        "Supports switching between common units: reduces manual conversion errors",
        "Theoretical yield calculation",
        "Actual yield check",
        "Troubleshooting low yield steps",
        "Total yield of a multi-step reaction",
    ]))

    write('index', build('index', [
        "Chemical Materials Tools",
        "Chemical Materials",
        "Chemical Materials Tools",
        "Enter the pipe diameter, length, flow velocity and friction factor, and compute the pressure drop along the pipe with the Darcy-Weisbach formula, for chemical piping design and pump selection.",
        "Enter a chemical formula (parentheses and water of crystallisation supported), automatically parse the atom count of each element and compute the molar mass (g/mol), for stoichiometry and formula calculation.",
        "Solution Concentration Calculation",
        "Convert between solution concentration units such as molar concentration, mass fraction, volume fraction and ppm, and supports dilution calculation, for laboratory work and process formulas.",
        "Convert between crude oil API gravity and density (kg/m3 or g/cm3), to unify the basis for crude oil trade metering and refinery formula calculation.",
        "Enter the tank dimensions and level height, compute the corresponding volume or back-compute the level, supporting both horizontal and vertical tanks, for stocktaking and loading quantity accounting.",
        "Enter specification data such as root collar diameter, height and crown spread of nursery stock, judge the grade against the quality grading standard and give a pass or fail acceptance conclusion, for nursery stock procurement and landscaping acceptance.",
        "Mixing Ratio",
        "Enter the concentrations and volumes of two solutions, compute the concentration after mixing, the water to add for dilution or the alcohol by volume, supporting reverse ratio calculation, for blending and lab preparation.",
        "Reaction Yield",
        "Enter the actual and theoretical yields of the reactants, compute the reaction yield and identify the limiting reactant, for chemical synthesis and lab yield assessment.",
        "Quality (Standard/Inspection/Rectification) System",
        "Self-check item by item across the three modules of standard management, process inspection and rectification closure, automatically computing the attainment rate of each module and the system compliance degree, locating weak links and outputting a rectification list.",
        "Quality (Purity/Standard/Testing) Assurance",
        "Supports acid-base titration and gravimetric methods to compute chemical purity; enter the experimental data to get the purity percentage automatically and judge pass or fail against the standard threshold.",
        "Budget Item Summary Analysis",
        "About Chemical Materials Tools",
        "The Chemical Materials Tools collection holds 11 free online tools covering the common calculation, conversion and lookup needs of chemical material scenarios. Whether you are a practitioner, a student or an ordinary user, you can find practical ready-to-use tools here. All tools run entirely in the front end, data is not uploaded to the server, and privacy is protected.",
        "The chemical materials tools collected on this page include (some representative tools):",
        "These tools help you quickly complete common chemical material related tasks, with no need to memorise complex formulas or convert manually; enter and you get the result.",
        "Do the Chemical Materials Tools need a download or registration?",
        "No. All chemical materials tools on this page are pure front-end online tools; just open the page and use them directly, with no software to install, no account to register, and no data uploaded.",
        "Are the Chemical Materials Tools results accurate? Is the data secure?",
        "The tools compute locally in your browser from public mathematical formulas and general industry standards, and results are available instantly. All computation is done locally on your device, data is never uploaded to the server, and privacy is protected.",
    ]))


if __name__ == '__main__':
    main()

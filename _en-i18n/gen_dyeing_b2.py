#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'dyeing')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'dyeing')
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
    out = {'slug': slug, 'industry': 'dyeing', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('color-diff', build('color-diff', [
        "🎨 Pad Dyeing Colour Difference Control",
        "Enter the pickup and the before/after colour difference ΔE to assess the pad dyeing process and colour difference pass rate",
        "Entering the pickup and the before/after colour difference ΔE to assess the pad dyeing process and colour difference pass rate is computed professionally from the input parameters and the results are output.",
        "📖 Read the \"Pad Dyeing Colour Difference Control Usage Guide\"",
        "Pickup (%)",
        "Cotton fabric",
        "Polyester fabric",
        "Viscose fibre",
        "💡 Pickup = (wet weight after padding − dry weight before padding)/dry weight before padding×100%; the smaller the colour difference ΔE the better, generally required ≤3",
        "Cotton fabric pickup should be 60%～75%; too high easily causes migration blotching",
        "Colour difference ΔE refers to the CIE Lab colour difference formula; customer standards may be stricter",
        "📚 In-Depth Analysis: Pad Dyeing Colour Difference Control",
        "Continuous pad dyeing process control: use the pickup to judge whether the liquor loading is right — too high causes migration, too low gives a pale shade.",
        "Online dyeing quality inspection: compare the front/back and left/right colour difference ΔE in real time and warn on out-of-tolerance.",
        "Colour difference complaint analysis: locate whether left/right or front/back differences come from pad pressure, pre-drying or the dye itself.",
        "Example colour difference check for polyester-cotton pad dyeing",
        "For a polyester-cotton blend with a reference pickup of 60%~70%, the measured 82% is high and indicates excess liquor loading with migration risk; the left/centre/right ΔEcmc are 0.6/0.4/1.3, and the right side exceeds the customer tolerance of 1.0, so it is judged fail and the pad pressure needs adjusting.",
        "What is pickup?",
        "The percentage of wet fabric weight relative to dry fabric weight after pad dyeing, which determines the actual liquor loading and directly affects shade depth and levelness — a key process parameter in pad dyeing.",
        "Where does the left/right colour difference come from?",
        "It usually comes from uneven left/right pad pressure, pre-drying temperature gradients or fabric tracking offset, making liquor loading or drying inconsistent across the width, which shows up as left/centre/right colour difference.",
        "What colour difference counts as pass?",
        "It depends on the customer contract; commonly ΔEcmc≤1.0~2.0. This tool grades by the reference range, and the sealed sample plus actual measurement take precedence.",
        "About \"Pad Dyeing Colour Difference Control\"",
        "Pad dyeing is an important continuous dyeing process, where the pickup determines liquor loading and the colour difference ΔE reflects front/back colour consistency. This tool assesses the reasonableness of the pickup and the pass rate of the colour difference by fabric type, helping judge quickly whether the pad dyeing process meets the standard.",
        "Gives a reference pickup range by fabric type",
        "Grades the colour difference ΔE (excellent / good / acceptable / fail)",
        "Overall pass/fail judgement",
        "Continuous pad dyeing process control",
        "Online dyeing quality inspection",
        "Colour difference complaint analysis",
        "Dyeing and printing process parameter optimisation",
        "Pickup",
        "Colour difference",
    ]))

    write('colorfast-1', build('colorfast-1', [
        "🧵 Colour Fastness Combination Assessment",
        "Enter washing, rubbing (dry rub) and light fastness grades to assess colour fastness comprehensively (grade 1～5, grade 5 is best)",
        "Core formula (by input variables): wash×0.3+rub×0.3+light×0.4; min(wash,rub,light)",
        "📖 Read the \"Colour Fastness Combination Assessment Usage Guide\"",
        "Wash fastness (grade)",
        "Rubbing fastness (grade)",
        "Light fastness (grade)",
        "💡 Composite score = wash×0.3 + rub×0.3 + light×0.4; at the same time the lowest item is used as the weak-link judgement",
        "Colour fastness grades run 1～5, and half grades (such as 3.5) are allowed",
        "The 8-level light fastness scale can be converted to the 5-level scale by ×5/8",
        "📚 In-Depth Analysis: Colour Fastness Combination Assessment",
        "Quality inspection of dyed finished goods: after grading the three items, take the lowest as the basis for overall pass, preventing a single strong item masking a weak one.",
        "Comparison of dye and process selection: compare the combination of three fastness items under different dyes and fixation processes to pick the best.",
        "Customer standard conformity judgement: check item by item against the buyer's stated grades (such as wash grade 4, rub grade 3-4).",
        "Example three-item fastness assessment for reactive dyed fabric",
        "Wash grade 4, dry rub grade 4-5, wet rub grade 3, light grade 5 give a weighted composite of about grade 4, but the weak link wet rub grade 3 is below the customer requirement of grade 3-4, so it is judged fail and fixation or the process must be adjusted.",
        "Which governs — the composite score or the weak link?",
        "For colour fastness it is safer to take the lowest weak-link item as the basis, so that one very poor item is not masked by averaging; this tool gives both the weighted composite and the weak link, and pass/fail takes the weak link.",
        "How do I enter half grades (such as 3.5)?",
        "Half grades are allowed when rating, and the tool supports half-grade input and includes it in the grading, consistent with GB/T series rating practice.",
        "How are the three weights set?",
        "Garment applications focus on wash and rub, outdoor applications on light; weights can be set by use, and the default recommendation is to prioritise the weak link with the composite as reference.",
        "About \"Colour Fastness Combination Assessment\"",
        "Colour fastness is an important indicator of dyed fabric quality. This tool performs a weighted composite assessment of wash, rubbing and light fastness, and gives a final pass judgement together with the lowest weak-link item, helping judge quickly whether a product meets quality requirements.",
        "Weighted composite score of three fastness items",
        "Identifies and rates the lowest weak-link item",
        "Supports half-grade input (e.g. 3.5)",
        "Quality inspection of dyed finished goods",
        "Comparison of dye and process selection",
        "Customer standard conformity judgement",
        "Teaching and experimental analysis for dyeing and printing",
        "Wash fastness",
        "Rubbing fastness",
        "Light fastness",
    ]))

    write('ratio-21', build('ratio-21', [
        "🎨 Pigment Binder Ratio",
        "Enter the print paste concentration, binder ratio and total formula weight to compute the amount of each component in a pigment printing paste",
        "Core formula (by input variables): total×thickener÷100; total×pigment÷100; total×binder÷100",
        "📖 Read the \"Pigment Binder Ratio Usage Guide\"",
        "Print paste (pigment) concentration (%)",
        "Binder ratio (%)",
        "Crosslinker ratio (%)",
        "Total formula weight (g)",
        "💡 Formula = pigment + binder + crosslinker + thickener + water (topped up to 100%)",
        "Pigment concentration is generally 0.5%～8%, binder 15%～25%",
        "Thickener and water top up to 100% of the total formula weight",
        "📚 In-Depth Analysis: Pigment Binder Ratio",
        "Pigment printing paste preparation: get the mass of each component in one step from the pigment content and the binder and crosslinker ratios, with water and thickener topping up to the total.",
        "Print sample formula adjustment: changing the pigment concentration or binder ratio recalculates immediately, enabling fast small samples.",
        "Binder dosage optimisation: balance hand feel and fastness, avoiding too much binder making the fabric stiff or too little causing flaking.",
        "Example pigment printing paste for cotton",
        "For a total formula weight of 1000 g with pigment 10%, binder 30%, crosslinker 3% and thickener 4%, the pigment is 100 g, binder 300 g, crosslinker 30 g and thickener 40 g, with water topping up 530 g; the check totals 100% without exceeding.",
        "What does the binder do?",
        "The pigment itself does not bond to the fibre; the binder forms a film that fixes the pigment on the fabric surface, and its dosage and type determine the fastness and hand feel.",
        "Is a crosslinker necessary?",
        "Adding a crosslinker raises the crosslink density of the film to improve wash and rub fastness; but too much may make the hand feel stiff, so choose based on binder type and fastness requirement.",
        "What happens if the ratios exceed 100%?",
        "It means the component sum exceeds the total, so the water cannot make up the difference and the formula cannot actually be prepared; the tool flags the over-limit and you need to lower some component ratio.",
        "About \"Pigment Binder Ratio\"",
        "Pigment printing relies on the binder forming a film to fix the pigment on the fabric surface. This tool automatically computes the actual amount of each component in the printing paste formula from the print paste concentration and the binder and crosslinker ratios, topping up with water and thickener to the total formula weight.",
        "One-step calculation of pigment, binder, crosslinker, thickener and water",
        "Automatic check of whether ratios exceed 100%",
        "Supports custom total formula weight",
        "Pigment printing paste preparation",
        "Print sample formula adjustment",
        "Binder dosage optimisation",
        "Print paste concentration",
        "Binder ratio",
        "Crosslinker ratio",
        "Total formula weight",
    ]))

    write('ratio-9', build('ratio-9', [
        "🧵 Dyeing Liquor Ratio",
        "Enter the liquor ratio, fabric weight and dye concentration to compute the water volume, dye and auxiliary dosages",
        "Core formula (by input variables): dyeG÷1000; w×c×10",
        "📖 Read the \"Dyeing Liquor Ratio Usage Guide\"",
        "Fabric weight (kg)",
        "Glauber's salt dosage (g/L)",
        "💡 Liquor volume = fabric weight × liquor ratio; auxiliary dosage = liquor volume × auxiliary concentration (g/L)",
        "Glauber's salt (sodium sulphate) is a builder for reactive dyes, specified in g/L",
        "📚 In-Depth Analysis: Dyeing Liquor Ratio",
        "Bulk exhaust liquor preparation: get the liquor volume, dye and auxiliary dosages directly from the liquor ratio and fabric weight, reducing manual conversion.",
        "Reactive dye formula: compute the Glauber's salt (builder) dosage and liquor concentration together for easy checking.",
        "Small-ratio energy-saving process design: compare water volume and levelling difficulty at different liquor ratios, balancing energy saving against quality.",
        "Example reactive exhaust dyeing liquor preparation",
        "Fabric 500 g, liquor ratio 1:15, shade depth 2% o.w.f, Glauber's salt 50 g/L → liquor volume 7.5 L, dye 10 g, Glauber's salt 7.5×50=375 g, liquor concentration about 1.33 g/L.",
        "How is the liquor ratio written?",
        "Liquor ratio = weight (or volume) of dye liquor : dry fabric weight, so 1:10 means ten times the fabric weight in liquor; it is a core parameter of exhaust dyeing.",
        "What are the pros and cons of a small liquor ratio?",
        "It saves water and energy and raises dye utilisation, but with little liquor the levelling window is narrow and blotching appears easily, so controlled addition and suitable equipment are needed.",
        "What does Glauber's salt do?",
        "It acts as a builder in reactive exhaust dyeing, reducing the negative charge repulsion on the fibre surface and raising the exhaustion rate; the dosage is adjusted with the dye and liquor ratio.",
        "About \"Dyeing Liquor Ratio\"",
        "The liquor ratio is a key exhaust dyeing parameter that determines the liquor volume and auxiliary dosage. This tool computes total liquor volume, dye dosage, builder (Glauber's salt) dosage and liquor concentration in one step from the liquor ratio, fabric weight and dye concentration, making liquor preparation easy.",
        "Computes liquor volume, dye and auxiliary dosages together",
        "Outputs liquor concentration for checking",
        "Supports custom liquor ratios and concentrations",
        "Bulk exhaust liquor preparation calculation",
        "Reactive dye formula",
        "Small-ratio energy-saving process design",
        "Liquor ratio",
        "Fabric weight",
        "Dye concentration",
        "Glauber's salt dosage",
    ]))

    write('shuixixiaolvjisuan', build('shuixixiaolvjisuan', [
        "⚡ Wash Efficiency Calculator",
        "Enter soaping temperature, number of washes and water volume per wash to estimate wash efficiency and the residual rate left unwashed",
        "Core formula (by input variables): max(0,min(1,0.5+(temp-60)÷100×0.4)); max(0.1,min(0.9,tempFactor×ratioFactor)); max(0.3,min(0.95,0.5+ratio÷40×0.3))",
        "📖 Read the \"Wash Efficiency Calculator Usage Guide\"",
        "Soaping temperature (℃)",
        "Number of washes",
        "Water volume per wash (L)",
        "💡 The single-pass removal rate rises with temperature; total efficiency = 1 − (1−r)ⁿ",
        "Soaping temperature is generally 90～95℃; the higher the temperature the faster the dye dissolves and diffuses",
        "This model is an empirical estimate; in reality it is affected by the dye, auxiliaries and mechanical action",
        "📚 In-Depth Analysis: Wash Efficiency Calculator",
        "Soaping process parameter optimisation: estimate the single-pass loose dye removal rate from temperature and liquor ratio to set the number of washes.",
        "Design of wash count and water volume: compare total efficiency and water consumption at different wash counts, balancing quality against cost.",
        "Water- and energy-saving process assessment: raise the temperature or lengthen liquor exchange to improve the single-pass removal rate and reduce the total number of washes.",
        "Example soaping efficiency for reactive dyeing",
        "Single-pass removal rate about 65% (temperature 90℃, liquor ratio 1:10); after 3 washes total efficiency 1-(1-0.65)^3=95.7% and residual rate 4.3%; dropping to 2 washes leaves 12.3% residual, so choose according to the fastness requirement.",
        "How is the single-pass removal rate estimated?",
        "This tool uses an empirical model corrected by water temperature and liquor ratio to estimate the single-pass loose dye removal proportion as a process reference; in practice rely on measured residual liquor colour or fastness.",
        "Why is multiple washing not simple addition?",
        "Each wash removes a portion of the current residue and follows a dilutional decay, so the total residual rate accumulates as (1-r)^n rather than n×r.",
        "How can I save more water?",
        "Raising the water temperature, changing the water promptly and adding soap when necessary all raise the single-pass removal rate, which reduces the total number of washes and total water use.",
        "About \"Wash Efficiency Calculator\"",
        "Washing (soaping) is the key process for removing unfixed loose dye. Based on temperature and liquor ratio this tool estimates the single-pass removal rate, computes total wash efficiency and residual rate by the multi-stage dilution principle, and helps optimise wash count and water volume, balancing quality against water saving.",
        "Single-pass removal rate double-corrected by temperature and liquor ratio",
        "Total wash efficiency and residual rate across multiple washes",
        "Efficiency grading and progress bar visualisation",
        "Soaping process parameter optimisation",
        "Wash count and water volume design",
        "Water- and energy-saving process assessment",
        "Soaping temperature",
        "Number of washes",
        "Water volume per wash",
        "Fabric weight",
    ]))


if __name__ == '__main__':
    main()
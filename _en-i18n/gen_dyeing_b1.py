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
    write('assessor-color-diff', build('assessor-color-diff', [
        "📋 Colour Difference ΔE(CMC) Assessment",
        "Computes the colour difference between a standard sample and a batch sample with the CMC(l:c) formula, commonly used for pass/fail colour difference judgement in textile dyeing and printing. Default CMC(2:1), lightness tolerance l=2, chroma tolerance c=1.",
        "Simple Colour Difference ΔE(CMC) Assessment",
        "/ Simple Colour Difference ΔE(CMC) Assessment",
        "📖 Read the \"Colour Difference ΔE(CMC) Assessment Usage Guide\"",
        "CMC(l:c) colour difference: ΔE_CMC = √((ΔL ÷ (l·S_L))² + (ΔC ÷ (c·S_C))² + (ΔH ÷ S_H)²), where ΔL, ΔC, ΔH are the lightness, chroma and hue differences and S_L, S_C, S_H the corresponding weights (computed from the standard sample Lab values); common parameters l:c = 2:1 (more tolerant of lightness difference, for textile dyeing and printing) or 1:1 (stricter on chroma difference, for coatings); ΔE_CMC not exceeding the tolerance (commonly 1.0 or 1.5) is judged pass.",
        "Standard sample (reference)",
        "Batch sample (under test)",
        "Lightness tolerance l",
        "Chroma tolerance c",
        "Acceptable threshold ΔE",
        "Compute colour difference",
        "CMC(2:1) is the colour difference formula common in textile dyeing and printing; it is closer to human vision than ΔE*ab, and the acceptable threshold is usually taken as 1.0",
        "Enter CIE L*a*b* values (D65/10° measurement condition); increasing l makes it more tolerant of lightness differences",
        "The pass line for colour difference depends on the customer or product; this tool's threshold is customisable and the results are for reference in matching and quality inspection",
        "📚 In-Depth Analysis: Colour Difference ΔE(CMC) Assessment",
        "Pass/fail judgement of colour difference between bulk production and the standard sample: read whether a batch is acceptable against the customer's tolerance (commonly 1.0~2.0).",
        "Visual consistency comparison of multiple matching recipes: sample several formulations against the same standard and quantify the colour differences to pick the best.",
        "Attribute the shade shift after a dye recipe adjustment: use the ΔL/ΔC/ΔH components to judge whether it is too dark or too light, too bright or too dull, or off-hue.",
        "Reactive black exhaust dyeing batch colour difference review",
        "Standard and batch L*a*b* are (25.1,0.3,-0.2) and (26.4,0.1,-0.5) respectively; CMC(2:1) gives ΔEcmc=1.4, below the customer tolerance of 2.0 so it is judged acceptable; ΔL=+1.3 runs dark and ΔH is slightly blue, so the dye concentration and shade can be fine-tuned.",
        "How does CMC(l:c) differ from CIELAB ΔE*ab?",
        "ΔE*ab weights all directions equally, which is inconsistent with human vision; CMC(l:c) weights lightness, chroma and hue separately (commonly l=2, c=1), is closer to actual visual tolerance, and is the colour difference standard the textile industry recommends.",
        "What values of l and c are normally used?",
        "Textile dyeing and printing commonly uses CMC(2:1), that is lightness weight 2 and chroma weight 1; for dark colours or special requirements it can be adjusted, but it must be agreed with the customer in the contract.",
        "Can the result be used directly as the basis for delivery?",
        "It can serve as an internal reference for colour difference reading and for choosing among recipes; final delivery is governed by the customer's sealed sample, the contractual tolerance and laboratory measurement, and does not replace a formal test report.",
        "About \"Colour Difference ΔE(CMC) Assessment\"",
        "The CMC(l:c) colour difference formula was proposed by the Society of Dyers and Colourists (SDC) of the UK. It weights lightness, chroma and hue differences separately, is visually more consistent than ΔE*ab, and is the mainstream standard for colour difference judgement in the textile dyeing and printing industry.",
        "Full CMC(l:c) formula implementation",
        "Outputs the ΔL/ΔC/ΔH components and direction",
        "Customisable acceptable threshold reading",
        "Batch colour difference pass/fail judgement",
        "Matching sample acceptance",
        "Customer sample comparison",
        "Dye recipe adjustment reference",
    ]))

    write('bumianphtiaojie', build('bumianphtiaojie', [
        "🎨 Fabric pH Adjustment",
        "Enter the current pH, target pH and fabric weight to estimate the acid/alkali adjusting agent dosage",
        "Core formula (by input variables): |(delta)|",
        "📖 Read the \"Fabric pH Adjustment Usage Guide\"",
        "Current fabric pH",
        "Auto select",
        "Glacial acetic acid (lowers pH)",
        "Soda ash (raises pH)",
        "💡 Adjusting agent dosage ≈ fabric weight × |ΔpH| × coefficient; the glacial acetic acid coefficient is about 2g/(kg·pH) and soda ash about 3g/(kg·pH)",
        "Fabric pH should be neutral or weakly acidic (6.5～7.5); too high affects shade and handle",
        "This model is an empirical estimate; in practice it must be corrected by small-scale trials",
        "📚 In-Depth Analysis: Fabric pH Adjustment",
        "Neutralisation after dyeing: after soaping, reactive/direct dye fabrics tend to be alkaline, so estimate the glacial acetic acid dosage to bring them back to near neutral.",
        "pH adjustment before finishing: ensure the fabric pH falls in the safe range (usually 4.0~7.5 depending on the product) to avoid fibre damage or skin irritation.",
        "Troubleshooting abnormal fabric pH: when pH deviates, work backwards to check whether the pretreatment wash or acid neutralisation step was adequate.",
        "Example of neutralising reactive dyed fabric",
        "With fabric weight 200 g, current pH 9.5 and target pH 7.0, the tool estimates about 0.6% (on fabric weight) of diluted glacial acetic acid along the neutralisation curve; after adjustment, retesting pH in the 6.8~7.2 range means it is compliant.",
        "Why must fabric pH be controlled?",
        "Residual alkali after dyeing and finishing raises the fabric pH, which over time affects shade, handle and the performance of finishing auxiliaries, and close-to-skin textiles may irritate the skin, so it must be neutralised into the standard range.",
        "When is glacial acetic acid used and when soda ash?",
        "Use glacial acetic acid (or dilute acid) to bring down alkaline fabric; if over-acid-washing in pretreatment has left it acidic, use soda ash to bring it back up. The tool determines the direction automatically from the difference between current and target pH.",
        "Can the result be used directly for bulk production?",
        "It is a reference estimate for neutralising dosage; in practice follow the GB/T 7573 water-extraction pH measurement, and the specific auxiliary concentration and temperature must be combined with the on-site process.",
        "About \"Fabric pH Adjustment\"",
        "Alkali agents often remain on fabric after dyeing, and a high pH affects shade, handle and finishing performance. This tool estimates the dosage of glacial acetic acid or soda ash from the difference between current and target pH and the fabric weight, and determines the adjustment direction automatically.",
        "Automatically determines the raise/lower pH direction",
        "Supports both glacial acetic acid and soda ash",
        "Target pH plausibility assessment",
        "Neutralisation after dyeing",
        "pH adjustment before finishing",
        "Troubleshooting abnormal fabric pH",
        "Target pH",
        "Fabric weight",
    ]))

    write('calc-65', build('calc-65', [
        "🧮 Exhaust and Fixation Rate Calculator",
        "Enter the dye liquor concentrations before and after dyeing to compute the exhaustion rate and fixation rate (exhaustion method)",
        "Core formula (by input variables): (c0-c1-cw)÷c0×100; (c0-c1)÷c0×100",
        "📖 Read the \"Exhaust and Fixation Rate Calculator Usage Guide\"",
        "Concentration before dyeing C₀ (g/L)",
        "Concentration after dyeing C₁ (g/L)",
        "Soaping liquor concentration Cw (g/L)",
        "💡 Formula: exhaustion rate E% = (C₀−C₁)/C₀×100%; fixation rate F% = (C₀−C₁−Cw)/C₀×100%",
        "Concentrations may be taken as values converted from absorbance measured by spectrophotometry",
        "The soaping liquor concentration Cw is the portion of unfixed dye washed off; enter 0 if there is no data",
        "📚 In-Depth Analysis: Exhaust and Fixation Rate Calculator",
        "Reactive dye exhaust process assessment: the exhaustion rate reflects the share of dye taken up by the fibre, while the fixation rate reflects the portion actually fixed.",
        "Dye recipe screening and comparison: compare exhaustion and fixation rates across recipes, temperatures and electrolytes side by side to pick the best.",
        "Dyeing quality control: a low fixation rate indicates much loose dye and a heavy soaping burden, so the process needs adjustment.",
        "Exhaust and fixation calculation for reactive black exhaust dyeing",
        "With initial dye liquor concentration C0, residual C1 and soaping liquor C2, compute exhaustion rate=(1-C1/C0)×100% and fixation rate=(C0-C1-C2)/C0×100%; the example C0=2.0, C1=0.3, C2=0.4 g/L gives an exhaustion rate of 85% and a fixation rate of 65%.",
        "What is the difference between exhaustion rate and fixation rate?",
        "The exhaustion rate is the share of the dye liquor taken up by the fibre; the fixation rate is the share chemically bonded to the fibre and resistant to soaping. Fixation rate ≤ exhaustion rate, and the difference is the unfixed loose dye.",
        "How is the concentration measured accurately?",
        "Usually the dye liquor absorbance is measured by spectrophotometry and converted to concentration via a standard curve; residual and soaping liquors must be sampled and mixed thoroughly to avoid colorimetric error.",
        "What counts as excellent?",
        "It depends on the dye and process; for exhaust dyeing with reactive dyes a fixation rate of 60%~80% or above is often required. The specific figure should balance the product standard against cost, and this tool is a calculation reference only.",
        "About \"Exhaust and Fixation Rate Calculator\"",
        "Exhaustion rate and fixation rate are the core indicators of the dyeing and printing process. Based on the exhaustion method, this tool measures the dye liquor concentration before and after dyeing plus the soaping liquor concentration to quickly compute the exhaustion and fixation rates, helping assess dye recipes and process results.",
        "Supports three calculations: exhaustion rate, fixation rate and unfixed dye",
        "Automatic grading (excellent / good / fair / low)",
        "Input validation to prevent abnormal data",
        "Reactive dye exhaust process assessment",
        "Dye recipe screening and comparison",
        "Dyeing quality control and analysis",
        "Teaching and lab data processing for dyeing and printing",
        "Concentration before dyeing",
        "Concentration after dyeing",
        "Soaping liquor concentration",
    ]))

    write('calc-dosage-2', build('calc-dosage-2', [
        "📐 Dye Dosage Calculator",
        "Compute dye dosage and dye liquor formulation from percentage on weight of fabric (% o.w.f)",
        "Core formula (by input variables): dyeKg×1000; w×c÷100",
        "📖 Read the \"Dye Dosage Calculator Usage Guide\"",
        "Fabric weight W (kg)",
        "💡 Formula: dye dosage = W × c%; o.w.f means on weight of fabric, i.e. the percentage of dye relative to fabric weight",
        "% o.w.f is the percentage of dye dosage relative to fabric weight, a common metering method for exhaust dyeing",
        "📚 In-Depth Analysis: Dye Dosage Calculator",
        "Weighing dye for exhaust lab dips: given fabric weight and % o.w.f, directly obtain the grams of dye and reduce manual conversion.",
        "Bulk production dye liquor preparation: derive total liquor volume and concentration together with the shade depth and liquor ratio, which makes liquor preparation easier.",
        "Dyeing",
        "recipe cost accounting",
        ": dye dosage and liquor ratio directly affect cost and water use, assisting process economic comparison.",
        "Example of reactive dyeing liquor preparation for cotton",
        "Fabric 1000 g, shade depth 3% o.w.f, liquor ratio 1:10 → dye dosage 30 g; total liquor 1000×10=10000 mL (10 L), liquor concentration 30 g/10 L=3 g/L.",
        "What does o.w.f mean?",
        "An abbreviation of on weight of fibre/fabric, meaning the percentage of dye or auxiliary dosage relative to the dry fabric weight — the most commonly used metering basis in dyeing and printing.",
        "How is it corrected when dye strength differs?",
        "Actual dosage = standard dosage ÷ strength(%). At 100% strength use the nominal figure; at 80% strength multiply the dosage by 1/0.8. The tool should support a strength correction or you can convert it yourself.",
        "Does the liquor ratio matter much?",
        "The liquor ratio determines liquor volume and concentration, which affect shade depth and levelness; a small ratio saves water and energy but makes levelling harder and requires auxiliaries and suitable equipment.",
        "About \"Dye Dosage Calculator\"",
        "The dye dosage calculator is based on the % o.w.f (on fabric weight) metering method. Enter the fabric weight and dye concentration to quickly obtain the dye dosage, and combine it with the liquor ratio to compute total liquor volume and liquor concentration. It suits exhaust lab dips and bulk production liquor preparation.",
        "Outputs dye dosage (g/kg), total liquor volume and liquor concentration together",
        "Supports custom liquor ratios",
        "Input validation with automatic anomaly detection",
        "Dye weighing for exhaust lab dips",
        "Bulk production dye liquor preparation",
        "Dyeing recipe cost accounting",
        "Fabric weight",
        "Dye concentration",
        "Liquor ratio",
    ]))


if __name__ == '__main__':
    main()
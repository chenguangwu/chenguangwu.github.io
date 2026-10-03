#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'paper')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'paper')
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
    out = {'slug': slug, 'industry': 'paper', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('moisture-calc', build('moisture-calc', [
        "🧮 Paper Moisture Content Calculation",
        "Compute the moisture content from the wet and dry weights of the paper, supporting both dry-basis and wet-basis calculation",
        "Paper Moisture Calculator",
        "/ Paper Moisture Calculator",
        "📖 View the usage guide for 'Paper Moisture Content Calculation'",
        "Wet-basis moisture = (wet weight - dry weight) / wet weight × 100%",
        "Paper wet weight (g)",
        "Paper oven-dry weight (g)",
        "Calculate moisture",
        "Wet-basis moisture = (wet weight - dry weight) / wet weight × 100%; dry-basis moisture = (wet weight - dry weight) / dry weight × 100%. The standard moisture content of paper is generally 4-10%.",
        "Standard moisture content of common paper types",
        "📚 Deep Dive: Paper Moisture Content Calculation",
        "In warehousing and print suitability control, the wet-basis/dry-basis moisture is computed from the wet and dry weights to judge whether the paper meets the standard.",
        "When adjusting the equilibrium moisture, monitor the moisture content to avoid print cockling and registration errors.",
        "In quality disputes, use the dry-basis figure as the basis to check the measurement difference between buyer and seller.",
        "Worked example: wet-basis and dry-basis moisture (wet weight 100g, dry weight 92g)",
        "Water weight=100−92=8 g; wet-basis moisture=8/100×100=8.00%; dry-basis moisture=8/92×100≈8.70%; dry-basis ratio=92.00%. 8% falls within the standard moisture range (4%–10%). Formula: wet basis = water/wet weight, dry basis = water/dry weight. [SRC]",
        "Worked example: assessment grading",
        "Wet basis 4%–10% is the 'standard moisture range'; <4% is on the dry side, ≤12% is on the high side, >12% is too high. The dry basis is used for laboratory oven-dry conversions and must not be confused with the wet basis.",
        "What is the difference between wet-basis and dry-basis moisture?",
        "Wet basis = water ÷ wet weight (used in daily work), dry basis = water ÷ dry weight (used in research and trade). For the same sample the dry-basis figure is slightly larger than the wet basis (here 8.00% vs 8.70%), so always state the basis when converting.",
        "What is the standard moisture content of paper?",
        "For most printing papers the equilibrium moisture is about 4%–10% (varying with",
        "the environment). Going outside this range easily causes print cockling and registration deviation; warehousing needs temperature and humidity control.",
        "About 'Paper Moisture Calculator'",
        "A paper moisture content calculator that computes the moisture percentage from the wet and dry weights, supporting conversion between oven-dry amount and moisture content. A business and office tool that improves work efficiency, with data processed locally to protect privacy.",
    ]))

    write('roll-length', build('roll-length', [
        "📏 Paper Roll Length Calculation",
        "Compute the paper roll length from the roll outer diameter, core diameter and paper thickness",
        "'Compute the paper roll length from the roll outer diameter, core diameter and paper thickness' performs a professional calculation from the input parameters and outputs the result.",
        "📖 View the usage guide for 'Paper Roll Length Calculation'",
        "Calculate length",
        "Calculate diameter",
        "Roll outer diameter (mm)",
        "Core inner diameter (mm)",
        "Paper thickness (mm)",
        "Required length (m)",
        "Calculation principle:",
        "A paper roll can be viewed as concentric annular layers; the length L = π × (D² - d²) / (4 × t), where D is the outer diameter, d the core inner diameter and t the paper thickness.",
        "Common paper thickness reference",
        "📚 Deep Dive: Paper Roll Length Calculation",
        "In printing and slitting, the usable length is back-calculated from the roll outer diameter, core inner diameter and thickness to avoid a shortfall in the remainder.",
        "When scheduling, back-calculate the required outer diameter from the target length, which helps with roll preparation and warehousing.",
        "In stocktaking, use the length to estimate the remaining quantity on a roll.",
        "Worked example: length from outer diameter (outer diameter 1000mm, core 76mm, thickness 0.1mm)",
        "Length=π×(D²−d²)/(4t)=π×(1000²−76²)/(4×0.1)≈7808.62 m; wound layers≈(1000−76)/(2×0.1)=4620 layers. Formula: L=π(D²−d²)/(4t). [SRC]",
        "Worked example: outer diameter from target length (target 500m, core 76mm, thickness 0.1mm)",
        "Required outer diameter D=√(4tL/π+d²)=√(4×0.1×500000/π+76²)≈263.5 mm. Formula: D=√(4tL/π+d²). [SRC]",
        "Where does the roll length formula L=π(D²−d²)/(4t) come from?",
        "Unroll the paper roll into a rectangle with cross-section area = π(D²−d²)/4, then divide by the thickness t to get the length. It assumes each layer has equal thickness and is wound tightly; in reality gaps and compression cause a small deviation.",
        "What if the computed length does not match reality?",
        "First check the thickness t (nominal values often run thin or thick), the core d, and whether splices are included; if the system produces by measured length, the measured length still governs, and the formula is for estimation and roll preparation reference.",
        "About 'Paper Roll Length Calculation'",
        "A paper roll length calculator that computes the total roll length from the roll diameter, core diameter and paper thickness, and back-calculates the diameter from a known length. A business and office tool that improves work efficiency, with data processed locally to protect privacy.",
    ]))

    write('pulp-yield', build('pulp-yield', [
        "🧮 Pulp Yield Calculation",
        "Compute the yield from the raw material weight and the resulting pulp weight to assess pulping efficiency",
        "📖 View the usage guide for 'Pulp Yield Calculation'",
        "Pulp yield = pulp weight / raw material weight × 100%",
        "Raw material weight (oven-dry, kg)",
        "Pulp weight (oven-dry, kg)",
        "Calculate yield",
        "Yield notes:",
        "Pulp yield = pulp weight / raw material weight × 100%. Mechanical pulp yield is about 90-95%, chemical pulp yield about 40-50%, and semi-chemical pulp yield about 60-80%.",
        "Yield reference for common pulping methods",
        "📚 Deep Dive: Pulp Yield Calculation",
        "In pulping process evaluation, the yield (%) is computed from the raw material and resulting pulp masses to assess fibre utilisation.",
        "In cost analysis, the yield directly affects raw material consumption and energy consumption per tonne of pulp.",
        "Comparing the yield before and after process improvement quantifies the effect of cooking and grinding optimisation.",
        "Worked example: chemical pulp yield (raw material 1000kg, pulp 480kg)",
        "Yield=480/1000×100=48.00%, which falls in the 'chemical pulp' range (40%–60%); pulp per tonne of raw material=480/1000=0.4800 t. Formula: yield = resulting pulp ÷ raw material × 100%. [SRC]",
        "Worked example: yield grading",
        "≥85% high yield (mechanical pulp), 60%–85% semi-chemical pulp, 40%–60% chemical pulp, <40% low yield. The higher the yield the more fully the fibres are used, but the strength is usually lower, so a trade-off is needed by product positioning.",
        "Why does mechanical pulp have a high yield but low strength?",
        "Mechanical pulp retains almost all the fibre so the yield is high, but lignin is not largely removed, so the fibre bonding is weak and the paper yellows easily; chemical pulp removes lignin and has a low yield but better strength and durability. Choose between them by end use.",
        "Can the yield directly reflect cost?",
        "The yield is a key factor: for every 1 percentage point of yield, raw material consumption per tonne of pulp drops proportionally. But it must be assessed together with energy and chemical costs, because high-yield mechanical pulp often consumes more power.",
        "About 'Pulp Yield Calculation'",
        "An online pulp yield calculator that computes the yield percentage from the raw material weight and the pulp weight, with yield references for multiple pulping methods. A business and office tool that improves work efficiency, with data processed locally to protect privacy.",
    ]))

    write('paper-grade', build('paper-grade', [
        "⚖️ Paper Grade Reference",
        "Common paper grade classifications, quality indicators and uses",
        "📖 View the usage guide for 'Paper Grade Reference'",
        "Paper grade reference: graded by indicators such as grammage (g/m²), density, brightness, burst strength and smoothness, e.g. offset paper grammage 60 to 120 g/m² and brightness 80% to 90%; the higher the grade the fewer the allowed appearance defects and the higher the strength indicators, so the grade can be matched to the printing method and use.",
        "Search paper name",
        "Grade notes:",
        "Grade A (superior) suits high-end printing; Grade B (first grade) suits general printing; Grade C (qualified) suits ordinary uses. Brightness is expressed on the ISO scale (%).",
        "Coated paper grades",
        "Offset paper grades",
        "White cardboard grades",
        "Kraft paper grades",
        "📚 Deep Dive: Paper Grade Reference",
        "When selecting paper for printing and comparing prices for procurement, use the reference table to locate the right grade and key indicators by use (book/packaging/food).",
        "When checking process compatibility, verify whether grammage, brightness, stiffness, surface strength and opacity meet the customer's requirements.",
        "In quality disputes, use the indicator thresholds corresponding to the grade standard as the acceptance basis.",
        "Example: choosing paper for book printing",
        "Filter the reference table by 'printing paper → books': common wood-free uncoated paper is 60–120 g/m², requiring opacity≥85% and surface strength adequate for high-speed offset. Choose the specific grade according to the printing method (offset/digital) and the image coverage.",
        "Example: how key indicators are organised",
        "The table is organised as 'category - grade - typical grammage - core indicators - use'. When checking, focus first on the 1-2 indicators strongly tied to the customer contract (e.g. food packaging looks at safety compliance and grammage, posters at brightness and stiffness) to avoid being distracted by irrelevant indicators.",
        "Which indicators matter most for paper grade?",
        "The core ones are grammage, thickness/density, brightness, opacity, stiffness, surface strength (pickup speed) and smoothness. The weights differ by use: books stress opacity and smoothness, packaging stresses stiffness and burst strength, food stresses safety compliance.",
        "Can the reference table replace the standard text?",
        "No. The table is an overview for quick lookup; acceptance should follow the indicator thresholds and test methods of the latest national/industry standards. The indicators here are common ranges; the formal standards and the contract govern.",
        "About 'Paper Grade Reference'",
        "A paper grade reference table giving the grade classification, technical indicators and applicable scenarios of various papers, for paper selection in printing. A business and office tool that improves work efficiency, with data processed locally to protect privacy.",
        "Enter the paper name…",
    ]))

    write('carbon-5', build('carbon-5', [
        "📄 Filler (Calcium Carbonate/Talc) Addition",
        "Compute the filler addition, retained amount and estimated ash content of the finished sheet from the oven-dry pulp amount and the filling rate (retention taken as 70%).",
        "📖 View the usage guide for 'Filler (Calcium Carbonate/Talc) Addition'",
        "Filler addition = oven-dry pulp amount × filling rate; retained filler = addition × 70%; ash content of the sheet = retained amount ÷ (pulp amount + retained amount) × 100%",
        "The retention of fillers such as calcium carbonate or talc is usually estimated at 70%; from the filling rate the filler actually entering the sheet, the ash content and the filler-to-fibre ratio are derived, for cost and quality balance.",
        "Oven-dry pulp amount (kg)",
        "Filling rate (%)",
        "💡 Filler addition = oven-dry pulp amount × filling rate; retention estimated at 70%; ash = retained amount ÷ (pulp amount + retained amount) × 100%.",
        "📚 Deep Dive: Filler (Calcium Carbonate/Talc) Addition",
        "Filling scheme design: compute the filler addition from the oven-dry pulp amount and the target filling rate, and estimate the filler entering the sheet and the ash content at 70% retention, avoiding ash above the limit that would cause a strength drop.",
        "Cost and quality balance: calcium carbonate and talc have different prices; compare the ash content and filler-to-fibre ratio at the same filling rate to judge whether a cheaper filler can replace part of the expensive one.",
        "Troubleshooting production deviations: when the measured ash content of the sheet is clearly below the estimate, it usually indicates a drop in retention (retention aid failure or excessive vacuum), which locates the process problem.",
        "Worked example: oven-dry pulp amount 1000 kg, filling rate 20%",
        "Filler addition = 1000 × 20% = 200.00 kg; at 70% retention, retained filler = 140.00 kg; estimated ash content = 140 ÷ (1000 + 140) × 100% = 12.28%; filler/fibre mass ratio = 0.1400; addition as a share of total oven-dry mass = 200 ÷ 1200 × 100% = 16.67%.",
        "Why is retention estimated at 70%?",
        "On a conventional paper machine section without retention aid, filler retention is about 50%–75%, so 70% is a moderately conservative empirical value; with a retention aid it can exceed 85%. In practice it should be back-calculated from the measured ash on the machine.",
        "Is a higher ash content always better?",
        "No. Filling improves opacity and smoothness and lowers cost, but excessive ash weakens fibre bonding and reduces tensile and fold strength; for printing papers the ash is usually kept in the 10%–25% range.",
        "About 'Filler (Calcium Carbonate/Talc) Addition'",
        "Filler (Calcium Carbonate/Talc) addition. A free online tool processed entirely in the browser, no data uploaded, privacy and security protected.",
        "Calcium carbonate",
        "Talc",
    ]))


if __name__ == '__main__':
    main()

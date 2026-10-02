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
    # calc-gsm (50)
    write('calc-gsm', build('calc-gsm', [
        "⚖️ Fabric (EPI/PPI / GSM) Calculator",
        "Fabric GSM calculation: three modes — direct weighing, unit conversion, and yarn count estimation",
        'Performs professional calculation and outputs results based on input parameters for "fabric GSM calculation: direct weighing, unit conversion, and yarn count estimation modes".',
        "📖 View 'Fabric (EPI/PPI / GSM) Calculator User Guide'",
        "⚖️ Weighing method",
        "🔄 Unit conversion",
        "🧶 Yarn count estimation",
        "Fabric weight (g)",
        "Fabric width (cm)",
        "Width (cm, optional)",
        "oz/yd² (oz per square yard)",
        "g/m (grams per linear meter)",
        "g/cm² (grams per square cm)",
        "Width (cm, for g/m conversion)",
        "Yarn count system",
        "Tex (g/km)",
        "English cotton count Ne",
        "Metric count Nm",
        "Denier (g/9km)",
        "Warp density (ends/cm)",
        "Weft density (picks/cm)",
        "Warp shrinkage (%)",
        "Weft shrinkage (%)",
        "💡 Conversions: 1 oz/yd² = 33.906 g/m²; tex = 590.5/Ne = 1000/Nm = denier/9; GSM = (warp density × warp tex + weft density × weft tex) × (1+shrinkage) ÷ 10",
        "Weighing method: cut a fabric piece of known area, weigh it, compute GSM directly (recommended 20×20 cm sample)",
        "Unit conversion: convert among GSM, oz/yd², g/m; g/m needs the fabric width",
        "Yarn count estimation: theoretical GSM from yarn count and warp/weft density; actual weight may vary ±5% due to weaving process",
        "Yarn conversion: tex = 590.5/Ne (English), tex = 1000/Nm (metric), tex = denier/9 (denier)",
        "📚 In-depth: GSM (Gram per Square Meter) Calculation",
        "In fabric sourcing/pricing, back-calculate GSM from weight, width and length to verify order compliance",
        "In inspection, sample-weigh to measure actual GSM and compare with nominal value for deviation",
        "When comparing prices of different widths, normalize to weight per unit area",
        "Back-calculate GSM from measurement",
        "A fabric 150 cm wide, 200 cm long, 480 g → area = 1.5 × 2 = 3 m² → GSM = 480 / 3 = 160 g/m².",
        "Width-normalized price comparison",
        "Fabric A 160 g/m² (150 cm width) vs B 150 g/m² (140 cm width); by weight per area A is heavier, so A costs more material at same width; price check must use this basis.",
        "How to measure GSM most accurately?",
        "Take a representative swatch, weigh dry, measure net size for area, GSM = weight / area; moisture regain affects result, weigh dry or conditioned weight.",
        "Can GSM and yarn count be inter-converted?",
        "Not directly; GSM depends on yarn count, density and structure; only with known warp/weft density and yarn tex can it be approximated.",
        "About the Fabric (EPI/PPI / GSM) Calculator",
        "Fabric GSM calculator supports three modes: weighing (GSM directly from weight and area), unit conversion (GSM / oz/yd² / g/m), and yarn-count estimation (theoretical GSM from yarn count and warp/weft density).",
        "Three calculation modes: weighing, unit conversion, yarn-count estimation",
        "Supports tex, English Ne, metric Nm and denier yarn systems",
        "Auto-computes per-linear-meter weight, per-100m weight, EPI/PPI conversion",
        "Accounts for warp/weft shrinkage for more realistic estimation",
        "Fabric sourcing and QC weight check",
        "Textile spec conversion and quoting",
        "Weaving process design and yarn selection",
        "Textile export unit conversion",
    ]))

    # color-fastness (58)
    write('color-fastness', build('color-fastness', [
        "📚 Color Fastness Rating Query",
        "Textile color fastness grade standard and gray scale comparison query",
        "📖 View 'color-fastness User Guide'",
        "📚 Color Fastness Rating Query",
        "Color fastness is graded by GB/T 3921: color change with gray scale (GB/T 250), staining with gray scale (GB/T 251), rated 1 to 5, 5 best and 1 worst, half-grade as finest step; wash fastness ≥4 is excellent, 3 is pass, below 3 fails; test conditions include temperature (40-95 ℃), time and soap concentration, varying by fiber and shade (dark shades may be relaxed by half grade).",
        "Fastness type",
        "Wash fastness",
        "Rub fastness",
        "Light fastness",
        "Perspiration fastness",
        "Saliva fastness",
        "Grade 4-5",
        "Grade 2-3",
        "📊 Gray Scale Grade Standard",
        "Color change degree",
        "Color difference (ΔE) range",
        "No change",
        "Excellent",
        "Extremely slight change",
        "Slight change",
        "Good",
        "Clearly visible change",
        "Obvious change",
        "Fairly severe change",
        "Severe change",
        "Extremely severe change",
        "📚 Fastness Standard Requirements by Type",
        "🌊 Wash Fastness (GB/T 3921)",
        "Assesses color change and staining after washing.",
        "Requirement: superior ≥4 | first-class ≥3-4 | qualified ≥3",
        "🖐️ Rub Fastness (GB/T 3920)",
        "Dry and wet rubbing; assesses color migration.",
        "Requirement: superior ≥4 (dry)/3 (wet) | first-class ≥3-4 | qualified ≥3",
        "☀️ Light Fastness (GB/T 8427)",
        "Assesses fading under light using blue wool standards.",
        "Requirement: superior ≥4 | first-class ≥3 | qualified ≥3",
        "💧 Perspiration Fastness (GB/T 3922)",
        "Acidic and alkaline perspiration; assesses change/staining after sweat contact.",
        "🧒 Saliva Fastness (GB/T 18886)",
        "Mandatory for infant textiles; assesses fastness after saliva contact.",
        "Requirement: infant products ≥4",
        "Fastness has two separately rated items: color change (original) and staining (white cloth). Light fastness uses 1-8 (8 best).",
        "📚 In-depth: Color Fastness Rating Query",
        "Factory inspection: check wash/rub/perspiration/saliva fastness grades per GB/T.",
        "Complaint adjudication: compare gray-scale grade and ΔE range to determine pass (grade 3 is the qualified floor).",
        "Infant products: mandatory saliva fastness ≥4 (GB/T 18886).",
        "Wash fastness",
        "Fastness rating",
        "Select wash fastness (GB/T 3921), grade 4 → slight change, ΔE 1.0-2.0, 'first-class pass'; if only grade 3 it is qualified pass, below grade 2 fails and needs process/finishing improvement.",
        "Why rate color change and staining separately?",
        "Different mechanisms: change sees original fading, staining sees white cloth dyed; one sample may score high on one and low on the other, rate separately and take the stricter; do not conflate.",
        "Why is light fastness 1-8 grades?",
        "Light uses blue wool standards 1-8 (8 best), different from the 1-5 gray scale; assess sun fading per GB/T 8427 separately, not by the gray scale directly.",
        "About the Color Fastness Rating Query",
        "Color fastness rating query — textile fastness grade standard, gray scale comparison for color change and staining, free to use. A business/office tool to boost efficiency, with local data processing for privacy.",
        "Before shipment, grade wash/rub/perspiration/saliva fastness per GB/T.",
        "On complaints, compare gray-scale grade and ΔE to judge compliance.",
        "Infant textiles must check saliva fastness ≥4.",
    ]))

    # colorfastness (39)
    write('colorfastness', build('colorfastness', [
        "📋 Color Fastness Rating (Gray Scale)",
        "Input original and tested colors; auto-grade gray scale level (1-5) by color difference",
        "Color fastness rating",
        "📖 View 'Color Fastness Rating (Gray Scale) User Guide'",
        "CIE76 color difference ΔE = √((ΔL)² + (Δa)² + (Δb)²), where ΔL is lightness difference, Δa and Δb are chroma differences; ΔE maps roughly to gray scale: ΔE 0.8 → grade 5, 1.7 → 4-5, 2.5 → 3-4, 3.4 → 3, 5.0 → 2, 7.5 → 1-2; ΔE ≤1.0 is barely perceptible, ≤3.0 acceptable, >5.0 clearly visible.",
        "Original color (before treatment)",
        "Tested color (after treatment)",
        "📋 Gray Scale Grade vs Color Difference",
        "No change (excellent)",
        "Extremely slight change",
        "Slight change (good)",
        "Visible change",
        "Obvious change (medium)",
        "Fairly severe change",
        "Severe change (poor)",
        "Extremely severe change",
        "Complete change (very poor)",
        "Note: this tool estimates with the CIE76 color difference formula for reference only; formal grading should use the standard gray scale by visual comparison.",
        "📚 In-depth: Color Fastness (Color-Difference Grading)",
        "After washing, rubbing or light exposure, compare original and tested samples to estimate color-change grade",
        "QC uses gray scale / CIE76 ΔE for objective grading, reducing visual subjectivity",
        "On fading complaints, re-measure and provide ΔE data as a basis for compensation",
        "CIE76 color difference estimation",
        "Original RGB(51,102,204), after wash RGB(60,108,210) → ΔE = √(9²+6²+6²) ≈ 11.9 → color-change grade about 3-4 (good, slightly low).",
        "Grading reference",
        "ΔE <1 nearly no change (grade 5); 1-3 (4-5); 3-6 (3-4); 6-12 (2-3); >12 (1-2, obvious fading).",
        "How does ΔE map to gray-scale grade?",
        "Smaller ΔE means higher grade; generally ΔE≤1 is grade 5, ≤3 grade 4, ≤6 grade 3; refer to GB/T 250 gray scale.",
        "What if visual and instrument results differ a lot?",
        "Baseline is gray-scale visual grading under a standard light box; instrument ΔE is auxiliary; mind the light source (D65) and neutral-gray background.",
        "About the Color Fastness Rating",
        "Color fastness rating tool: input original and tested colors, compute ΔE by CIE76 and auto-grade the gray scale (1-5), with a grade reference table.",
        "Intuitive color picking for comparison",
        "Auto-compute ΔE",
        "Gray-scale grade rating",
        "Color-change fastness assessment",
        "Dyeing quality inspection",
        "Wash/rub fastness reference",
        "Color difference analysis",
    ]))

    # convert-48 (20)
    write('convert-48', build('convert-48', [
        "🔄 Yarn Count (Ne / Nm / Tex) Converter",
        "Yarn count: tex = g/1000m; English count Ne = 590.5/tex; metric count Nm = 1000/tex",
        "📖 View 'Yarn Count (Ne / Nm / Tex) Converter User Guide'",
        "English count Ne",
        "Yarn count definition",
        "Textile standard: tex = grams/1000 meters; Ne = 590.5 / tex; Nm = 1000 / tex. They convert mutually.",
        "📚 In-depth: Yarn Count (Ne / Nm / Tex) Conversion",
        "When sourcing yarn, convert English count to metric or tex for a unified spec language",
        "Quick mutual conversion when the spec sheet uses tex but the supplier quotes English count",
        "Unify units before computing fabric parameters for blended yarn counts",
        "English count to tex/metric",
        "30 English count (cotton) → tex = 590.5 / 30 ≈ 19.68; Nm = 1000 / 19.68 ≈ 50.8; i.e. 30Ne ≈ 19.7tex ≈ 50.8Nm.",
        "tex to English count",
        "20 tex → Ne = 590.5 / 20 ≈ 29.5; Nm = 1000 / 20 = 50; i.e. 20tex ≈ 29.5Ne.",
        "Which is larger, English or metric count?",
        "Numerically metric ≈ 1.69× English (cotton type); tex is inversely proportional to count, smaller tex = finer yarn.",
        "Is the conversion factor the same for different fibers?",
        "Cotton type uses 590.5, linen about 1654; man-made fibers often use tex/Nm directly; confirm the basis before cross-fiber conversion.",
        "About the Yarn Count (Ne / Nm / Tex) Converter",
        "Yarn count (Ne / Nm / Tex) converter. A textile/apparel tool to help compute fabric parameters and usage.",
    ]))

    # convert-yarn (23)
    write('convert-yarn', build('convert-yarn', [
        "🧵 Yarn English/Metric/Denier Converter",
        "Online converter for yarn English/metric/denier counts",
        "📖 View 'Yarn English/Metric/Denier Converter User Guide'",
        "Yarn English count",
        "Milli English count",
        "Kilo English count",
        "Metric count",
        "Milli metric count",
        "Kilo metric count",
        "📚 In-depth: Yarn (Weight / Length / Conditioned) Conversion",
        "Compute yarn weight from tex and length to estimate per-piece yarn usage",
        "Convert net weight to conditioned weight at different moisture regain for fair settlement",
        "Convert tex and denier (denier = tex × 9)",
        "tex to denier",
        "20 tex → denier = 20 × 9 = 180 D; i.e. 20tex = 180 denier, commonly used for filaments.",
        "Conditioned weight conversion",
        "Net weight 1000 g, actual regain 6%, cotton conditioned regain 8.5% → conditioned weight = 1000 × (1 + 8.5%) / (1 + 6%) ≈ 1023.6 g.",
        "Why use conditioned weight?",
        "Yarn moisture varies with environment; conditioned weight normalizes by standard regain so trade measurement is fair and comparable.",
        "How do tex and denier differ?",
        "tex = g/km, denier = g/9km; denier is used for filaments, tex for staple and general use.",
        "About the Yarn English/Metric/Denier Converter",
        "Yarn English/metric/denier converter. A textile/apparel tool to help compute fabric parameters and usage.",
    ]))

if __name__ == "__main__":
    main()

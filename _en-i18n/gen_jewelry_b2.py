#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'jewelry')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'jewelry')
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
    out = {'slug': slug, 'industry': 'jewelry', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('gold-purity', build('gold-purity', [
        "Gold Purity Converter",
        "Convert between karat gold, ten-thousand-fineness gold, per-mille (‰), and percentage, and calculate the pure gold content of jewelry.",
        "View the Gold Purity Converter User Guide",
        "Pure gold (g) = total weight (g) × per-mille ÷ 1000; K value = per-mille ÷ 1000 × 24 (24K = 999, 22K ≈ 916, 18K = 750, 14K = 585, 9K = 375); percentage = per-mille ÷ 10; fine gold means gold content ≥ 990‰; recycle estimate = pure gold × today's gold price − labor and loss, and jewelry with solder points or non-gold parts must deduct the alloy weight before calculation.",
        "Total jewelry weight (g)",
        "Select purity",
        "999.9 Fine (ten-thousand-fineness)",
        "999 Fine (24K)",
        "Custom per-mille (‰)",
        "Gold purity reference table",
        "Karat gold:",
        "Using 24K as the pure-gold baseline, karat × 41.67 ≈ per-mille (18K = 18/24 = 75% = 750‰).",
        "Fine gold:",
        "990‰ and above is called fine gold; 999‰ is thousand-fine; 999.9‰ is ten-thousand-fine. In practice 24K is not 100% either, mostly 999‰.",
        "Gold content:",
        "Pure gold = total weight × per-mille / 1000.",
        "Karat gold adds alloys such as silver and copper to increase hardness, with colors like yellow, white, and rose gold.",
        "In-depth: Pure gold content calculation (total weight × per-mille)",
        "Given the jewelry total weight and hallmark per-mille, calculate its pure gold weight.",
        "Verify pure gold content when estimating recycle value.",
        "How much pure gold in 10g of Au916?",
        "Pure gold = total weight × per-mille/1000 = 10 × 916/1000 = 9.16 g. So 10 g of 22K gold contains 9.16 g of pure gold.",
        "Difference between Au999 and Au916",
        "At the same 10 g, Au999 has 9.99 g pure gold and Au916 has 9.16 g, a difference of 0.83 g pure gold; higher purity is softer and better suited to plain gold.",
        "What do hallmarks Au750/Au916 mean?",
        "The number after Au is the gold-content per-mille: Au750 = 75% (18K), Au916 = 91.6% (22K), Au999 = 99.9% (thousand-fine).",
        "Do solder points affect pure gold content?",
        "Yes. Solder points on karat jewelry usually use a lower-grade solder (e.g. 14K pieces use 10K solder); although the soldered part is a small weight share, its fineness is lower. For precision, weigh the solder separately and convert by its actual fineness; daily estimates can ignore it (solder is generally < 2% of total weight). During recycle refining, manufacturers weigh by the measured fineness after smelting, which often differs from the hallmark-based theoretical calculation by 1–3%.",
        "About the Gold Purity Converter",
        "The Gold Purity Converter is an everyday online tool. Practical, life-oriented, and easy to use.",
    ]))
    write('index', build('index', [
        "Jewelry Tools",
        "Jewelry Tools",
        "Estimate carat weight from diamond diameter, height, and other dimensions using a standard-cut formula, with carat–gram–milligram unit conversion, to assist diamond valuation and certificate verification.",
        "Gold Purity (Karat & Percentage) Converter",
        "Convert between karat gold (e.g. 24K/18K) and gold-content percentage, with common alloy references, suitable for jewelry shopping and marking verification; runs entirely in the browser.",
        "Convert gold purity by karat or percentage, giving the corresponding fine-gold and alloy meaning, for jewelry marking and recycle-estimate verification; instant in-browser conversion.",
        "List ring size numbers and inner circumference/diameter references for various countries; enter a known dimension to look up the matching size, convenient for online shopping and resizing; in-browser table lookup.",
        "Score pearl quality by five factors — luster, surface, shape, color, and size — and rate the grade by weighted dimensions with grading rationale, suitable for shopping, appraisal, or teaching.",
        "A Mohs hardness (Mohs) reference for common gems and minerals, listing hardness grades, durability, and wear-care advice, to prevent scratches when shopping for or wearing jewelry.",
        "About Jewelry Tools",
        "The Jewelry Tools collection includes 6 free online tools covering common calculation, conversion, and lookup needs in jewelry scenarios. Whether you are a professional, student, or general user in the field, you can find ready-to-use utilities here. All tools run entirely in the browser, upload no data to servers, and protect your privacy and security.",
        "Jewelry tools featured on this page (representative selection):",
        "These tools help you quickly complete common jewelry-related tasks without memorizing complex formulas or converting manually — just enter values and get results.",
        "Do Jewelry Tools require download or registration?",
        "No. All Jewelry Tools on this page are in-browser online tools; open the page and use them directly, with no software installation, no account registration, and no data upload.",
        "Are Jewelry Tools' results accurate? Is the data safe?",
        "The tools compute locally in your browser based on public math formulas and common industry standards, delivering instant results. All operations run on your device, data is never uploaded to servers, and your privacy and security are guaranteed.",
    ]))
    write('pearl-grading', build('pearl-grading', [
        "Pearl Grading Standard",
        "Assess pearl quality grade by five factors: luster, surface, shape, color, and size.",
        "View the Pearl Grading Standard User Guide",
        "Luster",
        "Exceptional — mirror-like reflection, clear image",
        "Strong — bright reflection, fairly clear image",
        "Medium — some reflection, blurry image",
        "Weak — dim reflection, almost no image",
        "Surface (Blemishes)",
        "Clean — no visible blemishes to the naked eye",
        "Minor — very few tiny blemishes",
        "Slight — a few visible blemishes",
        "Heavy — obvious blemishes",
        "Round",
        "Near-round",
        "Oval",
        "Baroque (irregular)",
        "Top colors (white-pink / deep gold / peacock green)",
        "Fine colors (white / gold / black-purple)",
        "Common colors (creamy white / pale yellow)",
        "Off colors (dark yellow / gray)",
        "Grade",
        "Pearl grading factors explained",
        "1. Luster — the most important factor",
        "Luster is the soul of pearl quality. A fine pearl's surface should clearly reflect object images like a mirror. Luster is determined by the thickness and regularity of the nacre layers; thicker and denser layers give stronger luster.",
        "2. Surface / Cleanliness",
        "Refers to the amount of surface blemishes (pinpoints, bumps, cracks, growth lines). A perfectly flawless pearl is extremely rare — 'no flaw, no pearl' is trade slang. Evaluation is based on the front visible area.",
        "3. Shape",
        "Perfect round is most precious, followed by round, near-round, oval, drop, and button. Baroque (irregular) shapes, though not round, have unique forms with collectible value.",
        "4. Color",
        "Different varieties have their own top colors: Akoya (white-pink / sky blue), South Sea (white-pink / deep gold), Tahitian (peacock green / eggplant purple). Color must be judged together with overtone and iridescence.",
        "5. Size",
        "Larger diameter is rarer and more precious. Freshwater pearls are commonly 6–10 mm, Akoya mostly 5–9 mm, South Sea 10–15 mm, Tahitian 8–14 mm. Over 15 mm is extremely rare.",
        "Pearl grade reference table",
        "Grade notes:",
        "This tool references GIA and common industry grading standards, with a weighted score of the five factors (luster × 0.35 + surface × 0.25 + shape × 0.15 + color × 0.15 + size × 0.10). For reference only; actual value requires assessment by a professional appraisal institution.",
        "In-depth: Pearl quality grading (luster / blemishes / shape / matching)",
        "Grade pearls across multiple dimensions to judge value.",
        "Compare appearance differences across grades.",
        "Meaning of grades 4 / 3 / 2 / 1",
        "Luster-led, with blemishes, shape, and matching as secondary: grade 4 has the strongest near-mirror luster and grade 5 flawless is rare; grade 3 strong luster with minor flaws; grade 2 medium; grade 1 weak luster with obvious flaws. Higher grades are rarer and more valuable.",
        "Necklace matching",
        "Multi-pearl jewelry additionally considers size/color/luster matching; a strand with small deviation (matching grade 4) affects overall price more than a single pearl's grade.",
        "Why is luster the most important?",
        "Luster (orient) is the soul of the pearl; strong luster compensates for minor flaws. Blemishes are irreversible but can be hidden by design and setting, so grading puts luster first.",
        "How many blemishes are acceptable?",
        "Under common grading systems, blemishes are classed as flawless / minute / slight / marked / heavy; a perfectly round flawless pearl is extremely rare and its price rises exponentially. A practical criterion is 'social distance': flaws invisible to the naked eye at normal conversation distance (about 50 cm) are perfectly acceptable for daily wear and offer the best value; pursuing perfection usually doubles the budget. Also note that flaws around the drill hole and on the back have far less visual impact than those on the front.",
        "About the Pearl Grading Standard",
        "The Pearl Grading Standard is an everyday online tool. Practical, life-oriented, and easy to use.",
    ]))
    write('ring-size', build('ring-size', [
        "Ring Size Chart",
        "International ring size comparison (China mainland / Hong Kong / US / UK / Japan / EU); enter circumference or diameter for automatic conversion.",
        "View the Ring Size Chart User Guide",
        "Diameter = circumference ÷ π (3.14159)",
        "Finger circumference (mm)",
        "Ring inner diameter (mm)",
        "Converted size",
        "Measurement method",
        "Method 1:",
        "Wrap a thin string or strip of paper around the finger once; the measured length is the circumference (mm).",
        "Method 2:",
        "Measure the inner diameter of an existing ring (mm).",
        "Conversion formula:",
        "Fingers are slightly thicker in the evening, so measure then; those with thicker knuckles should choose half a size up; in winter fingers are thinner and a smaller size may fit. This table is for reference; the actual fit should be confirmed by trying on the real ring.",
        "International ring size chart",
        "Size notes:",
        "China mainland / Hong Kong sizes are numbered by inner circumference (mm) (e.g. size 12 = 52 mm circumference); US sizes are based on diameter; Japan sizes are circumference minus 38; EU sizes are numbered by circumference.",
        "In-depth: Ring size conversion (circumference ↔ diameter)",
        "Measure finger circumference with a soft tape to get the diameter and match the ring number.",
        "Convert between different national sizing systems.",
        "Finger circumference 55 mm corresponding diameter",
        "Diameter = circumference ÷ π = 55 ÷ 3.14159 ≈ 17.5 mm. Hong Kong size is about 14 (inner 17.5 mm); EU is often marked 55.",
        "Measure in the afternoon for accuracy",
        "Fingers swell/shrink about ±0.5 size between morning/evening and with heat/cold; measure in the warm afternoon, taking a slightly snug fit that does not slip off as the standard, and add half a size for wide bands.",
        "How do Hong Kong and EU sizes correspond?",
        "EU sizes often mark the inner circumference directly (mm, e.g. 55); Hong Kong size roughly equals the inner diameter (mm) — about size 14 corresponds to 17.5 mm. Brands vary, so use the measured inner diameter.",
        "What if I cannot measure the inner diameter?",
        "Measuring circumference by wrapping a string around the finger is most reliable: cut a non-elastic string, wrap it around the finger base for one turn, mark the overlap, straighten and measure the length (mm) — that is the circumference; inner diameter = circumference ÷ π. Measure in the evening when the finger is thickest, and measure the finger base not the knuckle; if the knuckle is clearly thicker than the base, take the midpoint of the two values to avoid a ring that is too tight or slips off.",
        "About the Ring Size Chart",
        "The Ring Size Chart is an everyday online tool. Practical, life-oriented, and easy to use.",
    ]))

if __name__ == '__main__':
    main()

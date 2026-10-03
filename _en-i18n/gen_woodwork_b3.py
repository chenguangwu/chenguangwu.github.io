#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'woodwork')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'woodwork')
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
    out = {'slug': slug, 'industry': 'woodwork', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # ===== detector-32 (40) =====
    write('detector-32', build('detector-32', [
        '⚖️ Quality (standard / inspection / certification) assurance',
        'Enter furniture mechanical performance and eco indicators to judge the furniture quality grade by standards such as GB/T 3324',
        '/ Quality (standard / inspection / certification) assurance',
        '📖 View "Furniture quality grade assessment (standard / inspection) usage guide"',
        '⚖️ Quality (standard / inspection / certification) assurance',
        'Stability coefficient = anti-overturning moment / overturning moment',
        'Furniture type',
        'Wood furniture',
        'Metal furniture',
        'Upholstered furniture',
        'Formaldehyde emission (mg/L)',
        'Mechanical performance - load force (N)',
        'Durability - cycle count',
        'Stability coefficient',
        '📚 In-depth: furniture quality grade assessment (standard / inspection)',
        'Pre-purchase quality control',
        'Quality-compliance self-check',
        'Certification and inspection comparison',
        'Select the execution standard by furniture type (wood GB/T 3324, metal GB/T 3325, upholstered QB/T 1952.1); verify the four items formaldehyde≤1.5 mg/L, load force≥1000 N, durability≥10000 cycles, stability≥0.10 all pass, then output grade.',
        'Wood furniture input formaldehyde 0.8, load force 1200 N, durability 10000 cycles, stability 0.15 → all four pass and formaldehyde>0.5, judged "First-class (E1 grade)"; if formaldehyde drops to 0.4, upgrade to "Premium (E0 grade)"; if load force is only 800 N, "Unqualified".',
        'What is the difference between E0 and E1?',
        'Refers to the formaldehyde emission limit grade; E0(≤0.5 mg/L) is stricter than E1(≤1.5 mg/L); judged by the national-standard test report; this tool only does an input-check demo.',
        'How to read the stability coefficient?',
        'Stability≥0.10 is the general pass threshold; the larger the value, the less likely to overturn; children furniture has stricter requirements.',
        'Wood furniture by GB/T 3324, metal furniture by GB/T 3325, upholstered furniture by QB/T 1952.1',
        'Formaldehyde E0 grade ≤0.5mg/L, E1 grade ≤1.5mg/L (desiccator method)',
        'Mechanical performance includes table-top strength, cabinet strength, drawer-slide strength, etc.',
        'Durability test at least 10000 cycles',
        'Stability coefficient = anti-overturning moment / overturning moment, should be ≥0.10',
        'Desk dimension planning calculator',
        'About "quality (standard / inspection / certification) assurance"',
        'Furniture quality inspection and judgment tool: enter formaldehyde emission, mechanical performance, durability and other parameters to judge the furniture quality grade by GB/T standards.',
        'Three furniture standards selectable',
        'Formaldehyde E0/E1 grade judgment',
        'Mechanical performance and durability inspection',
        'Stability safety assessment',
        'Furniture factory inspection',
        'Furniture quality acceptance',
        'Green furniture certification',
        'Consumer purchasing reference',
    ]))

    # ===== detector-37 (43) =====
    write('detector-37', build('detector-37', [
        '⚖️ Quality (grade / moisture / standard) inspection',
        'Enter wood moisture content, knot dimensions and other parameters to judge the sawn-timber quality grade by standard GB/T 153',
        'Quality (grade / moisture / standard) inspection',
        '/ Quality (grade / moisture / standard) inspection',
        'Sawn-timber grade judgment (GB/T 153 and GB/T 4817): grade by moisture content, knot size and count, curvature, cracks, etc. — knot max-size-to-face-width ratio, knots per meter, and curvature (bow height ÷ length × 100%) beyond limit downgrade the grade; moisture over limit must be re-dried and re-inspected.',
        'Wood species',
        'Softwood sawn timber',
        'Hardwood sawn timber',
        'Moisture content (%)',
        'Max knot size (mm)',
        'Board width (mm)',
        'Knots per meter',
        'Max curvature (mm/m)',
        '📚 In-depth: wood quality grade inspection',
        'At incoming acceptance, judge sawn-timber grade by moisture, knot size/count and curvature as the basis for settlement and sorting.',
        'Judge softwood (GB/T 153) and hardwood (GB/T 4817) separately to avoid mixing standards.',
        'Pre-process grading: use special/first-class timber for visible parts, lower-class for concealed or secondary-load parts.',
        'Softwood sawn-timber grade judgment',
        'Softwood (GB/T 153), moisture 12% (pass range 8–18%), max knot 30 mm, board width 200 mm → knot-diameter ratio 15.0%, knots per meter 2, curvature 2 mm/m → meets "knot ratio ≤15% and knots/m ≤2 and curvature ≤2 and moisture pass" → judged Special grade. If max knot rises to 45 mm (22.5%), rest unchanged → downgraded to First grade; if moisture rises to 20% → moisture fails, check whether it meets second-class 6–22% range to set grade.',
        'What is the difference between the two standards?',
        'Softwood sawn timber judged by GB/T 153, hardwood by GB/T 4817; the thresholds of grading indicators (knot ratio, knots per meter, curvature, moisture) differ. After selecting the wood species, the tool auto-switches the corresponding standard.',
        'How to measure moisture accurately?',
        'Use a moisture meter averaging multiple points within 30 cm from the board end, or the oven-dry method. Boards that are surface-wet or just rained read high; let them equilibrate before measuring.',
        'Softwood sawn timber judged by GB/T 153, hardwood by GB/T 4817',
        'Moisture is the key indicator: furniture timber ≤12%, construction timber ≤15%, outdoor timber ≤18%',
        'Knot grading by max knot size to board width ratio; Special grade ≤15%',
        'Curvature includes bow, crook and cup; take the max for grading',
        'Wood should be inspected after moisture equilibration to avoid grading bias from drying stress',
        'Price (market / fluctuation / cost) analysis',
        'About "quality (grade / moisture / standard) inspection"',
        'Wood quality grade inspection tool: enter moisture, knot size, curvature and other parameters to judge sawn-timber grade by GB/T 153 / GB/T 4817.',
        'Comprehensive moisture / knot / curvature assessment',
        'Supports softwood and hardwood',
        'Auto grading by national standard',
        'Gives usage suggestions',
        'Sawn-timber quality acceptance',
        'Furniture timber selection',
        'Construction timber inspection',
        'Wood import / export inspection',
        'How to use quality (grade / moisture / standard) inspection',
        'What does quality (grade / moisture / standard) inspection do?',
        'How to use quality (grade / moisture / standard) inspection?',
        'Which scenarios is quality (grade / moisture / standard) inspection suitable for?',
    ]))

    # ===== index (23) =====
    write('index', build('index', [
        '🪚 Woodworking tools',
        'Woodworking',
        'Woodworking tools',
        'Desk dimension planning calculator',
        'Desk dimension planning calculator is a free online woodworking tool. How tall should the desk and chair be? By height and usage scenario, recommend desk height, chair height, screen-center height and desktop depth by ergonomic ratios. Runs entirely in the browser, no data uploaded, no registration; open the browser and use it.',
        'Tenon dimension calculator',
        'Enter the stock thickness, width, tenon-thickness ratio and tenon type to compute each dimension and the mortise depth by woodworking standard ratios (tenon ≈ 1/3 thickness, tenon length ≈ 1.5× thickness)',
        'Curve-saw bevel angle calculation',
        'Enter the target bevel angle, material thickness and blade type to compute the chamfer width, blade travel and blade-drift compensation, plus a compound miter/bevel conversion table',
        'Wood moisture content and shrinkage conversion',
        'Wood moisture content and shrinkage converter: from initial / final moisture content convert the shrinkage rate and size change, for reserving margin in woodworking.',
        'Quality (grade / moisture / standard) inspection',
        'Quality (grade / moisture / standard) inspection is a free online woodworking tool, a wood quality grade inspection tool: enter moisture, knot size, curvature and other parameters to judge sawn-timber grade by GB/T 153 / GB/T 4817. Runs entirely in the browser, no data upload, no registration; open the browser and use it.',
        'Wood price and cost fluctuation analysis',
        'Wood price and cost fluctuation analysis tool. Enter a price series and a reference base price to compute the mean, median, sample std dev, fluctuation coefficient CV and latest-price deviation, and judge fluctuation alert by the warning threshold, for wood procurement and inventory cost control.',
        'About "woodworking tools"',
        'The woodworking tools collection gathers 7 free online tools, covering common calculation, conversion and lookup needs in woodworking scenarios. Whether you are a practitioner, student or ordinary user in the field, you can find ready-to-use small tools here. All tools run entirely in the browser, data is not uploaded to the server, protecting privacy and security.',
        'The woodworking tools collected on this page include (some representative tools):',
        'These tools help you quickly complete common woodworking-related tasks without memorizing complex formulas or manual conversion; just input to get results.',
        'Do the woodworking tools need download or registration?',
        'No. All woodworking tools on this page are pure front-end online tools; open the page and use directly, no software install, no account registration, and no data upload.',
        'Are the woodworking tools calculation results accurate? Is the data safe?',
        'Tools compute locally in your browser based on public math formulas and general industry standards, results are instant. All operations complete on your device, data is not uploaded to any server, privacy and security are guaranteed.',
    ]))

    print('body_woodwork_b3 done')

if __name__ == '__main__':
    main()

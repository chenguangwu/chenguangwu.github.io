#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'archaeology')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'archaeology')
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
    out = {'slug': slug, 'industry': 'archaeology', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # ===== artifact-measurement (25) =====
    write('artifact-measurement', build('artifact-measurement', [
        '🏺 Artifact measurement record',
        'Record artifact dimensions and weight per archaeological survey standards; auto-compute volume, density and morphological index and generate standard record entries',
        '📖 View "Artifact measurement record user guide"',
        'Enter the artifact length, width, thickness (cm) and weight (g) per archaeological survey standards; auto-convert volume and density, compute the morphological index, and generate an archivable standard measurement record. All calculations run locally in the browser; data is not uploaded to the server.',
        'Stone tool',
        'Bone / antler artifact',
        'Metal artifact',
        'Length L (cm)',
        'Width W (cm)',
        'Thickness T (cm)',
        'Mouth diameter (cm, optional)',
        'Base diameter (cm, optional)',
        'Standard record entry',
        '📚 In-depth: artifact measurement record',
        'When registering field-excavated pottery sherds, stone tools, bone artifacts and the like, enter the three dimensions (L×W×T) and weight per archaeological survey standards, auto-convert volume and density, and generate standard record entries.',
        'Distinguish complete from broken artifacts: for broken pieces record only the maximum visible dimension and mark "broken" to avoid mixing with complete-artifact morphological indices.',
        'Before compiling the excavation artifact list, use the morphological index (length-width ratio, thickness-length ratio) to batch-distinguish vessel classes (pans, jars, bowls) and aid typological grouping.',
        'Pottery jar density estimate',
        'Measured length 18.5cm, width 12.0cm, thickness (belly-direction) 9.0cm, weight 1450g. Approximate volume by rectangular solid 18.5×12.0×9.0=1998 cm³, density=1450/1998≈0.73 g/cm³, within the common range of sandy pottery (0.6~1.4 g/cm³).',
        'In what units are artifact dimensions recorded?',
        'Field records generally use centimeters (cm) or millimeters (mm) uniformly; below 1cm record in mm to the integer; weight in grams (g). Units must be consistent within one site; calibrate the caliper and scale zero before entry.',
        'Use water displacement or dimension estimate for volume?',
        'For irregular artifacts (stone, bone) prefer water displacement for true volume; sherds and broken pieces can use L×W×T approximation, but note "estimated" in the record. Density is only an auxiliary discriminator (e.g. sandy pottery lighter, fine-paste pottery heavier) and cannot date alone.',
        'About "artifact measurement record"',
        'Artifact measurement record is an online tool in the scientific research field. A scientific research tool using standard scientific formulas for accurate calculation.',
    ]))

    # ===== dating-method (25) =====
    write('dating-method', build('dating-method', [
        '🏺 Archaeological dating methods',
        'Comparison of major archaeological dating methods such as C-14, thermoluminescence, optically stimulated luminescence, with dating range, applicable materials, principle and precision',
        '📖 View "Archaeological dating methods user guide"',
        'Compare the applicable range, materials and precision of C-14, TL, OSL, tree-ring and K-Ar dating methods, to choose means by excavated sample and cross-check. Compiled from public archaeological literature for study reference only.',
        'Radiocarbon',
        'Luminescence',
        'Isotope',
        'Radiation damage',
        'Tip: C-14 calibration needs the tree-ring calibration curve (e.g. IntCal); young samples (<300 yr) watch for "modern-carbon contamination", old samples (>30,000 yr) are limited by background.',
        '📚 In-depth: archaeological dating methods',
        'When judging a site age, choose the dating means by the excavated material (charcoal, bone, pottery, volcanic ash): organic samples use C-14, fired earth and pottery use TL/OSL, ancient volcanic rock uses K-Ar.',
        'Cross-check against the tree-ring chronology (IntCal) to convert C-14 age (BP) into calendar age (cal BC/AD), giving 1σ or 2σ',
        'When comparing multiple dating results, use cross-dating to verify each other — if C14 conflicts with stratigraphic superposition, re-check whether the sample is contaminated or the layer disturbed.',
        'C-14 age conversion',
        'Measured remaining 14C ratio is 50% of modern value, by',
        '5730 yr: after about 1 half-life ≈5730 yr, i.e. about 5730 BP; after IntCal curve the corresponding calendar age is about 4550 BC (calibration range per latest curve).',
        'How old a sample can C-14 date?',
        'C-14 effective upper limit is about 50,000 yr (after ~8~9 half-lives the signal approaches background). Older samples (e.g. Early Pleistocene, hominin fossils) need K-Ar, Ar-Ar or U-series instead.',
        'What is the difference between TL and OSL?',
        'Both measure the accumulated',
        'radiation dose since the mineral (quartz, feldspar) was last heated or exposed to light',
        '. Thermoluminescence (TL) is commonly used for fired earth and pottery (heat reset); optically stimulated luminescence (OSL) for sediments (light reset), dating tens of thousands to hundreds of thousands of years, suitable for judging the last-exposure age of strata.',
        'About "archaeological dating methods"',
        'Archaeological dating methods is an online tool in the scientific research field. A scientific research tool using standard scientific formulas for accurate calculation.',
        'Search method / material / principle...',
    ]))

    # ===== index (17) =====
    write('index', build('index', [
        '🏺 Archaeology & museum tools',
        'Archaeology & museum',
        'Archaeology & museum tools',
        'Compute the number of test pits, excavation area and each pit coordinate by site extent and pit specification (southwest corner as origin, north as +X, east as +Y)',
        'Record artifact dimensions and weight per archaeological survey standards; auto-compute volume, density and morphological index and generate standard record entries',
        'Count artifacts per test pit or sampling unit to compute artifact density and compare the richness of each layer and cultural deposit, aiding excavation records.',
        'Archaeological stratum identification comparison covering geological ages and major Chinese archaeological culture-period features, aiding site stratigraphic division and age judgment.',
        'Comparison of major archaeological dating methods such as C-14, TL, OSL, with dating range, applicable materials, principle and precision',
        'Pottery typology comparison listing pottery fabric, color, decoration and typical vessel forms by major Chinese archaeological culture periods, aiding field pottery sherd identification.',
        'About "archaeology & museum tools"',
        'The archaeology & museum tools collection gathers 6 free online tools, covering common calculation, conversion and lookup needs in archaeology & museum scenarios. Whether you are a practitioner, student or ordinary user in the field, you can find ready-to-use small tools here. All tools run entirely in the browser, data is not uploaded to the server, protecting privacy and security.',
        'The archaeology & museum tools collected on this page include (some representative tools):',
        'These tools help you quickly complete common archaeology & museum tasks without memorizing complex formulas or manual conversion; just input to get results.',
        'Do the archaeology & museum tools need download or registration?',
        'No. All archaeology & museum tools on this page are pure front-end online tools; open the page and use directly, no software install, no account registration, and no data upload.',
        'Are the archaeology & museum tools calculation results accurate? Is the data safe?',
        'Tools compute locally in your browser based on public math formulas and general industry standards, results are instant. All operations complete on your device, data is not uploaded to any server, privacy and security are guaranteed.',
    ]))

    print('body_archaeology_b1 done')

if __name__ == '__main__':
    main()

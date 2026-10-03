#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'printing')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'printing')
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
    out = {'slug': slug, 'industry': 'printing', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
# -*- coding: utf-8 -*-
def main():
    write('estimate-ink', build('estimate-ink', [
        '🔮 Ink Consumption Estimator (by Coverage)',
        'Estimate ink consumption from printed area, ink coverage, ink film thickness, ink density and print run, supporting single color and CMYK four-color separation',
        '"Estimate ink consumption from printed area, ink coverage, ink film thickness, ink density and print run, supporting single color and CMYK four-color separation" is computed from the input parameters and returns the result.',
        '📖 Read the "Ink Consumption Estimator (by Coverage) User Guide"',
        '🎨 Single color estimate',
        '🔮 CMYK four colors',
        'Printed area (m²/sheet)',
        'Ink coverage (%)',
        'Ink film thickness (μm)',
        'Ink density (g/cm³)',
        'Print run (sheets)',
        'Ink unit price (CNY/kg, optional)',
        'Including waste (5%)',
        'CMYK per-color coverage (%)',
        'Cyan C (%)',
        'Magenta M (%)',
        'Yellow Y (%)',
        'Black K (%)',
        '💡 Formula: ink(kg) = area(m²) × coverage × ink film thickness(μm) × density(g/cm³) × print run × (1+waste rate) ÷ 100000. Note: 1 μm × 1 m² = 1 cm³ (1e4 cm² × 1e-4 cm)',
        'Ink film thickness reference: offset 0.7-2.4 μm (default 1.5), gravure 5-10 μm, flexo 3-8 μm, screen 10-30 μm',
        'Ink density reference: offset ink 1.0-1.3 g/cm³, UV ink 1.1-1.2 g/cm³, water-based ink 1.0-1.2 g/cm³',
        'Ink film thickness may differ per CMYK color; adjust to actual conditions.',
        '📚 Deep dive: ink consumption estimator (by coverage)',
        'Before printing, estimate total ink from printed area, coverage, film thickness, density and print run so you can prepare ink in advance and avoid running out mid-run.',
        'Estimate single color and CMYK four-color separation separately; with high solid black coverage total ink rises sharply and needs careful accounting.',
        'Combine with the ink unit price to get total cost, or allocate leftover spot ink across jobs to control consumables expense.',
        'Take "single color: area 0.5 m², coverage 40%, film thickness 1.2 μm, density 1.2 g/cm³, print run 10,000, waste 5%" as an example',
        'Ink per sheet = area×coverage×thickness×density = 0.5×0.40×1.2×1.2 = 0.288 g. Per thousand sheets = 288 g; net total ink = 0.288×10000 = 2880 g, with 5% waste = 3024 g = 3.024 kg, of which 144 g is waste. Switching to CMYK coverage [40,30,25,90] (black 90% solid), total four-color ink = 0.5×((0.40+0.30+0.25+0.90)/100)×1.2×1.2×10000×1.05/1000 ≈ 13.99 kg, about 4.6 times the single-color case, showing how dominant heavy black coverage is in ink consumption.',
        'How do the dimensions cancel in the per-sheet formula?',
        'area(m²)×coverage(0~1)×thickness(μm, i.e. 10⁻⁶ m)×density(g/cm³ = 10⁶ g/m³) → g. That is 0.5×0.4×1.2e-6×1.2e6 = 0.288 g, and the dimensions automatically resolve to grams. The identity holds exactly when thickness uses micrometers and density uses g/cm³.',
        'Where does the 5% waste come from?',
        'It refers to process losses from ink washing, mixing, proofing and pipe residue; single color typically uses 3%-5%, and spot or light colors can be higher because washing is more frequent. It multiplies net ink by (1+waste%) rather than being deducted from the print run.',
        'About "Ink Consumption Estimator (by Coverage)"',
        'Enter printed area, ink coverage, ink film thickness, ink density and print run to estimate ink consumption and cost for single color or CMYK four color, with a configurable waste rate.',
        'Supports single color and CMYK four-color separation modes',
        'Computes volume and weight precisely from film thickness and ink density',
        'Configurable waste rate and ink unit price for cost estimation',
        'Visual CMYK per-color comparison of ink distribution',
        'Ink purchasing and cost budgeting for printers',
        'Prepress process parameter estimation',
        'Ink film thickness comparison across printing methods',
        'Printing quotes and material accounting',
    ]))

    write('ink-coverage', build('ink-coverage', [
        '🖨️ Ink Consumption',
        'Approximate ink consumption per sheet:',
        '📖 Read the "Ink Consumption User Guide"',
        'ink ≈ printed area × solid coverage × ink laydown (g/m²)',
        'Laydown varies with halftone/solid coverage, commonly 0.5-3 g/m²; solid full coverage uses the most ink.',
        'Total ink = per-sheet ink × print run × (1 + waste rate).',
        'With CMYK four-color separation, each color is measured independently and then summed.',
        'Results are used for ink purchasing and printing cost accounting; actual values deviate due to paper and dot gain.',
        'ink usage = sheet area × coverage × ink laydown × sheets × colors × (1 + waste rate)',
        'Estimate ink usage from printed area, coverage and ink laydown',
        'Print sheet width (mm)',
        'Print sheet length (mm)',
        'Number of printed sheets',
        'Ink coverage (%)',
        'Ink laydown (g/m², commonly 2-4)',
        'Number of colors (CMYK=4)',
        'Ink unit price (CNY/kg)',
        'Sheet area',
        '= width × length / 1000000 (m²)',
        'Ink usage',
        '= sheet area × coverage × laydown × sheets × colors × (1 + waste rate)',
        'Ink cost',
        '= ink usage (kg) × unit price',
        'Note: ink laydown is expressed in g/m²; actual values are affected by paper absorbency and ink viscosity, so this tool gives estimates.',
        '📚 Deep dive: ink consumption',
        'Estimate per-sheet and full-run ink consumption from printed area, solid coverage and laydown (g/m²), to schedule ink replenishment and spot color mixing ratios.',
        'Multi-color jobs scale by color count: laydown stacks per color, so a four-color solid uses several times the ink of a single color.',
        'Combine with the ink unit price to account for full-run consumables cost, or leave margin in quotes for ink consumption fluctuation.',
        'Take "printed area 700×1000 mm, print run 5000, solid coverage 30%, laydown 1.0 g/m², 4 colors, unit price 80 CNY/kg, waste 5%" as an example',
        'Sheet area = 700×1000/1e6 = 0.7 m². Ink per sheet = 0.7×30%×1.0×4 = 0.84 g. Net full-run ink = 0.84×5000 = 4200 g, with 5% waste = 4410 g = 4.41 kg, cost = 4.41×80 = 352.8 CNY, ink per thousand sheets 0.882 kg. If coverage rises to 50%, ink per sheet rises to 1.4 g and the full run to 7.35 kg, so ink grows roughly linearly with coverage.',
        'How does this tool differ from "Ink Consumption Estimator (by Coverage)"?',
        'Both estimate ink but use different bases: this tool multiplies area and color count directly by laydown in g/m² (ink per unit area of solid coverage), fitting processes with a known laydown spec; the other derives from film thickness (μm) × density, fitting physical coating parameters. Results cross-check each other, and differences come from how solid ink film is modeled.',
        'What laydown g/m² should I use?',
        'Single color solid laydown is commonly 1.0~1.5 g/m², while halftone printing is far lower due to low coverage; spot solid coverage can reach 2~3 g/m². It depends on plate line ruling, blanket pressure and paper absorbency, so proof measurements govern; tool values are a first estimate.',
        'About "Ink Consumption"',
        'The Ink Consumption calculator estimates ink usage and cost from printed area, coverage, laydown and color count, with configurable waste rate and ink unit price.',
        'Multi-color printing ink calculation',
        'Adjustable coverage and laydown',
        'Automatic ink cost accounting',
        'Printing ink purchasing estimates',
        'Printing cost accounting',
        'Consumables inventory management',
        'Quote reference',
    ]))


if __name__ == '__main__':
    main()

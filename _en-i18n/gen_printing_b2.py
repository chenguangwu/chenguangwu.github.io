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
    write('box-area', build('box-area', [
        '📦 Packaging Box Unfold Area',
        'Compute unfolded area, board size and paper usage from packaging box dimensions',
        'Packaging box unfolding',
        '/ Packaging box unfolding',
        '📖 Read the "Packaging Box Unfold Area User Guide"',
        'Surface area = 2×(L×W + L×H + W×H)',
        'Box style',
        'Rectangular box (6 faces)',
        'Tuck-end box (with flaps)',
        'Tray box',
        'Tuck/glue flap width (mm)',
        'Bleed (mm)',
        'Surface area',
        'Unfolded area',
        '= surface area + tuck/glue flaps + bleed',
        'Board size',
        '≈ longest and widest unfolded dimensions + margin',
        'Note: unfolding differs by box style; this tool gives approximate estimates, and the structural drawing governs.',
        '📚 Deep dive: packaging box unfold area',
        'Before quoting printing, compute the unfolded paper area of the packaging box and, combined with paper specs, estimate cost per box and paper usage per 1000 boxes.',
        'When designing the die line, confirm the net board size (length × width) leaving enough room for glue flaps and bleed in nesting and cutting.',
        'Compare paper usage across box styles (rectangular / tuck-end / tray) and pick the material-saving option that still meets structural strength.',
        'Take "rectangular box 300×200×100 mm length/width/height, glue flap 30 mm, bleed 3 mm" as an example',
        'Rectangular',
        'box surface area',
        '=2×(300×200+300×100+200×100)=220000 mm²=2200 cm². Unfolded area = side wall band 2×(300+200)×100=100000 + two ends 2×300×200=120000 + glue flaps 2×100+2×200 =30×600=18000, total 238000 mm²=2380 cm². Net board size = ((300+200)×2+30)×(100+200+30)=1030×330 mm, with bleed 1036×336 mm. Total area with bleed =(238000+(1030+330)×2×3)/100=2461.6 cm², paper usage per 1000 boxes =2461.6×1000/10000≈246.16 m².',
        'Where do the three box styles differ in unfolded area?',
        'A rectangular box has wall wrap + two ends + glue flaps; a tuck-end box adds flaps so the unfolded length is longer; a tray box has only a bottom + low walls + glue ears and uses the least paper. This tool applies the formula of the selected style - the more complex the style and the more tuck flaps, the larger the unfolded area.',
        'Why are bleed and glue flaps counted in paper usage?',
        'Bleed is the trim safety margin (usually 3 mm) preventing white slivers from mis-cutting; glue flaps are the glued overlap area during assembly, hidden but still consuming board. Quotes should use the net board size including bleed rather than the geometric surface area alone, otherwise paper usage is underestimated by 5%-10%.',
        'About "Packaging Box Unfolding"',
        'The Packaging Box Unfold Area calculator computes surface area, unfolded area, board size and paper usage by box style and dimensions, supporting rectangular, tuck-end and tray boxes.',
        'Three box styles selectable',
        'Glue flap / bleed counted automatically',
        'Paper usage estimate',
        'Packaging structure design',
        'Board material accounting',
        'Packaging cost estimation',
        'Prepress layout reference',
    ]))

    write('carton-design', build('carton-design', [
        '📦 Folding Carton Structure Parameters',
        'Compute folding carton structure parameters, crease lines and unfolded dimensions from volume or dimensions',
        '"Compute folding carton structure parameters, crease lines and unfolded dimensions from volume or dimensions" is computed from the input parameters and returns the result.',
        'Carton structure design',
        '/ Carton structure design',
        '📖 Read the "Folding Carton Structure Parameters User Guide"',
        'Compute by dimensions',
        'Compute backward from volume',
        'Target volume (mL)',
        'Length:width ratio (L:W)',
        'Height:width ratio (H:W)',
        '📐 Structure parameter notes',
        'Volume',
        '= L × W × H (inner dimensions)',
        'Inner dimensions',
        '= outer dimensions - 2 × board thickness',
        'Unfolded size',
        '= the largest length and width including glue flaps and crease lines',
        'Crease lines',
        ': folds must be creased; the count equals the number of edges',
        '📚 Deep dive: folding carton structure parameters',
        'Given outer dimensions and board thickness, back out inner dimensions and storable volume to confirm whether the product plus cushioning fits.',
        'Given a target volume, back out recommended inner dimensions from the length:width and height:width ratios, then compute outer dimensions and the die-line unfolded size.',
        'When designing the packaging structure, confirm the crease line count and nesting unfolded size of a tube-style folding box to help draw the die line.',
        'Take "outer dimensions 200×150×100 mm, board thickness 3 mm, compute inner dimensions and volume" as an example',
        'Inner dimensions = outer - 2×thickness: inner length 194, inner width 144, inner height 94 mm. Volume =194×144×94/1000≈2626 mL (about 2.63 L). Unfolded size =2×(194+144)+15(glue flap)=691 mm (length) × (94+144+5)=243 mm (width), i.e. a 691×243 mm die-line blank.',
        'Take "target volume 1000 mL, length:width ratio 2, height:width ratio 1.5, board thickness 2 mm, back out dimensions" as an example',
        'Volume V=L×W×H=(r×W)×W×(hwr×W)=r×hwr×W³, so W=³√(V×1000/(r×hwr))=³√(1000×1000/(2×1.5))=³√333333≈69.3 mm. Inner length L=2×69.3=138.7, inner height H=1.5×69.3=104.0 mm. Outer dimensions with thickness: 142.7×73.3×108.0 mm, unfolded 431×178.3 mm.',
        'Why is the inner dimension the outer dimension minus twice the thickness?',
        'Board has six faces, so the inner clearance loses one board thickness on each side in every direction; inner dimensions = outer dimensions - 2×thickness. Only volume from inner dimensions truly reflects storable space - using outer dimensions overestimates by about (2×thickness/outer dimension)³.',
        'Why are there 7 crease lines?',
        'A standard tube-style folding box (such as a toothpaste box) has 1 glue edge on the blank + 4 longitudinal creases forming the walls + 2 transverse creases at the ends, 7 in total, which determines how it folds and assembles. Special structures (such as auto-lock bottom) have more creases.',
        'About "Carton Structure Design"',
        'The Folding Carton Structure Parameters calculator supports computing volume and unfolded size from dimensions, or back out carton dimensions from a target volume, including crease line count and board thickness correction.',
        'Bidirectional size / volume computation',
        'Automatic board thickness correction',
        'Crease line count computation',
        'Volume compliance check',
        'Package size planning',
        'Prepress structure confirmation',
    ]))


if __name__ == '__main__':
    main()

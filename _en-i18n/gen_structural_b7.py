#!/usr/bin/env python3
# gen_structural_head.py — shared head for structural batches b1..bN
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'structural')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'structural')
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
    out = {'slug': slug, 'industry': 'structural', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('torsional-shear-shaft', build('torsional-shear-shaft', [
        "Shaft Surface Shear Stress from Torque and Diameter",
        "Enter torque T and shaft diameter d to find the maximum surface shear stress.",
        "Circular Shaft Torsional Shear-Stress Calculator",
        "/ Circular Shaft Torsional Shear-Stress Calculator",
        'View "Shaft Surface Shear Stress from Torque and Diameter User Guide"',
        "τ_max = T·r/J (circular shaft).",
        "T=500, d=50 mm → about 20.4 MPa.",
        "📚 In-Depth: Circular Shaft Maximum Torsional Shear Stress",
        "Maximum shear stress on the outer surface of a transmission shaft under torque.",
        "Shaft diameter selection to satisfy allowable shear stress.",
        "Combined stiffness/strength design with the angle of twist.",
        "Torque 500 N·m, diameter 50 mm",
        "Doubling the diameter",
        "d 0.05→0.10: τ drops to 1/8 = 2.55 MPa.",
        "Shear-stress distribution?",
        "Zero at the axis, increasing linearly to the outer surface maximum; hence a larger diameter markedly lowers τ_max.",
        "Design control?",
        "τ_max must be below the material's allowable shear stress and jointly constrained with the angle of twist.",
    ]))
    write('von-mises-2d', build('von-mises-2d', [
        "Equivalent Stress from Plane-Stress State",
        "Enter plane stresses σx, σy and shear τ to find the von Mises equivalent stress.",
        "Von Mises Equivalent-Stress Calculator",
        "/ Von Mises Equivalent-Stress Calculator",
        'View "Equivalent Stress from Plane-Stress State User Guide"',
        "Plane-stress von Mises formula.",
        "Example → about 101 MPa.",
        "📚 In-Depth: Plane von Mises Equivalent Stress",
        "Equivalent stress under biaxial stress by the fourth strength theory.",
        "Yield assessment (compared with the yield limit).",
        "FEA post-processing and pressure-vessel strength checks.",
        "Pure shear",
        "Meaning of von Mises?",
        "Converts complex stress into an equivalent uniaxial tensile stress, used for yield judgment of ductile materials.",
        "Compared with the maximum-shear-stress theory?",
        "Tresca is more conservative; von Mises lies between Tresca and experiment and is commonly used in engineering.",
    ]))

if __name__ == "__main__":
    main()

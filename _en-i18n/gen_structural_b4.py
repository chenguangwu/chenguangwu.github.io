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
    write('moment-of-inertia-circle', build('moment-of-inertia-circle', [
        "Solid Circular Section Moment of Inertia from Diameter",
        "Enter the circular-section diameter d to find the section moment of inertia.",
        "Circular Section Moment-of-Inertia Calculator",
        "/ Circular Section Moment-of-Inertia Calculator",
        'View "Solid Circular Section Moment of Inertia from Diameter User Guide"',
        "I = πd⁴/64 (solid circle).",
        "📚 In-Depth: Circular Section Moment of Inertia",
        "A basic geometric quantity for the bending-stiffness calculation of round shafts and bars.",
        "Compare the diameter effect when optimizing the section.",
        "Linked with deflection and buckling formulas.",
        "Diameter 100 mm",
        "Doubling the diameter",
        "d 0.1→0.2: I grows 16× = 7.85×10⁻⁵ m⁴.",
        "Relationship with polar moment of inertia?",
        "For a circular section I_polar = 2I, i.e. the polar moment is twice the moment about any axis.",
        "Unit?",
        "Fourth power of length (m⁴), reflecting the section's bending-resistance geometry.",
    ]))
    write('moment-of-inertia-rect', build('moment-of-inertia-rect', [
        "Moment of Inertia (I = b·h³ / 12)",
        "Moment of inertia of a rectangular section about its neutral axis.",
        "Rectangular Section Moment-of-Inertia Calculator",
        "/ Rectangular Moment of Inertia",
        "Rectangular Moment of Inertia",
        'View "Moment of Inertia (I = b·h³ / 12) User Guide"',
        "I = b·h³/12 (about the strong axis).",
        "0.1×0.2 m rectangle I≈6.67×10⁻⁵ m⁴.",
        "📚 In-Depth: Rectangular Section Moment of Inertia",
        "Moment of inertia of a rectangular beam (b width, h height) about its neutral axis.",
        "Sensitivity analysis of beam height on stiffness.",
        "Section design of timber and steel beams.",
        "Doubling the height",
        "h 0.2→0.4: I grows 8× (h³), stiffness greatly increases.",
        "Note on axis parallel shift?",
        "Here it is about the centroidal axis; for an offset axis use the parallel-axis theorem I=I_c+Ad².",
        "Effect of aspect ratio?",
        "Moment of inertia is proportional to h³; increasing height is more effective than increasing width for flexural stiffness.",
    ]))
    write('polar-moment-circle', build('polar-moment-circle', [
        "Solid Circular Section Polar Moment of Inertia from Diameter",
        "Enter the circular-section diameter d to find the polar moment of inertia.",
        "Circular Section Polar-Moment Calculator",
        "/ Circular Section Polar-Moment Calculator",
        'View "Solid Circular Section Polar Moment of Inertia from Diameter User Guide"',
        "📚 In-Depth: Circular Section Polar Moment of Inertia",
        "A basic geometric quantity for circular-shaft torsional-stiffness calculation.",
        "Linked with angle-of-twist and shear-stress formulas.",
        "Superposition of polar moments when combining multi-shaft sections.",
        "Diameter 100 mm",
        "Doubling the diameter",
        "d 0.1→0.2: J grows 16× = 1.57×10⁻⁴ m⁴.",
        "Polar vs planar moment of inertia?",
        "For a circular section J=2I; torsion uses J, bending uses I.",
        "Unit?",
        "Fourth power of length (m⁴), proportional to d⁴.",
    ]))
    write('radius-of-gyration', build('radius-of-gyration', [
        "Radius of Gyration (r = √(I / A))",
        "The radius of gyration reflects how far the section area is distributed from the centroid.",
        "Section Radius-of-Gyration Calculator",
        "/ Radius of Gyration",
        "Radius of Gyration",
        'View "Radius of Gyration (r = √(I / A)) User Guide"',
        "With I=1e-6 and A=1e-3, r≈31.6 mm.",
        "📚 In-Depth: Radius of Gyration",
        "Slenderness-ratio calculation of columns",
        "geometric parameter.",
        "Section compactness assessment (against local instability).",
        "Linked with Euler buckling and stability coefficients.",
        "Area increase",
        "A 1e-3→2e-3 (I unchanged): r drops to 22.4 mm.",
        "How to compute the slenderness ratio?",
        "λ=L/r; the larger r is, the less prone to buckling; slender columns have large λ and poor stability.",
        "Meaning?",
        "Equivalent to the effective section radius derived from the moment of inertia, reflecting how far the mass is distributed from the axis.",
    ]))

if __name__ == "__main__":
    main()

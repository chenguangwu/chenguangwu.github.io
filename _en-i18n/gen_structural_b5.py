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
    write('section-modulus-circle', build('section-modulus-circle', [
        "Circular Section Bending Modulus from Diameter",
        "Enter the circular-section diameter d to find the section bending modulus.",
        "Circular Section Bending-Modulus Calculator",
        "/ Circular Section Bending-Modulus Calculator",
        'View "Circular Section Bending Modulus from Diameter User Guide"',
        "S = πd³/32 (circular section).",
        "📚 In-Depth: Circular Section Modulus",
        "The section modulus in the circular-section bending stress σ=M/S.",
        "Bending section selection for round shafts.",
        "Linked with the beam bending-strength formula.",
        "Diameter 100 mm",
        "Doubling the diameter",
        "d 0.1→0.2: S grows 8× = 7.85×10⁻⁴ m³.",
        "Relationship with moment of inertia?",
        "For a circular section S=I/(d/2)=πd³/32, used directly in σ=M/S.",
        "Unit?",
        "Third power of length (m³).",
        "How to Use the Circular Section Bending Modulus from Diameter",
        "What does the Circular Section Bending Modulus from Diameter do?",
        "Circular Section Bending-Modulus Calculator: enter the circular-section diameter d and compute the section bending modulus by S = πd³/32, for round-shaft bending-stress checks.",
        "How do I use the Circular Section Bending Modulus from Diameter?",
        "Which scenarios suit the Circular Section Bending Modulus from Diameter?",
        "Circular section bending modulus Z=π·d³/32 (d diameter): the section's ability to resist bending moment under pure bending; a larger Z is less prone to bending failure.",
        "Bending normal stress σ=M/Z (M moment). Used for strength checks of round members such as shafts and columns; is the solid circle Z larger than a hollow circle of the same area? At the same outer diameter the solid is larger, but the hollow is lighter.",
    ]))
    write('section-modulus-rect', build('section-modulus-rect', [
        "Section Modulus (W = b·h² / 6)",
        "The section modulus is used in the bending normal stress σ = M/W.",
        "Rectangular Section Modulus Calculator",
        "/ Rectangular Section Modulus",
        "Rectangular Section Modulus",
        'View "Section Modulus (W = b·h² / 6) User Guide"',
        "W = b·h²/6 (about the strong axis).",
        "0.1×0.2 m rectangle W≈6.67×10⁻⁴ m³.",
        "📚 In-Depth: Rectangular Section Modulus",
        "Maximum bending stress σ=M/W calculation of a rectangular beam.",
        "Section design of timber and steel-plate beams.",
        "Sensitivity analysis of height on the section modulus.",
        "Doubling the height",
        "h 0.2→0.4: W grows 4× (h²) = 2.67×10⁻³ m³.",
        "Bending stress formula?",
        "σ_max=M/W; the larger W is, the smaller the maximum stress.",
        "Strong vs weak axis?",
        "When bending about the weak axis, W is small and stress is large; pay attention to the load direction in design.",
    ]))
    write('slenderness-ratio', build('slenderness-ratio', [
        "Slenderness Ratio (λ = L / r)",
        "The larger the slenderness ratio, the more prone to instability.",
        "Column Slenderness-Ratio Calculator",
        "/ Slenderness Ratio",
        "Slenderness Ratio",
        'View "Slenderness Ratio (λ = L / r) User Guide"',
        "Slenderness definition: λ = L/r, where L is the member's effective length and r is the section radius of gyration (r = sqrt(I/A)); a larger slenderness means higher buckling risk, commonly graded with 100 as a rough boundary; r is determined by the moment of inertia I and area A, and material strength cannot compensate for an excessive slenderness.",
        "Radius of gyration (m)",
        "λ = L/r; the larger λ, the more prone to buckling.",
        "L=2, r=0.0316 gives λ≈63.",
        "📚 In-Depth: Slenderness Ratio",
        "Core parameter for column stability classification (high/low slenderness).",
        "Prerequisite for looking up the steel-column stability coefficient.",
        "Radius-of-gyration optimization when selecting the section.",
        "Column length 2 m, r=31.6 mm",
        "Smaller radius of gyration",
        "r 31.6→15.8 mm: λ doubles to 126.5, more prone to buckling.",
        "What does the magnitude of λ mean?",
        "The larger λ, the closer to Euler buckling; the smaller, the closer to strength failure; steel structures often require λ below a limit.",
        "Effective length?",
        "Use L_e=KL in practice, where K is set by the end constraints.",
    ]))
    write('ss-point-deflection', build('ss-point-deflection', [
        "Mid-Span Deflection (δ = P·L³ / (48·E·I))",
        "Maximum deflection of a simply supported beam under a mid-span concentrated load.",
        "Simply Supported Beam Point-Load Deflection Calculator",
        "/ Simply Supported Beam Mid-Span Deflection",
        "Simply Supported Beam Mid-Span Deflection",
        'View "Mid-Span Deflection (δ = P·L³ / (48·E·I)) User Guide"',
        "δ = PL³/(48EI) (mid-span point load). Example about 8.33 mm.",
        "δ = PL³/(48EI) (mid-span point load).",
        "Example about 8.33 mm.",
        "📚 In-Depth: Simply Supported Beam Mid-Point Load Deflection",
        "Elastic deflection of a simply supported beam under a mid-span concentrated load.",
        "Floor-beam deflection-limit check.",
        "Comparison with the uniform-load case.",
        "10 kN mid-span / span 2 m",
        "Doubling the span",
        "L 2→4: δ grows 8× (L³) ≈ 66.7 mm.",
        "Compared with a cantilever?",
        "Under the same P, L and EI, the simply supported mid-span deflection is 1/4 of the cantilever end deflection.",
        "Deflection limit?",
        "Take L/250–L/400 etc. by usage; floor slabs commonly L/250.",
    ]))

if __name__ == "__main__":
    main()

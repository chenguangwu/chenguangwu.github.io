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
    write('allowable-stress', build('allowable-stress', [
        "Allowable Stress (σ_allow = σ_yield / n)",
        "Determines the allowable stress from the yield strength and safety factor.",
        "Allowable Stress Calculator",
        "/ Allowable Stress",
        'View "Allowable Stress (σ_allow = σ_yield / n) User Guide"',
        "Yield strength (MPa)",
        "250 MPa, n=1.5 → about 167 MPa.",
        "📚 In-Depth: Allowable Stress",
        "The upper stress limit a member can sustain long-term, based on the yield limit and safety factor.",
        "Strength-allowable verification in pressure-vessel and steel-structure member design.",
        "Recheck whether the allowable stress meets the service conditions when substituting materials.",
        "Q235 steel member (n=1.5)",
        "Yield strength σy=235 MPa, safety factor n=1.5: allowable stress σa=σy/n=235/1.5≈156.7 MPa.",
        "High-strength bolt (n=2.0)",
        "σy=900 MPa, n=2.0: σa=900/2=450 MPa; design at or below 450 MPa.",
        "How to choose the safety factor?",
        "For static loads on ductile materials, 1.5–2.0 is common; for dynamic loads or brittle materials use a larger value, set per code and failure consequence.",
        "Relationship between allowable stress and yield limit?",
        "Allowable stress = ultimate stress / safety factor; it is the permitted upper stress in design, not an intrinsic material property.",
    ]))
    write('angle-of-twist', build('angle-of-twist', [
        "Angle of Twist from Torque, Length and Stiffness",
        "Enter torque T, length L, shear modulus G and diameter d to find the angle of twist.",
        "Circular-Shaft Angle-of-Twist Calculator",
        "/ Circular-Shaft Angle-of-Twist Calculator",
        'View "Angle of Twist from Torque, Length and Stiffness User Guide"',
        "θ = TL/(GJ). Example → about 0.0102 rad.",
        "Example → about 0.0102 rad.",
        "📚 In-Depth: Angle of Twist",
        "Verification of the twist per unit length of a transmission shaft under torque.",
        "Stiffness design of long shafting, limiting the twist angle to avoid linkage error.",
        "Compare the torsional stiffness of shafts with different diameters.",
        "Steel transmission shaft 50 mm",
        "Doubling the diameter increases stiffness",
        "d from 0.05 to 0.10: J grows 16×, and under the same torque θ shrinks to about 1/16 (0.00064 rad).",
        "What if the angle of twist is too large?",
        "Too large causes transmission phase error and meshing shock; precision equipment must keep θ within the allowable range.",
        "What is G?",
        "Shear modulus",
        ", steel is about 79–80 GPa; it depends on the material, and a larger value resists torsional deformation better.",
    ]))
    write('axial-strain', build('axial-strain', [
        "Strain from Elongation and Original Length",
        "Enter elongation ΔL and original length L to find the axial strain.",
        "Axial Strain Calculator",
        "/ Axial Strain Calculator",
        'View "Strain from Elongation and Original Length User Guide"',
        "Elongation ΔL (m)",
        "ε is dimensionless.",
        "📚 In-Depth: Axial Strain",
        "Relative elongation or shortening of a tension/compression bar under axial force.",
        "Materials",
        "Strain calculation in testing.",
        "Structural-deformation monitoring: back-calculate displacement from strain.",
        "2 m bar elongates 2 mm",
        "ΔL=0.002 m, L=2 m: strain ε=ΔL/L=0.002/2=0.001=0.1%.",
        "Short column compression",
        "Original length 3 m compressed 1.5 mm: ε=0.0015/3=0.0005=0.05% (compressive strain).",
        "Does strain have a unit?",
        "Strain is a dimensionless ratio (ΔL/L), usually expressed as a percentage or microstrain με, where 1% = 10000 με.",
        "Sign of tensile vs compressive strain?",
        "Elongation is positive (tension), shortening is negative (compression); the deformation itself has no unit.",
    ]))
    write('beam-shear-center', build('beam-shear-center', [
        "Support Shear (V = P / 2)",
        "When a simply supported beam carries a mid-span concentrated load, each support takes half.",
        "Simply Supported Beam Mid-Span Point-Load Shear Calculator",
        "/ Simply Supported Beam Support Shear",
        "Simply Supported Beam Support Shear",
        'View "Support Shear (V = P / 2) User Guide"',
        "With a mid-span concentrated load P, V = P/2.",
        "10 kN load → 5 kN per support.",
        "📚 In-Depth: Beam Shear Distribution (Double Web)",
        "Web shear distribution of a double-web section under vertical shear.",
        "Preliminary shear-flow estimate for box girders and I-sections.",
        "When shear is symmetric, the two webs share the shear equally.",
        "Total shear 10 kN",
        "Symmetric double web: each web V=P/2=10/2=5 kN.",
        "Eccentric-load correction",
        "If the shear center is offset, distribute by the webs' distance from the neutral axis; here we approximate with symmetric equal sharing.",
        "What is the shear center?",
        "The point through which the shear-force line passes; a load through it bends the beam without twisting; especially important for open thin-walled sections.",
        "How about a single-web beam?",
        "A single web carries all the shear, V=P.",
    ]))

if __name__ == "__main__":
    main()

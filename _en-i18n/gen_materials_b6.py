#!/usr/bin/env python3
# gen_materials_b6.py — materials b6 (5 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'materials')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'materials')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

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
    out = {'slug': slug, 'industry': 'materials', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

MASS = [
 "Mass (m = ρ·V)",
 "Compute mass from density and volume.",
 "Mass from Density Calculator",
 "/ Mass from Density",
 "Mass from Density",
 "📖 View Guide: Mass (m = ρ·V)",
 "Mass–density relation: m = rho * V, i.e. mass equals density times volume; density rho = m/V is mass per unit volume; specific volume v = V/m = 1/rho is the reciprocal of density, the volume occupied per unit mass; the three are mutually convertible, and knowing any two yields the third.",
 "📚 In Depth: Mass from Density",
 "Back-calculate mass from density and volume",
 "Batching and cutting stock accounting",
 "Casting / injection molding usage",
 "2400 kg/m³, pour 0.5 m³: m = 1200 kg. Fix the volume first, then multiply by density to get mass.",
 "Versus weight",
 "In engineering mass is often treated as weight (multiply by g for gravity), but strictly mass is the amount of matter while weight is the gravitational force.",
 "Why compute volume first, then multiply by density?",
 "Density is an intensive quantity (independent of total amount), mass = density × volume; measuring or designing the volume first, then multiplying, is least error-prone.",
 "How to choose density for porous materials?",
 "Distinguish apparent density (including pores) from true density (excluding pores); material selection must specify which is used, as the apparent density of foamed metal is far below its true density.",
]

SHEAR = [
 "Shear Strain from Shear Stress and Modulus",
 "Enter shear stress τ and shear modulus G to find shear strain.",
 "Shear Strain Calculator",
 "/ Shear Strain Calculator",
 "📖 View Guide: Shear Strain from Shear Stress and Modulus",
 "Shear stress τ (Pa)",
 "📚 In Depth: Shear Strain (Material)",
 "Shear strain from shear stress and G",
 "Adhesive / riveted joint analysis",
 "Torsional deformation",
 "gamma = tau / G. With shear stress tau = 10 MPa and G = 77 GPa, gamma ≈ 1.3e-4 (radian). Shear strain is a dimensionless angular deformation.",
 "Versus angle",
 "For small deformation gamma ≈ tan(φ) ≈ φ (radian), the change in a right angle.",
 "What are the units of shear strain?",
 "Dimensionless (radian, since it is length over length). In engineering the right-angle change is expressed directly in radians.",
 "What is the difference between shear strain and normal strain?",
 "Normal strain is extension (rate of length change) while shear strain is angular distortion (right-angle change); they correspond to normal and tangential loading respectively.",
]

TENSILE = [
 "Tensile Force (F = σ·A)",
 "Given stress and cross-sectional area, find the sustainable tensile force.",
 "Cross-Section Tensile Load Calculator",
 "/ Tensile Load",
 "Tensile Load",
 "📖 View Guide: Tensile Force (F = σ·A)",
 "📚 In Depth: Tensile Stress",
 "Normal stress from force and area",
 "Strength verification",
 "Fracture prediction",
 "sigma = F / A. A 10 kN force on a 100 mm² section gives sigma = 100 MPa. A smaller A raises stress under the same force, more likely exceeding strength.",
 "Versus yield",
 "When sigma exceeds yield strength, plastic deformation begins; beyond tensile strength it fractures; design with a safety factor.",
 "Is stress the same as pressure?",
 "Same dimension (force/area), but stress is internal force distribution (tension, shear or compression) whereas pressure usually means external fluid pressure; solid mechanics uses stress.",
 "Why do cross-section transitions break easily?",
 "stress concentration",
 "It makes local sigma far above the nominal value, with cracks initiating at notches; hence avoid sharp corners and use fillet transitions.",
]

TRUE = [
 "True Strain (ε_t = ln(L / L₀))",
 "Strain defined by the natural logarithm under large deformation.",
 "True Strain Calculator",
 "/ True Strain",
 "True Strain",
 "📖 View Guide: True Strain (ε_t = ln(L / L₀))",
 "📚 In Depth: True Strain (Logarithmic Strain)",
 "Cumulative strain in large deformation / metal forming",
 "Rolling / extrusion",
 "Additivity",
 "engineering strain",
 "epsilon_t = ln(L/L0). Original length 100 stretched to 150: engineering strain 0.5, true strain ln1.5 ≈ 0.405. True strains from multiple passes are additive.",
 "Two-stage true strains add directly (e.g. 0.2 each totals 0.4); engineering strain cannot be simply added, so forming analysis uses true strain.",
 "Why use true strain for large deformation?",
 "True strain is based on instantaneous length, is additive, and unbounded, matching the material's actual accumulated damage; engineering strain distorts under large deformation.",
 "Can true strain exceed 1?",
 "Yes. Doubling length gives ln2 ≈ 0.693, tenfold gives ln10 ≈ 2.3; indicating severe forming (e.g. deep drawing).",
]

EED = [
 "Strain Energy Density from Stress and Modulus",
 "Enter stress σ and elastic modulus E to find strain energy per unit volume.",
 "Elastic Strain Energy Density Calculator",
 "/ Elastic Strain Energy Density Calculator",
 "📖 View Guide: Strain Energy Density from Stress and Modulus",
 "📚 In Depth: Elastic Strain Energy Density",
 "Elastic energy stored per unit volume",
 "Spring / beam energy storage",
 "Impact-resistant design",
 "U = sigma^2/(2E) = 1/2 * sigma * epsilon. Steel under 200 MPa with E = 200 GPa: U = 200e6^2/(2*200e9) = 100 J/m³. Fully released on unloading.",
 "Versus stiffness",
 "A large E gives low energy density (hard and brittle stores little); rubber has small E but large deformation, so total storage is significant.",
 "Why the sigma squared?",
 "In linear elasticity stress rises linearly with strain, average stress is half the peak, energy = average stress × strain = sigma^2/(2E).",
 "What is the difference between elastic energy and plastic work?",
 "Elastic energy is fully released on unloading (reversible), while plastic work turns into heat and defects (irreversible); impact energy-absorption design must distinguish them.",
]

write('mass-from-density', build('mass-from-density', MASS))
write('shear-strain', build('shear-strain', SHEAR))
write('tensile-force-area', build('tensile-force-area', TENSILE))
write('true-strain', build('true-strain', TRUE))
write('elastic-energy-density', build('elastic-energy-density', EED))

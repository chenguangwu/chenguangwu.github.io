#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""materials 第5批：shear-modulus / specific-weight / vickers-hardness / young-from-kg / engineering-strain"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'materials')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'materials')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        for i, it in enumerate(items):
            print('   ', i, repr((it.get('zh') or it.get('zh_src', ''))[:50]))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    return mp


def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'materials', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))


# ---------------- shear-modulus (19) ----------------
write('shear-modulus', build('shear-modulus', [
    "Shear Modulus (G = E / (2(1+ν)))",
    "The relation of shear modulus to Young's modulus and Poisson's ratio.",
    "/ Shear Modulus",
    "Shear Modulus",
    '\U0001F4D6 View the "Shear Modulus (G = E / (2(1+ν))) User Guide"',
    "\U0001F4DA Deep Dive: Shear Modulus G",
    "Measures a material's shear stiffness",
    "Torsion design",
    "Relation with E and nu",
    "G = tau / gamma (shear stress /",
    "Shear strain",
    "). For isotropic materials G = E/(2(1+nu)). Steel E=200GPa, nu=0.3 gives G about 77 GPa.",
    "Torsion",
    "Circular-shaft torsion angle",
    "θ = T*L/(G*J), larger G means more torsion resistance; spring stiffness also depends on G.",
    "Which is larger, G or E?",
    "G is always smaller than E (isotropic); G=E/(2(1+nu)), and for nu between 0~0.5, G is 1/3~1/2 of E.",
    "Why do springs use shear modulus?",
    "Helical springs are mainly under torque (shear stress); stiffness is set by G and coil geometry, so material selection looks at G.",
]))

# ---------------- specific-weight (19) ----------------
write('specific-weight', build('specific-weight', [
    "Specific Weight (γ = ρ·g)",
    "Weight per unit volume (specific weight).",
    "Specific Weight Calculator",
    "/ Specific Weight",
    "Specific Weight",
    '\U0001F4D6 View the "Specific Weight (γ = ρ·g) User Guide"',
    "Steel specific weight about 77 kN/m³.",
    "\U0001F4DA Deep Dive: Specific Weight (Unit Weight)",
    "Derive per-unit-volume gravity from density",
    "Geotechnical / structural loads",
    "Buoyancy",
    "Engineering loads",
    "2400 kg/m3: gamma=2400*9.81≈23.5 kN/m3, i.e. each cubic meter weighs 23.5kN. Common in geotechnics.",
    "Versus density",
    "Specific weight is the gravity form of density times g (N/m3 or kN/m3), convenient for computing gravity loads directly.",
    "What is the relation between specific weight and density?",
    "gamma=rho*g; density is mass density, specific weight is weight density. In engineering, structural/geotechnical loads commonly use specific weight to compute forces directly.",
    "Buoyancy and specific weight?",
    "Buoyancy = displaced-liquid specific weight × volume; an object floats if its specific weight is less than the liquid's (Archimedes' principle).",
]))

# ---------------- vickers-hardness (19) ----------------
write('vickers-hardness', build('vickers-hardness', [
    "Vickers Hardness (HV = 1.854·F / d²)",
    "Vickers hardness is obtained from the indentation diagonal length and test force (F converted to kgf).",
    "Vickers Hardness Calculator",
    "/ Vickers Hardness",
    '\U0001F4D6 View the "Vickers Hardness (HV = 1.854·F / d²) User Guide"',
    "Test force (N)",
    "Indentation diagonal (mm)",
    "HV = 1.854·F_kgf/d²; F is in kgf.",
    "\U0001F4DA Deep Dive: Vickers Hardness HV",
    "Diamond pyramid indentation hardness test",
    "Universal across the whole hardness range",
    "Thin layers / micro areas",
    "Precision quality inspection",
    "HV = 1.854*F/d^2 (F load N, d mean of the two diagonals mm, result kgf/mm2 or converted to GPa). Small indentation, adjustable load; universal from soft to hard.",
    "Geometrically self-similar and load-independent (same material); suited to thin coatings, welds and micro areas with high result comparability.",
    "Why is Vickers universal across the whole range?",
    "The regular pyramid indentation geometry is load-independent; soft and hard materials share one formula; Rockwell needs scale changes, Brinell is limited to medium hardness.",
    "Are HV and HB numerically comparable?",
    "In the medium-hardness region they are approximately equal; for high hardness/thin layers Vickers is more accurate, HB tends larger or inapplicable.",
]))

# ---------------- young-from-kg (18) ----------------
write('young-from-kg', build('young-from-kg', [
    "Back-calculate Young's Modulus from K and G",
    "Input bulk modulus K and shear modulus G to find Young's modulus E.",
    "Young's Modulus from K and G",
    "/ Young's Modulus from K and G",
    '\U0001F4D6 View the "Back-calculate Young\'s Modulus from K and G User Guide"',
    "E = 9KG/(3K+G). K=166.7, G=76.9 GPa → about 200 GPa.",
    "K=166.7, G=76.9 GPa → about 200 GPa.",
    "\U0001F4DA Deep Dive: Young's Modulus from Load",
    "Tensile test back-calculates E from force and elongation",
    "Material quality inspection",
    "Teaching experiments",
    "E = (F/A) / (ΔL/L0) = F*L0/(A*ΔL). Given cross-sectional area A, gauge length L0, applied force F and elongation ΔL, E is obtained.",
    "Must be measured in the elastic segment (stress below the proportional limit); beyond it becomes non-linear and E is no longer constant.",
    "Why measure in the elastic segment?",
    "Hooke's Law",
    "Only the elastic stress-strain is linear with constant E; the plastic segment slope changes and cannot represent Young's modulus.",
    "Does specimen size affect the result?",
    "E is a material constant, independent of size; but A and L0 must be measured accurately to compute correctly; thin specimens demand higher ΔL resolution.",
]))

# ---------------- engineering-strain (18) ----------------
write('engineering-strain', build('engineering-strain', [
    "Engineering Strain (ε = (L − L₀) / L₀)",
    "Relative change of the gauge length.",
    "Engineering Strain Calculator",
    "/ Engineering Strain",
    "Engineering Strain",
    '\U0001F4D6 View the "Engineering Strain (ε = (L − L₀) / L₀) User Guide"',
    "Engineering strain definition: epsilon = (L - L0)/L0, the length change divided by the original gauge length; elongation = epsilon × 100%; true strain epsilon_t = ln(L/L0) is more accurate than engineering strain under large deformation; both are positive in tension and negative in compression.",
    "\U0001F4DA Deep Dive: Engineering Strain",
    "Nominal strain for tension/compression",
    "Standard quantity in material testing",
    "Yield determination",
    "epsilon = (L - L0)/L0 = ΔL/L0. Original length 100mm stretched to 102mm: epsilon=0.02 (2%). Based on the original length.",
    "Versus true strain",
    "Under large deformation engineering strain deviates from the true value (see true-strain); under small deformation the two are approximately equal.",
    "What is the difference between engineering strain and true strain?",
    "Engineering strain is based on the initial length (ΔL/L0), true strain on the instantaneous length (ln(L/L0)); they approximate each other for small deformation but differ markedly for large deformation.",
    "Why do standards use engineering strain?",
    "Convenient to measure (only original and current length needed), sufficient for small deformation; true strain is used only for large deformation/formability analysis.",
]))

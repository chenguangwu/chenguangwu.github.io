#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""materials 第2批：hooke-strain / bulk-modulus / poisson-lateral / thermal-resistance / fracture-toughness"""
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


# ---------------- hooke-strain (30) ----------------
write('hooke-strain', build('hooke-strain', [
    "Axial Strain (ε = σ / E)",
    "Within the linear elastic range, strain equals stress divided by the elastic modulus.",
    "Hooke's Law Strain Calculator",
    "/ Hooke's Law Strain",
    "Hooke's Law Strain",
    '\U0001F4D6 View the "Axial Strain (ε = σ / E) User Guide"',
    "ε = σ/E (uniaxial stress).",
    "Steel at 200 MPa and 200 GPa → ε=0.001.",
    "\U0001F4DA Deep Dive: Hooke's Law (Stress-Strain)",
    "Under uniaxial stress sigma=E*epsilon",
    "Material linear elastic range",
    "Stiffness and deformation conversion",
    "sigma = E * epsilon (uniaxial). Steel E=200GPa, strain 0.001 gives sigma=200MPa, exactly within the elastic range.",
    "Three-dimensional",
    "General stress states use the generalized",
    "Hooke's Law",
    " (including",
    "Poisson's ratio",
    " coupling), uniaxial is a special case.",
    "Where is the linear elastic range?",
    "Below the proportional limit, sigma-epsilon is a straight line; beyond it turns plastic. Hooke's law holds only within the linear elastic range.",
    "Is E related to hardness?",
    "Indirectly. Hard materials often have large E, but hardness also involves plasticity/work-hardening and cannot be derived from E alone.",
    "How to Use Axial Strain (ε = σ / E)",
    "What does Axial Strain (ε = σ / E) do?",
    "Within the linear elastic range, input stress and elastic modulus; compute axial strain by ε = σ/E, used to estimate deformation under tension or compression.",
    "How do I use Axial Strain (ε = σ / E)?",
    "Which scenarios suit Axial Strain (ε = σ / E)?",
    "Axial strain ε=ΔL/L: the relative length change of an object after force, dimensionless (often expressed in %).",
    "Within the elastic range stress σ=E·ε (E is Young's modulus). Strain describes the degree of deformation and is the base quantity for strength and stiffness analysis.",
]))

# ---------------- bulk-modulus (26) ----------------
write('bulk-modulus', build('bulk-modulus', [
    "Bulk Modulus (K = E / (3(1−2ν)))",
    "Bulk modulus characterizes a material's resistance to uniform compression.",
    "Bulk Modulus Calculator",
    "/ Bulk Modulus",
    '\U0001F4D6 View the "Bulk Modulus (K = E / (3(1−2ν))) User Guide"',
    "\U0001F4DA Deep Dive: Bulk Modulus K",
    "Measures a material's resistance to uniform compression",
    "Hydraulics / crust / fluids",
    "Relation with E and nu",
    "K = -V*dp/dV (pressure increment /",
    "Volumetric strain",
    "). Isotropic K = E/(3(1-2nu)). Water K about 2.2 GPa, steel about 160 GPa.",
    "Compressibility",
    "Larger K means harder to compress; compressibility beta = 1/K. Gases have small K and compress easily, solids have large K.",
    "What is the relation between bulk modulus and Young's modulus?",
    "K=E/(3(1-2nu)); as nu→0.5, K→∞ (incompressible, e.g. rubber/water approximation).",
    "Why is bulk modulus often mentioned for liquids?",
    "Liquids are nearly unshearable (G≈0) but compressibility is described by K, so fluid mechanics uses K (or sound speed c=sqrt(K/rho)).",
    "How to Use Bulk Modulus (K = E / (3(1−2ν)))",
    "What does Bulk Modulus (K = E / (3(1−2ν))) do?",
    "The bulk modulus calculator computes a material's resistance to uniform compression from Young's modulus and Poisson's ratio via K=E/[3(1−2ν)], suited to elastic-parameter conversion in mechanics of materials and solid-state physics.",
    "How do I use Bulk Modulus (K = E / (3(1−2ν)))?",
    "Which scenarios suit Bulk Modulus (K = E / (3(1−2ν)))?",
    "Bulk modulus K=−V·dp/dV: the material's ability to resist uniform compression, unit pascal (Pa). Larger K means harder to compress.",
    "Related",
    "Related to Young's modulus E and Poisson's ratio ν by K=E/(3(1−2ν)). Fluids (liquids/gases) commonly use bulk modulus to describe compressibility.",
]))

# ---------------- poisson-lateral (24) ----------------
write('poisson-lateral', build('poisson-lateral', [
    "Lateral Strain (ε_lat = −ν·ε_long)",
    "When axially stretched, lateral contraction occurs; the proportionality coefficient is Poisson's ratio.",
    "Poisson Lateral Strain Calculator",
    "/ Poisson Lateral Strain",
    "Poisson Lateral Strain",
    '\U0001F4D6 View the "Lateral Strain (ε_lat = −ν·ε_long) User Guide"',
    "Axial strain",
    "ν=0.3, axial 0.001 → lateral −0.0003.",
    "\U0001F4DA Deep Dive: Lateral Strain (Poisson Effect)",
    "From",
    "Axial strain",
    "Poisson's ratio",
    "find lateral strain",
    "Deformation estimate of precision fits",
    "Prevent seizing",
    "epsilon_lat = - nu * epsilon_ax. Steel nu=0.3, axial stretch 1%, lateral shrinks 0.3%. Shaft thins under tension, thickens under compression.",
    "Engineering significance",
    "Interference fits and bearing press-fitting must account for lateral deformation; the barreling of compressed bars also originates here.",
    "How does lateral change under compression?",
    "Axial compression (epsilon_ax<0) gives lateral expansion (epsilon_lat>0); the sign is guaranteed by the negative in the formula.",
    "Volume change and Poisson's ratio?",
    "Small deformation",
    "Volumetric strain",
    "ε_v ≈ epsilon_ax*(1-2nu); at nu=0.5 volume is unchanged (incompressible).",
]))

# ---------------- thermal-resistance (22) ----------------
write('thermal-resistance', build('thermal-resistance', [
    "Thermal Resistance from Thickness, Conductivity and Area",
    "Input thickness L, thermal conductivity k and area A to find thermal resistance.",
    "Thermal Resistance Calculator",
    "/ Thermal Resistance Calculator",
    '\U0001F4D6 View the "Thermal Resistance from Thickness, Conductivity and Area User Guide"',
    "R_th = L/(k·A). Example → 0.1 K/W.",
    "Example → 0.1 K/W.",
    "\U0001F4DA Deep Dive: Thermal Resistance",
    "Total thermal resistance of multi-layer walls adds up",
    "Insulation design",
    "Equivalent circuit",
    "Heat-transfer calculation",
    "R = d/(k*A) (single layer). A three-layer wall has R1,R2,R3 in series, total R=R1+R2+R3, total heat flow q=ΔT/R_total, analogous to a circuit",
    "Ohm's law",
    "Contact thermal resistance",
    "Real interlayers have contact thermal resistance; design with a margin; convection/radiation boundaries are also converted to surface thermal resistance.",
    "How to reduce heat transfer?",
    "Increase total thermal resistance: thicken, use low-k material, add air layer, reduce contact thermal resistance.",
    "How do you stack the total thermal resistance of a multi-layer wall?",
    "Just series stacking: R_total=R1+R2+R3…, the same as in a circuit",
    "Series resistors",
    "Similarly. E.g. three-layer materials with R of 0.1000, 0.5000, 0.0500 K/W give total 0.6500 K/W; at 20 K difference heat flow q=ΔT/R_total≈30.8 W.",
]))

# ---------------- fracture-toughness (21) ----------------
write('fracture-toughness', build('fracture-toughness', [
    "Fracture Toughness from Stress Intensity Factor",
    "Input geometry factor Y, stress σ and crack half-length a to find the stress intensity factor.",
    "Fracture Toughness Calculator",
    "/ Fracture Toughness Calculator",
    '\U0001F4D6 View the "Fracture Toughness from Stress Intensity Factor User Guide"',
    "K = Y·σ·√(πa); unstable when K≥K_IC. Example → about 19.9 MPa√m.",
    "Geometry factor Y",
    "Crack half-length a (m)",
    "K = Y·σ·√(πa); unstable when K≥K_IC.",
    "Example → about 19.9 MPa√m.",
    "\U0001F4DA Deep Dive: Fracture Toughness K_IC",
    "Material's resistance to crack propagation",
    "Damage-tolerance design",
    "Safe critical crack",
    "Failure analysis",
    "K_IC is plane-strain fracture toughness (MPa·m^0.5). Critical K=Y*sigma*sqrt(pi*a); when K reaches K_IC it grows unstably. Steel K_IC about 50, aluminum alloy about 25.",
    "Given K_IC and stress, one can back-calculate the allowable max crack a_c; inspection thresholds are set accordingly.",
    "What does a large K_IC indicate?",
    "Even with cracks the material tolerates higher stress before growth, good brittle-fracture resistance; high-strength steel with low K_IC fears defects (e.g. weld cold cracking).",
    "Why are thick parts more brittle?",
    "Thick parts satisfy plane strain with the lowest (most conservative) K_IC; thin parts have high plane-stress toughness; hence use the thickest part's K_IC for conservative design.",
]))

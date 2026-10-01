#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""materials 第3批：volumetric-strain / bulk-modulus-e-nu / modulus-resilience / fourier-conduction / lame-lambda"""
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


# ---------------- volumetric-strain (21) ----------------
write('volumetric-strain', build('volumetric-strain', [
    "Volumetric Strain from Three Principal Strains",
    "Input three orthogonal-direction strains to find the volumetric strain.",
    "Volumetric Strain Calculator",
    "/ Volumetric Strain Calculator",
    '\U0001F4D6 View the "Volumetric Strain from Three Principal Strains User Guide"',
    "\U0001F4DA Deep Dive: Volumetric Strain",
    "Compute relative volume change",
    "Porosity / compression analysis",
    "Poisson's ratio",
    "Relationship",
    "epsilon_v = ΔV/V0. For isotropic small deformation epsilon_v ≈ epsilon_ax*(1-2nu); at incompressible nu=0.5 the volumetric strain ≈ 0.",
    "Hydraulic vessels, rock compression and rubber large-deformation all need to track volume change.",
    "Volumetric strain and Poisson's ratio?",
    "For isotropic small deformation ε_v=(1-2nu)*ε_ax; the larger nu, the harder volume changes; at nu=0.5 volume is conserved.",
    "Why care about volumetric strain?",
    "It directly links pressure and density change (K=-p/ε_v) and is a core quantity for fluids / porous media / constitutive relations.",
    "How to Use Volumetric Strain from Three Principal Strains",
    "What does Volumetric Strain from Three Principal Strains do?",
    "The volumetric strain calculator computes volumetric strain from three principal strains by ε_v=ε_x+ε_y+ε_z, suited to analysis of elastic-plastic deformation and rock/soil volume change.",
    "How do I use Volumetric Strain from Three Principal Strains?",
    "Which scenarios suit Volumetric Strain from Three Principal Strains?",
]))

# ---------------- bulk-modulus-e-nu (20) ----------------
write('bulk-modulus-e-nu', build('bulk-modulus-e-nu', [
    "Bulk Modulus from Elastic Modulus and Poisson's Ratio",
    "Input elastic modulus E and Poisson's ratio ν to find the bulk modulus.",
    "Bulk Modulus from E and ν Calculator",
    "/ Bulk Modulus from E and ν Calculator",
    '\U0001F4D6 View the "Bulk Modulus from Elastic Modulus and Poisson\'s Ratio User Guide"',
    "K = E/[3(1−2ν)]. Steel → about 166.7 GPa.",
    "Steel → about 166.7 GPa.",
    "\U0001F4DA Deep Dive: Bulk Modulus from E and ν",
    "Given",
    "Poisson's ratio",
    "Convert K",
    "Inter-conversion of material parameters",
    "FEM input preparation",
    "K = E / (3*(1-2*nu)). E=200GPa, nu=0.3: K=200/(3*0.4)=166.7 GPa. The three parameters (E,nu,G,K) have only two independent.",
    "Inter-conversion",
    "Given any two, derive the rest: G=E/(2(1+nu)), K=E/(3(1-2nu)), avoiding redundant measurement.",
    "Do the four elastic constants have only two independent?",
    "Isotropic linear elasticity has only 2 independent constants (e.g. E,nu); both G and K are determined by them, so they are inter-convertible.",
    "Why does K surge as nu approaches 0.5?",
    "The denominator (1-2nu)→0, K→∞, corresponding to the incompressible limit; numerically nu slightly over 0.5 gives negative K (non-physical).",
]))

# ---------------- modulus-resilience (21) ----------------
write('modulus-resilience', build('modulus-resilience', [
    "Resilience (U_r = σ_y² / (2E))",
    "Energy absorbed per unit volume within the elastic range of a material.",
    "Modulus of Resilience Calculator",
    "/ Modulus of Resilience",
    "Modulus of Resilience",
    '\U0001F4D6 View the "Resilience (U_r = σ_y² / (2E)) User Guide"',
    "Yield strength (Pa)",
    "250 MPa, 200 GPa → about 156 kJ/m³.",
    "\U0001F4DA Deep Dive: Modulus of Resilience (Elastic Specific Work)",
    "A material's ability to absorb elastic deformation energy",
    "Spring material selection",
    "Impact resistance",
    "Ur = sigma_y^2/(2E) (area before yield). High-Ur materials (high yield and low E, such as some spring steels/titanium) suit repeated energy absorption without residual deformation.",
    "Versus toughness",
    "Modulus of resilience only looks at the elastic segment; toughness includes the total plastic-segment area; rubber has a large elastic segment but a different yield concept.",
    "What is the difference between modulus of resilience and elastic strain energy?",
    "Modulus of resilience is the maximum elastic energy absorbed per unit volume up to yield (a material constant),",
    "Elastic strain-energy density",
    "which varies with stress.",
    "Why choose high-Ur materials for springs?",
    "Repeated loading must absorb energy within the elastic range without permanent deformation; a larger Ur means more energy absorbed per volume and longer life.",
]))

# ---------------- fourier-conduction (19) ----------------
write('fourier-conduction', build('fourier-conduction', [
    "Heat Flow Rate from Fourier's Law",
    "Input thermal conductivity k, area A, temperature difference ΔT and thickness L to find the heat flow rate.",
    "1D Heat Conduction Calculator",
    "/ 1D Heat Conduction Calculator",
    '\U0001F4D6 View the "Heat Flow Rate from Fourier\'s Law User Guide"',
    "q = k·A·ΔT/L. Steel k=50, example → 1000 W.",
    "Steel k=50, example → 1000 W.",
    "\U0001F4DA Deep Dive: Fourier Heat Conduction",
    "Compute 1D steady-state conduction power",
    "Insulation / heat-dissipation design",
    "Wall temperature difference",
    "Heat transfer",
    "q = k*A*ΔT/d (heat flow W). Wall k=0.04W/mK, A=10m2, thickness 0.2m, inside-outside difference 20K: q=0.04*10*20/0.2=40W. Thicken or lower k to reduce heat flow.",
    "Thermal resistance",
    "R=d/(kA), layered and stacked; equivalent-circuit thinking, total thermal resistance determines total heat flow.",
    "Is a large thermal conductivity k good or bad?",
    "Heat sinks need large k (fast conduction), insulation needs small k (e.g. rock wool, aerogel); it depends on the use.",
    "Why is double-glazed glass insulating?",
    "The middle air layer has very small k and blocks convection; total thermal resistance rises greatly, heat transfer far below single glazing.",
]))

# ---------------- lame-lambda (19) ----------------
write('lame-lambda', build('lame-lambda', [
    "Lamé's First Parameter from Elastic Modulus and Poisson's Ratio",
    "Input elastic modulus E and Poisson's ratio ν to find Lamé's first parameter λ.",
    "Lamé's First Parameter λ Calculator",
    "/ Lamé's First Parameter λ Calculator",
    '\U0001F4D6 View the "Lamé\'s First Parameter from Elastic Modulus and Poisson\'s Ratio User Guide"',
    "λ = Eν/[(1+ν)(1−2ν)]. Steel E=200GPa, ν=0.3 → about 115 GPa.",
    "Steel E=200GPa, ν=0.3 → about 115 GPa.",
    "\U0001F4DA Deep Dive: Lamé's First Parameter λ",
    "3D elastic constitutive (λ, G)",
    "FEM / continuum mechanics",
    "Stress-strain tensor",
    "lambda = E*nu/((1+nu)*(1-2nu)), with",
    "Shear modulus",
    "G together form the isotropic constitutive sigma = lambda*tr(epsilon)*I + 2G*epsilon.",
    "lambda reflects the volumetric response component, G reflects the shape response; their ratio is determined by nu.",
    "What is the relation between λ and K?",
    "K = lambda + 2G/3; both describe volumetric stiffness but in different formulations (Lamé uses λ,G, engineering commonly uses E,nu).",
    "Why does FEM prefer λ,G?",
    "Writing the 3D constitutive directly with λ,G is most concise and convenient to implement; preprocessing then converts from E,nu.",
]))

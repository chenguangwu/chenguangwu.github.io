#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""materials 第4批：linear-thermal-expansion / rule-of-mixtures / specific-heat-capacity / thermal-diffusivity / youngs-modulus"""
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


# ---------------- linear-thermal-expansion (19) ----------------
write('linear-thermal-expansion', build('linear-thermal-expansion', [
    "Thermal Elongation from Expansion Coefficient",
    "Input linear expansion coefficient α, original length L and temperature change ΔT to find the elongation.",
    "Linear Thermal Expansion Calculator",
    "/ Linear Thermal Expansion Calculator",
    '\U0001F4D6 View the "Thermal Elongation from Expansion Coefficient User Guide"',
    "ΔL = α·L·ΔT. Steel α=1.2e-5, L=2m, ΔT=100 → 2.4 mm.",
    "Steel α=1.2e-5, L=2m, ΔT=100 → 2.4 mm.",
    "\U0001F4DA Deep Dive: Linear Thermal Expansion",
    "Compute length change from temperature change",
    "Bridge / track expansion joints",
    "Assembly clearance",
    "Temperature compensation",
    "ΔL = alpha * L0 * ΔT. Steel alpha≈12e-6/°C, length 10m, heated 50°C: ΔL=12e-6*10*50=0.006m=6mm, an expansion joint is needed.",
    "Anisotropy",
    "Single crystals / composites have different alpha in each direction, which may cause warping; isotropic materials are the same in all directions.",
    "Why leave gaps in rails?",
    "Thermal elongation is large (centimeters accumulated over kilometers); without release it buckles, so expansion joints or seamless-track prestress compensation are used.",
    "What does a negative alpha mean?",
    "A few materials (e.g. antimony, some ceramics) shrink on heating (negative expansion) and can be used in precision dimensionally stable composites.",
]))

# ---------------- rule-of-mixtures (21) ----------------
write('rule-of-mixtures', build('rule-of-mixtures', [
    "Rule of Mixtures Calculator",
    "The longitudinal elastic modulus of fiber-reinforced composites is approximated as a volume-weighted average.",
    "/ Rule of Mixtures Modulus",
    "Rule of Mixtures Modulus",
    '\U0001F4D6 View the "Rule of Mixtures Calculator User Guide"',
    "Longitudinal modulus (E_c = V_f·E_f + V_m·E_m)",
    "Fiber volume fraction",
    "Fiber modulus (Pa)",
    "Matrix modulus (Pa)",
    "\U0001F4DA Deep Dive: Rule of Mixtures",
    "Estimate composite macro-properties",
    "Fiber-reinforced modulus",
    "Material selection design",
    "Multiphase materials",
    "Longitudinal modulus E_c = V_f*E_f + V_m*E_m (volume-fraction weighted). Carbon fiber E_f=230GPa at 60%, matrix E_m=3GPa: E_c≈0.6*230+0.4*3=139.2GPa.",
    "Bounds",
    "Longitudinal uses arithmetic mean (iso-strain), transverse uses harmonic mean (iso-stress), giving upper and lower bounds respectively; actual lies in between.",
    "Why is longitudinal stronger than transverse?",
    "Longitudinal fiber carries load (iso-strain, high arithmetic mean); transverse relies on matrix transfer (iso-stress, low harmonic mean), so composites are strongly anisotropic.",
    "Is the rule of mixtures exact?",
    "It is a first-order approximation (ignoring interface, distribution), giving bounds; exact needs micromechanics models, but engineering estimates suffice.",
]))

# ---------------- specific-heat-capacity (19) ----------------
write('specific-heat-capacity', build('specific-heat-capacity', [
    "Heat Capacity from Mass and Specific Heat",
    "Input mass m and specific heat c to find the heat capacity.",
    "Heat Capacity Calculator",
    "/ Heat Capacity Calculator",
    '\U0001F4D6 View the "Heat Capacity from Mass and Specific Heat User Guide"',
    "C = m·c. Water m=2kg, c=4200 → 8400 J/K.",
    "Water m=2kg, c=4200 → 8400 J/K.",
    "\U0001F4DA Deep Dive: Specific Heat Capacity",
    "Compute heating absorption Q=m*c*ΔT",
    "Thermal design",
    "Process temperature control",
    "Material heat capacity",
    "c is heat absorbed per unit mass to raise 1K. Water c=4186 J/(kg·K) is very large (good heat storage), aluminum 900, steel 460. Q=m*c*ΔT.",
    "Versus heat capacity",
    "Heat capacity C=m*c (total heat-absorbing ability); specific heat is an intensive quantity convenient for comparing materials.",
    "What is the difference between specific heat and thermal conductivity?",
    "Specific heat is 'how much heat can be stored' (J/kgK), thermal conductivity is 'how fast it transfers' (W/mK); insulation values the combination of both.",
    "Why is the coastal temperature difference small?",
    "Seawater has large specific heat, heats and cools slowly, moderating climate; inland has small specific heat, large day-night/seasonal swings.",
]))

# ---------------- thermal-diffusivity (19) ----------------
write('thermal-diffusivity', build('thermal-diffusivity', [
    "Thermal Diffusivity from Conductivity, Density and Specific Heat",
    "Input thermal conductivity k, density ρ and specific heat c to find the thermal diffusivity.",
    "Thermal Diffusivity Calculator",
    "/ Thermal Diffusivity Calculator",
    '\U0001F4D6 View the "Thermal Diffusivity from Conductivity, Density and Specific Heat User Guide"',
    "α = k/(ρ·c). Steel ≈ 1.4×10⁻⁵ m²/s.",
    "Steel ≈ 1.4×10⁻⁵ m²/s.",
    "\U0001F4DA Deep Dive: Thermal Diffusivity",
    "Gauges how fast temperature changes propagate in a material",
    "Transient heat transfer",
    "Unsteady-state analysis",
    "Material selection",
    "alpha = k/(rho*c). Large-alpha materials equalize temperature quickly inside (e.g. metals); small-alpha heat up slowly and insulate (e.g. wood, insulation).",
    "Versus thermal conductivity",
    "k is the 'rate ceiling' of heat transfer, alpha is the 'speed of temperature equalization'; both large means fast and uniform.",
    "What is the difference between thermal diffusivity and thermal conductivity?",
    "k governs 'how fast it transfers', alpha=k/(rho*c) governs 'how fast temperature responds'; high heat capacity slows equalization (small alpha).",
    "Why do metals feel cool to the touch?",
    "Metals have large k and alpha; touching draws heat away fast and surface cools quickly, so they feel cool (actual temperature is the same as the environment).",
]))

# ---------------- youngs-modulus (20) ----------------
write('youngs-modulus', build('youngs-modulus', [
    "Young's Modulus (E = σ / ε)",
    "Find the elastic modulus as the ratio of stress to strain.",
    "Young's Modulus Calculator",
    "/ Young's Modulus",
    '\U0001F4D6 View the "Young\'s Modulus (E = σ / ε) User Guide"',
    "Strain",
    "200 MPa / 0.001 = 200 GPa (steel).",
    "\U0001F4DA Deep Dive: Young's Modulus (Elastic Modulus)",
    "Measures axial stiffness of a material",
    "Structural design material selection",
    "Stress-strain slope",
    "E = sigma / epsilon (uniaxial stress/strain ratio), unit Pa. Steel E about 200 GPa is very stiff, rubber about 0.01 GPa very soft; larger E is harder to stretch-deform.",
    "Versus deformation",
    "Under the same stress, a material with smaller E has larger strain (softer). ΔL = F*L0/(E*A), bridge/",
    "Beam deflection",
    "is directly governed by E.",
    "What does a large E mean?",
    "Large axial stiffness, hard to stretch/compress; does not mean high strength (strength is the yield limit). Diamond has large E yet is brittle.",
    "What is the relation between Young's modulus and stiffness?",
    "E is the intrinsic material stiffness (stress per unit strain); structural stiffness also depends on shape (A, L), and E*A/L is the member's axial stiffness.",
]))

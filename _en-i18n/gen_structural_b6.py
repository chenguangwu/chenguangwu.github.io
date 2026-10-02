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
    write('ss-udl-moment', build('ss-udl-moment', [
        "Maximum Moment (M_max = w·L² / 8)",
        "For a simply supported beam under uniform load, the mid-span moment is maximum.",
        "Simply Supported Beam Uniform-Load Moment Calculator",
        "/ Simply Supported Beam Uniform-Load Moment",
        "Simply Supported Beam Uniform-Load Moment",
        'View "Maximum Moment (M_max = w·L² / 8) User Guide"',
        "Uniform load (kN/m)",
        "M_max = w·L²/8 (uniform w, simply supported).",
        "10 kN/m, 4 m span: mid-span moment 20 kN·m.",
        "📚 In-Depth: Simply Supported Beam Uniform Maximum Moment",
        "Mid-span maximum moment of a simply supported beam under uniform load.",
        "Design moment of floor and roof beams.",
        "Comparison with the point-load case.",
        "Uniform 10 kN/m, span 4 m",
        "w=10 kN/m, L=4 m: mid-span M_max=wL²/8=10×16/8=20 kN·m.",
        "Doubling the load",
        "w 10→20: M grows linearly to 40 kN·m.",
        "Where is the maximum moment?",
        "Under uniform load the mid-span is maximum and the end supports are zero.",
        "Relationship with shear?",
        "Support shear V=wL/2; at mid-span shear is zero and moment is maximum.",
    ]))
    write('stress-concentration', build('stress-concentration', [
        "Maximum Stress (σ_max = K_t · σ_nom)",
        "Stress is amplified at geometric discontinuities (holes, notches).",
        "Stress Concentration Calculator",
        "/ Stress Concentration",
        "Stress Concentration",
        'View "Maximum Stress (σ_max = K_t · σ_nom) User Guide"',
        "Stress concentration factor",
        "Nominal stress (MPa)",
        "σ_max = K_t·σ_nom; K_t is looked up from geometry tables.",
        "At K_t=2 the nominal stress is doubled.",
        "📚 In-Depth: Stress Concentration Factor",
        "Estimate of local maximum stress at notches, holes and steps.",
        "Nominal-stress correction at fatigue-sensitive locations.",
        "Compare Kt for different geometries.",
        "Kt=2, nominal 100 MPa",
        "Fillet optimization",
        "Increasing the fillet radius lowers Kt from 2 to 1.4: σ_max=140 MPa.",
        "What is Kt?",
        "Theoretical stress concentration factor = local maximum stress / nominal stress; it relates only to geometry, not to material.",
        "Is a ductile material safe?",
        "Under static load a ductile material can locally yield and redistribute, but fatigue cases remain dangerous and must be controlled.",
    ]))
    write('thermal-strain', build('thermal-strain', [
        "Thermal Strain from Expansion Coefficient and Temperature Difference",
        "Enter the linear expansion coefficient α and temperature difference ΔT to find the thermal strain.",
        "Thermal Strain Calculator",
        "/ Thermal Strain Calculator",
        'View "Thermal Strain from Expansion Coefficient and Temperature Difference User Guide"',
        "Steel α=1.2e-5, ΔT=100°C → 0.0012.",
        "📚 In-Depth: Thermal Strain",
        "Free thermal strain of a member under uniform heating/cooling.",
        "Temperature-deformation compensation design.",
        "Linked with constrained thermal stress (becomes stress when constrained).",
        "Steel temperature rise 100°C",
        "Temperature rise 50°C",
        "ΔT 100→50: ε halves to 0.06%.",
        "Why is free expansion stress-free?",
        "Free deformation produces strain only, not stress; if constrained, ε turns into thermal stress σ=EαΔT.",
        "Differences among materials?",
        "Steel α≈1.2e-5,",
        "≈1.0e-5, aluminum≈2.3e-5; deformation differs under temperature change.",
    ]))
    write('torsion-polar-j', build('torsion-polar-j', [
        "Polar Moment of Inertia (J = π·d⁴ / 32)",
        "Geometric parameter for circular-section torsion.",
        "Solid Circular Section Polar-Moment Calculator",
        "/ Circular Section Polar Moment",
        "Circular Section Polar Moment",
        'View "Polar Moment of Inertia (J = π·d⁴ / 32) User Guide"',
        "Diameter (m)",
        "At d=0.1 m, J≈9.82×10⁻⁶ m⁴.",
        "📚 In-Depth: Torsional Polar Moment of Inertia",
        "Input geometric quantity for circular-shaft torsion analysis (same as polar moment).",
        "Torsional-stiffness calculation of multi-step stepped shafts.",
        "Linked with shear-stress and angle-of-twist formulas.",
        "Diameter 100 mm",
        "Comparison with hollow shaft",
        "A hollow shaft of the same outer diameter (inner 0.05) has slightly smaller J but significantly less weight, with better specific strength.",
        "For non-circular sections?",
        "Non-circular torsion uses the Saint-Venant torsion constant; this circular formula does not apply.",
        "Unit of J?",
        "m⁴, proportional to d⁴.",
    ]))

if __name__ == "__main__":
    main()

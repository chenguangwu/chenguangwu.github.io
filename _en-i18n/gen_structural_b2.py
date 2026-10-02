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
    write('beam-shear-stress', build('beam-shear-stress', [
        "Maximum Shear Stress (τ_max = 1.5·V / A)",
        "For a rectangular-section beam the shear stress is greatest at the neutral axis, 1.5× the average shear stress.",
        "Rectangular Beam Shear-Stress Calculator",
        "/ Rectangular Beam Maximum Shear Stress",
        "Rectangular Beam Maximum Shear Stress",
        'View "Maximum Shear Stress (τ_max = 1.5·V / A) User Guide"',
        "Shear force (kN)",
        "τ_max = 1.5·V/A (rectangular section).",
        "📚 In-Depth: Web Average Shear Stress",
        "Estimate of the average shear stress in the web of an I-beam under shear.",
        "Shear check in composite-beam connection design.",
        "Combined strength assessment with the beam bending stress.",
        "Shear 5 kN / web 0.1 m²",
        "Web thickening",
        "A from 0.1 to 0.2 m²: τ halves to 37.5 kPa.",
        "Where does the 1.5 factor come from?",
        "The conversion coefficient from average shear stress for a rectangular section; the I-beam web uses 1.5 to approximate the maximum shear stress.",
        "Where is the maximum shear stress?",
        "Maximum at the neutral axis, distributed parabolically along the section height.",
    ]))
    write('bearing-pressure', build('bearing-pressure', [
        "Bearing Pressure (p = N / A)",
        "Average contact compressive stress at the foundation base.",
        "Base Average-Pressure Calculator",
        "/ Base Average Pressure",
        "Base Average Pressure",
        'View "Bearing Pressure (p = N / A) User Guide"',
        "Vertical force (kN)",
        "Base area (m²)",
        "p = N/A; with N in kN and A in m², p is in kPa.",
        "📚 In-Depth: Bearing Stress",
        "Average bearing pressure under column bases and support pads.",
        "Estimate of contact pressure between the base and the ground.",
        "Back-calculation of the support bearing area.",
        "Column base 100 kN / 10 m²",
        "Support pad",
        "Bearing and",
        "soil bearing capacity",
        "p must be below the allowable bearing value of the soil or pad material, otherwise increase the area.",
        "What to watch in local bearing?",
        "Local bearing has a strength-increase factor and must be checked separately per code.",
    ]))
    write('cantilever-end-moment', build('cantilever-end-moment', [
        "End Moment (M = F·L)",
        "A concentrated load at the free end of a cantilever produces the maximum moment at the fixed end.",
        "Cantilever End-Moment Calculator",
        "/ Cantilever End Moment",
        "Cantilever End Moment",
        'View "End Moment (M = F·L) User Guide"',
        "End force (kN)",
        "Cantilever length (m)",
        "M = F·L (cantilever fixed end).",
        "5 kN, 2 m cantilever → 10 kN·m.",
        "📚 In-Depth: Cantilever End Point-Load Fixed-End Moment",
        "Fixed-end moment of a cantilever under a free-end concentrated load.",
        "Moment design at the root of balconies and overhangs.",
        "Force check at the root of canopies and sign brackets.",
        "End 5 kN / length 2 m",
        "F=5 kN, L=2 m: fixed-end moment M=F·L=5×2=10 kN·m.",
        "Length effect",
        "L from 2 to 3 m: M=5×3=15 kN·m, increasing linearly.",
        "Where is the maximum moment?",
        "Maximum at the fixed end, decreasing linearly to zero at the free end.",
        "What about a uniform load?",
        "With uniform load w the fixed-end moment is M=wL²/2; use the corresponding uniform-load formula.",
    ]))
    write('deflection-cantilever-point', build('deflection-cantilever-point', [
        "Cantilever Deflection from End Point Load",
        "Enter end force F, length L, elastic modulus E and circular-section diameter d to find the deflection.",
        "Cantilever End-Load Deflection Calculator",
        "/ Cantilever End-Load Deflection Calculator",
        'View "Cantilever Deflection from End Point Load User Guide"',
        "δ = FL³/(3EI) (free end). Example → about 0.272 mm.",
        "End force F (N)",
        "δ = FL³/(3EI) (free end).",
        "Example → about 0.272 mm.",
        "📚 In-Depth: Cantilever End Point-Load Deflection",
        "Elastic deflection of a cantilever's free end under a concentrated load.",
        "Deflection-limit check at the end of equipment supports.",
        "Material selection and section optimization (deflection-sensitive cases).",
        "Steel round bar d=100 mm",
        "Doubling the diameter",
        "d 0.1→0.2: I grows 16×, δ drops to about 0.017 mm.",
        "Relationship between deflection and stiffness?",
        "δ is inversely proportional to EI, where EI is the flexural rigidity,",
        "section moment of inertia",
        "I has the most significant effect (fourth power).",
        "Difference between uniform and point load?",
        "The uniform-load end deflection is wL⁴/(8EI), about 5/8 of the same total point load.",
    ]))

if __name__ == "__main__":
    main()

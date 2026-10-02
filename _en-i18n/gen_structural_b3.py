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
    write('deflection-cantilever-udl', build('deflection-cantilever-udl', [
        "Cantilever Free-End Deflection from Uniform Load",
        "Enter uniform load w, length L, elastic modulus E and circular-section diameter d to find the deflection.",
        "Cantilever Uniform-Load Deflection Calculator",
        "/ Cantilever Uniform-Load Deflection Calculator",
        'View "Cantilever Free-End Deflection from Uniform Load User Guide"',
        "δ = wL⁴/(8EI) (free end). Example → about 2.04 mm.",
        "Uniform load w (N/m)",
        "δ = wL⁴/(8EI) (free end).",
        "Example → about 2.04 mm.",
        "📚 In-Depth: Cantilever Uniform-Load Deflection",
        "End deflection of a cantilever under a uniform load (e.g. self-weight, snow load).",
        "Deflection check of overhangs and cantilever slabs.",
        "Comparison with the point-load case.",
        "Uniform 1000 N/m / length 2 m",
        "Doubling the span",
        "L 2→4: δ grows 16× (L⁴) ≈ 32.6 mm.",
        "Why is it length-sensitive?",
        "Cantilever end deflection is proportional to L⁴; doubling the length increases deflection about 16×.",
        "Compared with a simply supported beam?",
        "Under the same span and load, the cantilever end deflection is clearly larger than the simply supported mid-span deflection.",
    ]))
    write('euler-buckling', build('euler-buckling', [
        "Euler Critical Load (P_cr = π²·E·I / L²)",
        "Buckling critical load of a slender column pinned at both ends.",
        "Column Euler Critical-Load Calculator",
        "/ Euler Critical Load",
        "Euler Critical Load",
        'View "Euler Critical Load (P_cr = π²·E·I / L²) User Guide"',
        "P_cr = π²EI/L² (both ends pinned). 200 GPa steel, I=1e-6, L=2 m → about 493 kN.",
        "Section moment of inertia (m⁴)",
        "P_cr = π²EI/L² (both ends pinned).",
        "200 GPa steel, I=1e-6, L=2 m → about 493 kN.",
        "📚 In-Depth: Euler Critical Load",
        "Buckling critical load of an axially compressed slender column.",
        "Stability design of pin-ended columns.",
        "When the slenderness ratio is too large, buckling rather than strength governs.",
        "Steel column E=200 GPa, I=1e-6, L=2 m",
        "Both ends pinned K=1: Pcr=π²EI/L²=π²×200e9×1e-6/4≈4.93×10⁵ N=493.5 kN.",
        "One end fixed, one end free",
        "Effective-length factor 2: L_e=4 m, Pcr drops to about 1/4 = 123 kN.",
        "How are boundary conditions reflected?",
        "Use the effective-length factor K as L_e=KL; both ends pinned K=1, both ends fixed K=0.5.",
        "Applicability?",
        "Applies to elastic buckling of high-slenderness columns; short stocky columns enter inelastic or strength failure.",
    ]))
    write('hoop-stress', build('hoop-stress', [
        "Hoop (Circumferential) Stress from Internal Pressure",
        "Enter internal pressure p, radius r and wall thickness t to find the hoop stress.",
        "Thin-Walled Cylinder Hoop-Stress Calculator",
        "/ Thin-Walled Cylinder Hoop-Stress Calculator",
        'View "Hoop (Circumferential) Stress from Internal Pressure User Guide"',
        "Thin-wall assumption t/r < 0.1.",
        "📚 In-Depth: Cylinder Hoop Stress",
        "Hoop stress of a thin-walled cylinder (pipe, vessel) under internal pressure.",
        "Pressure-vessel wall thickness",
        "preliminary design.",
        "Combined assessment with longitudinal stress.",
        "Internal pressure 2 MPa, radius 0.5 m",
        "Doubling the wall thickness",
        "t 0.01→0.02: σh halves to 50 MPa.",
        "Which is larger, hoop or longitudinal?",
        "Hoop stress is twice the longitudinal; the cylinder hoop (circumferential weld) is more critical.",
        "Thin-wall condition?",
        "Generally r/t>10 uses the thin-wall formula; thick walls require the Lamé formula.",
    ]))
    write('longitudinal-stress', build('longitudinal-stress', [
        "Longitudinal Stress from Internal Pressure",
        "Enter internal pressure p, radius r and wall thickness t to find the longitudinal stress.",
        "Thin-Walled Cylinder Longitudinal-Stress Calculator",
        "/ Thin-Walled Cylinder Longitudinal-Stress Calculator",
        'View "Longitudinal Stress from Internal Pressure User Guide"',
        "σ_l = σ_h/2. Same example → 50 MPa.",
        "Same example → 50 MPa.",
        "📚 In-Depth: Cylinder Longitudinal Stress",
        "Axial (longitudinal) stress of a thin-walled cylinder caused by internal pressure.",
        "Strength assessment of head-to-shell joints.",
        "Comparative design with hoop stress.",
        "Same cylinder as before",
        "Compared with hoop",
        "σl=50 MPa is exactly half of the hoop stress 100 MPa.",
        "Why is it half the hoop?",
        "Longitudinal is balanced by the head over the full section, while hoop is balanced by the side tensions per unit length; geometrically the difference is a factor of 2.",
        "Are there other axial forces?",
        "If axial load or temperature difference exists, it must be combined with the internal-pressure longitudinal stress.",
    ]))

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'engineering')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'engineering')
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
    out = {'slug': slug, 'industry': 'engineering', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
#!/usr/bin/env python3
def main():
    write('thermal-expansion', build('thermal-expansion', [
"🏋️ Linear Expansion Calculator (Engineering)",
"Compute the elongation of a member from the linear expansion coefficient, original length and temperature difference.",
"Linear Expansion Calculator",
"📖 Read the Linear Expansion Calculator (Engineering) guide",
"Thermal expansion elongation: ΔL = α · L₀ · ΔT; α is the linear expansion coefficient, L₀ the original length and ΔT the temperature difference.",
"Original length L₀ (m)",
"Steel α ≈ 12×10⁻⁶/°C, concrete ≈ 10×10⁻⁶/°C, aluminium ≈ 23×10⁻⁶/°C",
"Heating gives a positive value (elongation), cooling a negative one (shortening)",
"📚 In-depth analysis: linear expansion calculation (engineering)",
"A steam pipe elongates as it heats up, so fit a Π-type or bellows compensator to absorb ΔL.",
"Railway rails leave expansion gaps to prevent buckling at high temperatures.",
"Composite materials develop thermal stress between layers because α differs.",
"Thermal elongation of a steel pipe",
"For a steel pipe L=100 m, ΔT=80 °C, α=12×10⁻⁶/°C. ΔL=12×10⁻⁶×100×10³×80=96 mm, which a compensator must absorb.",
"What is the relation between linear and volumetric expansion?",
"The volumetric expansion coefficient≈3α (isotropic); restrained expansion generates thermal stress σ=E·α·ΔT.",
"What is the typical magnitude of α?",
"Steel 11–13×10⁻⁶, aluminium 23×10⁻⁶, copper 17×10⁻⁶,",
    ]))

    write('heat-transfer', build('heat-transfer', [
"🌡️ Heat Transfer Calculator",
"Conduction / convection / radiation heat transfer",
"Core formulas (by input variable): eps × sigma × A × ((T1)^4 - (T2)^4); 1÷(h1×A) + L÷(k×A) + 1÷(h2×A); 5.67e-8",
"📖 Read the Heat Transfer Calculator guide",
"📚 In-depth analysis: heat transfer calculation",
"For wall insulation, find the heat flux q=ΔT/Σ(δ/λ) from the conductivity λ.",
"For a heat exchanger, use the overall heat transfer coefficient U and",
"to compute the heat transferred.",
"An external insulation layer on a pipe reduces heat loss.",
"Heat conduction through a brick wall",
"Brick wall δ=240 mm, λ=0.8 W/(m·K), area 10 m², ΔT=20 °C. q=20/0.24=83.3 W/m²; Q=833 W.",
"What is the typical magnitude of λ?",
"Steel 45,",
"1.5, brick 0.8, rock wool 0.04, air 0.026 W/(m·K); insulation relies on low-λ materials.",
"What is the difference between convection and conduction?",
"Conduction occurs inside solids (k), while convection occurs at fluid boundaries (h, strongly affected by flow velocity); the overall coefficient U combines both with the wall resistance.",
"About the Heat Transfer Calculator",
"The heat transfer calculator is an online tool in the field of engineering calculation. An engineering calculation tool using standard engineering formulas for precise, reliable results.",
    ]))

    write('axial-stress', build('axial-stress', [
"⚙️ Axial Tension and Compression Stress and Strain Calculator (Engineering)",
"Compute normal stress, linear strain and axial deformation from the axial load and cross-sectional area.",
"Axial Tension and Compression Stress and Strain Calculator",
"📖 Read the Axial Tension and Compression Stress and Strain Calculator (Engineering) guide",
"Axial tension/compression: normal stress σ = F ÷ A, strain ε = σ ÷ E = F ÷ (A·E), and elongation ΔL = ε·L = F·L ÷ (A·E); F is the axial force, A the cross-sectional area, E the elastic modulus and L the original length.",
"Stress σ = F / A",
"Strain ε = σ / E (Hooke's law)",
"Deformation ΔL = ε · L",
"📚 In-depth analysis: axial tension and compression stress and strain calculation (engineering)",
"For a round steel tension rod, find σ from d and compare it with Q235 [σ]=140 MPa.",
"A column under compression needs slenderness ratio λ and stability coefficient φ checked in addition to strength.",
"For a hydraulic piston rod, check the diameter against the thrust.",
"Strength check of a round tension rod",
"Round rod d=20 mm in tension with F=30 kN. A=π×20²/4=314 mm²; σ=30000/314=95.5 MPa < 140 MPa, so it is satisfied.",
"What is the difference between strength and stability?",
"Short thick members are governed by strength σ≤[σ]; slender compression members buckle first and need λ=l/i with stability coefficient φ checked against N≤φ·A·[σ].",
"What safety factor should be taken?",
"Steel under static load 1.5–2, dynamic or alternating load 2–4, and brittle materials higher.",
    ]))

    write('bending-stress', build('bending-stress', [
"🧮 Maximum Bending Stress of a Beam Calculator (Engineering)",
"Compute the maximum bending normal stress of a beam from the bending moment and section modulus.",
"Maximum Bending Stress of a Beam Calculator",
"📖 Read the Maximum Bending Stress of a Beam Calculator (Engineering) guide",
"Beam bending: maximum bending normal stress σ_max = M ÷ W, and the section modulus of a rectangular section W = b·h² ÷ 6; M is the bending moment, b the section width and h the section depth.",
"W = bh²/6 (rectangular section)",
"Tensile stress acts on the tension edge and compressive stress on the compression edge",
"📚 In-depth analysis: maximum bending stress of a beam calculation (engineering)",
"A simply supported beam under uniform load has midspan maximum moment M=ql²/8; check whether the rectangular section modulus W=bh²/6 satisfies [σ].",
"A cantilever beam with an end force has fixed-end moment M=FL; select the model from the I-section modulus.",
"A shaft-like part under transverse bending is combined with torsion for a combined strength check.",
"Bending check of a rectangular timber beam",
"Rectangular timber beam b=100 mm, h=200 mm, midspan moment M=4 kN·m. W=bh²/6=100×200²/6=6.67×10⁵ mm³; σ=M/W=4×10⁶/6.67×10⁵=6.0 MPa; pine along the grain [σ]=8–10 MPa, so it is satisfied.",
"What is the relation between section modulus W and moment of inertia I?",
"W=I/y_max, where y_max is the distance from the farthest fibre to the neutral axis; for a rectangle W=bh²/6, for a circle W=πd³/32, and for an I-section look it up in the section tables.",
"How are tensile and compressive stress distributed?",
"One side of the neutral axis is in tension and the other in compression; for a symmetric section the absolute values match and the critical point is the outermost fibre, while an asymmetric section needs the two sides computed separately.",
    ]))


if __name__ == '__main__':
    main()
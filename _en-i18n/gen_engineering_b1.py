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
    write('index', build('index', [
"⚙️ Engineering Calculation Tools",
"Engineering Calculation",
"Engineering Calculation Tools",
"Linear Expansion Calculator",
"Linear expansion calculator. Enter the material's linear expansion coefficient, original length and temperature difference, and use ΔL = α·L₀·ΔT to find the length change caused by thermal expansion or contraction, for expansion compensation design of pipes, rails and precision structures.",
"Axial Tension and Compression Stress and Strain Calculator",
"Axial tension and compression stress and strain calculator. Enter axial force, cross-sectional area and elastic modulus, and compute σ = F/A and ε = σ/E for the axial stress and strain of a member, suitable for strength checks of structural components.",
"Maximum Bending Stress of a Beam Calculator",
"Maximum bending stress calculator for beams. Enter bending moment, section modulus and other parameters, and use σ = M/W to obtain the maximum bending normal stress of the beam section, for strength verification and material selection of beams under bending.",
"Poisson Ratio Transverse Strain Calculator",
"Poisson ratio transverse strain calculator. Enter axial strain and Poisson's ratio to compute the transverse strain under tension or compression (ε_t = −ν·ε_a), used for material deformation analysis and checking isotropic elastic behaviour.",
"Bolt Preload Calculator",
"Bolt preload calculator. Enter bolt size, friction coefficient and target clamping force to compute the required tightening torque and preload, suitable for tightening process design of flanges and joints.",
"Circular Shaft Torsional Shear Stress Calculator",
"Circular shaft torsional shear stress calculator. Enter torque, shaft radius and polar moment of inertia, and use τ = T·r/J to obtain the maximum torsional shear stress of a circular shaft, for drive shaft strength checks and diameter selection.",
"Section Moment of Inertia Calculator",
"Section moment of inertia calculator. Enter the dimensions of common sections (rectangular, circular, I-shaped and more) to compute the moment of inertia I about the neutral axis, giving the section stiffness parameter needed for beam bending and column stability analysis.",
"Thin-Walled Cylinder Vessel Wall Thickness Calculator",
"Thin-walled cylinder vessel wall thickness calculator. Enter internal pressure, radius, allowable stress and weld joint efficiency, and use the thin-wall formula to find the required wall thickness, for pressure vessel design and strength checks in line with engineering codes.",
"Fillet Weld Strength Calculator",
"Fillet weld strength calculator. Enter leg size, weld length and allowable steel stress to obtain the shear capacity and strength from the effective throat area of the fillet weld, for steel structure welded joint design and verification.",
"Beam Deflection Calculator",
"Simply supported beam deflection calculator. Choose a load case, enter span, section moment of inertia, elastic modulus and load, then obtain the maximum deflection, compare it with the allowable deflection and judge whether the stiffness requirement is met, for beam member design.",
"Stress Calculator",
"General stress calculator supporting tension/compression, shear, torsional and bending stress. Enter loads and geometric parameters to get stress results instantly, a common tool for strength analysis of mechanical and structural components.",
"Material Calculator",
"Material section calculator. Enter section dimensions and density to compute cross-sectional area, moment of inertia and weight, suitable for estimating mechanical parameters and selecting structural materials such as sections and plate.",
"Heat Transfer Calculator",
"Heat transfer calculator supporting conduction, convection and radiation. Enter material, temperature difference and geometric parameters to compute heat transfer power, suitable for equipment cooling, insulation design and thermodynamics teaching.",
"Cantilever Beam End Deflection Under Concentrated Load",
"Cantilever beam end deflection calculator under concentrated load. Enter beam length, elastic modulus, moment of inertia and end load, and use the cantilever formula to find the maximum end deflection, for cantilever stiffness checks and deformation prediction.",
"About the Engineering Calculation Tools",
"The engineering calculation tool collection brings together 14 free online tools covering the common calculation, conversion and lookup needs in engineering calculation scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you will find ready-to-use utilities here. Every tool runs entirely in the browser, uploads no data to a server, and keeps your privacy secure.",
"The engineering calculation tools collected on this page include (some representative tools):",
"These tools help you finish common engineering calculation tasks quickly, with no need to memorize complex formulas or do manual conversions, just enter and get the result.",
"Do the Engineering Calculation Tools need a download or registration?",
"No. All engineering calculation tools on this page are pure front-end online tools: open the page and use them directly, with no software to install, no account to register, and no data uploaded.",
"Are the Engineering Calculation Tools results accurate? Is my data safe?",
"The tools compute locally in your browser from public mathematical formulas and general industry standards, so results are available instantly. All computation happens on your own device, data is never uploaded to a server, and your privacy is protected.",
    ]))

    write('poisson-strain', build('poisson-strain', [
"🧮 Poisson Ratio Transverse Strain Calculator (Engineering)",
"Compute the transverse strain from the axial strain and Poisson's ratio.",
"Poisson Ratio Transverse Strain Calculator",
"📖 Read the Poisson Ratio Transverse Strain Calculator (Engineering) guide",
"Poisson effect: axial strain ε_x = ΔL ÷ L; transverse strain ε_y = −ν·ε_x, where ν is Poisson's ratio (about 0.3 for metals, about 0.5 for rubber); volumetric strain ε_v = ε_x(1 − 2ν); when ν = 0.5 the volume is unchanged.",
"Axial strain ε_x",
"ε_y = −ν·ε_x (transverse and axial act in opposite directions)",
"Steel ν≈0.3, concrete ν≈0.2, rubber ν≈0.5",
"Poisson's ratio is an inherent elastic constant of the material",
"📚 In-depth analysis: Poisson ratio transverse strain calculation (engineering)",
"A tension rod under tension, given the",
"axial strain",
", estimates the diameter reduction (such as wire rope, or bolt diameter shrinkage after preloading).",
"Rubber with ν≈0.49 is nearly incompressible, so the predicted volume change is extremely small.",
"Anisotropic composites need ν_xy and ν_yx taken along the principal directions.",
"Transverse contraction of a steel rod",
"For a steel rod with ν=0.3 and axial tensile strain ε=0.001, the transverse strain ε_lat=−0.3×0.001=−0.0003, and a 20 mm diameter shrinks by 0.006 mm.",
"Poisson's ratio",
"Can it exceed 0.5?",
"For isotropic linear elasticity it is below 0.5, and 0.5 means incompressible in volume (rubber); a negative Poisson's ratio (auxetic materials) belongs to special engineered materials.",
"Volumetric strain",
"How is it computed?",
"ε_v=ε_x+ε_y+ε_z=(1−2ν)·ε_axial; at ν=0.5 the volume is unchanged.",
    ]))

    write('weld-strength', build('weld-strength', [
"⚙️ Fillet Weld Strength Calculator (Engineering)",
"Compute the average shear stress of a fillet weld from the weld dimensions and the applied force.",
"Fillet Weld Strength Calculator",
"📖 Read the Fillet Weld Strength Calculator (Engineering) guide",
"Effective throat area of a fillet weld A_e = 0.7 · h_f · l_w, and the weld stress τ = F ÷ A_e; F is the applied force, h_f the leg size and l_w the effective weld length.",
"Applied force F (kN)",
"Leg size h_f (mm)",
"Effective weld length l_w (mm)",
"A_e = 0.7·h_f·l_w (effective section of a fillet weld)",
"τ = F / A_e, which must not exceed the design strength of the fillet weld",
"l_w should deduct the start/stop arc defects (usually 2h_f)",
"📚 In-depth analysis: fillet weld strength calculation (engineering)",
"For a fillet weld between an angle and a plate, find the required leg size a from the applied force.",
"For a lap joint welded on both sides, L is the sum of the effective lengths on both sides.",
"Dynamic or fatigue service requires reducing",
"or increasing the leg size.",
"Shear check of a fillet weld",
"A fillet weld carries F=50 kN with leg a=6 mm and total length L=200 mm on both sides. τ=50000/(0.707×6×200)=58.9 MPa, well below [τ]=120–140 MPa for an E43 electrode, so it is safe.",
"Why multiply by 0.707?",
"The critical section of a fillet weld is the 45° throat, so throat thickness=0.707a and effective area=0.707a·L.",
"What is the relation between leg size and plate thickness?",
"Generally a≈0.7t (thin plate) to t (thick plate), with a maximum of 1.2t; too thick risks cracking, too small gives insufficient strength.",
    ]))

    write('section-inertia', build('section-inertia', [
"📐 Section Moment of Inertia Calculator (Engineering)",
"Compute the moment of inertia I about the neutral axis and the section modulus W for rectangular or circular sections.",
"Section Moment of Inertia Calculator",
"📖 Read the Section Moment of Inertia Calculator (Engineering) guide",
"Section moment of inertia: rectangular I = b·h³ ÷ 12; circular I = π·D⁴ ÷ 64; b is the section width, h the section depth and D the diameter.",
"Shape (1 = rectangular, 2 = circular)",
"Rectangular width b (mm)",
"Rectangular depth h / circular diameter D (mm)",
"Rectangular: I = bh³/12, W = I / (h/2)",
"Circular: I = πD⁴/64, W = I / (D/2)",
"The moment of inertia is the core parameter of bending stiffness EI",
"📚 In-depth analysis: section moment of inertia calculation (engineering)",
"For a rectangular section I=bh³/12, compute the beam bending stiffness EI for the deflection formula.",
"For a composite section (T-shaped, box-shaped) use the parallel-axis theorem to get the overall moment of inertia.",
"For a circular section I=πd⁴/64, used to check bending about the axis.",
"Rectangular section moments of inertia about both axes",
"For a rectangular section b=50 mm, h=120 mm: about the strong axis I=bh³/12=50×120³/12=7.2×10⁶ mm⁴; about the weak axis I=hb³/12=120×50³/12=1.25×10⁶ mm⁴.",
"What are the strong and weak axes?",
"The axis with the larger moment of inertia is the strong axis (bending-wise strong) and the smaller one the weak axis; for a rolled section the strong axis should face the direction of the larger bending moment.",
"When is the parallel-axis theorem used?",
"When finding the moment of inertia about a non-centroidal axis, I=Ic+A·d², where d is the distance between the two axes; for a composite section first find Ic of each part about its own centroid, then translate and sum.",
    ]))

    write('shaft-torsion', build('shaft-torsion', [
"🧮 Circular Shaft Torsional Shear Stress Calculator (Engineering)",
"Compute the maximum shear stress and angle of twist per unit length of a circular shaft under torsion.",
"Circular Shaft Torsional Shear Stress Calculator",
"📖 Read the Circular Shaft Torsional Shear Stress Calculator (Engineering) guide",
"Circular shaft torsion: angle of twist θ = T·L ÷ (G·J), polar moment of inertia J = π·d⁴ ÷ 32; T is torque, L the shaft length, G the shear modulus and d the shaft diameter.",
"Torque T (kN·m)",
"Shaft length L (m)",
"Polar moment of inertia J = πd⁴/32",
"Maximum shear stress τ_max = T·r / J (r = d/2)",
"Angle of twist θ = T·L / (G·J)",
"📚 In-depth analysis: circular shaft torsional shear stress calculation (engineering)",
"Estimate the working torque of a motor output shaft from its rated power and speed, then check whether the shaft diameter meets the allowable shear stress [τ]=30–40 MPa of 45 steel.",
"At equal mass a hollow shaft is stiffer than a solid one; verify the polar moment of inertia Jp=π(D⁴−d⁴)/32 and the shear stress distribution using the inner-to-outer diameter ratio.",
"A low-speed shaft of a gearbox carries high torque; back-calculate the diameter with T=9549·P/n and allow a safety margin (usually n=1.5–2.5).",
"Check of a solid shaft for a 7.5 kW motor",
"Shaft of a 7.5 kW, 1450 r/min motor, solid shaft diameter d=25 mm, 45 steel [τ]=35 MPa. T=9549×7.5/1450=49.4 N·m; Jp=π·25⁴/32=3.835×10⁴ mm⁴; r=12.5 mm; τ=T·r/Jp=49.4×10³×12.5/3.835×10⁴=16.1 MPa < 35 MPa, so it is safe.",
"How do you choose between a solid and a hollow shaft?",
"At equal mass a hollow shaft has a larger torsional moment of inertia and higher stiffness, which suits weight-sensitive cases (aerospace, automotive drivelines); but a hollow shaft costs more to make and needs buckling protection, so ordinary machinery prefers solid shafts.",
"What allowable shear stress should be taken?",
"Quenched and tempered 45 steel is about 30–40 MPa, Q235 about 20–25 MPa, and alloy steel can reach 50–80 MPa; choose with the heat treatment and a service safety factor in mind.",
    ]))


if __name__ == '__main__':
    main()
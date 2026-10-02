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
    write('pressure-vessel', build('pressure-vessel', [
"🖥️ Thin-Walled Cylinder Vessel Wall Thickness Calculator (Engineering)",
"Compute the required wall thickness from the internal pressure using the thin-walled cylinder hoop stress formula.",
"Thin-Walled Cylinder Vessel Wall Thickness Calculator",
"📖 Read the Thin-Walled Cylinder Vessel Wall Thickness Calculator (Engineering) guide",
"Wall thickness of a thin-walled pressure vessel shell: t = P·D ÷ (2·[σ]·φ); P is the design internal pressure, D the vessel inner diameter, [σ] the allowable stress and φ the weld joint efficiency.",
"Design internal pressure P (MPa)",
"Vessel inner diameter D (mm)",
"t = P·D / (2[σ]·φ) (governed by hoop stress)",
"Suitable for thin-walled cylinders with D/t ≥ 20",
"Practical design should also check axial stress and stability",
"📚 In-depth analysis: thin-walled cylinder vessel wall thickness calculation (engineering)",
"For a cylindrical storage tank, find the required wall thickness t from design pressure p and diameter d.",
"For a gas cylinder (spherical shell), find the thickness from p; a spherical shell has equal stress in both directions and so saves material.",
"Pipe hoop stress governs, so welds require 100% inspection.",
"Cylindrical storage tank wall thickness",
"For a cylinder with p=1 MPa, d=1000 mm, [σ]=140 MPa and weld efficiency φ=0.85: t=pd/(2[σ]φ)=1×1000/(2×140×0.85)=4.2 mm (then add the corrosion allowance).",
"Why is the hoop stress twice the axial stress?",
"Hoop stress σθ=pd/2t balances the radial component of internal pressure, while axial σa=pd/4t is carried only through the end closures, so the hoop direction is more critical and needs focused control.",
"What about thick-walled vessels?",
"When t/d>0.1 use the Lamé formula σθ=r_i²·p/(r_o²−r_i²)·(r_o²/r²+1), where the inner wall stress is largest.",
    ]))

    write('cantilever-deflection', build('cantilever-deflection', [
"⚖️ Cantilever Beam End Deflection Under Concentrated Load (Engineering)",
"Compute the end deflection and free-end rotation of a cantilever beam carrying a concentrated force at the free end.",
"Cantilever Beam End Deflection Under Concentrated Load",
"📖 Read the Cantilever Beam End Deflection Under Concentrated Load (Engineering) guide",
"Cantilever beam end deflection under concentrated load: δ = P·L³ ÷ (3·E·I); P is the end load, L the beam length, E the elastic modulus and I the section moment of inertia.",
"End load P (kN)",
"Moment of inertia I (cm⁴)",
"End deflection δ = P·L³ / (3EI)",
"Free-end rotation θ = P·L² / (2EI)",
"Units must be unified to N and m",
"📚 In-depth analysis: cantilever beam end deflection under concentrated load (engineering)",
"For a cantilever rack beam loaded at the end, check whether the free-end droop meets [L/200].",
"For a canopy cantilever slab under uniform snow load, find the maximum deflection to prevent ponding.",
"For an end moment on a cantilever beam (such as a sign bracket), compute it from the M load case.",
"Concentrated end force on a steel cantilever beam",
"Cantilever beam L=2 m, EI=2×10¹¹ N·mm², end force P=1 kN. δ=PL³/(3EI)=1000×2000³/(3×2×10¹¹)=13.3 mm.",
"How much larger is cantilever deflection than simply supported?",
"With the same P, L and EI, the cantilever end deflection is about 4 times that of a simply supported beam at midspan; a cantilever is more flexible, so the design is more conservative.",
"What allowable deflection should be taken?",
"Roof and suspended ceiling [L/200]~[L/250]; precision equipment supports [L/500] or tighter.",
    ]))

    write('beam-calculator', build('beam-calculator', [
"🧮 Beam Deflection Calculator",
"Compute the maximum deflection of a simply supported beam",
"Core formulas (by input variable): 5 × q_Nmm × (L_mm)^4 ÷ (384 × E_Nmm × I_mm4); q_Nmm × (L_mm)^4 ÷ (8 × E_Nmm × I_mm4); P_N × (L_mm)^3 ÷ (48 × E_Nmm × I_mm4)",
"/ Beam Deflection",
"📖 Read the Beam Deflection Calculator guide",
"Load case",
"Uniformly distributed load q (kN/m)",
"Allowable deflection (L/x)",
"📚 In-depth analysis: beam deflection calculation",
"A simply supported beam with uniform load and a suspended ceiling, checking midspan deflection [L/250].",
"A cantilever canopy piled with load at the end, computing free-end deflection with the cantilever case.",
"Allow a safety margin in the equipment foundation beam under dynamic loading.",
"Uniform load deflection of a simply supported beam",
"Simply supported beam L=5 m, q=10 kN/m, E=200 GPa, I=500 cm⁴=5×10⁶ mm⁴. δ=5qL⁴/(384EI)≈16.3 mm; allowable L/250=20 mm, so it is satisfied.",
"How is the allowable deflection chosen?",
"Roof and suspended ceiling [L/200]~[L/250], floor [L/300]~[L/400], crane beam [L/600]~[L/750].",
"How do you unify the units of E and I?",
"Unify to N and mm: E(GPa)×1000=N/mm², I(cm⁴)×10⁴=mm⁴, giving δ in mm.",
"About the Beam Deflection Calculator",
"The beam deflection calculator is an online tool in the field of engineering calculation. An engineering calculation tool using standard engineering formulas for precise, reliable results.",
    ]))

    write('stress-calculator', build('stress-calculator', [
"⚙️ Stress Calculator",
"Tension/compression, shear, torsion and bending stress",
"Core formulas (by input variable): min(100, ratio × 100); π × ((D)^4 - (d)^4) ÷ 32; stress ÷ mat.E ÷ 1000",
"📖 Read the Stress Calculator guide",
"Stress type",
"📚 In-depth analysis: stress calculation",
"Distribute the forces at a multi-member truss node to each member to check σ.",
"For a tubular column under compression, use the net cross-sectional area to find the average stress.",
"For a composite section, find the eccentric stress about the centroidal axis.",
"Square section tension rod",
"A square 30×30 mm section in tension with F=50 kN. A=900 mm²; σ=55.6 MPa, below Q235 [σ]=140 MPa.",
"Average stress versus maximum stress?",
"For a uniform section it is the average stress; at holes and notches,",
"stress concentration",
"gives an actual peak of Kt·σ_avg (Kt is the stress concentration factor).",
"When should stability be considered?",
"When in compression with slenderness ratio λ>λp, stability governs; see the stability check in the axial stress tool.",
"About the Stress Calculator",
"The stress calculator is an online tool in the field of engineering calculation. An engineering calculation tool using standard engineering formulas for precise, reliable results.",
    ]))

    write('material-calculator', build('material-calculator', [
"🧮 Material Section Calculator",
"Compute cross-sectional area, moment of inertia and weight",
"Core formulas (by input variable): (a×a×a×a - inner×inner×inner×inner) ÷ 12; (b × (h)^3 - (b - d) × (h - 2×t)^3) ÷ 12; (b×(t)^3 + c×(t)^3 - (t)^4) ÷ 3",
"Material Calculator",
"/ Material Section",
"📖 Read the Material Section Calculator guide",
"Section shape",
"📚 In-depth analysis: material section calculation",
"For round bar cut lengths, use A=πd²/4 with a density of 7.85 g/cm³ to estimate unit weight.",
"For a square tube (outer minus inner), find the net cross-sectional area and weight per metre.",
"Cross-check rolled section theoretical weight against a table.",
"Unit weight of round bar",
"Round bar d=20 mm, L=6 m, ρ=7.85 g/cm³. A=π×2²/4=3.14 cm²; V=3.14×600=1884 cm³; m=14.8 kg.",
"What are the common material densities?",
"Steel 7.85, aluminium 2.7, copper 8.9, cast iron 7.2, PVC 1.4 g/cm³.",
"Why does theoretical weight differ from the real value?",
"The gap comes from dimensional tolerances and negative tolerance; rolled sections are priced by standard theoretical weight, so add 3%–5% cutting allowance.",
"About the Material Calculator",
"The material calculator is an online tool in the field of engineering calculation. An engineering calculation tool using standard engineering formulas for precise, reliable results.",
    ]))

    write('bolt-preload', build('bolt-preload', [
"⚙️ Bolt Preload Calculator (Engineering)",
"Estimate the axial bolt preload from the tightening torque and the torque coefficient.",
"Bolt Preload Calculator",
"📖 Read the Bolt Preload Calculator (Engineering) guide",
"Bolt preload: F = T ÷ (K · d), where T is the tightening torque (N·m), K the torque coefficient (about 0.2) and d the nominal thread diameter (m); preload is commonly taken as 60% to 70% of the yield load.",
"Tightening torque T (N·m)",
"F = T / (K · d), with d the nominal diameter (m)",
"The torque coefficient K is usually 0.1~0.25 (take the lower value when lubricated)",
"Real preload is affected by friction, so verify it with the tension method",
"📚 In-depth analysis: bolt preload calculation (engineering)",
"For a flanged connection, fix the preload from the sealing requirement and back-calculate the wrench torque.",
"For anchor bolts that must resist loosening, control the tightening torque with K and d.",
"A friction-type high-strength bolt connection relies on the preload to provide slip resistance.",
"Torque for an M16 bolt",
"Preload F=40 kN for an M16 bolt (d=16 mm) with K=0.2. T=0.2×40000×0.016=128 N·m.",
"What affects the torque coefficient K?",
"It is mainly set by the friction coefficient of the thread and the bearing face, from 0.1 (oiled) to 0.25 (rusted); the spread within one batch is large, so critical connections use torque plus angle or hydraulic tension control.",
"What happens if the preload is too large?",
"Exceeding the yield strength causes plastic elongation and bolt failure; a preload of 0.6–0.7 times the yield strength is common.",
    ]))


if __name__ == '__main__':
    main()
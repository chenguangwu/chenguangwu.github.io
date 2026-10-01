#!/usr/bin/env python3
# machinery batch3 (5 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'machinery')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'machinery')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'calc-strength': [
"😴 Shaft Strength / Stiffness / Fatigue Calculator",
"Compute the stress and safety factor of a solid circular shaft using the fourth strength theory",
'📖 View the "Shaft Strength / Stiffness / Fatigue Calculator Guide"',
"Shaft strength σ = M/W",
"45 steel (σb=600, σs=355)",
"40Cr quenched and tempered (σb=980, σs=785)",
"20CrMnTi carburised (σb=1080, σs=835)",
"Yield strength σs (MPa)",
"Bending moment M (N·m)",
"With keyway (stress concentration)",
"Hollow shaft",
"Inner diameter d₀ (mm)",
"💡 Fourth strength theory: σe=√(σ²+3τ²). Bending section modulus W=πd³/32, torsional section modulus Wp=πd³/16. Safety factor n=σs/σe.",
"Safety factor assessment criteria",
"n ≥ 1.5: safe (static strength sufficient)",
"1.2 ≤ n < 1.5: basically safe (general use)",
"1.0 ≤ n < 1.2: marginal (further fatigue checking needed)",
"n < 1.0: unsafe (increase the shaft diameter or change the material)",
"📚 In-Depth Analysis: Shaft Strength (Combined Bending and Torsion)",
"Check the critical section of a rotating shaft using the third strength theory (equivalent stress).",
"Bending stress σ=M/W, torsional shear stress τ=T/Wp, σe=√(σ²+3τ²).",
"Keyway",
"stress concentration",
"causes a correction that reduces the effective diameter.",
"Allowable check",
"Material σb=500 MPa, safety factor 2 → [σe]=250 MPa. In the example above σe=277.5>[σe], so the strength is insufficient and the diameter must be increased or the load reduced.",
"Why use σ²+3τ²?",
"The third strength theory (maximum shear stress) for ductile materials gives the equivalent stress σe=√(σ²+3τ²), conservative and commonly used in engineering.",
"Why does a keyway reduce the effective diameter?",
"A keyway produces stress concentration and weakens the section; empirically the effective diameter dEff≈d−keyway depth effect, and fatigue design requires the stress-concentration factor.",
"How to use the Shaft Strength / Stiffness / Fatigue Calculator",
"What does the Shaft Strength / Stiffness / Fatigue Calculator do?",
"Enter the circular shaft diameter, loads and material parameters to compute the combined stress and safety factor of a solid circular shaft using the fourth strength theory, assessing its strength and fatigue reliability under torsion and bending.",
"How do I use the Shaft Strength / Stiffness / Fatigue Calculator?",
"What scenarios suit the Shaft Strength / Stiffness / Fatigue Calculator?",
"Shaft diameter",
"Torque",
"Bending moment",
],
'calc-weld': [
"🧮 Welding Calculator (Fillet / Groove)",
"Strength and allowable-load calculation for fillet welds, butt welds and spot welds",
'📖 View the "Welding Calculator (Fillet / Groove) Guide"',
"Weld strength = leg × length × strength",
"Fillet weld",
"Butt weld (groove)",
"Spot weld",
"Weld leg size K (mm)",
"Weld length L (mm)",
"Applied load F (kN)",
"Material / electrode",
"E43 series (σb=430, matches Q235)",
"E50 series (σb=490, matches Q345)",
"E60 series (σb=590, matches Q390)",
"Weld tensile strength σb (MPa)",
"💡 Fillet weld throat a=0.707K, effective area A=a·L; butt welds are computed by plate thickness. Allowable shear stress [τ]≈0.4σb (AWS D1.1).",
"📚 In-Depth Analysis: Weld Strength Verification",
"Fillet weld τ=F/(0.707·K·L), butt weld σ=F/(t·L) verification.",
"For spot welding the recommended spot diameter d=5√t and spot spacing ≈4d.",
"Check whether the weld leg K is within the reasonable range 0.7t-1.2t.",
"Load F=10 kN, weld leg K=6 mm, weld length L=100 mm: τ=F/(0.707·K·L)=10000/(0.707×6×100)=10000/424.2≈23.6 MPa. Allowable [τ]=120 MPa, satisfied.",
"Spot weld diameter",
"Plate thickness t=2 mm: recommended spot diameter d=5√t=5×1.414≈7.07 mm; spot spacing ≈4d≈28 mm.",
"Where does 0.707 come from?",
"The fillet weld effective throat a=K·sin45°=0.707K, so the shear stress is computed on the throat",
" area calculation",
"Weld leg K too small / too large?",
"K<0.7t gives insufficient load capacity and K>1.2t tends to burn through; conventionally take K≈0.7t-1.0t (upper limit for thin plates).",
"How to use the Welding Calculator (Fillet / Groove)",
"What does the Welding Calculator (Fillet / Groove) do?",
"Enter the weld type (fillet, butt, spot) together with the geometry, weld leg and other parameters to compute the weld load capacity and allowable load, for the strength verification of welded structures.",
"How do I use the Welding Calculator (Fillet / Groove)?",
"What scenarios suit the Welding Calculator (Fillet / Groove)?",
"Plate thickness",
"Weld leg size",
"Weld length",
"Applied load",
],
'drive-2': [
"⚡ Worm Drive Efficiency / Self-Locking Verification",
"Efficiency calculation and self-locking condition check for a worm drive",
'📖 View the "Worm Drive Efficiency / Self-Locking Verification Guide"',
"Worm efficiency η = tanλ/tan(λ+ρ)",
"Number of worm starts z₁",
"Worm wheel teeth z₂",
"Worm diameter quotient q",
"Material pairing",
"Tin bronze worm wheel + steel worm (oil lubricated)",
"Bronze worm wheel + steel worm (grease lubricated)",
"Cast iron worm wheel + steel worm",
"Custom friction coefficient",
"Equivalent friction coefficient μᵥ",
"💡 Efficiency η=tanγ/tan(γ+ρ), where ρ=arctan(μᵥ) is the equivalent friction angle. Self-locking condition: γ ≤ ρ (i.e. η ≤ 0.5).",
"📚 In-Depth Analysis: Worm Gear Drive",
"Find the pitch circles and center distance from the module m, number of starts z1, tooth count z2 and diameter quotient q.",
"Lead pz=π·m·z1 and transmission ratio i=z2/z1.",
"Verify the center distance a=(d1+d2)/2.",
"Single-start worm",
"m=4, q=10, z1=1, z2=40: d1=q·m=40 mm, d2=z2·m=160 mm; center distance a=(40+160)/2=100 mm; lead pz=π·m·z1=π×4×1=12.57 mm; transmission ratio i=40.",
"Double-start",
"z1=2: pz=π×4×2=25.13 mm; i=40/2=20. The more starts, the larger the lead and the higher the efficiency, but the weaker the self-locking.",
"Why are worm drives often self-locking?",
"A single-start worm with a lead angle smaller than the equivalent friction angle is self-locking (only the worm can drive the wheel, not the reverse), used for reversing prevention in hoisting and similar applications.",
"What is the diameter quotient q?",
"q=d1/m characterises the worm's slenderness ratio and affects the stiffness and machining tooling; it is standardised to reduce hobbing-cutter specifications.",
"How to use the Worm Drive Efficiency / Self-Locking Verification",
"What does the Worm Drive Efficiency / Self-Locking Verification do?",
"A worm drive efficiency and self-locking verification tool: it computes the efficiency of a worm gear drive and judges whether the self-locking condition is met, suitable for the safety verification of transmission schemes in reducer and hoisting-equipment design.",
"How do I use the Worm Drive Efficiency / Self-Locking Verification?",
"What scenarios suit the Worm Drive Efficiency / Self-Locking Verification?",
"Number of worm starts",
"Worm wheel teeth",
"Module",
"Diameter quotient",
],
'energy-2': [
"⚡ Braking Energy Design",
"Enter the moment of inertia, the speeds before and after braking and the braking time to compute the braking torque, energy and average power",
'📖 View the "Braking Energy Design Guide"',
"Braking energy = ½J(ω₁² − ω₂²)",
"Speed before braking n₁ (r/min)",
"Speed after braking n₂ (r/min)",
"💡 Formula: ω=2πn/60; ΔE=½J(ω₁²-ω₂²); braking torque T=J(ω₁-ω₂)/t; average power P=ΔE/t",
"The speed before braking must be greater than after, otherwise it is treated as an acceleration process",
"The braking torque is the average under a constant-torque assumption; a real brake's torque varies with pressure",
"All braking energy is converted into heat, so the brake's heat-dissipation capacity must be checked",
"For frequent braking, the equivalent power and temperature rise should be calculated",
"📚 In-Depth Analysis: Equipment Energy Consumption / Efficiency",
"Motor output power = input × efficiency; estimate the running energy consumption.",
"Compare the annual electricity-cost difference between motors of different efficiency classes.",
"Total transmission efficiency = product of the efficiency of each stage.",
"Motor efficiency",
"Input 5 kW, efficiency η=90%: output P_out=5×0.9=4.5 kW; loss=0.5 kW. Annual operation of 4000 h consumes 5×4000=20000 kWh.",
"Overall system efficiency",
"Motor 0.92 × gearbox 0.95 × belt 0.97: total η=0.92×0.95×0.97≈0.848, so the system output is 84.8% of the input.",
"Why multiply efficiencies for the overall efficiency?",
"Each stage of a series transmission has losses, so the overall efficiency is the product (not the sum) of the stage efficiencies; the more stages, the lower the overall efficiency.",
"How to choose the efficiency class?",
"Higher classes (IE3/IE4) are more expensive but save electricity over long-term operation; compute the payback period from the annual operating hours and electricity price.",
'About "Braking Energy Design"',
"A braking energy design calculator: based on the moment of inertia and the speeds before and after braking, it computes the kinetic energy to be absorbed during braking, the required braking torque and the average braking power, for brake selection and heat-dissipation design.",
"Computes braking torque and energy together",
"Automatically detects braking / acceleration",
"Outputs angular acceleration and power",
"Brake selection and design",
"Crane braking verification",
"Vehicle braking-system energy analysis",
],
'estimate-gravity': [
"⚖️ Part Mass / Center of Gravity Estimation",
"Single-part mass calculation and multi-part combined center-of-gravity estimation",
'📖 View the "Part Mass / Center of Gravity Estimation Guide"',
"Center of gravity = Σ(m_i·x_i)/Σm_i",
"Part shape",
"Rectangular plate",
"Solid cylinder",
"Hollow tube",
"Hollow box",
"Solid sphere",
"Steel (7.85)",
"Stainless steel (7.93)",
"Aluminium (2.70)",
"Copper (8.90)",
"Brass (8.50)",
"Bronze (8.80)",
"Titanium (4.50)",
"ABS plastic (1.05)",
"Nylon (1.15)",
"Glass (2.50)",
"Concrete (2.40)",
"Diameter D (mm)",
"Length L (mm)",
"Outer diameter D (mm)",
"Inner diameter d (mm)",
"Outer length L (mm)",
"Outer width W (mm)",
"Outer height H (mm)",
"Base diameter D (mm)",
"Height H (mm)",
"🧮 Compute mass",
"➕ Add component",
"🗑️ Clear components",
"💡 Density in g/cm³, dimensions in mm, converted automatically. Center-of-gravity coordinates use the part's geometric center as the origin.",
"Combined center-of-gravity estimation",
"📚 In-Depth Analysis: Combined Center-of-Gravity Calculation",
"Combined center of gravity of multiple parts Xc=Σmi·xi/Σmi.",
"Centroid of an irregular section (numerical integration / decomposition method).",
"Verify the position of the center of gravity relative to the supports (anti-overturning).",
"Two-body combination",
"Part 1 mass 10 kg, xc=20 mm; part 2 mass 5 kg, xc=80 mm: Xc=(10×20+5×80)/(10+5)=(200+400)/15=40 mm. The center of gravity is closer to the heavier part.",
"Three-dimensional",
"Zc=Σmi·zi/Σmi, computed independently per axis; if Zc lies outside the support envelope there is an overturning risk.",
"Is the center of gravity the same as the centroid?",
"For a homogeneous body the center of gravity equals the centroid (geometric center); for a non-homogeneous body, mass weighting is required and geometry alone will not do.",
"Why compute the center of gravity?",
"Rotating parts need dynamic balancing, transported parts need anti-overturning measures and lifted parts need defined lifting points; the center of gravity is the basis of these designs.",
],
}

# term-link nodes missed by extract: zh -> en
EXTRA = {
}

def build(slug, en_list):
    path = os.path.join(WORK, slug + '.json')
    wj = json.load(open(path, encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('!! %s length mismatch %d vs %d' % (slug, len(en_list), len(items)))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if not en or not isinstance(en, str):
            print('!! %s empty translation' % slug)
            sys.exit(1)
        if CJK.search(en) or CNP.search(en):
            print('!! %s CJK/CNP violation: %s' % (slug, en[:60]))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('!! %s EXTRA CJK/CNP violation: %s' % (slug, en[:60]))
            sys.exit(1)
        mp[z] = en
    return mp

def write(slug, mp):
    os.makedirs(OUT, exist_ok=True)
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('name', slug)
    out = {'slug': slug, 'industry': 'machinery', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

for slug, en_list in EN.items():
    write(slug, build(slug, en_list))

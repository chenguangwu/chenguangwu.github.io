#!/usr/bin/env python3
# fire-rescue batch6 (5 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'fire-rescue')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'fire-rescue')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'fire-resistance-rating': [
"📋 Fire Resistance Rating Assessor",
"Look up the building fire-resistance-rating requirement and the fire-resistance limits of main members by building classification and height.",
"Public building",
"Building scale/importance",
"Ordinary building",
"Important building (hospital/mall/library, etc.)",
"Underground building?",
"📖 Fire Resistance Rating Reference",
"Building fire-resistance rating (GB 50016)",
"Grade I: important buildings and high-rise buildings (Class I high-rise)",
"Grade II: ordinary high-rise (Class II high-rise) and multi-storey important buildings",
"Grade III: ordinary multi-storey buildings",
"Grade IV: buildings with low fire hazard",
"Member fire-resistance limits (hours) reference",
"Fire wall: Grade I 3.0 h | Grade II 3.0 h | Grade III 3.0 h | Grade IV 3.0 h",
"Load-bearing wall: Grade I 3.0 h | Grade II 2.5 h | Grade III 2.0 h | Grade IV 0.5 h",
"Beam/column: Grade I 2.5-3.0 h | Grade II 2.0 h | Grade III 1.5 h | Grade IV 0.5 h",
"Floor slab: Grade I 1.5 h | Grade II 1.0 h | Grade III 0.5 h | Grade IV combustible",
"This tool provides reference based on the Code for Fire Protection Design of Buildings (GB 50016); actual engineering must follow the latest code clauses and local standards.",
"📚 In-Depth Analysis: Building Fire Resistance Rating Assessment",
"In design review, look up the required fire-resistance rating and main-member fire-resistance limits by building classification, height and importance.",
"Before an existing building changes use, quickly screen whether the original fire-resistance rating can meet the new functional requirements.",
"In fire inspections, verify whether the fire-resistance limits of the fire wall, load-bearing wall, column, beam, floor slab and other members meet the standard.",
"Rating determination for a 50 m important public building",
"With the default parameters (public building, height 50 m, important building, not underground): rated a Class II high-rise public building, requiring a fire-resistance rating not lower than Grade II; main-member fire-resistance limits: fire wall 3.0 h, load-bearing wall 2.5 h, column 2.5 h, beam 1.5 h, floor slab 1.0 h (all ≥ Grade II requirements). If it were an underground building, the fire-resistance rating should not be lower than Grade I.",
"How do Grade I and Grade II fire-resistance ratings differ?",
"The difference is mainly in the fire-resistance limits of the load-bearing wall, column, beam and floor slab: Grade I has column 3.0 h, beam 2.0 h, floor slab 1.5 h; Grade II has column 2.5 h, beam 1.5 h, floor slab 1.0 h. Important buildings and high-rise buildings must take a higher grade.",
"How is a member's fire-resistance limit confirmed?",
"It must be confirmed by fire-resistance testing, calculation or an existing inspection report and cannot be inferred from material alone; acceptance is based on the test/calculation conclusion, while this tool gives the code-required limits.",
'About "Fire Resistance Rating Assessor"',
"Based on building type, height and importance and per the Code for Fire Protection Design of Buildings (GB 50016), determine the building fire-resistance rating and give the fire-resistance-limit requirements for main members.",
"Automatic classification of four building types",
"Automatic fire-resistance-rating determination",
"Member fire-resistance-limit lookup",
"Special handling for high-rise/underground",
"Building fire-protection design",
"Fire acceptance reference",
"Structural selection assessment",
],
'fire-load': [
"⚖️ Fire Load Density Calculator",
"Compute the total heat of combustibles and the fire load density per unit area to assess fire severity.",
"Total fire load heat Q = Σ(m_i·h_i) (m_i = mass of combustible, h_i = heat per unit mass); fire load density q_f = Q ÷ A_f (MJ/m²).",
"Floor area Af (m²)",
"Combustible list (select a material and enter mass/quantity)",
"+ Add combustible",
"Fire load density formula",
"Total fire load Q = Σ(mi × Hi), where mi is the mass of the i-th combustible (kg) and Hi is its calorific value per unit mass (MJ/kg)",
"Fire load density q = Q / Af (MJ/m²)",
"Equivalent fire load qeq = q × combustion-efficiency factor (generally 0.8)",
"Typical combustible calorific-value reference",
"Wood: 16-19 MJ/kg | Paper: 13-17 MJ/kg | Cotton fabric: 17-20 MJ/kg",
"Plastic (PVC): 18-25 MJ/kg | Rubber: 30-35 MJ/kg | Gasoline: 43-47 MJ/kg",
"Furniture (combined): about 14-20 MJ/kg",
"Load density grade reference",
"Low: <500 MJ/m² | Medium: 500-1000 MJ/m² | High: 1000-2000 MJ/m² | Very high: >2000 MJ/m²",
"This tool is for engineering estimation of fire load; formal design should follow the Code for Fire Protection Design of Buildings and related standards.",
"📚 In-Depth Analysis: Fire Load Density Calculation",
"Input for performance-based fire design: ",
"fire load",
" density, as a boundary condition for the design fire curve and structural fire-resistance analysis.",
"Before a warehouse/workshop changes its stored-material category, re-check whether the load density exceeds the limit by the new materials' mass and calorific value.",
"In fire investigation, estimate the total heat from the burned area and residual combustibles to help judge the burning duration.",
"Load calculation for 20 kg of wood in a 90 m² room",
"With the default parameters (wood 10 kg × 2 items, calorific value 18 MJ/kg, room 90 m²): total fire load = 10×18×2 = 360 MJ; load density = 360/90 = 4 MJ/m²; converting at a wood calorific value of 18 MJ/kg gives an equivalent load of about 3 MJ/m², rated a low load grade. Ordinary offices are often 300-500 MJ/m², while libraries and warehouses can exceed 1000 MJ/m².",
"Is a higher load density always more dangerous?",
"Overall, the higher the load density, the greater the total heat release and the longer the burning, raising the requirements for structural fire resistance and smoke exhaust; but whether it is dangerous also depends on ventilation, suppression systems and occupancy density, so density is only one design input.",
"How to take the calorific value of mixed combustibles?",
"Take the mass-weighted average: wood about 18, paper 16, polyethylene 44, gasoline 44 MJ/kg; when plastics and oils make up a large share the total heat rises significantly, so a wood value cannot simply be applied.",
'About "Fire Load Density Calculator"',
"Based on the mass and calorific value per unit mass of various combustibles in a building, compute the total fire load and the fire load density per unit area and determine the fire-severity grade.",
"Additive calculation for multiple combustibles",
"Built-in calorific values of common materials",
"Equivalent-load conversion",
"Severity-grade determination",
"Building fire-load assessment",
"Fire-safety hazard screening",
],
'dizhensoujiuzhichengjisuan': [
"🚑 Earthquake Rescue Shoring Calculator",
"Enter the structure weight, shoring angle, number of shores and allowable capacity per shore to compute the shore axial force, horizontal thrust and stability safety factor.",
"Force per shore F = W÷(n·sinθ) (W = structure weight, n = number of shores, θ = shoring angle); horizontal thrust = F·cosθ; total shoring force = F·n; safety factor K = allowable capacity÷F, K≥3 safe.",
"Structure weight W (kN)",
"Shoring angle θ (°)",
"Number of shores n",
"Allowable capacity per shore (kN)",
"💡 Axial force per shore F = W/(n·sinθ); horizontal thrust = F·cosθ; safety factor K = allowable capacity / F (θ is the angle between the shore and the horizontal plane).",
"The shoring angle θ is the angle between the shore and the horizontal plane, usually 45°-60°; the smaller the angle the greater the horizontal thrust.",
"The safety factor K is recommended to be not less than 2.0, and should be raised appropriately for temporary rescue shoring.",
"The shore members, bearing plates and foundation must all have adequate load-bearing capacity to prevent settlement or sliding.",
"Earthquake rescue is high-risk work; the shoring scheme must be assessed and confirmed on site by professionals.",
"📚 In-Depth Analysis: Earthquake Rescue Shoring Calculation",
"In collapse rescue, calculate the axial force of a single shore from the wall/member load and shoring angle to determine the number and specification of shores.",
"Assess the overall stability safety factor of the shoring system and judge whether denser shoring or diagonal bracing is needed.",
"In training and plan drafting, demonstrate the significant effect of different shoring angles (e.g. 45°/60°) on the single-shore force.",
"Verification for a total horizontal thrust of 50 kN with 4 shores at 45°",
"With the default parameters (total horizontal thrust 50 kN, shoring angle 45°, 4 shores, 30 kN allowable per shore): horizontal thrust per shore = 50/4 = 12.50 kN, axial force per shore = 12.50/cos45° = 17.68 kN, less than the 30 kN allowable; stability safety factor K = 30/17.68 = 1.70, rated by the tool as 'critical, needs strengthening'. In practice a higher shoring safety factor is usually required, so shores should be densified or the shoring angle reduced to raise K.",
"Why should the shoring angle be as small as possible?",
"The axial force per shore = horizontal component / cosθ, and the larger the angle the greater the axial force. At 45° the axial force is already 1.41× the horizontal component and at 60° it reaches 2×; reducing the shoring angle greatly lowers the single-shore force and raises the stability safety factor.",
"Why is K=1.70 still considered critical?",
"This tool back-calculates K from the allowable capacity per shore, reflecting only the material strength margin. Real rescue must also consider joint connections, foundation bearing, secondary collapse and impact loads, so even with K>1, denser shoring or diagonal bracing is often required before work is allowed.",
'About "Earthquake Rescue Shoring Calculator"',
"For temporary shoring load calculation in earthquake collapsed-building rescue, compute the single-shore axial force, horizontal thrust and stability safety factor from the structure weight, shoring angle and number of shores, to aid shoring-scheme design.",
"Axial force computed by statics decomposition",
"Outputs the single-shore and total shoring force",
"Computes the horizontal thrust for foundation verification",
"Graded determination of the stability safety factor",
"Shoring for earthquake collapsed-building rescue",
"Force verification of temporary shoring schemes",
"Shore-member selection and layout",
"Rescue-technique training and instruction",
"Structure weight",
"Shoring angle",
"Number of shores",
"Allowable capacity per shore",
],
'length-distance': [
"📏 Fire Water-Supply Distance Calculator",
"Enter the pump outlet pressure, required outlet pressure, elevation difference and hose specification to compute the maximum effective supply distance of a single main.",
"Available pressure avail = P_pump − P_nozzle − ρg·Δh (Δh = elevation in m); friction loss per metre per_m = 10.67·Q^1.852÷(C^1.852·D^4.87)×0.00980665; max supply distance L_max = avail÷per_m.",
"Pump outlet pressure (MPa)",
"Required outlet pressure (MPa)",
"Elevation difference Δh (m)",
"pump",
"outlet",
" − 0.00981×Δh) / unit friction loss; friction loss is computed by the Hazen-Williams formula.",
"The elevation difference Δh is the vertical difference of the supply endpoint relative to the pump, positive for upward supply and negative for downward.",
"The required outlet pressure is the pressure needed for the nozzle to work normally, generally 0.2-0.35 MPa.",
"The calculation is for direct supply from a single main and does not include local losses at couplings or the effect of parallel splitting.",
"Actual supply should also consider a safety margin; retaining 0.05-0.1 MPa of pressure reserve is recommended.",
"📚 In-Depth Analysis: Maximum Water-Supply Distance Calculation",
"For long-distance supply, back-calculate the maximum layable length of a single main from the available friction pressure and the friction loss per metre.",
"In fire plans, determine whether a relay pump or parallel mains are needed to cover a distant fire point.",
"In training, demonstrate the effect of hose diameter/flow/lining coefficient (C value) on the supply distance.",
"Maximum layable length for Φ65, 6.5 L/s, C=140",
"With the default parameters (Φ65 mm, flow 6.5 L/s, lined hose C=140, available friction pressure 0.6 MPa): friction loss per metre about 0.0006 MPa/m, and the main can be laid about 1005.7 m (about 50.3 lengths of 20 m hose). If the actual fire point exceeds this distance, a relay pump must be added or mains laid in parallel to reduce the single-line loss.",
"Can parallel mains increase the supply distance?",
"When two mains of the same specification are laid in parallel, each carries only half the flow and the friction loss drops to about 30% of a single main, effectively lengthening the distance supportable by the 'available pressure'; this is the standard practice for long-distance supply.",
"How much does the lining coefficient C value matter?",
"The C value reflects the smoothness of the hose inner wall: polyurethane/rubber lining C≈140-150, while old canvas is only about 80-100; the lower the C value the greater the friction loss and the shorter the supply distance, so equipment maintenance directly affects supply capability.",
'About "Fire Water-Supply Distance Calculator"',
"Based on the fire-pump outlet pressure, required outlet pressure, terrain elevation difference and hose specification, estimate the maximum effective supply distance a single supply main can reach, for fire water-supply planning.",
"Accounts for pump pressure, elevation difference and friction loss together",
"Based on the Hazen-Williams friction-loss formula",
"Automatically converts to the number of hose lengths",
"Smart prompt when pressure is insufficient",
"Fire-scene supply-main laying planning",
"Relay water-supply estimation for high-rise buildings",
"Pump selection and pressure verification",
"Fire water-supply training drills",
"Pump outlet pressure",
"Required outlet pressure",
"Elevation difference",
],
'power-2': [
"🔥 Fire Pump Selection Calculator",
"Enter the design flow and head to compute the fire pump shaft power and motor power and recommend an XBD-series model.",
"Shaft power Pₛ = 0.00981·Q·H÷η (Q = design flow in L/s, H = head in m, η = pump efficiency); motor power Pₘ = Pₛ×service factor; flow Q(m³/h) = 3.6·Q.",
"Design flow Q (L/s)",
"Design head H (m)",
"Motor power service factor",
"💡 Formula: shaft power P = ρgQH / (1000η) = 0.00981 × Q(L/s) × H(m) / η; motor power = shaft power × service factor.",
"Pump efficiency is generally 70%-80%, and 75% is common for centrifugal fire pumps.",
"The motor power service factor is recommended to be 1.10-1.20 to avoid motor overload.",
"The recommended models are based on common XBD-series specifications; actual selection is subject to the manufacturer's catalogue and certification.",
"After selection, verify whether the pump's flow-head curve meets the design operating point.",
"📚 In-Depth Analysis: Fire Pump Shaft Power and Motor Selection",
"In fire-pump design selection, estimate the shaft power from the flow and head to back-calculate the required ",
" and model.",
"In an existing pump room, verify whether the motor power meets the most unfavorable condition to avoid overload at high flow.",
"Before procurement, pre-select an XBD-series pump and matching motor rating by the design condition (Q/H).",
"Selection for design condition Q=20 L/s and shaft power 15.7 kW",
"With the default parameters (flow 72 m³/h ≈ 20 L/s, shaft power 15.70 kW): considering motor efficiency and reserve, a motor power of 18.5 kW (corresponding rating) is recommended, with an efficiency of about 82%; recommended model XBD-series 18.5 kW (design condition Q=20 L/s, H=60 m). Actual selection should also add piping and standby margins and meet the duty/standby or two-duty/one-standby configuration.",
"Why must the motor power be greater than the shaft power?",
"The shaft power is what the pump itself consumes; the motor must also cover transmission losses, efficiency discounts and operating reserve and keep a certain overload margin, so the motor rated power is usually 10%-20% higher than the shaft power.",
"Where does the flow of 72 m³/h come from?",
"72 m³/h = 72000/3600 = 20 L/s, a common fire-pump design flow rating (e.g. XBD series); the specific value must be determined by the flow and head at the system's most unfavorable condition.",
'About "Fire Pump Selection Calculator"',
"Based on the design flow and head of the fire water-supply system, compute the required shaft power and motor power of the fire pump and recommend common XBD-series model ratings, to aid equipment selection.",
"Based on the standard pump power formula",
"Outputs multiple units (kW / HP) simultaneously",
"Automatically matches the standard motor power rating",
"Supports a custom efficiency and service factor",
"Fire water-supply system equipment selection",
"Fire pump room design and verification",
"Pump power verification in renovation projects",
"Fire-engineering budgeting and procurement",
"Design flow",
"Design head",
"Motor power service factor",
],
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
        if it.get('src_diff') and it.get('zh_src'):
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
    return mp

def write(slug, mp):
    os.makedirs(OUT, exist_ok=True)
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('name', slug)
    out = {'slug': slug, 'industry': 'fire-rescue', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

for slug, en_list in EN.items():
    write(slug, build(slug, en_list))

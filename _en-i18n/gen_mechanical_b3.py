#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'mechanical')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'mechanical')
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
    out = {'slug': slug, 'industry': 'mechanical', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('flywheel-energy', build('flywheel-energy', [
        "⚡ Flywheel Rotational Kinetic Energy Calculator (Mechanical)",
        "Estimate the rotational kinetic energy stored by a flywheel from its mass, radius and speed (solid disc model).",
        "Flywheel Rotational Kinetic Energy Calculator",
        "Flywheel energy E = ½·I·ω², disc moment of inertia I = ½·m·r²; m mass, r radius, ω angular velocity.",
        "E = ½·I·ω² (solid disc I = ½mr²)",
        "A flywheel smooths speed fluctuation and recovers braking energy",
        "Stored energy is proportional to the square of speed",
        "📚 In-Depth Analysis: Flywheel Rotational Kinetic Energy Calculator (Mechanical)",
        "Estimate the moment of inertia and stored energy from flywheel mass and radius, to assess storage capacity and speed stabilisation capability for flywheel selection.",
        "Estimate the energy released by the flywheel of intermittent-load equipment such as presses and shears, and judge whether it can suppress load fluctuation.",
        "Assess the kinetic energy of rotating parts during emergency stops, providing a basis for brake system and safety protection design.",
        "Approximated as a solid disc, the moment of inertia is I = ½·m·r² (kg·m²);",
        "Angular velocity",
        "Rotational kinetic energy",
        "E = ½·I·ω² (J). Energy is proportional to the moment of inertia and to the square of angular velocity.",
        "Flywheel mass m=50 kg, radius r=0.3 m, speed 1000 r/min: I = 0.5×50×0.3² = 2.250 kg·m²; ω = 2π×1000/60 ≈ 104.72 rad/s; E = 0.5×2.25×104.72² ≈ 12337.0 J ≈ 12.34 kJ. If the speed drops to 500 r/min, stored energy falls to about 3.08 kJ (about one quarter) — showing that raising speed stores more energy than simply adding weight to the flywheel",
        "Why is the solid disc model used?",
        "The tool uses the most common solid disc model I = ½mr²; real flywheels are mostly rim-concentrated mass types whose moment of inertia approaches m·r² (about twice this model), so the result here is conservative. Precise design should use the actual section or a 3D model.",
        "Why does a flywheel help hold speed?",
        "The more energy a flywheel stores, the less its speed is changed by instantaneous load: it releases energy under heavy load and absorbs energy under light load, smoothing out periodic load fluctuation. That is why presses, compressors and similar equipment are fitted with flywheels.",
    ]))

    write('centrifugal-force', build('centrifugal-force', [
        "🧮 Centrifugal Force Calculator (Mechanical)",
        "Calculate the centrifugal force (inertial force) of a rotating body from its mass, rotation radius and speed.",
        "Centrifugal Force Calculator",
        "Centrifugal force F = m·ω²·r, angular velocity ω = 2π·n ÷ 60; m mass, r rotation radius, n speed (rpm).",
        "Rotation radius r (m)",
        "F = m·ω²·r, ω = 2πn/60 (n in rpm)",
        "Centrifugal force is proportional to the square of speed and grows rapidly at high speed",
        "Commonly used in rotor balancing and centrifuge design",
        "📚 In-Depth Analysis: Centrifugal Force Calculator (Mechanical)",
        "Calculate the centrifugal force of rotating parts (counterweights, flywheels, drums) at a given speed, for strength and unbalance assessment.",
        "Evaluate the additional bearing load of high-speed rotating parts and judge whether dynamic balancing or speed limiting is required.",
        "Compare centrifugal force at different radii and speeds to understand that it is proportional to radius and to the square of speed.",
        "Angular velocity",
        "ω = 2π·n/60 (rad/s, n in r/min); centrifugal force F = m·ω²·r (N). F is proportional to mass and radius and to the square of angular velocity (speed), so raising speed affects centrifugal force far more than increasing the radius does.",
        "Mass m=10 kg, radius of gyration r=0.5 m, speed 600 r/min: ω = 2π×600/60 ≈ 62.83 rad/s; F = 10×62.83²×0.5 ≈ 19739.2 N ≈ 19.74 kN. If the speed doubles to 1200 r/min, the centrifugal force rises to about 4 times (≈78.96 kN) — which is why high-speed rotating equipment must be strictly speed-limited and dynamically balanced.",
        "Are centrifugal force and",
        "the same thing?",
        "They are numerically equal and oppositely directed, being two descriptions of the same interaction: centripetal force is the external force applied to the rotating body pointing to the centre, while centrifugal force is the inertial force observed in the rotating (non-inertial) frame. In engineering the latter is commonly used to describe the outward load a part has to withstand.",
        "Why does centrifugal force become four times larger when the speed doubles?",
        "Because F ∝ ω², doubling the speed doubles ω, which becomes 4 times after squaring. That is also why overspeed rotating equipment (grinders, centrifuges, flywheels) becomes extremely dangerous and must have overspeed protection and guards fitted.",
    ]))

    write('lever-advantage', build('lever-advantage', [
        "📡 Lever Mechanical Advantage Calculator (Mechanical)",
        "Calculate the mechanical advantage (force-saving ratio) of a lever from the effort arm and resistance arm lengths.",
        "Lever Mechanical Advantage Calculator",
        "Lever mechanical advantage MA = L₁ ÷ L₂; L₁ effort arm, L₂ resistance arm, the larger MA is the more effort is saved.",
        "Effort arm L₁ (m)",
        "Resistance arm L₂ (m)",
        "MA = L₁/L₂ (effort arm / resistance arm)",
        "MA>1 saves effort, at the cost of larger displacement at the effort end",
        "The mechanical advantage of a pulley block is about the number n of rope segments supporting the load",
        "📚 In-Depth Analysis: Lever Mechanical Advantage Calculator (Mechanical)",
        "Calculate the mechanical advantage of a lever from its effort arm and resistance arm lengths, to design force-saving or motion-amplifying mechanisms.",
        "Check whether the force amplification of hand tools (crowbars, pliers, handles) meets the required operating force.",
        "Trade off against travel and speed: the larger the advantage, the proportionally larger the travel at the effort end.",
        "Mechanical advantage MA = L₁/L₂ (L₁ effort arm, L₂ resistance arm); required effort = resistance/MA, i.e. the tool delivers 1/MA. An ideal lever conserves work: effort × effort-end travel = resistance × resistance-end travel.",
        "Effort arm L₁=1.0 m, resistance arm L₂=0.2 m: MA = 1.0/0.2 = 5.00; the required effort is 1/5 of the resistance (1/MA = 0.20), so lifting a 500 N load takes about 100 N of force, but the hand end has to move 5 times the distance.",
        "Is a larger mechanical advantage always better?",
        "Not necessarily. Saving effort always costs distance (or speed): MA=5 means 4/5 of the force is saved, but the travel at the effort end is 5 times that at the resistance end. Design must trade off against space, travel and speed requirements rather than blindly chasing a large advantage.",
        "Why is the actual advantage smaller than the theoretical value?",
        "The theoretical MA assumes a frictionless rigid lever; in reality there is pivot friction, member deformation and self weight, and efficiency is typically 90%~98%. For precision or heavy-load applications the efficiency should be factored in with margin.",
    ]))

    write('gear-ratio', build('gear-ratio', [
        "⚙️ Gear Ratio Calculator (Mechanical)",
        "Calculate the ratio from the tooth counts of the driving and driven gears and derive output speed and torque.",
        "Gear Ratio Calculator",
        "Gear ratio i = z₂ ÷ z₁ = n₁ ÷ n₂; driven torque T₂ = T₁ · i · η; z tooth count, n speed, η transmission efficiency.",
        "Driving gear teeth z₁",
        "Driven gear teeth z₂",
        "Driving gear torque T₁ (N·m)",
        "i = z₂/z₁; for reduction z₂>z₁ (i>1), for speed increase the opposite applies",
        "η takes the gear transmission efficiency (about 0.95~0.98 for a single stage)",
        "📚 In-Depth Analysis: Gear Ratio Calculator (Mechanical)",
        "Calculate the ratio from the tooth counts of the driving and driven gears and derive output speed and output torque, for reduction or speed-increase scheme design.",
        "Convert output torque using the transmission efficiency to assess power loss in multi-stage drives.",
        "Check the speed and torque matching of the motor–reducer–load combination.",
        "Ratio i = z2/z1; output speed n2 = n1/i; output torque T2 = T1·i·η (η is the transmission efficiency). In terms of power, ideally P = T·ω stays constant, while in reality efficiency loss makes the output power η times the input power.",
        "Driving gear z1=20, driven gear z2=40, input speed 1500 r/min, input torque 100 N·m, efficiency η=0.97: i = 2.000; n2 = 1500/2 = 750.0 r/min; T2 = 100×2×0.97 = 194.0 N·m. Speed is halved and torque roughly doubles (after the 3% efficiency loss), so power is essentially conserved.",
        "Does a larger ratio always mean larger torque?",
        "Yes, theoretically the output torque is amplified by i and the speed drops to 1/i; in practice efficiency and gear strength limit this. An excessively large single-stage ratio (generally ≤5~7 for spur gears) makes the large gear oversized or the structure impractical, so multi-stage drives are often used to share the ratio.",
        "What does an efficiency of 0.97 mean?",
        "A pair of involute cylindrical gears typically has a transmission efficiency of 0.97~0.99 (including mesh friction, oil churning and bearing losses); with multiple stages in series the overall efficiency is the product of the stage efficiencies, so more stages means greater total loss.",
    ]))

    write('beam-point-load', build('beam-point-load', [
        "🧮 Simply Supported Beam Central Point Load Calculator (Mechanical)",
        "Calculate the maximum bending moment, mid-span deflection and bending stress of a simply supported beam under a central point load.",
        "Simply Supported Beam Central Point Load Calculator",
        "Simply supported beam with central point load: maximum bending moment M_max = F·L ÷ 4, maximum deflection δ = F·L³ ÷ (48·E·I); F point load, L span, E elastic modulus, I second moment of area of the section.",
        "Point load F (kN)",
        "Central point load: M_max = FL/4, δ = FL³/(48EI)",
        "Units unified as N, mm, N/mm² (E: GPa→×1000, I: cm⁴→×1e4)",
        "σ = M/W, W = bh²/6 is the section modulus of a rectangular section",
        "📚 In-Depth Analysis: Simply Supported Beam Central Point Load Calculator (Mechanical)",
        "When a simply supported beam carries a central concentrated load, find the maximum bending moment, mid-span deflection and bending stress, for beam section selection and stiffness checks.",
        "Check deformation of conveyor line support beams, equipment cross members and similar members under concentrated load, and judge whether the deflection limit (such as L/250) is satisfied.",
        "Compare the effects of different sections (b×h) or materials (E) on deflection and stress to support lightweight design.",
        "Formulas and units",
        "Maximum bending moment M = F·L/4 (kN·m); mid-span deflection δ = F·L³/(48·E·I), which must be converted to the N–mm system (F in N, L in mm, E in N/mm², I in mm⁴); section modulus W = b·h²/6 (mm³); bending stress σ = M/W (MPa, with M converted to N·mm). The tool internally multiplies the input value of E in GPa by 1000 to get N/mm², and the input value of I in cm⁴ by 10⁴ to get mm⁴.",
        "Span L=4 m, point load F=10 kN, E=30 GPa, I=5000 cm⁴, rectangular section b=150 mm, h=300 mm: M = 10×4/4 = 10.00 kN·m; δ = 10×1000×4000³/(48×30000×5×10⁷) ≈ 8.89 mm; W = 150×300²/6 = 2.25×10⁶ mm³; σ = 10×10⁶/2.25×10⁶ ≈ 4.44 MPa. The deflection of 8.89 mm relative to a 4 m span is about L/450, satisfying the common L/250 limit; the stress of 4.44 MPa is far below the allowable value for steel, so this case is governed by stiffness rather than strength.",
        "Why must the deflection formula be converted to the N–mm system?",
        "In δ = F·L³/(48·E·I) the units are strongly coupled: with E in N/mm² and I in mm⁴, F must be in N and L in mm. Mixing kN, m, GPa and cm⁴ without conversion makes the result differ by several orders of magnitude, which is the most common hand-calculation error.",
        "Which matters more, the deflection limit or the stress limit?",
        "For steel beams strength (stress) is usually easy to satisfy while stiffness (deflection) is often the governing condition; for brittle materials or short stubby beams it is the opposite. Design should check the more critical of the two, and precision equipment supports must also consider vibration stiffness.",
    ]))

    write('calc-2', build('calc-2', [
        "⚙️ Chain Drive Calculator",
        "Calculate the roller chain ratio, chain speed, number of links, wrap angle and the tooth count of the large sprocket.",
        "Chain pitch p (mm)",
        "Initial centre distance a₀ (mm)",
        "Ratio i = z₂ / z₁",
        "Chain speed v = z₁ × p × n₁ / 60000 (m/s)",
        "Number of links Lp = 2a₀/p + (z₁+z₂)/2 + [(z₂−z₁)/(2π)]² × p/a₀, result rounded to an even number",
        "Wrap angle α₁ ≈ 180° − 57.3°×(d₂−d₁)/a₀ (d = p/sin(π/z) is the sprocket pitch circle diameter)",
        "📚 In-Depth Analysis: Chain Drive Calculator",
        "Calculate the ratio, chain speed, number of links and wrap angle from the sprocket tooth counts, chain pitch and centre distance, completing a preliminary roller chain design.",
        "Check the chain speed (for ordinary roller chains preferably ≤15 m/s) and the wrap angle on the small sprocket (preferably ≥120°), and judge whether parameters need adjustment.",
        "Back-calculate the tight-side tension from the transmitted power and chain speed, providing a basis for selecting chain size and lubrication method.",
        "Ratio i = z2/z1; chain speed v = z1·p·n1/60000 (m/s, p is the pitch in mm); n2 = n1/i; number of links Lp = 2a0/p + (z1+z2)/2 + [(z2−z1)/(2π)]²·p/a0, result taken as even; small sprocket wrap angle α1 ≈ 180° − 57.3·(d2−d1)/a0 (d = p/sin(π/z) is the sprocket pitch circle diameter); sprocket pitch circle d = p/sin(π/z); tight-side tension F = P×1000/v (N). Recommended chain speed ≤15 m/s.",
        "Small sprocket z1=19, large sprocket z2=57, pitch p=15.875 mm, centre distance a0=500 mm, n1=970 r/min, power 7.5 kW: i = 3.00; v = 19×15.875×970/60000 ≈ 4.88 m/s; n2 ≈ 323.3 r/min; theoretical number of links ≈ 102.15, rounded to even gives Lp = 102 links; α1 ≈ 158.0° (greater than 120°, wrap angle sufficient); small sprocket pitch circle ≈ 96.45 mm, large one ≈ 288.18 mm; tight-side tension ≈ 1538.1 N.",
        "Why must the number of links be even?",
        "A chain consists of alternating inner and outer link plates, so an even-link chain needs a connecting link to close; an odd number of links requires an extra transition link whose strength is markedly lower than ordinary links, so it should be avoided in design.",
        "What problems does excessive chain speed cause?",
        "Excessive chain speed aggravates impact and noise, accelerates hinge wear, and causes speed fluctuation through the polygon effect; for ordinary roller chains v ≤ 15 m/s is recommended, and high-speed applications should use small-pitch, high-tooth-count chains or inverted tooth chains with enhanced lubrication.",
    ]))


if __name__ == '__main__':
    main()
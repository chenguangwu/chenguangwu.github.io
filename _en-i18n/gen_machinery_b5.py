#!/usr/bin/env python3
# machinery batch5 (5 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'machinery')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'machinery')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'pressure-4': [
"🧮 Spline Specification Calculator",
"Enter the number of teeth, module, pressure angle and root form to compute the pitch circle, major diameter, minor diameter and base circle of an involute spline",
'📖 View the "Spline Specification Calculator Guide"',
"Spline compression σ = F/(d·l·z)",
"Root form",
"Flat root (30°)",
"Fillet root",
"45° pressure angle",
"💡 External spline: pitch circle D=mz; major diameter DEE=m(z+1); minor diameter DIE=m(z-1.5); base circle Db=D·cosα; tooth thickness s=πm/2",
"This calculation follows the GB/T 3478 involute spline standard; the 30° flat root is the most common",
"Module series for 30° pressure angle splines: 0.5, 1, 1.5, 2, 2.5, 3, 5, 10, etc.",
"45° pressure angle splines have shorter teeth and are used for thin-wall or static connections",
"The internal spline dimensions must mate accordingly (internal major diameter = external major diameter + clearance)",
"📚 In-Depth Analysis: Spline Joint Parameters",
"Pitch circle, base circle and tooth thickness calculation for rectangular/involute splines.",
"Major/minor diameter and flank fit check of internal and external splines.",
"Single-tooth arc length and compression area estimation.",
"Involute spline",
"Pitch circle D, pressure angle α=30°: base circle Db=D·cosα=D×0.866; tooth thickness s=π·D/(2·z) (approximate); circular pitch p=π·D/z. For D=30, z=10: Db=25.98, p=9.425 mm.",
"Compression check",
"For transmitted torque T, number of teeth z, working height h and mean radius r: pressure p=2T/(z·h·r·l), which must be below the allowable spline pressure.",
"Involute spline vs rectangular?",
"The involute spline has a thick tooth root, high strength and good self-centering and is often used for heavy loads; the rectangular spline is easy to machine and is used for light-to-medium loads.",
"Why compute the base circle?",
"The involute spline tooth profile is generated from the base circle, which determines the tooth form and the centering method (flank or major-diameter centering).",
'About "Spline Specification Calculator"',
"A spline specification calculator: per the GB/T 3478 involute spline standard, it computes the pitch circle, major diameter, minor diameter, base circle and tooth thickness of external/internal splines from the number of teeth, module, pressure angle and root form.",
"Supports three forms: flat root, fillet root and 45°",
"Outputs internal and external spline dimensions together",
"Tooth thickness and circular pitch calculation",
"Spline joint design",
"Spline machining parameter determination",
"Spline gauge design",
"Mechanical transmission fit selection",
],
'runhuaxitongsheji': [
"📐 Lubrication System Design",
"Enter the bearing diameter, length, speed, load and operating conditions to compute the contact pressure, PV value and required oil quantity, and recommend a lubrication method",
'📖 View the "Lubrication System Design Guide"',
"Oil quantity = f(power, speed)",
"Bearing diameter d (mm)",
"Bearing length L (mm)",
"Radial load W (kN)",
"Oil viscosity η (mPa·s)",
"Relative clearance ψ (‰)",
"Radial plain bearing",
"Thrust plain bearing",
"Rolling bearing",
"💡 Formula: contact pressure p=W/(d·L); speed v=π·d·n/60000; PV value=p·v; friction coefficient f≈2π²·η·n/(p·ψ); oil quantity Q=f·W·v/(ρ·cp·ΔT)",
"For radial plain bearings L/d is usually 0.5-1.5; too large tends to cause eccentric loading and heating",
"The PV value reflects the heating tendency of the bearing; the allowable PV for babbitt is about 10-15 MPa·m/s",
"Oil viscosity selection: high viscosity (46-68) for low speed and heavy load, low viscosity (10-22) for high speed and light load",
"The relative clearance ψ is usually 0.5‰-3‰, taking the smaller value for high precision",
"The oil quantity must meet the heat-dissipation requirement, and circulating lubrication must ensure sufficient flow",
"📚 In-Depth Analysis: Lubrication System Design",
"Check the lubrication state via the contact pressure p=W/A and PV=p·v.",
"Select the pump and piping from the oil supply and power consumption.",
"Boundary / hydrodynamic lubrication discrimination.",
"Journal lubrication",
"Load W=5 kN, projected area A=50×20=1000 mm², v=2 m/s: p=5000/1000=5 MPa; PV=5×2=10 MPa·m/s. Below the allowable value, so hydrodynamic lubrication holds.",
"Pump power",
"Flow Q=10 L/min, supply pressure 0.5 MPa: pump power ≈ p·Q/60 = 0.5×10/60 ≈ 0.083 kW (efficiency ignored).",
"What if the PV exceeds the limit?",
"Increase the area, reduce the speed, switch to a higher-PV material (such as bronze/PTFE addition) or adopt forced lubrication; otherwise boundary wear sets in.",
"Conditions for hydrodynamic lubrication?",
"Sufficient speed, viscosity and clearance are needed to form a wedge oil film; low speed with heavy load tends to shift to boundary lubrication and requires extreme-pressure additives.",
'About "Lubrication System Design"',
"A lubrication system design calculator: from the bearing diameter, length, speed, load and oil viscosity it computes the bearing contact pressure, surface speed, PV value, friction power and required oil flow, and recommends a suitable lubrication method for the operating conditions.",
"Computes the three core indices: contact pressure, speed and PV value",
"Estimates friction coefficient and power by the Petroff equation",
"Computes the required oil quantity from the heat-dissipation requirement",
"Recommends a lubrication method by speed and bearing type",
"Plain bearing lubrication scheme design",
"Circulating lubrication system flow selection",
"PV value check and material selection",
"Rolling bearing lubrication method determination",
],
'strength-15': [
"📐 Chain Design",
"Enter the power, small-sprocket speed and tooth count to compute the recommended pitch, chain speed and circumferential force and check the strength",
'📖 View the "Chain Design Guide"',
"Chain pull = power / speed",
"Small-sprocket speed n₁ (r/min)",
"💡 Chain speed v=z₁n₁p/(60×1000); circumferential force F=1000P/v; transmission ratio i=z₂/z₁; recommended center distance a₀=40p",
"Recommended small-sprocket tooth count z₁: ≥17 for roller chain, ideally 19-25, an odd number being preferable",
"A chain speed v<0.6 m/s is low-speed chain drive and v>12 m/s is high-speed chain drive",
"The large-sprocket tooth count should not exceed 120, otherwise the worn chain tends to jump off",
"The recommended pitch is chosen empirically from the small-sprocket speed; in practice the power curve must be checked",
"📚 In-Depth Analysis: Chain Drive / Pitch Selection",
"Recommend the chain pitch p from the small-sprocket speed.",
"Recommended center distance a0=40·p.",
"Check the chain speed v=z1·p·n1/60000.",
"Pitch recommendation",
"Small-sprocket speed n1=1000 rpm: recommended pitch p≈a standard value (such as the 12.7/15.875 mm series); taking p=15.875 → center distance a0=40×15.875≈635 mm.",
"Chain speed",
"z1=19, p=15.875, n1=1000: v=z1·p·n1/60000=19×15.875×1000/60000≈5.03 m/s, in the medium-speed range.",
"Does a larger pitch carry more load?",
"Yes, but a large pitch has a strong polygon effect and high noise and impact; high speed favours a small pitch and more teeth.",
"Why take the center distance as 40p?",
"Experience recommends a preliminary a0≈30-50 times the pitch, balancing the wrap angle and slack-side sag, and finally fine-tuned to the structure.",
'About "Chain Design"',
"A chain design calculator: from the power, small-sprocket speed and tooth count it empirically selects the recommended pitch and chain number and computes the chain speed, effective circumferential force, transmission ratio, center distance and number of links, aiding the preliminary design of roller chain drives.",
"Automatic selection of the recommended pitch and chain number",
"Chain speed and circumferential force calculation",
"Center distance and link-count estimation",
"Roller chain drive design",
"Chain drive selection",
"Reducer chain drive scheme",
"Mechanical transmission course design",
],
'strength-6': [
"⚙️ Key Joint Strength",
"Enter the shaft diameter, key dimensions, torque and material allowable stress to check the crushing and shear strength of a parallel key",
'📖 View the "Key Joint Strength Guide"',
"Key strength = crushing / shear check",
"Key width b (mm)",
"Key height h (mm)",
"Key length L (mm)",
"Key type",
"Round-ended parallel key (l=L-b)",
"Square-ended parallel key (l=L)",
"Allowable crushing stress [σp] (MPa)",
"💡 Working length l=L-b (round end) / L (square end); crushing stress σp=4T/(d·h·l); shear stress τ=2T/(d·b·l)",
"Allowable crushing stress [σp]: steel 110-150 MPa, cast iron 70-80 MPa (upper limit for static load)",
"Allowable shear stress [τ]: steel 90-120 MPa (upper limit for static load, 60-90 for dynamic load)",
"Select the key size from the standard by shaft diameter; this tool supports custom dimensions",
"When a single key is insufficient, two keys (180° apart) may be used, but the load capacity is taken as 1.5 times",
"📚 In-Depth Analysis: Key Joint Strength",
"Crushing σp=4T/(d·h·l), shear τ=2T/(d·b·l) check.",
"Load-carrying difference between a parallel key and a Woodruff key.",
"Check whether it is below the allowable value.",
"Parallel key",
"T=100 N·m=100000 N·mm, shaft d=20, key h=12, b=6, working length l=40: σp=4×100000/(20×12×40)=400000/9600=41.7 MPa; τ=2×100000/(20×6×40)=200000/4800=41.7 MPa. Allowable about [σp]=120, [τ]=90, satisfied.",
"Lengthened key",
"l 40→60: σp=4×100000/(20×12×60)=27.8 MPa, giving more margin.",
"Why check both crushing and shear?",
"The key simultaneously bears hub-on-key-side crushing (working face) and shear of the key cross-section; either can be the failure mode, so both must be checked separately.",
"Is l the full length?",
"Use the working length (excluding the end fillet/chamfer), slightly less than the total key length; otherwise the strength is overestimated.",
'About "Key Joint Strength"',
"A key joint strength verification calculator: from the shaft diameter, key dimensions and transmitted torque it computes the crushing stress and shear stress of a parallel key's working face and compares them with the material allowable values to judge whether the key joint meets the strength requirement.",
"Dual crushing and shear check",
"Supports round-ended / square-ended parallel keys",
"Custom allowable stress",
"Shaft-hub joint design",
"Parallel key selection verification",
"Reducer shaft key verification",
"Machine element course design",
],
'strength-7': [
"🧮 Riveted Joint Strength Calculator",
"Enter the rivet diameter, plate thickness, rivet count, plate width and load to check the shear, crushing and tearing strength and compute the riveted joint efficiency",
'📖 View the "Riveted Joint Strength Calculator Guide"',
"Riveted shear τ = F/(n·πd²/4)",
"Rivet diameter d (mm)",
"Rivet count n",
"Plate width W (mm)",
"Load F (kN)",
"Allowable crushing stress [σc] (MPa)",
"Allowable tensile stress [σt] (MPa)",
"💡 Formula: shear stress τ=F/(n·π·d²/4); crushing stress σc=F/(n·d·t); tearing stress σt=F/((W-n·d)·t); joint efficiency η=minimum breaking force/(W·t·[σt])×100%",
"The rivet diameter is usually 1.5-2.5 times the plate thickness, commonly 8-24 mm",
"Single shear suits a single lap; double shear (double cover plate) doubles the shear area",
"Rivet arrangement should meet the detailing requirements of edge distance ≥1.5d and pitch ≥3d",
"The allowable stress is selected by material and conditions; steel rivets commonly use [τ]=90-100 MPa",
"This tool computes for single-shear lap; for double shear, manually double d equivalently",
"📚 In-Depth Analysis: Pin / Rivet Joint Strength",
"Shear τ=F/As, crushing σc=F/Ab, tearing σt=F/A_net check.",
"Determine the failure mode (shear/crushing/tearing controlled).",
"Safety margin sf=allowable/actual.",
"Single-shear pin",
"F=8 kN, pin diameter d=10, plate thickness t=8, n=1: As=π·d²/4·n=78.54 mm²; τ=8000/78.54=101.9 MPa; Ab=d·t·n=80 mm²; σc=8000/80=100 MPa. With [τ]=120 and [σc]=150, shear controls but is satisfied.",
"Double shear",
"n=2: As=157.1, τ=50.9 MPa, doubling the strength.",
"Difference between single and double shear?",
"Single shear has one shear plane and double shear two; double shear doubles the shear area and gives higher load capacity, used for thick-plate connections.",
"What is tearing?",
"The plate tears at the hole edge (net section), A_net=(plate width−d)·t; when the edge distance is insufficient, tearing controls.",
'About "Riveted Joint Strength Calculator"',
"A riveted joint strength calculator: from the rivet diameter, plate thickness, rivet count, plate width and external load it computes the shear stress, crushing stress and tearing stress of the joint and derives the load capacity of each failure mode and the joint efficiency, aiding riveted joint design verification.",
"Comprehensive check of three failure modes (shear/crushing/tearing)",
"Automatically determines the weakest failure mode and gives the controlling type",
"Computes the joint efficiency, directly reflecting connection economy",
"Supports custom allowable stress for different materials",
"Steel structure riveted connection design",
"Boiler and pressure vessel riveted joint verification",
"Strength verification of riveted joints in bridges and lifting equipment",
"Riveting scheme comparison for mechanical structures",
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

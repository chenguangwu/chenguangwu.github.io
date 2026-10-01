#!/usr/bin/env python3
# machinery batch2 (5 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'machinery')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'machinery')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'calc-89': [
"🧮 Clutch Calculator",
"Enter the friction-disc dimensions, friction coefficient, spring force, number of friction surfaces and speed to compute the clutch's transmitted torque and power",
'📖 View the "Clutch Calculator Guide"',
"Clutch torque T = μ·F·R·Z",
"Friction disc outer diameter D (mm)",
"Friction disc inner diameter d (mm)",
"Number of friction surfaces z",
"💡 Formula: mean radius Rm=(D+d)/4; transmitted torque T=μ·F·Rm·z; contact pressure p=F/[π(D²-d²)/4]; power P=T·n/9550",
"Number of friction surfaces z: for a single-disc friction clutch z=2 (one pair of friction surfaces); for multi-disc, count the actual number of friction surfaces",
"Friction coefficient μ reference values: asbestos-based material 0.25-0.35, powder metallurgy 0.30-0.40, carbon-based material 0.20-0.30",
"The allowable contact pressure [p] is generally 0.1-0.3 MPa (wet) or 0.2-0.4 MPa (dry)",
"The calculation assumes an ideal state; in practice wear, thermal effects and a safety factor must be considered",
"📚 In-Depth Analysis: Flange Contact Pressure",
"Verify the flange contact pressure under bolt preload, p=W/A.",
"Combine with the PV value to judge whether higher tightening or a larger sealing surface is needed.",
"Check whether the seal contact pressure meets the gasket requirement.",
"Annular sealing surface",
"Seal outer diameter D=100, inner diameter d=60 mm, area A=π(D²−d²)/4=π(10000−3600)/4≈5026.5 mm²; bolt preload W=10 kN: p=W/A=10000/5026.5≈1.99 MPa.",
"PV value",
"If the relative sliding speed v=2 m/s: PV=p·v=1.99×2≈3.98 MPa·m/s. If it exceeds the gasket's allowable PV, enlarge the sealing surface or reduce the preload.",
"What is the difference between contact pressure and PV?",
"Contact pressure p is a static clamping stress; PV is p × speed, reflecting the frictional heat-generation power density, and is critical for dynamic seals (such as rotating shafts).",
"How is the preload determined?",
"Set it from the minimum seal contact pressure required by the gasket and the bolt",
"specification; too tight crushes the gasket, too loose causes leakage.",
'About "Clutch Calculator"',
"A clutch torque calculator: based on the friction-disc geometry, friction coefficient, spring clamping force and number of friction surfaces, it computes the maximum torque, power and contact pressure the clutch can transmit, for clutch design and selection verification.",
"Computes transmitted torque and power together",
"Automatically evaluates the contact pressure",
"Supports entering a multi-surface count",
"Friction clutch design",
"Automotive drivetrain selection",
"Machine-tool clutch verification",
"Mechanical transmission teaching",
"Friction disc outer diameter",
"Friction disc inner diameter",
"Number of friction surfaces",
],
'calc-gear': [
"🧮 Standard Gear Parameter Calculator",
"Supports basic parameter calculation for standard spur/helical cylindrical gears (GB/T 1356)",
'📖 View the "Standard Gear Parameter Calculator Guide"',
"Standard gear d = m·z",
"Spur cylindrical gear",
"Helical cylindrical gear",
"💡 Formula: pitch circle d=mz; base circle db=d·cosα; addendum circle da=d+2ha; dedendum circle df=d-2hf; circular pitch p=πm. Helical gears are computed with the normal module mn.",
"This tool applies to standard involute cylindrical gears (standard tooth system ha*=1, c*=0.25)",
"For helical gears enter the normal module mn; the helix angle β cannot be 0",
"Minimum number of teeth to avoid undercutting for standard gears: spur zmin=17, helical zmin=17·cos³β",
"Results are for reference only; for actual design consult the GB/T 1356 standard",
"📚 In-Depth Analysis: Gear Parameter Calculation",
"Enter the module, number of teeth and pressure angle to output the full gear geometry (pitch circle, base circle, addendum/dedendum circles, tooth thickness, base pitch).",
"Switch between spur and helical (transverse module, base pitch).",
"Check undercutting and addendum thickness.",
"m=2, z=20, α=20° spur",
"Helical transverse plane",
"Normal module 2, β=20°: mt=2/cos20°=2.128, pt=π·mt=6.685, pb=pt·cosα.",
"What is the relationship between the base pitch pb and the circular pitch p?",
"pb=p·cosα, the normal distance between adjacent same-side tooth profiles on the base circle, equal to the pitch projection used in contact-ratio calculation.",
"Default module / pressure angle?",
"This tool defaults to m=2 and α=20° (the most common) and both can be changed; helical gears also require the helix angle.",
"Module",
"Number of teeth",
"Pressure angle",
"Helix angle",
"Addendum coefficient",
"Clearance coefficient",
],
'calc-gear-1': [
"⚙️ Gear Basic Parameter Calculator",
"Enter the module, number of teeth and pressure angle to compute the pitch circle, addendum circle, dedendum circle and base circle of a standard spur cylindrical gear",
'📖 View the "Gear Basic Parameter Calculator Guide"',
"Gear module m = d/z",
"💡 Formula: d=mz; da=m(z+2); df=m(z-2.5); db=d·cosα; pitch p=πm; tooth thickness s=πm/2",
"This calculation applies to standard spur cylindrical gears (addendum coefficient ha*=1, clearance coefficient c*=0.25)",
"The standard pressure angle is usually 20°; special cases use 14.5°, 25° or 30°",
"The number of teeth z should not be less than the minimum (for standard gears at 20° the minimum without undercutting is 17)",
"Profile-shifted gears require separate calculation; this tool supports standard gears only",
"📚 In-Depth Analysis: Cylindrical Gear Geometry Parameters",
"Find the pitch circle, addendum/dedendum circles and base circle from the module m, number of teeth z and pressure angle α.",
"Judge whether a standard gear with z<17 will undercut.",
"Check whether the addendum thickness is too thin.",
"d=m·z=40 mm; da=m(z+2)=44; df=m(z−2.5)=35; db=d·cosα=40×0.9397=37.59; pitch p=π·m=6.283; pitch-circle tooth thickness s=π·m/2=3.142 mm.",
"Undercutting check",
"z=15<17: a standard gear (α=20°) has an undercutting risk and needs profile shifting or more teeth; z=20 does not undercut.",
"Why does z<17 undercut?",
"When machined with a standard rack-type cutter, a gear with fewer than the minimum number of teeth zmin≈17 (α=20°) has its tooth root cut away, weakening the bending strength.",
"What is the base circle for?",
"The involute is generated from the base circle, and the line of action coincides with the common tangent to the base circles; the base circle determines the pressure angle and transmission smoothness.",
'About "Gear Basic Parameter Calculator"',
"A gear basic parameter calculator: from the three basic parameters of module, number of teeth and pressure angle, it computes the pitch circle, addendum circle, dedendum circle, base circle diameter and the tooth thickness and pitch of a standard spur cylindrical gear, a fundamental tool for gear design.",
"One-click computation of all geometry parameters",
"Automatic undercutting-risk check",
"Supports a custom pressure angle",
"Gear geometry design",
"Gear surveying and reverse engineering",
"Theory of machines and mechanisms teaching",
"Gear machining parameter verification",
"Module",
"Number of teeth",
"Pressure angle",
],
'calc-gear-3': [
"⚙️ Gear Type Calculator",
"Select the gear type (spur/helical/bevel) and enter the corresponding parameters to compute the geometry",
'📖 View the "Gear Type Calculator Guide"',
"Gear parameter = standard module series",
"Gear type",
"Straight bevel gear",
"Normal module mn (mm)",
"Pressure angle αn (°)",
"Large-end module m (mm)",
"Pinion tooth count z1",
"Gear tooth count z2",
"💡 Spur: d=mz; da=m(z+2); df=m(z-2.5); db=d·cosα",
"Spur cylindrical gear: standard gear, addendum coefficient ha*=1, clearance coefficient c*=0.25",
"Helical cylindrical gear: the helix angle β is usually 8°-20°; too small gives a low axial force but poor smoothness, too large gives a high axial force",
"Straight bevel gear: the large-end module is the standard, and the pitch cone angle is determined by the tooth ratio",
"The bevel gear face width b is usually taken as 1/3 of the cone distance R",
"📚 In-Depth Analysis: Bevel / Helical Gear Geometry",
"Geometry parameter calculation for spur, helical and bevel gears.",
"Determination of the bevel gear cone distance R, mean module mm and face width b.",
"Helical gear dimensions with the transverse module mt and helix angle β.",
"Pinion z1=20, gear z2=40, module m=3, face width b=30: d1=m·z1=60, d2=120; cone distance R=√(d1²+d2²)/2=√(3600+14400)/2=√(18000)/2≈67.08 mm; mean module mm=m(1−b/(2R))=3(1−30/134.16)=3×0.776≈2.33 mm.",
"Helical gear transverse module",
"Normal module mn=2, helix angle β=15°: transverse module mt=mn/cosβ=2/0.9659≈2.07 mm; d=mt·z.",
"What is the role of the cone distance R?",
"The cone distance is the slant length of the pitch cone; it determines the gear size and the upper limit of the face width (b is usually ≤R/3) and affects the contact strength.",
"Why is the mean module smaller than the large-end module?",
"For a bevel gear the module increases along the face width from the small end to the large end; the mean module is the representative value used for strength checking.",
'About "Gear Type Calculator"',
"A gear type calculator supporting spur cylindrical, helical cylindrical and straight bevel gears; according to each type's parameter characteristics it computes the pitch circle, addendum circle, dedendum circle, equivalent number of teeth, cone distance and other geometry.",
"One-click switching between three gear types",
"Helical gears include equivalent tooth-count calculation",
"Bevel gears include pitch cone angle and cone distance calculation",
"Multi-type gear design and selection",
"Reducer gear parameter calculation",
"Mechanical transmission scheme comparison",
"Theory of machines and mechanisms teaching demonstration",
],
'calc-lifespan-belt': [
"🧮 Belt Drive Calculator (Mechanical Manufacturing)",
"Geometry parameters and mechanics calculation for an open belt drive",
'📖 View the "Belt Drive Calculator (Mechanical Manufacturing) Guide"',
"Belt life = f(tension, speed)",
"Small pulley diameter D₁ (mm)",
"Large pulley diameter D₂ (mm)",
"Small pulley speed n₁ (r/min)",
"Belt type",
"V-belt (friction coefficient μ≈0.51)",
"Flat belt (μ≈0.3)",
"Timing belt (tooth engagement)",
"💡 Belt length L≈2a+π(D₁+D₂)/2+(D₂-D₁)²/4a; wrap angle α₁=180°-2·arcsin((D₂-D₁)/2a)×57.3°. The small-pulley wrap angle should be ≥120°.",
"📚 In-Depth Analysis: Belt Drive Life / Belt Length",
"Find the V-belt datum length L from the center distance and pulley diameters.",
"Estimate the number of belts or the life from the power and speed.",
"Check whether the belt length is within the standard series.",
"Open belt length",
"Center distance a=500 mm, small pulley D1=100, large pulley D2=200: L≈2a+π(D1+D2)/2+(D2−D1)²/(4a)=1000+π×150+(100)²/2000=1000+471.2+5=1476.2 mm. Choose the nearest standard belt length from the 1400 or 1500 series.",
"Belt count estimation",
"Rated power per belt 1.5 kW, transmitted power 5 kW, service factor 1.2: required number of belts = 5×1.2/1.5 = 4.",
"Why does the belt-length formula include (D2−D1)²/4a?",
"It is a geometric correction term after unfolding the wrap angle; it cannot be neglected when the two pulleys differ in diameter, ensuring the belt length matches the actual routing path.",
"What affects the V-belt life?",
"Tension, wrap angle, speed (5-25 m/s recommended), temperature rise and alignment; a too-small wrap angle needs an idler pulley.",
"Small pulley diameter",
"Large pulley diameter",
"Center distance",
"Small pulley speed",
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

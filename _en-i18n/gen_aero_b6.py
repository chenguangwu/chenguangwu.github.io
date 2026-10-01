#!/usr/bin/env python3
# aerospace batch6 (6 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'aerospace')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'aerospace')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'thrust-required': [
"Level Flight T = D",
"Thrust Required",
"/ Thrust Required",
'📖 View the "Level Flight T = D Guide"',
"Reference area S (m²)",
"In level flight thrust equals drag.",
"It shares the dynamic-pressure term with lift.",
"📚 In-Depth Analysis: Level Flight T = D",
"Level-flight trim requires thrust = drag; compute the required thrust T=D=½ρV²·C_D·S from the drag equation.",
"Compare the thrust required at different altitudes (density falls) to assess the cruise thrust setting.",
"Given the available engine thrust, back-calculate the achievable cruise speed.",
"Cruise thrust required",
"Cruise altitude density ρ=0.4, speed V=250 m/s, C_D=0.03 and area S=30 m². T=D=½×0.4×250²×0.03×30=½×0.4×62500×0.03×30=1125 N. The engine must continuously provide about 1.1 kN to maintain level flight.",
"What is the relationship between thrust required and thrust available?",
"In level flight/steady speed they are equal; accelerating or climbing needs available > required (the surplus accelerates/climbs); required > available means decelerating and losing altitude. The performance envelope is the range over which available thrust covers required thrust.",
"How does altitude affect the thrust required?",
"Density falls with altitude, so drag at the same true speed decreases, but cruising at a higher true speed to maintain dynamic pressure may offset it; overall the cruise thrust first falls with altitude then is affected by engine decay. Checking the performance manual by altitude is most accurate.",
],
'reynolds-number': [
"Reynolds Number from Density, Speed, Characteristic Length and Viscosity",
"Enter the air density ρ, speed v, characteristic length L and dynamic viscosity μ to find the Reynolds number.",
'📖 View the "Reynolds Number Guide"',
"Characteristic length L (m)",
"Re determines the laminar/turbulent state.",
"📚 In-Depth Analysis: Reynolds Number from Density, Speed, Characteristic Length and Viscosity",
"Reynolds number Re=ρvL/μ, judging the flow regime (laminar/turbulent) and aerodynamic/hydrodynamic similarity.",
"Wind-tunnel tests match Re to ensure the model and the real flow are similar.",
"Assess the effect of boundary-layer transition (laminar to turbulent) on drag.",
"Wing-section Reynolds number",
"Air density ρ=1.225, speed v=50 m/s, characteristic length L=2 m and dynamic viscosity μ=1.81×10⁻⁵ Pa·s. Re=1.225×50×2/1.81e-5≈6.77×10⁶. At this magnitude the wing surface usually has a turbulent boundary layer.",
"Is a high or low Reynolds number better?",
"Neither is absolutely better: a high Re (high speed/large size/low viscosity) tends to turbulence with higher friction drag but controllable separation; a low Re (such as micro UAVs, models) is mostly laminar with viscosity dominating. The key is to match the model and the real object at the same order of Re to ensure similarity.",
"What should the characteristic length L be?",
"Take a length representative of the flow: chord for a wing, diameter for a cylinder, and the ",
"hydraulic diameter",
" for a pipe. A wrong L can change Re by a factor of several and lead to a wrong flow-regime judgement.",
],
'orbital-velocity': [
"Velocity from Gravitational Parameter and Orbital Radius",
"Enter the gravitational parameter μ and orbital radius r to find the circular orbital velocity.",
"/ Circular Orbital Velocity Calculator",
'📖 View the "Velocity from Gravitational Parameter and Orbital Radius Guide"',
"Low Earth orbit is about 7.7 km/s.",
"📚 In-Depth Analysis: Velocity from Gravitational Parameter and Orbital Radius",
"Circular orbital velocity v=√(μ/r), used for orbit-insertion velocity planning.",
"Compare low-orbit/high-orbit velocities to assess the Δv needed for orbital changes.",
"From the target orbital altitude, back-calculate the velocity to be reached.",
"Low Earth circular orbital velocity",
"Orbital radius r=6.77×10⁶ m and μ=3.986×10¹⁴, so circular orbital velocity v=√(3.986e14/6.77e6)=√(5.89e7)≈7672 m/s ≈ 7.67 km/s. That is, on the order of the first cosmic velocity.",
"How do I remember the orbital velocity and the ",
"escape velocity",
"?",
"Circular orbit v_c=√(μ/r), escape v_e=√2·v_c. Near Earth v_c≈7.9 km/s and v_e≈11.2 km/s. To leave Earth you need to accelerate from the orbital velocity by Δv≈3.3 km/s (ideal, excluding losses).",
"Is the actual orbit-insertion velocity just this value?",
"The theoretical circular orbital velocity is so, but a rocket inserting along a transfer orbit has a combination of velocity direction and magnitude and includes gravity/drag losses. This tool gives the ideal circular orbital velocity baseline.",
],
'drag-force': [
"Drag from Dynamic Pressure, Drag Coefficient and Area",
"Enter the air density ρ, speed v, drag coefficient C_D and reference area A to find the drag.",
"Drag Calculator",
"/ Drag Calculator",
'📖 View the "Drag Guide"',
"Reference area A (m²)",
"Drag is proportional to the square of the speed.",
"📚 In-Depth Analysis: Drag from Dynamic Pressure, Drag Coefficient and Area",
"Estimate flight drag from the drag equation D=½ρv²·C_D·A, used to trim thrust.",
"Compare the drag change at different C_D (shape/flaps) or speeds for a drag-reduction assessment.",
"Given the available thrust, back-calculate the achievable cruise speed ceiling.",
"Cruise drag estimate",
"Air density ρ=1.225 kg/m³, speed v=100 m/s, drag coefficient C_D=0.03 and reference area A=30 m². Dynamic pressure q=½×1.225×100²=6125 Pa; D=q×C_D×A=6125×0.03×30≈5513 N.",
"Are both parasite and induced drag included in C_D?",
"The total drag coefficient C_D = C_D0 (parasite, rising with speed squared) + C_Di (induced, rising with lift squared). This tool uses the total C_D you provide; to break it down, substitute the zero-lift drag and induced-drag components separately.",
"Which area should the reference area A be?",
"Usually the wing reference area (the wing planform projection), consistent with the C_D and lift-coefficient system. Different references may use the wetted area, so it must match the coefficient or the result differs by a factor of several.",
],
'stall-speed': [
"Stall Speed",
"Stall speed is determined by the maximum lift coefficient.",
'📖 View the "Stall Speed Guide"',
"Area S (m²)",
"The greater the weight, the higher the stall speed.",
"High-lift devices raise C_Lmax and lower V_s.",
"📚 In-Depth Analysis: Stall Speed",
"Compute the stall speed Vs=√(2W/(ρS·C_Lmax)) from the weight W, density ρ, area S and maximum lift coefficient C_Lmax.",
"Assess the takeoff/landing safety speed margin (usually 1.2-1.3 Vs).",
"Compare the stall-speed change at different weights/altitudes (densities).",
"Landing-configuration stall speed",
"Weight W=60000 N, density ρ=1.225, area S=20 m² and C_Lmax=1.5. Vs=√(2×60000/(1.225×20×1.5))=√(120000/36.75)=√3265≈57.1 m/s. The approach reference speed is about 1.3×Vs≈74 m/s.",
"Why is the stall speed higher when heavier?",
"To keep L=W, a greater weight needs a higher speed (or a larger C_L). So a fully loaded aircraft stalls more easily at low speed, and takeoff/landing must compute Vs at the maximum landing weight and leave a margin.",
"Does altitude affect the stall speed?",
"It does. At high altitude the density is low, so at the same weight a higher true speed is needed to produce the same lift, so the stall true speed rises with altitude; but the stall indicated airspeed (IAS) is essentially unchanged, because IAS is proportional to dynamic pressure.",
],
'orbital-period': [
"Orbital Period from Orbital Radius",
"Enter the gravitational parameter μ and orbital radius r to find the orbital period.",
"Orbital Period Calculator",
"/ Orbital Period Calculator",
'📖 View the "Orbital Period from Orbital Radius Guide"',
"The low Earth orbit period is about 90 minutes.",
"📚 In-Depth Analysis: Orbital Period from Orbital Radius",
"Compute the period T=2pi√(r³/μ) from the gravitational parameter μ and orbital radius r, used for satellite pass planning.",
"Compare the periods at different altitudes (LEO/geosynchronous) to arrange constellation phasing.",
"Given a period target (such as sun-synchronous), back-calculate the required orbital radius.",
"Low Earth orbit period",
"Orbital radius r=6.77×10⁶ m (about 400 km altitude) and Earth μ=3.986×10¹⁴. T=2pi√((6.77e6)³/3.986e14)=2pi√(3.10e20/3.986e14)=2pi√(7.78e5)≈2pi×882≈5540 s≈92.3 min. That is, about one orbit of the Earth every 92 minutes.",
"Is the period longer or shorter at higher orbit?",
"Longer. By Kepler's third law T is proportional to r^(3/2), so doubling the altitude markedly increases the period; geosynchronous orbit r≈4.2×10⁷ m has a period ≈24 h, synchronous with the rotation of the Earth.",
"How is an elliptical orbit period calculated?",
"Use the semi-major axis a in place of r (T=2pi√(a³/μ)); it is independent of the shape and depends only on the semi-major axis. This tool computes with the circular orbital radius r; for an ellipse substitute the semi-major axis.",
],
}

# term-link nodes missed by extract: zh -> en
EXTRA = {}

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
    out = {'slug': slug, 'industry': 'aerospace', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

for slug, en_list in EN.items():
    write(slug, build(slug, en_list))

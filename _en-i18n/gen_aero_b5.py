#!/usr/bin/env python3
# aerospace batch5 (6 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'aerospace')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'aerospace')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'lift-to-drag-ratio': [
"Aerodynamic Efficiency",
"/ Lift-to-Drag Ratio",
"Lift-to-drag ratio",
'📖 View the "Aerodynamic Efficiency Guide"',
"The higher the L/D ratio, the more fuel-efficient.",
"Gliders can reach 40+.",
"📚 In-Depth Analysis: Aerodynamic Efficiency",
"Compute the lift-to-drag ratio (L/D)=C_L/C_D from the lift coefficient C_L and drag coefficient C_D, measuring ",
"Find the speed at maximum L/D, the point of farthest glide/longest range.",
"Compare the glide ratio of different configurations (clean/with landing gear/flaps).",
"Cruise lift-to-drag ratio",
"Lift coefficient C_L=0.8 and drag coefficient C_D=0.04, so the L/D ratio = 0.8/0.04 = 20. That is, for every 1 unit of altitude lost the aircraft travels about 20 units of distance (glide ratio about 20:1), a typical transport cruise level.",
"Is a larger L/D ratio always better?",
"It is better for range/glide, but it is not the only goal. Pursuing a very high L/D often needs a high ",
"aspect ratio",
", sacrificing speed and manoeuvrability; fighters conversely want a lower L/D for high speed. Trade off by mission.",
"What speed does the maximum L/D correspond to?",
"It corresponds to the speed of minimum drag (the lowest point of the drag polar), which is also the best fuel-mileage point. Off it (faster or slower) the L/D falls and the range shortens.",
],
'lift-force': [
"Wing Lift",
"/ Lift Calculation",
"Lift calculation",
'📖 View the "Wing Lift Guide"',
"Lift L = ½ × ρ × V² × S × C_L, where ρ is air density (about 1.225 kg/m³ at sea level), V the airspeed (m/s), S the wing reference area (m²) and C_L the lift coefficient; dynamic pressure q = ½ρV², so L = q × S × C_L; in cruise lift equals weight (L = m × g), from which the required airspeed V = √(2mg ÷ (ρSC_L)).",
"Airspeed V (m/s)",
"Low-speed approximation treats the flow as incompressible.",
"C_L varies with angle of attack.",
"📚 In-Depth Analysis: Wing Lift",
"Compute the wing lift L=½ρV²·C_L·S from air density, airspeed, wing area and lift coefficient.",
"Trim calculation: the aircraft flies level when lift is about equal to weight, used for performance and load analysis.",
"Compare the lift required at different flight phases (takeoff high-lift, cruise, landing).",
"Landing-configuration lift",
"Landing density ρ≈1.225, airspeed V=70 m/s, area S=30 m² and flaps down C_L=1.8. L=½×1.225×70²×1.8×30 = ½×1.225×4900×1.8×30 ≈ 162 kN. High-lift devices help maintain enough lift at low speed for a safe landing.",
"How exactly is lift generated?",
"Essentially from the pressure difference caused by the airspeed difference between the upper and lower surfaces of the airfoil (Bernoulli + circulation). The lift coefficient C_L combines the angle of attack, flaps and shape into a single non-dimensional quantity, convenient for calculation with a unified equation.",
"How are lift and weight trimmed?",
"Steady level flight requires lift = weight. Increasing the load needs a larger C_L or speed, limited by stall and structure; beyond the envelope you must reduce load or adjust the CG.",
],
'lift-equation': [
"Lift from Dynamic Pressure, Lift Coefficient and Area",
"Enter the air density ρ, speed v, lift coefficient C_L and wing area A to find the lift.",
"Lift Equation Calculator",
"/ Lift Equation Calculator",
'📖 View the "Lift from Dynamic Pressure, Lift Coefficient and Area Guide"',
"Wing area A (m²)",
"Level flight requires lift to balance weight.",
"📚 In-Depth Analysis: Lift from Dynamic Pressure, Lift Coefficient and Area",
"The lift equation L=½ρv²·C_L·A, used for trim and performance calculation.",
"Compare the available lift at different C_L (increased when flaps are down) to assess takeoff and landing performance.",
"Given the weight to be balanced, back-calculate the required speed or C_L.",
"Cruise lift balance",
"Air density ρ=1.225, speed v=80 m/s, lift coefficient C_L=1.2 and area A=30 m². L=½×1.225×80²×1.2×30 = ½×1.225×6400×1.2×30 = 140,688 N ≈ 140.7 kN. Level flight when it just balances a weight of the same order.",
"How is the lift equation used at takeoff?",
"On the takeoff roll to the lift-off speed v, L≥W is required. Increase C_L (flaps) or speed to make L catch up with the weight; the ",
"Vs is exactly the minimum safe speed at which L=W (see the stall speed tool).",
"Which altitude value of ρ should be used?",
"Use the actual air density at the flight altitude; at sea level ρ≈1.225 and it falls markedly at cruise altitude. Lower density means less lift at the same speed, requiring a higher speed or a larger C_L (large wing area) to compensate.",
],
'descent-rate': [
"Descent rate = true airspeed × sin(flight path angle).",
"Descent Rate",
"/ Descent Rate",
'📖 View the "Descent Rate Guide"',
"True airspeed V (m/s)",
"Flight path angle γ (°)",
"A negative angle indicates descent.",
"Approaches commonly use a 3° glide path.",
"📚 In-Depth Analysis: Descent Rate",
"On approach and landing, compute the descent rate ROC=−V·sinγ from the true airspeed V and the flight path angle γ (negative on descent).",
"Compute the descent rate for a steady 3° approach glide path, matching ILS/visual approaches.",
"Given an allowable descent rate (such as 1000 ft/min), back-calculate the required true airspeed or flight path angle.",
"Descent rate for a 3° steady approach",
"True airspeed V=80 m/s and flight path angle γ=−3°. Descent rate ROC = −80×sin(−3°)= −80×(−0.0523)=4.19 m/s ≈ 825 ft/min. Within the common 700-1000 ft/min steady approach range.",
"Do descent rate and climb rate have opposite signs?",
"Yes, climb is positive and descent negative (defined along the lift direction). On approach you watch the absolute value (how fast the descent is); too large means the sink rate exceeds standard and needs a power reduction or a back-pressure correction.",
"Do true airspeed and ground speed affect the descent rate?",
"This formula uses true airspeed to compute the sink rate relative to the air; the sink relative to the ground is also affected by wind. Approach monitoring uses the descent rate from radar/radio altimeter.",
],
'breguet-range': [
"Breguet Range",
"The range formula for propeller aircraft.",
'📖 View the "Breguet Range Guide"',
"Takeoff weight (N)",
"Landing weight (N)",
"Range grows logarithmically with the lift-to-drag ratio.",
"Jets use the fuel-consumption-rate form.",
"📚 In-Depth Analysis: Breguet Range",
"Cruise range estimate for turbojet/turbofan aircraft: R=(V·L/D/g)·ln(Wi/Wf).",
"Compare the range gain from different ",
" values, guiding drag-reduction design.",
"Given a range target, back-calculate the required fuel fraction and takeoff weight.",
"Regional airliner cruise range",
"Cruise speed V=250 m/s, L/D=18, takeoff weight Wi=600000 N and landing weight Wf=500000 N. R=(250×18/9.81)×ln(600000/500000)=458.7×ln(1.2)≈458.7×0.1823≈83.6 (illustrative; note the unit should give metres, and this example uses a low L/D=18, so the result is illustrative). In practice use the real L/D and weights.",
"What are the assumptions of the Breguet formula?",
"It assumes steady cruise, approximately constant speed and L/D and fuel consumption proportional to thrust. It is quite accurate for turbofan cruise; for propeller or large speed-change segments it must be applied piecewise. The ln(Wi/Wf) term captures the cumulative effect of getting lighter and more efficient as it flies.",
"Why does the lift-to-drag ratio matter so much?",
"Range is proportional to L/D. Raising L/D from 15 to 20 (a 25% drag reduction) increases range proportionally, which is why airfoil/wetted-area drag reduction is highly valued.",
],
'aspect-ratio': [
"Aspect Ratio from Wingspan and Wing Area",
"Enter the wingspan b and wing area S to find the aspect ratio.",
"Aspect Ratio Calculator",
"/ Aspect Ratio Calculator",
'📖 View the "Aspect Ratio from Wingspan and Wing Area Guide"',
"Wingspan b (m)",
"Wing area S (m²)",
"A high aspect ratio favours gliding and fuel economy.",
"📚 In-Depth Analysis: Aspect Ratio from Wingspan and Wing Area",
"In preliminary wing design, compute the aspect ratio AR=b²/S from the wingspan b and wing area S to measure how slender the wing is.",
"Compare the induced-drag difference between gliders (high aspect ratio) and fighters (low aspect ratio) to aid selection.",
"Given a target AR and wing area, back-calculate the required wingspan and check whether the wingtip spacing exceeds the root limit.",
"Regional airliner aspect ratio",
"Wingspan b=10 m and wing area S=15 m², so aspect ratio AR = b²/S = 100/15 ≈ 6.67. This value is at the lower end of the common transport range of 7-9, indicating a somewhat short, stubby wing with slightly higher induced drag but a lighter structure.",
"What are the pros and cons of high and low aspect ratio?",
"A high aspect ratio (gliders can reach 30+) has low induced drag and high cruise efficiency, but a large structural slenderness, a heavy wing and unsuitability for high speed; a low aspect ratio (fighters 2-4) is structurally strong and suited to high-speed manoeuvring, but has high induced drag and a short range. Selection is a trade-off between cruise efficiency and manoeuvrability/speed.",
"Is it normal for the aspect ratio to come out as a decimal?",
"Yes, it is a non-dimensional ratio. Note the difference between the geometric aspect ratio and the effective aspect ratio (including winglet correction), the latter being larger. This tool computes by the geometric definition AR=b²/S.",
],
}

# term-link nodes missed by extract: zh -> en
EXTRA = {
'lift-equation': {'失速速度': 'stall speed'},
'breguet-range': {'升阻比 L/D': 'L/D ratio'},
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
    out = {'slug': slug, 'industry': 'aerospace', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

for slug, en_list in EN.items():
    write(slug, build(slug, en_list))

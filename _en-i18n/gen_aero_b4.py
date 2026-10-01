#!/usr/bin/env python3
# aerospace batch4 (6 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'aerospace')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'aerospace')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'turn-radius': [
"Coordinated Turn Radius",
"/ Turn Radius",
"Turn radius",
'📖 View the "Coordinated Turn Radius Guide"',
"The steeper the bank angle, the smaller the radius.",
"A steep bank needs a higher speed to maintain the horizontal component of lift.",
"📚 In-Depth Analysis: Coordinated Turn Radius",
"Coordinated turn radius R=V²/(g·tanφ): from the speed and the ",
"bank angle",
", find the turn radius.",
"Compare the radii at different bank angles to plan a standard turn or an emergency avoidance.",
"Given an airspace limit (radius ceiling), back-calculate the allowable speed or bank angle.",
"Coordinated turn radius at a 30° bank",
"Speed V=100 m/s and bank φ=30°. R=100²/(9.81×tan30°)=10000/(9.81×0.577)=10000/5.66≈1766 m. That is, at this speed and bank the turn diameter is about 3.5 km.",
"Why does a steeper bank give a smaller radius?",
"A steeper bank provides a larger horizontal ",
" component (n·sinφ), so the same speed turns in a tighter radius. But a steeper bank raises the load factor, so the occupants and structure bear more g.",
"What is a standard rate turn?",
"By civil aviation convention the turn rate is 3°/s (a full circle in about 2 minutes), corresponding to different bank angles at different speeds (about 15°-25°). This tool computes the actual radius and rate for the given speed and bank.",
],
'specific-impulse': [
"Specific impulse = thrust / (mass flow rate × g0).",
"Specific Impulse Isp",
"/ Rocket Specific Impulse",
"Rocket specific impulse",
'📖 View the "Specific Impulse Isp Guide"',
"Thrust F (N)",
"Mass flow rate mdot (kg/s)",
"The higher the specific impulse, the higher the propulsion efficiency.",
"Liquid hydrogen/oxygen can reach 450 s.",
"📚 In-Depth Analysis: Specific Impulse Isp",
"Compute the specific impulse Isp=F/(mdot·g0) from thrust F and mass flow rate mdot to measure engine efficiency.",
"Compare the specific-impulse magnitudes of chemical and electric propulsion for mission selection.",
"Given a target Isp and thrust, back-calculate the required propellant flow rate.",
"Specific impulse of a liquid hydrogen/liquid oxygen engine",
"Thrust F=1000 N and mass flow rate mdot=0.4 kg/s. Isp=1000/(0.4×9.81)=1000/3.924≈255 s. A typical LH2/LOX vacuum Isp can reach 440+ s; the higher it is, the greater the impulse per unit propellant.",
"Why is the unit of specific impulse seconds?",
"Isp=F/(mdot·g0) has the dimension of seconds, meaning the impulse per unit weight flow. The more seconds, the more propellant-efficient the engine. It can also be understood directly via the exhaust velocity v_e=Isp·g0 (m/s).",
"Is a higher specific impulse always better?",
"For Δv efficiency higher is better, but it is often accompanied by low thrust (electric propulsion) or a complex/expensive system (high chamber pressure, cryogenic propellants). Trade off efficiency, thrust and cost by mission.",
],
'payload-fraction': [
"Payload Fraction from Initial and Final Mass",
"Enter the initial mass m0 and final mass mf to find the payload fraction.",
"Payload fraction = (m0 − mf) / m0",
"/ Payload Fraction Calculator",
"Payload Fraction Calculator",
'📖 View the "Payload Fraction from Initial and Final Mass Guide"',
"Payload fraction = (m0−mf)/m0 × 100%",
"The higher the payload fraction, the higher the transport efficiency.",
"📚 In-Depth Analysis: Payload Fraction from Initial and Final Mass",
"For launch vehicles, compute the structural ratio mf/m0 and the payload fraction (m0−mf)/m0 from the initial mass m0 and final mass mf.",
"Assess the launch efficiency of different staging schemes.",
"Given a target payload fraction, back-calculate the allowable structural/propellant mass.",
"Rocket payload fraction",
"Initial mass m0=500 t and final mass mf=100 t. Structural ratio mf/m0=0.2; payload fraction=(500−100)/500=0.8 (in this example the final mass already includes the payload, illustrative; a real rocket payload fraction is often only 1%-4% depending on the number of stages).",
"Why is the payload fraction usually very small?",
"Most of the rocket mass is propellant and structure, and reaching orbit requires overcoming a huge Δv; according to the ",
", the payload fraction grows logarithmically with the mass ratio, so multiple stages, a light structure and a high specific impulse are all indispensable. 1%-4% is a common magnitude.",
"What is the difference between the structural ratio and the payload fraction?",
"The structural ratio mf/m0 is the final mass as a proportion of the initial mass (including payload + upper-stage remnants); the payload fraction refers specifically to payload/(total initial mass), measuring the cargo efficiency more directly - the same denominator but a different numerator.",
],
'load-factor': [
"Coordinated turn load factor n = 1/cos φ.",
"Load Factor n",
"/ Load Factor",
"Load factor",
'📖 View the "Load Factor n Guide"',
"At a 60° bank, n=2.",
"The structure must bear the corresponding g-load.",
"📚 In-Depth Analysis: Load Factor n",
"In a coordinated turn or manoeuvre, from the ",
"bank angle",
" φ, find the load factor n=1/cosφ (symmetric manoeuvre).",
"Given the structural limit load factor, back-calculate the allowable maximum bank angle or manoeuvre intensity.",
"Assess the additional load factor introduced by gusts.",
"Bank-angle load factor",
"Bank angle φ=60°, load factor n=1/cos60°=1/0.5=2. The aircraft and occupants bear 2g, a common manoeuvre range; if the structural limit is +2.5g, there is still 0.5g of margin.",
"What condition is n=1?",
"Level flight or a gentle turn at a small bank, where lift only balances weight and the occupants feel their normal weight. n>1 results from a pull-up/turn making lift greater than weight.",
"What are the consequences of exceeding the load factor limit?",
"Exceeding the limit load factor may cause permanent structural deformation or even failure. Airworthiness rules set positive/negative limits for each class of aircraft (such as +2.5/−1.0 for transports), and manoeuvres within the flight envelope must not exceed them.",
],
'bank-angle-load': [
"Manoeuvre Load Factor from Bank Angle",
"Enter the bank angle φ (degrees) to find the load factor.",
"Bank-Angle Load Factor Calculator",
"/ Bank-Angle Load Factor Calculator",
'📖 View the "Manoeuvre Load Factor from Bank Angle Guide"',
"Bank angle φ (degrees)",
"The greater the bank angle, the greater the lift required.",
"📚 In-Depth Analysis: Manoeuvre Load Factor from Bank Angle",
"In coordinated-turn design, from the ",
"bank angle",
" φ, find the load factor n=1/cosφ, used for structural strength checks.",
"Given the maximum load factor allowed for the aircraft (such as +2.5g), back-calculate the allowable maximum bank angle.",
"Compare the wing-loading change at different bank angles to aid manoeuvre planning.",
"Load factor at a 30° bank",
"Bank angle φ=30°, load factor n = 1/cos30° = 1/0.866 ≈ 1.155. That is, the aircraft bears about 1.155g, with ample structural margin. If n≤2.5g is required, the maximum bank is cos⁻¹(1/2.5)=66.4°.",
"Are load factor n and g-load the same thing?",
"Essentially synonymous: n is the load factor (lift/weight), n=1 (1g) in steady level flight and greater than 1 in a manoeuvre. Structural design checks against the limit load factor (such as +2.5/−1.0 for transports), and exceeding it is a structural risk.",
"What does this calculation ignore?",
"It assumes an ideal coordinated turn (no sideslip, symmetric pull-up) and excludes gust, discrete-gust increments and manoeuvre gradients. Actual airworthiness needs a fuller manoeuvre load envelope; this tool gives the theoretical baseline.",
],
'turn-rate': [
"Turn Rate",
"/ Turn Rate",
'📖 View the "Turn Rate Guide"',
"Turning (turn) performance: angular velocity ω = g·tanφ ÷ v, where φ is the bank angle and v the true airspeed; turn rate = ω × 180 ÷ π (°/s); turn radius R = v² ÷ (g·tanφ); load factor n = 1 ÷ cosφ; the steeper the bank, the faster the turn but the higher the load.",
"It is the reciprocal of the turn radius.",
"Fighters pursue a high turn rate.",
"📚 In-Depth Analysis: Turn Rate",
"Coordinated turn: ",
"angular velocity",
" ω=g·tanφ/V, finding how fast the turn is from the speed and bank.",
"Compare the turn rate at different speeds to plan a standard rate turn.",
"Assess whether the angle turned per unit time in a manoeuvre satisfies obstacle avoidance.",
"Coordinated turn angular velocity",
"Speed V=100 m/s and bank φ=30°. ω=g·tanφ/V=9.81×0.577/100≈0.0566 rad/s ≈ 3.24°/s. Close to the civil aviation standard rate turn (3°/s), suitable for instrument approach procedures.",
"What is the relationship between turn rate and turn radius?",
"ω=V/R: the smaller the radius or the higher the speed, the greater the angular velocity. This tool computes ω directly from V and φ; it complements the turn radius tool (one looks at how fast to turn, the other at how big a circle to turn).",
"Does a lower speed give a higher turn rate?",
"Yes, ω is proportional to 1/V. At the same bank a lower speed turns faster (higher angular velocity) but with a smaller radius. A low speed with a steep bank easily exceeds the structural load, so the load factor limit must be checked at the same time.",
],
}

# term-link nodes missed by extract: zh -> en
EXTRA = {
'turn-radius': {'向心力': 'centripetal force'},
'payload-fraction': {'齐奥尔科夫斯基公式': 'Tsiolkovsky rocket equation'},
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

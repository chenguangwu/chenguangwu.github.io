#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'dynamics')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'dynamics')
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
    out = {'slug': slug, 'industry': 'dynamics', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

def main():
    write('hooke-force', build('hooke-force', [
        "Spring Force from Stiffness and Deflection",
        "Enter stiffness k and deflection x to find the spring force magnitude.",
        "Spring Force Calculator",
        "/ Spring Force Calculator",
        "\U0001F4D6 View the \"Spring Force from Stiffness and Deflection Guide\"",
        "F = k\u00b7x (magnitude, directed opposite the deflection). k=200, x=0.1 \u2192 20 N.",
        "F = k\u00b7x (magnitude, directed opposite the deflection).",
        "\U0001F4DA In-depth Analysis: Spring Force from Stiffness and Deflection",
        "Spring loading: enter k and the stretch or compression to get the force magnitude and determine the restoring direction.",
        "Suspension systems: enter the deflection of a spring scale and work back from F=kx to the mass hanging on it.",
        "Classroom demo: show that spring force is proportional to deflection (within the elastic limit).",
        "Example: k=200 N/m, x=0.1 m, F=200\u00d70.1=20 N, directed toward the equilibrium position.",
        "What happens beyond the elastic limit?",
        "Once x grows past the elastic limit, F is no longer proportional to x, the spring may deform permanently and the formula breaks down. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "What are the units of k?",
        "N/m \u2014 the force needed per unit of deflection; the larger k is, the \"stiffer\" the spring. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "Are compression and extension the same?",
        "Within the elastic limit the formula is identical; only the sign of x differs, and the force always points toward equilibrium. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
    ]))

    write('impulse', build('impulse', [
        "The accumulation of force over time equals the change in momentum.",
        "Impulse Calculator",
        "/ Impulse",
        "Impulse",
        "\U0001F4D6 View the \"Impulse Calculator Guide\"",
        "Duration \u0394t (s)",
        "Units are equivalent to momentum, kg\u00b7m/s.",
        "\U0001F4DA In-depth Analysis: Impulse Calculator",
        "Cushioning design: enter the momentum change needed to slow something down and find how much a longer duration reduces the average impact force (as with airbags).",
        "Collision analysis: derive the momentum change from the pre- and post-impact velocities \u2014 that is the impulse received.",
        "Classroom demo: for the same momentum change, a longer duration means a smaller force.",
        "Example: a 1 kg object brought from 10 m/s to rest in 0.1 s gives \u0394p=10 kg\u00b7m/s and an average force F=\u0394p/\u0394t=100 N.",
        "Is impulse the same as work?",
        "No: impulse J=\u0394p (force \u00d7 time) changes momentum, while work W=\u0394E (force \u00d7 displacement) changes energy. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "Why does cushioning save lives?",
        "For a fixed momentum change, extending the duration \u0394t sharply lowers the average impact force F=\u0394p/\u0394t. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "What about a varying force?",
        "This tool uses the average force; the impulse of a varying force is the integral of force over time, and the result is the equivalent average. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
    ]))

    write('inclined-plane-accel', build('inclined-plane-accel', [
        "Downhill acceleration on an incline, with friction.",
        "Incline Downhill Acceleration Calculator",
        "/ Incline Acceleration",
        "Incline Acceleration",
        "\U0001F4D6 View the \"Incline Downhill Acceleration Calculator Guide\"",
        "a = g(sin\u03b8 \u2212 \u03bccos\u03b8). If \u03b8 is too small and \u03bc too large, it will not slide.",
        "If \u03b8 is too small and \u03bc too large, it will not slide down.",
        "\U0001F4DA In-depth Analysis: Incline Downhill Acceleration Calculator",
        "Sliding down an incline: enter the angle and friction coefficient to get the acceleration and judge whether the object accelerates (sin\u03b8>\u03bccos\u03b8).",
        "Conveying goods: enter parameters for a conveyor or ramp to estimate sliding, or the restraining force needed.",
        "Classroom demo: a larger angle raises the acceleration while greater friction lowers it.",
        "Example: \u03b8=30\u00b0, \u03bc=0.2, g=9.8, a=9.8\u00d7(0.5\u22120.2\u00d70.866)=9.8\u00d70.327\u22483.2 m/s\u00b2.",
        "Does the object always slide?",
        "It accelerates downward only when sin\u03b8>\u03bccos\u03b8 (that is tan\u03b8>\u03bc); otherwise it stays put or needs an external force. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "What if there is no friction?",
        "With \u03bc=0, a=g sin\u03b8 \u2014 the component along the incline sets the acceleration, independent of mass. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "Does mass affect the acceleration?",
        "For an ideal incline (no rolling) the acceleration is independent of mass; if rotational inertia (rolling) is taken into account it is slightly lower. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
    ]))

    write('index', build('index', [
        "\U0001F300 Dynamics Tools",
        "Dynamics",
        "Dynamics Tools",
        "Incline Downhill Acceleration Calculator",
        "Enter the incline angle, friction coefficient and gravity to compute the acceleration of an object sliding down an incline, for mechanics teaching and inclined-motion analysis.",
        "Angular Momentum Conservation Calculator",
        "Enter the initial and final states of moment of inertia and angular velocity, and use conservation of angular momentum I\u2081\u03c9\u2081=I\u2082\u03c9\u2082 to find the final angular velocity, for rotating systems (skaters, spinning tops).",
        "Point Mass Moment of Inertia Calculator",
        "Find the moment of inertia of a point mass from mass and radius",
        "Work-Energy Theorem Calculator",
        "Work-energy theorem calculator: enter mass and initial/final velocity to get the kinetic energy change (net work) via W=\u00bdm(v\u2082\u00b2\u2212v\u2081\u00b2), for work and energy analysis.",
        "Maximum Static Friction Calculator",
        "Enter the static friction coefficient and normal force to compute maximum static friction via f_max=\u03bcsN, for critical analysis of whether an object begins to slide.",
        "Banked Curve Design Speed Calculator",
        "Find the frictionless design speed from curve radius and banking angle",
        "Coefficient of Restitution Calculator",
        "Enter the velocities of two bodies before and after impact and compute the coefficient of restitution via e=(v\u2082\u2032\u2212v\u2081\u2032)/(v\u2081\u2212v\u2082) to judge how elastic the collision is (0 fully inelastic to 1 fully elastic).",
        "1D Elastic Collision Calculator",
        "Find post-collision velocities from masses and pre-collision velocities",
        "Find terminal velocity from the balance of gravity and drag",
        "Rotational Kinetic Energy Calculator",
        "Find rotational kinetic energy from moment of inertia and angular velocity",
        "Pendulum period calculator: enter pendulum length L and gravitational acceleration g to get the period via T=2\u03c0\u221a(L/g), for oscillation and timing analysis.",
        "Torque Calculator",
        "Enter force, lever arm and angle to compute torque via M=F\u00b7r\u00b7sin\u03b8, for levers, pivots and equilibrium analysis.",
        "Power Calculator",
        "Enter force and velocity (in the same direction) to compute power via P=Fv, for estimating mechanical work and motion power.",
        "Kinetic Friction Calculator",
        "Enter the kinetic friction coefficient and normal force to compute sliding friction via f=\u03bcN, for motion resistance and braking analysis.",
        "Perfectly Inelastic Collision Calculator",
        "Enter the masses and pre-collision velocities of two bodies and use momentum conservation to find the final velocity of a perfectly inelastic collision (common velocity), for collision analysis.",
        "Spring Force Calculator",
        "Spring force calculator: enter stiffness k and deflection x to get the force via F=k\u00b7x, for spring and elastic body analysis.",
        "Spring Potential Energy Calculator",
        "Enter spring stiffness and deflection to compute elastic potential energy via Ep=\u00bdkx\u00b2, for oscillation and energy storage analysis.",
        "Rotational Power Calculator",
        "Rotational power calculator: enter torque \u03c4 and angular velocity \u03c9 to get rotational power via P=\u03c4\u00b7\u03c9, for rotating machinery power analysis.",
        "Weight Force Calculator",
        "Enter mass and gravitational acceleration to compute weight via G=mg, supporting the g values of different celestial bodies for gravity comparison.",
        "Find the common velocity from masses and pre-collision velocities",
        "Angular Momentum Calculator",
        "Find angular momentum from moment of inertia and angular velocity",
        "Impulse Calculator",
        "Enter the applied force and duration (or the momentum change) to compute impulse via J=F\u00b7\u0394t=\u0394p, for mechanics analysis of collisions and impacts.",
        "Momentum Calculator",
        "Enter mass and velocity to compute momentum via p=mv, for comparing momentum magnitude and direction in motion and collisions.",
        "About \"Dynamics Tools\"",
        "The Dynamics tools collection gathers 23 free online tools covering the common calculations, conversions and lookups needed in dynamics work. Whether you are a practitioner in the field, a student or a casual user, you will find handy tools here that work the moment you open them. All tools run purely in the browser and no data is uploaded to a server, so your privacy stays safe.",
        "The dynamics tools listed on this page include (a selection of representative tools):",
        "These tools help you finish common dynamics tasks quickly, with no need to memorize complex formulas or convert values by hand \u2014 just enter them and get results.",
        "Do the dynamics tools need to be downloaded or registered?",
        "No. Every dynamics tool on this page is a pure front-end online tool \u2014 open the page and use it right away, with no software to install, no account to register, and no data uploaded.",
        "Are the dynamics tools' results accurate? Is my data safe?",
        "The tools compute locally in your browser using public formulas and common industry standards, so results appear instantly. All calculations run on your own device and no data is uploaded to a server, keeping your privacy secure.",
    ]))

    write('inelastic-collision', build('inelastic-collision', [
        "Find the Common Velocity from Masses and Pre-Collision Velocities",
        "Enter two masses and their pre-collision velocities to find the common velocity after they stick together.",
        "\U0001F4D6 View the \"Common Velocity from Masses and Pre-Collision Velocities Guide\"",
        "\U0001F4DA In-depth Analysis: Common Velocity from Masses and Pre-Collision Velocities",
        "Sticking collisions: enter the masses and pre-collision velocities of two bodies to find their common post-collision velocity.",
        "Capture processes: enter parameters for satellite capture, clay impacts and similar cases to estimate the merged body's velocity.",
        "Classroom demo: show that a perfectly inelastic collision loses the most kinetic energy (momentum is still conserved).",
        "Example: m\u2081=2, v\u2081=3, m\u2082=1, v\u2082=0, v=(2\u00d73+1\u00d70)/(2+1)=2 m/s \u2014 the combined body moves together at 2 m/s.",
        "Where did the kinetic energy go?",
        "A perfectly inelastic collision loses the most kinetic energy, converted into deformation, heat and sound; total momentum is still conserved. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "How is it different from an elastic collision?",
        "In an elastic collision the bodies separate and kinetic energy is conserved; in an inelastic one they share a velocity and kinetic energy is not conserved. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "How are opposite velocities handled?",
        "Substitute velocities with their signs (in one dimension); the sign of the result is the common direction of motion. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
    ]))


if __name__ == '__main__':
    main()

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
    write('power-force', build('power-force', [
        "Power when force and velocity point in the same direction.",
        "Power Calculator",
        "/ Power",
        "\U0001F4D6 View the \"Power Calculator Guide\"",
        "\U0001F4DA In-depth Analysis: Power Calculator",
        "Traction power: enter the running resistance and speed to find the power needed to hold a steady speed, helping with motor or engine selection.",
        "Mechanical output: enter force and speed for a conveyor or winch to get the output power.",
        "Classroom demo: at the same force, a higher speed means more power.",
        "Example: overcoming 500 N of resistance at a steady 10 m/s gives P=500\u00d710=5000 W=5 kW.",
        "What if force and velocity are not aligned?",
        "Use the component of force along the velocity: P=Fv cos\u03b8; the perpendicular component does no work and adds no power. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "How does it relate to work?",
        "Power is work per unit time, P=W/t; at constant speed W=Fd, so P=Fv (because d/t=v). Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "1 W = 1 J/s = 1 N\u00b7m/s; kW = 1000 W, commonly used for vehicles and",
        ". Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
    ]))

    write('power-rotational', build('power-rotational', [
        "Find Rotational Power from Torque and Angular Velocity",
        "Enter torque \u03c4 and angular velocity \u03c9 to find the rotational power.",
        "Rotational Power Calculator",
        "/ Rotational Power Calculator",
        "\U0001F4D6 View the \"Rotational Power from Torque and Angular Velocity Guide\"",
        "\U0001F4DA In-depth Analysis: Rotational Power from Torque and Angular Velocity",
        ": enter the output torque and speed to find the rotational power, supporting",
        "Drivetrains: enter the torque and",
        "angular velocity",
        "of gears or belts to get the transmitted power.",
        "Classroom demo: at the same torque, a higher speed means more power.",
        "Example: \u03c4=10 N\u00b7m, \u03c9=100 rad/s, P=10\u00d7100=1000 W=1 kW.",
        "How is rpm used?",
        "First convert with \u03c9=2\u03c0\u00b7rpm/60 (rad/s), then substitute into P=\u03c4\u03c9. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "How does it relate to P=Fv?",
        "The rotational form mirrors the translational one: \u03c4 corresponds to F and \u03c9 to v, both essentially force \u00d7 velocity. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "What are the units?",
        "\u03c4 in N\u00b7m, \u03c9 in rad/s and P in W; the radian is dimensionless. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
    ]))

    write('rotational-kinetic-energy', build('rotational-kinetic-energy', [
        "Find Rotational Kinetic Energy from Moment of Inertia and Angular Velocity",
        "Enter moment of inertia I and angular velocity \u03c9 to find the rotational kinetic energy.",
        "Rotational Kinetic Energy Calculator",
        "/ Rotational Kinetic Energy Calculator",
        "\U0001F4D6 View the \"Rotational Kinetic Energy from Moment of Inertia and Angular Velocity Guide\"",
        "\U0001F4DA In-depth Analysis: Rotational Kinetic Energy from Moment of Inertia and Angular Velocity",
        "Flywheel storage: enter moment of inertia and speed to get the rotational kinetic energy and understand a flywheel's storage capacity.",
        "Rotating body energy: enter parameters for a wheel or rotor to get the kinetic energy used in braking and cushioning design.",
        "Classroom demo: show that rotational kinetic energy grows with",
        "angular velocity",
        "squared.",
        "Example: I=0.5 kg\u00b7m\u00b2, \u03c9=20 rad/s, Ek=0.5\u00d70.5\u00d7400=100 J.",
        "Does it correspond to translational kinetic energy?",
        "Yes, it is the rotational counterpart: I matches m and \u03c9 matches v, so Ek=\u00bdI\u03c9\u00b2 mirrors \u00bdmv\u00b2. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "How much can a flywheel store?",
        "It depends on I and the maximum safe \u03c9; high-speed flywheels can store considerable energy, but material strength sets the limit. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "What are the units?",
        "J (joules), the same dimension as translational kinetic energy. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
    ]))

    write('spring-potential', build('spring-potential', [
        "Elastic potential energy stored in a deformed spring.",
        "Spring Potential Energy Calculator",
        "/ Spring Potential Energy",
        "Spring Potential Energy",
        "\U0001F4D6 View the \"Spring Potential Energy Calculator Guide\"",
        "Elastic potential energy U = \u00bd \u00d7 k \u00d7 x\u00b2, where k is the spring stiffness (N/m) and x the deflection (m); spring force F = k \u00d7 x; the energy grows with the square of the deflection, so doubling the deflection makes the energy four times larger (for example k = 200 N/m and x = 0.1 m give F = 20 N and U = 1 J).",
        "\U0001F4DA In-depth Analysis: Spring Potential Energy Calculator",
        "Spring storage: enter k and the compression or extension to get the stored elastic potential energy.",
        "Cushioning design: enter the deflection of a shock-absorbing spring to estimate the impact energy it can absorb.",
        "Classroom demo: show that the energy grows with the square of the deflection.",
        "Example: k=200 N/m, x=0.1 m, Ep=0.5\u00d7200\u00d70.01=1 J.",
        "How does it relate to the spring force formula?",
        "The spring force F=kx is the derivative of the potential, and the stored energy is the area integral Ep=\u00bdkx\u00b2. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "Are compression and extension the same?",
        "The formula contains only x\u00b2, so compression and extension store the same energy \u2014 the direction does not change the amount. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "What about going past the elastic limit?",
        "Beyond the limit the behaviour is nonlinear, \u00bdkx\u00b2 is no longer accurate, and permanent deformation may occur. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
    ]))

    write('static-friction-max', build('static-friction-max', [
        "The upper limit of static friction just before an object starts to slide.",
        "Maximum Static Friction Calculator",
        "/ Maximum Static Friction",
        "Maximum Static Friction",
        "\U0001F4D6 View the \"Maximum Static Friction Calculator Guide\"",
        "max = \u03bc_s\u00b7N. The static coefficient is usually greater than the kinetic one.",
        "Static friction coefficient \u03bc_s",
        "The static coefficient is usually greater than the kinetic one.",
        "\U0001F4DA In-depth Analysis: Maximum Static Friction Calculator",
        "Threshold to start moving: enter the normal force and \u03bcs to get the maximum static friction and see how large an external force is needed to move the object.",
        "Anti-slip check: enter parameters for a slope or a floor to judge whether the object will slide.",
        "Classroom demo: show that maximum static friction slightly exceeds kinetic friction, and that sliding begins once the external force reaches the limit.",
        "Example: N=200 N, \u03bcs=0.5, fs,max=0.5\u00d7200=100 N, so sliding starts only when the external force exceeds 100 N.",
        "Is static friction always equal to \u03bcsN?",
        "No \u2014 static friction varies between 0 and \u03bcsN along with the applied force; sliding is imminent only at the limit \u03bcsN. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "Which is larger, static or kinetic friction?",
        "Usually \u03bcs\u2265\u03bck, so breaking away takes the most force and slightly less is needed once the object is sliding. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "How should \u03bcs be chosen?",
        "It depends on the materials and their condition: dry clean surfaces give higher values, oiled or wet ones lower \u2014 rely on measured values. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
    ]))


if __name__ == '__main__':
    main()

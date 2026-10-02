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
    write('terminal-velocity', build('terminal-velocity', [
        "Find Terminal Velocity from the Balance of Gravity and Drag",
        "Enter mass m, g, \u03c1, Cd and A to find the terminal velocity.",
        "/ Terminal Velocity Calculator",
        "\U0001F4D6 View the \"Terminal Velocity Guide\"",
        "Terminal velocity is reached when mg = \u00bd\u03c1v\u00b2C_dA. Example \u2192 about 43.2 m/s.",
        "Terminal velocity is reached when mg = \u00bd\u03c1v\u00b2C_dA.",
        "Example \u2192 about 43.2 m/s.",
        "\U0001F4DA In-depth Analysis: Terminal Velocity from the Balance of Gravity and Drag",
        "Skydiving terminal velocity: enter the combined mass of jumper and canopy plus the drag parameters to get the steady descent speed and see how opening the chute slows the fall.",
        "Particle settling: enter parameters for dust or droplets to estimate the speed at which they settle in air.",
        "Classroom demo: show that drag increases with speed until it balances gravity, after which the speed stops rising.",
        "Example: m=80 kg, \u03c1=1.2, Cd=1.0, A=0.5, vt=\u221a(2\u00d780\u00d79.8/(1.2\u00d71.0\u00d70.5))\u2248\u221a(2613/0.6)\u2248\u221a(4355)\u224866 m/s (an approximation without a parachute).",
        "Why does the speed settle?",
        "As the fall speeds up, drag Fd=\u00bd\u03c1v\u00b2CdA grows; once it equals gravity the net force is zero and the object falls at constant speed. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "Why does opening the parachute slow the fall?",
        "Opening the canopy greatly increases A, so vt drops sharply and the descent continues at the new, much lower terminal speed, keeping the jumper safe. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "Does the medium matter?",
        "In water \u03c1 is much larger and vt far smaller; the same object settles far more slowly in water than in air. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
    ]))

    write('torque-force', build('torque-force', [
        "The turning effect of a force about an axis.",
        "Torque Calculator",
        "/ Torque",
        "Torque",
        "\U0001F4D6 View the \"Torque Calculator Guide\"",
        "\u03c4=rF at its maximum.",
        "At right angles \u03c4=rF is maximal.",
        "\U0001F4DA In-depth Analysis: Torque Calculator",
        "Wrenches: enter the lever arm and applied force to get the torque, and see why a longer wrench takes less effort.",
        "Lever balance: enter the torques on both sides of a lever to test the equilibrium condition (net torque zero).",
        "Classroom demo: a longer lever arm and a perpendicular force both give more torque.",
        "Example: r=0.3 m, F=100 N applied perpendicular (\u03b8=90\u00b0), \u03c4=0.3\u00d7100\u00d71=30 N\u00b7m.",
        "Is torque a vector?",
        "Yes \u2014 its direction follows the right-hand rule (r\u00d7F), giving a clockwise or counter-clockwise sense about the axis. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "Which angle is used?",
        "\u03b8 is the angle between the lever arm r and the force F; at 90\u00b0 sin\u03b8=1 and the torque is maximal. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "Are its units the same as those of work?",
        "Both come out in N\u00b7m, but torque is a vector (r\u00d7F) while work is a scalar (F\u00b7d), so they mean different things. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
    ]))

    write('weight-force', build('weight-force', [
        "The gravitational pull acting on an object.",
        "Weight Force Calculator",
        "/ Weight",
        "\U0001F4D6 View the \"Weight Force Calculator Guide\"",
        "Weight W = mass m \u00d7 gravitational acceleration g; standard gravity g = 9.80665 m/s\u00b2, with 9.81 m/s\u00b2 common in engineering; to convert to kilogram-force, W(kgf) = W(N) \u00f7 9.80665; surface gravity on the Moon is about 1/6 of Earth's and on Mars about 38%.",
        "\U0001F4DA In-depth Analysis: Weight Force Calculator",
        "Weighing and conversion: enter a mass to get the weight and understand the difference between mass and weight.",
        "Force analysis: enter an object's mass to get its weight, the basic force in any free-body diagram.",
        "Classroom demo: the same mass weighs differently under different g (Earth vs Moon).",
        "Example: m=70 kg, g=9.8, W=70\u00d79.8=686 N.",
        "Are mass and weight the same?",
        "No \u2014 mass is the amount of matter (kg, unchanged), while weight is the gravitational force (N, varying with local g). Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "How much does it weigh on the Moon?",
        "The Moon's g is about 1.6, so the same mass weighs roughly one sixth of its Earth weight. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "Is weight zero in weightlessness?",
        "In free fall or in orbit the apparent weight is zero (there is no supporting reaction), yet mass and gravity still exist. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
    ]))

    write('work-energy-theorem', build('work-energy-theorem', [
        "Find the Net Work from a Change in Velocity",
        "Enter mass and initial/final velocity to find the kinetic energy change (net work).",
        "Work-Energy Theorem Calculator",
        "/ Work-Energy Theorem Calculator",
        "\U0001F4D6 View the \"Net Work from a Change in Velocity Guide\"",
        "Initial velocity v\u2081 (m/s)",
        "Final velocity v\u2082 (m/s)",
        "\U0001F4DA In-depth Analysis: Net Work from a Change in Velocity",
        "Braking distance: enter the vehicle speed and the speed after braking, then use the kinetic energy change to find the net work required, supporting",
        "braking distance",
        "estimates.",
        "Impact analysis: enter the pre- and post-impact velocities to get the kinetic energy loss, that is the dissipated energy.",
        "Classroom demo: show that the net work equals the change in kinetic energy.",
        "Example: m=1000 kg, v\u2081=20, v\u2082=0, W=0.5\u00d71000\u00d7(0\u2212400)=\u2212200000 J, so braking dissipates 200 kJ.",
        "What does the theorem say?",
        "The work done by the net force on an object equals its change in kinetic energy: W=\u0394Ek, independent of the path and depending only on the initial and final velocities. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "What does negative work mean?",
        "When kinetic energy drops (as in braking) the net force does negative work and the energy is dissipated or transferred. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "How does it differ from the impulse theorem?",
        "The work-energy theorem links work and kinetic energy (scalars), while the impulse theorem links impulse and momentum (vectors): one concerns energy, the other momentum. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
    ]))


if __name__ == '__main__':
    main()

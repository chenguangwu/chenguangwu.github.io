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
    write('kinetic-friction', build('kinetic-friction', [
        "Sliding friction equals the kinetic friction coefficient times the normal force.",
        "Kinetic Friction Calculator",
        "/ Kinetic Friction",
        "Kinetic Friction",
        "\U0001F4D6 View the \"Kinetic Friction Calculator Guide\"",
        "Kinetic friction coefficient \u03bc_k",
        "Independent of contact area.",
        "\U0001F4DA In-depth Analysis: Kinetic Friction Calculator",
        "Sliding resistance: enter the normal force and \u03bck to get the sliding friction and the pull needed for constant speed.",
        "Braking analysis: enter ground friction parameters to get the deceleration resistance, supporting",
        "Classroom demo: show that kinetic friction is proportional to the normal force and independent of contact area.",
        "Example: N=100 N, \u03bck=0.3, fk=0.3\u00d7100=30 N, so pulling at constant speed must overcome 30 N of resistance.",
        "What is the difference between kinetic and static friction?",
        "Kinetic friction acts while surfaces slide relative to each other (fk=\u03bcN); static friction acts before sliding starts (\u2264\u03bcsN, varying with the applied force). Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "Does contact area matter?",
        "In the ideal model sliding friction is independent of contact area and depends only on the normal force and \u03bck. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "How large is \u03bck usually?",
        "It varies by material: roughly 0.1\u20130.3 between metals, and up to 0.6\u20131.0 for rubber on road; always rely on measured values. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
    ]))

    write('moment-of-inertia-point', build('moment-of-inertia-point', [
        "Find the Moment of Inertia of a Point Mass from Mass and Radius",
        "Enter mass m and radius of gyration r to find the moment of inertia.",
        "Point Mass Moment of Inertia Calculator",
        "/ Point Mass Moment of Inertia Calculator",
        "\U0001F4D6 View the \"Moment of Inertia of a Point Mass from Mass and Radius Guide\"",
        "\U0001F4DA In-depth Analysis: Moment of Inertia of a Point Mass from Mass and Radius",
        "Point mass rotation: enter mass and radius of gyration to get the moment of inertia and see that \"the farther the mass sits from the axis, the harder it is to turn\".",
        "Pendulum models: enter parameters for a simple or centrifugal pendulum to get the moment of inertia used in period and torque analysis.",
        "Classroom demo: at the same mass, doubling r makes I four times larger.",
        "Example: m=2 kg, r=0.5 m, I=2\u00d70.5\u00b2=0.5 kg\u00b7m\u00b2.",
        "Why is r squared?",
        "Moment of inertia reflects how far the mass is distributed from the axis; distant mass resists rotation more, hence the r\u00b2 weighting. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "How does it relate to a rigid body's I?",
        "A rigid body's I is the sum (integral) of mr\u00b2 over all its particles; this tool covers a single point mass or a lumped-mass model. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "What are the units?",
        "kg\u00b7m\u00b2, obtained from m (kg) and r\u00b2 (m\u00b2). Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
    ]))

    write('momentum-conservation', build('momentum-conservation', [
        "Perfectly Inelastic Collision Calculator",
        "Final velocity after sticking together.",
        "/ 1D Momentum Conservation",
        "1D Momentum Conservation",
        "\U0001F4D6 View the \"Perfectly Inelastic Collision Calculator Guide\"",
        "Final velocity of a perfectly inelastic collision.",
        "\U0001F4DA In-depth Analysis: Perfectly Inelastic Collision Calculator",
        "Collision systems: enter the masses and pre-collision velocities of several bodies to find the common post-collision velocity when the net external force is close to zero.",
        "Recoil processes: enter parameters for a shell leaving the barrel or a rocket's exhaust to estimate the recoil velocity.",
        "Classroom demo: show that the total momentum of a system stays constant when no external force acts.",
        "Example: m\u2081=3, v\u2081=4; m\u2082=2, v\u2082=\u22122 (opposite direction), system p=12\u22124=8, total mass 5, post-collision v=8/5=1.6 m/s.",
        "What are the conditions for conservation?",
        "Total momentum is conserved when the net external force on the system is zero; with significant external forces (such as strong ground friction) it does not hold strictly. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "and",
        "conservation of angular momentum",
        "conflict?",
        "No \u2014 they address different degrees of freedom: translation is described by linear momentum, rotation by",
        "angular momentum",
        ". Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "Is momentum conserved in an explosion?",
        "When internal forces far exceed external ones, momentum is approximately conserved even though kinetic energy increases (chemical energy is released). Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
    ]))

    write('momentum', build('momentum', [
        "The product of an object's mass and velocity.",
        "Momentum Calculator",
        "/ Momentum",
        "Momentum",
        "\U0001F4D6 View the \"Momentum Calculator Guide\"",
        "Momentum p = m \u00d7 v, where m is mass (kg) and v is velocity (m/s); kinetic energy Ek = \u00bd \u00d7 m \u00d7 v\u00b2; impulse F \u00d7 \u0394t equals the momentum change \u0394p; doubling the mass doubles the momentum, and doubling the velocity doubles the momentum while making kinetic energy four times larger (for example m = 1000 kg and v = 15 m/s give p = 15000 kg\u00b7m/s and Ek = 112500 J).",
        "A vector, pointing the same way as velocity.",
        "\U0001F4DA In-depth Analysis: Momentum Calculator",
        "Pre-collision quantities: enter the masses and velocities of two bodies to get the total momentum and judge whether the net external force on the system vanishes.",
        "Rocket principle: the ejected mass carries away momentum and the body gains an equal recoil momentum.",
        "Classroom demo: show that momentum changes linearly with velocity.",
        "Example: m=2 kg, v=3 m/s, p=2\u00d73=6 kg\u00b7m/s.",
        "Is momentum a vector?",
        "Yes, its direction is that of velocity; the total momentum of several bodies is the vector sum, and conservation means that vector sum stays unchanged. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "How does it differ from kinetic energy?",
        "Momentum p=mv is a vector, first power of v, while kinetic energy Ek=\u00bdmv\u00b2 is a scalar in v\u00b2; they serve different purposes. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "Does the reference frame matter?",
        "Velocity depends on the reference frame, so momentum does too; a conservation analysis must stay in one fixed inertial frame. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
    ]))

    write('period-pendulum', build('period-pendulum', [
        "Find the Pendulum Period from Length",
        "Enter pendulum length L and gravitational acceleration g to find the period.",
        "\U0001F4D6 View the \"Pendulum Period from Length Guide\"",
        "T = 2\u03c0\u221a(L/g) (small angles). L=1 m, g=9.81 \u2192 about 2.01 s.",
        "T = 2\u03c0\u221a(L/g) (small angles).",
        "L=1 m, g=9.81 \u2192 about 2.01 s.",
        "\U0001F4DA In-depth Analysis: Pendulum Period from Length",
        "Pendulum timing: enter the length to get the period and see how lengthening a pendulum clock changes its rate.",
        "Period comparison: compute T for different lengths to show T\u221d\u221aL (independent of mass and of amplitude at small angles).",
        "Classroom demo: doubling the length makes the period about 1.41 times longer.",
        "Example: L=1 m, g=9.8, T=2\u03c0\u221a(1/9.8)\u22482.01 s.",
        "Does the bob's mass matter?",
        "At small angles",
        "the pendulum period",
        "is independent of mass and depends only on length and g. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "Is it still accurate at large angles?",
        "At large amplitudes (say >15\u00b0) the period is slightly longer than the small-angle formula gives, and an elliptic-integral correction is needed. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
        "What if g is different?",
        "T\u221d1/\u221ag; on the Moon g is smaller, so the same length gives a longer period and the clock runs slow. Results are computed in real time from standard mechanics formulas for physics study, homework and engineering estimates; for safety-critical or real engineering work follow professional standards and measured data.",
    ]))


if __name__ == '__main__':
    main()

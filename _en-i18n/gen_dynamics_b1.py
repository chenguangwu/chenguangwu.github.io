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
    write('angular-momentum-conservation', build('angular-momentum-conservation', [
        "Find the final angular velocity from the initial state",
        "Enter the initial and final moments of inertia and the initial angular velocity to find the final angular velocity.",
        "Angular momentum conservation calculator",
        "/ Angular momentum conservation calculator",
        "📖 View the usage guide for Finding the final angular velocity from the initial state",
        "Conservation of angular momentum: L = I1 x w1 = I2 x w2, that is, the product of the moment of inertia and the angular velocity is conserved. If the moment of inertia decreases, the angular velocity increases in inverse proportion: w2 = I1 x w1 / I2. Rotational kinetic energy Ek = 0.5 x I x w^2; drawing the radius in increases the kinetic energy, and the difference comes from work done by internal forces.",
        "Initial inertia I1 (kg m^2)",
        "Initial angular velocity w1 (rad/s)",
        "Final inertia I2 (kg m^2)",
        "📚 Deep dive: finding the final angular velocity from the initial state",
        "Speeding up by drawing in the arms: enter the moments of inertia with the limbs extended and drawn in, plus the initial rotation rate, to find the rate after drawing in, as in figure skating.",
        "Celestial collapse: for a neutron star or stellar collapse, enter the initial and final moments of inertia to estimate how many times the spin rate increases.",
        "Teaching demonstration: show that w increases in inverse proportion as I decreases, verifying the conservation relation.",
        "Example: with I1 = 4 and w1 = 2 rad/s, and after drawing in I2 = 1, then w2 = I1 x w1 / I2 = 8 rad/s, so the rotation rate becomes four times as large.",
        "What are the conditions for conservation?",
        "It holds when the net external torque on the system is zero; it does not apply if there is significant friction or an external torque. Results are calculated in real time with standard mechanics formulas, for physics study, homework calculation and engineering estimation; for safety-critical or actual engineering work, follow professional standards and measured data.",
        "Does it conflict with conservation of energy?",
        "No.",
        "angular momentum",
        "When conservation holds,",
        "rotational kinetic energy",
        "often changes because I changes, since the kinetic energy comes from work done by internal forces. Results are calculated in real time with standard mechanics formulas, for physics study, homework calculation and engineering estimation; for safety-critical or actual engineering work, follow professional standards and measured data.",
        "Do the units have to be consistent?",
        "Use kg m^2 for I and rad/s for w; the result w is in rad/s, noting that the radian is dimensionless. Results are calculated in real time with standard mechanics formulas, for physics study, homework calculation and engineering estimation; for safety-critical or actual engineering work, follow professional standards and measured data.",
    ]))

    write('angular-momentum', build('angular-momentum', [
        "Find the angular momentum from the moment of inertia and the angular velocity",
        "Enter the moment of inertia I and the angular velocity w to find the angular momentum.",
        "Angular momentum calculator",
        "/ Angular momentum calculator",
        "📖 View the usage guide for Finding the angular momentum from the moment of inertia and the angular velocity",
        "📚 Deep dive: finding the angular momentum from the moment of inertia and the angular velocity",
        "Assessing the rotational quantity of a rotating body: enter the moment of inertia and the",
        "angular velocity",
        "to find the angular momentum and compare how strongly a body rotates at different speeds.",
        "Angular momentum conservation",
        "before the initial state: for processes such as drawing in the arms or collapse, enter the initial I and w to prepare for finding the final state by conservation.",
        "Teaching demonstration: show the linear growth of the angular momentum of the same body at different angular velocities, to help understand rotational conservation.",
        "Example: a uniform disk with I = 2 kg m^2 and w = 5 rad/s gives L = I x w = 10 kg m^2/s; doubling the rotation rate doubles the angular momentum.",
        "What is the difference between angular momentum and momentum?",
        "Linear momentum p = mv describes translation, while angular momentum L = I x w describes rotation; their dimensions and reference frames differ. Results are calculated in real time with standard mechanics formulas, for physics study, homework calculation and engineering estimation; for safety-critical or actual engineering work, follow professional standards and measured data.",
        "What are the units?",
        "The SI unit is kg m^2/s, obtained by multiplying I (kg m^2) by w (rad/s), with the radian dimensionless. Results are calculated in real time with standard mechanics formulas, for physics study, homework calculation and engineering estimation; for safety-critical or actual engineering work, follow professional standards and measured data.",
        "In what situation is it conserved?",
        "Angular momentum is conserved when the net external torque is zero, as when a figure skater draws in the arms to spin faster or a planet speeds up at perihelion. Results are calculated in real time with standard mechanics formulas, for physics study, homework calculation and engineering estimation; for safety-critical or actual engineering work, follow professional standards and measured data.",
    ]))

    write('banked-curve', build('banked-curve', [
        "Find the frictionless design speed from the curve radius and the banking angle",
        "Enter the curve radius r, the banking angle theta and g to find the design speed.",
        "Curve design speed calculator",
        "/ Curve design speed calculator",
        "📖 View the usage guide for Finding the frictionless design speed from the curve radius and the banking angle",
        "v = sqrt(r x g x tan theta) (no side slip). With r = 50 and theta = 30 degrees, about 16.8 m/s.",
        "v = sqrt(r x g x tan theta) (no side slip).",
        "With r = 50 and theta = 30 degrees, about 16.8 m/s.",
        "📚 Deep dive: finding the frictionless design speed from the curve radius and the banking angle",
        "Highway curve design: enter the curve radius and the proposed banking angle to find the design speed at which a vehicle needs no lateral friction, to guide speed limit sign setting.",
        "Racing track banking check: for a racing circuit, enter the actual banking angle and radius to back-calculate a safe cornering speed range.",
        "Teaching demonstration: show that a larger banking angle gives a higher design speed, to understand the",
        "source.",
        "Example: with r = 50 m, theta = 15 degrees and g = 9.8, v = sqrt(50 x 9.8 x tan 15 degrees), about sqrt(132), about 11.5 m/s (about 41 km/h).",
        "What does the design speed mean?",
        "At this speed the component of gravity supplies the centripetal force and the tyres need almost no lateral friction; above it, friction must make up the difference. Results are calculated in real time with standard mechanics formulas, for physics study, homework calculation and engineering estimation; for safety-critical or actual engineering work, follow professional standards and measured data.",
        "Should you actually corner more slowly?",
        "Considering a wet or slippery surface, the load and the safety margin, the actual speed limit is usually below the design speed and depends on tyre friction. Results are calculated in real time with standard mechanics formulas, for physics study, homework calculation and engineering estimation; for safety-critical or actual engineering work, follow professional standards and measured data.",
        "What if the banking angle is entered the wrong way round?",
        "If theta is taken from the user's viewpoint, make sure tan theta has the correct sign; a negative angle (banking inward) is unreasonable and the input must be checked. Results are calculated in real time with standard mechanics formulas, for physics study, homework calculation and engineering estimation; for safety-critical or actual engineering work, follow professional standards and measured data.",
        "How to use Finding the frictionless design speed from the curve radius and the banking angle",
        "Used for banking design of highway and racing curves, frictionless design speed estimation and speed limit reference, helping to understand the source of the centripetal force and driving safety.",
        "What does Finding the frictionless design speed from the curve radius and the banking angle do?",
        "A curve design speed calculator: enter the curve radius r, the banking angle theta and g, and use v = sqrt(r x g x tan theta) to find the frictionless design speed, for road and track design.",
        "How to use Finding the frictionless design speed from the curve radius and the banking angle?",
        "What scenarios is Finding the frictionless design speed from the curve radius and the banking angle suitable for?",
    ]))

    write('coefficient-restitution', build('coefficient-restitution', [
        "Find the coefficient of restitution from the velocities before and after a collision",
        "Enter the velocities of two bodies before and after the collision to find the coefficient of restitution.",
        "Coefficient of restitution calculator",
        "/ Coefficient of restitution calculator",
        "📖 View the usage guide for Finding the coefficient of restitution from the velocities before and after a collision",
        "e = 1 is perfectly elastic and e = 0 is perfectly inelastic. With 5, 0 going to 2, 3, e = 0.2.",
        "Post-collision v1' (m/s)",
        "Post-collision v2' (m/s)",
        "e = 1 is perfectly elastic and e = 0 is perfectly inelastic.",
        "📚 Deep dive: finding the coefficient of restitution from the velocities before and after a collision",
        "Elasticity judgement: enter the velocities before and after the collision, find e and distinguish perfectly elastic, partially elastic and inelastic collisions.",
        "Sports equipment selection: enter the rebound speed of basketballs, billiard balls and similar to assess elasticity and rebound performance.",
        "Teaching demonstration: compare the e values of different materials to understand energy loss.",
        "Example: before the collision v1 = 5 and v2 = 0, after the collision v1' = 2 and v2' = 3, so e = (3-2)/(5-0) = 0.2, a low-elasticity collision.",
        "What do e = 1 and e = 0 represent?",
        "e = 1 is perfectly elastic (kinetic energy conserved) and e = 0 is perfectly inelastic (the bodies move together afterwards and the kinetic energy loss is maximal). Results are calculated in real time with standard mechanics formulas, for physics study, homework calculation and engineering estimation; for safety-critical or actual engineering work, follow professional standards and measured data.",
        "Can e be greater than 1?",
        "For an ideal collision e is at most 1; e greater than 1 can occur only if internal energy is released during the collision, as in an explosion, which does not happen in ordinary contact collisions. Results are calculated in real time with standard mechanics formulas, for physics study, homework calculation and engineering estimation; for safety-critical or actual engineering work, follow professional standards and measured data.",
        "Do the velocities need to be in the same direction?",
        "The formula uses one-dimensional signed velocities; for multi-dimensional collisions take the component along the normal direction and avoid applying scalars directly. Results are calculated in real time with standard mechanics formulas, for physics study, homework calculation and engineering estimation; for safety-critical or actual engineering work, follow professional standards and measured data.",
    ]))

    write('elastic-collision-1d', build('elastic-collision-1d', [
        "Find the post-collision velocities from the masses and the pre-collision velocities",
        "Enter two masses and the pre-collision velocities to find the post-collision velocities.",
        "One-dimensional elastic collision calculator",
        "/ One-dimensional elastic collision calculator",
        "📖 View the usage guide for Finding the post-collision velocities from the masses and the pre-collision velocities",
        "One-dimensional elastic collision (momentum conservation plus kinetic energy conservation): v1' = (m1 - m2) / (m1 + m2) x v1 + 2 m2 / (m1 + m2) x v2; v2' = 2 m1 / (m1 + m2) x v1 + (m2 - m1) / (m1 + m2) x v2. For a head-on collision of equal masses the two exchange velocities. The check is that the total pre-collision momentum m1v1 + m2v2 and the total kinetic energy both equal the corresponding post-collision values, which can be used to verify whether the result is correct.",
        "Both momentum and kinetic energy are conserved.",
        "2 kg at 4 m/s striking 1 kg at rest gives v1' = 1.33 and v2' = 5.33 m/s.",
        "📚 Deep dive: finding the post-collision velocities from the masses and the pre-collision velocities",
        "Billiards analysis: enter the masses of two balls and their pre-collision velocities to find the post-collision velocities and judge the resulting positions.",
        "Particle collisions: enter the initial velocities of microscopic particles to find the velocity exchange after an elastic collision, which for equal masses means they swap.",
        "Teaching demonstration: demonstrate the velocity swap in a head-on collision of equal masses and the rebound of the lighter body when the masses differ greatly.",
        "Example: with m1 = m2 = 1, v1 = 4 and v2 = 0 in one dimension, after the collision v1' = 0 and v2' = 4, so the velocities are exchanged.",
        "What counts as an elastic collision?",
        "The total kinetic energy is the same before and after the collision (e = 1); this holds approximately for ideal rigid bodies or molecules, while in reality there is always some energy loss. Results are calculated in real time with standard mechanics formulas, for physics study, homework calculation and engineering estimation; for safety-critical or actual engineering work, follow professional standards and measured data.",
        "Why do equal masses exchange velocities?",
        "Solving momentum and kinetic energy conservation together shows that in a one-dimensional elastic head-on collision of equal masses the two bodies exchange velocities. Results are calculated in real time with standard mechanics formulas, for physics study, homework calculation and engineering estimation; for safety-critical or actual engineering work, follow professional standards and measured data.",
        "Can it be used for two-dimensional collisions?",
        "This tool is one-dimensional; for two dimensions the components along the line of centres must be handled separately, with the",
        "tangential velocity",
        "unchanged. Results are calculated in real time with standard mechanics formulas, for physics study, homework calculation and engineering estimation; for safety-critical or actual engineering work, follow professional standards and measured data.",
    ]))


if __name__ == '__main__':
    main()

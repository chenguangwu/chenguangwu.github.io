#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'kinematics')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'kinematics')
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
    out = {'slug': slug, 'industry': 'kinematics', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
#!/usr/bin/env python3

def main():
    # angular-accel (28)
    write('angular-accel', build('angular-accel', [
        "Rate of change of angular velocity.",
        "Angular Acceleration Calculator",
        "/ Angular Acceleration",
        "Angular acceleration",
        '📖 View "Angular Acceleration Calculator Guide"',
        "Angular acceleration α = angular velocity change Δω divided by time Δt; unit rad/s²; in degree units α(°/s²) = α(rad/s²) × 180 / π; angular velocity change Δω = α × Δt; rotation angle θ = ω₀ × t + ½ α t².",
        "Angular velocity change Δω (rad/s)",
        '📚 In-depth: Angular Acceleration (Δω/Δt)',
        "Find angular acceleration from how fast a turntable's speed changes.",
        "Analysis of motor start/stop processes.",
        "From",
        "Angular velocity",
        "the rate of change estimates the rotor's average angular acceleration.",
        "α = 10/2 = 5 rad/s². That is, angular velocity increases by 10 rad/s over 2 s, angular acceleration 5 rad/s².",
        "Angular velocity change 24 rad/s over 3 s",
        "α=Δω/Δt=24/3=8.000 rad/s². If the angular velocity is decreasing, just enter a negative value; the result will also be negative, indicating decelerating rotation.",
        "Relation to linear acceleration?",
        "Tangential acceleration",
        "a_t = α·r; on the same rigid body, the larger the radius, the greater the tangential acceleration; angular acceleration is the rotational counterpart.",
        "Is average angular acceleration the same as instantaneous angular acceleration?",
        "No. This tool gives the average over the whole interval Δω/Δt; if the speed is non-uniform, α differs at each instant. Only under uniform angular acceleration does the average equal the instantaneous value at any moment.",
        "How to use the Angular Acceleration Calculator",
        "What does the Angular Acceleration Calculator do?",
        "Online angular acceleration calculator: input angular velocity change and time interval to obtain average angular acceleration, or convert from linear acceleration and radius; suitable for rotational motion analysis, pure frontend.",
        "How to use the Angular Acceleration Calculator?",
        "What scenarios is the Angular Acceleration Calculator suitable for?",
        "Angular acceleration α=Δω/Δt: the rate of change of angular velocity over time, describing how fast the rotation speed changes.",
        "SI unit rad/s² (radian per second squared). Relation to linear acceleration a_t=α·r (r is the rotation radius).",
    ]))

    # angular-displacement (19)
    write('angular-displacement', build('angular-displacement', [
        "Angular displacement from initial angular velocity, angular acceleration and time",
        "Input initial angular velocity ω₀, angular acceleration α, and time t to find angular displacement.",
        "Angular Displacement Calculator",
        "/ Angular Displacement Calculator",
        '📖 View "Angular Displacement Calculator Guide"',
        '📚 In-depth: Angular Displacement (ω₀t + ½αt²)',
        "Find the angle turned under uniform angular acceleration.",
        "Estimate the radians turned by a turntable/flywheel.",
        "Find the total angle turned by a uniformly angularly-accelerating body over a time interval.",
        "θ = 2×3 + 0.5×1×3² = 6 + 4.5 = 10.5 rad. That is, 10.5 radians (about 1.67 turns) turned in 3 s.",
        "Initial",
        "Angular velocity",
        "Angular acceleration",
        "2 rad/s² over 4 s",
        "θ=ω₀t+½αt²=3×4+½×2×4²=12+16=28.000 rad, about 4.46 turns (divide by 2π).",
        "How to convert radians to turns?",
        "1 turn = 2π rad ≈ 6.283 rad; 10.5 rad ÷ 6.283 ≈ 1.67 turns.",
        "How to read a result over one turn?",
        "The tool returns the total radians, not a remainder. To convert to turns divide by 2π; to get the angle in degrees multiply by 180/π. For example 28.000 rad equals 4.46 turns, i.e. 4 turns plus about 166°.",
    ]))

    # angular-final-velocity (27)
    write('angular-final-velocity', build('angular-final-velocity', [
        "Final angular velocity from initial angular velocity, angular acceleration and time",
        "Input initial angular velocity ω₀, angular acceleration α, and time t to find final angular velocity.",
        "Final Angular Velocity Calculator",
        "/ Final Angular Velocity Calculator",
        '📖 View "Final Angular Velocity Calculator Guide"',
        '📚 In-depth: Final Angular Velocity (ω₀ + αt)',
        "Find angular velocity at a given moment under uniform angular acceleration",
        "Angular velocity",
        "Accelerate a motor to a target speed.",
        "Find the angular velocity of a uniformly angularly-accelerating body at a specified time.",
        "ω = 2 + 1×3 = 5 rad/s. That is, final angular velocity 5 rad/s at 3 s.",
        "Initial angular velocity 3 rad/s,",
        "Angular acceleration",
        "2 rad/s² over 4 s",
        'ω=ω₀+αt=3+2×4=11.000 rad/s. Pair it with the "',
        "Angular displacement",
        '" tool to also get the angle turned in this interval, 28.000 rad.',
        "How to convert to frequency?",
        "f = ω/(2π); 5 rad/s corresponds to about 0.796 Hz, i.e. about 0.8 turns per second.",
        "What does negative α mean?",
        'It means decelerating rotation, e.g. a flywheel under braking. When the computed ω becomes negative, the object has stopped and started rotating backward; to find "when it stops", use ω₀/|α| for the',
        "braking time",
        "How to use Final Angular Velocity from Initial Angular Velocity, Angular Acceleration and Time",
        "What does Final Angular Velocity from Initial Angular Velocity, Angular Acceleration and Time do?",
        "Input initial angular velocity ω₀, angular acceleration α and time t, solve final angular velocity by ω = ω₀ + αt, for estimating the speed of a uniformly angularly-accelerating body at a specified time and for exercise calculations.",
        "How to use Final Angular Velocity from Initial Angular Velocity, Angular Acceleration and Time?",
        "What scenarios is Final Angular Velocity from Initial Angular Velocity, Angular Acceleration and Time suitable for?",
    ]))

    # angular-velocity (15)
    write('angular-velocity', build('angular-velocity', [
        "Angular velocity is the ratio of linear velocity to radius.",
        "Angular Velocity Calculator",
        "/ Angular Velocity",
        "Angular velocity",
        '📖 View "Angular Velocity Calculator Guide"',
        '📚 In-depth: Angular Velocity (v/r)',
        "Find angular velocity from linear velocity and radius.",
        "Wheel/turntable speed conversion.",
        "Bidirectional conversion between linear and angular velocity.",
        "ω = 10/2 = 5 rad/s. That is, angular velocity 5 rad/s when linear speed 10 m/s and radius 2 m.",
        "Linear velocity 18 m/s, radius 3 m",
        "ω=v/r=18/3=6.000 rad/s; converted to rpm is ω×60/(2π)=57.296 rpm. The larger the radius, the lower the angular velocity for the same linear speed.",
        "How to convert rpm to rad/s?",
        "How do these three units verify each other?",
        'The core relation is v=ω·r: knowing any two gives the third. When converting rpm note that ω must be in rad/s; one turn is 2π radians, so rpm=ω×60/(2π) (multiply by 60 to change "per second" to "per minute").',
    ]))

    # avg-acceleration (16)
    write('avg-acceleration', build('avg-acceleration', [
        "Average acceleration from velocity change and time",
        "Input final velocity v, initial velocity v₀, and time t to find average acceleration.",
        "Average Acceleration Calculator",
        "/ Average Acceleration Calculator",
        '📖 View "Average Acceleration Calculator Guide"',
        '📚 In-depth: Average Acceleration (Δv/Δt)',
        "Average acceleration is velocity change divided by time.",
        "Vehicle acceleration/deceleration process evaluation.",
        "Use experimentally measured velocity endpoints to find the average acceleration over a process.",
        "a = (10−20)/2 = −5 m/s². That is, decelerating 10 m/s in 2 s, average acceleration −5 m/s² (negative sign means deceleration).",
        "Initial speed 6 m/s, final speed 30 m/s, over 4 s",
        "a=(v−v₀)/t=(30−6)/4=6.000 m/s². If final speed is less than initial, the result is negative, indicating deceleration.",
        "What does the negative sign mean?",
        "Opposite direction to initial velocity, indicating deceleration; magnitude 5 m/s² is the deceleration.",
        "Why might average acceleration differ a lot from per-second acceleration?",
        "Average acceleration only looks at the first and last velocities, smoothing out the middle. For example a car may accelerate hard then cruise; the average acceleration might be only 6.000 m/s² while the instant at start is far larger. For safety analysis focus on instantaneous values rather than averages.",
    ]))

if __name__ == "__main__":
    main()

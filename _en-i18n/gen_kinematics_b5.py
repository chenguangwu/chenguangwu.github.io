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
    # stopping-time (18)
    write('stopping-time', build('stopping-time', [
        "Braking time from initial velocity and deceleration",
        "Input initial velocity v₀ and deceleration a to find braking time.",
        "Braking Time Calculator",
        "/ Braking Time Calculator",
        '📖 View "Braking Time from Initial Velocity and Deceleration Guide"',
        '📚 In-depth: Braking Time (v₀/a)',
        "Initial speed divided by deceleration gives braking duration.",
        "Brake response evaluation.",
        "Find the time to come to a full stop from initial velocity and deceleration.",
        "t = 20/5 = 4 s. That is, from 20 m/s uniformly decelerating to stop takes 4 s (excluding reaction time).",
        "Initial velocity 30 m/s,",
        "braking deceleration",
        "t=v₀/a=30/6=5.000 s. During this time the",
        "is 15 m/s, corresponding to a glide distance of 75 m (verifiable with the \"displacement\" formula).",
        "Relation to braking distance?",
        "Distance = v₀t − ½at², substituting t=v₀/a gives v₀²/2a, both derived from the same kinematics.",
        "How should a be chosen here?",
        "Fill in the absolute value of deceleration during braking. Dry asphalt is generally 7~8 m/s², wet road may drop to 3~4 m/s², icy road even lower. Wrong value significantly affects the result; for safety evaluation use the worst-case road surface.",
    ]))

    # tangential-accel (19)
    write('tangential-accel', build('tangential-accel', [
        "Tangential acceleration from angular acceleration and radius",
        "Input angular acceleration α and radius r to find tangential acceleration.",
        "Tangential Acceleration Calculator",
        "/ Tangential Acceleration Calculator",
        '📖 View "Tangential Acceleration from Angular Acceleration and Radius Guide"',
        '📚 In-depth: Tangential Acceleration (α·r)',
        "Rotation",
        "angular acceleration",
        "the corresponding tangential acceleration.",
        "Turntable edge linear-acceleration analysis.",
        "Find the tangential acceleration at the edge from angular acceleration and radius.",
        "a_t = 2×0.5 = 1 m/s². That is, when angular acceleration is 2 and radius 0.5 m, edge tangential acceleration is 1 m/s².",
        "Angular acceleration 3.5 rad/s², radius 0.8 m",
        "a_t=α·r=3.5×0.8=2.800 m/s². The larger the radius, the greater the linear acceleration brought by the same angular acceleration.",
        "Is there also normal acceleration?",
        "Yes. Normal (centripetal) a_n=ω²r changes direction, tangential a_t=αr changes magnitude, total acceleration is their vector sum.",
        "Tangential acceleration and",
        "the same thing?",
        "No. Tangential acceleration reflects how fast the rotation speed changes (a_t=αr, non-zero only during variable-speed rotation); centripetal acceleration reflects how fast direction changes (a_n=ω²r, exists whenever rotating). During uniform rotation the former is 0 but the latter is not.",
    ]))

    # tangential-velocity (17)
    write('tangential-velocity', build('tangential-velocity', [
        "Tangential velocity from angular velocity and radius",
        "Input angular velocity ω and radius r to find tangential velocity.",
        "Tangential Velocity Calculator",
        "/ Tangential Velocity Calculator",
        '📖 View "Tangential Velocity from Angular Velocity and Radius Guide"',
        '📚 In-depth: Tangential Velocity (ω·r)',
        "Angular velocity",
        "the corresponding linear velocity.",
        "Turntable edge speed distribution.",
        "Find the linear velocity at a certain radius of a rotating body.",
        "v_t = 10×0.5 = 5 m/s. That is, at angular velocity 10 rad/s and radius 0.5 m, linear speed is 5 m/s.",
        "Angular velocity 12 rad/s, radius 0.4 m",
        "v=ω·r=12×0.4=4.800 m/s. At the same angular velocity, doubling the radius doubles the linear speed there.",
        "Faster at larger radius?",
        "At the same angular velocity v_t=ωr, the outer edge has larger linear speed; this is also why the outer edge of a turntable feels stronger centrifugal force.",
        "Why does the outer edge \"rotate faster\" yet completes one turn simultaneously with the center?",
        "Because angular velocity ω is the same across the disk (same rigidity), but linear velocity v=ωr grows with radius. A point on the outer edge must travel a longer circumference in the same time, so linear speed is larger — also why centrifugal equipment edges often have very high linear speeds.",
    ]))

    # uniform-displacement (18)
    write('uniform-displacement', build('uniform-displacement', [
        "Displacement from uniform speed and time",
        "Input speed v and time t to find displacement.",
        "Uniform Motion Displacement Calculator",
        "/ Uniform Motion Displacement Calculator",
        '📖 View "Displacement from Uniform Speed and Time Guide"',
        "s = v·t (uniform).",
        '📚 In-depth: Uniform Displacement (s=vt)',
        "Uniform motion displacement.",
        "Constant-speed trip estimation.",
        "Find the displacement of uniform linear motion over a time interval.",
        "s = 5×10 = 50 m. That is, 5 m/s uniform for 10 s is 50 m.",
        "Speed 12 m/s, duration 7 s",
        "s=v·t=12×7=84.000 m. If converted to km/h, 12 m/s equals 43.2 km/h.",
        "And",
        "relation?",
        "Under uniform motion instantaneous = average, s=vt is the special case of v̄t.",
        "Are displacement and distance equal here?",
        "Equal in one-directional linear motion. This tool assumes constant speed and unchanged direction; if it turns back or corners midway, displacement (vector) will be less than distance (scalar), requiring segment calculation.",
    ]))

    # velocity-squared (16)
    write('velocity-squared', build('velocity-squared', [
        "Velocity-displacement relation without time",
        "Velocity-Displacement Relation Calculator",
        "/ Velocity-Displacement Formula",
        "Velocity-displacement formula",
        '📖 View "Velocity-Displacement Relation Calculator Guide"',
        '📚 In-depth: Velocity-Displacement Relation (v²=v₀²+2aΔx)',
        "Unknown time: find final speed from displacement.",
        "Free-fall final speed (known height).",
        "Establish velocity-displacement relation directly without time.",
        "v = √(0+2×9.8×100) = √1960 ≈ 44.27 m/s. That is, free fall 100 m final speed about 44.3 m/s.",
        "Initial velocity 4 m/s, acceleration 3 m/s², displacement 20 m",
        "v=√(v₀²+2ax)=√(16+120)=√136=11.662 m/s. Applies to scenarios where only how far was traveled is known, not how long, e.g. inferring from brake mark length.",
        "Consistent with free-fall-time?",
        "Yes: eliminating t from h=½gt² and v=gt gives v²=2gh, the same motion in different expression.",
        "Can this formula be used in reverse?",
        "Yes. In traffic accident investigation, brake mark length x is often measured, assume deceleration a then infer initial speed v₀=√(v²−2ax); if the vehicle finally stops (v=0), then v₀=√(−2ax), just take a negative.",
    ]))

if __name__ == "__main__":
    main()

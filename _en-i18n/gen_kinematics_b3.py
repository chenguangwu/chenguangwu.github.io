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
    # freq-from-omega (19)
    write('freq-from-omega', build('freq-from-omega', [
        "Frequency from angular velocity",
        "Input angular velocity ω to find frequency f.",
        "Frequency Calculator",
        "/ Frequency Calculator",
        '📖 View "Frequency from Angular Velocity Guide"',
        '📚 In-depth: Frequency from Angular Velocity (f=ω/2π)',
        "Angular velocity",
        "Turns per second.",
        "Rotating equipment",
        "Frequency conversion",
        "Convert angular",
        "to how many turns per second (frequency value).",
        "f = 6.283/(2π) = 6.283/6.283 = 1 Hz. That is, 1 turn per second.",
        "Angular velocity 15.708 rad/s",
        "f=ω/(2π)=15.708/6.28318=2.5000 Hz, i.e. 2.5 turns per second.",
        "Relation to period?",
        "f = 1/T; frequency is turns per unit time, period is time per turn, reciprocal of each other.",
        "How to convert among frequency, period and rpm?",
        'Period T=1/f, so in this example T=0.4 s; rpm = f×60 = 150 rpm. The three describe the same thing, only in different units: Hz is "turns per second", rpm is "turns per minute".',
    ]))

    # height-fall-distance (27)
    write('height-fall-distance', build('height-fall-distance', [
        "Fall distance from fall time",
        "Input fall time t and gravitational acceleration g to find fall distance.",
        "Free Fall Distance Calculator",
        "/ Free Fall Distance Calculator",
        '📖 View "Fall Distance from Fall Time Guide"',
        "h = ½gt² (from rest).",
        '📚 In-depth: Fall Distance (½gt²)',
        "Given fall time, find height.",
        "Reverse-infer free-fall height.",
        "Given fall duration, find how far it fell in that time.",
        "h = 0.5×9.81×2² = 0.5×9.81×4 = 19.62 m. That is, about 19.6 m in 2 s of falling.",
        "Fall 3.5 s, gravitational acceleration 9.81 m/s²",
        "h=½gt²=0.5×9.81×3.5²=60.086 m. If switched to lunar gravity 1.62 m/s², the same time falls only about 9.92 m.",
        "Inverse of free-fall-time?",
        "Yes. t=√(2h/g) and h=½gt² are mutual rearrangements; given one you can find the other.",
        "Why is distance proportional to the square of time?",
        "Because the object accelerates while falling, each later second is faster than the previous, so accumulated displacement grows wider. When time doubles, distance becomes 4× (not 2×); this quadratic relation is also why a slightly higher speed in traffic accidents greatly increases braking distance.",
        "How to use Fall Distance from Fall Time",
        "What does Fall Distance from Fall Time do?",
        "Input fall time t and gravitational acceleration g (default 9.8 m/s²), compute free-fall distance by h = ½gt², for physics teaching demonstrations or estimating the displacement of an object falling from a height.",
        "How to use Fall Distance from Fall Time?",
        "What scenarios is Fall Distance from Fall Time suitable for?",
        "Free fall distance h=½·g·t² (t is fall time, g≈9.8 m/s² is gravitational acceleration).",
        "Units and range",
        "h in meters (m), t in seconds (s). Valid when initial speed is 0 and only gravity acts; result grows with t².",
        "Applicable boundary",
        "Ignore the small differences in g from air resistance and altitude variation; high drops or low-density objects need air-resistance correction.",
    ]))

    # period-from-omega (18)
    write('period-from-omega', build('period-from-omega', [
        "Rotation period from angular velocity",
        "Input angular velocity ω to find period T.",
        "Period Calculator",
        "/ Period Calculator",
        '📖 View "Rotation Period from Angular Velocity Guide"',
        '📚 In-depth: Period from Angular Velocity (T=2π/ω)',
        "Angular velocity",
        "Time per turn.",
        "Rotation period calculation.",
        "Convert angular",
        "to the period required for one turn.",
        "T = 2π/6.283 = 1 s. That is, when angular velocity is 6.283 rad/s, 1 s per turn.",
        "Angular velocity 1.5708 rad/s",
        "T=2π/ω=6.28318/1.5708=4.0000 s, i.e. one turn completed every 4 s.",
        "And frequency?",
        "T=1/f; period 1 s equals frequency 1 Hz, consistent.",
        "What is the relationship between period and frequency?",
        "Reciprocal: T=1/f. In this example T=4.0000 s corresponds to f=0.25 Hz. Note ω cannot be 0 — angular velocity 0 means no rotation, period tends to infinity, the tool will give a meaningless result.",
    ]))

    # projectile-max-height (18)
    write('projectile-max-height', build('projectile-max-height', [
        "Vertical maximum height reached by oblique projection.",
        "Projectile Max Height Calculator",
        "/ Projectile Max Height",
        "Projectile max height",
        '📖 View "Projectile Max Height Calculator Guide"',
        '📚 In-depth: Projectile Max Height (v²sin²θ/2g)',
        "Vertex height of oblique projection.",
        "Fountain/throwing highest point estimation.",
        "Find",
        "projectile motion",
        "the highest point reached (height relative to the launch plane).",
        "H = 30²×sin²60/(2×9.8) = 900×0.75/19.6 ≈ 34.4 m. That is, 60° throw at 30 m/s reaches max about 34.4 m.",
        "Initial speed 25 m/s, elevation 45°, gravitational acceleration 9.8 m/s²",
        "H=v²sin²θ/(2g)=625×(sin45°)²/(2×9.8)=625×0.5/19.6=15.944 m. 45° is not necessarily the highest angle — max height increases monotonically with angle, highest at 90° vertical throw.",
        "What angle is highest?",
        "Vertical throw (90°) is highest; but range is max at 45°, height and range have different goals so different angles are chosen.",
        "Why is the farthest range at 45°, but the highest point here is not?",
        "The two goals differ: range R=v²sin2θ/g is max at 45°; while max height H=v²sin²θ/(2g) increases monotonically with θ, reaching its maximum v²/(2g) at θ=90° (vertical throw). This example's 45° is a compromise for range, not for max height.",
    ]))

    # projectile-time-flight (16)
    write('projectile-time-flight', build('projectile-time-flight', [
        "Total flight time back to the same horizontal plane.",
        "Projectile Time of Flight Calculator",
        "/ Projectile Time of Flight",
        "Projectile time of flight",
        '📖 View "Projectile Time of Flight Calculator Guide"',
        '📚 In-depth: Projectile Time of Flight (2v·sinθ/g)',
        "Total duration of oblique projection from launch to landing.",
        "Throw hang-time estimation.",
        "Find total time from release to landing back on the same horizontal plane.",
        "T = 2×30×sin45/9.8 = 60×0.707/9.8 ≈ 4.33 s. That is, about 4.3 s in the air.",
        "Initial speed 25 m/s, elevation 30°, gravitational acceleration 9.8 m/s²",
        "T=2v·sinθ/g=2×25×sin30°/9.8=25/9.8=2.551 s. Time to rise to the highest point is exactly half the total, about 1.276 s.",
        "Landing point different height from launch?",
        "This formula assumes same-height landing; if landing is lower a quadratic must be solved, taking longer.",
        "Is it accurate when the landing point is higher (or lower) than the launch point?",
        "No. This formula assumes landing back on the same horizontal plane. If the landing point is higher (e.g. uphill), actual flight time is shorter; if lower (e.g. off a cliff), longer. Such cases require solving the vertical quadratic equation with the general formula.",
    ]))

if __name__ == "__main__":
    main()

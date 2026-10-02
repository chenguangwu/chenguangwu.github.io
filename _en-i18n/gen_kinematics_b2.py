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
    # avg-velocity (16)
    write('avg-velocity', build('avg-velocity', [
        "Average velocity (v̄ = Δx / Δt)",
        "The ratio of displacement change to elapsed time.",
        "Average Velocity Calculator",
        "/ Average Velocity",
        '📖 View "Average Velocity (v̄ = Δx / Δt) Guide"',
        '📚 In-depth: Average Velocity (Δx/Δt)',
        "Displacement divided by time gives average velocity.",
        "Overall speed/duration evaluation of a trip.",
        "Find average velocity by the ratio of displacement to time, distinct from average speed.",
        "v̄ = 100/10 = 10 m/s. That is, 100 m in 10 s, average 10 m/s (does not reflect mid-trip speed).",
        "Displacement 180 m, time 6 s",
        "v̄=Δx/Δt=180/6=30.000 m/s, converted to 108.000 km/h (multiply by 3.6).",
        "Average velocity and instantaneous velocity?",
        "Average is total displacement / total time; instantaneous is the speed at a moment. Under variable motion the two often differ.",
        "What is the difference between average velocity and average speed?",
        "Average velocity uses displacement (straight-line distance from start to end, with direction); average speed uses distance traveled (actual path length). Running one lap around a track back to the start, displacement is 0 so average velocity is 0, but average speed is not 0 — this tool strictly computes the former.",
    ]))

    # displacement-accel (17)
    write('displacement-accel', build('displacement-accel', [
        "Displacement formula (x = v₀·t + ½·a·t²)",
        "The sum of initial-velocity displacement and uniformly-accelerated displacement.",
        "Uniform Acceleration Displacement Calculator",
        "/ Uniform Acceleration Displacement",
        "Uniform acceleration displacement",
        '📖 View "Displacement Formula (x = v₀·t + ½·a·t²) Guide"',
        '📚 In-depth: Displacement Formula (v₀t + ½at²)',
        "Find displacement under uniform acceleration.",
        "Estimate starting acceleration distance.",
        "Given initial velocity, acceleration and time, find the linear displacement.",
        "x = 10×5 + 0.5×2×25 = 50 + 25 = 75 m. That is, 75 m traveled in 5 s of uniform acceleration.",
        "Initial velocity 4 m/s, acceleration 3 m/s², over 6 s",
        "x=v₀t+½at²=4×6+½×3×6²=24+54=78.000 m. If the object starts from rest (v₀=0), it reduces to the familiar x=½at².",
        "Consistent with v̄t?",
        "Under uniform acceleration average speed = (v₀+v)/2, displacement = v̄×t, equivalent to this formula; not valid for non-uniform acceleration.",
        "When to use this formula vs the velocity-displacement formula?",
        'Use this page\'s x=v₀t+½at² when time is known; when time is unknown but final velocity is known, use v²=v₀²+2ax instead (see the "Velocity-Displacement" tool). They are equivalent, differing only in known conditions.',
    ]))

    # displacement-va (17)
    write('displacement-va', build('displacement-va', [
        "Displacement from velocity change and acceleration",
        "Input final velocity v, initial velocity v₀, acceleration a to find displacement.",
        "Uniformly-Variable Displacement (known v, v₀, a) Calculator",
        "/ Uniformly-Variable Displacement (known v, v₀, a) Calculator",
        '📖 View "Displacement from Velocity Change and Acceleration Guide"',
        '📚 In-depth: Displacement (velocity difference squared / 2a)',
        "Unknown time: use initial/final velocity and acceleration to find displacement.",
        "Braking distance",
        "(known initial/final speed) estimation.",
        "When time is unknown, infer displacement from initial/final velocity and acceleration.",
        "s = (20²−10²)/(2×5) = (400−100)/10 = 30 m. That is, 10→20 uniform acceleration travels 30 m.",
        "Initial speed 5 m/s, final speed 25 m/s, acceleration 4 m/s²",
        "s=(v²−v₀²)/(2a)=(625−25)/8=75.000 m. This formula needs no time quantity at all, suitable for cases with only speed-measurement data.",
        "How to use deceleration?",
        "Just take a negative; e.g. 20→10, a=−5, s=(100−400)/(−10)=30 m, distance is positive.",
        "Is a negative displacement result an error?",
        "No. Displacement carries direction: if initial-velocity direction is positive and acceleration is negative (decelerate then reverse), or final-speed squared is less than initial-speed squared, the result is negative, meaning net displacement opposite to initial velocity. Numerically it is correct.",
    ]))

    # final-velocity-accel (22)
    write('final-velocity-accel', build('final-velocity-accel', [
        "Velocity formula (v = v₀ + a·t)",
        "Initial velocity plus the accumulation of acceleration over time.",
        "Uniform Acceleration Final Velocity Calculator",
        "/ Uniform Acceleration Final Velocity",
        "Uniform acceleration final velocity",
        '📖 View "Velocity Formula (v = v₀ + a·t) Guide"',
        "v = v₀ + a·t. Free fall 5 s: v = 9.8×5 = 49 m/s.",
        "Free fall 5 s: v = 9.8×5 = 49 m/s.",
        '📚 In-depth: Final Velocity (v₀ + at)',
        "Find velocity at a given moment under uniform acceleration.",
        "Free-fall final speed (v₀=0).",
        "Find the instantaneous velocity of uniformly accelerated linear motion at a given time.",
        "Free fall 5s",
        "v = 0 + 9.8×5 = 49 m/s. That is, free fall for 5 s reaches about 49 m/s (ignoring air resistance).",
        "Initial velocity 3 m/s, acceleration 2.5 m/s², over 8 s",
        "v=v₀+at=3+2.5×8=23.000 m/s, converted to 82.800 km/h.",
        "Air resistance effect?",
        "Ideal model ignores it; in reality at high speed resistance is significant, final speed tends to",
        "terminal velocity",
        ", this formula only applies to low-speed/short-range.",
        "Why is it free fall when v₀=0 and a=g?",
        "This formula is the general uniform-acceleration formula. Setting initial velocity to 0 and acceleration to g=9.8 m/s², v=gt is exactly the velocity formula for free fall from rest; when initial velocity is not 0 it corresponds to vertical downward throw.",
    ]))

    # free-fall-time (17)
    write('free-fall-time', build('free-fall-time', [
        "Time of free fall from rest given height.",
        "Free Fall Time Calculator",
        "/ Free Fall Time",
        "Free fall time",
        '📖 View "Free Fall Time Calculator Guide"',
        "100 m fall takes about 4.52 s.",
        '📚 In-depth: Free Fall Time (√(2h/g))',
        "Given height, find fall time.",
        "Estimate time for a dropped object to arrive.",
        "Infer the time to reach the ground from fall height (ignoring air resistance).",
        "t = √(2×100/9.8) = √20.41 ≈ 4.52 s. That is, a 100 m free fall touches ground in about 4.5 s.",
        "Drop height 45 m, gravitational acceleration 9.8 m/s²",
        "t=√(2h/g)=√(90/9.8)=3.030 s; impact speed v=gt=9.8×3.030=29.698 m/s (about 107 km/h).",
        "Does it depend on mass?",
        "Ideal free fall does not (Galileo); in reality large air-resisted objects are slightly slower.",
        "Why does time depend only on height, not on the object's mass?",
        "Ignoring air resistance, all objects accelerate by the same g, and mass cancels on both sides of the equation — this is exactly Galileo's falling-body conclusion. In reality with air resistance, light and fluffy objects are significantly slower than the theoretical value; this tool's result is the ideal lower bound.",
    ]))

if __name__ == "__main__":
    main()

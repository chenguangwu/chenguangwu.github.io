#!/usr/bin/env python3
# gen_robotics_b6.py — robotics b6 (3 slugs): stereo-depth/trajectory-time-linear/wheel-odometry
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'robotics')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'robotics')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

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
    out = {'slug': slug, 'industry': 'robotics', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

STD = [
 "Find the object depth from the disparity",
 "Enter the focal length f in pixels, the baseline B and the disparity d in pixels to get the depth.",
 "Stereo Vision Depth Calculator",
 "/ Stereo Vision Depth Calculator",
 "📖 View Guide: \"Find the object depth from the disparity\"",
 "Focal length f (px)",
 "Baseline B (m)",
 "Disparity d (px)",
 "Z = fB/d under the pinhole model.",
 "📚 Deep Dive: Stereo vision depth",
 "Get the object depth from the disparity.",
 "Baseline and focal length setup.",
 "How a depth camera works.",
 "Focal length 500 px, baseline 0.1 m, disparity 25 px",
 "Halving the disparity",
 "d = 12.5 gives Z = 4 m; a smaller disparity means a greater distance, since depth is inversely proportional to disparity.",
 "Units?",
 "Take f and d in pixels and B in metres, and Z comes out in metres.",
 "Is the error larger up close?",
 "Yes. Depth is sensitive to changes in disparity, so it is less stable nearby.",
]

TTL = [
 "Find the motion time from displacement and speed",
 "Enter the displacement d and the speed v to get the motion time.",
 "Linear Motion Time Calculator",
 "/ Linear Motion Time Calculator",
 "📖 View Guide: \"Find the motion time from displacement and speed\"",
 "t = d/v at constant speed.",
 "📚 Deep Dive: Linear trajectory time",
 "Arrival time at a constant speed.",
 "Estimating the task cycle time.",
 "Duration for path planning.",
 "Move 1 m at 0.2 m/s",
 "Speeding up to 0.5",
 "t = 2 s; a higher speed takes less time.",
 "What about acceleration and deceleration?",
 "This covers the constant speed segment; with acceleration you must integrate piece by piece.",
 "Versus an S curve?",
 "Industry commonly uses S-curve acceleration to reduce shock, while this is the simplified constant speed model.",
]

WOD = [
 "Estimate the pose change from the distance travelled by each wheel.",
 "Wheel Odometry Displacement Calculator",
 "/ Wheel Odometry",
 "Wheel Odometry",
 "📖 View Guide: \"Wheel Odometry Displacement Calculator\"",
 "Left wheel distance d_l (m)",
 "Right wheel distance d_r (m)",
 "The heading change equals the difference in wheel distances divided by the wheelbase.",
 "📚 Deep Dive: Wheel odometry",
 "Infer the pose change from the left and right wheel displacements.",
 "Dead reckoning for a differential chassis.",
 "Assessing localisation drift.",
 "Left 1.0, right 1.2 m, wheelbase 0.4 m",
 "ds = (1.0 + 1.2)/2 = 1.1 m and dθ = (1.2 - 1.0)/0.4 = 0.5 rad; the robot moves forward 1.1 m while turning right by 0.5 rad.",
 "Equal distances, straight line",
 "dθ = 0 and the motion is pure translation with ds = dl = dr.",
 "What is the wheelbase L?",
 "The distance between the two wheels, with dθ = (dr - dl)/L.",
 "Where does drift come from?",
 "Wheel radius error and slip make the integral drift, so IMU or visual fusion is needed to correct it.",
]

write('stereo-depth', build('stereo-depth', STD))
write('trajectory-time-linear', build('trajectory-time-linear', TTL))
write('wheel-odometry', build('wheel-odometry', WOD))

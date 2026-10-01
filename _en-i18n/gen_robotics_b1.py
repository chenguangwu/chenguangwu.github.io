#!/usr/bin/env python3
# gen_robotics_b1.py — robotics b1 (5 slugs): accel-distance/battery-runtime/belt-linear-speed/cable-tension-pulley/centripetal-speed-limit
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

ACD = [
 "Find the acceleration distance from the final speed and acceleration",
 "Enter the final speed v and the acceleration a to get the uniform acceleration distance.",
 "Uniform Acceleration Distance Calculator",
 "/ Uniform Acceleration Distance Calculator",
 "📖 View Guide: \"Find the acceleration distance from the final speed and acceleration\"",
 "d = v²/(2a) starting from rest.",
 "📚 Deep Dive: Uniform deceleration braking distance",
 "Safe stopping distance for mobile robots.",
 "Displacement for a given final speed and deceleration.",
 "Emergency stop design for obstacle avoidance.",
 "2 m/s decelerating at 1 m/s² to a stop",
 "d = v²/(2a) = 4/2 = 2 m; slowing uniformly from 2 m/s to rest takes 2 m of braking distance.",
 "Doubling the deceleration",
 "At a = 2, d = 4/4 = 1 m; the greater the deceleration, the shorter the stopping distance.",
 "What does the formula assume?",
 "Uniform deceleration down to zero speed, with the initial speed v and the deceleration a both constant.",
 "Is reaction time included?",
 "This covers only the braking phase; the total stopping distance must also add the reaction delay displacement v·t_react.",
]

BRT = [
 "Find the runtime from capacity and power draw",
 "Enter the battery capacity in Ah, the voltage V and the load power P to get the runtime.",
 "/ Battery Runtime Calculator",
 "📖 View Guide: \"Find the runtime from capacity and power draw\"",
 "t = capacity in Wh / power draw in W",
 "Capacity (Ah)",
 "📚 Deep Dive: Battery runtime",
 "Estimating the endurance of mobile robots.",
 "Capacity, voltage and",
 "power conversion",
 "Matching the power supply to the mission plan.",
 "12 V, 2 Ah supplying 24 W",
 "t = Ah·V/P = 2 x 12/24 = 1 h; a 24 Wh battery feeding a 24 W load lasts one hour.",
 "Load dropped to 12 W",
 "t = 24/12 = 2 h; halving the power draw doubles the runtime.",
 "Relation between Wh and Ah?",
 "Energy in Wh = Ah x V, and the runtime is Wh/P.",
 "Is the real value lower?",
 "Yes. Discharge rate, temperature and ageing all make the usable capacity fall below the nominal figure.",
]

BLS = [
 "Find the belt speed from the pulley diameter and rotation speed.",
 "Timing Belt Linear Speed Calculator",
 "/ Timing Belt Linear Speed",
 "Timing Belt Linear Speed",
 "📖 View Guide: \"Timing Belt Linear Speed Calculator\"",
 "Timing belt linear speed v = π x D x n / 60, where D is the pulley pitch diameter in metres and n the rotation speed in r/min; alternatively D = z x p / π from the tooth count z and the pitch p, which gives v = z x p x n / 60. It is used to check transmission ratios and validate timing belt selection.",
 "Pulley diameter D (m)",
 "📚 Deep Dive: Pulley linear speed",
 "Conveyor and timing belt speed.",
 "Conversion between wheel diameter and rotation speed.",
 "End effector feed speed.",
 "Diameter 60 mm at 300 rpm",
 "Doubling the diameter",
 "D = 0.12 gives v = 1.885 m/s; the linear speed is proportional to the diameter.",
 "Units",
 "Take D in metres and n in rpm to get m/s; you can also use v = πDn with n in rps.",
 "What about slip?",
 "A timing belt is essentially slip free, while a flat belt needs a slip factor applied.",
]

CTP = [
 "Find the single-side rope tension from the load",
 "Enter the lifted load F to get the single-side rope tension of an ideal fixed pulley.",
 "Ideal Pulley Rope Tension Calculator",
 "/ Ideal Pulley Rope Tension Calculator",
 "📖 View Guide: \"Find the single-side rope tension from the load\"",
 "Single-side rope tension T = mg/2",
 "Load F (N)",
 "For an ideal pulley T = F/2, shared equally by the two sides.",
 "📚 Deep Dive: Pulley rope tension",
 "Tension on both sides of a fixed pulley.",
 "Cable forces for suspended loads.",
 "Tension in counterweight systems.",
 "100 N load over a fixed pulley",
 "An ideal fixed pulley has no friction, so both sides carry T = F/2 = 50 N and together support the 100 N load.",
 "With friction",
 "With real friction the two sides differ and must be corrected for efficiency.",
 "Why 50 N on each side?",
 "In static equilibrium the two tensions are equal and sum to 100 N, so each is 50 N.",
 "What about a movable pulley?",
 "A movable pulley halves the effort, with the tension carrying load/2.",
]

CSL = [
 "The upper turning speed limit set by the maximum centripetal acceleration.",
 "Robot Turning Maximum Speed Calculator",
 "/ Turning Speed Limit",
 "Turning Speed Limit",
 "📖 View Guide: \"Robot Turning Maximum Speed Calculator\"",
 "Maximum acceleration a_max (m/s²)",
 "Turning radius R (m)",
 "📚 Deep Dive: Turning speed limit",
 "Maximum turning speed of a differential drive robot.",
 "A speed ceiling for a given",
 "centripetal acceleration limit.",
 "Speed that avoids rollover and skidding.",
 "Radius 1 m, a_max = 2 m/s²",
 "v = sqrt(a_max·R) = sqrt(2 x 1) = 1.41 m/s; beyond that the centripetal acceleration is exceeded.",
 "Halving the radius",
 "R = 0.5 gives v = 1.0 m/s; the limit falls with the",
 "square root",
 "of the radius.",
 "How is a_max chosen?",
 "It follows the skid limit of μg or the rollover threshold, commonly 1 to 3 m/s².",
 "Angular velocity",
 "Since v = ωR it can also be written as ω_max = sqrt(a_max/R).",
]

write('accel-distance', build('accel-distance', ACD))
write('battery-runtime', build('battery-runtime', BRT))
write('belt-linear-speed', build('belt-linear-speed', BLS))
write('cable-tension-pulley', build('cable-tension-pulley', CTP))
write('centripetal-speed-limit', build('centripetal-speed-limit', CSL))

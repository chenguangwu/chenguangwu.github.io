#!/usr/bin/env python3
# gen_robotics_b4.py — robotics b4 (5 slugs): joint-angular-velocity/lead-screw-speed/lifting-torque/linear-accel-force/motor-power
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

JAV = [
 "Find the joint angular velocity from the end linear speed and arm length",
 "Enter the end linear speed v and the arm length L to get the joint angular velocity.",
 "Joint Angular Velocity Calculator",
 "/ Joint Angular Velocity Calculator",
 "📖 View Guide: \"Find the joint angular velocity from the end linear speed and arm length\"",
 "End linear speed v (m/s)",
 "📚 Deep Dive: Joint angular velocity",
 "Convert the end linear speed into joint angular velocity.",
 "Motion of a single revolute joint.",
 "Speed planning.",
 "Linear speed 0.5 m/s, arm length 0.3 m",
 "Arm length 0.6 m",
 "ω = 0.83 rad/s; at the same linear speed a longer arm halves the angular velocity.",
 "When does it apply?",
 "For a single revolute joint whose end moves tangentially at speed v.",
 "Angular acceleration and",
 "tangential acceleration",
 "follow the same rule.",
]

LSS = [
 "Find the nut linear speed from the rotation speed and lead.",
 "Ball Screw Linear Speed Calculator",
 "/ Screw Linear Speed",
 "Screw Linear Speed",
 "📖 View Guide: \"Ball Screw Linear Speed Calculator\"",
 "Lead p (m/rev)",
 "📚 Deep Dive: Screw feed speed",
 "Speed of a linear module.",
 "Converting between lead and rotation speed.",
 "Z axis feed planning.",
 "Lead 5 mm at 300 rpm",
 "Lead 10 mm",
 "v = 50 mm/s; a larger lead feeds faster at the same rpm.",
 "What is the lead p?",
 "The advance per screw revolution in metres, with v = n·p/60 when n is in rpm.",
 "Accuracy versus lead?",
 "A large lead is faster but gives coarser resolution per step, so the two must be traded off.",
]

LFT = [
 "The holding torque a joint needs when lifting a load vertically.",
 "Load Handling Joint Torque Calculator",
 "/ Handling Joint Torque",
 "Handling Joint Torque",
 "📖 View Guide: \"Load Handling Joint Torque Calculator\"",
 "📚 Deep Dive: Lifting torque",
 "Hoisting or winching a load.",
 "Convert drum radius into torque.",
 "Lifting a",
 "2 kg load with a drum radius of 0.5 m",
 "Halving the radius",
 "r = 0.25 gives τ = 4.9 N·m; a smaller radius needs less torque.",
 "How does it differ from gravity compensation?",
 "This is the lifting torque about a drum, while gravity compensation holds an arm joint in a horizontal pose.",
 "What about accelerating the lift?",
 "You must also add the acceleration torque m·a·r.",
]

LAF = [
 "Find the driving force from mass and acceleration",
 "Enter the mass m and the acceleration a to get the driving force.",
 "Linear Motion Acceleration Force Calculator",
 "/ Linear Motion Acceleration Force Calculator",
 "📖 View Guide: \"Find the driving force from mass and acceleration\"",
 "📚 Deep Dive: Linear motion driving force",
 "The thrust required to",
 "accelerate, applying",
 "Newton's second law",
 ".",
 "Selecting motor thrust.",
 "10 kg accelerating at 2 m/s²",
 "Including friction",
 "Total thrust = 20 N plus the friction resistance, which must also cover ground and transmission losses.",
 "What force at constant speed?",
 "With no friction, a constant speed only has to overcome resistance, so F ≈ 0 apart from friction.",
 "On a slope?",
 "Add the m·g·sinα component.",
]

MTP = [
 "Find the mechanical power from torque and angular velocity",
 "Enter the torque τ and the angular velocity ω to get the mechanical power.",
 "Motor Power Calculator",
 "/ Motor Power Calculator",
 "📖 View Guide: \"Find the mechanical power from torque and angular velocity\"",
 "📚 Deep Dive: Motor mechanical power",
 "Torque times angular velocity gives the power.",
 "Motor and drive selection.",
 "Energy consumption estimates.",
 "Torque 2 N·m at 10 rad/s",
 "Angular velocity 20",
 "P = 40 W, and the power is proportional to the angular velocity.",
 "Units",
 "Use τ in N·m and ω in rad/s to get the result in W.",
 "Electrical power?",
 "The mechanical power",
 "divided by the efficiency gives the input",
 "electrical power.",
]

write('joint-angular-velocity', build('joint-angular-velocity', JAV))
write('lead-screw-speed', build('lead-screw-speed', LSS))
write('lifting-torque', build('lifting-torque', LFT))
write('linear-accel-force', build('linear-accel-force', LAF))
write('motor-power', build('motor-power', MTP))

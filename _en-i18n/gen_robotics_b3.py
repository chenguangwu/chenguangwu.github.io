#!/usr/bin/env python3
# gen_robotics_b3.py — robotics b3 (5 slugs): gear-ratio-speed/gear-ratio-torque/gravity-comp-torque/gripper-force/inverse-kinematics-2r
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

GRS = [
 "Find the output speed and linear speed from the input speed and reduction ratio.",
 "Gear Reduction Output Speed Calculator",
 "/ Reduction Ratio Output Speed",
 "Reduction Ratio Output Speed",
 "📖 View Guide: \"Gear Reduction Output Speed Calculator\"",
 "Input speed n_in (rpm)",
 "Output wheel radius R (m)",
 "📚 Deep Dive: Gear reduction output speed",
 "Output speed and linear speed of a gearbox.",
 "Transmission ratio conversion.",
 "Final stage speed of a wheeled chassis.",
 "Input 300 rpm, ratio 30, wheel radius 0.1 m",
 "Reduction ratio 60",
 "n_out = 5 rpm and the linear speed halves to 0.052 m/s, slower but with more force.",
 "Relation between speed and ratio?",
 "n_out = n_in/i with i > 1 for reduction, while the torque is multiplied by the ratio.",
 "Does efficiency affect speed?",
 "In theory there is no slip, so efficiency mainly affects the output torque rather than the speed.",
]

GRT = [
 "Find the output torque from the input torque and reduction ratio",
 "Enter the input torque τ_in, the reduction ratio GR and the efficiency η to get the output torque.",
 "Reduction Ratio Torque Multiplication Calculator",
 "/ Reduction Ratio Torque Multiplication Calculator",
 "📖 View Guide: \"Find the output torque from the input torque and reduction ratio\"",
 "Input torque τ_in (N·m)",
 "Reduction ratio GR",
 "📚 Deep Dive: Gear drive output torque",
 "Reduction for torque multiplication.",
 "Torque transfer including efficiency.",
 "Joint drive selection.",
 "Input 1 N·m, ratio 10, efficiency 0.9",
 "T_out = 1 x 10 x 0.9 = 9 N·m; a 10x reduction multiplies the torque and charges 10% loss.",
 "Efficiency 1.0",
 "T_out = 10 N·m, the ideal lossless case.",
 "Why does the torque grow?",
 "Reduction trades speed for torque, with T_out = T_in x i x η.",
 "Is work conserved?",
 "Ignoring losses the power is conserved: T_in·ω_in = T_out·ω_out.",
]

GCT = [
 "Find the gravity torque from link mass, length and angle",
 "Enter the mass m, arm length L, angle θ and g to get the joint gravity torque.",
 "Joint Gravity Compensation Torque Calculator",
 "/ Joint Gravity Compensation Torque Calculator",
 "📖 View Guide: \"Find the gravity torque from link mass, length and angle\"",
 "Angle θ (°)",
 "τ = m·g·L·cosθ, a maximum when the arm is horizontal.",
 "📚 Deep Dive: Gravity compensation torque",
 "Balancing gravity on a horizontal arm.",
 "Estimating joint torque.",
 "Design of balancing springs and counterweights.",
 "5 kg, arm length 0.3 m, horizontal",
 "τ = m·g·L·cosθ = 5 x 9.81 x 0.3 x 1 = 14.7 N·m, the maximum at θ = 0 when horizontal.",
 "Arm raised 90°",
 "cos 90° = 0, so the gravity torque vanishes and no compensation is needed.",
 "What angle is θ?",
 "The angle between the arm and the horizontal; the gravity torque peaks at θ = 0, the horizontal pose.",
 "What about multiple links?",
 "Sum the gravity torque of each link, adding up the normal distance of each centre of mass.",
]

GRF = [
 "Estimate the total two-finger grip force from the drive torque and lever arm.",
 "Gripper Clamping Force Calculator",
 "/ Gripper Clamping Force",
 "Gripper Clamping Force",
 "📖 View Guide: \"Gripper Clamping Force Calculator\"",
 "Drive torque τ (N·m)",
 "Lever arm L (m)",
 "F = 2τ/L for two fingers.",
 "📚 Deep Dive: Gripper clamping force",
 "Turning joint torque into clamping force.",
 "Assessing grip reliability.",
 "Setting up a force controlled gripper.",
 "Torque 5 N·m, lever arm 5 cm",
 "F = 2τ/L = 2 x 5/0.05 = 200 N; the two sides together supply 200 N of normal force.",
 "Doubling the lever arm",
 "L = 0.1 gives F = 100 N; a longer lever arm means a smaller clamping force.",
 "Why 2τ?",
 "A symmetric two-sided gripper produces a normal force from the torque on each side, giving a total of 2τ/L.",
 "Will the grip hold without slipping?",
 "It needs F·μ to be at least the workpiece weight plus disturbances, where μ is the friction coefficient.",
]

IK2 = [
 "Solve the joint angles θ₁ and θ₂ back from (x, y)",
 "Inverse solution for a planar two-link arm, including a reachability check.",
 "Two-Link Inverse Kinematics Calculator",
 "/ Two-Link Inverse Kinematics",
 "Two-Link Inverse Kinematics",
 "📖 View Guide: \"Solve the joint angles θ₁ and θ₂ back from (x, y)\"",
 "Target x (m)",
 "Target y (m)",
 "It is solvable only when |L₁ - L₂| ≤ sqrt(x² + y²) ≤ L₁ + L₂.",
 "📚 Deep Dive: Two-link inverse kinematics",
 "Find the joint angles from a known end position.",
 "Point reachability in the plane.",
 "Inverse solution along a trajectory.",
 "Target (1.3, 1.2) with each link 1 m",
 "r² = 1.3² + 1.2² = 3.13; cos θ2 = (3.13 - 2)/(2 x 1 x 1) = 0.565, so θ2 ≈ 55.6°, solvable and inside the workspace.",
 "Beyond r_max",
 "If r > 2 m there is no solution and the target must be replanned.",
 "This means the target lies outside the reachable radius and no inverse solution exists.",
 "How many solutions?",
 "A planar two-link arm usually has elbow-up and elbow-down solutions; choose according to the constraints.",
]

write('gear-ratio-speed', build('gear-ratio-speed', GRS))
write('gear-ratio-torque', build('gear-ratio-torque', GRT))
write('gravity-comp-torque', build('gravity-comp-torque', GCT))
write('gripper-force', build('gripper-force', GRF))
write('inverse-kinematics-2r', build('inverse-kinematics-2r', IK2))

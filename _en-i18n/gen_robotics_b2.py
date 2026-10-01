#!/usr/bin/env python3
# gen_robotics_b2.py — robotics b2 (5 slugs): dc-motor-back-emf/diff-drive-velocity/encoder-angle-resolution/end-effector-reach/forward-kinematics-2r
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

DBE = [
 "Find the back EMF from the back EMF constant and angular velocity",
 "Enter the back EMF constant k_e and the angular velocity ω to get the back EMF.",
 "DC Motor Back EMF Calculator",
 "/ DC Motor Back EMF Calculator",
 "📖 View Guide: \"Find the back EMF from the back EMF constant and angular velocity\"",
 "Back EMF constant k_e (V·s/rad)",
 "📚 Deep Dive: DC motor back EMF",
 "Infer the voltage from the motor speed.",
 "Applying the back EMF constant.",
 "Estimating the no-load speed.",
 "Constant 0.05 at 100 rad/s",
 "E = k_e·ω = 0.05 x 100 = 5 V; the higher the speed the larger the back EMF, which limits the current.",
 "Speed 200",
 "E = 10 V; as the back EMF approaches the supply voltage the current tends to zero.",
 "What does the back EMF do?",
 "It opposes the supply, so a rising E lowers the armature current I = (U - E)/R and naturally limits the speed.",
 "What is the unit of k_e?",
 "V·s/rad, or V/rpm which needs converting; it is set by the motor design.",
]

DDV = [
 "Find the robot linear and angular velocity from the left and right wheel speeds.",
 "Differential Drive Linear and Angular Velocity Calculator",
 "/ Differential Drive Velocity",
 "Differential Drive Velocity",
 "📖 View Guide: \"Differential Drive Linear and Angular Velocity Calculator\"",
 "Left wheel speed v_l (m/s)",
 "Right wheel speed v_r (m/s)",
 "Unequal wheel speeds produce turning.",
 "📚 Deep Dive: Differential drive linear and angular velocity",
 "Kinematics of a two-wheel differential chassis.",
 "Get the rate of pose change from the left and right wheel speeds.",
 "The basis of odometry.",
 "Left 0.5, right 1.0 m/s, wheelbase 0.4 m",
 "Equal speeds, straight line",
 "With vl = vr the angular velocity ω is zero and the motion is pure translation; opposite speeds rotate the robot on the spot.",
 "What is the wheelbase L?",
 "The distance between the two driven wheels, with ω = (vr - vl)/L.",
 "Relation to odometry?",
 "Displacement ds = (vl + vr)/2 · dt and rotation dθ = (vr - vl)/L · dt.",
]

EAR = [
 "Find the minimum angular resolution from the pulses per revolution",
 "Enter the pulses per revolution CPR, after quadrature decoding, to get the minimum angular resolution.",
 "Encoder Angular Resolution Calculator",
 "/ Encoder Angular Resolution Calculator",
 "📖 View Guide: \"Find the minimum angular resolution from the pulses per revolution\"",
 "Pulses per revolution CPR (PPR)",
 "After quadrature decoding the resolution is 360°/(4·CPR).",
 "📚 Deep Dive: Encoder angular resolution",
 "Angle subdivision with quadrature encoding.",
 "Converting between CPR and resolution.",
 "Assessing position control accuracy.",
 "θ = 360/(4 x CPR) = 360/4000 = 0.09°; quadrature decoding gives 4000 counts per revolution.",
 "θ = 360/16000 = 0.0225°, and the resolution improves as CPR rises.",
 "Why divide by 4?",
 "The two quadrature channels A and B are counted on every edge, giving four times the resolution.",
 "How does it differ from the step angle?",
 "The encoder gives the feedback resolution while stepping gives the open-loop step angle; the two are different things.",
]

EER = [
 "The annular workspace that a planar two-link arm can reach.",
 "Two-Link Workspace Calculator",
 "/ Workspace Reach Radius",
 "Workspace Reach Radius",
 "📖 View Guide: \"Two-Link Workspace Calculator\"",
 "The reachable radius lies between |L₁ - L₂| and L₁ + L₂.",
 "📚 Deep Dive: Reachable workspace of a robot arm",
 "Reachable radius range of a two-link arm.",
 "First check on whether a target point is reachable.",
 "Workspace planning.",
 "Link lengths 1 m and 0.8 m",
 "r_min = |1 - 0.8| = 0.2 m and r_max = 1 + 0.8 = 1.8 m; the end effector reaches an annulus from 0.2 to 1.8 m from the base.",
 "Equal lengths of 1 m",
 "r_min = 0, since the arm can fold onto the base, and r_max = 2 m.",
 "Is the radius alone enough?",
 "A planar two-link arm gives an annulus; with joint limits or in three dimensions the space becomes more complex.",
 "Singularities?",
 "Near full extension at r_max or folding at r_min the Jacobian degenerates, so those poses should be avoided.",
 "How to use the Two-Link Workspace Calculator",
 "What is the Two-Link Workspace Calculator for?",
 "The Two-Link Workspace Calculator takes the two link lengths and returns the inner and outer radius of the annular workspace reachable by a planar two-link arm, helping with arm layout and reach analysis.",
 "How do I use the Two-Link Workspace Calculator?",
 "Which scenarios suit the Two-Link Workspace Calculator?",
 "Workspace",
 "The reachable region of a two-link arm is an annulus centred on the base with radius between |L1 - L2| and L1 + L2, including its interior; the link lengths and joint angles determine reachability and blind spots.",
 "Use it to judge whether the arm can touch a target point and to plan trajectories clear of singularities and self-collision.",
 "This model is an ideal planar linkage; real arms have joint limits, singular configurations and 3D geometry, so the result is a geometric reference.",
]

FK2 = [
 "Find the end effector coordinates from the joint angles.",
 "Two-Link Forward Kinematics Calculator",
 "/ Two-Link Forward Kinematics",
 "Two-Link Forward Kinematics",
 "📖 View Guide: \"Two-Link Forward Kinematics Calculator\"",
 "Joint angle θ₁ (°)",
 "Joint angle θ₂ (°)",
 "θ₁ = 30° and θ₂ = 45° with L = 1 give about (1.297, 1.207).",
 "📚 Deep Dive: Two-link forward kinematics",
 "Find the end coordinates from known joint angles.",
 "A planar 2R arm.",
 "Computing trajectory points.",
 "θ1 = 30°, θ2 = 45°, each link 1 m",
 "Full extension",
 "θ1 = θ2 = 0 puts the end at (2,0), exactly r_max.",
 "Is θ2 a relative angle?",
 "Yes, it is the angle of the second link relative to the first, so the absolute angle is θ1 + θ2.",
 "Is there a unique solution?",
 "Forward kinematics is single valued, while inverse kinematics can have several solutions or none at all.",
]

write('dc-motor-back-emf', build('dc-motor-back-emf', DBE))
write('diff-drive-velocity', build('diff-drive-velocity', DDV))
write('encoder-angle-resolution', build('encoder-angle-resolution', EAR))
write('end-effector-reach', build('end-effector-reach', EER))
write('forward-kinematics-2r', build('forward-kinematics-2r', FK2))

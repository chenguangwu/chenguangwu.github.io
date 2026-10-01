#!/usr/bin/env python3
# gen_robotics_b5.py — robotics b5 (5 slugs): motor-torque-current/pid-controller/rotational-inertia-torque/servo-pwm-angle/stepper-step-angle
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

MTC = [
 "The torque of a DC motor is proportional to the current.",
 "Motor Torque Current Calculator",
 "/ Motor Torque Current",
 "Motor Torque Current",
 "📖 View Guide: \"Motor Torque Current Calculator\"",
 "Torque constant Kt (N·m/A)",
 "📚 Deep Dive: Motor torque and current",
 "Estimate the output torque from the current.",
 "Applying the torque constant.",
 "Current loop setting.",
 "Constant 0.05 N·m/A at a current of 10 A",
 "Current 20 A",
 "T = 1.0 N·m, and the torque is proportional to the current.",
 "k_t versus the back EMF constant?",
 "For an ideal motor k_t = k_e once the units match, and both are proportional to the magnetic flux.",
 "Stall?",
 "At stall both the current and the torque peak, but the motor overheats easily, so current limiting is needed.",
]

PID = [
 "Output of the proportional-integral-derivative control law.",
 "PID Controller Output Calculator",
 "/ PID Controller Output",
 "PID Controller Output",
 "📖 View Guide: \"PID Controller Output Calculator\"",
 "Proportional Kp",
 "Integral Ki",
 "Derivative Kd",
 "Error integral ∫e",
 "Previous error eₚ",
 "Sampling time dt (s)",
 "The integral term removes the steady state error.",
 "📚 Deep Dive: PID controller output",
 "Computing the closed loop control output.",
 "Combining the P, I and D terms.",
 "Verifying the parameter tuning.",
 "P control only",
 "With ki = kd = 0 the output is u = 2 and a steady state offset remains; adding I removes it and D damps the overshoot.",
 "What is ei?",
 "It is the accumulated error integral, while ep is the previous sample error used for the D term difference (e - ep)/dt.",
 "Integral windup?",
 "A large error integrated over a long time saturates easily, so anti-windup clamping is needed.",
]

RIT = [
 "Find the required torque from the moment of inertia and angular acceleration",
 "Enter the moment of inertia I and the angular acceleration α to get the required torque.",
 "Moment of Inertia Acceleration Torque Calculator",
 "/ Moment of Inertia Acceleration Torque Calculator",
 "📖 View Guide: \"Find the required torque from the moment of inertia and angular acceleration\"",
 "📚 Deep Dive: Torque required by moment of inertia",
 "Torque for rotational acceleration.",
 "Assessing joint inertia.",
 "Acceleration and deceleration planning.",
 "Inertia 0.5 kg·m² and",
 "angular acceleration",
 "Doubling the inertia",
 "I = 1 gives τ = 4 N·m; the same angular acceleration then needs more torque.",
 "Linear analogy?",
 "τ = Iα mirrors F = ma, with I the moment of inertia and α the angular acceleration.",
 "Does it include gravity?",
 "This covers only the acceleration term; a horizontal arm also needs the gravity torque added on.",
]

SPA = [
 "Angle = (pulse width - minimum) / (maximum - minimum) x 180°",
 "Find the servo angle from the PWM pulse width.",
 "Servo PWM Angle Calculator",
 "/ Servo PWM Angle",
 "Servo PWM Angle",
 "📖 View Guide: \"Angle = (pulse width - minimum) / (maximum - minimum) x 180°\"",
 "Angle = (pulse width - minimum)/(maximum - minimum) x 180°",
 "Pulse width (µs)",
 "Minimum pulse width (µs)",
 "Maximum pulse width (µs)",
 "1500 µs over a 500 to 2500 range gives 90°.",
 "Common servos use 1000 to 2000 µs.",
 "📚 Deep Dive: Servo PWM angle",
 "Map the servo pulse width to an angle.",
 "Controlling a 50 Hz servo.",
 "Setting a joint angle.",
 "Pulse width 1500 μs, range 500 to 2500",
 "θ = (1500 - 500)/(2500 - 500) x 180 = 1000/2000 x 180 = 90°, the centre position.",
 "Pulse width 2000 μs",
 "θ = (2000 - 500)/2000 x 180 = 135°, growing linearly with the pulse width.",
 "Standard pulse widths?",
 "Typically 500 μs means 0°, 1500 μs means 90° and 2500 μs means 180° at 50 Hz.",
 "Different ranges?",
 "Change pmin and pmax to suit 180° or 270° servos.",
]

SSA = [
 "Find the step angle from the steps per revolution",
 "Enter the steps per revolution N to get the step angle.",
 "Stepper Motor Step Angle Calculator",
 "/ Stepper Motor Step Angle Calculator",
 "📖 View Guide: \"Find the step angle from the steps per revolution\"",
 "Step angle = 360°/(steps per revolution)",
 "Steps per revolution N (steps/rev)",
 "N = 200 gives 1.8°, a common value.",
 "📚 Deep Dive: Stepper motor step angle",
 "The rotation angle of each step.",
 "Converting steps per revolution.",
 "Open loop positioning accuracy.",
 "200 steps per revolution",
 "θ = 360/200 = 1.8°; a revolution takes 200 full steps and microstepping can reduce the angle further.",
 "400 steps per revolution",
 "θ = 0.9°; halving the step angle gives higher accuracy.",
 "What is microstepping for?",
 "The driver subdivides each full step, by 1/16 for example, giving a smaller equivalent step at slightly lower torque.",
 "Lost steps?",
 "With no feedback in open loop, overload or high speed causes lost steps, so leave a margin or add an encoder.",
]

write('motor-torque-current', build('motor-torque-current', MTC))
write('pid-controller', build('pid-controller', PID))
write('rotational-inertia-torque', build('rotational-inertia-torque', RIT))
write('servo-pwm-angle', build('servo-pwm-angle', SPA))
write('stepper-step-angle', build('stepper-step-angle', SSA))
